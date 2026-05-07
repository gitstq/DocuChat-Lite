#!/usr/bin/env python3
"""
DocuChat-Lite - Lightweight RAG Document Chat Engine
轻量级文档智能问答引擎 - 零依赖核心设计
"""

import os
import sys
import json
import hashlib
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

__version__ = "1.0.0"
__author__ = "gitstq"

@dataclass
class Document:
    """Document model"""
    content: str
    metadata: Dict = field(default_factory=dict)
    chunk_id: str = ""
    
    def __post_init__(self):
        if not self.chunk_id:
            self.chunk_id = hashlib.md5(self.content.encode()).hexdigest()[:12]

@dataclass  
class Chunk:
    """Text chunk for embedding"""
    text: str
    metadata: Dict
    chunk_id: str
    
class SimpleVectorStore:
    """Zero-dependency vector store using keyword matching"""
    
    def __init__(self):
        self.chunks: List[Chunk] = []
        self.vocabulary: Dict[str, List[int]] = {}
    
    def add_chunk(self, chunk: Chunk):
        self.chunks.append(chunk)
        words = self._tokenize(chunk.text)
        for word in words:
            if word not in self.vocabulary:
                self.vocabulary[word] = []
            self.vocabulary[word].append(len(self.chunks) - 1)
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple Chinese/English tokenization"""
        text = text.lower()
        chinese_chars = re.findall(r'[\u4e00-\u9fff]+', text)
        english_words = re.findall(r'[a-z0-9]+', text)
        return chinese_chars + english_words
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Chunk, float]]:
        """Search using keyword frequency scoring"""
        query_words = set(self._tokenize(query))
        scores = {}
        
        for chunk_idx, chunk in enumerate(self.chunks):
            chunk_words = set(self._tokenize(chunk.text))
            intersection = query_words & chunk_words
            if intersection:
                scores[chunk_idx] = len(intersection) / len(query_words)
        
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [(self.chunks[idx], score) for idx, score in sorted_results[:top_k]]

class DocuChat:
    """Main document chat engine"""
    
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    
    def __init__(self, model_name: str = "default"):
        self.vector_store = SimpleVectorStore()
        self.model_name = model_name
        self.conversation_history: List[Dict] = []
        self._load_default_prompts()
    
    def _load_default_prompts(self):
        """Load default system prompts"""
        self.system_prompt = """You are a helpful AI assistant answering questions about documents.
Focus on providing accurate answers based on the given context. If the information is not in the context, say so."""
        
        self.qa_prompt = """Based on the following context, answer the question:

Context:
{context}

Question: {question}

Answer:"""
    
    def _chunk_text(self, text: str, metadata: Dict) -> List[Chunk]:
        """Split text into overlapping chunks"""
        chunks = []
        sentences = re.split(r'[。！？\n]', text)
        
        current = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if len(current) + len(sentence) <= self.CHUNK_SIZE:
                current += sentence + "。"
            else:
                if current:
                    chunks.append(Chunk(
                        text=current,
                        metadata=metadata.copy(),
                        chunk_id=hashlib.md5(current.encode()).hexdigest()[:12]
                    ))
                current = sentence + "。"
        
        if current:
            chunks.append(Chunk(
                text=current,
                metadata=metadata.copy(),
                chunk_id=hashlib.md5(current.encode()).hexdigest()[:12]
            ))
        
        return chunks
    
    def ingest_documents(self, documents: List[Document]) -> Dict:
        """Ingest documents into the knowledge base"""
        total_chunks = 0
        for doc in documents:
            chunks = self._chunk_text(doc.content, doc.metadata)
            for chunk in chunks:
                self.vector_store.add_chunk(chunk)
                total_chunks += 1
        
        return {
            "documents": len(documents),
            "chunks": total_chunks,
            "status": "success"
        }
    
    def ingest_folder(self, folder_path: str, extensions: List[str] = None) -> Dict:
        """Ingest all documents from a folder"""
        if extensions is None:
            extensions = ['.txt', '.md', '.pdf', '.docx']
        
        path = Path(folder_path)
        documents = []
        
        for ext in extensions:
            for file_path in path.glob(f"*{ext}"):
                try:
                    content = self._read_file(file_path)
                    documents.append(Document(
                        content=content,
                        metadata={
                            "source": str(file_path),
                            "filename": file_path.name,
                            "type": ext[1:]
                        }
                    ))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
        
        return self.ingest_documents(documents)
    
    def _read_file(self, file_path: Path) -> str:
        """Read file content"""
        if file_path.suffix == '.md':
            return file_path.read_text(encoding='utf-8')
        elif file_path.suffix == '.txt':
            return file_path.read_text(encoding='utf-8')
        else:
            return file_path.read_text(encoding='utf-8', errors='ignore')
    
    def query(self, question: str, top_k: int = 5, use_history: bool = True) -> Dict:
        """Query the document knowledge base"""
        results = self.vector_store.search(question, top_k)
        
        if not results:
            return {
                "answer": "抱歉，知识库中没有找到与您问题相关的信息。",
                "sources": [],
                "confidence": 0.0
            }
        
        context = "\n\n".join([f"[来源 {i+1}] {chunk.text}" for i, (chunk, score) in enumerate(results)])
        
        prompt = self.qa_prompt.format(context=context, question=question)
        
        self.conversation_history.append({
            "role": "user",
            "content": question,
            "timestamp": datetime.now().isoformat()
        })
        
        answer = self._generate_response(prompt, use_history)
        
        self.conversation_history.append({
            "role": "assistant",
            "content": answer,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "answer": answer,
            "sources": [
                {
                    "text": chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text,
                    "metadata": chunk.metadata,
                    "relevance": score
                }
                for chunk, score in results
            ],
            "confidence": results[0][1] if results else 0.0
        }
    
    def _generate_response(self, prompt: str, use_history: bool) -> str:
        """Generate response using available LLM backends"""
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if api_key:
            return self._call_openai(prompt, api_key)
        
        ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
        ollama_model = os.environ.get("OLLAMA_MODEL", "llama2")
        
        if self._check_ollama(ollama_url):
            return self._call_ollama(prompt, ollama_url, ollama_model)
        
        return self._fallback_response(prompt)
    
    def _call_openai(self, prompt: str, api_key: str) -> str:
        """Call OpenAI API"""
        try:
            import urllib.request
            import urllib.error
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions",
                data=json.dumps(data).encode('utf-8'),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content']
        except Exception as e:
            return f"OpenAI API调用失败: {str(e)}\n\n请确保OPENAI_API_KEY环境变量已设置。"
    
    def _check_ollama(self, url: str) -> bool:
        """Check if Ollama is available"""
        try:
            import urllib.request
            req = urllib.request.Request(f"{url}/api/tags")
            urllib.request.urlopen(req, timeout=2)
            return True
        except:
            return False
    
    def _call_ollama(self, prompt: str, url: str, model: str) -> str:
        """Call Ollama API"""
        try:
            import urllib.request
            import urllib.error
            
            data = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            req = urllib.request.Request(
                f"{url}/api/generate",
                data=json.dumps(data).encode('utf-8'),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('response', 'Ollama响应为空')
        except Exception as e:
            return f"Ollama调用失败: {str(e)}"
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when no LLM is available"""
        return """⚠️ 未检测到可用的LLM后端。

请选择以下任一方式配置：

1️⃣ OpenAI API:
   export OPENAI_API_KEY=your_api_key

2️⃣ Ollama (本地部署):
   export OLLAMA_URL=http://localhost:11434
   export OLLAMA_MODEL=llama2

📚 示例问题:
- 文档的主要内容是什么？
- 请总结关键要点
- 提取重要信息"""

    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        return {
            "total_chunks": len(self.vector_store.chunks),
            "vocabulary_size": len(self.vector_store.vocabulary),
            "conversation_turns": len(self.conversation_history) // 2,
            "model": self.model_name
        }
    
    def clear(self):
        """Clear all data"""
        self.vector_store = SimpleVectorStore()
        self.conversation_history = []


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🧠 DocuChat-Lite - 轻量级文档智能问答引擎"
    )
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    ingest_parser = subparsers.add_parser("ingest", help="📂 导入文档")
    ingest_parser.add_argument("path", help="文档或文件夹路径")
    ingest_parser.add_argument("--extensions", nargs="+", default=['.txt', '.md'], help="文件扩展名")
    
    query_parser = subparsers.add_parser("query", help="❓ 问答")
    query_parser.add_argument("question", help="问题")
    query_parser.add_argument("--top-k", type=int, default=5, help="返回结果数量")
    
    subparsers.add_parser("stats", help="📊 统计信息")
    subparsers.add_parser("clear", help="🗑️ 清除数据")
    
    args = parser.parse_args()
    
    chat = DocuChat()
    
    if args.command == "ingest":
        path = Path(args.path)
        if path.is_dir():
            result = chat.ingest_folder(str(path), args.extensions)
        else:
            content = path.read_text(encoding='utf-8')
            doc = Document(content=content, metadata={"source": str(path)})
            result = chat.ingest_documents([doc])
        print(f"✅ 导入完成: {result['documents']} 文档, {result['chunks']} 文本块")
    
    elif args.command == "query":
        result = chat.query(args.question, args.top_k)
        print(f"\n🤖 回答:\n{result['answer']}")
        print(f"\n📚 参考来源 (置信度: {result['confidence']:.2f}):")
        for i, source in enumerate(result['sources'], 1):
            print(f"   [{i}] {source['text'][:100]}...")
    
    elif args.command == "stats":
        stats = chat.get_stats()
        print(f"📊 知识库统计:")
        print(f"   文本块数: {stats['total_chunks']}")
        print(f"   词汇量: {stats['vocabulary_size']}")
        print(f"   对话轮次: {stats['conversation_turns']}")
    
    elif args.command == "clear":
        chat.clear()
        print("✅ 数据已清除")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

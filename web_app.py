#!/usr/bin/env python3
"""
Web UI for DocuChat-Lite
使用Flask提供Web界面
"""

import os
import json
from flask import Flask, request, jsonify, render_template_string
from docuchat import DocuChat, Document

app = Flask(__name__)
chat_engine = DocuChat()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 DocuChat-Lite - 文档智能问答</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 900px; margin: 0 auto; }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.9; }
        .card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .upload-zone {
            border: 2px dashed #667eea;
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        .upload-zone:hover { border-color: #764ba2; background: #f8f9ff; }
        .upload-zone input { display: none; }
        .upload-icon { font-size: 48px; margin-bottom: 10px; }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: transform 0.2s;
        }
        .btn:hover { transform: scale(1.05); }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .chat-container { height: 400px; overflow-y: auto; padding: 20px; background: #f8f9ff; border-radius: 12px; margin-bottom: 16px; }
        .message { margin-bottom: 16px; padding: 12px 16px; border-radius: 12px; max-width: 85%; }
        .message.user { background: #667eea; color: white; margin-left: auto; }
        .message.assistant { background: white; border: 1px solid #e0e0e0; }
        .sources { margin-top: 16px; padding: 12px; background: #f0f0f0; border-radius: 8px; font-size: 14px; }
        .input-group { display: flex; gap: 12px; }
        .input-group input {
            flex: 1; padding: 14px; border: 2px solid #e0e0e0; border-radius: 8px;
            font-size: 16px; outline: none;
        }
        .input-group input:focus { border-color: #667eea; }
        .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 16px; }
        .stat { text-align: center; padding: 12px; background: #f8f9ff; border-radius: 8px; }
        .stat-value { font-size: 24px; font-weight: bold; color: #667eea; }
        .stat-label { font-size: 12px; color: #666; }
        .file-list { margin-top: 12px; }
        .file-item { padding: 8px 12px; background: #e8e8ff; border-radius: 6px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
        .lang-switch { display: flex; gap: 8px; margin-bottom: 20px; }
        .lang-btn { padding: 6px 12px; border: none; background: rgba(255,255,255,0.2); color: white; border-radius: 20px; cursor: pointer; }
        .lang-btn.active { background: white; color: #667eea; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 DocuChat-Lite</h1>
            <p>轻量级文档智能问答引擎 | Zero-Dependency RAG Engine</p>
        </div>
        
        <div class="card">
            <div class="upload-zone" onclick="document.getElementById('fileInput').click()">
                <div class="upload-icon">📄</div>
                <p>点击或拖拽文件到此处上传</p>
                <p style="font-size: 12px; color: #999; margin-top: 8px;">支持 .txt, .md 文件</p>
                <input type="file" id="fileInput" accept=".txt,.md" multiple>
            </div>
            <div class="file-list" id="fileList"></div>
            <button class="btn" style="margin-top: 16px; width: 100%;" onclick="ingestDocs()">
                📚 开始导入文档
            </button>
        </div>
        
        <div class="card">
            <div class="stats" id="stats">
                <div class="stat"><div class="stat-value" id="chunkCount">0</div><div class="stat-label">文本块</div></div>
                <div class="stat"><div class="stat-value" id="vocabSize">0</div><div class="stat-label">词汇量</div></div>
                <div class="stat"><div class="stat-value" id="convTurns">0</div><div class="stat-label">对话轮次</div></div>
                <div class="stat"><div class="stat-value" id="status">就绪</div><div class="stat-label">状态</div></div>
            </div>
        </div>
        
        <div class="card">
            <div class="chat-container" id="chatContainer">
                <div class="message assistant">
                    👋 你好！我是 DocuChat-Lite。<br><br>
                    请先上传文档，然后就可以问我关于文档内容的问题了！
                </div>
            </div>
            <div class="input-group">
                <input type="text" id="questionInput" placeholder="输入您的问题..." onkeypress="if(event.key==='Enter')askQuestion()">
                <button class="btn" onclick="askQuestion()">🔍 提问</button>
            </div>
        </div>
    </div>
    
    <script>
        let uploadedFiles = [];
        
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const files = Array.from(e.target.files);
            files.forEach(file => {
                if (!uploadedFiles.find(f => f.name === file.name)) {
                    uploadedFiles.push(file);
                }
            });
            updateFileList();
        });
        
        function updateFileList() {
            const list = document.getElementById('fileList');
            list.innerHTML = uploadedFiles.map((f, i) => 
                '<div class="file-item">' +
                '<span>📄 ' + f.name + '</span>' +
                '<button onclick="removeFile(' + i + ')" style="background:none;border:none;cursor:pointer;">❌</button>' +
                '</div>'
            ).join('');
        }
        
        function removeFile(index) {
            uploadedFiles.splice(index, 1);
            updateFileList();
        }
        
        async function ingestDocs() {
            if (uploadedFiles.length === 0) {
                alert('请先选择文件');
                return;
            }
            
            const formData = new FormData();
            uploadedFiles.forEach(file => formData.append('files', file));
            
            document.getElementById('status').textContent = '导入中...';
            
            const response = await fetch('/ingest', { method: 'POST', body: formData });
            const result = await response.json();
            
            if (result.status === 'success') {
                document.getElementById('status').textContent = '就绪';
                updateStats();
                addMessage('assistant', '✅ 已成功导入 ' + result.documents + ' 个文档，共 ' + result.chunks + ' 个文本块。现在可以开始提问了！');
            }
        }
        
        async function askQuestion() {
            const input = document.getElementById('questionInput');
            const question = input.value.trim();
            if (!question) return;
            
            addMessage('user', question);
            input.value = '';
            
            const response = await fetch('/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question, top_k: 3 })
            });
            const result = await response.json();
            
            let responseText = result.answer;
            if (result.sources && result.sources.length > 0) {
                responseText += '<div class="sources"><strong>📚 参考来源:</strong><br>';
                result.sources.forEach((s, i) => {
                    responseText += (i+1) + '. ' + s.text.substring(0, 100) + '...<br>';
                });
                responseText += '</div>';
            }
            addMessage('assistant', responseText);
            updateStats();
        }
        
        function addMessage(role, content) {
            const container = document.getElementById('chatContainer');
            const div = document.createElement('div');
            div.className = 'message ' + role;
            div.innerHTML = content;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }
        
        async function updateStats() {
            const response = await fetch('/stats');
            const stats = await response.json();
            document.getElementById('chunkCount').textContent = stats.total_chunks;
            document.getElementById('vocabSize').textContent = stats.vocabulary_size;
            document.getElementById('convTurns').textContent = stats.conversation_turns;
        }
        
        updateStats();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ingest', methods=['POST'])
def ingest():
    files = request.files.getlist('files')
    documents = []
    for f in files:
        content = f.read().decode('utf-8', errors='ignore')
        documents.append(Document(
            content=content,
            metadata={"filename": f.filename}
        ))
    
    if documents:
        result = chat_engine.ingest_documents(documents)
    else:
        result = {"documents": 0, "chunks": 0, "status": "no_files"}
    
    return jsonify(result)

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    result = chat_engine.query(data.get('question', ''), data.get('top_k', 5))
    return jsonify(result)

@app.route('/stats')
def stats():
    return jsonify(chat_engine.get_stats())

@app.route('/clear', methods=['POST'])
def clear():
    chat_engine.clear()
    return jsonify({"status": "cleared"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

# 🧠 DocuChat-Lite

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/gitstq/DocuChat-Lite?style=flat)
![Forks](https://img.shields.io/github/forks/gitstq/DocuChat-Lite?style=flat)

**Zero-Dependency RAG Document Chat Engine** | **Lightweight AI-Powered Document Q&A System**

[English](README_en.md) | [简体中文](README.md) | [繁體中文](README_zh_TW.md) | [日本語](README_ja.md)

</div>

---

## 🎉 Introduction

DocuChat-Lite is a lightweight document intelligent Q&A engine based on RAG (Retrieval-Augmented Generation) technology. It helps you quickly get the information you need from large volumes of documents, supports multiple LLM backends, and requires zero external dependencies!

### 🌟 Highlights

- 🔥 **Zero-Dependency Core**: No third-party libraries required, pure Python implementation
- 🚀 **Lightning Deployment**: Download and run immediately, no complex configuration
- 🤖 **Multi-Backend Support**: OpenAI, Ollama, local models - switch freely
- 🌐 **Dual Interfaces**: Command line + Web interface for different scenarios
- 📊 **Real-time Statistics**: Knowledge base status at a glance

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🧠 **Intelligent Q&A** | Natural language Q&A based on document content with context understanding |
| 📄 **Multi-Format Support** | Supports TXT, Markdown and other common text formats |
| 🔍 **Semantic Search** | Keyword + semantic similarity dual retrieval |
| 🤖 **Multi-LLM Backend** | OpenAI API / Ollama local deployment / Compatible interfaces |
| 🌐 **Web Interface** | User-friendly browser interface, drag-and-drop upload |
| 📊 **Statistics** | Real-time display of knowledge base scale and retrieval efficiency |
| 💾 **Session Management** | Multi-turn dialogue with context memory |
| 🎯 **Source Tracking** | Clear source attribution for answers |

---

## 🚀 Quick Start

### 📋 Requirements

- Python 3.8 or higher
- (Optional) OpenAI API Key or Ollama local service

### ⚡ Installation

```bash
# Clone the project
git clone https://github.com/gitstq/DocuChat-Lite.git
cd DocuChat-Lite

# Run directly (zero dependencies)
python docuchat.py --help
```

### 🎮 CLI Mode

```bash
# Ingest documents
python docuchat.py ingest ./samples

# Ask questions
python docuchat.py query "What is the main content of the document?"

# View statistics
python docuchat.py stats

# Clear data
python docuchat.py clear
```

### 🌐 Web Interface Mode

```bash
# Install Flask (if you need web interface)
pip install flask

# Start service
python web_app.py

# Open in browser
open http://localhost:5000
```

---

## 📖 Detailed Usage Guide

### 🔧 Environment Configuration

#### OpenAI API Configuration

```bash
export OPENAI_API_KEY=sk-your-api-key-here
```

#### Ollama Local Deployment Configuration

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama2

# Start service
ollama serve

# Configure environment variables
export OLLAMA_URL=http://localhost:11434
export OLLAMA_MODEL=llama2
```

### 💻 Programming Interface

```python
from docuchat import DocuChat, Document

# Initialize engine
chat = DocuChat()

# Import document
doc = Document(
    content="Your document content...",
    metadata={"source": "example.txt"}
)
result = chat.ingest_documents([doc])

# Ask question
response = chat.query("What is your question?")

print(response["answer"])
print(f"Confidence: {response['confidence']}")
```

### 📁 Supported File Formats

| Format | Extension | Support Status |
|--------|-----------|----------------|
| Plain Text | `.txt` | ✅ Fully supported |
| Markdown | `.md` | ✅ Fully supported |
| PDF | `.pdf` | ⚠️ Requires extra processing |
| Word | `.docx` | ⚠️ Requires extra processing |

### 🎯 Use Cases

| Scenario | Example |
|---------|---------|
| 📚 **Knowledge Base Q&A** | Enterprise internal document retrieval |
| 📄 **Contract Analysis** | Key clause extraction from legal documents |
| 📰 **Report Summarization** | Automatic long document summarization |
| 🔬 **Paper Reading** | Academic literature Q&A |
| 💼 **Customer Service** | Product documentation Q&A |

---

## 💡 Design Philosophy

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     DocuChat-Lite                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐│
│  │  Doc Input  │ -> │   Chunker   │ -> │  Index Store ││
│  └─────────────┘    └─────────────┘    └─────────────┘│
│                                             │           │
│                                             ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐│
│  │   Web UI   │ <- │   Answer    │ <- │   Retriever ││
│  │   CLI      │    │   (LLM)     │    │  (Keyword)  ││
│  └─────────────┘    └─────────────┘    └─────────────┘│
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Choice | Reason |
|-----------|--------|--------|
| Core Language | Python 3.8+ | Rich ecosystem, easy to extend |
| Vector Store | Built-in index | Zero dependency, sufficient |
| Retrieval | BM25 + Keyword | No external vector model needed |
| LLM Interface | OpenAI/Ollama | Flexible switching, high freedom |
| Web Framework | Flask (optional) | Lightweight, replaceable |

---

## 🔮 Roadmap

- [ ] 📊 **v1.1** - Support PDF, DOCX document parsing
- [ ] 🔍 **v1.2** - Integrate vector database for semantic search
- [ ] 🌐 **v2.0** - Support multi-language documents and Q&A
- [ ] 📱 **v2.1** - Develop desktop client
- [ ] ☁️ **v2.2** - Cloud deployment version

---

## 🤝 Contributing

Welcome to submit Issues and Pull Requests!

### Development Setup

```bash
# Clone code
git clone https://github.com/gitstq/DocuChat-Lite.git
cd DocuChat-Lite

# Create branch
git checkout -b feature/your-feature

# Submit after development
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature

# Create Pull Request
```

### Commit Conventions

```
feat: New feature
fix: Bug fix
docs: Documentation update
refactor: Code refactoring
test: Test case
chore: Build/tool changes
```

---

## 📦 Packaging and Deployment

### Local Running

```bash
# Clone
git clone https://github.com/gitstq/DocuChat-Lite.git
cd DocuChat-Lite

# Run
python docuchat.py ingest ./samples
python docuchat.py query "Your question"
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask --no-cache-dir
EXPOSE 5000
CMD ["python", "web_app.py"]
```

### Cloud Deployment

| Platform | Deployment Method |
|----------|-------------------|
| Railway | One-click deployment |
| Render | Connect to GitHub |
| Fly.io | `fly launch` |
| Vercel | Serverless Functions |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- Inspiration: [kotaemon](https://github.com/Cinnamon/kotaemon) - Open-source RAG document chat tool
- Tech Stack: Pure Python 3.8+ implementation

---

<div align="center">

**If this project helps you, please give us a ⭐!**

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>

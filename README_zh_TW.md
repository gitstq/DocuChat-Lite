# 🧠 DocuChat-Lite

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/gitstq/DocuChat-Lite?style=flat)
![Forks](https://img.shields.io/github/forks/gitstq/DocuChat-Lite?style=flat)

**輕量級零依賴文檔智慧問答引擎** | **Zero-Dependency RAG Document Chat Engine**

[English](README_en.md) | [简体中文](README.md) | [繁體中文](README_zh_TW.md) | [日本語](README_ja.md)

</div>

---

## 🎉 專案介紹

DocuChat-Lite 是一款基於 RAG（檢索增強生成）技術的輕量級文檔智慧問答引擎。它能夠幫助您從大量文檔中快速獲取所需資訊，支援多種 LLM 後端，零外部依賴，即裝即用！

### 🌟 核心亮點

- 🔥 **零依賴核心**：無需安裝任何第三方庫，Python 原生實現
- 🚀 **極速部署**：下載即運行，無需複雜配置
- 🤖 **多後端支援**：OpenAI、Ollama、本地模型自由切換
- 🌐 **雙介面**：命令列 + Web 介面，滿足不同場景
- 📊 **即時統計**：知識庫狀態一目了然

---

## ✨ 核心功能

| 功能 | 描述 |
|------|------|
| 🧠 **智慧問答** | 基於文檔內容進行自然語言問答，理解上下文 |
| 📄 **多格式支援** | 支援 TXT、Markdown 等常見文字格式 |
| 🔍 **語義檢索** | 關鍵詞 + 語義相似度雙重檢索 |
| 🤖 **多LLM後端** | OpenAI API / Ollama 本地部署 / 相容介面 |
| 🌐 **Web介面** | 友善的瀏覽器介面，拖曳上傳即可使用 |
| 📊 **統計分析** | 即時顯示知識庫規模、檢索效率等指標 |
| 💾 **會話管理** | 支援多輪對話，上下文記憶 |
| 🎯 **來源追溯** | 明確標注答案來源，可信可靠 |

---

## 🚀 快速開始

### 📋 環境需求

- Python 3.8 或更高版本
- （可選）OpenAI API Key 或 Ollama 本地服務

### ⚡ 安裝方式

```bash
# 複製專案
git clone https://github.com/gitstq/DocuChat-Lite.git
cd DocuChat-Lite

# 直接運行（零依賴）
python docuchat.py --help
```

### 🎮 命令列模式

```bash
# 匯入文檔
python docuchat.py ingest ./samples

# 開始提問
python docuchat.py query "文檔的主要內容是什麼？"

# 查看統計
python docuchat.py stats

# 清除資料
python docuchat.py clear
```

### 🌐 Web介面模式

```bash
# 安裝 Flask（如需 Web 介面）
pip install flask

# 啟動服務
python web_app.py

# 瀏覽器開啟
open http://localhost:5000
```

---

## 📖 詳細使用指南

### 🔧 環境變數配置

#### OpenAI API 配置

```bash
export OPENAI_API_KEY=sk-your-api-key-here
```

#### Ollama 本地部署配置

```bash
# 安裝 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull llama2

# 啟動服務
ollama serve

# 設定環境變數
export OLLAMA_URL=http://localhost:11434
export OLLAMA_MODEL=llama2
```

### 💻 程式設計介面

```python
from docuchat import DocuChat, Document

# 初始化引擎
chat = DocuChat()

# 匯入文檔
doc = Document(
    content="您的文檔內容...",
    metadata={"source": "example.txt"}
)
result = chat.ingest_documents([doc])

# 提問
response = chat.query("您的問題是什麼？")

print(response["answer"])
print(f"置信度: {response['confidence']}")
```

### 📁 支援的檔案格式

| 格式 | 副檔名 | 支援狀態 |
|------|--------|----------|
| 純文字 | `.txt` | ✅ 完全支援 |
| Markdown | `.md` | ✅ 完全支援 |
| PDF | `.pdf` | ⚠️ 需額外處理 |
| Word | `.docx` | ⚠️ 需額外處理 |

---

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

### 提交規範

```
feat: 新功能
fix: 修復問題
docs: 文檔更新
refactor: 程式碼重構
test: 測試用例
chore: 構建/工具變動
```

---

## 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議，您可以自由使用、修改和散發本專案。

---

<div align="center">

**如果這個專案對您有幫助，請給我們一個 ⭐！**

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>

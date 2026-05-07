# 🧠 DocuChat-Lite

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/gitstq/DocuChat-Lite?style=flat)
![Forks](https://img.shields.io/github/forks/gitstq/DocuChat-Lite?style=flat)

**轻量级零依赖文档智能问答引擎** | **Zero-Dependency RAG Document Chat Engine**

[English](README_en.md) | [简体中文](README.md) | [繁體中文](README_zh_TW.md) | [日本語](README_ja.md)

</div>

---

## 🎉 项目介绍

DocuChat-Lite 是一款基于 RAG（检索增强生成）技术的轻量级文档智能问答引擎。它能够帮助您从大量文档中快速获取所需信息，支持多种 LLM 后端，零外部依赖，即装即用！

### 🌟 核心亮点

- 🔥 **零依赖核心**：无需安装任何第三方库，Python 原生实现
- 🚀 **极速部署**：下载即运行，无需复杂配置
- 🤖 **多后端支持**：OpenAI、Ollama、本地模型自由切换
- 🌐 **双界面**：命令行 + Web 界面，满足不同场景
- 📊 **实时统计**：知识库状态一目了然

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🧠 **智能问答** | 基于文档内容进行自然语言问答，理解上下文 |
| 📄 **多格式支持** | 支持 TXT、Markdown 等常见文本格式 |
| 🔍 **语义检索** | 关键词 + 语义相似度双重检索 |
| 🤖 **多LLM后端** | OpenAI API / Ollama 本地部署 / 兼容接口 |
| 🌐 **Web界面** | 友好的浏览器界面，拖拽上传即可使用 |
| 📊 **统计分析** | 实时显示知识库规模、检索效率等指标 |
| 💾 **会话管理** | 支持多轮对话，上下文记忆 |
| 🎯 **来源追溯** | 明确标注答案来源，可信可靠 |

---

## 🚀 快速开始

### 📋 环境要求

- Python 3.8 或更高版本
- （可选）OpenAI API Key 或 Ollama 本地服务

### ⚡ 安装方式

```bash
# 克隆项目
git clone https://github.com/gitstq/DocuChat-Lite.git
cd DocuChat-Lite

# 直接运行（零依赖）
python docuchat.py --help
```

### 🎮 命令行模式

```bash
# 导入文档
python docuchat.py ingest ./samples

# 开始提问
python docuchat.py query "文档的主要内容是什么？"

# 查看统计
python docuchat.py stats

# 清除数据
python docuchat.py clear
```

### 🌐 Web界面模式

```bash
# 安装 Flask（如需要 Web 界面）
pip install flask

# 启动服务
python web_app.py

# 浏览器打开
open http://localhost:5000
```

---

## 📖 详细使用指南

### 🔧 环境变量配置

#### OpenAI API 配置

```bash
export OPENAI_API_KEY=sk-your-api-key-here
```

#### Ollama 本地部署配置

```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull llama2

# 启动服务
ollama serve

# 配置环境变量
export OLLAMA_URL=http://localhost:11434
export OLLAMA_MODEL=llama2
```

### 💻 编程接口

```python
from docuchat import DocuChat, Document

# 初始化引擎
chat = DocuChat()

# 导入文档
doc = Document(
    content="您的文档内容...",
    metadata={"source": "example.txt"}
)
result = chat.ingest_documents([doc])

# 提问
response = chat.query("您的问题是什么？")

print(response["answer"])
print(f"置信度: {response['confidence']}")
```

### 📁 支持的文件格式

| 格式 | 扩展名 | 支持状态 |
|------|--------|----------|
| 纯文本 | `.txt` | ✅ 完全支持 |
| Markdown | `.md` | ✅ 完全支持 |
| PDF | `.pdf` | ⚠️ 需额外处理 |
| Word | `.docx` | ⚠️ 需额外处理 |

### 🎯 使用场景

| 场景 | 示例 |
|------|------|
| 📚 **知识库问答** | 企业内部文档检索 |
| 📄 **合同分析** | 法律文档关键条款提取 |
| 📰 **报告总结** | 长文档自动摘要 |
| 🔬 **论文研读** | 学术文献问答 |
| 💼 **客服助手** | 产品文档智能问答 |

---

## 💡 设计思路

### 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                     DocuChat-Lite                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐│
│  │  文档输入层  │ -> │   分块引擎   │ -> │  索引存储层  ││
│  └─────────────┘    └─────────────┘    └─────────────┘│
│                                             │           │
│                                             ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐│
│  │   Web UI    │ <- │   答案生成   │ <- │   检索引擎   ││
│  │   CLI       │    │   (LLM)     │    │  (关键词)    ││
│  └─────────────┘    └─────────────┘    └─────────────┘│
└─────────────────────────────────────────────────────────┘
```

### 技术选型

| 组件 | 选型 | 原因 |
|------|------|------|
| 核心语言 | Python 3.8+ | 生态丰富，易于扩展 |
| 向量存储 | 内置索引 | 零依赖，够用 |
| 检索算法 | BM25 + 关键词 | 无需外部向量模型 |
| LLM接口 | OpenAI/Ollama | 灵活切换，自由度高 |
| Web框架 | Flask (可选) | 轻量级，可替换 |

---

## 🔮 后续迭代计划

- [ ] 📊 **v1.1** - 支持 PDF、DOCX 等格式文档解析
- [ ] 🔍 **v1.2** - 集成向量数据库，支持语义检索
- [ ] 🌐 **v2.0** - 支持多语言文档和问答
- [ ] 📱 **v2.1** - 开发桌面客户端
- [ ] ☁️ **v2.2** - 云端部署版本

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境设置

```bash
# 克隆代码
git clone https://github.com/gitstq/DocuChat-Lite.git
cd DocuChat-Lite

# 创建分支
git checkout -b feature/your-feature

# 开发完成后提交
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature

# 创建 Pull Request
```

### 提交规范

```
feat: 新功能
fix: 修复问题
docs: 文档更新
refactor: 代码重构
test: 测试用例
chore: 构建/工具变动
```

---

## 📦 打包与部署

### 本地运行

```bash
# 克隆
git clone https://github.com/gitstq/DocuChat-Lite.git
cd DocuChat-Lite

# 运行
python docuchat.py ingest ./samples
python docuchat.py query "您的问题"
```

### Docker 部署

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask --no-cache-dir
EXPOSE 5000
CMD ["python", "web_app.py"]
```

### 云端部署

| 平台 | 部署方式 |
|------|----------|
| Railway | 一键部署 |
| Render | 连接到 GitHub |
| Fly.io | `fly launch` |
| Vercel | Serverless Functions |

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议，您可以自由使用、修改和分发本项目。

---

## 🙏 致谢

- 灵感来源：[kotaemon](https://github.com/Cinnamon/kotaemon) - 开源 RAG 文档聊天工具
- 技术栈：Python 3.8+ 原生实现

---

<div align="center">

**如果这个项目对您有帮助，请给我们一个 ⭐！**

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>

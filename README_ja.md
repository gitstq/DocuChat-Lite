# 🧠 DocuChat-Lite

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/gitstq/DocuChat-Lite?style=flat)
![Forks](https://img.shields.io/github/forks/gitstq/DocuChat-Lite?style=flat)

**依存関係ゼロの軽量ドキュメントAI问答エンジン** | **Zero-Dependency RAG Document Chat Engine**

[English](README_en.md) | [简体中文](README.md) | [繁體中文](README_zh_TW.md) | [日本語](README_ja.md)

</div>

---

## 🎉 プロジェクト紹介

DocuChat-Liteは、RAG（検索拡張生成）技術に基づいた軽量なドキュメントAI问答エンジンです。大量のドキュメントから必要な情報を素早く取得し、複数のLLMバックエンドをサポートし、外部依存関係なしで即座に使用できます！

### 🌟 コアハイライト

- 🔥 **依存関係ゼロ**：外部ライブラリ不要、Pythonネイティブ実装
- 🚀 **クイックデプロイ**：ダウンロードして即実行、複雑な設定不要
- 🤖 **マルチバックエンド対応**：OpenAI、Ollama、ローカルモデル自由切替
- 🌐 **Dualインターフェース**：コマンドライン + Webインターフェース
- 📊 **リアルタイム統計**：ナレッジベースのステータスを一目で確認

---

## ✨ コア機能

| 機能 | 説明 |
|------|------|
| 🧠 **インテリジェントQA** | ドキュメント内容に基づく自然言語问答 |
| 📄 **マルチフォーマット対応** | TXT、Markdown等のテキスト形式をサポート |
| 🔍 **セマンティック検索** | キーワード + 類似度二重検索 |
| 🤖 **マルチLLMバックエンド** | OpenAI API / Ollama / 互換インターフェース |
| 🌐 **Webインターフェース** | ドラッグ＆ドロップで簡単アップロード |
| 📊 **統計分析** | ナレッジベースの規模と検索効率を表示 |

---

## 🚀 クイックスタート

### 📋 必要環境

- Python 3.8 以上
- （オプション）OpenAI API Key または Ollamaローカルサービス

### ⚡ インストール

```bash
# プロジェクトをクローン
git clone https://github.com/gitstq/DocuChat-Lite.git
cd DocuChat-Lite

# そのまま実行（依存関係ゼロ）
python docuchat.py --help
```

### 🎮 コマンドラインモード

```bash
# ドキュメントをインポート
python docuchat.py ingest ./samples

# 質問する
python docuchat.py query "ドキュメントの主内容は？"

# 統計を表示
python docuchat.py stats

# データをクリア
python docuchat.py clear
```

### 🌐 Webインターフェースモード

```bash
# Flaskをインストール（Webが必要な場合）
pip install flask

# サービスを起動
python web_app.py

# ブラウザで開く
open http://localhost:5000
```

---

## 📖 詳細な使い方

### 🔧 環境変数の設定

#### OpenAI API設定

```bash
export OPENAI_API_KEY=sk-your-api-key-here
```

#### Ollamaローカルデプロイ設定

```bash
# Ollamaをインストール
curl -fsSL https://ollama.com/install.sh | sh

# モデルをダウンロード
ollama pull llama2

# サービスを起動
ollama serve

# 環境変数を設定
export OLLAMA_URL=http://localhost:11434
export OLLAMA_MODEL=llama2
```

### 💻 プログラミングインターフェース

```python
from docuchat import DocuChat, Document

# エンジンを初期化
chat = DocuChat()

# ドキュメントをインポート
doc = Document(
    content="ドキュメント内容...",
    metadata={"source": "example.txt"}
)
result = chat.ingest_documents([doc])

# 質問する
response = chat.query("あなたの質問は？")

print(response["answer"])
print(f"信頼度: {response['confidence']}")
```

---

## 🤝 コントリビュート

IssueとPull Requestを歓迎します！

### コミットルール

```
feat: 新機能
fix: バグ修正
docs: ドキュメント更新
refactor: リファクタリング
test: テストケース
chore: ビルド/ツール変更
```

---

## 📄 ライセンス

このプロジェクトは[MIT License](LICENSE)の下でライセンスされています。

---

<div align="center">

**このプロジェクトが役に立ったら、⭐をお願いします！**

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>

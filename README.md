# Gen AI Catalogue - Claude Code Action 記事生成システム

Claude Code Actionから直接AIツールのレビュー記事を自動生成し、WordPressに投稿するシステム

## 🎯 概要

このプロジェクトは、**Claude Code Action**を使用して、AIツールのURLを指定するだけで高品質なレビュー記事を自動生成するシステムです。ウェブインターフェースは不要で、Cursor内から直接実行できます。

## ✨ 主な機能

- **ワンクリック記事生成**: Claude Code ActionでAIツールのURLを指定するだけ
- **自動リサーチ**: Webスクレイピングでツール情報を自動収集
- **SEO最適化**: メタデータ、FAQ、構造化データを自動生成
- **WordPress連携**: 生成記事をWordPressに自動投稿
- **品質保証**: 複数のClaude モデルによる段階的な記事作成

## 🏗️ プロジェクト構造

```
Gen_AI_Catalogue/
├── .cursor/recipes/                    # Cursorレシピ
│   └── generate_ai_tool_article.json  # メイン記事生成レシピ
├── scripts/                           # 自動化スクリプト
│   ├── fetch_content.py              # Webコンテンツ取得
│   └── deploy_to_wordpress.py        # WordPress投稿
├── prompts/                          # Claudeプロンプトテンプレート
│   └── tool_review.yaml             # レビュー記事用テンプレート
├── content/                          # 生成されたMarkdown記事
├── tmp/                             # 一時ファイル
└── .github/workflows/               # GitHub Actions（オプション）
```

## 🚀 セットアップ

### 1. 依存関係のインストール

```bash
./setup.sh
```

### 2. WordPress認証情報の設定

`.env` ファイルを編集：

```bash
# WordPress設定
WORDPRESS_URL=https://genaicatalogue.com
WORDPRESS_USERNAME=your_username
WORDPRESS_PASSWORD=your_application_password
```

## 📝 使用方法

### Step 1: 記事生成

1. Cursorのコマンドパレット（Cmd+Shift+P）を開く
2. **"AI Tool Article Generator"** を選択
3. パラメータを入力：
   - `tool_url`: レビューするAIツールのURL（例: https://elevenlabs.io）
   - `primary_keyword`: SEOキーワード（例: "ElevenLabs review 2025"）

### Step 2: 記事の確認・編集

生成された記事は `content/` ディレクトリに保存されます：
- ファイル名: `YYYY-MM-DD_ツール名_review_final.md`
- アフィリエイトリンクは `[AFFILIATE_LINK]` プレースホルダーで表示

### Step 3: WordPress投稿

```bash
# アフィリエイトリンクを実際のURLに置換後
python3 scripts/deploy_to_wordpress.py
```

## 🔧 技術仕様

### 記事生成プロセス

1. **コンテンツ取得** (`fetch_content.py`)
   - BeautifulSoupでWebスクレイピング
   - 価格情報、機能、メタデータを抽出

2. **分析** (Claude Haiku)
   - ツール情報の整理・分析
   - 競合比較ポイントの抽出

3. **アウトライン作成** (Claude Sonnet)
   - SEO最適化された見出し構造
   - アフィリエイトリンク設置箇所の計画

4. **記事執筆** (Claude Opus)
   - 1600文字程度の詳細レビュー
   - 価格表、使用例、CTA含む

5. **SEO最適化** (Claude Haiku)
   - Meta Description
   - FAQ（3つ）
   - JSON-LD構造化データ

## 📊 出力例

実際の使用例：

```bash
# ElevenLabsの記事生成
tool_url: https://elevenlabs.io
primary_keyword: "ElevenLabs review 2025"

# 生成されるファイル
content/2025-06-21_elevenlabs_review_final.md
```

## 🔒 セキュリティ

- WordPress認証情報は環境変数で管理
- APIキーは `.env` ファイルで保護
- 生成されたコンテンツはローカルで確認後に投稿

## �� ライセンス

MIT License 
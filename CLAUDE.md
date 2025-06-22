# Claude Code Action Configuration - Gen AI Catalogue Project

## プロジェクト概要
Gen AI Catalogueは、生成AIツール・SaaS自動記事生成システムです。Claude Code Actionを活用して、AIツールのURLを指定するだけで高品質なレビュー記事を自動生成し、WordPressに投稿できます。

## Claude Code Action 実行ルール

### 必須事項
1. **常にPRを作成** - コード変更時は必ずPull Requestを作成
2. **AI統合重視** - Claude APIとの連携を最優先
3. **日本語サポート** - コメントとドキュメントは日本語で記述
4. **品質保証** - 記事品質の自動チェック機能を実装

### AI記事生成ワークフロー

#### 1. 記事生成開始
```bash
# Claude Code Actionから実行
python3 scripts/generate_article.py --url https://example-ai-tool.com --keyword "AI tool review 2025"
```

#### 2. 生成プロセス
1. **コンテンツ取得** - Webスクレイピングでツール情報収集
2. **分析** - Claude Haikuによるデータ構造化
3. **アウトライン作成** - Claude Sonnetによる記事構成設計
4. **記事執筆** - Claude Opusによる詳細レビュー作成
5. **SEO最適化** - Claude Haikuによるメタデータ生成

#### 3. 品質チェック
```bash
python3 scripts/quality_check.py --article-id <ARTICLE_ID>
```

#### 4. WordPress投稿
```bash
python3 scripts/deploy_to_wordpress.py --article-id <ARTICLE_ID>
```

### コーディングスタイル（AI-First Development）

#### 1. Claude API統合
```python
# 推奨パターン
async def generate_article_section(prompt: str, model: str = "claude-3-haiku"):
    """
    Claude APIを使用して記事セクションを生成
    
    Args:
        prompt: 生成用プロンプト
        model: 使用するClaudeモデル
    
    Returns:
        str: 生成されたコンテンツ
    """
    try:
        response = await claude_client.messages.create(
            model=model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        raise ArticleGenerationError(f"AI生成に失敗しました: {e}")
```

#### 2. プロンプト管理
```yaml
# prompts/tool_review.yaml
article_outline:
  system: |
    あなたは経験豊富なテックライターです。
    SEO最適化された記事アウトラインを作成してください。
  
  user_template: |
    以下のAIツールについて、詳細なレビュー記事のアウトラインを作成してください。
    
    ツール名: {tool_name}
    URL: {tool_url}
    主要機能: {main_features}
    価格: {pricing}
    
    要件:
    - 1600文字以上の記事構成
    - SEOキーワード「{seo_keyword}」を自然に含める
    - アフィリエイトリンク設置箇所を明示
    - 競合比較セクションを含める
```

#### 3. エラーハンドリング
```python
class ArticleGenerationError(Exception):
    """記事生成関連のエラー"""
    pass

async def safe_claude_call(prompt: str, max_retries: int = 3):
    """
    Claude API呼び出しのリトライ機能付きラッパー
    """
    for attempt in range(max_retries):
        try:
            return await generate_article_section(prompt)
        except Exception as e:
            if attempt == max_retries - 1:
                raise ArticleGenerationError(f"Claude API呼び出しが{max_retries}回失敗しました: {e}")
            await asyncio.sleep(2 ** attempt)  # 指数バックオフ
```

### PR作成時のテンプレート

```markdown
## 概要
[記事生成機能の変更内容を記載]

## 変更内容
- [ ] 記事生成ロジックの改善
- [ ] Claude API統合の更新
- [ ] SEO最適化機能の追加
- [ ] WordPress連携の改善

## 生成テスト結果
### テスト対象ツール
- URL: [テストに使用したAIツールのURL]
- 生成時間: XX秒
- 記事品質スコア: XX/100

### 生成された記事の品質
- 文字数: XXXX文字
- SEOスコア: XX/100
- 読みやすさ: XX/100
- アフィリエイトリンク: X箇所

## チェックリスト
- [ ] Claude API統合テスト成功
- [ ] 記事品質チェック通過
- [ ] WordPress投稿テスト成功
- [ ] エラーハンドリング確認

## 関連Issue
Closes #XX
```

### コミットメッセージ規約

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type（記事生成システム特化）
- `feat`: 新機能（記事生成、SEO最適化など）
- `fix`: バグ修正
- `ai`: AI統合関連の変更
- `seo`: SEO最適化の改善
- `wordpress`: WordPress連携の変更
- `prompt`: プロンプトテンプレートの更新
- `docs`: ドキュメント更新
- `test`: テスト追加・修正

#### 例
```
feat(ai): Claude Opus統合による記事品質向上

記事執筆フェーズでClaude Opusを使用することで、
より自然で読みやすい記事生成を実現しました。

- 文字数: 平均1800文字（従来比+20%）
- 読みやすさスコア: 85/100（従来比+15%）
- SEO最適化: メタデータ自動生成機能追加

Closes #123
```

### 開発環境セットアップ

```bash
# バックエンド
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 環境変数設定
cp .env.example .env
# .envファイルを編集してAPIキーを設定

# データベース初期化
alembic upgrade head

# サーバー起動（ポート5050）
python3 main.py

# フロントエンド
cd frontend
npm install
npm run dev  # ポート5173で起動
```

### 記事生成コマンド

```bash
# 基本的な記事生成
python3 scripts/generate_article.py --url https://elevenlabs.io --keyword "ElevenLabs review 2025"

# 詳細オプション付き
python3 scripts/generate_article.py \
  --url https://elevenlabs.io \
  --keyword "ElevenLabs review 2025" \
  --category "音声AI" \
  --target-length 2000 \
  --affiliate-links 3

# 記事品質チェック
python3 scripts/quality_check.py --article-id article_20250121_elevenlabs

# WordPress投稿（draft状態）
python3 scripts/deploy_to_wordpress.py --article-id article_20250121_elevenlabs --status draft

# WordPress投稿（公開）
python3 scripts/deploy_to_wordpress.py --article-id article_20250121_elevenlabs --status publish
```

### テスト実行コマンド

```bash
# バックエンドテスト
cd backend
pytest tests/ -v

# 記事生成テスト
pytest tests/test_article_generation.py -v

# Claude API統合テスト
pytest tests/test_claude_integration.py -v

# WordPress連携テスト
pytest tests/test_wordpress_integration.py -v

# フロントエンドテスト
cd frontend
npm test
```

### AI統合に関する注意事項

#### Claude API使用ガイドライン
- **レート制限**: 1分間に50リクエスト以下
- **トークン制限**: モデルごとの最大トークン数を遵守
- **コスト最適化**: 適切なモデル選択（Haiku < Sonnet < Opus）
- **エラーハンドリング**: 必ずリトライ機能を実装

#### プロンプト品質管理
- バージョン管理による改善履歴の記録
- A/Bテストによる効果測定
- 定期的な品質レビュー

#### 記事品質基準
- **最低文字数**: 1600文字
- **SEOスコア**: 80/100以上
- **読みやすさ**: 75/100以上
- **事実確認**: 生成内容の検証必須

### WordPress連携設定

#### 認証設定
```bash
# .envファイルに設定
WORDPRESS_URL=https://your-wordpress-site.com
WORDPRESS_USERNAME=your_username
WORDPRESS_PASSWORD=your_application_password
```

#### 投稿設定
```python
# デフォルト投稿設定
DEFAULT_POST_CONFIG = {
    "status": "draft",  # 初回はdraft
    "comment_status": "open",
    "ping_status": "open",
    "categories": ["AI Tools"],
    "tags": ["AI", "Review", "SaaS"]
}
```

### よくある質問と対処法

#### Q: Claude API呼び出しが失敗する
A: 以下を確認してください：
1. APIキーが正しく設定されているか（.envファイル）
2. レート制限に達していないか
3. インターネット接続が安定しているか

#### Q: 記事品質が低い
A: プロンプトテンプレートを改善してください：
1. より具体的な指示を追加
2. 例文を含める
3. 品質基準を明確化

#### Q: WordPress投稿が失敗する
A: 認証情報とAPI設定を確認してください：
1. Application Passwordが有効か
2. REST APIが有効化されているか
3. 必要な権限があるか

### 禁止事項
- 実際のAPIキーをコードにハードコーディング
- 著作権を侵害するコンテンツの生成
- 事実と異なる情報の記載
- 過度なSEOスパム的手法
- 本番WordPress環境での直接テスト

### 推奨ツール
- **Claude API**: 記事生成エンジン
- **FastAPI**: バックエンドフレームワーク
- **React + Vite**: フロントエンド
- **BeautifulSoup**: Webスクレイピング
- **SQLAlchemy**: データベースORM
- **pytest**: テストフレームワーク

### Claude Code Action 専用機能

#### 自動記事生成レシピ
Cursorの`.cursor/recipes/`ディレクトリに記事生成レシピを配置：

```json
{
  "name": "AI Tool Article Generator",
  "description": "AIツールのレビュー記事を自動生成",
  "parameters": [
    {
      "name": "tool_url",
      "description": "レビューするAIツールのURL",
      "type": "string",
      "required": true
    },
    {
      "name": "primary_keyword",
      "description": "SEO対策のメインキーワード",
      "type": "string",
      "required": true
    }
  ],
  "steps": [
    {
      "type": "command",
      "command": "python3 scripts/generate_article.py --url {tool_url} --keyword {primary_keyword}"
    }
  ]
}
```

#### 自動PR作成
- ブランチ名: `claude/article-<tool-name>-<timestamp>`
- PR本文に記事生成結果とメトリクスを自動挿入
- レビュー用チェックリストを自動生成

### 連絡先
質問や問題がある場合は、GitHubのIssueを作成してください。記事生成に関する改善提案も歓迎します。 
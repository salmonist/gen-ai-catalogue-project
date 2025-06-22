from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import uvicorn

# 環境変数を読み込み
load_dotenv()

app = FastAPI(
    title="Gen AI Catalogue API",
    description="生成AIツール・SaaS紹介ブログの自動記事生成システム",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """ヘルスチェックエンドポイント"""
    return {"message": "Gen AI Catalogue API is running!"}

@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "healthy", "service": "Gen AI Catalogue API"}

@app.post("/generate-article")
async def generate_article(request: dict):
    """記事生成エンドポイント"""
    try:
        url = request.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="URLが必要です")
        
        # TODO: Claude Code Actionsとの連携を実装
        return {
            "status": "success",
            "message": "記事生成を開始しました",
            "url": url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/articles")
async def get_articles():
    """生成された記事一覧を取得"""
    # TODO: データベースから記事一覧を取得
    return {"articles": []}

@app.post("/publish-to-wordpress")
async def publish_to_wordpress(request: dict):
    """WordPressに記事を投稿"""
    try:
        article_id = request.get("article_id")
        if not article_id:
            raise HTTPException(status_code=400, detail="記事IDが必要です")
        
        # TODO: WordPress REST APIとの連携を実装
        return {
            "status": "success",
            "message": "WordPressに投稿しました",
            "article_id": article_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("BACKEND_PORT", 5050))
    uvicorn.run(app, host="0.0.0.0", port=port) 
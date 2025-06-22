#!/bin/bash

echo "🚀 Gen AI Catalogue - Claude Code Action 記事生成システムのセットアップ"

# 環境変数ファイルをコピー
if [ ! -f .env ]; then
    echo "📝 環境変数ファイルを作成中..."
    cp env.example .env
    echo "✅ .env ファイルを作成しました。WordPress認証情報を設定してください。"
else
    echo "ℹ️  .env ファイルは既に存在します。"
fi

# Python依存関係のインストール
echo "📥 Python依存関係をインストール中..."
pip3 install -r requirements.txt

# 実行権限の設定
echo "🔧 スクリプトの実行権限を設定中..."
chmod +x scripts/*.py
chmod +x setup.sh

echo ""
echo "✅ セットアップが完了しました！"
echo ""
echo "🎯 使用方法:"
echo "1. .env ファイルにWordPress認証情報を設定"
echo "2. Claude Code Actionで 'AI Tool Article Generator' を実行"
echo "3. AIツールのURLを指定して記事を自動生成"
echo "4. 生成された記事を確認・編集"
echo "5. python3 scripts/deploy_to_wordpress.py でWordPressに投稿"
echo ""
echo "📚 詳細は README.md をご覧ください。" 
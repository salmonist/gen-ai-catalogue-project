#!/usr/bin/env python3
"""
生成された記事をWordPressに自動投稿するスクリプト
"""

import os
import sys
import glob
import json
import markdown
from datetime import datetime
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import re

def parse_markdown_post(file_path):
    """Markdownファイルを解析してWordPress投稿用のデータを作成"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # フロントマターを抽出
    frontmatter = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            # YAMLフロントマターを簡易パース
            frontmatter_text = parts[1].strip()
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')
            content = parts[2].strip()
    
    # MarkdownをHTMLに変換
    html_content = markdown.markdown(content, extensions=['tables', 'fenced_code'])
    
    # タイトルを抽出（最初のH1タグまたはフロントマターから）
    title = frontmatter.get('title', '')
    if not title:
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        else:
            title = os.path.basename(file_path).replace('.md', '').replace('_', ' ')
    
    # メタ情報を抽出
    meta_description = frontmatter.get('description', '')
    tags = frontmatter.get('tags', '').split(',') if frontmatter.get('tags') else []
    categories = frontmatter.get('categories', '').split(',') if frontmatter.get('categories') else ['AI Tools']
    
    return {
        'title': title,
        'content': html_content,
        'meta_description': meta_description,
        'tags': [tag.strip() for tag in tags if tag.strip()],
        'categories': [cat.strip() for cat in categories if cat.strip()],
        'status': frontmatter.get('status', 'draft')
    }

def create_wordpress_post(client, post_data):
    """WordPressに投稿を作成"""
    try:
        post = WordPressPost()
        post.title = post_data['title']
        post.content = post_data['content']
        post.post_status = post_data['status']
        
        # カテゴリとタグを設定
        if post_data['categories']:
            post.terms_names = {
                'category': post_data['categories'],
                'post_tag': post_data['tags']
            }
        
        # メタデータを設定
        if post_data['meta_description']:
            post.custom_fields = [{
                'key': 'meta_description',
                'value': post_data['meta_description']
            }]
        
        # 投稿を作成
        post_id = client.call(NewPost(post))
        return post_id
        
    except Exception as e:
        print(f"❌ WordPress投稿エラー: {str(e)}", file=sys.stderr)
        return None

def main():
    # 環境変数から設定を取得
    wp_url = os.getenv('WORDPRESS_URL')
    wp_username = os.getenv('WORDPRESS_USERNAME')
    wp_password = os.getenv('WORDPRESS_PASSWORD')
    
    if not all([wp_url, wp_username, wp_password]):
        print("❌ WordPress認証情報が設定されていません", file=sys.stderr)
        print("以下の環境変数を設定してください:", file=sys.stderr)
        print("- WORDPRESS_URL", file=sys.stderr)
        print("- WORDPRESS_USERNAME", file=sys.stderr)
        print("- WORDPRESS_PASSWORD", file=sys.stderr)
        sys.exit(1)
    
    # WordPressクライアントを初期化
    try:
        client = Client(f"{wp_url}/xmlrpc.php", wp_username, wp_password)
    except Exception as e:
        print(f"❌ WordPress接続エラー: {str(e)}", file=sys.stderr)
        sys.exit(1)
    
    # 新しい記事ファイルを検索
    content_files = glob.glob('content/*_final.md')
    if not content_files:
        print("📝 投稿する新しい記事が見つかりません")
        return
    
    success_count = 0
    error_count = 0
    
    for file_path in content_files:
        print(f"📄 処理中: {file_path}")
        
        try:
            # Markdownファイルを解析
            post_data = parse_markdown_post(file_path)
            
            # WordPressに投稿
            post_id = create_wordpress_post(client, post_data)
            
            if post_id:
                print(f"✅ 投稿成功: '{post_data['title']}' (ID: {post_id})")
                success_count += 1
                
                # 成功した場合、ファイルを処理済みディレクトリに移動
                processed_dir = 'content/processed'
                os.makedirs(processed_dir, exist_ok=True)
                processed_path = os.path.join(processed_dir, os.path.basename(file_path))
                os.rename(file_path, processed_path)
                
            else:
                print(f"❌ 投稿失敗: {file_path}")
                error_count += 1
                
        except Exception as e:
            print(f"❌ ファイル処理エラー ({file_path}): {str(e)}", file=sys.stderr)
            error_count += 1
    
    # 結果サマリー
    print(f"\n📊 処理結果:")
    print(f"   成功: {success_count}件")
    print(f"   エラー: {error_count}件")
    
    if error_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main() 
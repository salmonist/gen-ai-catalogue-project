#!/usr/bin/env python3
"""
Claude Code Action用記事生成スクリプト
"""

import argparse
import os
import sys
import requests
from datetime import datetime
from pathlib import Path
import json

def fetch_tool_info(url):
    """
    指定されたURLからツール情報を取得
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 基本的なメタデータを抽出
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find('title')
        title_text = title.text.strip() if title else "AI Tool"
        
        description = soup.find('meta', attrs={'name': 'description'})
        description_text = description.get('content', '') if description else ""
        
        return {
            'title': title_text,
            'description': description_text,
            'url': url
        }
    except Exception as e:
        print(f"Warning: Could not fetch tool info from {url}: {e}")
        return {
            'title': 'AI Tool',
            'description': 'AI tool description',
            'url': url
        }

def generate_article_with_claude(tool_info, keyword, category, target_length):
    """
    Claude APIを使用して記事を生成
    """
    try:
        import anthropic
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = f"""
あなたは経験豊富なテクニカルライターです。以下のAIツールについて、SEO最適化された詳細なレビュー記事を執筆してください。

## ツール情報
- タイトル: {tool_info['title']}
- URL: {tool_info['url']}
- 説明: {tool_info['description']}
- カテゴリ: {category}
- SEOキーワード: {keyword}

## 記事要件
- 目標文字数: {target_length}文字程度
- Markdown形式で出力
- SEOキーワード「{keyword}」を自然に含める
- 以下の構成で作成:
  1. 導入（ツールの概要）
  2. 主な機能・特徴
  3. 使用方法
  4. 料金プラン
  5. メリット・デメリット
  6. 競合ツールとの比較
  7. まとめ

## 注意事項
- 事実に基づいた内容にする
- 読者にとって有用な情報を提供
- 自然な日本語で執筆
- フロントマターを含める（title, description, tags, category）

記事を生成してください。
"""

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
        
    except Exception as e:
        print(f"Error generating article with Claude: {e}")
        # フォールバック: 基本的な記事テンプレート
        return generate_fallback_article(tool_info, keyword, category, target_length)

def generate_fallback_article(tool_info, keyword, category, target_length):
    """
    Claude APIが利用できない場合のフォールバック記事生成
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    article = f"""---
title: "{keyword} - {tool_info['title']}の詳細レビュー"
description: "{tool_info['title']}の機能、料金、使い方を詳しく解説。{keyword}に関する最新情報をお届けします。"
date: {today}
category: {category}
tags: [AI, {category}, レビュー, {keyword}]
---

# {keyword} - {tool_info['title']}の詳細レビュー

## はじめに

{tool_info['title']}は、{category}分野で注目を集めているAIツールです。本記事では、{keyword}について詳しく解説し、実際の使用感や料金プランについてレビューします。

## 主な機能・特徴

{tool_info['title']}の主な特徴は以下の通りです：

- **高性能AI**: 最新のAI技術を活用
- **使いやすいインターフェース**: 直感的な操作が可能
- **多様な機能**: 幅広い用途に対応

## 使用方法

1. 公式サイト（{tool_info['url']}）にアクセス
2. アカウントを作成
3. 必要な設定を行い利用開始

## 料金プラン

詳細な料金プランについては、公式サイトでご確認ください。

## メリット・デメリット

### メリット
- 高品質な結果が得られる
- 操作が簡単
- サポートが充実

### デメリット
- 料金が高い場合がある
- 学習コストが必要

## まとめ

{tool_info['title']}は、{category}分野において非常に有用なツールです。{keyword}を検討している方には、ぜひ一度試していただきたいツールです。

詳細については、[公式サイト]({tool_info['url']})をご確認ください。

---
*この記事は Claude Code Action により生成されました*
"""
    
    return article

def save_article(content, tool_info, keyword):
    """
    記事をファイルに保存
    """
    # ファイル名を生成
    today = datetime.now().strftime("%Y-%m-%d")
    tool_name = tool_info['title'].replace(' ', '_').replace('/', '_').lower()
    filename = f"{today}_{tool_name}_review.md"
    
    # contentディレクトリに保存
    content_dir = Path("content")
    content_dir.mkdir(exist_ok=True)
    
    filepath = content_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 記事を生成しました: {filepath}")
    return str(filepath)

def main():
    parser = argparse.ArgumentParser(description="Claude Code Action記事生成")
    parser.add_argument("--url", required=True, help="AIツールのURL")
    parser.add_argument("--keyword", required=True, help="SEOキーワード")
    parser.add_argument("--category", default="AI Tool", help="ツールのカテゴリ")
    parser.add_argument("--target-length", type=int, default=1600, help="目標文字数")
    
    args = parser.parse_args()
    
    print(f"🚀 記事生成を開始します...")
    print(f"   URL: {args.url}")
    print(f"   キーワード: {args.keyword}")
    print(f"   カテゴリ: {args.category}")
    print(f"   目標文字数: {args.target_length}文字")
    
    # ツール情報を取得
    print("\n📡 ツール情報を取得中...")
    tool_info = fetch_tool_info(args.url)
    
    # 記事を生成
    print("\n✍️ 記事を生成中...")
    article_content = generate_article_with_claude(
        tool_info, args.keyword, args.category, args.target_length
    )
    
    # 記事を保存
    print("\n💾 記事を保存中...")
    filepath = save_article(article_content, tool_info, args.keyword)
    
    print(f"\n🎉 記事生成が完了しました!")
    print(f"   ファイル: {filepath}")
    print(f"   文字数: {len(article_content)}文字")

if __name__ == "__main__":
    main() 
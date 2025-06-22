#!/usr/bin/env python3
"""
URLからコンテンツを取得してJSONファイルに出力するスクリプト
"""

import sys
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from datetime import datetime

def fetch_content(url):
    """指定されたURLからコンテンツを取得"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # メタデータを取得
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ""
        
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description.get('content', '') if meta_description else ""
        
        # 主要コンテンツを抽出
        content_selectors = [
            'main', 'article', '.content', '#content', 
            '.post', '.entry-content', '.article-content'
        ]
        
        content_text = ""
        for selector in content_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                content_text = content_element.get_text()
                break
        
        if not content_text:
            # フォールバック: body全体から取得
            body = soup.find('body')
            if body:
                content_text = body.get_text()
        
        # テキストをクリーンアップ
        content_text = re.sub(r'\s+', ' ', content_text).strip()
        
        # 価格情報を抽出
        price_patterns = [
            r'\$\d+(?:\.\d{2})?(?:/month|/mo|/year|/yr)?',
            r'¥\d+(?:,\d{3})*',
            r'€\d+(?:\.\d{2})?',
            r'Free|無料|フリー'
        ]
        
        prices = []
        for pattern in price_patterns:
            matches = re.findall(pattern, content_text, re.IGNORECASE)
            prices.extend(matches)
        
        # 特徴・機能を抽出（簡易版）
        features = []
        feature_keywords = [
            'feature', 'function', '機能', '特徴', 'capability', 'benefit'
        ]
        
        for keyword in feature_keywords:
            pattern = rf'{keyword}[^.]*\.'
            matches = re.findall(pattern, content_text, re.IGNORECASE)
            features.extend(matches[:3])  # 最大3つまで
        
        # 結果をJSONで出力
        result = {
            'url': url,
            'title': title_text,
            'description': description,
            'content': content_text[:2000],  # 最初の2000文字
            'prices': list(set(prices))[:5],  # 重複を除いて最大5つ
            'features': features[:5],  # 最大5つ
            'extracted_at': datetime.now().isoformat(),
            'domain': urlparse(url).netloc
        }
        
        return result
        
    except requests.RequestException as e:
        return {
            'error': f'HTTP Error: {str(e)}',
            'url': url,
            'extracted_at': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'error': f'General Error: {str(e)}',
            'url': url,
            'extracted_at': datetime.now().isoformat()
        }

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fetch_content.py <URL>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    result = fetch_content(url)
    
    # JSONとして出力
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 
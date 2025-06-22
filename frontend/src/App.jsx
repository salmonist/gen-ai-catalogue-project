import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [articles, setArticles] = useState([])
  const [isGenerating, setIsGenerating] = useState(false)
  const [url, setUrl] = useState('')

  // バックエンドAPIからの記事一覧取得
  useEffect(() => {
    fetchArticles()
  }, [])

  const fetchArticles = async () => {
    try {
      const response = await fetch('http://localhost:5050/articles')
      const data = await response.json()
      setArticles(data.articles)
    } catch (error) {
      console.error('記事の取得に失敗しました:', error)
    }
  }

  const generateArticle = async () => {
    if (!url) return
    
    setIsGenerating(true)
    try {
      const response = await fetch('http://localhost:5050/generate-article', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url })
      })
      const data = await response.json()
      console.log('記事生成結果:', data)
      setUrl('')
      fetchArticles() // 記事一覧を再取得
    } catch (error) {
      console.error('記事生成に失敗しました:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* ヘッダー */}
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg p-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Gen AI Catalogue
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              生成AIツール・SaaS自動記事生成システム
            </p>

            {/* 記事生成フォーム */}
            <div className="bg-white shadow rounded-lg p-6 mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                新しい記事を生成
              </h2>
              <div className="flex gap-4">
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="生成AIツールのURLを入力してください"
                  className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
                <button
                  onClick={generateArticle}
                  disabled={isGenerating || !url}
                  className="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isGenerating ? '生成中...' : '記事生成'}
                </button>
              </div>
            </div>

            {/* 記事一覧 */}
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-2xl font-semibold text-gray-900">
                  生成された記事
                </h2>
              </div>
              <div className="p-6">
                {articles.length === 0 ? (
                  <p className="text-gray-500 text-center py-8">
                    まだ記事が生成されていません
                  </p>
                ) : (
                  <div className="grid gap-4">
                    {articles.map((article, index) => (
                      <div key={index} className="border rounded-lg p-4">
                        <h3 className="font-semibold text-lg">{article.title}</h3>
                        <p className="text-gray-600 mt-2">{article.summary}</p>
                        <div className="mt-4 flex gap-2">
                          <button className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                            WordPress投稿
                          </button>
                          <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                            編集
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App 
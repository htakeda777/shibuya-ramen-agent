#!/usr/bin/env python3
"""
AI ニュース検索 Web ページ生成スクリプト

収集した JSON データから HTML + JS の検索可能な Web ページを生成
"""

import json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent.parent / "docs" / "ai_news_agent"
DATA_FILE = OUTPUT_DIR / "ai_news.json"


def generate_html(data: dict) -> str:
    """
    検索可能な HTML ページを生成
    """
    articles = data.get('articles', [])
    collected_at = data.get('collected_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # カテゴリ、ソース、重要度のリストを抽出
    categories = sorted(set(article.get('category', '') for article in articles if article.get('category')))
    sources = sorted(set(article.get('source', '') for article in articles if article.get('source')))
    importances = ['high', 'medium', 'low']

    # JSON データを埋め込み用に整形
    articles_json = json.dumps(articles, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI News Aggregator</title>
    <style>
        :root {{
            --primary: #00d4ff;
            --primary-dark: #00a8cc;
            --bg-dark: #0a0f1a;
            --bg-card: #1a2332;
            --bg-card-hover: #243046;
            --text-primary: #e8eaed;
            --text-secondary: #9aa0a6;
            --border: #2d3748;
            --high: #ff4d6d;
            --medium: #ffc107;
            --low: #28a745;
            --shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }}

        .header {{
            background: linear-gradient(180deg, rgba(0, 212, 255, 0.1) 0%, transparent 100%);
            border-bottom: 1px solid var(--border);
            padding: 2rem;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary) 0%, #00ffaa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }}

        .header p {{
            color: var(--text-secondary);
            font-size: 1rem;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .filter-section {{
            background: var(--bg-card);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow);
        }}

        .search-row {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
        }}

        .search-input {{
            flex: 1;
            position: relative;
        }}

        .search-input input {{
            width: 100%;
            padding: 1rem 1.25rem;
            background: var(--bg-dark);
            border: 2px solid var(--border);
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 1rem;
            transition: all 0.3s ease;
        }}

        .search-input input:focus {{
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.15);
        }}

        .search-input input::placeholder {{
            color: var(--text-secondary);
        }}

        .filter-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            align-items: center;
        }}

        .filter-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
        }}

        .filter-group select {{
            padding: 0.75rem 1rem;
            background: var(--bg-dark);
            border: 2px solid var(--border);
            border-radius: 10px;
            color: var(--text-primary);
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.3s ease;
            min-width: 140px;
        }}

        .filter-group select:focus {{
            outline: none;
            border-color: var(--primary);
        }}

        .filter-group select option {{
            background: var(--bg-card);
            color: var(--text-primary);
        }}

        .stats-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
        }}

        .stats-text {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .stats-text strong {{
            color: var(--primary);
        }}

        .clear-btn {{
            background: transparent;
            border: 2px solid var(--primary);
            color: var(--primary);
            padding: 0.5rem 1.25rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }}

        .clear-btn:hover {{
            background: var(--primary);
            color: var(--bg-dark);
        }}

        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 1.5rem;
        }}

        .news-card {{
            background: var(--bg-card);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
        }}

        .news-card:hover {{
            transform: translateY(-4px);
            background: var(--bg-card-hover);
            box-shadow: 0 8px 30px rgba(0, 212, 255, 0.15);
        }}

        .news-header {{
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--border);
        }}

        .news-meta {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.75rem;
            flex-wrap: wrap;
        }}

        .badge {{
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .badge-category {{
            background: rgba(0, 212, 255, 0.15);
            color: var(--primary);
            border: 1px solid var(--primary);
        }}

        .badge-importance {{
            border: none;
        }}

        .badge-importance.high {{
            background: rgba(255, 77, 109, 0.2);
            color: var(--high);
        }}

        .badge-importance.medium {{
            background: rgba(255, 193, 7, 0.2);
            color: var(--medium);
        }}

        .badge-importance.low {{
            background: rgba(40, 167, 69, 0.2);
            color: var(--low);
        }}

        .news-source {{
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}

        .news-title {{
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--text-primary);
            line-height: 1.4;
        }}

        .news-title a {{
            color: inherit;
            text-decoration: none;
            transition: color 0.3s ease;
        }}

        .news-title a:hover {{
            color: var(--primary);
        }}

        .news-body {{
            padding: 1.25rem 1.5rem;
            flex: 1;
            display: flex;
            flex-direction: column;
        }}

        .news-date {{
            color: var(--text-secondary);
            font-size: 0.85rem;
            margin-bottom: 0.75rem;
        }}

        .news-summary {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.6;
            flex: 1;
        }}

        .news-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
        }}

        .tag {{
            background: var(--bg-dark);
            color: var(--text-secondary);
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-size: 0.8rem;
        }}

        .no-results {{
            text-align: center;
            padding: 4rem 2rem;
            color: var(--text-secondary);
        }}

        .no-results h3 {{
            font-size: 1.5rem;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }}

        .footer {{
            text-align: center;
            padding: 3rem 2rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
            border-top: 1px solid var(--border);
            margin-top: 2rem;
        }}

        .footer a {{
            color: var(--primary);
            text-decoration: none;
        }}

        .footer a:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}

            .header {{
                padding: 1.5rem 1rem;
            }}

            .header h1 {{
                font-size: 1.75rem;
            }}

            .search-row {{
                flex-direction: column;
            }}

            .filter-row {{
                flex-direction: column;
                align-items: stretch;
            }}

            .filter-group {{
                flex-direction: column;
            }}

            .filter-group select {{
                width: 100%;
            }}

            .news-grid {{
                grid-template-columns: 1fr;
            }}

            .stats-bar {{
                flex-direction: column;
                gap: 1rem;
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <h1>AI News Aggregator</h1>
        <p>AI 関連の最新ニュースを検索・フィルタリング</p>
    </header>

    <main class="container">
        <section class="filter-section">
            <div class="search-row">
                <div class="search-input">
                    <input type="text" id="searchText" placeholder="キーワードで検索（タイトル、要約、タグ）...">
                </div>
            </div>
            <div class="filter-row">
                <div class="filter-group">
                    <select id="categoryFilter">
                        <option value="">全カテゴリ</option>
                        {generate_options(categories)}
                    </select>
                    <select id="sourceFilter">
                        <option value="">全ソース</option>
                        {generate_options(sources)}
                    </select>
                    <select id="importanceFilter">
                        <option value="">全重要度</option>
                        <option value="high">High</option>
                        <option value="medium">Medium</option>
                        <option value="low">Low</option>
                    </select>
                    <select id="sortOrder">
                        <option value="date">日付順（新しい順）</option>
                        <option value="importance">重要度順</option>
                        <option value="source">ソース順</option>
                        <option value="category">カテゴリ順</option>
                    </select>
                </div>
            </div>
            <div class="stats-bar">
                <span class="stats-text">表示中: <strong id="resultCount">{len(articles)}</strong> 件 / 全 {len(articles)} 件</span>
                <button class="clear-btn" onclick="clearFilters()">フィルターをクリア</button>
            </div>
        </section>

        <section class="news-grid" id="newsGrid">
            <!-- ニュースカードがここに動的に挿入される -->
        </section>

        <div class="no-results" id="noResults" style="display: none;">
            <h3>該当するニュースがありません</h3>
            <p>検索条件を変更してお試しください</p>
        </div>
    </main>

    <footer class="footer">
        <p>データ収集日時: {collected_at}</p>
        <p>Claude Agent SDK を使用して自動収集</p>
    </footer>

    <script>
        // ニュースデータ
        const articles = {articles_json};
        const totalCount = {len(articles)};

        // DOM 要素
        const searchText = document.getElementById('searchText');
        const categoryFilter = document.getElementById('categoryFilter');
        const sourceFilter = document.getElementById('sourceFilter');
        const importanceFilter = document.getElementById('importanceFilter');
        const sortOrder = document.getElementById('sortOrder');
        const newsGrid = document.getElementById('newsGrid');
        const resultCount = document.getElementById('resultCount');
        const noResults = document.getElementById('noResults');

        // 重要度の優先順位
        const importancePriority = {{ 'high': 0, 'medium': 1, 'low': 2 }};

        // 検索とフィルタリング
        function filterAndSort() {{
            const query = searchText.value.toLowerCase();
            const category = categoryFilter.value;
            const source = sourceFilter.value;
            const importance = importanceFilter.value;
            const sort = sortOrder.value;

            let filtered = articles.filter(article => {{
                // テキスト検索
                if (query) {{
                    const searchFields = [
                        article.title,
                        article.summary,
                        article.source,
                        article.category,
                        ...(article.tags || [])
                    ].filter(Boolean).join(' ').toLowerCase();

                    if (!searchFields.includes(query)) {{
                        return false;
                    }}
                }}

                // カテゴリフィルタ
                if (category && article.category !== category) {{
                    return false;
                }}

                // ソースフィルタ
                if (source && article.source !== source) {{
                    return false;
                }}

                // 重要度フィルタ
                if (importance && article.importance !== importance) {{
                    return false;
                }}

                return true;
            }});

            // ソート
            filtered.sort((a, b) => {{
                switch (sort) {{
                    case 'importance':
                        const impA = importancePriority[a.importance] ?? 3;
                        const impB = importancePriority[b.importance] ?? 3;
                        if (impA !== impB) return impA - impB;
                        return (b.date || '').localeCompare(a.date || '');
                    case 'source':
                        return (a.source || '').localeCompare(b.source || '');
                    case 'category':
                        return (a.category || '').localeCompare(b.category || '');
                    case 'date':
                    default:
                        return (b.date || '').localeCompare(a.date || '');
                }}
            }});

            renderNews(filtered);
        }}

        // ニュースカードのレンダリング
        function renderNews(filteredArticles) {{
            resultCount.textContent = filteredArticles.length;

            if (filteredArticles.length === 0) {{
                newsGrid.innerHTML = '';
                noResults.style.display = 'block';
                return;
            }}

            noResults.style.display = 'none';

            newsGrid.innerHTML = filteredArticles.map(article => `
                <article class="news-card">
                    <div class="news-header">
                        <div class="news-meta">
                            ${{article.category ? `<span class="badge badge-category">${{escapeHtml(article.category)}}</span>` : ''}}
                            ${{article.importance ? `<span class="badge badge-importance ${{article.importance}}">${{article.importance}}</span>` : ''}}
                            <span class="news-source">${{escapeHtml(article.source || 'Unknown')}}</span>
                        </div>
                        <h2 class="news-title">
                            ${{article.url
                                ? `<a href="${{escapeHtml(article.url)}}" target="_blank" rel="noopener noreferrer">${{escapeHtml(article.title)}}</a>`
                                : escapeHtml(article.title)
                            }}
                        </h2>
                    </div>
                    <div class="news-body">
                        ${{article.date ? `<div class="news-date">${{escapeHtml(article.date)}}</div>` : ''}}
                        ${{article.summary ? `<p class="news-summary">${{escapeHtml(article.summary)}}</p>` : ''}}
                        ${{article.tags && article.tags.length > 0 ? `
                            <div class="news-tags">
                                ${{article.tags.map(tag => `<span class="tag">${{escapeHtml(tag)}}</span>`).join('')}}
                            </div>
                        ` : ''}}
                    </div>
                </article>
            `).join('');
        }}

        // HTML エスケープ
        function escapeHtml(text) {{
            if (!text) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}

        // フィルタクリア
        function clearFilters() {{
            searchText.value = '';
            categoryFilter.value = '';
            sourceFilter.value = '';
            importanceFilter.value = '';
            sortOrder.value = 'date';
            filterAndSort();
        }}

        // イベントリスナー
        searchText.addEventListener('input', filterAndSort);
        categoryFilter.addEventListener('change', filterAndSort);
        sourceFilter.addEventListener('change', filterAndSort);
        importanceFilter.addEventListener('change', filterAndSort);
        sortOrder.addEventListener('change', filterAndSort);

        // 初期表示
        filterAndSort();
    </script>
</body>
</html>
'''
    return html


def generate_options(items: list) -> str:
    """
    select タグ用のオプションを生成
    """
    return '\n'.join(f'<option value="{item}">{item}</option>' for item in items)


def main():
    """
    メイン実行関数
    """
    print("=" * 60)
    print("AI News Web ページ生成")
    print("=" * 60)
    print()

    # JSON データを読み込み
    if not DATA_FILE.exists():
        print(f"データファイルが見つかりません: {DATA_FILE}")
        print("先に news_collector.py を実行してデータを収集してください。")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    articles_count = len(data.get('articles', []))
    print(f"{articles_count} 件のニュースデータを読み込みました")

    # HTML を生成
    html = generate_html(data)

    # ファイルに保存
    output_file = OUTPUT_DIR / "index.html"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Web ページを生成しました: {output_file}")
    print()
    print("ローカルサーバーで起動するには:")
    print(f"   cd {OUTPUT_DIR.parent} && python -m http.server 8000")
    print("   http://localhost:8000/ai_news_agent/ でアクセス")
    print()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
渋谷区ラーメン店検索 Web ページ生成スクリプト

収集した JSON データから HTML + JS の検索可能な Web ページを生成
"""

import json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent.parent / "docs" / "shibuya_ramen_agent"
DATA_FILE = OUTPUT_DIR / "ramen_shops.json"


def generate_html(data: dict) -> str:
    """
    検索可能な HTML ページを生成
    """
    shops = data.get('shops', [])
    collected_at = data.get('collected_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # エリアとジャンルのリストを抽出
    areas = sorted(set(shop.get('area', '不明') for shop in shops if shop.get('area')))
    genres = sorted(set(shop.get('genre', '不明') for shop in shops if shop.get('genre')))

    # JSON データを埋め込み用に整形
    shops_json = json.dumps(shops, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>渋谷区ラーメン店検索</title>
    <style>
        :root {{
            --primary-color: #e74c3c;
            --secondary-color: #c0392b;
            --bg-color: #fdf6f0;
            --card-bg: #ffffff;
            --text-color: #2c3e50;
            --text-light: #7f8c8d;
            --border-color: #ecf0f1;
            --shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Hiragino Kaku Gothic ProN', 'Yu Gothic', Meiryo, sans-serif;
            background: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
        }}

        .header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 2rem;
            text-align: center;
            box-shadow: var(--shadow);
        }}

        .header h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}

        .header p {{
            opacity: 0.9;
            font-size: 0.95rem;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .search-section {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow);
        }}

        .search-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 1rem;
        }}

        .search-input {{
            flex: 1;
            min-width: 200px;
        }}

        .search-input input {{
            width: 100%;
            padding: 0.75rem 1rem;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }}

        .search-input input:focus {{
            outline: none;
            border-color: var(--primary-color);
        }}

        .filter-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}

        .filter-group select {{
            padding: 0.75rem 1rem;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            font-size: 0.95rem;
            background: white;
            cursor: pointer;
            transition: border-color 0.3s;
        }}

        .filter-group select:focus {{
            outline: none;
            border-color: var(--primary-color);
        }}

        .stats {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
        }}

        .stats-text {{
            color: var(--text-light);
            font-size: 0.9rem;
        }}

        .clear-btn {{
            background: none;
            border: 2px solid var(--primary-color);
            color: var(--primary-color);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s;
        }}

        .clear-btn:hover {{
            background: var(--primary-color);
            color: white;
        }}

        .shop-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
        }}

        .shop-card {{
            background: var(--card-bg);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .shop-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}

        .shop-header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 1rem 1.25rem;
        }}

        .shop-name {{
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.25rem;
        }}

        .shop-area {{
            opacity: 0.9;
            font-size: 0.9rem;
        }}

        .shop-body {{
            padding: 1.25rem;
        }}

        .shop-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }}

        .tag {{
            background: #fff3f0;
            color: var(--primary-color);
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }}

        .tag.genre {{
            background: #ffeaa7;
            color: #d68910;
        }}

        .tag.rating {{
            background: #d5f5e3;
            color: #27ae60;
        }}

        .shop-info {{
            font-size: 0.9rem;
            color: var(--text-color);
        }}

        .shop-info p {{
            margin-bottom: 0.5rem;
            display: flex;
            align-items: flex-start;
        }}

        .shop-info .icon {{
            width: 20px;
            margin-right: 0.5rem;
            flex-shrink: 0;
        }}

        .shop-description {{
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
            color: var(--text-light);
            font-size: 0.9rem;
        }}

        .specialties {{
            margin-top: 1rem;
        }}

        .specialties h4 {{
            font-size: 0.85rem;
            color: var(--text-light);
            margin-bottom: 0.5rem;
        }}

        .specialties-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}

        .specialty-item {{
            background: var(--bg-color);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.85rem;
        }}

        .shop-link {{
            display: inline-block;
            margin-top: 1rem;
            color: var(--primary-color);
            text-decoration: none;
            font-size: 0.9rem;
            transition: color 0.3s;
        }}

        .shop-link:hover {{
            color: var(--secondary-color);
            text-decoration: underline;
        }}

        .no-results {{
            text-align: center;
            padding: 3rem;
            color: var(--text-light);
        }}

        .no-results h3 {{
            margin-bottom: 0.5rem;
        }}

        .footer {{
            text-align: center;
            padding: 2rem;
            color: var(--text-light);
            font-size: 0.9rem;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}

            .shop-grid {{
                grid-template-columns: 1fr;
            }}

            .search-row {{
                flex-direction: column;
            }}

            .filter-group {{
                width: 100%;
            }}

            .filter-group select {{
                flex: 1;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <h1>🍜 渋谷区ラーメン店検索</h1>
        <p>渋谷区内の人気ラーメン店を検索できます</p>
    </header>

    <main class="container">
        <section class="search-section">
            <div class="search-row">
                <div class="search-input">
                    <input type="text" id="searchText" placeholder="店名、住所、特徴などで検索...">
                </div>
            </div>
            <div class="search-row">
                <div class="filter-group">
                    <select id="areaFilter">
                        <option value="">全エリア</option>
                        {generate_options(areas)}
                    </select>
                    <select id="genreFilter">
                        <option value="">全ジャンル</option>
                        {generate_options(genres)}
                    </select>
                    <select id="sortOrder">
                        <option value="name">名前順</option>
                        <option value="rating">評価順</option>
                        <option value="area">エリア順</option>
                    </select>
                </div>
            </div>
            <div class="stats">
                <span class="stats-text" id="resultCount">全 {len(shops)} 店舗</span>
                <button class="clear-btn" onclick="clearFilters()">クリア</button>
            </div>
        </section>

        <section class="shop-grid" id="shopGrid">
            <!-- 店舗カードがここに動的に挿入される -->
        </section>

        <div class="no-results" id="noResults" style="display: none;">
            <h3>該当する店舗が見つかりません</h3>
            <p>検索条件を変更してお試しください</p>
        </div>
    </main>

    <footer class="footer">
        <p>データ収集日: {collected_at}</p>
        <p>Claude Agent SDK を使用して自動収集</p>
    </footer>

    <script>
        // 店舗データ
        const shops = {shops_json};

        // DOM 要素
        const searchText = document.getElementById('searchText');
        const areaFilter = document.getElementById('areaFilter');
        const genreFilter = document.getElementById('genreFilter');
        const sortOrder = document.getElementById('sortOrder');
        const shopGrid = document.getElementById('shopGrid');
        const resultCount = document.getElementById('resultCount');
        const noResults = document.getElementById('noResults');

        // 検索とフィルタリング
        function filterAndSort() {{
            const query = searchText.value.toLowerCase();
            const area = areaFilter.value;
            const genre = genreFilter.value;
            const sort = sortOrder.value;

            let filtered = shops.filter(shop => {{
                // テキスト検索
                if (query) {{
                    const searchFields = [
                        shop.name,
                        shop.address,
                        shop.area,
                        shop.genre,
                        shop.description,
                        ...(shop.specialties || [])
                    ].filter(Boolean).join(' ').toLowerCase();

                    if (!searchFields.includes(query)) {{
                        return false;
                    }}
                }}

                // エリアフィルタ
                if (area && shop.area !== area) {{
                    return false;
                }}

                // ジャンルフィルタ
                if (genre && shop.genre !== genre) {{
                    return false;
                }}

                return true;
            }});

            // ソート
            filtered.sort((a, b) => {{
                switch (sort) {{
                    case 'rating':
                        return (b.rating || 0) - (a.rating || 0);
                    case 'area':
                        return (a.area || '').localeCompare(b.area || '');
                    case 'name':
                    default:
                        return (a.name || '').localeCompare(b.name || '');
                }}
            }});

            renderShops(filtered);
        }}

        // 店舗カードのレンダリング
        function renderShops(filteredShops) {{
            resultCount.textContent = `${{filteredShops.length}} 店舗`;

            if (filteredShops.length === 0) {{
                shopGrid.innerHTML = '';
                noResults.style.display = 'block';
                return;
            }}

            noResults.style.display = 'none';

            shopGrid.innerHTML = filteredShops.map(shop => `
                <article class="shop-card">
                    <div class="shop-header">
                        <h2 class="shop-name">${{escapeHtml(shop.name)}}</h2>
                        <div class="shop-area">📍 ${{escapeHtml(shop.area || '渋谷区')}}</div>
                    </div>
                    <div class="shop-body">
                        <div class="shop-tags">
                            ${{shop.genre ? `<span class="tag genre">${{escapeHtml(shop.genre)}}</span>` : ''}}
                            ${{shop.rating ? `<span class="tag rating">⭐ ${{shop.rating}}</span>` : ''}}
                            ${{shop.price_range ? `<span class="tag">💰 ${{escapeHtml(shop.price_range)}}</span>` : ''}}
                        </div>
                        <div class="shop-info">
                            ${{shop.address ? `<p><span class="icon">🏠</span>${{escapeHtml(shop.address)}}</p>` : ''}}
                            ${{shop.hours ? `<p><span class="icon">🕐</span>${{escapeHtml(shop.hours)}}</p>` : ''}}
                            ${{shop.closed_days ? `<p><span class="icon">📅</span>定休日: ${{escapeHtml(shop.closed_days)}}</p>` : ''}}
                        </div>
                        ${{shop.specialties && shop.specialties.length > 0 ? `
                            <div class="specialties">
                                <h4>おすすめ・特徴</h4>
                                <div class="specialties-list">
                                    ${{shop.specialties.map(s => `<span class="specialty-item">${{escapeHtml(s)}}</span>`).join('')}}
                                </div>
                            </div>
                        ` : ''}}
                        ${{shop.description ? `<p class="shop-description">${{escapeHtml(shop.description)}}</p>` : ''}}
                        ${{shop.url ? `<a href="${{escapeHtml(shop.url)}}" target="_blank" rel="noopener noreferrer" class="shop-link">詳細を見る →</a>` : ''}}
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
            areaFilter.value = '';
            genreFilter.value = '';
            sortOrder.value = 'name';
            filterAndSort();
        }}

        // イベントリスナー
        searchText.addEventListener('input', filterAndSort);
        areaFilter.addEventListener('change', filterAndSort);
        genreFilter.addEventListener('change', filterAndSort);
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
    print("🌐 渋谷区ラーメン店検索 Web ページ生成")
    print("=" * 60)
    print()

    # JSON データを読み込み
    if not DATA_FILE.exists():
        print(f"❌ データファイルが見つかりません: {DATA_FILE}")
        print("   先に ramen_collector.py を実行してデータを収集してください。")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    shops_count = len(data.get('shops', []))
    print(f"📖 {shops_count} 店舗のデータを読み込みました")

    # HTML を生成
    html = generate_html(data)

    # ファイルに保存
    output_file = OUTPUT_DIR / "index.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Web ページを生成しました: {output_file}")
    print()
    print("🖥️  ブラウザで開くには:")
    print(f"   file://{output_file}")
    print()
    print("🌐 ローカルサーバーで起動するには:")
    print(f"   cd {OUTPUT_DIR} && python -m http.server 8000")
    print("   http://localhost:8000 でアクセス")
    print()


if __name__ == "__main__":
    main()

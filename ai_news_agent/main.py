#!/usr/bin/env python3
"""
AI ニュース収集・Web 生成 統合エージェント

Claude Agent SDK を使用して AI ニュースを収集し、
検索可能な Web ページを自動生成するエージェント
"""

import asyncio
import sys
from pathlib import Path

# モジュールのパスを追加
sys.path.insert(0, str(Path(__file__).parent))

from news_collector import collect_news_data, save_data
from generate_web import generate_html, OUTPUT_DIR, DATA_FILE


async def main():
    """
    メイン実行関数：データ収集から Web 生成まで一括実行
    """
    print()
    print("=" * 60)
    print(" AI News Aggregator - ニュース収集・Web 生成エージェント ")
    print("=" * 60)
    print()
    print("このエージェントは以下の処理を自動実行します:")
    print("  1. Web 検索で AI 関連ニュースを収集")
    print("  2. 収集データを JSON 形式で保存")
    print("  3. 検索可能な HTML + JS Web ページを生成")
    print()
    print("-" * 60)

    # ステップ 1: データ収集
    print("\n[Step 1/3] AI ニュースを収集中...")
    print("-" * 60)

    try:
        news_data = await collect_news_data()
    except Exception as e:
        print(f"\nデータ収集中にエラーが発生しました: {e}")
        print("Claude Agent SDK がインストールされているか確認してください。")
        print("pip install claude-agent-sdk")
        return 1

    # ステップ 2: データ保存
    print("\n[Step 2/3] データを JSON 形式で保存中...")
    print("-" * 60)

    filepath = save_data(news_data)

    articles_count = len(news_data.get('articles', []))
    if articles_count == 0:
        print("\n収集できた記事数が 0 です。")
        print("ネットワーク接続や API 制限を確認してください。")
        return 1

    print(f"保存完了: {articles_count} 件のニュース")

    # ステップ 3: Web ページ生成
    print("\n[Step 3/3] 検索 Web ページを生成中...")
    print("-" * 60)

    html = generate_html(news_data)

    output_file = OUTPUT_DIR / "index.html"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"生成完了: {output_file}")

    # 完了サマリー
    print()
    print("=" * 60)
    print(" 処理完了 ")
    print("=" * 60)
    print()
    print(f"収集結果:")
    print(f"   - 記事数: {articles_count} 件")

    if news_data.get('articles'):
        categories = {}
        for article in news_data['articles']:
            cat = article.get('category', '不明')
            categories[cat] = categories.get(cat, 0) + 1

        top_cats = sorted(categories.items(), key=lambda x: -x[1])[:5]
        print(f"   - カテゴリ: {', '.join(f'{c}({n})' for c, n in top_cats)}")

    print()
    print(f"出力ファイル:")
    print(f"   - JSON: {DATA_FILE}")
    print(f"   - HTML: {output_file}")
    print()
    print("Web ページを表示するには:")
    print(f"   cd {OUTPUT_DIR.parent} && python -m http.server 8000")
    print("   ブラウザで http://localhost:8000/ai_news_agent/ を開いてください")
    print()

    return 0


def run_web_generation_only():
    """
    既存の JSON データから Web ページのみを生成
    """
    print()
    print("既存データから Web ページを生成")
    print("-" * 60)

    if not DATA_FILE.exists():
        print(f"データファイルが見つかりません: {DATA_FILE}")
        print("先にデータ収集を実行してください。")
        return 1

    import json
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    html = generate_html(data)

    output_file = OUTPUT_DIR / "index.html"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Web ページを生成しました: {output_file}")
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="AI News Aggregator - ニュース収集・Web 生成エージェント"
    )
    parser.add_argument(
        '--web-only',
        action='store_true',
        help='既存の JSON データから Web ページのみを生成'
    )

    args = parser.parse_args()

    if args.web_only:
        sys.exit(run_web_generation_only())
    else:
        sys.exit(asyncio.run(main()))

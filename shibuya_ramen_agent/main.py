#!/usr/bin/env python3
"""
渋谷区ラーメン店データ収集・Web生成 統合エージェント

Claude Agent SDK を使用してラーメン店データを収集し、
検索可能な Web ページを自動生成するエージェント
"""

import asyncio
import sys
from pathlib import Path

# モジュールのパスを追加
sys.path.insert(0, str(Path(__file__).parent))

from ramen_collector import collect_ramen_data, save_data
from generate_web import generate_html, OUTPUT_DIR, DATA_FILE


async def main():
    """
    メイン実行関数：データ収集から Web 生成まで一括実行
    """
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " 🍜 渋谷区ラーメン店データ収集・Web生成エージェント 🍜 ".center(56) + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    print("このエージェントは以下の処理を自動実行します:")
    print("  1. Web 検索で渋谷区のラーメン店情報を収集")
    print("  2. 収集データを JSON 形式で保存")
    print("  3. 検索可能な HTML + JS Web ページを生成")
    print()
    print("─" * 60)

    # ステップ 1: データ収集
    print("\n📡 ステップ 1/3: ラーメン店データを収集中...")
    print("─" * 60)

    try:
        ramen_data = await collect_ramen_data()
    except Exception as e:
        print(f"\n❌ データ収集中にエラーが発生しました: {e}")
        print("   Claude Agent SDK がインストールされているか確認してください。")
        print("   pip install claude-agent-sdk")
        return 1

    # ステップ 2: データ保存
    print("\n💾 ステップ 2/3: データを JSON 形式で保存中...")
    print("─" * 60)

    filepath = save_data(ramen_data)

    shops_count = len(ramen_data.get('shops', []))
    if shops_count == 0:
        print("\n⚠️  収集できた店舗数が 0 です。")
        print("   ネットワーク接続やAPI制限を確認してください。")
        return 1

    print(f"   保存完了: {shops_count} 店舗のデータ")

    # ステップ 3: Web ページ生成
    print("\n🌐 ステップ 3/3: 検索 Web ページを生成中...")
    print("─" * 60)

    html = generate_html(ramen_data)

    output_file = OUTPUT_DIR / "index.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"   生成完了: {output_file}")

    # 完了サマリー
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " ✅ 処理完了 ".center(56) + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    print(f"📊 収集結果:")
    print(f"   - 店舗数: {shops_count} 店")

    if ramen_data.get('shops'):
        areas = {}
        for shop in ramen_data['shops']:
            area = shop.get('area', '不明')
            areas[area] = areas.get(area, 0) + 1

        print(f"   - エリア: {', '.join(f'{a}({c})' for a, c in sorted(areas.items(), key=lambda x: -x[1])[:5])}")

    print()
    print(f"📁 出力ファイル:")
    print(f"   - JSON: {DATA_FILE}")
    print(f"   - HTML: {output_file}")
    print()
    print("🖥️  Web ページを表示するには:")
    print(f"   cd {OUTPUT_DIR} && python -m http.server 8000")
    print("   ブラウザで http://localhost:8000 を開いてください")
    print()

    return 0


def run_web_generation_only():
    """
    既存の JSON データから Web ページのみを生成
    """
    print()
    print("🌐 既存データから Web ページを生成")
    print("─" * 60)

    if not DATA_FILE.exists():
        print(f"❌ データファイルが見つかりません: {DATA_FILE}")
        print("   先にデータ収集を実行してください。")
        return 1

    import json
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    html = generate_html(data)

    output_file = OUTPUT_DIR / "index.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Web ページを生成しました: {output_file}")
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="渋谷区ラーメン店データ収集・Web生成エージェント"
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

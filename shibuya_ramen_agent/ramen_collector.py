#!/usr/bin/env python3
"""
渋谷区ラーメン店データ収集エージェント

Claude Agent SDK を使用して渋谷区のラーメン店情報を Web から収集し、
JSON 形式で保存するエージェント
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Any

from claude_agent_sdk import query, ClaudeAgentOptions


# 出力ディレクトリ
OUTPUT_DIR = Path(__file__).parent.parent / "output"

# エージェントへのシステムプロンプト
SYSTEM_PROMPT = """あなたは渋谷区のラーメン店情報を収集する専門エージェントです。

## タスク
渋谷区にあるラーメン店の情報を収集し、構造化されたJSON形式で出力してください。

## 収集する情報
各ラーメン店について以下の情報を収集してください：
- name: 店名
- address: 住所
- area: エリア（渋谷、恵比寿、代官山、原宿、表参道、神泉など）
- genre: ラーメンの種類（醤油、味噌、塩、豚骨、家系、二郎系、つけ麺など）
- rating: 評価（5点満点、不明な場合は null）
- price_range: 価格帯（例: "800-1200円"）
- specialties: 看板メニューや特徴（リスト形式）
- hours: 営業時間
- closed_days: 定休日
- url: 公式サイトまたは情報源URL
- description: 店舗の説明や特徴

## 収集方法
1. WebSearch ツールを使用して「渋谷区 ラーメン」「渋谷 ラーメン 人気」などのキーワードで検索
2. 検索結果から有名店や人気店を特定
3. WebFetch ツールを使用して各店舗の詳細情報を収集
4. 最低20店舗以上の情報を収集することを目標とする

## 出力形式
最終的に以下のJSON形式で結果を出力してください：

```json
{
  "collected_at": "YYYY-MM-DD HH:MM:SS",
  "total_count": 数値,
  "shops": [
    {
      "name": "店名",
      "address": "住所",
      "area": "エリア",
      "genre": "ジャンル",
      "rating": 4.5,
      "price_range": "800-1200円",
      "specialties": ["特製ラーメン", "チャーシュー麺"],
      "hours": "11:00-23:00",
      "closed_days": "月曜日",
      "url": "https://...",
      "description": "説明文"
    }
  ]
}
```

## 重要な注意事項
- 実在する店舗の情報のみを収集してください
- 情報が不明な場合は null を設定してください
- 閉店した店舗は含めないでください
- 情報源を明記してください

最後に、収集した全データを上記の JSON 形式で出力してください。
JSON は ```json と ``` で囲んで出力してください。
"""


async def collect_ramen_data() -> dict[str, Any]:
    """
    渋谷区のラーメン店データを収集するエージェントを実行
    """
    print("=" * 60)
    print("🍜 渋谷区ラーメン店データ収集エージェント")
    print("=" * 60)
    print()

    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        allowed_tools=["WebSearch", "WebFetch"],
        permission_mode='acceptEdits',
        max_turns=50,  # 十分な探索を許可
    )

    collected_text = ""

    print("📡 エージェントを起動してデータを収集中...")
    print("-" * 60)

    async for message in query(
        prompt="""渋谷区のラーメン店情報を収集してください。

以下の手順で進めてください：
1. まず「渋谷区 ラーメン ランキング」「渋谷 ラーメン 人気」で検索して有名店をリストアップ
2. 各エリア（渋谷、恵比寿、代官山、原宿、表参道）ごとにも検索
3. 見つかった店舗の詳細情報を WebFetch で収集
4. 最終的に JSON 形式で出力

できるだけ多くの店舗情報（20店舗以上）を収集してください。""",
        options=options
    ):
        # メッセージの処理
        if hasattr(message, 'content'):
            for block in message.content:
                if hasattr(block, 'text'):
                    text = block.text
                    print(text)
                    collected_text += text + "\n"
                elif hasattr(block, 'name'):
                    # ツール使用の表示
                    print(f"\n🔧 Tool: {block.name}")
        elif hasattr(message, 'type') and message.type == 'result':
            # ツール結果（簡略表示）
            if hasattr(message, 'content'):
                result_preview = str(message.content)[:200]
                print(f"   ↳ {result_preview}...")

    print("-" * 60)
    print("✅ データ収集完了")
    print()

    # JSON を抽出
    ramen_data = extract_json_from_text(collected_text)

    return ramen_data


def extract_json_from_text(text: str) -> dict[str, Any]:
    """
    テキストから JSON データを抽出
    """
    import re

    # ```json ... ``` パターンを探す
    json_pattern = r'```json\s*([\s\S]*?)\s*```'
    matches = re.findall(json_pattern, text)

    if matches:
        # 最後の JSON ブロックを使用（最終結果のはず）
        try:
            return json.loads(matches[-1])
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON パースエラー: {e}")

    # フォールバック：{...} パターンを探す
    brace_pattern = r'\{[\s\S]*"shops"[\s\S]*\}'
    brace_matches = re.findall(brace_pattern, text)

    if brace_matches:
        for match in reversed(brace_matches):
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue

    # データが見つからない場合は空のテンプレートを返す
    return {
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_count": 0,
        "shops": [],
        "error": "JSON データの抽出に失敗しました"
    }


def save_data(data: dict[str, Any], filename: str = "ramen_shops.json") -> Path:
    """
    データを JSON ファイルに保存
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"💾 データを保存しました: {filepath}")
    return filepath


async def main():
    """
    メイン実行関数
    """
    try:
        # データ収集
        ramen_data = await collect_ramen_data()

        # データ保存
        save_data(ramen_data)

        # 統計表示
        print()
        print("=" * 60)
        print("📊 収集結果サマリー")
        print("=" * 60)
        print(f"収集日時: {ramen_data.get('collected_at', 'N/A')}")
        print(f"店舗数: {ramen_data.get('total_count', len(ramen_data.get('shops', [])))}")

        if ramen_data.get('shops'):
            # エリア別集計
            areas = {}
            genres = {}
            for shop in ramen_data['shops']:
                area = shop.get('area', '不明')
                genre = shop.get('genre', '不明')
                areas[area] = areas.get(area, 0) + 1
                genres[genre] = genres.get(genre, 0) + 1

            print("\n🗺️ エリア別:")
            for area, count in sorted(areas.items(), key=lambda x: -x[1]):
                print(f"   {area}: {count}店")

            print("\n🍜 ジャンル別:")
            for genre, count in sorted(genres.items(), key=lambda x: -x[1]):
                print(f"   {genre}: {count}店")

        print()

    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

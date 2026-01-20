#!/usr/bin/env python3
"""
AI ニュース収集エージェント

Claude Agent SDK を使用して AI 関連ニュースを Web から収集し、
JSON 形式で保存するエージェント
"""

import asyncio
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Any

from claude_agent_sdk import query, ClaudeAgentOptions


# 出力ディレクトリ
OUTPUT_DIR = Path(__file__).parent.parent / "docs" / "ai_news_agent"

# エージェントへのシステムプロンプト
SYSTEM_PROMPT = """あなたは AI 関連ニュースを収集する専門エージェントです。

## タスク
最新の AI 関連ニュースを収集し、構造化された JSON 形式で出力してください。

## 収集対象カテゴリ
以下のカテゴリに関するニュースを収集してください：
- LLM: 大規模言語モデル（GPT、Claude、Gemini、LLaMA 等）
- Computer Vision: 画像認識、動画生成、マルチモーダル AI
- Robotics: ロボティクス、自律システム
- AI Ethics: AI 倫理、安全性、規制
- AI Startups: AI スタートアップ、資金調達
- Research: 学術研究、論文、技術革新
- Industry: 企業の AI 活用、製品発表
- Regulation: 政府の AI 規制、政策

## 収集する情報
各ニュース記事について以下の情報を収集してください：
- title: 記事タイトル
- source: 情報源（TechCrunch, The Verge, VentureBeat, Wired, MIT Tech Review 等）
- category: 上記カテゴリのいずれか
- date: 公開日（YYYY-MM-DD 形式）
- summary: 記事の要約（2-3文）
- url: 記事の URL
- importance: 重要度（high, medium, low）
  - high: 業界に大きな影響、メジャーな発表
  - medium: 注目すべきニュース、興味深い開発
  - low: マイナーなアップデート、ニッチな話題
- tags: 関連キーワード（例: ["OpenAI", "GPT-5", "API"]）

## 収集方法
1. WebSearch ツールを使用して「AI news」「artificial intelligence」「LLM news」などで検索
2. 主要なテック系メディア（TechCrunch, The Verge, VentureBeat, Wired 等）の最新記事を探す
3. WebFetch ツールを使用して記事の詳細を確認
4. 最低15記事以上の情報を収集することを目標とする

## 出力形式
最終的に以下の JSON 形式で結果を出力してください：

```json
{
  "collected_at": "YYYY-MM-DD HH:MM:SS",
  "total_count": 数値,
  "articles": [
    {
      "title": "記事タイトル",
      "source": "TechCrunch",
      "category": "LLM",
      "date": "2026-01-20",
      "summary": "要約...",
      "url": "https://...",
      "importance": "high",
      "tags": ["OpenAI", "GPT-5"]
    }
  ]
}
```

## 重要な注意事項
- 実在する記事の情報のみを収集してください
- 情報が不明な場合は null を設定してください
- できるだけ最新のニュース（過去1週間以内）を優先してください
- 英語・日本語両方のソースから収集可能です

最後に、収集した全データを上記の JSON 形式で出力してください。
JSON は ```json と ``` で囲んで出力してください。
"""


async def collect_news_data() -> dict[str, Any]:
    """
    AI ニュースデータを収集するエージェントを実行
    """
    print("=" * 60)
    print("AI News Aggregator - ニュース収集エージェント")
    print("=" * 60)
    print()

    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        allowed_tools=["WebSearch", "WebFetch"],
        permission_mode='acceptEdits',
        max_turns=50,
    )

    collected_text = ""

    print("エージェントを起動してニュースを収集中...")
    print("-" * 60)

    async for message in query(
        prompt="""最新の AI 関連ニュースを収集してください。

以下の手順で進めてください：
1. まず「AI news 2026」「LLM news」「artificial intelligence latest」で検索
2. TechCrunch, The Verge, VentureBeat, Wired, MIT Technology Review などの主要メディアを優先
3. カテゴリ別（LLM, Computer Vision, Robotics, AI Ethics, AI Startups, Research, Industry, Regulation）にバランスよく収集
4. 重要度が高い記事を優先的に収集
5. 最終的に JSON 形式で出力

できるだけ多くの記事情報（15記事以上）を収集してください。""",
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
                    print(f"\n[Tool: {block.name}]")
        elif hasattr(message, 'type') and message.type == 'result':
            # ツール結果（簡略表示）
            if hasattr(message, 'content'):
                result_preview = str(message.content)[:200]
                print(f"   -> {result_preview}...")

    print("-" * 60)
    print("データ収集完了")
    print()

    # JSON を抽出
    news_data = extract_json_from_text(collected_text)

    return news_data


def extract_json_from_text(text: str) -> dict[str, Any]:
    """
    テキストから JSON データを抽出
    """
    # ```json ... ``` パターンを探す
    json_pattern = r'```json\s*([\s\S]*?)\s*```'
    matches = re.findall(json_pattern, text)

    if matches:
        # 最後の JSON ブロックを使用（最終結果のはず）
        try:
            return json.loads(matches[-1])
        except json.JSONDecodeError as e:
            print(f"JSON パースエラー: {e}")

    # フォールバック：{...} パターンを探す
    brace_pattern = r'\{[\s\S]*"articles"[\s\S]*\}'
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
        "articles": [],
        "error": "JSON データの抽出に失敗しました"
    }


def save_data(data: dict[str, Any], filename: str = "ai_news.json") -> Path:
    """
    データを JSON ファイルに保存
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"データを保存しました: {filepath}")
    return filepath


async def main():
    """
    メイン実行関数
    """
    try:
        # データ収集
        news_data = await collect_news_data()

        # データ保存
        save_data(news_data)

        # 統計表示
        print()
        print("=" * 60)
        print("収集結果サマリー")
        print("=" * 60)
        print(f"収集日時: {news_data.get('collected_at', 'N/A')}")
        print(f"記事数: {news_data.get('total_count', len(news_data.get('articles', [])))}")

        if news_data.get('articles'):
            # カテゴリ別集計
            categories = {}
            sources = {}
            importance_counts = {}
            for article in news_data['articles']:
                cat = article.get('category', '不明')
                source = article.get('source', '不明')
                imp = article.get('importance', '不明')
                categories[cat] = categories.get(cat, 0) + 1
                sources[source] = sources.get(source, 0) + 1
                importance_counts[imp] = importance_counts.get(imp, 0) + 1

            print("\nカテゴリ別:")
            for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
                print(f"   {cat}: {count}件")

            print("\nソース別:")
            for source, count in sorted(sources.items(), key=lambda x: -x[1])[:5]:
                print(f"   {source}: {count}件")

            print("\n重要度別:")
            for imp, count in sorted(importance_counts.items()):
                print(f"   {imp}: {count}件")

        print()

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

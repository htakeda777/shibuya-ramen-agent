# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

AI News Aggregator - Claude Agent SDK を使用して AI 関連ニュースを Web から自動収集し、検索可能な HTML ページを生成するツール。

## コマンド

```bash
# 仮想環境のセットアップ
python -m venv venv
source venv/bin/activate
pip install claude-agent-sdk

# フル実行（データ収集 + Web生成）
python main.py

# Web生成のみ（既存JSONデータから）
python main.py --web-only

# 個別実行
python news_collector.py   # データ収集のみ
python generate_web.py     # Web生成のみ

# ローカルサーバーでWebページを確認
cd ../docs && python -m http.server 8000
# http://localhost:8000/ai_news_agent/
```

## アーキテクチャ

```
main.py                    # エントリーポイント、パイプライン統合
    ↓
news_collector.py          # Claude Agent SDK でデータ収集
    ├─ WebSearch ツール     # AI ニュースを検索
    └─ WebFetch ツール      # 記事詳細情報取得
    ↓
docs/ai_news_agent/ai_news.json  # 構造化されたニュースデータ
    ↓
generate_web.py            # HTML + JS 生成
    ↓
docs/ai_news_agent/index.html    # 検索・フィルタリング機能付きWebページ
```

## 主要コンポーネント

### news_collector.py
- `collect_news_data()`: 非同期エージェント実行、WebSearch/WebFetch でニュース収集
- `SYSTEM_PROMPT`: エージェントへの指示（カテゴリ、重要度、JSON出力形式を定義）
- `extract_json_from_text()`: エージェント出力から JSON を抽出（フォールバック処理付き）
- 収集目標: 最低15記事（`max_turns=50` で十分な探索を許可）

### generate_web.py
- `generate_html()`: JSON から完全な HTML ページを生成
- ダークテーマ UI（Primary: #00d4ff シアン）
- JavaScript で検索・フィルタリング・ソート機能を実装
- レスポンシブデザイン（768px以下でシングルカラム）

## データ構造

ニュースデータの JSON スキーマ:
```json
{
  "collected_at": "2026-01-20 14:30:00",
  "total_count": 25,
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

## カテゴリ

- **LLM**: 大規模言語モデル（GPT、Claude、Gemini、LLaMA 等）
- **Computer Vision**: 画像認識、動画生成、マルチモーダル AI
- **Robotics**: ロボティクス、自律システム
- **AI Ethics**: AI 倫理、安全性、規制
- **AI Startups**: AI スタートアップ、資金調達
- **Research**: 学術研究、論文、技術革新
- **Industry**: 企業の AI 活用、製品発表
- **Regulation**: 政府の AI 規制、政策

## 重要度レベル

- **high**: 業界に大きな影響、メジャーな発表
- **medium**: 注目すべきニュース、興味深い開発
- **low**: マイナーなアップデート、ニッチな話題

## 設定変更ポイント

- **収集記事数**: `news_collector.py` の `SYSTEM_PROMPT` 内「15記事以上」を変更
- **カテゴリ追加**: `SYSTEM_PROMPT` 内のカテゴリリストを変更
- **最大ターン数**: `ClaudeAgentOptions` の `max_turns` を調整
- **デザイン変更**: `generate_web.py` の CSS 変数（`:root`）を編集

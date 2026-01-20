# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

渋谷区ラーメン店データ収集エージェント - Claude Agent SDK を使用して Web からラーメン店情報を自動収集し、検索可能な HTML ページを生成するツール。

## コマンド

```bash
# 仮想環境のアクティベート
source venv/bin/activate

# フル実行（データ収集 + Web生成）
python main.py

# Web生成のみ（既存JSONデータから）
python main.py --web-only

# 個別実行
python ramen_collector.py   # データ収集のみ
python generate_web.py      # Web生成のみ

# ローカルサーバーでWebページを確認
cd ../docs && python -m http.server 8888
```

## アーキテクチャ

```
main.py                    # エントリーポイント、パイプライン統合
    ↓
ramen_collector.py         # Claude Agent SDK でデータ収集
    ├─ WebSearch ツール     # 「渋谷区 ラーメン」等で検索
    └─ WebFetch ツール      # 店舗詳細情報取得
    ↓
docs/ramen_shops.json      # 構造化された店舗データ
    ↓
generate_web.py            # HTML + JS 生成
    ↓
docs/index.html            # 検索・フィルタリング機能付きWebページ
```

## 主要コンポーネント

### ramen_collector.py
- `collect_ramen_data()`: 非同期エージェント実行、WebSearch/WebFetch で店舗情報収集
- `SYSTEM_PROMPT`: エージェントへの指示（収集フィールド、JSON出力形式を定義）
- `extract_json_from_text()`: エージェント出力から JSON を抽出（フォールバック処理付き）
- 収集目標: 最低20店舗（`max_turns=50` で十分な探索を許可）

### generate_web.py
- `generate_html()`: JSON から完全な HTML ページを生成
- JavaScript で検索・フィルタリング・ソート機能を実装
- レスポンシブデザイン（768px以下でシングルカラム）

## データ構造

店舗データの JSON スキーマ:
```json
{
  "name": "店名",
  "address": "住所",
  "area": "エリア（渋谷、恵比寿等）",
  "genre": "ジャンル（醤油、豚骨等）",
  "rating": 4.5,
  "price_range": "800-1200円",
  "specialties": ["メニュー1", "メニュー2"],
  "hours": "営業時間",
  "closed_days": "定休日",
  "url": "情報源URL",
  "description": "説明文"
}
```

## 設定変更ポイント

- **収集店舗数**: `ramen_collector.py` の `SYSTEM_PROMPT`（46行目）と `query()` プロンプト（114行目）の「20店舗以上」を変更
- **対象エリア**: `SYSTEM_PROMPT` 内のエリアリストを変更
- **最大ターン数**: `ClaudeAgentOptions` の `max_turns` を調整

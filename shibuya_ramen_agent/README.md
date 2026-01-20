# 渋谷区ラーメン店データ収集エージェント

Claude Agent SDK を使用して渋谷区のラーメン店情報を自動収集し、検索可能な Web ページを生成するエージェントです。

## 機能

- 🔍 **自動データ収集**: Claude Agent SDK の WebSearch/WebFetch ツールを使用して、Web からラーメン店情報を収集
- 📊 **JSON 出力**: 構造化されたデータを JSON 形式で保存
- 🌐 **検索 Web 生成**: HTML + JavaScript による検索・フィルタリング機能付きの Web ページを自動生成

## 収集する情報

各ラーメン店について以下の情報を収集します：

| フィールド | 説明 |
|-----------|------|
| name | 店名 |
| address | 住所 |
| area | エリア（渋谷、恵比寿、代官山など） |
| genre | ラーメンの種類（醤油、味噌、豚骨など） |
| rating | 評価（5点満点） |
| price_range | 価格帯 |
| specialties | 看板メニュー・特徴 |
| hours | 営業時間 |
| closed_days | 定休日 |
| url | 情報源 URL |
| description | 店舗の説明 |

## インストール

```bash
# リポジトリのクローン（またはファイルをコピー）
cd shibuya_ramen_agent

# 依存パッケージのインストール
pip install -r requirements.txt
```

## 使い方

### 基本的な使い方（データ収集 + Web 生成）

```bash
python main.py
```

このコマンドで以下の処理が実行されます：
1. Web からラーメン店情報を収集
2. `output/ramen_shops.json` にデータを保存
3. `output/index.html` に検索 Web ページを生成

### Web ページのみ再生成

既存の JSON データから Web ページのみを再生成する場合：

```bash
python main.py --web-only
```

### 個別スクリプトの実行

```bash
# データ収集のみ
python ramen_collector.py

# Web 生成のみ
python generate_web.py
```

## Web ページの表示

生成された Web ページを表示するには：

```bash
cd output
python -m http.server 8000
```

ブラウザで http://localhost:8000 を開いてください。

## 出力ファイル

```
output/
├── ramen_shops.json   # 収集したラーメン店データ（JSON）
└── index.html         # 検索可能な Web ページ
```

## プロジェクト構成

```
shibuya_ramen_agent/
├── main.py              # 統合実行スクリプト
├── ramen_collector.py   # データ収集エージェント
├── generate_web.py      # Web ページ生成スクリプト
├── requirements.txt     # 依存パッケージ
└── README.md            # このファイル
```

## 技術スタック

- **Claude Agent SDK**: Anthropic の公式エージェント SDK
- **WebSearch**: Web 検索ツール
- **WebFetch**: Web ページ取得ツール
- **HTML/CSS/JavaScript**: フロントエンド

## カスタマイズ

### 収集対象の変更

`ramen_collector.py` の `SYSTEM_PROMPT` を編集して、収集する情報や対象エリアを変更できます。

### Web デザインの変更

`generate_web.py` の `generate_html()` 関数内の CSS を編集して、デザインをカスタマイズできます。

## 注意事項

- データ収集には API 呼び出しが発生するため、適切な API キーの設定が必要です
- 収集されるデータは Web 上の公開情報に基づいています
- 店舗情報は変更される可能性があるため、最新情報は各店舗の公式サイトでご確認ください

## ライセンス

MIT License

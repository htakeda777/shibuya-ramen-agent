# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## リポジトリ概要

Claude Agent SDKを使用したエージェントプロジェクト集。GitHub Pagesでデプロイ。

## コマンド

```bash
# shibuya_ramen_agent の実行
cd shibuya_ramen_agent
source venv/bin/activate
python main.py              # データ収集 + Web生成
python main.py --web-only   # Web生成のみ

# ローカル確認
cd docs && python -m http.server 8000

# デプロイ（GitHub Pagesは docs/ を自動公開）
git add docs/ && git commit -m "Update" && git push
```

## 構造

```
/
├── shibuya_ramen_agent/    # ラーメン店データ収集エージェント（詳細は内部のCLAUDE.md参照）
│   ├── main.py             # エントリーポイント
│   ├── ramen_collector.py  # Claude Agent SDK でデータ収集
│   └── generate_web.py     # HTML生成
│
└── docs/                   # GitHub Pages公開ディレクトリ
    ├── index.html          # プロジェクト一覧ページ
    └── shibuya_ramen_agent/
        ├── index.html      # ラーメン店検索アプリ
        └── ramen_shops.json
```

## GitHub Pages

- URL: https://htakeda777.github.io/shibuya-ramen-agent/
- ソース: `master` ブランチの `/docs` フォルダ
- 新規プロジェクト追加時: `docs/<project>/` にフォルダ作成し、`docs/index.html` にリンク追加

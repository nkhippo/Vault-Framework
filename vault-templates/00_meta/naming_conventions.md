---
created: 2026-07-13 21:43:00+09:00
keywords:
- naming
- conventions
- vault
- vault-mcp
- framework
- hashicorp-collision
status: published
summary: Vault 内のファイル・ディレクトリの命名規約と、Vault-Framework が推奨する 3 リポジトリ命名スキーム。名前衝突への対処も含む。
tags:
- framework
- vault-templates
- meta
title: 命名規約
type: knowledge
updated: 2026-07-13 21:43:00+09:00
id: pj-2026-07-13-6106
aliases:
- pj-2026-07-13-6106
---

## Summary

Vault 内のファイル・ディレクトリの命名規約と、Vault-Framework が推奨する外部リポジトリ命名スキーム(Vault*)を定義。

## ファイル名

形式: `<日付>_<kebab-case-slug>.md`

- 日付: `YYYY-MM-DD`
- スラグ: 英小文字 + ハイフン、30 字以内目安
- 例: `2026-07-12_cloudflare-vs-cloudrun.md`

### 例外(日付なしで可)

`30_projects/<RepoName>/` 内の恒常更新ファイル:
- `README.md`
- `design-decisions.md`
- `open-questions.md`
- `roadmap.md`

`50_self/diary/` は `YYYY-MM-DD.md`(スラグなし、日付のみ)。

## ディレクトリ名

### トップレベル
- 形式: `<数字プレフィックス>_<snake_case>` (例: `10_chat_logs`)
- 数字は 10 刻み(将来挿入余地を残す)

### 中階層
- 年月: `YYYY/MM/`
- プロジェクト名: **GitHub リポジトリ名と完全一致**
- アイデア slug: `kebab-case`

## 数字プレフィックスの意味

- `00_` メタ
- `10_` 生ログ(または captures)
- `20_` 成果物(note)
- `30_` プロジェクト
- `40_` 汎用ナレッジ
- `50_` 個人的な記録
- `90_` 一時置き場

## アイデア slug の命名

- 英小文字 + ハイフン
- 3 語以内目安
- リポジトリ化時に GitHub リポジトリ名(PascalCase)に変わることを想定して、意味が伝わる名前にする
- 例: `pronunciation-video-analyzer` → 昇格後 `Pronunciation-Video-Analyzer`

## Vault-Framework 推奨のリポジトリ命名スキーム

Vault-Framework は 3 リポジトリ構成を推奨する。導入者は自分の GitHub アカウントで以下を作成:

| 対象 | 推奨リポジトリ名 | 説明 |
|---|---|---|
| vault 本体 | `Vault` | Chat 集約とドキュメントの保管 |
| MCP サーバ | `Vault-MCP` | Cloudflare Workers デプロイ、vault リポジトリを操作 |
| Framework | (直接 Fork or 参照) | `nkhippo/Vault-Framework` を参照 |

### MCP コネクタ名の表記ルール

- **表示名(Claude UI 上)**: 空白区切り + 大文字始まり(例: `Vault MCP`)
- **リポジトリ名**: ハイフン区切り + 大文字始まり(例: `Vault-MCP`)
- **Cloudflare Workers URL**: 小文字 + ハイフン(例: `vault-mcp.<your-subdomain>.workers.dev`)

同一の実体を指す 3 表記が並立する点に注意。ドキュメント内では文脈に応じて使い分ける。

## 名前衝突への対処

`Vault` は HashiCorp Vault 等の既存製品と衝突しやすい。Private 運用中は問題ないが、将来 Public 化する予定がある場合や、混乱を避けたい場合は以下の代替命名を推奨:

- `<YourName>-Vault`(例: `naoya-vault`)
- `Personal-Vault`
- `Knowledge-Vault`
- あなたのブランドや好みに合った名前

Skill と MCP の内部識別子(vault-manager 等)は変えずに、リポジトリ名だけカスタマイズすることが可能。その場合、MCP サーバの `wrangler.toml` の `GITHUB_REPO` 変数を新リポジトリ名に合わせる。

## 導入者への注意

上記の命名規則は Vault-Framework の推奨であり、絶対ではない。ただし以下 2 点は Skill との整合上、変更に注意:

1. トップレベル数字プレフィックスの位置(`00_meta/` の位置と存在)
2. `30_projects/<RepoName>/` の命名パターン(GitHub リポジトリ名との一致)

これら以外は自由にカスタマイズしてよい。

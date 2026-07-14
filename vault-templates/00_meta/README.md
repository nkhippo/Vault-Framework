---
created: 2026-07-13T21:41:00+09:00
keywords:
  - 00_meta
  - vault-templates
  - readme
  - framework
project: Vault-Framework
status: published
summary: vault-templates/00_meta/ の各ファイルの役割と、導入者がカスタマイズすべきファイルの説明。
tags:
  - framework
  - vault-templates
  - meta
title: vault-templates/00_meta/ README
type: knowledge
updated: 2026-07-13T21:41:00+09:00
---

## Summary

Vault の運用ルールを定義する AI 向けメタ情報を集約するディレクトリ。Claude は初回セッションでここを参照して、vault の構造・命名規約・統制語彙・操作規約を把握する。

## 各ファイルの役割

| ファイル | 役割 |
|---|---|
| `vault_structure.md` | vault トップレベルディレクトリの意味と役割 |
| `naming_conventions.md` | ファイル名・ディレクトリ名の規約 |
| `frontmatter_schema.md` | Front Matter の必須・任意フィールド定義 |
| `vocabulary.md` | type / status / tags / project の統制語彙 |
| `claude_operation_rules.md` | Claude が vault を操作する際の振る舞い規約 |
| `project_aliases.md` | プロジェクトのあいまい名解決辞書 |
| `project_instructions_vault.md` | Claude Projects の Vault Project 運用ルール |
| `templates/` | 各 type の Front Matter + 見出しテンプレート |

## Claude が読む順序

Skill `vault-manager` は必要に応じて以下の順序で読む(prompt caching への配慮):

1. `vault_structure.md`
2. `naming_conventions.md`
3. `vocabulary.md`
4. `frontmatter_schema.md`(必要時)
5. `project_aliases.md`(あいまい名解決時)
6. `templates/<type>.md`(保存時)

## メンテナンス

これらのファイルの多くは Naoya が Obsidian で直接編集できる。統制語彙(vocabulary)と命名規約(naming_conventions)を変更した際は Skill `vault-manager` の記述と矛盾しないよう確認する。矛盾した場合、vocabulary.md と命名規約が正典とみなされる(ただし Skill 側の MCP 接続失敗ルール・sensitive 引用禁止ルールは Skill 優先)。

## 導入者への注意

このディレクトリの多くはあなた(導入者)のドメイン固有情報(プロジェクト名、alias 等)を含みます。特に以下 3 ファイルは初回導入時に必ずカスタマイズする:

- `vocabulary.md` の `project` セクション
- `project_aliases.md` の全体
- `project_instructions_vault.md` のプレースホルダ

その他は初期状態のまま運用開始でき、必要に応じて後から拡張する。

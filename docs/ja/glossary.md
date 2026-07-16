---
audience: mixed
date: 2026-07-14
keywords:
- glossary
- 用語集
- terminology
related_adrs: []
related_specs: []
status: published
summary: Vault-Framework 全体で使われる用語の一覧。導入者や第三者がドキュメントを読む際に、独自用語の意味を素早く確認できるようにする。
title: 用語集
title_en: Glossary
type: reference
created: 2026-07-14 20:48:28+09:00
updated: 2026-07-14 20:48:28+09:00
id: pj-2026-07-13-bc88
aliases:
- pj-2026-07-13-bc88
---

## Summary

Vault-Framework 全体で使われる用語の一覧。導入者や第三者がドキュメントを読む際に、独自用語の意味を素早く確認できるようにする。

## 用語一覧

### Vault(ボールト)

個人のナレッジベース兼 Chat 集約先となる GitHub リポジトリ。`nkhippo/Vault` がその実運用インスタンス。Markdown ファイルと Front Matter で構造化されたデータを保持する。

### Vault-MCP

Vault を MCP(Model Context Protocol)経由で操作するためのサーバ実装。Cloudflare Workers 上にデプロイされ、GitHub API を介して Vault リポジトリの読み書きを行う。

### Vault-Framework

Vault と Vault-MCP の運用知見を一般化した公開用フレームワーク。このリポジトリ自体を指す。設計思想、Skill、テンプレート、導入手順を含む。

### Skill(vault-manager)

Claude Skills にアップロードする `SKILL.md`。Claude の振る舞いロジック(保存判断、参照判断、あいまい名解決等)を定義する。

### MCP(Model Context Protocol)

Anthropic が定義する、AI モデルが外部ツールやデータソースと連携するためのプロトコル。Vault-MCP はこのプロトコルに準拠したサーバ実装。

### Front Matter

Markdown ファイルの先頭に置く YAML 形式のメタデータブロック。`title`、`type`、`status`、`tags` 等のフィールドを含む。

### 統制語彙(Controlled Vocabulary)

`type`、`status`、`tags`、`project` フィールドで使用が許可された値の集合。表記揺れを防ぎ、AI の判定精度を上げるために管理される。

### 参照レベル(Reference Level)

Skill が vault を参照する深度を 0〜4 の 5 段階で表現したもの。Level 0(参照しない)がデフォルトで、必要に応じて段階的に深く参照する。

### あいまい名解決(Ambiguous Name Resolution)

ユーザーが機能表現や通称でプロジェクト・アプリを指した際に、Skill が正式なリポジトリ名を特定するフロー。`project_aliases.md` を参照して行う。

### handoff(ハンドオフ)

各プロジェクトの「直近の状態」を記録する `current-state.md` と、詳細な変更履歴を記録する `recent-changes/` ディレクトリの総称。新しい Chat セッションでのキャッチアップを容易にする。

### 保守運用 4 レベル(Four-Level Maintenance)

Vault のエントロピー(統制語彙の揺らぎ、リンク切れ等)に対処するための、頻度と担当が異なる 4 段階の保守運用フロー(Level 1〜4)。

### 抽象生成(Abstract Generation)

具体的な chat_log から、ADR・spec・rejected-alternatives のような抽象的なドキュメントを生成するプロセス。保守運用 4 レベルとは独立した並行運用。

### ADR(Architecture Decision Record)

意思決定記録。「何を」「なぜ」決定したかを構造化して記録する形式。Vault-Framework の `docs/ja/decisions/` 配下に蓄積されている。

### rejected-alternatives(却下案)

意思決定の過程で検討されたが採用されなかった選択肢を記録するドキュメント。ADR と対になって、なぜその案が採用されなかったかを明示する。

### スラグ(Slug)

ファイル名の一部として使う、英語の kebab-case で表現された識別子。例: `mcp-platform-selection`。

### kebab-case

単語をハイフンでつなぐ命名記法(例: `file-naming`)。Vault-Framework のスラグやディレクトリ名で使用される。

### sensitive フィールド

Front Matter の boolean フィールド。`true` の場合、そのファイルの内容は他コンテキストで引用・要約しない扱いになる(50_self/ 配下のファイルはデフォルトで `true`)。

### Cursor 委譲

複数ファイルにまたがる整合性が必要な作業を、Claude が直接行わず、Cursor(コーディングエージェント)向けの指示書を作成して委譲すること。

### GitHub-as-a-Backend

Vault-Framework の中核思想。個人ナレッジベースの正典データストアとして GitHub リポジトリを採用する設計判断([Philosophy](./philosophy.md) 参照)。

### 3 層構造(Skill・Project・Vault)

Vault-Framework の運用アーキテクチャ。Skill(振る舞いロジック)、Project Instructions(最小限のポインタ)、Vault(運用ルールの正典)の 3 層に責務を分離する([Architecture](./architecture.md) 参照)。

## 関連

- [Philosophy: GitHub-as-a-Backend](./philosophy.md)
- [Architecture: Skill・Project・Vault の 3 層](./architecture.md)
- [naming-conventions.md: 命名規約の思想](./naming-conventions.md)
- [maintenance-guide.md: 保守運用ガイド](./maintenance-guide.md)

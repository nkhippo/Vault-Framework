---
created: 2026-07-13 21:45:00+09:00
keywords:
  - vocabulary
  - controlled-vocabulary
  - type
  - tags
  - status
  - project
  - 統制語彙
status: published
summary: Front Matter の統制語彙。type、status、tags、project、および backlog_item(kind/state/assignee)の定義と拡張手順。プレースホルダ形式で導入者がカスタマイズする部分を明示。
tags:
  - framework
  - vault-templates
  - meta
  - vocabulary
title: 統制語彙
type: knowledge
updated: 2026-07-18T00:42:30+09:00
---

## Summary

Front Matter の `type` / `status` / `tags` / `project` はここで定義された値のみ使用する。
新規追加時は必ずこのファイルを更新してから使う。

## Skill との関係

このファイルは Skill `vault-manager` からも参照される正典。Skill と vocabulary.md の記述が矛盾したら vocabulary.md を正とする。新規 tag / type / project を使う前に必ずこのファイルに追加する。

## type(排他的、1 ファイル 1 つ)

### コンテンツ系

- `chat_log` - Claude との会話の生ログ
- `note_draft` - note 記事の下書き
- `note_published` - note 公開済み清書版
- `project_idea` - リポジトリ化前のアイデア段階の検討記録
- `project_design` - リポジトリ化済みプロジェクトの設計・意思決定記録
- `knowledge` - 汎用ナレッジ
- `inbox` - 未分類

### 個人系(50_self/ 配下でのみ使用)

- `diary` - 日々の記録(日記)。デフォルトで `sensitive: true`
- `reflection` - 週次・月次の振り返り。デフォルトで `sensitive: true`
- `goal` - 目標・意向の記録。デフォルトで `sensitive: true`

### 運用系

- `handoff` - handoff 領域のファイル(current-state.md や recent-changes/)
- `template` - 00_meta/templates/ 配下の雛形ファイル
- `report` - 作業実行レポート
- `project_readme` - プロジェクト直下 README.md(例: `30_projects/<your-project>/README.md`)
- `backlog_item` - 課題・タスクノード(詳細は `templates/backlog_item.md` / `frontmatter_schema/backlog_item.md`)

## Backlog 系(type: backlog_item)

課題・タスクを「1 ノード 1 ファイル」で明示管理するための統制。スキーマ詳細は `frontmatter_schema/backlog_item.md`、雛形は `templates/backlog_item.md`、tag 運用ルールは `backlog_tags.md` を参照。

### kind(排他的、起票時確定・原則不変)

- `task` - 方針決定済み、実行段階
- `issue` - 方針未決、検討段階

### state(遷移可能)

- `open` - 起票時デフォルト、棚卸し対象
- `done` - 完了(`completed_at` を記録)
- `abandoned` - 方向転換で不要(`abandoned_at` / `abandoned_reason` を記録)

### assignee(必須、null 禁止)

- `owner` - あなた(Vault の持ち主)が握っている
- `cursor` - 実装 AI(Cursor 等)へ委譲済み

<!-- 導入者メモ: `owner` は自分の名前に置き換えてもよい(例: 自分の名前)。Cursor 以外の実装 AI を使う場合は値名を読み替える。 -->

### 参照・連携フィールド

- `derived_from_id` - 親 backlog item の id(課題 → タスク発展時)
- `related_ids` - 関連 item の id 配列(親子関係以外)
- `cursor_instruction_id` - 実装 AI 指示書への参照
- `github_issue` - `owner/repo#N` 形式

## status

### 通常の type 用
- `draft` - 書き始め、内容未固定
- `wip` - 進行中、参照時は注意
- `published` - 公開済み・確定済み
- `archived` - 過去のもの、参照歴史的価値のみ

### project_idea 専用(_ideas/ 配下でのみ使用)
- `incubating` - 温めているだけ
- `active` - 検討進行中、リポジトリ化目前
- `shelved` - 一時保留(復活の余地あり)
- `rejected` - やらないと決めた

## sensitive フィールド

`sensitive: true` の場合、Claude はそのファイルの本文を他コンテキストで引用・要約してはならない。
以下の type はデフォルトで `sensitive: true`:

- `diary`
- `reflection`
- `goal`

上記以外でも、あなた(導入者)の個人的トピック(健康、家族、財務、感情等)を含む場合は明示的に `sensitive: true` を付ける。

## project(30_projects/ 配下でのみ使用)

**導入者はここに自分の GitHub リポジトリ名(30_projects/ 配下のディレクトリ名と一致)を追加する。**

初期状態のプレースホルダ:

```
- <your-project-1>
- <your-project-2>
- <your-mcp-server>
```

<!-- 実際の記入例:
- <your-project>
- <your-project>
- <your-project>
- Vault
- Vault-MCP
- Vault-Framework
-->

新規リポジトリ作成時は必ずこの一覧に追加する。

## 日記・振り返り専用フィールド(任意)

`diary` および `reflection` type で使える任意フィールド:

### mood(気分)

- `great` - 最高
- `good` - 良い
- `neutral` - 普通
- `low` - 沈み気味
- `bad` - 悪い

### energy(エネルギー)

- `high` - 高い
- `medium` - 普通
- `low` - 低い

### weather(天気)

自由記述(晴れ、曇り、雨、雪 等)。

## tags(拡張可能、追加時はこのファイルを更新)

**導入者は必要に応じて自分のドメインの tag を追加する。**

### 基本セット(推奨)

**技術系**
`ai`, `mcp`, `cloudflare`, `github`, `obsidian`, `cursor`, `typescript`, `python`, `react`

**コンテンツ系**
`note-article`, `design-decision`, `retrospective`, `learning`

**個人系**
`self`, `diary`, `daily`, `reflection`, `goal`, `health`, `relation`

**メタ系**
`experimental`, `deprecated`, `important`, `sensitive`

### Backlog 系(backlog_item 用)

必須: `backlog`

主題系(汎用): `ui`, `ux`, `performance`, `docs`, `architecture`, `spec`

性質系: `bug-fix`, `enhancement`, `investigation`, `refactor`, `design`, `question`

状況系: `urgent`, `blocked`, `stalled`

<!-- ドメイン固有の主題 tag は導入者が追加(例: `pronunciation`, `vocabulary`)。追加は backlog_tags.md の追加ルールに従う。 -->

Backlog tag の追加は `backlog_tags.md` の追加ルールに従い、あなたの明示承認を前提とする。

### プロジェクト系(導入者が追加)

各プロジェクトに対応した tag を導入者が追加。命名規則: `kebab-case`、プロジェクト名の短縮形が使いやすい。

<!-- 実際の記入例:
- `ipa-drill` (<your-project> 用)
- `vct` (<your-project> 用)
- `vault-mcp` (Vault-MCP 用)
-->

## 拡張手順

新しい type / tag / project を導入したい場合:

1. このファイルの該当セクションに追加
2. Skill が読む可能性のあるファイル(project_aliases.md 等)にも反映
3. 過去ファイルへの遡及適用は不要(前方互換)

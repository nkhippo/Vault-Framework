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
summary: Front Matter の統制語彙。type、status、tags、project の定義と拡張手順。プレースホルダ形式で導入者がカスタマイズする部分を明示。
tags:
- framework
- vault-templates
- meta
- vocabulary
title: 統制語彙
type: knowledge
updated: 2026-07-13 21:45:00+09:00
id: pj-2026-07-13-24f6
aliases:
- pj-2026-07-13-24f6
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
- IPASoundDrill
- English-Vocab-Chunk-Trainer
- ThinkGrindAi
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

### プロジェクト系(導入者が追加)

各プロジェクトに対応した tag を導入者が追加。命名規則: `kebab-case`、プロジェクト名の短縮形が使いやすい。

<!-- 実際の記入例:
- `ipa-drill` (IPASoundDrill 用)
- `vct` (English-Vocab-Chunk-Trainer 用)
- `vault-mcp` (Vault-MCP 用)
-->

## 拡張手順

新しい type / tag / project を導入したい場合:

1. このファイルの該当セクションに追加
2. Skill が読む可能性のあるファイル(project_aliases.md 等)にも反映
3. 過去ファイルへの遡及適用は不要(前方互換)

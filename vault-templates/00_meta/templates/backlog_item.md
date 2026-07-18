---
keywords:
  - backlog
  - template
  - task
  - issue
  - meta
  - framework
status: published
summary: Backlog item(task / issue)を新規作成する時の雛形(骨格)。Claude は本テンプレを起点に FM を生成する。kind で task / issue を区別する。
tags:
  - framework
  - vault-templates
  - meta
  - backlog
  - template
title: Backlog Item Template
type: template
created: 2026-07-18T00:59:01+09:00
updated: 2026-07-18T00:59:01+09:00
---

## Summary

`type: backlog_item` の新規ノード作成テンプレ。task と issue を単一テンプレで扱い、`kind` フィールドで区別する。

## Template

以下を新規 backlog item のスケルトンとして使う。`< >` は Claude が置換する部分。

````markdown
---
id: <prefix>-YYYY-MM-DD-<4hex>  # prefix は path から infer(通常 pj-)
aliases: [<id と同じ値>]
title: <主題>
type: backlog_item
kind: task | issue  # 起票時に確定、原則不変
state: open  # open → done or abandoned
assignee: owner | cursor  # 必須、null 禁止
project: <RepoName or _life or _ideas/<slug>>  # 所属プロジェクト
created: <ISO8601 JST>
updated: <ISO8601 JST>
tags: [backlog, <主題 tag>, <性質 tag>, ...]  # 1-3 個目安、backlog_tags.md 参照
summary: <1-2 行の要約>

# 以下は状況に応じて追加

# derived_from_id: <parent-id>  # 派生元があれば(親課題→タスク遷移時等)
# related_ids: [<id>, ...]  # 関連するが親子関係にない他 item

# 実装レイヤに降りた時

# cursor_instruction_id: <path or id>  # 実装 AI(Cursor 等)委譲時
# github_issue: <owner/repo#N>  # GitHub Issue 起票時

# 完了・放棄

# completed_at: <ISO8601 JST>  # state=done 時
# abandoned_at: <ISO8601 JST>  # state=abandoned 時
# abandoned_reason: <短い理由>  # state=abandoned 時
---

## Summary

<主題を 2-3 段落で>

## Context

<なぜこの item が発生したか、背景>

## Definition of Done(kind: task の場合)

- <完了条件 1>
- <完了条件 2>
- ...

## Open questions(kind: issue の場合)

- <解決すべき問い 1>
- <解決すべき問い 2>
- ...

## History

- <YYYY-MM-DD>: <起票 or 遷移>(kind=<>, state=<>, assignee=<>)
- ...
````

## Path 命名規約

`30_projects/<Repo or _life or _ideas/<slug>>/backlog/YYYY-MM-DD_slug.md`

- `YYYY-MM-DD` は起票日(JST)
- `slug` は英数ハイフン、主題を短く(例: `ui-review`, `startup-latency`)
- 同日複数起票は slug で識別

## Kind と State の遷移

**Kind**: 起票時に決定、原則不変。

- `task`: 方針決定済み、実行段階
- `issue`: 方針未決、検討段階

課題 → タスクの発展時は **同ファイルの kind を書き換えない**、新規 backlog item を作成して `derived_from_id` で親を指す(H2 History で経緯記録)。

**State**: 遷移可能。

- `open`: 起票時デフォルト、棚卸し対象
- `done`: 完了、`completed_at` を記録
- `abandoned`: 方向転換で不要、`abandoned_at` と `abandoned_reason` を記録

## Assignee

- `owner`: あなた(Vault の持ち主)が握っている(検討中、実装中、確認中)
- `cursor`: 実装 AI(Cursor 等)へ委譲済み(`cursor_instruction_id` 存在)

<!-- 導入者メモ: `owner` は自分の名前に置き換えてもよい。実装 AI が Cursor 以外なら値名を読み替える。 -->

完了・放棄後は **最後の握り手を保持**(実装 AI が完了させたら `done` + `assignee: cursor` のまま残す)。

## 関連

- Tag 一覧: `backlog_tags.md`
- スキーマ: `frontmatter_schema/backlog_item.md`
- ID scheme / Front Matter: `naming_conventions.md` / `frontmatter_schema.md`

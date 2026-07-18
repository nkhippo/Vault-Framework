---
keywords:
  - backlog
  - schema
  - frontmatter
  - meta
  - framework
status: published
summary: type backlog_item の Front Matter スキーマ(骨格)。必須・不変・起票時・後追加フィールドを分類する。
tags:
  - framework
  - vault-templates
  - meta
  - backlog
  - schema
title: Front Matter スキーマ - backlog_item
type: knowledge
created: 2026-07-18T00:59:26+09:00
updated: 2026-07-18T00:59:26+09:00
---

## Summary

`type: backlog_item` の Front Matter 定義。task と issue を単一 type で扱い、`kind` で区別する。詳細な起票手順は `templates/backlog_item.md` を参照。

## 完全に不変(作成後変更禁止)

| Field | Type | Notes |
|---|---|---|
| `id` | string | `<prefix>-YYYY-MM-DD-<4hex>` |
| `type` | enum | 常に `backlog_item` |
| `kind` | enum | `task` \| `issue`(起票時確定、原則不変) |
| `created` | ISO8601 | 起票時刻 JST |
| `derived_from_id` | string (optional) | 親 item の id。設定したら変更しない |

## 原則不変(変更は例外的・明示判断)

| Field | Type | Notes |
|---|---|---|
| `title` | string | 主題。大幅変更より新規 item + derived_from_id を優先 |
| `project` | string | `RepoName` / `_life` / `_ideas/<slug>` |
| `aliases` | [string] | `aliases[0] == id` を維持 |

## 起票時に埋める

| Field | Type | Default / Notes |
|---|---|---|
| `state` | enum | `open` |
| `assignee` | enum | `owner` \| `cursor`(必須、null 禁止) |
| `summary` | string | 1-2 行 |
| `tags` | [string] | 必ず `backlog` を含み、`backlog_tags.md` から 1-3 個目安 |
| `updated` | ISO8601 | 起票時 = created |

## 後から追加・更新

| Field | Type | When |
|---|---|---|
| `related_ids` | [string] | 関連 item(親子でない) |
| `cursor_instruction_id` | string | 実装 AI 委譲時 |
| `github_issue` | string | `owner/repo#N` 形式、Issue 起票時 |
| `completed_at` | ISO8601 | `state=done` 時 |
| `abandoned_at` | ISO8601 | `state=abandoned` 時 |
| `abandoned_reason` | string | `state=abandoned` 時 |
| `updated` | ISO8601 | 内容変更のたび更新 |

## Kind / State 要約

- **Kind**: 不変。課題 → タスクは新規ノード + `derived_from_id`
- **State**: `open` → `done` / `abandoned`
- **Assignee**: 完了後も最後の握り手を保持

## 関連

- Template: `templates/backlog_item.md`
- Tags: `backlog_tags.md`
- 共通スキーマ概要: `frontmatter_schema.md`

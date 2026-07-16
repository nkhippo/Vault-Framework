---
id: pj-2026-07-17-cb46
aliases:
- pj-2026-07-17-cb46
title: Backlog System Overview
type: knowledge
status: published
created: 2026-07-17T02:05:00+09:00
updated: 2026-07-17T02:05:00+09:00
tags: [backlog, design, overview]
summary: Backlog システム(Chat 発生の課題・タスクを Vault で管理する仕組み)の全体設計。Phase 1a 実装、type/kind/state/assignee モデル、遷移ルール。
---

# Backlog System Overview

## Summary

Chat で発生する課題・タスクを Vault で構造化管理する仕組み。Vault が master、GitHub Issue は下流の実装レイヤ、Cursor は作業者。

## 設計原則

- **Vault が master**: 全ての課題・タスクは Vault の backlog item として起票、GitHub Issue や Cursor 指示書は派生
- **単一 type + kind 分離**: `type: backlog_item`、`kind: task | issue`
- **State 遷移**: `open → done | abandoned`(kind は不変)
- **Assignee 必須**: `naoya | cursor`、null 禁止、完了後も最後の握り手保持
- **課題→タスク発展は新規ノード**: `derived_from_id` で親を指す(同一ファイル内の kind 書き換えはしない)

## Kind と State

### Kind

- `task`: 方針決定済み、実行段階
- `issue`: 方針未決、検討段階(いわゆる「課題」)

### State

- `open`: 起票時デフォルト、棚卸し対象
- `done`: 完了、`completed_at` 記録
- `abandoned`: 方向転換で不要、`abandoned_at` と `abandoned_reason` 記録

### 遷移パターン

- 課題(issue, open)→ 検討 → 方針決定 → 新規 task item 起票 + 元 issue を done or "converted"
- 課題(issue, open)→ 不要判断 → abandoned
- タスク(task, open)→ 実行中に壁 → 新規 issue item 起票 + 元 task を open のまま blocked tag
- タスク(task, open)→ 完了 → done

## Placement

Phase 1a で確定:

- `30_projects/<Repo>/backlog/YYYY-MM-DD_slug.md`(通常プロジェクト)
- `30_projects/_life/backlog/`(対象リポジトリなしの life-scope)
- `30_projects/_ideas/incubating/<slug>/backlog/`(アイデア段階、必要時)

## Front Matter Schema

Phase 1a で確定した schema を参照: Vault の `00_meta/frontmatter_schema/backlog_item.md`

## Tag 管理

Vault の `00_meta/backlog_tags.md` に一覧集約。Naoya 承認なく新規 tag 追加禁止(氾濫防止)。

## Assignee モデル

- `naoya`: 検討中、実装中、確認中、または `_life/` に属する item
- `cursor`: Cursor 委譲済み(`cursor_instruction_id` あり)

完了・放棄後は **最後の握り手を保持**(Cursor が完了させたら done + assignee: cursor のまま残す)。

## GitHub Issue との関係

詳細は [[pj-2026-07-17-315f|GitHub Issue 境界]] 参照。

要点:
- Vault は master
- Cursor 委譲対象タスクは GitHub Issue に降ろす(`github_issue` フィールドで紐付け)
- Issue 完了時は Vault を手動 or Claude 補助で更新

## 既存資産との関係

詳細は [[pj-2026-07-17-7293|既存資産統合]] 参照。

要点:
- `open-questions.md`: 思いつきレベル、状態管理なし(単純箇条書き)
- `backlog/`: 状態管理あり、棚卸し対象、GitHub/Cursor と連携
- `roadmap.md`: 方針レベルの手段連なり、backlog と並列共存
- `design-decisions.md`: 決着済み方針、backlog item の議論結果として追記されうる

## 実運用フローの scope

本 doc は基盤・規約の記述のみ。以下は Phase 1c-1d で確定:

- 「今仕掛かりのタスクは?」等の参照 workflow(Phase 1c)
- 「保存して」時の backlog 判定 & 起票フロー(Phase 1d)
- 停滞検出(Phase 1d + vault-maintainer 対応)

## Related

- [[pj-2026-07-17-a9e4|Backlog docs index]]
- [[pj-2026-07-17-e9df|ADR-0018 backlog-system]]
- Vault 実装: `30_projects/*/backlog/`, `00_meta/backlog_tags.md`, `00_meta/templates/backlog_item.md`

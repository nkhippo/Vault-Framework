---
created: 2026-07-17 02:05:00+09:00
status: accepted
summary: Chat 発生の課題・タスクを構造化管理する Backlog System を Vault に導入する意思決定記録。Phase 1a-1b で基盤
  + 規約が確立。
tags:
- adr
- backlog
- phase-1
title: 0018 - Backlog System の導入
type: knowledge
updated: 2026-07-17 02:05:00+09:00
---

# ADR 0018: Backlog System の導入

## Context

あなた(導入者) が Chat で複数の相談を並行して行い、途中で「後で考えましょう」となる課題や、別 Chat に切り出したタスクが増えている。全体像が見えなくなりつつあり、次のような要求が生まれた:

- 各プロジェクトで残っている課題・仕掛かり中のタスクを一覧化したい
- 課題やタスクが対象プロジェクトの目的に沿っているか確認したい
- Chat で「これタスクとして残して」と言った時に structured に管理したい

## Decision

以下を採用する:

### Placement

- `30_projects/<Repo>/backlog/YYYY-MM-DD_slug.md`(通常プロジェクト)
- `30_projects/_life/backlog/`(人生軸の並列プロジェクト)
- `30_projects/_ideas/incubating/<slug>/backlog/`(アイデア段階)

### Model

- 単一 type `backlog_item`
- Kind: `task | issue`(不変)
- State: `open | done | abandoned`(遷移)
- Assignee: `owner | cursor`(必須、null 禁止)
- 課題→タスクの発展は **新規ノード**、`derived_from_id` で親指定

### GitHub Issue との関係

- Vault が master
- Task 化 + 対象 repo 確定 + Cursor 委譲対象で昇格
- Vault は open のまま、`assignee: cursor` + `cursor_instruction_id` + `github_issue` セット
- Issue 完了確認は棚卸し時に Claude 補助

### Tag 管理

- `00_meta/backlog_tags.md` に一覧集約
- あなた(導入者) 承認なく新規 tag 追加禁止

### 既存資産との共存

- `open-questions.md`(思いつき)、`roadmap.md`(方針)、`design-decisions.md`(決着)は共存
- あなた(導入者) 明示指示で open-questions → backlog に選択的昇格
- 一括移行はしない

## Consequences

### Positive

- Chat 発生の課題・タスクが構造化される
- 「今仕掛かりは?」に Claude が正確に答えられる
- GitHub Issue との明確な境界
- Cursor 委譲との自然な統合

### Negative

- Vault 内の管理オブジェクトが増える
- 昇格判断が あなた(導入者) の負荷になる(明示指示ベース)
- GitHub Issue と Vault の同期に手間が発生

### Neutral

- Skill vault-manager の更新が必要(Phase 1c で実施)
- Vault-maintainer に停滞検出ジョブが将来追加される可能性(Phase 1d)

## Alternatives Considered

### A. open-questions.md の拡張(構造化 TODO 化)

open-questions.md に status/assignee/GitHub 連携カラムを追加する案。

**却下理由**: 1 ファイル肥大化、履歴追跡困難、Cursor 指示書との対応が不自然、Chat 記録との相互 link が薄くなる。

### B. GitHub Issue 直行

Vault を挟まず GitHub Issue に直接起票する案。

**却下理由**: 対象リポジトリなしのタスク(life-scope, ideas)が管理できない、Vault の議論履歴と分離、GitHub は概念レベルの検討には向かない。

### C. 外部ツール(Todoist, Linear 等)

**却下理由**: Vault 統合の思想と衝突、AI ファースト運用と不一致、追加ツールの保守コスト。

## Related

- Phase 1a: [Vault #8](https://github.com/nkhippo/Vault/pull/8)(基盤構築)
- Phase 1b: 本 PR
- Backlog docs: Backlog docs index
- ID scheme: id-scheme

---
title: '0019 - Skill Backlog Reference Workflow'
type: knowledge
status: accepted
created: 2026-07-17T02:20:00+09:00
updated: 2026-07-17T02:20:00+09:00
tags: [adr, skill, backlog, phase-1c]
summary: Skill vault-manager に backlog 参照系 workflow(一覧・棚卸し・単一 item 参照)を追加する意思決定記録。
---

# ADR 0019: Skill Backlog Reference Workflow

## Context

Phase 1a-1b で Vault backlog 基盤と運用規約が整った。次に Skill vault-manager が Chat 内での参照要求(「今仕掛かりは?」「棚卸しして」等)に応答できる必要がある。

保存系 workflow(起票、昇格、Cursor 委譲連携)は Phase 1d で対応するため、本 Phase 1c は **参照系のみ**にスコープを絞る。

## Decision

Skill vault-manager に以下 3 種類の workflow を追加:

1. 一覧提示 flow(トリガー: 「今仕掛かりは?」等)
2. 棚卸し flow(トリガー: 「棚卸しして」等、GitHub Issue 状態確認込み)
3. 単一 item 参照 flow(トリガー: 「〜の詳細見せて」等)

詳細規約は Vault-Framework `docs/ja/backlog/reference-workflow.md` に集約、Skill は要点参照。

### 作業混ざり防止規約の適用

- 対象プロジェクト外の GitHub コネクタは能動的に使わない
- 全体棚卸しは あなた(導入者) の明示指示があった時のみ、複数コネクタ切り替えを許容
- Backlog 参照で 50_self/ や他プロジェクト docs を波及参照しない

### あなた(導入者) 承認 gate

- Backlog item の状態変更・tag 変更・Front Matter 更新は必ず あなた(導入者) の明示承認を経る
- 無断更新禁止(Skill の既存原則を継続)

## Consequences

### Positive

- あなた(導入者) が Chat で backlog 状態を素早く把握できる
- 棚卸しが自動化(候補提案 + あなた(導入者) 承認)、GitHub 状態同期の手間削減
- Skill 既存挙動を破壊しない(追加のみ)

### Negative

- Skill サイズ増加(要点のみ記載で肥大化を最小限に抑える)
- 全体棚卸しで複数 GitHub コネクタ切り替えが必要になり時間コスト増

### Neutral

- 保存系 workflow は Phase 1d で追加、それまで新規起票は暫定挙動(open-questions.md への追記提案)
- vault-maintainer に停滞検出ジョブ追加は Phase 1d の対象

## Alternatives Considered

### A. 参照 workflow を独立 Skill として切り出し

新規 Skill `backlog-reference` を作る案。

**却下理由**: Skill 数の増加は認知コスト増、既存 vault-manager と密結合(Vault 参照ルール、あいまい名解決等)しているため統合が自然。

### B. Skill 内に詳細実装、docs 参照なし

reference-workflow.md を作らず、Skill 内にすべて記載する案。

**却下理由**: Skill 肥大化、他プロジェクトからの参照可能性が下がる、Vault-Framework が source-of-truth という設計思想と不一致。

### C. 参照系と保存系を同時に(Phase 1c で 1c+1d)

**却下理由**: 変更範囲が大きくレビュー困難、保存系は open-questions 昇格や Cursor 委譲との連携が複雑で慎重な検証が必要。段階分割の方が品質・保守性優先の方針と整合。

## Related

- Phase 1a: Vault #8
- Phase 1b: Vault-Framework #9(ADR-0018)
- Reference workflow doc: [[pj-2026-07-17-27e2|reference-workflow]]
- Skill: `skills/vault-manager/SKILL.md`

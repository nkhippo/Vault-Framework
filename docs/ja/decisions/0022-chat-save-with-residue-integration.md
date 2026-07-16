---
id: pj-2026-07-17-ba5f
aliases:
- pj-2026-07-17-ba5f
- adr-0022
title: '0022 - Chat Save With Residue Integration'
type: knowledge
status: superseded
created: 2026-07-17T03:30:00+09:00
updated: 2026-07-17T05:10:00+09:00
tags: [adr, skill, backlog, chat, handoff, phase-1e]
summary: Chat 保存と残タスク一括起票の統合フローを Skill vault-manager に追加する意思決定記録。別 Chat 引き継ぎ時の重複作業排除。
---

# ADR 0022: Chat Save With Residue Integration

## Context

Phase 1a-1d で Backlog システムが完成し実運用可能。実運用で高頻度に発生するユースケースとして、別 Chat への引き継ぎ時に以下を毎回行う必要がある:

1. 「Vault に保存して」→ chat_log 保存
2. 「未決事項を backlog に候補リスト作って」→ 手動で backlog 起票

毎回 2 コマンド発話する運用は疲弊し、統合フローへの需要が発生。

## Decision

Skill vault-manager に「chat 保存 + 残タスク自動抽出 + 承認 gate + 一括起票」の統合フローを追加する。

### Trigger phrase の分岐

- 単純 chat 保存(「Vault に保存して」)→ 従来通り
- 統合フロー(「ここまでの会話を Vault に保存」「引き継ぎ用に保存」等)→ 本 Phase 1e フロー

### Naoya 承認 gate(必須維持)

- 候補リスト提示 → Naoya action → 実施
- 自動起票禁止(既存 Skill 原則の継続)

### chat_log ↔ backlog 相互リンク

- backlog item に `source_chat_log_id`
- chat_log に `spawned_backlog_ids: [...]`
- 後から辿れる仕組みを担保

### 詳細規約の集約

Vault-Framework `docs/ja/backlog/chat-save-with-residue-workflow.md` に集約、Skill は要点のみ。

## Consequences

### Positive

- 別 Chat 引き継ぎが 1 コマンドで完了
- chat_log と backlog の相互リンクが完全化、後から辿れる
- 既存 handoff/current-state.md 慣習の補完 or 代替として機能
- 抽出漏れは Naoya が承認 gate で追加可能、過剰抽出は skip で除外可能

### Negative

- Skill body サイズ増加(description は触らない、body のみ)
- Chat 抽出精度への依存(Claude の理解精度が抽出品質を決める)
- Naoya のレビュー負荷(候補数次第、多い場合は疲弊の可能性)

### Neutral

- 既存 workflow(単純保存、明示起票、参照)は変更なし、独立して動作
- Vault-maintainer は本 PR 対象外

## Alternatives Considered

### A. 現状維持(2 コマンド運用)

**却下理由**: 実運用で頻繁に発生するユースケースで摩耗する、Skill の目的(Naoya のユースケース最適化)と不一致。

### B. Chat 保存時に常時自動抽出(承認 gate なし)

**却下理由**: Naoya 承認原則違反、過剰起票の危険、既存 Skill 挙動と不一致。

### C. Trigger phrase を追加せず、対話内で誘導するのみ

**却下理由**: 発火が Skill 側にないため trigger 認識できず、Naoya が毎回誘導する必要がある。

### D. 別 Skill として切り出し

**却下理由**: 既存 vault-manager と密結合(chat 保存、backlog 起票の両方を含む)、統合の方が自然。

## Related

- Phase 1d PR-A(ADR-0020): Save workflow 基盤
- Phase 1a: backlog_item schema(`source_chat_log_id` は既存)
- Chat save with residue workflow doc: `docs/ja/backlog/chat-save-with-residue-workflow.md`(Phase 1f で削除)
- Skill: `skills/vault-manager/SKILL.md`

## Superseded by

[[pj-2026-07-17-c14c|ADR-0023 Phase 1f Three Independent Commands]] により置換された。Phase 1e の実運用資産は保持し、本 ADR の内容も履歴として残す。

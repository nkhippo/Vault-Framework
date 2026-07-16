---
id: pj-2026-07-17-632e
aliases:
- pj-2026-07-17-632e
- adr-0020
title: '0020 - Skill Backlog Save Workflow'
type: knowledge
status: accepted
created: 2026-07-17T02:30:00+09:00
updated: 2026-07-17T02:30:00+09:00
tags: [adr, skill, backlog, phase-1d]
summary: Skill vault-manager に backlog 保存系 workflow(起票、昇格、Cursor 委譲、Issue 起票)を追加する意思決定記録。
---

# ADR 0020: Skill Backlog Save Workflow

## Context

Phase 1a-1c で Vault backlog 基盤、運用規約、参照系 workflow が確立。**保存系 workflow が未実装**のため、Chat から backlog item を起票する行為は開いたまま(Phase 1c で参照要求中の起票要求は open-questions 追記提案で暫定応答)。

Backlog システムを実運用可能状態にするには、以下 workflow を Skill に追加する必要がある:

- 新規 task/issue 起票
- open-questions.md からの選択的昇格
- Cursor 委譲(指示書作成)+ 対応する GitHub Issue 起票
- Direct Issue 起票(小 task で指示書なし)
- 保留系(「後で考えましょう」)

## Decision

上記 5 種類の workflow を Skill vault-manager に追加する。詳細規約は Vault-Framework `docs/ja/backlog/save-workflow.md` に集約、Skill は要点参照。

### 起票案の 2 段階(案提示 → Naoya 承認 → 実施)

- 全ての新規起票、Front Matter 変更、外部書き込み(open-questions 更新、Cursor 指示書作成、GitHub Issue 起票)は **必ず Naoya 明示承認**を経る
- 案提示 → 承認 gate → 実施の 2 段階を厳守
- 「無断で起票して結果報告」は禁止

### Vault が master、GitHub は下流

- Cursor 指示書と GitHub Issue は backlog item の派生
- 起票順序: backlog item → Cursor 指示書(必要時)→ GitHub Issue(必要時)
- Vault backlog に `cursor_instruction_id`, `github_issue` として紐付け

### Idempotency / 再起票の扱い

- 同じ主題で複数回「起票して」と要求された場合、Claude は既存 backlog item がないか `search_by_keyword` で確認 → 既存があれば「これ既に起票済みです」と報告して重複起票を回避

## Consequences

### Positive

- Backlog システムが実運用可能状態に到達
- Chat の議論から自然な流れで backlog item が生まれる
- Naoya の元々の目的(Chat 発生の課題・タスクを Vault で管理)が達成

### Negative

- Skill サイズ増加(要点のみ記載、詳細は save-workflow.md 参照で肥大化最小)
- 起票案提示 → 承認 → 実施の 2 段階は Naoya の対話回数が増える(品質優先の代償)

### Neutral

- 停滞検出は vault-maintainer 側(Phase 1d PR-B)で対応
- 既存 open-questions.md, roadmap.md, design-decisions.md との棲み分けは Phase 1b で確立済み、本 PR では実装のみ

## Alternatives Considered

### A. 承認 gate 省略(自動起票)

Naoya が「起票して」と言ったら即実施する案。

**却下理由**: title/summary/tags の判断が Claude 側で誤る余地大、事後訂正のコスト高、既存 Skill の「無断更新禁止」原則と不一致。品質優先の方針からも 2 段階が妥当。

### B. Cursor 委譲と Issue 起票を独立 workflow に分離

**却下理由**: 実運用では両者が連続して発生することが多く、独立化するとステップ増加。Skill 側で連続提案する方が自然。

### C. Phase 1c と 1d を同時実装(参照 + 保存)

**却下理由**: 変更範囲が大きすぎ、テストシナリオが膨大に。段階分割で品質担保の方が優先。

## Related

- Phase 1a: Vault #8
- Phase 1b: Vault-Framework #9(ADR-0018)
- Phase 1c: Vault-Framework #10(ADR-0019)
- Save workflow doc: [[pj-2026-07-17-64df|save-workflow]]
- Skill: `skills/vault-manager/SKILL.md`

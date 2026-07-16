---
id: pj-2026-07-17-e2ef
aliases:
- pj-2026-07-17-e2ef
- adr-0021
title: '0021 - Vault-maintainer Stalled Detection'
type: knowledge
status: accepted
created: 2026-07-17T02:45:00+09:00
updated: 2026-07-17T02:45:00+09:00
tags: [adr, skill, backlog, maintainer, phase-1d]
summary: vault-maintainer の Level 2 週次メンテナンスに backlog stalled detection を追加する意思決定記録。Backlog システムの周期的健全性維持。
---

# ADR 0021: Vault-maintainer Stalled Detection

## Context

Phase 1d PR-A で Backlog システムが実運用可能状態になった。ただし停滞 backlog item(state: open だが動きがない)は現状:

- vault-manager 側の「棚卸しして」応答(on-demand)でのみ検出可能
- Naoya が「棚卸しして」と発話しなければ停滞 item は放置される

これは長期運用で問題になる:

- 実質的に abandoned な item が open のまま蓄積
- 進捗確認が必要な item が忘れられる
- Backlog システムの健全性が劣化

## Decision

vault-maintainer Skill の **Level 2 週次メンテナンス**に backlog stalled detection ジョブを追加する。

### Threshold

- Default: 14 日(2 週間)
- Naoya が明示指示すれば任意に変更可(7 日、30 日等)

### 検出フロー

1. `state: open` かつ `updated < today - threshold` の backlog item を列挙
2. `stalled` tag の有無で 2 グループに分ける
3. 各グループに対して action 提案(tag 付与、abandoned 化、進捗確認、skip)
4. Naoya 承認 gate 経由で反映

### vault-manager との分業

- vault-manager: on-demand 棚卸し(Phase 1c 参照 workflow の 3 flow)
- vault-maintainer: 週次または明示指示での周期的検出(本 PR)

補完関係、責任分離。

### 詳細規約の集約

Vault-Framework `docs/ja/backlog/maintainer-workflow.md` に詳細規約を集約、Skill は要点のみ記載。

## Consequences

### Positive

- 停滞 item が systematically 検出される
- Backlog システムの長期健全性が担保される
- 週次メンテナンスに自然に統合、Naoya の追加負担は「週 1 回のレビュー」のみ
- Backlog システム(Phase 1a-1d)全体が完成

### Negative

- vault-maintainer Skill サイズ増加(要点のみ記載で最小化)
- 週次メンテ実行時間の増加(全 backlog スキャン + Issue state 確認)

### Neutral

- 停滞判定 threshold は default 14 日、Naoya が調整可
- 一括処理も許容するが、慎重確認が必要

## Alternatives Considered

### A. vault-manager 側で停滞検出も担当

**却下理由**: vault-manager は「Naoya の指示に応答」する Skill、maintainer は「周期的なメンテ」を担当。責任分離が自然で、両 Skill の Skill サイズ肥大を分散できる。

### B. External cron script で自動検出

**却下理由**: AI ファースト運用と整合しない、Skill/MCP の枠外での運用は保守負荷増、Naoya 承認 gate が失われる。

### C. GitHub Actions で stalled tag 自動付与

**却下理由**: 上記 B と同じ理由 + Naoya の判断 gate が失われる。品質優先の方針と不一致。

### D. Threshold を hardcoded にしない、常に Naoya に確認

**却下理由**: 過度な確認は運用疲弊、default を持たせて明示指示時のみ override が現実的。

## Related

- Phase 1a-1c: 基盤 + 規約 + 参照 workflow
- Phase 1d PR-A: 保存 workflow(ADR-0020)
- **本 PR: Phase 1d PR-B = Backlog システム完成マイルストーン**
- Maintainer workflow: [[pj-2026-07-17-74af|maintainer-workflow]]
- Skill: `skills/vault-maintainer/SKILL.md`
- Maintenance framework: [[pj-2026-07-13-d0dd|maintenance-four-levels]]

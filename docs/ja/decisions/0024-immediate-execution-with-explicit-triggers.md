---
created: 2026-07-17 06:00:00+09:00
status: accepted
summary: 3 独立コマンド(chat_log 保存 / 候補抽出+起票 / handoff 保存)を明示 trigger phrase で駆動、全て即時実行(承認
  gate なし)。候補抽出のみ 2 step(抽出→保存 trigger)。Cursor 委譲・Issue 起票等の外部影響 flow は現状維持。
tags:
- adr
- skill
- backlog
- chat
- handoff
- phase-1g
- trigger-phrase
title: 0024 - Immediate Execution With Explicit Trigger Phrases
type: knowledge
updated: 2026-07-17 06:00:00+09:00
amends:
- ADR-0020
- ADR-0023
---

# ADR 0024: Immediate Execution With Explicit Trigger Phrases

## Context

Phase 1f 実運用直後の あなた(導入者) feedback:

- 「1 と 2 に関しては、承認なしで行われるようにしたい」
- 続いて trigger phrase の明示指定と全 3 コマンド即時実行の訂正

Phase 1d PR-A(ADR-0020)以降の「案提示 → 承認 → 実施」原則は、次の点で実運用意図と乖離していた:

- Trigger 発話を承認扱いすべきで、案提示は冗長
- 事後修正が容易な chat_log / backlog item / handoff は初回承認不要
- 明示 trigger phrase により意図を十分明確化できる

## Decision

### 明示 Trigger phrase

各コマンドに あなた(導入者) 指定の primary trigger phrase を採用し、既存類似 phrase は secondary(compat)として残す:

| コマンド | Primary trigger | 挙動 |
|---|---|---|
| 1: chat_log 保存 | 「会話の内容を Vault に保存して」 | 即時保存 |
| 2 Step 1: 候補抽出 | 「会話内のタスクを Vault に保存して」 | 抽出 + 候補提示 |
| 2 Step 2: 即保存 | 「これを保存して」 | 全件即保存 |
| 3: handoff 保存 | 「別のチャットに引き継げるように Vault に保存して」 | 即時保存 |

### 承認 gate 撤廃(コマンド 1, 2, 3 全て)

- Trigger 発話 = 承認扱い
- 案提示ステップなし
- Skill が path/id/title/tags/summary/body を自律決定して即実行

### コマンド 2 のみ 2 step 構造

Step 1 で抽出 + 候補提示、Step 2 で保存 trigger を待つ:

- Step 1 の候補提示は承認 gate ではなく、次の trigger 判断に必要な情報提示
- 「これを保存して」→ 全件即保存
- 部分保存(「1 と 3 だけ」)や修正保存(「タイトルを X に変えて」)も可能
- Step 1 と Step 2 の間に別の話題へ移った場合は自然に中断

### 承認 gate を維持する flow

以下は外部影響または内容重要性が高いため、案提示 → 承認 → 実施を維持:

- Cursor 委譲 flow
- GitHub Issue 起票 flow
- open-questions 昇格 flow
- 明示個別起票(「これタスクとして起票して」等)

### 複合 phrase への応答

3 primary trigger のいずれにも該当しない曖昧 phrase(例:「ここまでの会話を Vault に保存」)には、3 コマンドの選択肢を提示し、あなた(導入者) の選択で分岐する。

## Consequences

### Positive

- あなた(導入者) の実運用意図と整合し、判断負荷と案提示 turn を削減
- 明示 trigger phrase で意図表明が明確
- 事後修正と Level 1 棚卸しで quality control 可能

### Negative

- Skill 側の kind/project/tags/path/title 判定負担が増加
- コマンド 2 は抽出精度に依存

Mitigation: 過剰起票は事後 abandoned/update、抽出漏れは直接明示起票で対応する。

### Neutral

- ADR-0020、ADR-0023 は supersede せず部分 amend
- 外部影響 flow の承認 gate は維持
- 「無断起票禁止」は「Trigger 発話 = 承認、Skill 単独判断禁止」と再定義

## Alternatives Considered

### A. 全 flow で承認 gate を撤廃

**却下理由**: Cursor 委譲、Issue 起票、open-questions 昇格は外部影響があり慎重確認が必要。

### B. 全て現状維持

**却下理由**: あなた(導入者) の明示 feedback と不一致。

### C. コマンド 1, 2 のみ撤廃、3 は維持

**却下理由**: あなた(導入者) の訂正で handoff も即時実行と明示された。

### D. 3 コマンド全て即時実行 + 明示 trigger phrase(採用)

**採用**。あなた(導入者) の意図と整合する。

### E. コマンド 2 も 1 step

**却下理由**: 候補提示をなくすと抽出結果不明のまま起票され、quality が低下する。

## Related

- ADR-0020 Skill Backlog Save Workflow(部分 amend)
- ADR-0023 Phase 1f Three Independent Commands(部分 amend)
- Candidate Extraction Workflow
- Handoff Workflow
- Save Workflow
- Skill: `skills/vault-manager/SKILL.md`

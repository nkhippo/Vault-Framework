---
audience: mixed
created: 2026-07-14 04:10:00+09:00
date: 2026-07-13
id: pj-2026-07-13-ab24
keywords:
- issue-creation
- mcp-extension
- sequencing
- phase3.2
- framework-priority
- workflow
related_adrs:
- '0002'
- '0005'
- '0012'
related_chats:
- 10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md
related_specs: []
status: accepted
summary: Vault-MCP の GitHub Issue 起票機能を Vault-Framework 分離完了後(Phase 3.2)に実装する決定。Framework
  の完成度優先と Phase 3.1(トークン節約系)先行の 2 つの理由。
superseded_by: null
supersedes: null
tags:
- adr
- vault-mcp
- sequencing
title: 'ADR-0015: Issue 起票機能は Framework 分離の次'
type: adr
updated: 2026-07-14 04:10:00+09:00
aliases:
- pj-2026-07-13-ab24
- adr-0015
---

## Summary

Vault-MCP に対する GitHub Issue 起票機能(`create_issue`、`list_issues`、`add_issue_comment`)の実装タイミングを、Vault-Framework 分離作業(ADR-0005)完了後に確定した意思決定。Framework の完成度優先と、Phase 3.1(トークン節約系)先行の 2 つの理由。

## Context

Vault-MCP の拡張候補として、以下 2 系統の機能追加が同時に検討されていた:

- **系統 1**: トークン節約系(get_frontmatter、search_by_keyword、get_section)
- **系統 2**: GitHub Issue 系(create_issue、list_issues、add_issue_comment)

Issue 起票機能の意義:

- Chat 内で「対象アプリの実装を変える必要がある」と判断した時、直接 GitHub Issue を起票して Cursor 側で消化する workflow が可能
- Vault-Framework での議論から、対象アプリのリポジトリに向けた作業依頼を自然に発生させられる
- Naoya のプロダクト開発全般で活用できる

同時に、以下 2 つの外部要因があった:

- Vault-Framework 分離作業(ADR-0005)が進行中で、リソースが集中していた
- Issue 起票機能を実装するには PAT のスコープ拡大(Issues R/W 追加)が必要

## Decision

**Issue 起票機能の実装は Vault-Framework 分離完了後(Phase 3.2)に実施する**

- Phase 順序:
  1. Phase 1+2: 基本 5 ツール(完了、2026-07-13)
  2. **Vault-Framework 分離作業**(step 2 / step 3、2026-07-13〜14)
  3. Phase 3.1: トークン節約系 3 ツール(完了、2026-07-14)
  4. **Phase 3.2: GitHub Issue 系 3 ツール**(次期リリース)
  5. Phase 3.3: QoL 系(必要時に判断)

### Issue 起票機能を先送りにした理由

1. **Framework の完成度優先**: Framework 分離が進行中で、リソースの分散を避ける
2. **日常運用への影響が大きい方を優先**: トークン節約系は日常の全 vault 操作に効くが、Issue 起票は用途が限定的
3. **PAT スコープ拡大の慎重な検討**: Contents R/W の限定運用を維持したい期間があり、Issues 追加は Framework 落ち着いてから判断
4. **Framework 完成が Issue 起票の workflow 設計にも影響**: Cursor 指示書テンプレートが Framework 側で確立してから、Issue 本文フォーマットを設計するのが自然

### Phase 3.2 の見込み(参考)

- 実装ツール 3 個: `create_issue`, `list_issues`, `add_issue_comment`
- 総所要: 3-5 日(PAT 更新 + 実装 + テスト + Skill 側の Cursor 委譲フロー更新)
- 詳細は Vault-MCP プロジェクトの `roadmap.md` 参照

## Consequences

**Positive**:

- Framework 分離作業に集中でき、完成度が上がる
- Phase 3.1(トークン節約系)を先にリリースすることで、日常運用の改善が先行
- Cursor 指示書テンプレートが Framework 側で確立してから Issue 起票の workflow を設計できる
- PAT スコープ拡大のリスクを慎重に評価する時間が確保できる

**Negative**:

- Issue 起票 workflow の成立が数日〜数週間遅れる
- その間は Naoya が手動で GitHub Issue を起票する必要がある(現状の運用と変わらないが、Framework での議論を直接 Issue 化する体験は得られない)
- Phase 3.2 実装時に Framework 側の Cursor 指示書テンプレートとの整合を取る必要がある

**Mitigation**:

- 手動 Issue 起票は現状既に可能(Framework で議論 → Naoya が Cursor に指示 → Cursor が Issue 起票)
- Framework 側の Cursor 指示書テンプレートで、Issue 起票を伴う場合の指示形式を予め定めておく(step 2 の scaffold に含める)

## Alternatives Considered

### 案 A: Issue 起票を Phase 3.1 として先行実装

トークン節約系より Issue 起票を先に実装する案。

**却下理由**:

- 日常運用への影響が Phase 3.1(トークン節約系)の方が大きい
- Framework 分離作業と PAT 更新の 2 系統の変更を並行させると、リスクが高い

### 案 B: Framework 分離と Phase 3.2 を並行実装

Framework 分離作業と GitHub Issue 系ツール実装を並行で進める案。

**却下理由**:

- リソースの分散でどちらの完成度も落ちるリスク
- Framework の Cursor 指示書テンプレートが完成する前に Issue 起票 workflow を設計すると、後日の整合作業が発生

### 案 C: 全 Phase 3 を一度に実装

Phase 3.1、3.2、3.3 を全て一度にリリースする案。

**却下理由**:

- スコープが広く、リリースが遅れる
- Phase 3.1 の日常改善効果を先行して得られない
- 段階リリースの方が価値提供が速い

## Related

- **前提 ADR**: 
  - ADR-0005(Vault-Framework 早期分離、この判断の前提)
  - ADR-0002(Cloudflare Workers 採用、MCP 実装の前提)
- **後続 ADR**: 
  - ADR-0012(Fine-grained PAT 採用、PAT スコープ拡大のセキュリティ設計)
- **関連 spec**: なし
- **元記録**: `10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md`
- **Vault-MCP 側の詳細**:
  - `../../30_projects/Vault-MCP/design-decisions.md`(意思決定 6-12)
  - `../../30_projects/Vault-MCP/roadmap.md`(Phase 3.1/3.2/3.3 マイルストーン)

## Change Log

- 2026-07-13: 初版(Framework 分離後に実装する順序を確定)
- 2026-07-14: Phase 3.1 完了、Phase 3.2 が次期リリース対象として明示化

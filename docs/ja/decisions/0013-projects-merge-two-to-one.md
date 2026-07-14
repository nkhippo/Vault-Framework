---
audience: mixed
created: 2026-07-14T04:05:00+09:00
date: 2026-07-13
id: adr-0013
keywords:
  - projects
  - merge
  - claude-projects
  - ux
  - consolidation
  - memory-fragmentation
related_adrs:
  - "0003"
  - "0004"
related_chats:
  - 10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md
related_specs:
  - ambiguous-name-resolution
status: accepted
summary: "当初 2 分割していた Claude Projects(Vault: General と Vault: Project Design)を 1 Project(Vault)に統合した意思決定。実運用で UX 上の摩擦と記憶の分断が発生したため。あいまい名解決フローで用途値換は可能。"
superseded_by: null
supersedes: null
tags:
  - adr
  - projects
  - ux
title: "ADR-0013: Projects 統合(2 → 1)"
type: adr
updated: 2026-07-14T04:05:00+09:00
---

## Summary

Claude Projects を「Vault: General(汎用)」と「Vault: Project Design(プロジェクト別設計)」の 2 分割で運用していたが、UX 上の摩擦と記憶の分断が発生したため、1 Project(`Vault`)に統合した意思決定。あいまい名解決フローが機能するため、1 Project でも用途の切り替えは可能。

## Context

Vault 運用初期、Claude Projects を以下 2 つに分割していた:

- **Vault: General**: note 執筆、汎用ナレッジ、雑談、リポジトリ化前アイデア
- **Vault: Project Design**: 特定リポジトリ(IPASoundDrill、Vault-MCP 等)の設計相談

分割の意図:

- 各 Project の Instructions で用途に応じた指示を書き分けられる
- Chat の集約先が明確に分かれ、検索が容易になる
- Claude が「今はどの用途の Chat か」を判断しやすい

しかし数日の実運用で以下の問題が顕在化:

- **UX 上の摩擦**: 議論が「note 執筆 → プロジェクト設計」に自然に移った時、Project を切り替える必要があり、心理的コスト
- **記憶の分断**: `conversation_search` の対象が Project 単位で分かれるため、横断検索が効かない
- **判断の混乱**: 「これはどっちの Project で議論すべきか」を毎回考える必要
- **Chat の重複**: 同じ話題が両 Project にまたがって記録される

## Decision

**2 Projects を 1 Project(`Vault`)に統合**

- 統合後の Project: `Vault`(汎用、全用途を扱う)
- Instructions は激薄(ADR-0004)のまま、用途に応じた切り替えは Skill のあいまい名解決フローで対応
- 過去の `Vault: Project Design` Project の Chat は履歴として残す(移行は不要、conversation_search で横断検索できるため)
- Claude は Chat 冒頭の文脈から用途を判定し、必要な情報を必要な範囲で取得する

### 用途判定の仕組み

Skill `vault-manager` が以下のフローで対応:

1. Chat 冒頭でアプリ名や機能表現が出る → プロジェクト特定(Level 2 参照)
2. note 執筆や汎用ナレッジ → プロジェクト情報読み込みスキップ
3. 日記・振り返り → 50_self/ 保存フロー
4. 意図不明 → 会話の中で自然に明らかにする

この判定フローで、1 Project でも用途に応じた振る舞いが可能。

## Consequences

**Positive**:

- UX 改善: Project 切り替えの心理的コストが消える
- 記憶の分断解消: `conversation_search` が 1 Project 内で完結し、横断検索が効く
- 議論の連続性: 「note 執筆 → プロジェクト設計」の自然な流れを妨げない
- 管理コスト削減: 2 つの Project Instructions を同期する必要がない

**Negative**:

- 過去の 2 Project の Chat が別々に残る(履歴の分割)
- Chat 数が 1 Project に集中し、conversation_search のヒット数が増える(ノイズ増加の可能性)
- 用途別の Instructions を書き分けられない(激薄 Instructions 方針との整合は取れる)

**Mitigation**:

- 過去の Chat は履歴として保持(移行しない、conversation_search で横断)
- Chat 数増加によるノイズは、Front Matter の keywords/tags を活用したフィルタリングで軽減
- 用途別の細かい振る舞いは Skill の判定フローで対応(Instructions で書き分ける必要がない)

## Alternatives Considered

### 案 A: 2 Projects 維持

`Vault: General` と `Vault: Project Design` の 2 分割を維持する案。

**却下理由**: UX 上の摩擦と記憶の分断が実運用で問題化(数日運用で顕在化)。

詳細: [[../rejected-alternatives/projects-split-two.md]]

### 案 B: 3+ Projects に細分化

用途別にさらに細分化(note 用、プロジェクト設計用、日記用、雑談用等)する案。

**却下理由**: 分断コストがさらに増加。用途が明確な場合は Project 内で Chat を分ければよく、Project レベルの分割は不要。

### 案 C: Project を廃止し、Claude UI の Skill だけで対応

Claude Projects を使わず、Skill だけで発火判定する案。

**却下理由**: Project は「chat の集約単位」として自然な粒度であり、UI 上の使いやすさもある。Project 廃止のメリットが薄い。

## Related

- **前提 ADR**: 
  - ADR-0003(Skill・Project・Vault の 3 層アーキ、Project 層の粒度に関する追加判断)
  - ADR-0004(激薄 Project Instructions、Instructions で用途を書き分けないため統合が可能)
- **後続 ADR**: なし
- **関連 spec**: 
  - `../specs/ambiguous-name-resolution.md`(あいまい名解決フロー、1 Project で用途判定する仕組み)
- **元記録**: `10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md`

## Change Log

- 2026-07-13 初期: 2 Projects 分割で運用開始
- 2026-07-13 中期: 実運用で摩擦顕在化
- 2026-07-13 後期: 1 Project に統合(現行)

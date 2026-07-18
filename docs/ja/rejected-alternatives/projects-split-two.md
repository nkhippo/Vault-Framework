---
audience: mixed
created: 2026-07-14 05:40:00+09:00
date: 2026-07-13
keywords:
- projects-split
- two-projects
- consolidation
- ux
- memory-fragmentation
related_adrs:
- '0004'
- '0013'
status: rejected
summary: 'Claude Projects を「Vault: General」と「Vault: Project Design」の 2 分割で運用した案。UX
  上の摩擦と記憶の分断が発生したため却下、後に 1 Project に統合された。'
superseded_by: '0013'
tags:
- rejected
- projects
title: '却下案: Projects 2 分割運用'
type: rejected_alternative
updated: 2026-07-14 05:40:00+09:00
---

## Summary

Claude Projects を「Vault: General(汎用)」と「Vault: Project Design(プロジェクト別)」の 2 分割で運用した案。UX 上の摩擦と記憶の分断が発生したため却下。ADR-0013 で 1 Project(`Vault`)に統合。

## What Was Proposed

Claude Projects を用途別に 2 つに分割:

- **Vault: General**: 
  - note 執筆、汎用ナレッジ、雑談、リポジトリ化前のアイデア
  - Instructions は「note と汎用ナレッジを中心に扱う」を明示
- **Vault: Project Design**: 
  - 特定リポジトリ(<your-project>、Vault-MCP 等)の設計相談
  - Instructions は「30_projects/ 配下を優先参照」を明示

各 Project の Instructions を用途に応じて書き分け、Claude が「今どの Project にいるか」で振る舞いを切り替える構想。

## Why It Was Considered

- **用途別 Instructions**: 各 Project で異なる指示を書けるため、精緻な振る舞い制御が可能
- **conversation_search の絞り込み**: 用途別に Chat が分かれるため、検索対象を明確化できる
- **判断負荷の軽減**: Claude が「今は note 執筆」「今はプロジェクト設計」と判断する必要がなくなる
- **Chat 集約の明確さ**: どの Chat がどの用途で行われたかが Project 単位で自明

## Why It Was Rejected

- **UX 上の摩擦**: 議論が「note 執筆 → プロジェクト設計」に自然に移った時、Project を切り替える必要があり心理的コストが高い
- **記憶の分断**: `conversation_search` の対象が Project 単位で分かれるため、横断検索が効かない
- **判断の混乱**: 「これはどっちの Project で議論すべきか」を毎回考える必要
- **Chat の重複**: 同じ話題が両 Project にまたがって記録される
- **Instructions 同期の煩雑さ**: 2 つの Project Instructions を同期する運用負担
- **激薄 Instructions 方針(ADR-0004)との整合**: Instructions を用途別に書き分ける前提だが、激薄化との衝突
- **あいまい名解決フローの機能**: 1 Project でも用途判定は Skill 側で可能(実運用で確認)

数日の運用後、上記問題が顕在化し、統合の判断に至った。

## What Was Chosen Instead

- **採用案**: ADR-0013「Projects 統合(2 → 1)」
- **参照**: `id-ref-removed`

1 Project(`Vault`)に統合し、用途判定は Skill のあいまい名解決フローで対応。過去の 2 Project の Chat は履歴として残す(conversation_search で横断検索可能)。

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md`
- 対応 ADR: `id-ref-removed`
- 関連 ADR: `id-ref-removed`(激薄 Instructions 方針との整合)

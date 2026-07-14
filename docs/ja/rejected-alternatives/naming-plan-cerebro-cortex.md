---
audience: mixed
created: 2026-07-14T06:05:00+09:00
date: 2026-07-13
keywords:
  - naming
  - cerebro
  - cortex
  - memex
  - synapse
  - brain-metaphor
  - rhetorical
related_adrs:
  - "0006"
status: rejected
summary: 3 リポジトリを脳・記憶メタファ(Cerebro、Cortex、Memex、Synapse 等)で命名する案。過度に修辞的で、機能理解を阫害するため却下。
superseded_by: "0006"
tags:
  - rejected
  - naming
title: "却下案: Cerebro / Cortex 系命名"
type: rejected_alternative
updated: 2026-07-14T06:05:00+09:00
---

## Summary

3 リポジトリを脳・記憶メタファ(Cerebro、Cortex、Memex、Synapse 等)で命名する案。過度に修辞的で、機能理解を阻害するため却下。ADR-0006 で `Vault-*` に統一。

## What Was Proposed

3 リポジトリを脳の各部位や記憶関連の語彙で命名する案:

**候補パターン A(Cerebro 中心)**:
- `Cerebro`(vault 本体、大脳)
- `Cerebro-MCP`(MCP サーバ)
- `Cerebro-Framework`(Framework)

**候補パターン B(Cortex 中心)**:
- `Cortex`(vault 本体、皮質)
- `Neural-Bridge`(MCP、神経路)
- `Cortex-Kit`(Framework、キット)

**候補パターン C(Memex 系)**:
- `Memex`(記憶拡張、Vannevar Bush の概念)
- `Memex-Link`(MCP)
- `Memex-Blueprint`(Framework)

**候補パターン D(Synapse 系)**:
- `Synapse`(vault 本体)
- `Synapse-Relay`(MCP)
- `Synapse-Framework`(Framework)

## Why It Was Considered

- **知的で洒落たイメージ**: 「AI と個人記憶」というコンセプトに合う修辞
- **記憶しやすい名前**: 独特な語なので、ブランドとして印象に残る
- **参照先の連想**: Cerebro(X-MEN)、Memex(Vannevar Bush)等の文化的レファレンスがある
- **技術者好み**: 神経科学の用語で AI プロジェクトを命名するのは技術者コミュニティで一般的

## Why It Was Rejected

- **過度に修辞的**: リポジトリ名から機能・用途が推測できない(Cerebro が何を意味するか、初見では不明)
- **機能理解の阻害**: 「これは何?」を毎回説明する必要がある(Fable マニュアル、Public 化時)
- **導入者への負担**: 導入者が Framework を Fork する時、「Cerebro って何?」から入る必要がある
- **一般名詞との衝突**: Cortex は既に他のツール名で使われている(Cortex XSOAR 等)
- **X-MEN との連想**: Cerebro は Marvel の X-MEN で有名すぎ、法的な IP リスクは低いが混乱を招く可能性
- **Vault の直感性の喪失**: 「vault(金庫、保管庫)」という直感的な命名の方が、機能を素直に表現
- **ブランド性より機能性を優先**: プロダクト命名として、機能を素直に表現する方が長期的に有利

## What Was Chosen Instead

- **採用案**: ADR-0006「命名スキーム: Vault / Vault-MCP / Vault-Framework」
- **参照**: [[../decisions/0006-naming-vault-scheme.md]]

「Vault」は金庫・保管庫を意味し、Chat と個人ナレッジを保管するプロジェクトの機能を直接的に表現。修辞より機能性を優先。

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md`
- 対応 ADR: [[../decisions/0006-naming-vault-scheme.md]]
- 関連却下案: 他 5 命名候補

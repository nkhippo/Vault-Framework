---
audience: mixed
created: 2026-07-14T06:10:00+09:00
date: 2026-07-13
keywords:
  - naming
  - codex
  - grimoire
  - compendium
  - openai-collision
  - brand-conflict
related_adrs:
  - "0006"
status: rejected
summary: 3 リポジトリを Codex・Grimoire・Compendium 等の規範集・書物系で命名する案。OpenAI Codex との衝突リスクと修辞的すぎる点で却下。
superseded_by: "0006"
tags:
  - rejected
  - naming
title: "却下案: Codex 系命名"
type: rejected_alternative
updated: 2026-07-14T06:10:00+09:00
---

## Summary

3 リポジトリを Codex(規範集、書物)系(Codex、Grimoire、Compendium 等)で命名する案。OpenAI Codex との衝突リスクと、修辞的すぎる点で却下。ADR-0006 で `Vault-*` に統一。

## What Was Proposed

3 リポジトリを「規範集・書物」を意味する語彙で命名する案:

**候補パターン A(Codex 中心)**:
- `Codex`(vault 本体、規範集)
- `Codex-MCP`(MCP)
- `Codex-Framework`(Framework)

**候補パターン B(Grimoire 系)**:
- `Grimoire`(vault、魔導書)
- `Grimoire-Sync`(MCP)
- `Grimoire-Kit`(Framework)

**候補パターン C(Compendium 系)**:
- `Compendium`(vault、要約書)
- `Compendium-Access`(MCP)
- `Compendium-Framework`(Framework)

## Why It Was Considered

- **知的な響き**: 「Codex(規範集)」「Grimoire(魔導書)」は書物・知識の集約を連想させる
- **記録・体系化のイメージ**: Chat と設計判断を体系的に記録する用途と合致
- **ブランド性**: 独特な語で、ブランドとして印象に残る
- **ラテン語系のカッコよさ**: 技術者コミュニティで好まれる語彙

## Why It Was Rejected

### OpenAI Codex との衝突(最大の理由)

- **OpenAI Codex は AI コード生成ツールとして広く知られている**: GitHub Copilot の基盤モデルとして 2021 年以降流通
- **AI プロジェクトの命名で「Codex」を使うと、OpenAI Codex との混同が発生**: 導入者・第三者が「これは OpenAI 系?」と誤解する
- **検索性の低下**: `Codex` で検索すると OpenAI 関連コンテンツが上位を占め、このプロジェクトが埋もれる
- **Legal リスクは低いが、認知混乱**: 商標問題は低いが、認知面で不利

### その他の理由

- **修辞的すぎる**: Cerebro/Cortex 系と同様、機能理解を阻害
- **Grimoire・Compendium の一般性**: 魔導書・要約書という語は Chat 集約用途とは若干のズレ
- **カッコよさより機能性**: プロダクト命名として、機能を素直に表現する方が長期的に有利

## What Was Chosen Instead

- **採用案**: ADR-0006「命名スキーム: Vault / Vault-MCP / Vault-Framework」
- **参照**: [[../decisions/0006-naming-vault-scheme.md]]

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md`
- 対応 ADR: [[../decisions/0006-naming-vault-scheme.md]]
- 関連却下案: [[./naming-plan-cerebro-cortex.md]](Cerebro/Cortex 系)
- 参考: OpenAI Codex(https://openai.com/blog/openai-codex)

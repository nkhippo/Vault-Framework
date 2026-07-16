---
audience: mixed
created: 2026-07-14 06:20:00+09:00
date: 2026-07-13
keywords:
- naming
- archive
- ledger
- repository
- registry
- stale-feel
- financial-connotation
related_adrs:
- '0006'
status: rejected
summary: 3 リポジトリを Archive・Ledger・Repository・Registry 系の書庫・台帳・保管所で命名する案。Archive の「終わった感」や
  Ledger の金融連想で違和感が強く却下。
superseded_by: '0006'
tags:
- rejected
- naming
title: '却下案: Archive / Ledger 系命名'
type: rejected_alternative
updated: 2026-07-14 06:20:00+09:00
id: pj-2026-07-13-dc3d
aliases:
- pj-2026-07-13-dc3d
---

## Summary

3 リポジトリを Archive(書庫)や Ledger(台帳)系(Archive、Ledger、Repository、Registry 等)で命名する案。「終わった感」や「金融連想」により違和感が強く却下。ADR-0006 で `Vault-*` に統一。

## What Was Proposed

3 リポジトリを「書庫・台帳」を意味する語彙で命名する案:

**候補パターン A(Archive 中心)**:
- `Archive`(vault 本体、書庫)
- `Archive-MCP`(MCP)
- `Archive-Framework`(Framework)

**候補パターン B(Ledger 中心)**:
- `Ledger`(vault、台帳)
- `Ledger-Sync`(MCP)
- `Ledger-Kit`(Framework)

**候補パターン C(Repository/Registry)**:
- `Repository`(vault、保管所)
- `Registry-MCP`(MCP、登録所)
- `Registry-Framework`(Framework)

## Why It Was Considered

- **保存・記録の直接的な表現**: Archive(書庫)、Ledger(台帳)は「保存する」という機能を素直に表現
- **企業システム風の重厚感**: Ledger は会計台帳、Registry は登録所として、堅牢さのイメージ
- **英語圏での認知度**: これらの語は英語圏で普段使いされる語で、理解しやすい

## Why It Was Rejected

### Archive の「終わった感」

- **Archive は「アーカイブされた、古い、使わないもの」の連想が強い**: 「過去に集めたもの」というニュアンス
- **Vault の「現役で使う保管庫」というイメージと合わない**: Chat と設計判断は「今も使う」もの
- **Obsidian の運用と齟齬**: 日常的にアクセスする vault の命名として不適切

### Ledger の「金融連想」

- **Ledger は会計・簿記の連想が強すぎる**: 財務系ソフトウェアや暗号資産ウォレット(Ledger Nano 等)を連想
- **Ledger Nano との商標衝突リスク**: 暗号資産ハードウェアウォレットとして有名
- **Chat と Ledger は概念的にズレ**: 議論や意思決定を「台帳」というのは違和感

### Repository/Registry の一般性

- **Repository は GitHub 用語と重複**: 「repository」と言うと GitHub リポジトリを想起
- **Registry は npm/Docker Registry を想起**: パッケージ登録サービスとの混同
- **一般的すぎて識別性が低い**: プロダクト名として個別性が薄い

### 全般的な理由

- **修辞より機能の直接性を優先**: `Vault` の方が「安全に保管する」機能を最も直接的に表現
- **UX 上の統一感**: どのリポジトリも「Vault」ブランドの一部という認識が持ちやすい

## What Was Chosen Instead

- **採用案**: ADR-0006「命名スキーム: Vault / Vault-MCP / Vault-Framework」
- **参照**: [[pj-2026-07-13-e13e]]

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md`
- 対応 ADR: [[pj-2026-07-13-e13e]]
- 関連却下案: [[pj-2026-07-13-395d]]、[[pj-2026-07-13-3e01]]

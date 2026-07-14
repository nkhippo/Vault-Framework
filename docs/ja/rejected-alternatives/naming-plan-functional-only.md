---
audience: mixed
created: 2026-07-14T06:30:00+09:00
date: 2026-07-13
keywords:
  - naming
  - functional-only
  - descriptive
  - brand
  - identity
  - verbose
related_adrs:
  - "0006"
status: rejected
summary: 3 リポジトリを機能を直接説明する記述的な名前(chat-storage、mcp-server、docs-framework 等)で命名する案。ブランド性の欠如と、プロジェクトとしての一体感が出ないため却下。
superseded_by: "0006"
tags:
  - rejected
  - naming
title: "却下案: 機能名オンリー命名"
type: rejected_alternative
updated: 2026-07-14T06:30:00+09:00
---

## Summary

3 リポジトリを機能を直接説明する記述的な名前(chat-storage、mcp-server、docs-framework 等)で命名する案。ブランド性の欠如と、プロジェクトとしての一体感が出ないため却下。ADR-0006 で `Vault-*` に統一。

## What Was Proposed

3 リポジトリを機能を素直に説明する名前で命名する案:

**候補パターン A(chat-storage 系)**:
- `chat-storage`(vault、Chat 保存)
- `chat-storage-mcp`(MCP)
- `chat-storage-framework`(Framework)

**候補パターン B(記述的分離)**:
- `mcp-vault-storage`(vault)
- `mcp-server-cloudflare`(MCP、実装技術で命名)
- `mcp-vault-docs`(Framework、ドキュメント)

**候補パターン C(function-first)**:
- `personal-knowledge-base`(vault)
- `knowledge-mcp-bridge`(MCP)
- `knowledge-vault-framework`(Framework)

## Why It Was Considered

- **機能の直接的な理解**: リポジトリ名を見ただけで「これは何?」が分かる
- **SEO の有利さ**: 「chat-storage」で検索すると関連コンテンツが上位に来る
- **導入者への親切さ**: Fork する時、「何のためのリポジトリか」が明白
- **修辞やブランドを排した実用主義**: 過剰装飾を避ける

## Why It Was Rejected

### ブランド性の欠如

- **プロジェクトとしての一体感が出ない**: `chat-storage`、`chat-storage-mcp`、`chat-storage-framework` は「関連リポジトリ」感が薄い
- **記憶しにくい**: 記述的すぎて、逆に印象に残らない
- **プロダクトとしての identity 欠如**: 「これは Vault というプロジェクトだ」という主張が弱い

### 冗長性

- **`personal-knowledge-base` は長い**: 21 文字、`Vault` の 5 文字と比較して 4 倍以上
- **typing コストが増える**: 頻繁に参照する名前が長いと運用の摩擦が大きい

### 実装技術と命名の癒着

- **`mcp-server-cloudflare` のように実装技術を含めると、将来の技術変更で命名が古びる**: 万一 Cloudflare 以外に移行する時、リネームが必要
- **実装技術より機能・用途の抽象度で命名する方が長期的**: `Vault-MCP` は「MCP プロトコル」という抽象度、実装技術に依存しない

### 「機能名オンリー」の限界

- **一般名詞の連続で識別性が低い**: `chat-storage` は「Chat 保存機能」を持つ多数のツールと衝突
- **オリジナリティなし**: プロダクトとして立てにくい

## What Was Chosen Instead

- **採用案**: ADR-0006「命名スキーム: Vault / Vault-MCP / Vault-Framework」
- **参照**: [[../decisions/0006-naming-vault-scheme.md]]

`Vault` は「安全に保管する」機能を表現しつつ、簡潔でブランドとして立つ命名。

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md`
- 対応 ADR: [[../decisions/0006-naming-vault-scheme.md]]
- 関連却下案: 他 6 命名候補

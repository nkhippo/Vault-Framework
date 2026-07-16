---
title: Project Instructions Templates
title_ja: Project Instructions テンプレート
type: index
audience: mixed
status: published
date: 2026-07-13
keywords:
- project-instructions
- claude-projects
- templates
- thin-instructions
summary: Claude Projects の Instructions フィールド用の「激薄」テンプレ。実質的なルールは vault の 00_meta/project_instructions_vault.md
  に集約する。
id: pj-2026-07-13-8e6b
aliases:
- pj-2026-07-13-8e6b
---

## Purpose

Claude Projects の Instructions フィールドは「激薄」に保ち、実質的なルールは vault (`00_meta/project_instructions_vault.md`) に集約する方針(ADR 0004)。このディレクトリはそのテンプレ集。

## テンプレ一覧

| ファイル | 用途 |
|---|---|
| [vault-project.ja.md](./vault-project.ja.md) | Vault プロジェクト(汎用)の Instructions(日本語) |
| [vault-project.en.md](./vault-project.en.md) | Same in English |
| [app-project.ja.md](./app-project.ja.md) | 特定アプリ用 Project の Instructions(日本語) |
| [app-project.en.md](./app-project.en.md) | Same in English |

## Rationale

- [`rationale.md`](./rationale.md) - 激薄 Instructions 方針の設計根拠(ADR 0004 のポインタと要約)

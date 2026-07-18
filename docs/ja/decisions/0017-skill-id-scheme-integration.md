---
audience: mixed
created: 2026-07-17T01:30:00+09:00
date: 2026-07-17
keywords:
- skill
- vault-manager
- id-scheme
- phase-0.6
- aliases
- wikilink
related_adrs:
- '0003'
- '0006'
- '0007'
related_chats: []
related_specs:
- id-scheme
- frontmatter-spec
- wikilink-conventions
status: accepted
summary: Phase 0.5 で全 markdown に id scheme を適用済みのため、Skill vault-manager の新規保存時に
  id/aliases を必須化し、Body/FM 参照を ID 形式に統一する。
superseded_by: null
supersedes: null
tags:
- adr
- skill
- id-scheme
- phase-0.6
title: 'ADR-0017: Skill vault-manager への id scheme 統合'
type: adr
updated: 2026-07-17T01:30:00+09:00
---

## Summary

Skill vault-manager を Phase 0.6 として更新し、create_note 時の Front Matter に `id` / `aliases` を必須化する。Body 内参照は wikilink ID 形式、FM 参照は `_id` / `_ids` サフィックスに統一する。

# 0017: Skill vault-manager への id scheme 統合

## Context

Phase 0.5 で全 markdown に id scheme を適用済み。新規保存時も自動で id が付与される必要がある。現行 Skill は `title` / `type` / `created` 等を生成するが `id` / `aliases` を含まないため、このままでは CI validate FAIL や id ベース参照不能が発生する。

## Decision

Skill vault-manager を Phase 0.6 として更新:

- create_note 時の FM に `id` / `aliases` 必須化
- Type prefix inference を Skill に組込み(要点のみ、詳細は `docs/id-scheme.md`)
- Body 内参照を wikilink ID 形式(`[[<id>|display]]`)に統一
- FM 参照フィールドは `_id` / `_ids` サフィックス規約
- Collision 回避: `search_by_keyword` で最大 3 回 retry

Skill 更新は Vault-Framework の source of truth を編集し、あなた(導入者) が Anthropic Skills に再アップロードする。

## Consequences

- 新規保存が id scheme 準拠になる
- CI validate が新規ファイルでも PASS
- Skill サイズ増加は最小(要点のみ記載、詳細は Vault-Framework docs にリンク)
- Backlog システム(Phase 1)実装時に id 前提で設計可能
- 既存の保存判断フロー・sensitive 領域・MCP 失敗時中断等の挙動は変更しない

## Alternatives considered

- Vault-MCP 側で id 自動生成: MCP コード変更が必要、Phase 0.6 スコープ外
- Manual id 付与運用: 運用破綻リスク大、却下

## Related

- `docs/id-scheme.md`
- `docs/frontmatter-spec.md`
- `docs/wikilink-conventions.md`
- `skills/vault-manager/SKILL.md`
- `docs/ja/guidelines/save-decision-flow.md`

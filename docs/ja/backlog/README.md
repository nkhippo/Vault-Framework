---
id: pj-2026-07-17-a9e4
aliases:
- pj-2026-07-17-a9e4
title: Backlog System - Index
type: knowledge
status: published
created: 2026-07-17T02:05:00+09:00
updated: 2026-07-17T02:05:00+09:00
tags: [backlog, index, docs]
summary: Vault-Framework の backlog システム関連 docs の索引。全体設計・境界規約・既存資産統合ルールへの入口。
---

# Backlog System - Index

## Summary

Vault-Framework の backlog システム関連ドキュメントの索引。

## Docs

- [[pj-2026-07-17-cb46|Backlog System Overview]] — 全体設計、Phase 1a 実装への参照
- [[pj-2026-07-17-315f|GitHub Issue 境界]] — Vault backlog と GitHub Issue の境界、昇格タイミング
- [[pj-2026-07-17-7293|既存資産統合]] — open-questions.md, roadmap.md, design-decisions.md との棲み分け
- [[pj-2026-07-17-27e2|Reference Workflow]] — 参照系 workflow 詳細(Phase 1c)
- [[pj-2026-07-17-64df|Save Workflow]] — 保存系 workflow 詳細(Phase 1d PR-A)
- [[pj-2026-07-17-74af|Maintainer Workflow]] — 停滞検出 workflow 詳細(Phase 1d PR-B)

## Related

- ADR: [[pj-2026-07-17-e9df|0018-backlog-system]], [[pj-2026-07-17-a25e|0019-skill-backlog-reference-workflow]], [[pj-2026-07-17-632e|0020-skill-backlog-save-workflow]], [[pj-2026-07-17-e2ef|0021-vault-maintainer-stalled-detection]]
- ID scheme: [[pj-2026-07-16-4a20|id-scheme]]
- Frontmatter spec: [[pj-2026-07-16-bc64|frontmatter-spec]]
- Skill: `skills/vault-manager/SKILL.md`(Phase 1c 参照 + Phase 1d 保存 workflow)
- Skill: `skills/vault-maintainer/SKILL.md`(Phase 1d PR-B stalled detection)

## 位置付け

- 本ディレクトリの docs は **source-of-truth**
- Skill と Vault operational meta 側はこれらを参照する
- 更新時は本ディレクトリを先に、Skill と Vault を後で更新

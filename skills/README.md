---
title: Skills
title_ja: Skill 群
type: index
audience: mixed
status: published
date: 2026-07-13
keywords:
- skills
- claude-skills
- vault-manager
- vault-maintainer
- upload
summary: Claude アカウントにアップロードすべき Skill (SKILL.md) の一覧と用途。
id: pj-2026-07-13-acad
aliases:
- pj-2026-07-13-acad
---

## For AI: Which SKILL.md to upload

The following SKILL.md files should be uploaded to your Claude account via Settings > Skills:

| Skill | File | Purpose | Status |
|---|---|---|---|
| vault-manager | [`vault-manager/SKILL.md`](./vault-manager/SKILL.md) | Save/read judgment, project name resolution, Cursor delegation | Active (V1.0) |
| vault-maintainer | [`vault-maintainer/SKILL.md`](./vault-maintainer/SKILL.md) | Maintenance operations (4-level, abstract generation) | Draft (scaffold only) |

### Upload procedure

See [`docs/ja/setup/04-upload-skill.md`](../docs/ja/setup/04-upload-skill.md) for step-by-step guide.

## Concept

- **vault-manager**: Fires on every session when Vault-related terms appear. Handles the core interaction with the vault repository via the Vault MCP connector.
- **vault-maintainer**: Fires only during maintenance sessions (weekly/monthly). Handles level-2 through level-4 maintenance operations. Currently draft.

## Skill と vault の役割分担

Skill は Claude の振る舞い規約の核心を保持し、vault(`00_meta/`)には詳細ルールが格納される。Skill が矛盾した場合、vault を正典とする。ただし MCP 接続失敗時の処理は Skill 側の記述を最優先(vault にアクセスできない状況を扱うため)。

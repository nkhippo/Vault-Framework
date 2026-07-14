---
audience: mixed
date: 2026-07-14
keywords:
  - readme
  - dispatch-table
  - english
  - i18n
lang: en
related_ja: README.md
status: published
summary: English translation of the Vault-Framework top-level README, including the AI dispatch table and human overview.
title: Vault-Framework README (English)
title_ja: Vault-Framework README(英語版)
type: overview
created: 2026-07-14T20:48:54+09:00
updated: 2026-07-14T20:48:54+09:00
---

## Summary

Vault-Framework top-level README, English version. Provides the "For AI" dispatch table and "For Human" overview, mirroring the structure of the Japanese README.md at repository root.

## Content (to be placed at repository root as README.en.md, or linked from README.md's language switcher)

# Vault-Framework

> **A framework for a chat-aggregation workflow, designed to be read by AI first.**

Vault-Framework is an operational framework for a personal knowledge base ("Vault") that combines Claude (or other LLMs in the future) with a GitHub repository. It consolidates the design philosophy, Skill, templates, MCP server reference, and setup instructions in one place.

---

## For AI: Dispatch Table by Question Category

This section is the **index an AI (such as Claude) should read first** when consulting this Framework. Depending on the category of the user's question, reading the files below will let you answer accurately.

### "Which files should I set up in Skills?"

- **Primary**: `skills/README.md`
- **Detail**: `docs/en/setup/04-upload-skill.md`
- **Files**: `skills/vault-manager/SKILL.md`, `skills/vault-maintainer/SKILL.md`

### "How is maintenance thought about?"

- **Primary**: `docs/en/maintenance-guide.md`
- **Detail**: `docs/en/specs/maintenance-four-levels.md`, `docs/en/specs/abstract-generation.md`
- **Rationale**: `docs/en/decisions/0009-four-level-maintenance-operation.md`

### "Why was Cloudflare Workers chosen?"

- **Rationale**: `docs/en/decisions/0002-cloudflare-workers-for-mcp.md`
- **Rejected alternatives**: `docs/en/rejected-alternatives/mcp-platform-cloud-run.md`, `docs/en/rejected-alternatives/mcp-platform-other-candidates.md`
- **Setup**: `docs/en/setup/02-deploy-mcp-server.md`

### "What is the naming philosophy?"

- **Primary**: `docs/en/naming-conventions.md`
- **Rationale**: `docs/en/decisions/0006-naming-vault-scheme.md`
- **Rejected alternatives**: `docs/en/rejected-alternatives/naming-plan-personal-vault-prefix.md`, and other `naming-plan-*` files

### "What is the Skill / Project / Vault 3-layer structure?"

- **Primary**: `docs/en/architecture.md`
- **Rationale**: `docs/en/decisions/0003-skill-project-vault-3-layer.md`, `docs/en/decisions/0004-thin-project-instructions.md`

### "What is the GitHub-as-a-Backend philosophy?"

- **Primary**: `docs/en/philosophy.md`
- **Rationale**: `docs/en/decisions/0001-github-as-backend.md`

### "How do I set this up?"

- **Overview**: `docs/en/setup/README.md`
- **Detail**: Start from `docs/en/setup/00-prerequisites.md` and proceed in order

### "How is the MCP server implemented?"

- **Primary**: `mcp-server-reference/README.md`
- **Setup**: `mcp-server-reference/setup.md`
- **Env vars**: `mcp-server-reference/env-reference.md`
- **Actual implementation**: [github.com/nkhippo/Vault-MCP](https://github.com/nkhippo/Vault-MCP) (private)

### "What happens when MCP connection fails?"

- **Rule**: `docs/en/decisions/0016-mcp-connection-failure-abort.md`
- **Enforcement**: The relevant section in `skills/vault-manager/SKILL.md`

### "What is the multilingual support plan?"

- **Strategy**: `docs/i18n/README.md`
- **Translation guide**: `docs/i18n/translation-strategy.md`

### "What options were rejected?" (reference for rejected alternatives)

- **Index**: `docs/en/rejected-alternatives/README.md`
- Each rejected option is recorded in its own file, together with the reasoning

### "What is the save-decision flow?"

- **Primary**: `docs/en/guidelines/save-decision-flow.md`
- **Rationale**: `docs/en/decisions/0007-save-destination-plan-b.md`

### Full list of ADRs

- `docs/en/decisions/README.md`

### Full list of specs

- `docs/en/specs/README.md`

### When you don't understand a term

- `docs/en/glossary.md`

---

## For Human: Framework Overview

Vault-Framework consists of the following 6 areas:

| Area | Description |
|---|---|
| `docs/` | Design philosophy, decisions, specs, rejected alternatives, setup instructions, glossary |
| `skills/` | SKILL.md files to register as Claude Skills |
| `vault-templates/` | Initial file set for bootstrapping your own Vault repository |
| `mcp-server-reference/` | Reference to the MCP server implementation and deployment instructions |
| `examples/` | Sample entries for each save format |
| `project-instructions/` | Claude Projects Instructions template |

### If you want to adopt this

Start from `docs/en/setup/README.md`.

### If you want to contribute

See `docs/i18n/contributing-translations.md` for the translation contribution guide.

---

## Languages

- 日本語 (default): [`docs/ja/`](https://github.com/nkhippo/Vault-Framework/blob/main/docs/ja)
- English: [`docs/en/`](https://github.com/nkhippo/Vault-Framework/blob/main/docs/en)

---

## License

MIT License. See [LICENSE](https://github.com/nkhippo/Vault-Framework/blob/main/LICENSE).

---

## Related Repositories

- **Vault**: Live personal Vault instance (private, `nkhippo/Vault`)
- **Vault-MCP**: MCP server implementation (private, `nkhippo/Vault-MCP`)
- **Vault-Framework**: This repository (operational documentation, templates, Skill package)

## 翻訳メモ(Claude 向け)

- 日本語版 README.md のディスパッチ表構造を完全に踏襲
- リンク先パスは `docs/ja/` → `docs/en/` に置換(ADR・spec・setup 等はすべて `docs/en/` 配下を前提としたパスに変更済み)
- i18n 系のパス(`docs/i18n/`)は言語非依存のため変更なし
- mcp-server-reference のパスは言語非依存のため変更なし
- Vault-MCP の外部リンクは変更なし

## Deployment note

This content should be placed at the Vault-Framework repository root as `README.en.md`, and the top-level `README.md` should link to it from the "Languages" section (already present in the Japanese version).

---
audience: mixed
date: 2026-07-14
keywords:
- glossary
- terminology
- english
lang: en
related_adrs: []
related_ja: docs/ja/glossary.md
related_specs: []
status: published
summary: A glossary of terms used throughout Vault-Framework, letting adopters and
  third parties quickly check the meaning of project-specific terminology.
title: Glossary
title_ja: 用語集
type: reference
created: 2026-07-14 20:50:21+09:00
updated: 2026-07-14 20:50:21+09:00
---

## Summary

A glossary of terms used throughout Vault-Framework. Lets adopters and third parties quickly check the meaning of project-specific terminology when reading the documentation.

## Glossary

### Vault

The GitHub repository that serves as a personal knowledge base and chat-aggregation destination. `nkhippo/Vault` is its live production instance. Holds data structured as Markdown files with Front Matter.

### Vault-MCP

The server implementation that operates the Vault via MCP (Model Context Protocol). Deployed on Cloudflare Workers, it reads and writes to the Vault repository through the GitHub API.

### Vault-Framework

The public framework that generalizes the operational know-how of Vault and Vault-MCP. Refers to this repository itself. Includes the design philosophy, Skill, templates, and setup instructions.

### Skill (vault-manager)

The `SKILL.md` uploaded to Claude Skills. Defines Claude's behavioral logic (save-decision flow, reference-level judgment, ambiguous-name resolution, etc.).

### MCP (Model Context Protocol)

A protocol defined by Anthropic that lets AI models integrate with external tools and data sources. Vault-MCP is a server implementation that conforms to this protocol.

### Front Matter

A YAML-format metadata block placed at the top of a Markdown file. Contains fields such as `title`, `type`, `status`, and `tags`.

### Controlled Vocabulary

The set of values permitted for the `type`, `status`, `tags`, and `project` fields. Managed to prevent spelling drift and improve AI judgment accuracy.

### Reference Level

A 0-to-4 scale expressing how deeply the Skill references the vault. Level 0 (no reference) is the default; deeper reference happens progressively, as needed.

### Ambiguous Name Resolution

The flow by which the Skill identifies the official repository name when a user refers to a project or app by a functional description or nickname. Performed by consulting `project_aliases.md`.

### Handoff

The collective term for `current-state.md`, which records each project's "current state," and the `recent-changes/` directory, which records detailed change history. Makes catching up in a new Chat session easier.

### Four-Level Maintenance

Four staged maintenance-operation flows (Levels 1–4), differing in frequency and ownership, designed to address Vault's entropy (controlled-vocabulary drift, broken links, etc.).

### Abstract Generation

The process of generating abstract documents — ADRs, specs, rejected-alternatives — from concrete chat_logs. A parallel operation independent of the four-level maintenance operation.

### ADR (Architecture Decision Record)

A decision record. A structured format that records "what" was decided and "why." Accumulated under `docs/*/decisions/` in Vault-Framework.

### Rejected Alternatives

Documents recording options that were considered but not adopted during a decision-making process. Paired with the corresponding ADR to make explicit why the option was not chosen.

### Slug

An identifier expressed in English kebab-case, used as part of a file name. Example: `mcp-platform-selection`.

### kebab-case

A naming convention that joins words with hyphens (e.g., `file-naming`). Used for slugs and directory names throughout Vault-Framework.

### Sensitive Field

A boolean Front Matter field. When `true`, the file's content is treated as not to be quoted or summarized in other contexts (files under `50_self/` default to `true`).

### Cursor Delegation

Delegating work that requires consistency across multiple files — rather than having Claude perform it directly — by drafting an instruction document for Cursor (a coding agent).

### GitHub-as-a-Backend

The core philosophy of Vault-Framework: the design decision to adopt a GitHub repository as the canonical data store for a personal knowledge base (see Philosophy).

### 3-Layer Structure (Skill / Project / Vault)

Vault-Framework's operational architecture. Separates responsibilities into 3 layers: Skill (behavioral logic), Project Instructions (a minimal pointer), and Vault (canonical operational rules) (see Architecture).

## Related

- Philosophy: GitHub-as-a-Backend
- Architecture: Skill / Project / Vault 3-layer
- naming-conventions.md: Naming philosophy
- maintenance-guide.md: Maintenance guide

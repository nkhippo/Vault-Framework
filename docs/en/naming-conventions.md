---
audience: mixed
date: 2026-07-14
keywords:
  - naming
  - kebab-case
  - repository-naming
  - hashicorp-collision
  - english
lang: en
related_adrs:
  - "0006"
related_ja: docs/ja/naming-conventions.md
related_specs:
  - file-naming
  - vocabulary-design
status: published
summary: Overview of Vault-Framework's naming conventions covering file names, directory names, and repository names.
title: Naming Conventions Overview
title_ja: 命名規約の思想
type: overview
created: 2026-07-14T20:49:45+09:00
updated: 2026-07-14T20:49:45+09:00
---

## Summary

Overview of Vault-Framework's naming conventions. Covers the naming philosophy for file names, directory names, and repository names, with detailed specs referenced separately.

## Overall Naming Policy

Vault-Framework's naming conventions are guided by three principles:

1. **AI must be able to identify things without guessing**: kebab-case, unified date formats, and other mechanically predictable patterns
2. **Readable by humans too**: avoid excessive abbreviation; use meaningful words
3. **Brand neutrality**: avoid name collisions with specific tools (e.g., Obsidian) or existing products (e.g., HashiCorp Vault)

## File Naming Rules (Overview)

The standard format is `YYYY-MM-DD_kebab-case-slug.md`.

- The date is the date portion of ISO 8601 (JST-based)
- The slug is an English kebab-case string, at most 30 characters
- There are exception patterns (e.g., diary entries) — see the spec for details

For detailed rules, slug-generation logic, and the Skill's auto-generation algorithm, see the [file-naming spec](./specs/file-naming.md) *(English translation pending)*.

## Directory Naming Rules (Overview)

Top-level directories follow the `<numeric-prefix>_<snake_case>` format (e.g., `10_chat_logs/`). The numeric prefix increments by 10, leaving room for future expansion.

Project directories (`30_projects/<RepoName>/`) exactly match the corresponding GitHub repository name.

## History of Repository Naming

The three repositories that make up the Vault-Framework ecosystem are named as follows:

- `Vault` (data itself, private)
- `Vault-MCP` (MCP server implementation, Cloudflare Workers)
- `Vault-Framework` (public framework, this repository)

### Background of the naming change

Early naming candidates included ones referencing the Obsidian brand (e.g., `Obsidian-Vault`) and ones with a `Personal-Vault` prefix, but the project ultimately settled on the current naming (`Vault` / `Vault-MCP` / `Vault-Framework`).

Main reasons:

- **Independence from the Obsidian brand**: Vault-Framework is designed to not depend on Obsidian (see philosophy.md), and the naming was judged to reflect that
- **Prioritizing simplicity**: Prefixes like `Personal-Vault` were judged redundant and dropped
- **Risk of name collision with HashiCorp Vault**: The bare name `Vault` risks colliding with HashiCorp's secrets-management tool, so when publishing or forking, adopters are recommended to choose their own naming (e.g., `<YourName>-Vault`) — see the setup guide

For details on the rejected naming candidates, see the [naming-plan-* files under rejected-alternatives](./rejected-alternatives/README.md) *(English translation pending)*.

## Relationship to Controlled Vocabulary

Separate from naming rules, the Front Matter fields `type`, `status`, `tags`, and `project` use a controlled vocabulary. This is a different layer of control from file/directory "naming" — see the [vocabulary-design spec](./specs/vocabulary-design.md) *(English translation pending)* for details.

## Related

- [ADR 0006: Finalizing the naming scheme](../ja/decisions/0006-naming-vault-scheme.md) *(English translation pending)*
- [file-naming spec: Detailed file-naming specification](./specs/file-naming.md) *(English translation pending)*
- [vocabulary-design spec: Controlled vocabulary design](./specs/vocabulary-design.md) *(English translation pending)*
- [rejected-alternatives: Rejected naming candidates](./rejected-alternatives/README.md) *(English translation pending)*
- [Philosophy: GitHub-as-a-Backend](./philosophy.md)

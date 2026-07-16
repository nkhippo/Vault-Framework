---
audience: mixed
date: 2026-07-13
id: pj-2026-07-15-318e
keywords:
- architecture
- skill
- project
- vault
- 3-layer
- layering
- separation-of-concerns
- english
lang: en
related_adrs:
- '0001'
- '0004'
- '0013'
- '0016'
related_ja: docs/ja/decisions/0003-skill-project-vault-3-layer.md
related_specs:
- reference-level-system
status: accepted
summary: 'Decision to separate Vault operation responsibilities into three layers:
  Skill, Project, and Vault. The Skill holds behavioral rules, the Project holds use-case
  operational policy, and the Vault holds detailed rules and data. Conflict priority
  is also finalized.'
tags:
- adr
- architecture
- important
title: 'ADR-0003: Skill / Project / Vault 3-layer Operational Architecture'
title_ja: 'ADR-0003: Skill・Project・Vault の 3 層運用アーキテクチャ'
type: adr
created: 2026-07-14 21:42:50+09:00
updated: 2026-07-14 21:42:50+09:00
aliases:
- pj-2026-07-15-318e
- adr-0003
---

## Summary

Decision to separate the responsibilities of Vault operation into three layers: Skill (the whole Claude account), Project (Claude Projects), and Vault (00_meta inside the GitHub repository). The Skill holds the core behavioral rules, the Project holds use-case-specific operational policy, and the Vault holds detailed rules and data. The priority order in case of conflict was also finalized.

## Context

In the early stage of Vault operation, it was ambiguous where the following information should be consolidated:

- Claude's behavioral rules (trigger detection, save decisions, reference decisions)
- Operational policy for the whole session (what projects it handles, behavior at session start)
- Front Matter schema, controlled vocabulary, templates
- Design decisions of each project
- Records of past discussions

Mixing these together bloats what Claude must load when deciding behavior, worsening response cost and latency. They also differ in update frequency (behavioral rules change rarely, operational policy roughly monthly, templates get fine-tuned daily).

## Decision

**Separate responsibilities into three layers:**

### Layer 1: Skill (the whole Claude account)

- File: `SKILL.md` (registered under Claude Settings > Skills)
- Contents: the core of behavioral rules (reference-decision rules, save-decision flow, ambiguous-name resolution, Cursor-delegation judgment, MCP connection-failure handling)
- Update frequency: rare (re-upload only on important changes)
- Reference timing: auto-triggered in every Chat (on trigger match)

### Layer 2: Project (Claude Projects' Instructions)

- File: the Instructions field of the relevant Project
- Contents: only "required actions at session start" + a pointer saying "read the canonical operational rules of the vault" (very thin)
- Update frequency: medium (on use-case change)
- Reference timing: at the start of every Chat within the relevant Project

### Layer 3: Vault (`00_meta/` inside the GitHub repository)

- Files: `00_meta/*.md` (vault_structure, naming_conventions, vocabulary, frontmatter_schema, claude_operation_rules, project_aliases, project_instructions_vault, templates/)
- Contents: detailed rules, controlled vocabulary, templates, project aliases, operational policy as a Chat-aggregation destination
- Update frequency: high (daily fine-tuning, vocabulary extension, template adjustment)
- Reference timing: read via MCP only when the Skill judges it necessary

## Priority Order

The priority order when the three sources conflict:

- **Normally**: Skill > Vault > Project Instructions
- **Controlled vocabulary, naming conventions, template formats**: Vault takes priority (if the Skill side is stale, the Vault is authoritative)
- **MCP connection-failure handling, strict Level 0, the ban on quoting sensitive files**: Skill takes priority (because it handles situations where the vault is inaccessible)

## Consequences

**Positive**:

- Responsibilities are clear; each layer updates independently
- Naoya can directly edit Vault-side rules in Obsidian (no Skill re-upload needed)
- SKILL.md can be kept compact (detailed rules delegated to the Vault)
- What must be loaded at Chat-session start is minimized (consideration for prompt caching)

**Negative**:

- The three layers require synchronization (risk of naming or reference rules diverging between Skill and Vault)
- An adopter must understand three places
- The conflict-priority rule must be managed explicitly

**Mitigation**:

- Incorporate periodic three-layer consistency checks into Level 3 (monthly correction) of the four-level maintenance operation (ADR-0009)
- Emphasize the role division of the three layers in the Framework's docs (architecture.md, philosophy.md)

## Alternatives Considered

### Option A: Two layers (Skill + Vault, abolishing Project Instructions)

An option to abolish Project Instructions and operate with two layers: Skill and Vault.

**Reason for rejection**: When wanting to switch use cases per Project (a Project for the Vault, a Project for a specific app, etc.), identification and trigger detection become cumbersome with the Skill alone.

### Option B: Four layers (Skill + Project + Vault + external config)

An option to separate Naoya-specific settings (tokens, URLs, etc.) into a separate external config.

**Reason for rejection**: Managing an external config creates an additional sync path, raising complexity. The current Cloudflare Secrets plus the Vault's 00_meta are sufficient.

### Option C: Single layer (cram everything into the Skill)

An option to consolidate all rules and reference rules into SKILL.md.

**Reason for rejection**: Including detailed rules bloats SKILL.md and requires re-upload on every Skill update. Naoya would lose the freedom to edit in Obsidian.

## Related

- **Prerequisite ADR**: ADR-0001 (GitHub-as-a-Backend)
- **Successor ADRs**:
  - ADR-0004 (Very thin Project Instructions, the Project-side implementation policy for this 3-layer structure)
  - ADR-0013 (Project consolidation, an additional decision on the granularity of the Project layer)
  - ADR-0016 (Retry and abort on MCP connection failure, an application of the Skill-layer-priority rule)
- **Related spec**: `../specs/reference-level-system.md` (design of the 5-level reference system) *(English translation pending)*
- **Source record**: `10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md`

## Change Log

- 2026-07-13: Initial version (finalized the 3-layer architecture)

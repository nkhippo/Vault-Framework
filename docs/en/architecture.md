---
audience: mixed
date: 2026-07-14
keywords:
- architecture
- 3-layer
- skill
- project
- vault
- priority
- english
lang: en
related_adrs:
- '0003'
- '0004'
related_ja: docs/ja/architecture.md
related_specs: []
status: published
summary: Overview of the Skill / Project / Vault 3-layer operational architecture.
  Organizes the role, priority, and data flow of each layer.
title: 'Architecture: Skill / Project / Vault 3-layer'
title_ja: 'アーキテクチャ: Skill・Project・Vault の 3 層'
type: overview
created: 2026-07-14 20:49:30+09:00
updated: 2026-07-14 20:49:30+09:00
id: pj-2026-07-15-89b9
aliases:
- pj-2026-07-15-89b9
---

## Summary

Explains the core operational architecture of Vault-Framework: the "Skill / Project / Vault 3-layer structure." Organizes the role, priority, and data flow of each layer, and explains why this separation is necessary.

## Overview of the 3 Layers

Vault-Framework's operation consists of the following 3 layers:

### Layer 1: Skill (`vault-manager` SKILL.md)

- **Role**: The core behavioral logic for Claude
- **Contents**: Trigger detection, save-decision flow, reference-level system, ambiguous-name resolution flow, MCP connection-failure handling, Cursor-delegation judgment
- **Update frequency**: Low (requires re-upload to Claude Skills)
- **Visibility**: Always loaded by Claude (as part of the system prompt)

### Layer 2: Project Instructions (Claude Projects' Instructions)

- **Role**: A minimal pointer only
- **Contents**: Just the instruction "check the Vault MCP connector, read `project_instructions_vault.md` inside the vault, and follow it"
- **Update frequency**: Almost never (kept intentionally thin by design)
- **Visibility**: Passed to Claude at the start of a Chat session

### Layer 3: Vault (operational rules under `00_meta/`)

- **Role**: The canonical source of substantive operational rules
- **Contents**: Controlled vocabulary, naming conventions, Front Matter schema, project aliases, day-to-day operational policy that changes frequently
- **Update frequency**: High (directly editable in Obsidian)
- **Visibility**: Fetched via MCP as needed (following the reference-level system)

## Priority Between Layers

If the content of the 3 layers conflicts, the priority order is **Skill > Vault > Project Instructions**.

### Why this order

- **Skill takes top priority**: Safety-critical rules — MCP connection-failure handling, the strict Level-0 anti-overreference rule, and the ban on quoting sensitive files — are written in the Skill, and these should always apply regardless of the vault's content
- **Vault comes next**: Day-to-day operational rules that change frequently — controlled vocabulary, naming conventions, template formats — are canonical on the vault side. If the Skill's description becomes stale, the vault takes precedence
- **Project Instructions comes last**: Intentionally kept "very thin," holding almost no substantive rules. When a conflict arises, the other two layers take precedence

### Normally, conflicts are managed to not occur

This priority order is only a fallback rule for the rare case of conflict; under normal operation, the 3 layers are maintained to stay consistent (as part of the four-level maintenance operation).

## Data Flow

The typical data flow within a Chat session is as follows:

```
[Chat session starts]
    ↓
Project Instructions (Layer 2) is passed to Claude
    ↓
Claude executes "check MCP connector → read project_instructions_vault.md" (Level 1 reference)
    ↓
The conversation proceeds according to the Skill's (Layer 1) decision logic
    ↓
Additional information is fetched from Vault (Layer 3) as needed, following the reference-level system
    ↓
If there is a save instruction, Claude writes to Vault (Layer 3) according to the Skill's (Layer 1) save-decision flow
```

The Skill decides "when and how to act," while the Vault provides the detailed "specifically which rules to judge by" — this is the role division.

## Why We Split Into 3 Layers

An alternative of putting all rules into a single file was also considered (see the rejected alternatives in ADR-0003), but the 3-layer split was adopted for the following reasons:

- **Differing update frequencies**: The Skill requires re-upload (high update cost), while the Vault can be edited immediately in Obsidian. Placing frequently-changing content in the Vault reduces operational friction
- **Clarity of responsibility**: Separating "behavioral logic" from "detailed data and rules" makes it less likely for a change in one to affect the other
- **Thinness of Project Instructions**: Claude Projects' Instructions are consumed as context on every turn, so keeping them thin is more cost-efficient

## Related

- [ADR 0003: Skill / Project / Vault 3-layer structure](../ja/decisions/0003-skill-project-vault-3-layer.md) *(English translation pending)*
- [ADR 0004: Keeping Project Instructions very thin](../ja/decisions/0004-thin-project-instructions.md) *(English translation pending)*
- [Philosophy: GitHub-as-a-Backend](./philosophy.md)
- [Reference-Level System spec](../ja/specs/reference-level-system.md) *(English translation pending)*

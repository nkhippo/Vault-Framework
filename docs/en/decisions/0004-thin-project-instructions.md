---
audience: mixed
date: 2026-07-13
id: pj-2026-07-15-721d
keywords:
- project-instructions
- thin
- delegation
- vault
- canonical
- instructions-template
- english
lang: en
related_adrs:
- '0003'
- '0013'
- '0016'
related_ja: docs/ja/decisions/0004-thin-project-instructions.md
related_specs: []
status: accepted
summary: Policy to keep Claude Projects' Instructions very thin, consolidating substantive
  operational rules into 00_meta/project_instructions_vault.md inside the vault. The
  Instructions hold only a pointer at session start saying to read the vault's canonical
  rules.
tags:
- adr
- instructions
title: 'ADR-0004: Very Thin Project Instructions Policy'
title_ja: 'ADR-0004: 激薄 Project Instructions 方針'
type: adr
created: 2026-07-14 21:43:32+09:00
updated: 2026-07-14 21:43:32+09:00
aliases:
- pj-2026-07-15-721d
- adr-0004
---

## Summary

Policy to keep the Instructions field of Claude Projects "very thin," consolidating the substantive operational rules into `00_meta/project_instructions_vault.md` inside the vault. The Instructions hold only a pointer at session start saying "read the vault's canonical rules."

## Context

After adopting the Skill / Project / Vault 3-layer architecture in ADR-0003, a decision was needed about what specifically to write in the Project layer (the Instructions field of Claude Projects). Three options were considered:

- **Option A**: Thick Instructions (write out all of the whole-session operational policy, reference rules, save flow, etc.)
- **Option B**: Very thin Instructions (only a pointer saying "read the vault's canonical rules")
- **Option C**: Attached-file method (a pointer in the Instructions, detailed rules as an attached file)

Criteria:

- Update frequency: operational rules are fine-tuned daily on the vault side, making it cumbersome to keep the Instructions side in sync
- Ease of editing for Naoya: the vault side can be edited directly in Obsidian, but Instructions must be edited via the Claude UI
- Consistency with the Skill: putting similar information in the Skill too would mean syncing three places, with high divergence risk
- Behavior when MCP is disconnected: whether it can work with Instructions alone

## Decision

**Adopt Option B (very thin Instructions).**

- The Project Instructions contain only the following:
  1. The Project's purpose (e.g., "the core Chat-aggregation destination for Naoya's personal Vault operation")
  2. Required actions at session start ("if the MCP connector is connected, read the vault's `00_meta/project_instructions_vault.md`")
  3. Fallback behavior when MCP is disconnected ("handle within the scope of the Skill and userMemories; be honest when vault reference is needed")
  4. The role division of the three parties and the priority rule (Skill > vault > Instructions)
- Substantive operational rules (reference rules, save flow, ambiguous-name resolution, Cursor-delegation judgment, etc.) are consolidated on the Skill and vault sides
- Updating the Instructions is generally unnecessary (only on a change of the Project's purpose)

### Template for the very thin Instructions

Placed in the Framework's `project-instructions/vault-project.ja.md`. The following skeleton:

```markdown
# Vault - Project Instructions

This project is the core Chat-aggregation destination for <your-name>'s personal Vault operation.

## Required actions at session start
1. Check whether the MCP connector `Vault MCP` is connected
2. If connected, read 00_meta/project_instructions_vault.md via MCP
3. Proceed with the conversation according to its contents

## Role division between these Instructions and the vault
- Instructions: only a minimal pointer
- vault's 00_meta/project_instructions_vault.md: the canonical operational rules
- Skill vault-manager: the core of behavioral rules

If the three conflict, the priority is Skill > vault > Instructions
```

## Consequences

**Positive**:

- The Instructions update frequency is minimal (only on use-case change), so Naoya's operational burden is low
- The canonical source of operational rules is consolidated on the vault side, directly editable in Obsidian
- Easy to keep consistency with the Skill (the Instructions only say "read," holding no substantive rules)
- When the Framework is turned into a Fable manual, the explanation of the Instructions template is simple
- Adopters edit the Instructions infrequently and can forget about them after initial setup

**Negative**:

- When the MCP connector is disconnected, the Instructions alone are insufficient (they hold no substantive operational rules)
- Claude must always read the vault in the first session, slightly increasing token consumption
- Someone viewing the Instructions (a third party other than Naoya) may wonder "does this really work on its own?"

**Mitigation**:

- Clearly state the fallback behavior for MCP disconnection in the Instructions ("handle within the scope of the Skill and userMemories")
- Explain in the Framework's `docs/ja/setup/05-configure-project.md` that "very thin Instructions is an intentional design"
- Explicitly write in the Instructions that "substantive rules are consolidated on the vault side" (to help a third party understand)

## Alternatives Considered

### Option A: Thick Instructions (write out all rules)

An option to write all of the reference rules, save flow, ambiguous-name resolution flow, etc., in the Instructions.

**Reasons for rejection**:

- Requires triple synchronization with the Skill (Skill, Instructions, vault)
- The Instructions update frequency rises, increasing Naoya's operational burden
- Flexible changes on the vault side are not reflected in the Instructions, causing divergence

### Option C: Attached-file method

An option to write a pointer in the Instructions and attach detailed rules as a file.

**Reasons for rejection**:

- The attached file's update frequency drops (attaching via the Claude UI is cumbersome)
- Vault-side changes are not reflected, essentially the same problem as Option A

Details: [[../rejected-alternatives/instructions-attached-file.md]]

## Related

- **Prerequisite ADR**: ADR-0003 (Skill / Project / Vault 3-layer architecture, the implementation policy for the Project layer)
- **Successor ADRs**:
  - ADR-0013 (Project consolidation, an additional decision on the granularity of the Project layer)
  - ADR-0016 (Retry and abort on MCP connection failure, corresponding to the Instructions' MCP-disconnection fallback)
- **Related spec**: none
- **Source record**: `10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md`
- **Placement in the Framework**: `project-instructions/vault-project.ja.md`

## Change Log

- 2026-07-13: Initial version (finalized the very-thin-Instructions policy)

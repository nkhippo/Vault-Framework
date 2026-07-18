---
audience: mixed
date: 2026-07-13
keywords:
- maintenance
- four-level
- level-1
- level-2
- level-3
- level-4
- abstract-generation
- cadence
- english
lang: en
related_adrs:
- '0003'
- 0008
- '0011'
related_ja: docs/ja/decisions/0009-four-level-maintenance-operation.md
related_specs:
- maintenance-four-levels
- abstract-generation
status: accepted
summary: Decision to classify Vault maintenance operations into four levels (daily
  trigger / weekly / monthly / seasonal correction) and to position abstract generation
  as an independent parallel operation. Frequency, ownership, and intervention cost
  are made explicit.
tags:
- adr
- maintenance
- important
title: 'ADR-0009: Four-Level Maintenance Operation + Abstract Generation in Parallel'
title_ja: 'ADR-0009: 保守運用 4 レベル + 抽象生成の並行運用'
type: adr
created: 2026-07-15 08:29:44+09:00
updated: 2026-07-15 08:29:44+09:00
---

## Summary

Decision to classify Vault maintenance operations into four levels (Level 1 daily trigger / Level 2 weekly correction / Level 3 monthly correction / Level 4 seasonal correction), and to position "abstract generation" — which produces abstract specs / ADRs from concrete chat_logs — as an independent parallel operation. Frequency, ownership, and intervention cost are made explicit.

## Context

Regarding Vault's maintenance operations, the following implicit operations were occurring in parallel:

- Automatic checks on Chat save (controlled-vocabulary violations, missing Front Matter)
- Cleanup done ad hoc, weekly or monthly, when noticed
- Extracting learnings from chat_logs as specs or ADRs

Without systematizing these, the following problems arise:

- Judgment wavers on "which level of maintenance is this work?"
- Cost estimation for maintenance work is difficult
- The operational policy cannot be conveyed to adopters (via the Framework)
- The role division between Skill and Cursor is ambiguous

At the same time, consistency with the Cursor-delegation judgment (ADR-0008) had to be maintained.

## Decision

**Classify maintenance into four levels; manage abstract generation independently as a parallel operation.**

### Level 1: daily trigger

- **Timing**: automatically judged by the Skill on Chat save/reference
- **Owner**: Claude (the `vault-manager` Skill) alone
- **Content**:
  - Auto-correction of controlled-vocabulary violations (typos; drift in type/status/tags)
  - Completion of required Front Matter fields
  - Warning on naming-convention violations
- **Intervention cost**: zero (done without the user noticing)
- **Cursor delegation**: not needed

### Level 2: weekly correction

- **Timing**: weekly (recommended: Sunday)
- **Owner**: Cursor performs it after the adopter's approval
- **Content**:
  - Re-classification of chat_logs (moving items that fell into the inbox to their proper place)
  - Consistency check of Front Matter against the controlled vocabulary
  - Detection of broken links
- **Intervention cost**: 30 minutes to 1 hour
- **Cursor delegation**: standard (uses an instruction template)

### Level 3: monthly correction

- **Timing**: monthly (recommended: the 1st of the month)
- **Owner**: Cursor performs it after the adopter's approval
- **Content**:
  - Structural consistency check (confirmation of handoff/current-state.md updates across 30_projects)
  - Archiving of handoff's recent-changes/
  - Review and extension of the controlled vocabulary
  - Check for drift between Skill and Vault
- **Intervention cost**: 1 to 3 hours
- **Cursor delegation**: standard (uses a dedicated instruction template)

### Level 4: seasonal correction

- **Timing**: seasonal (March, June, September, December)
- **Owner**: led by the adopter, performed by Cursor
- **Content**:
  - Large structural changes (directory restructuring, bulk renaming of old names)
  - Cleanup of deprecated tags and retroactive application to past files
  - Update of the Fable packaging on the Framework side
  - Major version upgrades of Vault-MCP and the Skill
- **Intervention cost**: several hours to a day
- **Cursor delegation**: large-scale; create a dedicated plan and instruction document

### Abstract generation (parallel operation)

- **Timing**: any timing at the adopter's discretion (recommended: monthly to quarterly)
- **Owner**: Claude proposes + the adopter judges + Cursor performs
- **Content**:
  - Extract common patterns from multiple chat_logs and organize them as specs
  - Structure the results of discussions as ADRs
  - Organize records of rejected options as rejected-alternatives
- **Intervention cost**: per session (1-3 hours)
- **Cursor delegation**: partial (Claude writes; Cursor reflects into the structure)

## Consequences

**Positive**:

- Timing, ownership, and cost of maintenance work are made clear
- Directly linked with the Cursor-delegation judgment (ADR-0008) (Level 2 and above are basically Cursor-delegated)
- Can convey to adopters "here is how we think about vault maintenance"
- Abstract generation becomes the path for leveraging the huge accumulation of chat_logs
- vault_maintenance_config.md (00_meta/) lets adopters control the cadence

**Negative**:

- Need to manage 5 tracks (4 levels + abstract generation)
- There are ambiguous cases at the level boundaries (a "weekly" one that became "monthly," etc.)
- Level 4 (seasonal correction) fires only four times a year, so it's easy to forget

**Mitigation**:

- Set the cadence in vault_maintenance_config.md and make it function as a reminder
- Make it an implicit rule to "treat it as one level higher" when the level boundary is ambiguous
- Tie Level 4 to Framework Fable updates and the like to make it harder to forget

## Alternatives Considered

### Option A: single level (delegate all maintenance to Cursor)

An option that does not classify maintenance work and delegates all of it to Cursor.

**Reasons for rejection**:

- Making Level 1 (daily trigger) a Cursor delegation makes the invocation cost too high
- Interposing Cursor at every Chat save is excessive

### Option B: three levels (only Level 1 + Level 3; merge Level 2 and Level 4)

An option to merge weekly and monthly, and to include seasonal correction in monthly.

**Reasons for rejection**:

- Weekly and monthly differ significantly in the granularity of the work
- Seasonal correction has a "major version upgrade" character, and separating it from monthly is more natural

### Option C: merge abstract generation into Level 3

An option not to have abstract generation stand alone, but to perform it as part of Level 3 (monthly correction).

**Reasons for rejection**:

- Abstract generation should be done at any timing at the adopter's discretion (does not fit periodization)
- Its nature differs from the other Level 3 work (consistency checks, handoff archiving)
- Keeping it independent as a parallel operation allows flexible firing according to intent

## Related

- **Prerequisite ADRs**:
  - ADR-0003 (Skill / Project / Vault 3-layer architecture; the Skill owns Level 1)
  - ADR-0008 (Cursor-delegation judgment; Level 2 and above are basically Cursor-delegated)
- **Successor ADRs**:
  - ADR-0011 (Directory-structure overhaul, a representative example of Level 4)
- **Related specs**:
  - `../specs/maintenance-four-levels.md` (detailed spec of the four levels) *(English translation pending)*
  - `../specs/abstract-generation.md` (operational spec of abstract generation) *(English translation pending)*
- **Source record**: `10_chat_logs/2026/07/2026-07-13_maintenance-operation-design.md`
- **Implementation**: `vault-templates/00_meta/vault_maintenance_config.md` (config file for adopters)

## Change Log

- 2026-07-13: initial version (finalized the parallel operation of 4 levels + abstract generation)

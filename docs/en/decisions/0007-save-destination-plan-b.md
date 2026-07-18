---
audience: mixed
date: 2026-07-13
keywords:
- save-destination
- plan-b
- inbox
- classification
- save-flow
- gtd
- 3-second-rule
- english
lang: en
related_adrs:
- '0003'
- 0008
- '0011'
related_ja: docs/ja/decisions/0007-save-destination-plan-b.md
related_specs:
- ../guidelines/save-decision-flow
- reference-level-system
status: accepted
summary: Decision to adopt the policy that Claude judges from the Chat context and
  saves Chat content directly to the appropriate directory (Option B). The via-inbox
  Option A is explicitly rejected because it caused a vicious cycle in actual operation.
tags:
- adr
- save
- important
title: 'ADR-0007: Save Destination Philosophy: Right Place From the Start (Option
  B)'
title_ja: 'ADR-0007: 保存先思想: 最初から適切な場所へ(案 B)'
type: adr
created: 2026-07-15 08:29:04+09:00
updated: 2026-07-15 08:29:04+09:00
---

## Summary

Decision to adopt the policy that, when saving Chat content to the Vault, Claude judges from the Chat context and saves directly to the appropriate directory (Option B). The "route everything through inbox" option (Option A) is explicitly rejected because it caused a vicious cycle in actual operation.

## Context

When saving Chat content to the Vault, three options were considered:

- **Option A**: save everything to `90_inbox/` first and classify/organize later
- **Option B**: Claude judges from the Chat context and saves to the appropriate place from the start
- **Option C**: ask the user "where should I save this?" every time

The debate was about how to balance classification cost, UX, and the risk of misjudgment.

Right after the initial start of Vault operation, Option A (via inbox) was implicitly adopted. However, after a few days of operation, the inbox kept accumulating and classification work was postponed, forming a vicious cycle. Based on that experience, a design decision was made anew.

## Decision

**Adopt Option B (appropriate place from the start).**

- Claude (the `vault-manager` Skill) judges from the Chat content and saves directly to the appropriate directory
- Explicitly define the save-decision flow (in SKILL.md) and finalize the typical save destination per type
- When unsure, fall back to `90_inbox/` under a **3-second rule** (but only as an exception, do not normalize it)
- Do not ask the user "where should I save this?" (avoid UX friction)

### Skeleton of the save-decision flow

Details are defined in SKILL.md; judge in the following order:

1. Is it a diary, reflection, or goal? → `50_self/` (auto-set `sensitive: true`)
2. Is it strongly chat-log-like (a record of deliberation/discussion)? → `10_chat_logs/YYYY/MM/`
3. In-progress or published note? → `20_notes/wip/` or `published/`
4. New idea (not yet turned into a repository)? → `30_projects/_ideas/incubating/` or `active/`
5. Design or decision for a specific repository? → `30_projects/<RepoName>/logs/YYYY/MM/`
   - Exception: finalized decision → append to `design-decisions.md`
   - Exception: new unresolved issue → append to `open-questions.md`
   - Exception: snapshot of the current state → update `handoff/current-state.md`
6. General-purpose knowledge? → `40_knowledge/<category>/`
7. Hard to judge? → `90_inbox/` (only when the 3-second rule fires)

## Consequences

**Positive**:

- Avoids the bad habit of postponing classification work
- Minimum dialogue cost with the user (no confirmation questions in response to a save instruction)
- By being organized into the relevant project's folder immediately upon saving, later referenceability is high
- Maintains a state where Cursor delegation (bulk operations of 3+ files) is less likely to fire

**Negative**:

- Claude's misjudgments are possible (saving to the wrong place)
- The judgment cost is concentrated on Claude's side (slight increase in token consumption)
- The application criterion for the "3-second rule" is subjective, so interpretation may waver by Skill implementer (Claude)

**Mitigation**:

- Misjudgments are traceable and fixable via Git history (moves are delegated to Cursor)
- Explicitly define the save-decision flow in SKILL.md to minimize variance
- The 3-second rule includes the meta-rule "if it fires frequently, add to the judgment flow on the SKILL.md side"

## Alternatives Considered

### Option A: classify via inbox

An option to save all Chat content to `90_inbox/` first and let the adopter classify/organize it later.

**Reasons for rejection**:

- Experienced a vicious cycle in actual operation where the inbox kept accumulating and classification was postponed (became evident in the first few days)
- "Sort it out later" is often not done (a counterexample to GTD's Inbox Zero principle)
- Immediately after saving, information is not placed in "where you would go to look for it," so referenceability is low

Details: `id-ref-removed` *(English translation pending)*

### Option C: ask the user every time

An option to ask the user "where should I save this?" every time there is a save instruction.

**Reasons for rejection**:

- High UX friction (the psychological cost of saving rises, and valuable discussions stop being saved)
- Puts the burden on the user to decide in scenes where they want to delegate the judgment
- Overconfirming out of fear of Claude's misjudgment reduces the AI's usefulness

## Related

- **Prerequisite ADR**: ADR-0003 (Skill / Project / Vault 3-layer architecture, the premise that the Skill holds the save decision)
- **Successor ADRs**:
  - ADR-0008 (Cursor-delegation judgment, the threshold for multi-file operations)
  - ADR-0011 (Directory-structure overhaul, expansion of save destination options)
- **Related specs**:
  - `../guidelines/save-decision-flow.md` (details of the save-decision flow) *(English translation pending)*
  - `../specs/reference-level-system.md` (correspondence with the reference-level system) *(English translation pending)*
- **Source record**: `10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md`

## Change Log

- 2026-07-13: initial version (adopted Option B based on reflection on inbox operation)

---
audience: mixed
date: 2026-07-14
keywords:
  - maintenance
  - four-levels
  - abstract-generation
  - english
lang: en
related_adrs:
  - "0008"
  - "0009"
related_ja: docs/ja/maintenance-guide.md
related_specs:
  - maintenance-four-levels
  - abstract-generation
status: published
summary: Overview of Vault's four-level maintenance operation, letting readers grasp the position and overall picture of each level.
title: Maintenance Guide
title_ja: 保守運用ガイド
type: overview
created: 2026-07-14T20:50:04+09:00
updated: 2026-07-14T20:50:04+09:00
---

## Summary

Overview of Vault's four-level maintenance operation. Detailed specs are referenced separately; this file lets readers grasp the position and overall picture of each level.

## Overview of Maintenance Operations

The longer a Vault is used, the more "entropy" accumulates — drift in controlled vocabulary, missing Front Matter fields, deviation from naming conventions, bloated handoff files, and so on. To address this, Vault-Framework defines **four levels of maintenance operation**.

| Level | Frequency | Owner | Typical work |
|---|---|---|---|
| Level 1 | Daily (event-driven) | Claude alone | Auto-correcting controlled vocabulary, completing Front Matter |
| Level 2 | Weekly | Delegated to Cursor | Re-classification, detecting broken links |
| Level 3 | Monthly | Delegated to Cursor | Structural consistency checks, handoff archiving |
| Level 4 | Seasonal (every 3 months) | Led by Naoya + Cursor | Large-scale structural changes, cleanup of deprecated tags |

The design is such that higher-frequency levels do lighter work, and lower-frequency levels do heavier work.

## Level 1: Daily Trigger (Automatic)

Every time a Chat saves or references something, Claude (the Skill) automatically checks and fixes:

- Controlled-vocabulary spelling drift (e.g., `ChatLog` → `chat_log`)
- Completing required Front Matter fields
- Warning about naming-convention violations

The intervention cost to Naoya is near zero — this happens without being noticed.

## Level 2: Weekly Correction (Delegated to Cursor)

Once a week, with Naoya's approval, Cursor performs:

- Re-classifying files that landed in `90_inbox/`
- Checking consistency against `vocabulary.md`
- Detecting broken wikilinks

## Level 3: Monthly Correction (Delegated to Cursor)

Once a month, the following is performed:

- Confirming each project's `handoff/current-state.md` is up to date
- Archiving into `recent-changes/` if `current-state.md` has become bloated
- Analyzing controlled-vocabulary usage frequency and proposing extension candidates

## Level 4: Seasonal Correction (Led by Naoya)

Roughly once every 3 months, larger-scale work is performed, such as:

- Restructuring directories (e.g., revisiting the sub-classification of `10_chat_logs/`)
- Bulk cleanup of deprecated tags/types
- Handling major version upgrades of the Skill or Vault-MCP

## Abstract Generation: A Parallel Operation

Independent from the four-level maintenance operation, there is a parallel process called **abstract generation**. This is the process of generating abstract documents — ADRs, specs, rejected-alternatives — from concrete chat_logs, performed at any timing (monthly to quarterly).

All 16 ADRs, 16 rejected-alternatives, and 8 specs for Vault-Framework itself were generated through this abstract-generation process, from accumulated chat_logs and design discussions.

## Why We Split Into 4 Levels

Rather than a single "maintenance" concept, the operation was split into 4 levels along the axes of frequency and ownership, for the following reasons:

- **Different frequencies call for different owners**: Delegating minor daily fixes to Cursor would be inefficient; conversely, having Claude alone handle a large-scale monthly check would carry too high a judgment cost
- **Judgment weight and frequency are inversely correlated**: High-frequency work tends to be resolvable with mechanical rules, while low-frequency work tends to require human judgment

## Related

- [ADR 0008: Criteria for Cursor delegation](../ja/decisions/0008-cursor-delegation-by-maintenance-level.md) *(English translation pending)*
- [ADR 0009: Four-level maintenance + abstract generation](../ja/decisions/0009-four-level-maintenance-operation.md) *(English translation pending)*
- [maintenance-four-levels spec: Detailed maintenance specification](./specs/maintenance-four-levels.md) *(English translation pending)*
- [abstract-generation spec: Detailed abstract-generation specification](./specs/abstract-generation.md) *(English translation pending)*

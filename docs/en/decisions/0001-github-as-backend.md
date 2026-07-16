---
audience: mixed
date: 2026-07-13
id: pj-2026-07-15-e78f
keywords:
- github
- backend
- vault
- obsidian
- storage
- philosophy
- single-source-of-truth
- english
lang: en
related_adrs:
- '0002'
- '0003'
- '0012'
related_ja: docs/ja/decisions/0001-github-as-backend.md
related_specs: []
status: accepted
summary: Decision to adopt a GitHub repository as the de facto backend for persisting
  Chat content. Obsidian is the editing UI; the source of truth is GitHub. This decision
  is the starting point of the entire Framework.
tags:
- adr
- important
title: 'ADR-0001: Adopting GitHub-as-a-Backend'
title_ja: 'ADR-0001: GitHub-as-a-Backend の採用'
type: adr
created: 2026-07-14 21:14:17+09:00
updated: 2026-07-14 21:14:17+09:00
aliases:
- pj-2026-07-15-e78f
- adr-0001
---

## Summary

Decision to adopt a GitHub repository (`nkhippo/Vault`) as the de facto backend storage for persisting Chat content. Obsidian is used as the editing UI, but the source of truth is GitHub. This decision is the starting point for the entire Framework's design.

## Context

Naoya had been running a personal knowledge base in Obsidian, but the lack of a systematic place to aggregate Chat content was a problem. Although multiple devices were synced via Obsidian Sync + iCloud, integration with Claude was mostly manual copy-paste, which led to the following issues:

- Claude could not reference past discussions or decisions (no memory across sessions)
- Valuable discussions were lost due to the friction of saving
- Search and cross-referencing were inefficient

Three options were compared as a save strategy for Chat aggregation:

- **Option 1**: GitHub-as-a-Backend (a GitHub repository as the de facto backend, Obsidian as the editing UI)
- **Option 2**: Obsidian-Sync-led (paid Obsidian Sync as the primary axis, GitHub as auxiliary)
- **Option 3**: Hybrid configuration (running both in parallel)

Key evaluation axes for each option: strength of version control, multi-device support, ease of Claude integration, cost, vendor lock-in, and the possibility of future publishing/packaging.

## Decision

**Adopt Option 1 (GitHub-as-a-Backend).** The following were finalized:

- The source of truth for the vault: `nkhippo/Vault` (a GitHub repository)
- Obsidian is used as the editing UI (local mirror via iCloud Drive, changes pushed to GitHub)
- Reads and writes from Claude go through the MCP server (Vault-MCP), which calls the GitHub API
- All changes remain in Git history and are recoverable by SHA

## Consequences

**Positive**:

- All changes are trackable via Git history; SHA-based recovery is always possible
- Redundancy through two-stage backup: iCloud Drive + GitHub
- Complex bulk operations (renames, wikilink rewrites, etc.) can be delegated to Cursor
- Room for future public release / Fable packaging (a premise for splitting off the Framework)
- Security can be strengthened with a fine-grained PAT
- The MCP server implementation is consolidated onto a single GitHub API, keeping it simple

**Negative**:

- Two write paths — direct editing (Obsidian) and via Claude (MCP) — coexist, requiring care about sync timing
- Due to iCloud sync lag, a Claude reference made right after an edit may see a stale state
- MCP response time depends on GitHub API rate/latency
- When Naoya is offline, Obsidian editing is possible but Claude integration does not work

**Mitigation**:

- Large-scale operations are delegated to Cursor to ensure consistency
- The retry + abort rule on MCP connection failure (ADR-0016) forbids "continuing on guesswork"

## Alternatives Considered

### Option 2: Obsidian-Sync-led

An option using Obsidian Sync (Obsidian's official paid sync service) as the primary axis, with GitHub as auxiliary backup. For details, see [[../rejected-alternatives/vault-composition-plan-2-obsidian-sync.md]].

**Reasons for rejection**:
- Vendor lock-in (dependent on Obsidian's continued operation)
- Monthly subscription is costly for personal use
- Cannot leverage GitHub's history management, PR, and Issue features
- Claude integration would go through the Obsidian Sync API, requiring an extra integration layer

### Option 3: Hybrid configuration

An option running Obsidian Sync and GitHub in parallel, leveraging the strengths of each. For details, see [[../rejected-alternatives/vault-composition-plan-3-hybrid.md]].

**Reasons for rejection**:
- Cannot maintain a single source of truth; high integration cost when divergence occurs
- Complexity of operating two sync paths
- The MCP implementation would need judgment logic for "which is authoritative," spiking complexity

## Related

- **Successor ADRs**:
  - ADR-0002 (Adopting Cloudflare Workers as the MCP platform)
  - ADR-0003 (Skill / Project / Vault 3-layer architecture)
  - ADR-0012 (Adopting a fine-grained PAT, strengthening GitHub integration security)
- **Related specs**: none
- **Source record**: `10_chat_logs/2026/07/2026-07-13_vault-system-design-inception-to-completion.md`
- **Rejected alternatives**:
  - `../rejected-alternatives/vault-composition-plan-2-obsidian-sync.md`
  - `../rejected-alternatives/vault-composition-plan-3-hybrid.md`

## Change Log

- 2026-07-13: Initial version (adopted Option 1 from a comparison of 3 vault-composition options)

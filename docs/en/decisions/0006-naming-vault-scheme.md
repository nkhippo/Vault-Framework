---
audience: mixed
date: 2026-07-13
id: adr-0006
keywords:
  - naming
  - vault
  - vault-mcp
  - vault-framework
  - convention
  - rename
  - personal-vault
  - hashicorp-collision
  - english
lang: en
related_adrs:
  - "0001"
  - "0005"
related_ja: docs/ja/decisions/0006-naming-vault-scheme.md
related_specs:
  - file-naming
status: accepted
summary: Decision that finalized the naming of the three repositories (Vault / Vault-MCP / Vault-Framework). The original personal-vault-* prefix proposal was withdrawn; naming was unified to Vault-* for simplicity. Internal designation and external name are unified.
tags:
  - adr
  - naming
  - important
title: "ADR-0006: Naming Scheme: Vault / Vault-MCP / Vault-Framework"
title_ja: "ADR-0006: 命名スキーム: Vault / Vault-MCP / Vault-Framework"
type: adr
created: 2026-07-15T08:28:27+09:00
updated: 2026-07-15T08:28:27+09:00
---

## Summary

Decision that finalized the naming of the three repositories (`Vault` / `Vault-MCP` / `Vault-Framework`). The original `personal-vault-*` prefix proposal was withdrawn, and the naming was unified to `Vault-*` for simplicity. The internal designation and the external name are unified.

## Context

In splitting off Vault-Framework (ADR-0005), the naming of the three repositories had to be finalized. The following eight naming candidates were compared:

- Option A: `Vault` only (do not distinguish Framework or MCP by name)
- Option B: `personal-vault-*` prefix unified (personal-vault, personal-vault-mcp, personal-vault-framework)
- Option C: `<Naoya>-Vault` series (naoya-vault, naoya-vault-mcp)
- Option D: metaphorical series (brain/memory metaphors such as Cerebro / Cortex / Memex)
- Option E: Codex series (codex, codex-mcp)
- Option F: Archive / Ledger series (archive-* / ledger-*)
- Option G: Japanese naming (記録所, 知識庫, etc.)
- Option H: function-name only (descriptive naming such as chat-storage, mcp-server)

A separate point was whether to keep the internal designation and the external name (GitHub repository name) different. An early proposal had a two-tier structure of "internal `Vault` / external `personal-vault-*`," but the policy was later shifted to "unify for simplicity."

## Decision

**Naming: unified as `Vault` / `Vault-MCP` / `Vault-Framework`**

| Target | GitHub repository name | iCloud folder name | Internal designation |
|---|---|---|---|
| The vault itself | `Vault` | `Vault` | Vault |
| MCP server | `Vault-MCP` | `Vault-MCP` | Vault-MCP |
| Framework | `Vault-Framework` | `Vault-Framework` | Vault-Framework |

### Notation rule for the MCP connector name

Three notations that refer to the same entity coexist — note this:

- **Display name (in the Claude UI)**: space-separated, capitalized (e.g., `Vault MCP`)
- **Repository name**: hyphen-separated, capitalized (e.g., `Vault-MCP`)
- **Cloudflare Workers URL**: lowercase with hyphens (e.g., `vault-mcp.<subdomain>.workers.dev`)

### Recommendation for adopters

Recommend the same naming to Framework adopters. Offer a simple experience: "if an adopter names their own GitHub repository `Vault`, everything works as the documentation says." However, include guidance on how to handle the collision risk with HashiCorp Vault in the Framework's `docs/en/naming-conventions.md`.

## Consequences

**Positive**:

- Simple, unified feel, minimum typing cost
- Minimum customization burden for adopters (no need to manage a two-tier internal/external name)
- Consistent documentation phrasing (the vault repository = `Vault`, the concept = vault — the two can be distinguished)
- When the Framework is turned into a Fable manual, the naming can be explained mechanically

**Negative**:

- Name collision with HashiCorp Vault (they mix in GitHub search; potential confusion)
- May be an obstacle when a third party forks it on public release
- Because it overlaps with the common noun "vault," there are situations where context is needed to tell them apart

**Mitigation**:

- Zero practical harm while operating as a private repository (third parties cannot see it)
- The public-release guide presents alternative names (`<YourName>-Vault`, `Personal-Vault`, `Knowledge-Vault`, etc.)
- In the documentation, use the glossary to clarify the distinction between "capitalized Vault as the repository" and "lowercase vault as the concept" (see the related spec in ADR-0003)

## Alternatives Considered

### Option B: `personal-vault-*` prefix (once adopted → withdrawn)

This prefix proposal was adopted early on and was even incorporated into the initial structural plan for Vault-Framework. It was later withdrawn for the following reasons:

- Verbosity (`personal-vault-mcp` has a high typing cost)
- The word "personal" feels off for adopters (a third-party adopter would feel "this isn't mine")
- `Vault-*` is also better in URL brevity

Details: [[../rejected-alternatives/naming-plan-personal-vault-prefix.md]] *(English translation pending)*

### Other rejected options

- **Option A** (Vault only): impossible to distinguish MCP and Framework. Details: [[../rejected-alternatives/naming-plan-vault-only.md]] *(English translation pending)*
- **Option D** (Cerebro/Cortex series): overly ornamental; hinders understanding of function. Details: [[../rejected-alternatives/naming-plan-cerebro-cortex.md]] *(English translation pending)*
- **Option E** (Codex series): risk of collision with OpenAI Codex. Details: [[../rejected-alternatives/naming-plan-codex.md]] *(English translation pending)*
- **Option F** (Archive/Ledger series): feels "finished" or evokes finance. Details: [[../rejected-alternatives/naming-plan-archive-ledger.md]] *(English translation pending)*
- **Option G** (Japanese naming): a barrier to multilingual support; reduces readability of GitHub URLs. Details: [[../rejected-alternatives/naming-plan-japanese.md]] *(English translation pending)*
- **Option H** (function-name only): lacks branding; the project loses a sense of unity. Details: [[../rejected-alternatives/naming-plan-functional-only.md]] *(English translation pending)*

## Related

- **Prerequisite ADRs**: ADR-0001 (GitHub-as-a-Backend, the premise for repository naming), ADR-0005 (early split of the Framework, the premise for the 3-repository structure)
- **Successor ADRs**: none (this naming is the foundation referenced by other ADRs)
- **Related spec**: `../specs/file-naming.md` (corresponds to the kebab-case rule for file names) *(English translation pending)*
- **Source records**:
  - `10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md`
  - Withdrawal session: late night of 2026-07-13 (after the initial structure was built)

## Change Log

- 2026-07-13 (noon): initial version (adopted the `personal-vault-*` prefix proposal)
- 2026-07-13 (evening): withdrawn; unified to `Vault-*` (current)

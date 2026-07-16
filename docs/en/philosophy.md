---
audience: mixed
date: 2026-07-14
keywords:
- philosophy
- github-as-a-backend
- obsidian
- ai-first
- english
lang: en
related_adrs:
- '0001'
related_ja: docs/ja/philosophy.md
related_specs: []
status: published
summary: Explains the GitHub-as-a-Backend philosophy and the premise that AI is the
  primary reader, and its relationship with the Obsidian brand.
title: 'Philosophy: GitHub-as-a-Backend'
title_ja: '思想: GitHub-as-a-Backend'
type: overview
created: 2026-07-14 20:49:11+09:00
updated: 2026-07-14 20:49:11+09:00
id: pj-2026-07-15-4872
aliases:
- pj-2026-07-15-4872
---

## Summary

Explains the core philosophy behind Vault-Framework: "GitHub-as-a-Backend." Covers the central idea of using a GitHub repository as the canonical data store, structuring it with Markdown + Front Matter, and having AI (Claude) read and write to it.

## What is GitHub-as-a-Backend

The most fundamental design decision in Vault-Framework is **adopting a GitHub repository as the canonical data store for a personal knowledge base**.

Typical "second brain" tools (Notion, proprietary Obsidian sync services, dedicated apps) often depend on a dedicated cloud service or a proprietary data format. Vault-Framework avoids this and instead adopts a GitHub repository as its backend, which has the following properties:

- **Plain text (Markdown)**: No lock-in; readable and writable by any tool
- **Git history**: Every change is tracked, making recovery from mistakes easy
- **REST API**: Programmatically readable and writable (the foundation for the MCP server implementation)
- **Free or low-cost**: A GitHub free plan is sufficient to operate
- **Existing ecosystem**: Existing features like GitHub Actions, Issues, and PRs can be leveraged in the future

In short, this achieves a separation where "data lives in GitHub, but the UI and access method can be chosen freely."

## The Premise That AI Is the Primary Reader

Another core idea in Vault-Framework is the premise that **the primary reader of this Vault is not a human, but an AI (Claude)**.

Traditional knowledge bases are designed with human readers in mind (prioritizing visual polish and ease of navigation). Vault-Framework flips this and instead prioritizes:

- **Structured Front Matter**: Metadata that lets AI quickly grasp the content
- **Consistent naming conventions**: Lets AI locate files without guessing
- **Explicit cross-links**: Lets AI trace related information
- **Controlled vocabulary**: Improves AI's judgment accuracy

The human (Naoya) browses and edits this data through tools like Obsidian, but day-to-day interactions (saving, searching, referencing) mostly happen through Claude. This "AI-first" design philosophy runs through the entire Framework — the Front Matter schema, naming conventions, reference-level system, and more.

## Relationship With the Obsidian Brand

Because Vault-Framework is Markdown-file-based, it has strong affinity with Obsidian (a popular Markdown note-taking app). However, Vault-Framework is designed to not depend on Obsidian.

- **Obsidian is one option among UI layers**: Opening the vault in Obsidian automatically enables wikilinks and graph view. But the vault works completely even without Obsidian (it can also be operated via GitHub's web UI, any text editor, or through Claude)
- **Naming independence**: Early naming candidates for the vault included ones referencing "Obsidian," but ultimately a naming scheme independent of the Obsidian brand (`Vault`) was adopted (see ADR-0006 for details). This was also a deliberate design decision to eliminate dependency on the Obsidian tool at the naming level
- **Adoption of wikilink notation**: The `[[path/to/file.md]]` wikilink notation itself follows a convention widely used in Obsidian, but it still functions as readable plain text on GitHub (even though it isn't rendered there)

## Connection to Design Principles

This GitHub-as-a-Backend philosophy connects to the following design decisions across the Framework:

- **Skill / Project / Vault 3-layer structure** (see architecture.md): Separating data (Vault) from logic (Skill) is possible precisely because Vault sits on a neutral backend — GitHub
- **Bridging via the MCP server** (see mcp-server-reference/): An MCP server that calls the GitHub API via Cloudflare Workers bridges AI and the GitHub repository
- **Naming conventions and directory structure** (see naming-conventions.md): Designed so AI can construct exact paths without guessing
- **Four-level maintenance operation** (see maintenance-guide.md): Enables staged maintenance operations that leverage Git's commit history

## Related

- [ADR 0001: Adoption of GitHub-as-a-Backend](../ja/decisions/0001-github-as-backend.md) *(English translation pending)*
- [Architecture: Skill / Project / Vault 3-layer](./architecture.md)

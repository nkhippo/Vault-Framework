---
title: Vault Project Instructions (thin template, English)
type: template
audience: human_primary
status: draft
date: 2026-07-13
keywords: [vault-project, instructions, template, en, thin]
summary: English thin Instructions template for the Vault project. Pending full translation.
---

# Vault Project Instructions Template (English)

<!-- TODO: Translate vault-project.ja.md body -->

Paste the following into Claude Projects Instructions. Replace `<your-*>` placeholders.

```
# Vault - Project Instructions

This project is the primary chat hub for <your-name>'s personal vault operations.

## Required actions at session start

Assuming Skill `vault-manager` is enabled:

1. Confirm MCP connector `Vault MCP` is connected
2. If connected, read `00_meta/project_instructions_vault.md` via MCP
3. Follow that content for the rest of the session

If MCP is not connected, tell <your-name> and operate within Skill + userMemories only.
When vault reference is required, say honestly that MCP is not connected.
```

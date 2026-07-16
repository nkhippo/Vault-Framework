---
title: Vault MCP Server Reference
title_ja: Vault MCP サーバ参照
type: reference
audience: mixed
status: published
date: 2026-07-13
keywords:
- mcp
- mcp-server
- cloudflare-workers
- vault-mcp
- reference
- deployment
summary: Reference documentation for the Vault MCP server implementation, deployment,
  and configuration.
id: pj-2026-07-13-d955
aliases:
- pj-2026-07-13-d955
---

# Vault MCP Server Reference

The Vault MCP server is implemented in a separate repository. This directory provides deployment guides and reference documentation.

## Implementation

- **Repository**: [nkhippo/Vault-MCP](https://github.com/nkhippo/Vault-MCP) (private)
- **Runtime**: Cloudflare Workers (TypeScript, nodejs_compat)
- **Protocol**: Model Context Protocol (MCP)
- **Client**: Claude Pro Connectors

## Available Tools (Phase 1+2)

- `list_directory(path)` - List directory contents
- `get_file_content(path)` - Read file content
- `create_note(path, frontmatter, body, commit_message?)` - Create new note
- `update_note(path, mode, content, update_frontmatter?)` - Update existing note
- `delete_note(path, commit_message?)` - Delete note

## Documentation

- [[pj-2026-07-13-2157|Setup Guide]] - Deployment to Cloudflare Workers
- [[pj-2026-07-13-9d1f|Environment Variables]] - Required env vars and PAT scopes
- [[pj-2026-07-13-8f48|Design Rationale]] - Why Cloudflare Workers, why Fine-grained PAT

## Related

- ADR: [[pj-2026-07-13-bccd|`docs/ja/decisions/0002-cloudflare-workers-for-mcp.md`]]
- ADR: [[pj-2026-07-13-9107|`docs/ja/decisions/0012-fine-grained-pat-adoption.md`]]
- Setup: [[pj-2026-07-13-1341|`docs/ja/setup/02-deploy-mcp-server.md`]]

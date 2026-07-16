---
title: Environment Variables Reference
title_ja: 環境変数リファレンス
type: reference
audience: mixed
status: draft
date: 2026-07-13
keywords:
- env
- secrets
- pat
- fine-grained
- wrangler
summary: Cloudflare Secrets / wrangler.toml 変数と Fine-grained PAT スコープの参照。
id: pj-2026-07-13-9d1f
aliases:
- pj-2026-07-13-9d1f
---

## Summary

<!-- TODO: 環境変数の概要 -->

## Environment Variables (Cloudflare Secrets)

| Variable | Required | Description | Example |
|---|---|---|---|
| `GITHUB_TOKEN` | Yes | Fine-grained PAT with Contents R/W | ghp_xxx (redacted) |
| `MCP_ACCESS_TOKEN` | Yes | Random token for connector auth | (generate with `openssl rand -hex 32`) |

## Wrangler Variables (wrangler.toml)

| Variable | Description | Example |
|---|---|---|
| `GITHUB_OWNER` | GitHub username or org | `<your-github-username>` |
| `GITHUB_REPO` | Vault repository name | `Vault` |
| `DEFAULT_BRANCH` | Default branch | `main` |

## Fine-grained PAT Permissions

Required permissions:
- Repository access: Only select repositories → `<your-github-username>/Vault`
- Repository permissions:
  - Contents: Read and write
  - Metadata: Read-only (automatic)

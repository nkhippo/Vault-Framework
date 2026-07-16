---
audience: mixed
date: 2026-07-13
id: pj-2026-07-15-f3be
keywords:
- mcp
- cloudflare-workers
- platform
- cloud-run
- deployment
- cold-start
- wrangler
- edge
- english
lang: en
related_adrs:
- '0001'
- '0012'
- '0015'
- '0016'
related_ja: docs/ja/decisions/0002-cloudflare-workers-for-mcp.md
related_specs: []
status: accepted
summary: Decision to adopt Cloudflare Workers from 8 candidates as the MCP server
  hosting platform. Near-0ms cold start, a generous free tier, and a simple operational
  model were the deciding factors.
tags:
- adr
- mcp
- platform
title: 'ADR-0002: Cloudflare Workers for the MCP Platform'
title_ja: 'ADR-0002: MCP プラットフォームに Cloudflare Workers'
type: adr
created: 2026-07-14 21:15:01+09:00
updated: 2026-07-14 21:15:01+09:00
aliases:
- pj-2026-07-15-f3be
- adr-0002
---

## Summary

Decision to adopt Cloudflare Workers, chosen from 8 candidates, as the hosting platform for the MCP server. Near-0ms cold start, a generous free tier, and a simple operational model were the deciding factors.

## Context

To implement Vault-MCP, the following 8 platform candidates were compared:

- **Candidate 1**: Cloudflare Workers (serverless, Edge)
- **Candidate 2**: Google Cloud Run (serverless, container)
- **Candidate 3**: Fly.io (always-on VM/container)
- **Candidate 4**: Railway (always-on, developer-oriented PaaS)
- **Candidate 5**: Render (always-on, simple PaaS)
- **Candidate 6**: Vercel (Edge Functions, oriented toward Next.js-style workloads)
- **Candidate 7**: Netlify (Edge Functions, oriented toward static sites)
- **Candidate 8**: Deno Deploy (Deno-native, Edge)

Evaluation axes:

- **Cold-start time**: MCP is an interactive workload, so this directly affects UX
- **Cost model**: assuming personal use — initial investment and monthly cost
- **State retention**: MCP is basically stateless, but state may be needed for rate limiting, etc.
- **TypeScript support**: possible on all candidates, but toolchain maturity differs
- **Ease of deployment**: consistency of CLI experience across wrangler, gcloud, fly, etc.
- **Future potential**: support for Anthropic's MCP ecosystem, possibility of supporting other LLMs

## Decision

**Adopt Cloudflare Workers.**

Key deciding factors:

1. **Effectively 0ms cold start**: decisively affects the MCP interactive experience. Cloud Run is at best several hundred ms; always-on options like Fly.io / Railway make this negligible but incur monthly charges
2. **Generous free tier**: the assumed personal-use volume (under 100k req/day) fits within the free tier
3. **Simple operation with `wrangler.toml` + Secrets**: encrypted management of environment variables is self-contained in Secrets, and GitHub Actions integration is easy
4. **Room for future expansion**: Durable Objects can later add rate limiting or state management
5. **Edge network**: low latency from anywhere in the world (comfortable even when working while traveling)

### Implementation stack

- Cloudflare Workers (TypeScript, `nodejs_compat` flag)
- `@modelcontextprotocol/sdk` (latest version)
- `@octokit/core` + `@octokit/request` (GitHub API)
- `yaml` package (Front Matter processing)
- `zod` (input validation)

## Consequences

**Positive**:

- Effectively zero cold start, making the MCP interactive experience comfortable
- No cost at the assumed personal-use volume
- Secrets management is self-contained on the Cloudflare side, lowering the risk of tokens leaking into code
- Room for future feature expansion (Durable Objects, KV, R2, etc.)
- Low latency worldwide via the Edge network

**Negative**:

- Per-request CPU time limit on Workers (Free plan: 10ms, Paid plan: 30 seconds)
- Node.js compatibility requires the `nodejs_compat` flag, and some APIs are unavailable
- Need to learn Cloudflare-specific operations (wrangler, Dashboard)
- Vendor lock-in (dependence on Cloudflare's continued operation)

**Mitigation**:

- For Vault-MCP's use case, even 10ms CPU time is usually sufficient (roughly a GitHub API call + Front Matter parsing)
- With the `nodejs_compat` flag, `Buffer` and `crypto` are available; @modelcontextprotocol/sdk works with this
- The learning cost of wrangler can be recouped in about half a day
- Because the implementation conforms to the MCP protocol, migration to another platform is possible in the future

## Alternatives Considered

### Candidate 2: Google Cloud Run

Container-based serverless, fully managed.

**Reasons for rejection**:

- Cold start of several hundred ms to seconds (disadvantageous for interactive UX)
- The per-request pricing model could be more expensive than Workers at the assumed personal-use volume
- Complexity of container builds and gcloud CLI operations

Details: [[../rejected-alternatives/mcp-platform-cloud-run.md]]

### Candidates 3-8: Fly.io, Railway, Render, Vercel, Netlify, Deno Deploy

**Reasons for rejection** (consolidated record):

- **Fly.io / Railway / Render**: always-on VM/container model. Overkill for a use case that needs burst responsiveness like MCP, and incurs ongoing monthly charges
- **Vercel / Netlify**: Edge Functions are available, but the feature set centers on Next.js / static sites. Optimization as an MCP server is thin
- **Deno Deploy**: assumes the Deno ecosystem, with uncertainty around compatibility with the Node.js SDK (@modelcontextprotocol/sdk)

Details: [[../rejected-alternatives/mcp-platform-other-candidates.md]]

## Related

- **Prerequisite ADR**:
  - ADR-0001 (GitHub-as-a-Backend, the premise that MCP calls the GitHub API)
- **Successor ADRs**:
  - ADR-0012 (Fine-grained PAT, premised on storage in Cloudflare Secrets)
  - ADR-0015 (Implementation order of the Issue-creation feature, implementation plan on Workers)
  - ADR-0016 (Rule on MCP connection failure, handling 502 errors on the Workers side)
- **Related specs**: none
- **Source record**: `10_chat_logs/2026/07/2026-07-13_platform-selection-and-phase12-completion.md`
- **Vault-MCP-side details**: Decision 1 in `../../30_projects/Vault-MCP/design-decisions.md`

## Change Log

- 2026-07-13: Initial version (selected Cloudflare Workers from 8 candidates)

---
audience: mixed
created: 2026-07-14T04:20:00+09:00
date: 2026-07-13
id: adr-0002
keywords:
  - mcp
  - cloudflare-workers
  - platform
  - cloud-run
  - deployment
  - cold-start
  - wrangler
  - edge
related_adrs:
  - "0001"
  - "0012"
  - "0015"
  - "0016"
related_chats:
  - 10_chat_logs/2026/07/2026-07-13_platform-selection-and-phase12-completion.md
related_specs: []
status: accepted
summary: MCP サーバのホスティングプラットフォームとし、8 候補から Cloudflare Workers を採用した意思決定。コールドスタート 0ms、広い無料枠、シンプルな運用モデルが決定要因。
superseded_by: null
supersedes: null
tags:
  - adr
  - mcp
  - platform
title: "ADR-0002: MCP プラットフォームに Cloudflare Workers"
type: adr
updated: 2026-07-14T04:20:00+09:00
---

## Summary

Vault-MCP サーバのホスティングプラットフォームとして、8 候補から Cloudflare Workers を採用した意思決定。コールドスタート 0ms、広い無料枠、シンプルな運用モデルが決定要因。

## Context

Vault-MCP を実装するにあたり、以下 8 候補のプラットフォームを比較検討した:

- **候補 1**: Cloudflare Workers(サーバレス、Edge)
- **候補 2**: Google Cloud Run(サーバレス、コンテナ)
- **候補 3**: Fly.io(常時稼働 VM/コンテナ)
- **候補 4**: Railway(常時稼働、開発者向け PaaS)
- **候補 5**: Render(常時稼働、簡易 PaaS)
- **候補 6**: Vercel(Edge Functions、Next.js 系ワークロード寄り)
- **候補 7**: Netlify(Edge Functions、静的サイト寄り)
- **候補 8**: Deno Deploy(Deno ネイティブ、Edge)

評価軸:

- **コールドスタート時間**: MCP は対話系ワークロードのため直接 UX に効く
- **費用モデル**: 個人利用の想定、初期投資と月額費用
- **状態保持**: MCP は基本ステートレスだが、レート制御等で必要になる可能性
- **TypeScript サポート**: 全候補で可能だが、ツールチェーンの成熟度が異なる
- **デプロイの手軽さ**: wrangler、gcloud、fly 等の CLI 経験の一貫性
- **将来性**: Anthropic の MCP エコシステム対応、他 LLM 対応可能性

## Decision

**Cloudflare Workers を採用**

主要な決め手:

1. **コールドスタート実質 0ms**: MCP の対話体験に決定的に効く。Cloud Run は最短でも数百 ms、Fly.io / Railway 等の常時稼働は無視できるが月額課金
2. **無料枠が広い**: 個人利用の想定量(100k req/day 以下)は無料枠内で完結
3. **`wrangler.toml` + Secrets の運用がシンプル**: 環境変数の暗号化管理が Secrets で完結、GitHub Actions 統合も容易
4. **将来拡張の余地**: Durable Objects で将来のレート制御やステート管理を追加できる
5. **Edge ネットワーク**: 世界中どこからでも低レイテンシ(旅先での作業でも快適)

### 実装スタック

- Cloudflare Workers(TypeScript、`nodejs_compat` フラグ)
- `@modelcontextprotocol/sdk`(最新版)
- `@octokit/core` + `@octokit/request`(GitHub API)
- `yaml` パッケージ(Front Matter 処理)
- `zod`(入力バリデーション)

## Consequences

**Positive**:

- コールドスタートが実質ゼロで、MCP 対話体験が快適
- 個人利用の想定量では料金がかからない
- Secrets 管理が Cloudflare 側で完結し、コードにトークンが混入するリスクが低い
- 将来的な機能拡張(Durable Objects、KV、R2 等)の余地
- Edge ネットワークで全世界から低レイテンシ

**Negative**:

- Workers のリクエストごとの CPU 時間制限(Free plan: 10ms、Paid plan: 30 秒)
- Node.js 互換性は `nodejs_compat` フラグが必要で、一部 API は使えない
- Cloudflare 独自の運用(wrangler、Dashboard)を学ぶ必要がある
- Vendor Lock-in(Cloudflare の運営継続への依存)

**Mitigation**:

- Vault-MCP の用途では CPU 時間 10ms でも通常は収まる(GitHub API 呼び出し + Front Matter パース程度)
- `nodejs_compat` フラグで `Buffer` や `crypto` は使える。@modelcontextprotocol/sdk はこれで動作
- wrangler の学習コストは半日程度で回収可能
- MCP プロトコル準拠の実装のため、他プラットフォームへの移行は将来的に可能

## Alternatives Considered

### 候補 2: Google Cloud Run

コンテナベースのサーバレス、フルマネージド。

**却下理由**:

- コールドスタート数百 ms〜数秒(対話系 UX に不利)
- 料金モデルがリクエスト単位で、個人利用の想定量では Workers より高くなる可能性
- コンテナビルドと gcloud CLI 操作の複雑度

詳細: [[../rejected-alternatives/mcp-platform-cloud-run.md]]

### 候補 3-8: Fly.io, Railway, Render, Vercel, Netlify, Deno Deploy

**却下理由**(統合記録):

- **Fly.io / Railway / Render**: 常時稼働の VM/コンテナモデル。MCP のような瞬発力が必要な用途にはオーバー、常時月額課金が発生
- **Vercel / Netlify**: Edge Functions は使えるが、Next.js / 静的サイト向けの機能が中心。MCP サーバとしての最適化が薄い
- **Deno Deploy**: Deno エコシステムを前提とし、Node.js SDK(@modelcontextprotocol/sdk)との互換性に不確定要素

詳細: [[../rejected-alternatives/mcp-platform-other-candidates.md]]

## Related

- **前提 ADR**: 
  - ADR-0001(GitHub-as-a-Backend、MCP が GitHub API を叩く前提)
- **後続 ADR**: 
  - ADR-0012(Fine-grained PAT、Cloudflare Secrets への保存前提)
  - ADR-0015(Issue 起票機能の実装順序、Workers 上での実装計画)
  - ADR-0016(MCP 接続失敗時のルール、Workers 側の 502 エラー対応)
- **関連 spec**: なし
- **元記録**: `10_chat_logs/2026/07/2026-07-13_platform-selection-and-phase12-completion.md`
- **Vault-MCP 側の詳細**: `../../30_projects/Vault-MCP/design-decisions.md` の意思決定 1

## Change Log

- 2026-07-13: 初版(8 候補から Cloudflare Workers 選定)

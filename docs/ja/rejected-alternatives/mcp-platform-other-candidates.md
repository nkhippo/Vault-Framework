---
audience: mixed
created: 2026-07-14 05:30:00+09:00
date: 2026-07-13
keywords:
- mcp-platform
- fly-io
- railway
- render
- vercel
- netlify
- deno-deploy
related_adrs:
- '0002'
status: rejected
summary: Vault-MCP のホスティングプラットフォームとして、Cloudflare Workers と Cloud Run 以外の 6 候補(Fly.io、Railway、Render、Vercel、Netlify、Deno
  Deploy)を検討した記録。各候補の個別理由を統合。
superseded_by: '0002'
tags:
- rejected
- mcp-platform
title: '却下案: Fly.io / Railway / Render / Vercel / Netlify / Deno Deploy'
type: rejected_alternative
updated: 2026-07-14 05:30:00+09:00
id: pj-2026-07-13-6540
aliases:
- pj-2026-07-13-6540
---

## Summary

Vault-MCP のホスティングプラットフォームとして、Cloudflare Workers と Google Cloud Run 以外の 6 候補(Fly.io、Railway、Render、Vercel、Netlify、Deno Deploy)を検討した記録。各候補の個別理由の統合。ADR-0002 で Cloudflare Workers を採用。

## What Was Proposed

以下 6 候補を、Vault-MCP のホスティング先として個別に検討:

1. **Fly.io**: エッジロケーションで稼働する VM/コンテナ
2. **Railway**: 開発者向け PaaS、GitHub 連携が容易
3. **Render**: 簡易 PaaS、Web サービスや Cron ジョブに対応
4. **Vercel**: Edge Functions、Next.js エコシステム中心
5. **Netlify**: Edge Functions、静的サイト + 関数
6. **Deno Deploy**: Deno ネイティブの Edge プラットフォーム

## Why It Was Considered

各候補それぞれのメリット:

- **Fly.io**: エッジ配置、常時稼働可能、Docker サポート
- **Railway**: シンプルなデプロイ体験、GitHub リポジトリ push で自動デプロイ
- **Render**: フリープラン有り、静的サイトと関数の統合が容易
- **Vercel**: フロントエンド開発者に馴染み、優秀な CI/CD 統合
- **Netlify**: JAMstack 対応、Serverless Functions の実績
- **Deno Deploy**: Deno エコシステムでの最先端、TypeScript ネイティブ

## Why It Was Rejected

各候補ごとの却下理由:

### Fly.io、Railway、Render

- **常時稼働型 VM/コンテナモデル**: MCP のような瞬発力が必要な用途にはオーバー
- **月額課金**: 常時稼働のため使わない時間もコストが発生
- **リソースサイズの過剰**: MCP は軽量ワークロード、専用 VM/コンテナは overspec

### Vercel、Netlify

- **フロントエンド寄りの最適化**: Next.js / 静的サイト向けの機能が中心
- **MCP サーバとしての最適化が薄い**: Edge Functions は使えるが、MCP プロトコルとの相性の実績が少ない
- **ロードバランサやスケーリング設定が Cloudflare Workers より複雑**

### Deno Deploy

- **Deno エコシステム前提**: Node.js SDK(@modelcontextprotocol/sdk)との互換性に不確定要素
- **成熟度**: Cloudflare Workers と比較すると 2026 時点でエコシステムがまだ小さい
- **将来性**: Deno 自体は素晴らしいが、MCP エコシステムの主流は Node.js 系

## 共通の却下理由

- **コールドスタート**: Cloudflare Workers の実質 0ms に対して、他候補は 100ms〜数秒
- **無料枠**: Cloudflare Workers の 100k req/day 無料枠が個人利用として最も広い
- **Secrets 管理の簡潔さ**: `wrangler.toml` + `wrangler secret put` の運用が最もシンプル
- **Edge ネットワーク**: 世界中のエッジで低レイテンシ、Fly.io 以外は特定リージョン中心

## What Was Chosen Instead

- **採用案**: ADR-0002「MCP プラットフォームに Cloudflare Workers」
- **参照**: [[../decisions/0002-cloudflare-workers-for-mcp.md]]

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_platform-selection-and-phase12-completion.md`
- 対応 ADR: [[../decisions/0002-cloudflare-workers-for-mcp.md]]
- 関連却下案: [[./mcp-platform-cloud-run.md]](Cloud Run 個別記録)

---
audience: mixed
created: 2026-07-14 05:25:00+09:00
date: 2026-07-13
keywords:
- mcp-platform
- cloud-run
- google-cloud
- cold-start
- container
related_adrs:
- '0002'
status: rejected
summary: Vault-MCP のホスティングプラットフォームとして Google Cloud Run を採用する案。コールドスタート数百 ms〜数秒がネックとなり、MCP
  の対話系ワークロードに不利。
superseded_by: '0002'
tags:
- rejected
- mcp-platform
title: '却下案: Google Cloud Run'
type: rejected_alternative
updated: 2026-07-14 05:25:00+09:00
id: pj-2026-07-13-a307
aliases:
- pj-2026-07-13-a307
---

## Summary

Vault-MCP のホスティングプラットフォームとして Google Cloud Run を採用する案。コールドスタート数百 ms〜数秒がネックとなり、MCP の対話系ワークロードに不利。ADR-0002 で Cloudflare Workers を採用。

## What Was Proposed

Vault-MCP を Google Cloud Run にデプロイする案:

- **ホスティング**: Google Cloud Run(サーバレス、コンテナベース)
- **ランタイム**: Node.js または Deno コンテナ
- **認証**: Google Secret Manager で GitHub PAT を管理
- **デプロイ**: `gcloud run deploy` コマンドまたは Cloud Build CI/CD
- **カスタムドメイン**: Cloud Run 用のカスタムドメインマッピング

## Why It Was Considered

- **フルマネージド**: サーバ管理不要、スケーリング自動
- **コンテナベース**: Node.js の任意バージョン、任意依存パッケージが使える(Workers の nodejs_compat 制約なし)
- **Google Cloud エコシステム**: 他の Google Cloud サービス(Firestore、Cloud Storage 等)との統合が容易
- **リクエストごとの課金**: 使わない時は課金されない(常時稼働型と違う)
- **エンタープライズ実績**: 大規模利用の実績豊富、SLA も明確

## Why It Was Rejected

- **コールドスタート数百 ms〜数秒**: MCP の対話体験に決定的に不利。ユーザーが「保存して」と言った時の応答遅延が UX に直接影響
- **料金モデル**: リクエスト単位課金だが、Workers の無料枠と比べると個人利用ではコスト高になる可能性
- **コンテナビルドと `gcloud` CLI 操作の複雑度**: wrangler の簡潔さと比較すると学習・運用コスト高
- **Cloudflare Secrets との比較**: Google Secret Manager は別途 IAM 設定が必要、Cloudflare Secrets の方が直感的
- **Edge ネットワークの活用不可**: Google Cloud Run は特定リージョンで稼働。旅先(海外)からの利用時、レイテンシが増える

## What Was Chosen Instead

- **採用案**: ADR-0002「MCP プラットフォームに Cloudflare Workers」
- **参照**: [[../decisions/0002-cloudflare-workers-for-mcp.md]]

Cloudflare Workers はコールドスタート実質 0ms、Edge ネットワークでレイテンシ最小、`wrangler.toml` + Secrets の運用がシンプル。

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_platform-selection-and-phase12-completion.md`
- 対応 ADR: [[../decisions/0002-cloudflare-workers-for-mcp.md]]
- 関連却下案: [[./mcp-platform-other-candidates.md]](他 6 候補の統合記録)

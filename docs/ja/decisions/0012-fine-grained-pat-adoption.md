---
audience: mixed
created: 2026-07-14 04:25:00+09:00
date: 2026-07-13
id: pj-2026-07-13-9107
keywords:
- fine-grained-pat
- github
- security
- pat
- classic-pat
- least-privilege
- authentication
related_adrs:
- '0001'
- '0002'
- '0015'
related_chats:
- 10_chat_logs/2026/07/2026-07-13_platform-selection-and-phase12-completion.md
related_specs: []
status: accepted
summary: Vault-MCP から GitHub API へのアクセス認証に Fine-grained PAT を採用し、権限を nkhippo/Vault
  の Contents R/W のみに限定した意思決定。事故時の被害範囲を単一リポジトリに閉じ込めるセキュリティ設計。
superseded_by: null
supersedes: null
tags:
- adr
- security
- important
title: 'ADR-0012: Fine-grained PAT の採用'
type: adr
updated: 2026-07-14 04:25:00+09:00
aliases:
- pj-2026-07-13-9107
- adr-0012
---

## Summary

Vault-MCP から GitHub API へのアクセス認証に Fine-grained Personal Access Token(PAT)を採用し、権限を `nkhippo/Vault` の Contents R/W のみに限定した意思決定。事故時の被害範囲を単一リポジトリに閉じ込めるセキュリティ設計。

## Context

Vault-MCP の実装時、GitHub API へのアクセス認証方式として以下 3 案を検討:

- **案 A**: Classic Personal Access Token(全リポジトリアクセス、粗粒度スコープ)
- **案 B**: Fine-grained Personal Access Token(特定リポジトリ + 特定権限)
- **案 C**: GitHub App(細かい権限制御、複雑な認証フロー)

判断基準:

- **被害範囲の最小化**: PAT が漏洩・悪用された場合の影響範囲
- **運用の容易さ**: 発行、更新、失効の手続き
- **必要権限**: Vault-MCP が実際に必要とするアクセス(Contents R/W のみ、他は不要)
- **将来拡張**: Phase 3.2 で Issue 系の権限追加が必要になる可能性

同時に、当初は Classic PAT で運用していたが、被害範囲の広さが気になり途中で Fine-grained PAT に切り替えた経緯がある。

## Decision

**Fine-grained PAT を採用し、権限を最小化**

具体的なスコープ設計:

### 初期(Phase 1+2、2026-07-13 実装時)

- **Repository access**: `nkhippo/Vault` のみ(Selected repositories)
- **Repository permissions**:
  - Contents: Read and write
  - Metadata: Read-only(自動付与)

### Phase 3.2 実装時(将来)

Issue 起票機能を追加する時、以下の権限追加が必要:

- **Repository access**: 対象アプリのリポジトリを追加(allowlist 方式)
- **Repository permissions**:
  - Contents: Read and write(既存)
  - **Issues: Read and write**(新規追加)
  - Metadata: Read-only(自動付与)

新 PAT を発行するか、既存 PAT を編集するかは Phase 3.2 実装時に判断(Vault-MCP の `open-questions.md` 論点 5 参照)。

## Consequences

**Positive**:

- **被害範囲が単一リポジトリに閉じ込められる**: PAT が漏洩しても、他のリポジトリ(IPASoundDrill、English-* 等)は影響を受けない
- 権限最小化により、意図しない書き込み(例: リポジトリ削除)を物理的に防止
- Fine-grained PAT の有効期限を柔軟に設定できる(1 年、6 ヶ月等)
- GitHub 側で PAT の使用状況を可視化できる

**Negative**:

- Fine-grained PAT はまだベータ機能(2024 時点、2026 では GA だが仕様変更の可能性は残る)
- 発行手続きが Classic PAT より若干煩雑
- 複数リポジトリに拡張する場合、明示的に追加する必要がある(自動的には拡がらない、これは Positive とも捉えられる)

**Mitigation**:

- ベータ機能の仕様変更リスクは、リリース時期(2024 頃 GA)後は低いと判断
- 発行手続きの煩雑さは Framework の `docs/ja/setup/02-deploy-mcp-server.md` で手順化して導入者を支援

## Alternatives Considered

### 案 A: Classic PAT

全リポジトリアクセスの Classic PAT を使う案(初期採用 → 変更)。

**却下理由**:

- 全リポジトリアクセスの権限が広すぎる
- スコープが粗く(`repo` などの粗粒度)、必要以上の権限を持つ
- 事故時の被害範囲が全プライベートリポジトリに広がる
- Naoya の全リポジトリ(nkhippo 配下)が影響を受けるリスク

Classic PAT で 2 週間程度運用したが、リスクが気になり Fine-grained PAT に切り替えた。

### 案 C: GitHub App

GitHub App として登録し、Installation Access Token で認証する案。

**却下理由**:

- 実装複雑度が高い(JWT 生成、Installation ID 管理等)
- 個人利用のスケールでは Fine-grained PAT で十分
- GitHub App は複数ユーザー・組織向けの機能で、単一ユーザーの vault 運用には過剰

将来的にチーム展開する場合は GitHub App への移行を検討する余地はあるが、現状では不要。

## Related

- **前提 ADR**: 
  - ADR-0001(GitHub-as-a-Backend、GitHub API アクセスの前提)
  - ADR-0002(Cloudflare Workers 採用、Secrets 保存先の前提)
- **後続 ADR**: 
  - ADR-0015(Issue 起票機能の実装順序、PAT スコープ拡大の計画)
- **関連 spec**: なし
- **元記録**: 
  - `10_chat_logs/2026/07/2026-07-13_platform-selection-and-phase12-completion.md`(Phase 1+2 完了時に確定)
- **Vault-MCP 側の詳細**: 
  - `../../30_projects/Vault-MCP/design-decisions.md` の意思決定 2 と 11
  - `../../30_projects/Vault-MCP/open-questions.md` の論点 5(Phase 3.2 の PAT 更新タイミング)

## Change Log

- 2026-07-13 前半: Classic PAT で運用開始
- 2026-07-13 後半: Fine-grained PAT に切り替え(現行)
- 2026-07-14(予定): Phase 3.2 実装時に Issues R/W 権限追加

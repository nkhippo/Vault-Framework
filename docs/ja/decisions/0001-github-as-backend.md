---
audience: mixed
created: 2026-07-14T03:30:00+09:00
date: 2026-07-13
id: adr-0001
keywords:
  - github
  - backend
  - vault
  - obsidian
  - storage
  - philosophy
  - single-source-of-truth
related_adrs:
  - "0002"
  - "0003"
  - "0012"
related_chats:
  - 10_chat_logs/2026/07/2026-07-13_vault-system-design-inception-to-completion.md
related_specs: []
status: accepted
summary: Chat 内容の永続化にあたり、GitHub リポジトリを実質バックエンドとして採用した意思決定。Obsidian は編集 UI、真実の source は GitHub。この決定が Framework 全体の起点。
superseded_by: null
supersedes: null
tags:
  - adr
  - important
title: "ADR-0001: GitHub-as-a-Backend の採用"
type: adr
updated: 2026-07-14T03:30:00+09:00
---

## Summary

Chat 内容の永続化にあたり、GitHub リポジトリ(`nkhippo/Vault`)を実質的なバックエンドストレージとして採用した意思決定。Obsidian は編集 UI として使用するが、真実の source は GitHub。この決定が Framework 全体の設計の起点になる。

## Context

Naoya は Obsidian で個人ナレッジベースを運用していたが、Chat の内容を体系的に集約する場所が課題だった。Obsidian Sync + iCloud で複数デバイス同期していたものの、Claude との連携は手動コピペ中心で、以下の問題があった:

- Claude が過去の議論や意思決定を参照できない(セッション間で記憶を持たない)
- 保存の手間で貴重な議論が消える
- 検索・横断参照が非効率

Chat 集約のための保存戦略として、3 案を比較検討:

- **案 1**: GitHub-as-a-Backend(GitHub リポジトリを実質バックエンドに、Obsidian は編集 UI)
- **案 2**: Obsidian Sync 主導(有料の Obsidian Sync を主軸に、GitHub は補助)
- **案 3**: ハイブリッド構成(両者を並列運用)

各案の主要な評価軸: バージョン管理の強度、複数デバイス対応、Claude 連携の容易さ、費用、Vendor Lock-in、将来の公開・パッケージ化可能性。

## Decision

**案 1(GitHub-as-a-Backend)を採用**。以下を確定:

- vault の真実の source: `nkhippo/Vault`(GitHub リポジトリ)
- Obsidian は編集 UI として使用(iCloud Drive 経由でローカルミラー、変更を GitHub に push)
- Claude からの読み書きは MCP サーバ(Vault-MCP)経由で GitHub API を叩く
- 全変更が Git 履歴に残り、SHA で復元可能

## Consequences

**Positive**:

- Git 履歴で全変更が追跡可能、SHA ベースの復元が常に可能
- iCloud Drive + GitHub の 2 段バックアップで冗長性
- Cursor で複雑な一括操作(リネーム、wikilink 書き換え等)を委譲可能
- 将来の Public 化・Fable パッケージ化の余地(Framework 分離の前提)
- Fine-grained PAT でセキュリティ強化可能
- MCP サーバの実装が単一の GitHub API に集約され、シンプル

**Negative**:

- 直接編集(Obsidian)と Claude 経由(MCP)の 2 系統の書き込みパスが並立し、同期タイミングに注意が必要
- iCloud 同期のタイムラグで、直後の Claude 参照が古い状態を見る可能性
- MCP のレスポンスタイムが GitHub API の rate/latency に依存
- Naoya がオフラインの時、Obsidian 編集は可能だが Claude 連携は動かない

**Mitigation**:

- 大掛かりな操作は Cursor 委譲で整合性を確保
- MCP 接続失敗時のリトライ + 中断ルール(ADR-0016)で「憶測での続行」を禁止

## Alternatives Considered

### 案 2: Obsidian Sync 主導

Obsidian Sync(有料の Obsidian 純正同期サービス)を主軸に、GitHub は補助バックアップとして使う案。詳細は [[../rejected-alternatives/vault-composition-plan-2-obsidian-sync.md]]。

**却下理由**:
- Vendor Lock-in(Obsidian の運営継続に依存)
- 月額課金で個人利用としてはコスト高
- GitHub の履歴管理・PR・Issue 機能を活かせない
- Claude 連携が Obsidian Sync API 経由になり、追加の連携層が必要

### 案 3: ハイブリッド構成

Obsidian Sync と GitHub を並列運用し、それぞれの強みを活かす案。詳細は [[../rejected-alternatives/vault-composition-plan-3-hybrid.md]]。

**却下理由**:
- 単一 source of truth を維持できず、乖離が発生した時の統合コストが高い
- 2 つの同期経路を運用する複雑度
- MCP 実装が「どちらを正とみなすか」の判断ロジックを持つ必要があり、複雑度が跳ね上がる

## Related

- **後続 ADR**:
  - ADR-0002(MCP プラットフォームに Cloudflare Workers 採用)
  - ADR-0003(Skill・Project・Vault の 3 層アーキテクチャ)
  - ADR-0012(Fine-grained PAT 採用、GitHub 連携のセキュリティ強化)
- **関連 spec**: なし
- **元記録**: `10_chat_logs/2026/07/2026-07-13_vault-system-design-inception-to-completion.md`
- **却下案の詳細**:
  - `../rejected-alternatives/vault-composition-plan-2-obsidian-sync.md`
  - `../rejected-alternatives/vault-composition-plan-3-hybrid.md`

## Change Log

- 2026-07-13: 初版(vault 構成 3 案比較で案 1 採用)

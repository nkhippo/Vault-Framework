---
audience: mixed
created: 2026-07-14 05:15:00+09:00
date: 2026-07-13
keywords:
- obsidian-sync
- vendor-lock-in
- backend
- monthly-subscription
- sync
related_adrs:
- '0001'
status: rejected
summary: Vault の主たる同期・保存手段として Obsidian Syncを採用し、GitHub は補助バックアップに留める案。Vendor Lock-inと
  Claude 連携の複雑化により却下。
superseded_by: '0001'
tags:
- rejected
- vault-composition
title: '却下案: Obsidian Sync 主導'
type: rejected_alternative
updated: 2026-07-14 05:15:00+09:00
id: pj-2026-07-13-e650
aliases:
- pj-2026-07-13-e650
---

## Summary

Vault の主たる同期・保存手段として Obsidian Sync(Obsidian 純正の有料同期サービス)を採用し、GitHub は補助バックアップに留める案。Vendor Lock-in と Claude 連携の複雑化により却下。ADR-0001 で GitHub-as-a-Backend を採用。

## What Was Proposed

Vault の運用を以下の構成で行う案:

- **主要バックエンド**: Obsidian Sync(月額課金)
- **補助バックアップ**: GitHub リポジトリ(定期同期スクリプト)
- **編集 UI**: Obsidian(iCloud Drive 経由の同期は不要、Obsidian Sync が担当)
- **Claude 連携**: Obsidian の Community Plugin または Obsidian Sync API 経由

Naoya は Obsidian の既存ユーザーであり、Obsidian Sync を追加契約する敷居は低い状態だった。

## Why It Was Considered

- **Obsidian 純正のサポート**: 公式サービスなので、Obsidian 側の機能アップデートに追随しやすい
- **編集体験の一貫性**: Obsidian のリンク、グラフビュー、テーマ等の機能が全デバイスで同一
- **バイナリファイル対応**: 画像、PDF、動画等も含めた同期が容易(GitHub は LFS が必要)
- **同期の透過性**: Obsidian Sync はバックグラウンドで自動同期、ユーザーが git push を意識しない

## Why It Was Rejected

- **Vendor Lock-in**: Obsidian の運営継続に完全依存。Obsidian の会社が閉業したり、Sync サービスを廃止したりした場合、資産の移行が困難
- **月額課金**: 個人利用としてはコスト高(2026 年時点で月 $10 前後)。年間 $120 は無視できない
- **GitHub の履歴管理・PR・Issue 機能を活かせない**: 変更履歴が Obsidian Sync 内でしか見えず、Cursor 委譲や Issue ベースの workflow が組めない
- **Claude 連携の複雑化**: MCP 経由で Obsidian Sync にアクセスするには、専用の API 連携が必要(現状 MCP プロトコルとの相性が良い実装が存在しない)
- **Public 化・Fable パッケージング困難**: Framework を公開する構想と根本的に相性が悪い(Obsidian Sync 前提の Framework は導入者にコストを強いる)
- **Cursor 委譲との相性**: Cursor は git ベースの操作が中心。Obsidian Sync では git 操作を挟めない

## What Was Chosen Instead

- **採用案**: ADR-0001「GitHub-as-a-Backend」
- **参照**: [[pj-2026-07-13-2564]]

GitHub リポジトリを実質バックエンドとし、Obsidian は編集 UI として使用する。iCloud Drive 経由でローカルミラーし、変更を GitHub に push する運用。

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_vault-system-design-inception-to-completion.md`
- 対応 ADR: [[pj-2026-07-13-2564]]
- 関連却下案: [[pj-2026-07-13-8398]](ハイブリッド構成)

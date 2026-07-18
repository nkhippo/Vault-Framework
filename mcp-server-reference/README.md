---
audience: adopter
keywords:
- mcp
- vault-mcp
- reference
- cloudflare-workers
- framework
status: draft
summary: Vault-MCP サーバ(Cloudflare Workers 実装)の技術リファレンスセクションの入り口。位置づけ、対象読者、章立て、ツールカテゴリ概観を含む。入門は
  setup/02、拡張・deep dive は本セクションという役割分担。
tags:
- framework
- mcp-server-reference
- reference
- mcp
title: Vault-MCP 技術リファレンス
type: setup
created: 2026-07-18 14:47:07+09:00
updated: 2026-07-18 14:47:07+09:00
---

Vault-MCP は Vault-Framework の中核となる **Model Context Protocol サーバ**の参照実装。Claude(あるいは他の MCP 対応クライアント)から個人 Vault(GitHub 上の Markdown リポジトリ)への読み書きを可能にする。

このディレクトリは、adopter が Vault-MCP を自分の環境にデプロイする詳細手順、独自に fork して拡張する際のガイド、および全ツールのリファレンスを収録する。

## 位置づけ

Vault-MCP はスタンドアロンのリポジトリとして公開されており(`<owner>/Vault-MCP`)、adopter は下記の 2 通りで使う:

- **そのまま使う**: 参照実装をそのまま fork してデプロイ。Framework で規定された 17 ツールがそのまま使える(Vault-MCP v1.6.0)(推奨)
- **fork して拡張**: 自分の運用に必要な独自ツールを追加。例えば「特定ドメイン用の tag 検証ツール」や「GitHub 以外のバックエンド(例: Notion、Obsidian Live Sync)への切替」など

このディレクトリは両方をサポートする。

## この Framework との関係

Vault-Framework は「Skill(Claude 側)+ vault-templates(GitHub 側)+ Vault-MCP(Cloudflare 側)」の 3 層で成立している。Vault-MCP がなければ Skill は Vault を読み書きできない。

| 層 | 役割 | 配布形態 |
|---|---|---|
| Skill(`skills/vault-manager` 等) | Claude の振る舞い規約 | Framework 配下、zip アップロード |
| vault-templates | Vault リポジトリの骨格 | Framework 配下、コピー |
| **Vault-MCP** | **Claude ↔ Vault の橋渡し** | **別リポジトリ、fork してデプロイ** |

Vault-MCP は Cloudflare Workers 上で動作する TypeScript 実装で、GitHub Contents API を通じて Vault リポジトリを操作する。

## 対象読者

このディレクトリの内容は以下のいずれかに該当する adopter 向け:

- **入門者**: `docs/ja/setup/02-deploy-mcp-server.md` で一度 deploy を完了した後、動作原理を理解したい
- **拡張者**: 独自ツールを追加する、または内部構造を fork ベースで変更したい
- **保守者**: Framework 更新に追随して MCP サーバを update する、または独自の変更を Framework 更新と両立させたい
- **debug 者**: MCP コネクタが期待通り動かない、tool call が失敗する、等の技術的問題を調査したい

setup/02 だけで運用に入れる場合、このディレクトリを読む必要はない。

## 内容

| ファイル | 内容 |
|---|---|
| `README.md` | このファイル |
| `architecture.md` | Cloudflare Workers + GitHub Contents API を組み合わせたアーキテクチャ、リクエストフロー、認証モデル |
| `env-vars.md` | 環境変数と Secrets の詳細リファレンス |
| `tools/reference.md` | 全ツールの API リファレンス(パラメータ・戻り値・使用例・注意事項) |
| `extending.md` | fork して独自ツールを追加する手順、既存ツールを改変する際の注意 |
| `troubleshooting.md` | 拡張トラブルシューティング(setup/02 の Troubleshooting セクションの深掘り) |

## ツールカテゴリ概観

Vault-MCP が現在提供する 17 ツール(+1 reserved)は大きく 4 系統に分かれる。詳細は `tools/reference.md`。

- **Read 系**(7): `get_file_content`, `get_frontmatter`, `get_frontmatter_batch`, `get_section`, `list_directory`, `get_project_bundle`, `search_by_keyword`
- **Write 系**(6): `create_note`, `update_note`, `delete_note`, `move_note`, `skill_note`, `create_directory`
- **Issue 系**(3): `list_issues`, `create_issue`, `add_issue_comment`
- **Repo 系**(2 前後): `list_recent_commits`, `get_file_permissions`

## Framework 更新と Vault-MCP の関係

Framework の update(`docs/ja/setup/08-update.md`)で **Vault-MCP 本体は更新対象に含まれない**。Vault-MCP は Framework とは別のリリースサイクルで動く独立プロダクト。

ただし、Framework 側の Skill や templates が新しいツールを前提とする改修を含む場合、Framework の CHANGELOG に「Vault-MCP vX.Y.Z 以降が必要」と明示される。その場合は adopter は Vault-MCP を先に update してから Framework update に進む。

Vault-MCP の CHANGELOG は Vault-MCP リポジトリ側で管理される。

## 関連

- 導入手順(初回 deploy): `docs/ja/setup/02-deploy-mcp-server.md`
- MCP コネクタ登録: `docs/ja/setup/03-configure-mcp-connector.md`
- Vault-Framework update: `docs/ja/setup/08-update.md`
- canonical/personal 境界: `docs/ja/setup/canonical-vs-personal.md`

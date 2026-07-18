---
audience: adopter
created: 2026-07-14 08:35:00+09:00
keywords:
  - setup
  - overview
  - roadmap
  - 10-steps
  - framework-adoption
status: published
summary: Vault-Framework を導入して、自分の個人 Vault 運用を立ち上げるための導入手順集の概要とロードマップ。Phase 1〜7 の段階構成で、システム作業・初期認識合わせ・カスタマイズ・Framework 更新取り込みまでをカバーする。
tags:
  - setup
  - overview
title: セットアップガイド - 全体の流れ
type: setup
updated: 2026-07-18T12:54:34+09:00
---

## Summary

Vault-Framework を導入して、自分の個人 Vault 運用を立ち上げるための導入手順集の概要とロードマップ。Phase 1〜7 の段階構成で、各ステップを順に実施することで、あなた個人の Vault 運用体制を構築し、以降の Framework 更新も安全に取り込める。

## 目的

このドキュメント群は、以下を実現するためのステップバイステップガイドです:

- 自分の GitHub アカウントに Vault リポジトリを立ち上げ
- Cloudflare Workers 上に MCP サーバをデプロイ
- Claude Pro Connectors で MCP コネクタを設定
- Skill `vault-manager` を Claude Skills にアップロード
- Claude Projects で Vault Project を設定
- 初回保存動作を確認して稼働開始
- **Chat で Claude と初期認識合わせを行い、あなた固有の profile / vocabulary / 初期プロジェクトを反映**
- **Framework の新版が出たときに update を安全に取り込む**

すべてのステップ完了時、Framework の思想と同等の運用体制が手に入ります。

## 全体所要時間

- **初回導入(Phase 1〜4)**: 2-4 時間(慣れていれば 1-2 時間)
- **初期認識合わせ(Phase 5)**: 30-60 分
- **カスタマイズ(Phase 6)**: 数時間〜数日(必要な範囲で)
- **update(Phase 7)**: 通常 10-30 分、破壊的変更ありで 30-60 分

## ステップ構成

### Phase 1: 前提確認と準備

- 00-prerequisites.md - 前提となる環境(GitHub、Cloudflare、Claude Pro 契約)の確認

### Phase 2: リポジトリの初期化

- 01-fork-vault-templates.md - Framework の vault-templates/ を元に vault リポジトリを初期化
- 02-deploy-mcp-server.md - Vault-MCP を Cloudflare Workers にデプロイ

### Phase 3: Claude 側の設定

- 03-configure-mcp-connector.md - Claude Pro Connectors で MCP コネクタを追加
- 04-upload-skill.md - Skill `vault-manager` を Claude Skills にアップロード
- 05-configure-project.md - Claude Projects で Vault Project を作成・設定

### Phase 4: 動作確認

- 06-first-save-test.md - 初回保存動作を確認して稼働開始

### Phase 5: 初期認識合わせ(推奨)

- `07-initial-alignment-session.md` - Chat で Claude と対話しながら、`profile.md` / `vocabulary.md` / 初期プロジェクト骨組みをあなた固有の内容に更新。MCP 疎通テストも兼ねる

### Phase 6: カスタマイズと運用

- customization.md - 統制語彙拡張・テンプレ追加等のカスタマイズ手順
- troubleshooting.md - 問題解決とトラブルシューティング

### Phase 7: Framework 更新の取り込み

- `08-update.md` - 新バージョンが公開されたときの update 手順
- `canonical-vs-personal.md` - canonical / personal / hybrid 境界表(update 時に何を差し替え・何を残すか)
- 変更履歴は Framework リポジトリ ルート `CHANGELOG.md`

## 推奨する導入順序

以下の順序で進めることを推奨します:

1. **Phase 1**: 前提確認(30 分)
2. **Phase 2**: リポジトリ初期化(1-2 時間)
3. **Phase 3**: Claude 側設定(30 分〜1 時間)
4. **Phase 4**: 動作確認(15 分)
5. **Phase 5**: 初期認識合わせ(30-60 分)
6. **Phase 6**: 慣れてきたら段階的にカスタマイズ
7. **Phase 7**: Framework の新版が出たら update を取り込む

各 Phase の完了後、次に進む前に動作確認を推奨します。

## Prerequisites Summary

前提として以下が必要です(詳細は 00-prerequisites.md):

- **GitHub アカウント**: リポジトリ作成が可能
- **Cloudflare アカウント**: Workers デプロイに必要(無料プランで OK)
- **Claude Pro / Team / Enterprise 契約**: Connectors と Skills 機能が必要
- **Node.js 18+ / npm**: MCP サーバのビルド・デプロイに必要
- **Git**: ローカル操作用
- **Obsidian(推奨)**: vault の直接編集用(なくても動く)
- **iCloud Drive または類似の同期サービス(推奨)**: vault のローカルミラー用

## What This Framework Provides

Framework が提供するもの:

- **vault-templates/**: 00_meta/ 一式、templates/ 一式、その他のディレクトリ構造
- **skills/vault-manager/**: SKILL.md canonical 版と管理 README
- **skills/vault-maintainer/**: 週次・月次メンテナンス系 Skill
- **mcp-server-reference/**: Vault-MCP のリポジトリと稼働手順
- **examples/**: 各 type の記入例
- **docs/ja/prompts/initial-alignment.md**: 初期認識合わせセッションを Claude が実行するためのプロンプト
- **docs/ja/guardrails/claude-behavior.md**: Claude カスタマイズ・ガードレール
- **CHANGELOG.md**: 変更履歴(SemVer 準拠)

これらをベースに、Phase 5 の初期認識合わせで自分の運用に合わせて反映します。

## What You Need to Customize

導入後に自分でカスタマイズする箇所:

- **`00_meta/profile.md`**: Life Strategy と価値観(Phase 5 の対話で埋める)
- **`00_meta/vocabulary.md` の project セクション**: 自分のプロジェクト一覧(Phase 5)
- **ドメイン固有の主題 tag**: `backlog_tags.md` へ追記(Phase 5 または後追い)
- **`30_projects/<Repo>/`**: プロジェクト骨組み(Phase 5 または通常運用の中で)

他の 00_meta ファイルは初期状態のまま運用開始でき、必要に応じて後から拡張します。カスタマイズ手順の詳細は customization.md と `canonical-vs-personal.md` を参照。

## Common Pitfalls(先に把握しておくべきこと)

以下は初回導入時によくつまづくポイント:

- **Fine-grained PAT の権限設定**: Contents R/W 限定を必ず守る(セキュリティ)
- **Cloudflare Secrets の設定漏れ**: wrangler.toml の vars ではなく必ず Secrets 経由で保存
- **Claude Pro プランの確認**: Free プランでは Connectors と Skills が使えない
- **Skill.md の Front Matter**: `name` と `description` のみで純粋な Claude Skills 形式を守る
- **HashiCorp Vault との命名衝突**: リポジトリ名を `Vault` にする場合の注意(代替命名候補は 01-fork-vault-templates.md 参照)
- **Phase 5 のスキップ**: Phase 5 を飛ばすと profile / vocabulary が骨格のままになり、Claude の判断精度が下がる。動作確認直後にセッション実施を推奨

詳細な対処法は各ステップの手順および troubleshooting.md 参照。

## Next Step

準備ができたら 00-prerequisites.md に進んでください。

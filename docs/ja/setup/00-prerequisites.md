---
audience: adopter
created: 2026-07-14 08:40:00+09:00
keywords:
- setup
- prerequisites
- github
- cloudflare
- claude-pro
- nodejs
- obsidian
status: published
summary: Vault-Framework を導入する前に確認しておくべき前提となる環境と、必要なアカウント・ツール類。契約プラン、権限、ローカル環境について詳細を規定。
tags:
- setup
- prerequisites
title: 00 - 前提確認
type: setup
updated: 2026-07-14 08:40:00+09:00
---

## Summary

Vault-Framework を導入する前に確認しておくべき前提となる環境と、必要なアカウント・ツール類。契約プラン、権限、ローカル環境について詳細を規定。

## 前提となる契約・アカウント

### 1. GitHub アカウント

- **必須**: リポジトリ作成が可能なアカウント
- **推奨**: Private リポジトリを作成可能(GitHub Free でも可能)
- **アクセス権限**: 
  - 自分のアカウントで公開・非公開リポジトリ作成
  - Fine-grained Personal Access Token(PAT)の発行権限

**確認方法**:
- https://github.com/settings/tokens?type=beta にアクセス
- 「Generate new token」ボタンが表示されることを確認

### 2. Cloudflare アカウント

- **必須**: Workers を利用するためのアカウント
- **推奨プラン**: **Free プラン**(個人利用なら十分)
- **必要な機能**:
  - Cloudflare Workers(100k req/day、Free 枠)
  - Wrangler CLI(ローカルからのデプロイ)
  - Secrets(暗号化された環境変数)

**確認方法**:
- https://dash.cloudflare.com にログイン
- Workers セクションが利用可能なことを確認

**注意**: Workers Paid プラン(月 $5)は個人利用では不要。CPU 時間や複雑な処理が必要になった時に検討。

### 3. Anthropic Claude 契約(Pro / Team / Enterprise)

- **必須**: Connectors と Skills 機能が使えるプラン
- **推奨**: **Claude Pro プラン**($20/月、個人利用として最適)
- **必要な機能**:
  - Custom Connectors(MCP コネクタの追加)
  - Skills(SKILL.md のアップロード)
  - Claude Projects(Vault Project の作成)

**確認方法**:
- https://claude.ai/settings/plans で現在のプランを確認
- Free プランの場合、上記機能が使えないため Pro 以上へのアップグレードが必要

**代替**: Team / Enterprise でも同じ機能が使えますが、個人利用では Pro で十分です。

### 4. Anthropic Console アカウント(オプション、開発者向け)

- **オプション**: MCP サーバのデプロイテストで API を叩く場合
- **必要度**: 通常運用では不要

## 必要なローカルツール

### 1. Node.js 18+ / npm

- **必須**: MCP サーバのビルド・デプロイに必要
- **推奨バージョン**: Node.js 20 LTS(2026 時点)
- **確認方法**:

```bash
node --version   # v20.x.x またはそれ以上
npm --version    # 10.x.x またはそれ以上
```

- **インストール方法**:
  - macOS: `brew install node`
  - Ubuntu/Debian: `sudo apt install nodejs npm`
  - Windows: https://nodejs.org からインストーラーをダウンロード

### 2. Git

- **必須**: ローカルでのリポジトリ操作、GitHub との連携
- **確認方法**:

```bash
git --version   # 2.30 以上を推奨
```

- **インストール方法**:
  - macOS: `brew install git`(または Xcode Command Line Tools)
  - Ubuntu/Debian: `sudo apt install git`
  - Windows: https://git-scm.com からインストーラー

### 3. Wrangler(Cloudflare CLI)

- **必須**: Cloudflare Workers へのデプロイ
- **インストール**:

```bash
npm install -g wrangler
wrangler --version
```

### 4. Editor(推奨)

- **推奨**: VS Code、Cursor、または類似のエディタ
- **理由**: TypeScript コードの編集、Markdown プレビュー、Cursor 委譲による自動編集
- **Cursor 使用の場合**: Claude 統合機能で Vault 運用時の指示書実行がスムーズ

## 推奨するツール

### 1. Obsidian(強く推奨)

- **推奨**: vault の直接編集用
- **代替**: 通常のエディタ(VS Code 等)でも動く
- **利点**:
  - Wikilink の自動補完
  - グラフビュー(ファイル間の関連を可視化)
  - Markdown プレビュー
  - iCloud Drive との相性が良い

**インストール**: https://obsidian.md からダウンロード

**Vault 設定**:
- Vault の場所を後述の iCloud パスに設定
- Community Plugin は不要(vanilla Obsidian で動く)

### 2. iCloud Drive(推奨、macOS の場合)

- **推奨**: vault のローカルミラーとして
- **代替**: 
  - Windows: OneDrive
  - Linux: rsync + cron、または Syncthing

**設定**:
- macOS の場合、GitHub リポジトリを clone する場所を `~/Library/Mobile Documents/com~apple~CloudDocs/Vault/` にする
- または `~/iCloud Drive/Vault/` のシンボリックリンク

### 3. GitHub CLI(オプション)

- **オプション**: リポジトリの Fork や作成をコマンドラインで
- **インストール**: `brew install gh` または https://cli.github.com
- **代替**: GitHub のブラウザ UI でも同じ操作可能

## Skill セット(必要な技術理解)

以下の知識があると導入がスムーズです(なくても手順に従えば動きます):

- **Git の基本**: clone、commit、push
- **npm / Node.js の基本**: package.json、npm install、npm run
- **YAML の読み書き**: Front Matter、wrangler.toml
- **Markdown の基本**: Wikilink、Front Matter
- **環境変数の扱い**: Cloudflare Secrets(GUI で設定可能)

これらに慣れていない場合、03-configure-mcp-connector.md 以降のステップで手取り足取り説明します。

## Prerequisites チェックリスト

導入前に以下をチェック:

- [ ] GitHub アカウントで Fine-grained PAT の発行権限を確認
- [ ] Cloudflare アカウントで Workers が利用可能
- [ ] Claude Pro / Team / Enterprise プランに契約済み
- [ ] Node.js 18+ がローカルにインストール済み
- [ ] Git がローカルにインストール済み
- [ ] Wrangler CLI がインストール済み(`npm install -g wrangler`)
- [ ] Editor(VS Code、Cursor 等)がインストール済み
- [ ] Obsidian をインストール済み(推奨)
- [ ] iCloud Drive などの同期サービスが有効(推奨)

すべてチェックできたら次のステップに進んでください。

## Cost Overview

Vault-Framework 運用にかかる費用の目安:

| サービス | 費用 | 備考 |
|---|---|---|
| GitHub | $0 | Free プランで OK |
| Cloudflare Workers | $0 | Free 枠 100k req/day で個人利用は十分 |
| Claude Pro | $20/月 | Skills と Connectors が必要 |
| Obsidian | $0 | 個人利用は無料 |
| iCloud Drive | $0-$1/月 | 5GB 無料、追加は $0.99/月 |
| **合計** | **$20/月程度** | Claude Pro 契約が主なコスト |

## Next Step

前提の確認ができたら 01-fork-vault-templates.md に進んでください。

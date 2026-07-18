---
audience: adopter
created: 2026-07-14 08:55:00+09:00
keywords:
- setup
- deploy
- cloudflare-workers
- wrangler
- fine-grained-pat
- secrets
status: published
summary: Vault-MCP サーバを Cloudflare Workers にデプロイする手順。Fine-grained PAT の発行、Cloudflare
  Secrets の設定、wrangler.toml のカスタマイズ、初回デプロイ、動作確認までを含む。
tags:
- setup
- mcp-deploy
title: 02 - MCP サーバのデプロイ
type: setup
updated: 2026-07-14 08:55:00+09:00
---

## Summary

Vault-MCP サーバを Cloudflare Workers にデプロイする手順。Fine-grained PAT の発行、Cloudflare Secrets の設定、wrangler.toml のカスタマイズ、初回デプロイ、動作確認までを含む。

## Step 1: Vault-MCP リポジトリの取得

### 方法 A: Fork(推奨)

1. https://github.com/nkhippo/Vault-MCP にアクセス
2. 「Fork」ボタンをクリック
3. 自分のアカウントに Fork(例: `<YourGitHubUsername>/Vault-MCP`)
4. ローカルにクローン:

```bash
git clone https://github.com/<YourGitHubUsername>/Vault-MCP.git
cd Vault-MCP
```

### 方法 B: Template として使用

- Vault-MCP を template repository として指定してある場合、「Use this template」から作成

### 方法 C: 直接 clone

- Fork せず、自分のアカウントに新規リポジトリを作り、コードをコピーして push

## Step 2: 依存パッケージのインストール

```bash
npm install
```

期待: `node_modules/` が作成され、エラーなく完了。

## Step 3: Fine-grained PAT の発行

### 発行手順

1. https://github.com/settings/tokens?type=beta にアクセス
2. 「Generate new token」→「Fine-grained personal access token」
3. **Token name**: `vault-mcp-<vault-repo-name>`(例: `vault-mcp-Vault`)
4. **Expiration**: 90 days または 1 year(用途に応じて)
5. **Repository access**: **Only select repositories** → あなたの vault リポジトリを選択
6. **Repository permissions**:
   - **Contents**: Read and write(必須)
   - **Metadata**: Read-only(自動選択)
7. 「Generate token」をクリック
8. **トークンをコピー**(この画面を閉じると再表示不可)

### セキュリティ注意

- トークンは他のリポジトリや Issues 権限を含まない Fine-grained 設定にする
- Phase 3.2 で Issue 起票機能を使う場合は、後日「Issues: Read and write」を追加

## Step 4: Cloudflare Secrets の設定

### 4.1 wrangler ログイン

```bash
wrangler login
```

ブラウザが開き、Cloudflare アカウントでログイン。

### 4.2 GitHub PAT の登録

```bash
wrangler secret put GITHUB_TOKEN
# プロンプト表示 → Step 3 で発行したトークンを貼り付け → Enter
```

### 4.3 MCP アクセストークンの登録(オプション、推奨)

MCP コネクタからのアクセスを認証するためのトークンを生成:

```bash
# ランダムトークン生成(例)
openssl rand -hex 32
```

このトークンを Secrets に登録:

```bash
wrangler secret put MCP_ACCESS_TOKEN
# 生成したトークンを貼り付け → Enter
```

## Step 5: wrangler.toml のカスタマイズ

`wrangler.toml` を編集:

```toml
name = "vault-mcp"  # Worker 名(自分の運用に合わせて変更可)
main = "src/index.ts"
compatibility_date = "2026-01-01"
compatibility_flags = ["nodejs_compat"]

[vars]
GITHUB_OWNER = "<YourGitHubUsername>"  # あなたの GitHub ユーザー名
GITHUB_REPO = "<VaultRepoName>"        # Step 1(fork-vault-templates)で選んだリポジトリ名
```

**注意**: `[vars]` セクションには secrets を絶対に置かない(平文でリポジトリに残る)。トークン類は Step 4 の Secrets 経由で。

## Step 6: 初回デプロイ

```bash
npx wrangler deploy
```

期待する出力:

```
Total Upload: XX.X KiB / gzip: XX.X KiB
Uploaded vault-mcp (X.XX sec)
Published vault-mcp (X.XX sec)
  https://vault-mcp.<your-subdomain>.workers.dev
```

デプロイ URL(`https://vault-mcp.<your-subdomain>.workers.dev`)を控える。

## Step 7: 動作確認

### 7.1 health エンドポイント(実装があれば)

```bash
curl https://vault-mcp.<your-subdomain>.workers.dev/health
```

### 7.2 MCP プロトコル初期化

MCP プロトコル準拠のクライアント(または Claude Pro Connectors)から接続確認。

### 7.3 tools/list の確認

```bash
curl -X POST https://vault-mcp.<your-subdomain>.workers.dev/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <MCP_ACCESS_TOKEN>" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

期待: Phase 1+2 の 5 ツール + Phase 3.1 の 3 ツール = 8 ツールが返る。

## Cost

Cloudflare Workers Free プランで運用可能。

- Free 枠: 100k req/day
- 個人利用: 通常 1000 req/day 以下、Free 枠内で完結

## Troubleshooting

### `wrangler deploy` でエラー

- ログイン確認: `wrangler whoami`
- アカウントの Workers 有効化: Cloudflare Dashboard で確認
- 詳細エラーメッセージは `wrangler deploy --verbose`

### GitHub API エラー(401 Unauthorized)

- PAT の権限確認(Contents R/W が付与されているか)
- PAT の有効期限確認
- リポジトリ選択の確認(Fine-grained PAT で対象リポジトリが含まれているか)

### CORS エラー

- Claude Pro Connectors からのアクセスは通常 CORS 対応済み
- 独自クライアントからアクセスする場合、Worker 側で CORS ヘッダーの設定が必要

## Next Step

MCP サーバのデプロイが完了したら 03-configure-mcp-connector.md で Claude Pro Connectors に登録します。

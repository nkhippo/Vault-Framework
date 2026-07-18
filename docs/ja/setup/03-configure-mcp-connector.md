---
audience: adopter
created: 2026-07-14 09:00:00+09:00
keywords:
- setup
- mcp-connector
- claude-pro-connectors
- authentication
- bearer-token
status: published
summary: Cloudflare Workers にデプロイした Vault-MCP を、Claude Pro Connectors に登録する手順。コネクタ表示名、URL、認証トークンの設定、動作確認までを含む。
tags:
- setup
- mcp-connector
title: 03 - MCP コネクタの設定
type: setup
updated: 2026-07-14 09:00:00+09:00
---

## Summary

Cloudflare Workers にデプロイした Vault-MCP を、Claude Pro Connectors に登録する手順。コネクタ表示名、URL、認証トークンの設定、動作確認までを含む。

## Step 1: Claude Pro Connectors ページを開く

1. https://claude.ai にログイン
2. Settings(左サイドバー下部)→ Connectors
3. 「Add custom connector」または「Add new connector」をクリック

## Step 2: コネクタ情報を入力

### 基本情報

| 項目 | 推奨値 | 説明 |
|---|---|---|
| **Name** | `Vault MCP` | UI 上の表示名(スペース区切り + 大文字始まり) |
| **Description** | 「個人 Vault の読み書き」等 | 任意 |
| **URL** | `https://vault-mcp.<your-subdomain>.workers.dev` | Step 6(02-deploy-mcp-server)のデプロイ URL |

### 認証(Bearer トークン)

- **Authentication Type**: Bearer Token(または OAuth 2.0 未対応時は API Key)
- **Token**: Step 4.3(02-deploy-mcp-server)で登録した `MCP_ACCESS_TOKEN` を入力

### 高度な設定(必要に応じて)

- **Timeout**: デフォルト(通常 30 秒)で OK
- **Retries**: 1(ADR-0016 のリトライルールと整合)

## Step 3: コネクタの追加

「Add」または「Save」をクリック。以下のいずれかが起きます:

### 成功パターン

- コネクタが Connectors 一覧に追加される
- 状態が「Connected」または「Active」になる
- ツール一覧が Claude UI に表示される(通常 8 ツール)

### エラーパターン

- 接続失敗のメッセージ
- 詳細は Troubleshooting セクション参照

## Step 4: 動作確認

### 4.1 新規 Chat の開始

- 通常の Chat(Vault Project ではない)を開始
- 発話: 「Vault MCP のツール一覧を教えて」

### 4.2 期待する応答

Claude が以下のツールを列挙:

- `list_directory`
- `get_file_content`
- `create_note`
- `update_note`
- `delete_note`
- `get_frontmatter`
- `search_by_keyword`
- `get_section`

Phase 3.2 完了後は Issue 系ツールも追加(将来)。

### 4.3 実際の動作テスト

```
発話: 「Vault MCP で 00_meta/ の中身を list_directory してみて」

期待: Claude が list_directory を呼び出し、00_meta/ の中身が返る
```

## Step 5: コネクタ設定の確認

Connectors ページで以下を確認:

- **Status**: Connected(緑色)
- **Last used**: 直近の時刻
- **Tool count**: 8

## Enabling/Disabling per Chat

Chat ごとにコネクタの有効/無効を切り替えできます:

- Chat 画面の「Tools」または「Connectors」アイコンをクリック
- Vault MCP のトグルを ON/OFF

**推奨**: Vault 関連の Chat では ON、それ以外では OFF(トークン節約)

## Multiple MCP Connectors

複数の MCP コネクタを設定する場合の注意:

- 各コネクタの名前は一意に(Vault MCP、Other MCP 等)
- ツール名の衝突を避ける
- Chat ごとに使うコネクタを選択

## Troubleshooting

### 接続失敗

**原因 1**: URL の誤り

- `wrangler deploy` の出力を再確認
- URL 末尾の `/` の有無に注意

**原因 2**: 認証トークンの誤り

- Cloudflare Secrets の `MCP_ACCESS_TOKEN` と、Connectors で入力したトークンが一致するか確認
- 再生成が必要な場合、Step 4.3(02-deploy-mcp-server)を再実行

**原因 3**: Worker のデプロイ失敗

- `wrangler tail` でリアルタイムログを確認
- Cloudflare Dashboard でエラーを確認

### ツールが表示されない

- Chat を再起動(新規 Chat を開始)
- Connectors の再接続(削除 → 再追加)
- MCP プロトコルバージョンの整合性を確認

### 認証エラーの繰り返し

- PAT の有効期限を確認(GitHub の Settings)
- Fine-grained PAT の権限を確認(Contents R/W)
- Cloudflare Secrets の再登録: `wrangler secret put GITHUB_TOKEN`

## Security Notes

- **MCP アクセストークン**: 定期的にローテーション推奨(3-6 ヶ月毎)
- **GitHub PAT**: 定期的に再発行(有効期限が切れる前)
- **Cloudflare アカウント**: 2FA を有効化推奨

## Next Step

MCP コネクタの設定が完了したら 04-upload-skill.md で Skill `vault-manager` を Claude Skills にアップロードします。

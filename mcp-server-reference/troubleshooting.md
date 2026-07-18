---
title: Vault-MCP トラブルシューティング
type: setup
status: published
audience: adopter
tags:
- framework
- mcp-server-reference
- troubleshooting
keywords:
- mcp
- vault-mcp
- troubleshooting
summary: deploy / 401 / 409 / 422 / CORS / cold start / PAT rotation / リポジトリ移動などの深掘り手順。
created: '2026-07-18T15:40:00+09:00'
updated: '2026-07-18T15:40:00+09:00'
---

setup/02 の Troubleshooting を深掘りし、デプロイ後〜運用中に多い障害を手順化する。まず `wrangler tail` で Worker 側の事実を取り、次に GitHub API のステータスを疑う。

## 調査の基本手順

1. `wrangler whoami` で正しいアカウントか確認
2. `wrangler secret list` で Secret 名が揃っているか確認(値は見えない)
3. `wrangler tail` を張った状態で再現
4. 同条件で `curl` による `tools/list` / `tools/call`
5. GitHub 側: PAT 期限、権限、リポジトリ選択、API ステータス

## wrangler deploy でエラー

**症状**: deploy が失敗、または古いスクリプトのまま

**確認**:

```bash
wrangler whoami
wrangler deploy --verbose
```

**よくある原因**:

- 未ログイン / 別アカウント
- Workers 未有効化(Dashboard で有効化)
- `wrangler.toml` の KV id が自分のアカウントに無い
- `compatibility_date` / `nodejs_compat` 不足でビルド失敗

**対処**: アカウントを揃え、KV を作り直して id を書き換える。必要なら `npx wrangler@latest`。

## GitHub API 401 Unauthorized

**症状**: すべての読取/書込が UNAUTHORIZED

**確認**:

- Fine-grained PAT の期限
- Contents R/W(と Issue 利用時は Issues R/W)
- 対象リポジトリに Vault が含まれているか
- `GITHUB_TOKEN` secret が最新か(`wrangler secret put` で再設定)

クラシック PAT を使う場合も scopes を再確認。

## GitHub API 409 Conflict

**症状**: `update_note` / `delete_note` が CONFLICT

**意味**: 送った `sha` が最新でない(並行更新または連続更新の取りこぼし)

**対処**:

1. `get_file_content` で最新 `sha` と内容を取り直す
2. 変更を載せ直す
3. 再度更新

Skill でも「同一ファイルを連続更新する前に再読取」が推奨。

## GitHub API 422 Unprocessable Entity

**症状**: create/update が 422

**典型原因**:

- パス不正(先頭 `/`、空、ディレクトリをファイルとして PUT)
- 既存パスへの `create_note`
- 不正な base64 / 空 content(実装依存)
- Issue の存在しない label / assignee

**対処**: エラーメッセージの `message` / `documentation_url` を読み、パスと FM を修正。既存なら `update_note`。

## CORS エラー

MCP コネクタ(サーバ間)経由では通常出ない。

ブラウザや独自フロントから Worker を直接叩くと CORS が必要になる。現行 Vault-MCP はブラウザ公開 API を主目的にしていない。

**対処**: サーバ側クライアント(Claude Connectors、自前 backend)から呼ぶ。どうしてもブラウザからなら Worker に CORS ヘッダを足す改変が必要(セキュリティ影響を評価)。

## wrangler tail の使い方

```bash
wrangler tail
# 別端末でツール呼び出しを再現
```

見るポイント:

- 認証失敗の有無
- ツール名とエラーコード
- サブリクエスト予算超過
- 予期しない 5xx

Dashboard の Workers Logs(observability)が有効なら同様の情報を UI でも確認できる。

## cold start による初回タイムアウト

**症状**: 朝一や長時間空き後の最初の 1 回だけ失敗/遅い

**背景**: Workers の isolate 起動 + GitHub 往復

**mitigation**:

- クライアント側リトライ(1 回)
- 定期的な health / `tools/list` で warm を維持(過剰にすると Workers 枠を消費)
- cron はインデックス用途であり、汎用 keep-warm 目的ではない点に注意

## PAT の rotation

1. GitHub で新しい Fine-grained PAT を発行(権限は同一)
2. `wrangler secret put GITHUB_TOKEN` で差し替え
3. `tools/list` と軽微な `get_file_content` で確認
4. 旧 PAT を revoke
5. カレンダーに次回期限を入れる(90 days 目安)

`MCP_ACCESS_TOKEN` を回す場合は、Worker secret と Claude コネクタ設定を**同時に**更新する。片方だけだと全リクエストが 401 になる。

## リポジトリ移動時

Vault を別 owner/name に移す場合:

1. GitHub でリポジトリ移動
2. `wrangler.toml` の `GITHUB_OWNER` / `GITHUB_REPO` を更新して deploy
3. PAT の Repository access を新リポジトリに付け直す
4. Issue 系の owner 固定(`ALLOWED_ISSUE_OWNER`)をコード上も新 owner に合わせる
5. FM インデックス KV を rebuild

履歴(git history)は GitHub の移動に追従。Worker 側に追加作業はほぼ無い。

## MCP 認証は通るが tools/list が空/少ない

- 古い Worker が残っていないか(別名 worker)
- デプロイしたブランチ/版が想定と違う
- 期待数は **17**(v1.6.0)。8 のままのドキュメントは古い

## move_note 後にファイルが二重

create 成功・delete 失敗の典型。`to` を正とし、`from` を `delete_note` で掃除。再発防止のため移動は低頻度・確認付きで。

## search_by_keyword がヒットしない

- 本文しかマッチしない語を使っていないか(本文非検索)
- KV インデックス遅延 → `get_frontmatter` で存在確認、必要なら rebuild
- `path_prefix` の指定ミス

## エスカレーション

1. 本ドキュメントと `architecture.md` / `env-vars.md`
2. Vault-MCP リポジトリの Issue
3. Framework の運用相談(Skill 側の問題か切り分けてから)

## 関連

- setup 簡易版: `docs/ja/setup/02-deploy-mcp-server.md`
- 環境変数: `env-vars.md`
- アーキテクチャ: `architecture.md`


## 切り分けフローチャート(文章版)

1. `tools/list` が 401 → MCP_ACCESS_TOKEN 不一致
2. `tools/list` は 200 だが件数不足 → 古いデプロイ
3. 読取だけ 401/403 → GITHUB_TOKEN 権限
4. 特定パスだけ NOT_FOUND → パス/ブランチ違い
5. 更新だけ CONFLICT → sha 再取得
6. batch だけ失敗 → サブリクエスト予算
7. 検索だけ欠落 → KV インデックス

## curl レシピ集

### tools/list

```bash
curl -sS -X POST "$WORKER_URL/"   -H "Content-Type: application/json"   -H "Authorization: Bearer $MCP_ACCESS_TOKEN"   -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | jq '.result.tools | length'
```

期待: `17`

### get_file_content

```bash
curl -sS -X POST "$WORKER_URL/"   -H "Content-Type: application/json"   -H "Authorization: Bearer $MCP_ACCESS_TOKEN"   -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_file_content","arguments":{"path":"00_meta/vocabulary.md"}}}'
```

## Cloudflare 側の追加チェック

- Workers のルート/カスタムドメインが古い Worker を向いていないか
- 無料枠のリクエスト枯渇
- 誤って別アカウントに deploy していないか

## 「動いたのに急に死んだ」チェックリスト

- [ ] PAT 期限
- [ ] secret の誤上書き
- [ ] GitHub 障害/レート制限
- [ ] KV バインディング削除
- [ ] wrangler.toml の owner/repo 変更のデプロイ忘れ


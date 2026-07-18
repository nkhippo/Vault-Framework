---
title: Vault-MCP 環境変数リファレンス
type: setup
status: published
audience: adopter
tags:
- framework
- mcp-server-reference
- env-vars
keywords:
- mcp
- vault-mcp
- env-vars
summary: Secrets(GITHUB_TOKEN / MCP_ACCESS_TOKEN)と Variables(GITHUB_OWNER 等)、セキュリティ注意、確認方法。
created: '2026-07-18T15:40:00+09:00'
updated: '2026-07-18T15:40:00+09:00'
---

Vault-MCP をデプロイ・運用するときに設定する Secrets / Variables の詳細。値の例はプレースホルダのみを示す。**実トークンを Git にコミットしないこと**。

## 設定の二層

| 種類 | 置き場所 | 可視性 |
|---|---|---|
| Secrets | `wrangler secret put` | ダッシュボード/暗号化。リポジトリに出ない |
| Variables | `wrangler.toml` の `[vars]` | **リポジトリに平文で残る** |

Secrets を `[vars]` に書いてはいけない。

## Secrets(必須)

### `GITHUB_TOKEN`

- **意味**: Worker → GitHub API の認証(Fine-grained PAT 推奨)
- **最小権限(Contents のみ運用)**:
  - Repository access: Vault リポジトリのみ
  - Contents: Read and write
  - Metadata: Read-only(自動)
- **Issue 系ツールを使う場合**: Issues: Read and write を追加
- **有効期限**: 90 days 推奨。切れそうになったら `troubleshooting.md` の rotation 手順へ
- **設定**:

```bash
wrangler secret put GITHUB_TOKEN
# プロンプトに PAT を貼る(ログに残さない)
```

### `MCP_ACCESS_TOKEN`

- **意味**: MCP クライアント(Claude Connectors 等) → Worker の共有秘密
- **生成例**:

```bash
openssl rand -hex 32
```

- **要件**: 32 バイト以上のランダムを推奨。推測可能な文字列禁止
- **設定**:

```bash
wrangler secret put MCP_ACCESS_TOKEN
```

- Claude 側コネクタ設定の Bearer と**完全一致**させる

## Variables(`wrangler.toml` `[vars]`)

現行参照実装の典型:

```toml
[vars]
GITHUB_OWNER = "<your-account>"
GITHUB_REPO = "Vault"
DEFAULT_BRANCH = "main"
```

| 変数 | 必須 | 説明 |
|---|---|---|
| `GITHUB_OWNER` | ✓ | GitHub ユーザーまたは org |
| `GITHUB_REPO` | ✓ | Vault リポジトリ名 |
| `DEFAULT_BRANCH` | ✓(推奨) | 既定 `main`。別名ブランチ運用時のみ変更 |

### ブランチ名について

指示書や古いメモで `GITHUB_BRANCH` と書かれている場合があるが、**現行 Vault-MCP の Env 型 / wrangler は `DEFAULT_BRANCH`**。fork 時は `src/types.ts` と `repoContext` を確認すること。

### 自動注入フラグについて

初期ドキュメントで想定されていた `AUTO_INJECT_ID` / `AUTO_INJECT_UPDATED` のような**独立 env フラグは、現行実装に無い**。

代わりにコード固定の挙動:

| ツール | `created`/`updated` | 備考 |
|---|---|---|
| `create_note` / `update_note` | `ensureTimestamps` で自動 | `updated` は更新時に上書きされやすい |
| `skill_note` | **自動注入しない** | Skill FM を壊さないため |

`id` / `aliases` の自動採番が有効かはバージョン依存。Skill / templates の規約に合わせ、足りなければクライアント側で付与する。

## KV バインディング

```toml
[[kv_namespaces]]
binding = "VAULT_FM_INDEX"
id = "<your-kv-namespace-id>"
```

- Front Matter 検索インデックス用
- 未設定でも基本の Read/Write は動くが、`search_by_keyword` が遅延/劣化しうる
- rebuild は cron(`wrangler.toml` `[triggers].crons`)と admin エンドポイントで実施

## セキュリティ注意

1. **Secrets を `[vars]` に置かない**(GitHub に平文コミットされる)
2. **PAT は最小権限・短期限**
3. **`MCP_ACCESS_TOKEN` を Issue/Chat/スクショに貼らない**
4. **プレビュー URL**(`preview_urls = true`)を使う場合、トークン管理を本番同様に
5. **ログ**: `wrangler tail` に認可ヘッダが出ないか確認。出る実装なら無効化/マスク

## 確認方法

```bash
# ログイン中アカウント
wrangler whoami

# Secret 名の一覧(値は見えない)
wrangler secret list

# ランタイムログ
wrangler tail

# 疎通(値は環境のトークンに置換)
curl -sS -X POST "https://<worker>.workers.dev/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <MCP_ACCESS_TOKEN>" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

Dashboard の Workers → Settings → Variables and Secrets でも確認できる。

## Fine-grained PAT チェックリスト

- [ ] 対象リポジトリに Vault のみ選択
- [ ] Contents: R/W
- [ ] Issues: R/W(Issue ツール利用時)
- [ ] 期限が切れていない
- [ ] 古い PAT を revoke 済み(rotation 後)

## 関連

- アーキテクチャ: `architecture.md`
- トラブルシュート: `troubleshooting.md`
- 導入: `docs/ja/setup/02-deploy-mcp-server.md`


## 設定例(安全な雛形)

```toml
name = "vault-mcp"
main = "src/index.ts"
compatibility_date = "2026-07-01"
compatibility_flags = ["nodejs_compat"]
workers_dev = true

[vars]
GITHUB_OWNER = "<your-account>"
GITHUB_REPO = "Vault"
DEFAULT_BRANCH = "main"

# Secrets はここに書かない:
# GITHUB_TOKEN / MCP_ACCESS_TOKEN
```

## ローカル開発時

`wrangler dev` では `.dev.vars` に Secrets 相当を置ける(gitignore 必須)。

```
GITHUB_TOKEN=...
MCP_ACCESS_TOKEN=...
```

`.dev.vars` を commit しない。チーム共有は 1Password 等のシークレットマネージャ経由。

## 権限を足す判断

| 使いたいツール | 追加権限 |
|---|---|
| Read/Write ノート系のみ | Contents R/W |
| `list_issues` / `create_issue` / `add_issue_comment` | + Issues R/W |
| 将来の Checks/Actions 連携 | 都度最小追加 |

「とりあえず admin」は禁止。

## よくある誤り

- Dashboard で Variable として PAT を追加してしまう
- `MCP_ACCESS_TOKEN` を短すぎる文字列にする
- owner/repo を fork 元のまま自分の Vault に向け忘れる
- DEFAULT_BRANCH を `master` のままにする

## ローテーション記録テンプレ

```text
date:
rotated: GITHUB_TOKEN | MCP_ACCESS_TOKEN
old_expires:
new_expires:
verified_tools_list: yes/no
old_revoked: yes/no
```

Vault の運用メモ(個人領域)に残すと忘れにくい。


---
title: Vault-MCP アーキテクチャ
type: setup
status: published
audience: adopter
tags:
- framework
- mcp-server-reference
- architecture
keywords:
- mcp
- vault-mcp
- architecture
summary: Claude → Worker → GitHub のリクエストフロー、認証、レート制限、ステートレス設計、KV インデックスを説明。
created: '2026-07-18T15:40:00+09:00'
updated: '2026-07-18T15:40:00+09:00'
---

Vault-MCP の内部アーキテクチャを、adopter が fork / 拡張 / 障害調査するときに必要な粒度で説明する。入門のデプロイ手順は `docs/ja/setup/02-deploy-mcp-server.md`、ツール契約は `tools/reference.md` を参照。

## 全体像

```
Claude (or MCP client)
    |  MCP JSON-RPC (HTTPS)
    |  Authorization: Bearer <MCP_ACCESS_TOKEN>
    v
Cloudflare Worker (Vault-MCP)
    |  Octokit / fetch
    |  Authorization: token <GITHUB_TOKEN>
    v
GitHub Contents / Issues / Commits API
    |
    v
GitHub Repository (個人 Vault)
```

応答は逆方向に同じ経路を辿る。Worker はステートレスで、永続データの正本は常に GitHub リポジトリ側にある。

## リクエストフロー(詳細)

1. **クライアント認証**: Worker 入口で `Authorization: Bearer` を `MCP_ACCESS_TOKEN` と照合。不一致は 401
2. **MCP ルーティング**: `@modelcontextprotocol/sdk` の `McpServer` が `tools/list` / `tools/call` を処理
3. **ツール実行**: `src/mcp/tools/*.ts` が Octokit 経由で GitHub API を呼ぶ
4. **楽観ロック**: 更新系は Contents API の blob `sha` を付与。不一致は 409 → アプリ層で `CONFLICT`
5. **付随更新**: 書き込み成功後、可能なら Workers KV(`VAULT_FM_INDEX`)へ Front Matter インデックスを write-through
6. **応答**: MCP の tool result(JSON)としてクライアントへ返す

失敗時はツール単位のエラーコードに正規化される(詳細は `tools/reference.md` の共通エラー表)。

## Cloudflare Workers ランタイムモデル

- **isolate**: リクエストごとに軽量 isolate で JS/TS が実行される
- **edge**: 地理的に近い PoP で動くが、GitHub API は中央寄りなのでレイテンシの支配要因は GitHub 側になりやすい
- **cold start**: しばらく呼ばれていない Worker の初回は起動遅延が乗る。MCP コネクタのタイムアウトとぶつかると「初回だけ失敗」に見える
- **nodejs_compat**: Vault-MCP は `compatibility_flags = ["nodejs_compat"]` を使い、Buffer 等を必要とする SDK を動かす
- **CPU / サブリクエスト上限**: 1 リクエストあたりの外部 fetch 数に上限がある。`get_frontmatter_batch` / `get_project_bundle` は特に消費が大きい

## GitHub Contents API の使い方

Vault-MCP が主に使う操作:

| 操作 | API | 用途 |
|---|---|---|
| 読取 | `GET /repos/{owner}/{repo}/contents/{path}` | `get_file_content` 等 |
| 作成/更新 | `PUT .../contents/{path}` + `sha`(更新時) | `create_note` / `update_note` / `skill_note` |
| 削除 | `DELETE .../contents/{path}` + `sha` | `delete_note` |
| 一覧 | contents(ディレクトリ) | `list_directory` |
| 木走査 | Git Trees API | 検索フォールバック等 |

**blob sha ベースの楽観ロック**:

- 読み取り応答の `sha` を保持し、更新時に送る
- 別クライアントが先に更新していると 409 Conflict
- 対処は「再読取 → 再適用 → 再更新」。Skill 側でも同一セッション内の連続更新で踏む

**Tree API との使い分け**:

- 単一ファイル: Contents
- 広範囲スキャン: Trees(+ KV インデックス)。毎回 Contents を連打しない

## 認証モデル

2 系統の秘密がある。混同しないこと。

| トークン | 区間 | 役割 |
|---|---|---|
| `MCP_ACCESS_TOKEN` | クライアント → Worker | 「誰がこの Worker を叩けるか」 |
| `GITHUB_TOKEN` | Worker → GitHub | 「Worker が Vault をどう操作できるか」 |

- `MCP_ACCESS_TOKEN` が漏洩すると、PAT 権限の範囲で Vault を遠隔操作できる
- `GITHUB_TOKEN` が漏洩すると、PAT 直接攻撃になる
- どちらも wrangler **secret**(平文 vars 禁止)

詳細は `env-vars.md`。

## レート制限

| 層 | 目安 | 影響 |
|---|---|---|
| Cloudflare Workers Free | 100k req/day 前後 | Worker 自体の呼び出し上限 |
| GitHub REST(認証付き) | 5000 req/hour 目安 | Contents/Issues 連打で到達 |
| Worker サブリクエスト | 1 invocation あたり上限 | batch/bundle で `SUBREQUEST_BUDGET_EXCEEDED` |

個人利用は通常 Free 枠内。自動化や全 Vault スキャンを頻繁に回すと GitHub 側が先に尽きる。

## キャッシュ戦略

現行 Vault-MCP(v1.6.0 系)の実装傾向:

- **正本キャッシュは持たない**(ファイル内容の長期キャッシュ無し)
- **Workers KV `VAULT_FM_INDEX`**: Front Matter 検索用インデックス。write-through + 週次 rebuild cron
- 検索はインデックス優先、欠落時は tree 走査へフォールバック(遅い)

つまり「さっき書いた内容が search に出ない」はインデックス遅延の可能性あり。確実な内容確認は `get_file_content` / `get_frontmatter`。

## ステート

Vault-MCP は**ステートレス**を基本方針とする。

- セッション状態・会話履歴は Worker に保存しない
- 永続化は GitHub(と検索用 KV インデックス)のみ
- 水平スケールや再デプロイでユーザーデータは消えない(KV は検索補助。失っても rebuild 可能)

## 関連コンポーネント

| パス | 役割 |
|---|---|
| `src/index.ts` | HTTP 入口、認証、MCP 接続 |
| `src/mcp/server.ts` | ツール登録(version 表示もここ) |
| `src/mcp/tools/*` | 各ツール実装 |
| `src/github/*` | Contents/エラーマッピング |
| `src/frontmatter/*` | YAML 解析・`ensureTimestamps` |
| `src/kv/*` | FM インデックス |
| `wrangler.toml` | vars / KV / cron / observability |

## 設計上のトレードオフ

- **シンプルさ優先**: 独自 DB を持たず GitHub を正本にする
- **アトミック移動は弱い**: `move_note` は create+delete
- **Issue owner 制限**: MVP で固定 owner。fork 利用者はコード変更が必要
- **Skill 専用書き込み**: `skill_note` で auto-`updated` を避ける

## 関連

- 環境変数: `env-vars.md`
- 拡張: `extending.md`
- 障害対応: `troubleshooting.md`
- ツール契約: `tools/reference.md`


## シーケンス例: create_note

1. Client `tools/call` create_note
2. Worker が Bearer 検証
3. 既存 path の有無を Contents GET で確認(あれば ALREADY_EXISTS)
4. frontmatter に `ensureTimestamps({isCreate:true})`
5. Markdown を組み立て Contents PUT(sha なし)
6. KV インデックスへ upsert(失敗しても本処理は成功扱いの実装がありうる)
7. `{path, sha, commit_url}` を返却

## シーケンス例: update_note(replace_body)

1. 現行ファイルを GET(sha 取得)
2. frontmatter / body を分離
3. mode に応じて body を置換/追記
4. `update_frontmatter` をマージ + timestamps
5. PUT with sha
6. 409 ならクライアント再試行

## セキュリティ境界

- Worker はインターネットに公開される URL を持つ前提
- 認可の単一鍵が MCP_ACCESS_TOKEN
- ネットワーク ACL は Cloudflare 側の追加設定(IP allowlist 等)で強化可能だが、参照実装の既定には含めない
- Prompt injection で「PAT を話せ」と来ても、Worker はモデルに PAT を返さない(サーバ秘密)

## 可観測性

`wrangler.toml` の observability.logs が有効なら、呼び出しログを Dashboard で追える。traces は既定無効。メトリクス(ツール名、エラー、サブリクエスト)は `src/utils/metrics.ts` 経由。

## バージョン表示

`src/mcp/server.ts` の `version` フィールド(例: `1.6.0`)が MCP initialize 応答に載る。ドキュメントの「17 ツール」記述と突き合わせるときに使う。


---
title: Vault-MCP 拡張ガイド
type: setup
status: published
audience: adopter
tags:
- framework
- mcp-server-reference
- extending
keywords:
- mcp
- vault-mcp
- extending
summary: fork 方針、独自ツール追加手順、既存ツール改変時の後方互換、Skill との関係。
created: '2026-07-18T15:40:00+09:00'
updated: '2026-07-18T15:40:00+09:00'
---

Vault-MCP を fork して独自ツールを足す、あるいは既存ツールを改変するためのガイド。Framework Skill が前提とする契約を壊さないことが最重要。

## 推奨方針: fork + upstream merge

1. `https://github.com/nkhippo/Vault-MCP` を fork
2. 自分のアカウントで Workers にデプロイ(setup/02)
3. 独自変更は専用ブランチ(例: `feat/my-tool`)で行う
4. 定期的に upstream `main` を merge / rebase

スタンドアロン複製より fork の方がセキュリティ修正の取り込みが楽。

## リポジトリ内の拡張ポイント

| 場所 | 何をするか |
|---|---|
| `src/mcp/tools/<name>.ts` | ツール実装 + zod schema |
| `src/mcp/server.ts` | `registerTool` |
| `src/github/*` | GitHub API ラッパの再利用 |
| `src/types.ts` | Env 追加が必要なら |
| `test` / `src/__tests__` | 単体テスト |
| `wrangler.toml` | 新 KV / cron / vars |

## 独自ツール追加手順

### 1. 実装ファイルを作る

`src/mcp/tools/my_tool.ts` に、既存ツールと同じパターンで:

- `export const myToolSchema = { ... zod ... }`
- `export async function myToolTool(env, args) { ... instrumentTool ... }`

成功は `toolSuccess`、失敗は `toolError` に寄せるとクライアントが共通処理できる。

### 2. `server.ts` で登録

```ts
server.registerTool(
  "my_tool",
  { description: "...", inputSchema: myToolSchema },
  async (args) => myToolTool(env, args)
);
```

`createMcpServer` の version 文字列も、破壊的変更時は上げる。

### 3. ローカル検証

```bash
npm test
wrangler dev
# 別ターミナルで tools/list / tools/call
```

### 4. デプロイ

```bash
wrangler deploy
```

### 5. クライアント確認

- Claude Connectors で `tools/list` に新ツールが出るか
- 実際の `tools/call` で引数・エラーを確認

## 既存ツール改変時の注意

Framework の `skills/vault-manager` 等は、次を**契約**として扱う。

- `create_note` は既存パスで失敗(上書きしない)
- `update_note` の mode 意味を変えない
- `skill_note` は `updated` を自動注入しない
- Issue 系の承認ゲートは Skill 側。サーバが勝手に緩和しても Skill は承認前提のまま

**後方互換のルール**:

- パラメータ追加: オプションなら互換
- パラメータ削除・意味変更・必須化: 破壊的。Framework CHANGELOG / Vault-MCP CHANGELOG に明記し、MINOR/MAJOR を適切に

## upstream merge の頻度

- Vault-MCP の CHANGELOG / Release を購読
- Framework CHANGELOG に「Vault-MCP vX.Y.Z 以降が必要」と出たら**先に MCP を上げてから** Framework update(`docs/ja/setup/08-update.md`)
- 目安: 月 1 回 upstream を取り込む。セキュリティ修正は即時

衝突しやすい箇所: `server.ts` の登録順、`wrangler.toml` の KV id、独自 env。

## 独自ツールと Framework Skill の関係

- Skill は知らないツールを自動では使わない
- 独自ツールを常用するなら:
  1. プロジェクト Instructions に「いつどのツールを使うか」を書く
  2. 必要なら fork した Skill にトリガー文を追加(Framework canonical を直接汚さない)
- canonical/personal 境界は `docs/ja/setup/canonical-vs-personal.md`

## テストの最低ライン

- zod スキーマの失敗ケース
- GitHub 404/409 のマッピング
- 冪等なツール(`create_directory`)の再実行
- 予算超過時のエラー(batch 系を触る場合)

## やってはいけないこと

- Secrets をコードやテストフィクスチャに直書き
- `ensureTimestamps` を Skill パスに適用してしまう
- owner 制限を外したまま公開 Worker を無認証で晒す
- Framework の examples を個人運用の正本にする(スナップショットにすぎない)

## 関連

- ツール契約: `tools/reference.md`
- 環境変数: `env-vars.md`
- アーキテクチャ: `architecture.md`


## 実装テンプレート(骨格)

```ts
import { z } from "zod";
import type { Env } from "../../types.js";
import { instrumentTool } from "../../utils/metrics.js";
import { toolError, toolSuccess } from "../response.js";

const TOOL_NAME = "my_tool";

export const myToolSchema = {
  path: z.string().min(1).describe("Vault-relative path"),
};

export async function myToolTool(env: Env, args: { path: string }) {
  return instrumentTool(TOOL_NAME, async (budget) => {
    try {
      // ... use createOctokit(env, budget) ...
      return toolSuccess({ ok: true });
    } catch (error) {
      return toolError(error, TOOL_NAME);
    }
  });
}
```

## レビューチェックリスト(PR 前)

- [ ] description が tools/list で意味を成す
- [ ] 必須/任意が Skill から見て直感的
- [ ] エラーが共通コードにマップされる
- [ ] サブリクエスト数が見積もれる
- [ ] 秘密がログに出ない
- [ ] Framework Skill の契約を壊していない
- [ ] テストまたは手動再現手順がある

## ドキュメント同期

独自ツールを公開するなら、自分の fork 配下に `tools/reference` 相当を足すか、個人 Vault の project instructions に契約を書く。Framework 本家の `mcp-server-reference/` に個人ツールを混ぜない。

## monorepo にしたくなったら

Vault-MCP を Framework に取り込みたくなるが、リリース周期が違う。現状の「別リポジトリ」を維持し、Framework は契約ドキュメントだけ持つ方針が v1.1.0 の前提。


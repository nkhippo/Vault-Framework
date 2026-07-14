---
created: 2026-07-13T22:30:00+09:00
example_of_type: knowledge
keywords:
  - example
  - knowledge
  - cloudflare-workers
  - mcp
  - constraints
  - nodejs_compat
  - secrets
related: []
status: published
summary: knowledge type の記入例。Cloudflare Workers で MCP サーバを実装した際の制約と対処法を題材にした汎用ナレッジの例。特定プロジェクトに依存しない形で技術的な学びを残す。
tags:
  - example
  - knowledge
  - cloudflare
  - mcp
  - dev
title: "例: Cloudflare Workers で MCP サーバを実装して学んだこと"
type: example
updated: 2026-07-13T22:30:00+09:00
---

## Summary

Cloudflare Workers で MCP サーバを実装した際に得た、Cloudflare Workers 特有の制約と対処法のメモ。汎用ナレッジとして参照可能な例。

**この例が示す構造**: knowledge type の標準構造(Summary → 内容の見出し別記述 → 出典・参考)。技術的な学びを、特定プロジェクトに依存しない形で残す。

## Cloudflare Workers の主要な制約

### CPU 時間制限

- **Free plan**: 10ms/request
- **Paid plan**: 30 秒/request(現行)

MCP サーバの用途では、GitHub API 呼び出しと Front Matter のパース程度なので Free plan の 10ms でも通常は収まる。ただし複雑なファイル整形やバッチ処理をやると超える可能性あり。

### メモリ制限

- 128 MB per request

通常は問題にならない。大量のファイル一括処理をやる場合(例: 100 ファイル同時に list_directory)は要注意。

### nodejs_compat フラグの必要性

- `wrangler.toml` で `compatibility_flags = ["nodejs_compat"]` を有効化
- `Buffer` や `crypto` 等の Node.js 互換 API が使えるようになる
- `@modelcontextprotocol/sdk` は Buffer を使うため、これが必要

### Secrets の管理

- `wrangler secret put <NAME>` で環境変数として暗号化保存
- コード内では `env.<NAME>` で参照
- Fine-grained PAT や MCP アクセストークンはここに置く
- `wrangler.toml` の `vars` セクションには **絶対に置かない**(平文でリポジトリに残る)

## MCP プロトコル実装での落とし穴

### SSE(Server-Sent Events)のサポート

- MCP は SSE ベースのプロトコル
- Cloudflare Workers はネイティブに SSE をサポート
- Response の `Content-Type: text/event-stream` と、`Transfer-Encoding: chunked` の適切な処理が必要

### ツール定義の JSON Schema

- 各ツールは name / description / inputSchema を持つ
- `inputSchema` は zod → JSON Schema 変換ライブラリで生成できる
- Claude 側の tool_use で `input` パラメータ名として使われるため、命名は明快に

### エラーレスポンス

- ツール実行時のエラーは MCP プロトコル準拠のエラーレスポンスを返す
- 単なる throw ではなく、`isError: true` のツール結果として返す

## GitHub API 使用時の注意

### Rate limit

- Fine-grained PAT: 5000 requests/hour(認証済みなら十分)
- 個人利用では通常到達しない

### Contents API vs Git Data API

- 単一ファイル読み書きは Contents API(`GET/PUT /repos/{owner}/{repo}/contents/{path}`)で十分
- 一括操作や高度な履歴操作は Git Data API が必要
- 個人利用の MCP サーバは Contents API のみで完結する

### ファイル名の URL エンコード

- パスに日本語や特殊文字が含まれる場合、URL エンコードが必要
- `@octokit/request` は自動でエンコードするが、生 fetch で叩く場合は要注意

## 出典・参考

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [GitHub REST API Reference](https://docs.github.com/en/rest)
- Vault-Framework 内の関連 ADR: `docs/ja/decisions/0002-cloudflare-workers-for-mcp.md`, `docs/ja/decisions/0012-fine-grained-pat-adoption.md`

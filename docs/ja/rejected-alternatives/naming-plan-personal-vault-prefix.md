---
audience: mixed
created: 2026-07-14 05:55:00+09:00
date: 2026-07-13
keywords:
- naming
- personal-vault
- kebab-case
- prefix
- verbose
related_adrs:
- '0006'
status: rejected
summary: 3 リポジトリの命名に personal-vault-* プレフィックスを付ける案。一度は採用されたが、冗長性と「personal」の違和感で撤回され、Vault-*
  へ変更。
superseded_by: '0006'
tags:
- rejected
- naming
title: '却下案: personal-vault-* プレフィックス'
type: rejected_alternative
updated: 2026-07-14 05:55:00+09:00
---

## Summary

3 リポジトリの命名に `personal-vault-*` プレフィックスを付ける案(personal-vault、personal-vault-mcp、personal-vault-framework)。一度は採用されたが、冗長性と「personal」の違和感で撤回。ADR-0006 で `Vault-*` に統一。

## What Was Proposed

3 リポジトリの命名を以下の kebab-case 統一で行う案:

- `personal-vault`(vault 本体)
- `personal-vault-mcp`(MCP サーバ)
- `personal-vault-framework`(Framework)

判断の背景として、この命名は初期段階(2026-07-13 昼〜夕方)で一度採用され、Vault-Framework の初期構造構築計画(step 2 の Cursor 指示書)にも組み込まれていた。しかし step 2 実行前に撤回された。

## Why It Was Considered

- **明示的な「個人所有」の宣言**: personal というプレフィックスで「これは個人利用の vault」であることが明確
- **他リポジトリとの区別**: nkhippo 配下の他リポジトリ(<your-project> 等)と命名で区別できる
- **公開時の非侵襲性**: Public 化した時「personal」という語で「これは俺のもの、参考にどうぞ」感が出る
- **kebab-case 統一**: GitHub の他リポジトリ命名スタイルと一貫

## Why It Was Rejected

- **typing コスト高**: `personal-vault-mcp` は 17 文字、対して `Vault-MCP` は 9 文字。日常的な typing 頻度を考えると差が大きい
- **「personal」の違和感**: 導入者(第三者)が Fork する時、「personal」という語が「これは自分のものではない」感を強化する
- **URL 長さ**: GitHub URL(`github.com/<user>/personal-vault-mcp`)、Cloudflare Workers URL(`personal-vault-mcp.<subdomain>.workers.dev`)の可読性が低下
- **Fable マニュアル化時の記述量**: Framework のドキュメントで「personal-vault-mcp」を何度も繰り返す必要があり、記述が冗長
- **kebab-case への統一の魅力より、簡潔さの魅力が勝る**: リポジトリ名を短くすることのメリットが大きい
- **表示名との差**: MCP コネクタ表示名は「Personal Vault MCP」となるが、これも長い

## What Was Chosen Instead

- **採用案**: ADR-0006「命名スキーム: Vault / Vault-MCP / Vault-Framework」
- **参照**: `id-ref-removed`

`Vault-*` に統一。内部呼称と外部名を統一、typing コスト最小。

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md`
- 対応 ADR: `id-ref-removed`
- 関連却下案: 他 6 命名候補(下記)
  - `id-ref-removed`
  - `id-ref-removed`
  - `id-ref-removed`
  - `id-ref-removed`
  - `id-ref-removed`
  - `id-ref-removed`

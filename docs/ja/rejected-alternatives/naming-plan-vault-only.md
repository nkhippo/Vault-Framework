---
audience: mixed
created: 2026-07-14 06:00:00+09:00
date: 2026-07-13
keywords:
- naming
- vault-only
- monorepo
- single-name
- identification
related_adrs:
- '0005'
- '0006'
status: rejected
summary: 3 リポジトリを全て Vault と命名し、区別を付けない案。MCP・Framework がリポジトリ名で識別できず、Public 化時に混乱を招くため却下。
superseded_by: '0006'
tags:
- rejected
- naming
title: '却下案: Vault のみ命名'
type: rejected_alternative
updated: 2026-07-14 06:00:00+09:00
id: pj-2026-07-13-cb3e
aliases:
- pj-2026-07-13-cb3e
---

## Summary

3 リポジトリを全て `Vault` と命名し、区別を付けない案(内部で MCP・Framework を区別する)。MCP・Framework がリポジトリ名で識別できず、Public 化時に混乱を招くため却下。ADR-0006 で `Vault-*` に統一。

## What Was Proposed

3 リポジトリを全て `Vault` と命名し、以下のように区別する案:

- リポジトリ名: 全て `Vault`(実際には別リポジトリだが、内部呼称で区別)
  - `nkhippo/Vault`(データ本体)
  - `nkhippo/Vault`(MCP、別 organization or サブディレクトリ)
  - `nkhippo/Vault`(Framework、別 organization or サブディレクトリ)
- 内部呼称: 「Vault データ」「Vault MCP」「Vault Framework」で区別

または、モノレポで 1 つの `Vault` リポジトリ内に:

- `/data/`(実データ)
- `/mcp/`(MCP サーバコード)
- `/framework/`(Framework ドキュメント)

## Why It Was Considered

- **シンプルさの極致**: 覚えるべき名前が 1 つだけ
- **統一ブランド**: 「Vault」というブランドが一貫し、記憶しやすい
- **モノレポの利便性**: 1 リポジトリで全てが管理される場合、Cursor でのマルチファイル操作が容易
- **URL の一貫性**: どこを見ても `Vault` という語

## Why It Was Rejected

- **リポジトリ名の識別不能**: GitHub 上で「これはどの Vault か?」が名前だけでは判別できない
- **Public 化時の混乱**: 導入者が Fork する時、「どのリポジトリを Fork すべきか」が不明確
- **モノレポの弊害**: データ(private 前提)と Framework(public)を同一リポジトリに置くと、公開範囲の制御が困難
- **役割の混在**: データ集約・MCP 実装・Framework 定義の 3 つの異なる責務が同一リポジトリに混在
- **Cloudflare Workers 側の設定**: MCP サーバのリポジトリ名を wrangler.toml で指定する時、「Vault のどのサブディレクトリか」を指定する必要があり煩雑
- **Cursor の混乱**: 「Vault のどこを触るか」を毎回明示する必要があり、指示書が長くなる
- **Fable パッケージング困難**: Framework 部分だけをパッケージ化する時、モノレポからの抽出が必要

## What Was Chosen Instead

- **採用案**: ADR-0006「命名スキーム: Vault / Vault-MCP / Vault-Framework」
- **参照**: [[../decisions/0006-naming-vault-scheme.md]]

3 リポジトリを明確に別名で区別。責務分離とパッケージ化の柔軟性を確保。

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md`
- 対応 ADR: [[../decisions/0006-naming-vault-scheme.md]]
- 関連 ADR: [[../decisions/0005-early-framework-separation.md]](Framework 分離の意義)

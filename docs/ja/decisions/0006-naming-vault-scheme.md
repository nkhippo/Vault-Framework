---
audience: mixed
created: 2026-07-14 03:40:00+09:00
date: 2026-07-13
id: pj-2026-07-13-e13e
keywords:
- naming
- vault
- vault-mcp
- vault-framework
- convention
- rename
- personal-vault
- hashicorp-collision
related_adrs:
- '0001'
- '0005'
related_chats:
- 10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md
related_specs:
- file-naming
status: accepted
summary: 3 リポジトリ(Vault / Vault-MCP / Vault-Framework)の命名を確定した意思決定。当初の personal-vault-*
  プレフィックス案は撤回され、シンプルさ優先で Vault-* に統一。内部命称と外部名を統一する方針。
superseded_by: null
supersedes: null
tags:
- adr
- naming
- important
title: 'ADR-0006: 命名スキーム: Vault / Vault-MCP / Vault-Framework'
type: adr
updated: 2026-07-14 03:40:00+09:00
aliases:
- pj-2026-07-13-e13e
- adr-0006
---

## Summary

3 リポジトリ(`Vault` / `Vault-MCP` / `Vault-Framework`)の命名を最終確定した意思決定。当初は `personal-vault-*` プレフィックス案だったが、シンプルさ優先で `Vault-*` に統一。内部呼称と外部名を統一する方針。

## Context

Vault-Framework 分離(ADR-0005)にあたり、3 リポジトリの命名を確定させる必要があった。以下 8 命名候補を比較検討:

- 案 A: Vault のみ(Framework も MCP も名前で区別しない)
- 案 B: `personal-vault-*` プレフィックス統一(personal-vault、personal-vault-mcp、personal-vault-framework)
- 案 C: `<Naoya>-Vault` 系(naoya-vault、naoya-vault-mcp)
- 案 D: 比喩系(Cerebro / Cortex / Memex 等の脳・記憶メタファ)
- 案 E: Codex 系(codex、codex-mcp)
- 案 F: Archive / Ledger 系(archive-* / ledger-*)
- 案 G: 日本語命名(記録所、知識庫 等)
- 案 H: 機能名オンリー(chat-storage、mcp-server 等の記述的命名)

同時に、内部呼称と外部名(GitHub リポジトリ名)を分けるかどうかも論点だった。初期案では「内部 Vault / 外部 personal-vault-*」の 2 段構えを想定していたが、後日「シンプルさ優先で統一」に方針転換。

## Decision

**命名: `Vault` / `Vault-MCP` / `Vault-Framework` で統一**

| 対象 | GitHub リポジトリ名 | iCloud フォルダ名 | 内部呼称 |
|---|---|---|---|
| vault 本体 | `Vault` | `Vault` | Vault |
| MCP サーバ | `Vault-MCP` | `Vault-MCP` | Vault-MCP |
| Framework | `Vault-Framework` | `Vault-Framework` | Vault-Framework |

### MCP コネクタ名の表記ルール

同一実体を指す 3 表記が並立する点に注意:

- **表示名(Claude UI 上)**: 空白区切り + 大文字始まり(例: `Vault MCP`)
- **リポジトリ名**: ハイフン区切り + 大文字始まり(例: `Vault-MCP`)
- **Cloudflare Workers URL**: 小文字 + ハイフン(例: `vault-mcp.<subdomain>.workers.dev`)

### 導入者向けの推奨

Framework の導入者にも同じ命名を推奨する。「導入者は自分の GitHub でリポジトリ名を `Vault` にすれば、ドキュメント通りに動く」というシンプルな体験を提供。ただし、HashiCorp Vault との衝突リスクへの対処ガイドを Framework の `docs/ja/naming-conventions.md` に含める。

## Consequences

**Positive**:

- シンプル、統一感、typing コスト最小
- 導入者のカスタマイズ負荷が最小(内部呼称と外部名の 2 段管理が不要)
- ドキュメント記述が一貫(vault リポジトリ = `Vault`、vault の概念 = vault、と使い分け可能)
- Framework の Fable マニュアル化時、命名を機械的に説明できる

**Negative**:

- HashiCorp Vault との名前衝突(GitHub 検索で混じる、混乱の可能性)
- Public 化時に第三者が Fork する時の障害になる可能性
- 「vault」という一般名詞と重なるため、文脈で判別が必要な場面がある

**Mitigation**:

- Private リポジトリ運用中は実害ゼロ(第三者からは見えない)
- Public 化ガイドで代替命名を提示(`<YourName>-Vault`、`Personal-Vault`、`Knowledge-Vault` 等)
- ドキュメント内で「大文字 Vault はリポジトリ、小文字 vault は概念」の使い分けを glossary で明示(ADR-0003 の関連 spec 参照)

## Alternatives Considered

### 案 B: `personal-vault-*` プレフィックス案(一度採用 → 撤回)

このプレフィックス案は初期に採用され、Vault-Framework の初期構造構築計画にも組み込まれていた。しかしその後、以下理由で撤回:

- 冗長性(`personal-vault-mcp` は typing コストが高い)
- 「personal」という語が導入者にとって違和感(第三者導入時に「これは自分のものではない」感)
- URL 短さも Vault-* の方が優位

詳細: [[pj-2026-07-13-f5da]]

### その他の却下案

- **案 A**(Vault のみ): MCP・Framework の区別不能。詳細: [[pj-2026-07-13-cb3e]]
- **案 D**(Cerebro/Cortex 系): 過度に修辞的、機能理解を阻害。詳細: [[pj-2026-07-13-395d]]
- **案 E**(Codex 系): OpenAI Codex との衝突リスク。詳細: [[pj-2026-07-13-3e01]]
- **案 F**(Archive/Ledger 系): 「終わった感」or「金融連想」で違和感。詳細: [[pj-2026-07-13-dc3d]]
- **案 G**(日本語命名): 多言語対応時の障壁、GitHub URL の可読性低下。詳細: [[pj-2026-07-13-93a4]]
- **案 H**(機能名オンリー): ブランド性欠如、プロジェクトの一体感が出ない。詳細: [[pj-2026-07-13-156d]]

## Related

- **前提 ADR**: ADR-0001(GitHub-as-a-Backend、リポジトリ命名の前提)、ADR-0005(Framework 早期分離、3 リポジトリ構成の前提)
- **後続 ADR**: なし(この命名は他 ADR で参照される基盤)
- **関連 spec**: `../specs/file-naming.md`(ファイル名の kebab-case 規約と対応)
- **元記録**: 
  - `10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md`
  - 撤回セッション: 2026-07-13 深夜(初期構造構築後)

## Change Log

- 2026-07-13 昼: 初版(`personal-vault-*` プレフィックス案採用)
- 2026-07-13 夕方: 撤回、`Vault-*` に統一(現行)

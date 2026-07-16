---
audience: mixed
created: 2026-07-14 06:25:00+09:00
date: 2026-07-13
keywords:
- naming
- japanese
- romaji
- kanji
- multilingual
- public-adopters
- seo
related_adrs:
- '0005'
- '0006'
status: rejected
summary: 3 リポジトリを日本語(記録所、知識庫、保管室 等)で命名する案。多言語対応時の障壁、GitHub URL の可読性低下、Framework の
  Public 化戦略との不整合により却下。
superseded_by: '0006'
tags:
- rejected
- naming
title: '却下案: 日本語命名'
type: rejected_alternative
updated: 2026-07-14 06:25:00+09:00
id: pj-2026-07-13-93a4
aliases:
- pj-2026-07-13-93a4
---

## Summary

3 リポジトリを日本語(記録所、知識庫、保管室 等)で命名する案。多言語対応時の障壁、GitHub URL の可読性低下、Framework の Public 化戦略との不整合により却下。ADR-0006 で `Vault-*` に統一。

## What Was Proposed

3 リポジトリを日本語(ローマ字表記または漢字表記)で命名する案:

**候補パターン A(ローマ字表記)**:
- `Kirokusho`(記録所、vault 本体)
- `Kirokusho-MCP`(MCP)
- `Kirokusho-Framework`(Framework)

**候補パターン B(漢字混在)**:
- `記録所`(vault、URL では `%E8%A8%98...` 表記)
- `Kioku-MCP`(記憶 MCP)
- `Chishikitaikei`(知識体系、Framework)

**候補パターン C(訳語系)**:
- `Chishiki-Ko`(知識庫)
- `Chishiki-MCP`
- `Chishiki-Framework`

## Why It Was Considered

- **母語の親近感**: Naoya にとって最も直感的な命名
- **オリジナリティ**: 英語圏で既にある命名との衝突を回避
- **日本語コンテンツとの一貫性**: vault の内容(記録、note 記事)が日本語中心のため、リポジトリ名も日本語で揃える
- **文化的アイデンティティ**: 日本発のプロジェクトであることを明示

## Why It Was Rejected

### 多言語対応時の障壁

- **将来 Public 化・Fable 展開時、英語圏の導入者にとって理解不能**: `Kirokusho` の意味が伝わらず、フォーク数減少
- **Framework の Fable マニュアル化と不整合**: ドキュメントを英語で書く時、リポジトリ名だけ日本語は違和感
- **国際 SEO の低下**: `Kirokusho` の検索ボリュームは実質ゼロ、発見性低下

### GitHub URL の可読性

- **`Kirokusho-MCP` は英語ネイティブに typing しにくい**: R-O-K-U-S-H-O の順序が直感的でない
- **漢字表記(`記録所`)は URL エンコードで文字化け表示**: `github.com/nkhippo/%E8%A8%98...` は読めない
- **Cloudflare Workers URL**: `kirokusho-mcp.<subdomain>.workers.dev` は打ちにくい

### コード内での混在

- **英語のコード + 日本語のリポジトリ名 = 認知負荷増**: `import from 'kirokusho-mcp'` は違和感
- **エラーメッセージ・ログの検索性低下**: 日本語のリポジトリ名を含むログを英語圏の開発者が読む時のノイズ

### プロジェクト目標との衝突

- **Framework の目標: Public 化・Fable パッケージング**: 導入者は英語圏を含む
- **単一言語ロックの回避**: リポジトリ名を英語にしておく方が、後日の多言語対応で自由度が高い

## What Was Chosen Instead

- **採用案**: ADR-0006「命名スキーム: Vault / Vault-MCP / Vault-Framework」
- **参照**: [[../decisions/0006-naming-vault-scheme.md]]

英語名で統一。ドキュメントは日本語版(ja/)と英語版(en/)を並列で用意する Framework 構成。

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md`
- 対応 ADR: [[../decisions/0006-naming-vault-scheme.md]]
- 関連 ADR: [[../decisions/0005-early-framework-separation.md]](Public 化・Fable 化の前提)

---
audience: mixed
date: 2026-07-14
keywords:
- naming
- 命名規約
- kebab-case
- repository-naming
- hashicorp-collision
related_adrs:
- '0006'
related_specs:
- file-naming
- vocabulary-design
status: published
summary: Vault-Framework の命名規約の全体像。ファイル名、ディレクトリ名、リポジトリ名それぞれの命名思想を概説。
title: 命名規約の思想
title_en: Naming Conventions Overview
type: overview
created: 2026-07-14 20:47:31+09:00
updated: 2026-07-14 20:47:31+09:00
id: pj-2026-07-13-d0c9
aliases:
- pj-2026-07-13-d0c9
---

## Summary

Vault-Framework の命名規約の全体像を概説する。ファイル名、ディレクトリ名、リポジトリ名それぞれの命名思想を扱い、詳細仕様は spec を参照する形にする。

## 命名の全体方針

Vault-Framework の命名規約は、以下 3 つの原則を貫いている:

1. **AI が推測なしに特定できること**: kebab-case、日付形式の統一等、機械的に予測可能なパターン
2. **人間にも読みやすいこと**: 過度に省略しない、意味のある単語を使う
3. **ブランド中立性**: 特定のツール(Obsidian 等)や既存プロダクト(HashiCorp Vault 等)との名前衝突を避ける

## ファイル名の命名規則(概要)

標準形式は `YYYY-MM-DD_kebab-case-slug.md`。

- 日付は ISO 8601 の日付部分(JST 基準)
- スラグは英語の kebab-case、30 文字以内
- 日記等の例外パターンあり(詳細は spec 参照)

詳細な規則、スラグ生成ロジック、Skill 側の自動生成アルゴリズムは [[pj-2026-07-13-5c9b|file-naming spec]] を参照。

## ディレクトリ名の命名規則(概要)

トップレベルディレクトリは `<数字プレフィックス>_<snake_case>` 形式(例: `10_chat_logs/`)。数字プレフィックスは 10 刻みで、将来の拡張余地を残している。

プロジェクトディレクトリ(`30_projects/<RepoName>/`)は GitHub リポジトリ名と完全一致させる。

## リポジトリ命名の経緯

Vault-Framework エコシステムを構成する 3 つのリポジトリは以下のように命名されている:

- `Vault`(データ本体、Private)
- `Vault-MCP`(MCP サーバ実装、Cloudflare Workers)
- `Vault-Framework`(公開用フレームワーク、このリポジトリ)

### 命名変更の経緯

当初の命名候補には Obsidian ブランドを含むもの(`Obsidian-Vault` 等)や、`Personal-Vault` プレフィックスを持つものがあったが、最終的に現在の命名(`Vault` / `Vault-MCP` / `Vault-Framework`)に落ち着いた。

主な理由:

- **Obsidian ブランドからの独立**: Vault-Framework は Obsidian に依存しない設計(philosophy.md 参照)であり、命名もそれを反映すべきと判断
- **シンプルさの優先**: `Personal-Vault` 等のプレフィックスは冗長と判断し撤回
- **HashiCorp Vault との名前衝突リスク**: `Vault` という単体の名前は HashiCorp のシークレット管理ツールと衝突する可能性があるため、Public 化・Fork 時には導入者が独自の命名(`<YourName>-Vault` 等)を選ぶことを推奨している(setup ガイド参照)

検討された却下案の詳細は [[pj-2026-07-13-3fc6|rejected-alternatives の naming-plan-* 系]] を参照。

## 統制語彙との関係

命名規則とは別に、Front Matter の `type`、`status`、`tags`、`project` フィールドには統制語彙(controlled vocabulary)を用いる。これはファイル名やディレクトリ名の「命名」とは異なるレイヤーの統制であり、詳細は [[pj-2026-07-13-f5e9|vocabulary-design spec]] を参照。

## ID scheme(Phase 0.5-0.6 以降)

Vault 内の全 markdown は Front Matter に `id: <prefix>-YYYY-MM-DD-<4hex>` を持つ。
詳細はリポジトリ直下の [`docs/id-scheme.md`](../../id-scheme.md) を参照。命名との関係:

- ファイル名は既存規約通り(README.md 等の特殊ファイルは維持)
- id はファイル名と独立の識別子として機能する
- `aliases` 経由でファイルパスと id が結び付けられる(`aliases[0] == id`)
- 新規保存時の id 付与手順は Skill `vault-manager`(Phase 0.6)と [save-decision-flow](../guidelines/save-decision-flow.md) を参照

## 関連

- [ADR 0006: 命名スキームの確定](../decisions/0006-naming-vault-scheme.md)
- [ADR 0017: Skill vault-manager への id scheme 統合](../decisions/0017-skill-id-scheme-integration.md)
- [[pj-2026-07-13-5c9b|file-naming spec: ファイル名規約の詳細仕様]]
- [[pj-2026-07-13-f5e9|vocabulary-design spec: 統制語彙の設計]]
- [[pj-2026-07-13-3fc6|rejected-alternatives: 却下された命名案]]
- [[pj-2026-07-13-b9c7|Philosophy: GitHub-as-a-Backend]]

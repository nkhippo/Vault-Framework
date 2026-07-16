---
title: Wikilink Conventions
created: 2026-07-16
status: draft
tags:
- id-scheme
- phase-0.5
id: pj-2026-07-16-8def
aliases:
- pj-2026-07-16-8def
---

# Wikilink Conventions

## Summary

Markdown body 内のリンクは、path ではなく **ID ベースの wikilink** を標準記法とする。構造的な関係（親子・派生元など）は Front Matter の `_id` / `_ids` で表現し、文脈的な言及は body 内 wikilink で行う。両者の役割を混同しない。

## 基本記法

- 基本: `[[<id>|<display text>]]`
- 例: `[[pj-2026-07-16-a3f2|発音アプリの UI 見直し]]`
- Display text は原則必須（可読性のため）。例外的に `[[<id>]]` も許容する（display を省くと Obsidian は id 文字列をそのまま表示する）

```markdown
[[pj-2026-07-16-a3f2|発音アプリの UI 見直し]]
[[pj-2026-07-16-a3f2]]
```

## セクションリンク

- 他ファイルのセクション: `[[<id>#見出し名|display text]]`
- 同ファイル内のセクション: `[[#見出し名]]`
- セクション名は該当ファイルの H2 以下の見出しに完全一致（case-insensitive）

```markdown
[[pj-2026-07-16-a3f2#参照フィールド命名規約|命名規約]]
[[#Summary]]
```

## 解決メカニズム

Obsidian は wikilink `[[<id>]]` を以下の順で解決する:

1. ファイル basename と完全一致
2. Front Matter `aliases` 配列に含まれる値と一致

本 scheme では **(2) で解決**される。全ての markdown が `aliases: [<id>]` を持つためである。ファイル名は既存を維持する（`README.md` は `README.md` のまま変更しない）。

## Front Matter 参照との使い分け

- Front Matter `_id` / `_ids`: **構造的関係**（親子、派生元、対応する Issue 等）
- Body 内 wikilink: **文脈的な参照**（「詳細は [[pj-2026-07-16-a3f2|X]] を参照」等）
- 両者は独立して使い、混同しない

## Cross-repo リンクの扱い

- 第 1 段階ではスコープ外
- 全ての wikilink は same-repo 内で解決する前提
- 将来 cross-repo が必要になった場合、`[[<repo>:<id>]]` のような prefix 記法を検討する（現時点では実装しない）

## CI 検証項目（概要）

- 全 wikilink の id が repo 内に存在する
- セクションリンクのセクション名が対象ファイルの見出しに一致する
- `[[path/*]]` のような path 記法（スラッシュを含む）は禁止し、CI で fail とする

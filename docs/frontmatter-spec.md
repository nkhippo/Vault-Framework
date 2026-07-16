---
title: Front Matter Spec
created: 2026-07-16
status: draft
tags:
- id-scheme
- phase-0.5
id: pj-2026-07-16-bc64
aliases:
- pj-2026-07-16-bc64
---

# Front Matter Spec

## Summary

すべての markdown は、自己識別のための `id` / `aliases` と、人間可読な `title` / `created` を Front Matter に持つ。他ノードへの参照は `_id` / `_ids` サフィックス付きフィールドで行い、path ベースの legacy フィールドより優先する。本文書はその必須項目と migration 時の生成規則の正典である。

## 全 markdown 必須項目

以下 4 項目を全 markdown で必須とする。

```yaml
---
id: <prefix>-YYYY-MM-DD-<4hex>
aliases: [<id と同じ値>]
title: <人間可読の主題>
created: <ISO8601 JST または YYYY-MM-DD>
---
```

- `aliases[0]` は必ず `id` の値と一致する（CI 強制）
- `aliases` は配列。既存 alias がある場合は先頭に `id` を追加し、後続に既存 alias を保持する
- `created` は起票日時。ISO8601 JST（例: `2026-07-16T15:30:00+09:00`）または `YYYY-MM-DD` を許容する

## 参照フィールドの命名原則

- 参照フィールドは必ず `_id` または `_ids` サフィックスを付ける
- 詳細は [[id-scheme#参照フィールド命名規約|ID Scheme の参照フィールド命名規約]] を参照
- Legacy path フィールドと共存する場合、`_id` / `_ids` が第一優先

## 型ごとの推奨追加項目

各 markdown の type（vault の vocabulary で定義）に応じて、以下のような項目を追加する。

- `type`: 文書の種類（vault の vocabulary で定義された値）
- `status`: `draft`, `published`, `archived` 等
- `tags`: 主題を表す tag の配列
- `summary`: 1-2 行の要約
- `updated`: 最終更新日時（ISO8601 JST）

これらは vault の既存 vocabulary に従うため、本文書では詳細を規定しない。

## Migration 時の Front Matter 生成

既存 Front Matter が無いファイル（README、一般 markdown 等）への migration 手順:

- `title`: 先頭 H1 → ファイル名（拡張子除く）の順で fallback
- `created`: git log の初回追加コミット日時 → migration 実行日で fallback
- `id`, `aliases[0]`: `id-scheme.md` の規則で生成

既存 Front Matter がある場合は既存フィールドを維持し、必須項目のみを追加/更新する。

## Legacy path フィールドの扱い

- 既存の path 参照フィールド（`related`, `derived_from`, `source`, `link`, `ref`, `parent` 等）は削除せず残してもよい（運用上の便宜のため）
- ただし、対応する `_id` / `_ids` フィールドが **必ず存在** し、そちらが authoritative とする
- 両者が矛盾した場合は `_id` / `_ids` の値が正
- CI 検証は `_id` / `_ids` フィールドを対象とし、legacy path フィールドの整合性は検証しない

## CI 検証項目（概要）

詳細は `validate-markdown-refs.py` で規定する。概要のみ:

- **V1**: 全 markdown に `id` フィールドが存在し、正規表現に一致する
- **V2**: `aliases[0] == id`
- **V3**: `id` がリポジトリ内でユニーク
- **V4**: 全ての `_id` / `_ids` フィールドの値が有効な ID フォーマット
- **V5**: 全ての `_id` / `_ids` フィールドの参照先が実在する
- **V6**: Body 内の全 wikilink `[[<id>...]]` の id が実在する

---
audience: mixed
created: 2026-07-14T07:00:00+09:00
keywords:
  - frontmatter
  - schema
  - yaml
  - metadata
  - required-fields
  - optional-fields
  - type-specific-fields
  - sensitive
related_adrs: []
status: published
summary: Vault 内の Markdown ファイルの Front Matter スキーマの詳細仕様。必須・任意フィールド、type 別の追加必須フィールド、YAML 記述ルール、バリデーション手順を定義。
tags:
  - spec
  - frontmatter
  - schema
title: Front Matter スキーマ 仕様
type: spec
updated: 2026-07-14T07:00:00+09:00
---

## Summary

Vault 内の Markdown ファイルの Front Matter(YAML メタデータ)の詳細スキーマ。必須・任意フィールド、type 別の追加必須フィールド、YAML 記述ルール、バリデーション手順を定義。00_meta/frontmatter_schema.md の完全版として位置づける。

## Scope

このスペックが規定するもの:

- Front Matter に含めるフィールドの一覧と意味
- 各フィールドの型・値制約
- type ごとの追加必須フィールド
- YAML 記述の細かなルール(quoting、日付形式、配列表記等)
- sensitive フィールドの扱い
- バリデーション手順

このスペックが規定しないもの:

- 統制語彙の設計原則(vocabulary-design.md 参照)
- ファイル名の規約(file-naming.md 参照)

## Front Matter の位置

- ファイルの最上部に配置
- `---` で開始し、`---` で終了する YAML ブロック
- 直後に空行を 1 行入れて本文開始

**例**:

```markdown
---
title: MCP プラットフォーム選定
type: chat_log
status: published
...
---

## Summary

...
```

## Required Fields(全 type 共通)

### `title`

- **型**: string
- **意味**: ファイルの主題を日本語で表現
- **例**: `MCP プラットフォーム選定`
- **制約**: 1 行、最大 100 文字目安
- **例外**: `diary` type は `YYYY-MM-DD` を title に使う

### `created`

- **型**: ISO 8601 datetime with timezone
- **意味**: 初回保存日時
- **例**: `2026-07-13T15:30:00+09:00`
- **タイムゾーン**: JST(`+09:00`)固定

### `updated`

- **型**: ISO 8601 datetime with timezone
- **意味**: 最新更新日時
- **例**: `2026-07-14T02:30:00+09:00`
- **タイムゾーン**: JST(`+09:00`)固定
- **注意**: Vault-MCP の `create_note` / `update_note` が自動的に現在時刻に更新する

### `type`

- **型**: enum(vocabulary.md 参照)
- **意味**: ファイルの種類
- **値**: `chat_log`, `note_draft`, `note_published`, `project_idea`, `project_design`, `knowledge`, `handoff`, `template`, `report`, `spec`, `adr`, `example`, `rejected_alternative`, `diary`, `reflection`, `goal`, `inbox`

### `status`

- **型**: enum
- **意味**: ファイルの状態
- **値(通常)**: `draft`, `wip`, `published`, `archived`
- **値(project_idea 専用)**: `incubating`, `active`, `shelved`, `rejected`
- **値(rejected_alternative)**: `rejected`

## Optional Fields(全 type 共通)

### `tags`

- **型**: array of string
- **意味**: 検索・分類用のタグ
- **例**: `[design-decision, mcp, cloudflare]`
- **制約**: vocabulary.md の定義済み tag を使用

### `summary`

- **型**: string
- **意味**: ファイル内容の 1-3 文要約
- **例**: `MCP プラットフォームを 8 候補から Cloudflare Workers に決定した記録`
- **用途**: 検索時の判定を高速化、Skill が Front Matter だけで内容を把握するため
- **推奨**: 全てのファイルに設定

### `keywords`

- **型**: array of string
- **意味**: 検索キーワード(日英混在可)
- **例**: `[MCP, cloudflare-workers, cold-start, プラットフォーム選定]`
- **用途**: search_by_keyword ツールでのヒット精度向上

### `related`

- **型**: array of wikilink
- **意味**: 関連ファイルへのリンク
- **例**: `["[[../decisions/0002-cloudflare-workers-for-mcp.md]]"]`

### `supersedes`

- **型**: string(ファイル path or wikilink)
- **意味**: このファイルが置き換えた旧ファイル
- **例**: `[[10_chat_logs/2026/07/2026-07-13_early-design.md]]`

### `superseded_by`

- **型**: string
- **意味**: このファイルを置き換えた新ファイル(ADR 番号または wikilink)
- **例**: `"0006"`(ADR 番号)、`"[[../decisions/0006-naming-vault-scheme.md]]"`(wikilink)

### `sensitive`

- **型**: boolean
- **意味**: 他コンテキストでの引用禁止フラグ
- **デフォルト**: `false`(通常 type)、`true`(diary/reflection/goal)
- **効果**:
  - Skill は他 Chat で内容を引用・要約しない
  - 検索結果に含まれても、能動的に読まない
  - 過去 Chat 検索の結果に含まれても、要約対象にしない

## Type 別の追加必須フィールド

### chat_log

- `source_chat_date`: string (YYYY-MM-DD) - Chat が行われた日
- `summary`: string - 内容要約
- 推奨: `related`, `keywords`

### note_draft

- `summary`: string
- 推奨: `target_publish_date`(string、YYYY-MM-DD、公開予定日)

### note_published

- `published_date`: string (YYYY-MM-DD)
- `published_url`: string (URL)
- `summary`: string
- 注意: `sensitive: false` 固定(公開版なのでセンシティブ扱いしない)

### project_idea

- `idea_slug`: string(kebab-case、ディレクトリ名と一致)
- `summary`: string

### project_design

- `project`: string(GitHub リポジトリ名と一致)
- `summary`: string

### knowledge

- `summary`: string
- `tags`: array(推奨、`ai`/`dev`/`english`/`other` 等のカテゴリ)

### handoff

- `project`: string
- `summary`: string
- `one_line_purpose`: string(1 行の目的説明)

### diary

- `date`: string (YYYY-MM-DD)
- `sensitive: true`(自動付与、上書き禁止)
- 任意: `mood`, `energy`, `weather`

### reflection

- `date`: string (YYYY-MM-DD、週次は YYYY-WW)
- `sensitive: true`(自動付与)

### goal

- `sensitive: true`(自動付与)

### spec / adr

- `id`: string(例: `adr-0001`)
- `keywords`: array
- `related_adrs`: array of string
- `related_specs`: array of string
- `related_chats`: array of path
- `summary`: string
- `date`: string(意思決定・策定日)
- `audience`: string(`mixed`、`导入者`、`developer` 等)

### rejected_alternative

- `keywords`: array
- `related_adrs`: array(対応する ADR)
- `superseded_by`: string(採用 ADR の番号)
- `summary`: string
- `date`: string

## Diary / Reflection 専用フィールド(任意)

### mood

- **型**: enum
- **値**: `great`, `good`, `neutral`, `low`, `bad`

### energy

- **型**: enum
- **値**: `high`, `medium`, `low`

### weather

- **型**: string(自由記述)
- **例**: `晴れ`, `曇り時々雨`, `雪`

## YAML 記述ルール

### 基本形式

```yaml
key: value
```

- キーは英小文字 + アンダースコア(`snake_case`)
- 値は文字列、数値、boolean、配列、オブジェクト

### 文字列

- **通常**: quoting なし
- **Special character を含む場合**: double-quote または single-quote
  - コロン、ハイフン先頭、YAML 予約語(`true`, `false`, `null`, `yes`, `no` 等)

```yaml
title: MCP プラットフォーム選定             # quoting なし
description: "Use this skill when..."       # double-quote(内部に : を含むため)
notes: 'It is Naoya''s project'             # single-quote(内部に ' を含む場合はエスケープ)
```

### 配列(リスト)

インライン形式:

```yaml
tags: [design-decision, mcp, cloudflare]
```

ブロック形式:

```yaml
tags:
  - design-decision
  - mcp
  - cloudflare
```

推奨: 短い配列はインライン、長い配列はブロック

### 日付

ISO 8601:

- 日付のみ: `2026-07-13`
- 日時: `2026-07-13T15:30:00+09:00`(必ずタイムゾーン付き)

### null

明示的に null を示す場合:

```yaml
supersedes: null
```

または省略。省略が推奨。

## Body Section Rules

### Summary Section(必須)

Front Matter 直後に H2 `## Summary` セクションを置く:

```markdown
---
...
---

## Summary

<2-4 行の要約>
```

**例外**:

- `diary` type: テンプレの見出し(「今日あったこと」等)で開始、Summary 不要
- `template` type: テンプレファイル自体、Summary 省略可
- 極短の `inbox`: Summary 省略可

### 見出しレベル

- H1(`#`): 使わない(タイトルは Front Matter の `title` で表現)
- H2(`##`): セクション見出し
- H3(`###`): サブセクション
- H4(`####`): さらに細分化

## Validation

### 保存時の自動チェック(Level 1、Skill 実施)

- Front Matter が YAML として parse できる
- 必須フィールドが全て存在する
- type、status、tags が vocabulary.md に登録されている
- 日付が ISO 8601 形式

### 週次バッチチェック(Level 2、Cursor 実施)

- タイポ、余計なスペース、統制語彙外のタグ
- related の wikilink が実在するファイルを指す
- superseded_by の ADR 番号が実在

### 月次チェック(Level 3、Cursor 実施)

- Front Matter スキーマとの整合性(この spec に基づく)
- 廃止 tag が残っていないか
- 新規追加した type が全ファイルに正しく適用されているか

## References

- **関連 ADR**: なし(schema はスペックとして独立)
- **関連 spec**: 
  - [[./vocabulary-design.md]](統制語彙の設計原則)
  - [[./file-naming.md]](ファイル名の規則)
- **実装**: `vault-templates/00_meta/frontmatter_schema.md`(vault 内正典)

## Change Log

- 2026-07-13: 初版(スキーマの詳細確定)
- 2026-07-13: v1.1 で diary/reflection/goal の追加フィールドと sensitive を明示化

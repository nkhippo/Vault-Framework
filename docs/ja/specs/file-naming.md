---
audience: mixed
created: 2026-07-14 06:55:00+09:00
keywords:
- file-naming
- spec
- kebab-case
- date-format
- slug
- directory-naming
- auto-generation
related_adrs:
- '0006'
- '0007'
status: published
summary: Vault 内のファイル名とディレクトリ名の命名規約の詳細仕様。日付形式、スラグ規則、例外パターン、Skill 側の自動生成ロジックを定義。
tags:
- spec
- naming
title: ファイル名規約 仕様
type: spec
updated: 2026-07-14 06:55:00+09:00
id: pj-2026-07-13-5c9b
aliases:
- pj-2026-07-13-5c9b
---

## Summary

Vault 内のファイル名とディレクトリ名の命名規約の詳細仕様。ADR-0006 の命名スキームを補完し、日付形式・スラグ規則・例外パターン・Skill 側の生成ロジックを定義する。

## Scope

このスペックが規定するもの:

- Chat 保存時のファイル名生成ルール
- ディレクトリ名の命名規約
- 日付形式とタイムゾーン
- スラグ(識別子)の作り方
- 例外パターン(README、handoff、diary 等の日付なしファイル)
- Skill 側の自動生成ロジック

このスペックが規定しないもの:

- リポジトリ名の命名(ADR-0006 参照)
- Front Matter の `title` フィールド内容(frontmatter-schema.md 参照)

## Standard Format

### 通常ファイル名

形式: `<日付>_<スラグ>.md`

- **日付**: `YYYY-MM-DD` 形式(ISO 8601 日付部分)
- **区切り**: アンダースコア(`_`)
- **スラグ**: 英小文字 + ハイフン(kebab-case)
- **拡張子**: `.md`

**例**:
- `2026-07-13_vault-system-design-inception.md`
- `2026-07-14_phase31-implementation-report.md`
- `2026-06-30_cursor-instructions-mirroring.md`

### スラグの規則

- **文字セット**: `[a-z0-9-]` のみ(英小文字、数字、ハイフン)
- **長さ**: 30 文字以内(ハード上限 50 文字)
- **語数**: 3-6 語程度
- **命名の意図**: 会話の主題を英語の名詞句で表現
- **禁止**: アンダースコア(`_`)、日本語、大文字、記号

**良いスラグの例**:
- `mcp-platform-selection`
- `vault-structure-restructure`
- `sonnet-standardization`

**悪いスラグの例**:
- `Chat_About_MCP.md`(大文字、アンダースコア)
- `メタ情報検討.md`(日本語)
- `chat.md`(スラグとして情報量ゼロ)
- `discussion-about-the-implementation-details-of-mcp-server-tools-and-authentication-and-deployment.md`(過剰に長い)

## Date Rules

### タイムゾーン

- **JST 固定**: すべての日付は Naoya のタイムゾーン(JST = UTC+9)基準
- **日付境界**: 深夜作業では、その作業のセッションが始まった日を使用
  - 例: 2026-07-13 23:50 に始まった議論が 2026-07-14 01:30 に終わった場合、`2026-07-13_*` を使う

### 日付フィールドの整合

- ファイル名の日付と Front Matter の以下フィールドは一致させる:
  - `created`(初回保存日時)
  - `source_chat_date`(Chat が行われた日、chat_log type の場合)

- ファイル名の日付と Front Matter の `updated` は一致しない(updated は最新編集日時)

## Directory Naming

### トップレベル

形式: `<数字プレフィックス>_<snake_case>`

- **数字プレフィックス**: 2 桁ゼロ埋め、10 刻み
- **区切り**: アンダースコア(`_`)
- **名前**: 英小文字 + アンダースコア(snake_case)
- **拡張子**: なし(ディレクトリ)

**例**:
- `00_meta/`
- `10_chat_logs/`
- `20_notes/`
- `30_projects/`
- `40_knowledge/`
- `50_self/`
- `90_inbox/`

### 中階層

- **年月**: `YYYY/MM/`(0 埋めなし: 7 月は `07`)
- **プロジェクト名**: GitHub リポジトリ名と完全一致(大文字小文字含む)
- **アイデア slug**: `kebab-case`(ファイル名スラグと同じ規則)

**例**:
- `10_chat_logs/2026/07/`
- `30_projects/IPASoundDrill/`(GitHub リポジトリ名と一致)
- `30_projects/_ideas/incubating/pronunciation-video-analyzer/`

## Exceptions

以下のパターンは日付なしファイル名を使う:

### プロジェクトの恒常更新ファイル

- `README.md` - プロジェクト概要
- `design-decisions.md` - 意思決定集約(追記型)
- `open-questions.md` - 未解決論点(追記型)
- `roadmap.md` - ロードマップ

これらは各プロジェクトディレクトリ直下に配置され、日付を含まない。

### handoff/ 配下

- `handoff/current-state.md` - 現状スナップショット(prepend 更新)
- `handoff/recent-changes/YYYY/MM/YYYY-MM-DD_*.md` - 変更履歴詳細(日付あり)

current-state.md は「今の状態」を表すため日付なし。recent-changes/ は履歴のため日付あり。

### diary(50_self/diary/)

- 形式: `50_self/diary/YYYY/MM/YYYY-MM-DD.md`(スラグなし、日付のみ)
- **理由**: 1 日 1 ファイル原則、内容がスラグで簡潔に表現できない

### templates(00_meta/templates/)

- 形式: `<type_name>.md`(例: `chat_log.md`、`diary.md`)
- **理由**: type 名に対応する雛形、日付は無意味

### 特殊ファイル

- `.gitkeep`(空ディレクトリの維持)
- `.editorconfig`
- `LICENSE`
- `CHANGELOG.md`

## Skill's Auto-Generation Logic

Skill `vault-manager` は保存指示を受けた時、以下の順序で名前を生成:

### Step 1: 保存先ディレクトリ判定

保存判断フロー(ADR-0007 の Step 1)で保存先を確定。

### Step 2: ファイル名パターン判定

保存先に応じて以下のパターンを選択:

| 保存先 | ファイル名パターン |
|---|---|
| `10_chat_logs/YYYY/MM/` | `YYYY-MM-DD_kebab-slug.md`(通常) |
| `20_notes/wip/` | `YYYY-MM-DD_kebab-slug.md` |
| `30_projects/<Repo>/logs/YYYY/MM/` | `YYYY-MM-DD_kebab-slug.md` |
| `30_projects/<Repo>/handoff/recent-changes/YYYY/MM/` | `YYYY-MM-DD_kebab-slug.md` |
| `50_self/diary/YYYY/MM/` | `YYYY-MM-DD.md`(スラグなし) |
| `40_knowledge/<category>/` | `YYYY-MM-DD_kebab-slug.md` |
| `90_inbox/` | `YYYY-MM-DD_kebab-slug.md` |

### Step 3: スラグ生成

Chat 主題から英語の名詞句を抽出、以下のルールで正規化:

1. 全て小文字に変換
2. スペースをハイフンに置換
3. 英数字とハイフン以外の文字を削除
4. 30 文字以内にトリミング(単語境界で切る)

### Step 4: 重複チェック

- 生成した名前で `create_note` を呼ぶ
- 同名エラーが返った場合の対応:
  - **diary の場合**: `update_note(mode=append)` に切り替えて追記
  - **通常の場合**: ユーザーに確認(`_v2` 付与や別スラグの候補提案)

## Validation

### 命名規約チェック

保存前および保守運用 Level 1 で以下をチェック:

- ファイル名が正規表現 `^\d{4}-\d{2}-\d{2}_[a-z0-9-]+\.md$` にマッチ(通常ファイル)
- 例外パターンに該当する場合はスキップ(README.md、diary の YYYY-MM-DD.md、handoff/current-state.md 等)

### ディレクトリ名チェック

保守運用 Level 2 で以下をチェック:

- トップレベル: `^\d{2}_[a-z_]+$`
- プロジェクトディレクトリ: 対応する GitHub リポジトリ名と一致(要 GitHub API 参照)

## Edge Cases

### 同日複数保存

同じ日に同じ主題で複数保存する場合:

- **diary**: 追記(update_note mode=append)
- **通常**: 別スラグで新規保存(例: `2026-07-13_mcp-selection-part-2.md`)

### タイムゾーン跨ぎ

- Naoya が海外滞在中の場合も JST 基準(vault の一貫性を優先)
- 現地時間で議論した内容も、Front Matter の created は JST で記録

### 日本語主題を英語スラグに変換

Skill は主題を英語で表現する。日本語で発話された主題も英訳して kebab-case に:

- 「MCP サーバのプラットフォーム選定」→ `mcp-platform-selection`
- 「Vault の 3 層アーキ検討」→ `vault-3-layer-architecture`

## References

- **関連 ADR**: 
  - [[pj-2026-07-13-e13e]](リポジトリ命名)
  - [[pj-2026-07-13-b5c2]](保存先判断)
- **関連 spec**: 
  - [[pj-2026-07-13-9fa5]](Front Matter の title フィールド)
  - [[pj-2026-07-13-c1bd]](handoff/ 配下のファイル名例外)

## Change Log

- 2026-07-13: 初版(命名規約の詳細仕様確定)

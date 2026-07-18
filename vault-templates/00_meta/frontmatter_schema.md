---
created: 2026-07-13 21:44:00+09:00
keywords:
- frontmatter
- schema
- yaml
- metadata
- fields
- required
- optional
- sensitive
status: published
summary: Vault 内の Markdown ファイルの Front Matter スキーマ。必須・任意フィールド、type 別の追加必須フィールド、sensitive
  の扱いを定義。
tags:
- framework
- vault-templates
- meta
- schema
title: Front Matter スキーマ
type: knowledge
updated: 2026-07-13 21:44:00+09:00
---

## Summary

Vault 内のすべての `.md` ファイルの Front Matter スキーマを定義。type / status / tags / project は vocabulary.md で定義された値のみ使用する。

## 必須フィールド

```yaml
---
title: string           # ファイルのタイトル
created: ISO8601        # 例: 2026-07-12T15:30:00+09:00
updated: ISO8601        # 同上
type: enum              # vocabulary.md 参照
status: enum            # vocabulary.md 参照
---
```

## 任意フィールド

```yaml
tags: [string]          # vocabulary.md の語彙から
summary: string         # 1-2 行の要約(検索時のヒット判定を高速化)
keywords: [string]      # 検索用キーワード(日英混在 OK)
related: [wikilink]     # 関連ファイルへのリンク
supersedes: wikilink    # このファイルが置き換えた旧ファイル
superseded_by: wikilink # このファイルを置き換えた新ファイル
sensitive: boolean      # true なら他コンテキストでの引用禁止
```

## type 別の追加必須フィールド

| type | 追加必須 |
|---|---|
| `chat_log` | `source_chat_date`, `summary` |
| `note_draft` | `summary` |
| `note_published` | `published_date`, `published_url`, `summary` |
| `project_idea` | `idea_slug`, `summary` |
| `project_design` | `project`, `summary` |
| `knowledge` | `summary`, `tags` |
| `handoff` | `project`, `summary`, `one_line_purpose` |
| `diary` | `date`, `sensitive: true`(自動付与) |
| `reflection` | `date`, `sensitive: true`(自動付与) |
| `goal` | `sensitive: true`(自動付与) |
| `inbox` | (最小限で可) |

## 昇格関連フィールド(project_idea → project_design 時に付与)

```yaml
promoted_to: wikilink        # 昇格先の README.md へのリンク
promoted_at: ISO8601
promoted_repo: URL           # GitHub リポジトリ URL
```

## diary / reflection 専用フィールド(任意)

```yaml
mood: enum              # great | good | neutral | low | bad
energy: enum            # high | medium | low
weather: string         # 自由記述
```

## 本文冒頭のルール

Front Matter 直後に必ず H2 の Summary セクションを置く:

```markdown
## Summary

このファイルの内容を 2〜4 行で要約する。
Claude が検索結果から取捨選択する際に読むセクション。
```

### 例外

以下 type は Summary セクションを省略可:

- `diary`(テンプレの見出しが「今日あったこと」等で始まる)
- `template`(テンプレファイル自体)
- 極端に短い `inbox` 等

## sensitive フィールドの扱い

`sensitive: true` のファイルは以下の扱いを受ける:

- Skill は他コンテキストで内容を引用・要約しない
- 検索操作で偶然一覧に出た場合も、能動的に読まない
- 過去 Chat 検索の結果に含まれても、要約や引用の対象にしない

50_self/ 配下は原則すべて `sensitive: true`(default)。それ以外でも個人的トピック(健康、家族、財務、感情等)を含む場合は明示的に付与。

## 実装ノート(Vault-MCP 使用時)

Vault-MCP の `create_note` および `update_note` は、Front Matter の `updated` フィールドを自動的に現在時刻に更新する。導入者はこれを前提とした運用を行う。ただし SKILL.md 等の一部ファイルは Claude Skills の parser との互換性のため純粋な形式が求められる場合があり、その場合は手動で `updated` を削除する必要がある。

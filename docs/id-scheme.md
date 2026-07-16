---
title: ID Scheme
created: 2026-07-16
status: draft
tags:
- id-scheme
- phase-0.5
id: pj-2026-07-16-4a20
aliases:
- pj-2026-07-16-4a20
---

# ID Scheme

## Summary

Markdown 間の参照を path ではなく **ID** で結ぶことで、フォルダ再編やファイル移動でもリンクが切れない状態を目指す。ID は各 markdown の Front Matter に持ち、参照側は `_id` / `_ids` サフィックス付きフィールド、または body 内 wikilink で指す。これにより「どこに置かれているか」ではなく「何であるか」が single source of truth になる。

ID には文書種別を表す **4 種の prefix**（`pj` / `nt` / `kn` / `mt`）を付ける。参照フィールドは意味を表す名前に `_id`（単一）または `_ids`（複数）を付ける原則を、リポジトリ横断で永続的に維持する。

## ID 形式

基本形式:

```text
<prefix>-YYYY-MM-DD-<4hex>
```

例:

```text
pj-2026-07-16-a3f2
```

正規表現:

```text
^(pj|nt|kn|mt)-\d{4}-\d{2}-\d{2}-[0-9a-f]{4}$
```

## Type Prefix（4 種）

| Prefix | 対象 | 場所の例 |
|---|---|---|
| `pj-` | project 関連文書全般 | `30_projects/<Repo>/**`, `30_projects/_ideas/**`, `30_projects/_life/**`, `30_projects/<Repo>/logs/**`, および非 Vault repo の全 markdown |
| `nt-` | note（発信物） | `20_notes/wip/**`, `20_notes/published/**` |
| `kn-` | knowledge（汎用ナレッジ・学び、および特定プロジェクトに紐付かない chat_log） | `40_knowledge/**`, `10_chat_logs/**` |
| `mt-` | meta（vault 運営全般、self、skill、template） | `00_meta/**`, `50_self/**` |

## Type Inference（Migration 時の自動推定）

| Path pattern | Prefix |
|---|---|
| `30_projects/<Repo>/logs/**` | `pj-` |
| `30_projects/<Repo>/**`（logs 以外） | `pj-` |
| `30_projects/_ideas/**` | `pj-` |
| `30_projects/_life/**` | `pj-` |
| `20_notes/**` | `nt-` |
| `40_knowledge/**` | `kn-` |
| `10_chat_logs/**` | `kn-` |
| `50_self/**` | `mt-` |
| `00_meta/**` | `mt-` |
| 非 Vault repo の全 markdown | `pj-` |
| 上記に当てはまらない | `mt-` fallback、CSV に列挙して Naoya 確認 |

## 日付部の生成規則

- 起票日を JST（Asia/Tokyo）で `YYYY-MM-DD` 形式にする
- Migration 時は `git log --diff-filter=A --format=%aI -- <file>` で取得した初回追加コミット日時を JST に変換する
- 取得不能な場合は migration 実行日で仮置きする

## Random 部の生成規則

- 4 文字の lowercase hex
- Migration 時は deterministic に生成する:

```python
hashlib.sha256(f"{repo}:{path}:{first_commit_date}".encode()).hexdigest()[:4]
```

- 衝突時は salt を付けて再生成する
- 新規起票時（migration 後の日常運用）は乱数生成し、衝突チェックしてリトライする

## ユニーク性

- リポジトリ内で全 ID がユニークであること
- 将来 cross-repo 検証を導入する場合、全 nkhippo 配下で全 ID がユニークになるよう設計上担保する（現時点では repo 内のみ検証）

## 参照フィールド命名規約

本規約は **最重要かつ永続維持** する。

### 原則

- **自己識別**: `id: <id-value>`（単一）
- **単一参照**: `<意味>_id: <target-id>`
  - 例: `derived_from_id`, `parent_id`, `source_chat_log_id`, `cursor_instruction_id`, `github_issue_id`
- **複数参照**: `<意味>_ids: [<target-id>, ...]`
  - 例: `related_ids`, `children_ids`, `blockers_ids`

### 永続維持の原則

- `_id` / `_ids` サフィックス規約は、リポジトリ追加・プロジェクト追加・その他あらゆる将来変更があっても不変とする
- 参照系フィールドは必ずこのサフィックスで命名する
- 既存の legacy path フィールド（`related`, `derived_from`, `source`, `link`, `ref`, `parent` 等）は運用上残してもよいが、`_id` / `_ids` フィールドが **第一優先の authoritative source** となる
- 両方が存在する場合は `_id` / `_ids` の値が正、legacy path は参考情報として扱う
- CI 検証は `_id` / `_ids` フィールドを対象とし、legacy path フィールドは検証対象外とする

## 参照フィールドの標準例

| フィールド名 | 意味 | 使用場所の例 |
|---|---|---|
| `derived_from_id` | このノードが派生した元のノード | backlog item |
| `parent_id` | 親ノード（汎用） | 階層のあるノード |
| `source_chat_log_id` | 発生源となった chat log | design-decisions, backlog item |
| `cursor_instruction_id` | 対応する Cursor 作業指示書 | backlog item |
| `github_issue_id` | 対応する GitHub Issue の ID | backlog item |
| `related_ids` | 関連ノードの配列 | 汎用 |
| `children_ids` | 子ノードの配列（明示的に持つ場合） | 汎用 |
| `blockers_ids` | ブロッカーの配列 | task-oriented ノード |

新規フィールドは同じサフィックス規約に従って追加する。フィールド名の意味は各文書のスキーマで定義する。

## Broken ID の扱い

- 参照している ID が存在しない場合は CI fail とする
- 自動削除は行わない（データロス防止）
- 修正は Naoya または Cursor が行う
- 移行時に発生した broken は `migration/broken-refs.csv` に記録し、legacy path で残す

---
audience: adopter
keywords:
  - mcp
  - tools
  - api-reference
  - vault-mcp
  - framework
status: draft
summary: Vault-MCP が提供する全 17 ツールの API リファレンス。Read/Write/Issue/Repo の 4 カテゴリで各ツールの目的・パラメータ・戻り値・使用例・注意事項を統一フォーマットで記述。get_file_permissions は未実装 reserved。
tags:
  - framework
  - mcp-server-reference
  - tools
  - reference
title: Vault-MCP ツールリファレンス
type: setup
created: 2026-07-18 14:48:22+09:00
updated: 2026-07-18T15:57:13+09:00
---

Vault-MCP が提供する全ツールの API リファレンス。各ツールについて、目的・パラメータ・戻り値・使用例・注意事項を統一フォーマットで記述する。

## このリファレンスの読み方

各ツールは以下の統一フォーマットで記述される。

**目的**: 1 行で何をするか。
**パラメータ**: 名前・型・必須/オプション・説明の表。
**戻り値**: JSON スキーマまたは説明。
**使用例**: MCP プロトコル(JSON-RPC 2.0)での呼び出し例、または `curl` での動作確認例。
**注意事項**: よくあるミス・エッジケース・関連ツールへの案内。

## ツール一覧(概観)

| カテゴリ | ツール数 | ツール |
|---|---|---|
| Read | 7 | `get_file_content` / `get_frontmatter` / `get_frontmatter_batch` / `get_section` / `list_directory` / `get_project_bundle` / `search_by_keyword` |
| Write | 6 | `create_note` / `update_note` / `delete_note` / `move_note` / `skill_note` / `create_directory` |
| Issue | 3 | `list_issues` / `create_issue` / `add_issue_comment` |
| Repo | 1(+1 reserved) | `list_recent_commits` / (`get_file_permissions` は未実装) |

**実装ツール総数: 17**(Vault-MCP `server.ts` version `1.6.0`)。`tools/list` でこの数が返ることを確認する。

## Read 系

### get_file_content

**目的**: Vault 内の Markdown または他テキストファイルの内容(フロントマター + 本文)を取得する。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `path` | string | ✓ | Vault ルートからの相対パス。例: `00_meta/vocabulary.md` |

**戻り値**:

```json
{
  "path": "00_meta/vocabulary.md",
  "content": "---\ntitle: ...\n---\n\n## Summary\n\n...",
  "sha": "e845d70830272d..."
}
```

- `content` はフロントマター + 本文の全体
- `sha` は GitHub Contents API が返す blob SHA。**後続の `update_note` で楽観ロックに使う**

**使用例**(MCP JSON-RPC):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_file_content",
    "arguments": {"path": "00_meta/vocabulary.md"}
  }
}
```

**注意事項**:

- パスが存在しない場合はエラー(`NOT_FOUND`)を返す。ディレクトリ確認には先に `list_directory` を呼ぶ
- 大きなファイル(200KB 超)は content 全体が返る。フロントマターだけ欲しいなら `get_frontmatter` の方が 5-10 倍高速
- 特定セクションのみ欲しいなら `get_section` を推奨

### get_frontmatter

**目的**: 指定ファイルの Front Matter(パース済み YAML)だけを返す。本文は読まない。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `path` | string | ✓ | Vault ルートからの相対パス。例: `00_meta/README.md` |

**戻り値**:

```json
{
  "path": "00_meta/vocabulary.md",
  "frontmatter": {"title": "...", "type": "knowledge", "status": "published"},
  "sha": "e845d708..."
}
```

**使用例**:

```json
{
  "name": "get_frontmatter",
  "arguments": {"path": "00_meta/vocabulary.md"}
}
```

**注意事項**:

- `get_file_content` より 5-10 倍トークン節約。スキャン・棚卸しはこちらを先に使う
- Front Matter が無いファイルでもエラーにせず、空オブジェクト相当で返す場合がある(実装依存)。無いことが確定したいなら `get_file_content` で確認
- 複数ファイルをまとめて見るなら `get_frontmatter_batch`(最大 20)
- 返り値の `sha` は後続 `update_note` の楽観ロック用に保持しておくとよい

### get_frontmatter_batch

**目的**: 複数パスの Front Matter を並列取得する(1 回あたり最大 20)。Level 2 スキャン向け。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `paths` | string[] | ✓ | Vault 相対パスの配列(1〜20) |
| `include_body_summary` | boolean |   | `true` のとき各ファイルの `## Summary` 本文も返す |

**戻り値**:

```json
{
  "results": [
    {"path": "a.md", "frontmatter": {...}, "sha": "...", "body_summary": "..."},
    {"path": "missing.md", "error": {"code": "NOT_FOUND", "message": "..."}}
  ],
  "errors_count": 1,
  "meta": {"subrequests_used": 2}
}
```

**使用例**:

```json
{
  "name": "get_frontmatter_batch",
  "arguments": {
    "paths": [
      "00_meta/vocabulary.md",
      "00_meta/project_aliases.md",
      "00_meta/vault_index.md"
    ],
    "include_body_summary": true
  }
}
```

**注意事項**:

- 1 パス失敗しても全体は失敗しない。`results[].error` と `errors_count` を見る
- Cloudflare Workers のサブリクエスト予算を消費する。20 件一気より、必要最小限に分ける
- 予算超過時は `SUBREQUEST_BUDGET_EXCEEDED`。paths を減らして再試行
- Skill Level 2 で「同じ順序で呼ぶ」ルールと相性が良い(キャッシュ効率)

### get_section

**目的**: ファイル本文の特定 H2 セクションだけを返す(見出し行は含まない)。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `path` | string | ✓ | Vault 相対パス |
| `section_name` | string | ✓ | H2 見出しテキスト。大文字小文字無視の完全一致。例: `Summary` |

**戻り値**:

```json
{
  "path": "docs/ja/specs/foo.md",
  "section_name": "Summary",
  "content": "このセクションの本文...",
  "sha": "..."
}
```

**使用例**:

```json
{
  "name": "get_section",
  "arguments": {
    "path": "00_meta/project_aliases.md",
    "section_name": "Vault-Framework"
  }
}
```

**注意事項**:

- H2(`##`)のみ対象。H3 以下は親 H2 の一部として返る
- 見出しが見つからないと `NOT_FOUND`。表記ゆれ(全角/半角、末尾スペース)に注意
- 大きい仕様書から「Behavior」だけ取る用途で 3-10x トークン節約
- 内部的にはファイル全体を取得してから抽出する。超巨大ファイルでは `get_file_content` と同コストに近づく

### list_directory

**目的**: Vault 内ディレクトリの直下エントリ(ファイル/ディレクトリ)を一覧する。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `path` | string | ✓ | Vault 相対ディレクトリ。ルートは空文字 `""` |

**戻り値**(概略):

```json
{
  "path": "30_projects",
  "entries": [
    {"name": "Vault-Framework", "type": "dir", "path": "30_projects/Vault-Framework"},
    {"name": "README.md", "type": "file", "path": "30_projects/README.md"}
  ]
}
```

**使用例**:

```json
{
  "name": "list_directory",
  "arguments": {"path": "30_projects"}
}
```

**注意事項**:

- 再帰一覧ではない。深い木は階層ごとに呼ぶか、検索には `search_by_keyword` を使う
- 存在しないパスは `NOT_FOUND`
- GitHub Contents API のディレクトリ一覧制限に依存。巨大ディレクトリでは応答が重い
- 空ディレクトリは Git 上に存在しない(`.gitkeep` がある場合のみ見える)

### get_project_bundle

**目的**: プロジェクト Level 2 参照を 1 コールでまとめて取る(README / design-decisions / open-questions / handoff / instructions / profile Summary / applies_common Summaries)。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `project` | string | ✓ | `00_meta/vocabulary.md` のプロジェクト一覧にある**正確な名前** |

**戻り値**(概略):

```json
{
  "project_root": "30_projects/MyProject",
  "files": {
    "readme": {"path": "...", "content": "...", "sha": "..."},
    "design_decisions": null,
    "open_questions": {...},
    "current_state": {...},
    "project_instructions": {...},
    "naoya_profile": {"path": "00_meta/profile.md", "summary": "..."},
    "applies_common": [{"path": "00_meta/operations/dev_project_common.md", "summary": "..."}]
  },
  "meta": {
    "resolved_at": "2026-07-18T...",
    "subrequests_used": 8,
    "project_valid": true,
    "warnings": []
  }
}
```

**使用例**:

```json
{
  "name": "get_project_bundle",
  "arguments": {"project": "Vault-Framework"}
}
```

**注意事項**:

- vocabulary に無い名前は `NOT_FOUND`。通称ではなく統制語彙の正式名を渡す
- 欠損ファイルは `null` + `warnings`。必須ファイルが無くても全体は成功しうる
- フィールド名 `naoya_profile` は実装上の歴史的命名。中身は `00_meta/profile.md` の Summary
- サブリクエストを多く使う。連続呼び出しはレート/予算に注意

### search_by_keyword

**目的**: Front Matter(`title` / `summary` / `keywords` / `tags`)とファイルパスをキーワード検索する(本文は検索しない)。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `keyword` | string | ✓ | 検索語。大文字小文字無視の部分一致 |
| `path_prefix` | string |   | ディレクトリ接頭辞で範囲制限。例: `30_projects/` |
| `path_pattern` | string |   | glob 風フィルタ。例: `**/wip-*.md` |
| `limit` | number |   | 最大件数(default 20、max 50) |
| `cursor` | string |   | 前回応答の続き読み用カーソル |

**戻り値**(概略):

```json
{
  "results": [
    {
      "path": "10_chat_logs/2026/07/foo.md",
      "title": "...",
      "summary": "...",
      "matched_fields": ["title", "tags"]
    }
  ],
  "next_cursor": null
}
```

**使用例**:

```json
{
  "name": "search_by_keyword",
  "arguments": {
    "keyword": "backlog",
    "path_prefix": "30_projects/Vault-Framework/",
    "limit": 10
  }
}
```

**注意事項**:

- **本文検索はしない**。本文ヒットが必要なら別手段(ローカル grep / 将来拡張)
- KV の FM インデックスがある場合は高速。無い/古い場合は tree 走査にフォールバックし遅い
- `path_prefix` 無しの全 Vault 検索はコスト高。可能な限り絞る
- 週次でインデックス再構築 cron がある実装では、直後の書き込みが検索に遅延反映しうる

## Write 系

### create_note

**目的**: 新規 Markdown ファイルを作成する。既存パスへの上書きは失敗するため、上書きしたい場合は `update_note` を使う。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `path` | string | ✓ | Vault ルートからの相対パス。例: `10_chat_log/2026/07/2026-07-18_topic.md` |
| `frontmatter` | object | ✓ | 構造化フロントマターフィールド(下記参照) |
| `body` | string | ✓ | Markdown 本文(フロントマターを含めない) |
| `commit_message` | string |   | Git commit メッセージ。省略時のデフォルト: `feat: create <path>` |

**frontmatter オブジェクトの必須フィールド**(vault-templates の `frontmatter_schema.md` に準拠):

- `title` / `type` / `status` / `tags` / `summary` は最低限埋めることを推奨
- `id` / `aliases` / `created` / `updated` は Vault-MCP 実装(`ensureTimestamps` 等)がコード固定で自動注入する(env で無効化不可、詳細は `env-vars.md` の該当節)

**戻り値**:

```json
{
  "path": "10_chat_log/2026/07/2026-07-18_topic.md",
  "sha": "abc123...",
  "commit_url": "https://github.com/<owner>/<repo>/commit/xyz789..."
}
```

**使用例**:

```json
{
  "name": "create_note",
  "arguments": {
    "path": "10_chat_log/2026/07/2026-07-18_topic.md",
    "frontmatter": {
      "title": "Chat 議論: トピック名",
      "type": "chat_log",
      "status": "published",
      "tags": ["ai", "design"],
      "summary": "1-2 行の要約"
    },
    "body": "## Summary\n\n本文..."
  }
}
```

**注意事項**:

- 既存パスへ再作成しようとするとエラー。**必ず `update_note` を使う**
- `body` にフロントマター(`---\n...\n---`)を含めない。フロントマターは `frontmatter` パラメータでオブジェクトとして渡す
- 深いパスの中間ディレクトリは自動作成される(GitHub Contents API の挙動)。空ディレクトリを作りたい場合のみ `create_directory`

### update_note

**目的**: 既存 Markdown ファイルを更新する。本文・フロントマター双方に対応、複数のモードで書き換えの粒度を選べる。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `path` | string | ✓ | Vault ルートからの相対パス |
| `content` | string | ✓ | モードに応じた新しいコンテンツ |
| `mode` | enum | ✓ | `replace_body` / `append` / `prepend` / `replace_all` |
| `update_frontmatter` | object |   | 部分的にマージするフロントマターフィールド(`replace_all` 時は無視) |
| `commit_message` | string |   | Git commit メッセージ |

**mode の意味**:

- `replace_body`: 本文のみ差し替え。フロントマターは維持(`update_frontmatter` があればマージ)
- `append`: 現行本文の末尾に `content` を追加
- `prepend`: `## Summary` の前に `content` を挿入
- `replace_all`: フロントマター + 本文の全体を `content` で置き換え。**破壊的、注意**

**戻り値**: `create_note` と同じ形式。

**使用例**(replace_body + フロントマターマージ):

```json
{
  "name": "update_note",
  "arguments": {
    "path": "30_projects/MyProject/handoff/current-state.md",
    "content": "## Summary\n\n最新の状態は...",
    "mode": "replace_body",
    "update_frontmatter": {
      "status": "wip"
    },
    "commit_message": "chore(handoff): current-state を更新"
  }
}
```

`updated` を明示的に指定していないのは、`ensureTimestamps` によりコード側で自動更新されるため。バックデート等の意図がなければ指定不要。

**注意事項**:

- **同一ファイルを 1 セッション内で複数回更新する場合、毎回 `get_file_content` で最新 sha を取り直す**(Vault-MCP 内部で楽観ロックしている場合、古い sha だと 409 Conflict になる)
- `append` は末尾に単に追加するのみ、フロントマターの `updated` は `ensureTimestamps` により自動更新される
- `replace_all` は全内容を投入するため、フロントマター行を `content` に含めること
- SKILL.md ファイルは `skill_note` を使う(`ensureTimestamps` を行わない実装のため)

### delete_note

**目的**: Vault 上のファイルを GitHub Contents API 経由で削除する。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `path` | string | ✓ | 削除する Vault 相対パス |
| `commit_message` | string |   | 省略時 `chore: delete <path>` |

**戻り値**: 削除結果(commit URL 等)。実装は `sha` / `commit_url` を含む。

**使用例**:

```json
{
  "name": "delete_note",
  "arguments": {
    "path": "90_inbox/tmp-scratch.md",
    "commit_message": "chore: remove scratch note"
  }
}
```

**注意事項**:

- **破壊的操作**。Skill ではユーザー確認を取る運用が推奨
- 存在しないパスは `NOT_FOUND`
- FM インデックスからエントリ削除を試みる。KV 失敗しても Git 削除自体は成功しうる(インデックス遅延)
- ディレクトリ削除は非対応。中身を個別削除 + `.gitkeep` 削除が必要

### move_note

**目的**: Markdown ノートを移動/リネームする(先に宛先 create、成功後に元を delete)。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `from` | string | ✓ | 移動元。`.md` で終わること |
| `to` | string | ✓ | 移動先。`.md` で終わること |
| `commit_message` | string |   | 省略時は create/delete それぞれに既定メッセージ |

**戻り値**:

```json
{
  "from": "90_inbox/a.md",
  "to": "40_knowledge/dev/a.md",
  "new_sha": "...",
  "commit_url": "..."
}
```

**使用例**:

```json
{
  "name": "move_note",
  "arguments": {
    "from": "90_inbox/draft.md",
    "to": "20_notes/wip/draft.md"
  }
}
```

**注意事項**:

- **アトミックではない**(create 後に delete)。delete 失敗時は両方残る可能性あり。手動クリーンアップが必要
- 宛先が既にある、または `from === to` は `VALIDATION` エラー
- 履歴上は「移動」ではなく 2 コミットに近い挙動。Git rename 検出は保証されない
- Front Matter の `id` は維持されるが、パス前提の文書内リンクは別途直す

### skill_note

**目的**: `SKILL.md` 専用の create/update。`updated` の自動注入を行わない。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `path` | string | ✓ | 末尾が `SKILL.md` であること |
| `body` | string | ✓ | 本文(フロントマター無し) |
| `frontmatter` | object | ✓ | そのまま書き込む FM。`updated` は自動付与しない |
| `commit_message` | string |   | 省略時 create/update の既定メッセージ |

**戻り値**:

```json
{
  "path": ".../SKILL.md",
  "sha": "...",
  "commit_url": "...",
  "mode": "created"
}
```

`mode` は `created` | `updated`。

**使用例**:

```json
{
  "name": "skill_note",
  "arguments": {
    "path": "30_projects/Vault-Framework/skills/vault-manager/SKILL.md",
    "frontmatter": {
      "name": "vault-manager",
      "description": "…",
      "updated": "2026-07-18T15:00:00+09:00"
    },
    "body": "# Vault Manager\n\n..."
  }
}
```

**注意事項**:

- `create_note` / `update_note` は `ensureTimestamps` で `updated` を自動注入する。**Skill の description 長制約・意図した updated を壊す**ため Skill 書き込みは本ツール必須
- パスが `SKILL.md` で終わらないと `VALIDATION`
- 既存があれば上書き(update)、無ければ create。通常の `create_note` のような「既存で失敗」ではない
- `id` / `aliases` の自動付与もしない(呼び側が必要なら FM に含める)

### create_directory

**目的**: `path/.gitkeep` を書いてディレクトリを作る(GitHub は空ディレクトリを保持できない)。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `path` | string | ✓ | ディレクトリパス。先頭/末尾 `/` 無し |
| `commit_message` | string |   | 省略時 `chore: create directory <path>` |

**戻り値**:

```json
{
  "path": "30_projects/NewProject/logs",
  "gitkeep_path": "30_projects/NewProject/logs/.gitkeep",
  "commit_url": "...",
  "created": true
}
```

既に `.gitkeep` がある場合は `created: false`、`commit_url` は空文字。

**使用例**:

```json
{
  "name": "create_directory",
  "arguments": {"path": "30_projects/NewProject/handoff/recent-changes"}
}
```

**注意事項**:

- **冪等**。何度呼んでも安全
- `create_note` は中間ディレクトリを暗黙作成するため、ノート作成だけなら不要なことが多い
- 空の運用ディレクトリ(logs 等)を先に用意したいときに使う
- パス末尾 `/` は不可

## Issue 系

### list_issues

**目的**: 指定リポジトリの GitHub Issue を一覧する(Pull Request は除外)。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `owner` | string | ✓ | GitHub owner。**MVP は `nkhippo` 固定**(他は拒否) |
| `repo` | string | ✓ | リポジトリ名 |
| `state` | enum |   | `open` / `closed` / `all`(default `open`) |
| `labels` | string[] |   | ラベルフィルタ |
| `limit` | number |   | 1〜100(default 20) |

**戻り値**:

```json
{
  "owner": "nkhippo",
  "repo": "Vault-Framework",
  "state": "open",
  "total": 2,
  "issues": [{"issue_number": 1, "title": "...", "state": "open", "issue_url": "..."}],
  "truncated": false
}
```

**使用例**:

```json
{
  "name": "list_issues",
  "arguments": {
    "owner": "nkhippo",
    "repo": "Vault-Framework",
    "state": "open",
    "limit": 20
  }
}
```

**注意事項**:

- PAT に Issues Read が必要
- MVP の owner 制限は fork 利用者が自アカウントへ緩める改変ポイント(`issue_helpers.ts`)
- GitHub の issues API は PR を含むため、実装側で PR を除外している
- `truncated: true` のときは limit を上げるかページング相当の再取得を検討

### create_issue

**目的**: GitHub Issue を新規起票する。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `owner` | string | ✓ | MVP: `nkhippo` のみ |
| `repo` | string | ✓ | リポジトリ名 |
| `title` | string | ✓ | Issue タイトル |
| `body` | string | ✓ | Markdown 本文 |
| `labels` | string[] |   | ラベル名 |
| `assignees` | string[] |   | 担当者 login |

**戻り値**:

```json
{
  "owner": "nkhippo",
  "repo": "Vault-Framework",
  "issue_number": 42,
  "issue_url": "https://github.com/nkhippo/Vault-Framework/issues/42",
  "title": "...",
  "state": "open",
  "created_at": "..."
}
```

**使用例**:

```json
{
  "name": "create_issue",
  "arguments": {
    "owner": "nkhippo",
    "repo": "Vault-Framework",
    "title": "docs: fix setup typo",
    "body": "## Context\n\n...",
    "labels": ["documentation"]
  }
}
```

**注意事項**:

- Issues Read and write 権限が必要
- Skill では**承認後**に呼ぶ運用(勝手起票禁止)
- プロジェクト専用 MCP コネクタ以外を使わない(混線防止)
- ラベル/assignee がリポジトリに存在しないと GitHub 側で 422 になりうる

### add_issue_comment

**目的**: 既存 Issue にコメントを追加する。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `owner` | string | ✓ | MVP: `nkhippo` のみ |
| `repo` | string | ✓ | リポジトリ名 |
| `issue_number` | number | ✓ | Issue 番号 |
| `comment` | string | ✓ | Markdown コメント本文 |

**戻り値**:

```json
{
  "owner": "nkhippo",
  "repo": "Vault-Framework",
  "issue_number": 42,
  "comment_id": 123456,
  "comment_url": "https://github.com/...#issuecomment-123456",
  "created_at": "..."
}
```

**使用例**:

```json
{
  "name": "add_issue_comment",
  "arguments": {
    "owner": "nkhippo",
    "repo": "Vault-Framework",
    "issue_number": 42,
    "comment": "Vault 側で方針確定。実装に着手します。"
  }
}
```

**注意事項**:

- 存在しない Issue 番号は GitHub 404 → ラップされたエラー
- 長いコメントは GitHub 制限に注意
- Skill では承認ゲート対象
- Issue 本文の編集ではなく**コメント追加**のみ

## Repo 系

### list_recent_commits

**目的**: Vault リポジトリの最近の commit を一覧する。

**パラメータ**:

| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| `limit` | number |   | 1〜100(default 20) |
| `path` | string |   | このパスに触れた commit のみ |

**戻り値**:

```json
{
  "commits": [
    {
      "sha": "abc123...",
      "message": "feat: ...",
      "author": "name",
      "timestamp": "2026-07-18T...",
      "html_url": "https://github.com/..."
    }
  ],
  "meta": {"subrequests_used": 1}
}
```

**使用例**:

```json
{
  "name": "list_recent_commits",
  "arguments": {
    "limit": 10,
    "path": "30_projects/Vault-Framework/skills/"
  }
}
```

**注意事項**:

- `message` は先頭行のみ
- `path` フィルタは GitHub API の path パラメータに依存
- 監査・「誰がいつ変えたか」の確認向け。本文 diff は返さない
- 対象は `GITHUB_OWNER`/`GITHUB_REPO` の Vault。別 repo の commit 一覧は非対応

### get_file_permissions

**目的**(予定): パス単位の権限/可視性メタデータを返す。

**ステータス**: **未実装**(Vault-MCP v1.6.0 の `tools/list` には含まれない)。

初期の Framework 概観表に名前だけ載っていたが、実装リポジトリには `registerTool` が無い。adopter は本ツールを呼び出さないこと。

**代替**:

- リポジトリ権限は GitHub Settings / PAT スコープで管理
- ファイルの存在確認は `get_file_content` / `list_directory`
- 将来実装された場合は本節を更新し、総ツール数を 18 に更新する

---

## 共通のエラーハンドリング

Vault-MCP は下記のエラーコードを返す。全ツール共通。

| コード | 意味 | 対処 |
|---|---|---|
| `NOT_FOUND` | パスが存在しない | パスの確認、または先に `list_directory` |
| `CONFLICT` | sha 不一致(並行更新) | `get_file_content` で最新 sha を取得して再実行 |
| `UNAUTHORIZED` | GitHub PAT の権限不足 | Fine-grained PAT に Contents R/W(または Issues R/W)が付与されているか確認 |
| `RATE_LIMIT` | GitHub API のレート制限 | 一定時間待機して再試行。頻発する場合は PAT の rate limit を確認 |
| `INVALID_ARGUMENT` | パラメータ不正 | エラーメッセージに従って修正 |
| `INTERNAL_ERROR` | サーバ内部エラー | Cloudflare Workers のログを `wrangler tail` で確認 |
| `VALIDATION` / `INVALID_ARGUMENT` | 引数不正 | スキーマ(必須・型・owner 制限等)を確認 |
| `ALREADY_EXISTS` | 既存パスへの create | `update_note` / `skill_note` / 別パスを使う |
| `SUBREQUEST_BUDGET_EXCEEDED` | Workers サブリクエスト上限 | batch の paths を減らす、呼び出しを分割 |
| `GITHUB_RATE_LIMIT` / `RATE_LIMIT` | GitHub API 制限 | 待機後リトライ。PAT の残り quota を確認 |

## 認証

全ツール呼び出しには `Authorization: Bearer <MCP_ACCESS_TOKEN>` ヘッダが必要(MCP コネクタが自動付与)。

詳細は `env-vars.md` を参照。

## 関連

- 環境変数: `env-vars.md`
- 拡張ガイド: `extending.md`
- deploy 手順: `docs/ja/setup/02-deploy-mcp-server.md`

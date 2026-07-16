---
title: FM value wikilink-bracket wrapping (Vault Batch 5 findings)
created: 2026-07-17
status: published
tags: [id-scheme, phase-0.5, troubleshooting, frontmatter]
---

# FM value `[[]]` wrapping (2026-07-17)

Vault Batch 5（PR #6, main `@ f8e1d6d`）で broken 160 件中 **135 件が frontmatter パターン**だった原因の記録。

## 症状

`04_rewrite_refs.py` が FM path キー（`related`, `derived_from`, `source`, `link`, `ref`, `parent`）を解決するとき、値が Obsidian 記法のまま格納されていると `target_not_found` になる。

Vault 実測（`migration/broken-refs.csv`）:

| | |
|---|---|
| FM broken | 135 / 160 |
| 書式 | 全件 `"[[path.md]]"`（section/alias なし） |
| 主フィールド | `related` |
| `50_self/` source | 0 |

### 実例（50_self/ 除外）

```yaml
related:
  - "[[30_projects/Vault/handoff/current-state.md]]"
  - "[[10_chat_logs/2026/07/2026-07-13_vault-system-design-inception-to-completion.md]]"
```

現行 resolver は `[[30_projects/...]]` をそのまま path として扱い、index に存在しないため失敗する。

## 根本原因

1. Vault（Obsidian native）は FM 参照を **wikilink ラップ済み文字列**で持つ運用がある
2. `rewrite_frontmatter` は bare path / markdown_link 想定で、ラップ剥離をしていなかった
3. `looks_like_path` は `.md` 部分一致でラップ値も「path っぽい」と判定 → broken に積む

## 修正（本 revision）

`strip_wikilink_wrapping()` を FM 解決前に適用:

| Input | Output |
|---|---|
| `[[path.md]]` | `path.md` |
| `[[path.md\|display]]` | `path.md` |
| `[[path.md#sec]]` | `path.md` |
| `[[path.md#sec\|display]]` | `path.md` |
| `  [[path]]  ` | `path.md`（拡張子補完） |

加えて **idempotency**: 既に `{key}_id` / `{key}_ids` があるキーは skip（Vault 再実行で成功済み FM を壊さない）。

## Fixture

`tests/fixtures/vault-fm-brackets/` — 上記パターンの代表 8 ファイル。

## 関連

- Vault Batch 5: `nkhippo/Vault#6`
- Scripts pin at Batch 5: Vault-Framework `@ 72bb57b`
- 次作業: 本 fix マージ後に Vault で 04 再実行し broken 削減

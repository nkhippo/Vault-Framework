---
title: Migration Runbook
created: 2026-07-16
status: draft
tags:
- id-scheme
- phase-0.5
id: pj-2026-07-16-9364
aliases:
- pj-2026-07-16-9364
---

# Migration Runbook

## Summary

各リポジトリで migration スクリプトを実行し、path ベースの参照を wikilink ID 参照へ一斉変換する手順を定める。スクリプト本体は `Vault-Framework/scripts/migration/` に配置される予定（別 PR）。本文書はプロセスと期待値のみを規定する。

## 前提

- `Vault-Framework/scripts/migration/` に 6 本の Python スクリプトが存在する
- Python 3.11+、PyYAML がインストール済みである
- Naoya の GitHub アクセス権限で PR 作成が可能である

## スクリプト構成（概要）

以下 6 スクリプトを順に実行する。詳細仕様は各スクリプトの docstring と、scripts の PR で追加される文書を参照する。

| スクリプト | 役割 |
|---|---|
| `01_scan.py` | 全 markdown をスキャンし、対象リストと初期メタを `migration/scan.jsonl` に出力 |
| `02_assign_ids.py` | 各ファイルに ID を生成し、Front Matter に `id` / `aliases` を追加 |
| `03_build_index.py` | path → id の完全マッピングを `migration/index.json` に構築 |
| `04_rewrite_refs.py` | Path ref を wikilink ID ref に書き換え。Front Matter の legacy path フィールドがある場合、対応する `_id` / `_ids` を追加（legacy path は残す） |
| `05_verify.py` | 検証（全 ID ユニーク、全 wikilink resolvable、path ref 残存ゼロ、`_id`/`_ids` 参照先実在） |
| `06_report.py` | `migration/report-YYYY-MM-DD.md` を生成 |

### `04_rewrite_refs.py` の path 解決順序

Path / path-wikilink の解決は次の順で最初に index に当たったものを採用する:

1. **absolute**（先頭 `/`）— repo-root からの絶対 path
2. **vault-root** — 先頭スラッシュなしの path を repo-root から解決（Obsidian 標準の vault 起点記法）
3. **file-relative** — 参照元ファイルの親ディレクトリからの相対 path
4. **basename** — 拡張子込み basename が index 内で一意なら採用。複数候補は `ambiguous_target`

Fenced code（\`\`\` / \`\`\`\` 等）内の参照は書き換えない。閉じフェンスは info string を許容しない（CommonMark 風）。4-space indented block は fence 対象外。

### Known issues resolved（2026-07-17 / Phase 0.5B revision）

Batch 4（ThinkGrindAi）で判明し、本 revision で修正済み:

| 問題 | 修正 |
|---|---|
| `split_fenced_regions` が info string 付き行で誤クローズ | 閉じは同じ文字 ≥N かつ info なしのみ |
| Vault-root 風 `[[docs/foo.md]]` が file-relative のみで `target_not_found` | 上記 4 段階解決 |
| V8 が同じ誤 fence 判定で偽陰性 | 共有 `split_fenced_regions` 修正で解消 |

**注:** ThinkGrindAi `docs/setup/OBSIDIAN_SETUP.md` の残存 path wikilink 5 件は、調査の結果 **例示用 \`\`\`markdown フェンス内**であり、正しい判定では書き換え対象外。実リンクとして直す場合は指示書 9 でテンプレ本文側を別途扱う。

## リポジトリごとの実行手順

1. 対象リポジトリの最新 `main`（または `master`）を取得する
2. 新規ブランチ作成: `chore/migrate-to-id-refs-YYYY-MM-DD`
3. `Vault-Framework/scripts/migration/` から最新スクリプトを取得し、対象リポジトリの `scripts/migration/` にコピーする（手動または `curl` で raw URL 取得）
4. スクリプト先頭に `# Source: Vault-Framework/scripts/migration/xxx.py @ <commit-sha>` コメントを追加する
5. `python scripts/migration/01_scan.py` から順に実行する
6. `05_verify.py` が全 PASS することを確認する
7. Commit を 3 つに分ける:
   - `feat: add id/aliases frontmatter to all markdown`（02 の結果）
   - `chore: rewrite path refs to wikilink id refs`（04 の結果）
   - `chore: add migration scripts and report`（script / report / broken-refs 追加）
8. PR タイトル: `chore: migrate markdown refs from path to wikilink id`
9. PR 本文に `06_report.py` が生成した Summary + Verification 結果 + broken-refs 件数を含める

## Broken ref の扱い

- 参照先が見つからない path ref は書き換えず、元の path のまま残す
- `migration/broken-refs.csv` に `(source_file, line, referenced_path, reason)` を記録する
- Reason 例: `target_not_found`, `outside_repo`, `ambiguous_target`
- V5/V6 検証は `broken-refs.csv` 記載分を除外する
- PR に `broken-refs.csv` を含めて Naoya がレビューする
- Broken ref は CI hook でホワイトリスト化し、後日 Naoya 判断で手動修正する

## Migration 履歴の永続保管

各リポジトリの migration 完了後、以下を Vault-Framework に集約する:

- 配置: `Vault-Framework/migration-history/<repo>-YYYY-MM-DD.jsonl`
- 内容: `{path, id, first_commit_date}` の JSONL（全ファイル分）
- 目的: 「昔ここにあったファイル、今どの ID?」を後から追える historical record として

集約方法は別途 Cursor 作業として実施する（本 runbook のスコープ外）。

## Deterministic 保証と再実行

- Migration スクリプトは deterministic に設計されている（ID 割り当てが hash ベース）
- 中断してもやり直し可能（同じリポジトリで再実行すると同じ ID になる）
- 各スクリプトは `--dry-run` オプションを持つ（実行前に変更内容を確認可能）

## 実行順序（全リポジトリ）

1. `Vault-Framework` を最初に実施（本体を確定させてから展開）
2. その他 10 リポジトリ（IPASoundDrill, ThinkGrindAi, English-* 系, Vault-MCP, ipasounddrill-mcp）
3. `Vault` を最後に実施

## 完了条件

- 対象リポジトリで PR 作成され、`05_verify.py` の全 PASS が PR 本文で確認できる
- 3 コミット構成で PR が構成されている
- `broken-refs.csv`、`migration/report-YYYY-MM-DD.md`、scripts が PR に含まれる

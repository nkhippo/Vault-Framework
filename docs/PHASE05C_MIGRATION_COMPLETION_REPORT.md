---
title: Vault-Framework migration 完了レポート (Phase 0.5C)
title_en: Vault-Framework Migration Completion Report (Phase 0.5C)
type: report
audience: mixed
status: published
date: 2026-07-16
keywords:
- id-scheme
- migration
- phase-0.5c
- wikilink
- ci
- report
summary: 2026-07-16_cursor-instruction-3_vault-framework-migration.md の実行結果。
  Vault-Framework 自身への path→wikilink ID 移行と CI 有効化を PR #4 で main にマージ。
id: pj-2026-07-16-9c88
aliases:
- pj-2026-07-16-9c88
---

# Vault-Framework migration 完了レポート (Phase 0.5C)

**対象リポジトリ**: [nkhippo/Vault-Framework](https://github.com/nkhippo/Vault-Framework)  
**指示書**: `2026-07-16_cursor-instruction-3_vault-framework-migration.md`  
**実行日**: 2026-07-16  
**実行者**: Cursor (Composer)  
**PR**: [#4](https://github.com/nkhippo/Vault-Framework/pull/4) (merged)  
**Merge commit**: `04ab894`  
**Branch**: `chore/migrate-to-id-refs-2026-07-16`

---

## 1. 完了判定

| 条件 | 結果 |
|---|---|
| Steps 1–9 (scan → assign → index → rewrite → verify → report → CI) | ✅ |
| `05_verify.py` exit 0 / V1–V8 PASS | ✅ |
| `migration/report-2026-07-16.md` 生成 | ✅ |
| `.github/workflows/validate-markdown-refs.yml` 配置 | ✅ |
| PR 作成・main マージ push | ✅ PR #4 |

---

## 2. Migration 結果サマリ

| 項目 | 値 |
|---|---|
| Markdown files | 158 |
| IDs assigned | 158 (added_fm 2 / updated_fm 156 / skipped 0) |
| Prefix | `pj-` 100% |
| Refs rewritten | 319 |
| Broken refs (whitelist) | 42 (all `target_not_found`) |
| Verify | V1–V8 PASS |

詳細: `migration/report-2026-07-16.md`

### Dry-run 02

- Total 158 / pj 158 (100%) / skipped 0
- Legacy `adr-NNNN` は scheme 非準拠のため **置換**し、legacy 値は `aliases` に保持（下記 tooling fix）

### Dry-run 04

- Detected 361 (audit expected ~363)
- Rewrites: markdown_link 176 / wikilink 143 / frontmatter 0
- Broken 42 (11.6% — 10% advisory gate 超過だが、欠落 EN パス・placeholder・誤 relative のみのため本実行継続)

### Broken refs 内訳

| reason | count |
|---|---|
| target_not_found | 42 |
| outside_repo | 0 |
| ambiguous_target | 0 |

代表例: EN ADR → 未翻訳 `rejected-alternatives/`、EN backbone → 欠落 `docs/en/specs/`、`path/to/file.md`、誤った `../decisions/`。手動修正は後続（指示書どおり対象外）。

---

## 3. コミット構成

指示書の 4 コミットに加え、実行中の tooling / docs fix を含む。

| SHA | Message |
|---|---|
| `a844adf` | fix(migration): replace legacy non-scheme id instead of skipping |
| `0604aaf` | feat: add id/aliases frontmatter to all markdown |
| `91a9d13` | fix(migration): exclude migration/ and audit/ from markdown scans |
| `ded8119` | chore: rewrite path refs to wikilink id refs |
| `6ebc739` | fix(docs): use real id in wikilink-conventions examples for V6 |
| `520cb8f` | chore: add migration artifacts |
| `62879b9` | ci: enable validate-markdown-refs workflow |
| `04ab894` | Merge pull request #4 |

### Tooling / docs fixes の理由

1. **legacy ADR id**: `02_assign_ids` が scheme 非準拠 id を skip すると ≥5 skip で中断。置換 + aliases 保持に変更。
2. **EXCLUDE_DIRS**: `migration/` dry-run 成果物を scan 対象外に（id なし md で 03 が失敗）。
3. **wikilink-conventions 例示 id**: 架空 `pj-2026-07-16-a3f2` が V6 で FAIL → 実 id `pj-2026-07-16-8def` に置換。

---

## 4. CI

- 配置: `.github/workflows/validate-markdown-refs.yml`（templates から copy、templates は残置）
- PR / push(main) で `validate-markdown-refs.py` 実行
- Whitelist: `migration/broken-refs.csv`

---

## 5. Claude 向け確認ポイント

1. `migration/verify-report.jsonl` — 全行 PASS
2. `migration/broken-refs.csv` — 42 件が妥当か（欠落翻訳・placeholder）
3. サンプル md の FM に `id` / `aliases` があること
4. Body の path markdown link / path wikilink が ID ベース wikilink になっていること
5. `.github/workflows/validate-markdown-refs.yml` が存在すること
6. main tip が merge `04ab894`（またはその後の本レポート commit）であること

---

## 6. Sequence

- Phase 0.5A docs — PR #2 ✅
- Phase 0.5B scripts — PR #3 ✅
- **Phase 0.5C Framework 自身 migration + CI** — PR #4 ✅
- 次: Phase 0.5D–F（他 repo / Vault 本体）

---

## 7. 環境メモ

- Python: Homebrew `python@3.11` (`/opt/homebrew/opt/python@3.11/bin/python3.11`)
- PyYAML: インストール済み
- System python 3.9.6 は未使用

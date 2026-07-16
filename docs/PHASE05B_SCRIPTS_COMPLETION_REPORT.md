---
title: Vault-Framework scripts 完了レポート (Phase 0.5B)
title_en: Vault-Framework Scripts Completion Report (Phase 0.5B)
type: report
audience: mixed
status: published
date: 2026-07-16
keywords: [id-scheme, migration, scripts, phase-0.5b, report]
summary: 2026-07-16_cursor-instruction-2_vault-framework-scripts.md の実行結果。migration 6 + validate 1 + workflow 1 を PR #3 で main にマージ済み。
---

# Vault-Framework scripts 完了レポート (Phase 0.5B)

**対象リポジトリ**: [nkhippo/Vault-Framework](https://github.com/nkhippo/Vault-Framework)  
**指示書**: `2026-07-16_cursor-instruction-2_vault-framework-scripts.md`  
**実行日**: 2026-07-16  
**実行者**: Cursor (Composer)  
**PR**: [#3](https://github.com/nkhippo/Vault-Framework/pull/3) (merged)  
**Merge commit**: `fdfdb3a`

---

## 1. 完了判定

| 条件 | 結果 |
|---|---|
| 8 ファイル配置 | ✅ (+ `scripts/lib/` 共有 3 ファイル) |
| 各スクリプト `--help` 実行可 | ✅ |
| docstring / type hint | ✅ |
| 2 コミット構成の PR | ✅ |
| `main` へマージ push | ✅ PR #3 merge |

---

## 2. 追加ファイル

### Migration (`scripts/migration/`)

| ファイル | 役割 |
|---|---|
| `01_scan.py` | 全 md スキャン → `migration/scan.jsonl` |
| `02_assign_ids.py` | ID 生成 & Front Matter 更新 (`--dry-run`) |
| `03_build_index.py` | `index.json` / `index-reverse.json` |
| `04_rewrite_refs.py` | path ref → wikilink ID (`--dry-run`) |
| `05_verify.py` | V1–V8 総合検証 |
| `06_report.py` | 人間可読 report markdown |

### Shared lib (`scripts/lib/`)

| ファイル | 役割 |
|---|---|
| `common.py` | 除外 dir、FM パース、`infer_prefix`、CLI 共通 |
| `verify_core.py` | V1–V8（05 / validate 共有） |
| `__init__.py` | パッケージ初期化 |

### Validate / Workflow

| ファイル | 役割 |
|---|---|
| `scripts/validate/validate-markdown-refs.py` | CI 継続検証（PR / full-scan） |
| `templates/github-workflows/validate-markdown-refs.yml` | GHA テンプレ |

---

## 3. コミット SHA

| SHA | Message |
|---|---|
| `14ef9bf` | feat: add migration scripts (01-06) |
| `8a882b5` | feat: add validate script and workflow template |
| `fdfdb3a` | Merge pull request #3 from nkhippo/feat/id-scheme-scripts |

---

## 4. スモークテスト

```
python3 scripts/migration/01_scan.py --help        # OK (他 6 本も同様)
python3 scripts/migration/01_scan.py --repo-root .
# -> wrote 157 rows -> migration/scan.jsonl (ローカル /tmp で確認、repo 未コミット)
```

**未実施（指示書どおり対象外）**: Vault-Framework 自身への migration 実行（Phase 0.5C）

---

## 5. 実装メモ

- 外部依存: **PyYAML のみ**
- Path: POSIX 統一、`infer_prefix` は非 Vault repo → 常に `pj`
- `01_scan`: YAML `date` オブジェクトは `json_safe` で ISO 文字列化
- `validate`: `migration/broken-refs.csv` 欠落時は空ホワイトリスト
- Source ヘッダーは placeholder `@ <commit-sha will be filled by caller>` のまま

---

## 6. Follow-up (Phase 0.5C)

- Vault-Framework 自身で `01`→`06` を実行
- broken-refs レビュー
- workflow テンプレを `.github/workflows/` へ展開（別判断）

---

**End of PHASE05B_SCRIPTS_COMPLETION_REPORT.md**

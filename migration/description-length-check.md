# SKILL.md Description Length Check

実行日: 2026-07-17 (JST)

Anthropic Skills `description` 上限: **1024 文字**  
運用目標: **800 文字未満**(将来の追加余地)

## Before

| File | Length | Status |
|---|---|---|
| `skills/vault-manager/SKILL.md` | 1428 | **OVER** |
| `skills/vault-maintainer/SKILL.md` | 867 | &gt;800 運用目標 |

## After vault-manager (Commit 1)

| File | Length | Status |
|---|---|---|
| `skills/vault-manager/SKILL.md` | 266 | OK |

## Root cause

Phase 0.6 / 1c / 1d PR-A で `description` にトリガー phrase を累積追加。詳細は body 参照。

---
id: pj-2026-07-17-19a5
aliases:
- pj-2026-07-17-19a5
title: SKILL.md Description Length Check
type: report
status: published
created: 2026-07-17T03:00:00+09:00
summary: Anthropic Skills description 1024-char 上限チェック記録。vault-manager / vault-maintainer 圧縮前後の文字数。
---

# SKILL.md Description Length Check

実行日: 2026-07-17 (JST)

Anthropic Skills `description` 上限: **1024 文字**  
運用目標: **800 文字未満**(将来の追加余地)

## Before (Phase 1d PR-B 時点)

| File | Length | Status |
|---|---|---|
| `skills/vault-manager/SKILL.md` | 1428 | **OVER** (upload 失敗) |
| `skills/vault-maintainer/SKILL.md` | 867 | OK (&lt;1024) but &gt;800 運用目標 |

## After fix

| File | Before | After | Status |
|---|---|---|---|
| `skills/vault-manager/SKILL.md` | 1428 | 266 | OK |
| `skills/vault-maintainer/SKILL.md` | 867 | 228 | OK |

## Root cause

Phase 0.6 / 1c / 1d PR-A で `description` にトリガー phrase を累積追加し 1024 超過。詳細は body の workflow セクションに既存。修正は `description` のみ、body unchanged。

## Follow-up fix (2026-07-17): dual frontmatter merge

- `skills/vault-maintainer/SKILL.md`: 2 frontmatter blocks → merged to 1
- Root cause: Anthropic Skills parser が第 2 frontmatter を body 内 YAML として誤解釈
- Fix: `name` / `description` を第 1 frontmatter に merge、第 2 ブロック削除
- description length: 228 chars(維持)
- Body unchanged

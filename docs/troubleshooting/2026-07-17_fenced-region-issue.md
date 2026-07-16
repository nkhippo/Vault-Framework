---
title: Fenced-region and vault-root path issues (Batch 4 findings)
created: 2026-07-17
status: draft
tags: [id-scheme, phase-0.5, troubleshooting]
---

# Fenced-region / vault-root path issues (2026-07-17)

Batch 4（ThinkGrindAi）で観測された script 限界の根本原因調査メモ。

## Issue 1: `split_fenced_regions` と OBSIDIAN_SETUP wikilink 5 件

### 当初の症状

`docs/setup/OBSIDIAN_SETUP.md` の path wikilink 5 件が `in_code=True` となり rewrite されない。

### 調査結果（重要）

CommonMark 相当の fence 追跡で再評価すると、**当該 5 件はいずれも ` ```markdown ` のコードフェンス例示ブロック内**にある。

| 残存 wikilink | 所属 |
|---|---|
| `[[docs/requirements-thinking.md]]` 等 3 件 | REQ テンプレ例示フェンス内（「リンク・参考」セクションのサンプル） |
| `[[ideas/REQ-001-thinking.md]]` | Claude 議論テンプレ例示フェンス内 |
| `[[docs/specification-thinking.md]]` | 「リンク記法」説明の ` ```markdown ` 例示内 |

つまり Batch 4 レポートの「誤判定」は、**例示コード内の path を実リンクと見なした監査側の解釈**に近い。正しい fence 判定ではこれらは引き続き in_code になるのが妥当。

### それでも直すべき実バグ

`split_fenced_regions` には以下の実害がある:

1. **閉じフェンスが info string を許容**  
   `startswith("```")` のため、フェンス内の ` ```javascript ` 行が外側 ` ```markdown ` を誤って閉じる。
2. **インデント 4 スペース / タブを常に code 扱い**  
   指示書どおり indented code block は対象外とする（Obsidian 文書で誤爆しやすい）。
3. **開きフェンスの marker 長を 3 固定**  
   4 本以上のバッククォート開きに対し、閉じ条件が不正確。

## Issue 2: Vault-root path 解決

`[[docs/foo.md]]` を参照元 `docs/setup/x.md` から見ると、現行実装は `docs/setup/docs/foo.md` へ相対解決し `target_not_found`。

Obsidian では vault-root 起点の path が一般的。解決順を次に変更する:

1. absolute (`/docs/foo.md`)
2. vault-root (`docs/foo.md` を repo-root から)
3. file-relative（現行）
4. basename 一意マッチ

## Issue 3: V8 偽陰性

V8 は `split_fenced_regions` + `offset_in_code` を共有。Issue 1 の閉じ誤検出が直れば、フェンス外に残った path wikilink は検出できるようになる。

例示フェンス内の 5 件は **V8 でもスキップが正しい**（コード例を壊さない）。Batch 5 前に必要なのは「フェンス外の残存を落とさない」こと。

## 修正方針サマリ

| 項目 | 方針 |
|---|---|
| Fence | CommonMark 風: 行頭（最大 3 スペース）+ N≥3 backticks/tildes、閉じは同じ文字で ≥N かつ info string なし |
| Indented | 対象外（code にしない） |
| Path | absolute → vault-root → relative → basename |
| V8 | 共有 `split_fenced_regions` を使用し続け、false negative を潰す |

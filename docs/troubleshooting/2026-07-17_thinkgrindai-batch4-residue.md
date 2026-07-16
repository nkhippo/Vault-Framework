---
title: ThinkGrindAi Batch 4 残債の記録(Option α2 保留分)
created: 2026-07-17
status: published
tags: [troubleshooting, migration, thinkgrindai, phase-0.5, deferred]
---

# ThinkGrindAi Batch 4 残債の記録

## 背景

Phase 0.5D Batch 4(2026-07-17)で ThinkGrindAi(56 refs)を migration。
その後 PR #5(scripts revision)により fenced-region 誤判定・Vault-root path 解決を修正したが、
ThinkGrindAi は「Option α2」に基づき **再 migration せず**とする方針を採用。

本文書は残債 16 件(例示 5 + 本質的 broken 11)の記録と、後日対応判断の材料。

## 残債 1: OBSIDIAN_SETUP.md 内の例示 wikilink 5 件

### 概要

`docs/setup/OBSIDIAN_SETUP.md` の ` ```markdown ` フェンス内に 5 件の wikilink が存在。
これらは **Obsidian 設定手順の例示コード** であり、rewrite 対象外が正しい。

### 対象一覧

| Line | Content | Reason for skip |
|---|---|---|
| 151 | `[[docs/requirements-thinking.md]]` | 例示フェンス内 |
| 152 | `[[docs/specification-thinking.md]]` | 例示フェンス内 |
| 153 | `[[docs/cursor-instructions/cursor_instruction_thinking_v2.md]]` | 例示フェンス内 |
| 184 | `[[ideas/REQ-001-thinking.md]]` | 例示フェンス内 |
| 473 | `[[docs/specification-thinking.md]]` | 例示フェンス内 |

### 対応方針

**変更不要**。PR #5 修正後の `split_fenced_regions` は正しくフェンス内と判定し skip する。
V8 spot check でも「意図した skip」として PASS。

将来的に本ファイルの内容を更新して例示以外に本文リンクを追加する場合、
本文側に実 wikilink `[[<id>|display]]` を書けば V8 で検出・保護される。

## 残債 2: 本質的 broken 11 件(target_not_found)

### 概要

Batch 4 の migration で `target_not_found` として broken 判定された 11 件。
主に `.github/wiki/` からの `../CLAUDE.md` 等、**repo 外への参照**が原因。
Script 修正では解消不能(参照先が repo 外に実在しないため)。

### 上位 location

- `.github/wiki/`: 多数(`../CLAUDE.md`, `../docs/PROJECT_CONTEXT.md`)
- `docs/setup/`: 少数
- `legacy/js/`: 少数

### 対応方針

**優先度低、後日 Naoya 個別判断**。オプション:
1. `.github/wiki/` の該当ファイルを削除 or 修正(参照先を実在ファイルに変える)
2. 参照先が `.github/wiki/` の姉妹ページなら、そのページを migration 対象に含めて再判定
3. 意図的な dead link なら現状維持

### 詳細一覧

`ThinkGrindAi/migration/broken-refs.csv` を参照。

## 後日対応の指針

- 本残債は Phase 0.5 完了後の後続作業として位置付け
- Naoya が個別 review のタイミングで判断
- 対応時は Vault-Framework の migration scripts を再利用可能(pin は最新 main)
- 対応 PR は独立に切り、本 doc の該当セクションを "resolved" として更新

## 関連

- 元 PR: `nkhippo/ThinkGrindAi#372`(Batch 4 merge、Phase 0.5D)
- Scripts revision: `nkhippo/Vault-Framework#5`(PR #5, Phase 0.5B revision)
- FM strip fix: `nkhippo/Vault-Framework#6`(PR #6)
- 意思決定: Option α2(2026-07-17、Vault-Framework main 直行)

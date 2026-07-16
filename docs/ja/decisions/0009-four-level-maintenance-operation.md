---
audience: mixed
created: 2026-07-14 04:45:00+09:00
date: 2026-07-13
id: pj-2026-07-13-48bc
keywords:
- maintenance
- four-level
- level-1
- level-2
- level-3
- level-4
- abstract-generation
- cadence
related_adrs:
- '0003'
- 0008
- '0011'
related_chats:
- 10_chat_logs/2026/07/2026-07-13_maintenance-operation-design.md
related_specs:
- maintenance-four-levels
- abstract-generation
status: accepted
summary: Vault の保守運用を 4 レベル(日常発火 / 週次補正 / 月次補正 / 季節補正)に分類し、抽象生成を並行運用として独立管理した意思決定。頃度・担当・介入コストを明確化。
superseded_by: null
supersedes: null
tags:
- adr
- maintenance
- important
title: 'ADR-0009: 保守運用 4 レベル + 抽象生成の並行運用'
type: adr
updated: 2026-07-14 04:45:00+09:00
aliases:
- pj-2026-07-13-48bc
- adr-0009
---

## Summary

Vault の保守運用を 4 レベルに分類し(Level 1 日常発火 / Level 2 週次補正 / Level 3 月次補正 / Level 4 季節補正)、さらに具体的な chat_log から抽象的な spec / ADR を生成する「抽象生成」を並行運用として位置づけた意思決定。頻度・担当・介入コストを明確化。

## Context

Vault の保守運用について、以下の暗黙的な運用が並行して発生していた:

- Chat 保存時の自動チェック(統制語彙違反、Front Matter 欠如)
- 週次・月次で気がついた時のクリーンアップ
- Chat_log から得られた学びを spec や ADR として抽出する作業

これらを体系化しないと、以下の問題が発生する:

- 「今この作業はどのレベルの保守か?」の判断がぶれる
- 保守作業のコスト見積もりが困難
- 導入者(Framework 経由)に運用方針を伝えられない
- Skill と Cursor の役割分担が曖昧

同時に、Cursor 委譲判定(ADR-0008)との整合を取る必要があった。

## Decision

**保守運用を 4 レベルに分類し、抽象生成は並行運用として独立管理**

### Level 1: 日常発火

- **タイミング**: Chat 保存・参照時に Skill が自動判定
- **担当**: Claude(Skill `vault-manager`)単独
- **内容**:
  - 統制語彙違反の自動修正(誤字、type/status/tags の揺らぎ)
  - Front Matter の必須フィールド補完
  - 命名規約違反の警告
- **介入コスト**: ゼロ(ユーザーが気づかないうちに実施)
- **Cursor 委譲**: 不要

### Level 2: 週次補正

- **タイミング**: 週次(推奨: 日曜日)
- **担当**: Naoya の承認を経て Cursor が実施
- **内容**:
  - Chat_log の分類再確認(inbox に落ちたものを本来の場所へ移動)
  - Front Matter の統制語彙整合チェック
  - リンク切れの検出
- **介入コスト**: 30 分〜1 時間
- **Cursor 委譲**: 標準(指示書テンプレを使用)

### Level 3: 月次補正

- **タイミング**: 月次(推奨: 月初 1 日)
- **担当**: Naoya の承認を経て Cursor が実施
- **内容**:
  - 構造的な整合性チェック(30_projects 全体の handoff/current-state.md 更新確認)
  - handoff の recent-changes/ のアーカイブ
  - 統制語彙の見直しと拡張
  - Skill と vault の乖離チェック
- **介入コスト**: 1〜3 時間
- **Cursor 委譲**: 標準(専用指示書テンプレを使用)

### Level 4: 季節補正

- **タイミング**: 季節(3、6、9、12 月)
- **担当**: Naoya が主導、Cursor が実施
- **内容**:
  - 大きな構造変更(ディレクトリ再編、旧命名の一括書き換え)
  - 廃止 tag の整理と過去ファイルへの遡及適用
  - Framework 側の Fable パッケージング更新
  - Vault-MCP や Skill のメジャーバージョンアップ
- **介入コスト**: 数時間〜1 日
- **Cursor 委譲**: 大規模、専用の計画・指示書を作成

### 抽象生成(並行運用)

- **タイミング**: Naoya の意向で任意タイミング(推奨: 月次〜四半期)
- **担当**: Claude 提案 + Naoya の判断 + Cursor 実施
- **内容**:
  - 複数の chat_log から共通パターンを抽出し、spec として整理
  - 議論の結果を ADR として構造化
  - 却下案の記録を rejected-alternatives として整理
- **介入コスト**: セッション単位(1-3 時間)
- **Cursor 委譲**: 部分的(執筆は Claude、構造反映は Cursor)

## Consequences

**Positive**:

- 保守作業のタイミング・担当・コストが明確化
- Cursor 委譲判定(ADR-0008)と直接的にリンク(Level 2 以上は基本 Cursor 委譲)
- 導入者に「vault のメンテナンスはこう考える」を伝えられる
- 抽象生成が chat_log の膨大な蓄積を活用する道筋になる
- vault_maintenance_config.md(00_meta/)で導入者が cadence を制御できる

**Negative**:

- 4 レベル + 抽象生成の 5 系統を管理する必要がある
- レベル境界が曖昧なケースがある(週次のつもりが月次になった、等)
- Level 4(季節補正)は年に 4 回しか発火せず、忘れがち

**Mitigation**:

- vault_maintenance_config.md で cadence を設定し、リマインダーとして機能させる
- レベル境界が曖昧な時は「1 つ上のレベルとして扱う」を暗黙のルールに
- Level 4 は Framework の Fable 更新等と連動させて忘れにくくする

## Alternatives Considered

### 案 A: 単一レベル(全保守を Cursor 委譲)

保守作業を分類せず、全て Cursor 委譲とする案。

**却下理由**:

- Level 1(日常発火)を Cursor 委譲にすると起動コストが高すぎる
- Chat 保存のたびに Cursor を挟むのは過剰

### 案 B: 3 レベル(Level 1 + Level 3 のみ、Level 2 と 4 を統合)

週次と月次を統合し、季節補正を月次に含める案。

**却下理由**:

- 週次と月次では作業内容の粒度が大きく異なる
- 季節補正は「メジャーバージョンアップ」的な位置づけで、月次と分けるのが自然

### 案 C: 抽象生成を Level 3 に統合

抽象生成を独立させず、Level 3(月次補正)の一部として実施する案。

**却下理由**:

- 抽象生成は Naoya の意向で任意タイミングで実施したい(定期化になじまない)
- Level 3 の他の作業(整合性チェック、handoff アーカイブ)とは性質が違う
- 並行運用として独立させる方が、意向に応じた柔軟な発火が可能

## Related

- **前提 ADR**: 
  - ADR-0003(Skill・Project・Vault の 3 層アーキ、Skill が Level 1 を担当)
  - ADR-0008(Cursor 委譲判定、レベル 2 以上は基本 Cursor 委譲)
- **後続 ADR**: 
  - ADR-0011(ディレクトリ構造刷新、Level 4 の代表例)
- **関連 spec**: 
  - `../specs/maintenance-four-levels.md`(4 レベルの詳細仕様)
  - `../specs/abstract-generation.md`(抽象生成の運用仕様)
- **元記録**: `10_chat_logs/2026/07/2026-07-13_maintenance-operation-design.md`
- **実装**: `vault-templates/00_meta/vault_maintenance_config.md`(導入者向け設定ファイル)

## Change Log

- 2026-07-13: 初版(4 レベル + 抽象生成の並行運用を確定)

---
audience: mixed
created: 2026-07-14 04:40:00+09:00
date: 2026-07-13
keywords:
- cursor
- delegation
- maintenance-level
- criteria
- file-count
- task-type
- delegation-judgment
related_adrs:
- '0003'
- 0009
related_chats:
- 10_chat_logs/2026/07/2026-07-13_cursor-delegation-and-maintenance-levels.md
related_specs: []
status: accepted
summary: Cursor に委譲すべき作業の判定基準を「3 ファイル以上の一括操作」の単純な数値ルールから、作業種別 × 保守レベルの組み合わせに変更した意思決定。機械的すぎる判定を廃し、作業の質を評価する方式に移行。
superseded_by: null
supersedes: null
tags:
- adr
- cursor
- delegation
title: 'ADR-0008: Cursor 委譲判定: メンテナンスレベル方式'
type: adr
updated: 2026-07-14 04:40:00+09:00
---

## Summary

Cursor に委譲すべき作業の判定基準を「3 ファイル以上の一括操作」等の単純な数値ルールから、「作業種別 × 保守運用レベル(ADR-0009)の組み合わせ」に変更した意思決定。機械的すぎる判定を廃し、作業の質を評価する方式に移行。

## Context

Vault 運用初期、以下のシンプルな数値ルールで Cursor 委譲を判定していた:

- 「3 ファイル以上の一括操作は Cursor 委譲」
- 「ディレクトリ再編は Cursor 委譲」

しかし数日の運用で以下の問題が顕在化:

- **単一ファイル操作でも Cursor 委譲が必要な場合がある**: 例えば「vault_index.md の全プロジェクト一覧を更新」は 1 ファイル操作だが、他ファイルとの整合(統制語彙、リポジトリ一覧)を伴うため、Cursor で整合性チェック込みで実施する方が安全
- **3 ファイル未満でも Claude 単独では危険な操作がある**: 例えば「あるプロジェクトを rename」は 2 ファイル操作(README + design-decisions.md)でも、wikilink 波及があるため Cursor 委譲が望ましい
- **3 ファイル以上でも Claude 単独で安全な場合がある**: 例えば「連続 3 件の日記追記」は 3 ファイル操作だが、それぞれ独立しており Claude 単独で問題ない

つまり、ファイル数は判定基準として粗すぎ、作業の性質(整合性の要求、波及範囲、リグレッションリスク)を評価する方が正しい。

## Decision

**Cursor 委譲判定を「作業種別 × 保守運用レベル」の組み合わせで実施**

### 判定基準

以下の作業は、ファイル数に関係なく Cursor 委譲を推奨:

- **リネーム操作**(ファイル、ディレクトリ、プロジェクト)- wikilink 波及があるため
- **ディレクトリ再編**(構造変更、ファイル移動を伴う)
- **アイデア → プロジェクト昇格**(_ideas/active/ → 30_projects/<RepoName>/、複数ファイル連携)
- **Front Matter の一括更新**(統制語彙変更に伴う全ファイル遡及)
- **wikilink の書き換えを伴う操作**
- **delete_note を伴う操作**(単発でもユーザー確認を推奨)
- **保守運用 Level 2 以上**(週次補正、月次補正、季節補正、ADR-0009 参照)

以下の作業は Claude 単独で実施可能:

- 1-2 ファイルの独立した作成・更新(単純な追記含む)
- 検索・参照(list_directory、get_file_content、get_frontmatter、search_by_keyword、get_section 等)
- **保守運用 Level 1**(日常発火、自動判定・自動修正)

### 判定に迷った場合

あなた(導入者) に以下を提案:

```
この作業は複数ファイルの整合性が必要なため、Cursor 経由での実施を推奨します。
指示書を作成しますか?
```

Cursor 委譲指示書のテンプレは Framework の `vault-templates/docs/cursor_instructions/_template.md` を参照。

## Consequences

**Positive**:

- 単純な数値ルールの限界を超え、作業の性質を評価できる
- ファイル数が少なくても波及が大きい操作を適切に Cursor に委譲
- ファイル数が多くても独立した操作は Claude 単独で高速に実施
- 保守運用レベル(ADR-0009)との整合が取れる
- 導入者(Framework 経由)にも判定基準が伝わりやすい

**Negative**:

- 判定基準が主観的で、Claude のセッションによってブレが出る可能性
- 「作業種別」の分類が完全ではなく、境界事例で判断に迷う
- 新しい作業種別が出た時、判定基準を追加する必要がある

**Mitigation**:

- Skill.md で判定基準を明示的に列挙(境界事例のパターンを蓄積)
- 判断に迷う時は あなた(導入者) に確認するフローを標準化
- 新しい判定パターンは月次補正(Level 3)時に Skill.md への追加を検討

## Alternatives Considered

### 案 A: ファイル数の閾値を上げる(3 → 5 等)

「5 ファイル以上で Cursor 委譲」等、閾値を調整する案。

**却下理由**: ファイル数という指標そのものが誤っており、閾値を変えても本質的な問題は解決しない。

詳細: `id-ref-removed`

### 案 B: 全ての操作を Cursor 委譲

安全側に倒し、あらゆる書き込み操作を Cursor 委譲する案。

**却下理由**:

- Cursor 起動コストが高く、日常運用の摩擦が大きい
- 単純な chat_log 保存に毎回 Cursor を挟むのは過剰
- 「Claude と直接会話しながら保存する」体験が失われる

### 案 C: 全て Claude 単独で実施(Cursor 委譲なし)

Cursor 委譲を廃止する案。

**却下理由**:

- 波及範囲の大きい操作(rename、restructure)で整合性エラーが発生する
- MCP 経由の複数ファイル一括操作は原子性がなく、失敗時の復旧が難しい
- Cursor の得意領域(構造化された一括操作)を活かせない

## Related

- **前提 ADR**: 
  - ADR-0003(Skill・Project・Vault の 3 層アーキ、Skill が委譲判定を持つ前提)
- **後続 ADR**: 
  - ADR-0009(保守運用 4 レベル、委譲判定と連動する保守レベル)
- **関連 spec**: なし
- **元記録**: `10_chat_logs/2026/07/2026-07-13_cursor-delegation-and-maintenance-levels.md`

## Change Log

- 2026-07-13 初期: 「3 ファイル以上」ルールで運用開始
- 2026-07-13 中期: 実運用でルールの限界が顕在化
- 2026-07-13 後半: メンテナンスレベル方式に変更(現行)

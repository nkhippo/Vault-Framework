---
audience: mixed
created: 2026-07-14 03:45:00+09:00
date: 2026-07-13
id: pj-2026-07-13-b5c2
keywords:
- save-destination
- plan-b
- inbox
- classification
- save-flow
- gtd
- 3-second-rule
related_adrs:
- '0003'
- 0008
- '0011'
related_chats:
- 10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md
related_specs:
- ../guidelines/save-decision-flow
- reference-level-system
status: accepted
summary: Chat 内容を Vault に保存する際、Claude が Chat 文脈から判断して直接該当ディレクトリに保存する方針(案 B)を採用した意思決定。inbox
  経由案は実際の運用で悪循環が発生したため明示的に却下。
superseded_by: null
supersedes: null
tags:
- adr
- save
- important
title: 'ADR-0007: 保存先思想: 最初から適切な場所へ(案 B)'
type: adr
updated: 2026-07-14 03:45:00+09:00
aliases:
- pj-2026-07-13-b5c2
- adr-0007
---

## Summary

Chat 内容を Vault に保存する際、Claude が Chat 文脈から直接該当ディレクトリに保存する方針(案 B)を採用した意思決定。全部 inbox に置いて後で分類する案 A を明示的に却下。

## Context

Chat 内容を Vault に保存する時、以下 3 案が考えられた:

- **案 A**: 全部一旦 `90_inbox/` に保存し、後で分類・整理する
- **案 B**: Claude が Chat の文脈から判断して、最初から適切な場所に保存する
- **案 C**: ユーザーに毎回「どこに保存しますか?」と確認する

分類作業のコスト、UX、判断ミスのリスクをどう bilancing するかが論点だった。

初期の Vault 運用開始直後、案 A(inbox 経由)を暗黙的に採用していた。しかし数日運用した結果、inbox が溜まり続けて分類作業が後回しになる悪循環が発生。この経験を踏まえて改めて設計判断を行った。

## Decision

**案 B(最初から適切な場所)を採用**

- Claude(Skill `vault-manager`)が Chat 内容から判断して、直接該当ディレクトリに保存する
- 保存判断フロー(Skill.md で定義)を明示的に定め、type ごとの典型的な保存先を確定
- 判断に迷ったら **3 秒ルール** で `90_inbox/` にフォールバック(ただし例外扱い、常態化させない)
- ユーザーに「どこに保存しますか?」とは聞かない(UX 上の摩擦を避ける)

### 保存判断フローの骨子

Skill.md に詳細を定義し、以下の順序で判断:

1. 日記・振り返り・目標の意図か? → `50_self/`(sensitive: true 自動付与)
2. Chat の生ログ性が強い(検討・議論の記録)→ `10_chat_logs/YYYY/MM/`
3. note 執筆中・公開版か → `20_notes/wip/` or `published/`
4. 新規アイデア(未リポジトリ化)→ `30_projects/_ideas/incubating/` or `active/`
5. 特定リポジトリの設計・意思決定 → `30_projects/<RepoName>/logs/YYYY/MM/`
   - 例外: 意思決定確定 → `design-decisions.md` に追記
   - 例外: 新規未解決論点 → `open-questions.md` に追記
   - 例外: 直近状態のスナップショット → `handoff/current-state.md` を更新
6. 汎用ナレッジ → `40_knowledge/<category>/`
7. 判断困難 → `90_inbox/`(3 秒ルール発動時のみ)

## Consequences

**Positive**:

- 分類作業を後回しにする悪習を回避
- ユーザーとの対話コスト最小(保存指示に対して確認質問なし)
- 保存直後に該当プロジェクトのフォルダに整理されることで、後日の参照性が高い
- Cursor 委譲(3 ファイル以上の一括操作)を発火させにくい状態を維持できる

**Negative**:

- Claude の判断ミスがあり得る(誤った場所に保存)
- 判断コストが Claude 側に集中(トークン消費が若干増える)
- 「3 秒ルール」の適用基準が主観的で、Skill 実装者(Claude)によって解釈がぶれる可能性

**Mitigation**:

- 判断ミスは Git 履歴で追跡・修正可能(移動は Cursor 委譲)
- Skill.md で保存判断フローを明示的に定義し、揺らぎを最小化
- 3 秒ルールは「頻繁に発動する場合は Skill.md 側の判断フローに追記」というメタルール

## Alternatives Considered

### 案 A: inbox 経由分類

全 Chat 内容を一旦 `90_inbox/` に保存し、後で Naoya が分類・整理する案。

**却下理由**:

- 実際の運用で inbox が溜まり続けて分類作業が後回しになる悪循環を経験(初期数日で顕在化)
- 「後で整理する」は多くの場合実行されない(GTD の Inbox Zero 原則の反例)
- 保存直後に情報が「探しに行く場所」に置かれず、参照性が低い

詳細: [[pj-2026-07-13-8dfd]]

### 案 C: ユーザーに毎回確認

保存指示のたびに「どこに保存しますか?」とユーザーに確認する案。

**却下理由**:

- UX 上の摩擦が大きい(保存の心理的コストが上がり、貴重な議論が保存されなくなる)
- ユーザーが判断を委ねたいシーンで自分で判断させられる負担
- Claude の判断ミスを恐れて過剰確認するのは、AI の有用性を減じる

## Related

- **前提 ADR**: ADR-0003(Skill・Project・Vault の 3 層アーキ、Skill が保存判断を持つ前提)
- **後続 ADR**: 
  - ADR-0008(Cursor 委譲判定、複数ファイル操作の閾値)
  - ADR-0011(ディレクトリ構造刷新、保存先の選択肢を拡張)
- **関連 spec**: 
  - `../guidelines/save-decision-flow.md`(保存判断フローの詳細)
  - `../specs/reference-level-system.md`(参照レベルとの対応)
- **元記録**: `10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md`

## Change Log

- 2026-07-13: 初版(inbox 運用の反省を踏まえて案 B 採用)

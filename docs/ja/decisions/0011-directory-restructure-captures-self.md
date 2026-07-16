---
audience: mixed
created: 2026-07-14 04:55:00+09:00
date: 2026-07-13
id: pj-2026-07-13-ab6d
keywords:
- directory
- restructure
- captures
- self
- handoff
- 10_captures
- 50_self
- sub-classification
related_adrs:
- '0007'
- 0009
- '0010'
related_chats:
- 10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md
related_specs:
- handoff-mechanism
status: accepted
summary: 'Vault のトップレベルディレクトリ構造を実運用の学びに基づいて刷新した意思決定。主要な変更は 3 点: 10_chat_logs/ → 10_captures/
  サブ分類化、50_self/ 新設、handoff/ を全プロジェクトに展開。'
superseded_by: null
supersedes: null
tags:
- adr
- structure
- important
title: 'ADR-0011: ディレクトリ構造刷新'
type: adr
updated: 2026-07-14 04:55:00+09:00
aliases:
- pj-2026-07-13-ab6d
- adr-0011
---

## Summary

Vault のトップレベルディレクトリ構造を実運用の学びに基づいて刷新した意思決定。主要な変更は 3 点:`10_chat_logs/` を将来 `10_captures/` にリネームしてサブ分類化、`50_self/` を新設して個人領域を分離、`handoff/` を全プロジェクトに展開。

## Context

Vault 運用の数日〜数週間で、以下の構造的な改善点が見えてきた:

- **10_chat_logs/ の粒度**: Chat 内容だけでなく、discussions(議論の記録)、quick-thoughts(思考の断片)、external-inputs(記事や書籍からの入力)等、より細かい分類が可能
- **個人領域の欠如**: 日記や振り返り、目標など、Naoya の個人的な記録を置く適切な場所がなかった(90_inbox/ に投げるのは違和感)
- **handoff/ が Vault-Framework にしかない**: ADR-0010 で導入した handoff/ 領域が、他のプロジェクト(IPASoundDrill、English-* 等)には未展開

これらを個別に対処するのではなく、構造刷新として一括で見直す判断が必要だった。同時に、Framework の vault-templates/ にも反映する必要がある(導入者にも同じ構造を提供)。

## Decision

**ディレクトリ構造を以下の 3 点で刷新**

### 変更 1: 10_chat_logs/ → 10_captures/ サブ分類化(将来)

現行:

```
10_chat_logs/YYYY/MM/*.md
```

将来:

```
10_captures/
├── discussions/YYYY/MM/*.md    # 議論の記録
├── quick-thoughts/YYYY/MM/*.md # 思考の断片
└── external-inputs/YYYY/MM/*.md # 記事、書籍からの入力
```

- **10_chat_logs/ → 10_captures/**: 「Chat のログ」より「捕捉した情報」の方が本質を捉える(discussions は Chat とは限らないため)
- **サブ分類の導入**: type を discussions/quick-thoughts/external-inputs で明示化
- **移行タイミング**: Level 4 季節補正(ADR-0009)で実施予定、まだ未実施

### 変更 2: 50_self/ 新設(v1.1、2026-07-13 実施済み)

```
50_self/
├── README.md
├── diary/YYYY/MM/YYYY-MM-DD.md  # 日記
├── reflections/                  # 振り返り(将来)
│   ├── weekly/YYYY/YYYY-WW.md
│   └── monthly/YYYY/YYYY-MM.md
├── goals/                        # 目標(将来)
└── health/                       # 健康関連(将来)
```

- 個人的な記録の専用領域を新設
- デフォルトで `sensitive: true`(Skill の参照ルールで厳格化、ADR-0016 の sensitive 引用禁止と連動)
- diary/ のみ v1.1 で実装、reflections/ 以下は将来対応

### 変更 3: handoff/ を全プロジェクトに展開

- 現状: `30_projects/Vault-Framework/handoff/`、`30_projects/Vault/handoff/`、`30_projects/Vault-MCP/handoff/` のみ
- 将来: 全 30_projects/<RepoName>/ に handoff/ を配置
- 移行タイミング: 各プロジェクトの current-state.md を初回作成する時に自動配置

## Consequences

**Positive**:

- 情報の分類粒度が細かくなり、検索性が向上
- 個人領域(50_self/)が明示的に分離され、sensitive 扱いが自然
- handoff/ が全プロジェクトに展開されると、任意のプロジェクトで同じキャッチアップ手順が使える
- Framework の vault-templates/ に反映することで、導入者にも同じ構造を提供

**Negative**:

- 変更 1(10_captures/ 移行)は過去 chat_log 内の wikilink を大量に書き換える必要があり、大規模作業
- サブ分類の判定が主観的で、discussions と quick-thoughts の境界が曖昧なケースがある
- 全プロジェクトへの handoff/ 展開は、各プロジェクトの初回 current-state 作成が必要

**Mitigation**:

- 10_captures/ 移行は Level 4 季節補正として計画(Cursor 委譲、専用指示書)
- 過去の chat_log wikilink 書き換えは同時実施(step 5 として Cursor に委譲予定)
- サブ分類の判定基準は保守運用 Level 3 で見直し
- handoff/ 展開は「該当プロジェクトを触った Chat セッション」で順次実施(一括でなく)

## Alternatives Considered

### 案 A: 現状維持(構造刷新なし)

刷新せず、現行の 10_chat_logs/ + 50_self/ 未設定のまま運用する案。

**却下理由**:

- 10_chat_logs/ の粒度不足がスケール時に問題化(数百 chat_log で検索性が低下)
- 個人領域が無いことで、日記等が inbox に紛れる違和感
- Framework の完成度を上げる観点で、構造の整理が必要

### 案 B: 段階的刷新(50_self/ のみ先行、10_captures/ は将来)

50_self/ 新設だけ先行し、10_captures/ 移行は忘れる案。

**却下理由**:

- 10_captures/ 移行を計画に載せておかないと、いつまでも 10_chat_logs/ のまま塩漬け
- ADR に記録することで「将来やる」が明示化され、忘れにくくなる

### 案 C: 数字プレフィックスの見直し(00, 10, 20 の刻みを変える)

`00_meta/`、`10_captures/` の代わりに `10_meta/`、`20_captures/` 等に変更する案。

**却下理由**:

- 過去のファイルの wikilink 書き換えコストが膨大
- 現行の 10 刻みで拡張余地(60_/70_/80_)は十分ある
- 数字より名前の意味の方が重要

## Related

- **前提 ADR**: 
  - ADR-0007(保存先思想、直接適切な場所へ)
  - ADR-0009(保守運用 4 レベル、Level 4 として実施予定)
  - ADR-0010(handoff/ 領域の新設、この ADR でその展開を確定)
- **後続 ADR**: なし
- **関連 spec**: `../specs/handoff-mechanism.md`(handoff 機構の詳細)
- **元記録**: `10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md`
- **実装状況**:
  - 50_self/ の diary サブディレクトリ: v1.1 で実装済み(2026-07-13)
  - 10_captures/ 移行: 未実施(Level 4 季節補正待ち)
  - handoff/ 全プロジェクト展開: 部分実施(Vault、Vault-MCP、Vault-Framework の 3 プロジェクトのみ)

## Change Log

- 2026-07-13: 初版(3 点刷新の計画確定)
- 2026-07-13: 50_self/diary/ 実装(v1.1)
- 2026-07-14 予定: 10_captures/ 移行と wikilink 書き換え(Level 4)

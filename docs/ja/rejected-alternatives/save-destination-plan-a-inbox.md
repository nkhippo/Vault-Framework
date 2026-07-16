---
audience: mixed
created: 2026-07-14 05:35:00+09:00
date: 2026-07-13
keywords:
- inbox
- save-destination
- plan-a
- classification
- gtd
related_adrs:
- '0007'
status: rejected
summary: Chat 保存時に全て一旦 90_inbox/ に置き、後で分類する運用案(案 A)。実運用で inbox が溢まり続けて分類が後回しになる悪循環が発生したため却下。
superseded_by: '0007'
tags:
- rejected
- save-destination
title: '却下案: inbox 経由分類方式'
type: rejected_alternative
updated: 2026-07-14 05:35:00+09:00
id: pj-2026-07-13-8dfd
aliases:
- pj-2026-07-13-8dfd
---

## Summary

Chat 保存時に全て一旦 `90_inbox/` に置き、後で分類する運用案(案 A)。実運用で inbox が溜まり続けて分類が後回しになる悪循環が発生したため却下。ADR-0007 で「最初から適切な場所へ(案 B)」を採用。

## What Was Proposed

保存指示への対応として、以下の運用を行う案:

- Chat 保存時、Claude は判断せず全て `90_inbox/YYYY-MM-DD_slug.md` に保存
- Naoya が定期的(週次〜月次)に inbox の中身を確認し、適切な場所へ移動
- 移動は Cursor 委譲 or Obsidian で手動実施
- 移動時に Front Matter の統制語彙を最終確認

## Why It Was Considered

- **判断ミスがゼロ**: Claude が保存先を判断しないため、誤った場所への保存が発生しない
- **保存が高速**: Claude が判断ロジックを実行しないため、応答が速い
- **Naoya のコントロール**: 最終的な分類は Naoya の判断で行うため、意図と一致
- **後で見直せる**: 保存直後は判断できない微妙な話題も、時間を置いてから分類できる

## Why It Was Rejected

- **inbox が溜まり続ける**: 実運用で 90_inbox/ が急速に肥大化(数日で数十ファイル)
- **分類作業が後回しになる**: 「後で整理する」は多くの場合実行されない(GTD の Inbox Zero の反例)
- **参照性が低い**: 保存直後の Chat 内容が inbox にあるため、後日「あの議論どこにあった?」を探すのが困難
- **conversation_search との相性**: 過去 Chat 検索でも、inbox に散在するファイルは分類済みファイルより見つけにくい
- **Cursor 委譲の頻度が上がる**: 週次 inbox 整理を Cursor 委譲する必要があり、そのオーバーヘッド
- **設計判断のフラッシュバック**: 「案 A で始めて数日後に苦痛が顕在化した」経験そのものが、この案の欠陥を実証

## What Was Chosen Instead

- **採用案**: ADR-0007「保存先思想:最初から適切な場所へ(案 B)」
- **参照**: [[pj-2026-07-13-b5c2]]

Skill が Chat 文脈から判断して直接該当ディレクトリに保存する。判断に迷ったら 3 秒ルールで 90_inbox/ にフォールバック(常態化させない)。

## References

- 実運用の記録: 2026-07-13 早期の運用開始と数日後の反省
- 対応 ADR: [[pj-2026-07-13-b5c2]]

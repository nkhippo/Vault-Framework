---
audience: mixed
date: 2026-07-14
keywords:
- maintenance
- 保守運用
- four-levels
- abstract-generation
related_adrs:
- 0008
- 0009
related_specs:
- maintenance-four-levels
- abstract-generation
status: published
summary: Vault の保守運用 4 レベルの全体像。各レベルの位置づけと全体像を把握できるようにする。
title: 保守運用ガイド
title_en: Maintenance Guide
type: overview
created: 2026-07-14 20:47:58+09:00
updated: 2026-07-14 20:47:58+09:00
---

## Summary

Vault の保守運用 4 レベルの全体像を概説する。詳細は spec を参照する形にし、ここでは各レベルの位置づけと全体像を把握できるようにする。

## 保守運用の全体像

Vault は使い続けるほど、統制語彙の揺らぎ、Front Matter の欠損、命名規約の逸脱、handoff の肥大化等、様々な「エントロピー」が蓄積する。これに対処するため、Vault-Framework は **4 段階の保守運用レベル** を定義している。

| レベル | 頻度 | 担当 | 典型的な作業 |
|---|---|---|---|
| Level 1 | 日常(イベント駆動) | Claude 単独 | 統制語彙の自動修正、Front Matter 補完 |
| Level 2 | 週次 | Cursor 委譲 | 分類再確認、リンク切れ検出 |
| Level 3 | 月次 | Cursor 委譲 | 構造整合性チェック、handoff アーカイブ |
| Level 4 | 季節(3ヶ月毎) | あなた(導入者) 主導 + Cursor | 大規模構造変更、廃止 tag 整理 |

頻度が高いレベルほど軽い作業、頻度が低いレベルほど重い作業という設計になっている。

## Level 1: 日常発火(自動)

Chat での保存・参照のたびに、Claude(Skill)が自動的に以下をチェック・修正する:

- 統制語彙の表記揺れ(`ChatLog` → `chat_log` 等)
- Front Matter の必須フィールド補完
- 命名規約違反の警告

あなた(導入者) の介入コストはほぼゼロ。気づかないうちに実施される。

## Level 2: 週次補正(Cursor 委譲)

週に一度、あなた(導入者) の承認を得て Cursor が以下を実施:

- 90_inbox/ に落ちたファイルの再分類
- vocabulary.md との整合チェック
- wikilink の切れたリンクの検出

## Level 3: 月次補正(Cursor 委譲)

月に一度、以下を実施:

- 各プロジェクトの handoff/current-state.md の更新確認
- current-state.md が肥大化していれば recent-changes/ へのアーカイブ
- 統制語彙の使用頻度分析、拡張候補の提案

## Level 4: 季節補正(あなた(導入者) 主導)

3ヶ月に一度程度、以下のような大規模作業を実施:

- ディレクトリ構造の再編(例: `10_chat_logs/` の下位分類見直し)
- 廃止 tag/type の一括整理
- Skill や Vault-MCP のメジャーバージョンアップ対応

## 抽象生成という並行運用

保守運用 4 レベルとは独立して、**抽象生成**という並行運用がある。これは具体的な chat_log から ADR / spec / rejected-alternatives のような抽象的なドキュメントを生成するプロセスで、任意のタイミング(月次〜四半期)で実施される。

Vault-Framework 自体の ADR 16 本、rejected-alternatives 16 本、spec 8 本はすべてこの抽象生成プロセスによって、蓄積された chat_log や設計議論から生成されたものである。

## なぜ 4 レベルに分けたか

単一の「メンテナンス」概念ではなく、頻度と担当を軸に 4 レベルに分けたのは、以下の理由による:

- **頻度が違えば担当も変わるべき**: 毎日発生する軽微な修正を Cursor 委譲するのは非効率、逆に月次の大規模チェックを Claude が単独でやるのは判断コストが高すぎる
- **判断の重さと頻度は逆相関する**: 高頻度な作業ほど機械的な判定で済むものが多く、低頻度な作業ほど人間の判断が必要になる傾向がある

## 関連

- ADR 0008: Cursor 委譲の判定基準
- [ADR 0009: 保守運用 4 レベル + 抽象生成](../decisions/0009-four-level-maintenance-operation.md)
- maintenance-four-levels spec: 保守運用の詳細仕様
- abstract-generation spec: 抽象生成の詳細仕様

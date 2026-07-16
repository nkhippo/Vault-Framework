---
created: 2026-07-13 21:42:00+09:00
keywords:
- vault-structure
- directory
- top-level
- framework
- 50_self
- captures
status: published
summary: Vault のトップレベルディレクトリの構造と役割を定義。導入者はこの構造を採用することが推奨される。
tags:
- framework
- vault-templates
- meta
title: Vault 構造
type: knowledge
updated: 2026-07-13 21:42:00+09:00
id: pj-2026-07-13-0391
aliases:
- pj-2026-07-13-0391
---

## Summary

Vault のトップレベルディレクトリの構造と役割を定義。導入者が自分の Vault リポジトリを立ち上げる際、この構造を採用することが推奨される。

## トップレベル

| ディレクトリ | 用途 | 保存するもの | 保存しないもの |
|---|---|---|---|
| `00_meta/` | AI 向けメタ情報 | 規約、テンプレート、語彙 | 実コンテンツ |
| `10_chat_logs/` | 生の会話ログ | Claude との対話記録 | 清書したもの(→ `20_notes/`) |
| `20_notes/wip/` | note 執筆中 | 下書き、構成案 | 完成品(→ `published/`) |
| `20_notes/published/` | note 公開済み清書 | 実際に投稿した最終版 | 下書き |
| `30_projects/<RepoName>/` | アプリ別設計記録 | 仕様、意思決定、レビュー | 実装ログ(各アプリの GitHub リポジトリで管理) |
| `30_projects/_ideas/` | リポジトリ化前のアイデア | コンセプト検討、初期メモ | リポジトリ化されたもの |
| `40_knowledge/` | 汎用ナレッジ | 参考情報、学び、メモ | 特定プロジェクト固有の情報 |
| `50_self/` | 個人的な記録 | 日記、振り返り、目標、健康関連 | 他 |
| `90_inbox/` | 一時置き場 | 分類迷い時の暫定保管 | 分類確定したもの |

## 保存しないもの(重要)

- 各アプリで Cursor が対応した実装記録(各アプリの GitHub リポジトリで管理)
- ビルドログ、テスト結果
- 機微な資格情報(トークン等)

## `30_projects/` の命名規則

サブディレクトリ名は **GitHub リポジトリ名と完全一致**させる(大文字小文字含む)。
これにより「ディレクトリ名 = リポジトリ名」の 1:1 対応が保たれ、Cursor 委譲時の指示ミスを防ぐ。

## `50_self/` の扱い(センシティブ)

50_self/ 配下はデフォルトで `sensitive: true` として扱われ、Skill による自動参照は原則行わない。詳細は 50_self/README.md 参照。

## アイデアのライフサイクル

```
[アイデア発生]
  ↓
30_projects/_ideas/incubating/<slug>/    温めているだけ
  ↓
30_projects/_ideas/active/<slug>/        検討進行中、リポジトリ化目前
  ↓  (リポジトリ作成)
30_projects/<RepoName>/                  昇格。旧記録は _history/ に保管
```

分岐: active から shelved(復活余地あり) / rejected(やらないと確定) に移動も可能。

## 分類に迷ったら

1. 日記・振り返り・目標の意図 → `50_self/diary/` or `reflections/` or `goals/`
2. Chat のログ性が強い → `10_chat_logs/YYYY/MM/`
3. note にする予定 → `20_notes/wip/`
4. リポジトリ化済みプロジェクトの話 → `30_projects/<RepoName>/logs/YYYY/MM/`
5. 新規アイデアの話 → `30_projects/_ideas/incubating/<slug>/` または `active/<slug>/`
6. 判断つかない → `90_inbox/` に置いて後で移動

## 導入者への注意

このディレクトリ構造は Framework の推奨構造。プロジェクト規模や運用スタイルに応じて以下のカスタマイズが可能:

- 数字プレフィックスの間隔(10 刻み → 20 刻みや連番)
- ディレクトリの追加(例: `60_reference/` の新設)
- 一部ディレクトリの省略(50_self/ を使わない等)

ただし `00_meta/` は Skill が参照する起点のため、名前と位置は保持することを強く推奨。

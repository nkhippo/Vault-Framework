---
keywords:
  - backlog
  - tags
  - vocabulary
  - meta
  - framework
status: published
summary: Backlog item に付与する tag の一覧・意図・追加ルール(骨格)。tag の氾濫を防ぐため Claude はこの一覧から選ぶ。ドメイン固有の主題 tag は導入者が追加する。
tags:
  - framework
  - vault-templates
  - meta
  - backlog
  - vocabulary
title: Backlog Tags 一覧
type: knowledge
created: 2026-07-18T00:58:23+09:00
updated: 2026-07-18T00:58:23+09:00
---

## Summary

Backlog item(`type: backlog_item`)の Front Matter `tags` に含める tag の管理カタログ。tag の氾濫を防ぐため、**Claude は backlog 操作時に本ファイルを読み込み、この一覧から選ぶ**。新規追加はあなた(導入者)の明示承認を前提とする。

## 必須 tag

- **`backlog`**: 全ての backlog item に自動付与(`type: backlog_item` と同義的な cross-cutting 検索用)

## 任意 tag(1-3 個目安、選定は主題に応じる)

### 主題系(汎用)

議論の主題を表す tag。プロジェクト固有の主題はあなたが追加する。

| Tag | 意図 | 使用例 |
|---|---|---|
| `ui` | UI 設計・見た目 | 「画面 UI を見直す」 |
| `ux` | User Experience、操作フロー | 「操作フローを改善する」 |
| `performance` | 実行速度、リソース効率 | 「起動時間を短縮する」 |
| `docs` | ドキュメント整備 | 「README を更新する」 |
| `architecture` | 全体構造、モジュール分割 | 「サーバの責務を分割する」 |
| `spec` | 仕様策定・仕様変更 | 「仕様を決める」 |

<!-- ドメイン固有の主題 tag はあなたが追加する(実運用例: `pronunciation`, `vocabulary`)。追加は下記「追加ルール」に従う。 -->

### 性質系

item の性質(何をする性質のものか)。

| Tag | 意図 | 使用例 |
|---|---|---|
| `bug-fix` | 既知バグの修正 | 「特定条件でクラッシュする問題」 |
| `enhancement` | 機能拡張・改善 | 「フィルタ機能を追加」 |
| `investigation` | 調査・検証(方針未決) | 「ライブラリ選定の調査」 |
| `refactor` | リファクタリング | 「dependency injection 導入」 |
| `design` | 設計・思想検討 | 「ID scheme の設計」 |
| `question` | 疑問・不明点 | 「仕様を確認したい」 |

### 状況系

item の現在の状況を示す(自動付与ではなく、あなたが明示的に付ける)。

| Tag | 意図 | 使用例 |
|---|---|---|
| `urgent` | 優先度が高い | 締切直前 |
| `blocked` | 他 item の完了待ち | 依存関係あり |
| `stalled` | 一定期間(例: 2 週間)以上動きがない | 週次棚卸しで検出 |

## 追加ルール

新しい tag を追加したい時:

1. **Claude 側**: 既存 tag で表現できないと判断したら、あなたに「新規 tag `xxx` を追加していい?」と明示確認
2. **承認後**: 本ファイルの適切なカテゴリ(主題/性質/状況)に追加、意図・使用例を記載
3. Claude は次回以降、この tag を使用可能

**あなたの明示承認なく tag を新規追加してはならない**。

## 使用時の注意

- Tag は 1-3 個目安。多すぎると検索性が下がる
- 主題系は 1-2 個で十分(重複させない)
- 性質系は 1 個(refactor と bug-fix を同時に付けない、どちらが主目的か)
- 状況系は状況が変わったら update(stalled → 動き出したら削除)

## 関連

- Backlog item テンプレ: `templates/backlog_item.md`
- Backlog スキーマ: `frontmatter_schema/backlog_item.md`

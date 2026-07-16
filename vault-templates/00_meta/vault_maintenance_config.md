---
created: 2026-07-14 02:20:00+09:00
keywords:
- maintenance
- config
- 4-level
- abstract-generation
- cursor-delegation
- sensitive
- cadence
status: published
summary: 保守運用(4 レベル + 抽象生成)の設定ファイル。導入者が「どの保守を、いつ、どこまで自動で走らせるか」をカスタマイズする。
tags:
- framework
- vault-templates
- meta
- maintenance
- config
title: Vault Maintenance Config
type: knowledge
updated: 2026-07-14 02:20:00+09:00
id: pj-2026-07-13-18e5
aliases:
- pj-2026-07-13-18e5
---

## Summary

Vault の保守運用(4 レベル + 抽象生成)の設定ファイル。導入者が「どの保守を、いつ、どこまで自動で走らせるか」をカスタマイズする。Skill `vault-maintainer`(将来分離予定)がこの設定に基づいて動作する。

**このファイルの位置づけ**: 保守運用のポリシーを一元管理。手動編集を想定。

## 保守運用の 4 レベル

Vault-Framework は保守を以下 4 レベルに分類する:

- **Level 1(日常発火)**: 保存・参照時に Skill が自動判定・自動修正できる範囲(誤字修正、簡単な統制語彙違反、タグ追加漏れ等)
- **Level 2(週次補正)**: 週次で Naoya が承認しつつ Cursor に委譲する軽い一括修正
- **Level 3(月次補正)**: 月次で構造的な整合性チェック、リンク切れ、Front Matter 統一
- **Level 4(季節補正)**: 大きな構造変更、旧命名の一括書き換え、廃止 tag の整理

詳細は Framework の `docs/ja/specs/maintenance-four-levels.md` 参照。

## 抽象生成の並行運用

具体的な chat_log から、より抽象的な spec や ADR を生成する運用。定期実施を想定。詳細は Framework の `docs/ja/specs/abstract-generation.md` 参照。

## 設定項目

### 保守レベルの ON/OFF

導入者はこのセクションで「どのレベルを自動で走らせるか」を制御する。

```yaml
maintenance_levels:
  level_1_daily_on_save: true        # 保存時に Skill が自動修正
  level_2_weekly_batch: false        # 週次バッチ(手動起動)
  level_3_monthly_check: false       # 月次チェック(手動起動)
  level_4_seasonal_migration: false  # 季節補正(手動起動、専用計画付き)
```

### 保守運用の cadence(頻度)

```yaml
cadence:
  weekly_batch_day: "sun"            # 週次: 日曜日推奨(0=Sun, 1=Mon, ...)
  monthly_check_day: 1               # 月次: 月初 1 日推奨
  seasonal_month: [3, 6, 9, 12]      # 季節: 3, 6, 9, 12 月推奨
```

### 抽象生成の対象範囲

```yaml
abstract_generation:
  enabled: false                     # 有効化する場合は true
  source_dirs: 
    - "10_chat_logs/"               # 生ログを抽象化の対象に
    - "30_projects/*/logs/"          # プロジェクト別ログも対象
  exclude_paths:
    - "50_self/"                    # センシティブ領域は除外
    - "90_inbox/"                   # 未分類は除外
  target_types:
    - "chat_log"                    # 対象 type
    - "project_design"
  minimum_length_chars: 500          # この文字数未満の chat_log は抽象化対象外
```

### Cursor 委譲判定の閾値

```yaml
cursor_delegation:
  max_files_for_direct: 2            # Claude が単独で操作する上限
  always_delegate_operations:
    - "rename"
    - "restructure"
    - "batch_frontmatter_update"
    - "wikilink_rewrite"
    - "promotion"                    # アイデア → プロジェクト昇格
```

### センシティブ扱いのデフォルト

```yaml
sensitive_defaults:
  types:
    - "diary"                        # デフォルトで sensitive: true
    - "reflection"
    - "goal"
  paths:
    - "50_self/"                     # このパス配下は sensitive
    - "40_knowledge/health/"         # 例(必要に応じて追加)
```

### 通知先(将来、GitHub Actions 等連携時)

```yaml
notifications:
  weekly_batch_report_to: ""         # 通知先(email or webhook URL)
  monthly_check_report_to: ""
  errors_report_to: ""
```

## 適用例(Naoya の実運用)

<!-- 導入者はここに自分の適用実例を書く。
以下は Naoya の 2026-07-14 時点の例:

- Level 1 のみ ON、Level 2-4 は手動起動
- 抽象生成は未開始
- Cursor 委譲は max_files_for_direct: 2 で運用
- センシティブは 50_self/ 配下と、40_knowledge/health/ 予定
-->

## 変更履歴の管理

このファイルの設定変更は Git 履歴に残る。設定を変えたらコミットメッセージに理由を書く。

```
docs(00_meta): raise cursor_delegation.max_files_for_direct to 3
Reason: 単一 file 操作が多く、頻繁に Cursor 委譲が発火していた
```

## 導入者への注意

初期状態のこのファイルは「Level 1 のみ ON、他は OFF」で運用開始できる。導入者は必要に応じて他レベルを ON にする。ただし、有効化する前に対応する保守運用の手順書(週次バッチのコマンド、月次チェックの実行方法等)を確認してから起動すること。

保守運用の詳細は Framework の `docs/ja/maintenance-guide.md` を参照。

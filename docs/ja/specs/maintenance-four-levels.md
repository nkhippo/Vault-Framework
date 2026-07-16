---
audience: mixed
created: 2026-07-14 07:35:00+09:00
keywords:
- maintenance
- four-levels
- spec
- level-1
- level-2
- level-3
- level-4
- cadence
- cursor-delegation
related_adrs:
- 0008
- 0009
- '0011'
status: published
summary: Vault の保守運用 4 レベルの詳細仕様。各レベルの発火条件、担当、作業内容、Cursor 委譲判定、cadence 設定を規定。
tags:
- spec
- maintenance
title: 保守運用 4 レベル 仕様
type: spec
updated: 2026-07-14 07:35:00+09:00
id: pj-2026-07-13-d0dd
aliases:
- pj-2026-07-13-d0dd
---

## Summary

Vault の保守運用 4 レベル(Level 1 日常発火 / Level 2 週次補正 / Level 3 月次補正 / Level 4 季節補正)各レベルの詳細仕様。発火条件、担当、作業内容、Cursor 委譲判定、cadence 設定を規定。ADR-0009 の実装スペック。

## Scope

このスペックが規定するもの:

- 4 レベル各レベルの詳細
- 発火条件と担当(Claude 単独 or Cursor 委譲)
- 標準の作業内容とチェックリスト
- cadence(発火頻度)の設定と管理
- vault_maintenance_config.md との連動

このスペックが規定しないもの:

- 抽象生成の並行運用(abstract-generation.md 参照)
- Cursor 委譲判定の詳細(ADR-0008 参照)

## Design Principle

**「頻度・担当・介入コスト」の 3 軸で分類**。以下 3 原則:

1. **頻度と作業重さの逆相関**: 高頻度は軽い作業(Level 1)、低頻度は重い作業(Level 4)
2. **担当の明確化**: Level 1 は Claude 単独、Level 2+ は基本 Cursor 委譲
3. **cadence の柔軟化**: 導入者が vault_maintenance_config.md で頻度を制御可能

## Level 1: 日常発火

### 発火条件

- Chat 保存時(create_note / update_note の実行時)
- Chat 参照時(get_file_content / get_frontmatter / list_directory の実行時)
- 発火はイベント駆動、cadence 設定なし(発生の度に自動実施)

### 担当

- **Claude(Skill `vault-manager`)単独**
- Cursor 委譲なし
- Naoya の承認不要

### 作業内容

以下を自動チェック・自動修正:

#### 統制語彙違反の自動修正

- **大文字小文字の揺らぎ**: `ChatLog` → `chat_log`
- **区切り文字の揺らぎ**: `chat-log` → `chat_log`
- **タイポの修正**: `chat_lo` → `chat_log`(明らかな typo のみ)

#### Front Matter の必須フィールド補完

- `created` / `updated` が欠けている場合、現在時刻を自動補完
- `type` が欠けている場合、保存先ディレクトリから推定
- `title` が欠けている場合、Chat 主題から生成

#### 命名規約違反の警告

- ファイル名が `YYYY-MM-DD_kebab-slug.md` パターンに合わない場合、警告
- Naoya に確認して修正するか、そのまま保存するかを提案

#### sensitive フィールドの自動付与

- diary/reflection/goal type の場合、`sensitive: true` を自動付与
- 50_self/ 配下のファイルは自動的に sensitive 扱い

### 介入コスト

- **ゼロ**: Naoya が気づかないうちに実施
- 例外: 命名規約違反等で確認が必要な場合のみ、1-2 秒の対話

### Cursor 委譲

- **不要**: Claude で完結

## Level 2: 週次補正

### 発火条件

- 週次(推奨: 日曜日、vault_maintenance_config.md で cadence 設定可能)
- Naoya が明示的に「週次の Vault メンテナンスをお願いします」と発話した時
- Level 1 で検出した違反が 10 件以上蓄積した時(バッチ処理の必要性)

### 担当

- **Naoya の承認を経て Cursor が実施**
- Claude(Skill)は指示書を作成、Naoya が Cursor に渡す

### 作業内容

以下を実施:

#### Chat_log の分類再確認

- 90_inbox/ に落ちたファイルの再分類
- 誤った場所に保存されたファイルの移動

#### Front Matter の統制語彙整合チェック

- vocabulary.md に未登録の tag/type を使っているファイルを検出
- 過去ファイルに混在する古い表記を修正

#### リンク切れの検出

- wikilink の指し先が実在するかチェック
- 存在しないファイルへのリンクを修正または削除

#### 週次スナップショット

- 各プロジェクトの handoff/current-state.md の updated 日時をチェック
- 1 週間以上更新されていないプロジェクトを Naoya に報告

### 介入コスト

- **30 分〜1 時間**(Naoya のレビュー含む)
- Cursor の実行は 5-10 分、レビューが主要な時間

### Cursor 委譲

- **標準**: 週次バッチ用の指示書テンプレを使用
- 指示書テンプレ: `vault-templates/docs/cursor_instructions/weekly-batch.md`(将来作成)

## Level 3: 月次補正

### 発火条件

- 月次(推奨: 月初 1 日、vault_maintenance_config.md で cadence 設定可能)
- Naoya が明示的に「月次のクリーンアップをお願いします」と発話した時

### 担当

- **Naoya の承認を経て Cursor が実施**

### 作業内容

以下を実施:

#### 構造的な整合性チェック

- 30_projects 全体の handoff/current-state.md 更新確認
- 各プロジェクトの design-decisions.md、open-questions.md、roadmap.md の整合性
- 30_projects/_ideas/ の incubating → active 昇格候補の抽出

#### handoff の recent-changes/ アーカイブ

- current-state.md が prepend で肥大化している場合、月次アーカイブ実施
- 詳細は handoff-mechanism.md の Monthly Archive Procedure 参照

#### 統制語彙の見直しと拡張

- 使用頻度分析(未使用 tag、過剰使用 tag)
- 新規 type/tag の追加提案(実運用で頻出するようになったもの)

#### Skill と vault の乖離チェック

- SKILL.md の記述と vault 側 00_meta の記述が一致しているか
- 乖離があれば Naoya に報告し、どちらを正とみなすか確認

### 介入コスト

- **1〜3 時間**(Naoya のレビュー含む)
- Cursor の実行は 15-30 分

### Cursor 委譲

- **標準**: 月次補正用の指示書テンプレを使用
- 指示書テンプレ: `vault-templates/docs/cursor_instructions/monthly-check.md`(将来作成)

## Level 4: 季節補正

### 発火条件

- 季節(3、6、9、12 月、vault_maintenance_config.md で cadence 設定可能)
- 大きな構造変更が必要になった時(例: 10_chat_logs/ → 10_captures/ 移行)
- Skill や Vault-MCP のメジャーバージョンアップ時

### 担当

- **Naoya が主導、Cursor が実施**
- 大規模作業のため、複数セッションに分けて実施することも

### 作業内容

以下を実施(該当するもののみ):

#### 大きな構造変更

- ディレクトリ再編(例: 10_chat_logs/ → 10_captures/ + サブ分類)
- 旧命名の一括書き換え(過去 chat_log の wikilink 更新)
- トップレベル数字プレフィックスの見直し

#### 廃止 tag/type の整理

- 廃止された tag を過去ファイルから削除
- 廃止された type を新 type に一括更新

#### Framework 側の Fable パッケージング更新

- Vault-Framework の Public 化準備
- ドキュメントの英語翻訳(docs/en/)の同期
- リリースノート作成

#### Vault-MCP や Skill のメジャーバージョンアップ

- MCP プロトコルの新バージョン対応
- Skill v1 → v2 の設計変更
- API の互換性維持と破壊的変更の管理

### 介入コスト

- **数時間〜1 日**(セッション分割の場合、合計はさらに大きい)
- Cursor の実行は 30 分-2 時間
- Naoya のレビューが最も時間かかる

### Cursor 委譲

- **大規模、専用計画と指示書を作成**
- 複数の Cursor 指示書を並行または直列で実施
- 事前に Level 3 で情報整理をしておく必要

## Cadence Configuration

vault_maintenance_config.md での cadence 設定:

```yaml
cadence:
  weekly_batch_day: "sun"            # 週次: 日曜日推奨
  monthly_check_day: 1               # 月次: 月初 1 日推奨
  seasonal_month: [3, 6, 9, 12]      # 季節: 3, 6, 9, 12 月推奨
```

- 各 cadence は導入者が調整可能
- 通知(GitHub Actions 等連携時)は notifications セクションで設定
- Level 1 は cadence 設定なし(イベント駆動)

### 導入者への注意

- 初期状態: Level 1 のみ ON、Level 2-4 は手動起動推奨
- 慣れてきたら Level 2 の自動化を検討(Cron ジョブ + Cursor CLI)
- Level 3、4 は手動起動を維持(判断が必要な作業のため)

## Level Transition and Interaction

### Level 間の連携

- **Level 1 → Level 2**: Level 1 で検出した違反が蓄積したら、次回 Level 2 で一括処理
- **Level 2 → Level 3**: Level 2 で残った問題(判断が難しいもの)を Level 3 で処理
- **Level 3 → Level 4**: Level 3 で提案した大きな変更を Level 4 で実施

### 抽象生成との並行運用

- 保守運用と抽象生成は独立
- 抽象生成は Naoya の意向で任意タイミング(月次〜四半期)で発火
- 詳細は abstract-generation.md 参照

## Monitoring and Reporting

### Level 1 の実施状況

- 保守運用ログとして、Level 1 で修正した内容を記録(将来の spec 化候補)
- Skill 側で「今日修正した件数」を Chat の最後に報告(オプション)

### Level 2、3、4 の実施レポート

- 各実施の完了レポートを handoff/recent-changes/YYYY/MM/ に保存
- 実施内容、修正件数、Naoya の判断ポイントを記録

### 定期的な振り返り

- 四半期毎に、保守運用の効率と改善点を振り返り
- 統制語彙の追加候補、Skill 側の判定基準の更新等をこのタイミングで提案

## References

- **関連 ADR**: 
  - [[../decisions/0009-four-level-maintenance-operation.md]](4 レベル + 抽象生成)
  - [[../decisions/0008-cursor-delegation-by-maintenance-level.md]](Cursor 委譲判定)
  - [[../decisions/0011-directory-restructure-captures-self.md]](Level 4 の例)
- **関連 spec**: 
  - [[./abstract-generation.md]](抽象生成の並行運用)
  - [[./handoff-mechanism.md]](Level 3 の月次アーカイブ)
- **実装**: `vault-templates/00_meta/vault_maintenance_config.md`(cadence 設定)

## Change Log

- 2026-07-13: 初版(4 レベルの詳細仕様確定)

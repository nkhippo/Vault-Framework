---
audience: adopter
created: 2026-07-14 09:20:00+09:00
keywords:
- setup
- customization
- vocabulary-extension
- templates
- skill-adjustment
- iteration
status: published
summary: Vault-Framework の初期セットアップ完了後、自分の運用に合わせて Vault をカスタマイズする方法。統制語彙の拡張、テンプレートの追加、Skill
  の調整、Vault 構造のカスタマイズを扱う。
tags:
- setup
- customization
title: カスタマイズ
type: setup
updated: 2026-07-14 09:20:00+09:00
id: pj-2026-07-13-e55f
aliases:
- pj-2026-07-13-e55f
---

## Summary

Vault-Framework の初期セットアップ完了後、自分の運用に合わせて Vault をカスタマイズする方法。統制語彙の拡張、テンプレートの追加、Skill の調整、Vault 構造のカスタマイズを扱う。

## Design Principle

**「使いながら育てる」**。初期状態のまま運用開始し、必要になった時に少しずつ拡張する。過度に前もって設定しない。

## Customization 1: 統制語彙(vocabulary.md)の拡張

### 新規プロジェクトを追加

新規 GitHub リポジトリを作成した時、以下を更新:

1. **vocabulary.md の project セクション** に新規プロジェクト名を追加
2. **project_aliases.md** に新規プロジェクトのエントリを追加
3. **30_projects/<NewRepoName>/** ディレクトリを作成
4. 該当プロジェクト用の README、design-decisions、handoff/current-state.md を作成

### 新規 tag の追加

3 ファイル以上で同じキーワードが tag として自然に浮かんできたら追加:

```markdown
### プロジェクト系(導入者が追加)

- `your-project-tag`  # 例: プロジェクト固有の tag
```

追加後、過去ファイルへの遡及適用は不要(前方互換)。

### 新規 type の追加

- 既存 type で対応できない事例が 3 件以上蓄積されたら追加検討
- ADR を作成して意思決定を記録
- vocabulary.md に追加
- 対応する template を `00_meta/templates/<type>.md` に作成

## Customization 2: テンプレートの追加

### 独自 template の作成

例: `weekly-summary` type を追加する場合

1. `vocabulary.md` の type に `weekly-summary` を追加
2. `frontmatter-schema.md` に追加必須フィールドを追記
3. `00_meta/templates/weekly-summary.md` を作成:

```markdown
---
title: 
created: 
updated: 
type: weekly-summary
status: published
summary: 
week_of: YYYY-WW
tags: [weekly, summary]
---

## Summary

<今週の概要>

## 主な出来事

## 学び

## 来週の計画
```

## Customization 3: ディレクトリ構造の追加

### 新規トップレベルディレクトリ

例: `60_reference/` を追加する場合

1. `00_meta/vault_structure.md` に新規ディレクトリを追記
2. 該当ディレクトリを作成(`.gitkeep` 配置)
3. `00_meta/vault_index.md` に新規ディレクトリの説明を追加

### 中階層の分類

例: `40_knowledge/programming-language/` サブディレクトリ

- 特別な設定なしに作成できる
- 参照時は `40_knowledge/programming-language/` として認識される

## Customization 4: Skill の調整

### SKILL.md の編集

Framework の canonical をベースに、自分の運用に合わせて調整:

1. Framework から `skills/vault-manager/SKILL.md` をダウンロード
2. 必要な調整を実施(発火 phrase の追加、判定フローのカスタマイズ等)
3. zip 化して再アップロード

### よくあるカスタマイズ

- **発火 phrase の追加**: 自分の口癖(「保存しといて」等)を追加
- **保存判断フローの調整**: 独自の type や領域への保存判断
- **参照レベルの調整**: 独自のプロジェクトカテゴリでの参照ルール

## Customization 5: 保守運用の cadence

### vault_maintenance_config.md の編集

`00_meta/vault_maintenance_config.md` で保守運用の頻度を調整:

```yaml
maintenance_levels:
  level_1_daily_on_save: true      # 保存時の自動修正
  level_2_weekly_batch: true       # 週次バッチを ON(初期は false)
  level_3_monthly_check: false     # 月次チェック
  level_4_seasonal_migration: false # 季節補正
```

### 段階的な有効化

推奨する段階:

1. **初期(セットアップ直後)**: Level 1 のみ
2. **1 ヶ月後**: Level 2(週次バッチ)を追加
3. **3 ヶ月後**: Level 3(月次チェック)を追加
4. **半年後**: Level 4 の初回実施

## Customization 6: 50_self/ の拡張

### 個人領域の追加

50_self/ 配下に独自のサブディレクトリを追加可能:

- `50_self/health/`(健康記録)
- `50_self/finance/`(財務記録)
- `50_self/hobby/`(趣味の記録)

**注意**: すべて sensitive: true 扱い(claude_operation_rules.md の該当セクション参照)

## Customization 7: 抽象生成の対象範囲

### vault_maintenance_config.md での設定

```yaml
abstract_generation:
  enabled: true                  # 抽象生成を有効化
  source_dirs: 
    - "10_chat_logs/"
    - "30_projects/*/logs/"
  exclude_paths:
    - "50_self/"                 # センシティブ領域は除外
    - "90_inbox/"
  target_types:
    - "chat_log"
    - "project_design"
  minimum_length_chars: 500       # 短すぎる chat_log は対象外
```

## Customization 8: 命名規約の調整

### 独自の命名パターン

Framework の推奨(`YYYY-MM-DD_kebab-slug.md`)に対して、独自の命名を使う場合:

- `naming_conventions.md` を編集
- Skill(SKILL.md)も同様に調整
- ただし、Skill との整合を必ず取る(乖離は判定ミスの原因)

## Customization 9: Custom Instructions の拡張

Claude Projects の Custom Instructions を活用:

- 応答スタイル(丁寧、砕けた等)
- 出力形式(Markdown、Plain text)
- 特定の観点(セキュリティ重視、パフォーマンス重視等)

Instructions とは別に、より Chat レベルでの調整を行う。

## Customization 10: Fable マニュアル化(将来)

### Framework の Public 化

自分の Vault-Framework をベースに、他人にも使えるパッケージを作る:

1. 個人情報を完全に除去(Naoya のパターンを参考)
2. `<your-*>` プレースホルダで汎用化
3. GitHub で Public リポジトリとして公開
4. README で導入方法を明示
5. Fable(Anthropic の Framework 配布形式)で登録

## Best Practices

### DO(推奨)

- 使いながら気づいた時に少しずつ調整
- ADR で意思決定を記録(自分用の ADR)
- vocabulary.md の拡張手順に従う
- Skill と vault の整合を保つ

### DON'T(非推奨)

- 前もって過剰にカスタマイズ
- Skill と vault の乖離を放置
- 統制語彙違反を無視
- sensitive 領域の扱いを緩和

## Iteration Pattern

カスタマイズは 1 回で完成しない:

1. **初回セットアップ**: 最小限で運用開始
2. **1 週間後**: 気づいた点を調整
3. **1 ヶ月後**: 統制語彙を拡張、Level 2 を有効化
4. **3 ヶ月後**: 独自の template や type を追加
5. **半年後**: Fable マニュアル化を検討

## References

- **関連 spec**: 
  - [[pj-2026-07-13-f5e9]](統制語彙の拡張手順)
  - [[pj-2026-07-13-d0dd]](保守運用の詳細)
- **関連 guideline**: 
  - [[pj-2026-07-13-988d]](日常運用パターン)
- **実装**: `vault-templates/00_meta/`(カスタマイズ対象の canonical)

## Next Step

問題が発生した時は [[pj-2026-07-13-e32c|troubleshooting.md]] を参照してください。

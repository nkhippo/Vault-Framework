---
audience: mixed
created: 2026-07-14 08:25:00+09:00
keywords:
- sonnet
- sonnet-5
- optimization
- prompt-engineering
- guidelines
- structural-modification
- prompt-caching
related_adrs:
- '0014'
status: published
summary: Anthropic が Sonnet 5 を標準モデルとして推進する動向に対応した最適化ガイド。ADR-0014 のプロンプト工夫 5 個 + 構造修正
  4 点を具体的な実装レベルで詳述。
tags:
- guideline
- sonnet
- prompt-engineering
title: Sonnet 5 最適化
type: guideline
updated: 2026-07-14 08:25:00+09:00
id: pj-2026-07-13-b12c
aliases:
- pj-2026-07-13-b12c
---

## Summary

Anthropic が Sonnet 5 を標準モデルとして推進する動向に対応した最適化ガイド。ADR-0014 のプロンプト工夫 5 個 + 構造修正 4 点を具体的な実装レベルで詳述。Sonnet 5 特有の特性を活かしつつ、Opus 使用時にも品質改善となる汎用的な最適化。

## Scope

このガイドラインが規定するもの:

- Sonnet 5 特有の特性と対応方針
- プロンプト工夫 5 個の具体的実装
- 構造修正 4 点の具体的実装
- Opus 使用時への影響と副次的品質改善
- 将来のモデル更新への追随方針

このガイドラインが規定しないもの:

- Sonnet 5 標準化の意思決定背景(ADR-0014 参照)
- 個別 spec の実装(該当 spec 参照)

## Design Principle

**「Sonnet 5 対応 = 明示性と一貫性の向上」**。以下 3 原則:

1. **暗黙より明示**: 微妙なニュアンスに頼らず、直接的な指示
2. **順序の固定**: 判断ロジックのブレを最小化
3. **副次効果の活用**: Sonnet 5 対応の変更が Opus でも品質改善になる

## Sonnet 5 特有の特性(観察)

以下の特性を踏まえた対応が必要:

### Response length の傾向

- **観察**: Sonnet 5 は Opus 4.7 に比べて簡潔な応答を生成する傾向
- **影響**: 詳細な説明が省略される可能性、判断過程が見えにくくなる
- **対応**: 明示的な指示で「詳細に説明せよ」と誘導、Skill 側で必要な粒度を規定

### Reasoning の質

- **観察**: 複雑な多段階の判断で、Opus と比較して若干のブレが出る可能性
- **影響**: 保存判断・参照判断の一貫性が下がる可能性
- **対応**: 判定フローを番号付きで明示、境界事例を具体例で説明

### プロンプト解釈

- **観察**: 微妙なニュアンスへの感度が Opus と若干異なる
- **影響**: 「なるべく〜」「基本的には〜」等の曖昧な指示の解釈がぶれる
- **対応**: 「絶対に禁止」「必ず〜」等の強い表現、明示的な優先順位

### prompt caching への相性

- **観察**: 同じ文脈のキャッシュヒット率が Opus より高い傾向
- **影響**: 順序を固定するとキャッシュ効率が大幅に向上
- **対応**: ファイル読み込みの固定順序を明示

## Prompt 工夫 1: 明示的な優先順位の記述

### 実装

SKILL.md 冒頭に以下を明示:

```markdown
## 優先順位ルール

- 通常: Skill > Vault > Instructions
- 統制語彙・命名規約・テンプレ形式: Vault 優先
- MCP 接続失敗、Level 0 厳格化、sensitive 引用禁止: Skill 優先
```

### 効果

- Sonnet 5 の暗黙のニュアンス推測を回避
- Opus 使用時にも判断のブレを最小化

## Prompt 工夫 2: 参照レベルの数値化と明示

### 実装

reference-level-system.md および SKILL.md で:

```markdown
## 参照レベル(0〜4)

- Level 0: 参照しない(デフォルト、明示的トリガーがない限り)
- Level 1: 最小参照(00_meta/ の必要ファイル)
- Level 2: プロジェクト情報(README、design-decisions 等)
- Level 3: 過去記録の検索
- Level 4: 全文精読
```

Level 遷移条件を番号付きで明示。

### 効果

- 「今 Level 何?」を Skill が明確に把握
- Sonnet 5 が「なんとなく」で参照レベルを上げるのを防ぐ

## Prompt 工夫 3: 「絶対禁止」表現の明確化

### 実装

MCP 接続失敗時のルール等、絶対に守るべき事項:

```markdown
## MCP 接続失敗時(絶対に禁止)

- Claude の一般知識や訓練データから憶測で補って処理を続けること
- 前回セッションの記憶やキャッシュから補って処理を続けること
- vault の想定される内容を推定して処理を続けること
```

「なるべく」「原則」等の表現を避け、「絶対に禁止」を明示。

### 効果

- Sonnet 5 の判断でフォールバック挙動を取らない
- prompt injection への防御を強化

## Prompt 工夫 4: 具体例と反例の併記

### 実装

保存判断フローで、境界事例を具体例で説明:

```markdown
## chat_log vs 日記の判定

**chat_log として保存する例**:
- 「今日 MCP プラットフォームについて議論した」→ chat_log
- 「Vault の設計判断を Claude と検討した」→ chat_log

**日記として保存する例**:
- 「今日は疲れたけど、Vault が完成に近づいて嬉しい」→ diary
- 「今日あったこと: 発表準備、家族との時間」→ diary

**判定に迷う例**:
- 「今日は Vault の設計をした感想」→ 主に感想なら diary、主に設計内容なら chat_log
```

### 効果

- Sonnet 5 の推論 gap を埋める
- 判定の一貫性を向上

## Prompt 工夫 5: prompt caching への配慮ルール

### 実装

SKILL.md に以下を明示:

```markdown
## Prompt caching への配慮

Level 1 で複数の 00_meta ファイルを読む時は、常に以下の固定順序:

1. 00_meta/vault_structure.md
2. 00_meta/naming_conventions.md
3. 00_meta/vocabulary.md
4. 00_meta/frontmatter_schema.md(必要時のみ)
5. 00_meta/project_aliases.md(あいまい名解決時のみ)
6. 00_meta/templates/<type>.md(保存時のみ)

同一 Chat 内で既に読んだファイルは再取得しない。
```

### 効果

- Sonnet 5 の cache ヒット率を最大化
- 2 ターン目以降のレスポンス高速化

## 構造修正 1: 統制語彙の重複排除

### 実装

vocabulary.md の記述を厳格化:

- 同義語を作らない(例: `chat_log` と `chat-log` を並列にしない)
- カテゴリを明確に分ける(技術系、コンテンツ系、プロジェクト系、個人系、メタ系)
- 拡張手順を明示(vocabulary-design.md)

### 効果

- Sonnet 5 の推論で同義語を混在させない
- 検索精度の向上

## 構造修正 2: Front Matter スキーマの明確化

### 実装

frontmatter-schema.md で:

- 必須・任意フィールドを表形式で明示
- type ごとの追加必須フィールドを明示
- YAML 記述ルールを明示

### 効果

- 「なんとなくで埋める」のブレを最小化
- Sonnet 5 の生成する Front Matter が一貫

## 構造修正 3: あいまい名解決のフローチャート化

### 実装

project_aliases.md を以下の統一形式で:

```markdown
### <RepoName>

- 正式リポジトリ名: `<RepoName>`
- カテゴリ: <カテゴリ>
- 通称: <カンマ区切り>
- 機能キーワード: <カンマ区切り>
- 対象言語: <該当する場合>
- 一言メモ: <1-2 行>
```

各エントリを厳密に統一。

### 効果

- Sonnet 5 が「候補が 1 個 or 複数」を明確に判定
- あいまい名解決フローの精度向上

## 構造修正 4: handoff/current-state.md の見出し統一

### 実装

全プロジェクトの current-state.md で以下の見出しを統一:

- Summary
- 現在のフェーズ
- 直近の重要決定
- 実施済み構造
- 未解決の論点
- 直近のアクション
- 関連ファイル
- 他 Chat からのキャッチアップ手順

### 効果

- Sonnet 5 が構造化された情報を素早く parse
- 複数プロジェクトの状態比較が容易

## Opus 使用時への影響

Sonnet 5 対応の 9 項目は、Opus 使用時にも副次的な品質改善をもたらす:

- **プロンプト工夫 1-3**: 明示性の向上は Opus でもブレを減らす
- **プロンプト工夫 4**: 境界事例の具体例は判定精度を向上
- **プロンプト工夫 5**: prompt caching は Opus でも有効(効果は Sonnet 5 より小さい)
- **構造修正 1-4**: 統制語彙・スキーマ・フローチャート化は普遍的な品質改善

## 将来のモデル更新への追随

Anthropic の将来のモデル更新(Sonnet 6、Opus 5 等)への対応方針:

### モデル特性の観察

- 新モデルリリース時、以下を観察:
  - Response length の傾向
  - Reasoning の質
  - プロンプト解釈のニュアンス
  - prompt caching への相性

### 追加対応の判断

- 現行の 9 項目(プロンプト工夫 5 + 構造修正 4)で対応可能か
- 新たな対応が必要な場合、この guideline を supersede する新版を作成

### バージョン管理

- Skill.md の Change Log で「Sonnet 5 対応」等を明示
- Framework の decisions/ に対応 ADR を追加

## Implementation Checklist

Sonnet 5 対応が完了しているかのチェックリスト:

- [ ] SKILL.md 冒頭に優先順位ルールを明示
- [ ] 参照レベル(0-4)を番号付きで明示
- [ ] 「絶対禁止」表現を該当箇所に使用
- [ ] 保存判断フローに境界事例の具体例を追加
- [ ] Prompt caching の固定順序を SKILL.md に明示
- [ ] vocabulary.md の同義語を排除
- [ ] frontmatter-schema.md で type 別必須フィールドを表形式化
- [ ] project_aliases.md のエントリ形式を統一
- [ ] 全プロジェクトの current-state.md の見出しを統一

## References

- **関連 ADR**: [[pj-2026-07-13-d3c5]]
- **関連 spec**: 
  - [[pj-2026-07-13-dd44]](プロンプト工夫 2)
  - [[pj-2026-07-13-9fa5]](構造修正 2)
  - [[pj-2026-07-13-f5e9]](構造修正 1)
  - [[pj-2026-07-13-47fd]](構造修正 3)
  - [[pj-2026-07-13-c1bd]](構造修正 4)
- **関連 guideline**: 
  - [[pj-2026-07-13-fba6]](Principle 9: prompt caching)

## Change Log

- 2026-07-13: 初版(Sonnet 5 対応 9 項目の詳細)
- 2026-07-14: v1.1 で prompt caching 対応と Skill 実装への反映を強化

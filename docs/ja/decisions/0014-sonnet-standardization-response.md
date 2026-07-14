---
audience: mixed
created: 2026-07-14T05:00:00+09:00
date: 2026-07-13
id: adr-0014
keywords:
  - sonnet
  - sonnet-5
  - opus
  - standardization
  - prompt-engineering
  - response-length
  - prompt-caching
related_adrs:
  - "0003"
related_chats:
  - 10_chat_logs/2026/07/2026-07-13_maintenance-operation-design.md
related_specs:
  - reference-level-system
status: accepted
summary: Anthropic が Sonnet 5 を標準モデルとして推進する動向に対応し、Vault 運用の Chat 体験を維持するため、プロンプト工夫 5 個 + 構造修正 4 点で対応する意思決定。Sonnet 5 特有の特性を踏まえて Skill と vault の記述を調整。
superseded_by: null
supersedes: null
tags:
  - adr
  - sonnet
  - prompt-engineering
title: "ADR-0014: Sonnet 5 標準化への対応"
type: adr
updated: 2026-07-14T05:00:00+09:00
---

## Summary

Anthropic が Sonnet 5 を標準モデルとして推進する動向に対応し、Vault 運用の Chat 体験を維持するため、プロンプト工夫 5 個 + 構造修正 4 点で対応する意思決定。Sonnet 5 特有の特性(response length の傾向、reasoning の質)を踏まえて Skill と vault の記述を調整。

## Context

Anthropic は Sonnet 5(claude-sonnet-5)を標準モデルとして推進する動向を見せている(2026 年時点)。従来 Opus 4.7 を主軸として Vault 運用していたが、Sonnet 5 に切り替わった場合の以下影響が懸念された:

- **Response length の傾向**: Sonnet 5 は Opus に比べて簡潔な応答を生成する傾向(前後関係の推論は同等〜優位、ただし出力量は控えめ)
- **Reasoning の質**: 複雑な多段階の判断において、Opus と比較して若干のブレが出る可能性
- **プロンプト解釈**: 微妙にニュアンスが異なる指示への感度が異なる可能性
- **保存判断・参照判断への影響**: Vault の Skill が Sonnet 5 で正しく発火するか、判定フローが機能するか

Sonnet 5 標準化は Vault の運用体験に直接影響するため、事前に対応策を用意する必要がある。実験的に Sonnet 5 で Vault を運用してみた結果を元に、以下 9 項目の対応を確定した。

## Decision

**プロンプト工夫 5 個 + 構造修正 4 点で対応**

### プロンプト工夫(SKILL.md および 00_meta 側の記述改善)

#### プロンプト 1: 明示的な優先順位の記述

「Skill > Vault > Instructions」の 3 者優先順位を SKILL.md 冒頭に明示。Sonnet 5 は暗黙のニュアンスを推測するより明示的な指示を優先する傾向があるため。

#### プロンプト 2: 参照レベルの数値化と明示

Level 0〜4 の 5 段階を SKILL.md で番号付きで明示化。「明示的トリガーがない限り Level 0」というルールを強調。

#### プロンプト 3: 「絶対禁止」表現の明確化

MCP 接続失敗時の禁止事項(憶測での続行禁止)を「絶対に禁止する」と強い表現で明示。Sonnet 5 の判断で誤ってフォールバック挙動を取らないように。

#### プロンプト 4: 具体例と反例の併記

保存判断フローで、「これは chat_log」「これは日記」の判定に具体例と反例を併記。境界事例を Sonnet 5 が推論する際の gap を減らす。

#### プロンプト 5: prompt caching への配慮ルール

Anthropic prompt caching を活かすため、ファイル読み込みの固定順序を SKILL.md で明示。Sonnet 5 は同じ文脈のキャッシュヒット率が高い傾向があり、この最適化の効果が大きい。

### 構造修正(vault 側の記述改善)

#### 構造修正 1: 統制語彙の重複排除

vocabulary.md の type / status / tags の定義を厳格化し、同義語や別表現を削除。Sonnet 5 の推論で同義語を混在させないため。

#### 構造修正 2: Front Matter スキーマの明確化

frontmatter_schema.md で type ごとの必須・任意フィールドを表形式で明示。「なんとなくで埋める」のブレを減らす。

#### 構造修正 3: あいまい名解決のフローチャート化

project_aliases.md でエイリアスと機能キーワードを 1 プロジェクト 1 セクションで統一。Sonnet 5 が「候補が 1 個 or 複数」を明確に判定できる形に。

#### 構造修正 4: handoff/current-state.md の見出し統一

全プロジェクトの current-state.md で「Summary → 現在のフェーズ → 直近の重要決定 → 実施済み構造 → 未解決の論点 → 直近のアクション → 関連 → キャッチアップ手順」の見出しを統一。Sonnet 5 が構造化された情報を素早く parse できるように。

## Consequences

**Positive**:

- Sonnet 5 でも Opus と同等の Vault 運用体験を維持
- プロンプトの明示性が全体的に上がり、Opus 使用時にも判断のブレが減る(結果的に品質向上)
- 統制語彙・スキーマ・handoff 構造の統一で、Cursor 委譲時の指示書作成も高速化
- Anthropic の将来のモデル更新(Sonnet 6、Opus 5 等)への追随コストが下がる

**Negative**:

- SKILL.md の文字数が増加(明示的な記述が増えるため)
- プロンプト caching の恩恵は受けやすくなるが、初回セッションの起動コストは若干増加
- Sonnet 5 特有の対応が Opus 使用時に「過剰」に感じられる可能性

**Mitigation**:

- SKILL.md の文字数増加は、Skill レベルでは実質無視できる(初回のみで、以降キャッシュ)
- Opus 使用時にも「明示性の向上」は品質改善なので、過剰と感じる部分は文脈で判断
- 将来 Sonnet 6 等で新たな特性が観察されたら、この ADR を supersede する

## Alternatives Considered

### 案 A: 対応せず、Opus 継続を前提とする

Sonnet 5 標準化に対応せず、Opus を明示的に選択して使い続ける案。

**却下理由**:

- Opus は使用制限や料金が Sonnet より厳しい傾向(2026 時点)
- Anthropic の推奨に逆行する運用は、ドキュメントとの整合が取りにくくなる
- Sonnet 5 でも運用できる形にしておく方が、将来の変化に柔軟

### 案 B: Sonnet 5 用の別 Skill を用意

Sonnet 5 専用の別 SKILL.md を作成する案。

**却下理由**:

- Skill の 2 系統管理は同期コストが高い
- Sonnet と Opus の両方で使える共通 Skill の方が保守性が高い
- 対応 5+4 項目は Sonnet 特化ではなく、Opus 使用時にも品質向上

### 案 C: 対応を大幅に縮小(1-2 項目のみ)

対応項目を絞り、最小限の変更にする案。

**却下理由**:

- Sonnet 5 の特性を踏まえた対応は、9 項目の相互作用で効果を発揮
- 一部だけ実施すると、境界事例で振る舞いの一貫性が保てない

## Related

- **前提 ADR**: 
  - ADR-0003(Skill・Project・Vault の 3 層アーキ、Skill の記述改善の対象)
- **後続 ADR**: なし
- **関連 spec**: 
  - `../guidelines/sonnet-optimization.md`(Sonnet 5 対応の詳細ガイドライン)
  - `../specs/reference-level-system.md`(参照レベル 5 段階、プロンプト 2 の対応)
- **元記録**: `10_chat_logs/2026/07/2026-07-13_maintenance-operation-design.md`
- **実装**: 
  - SKILL.md v1.1(2026-07-13):構造修正 4 点をほぼ反映済み、プロンプト工夫 5 個は部分反映

## Change Log

- 2026-07-13: 初版(Sonnet 5 対応 9 項目確定)
- 2026-07-13: SKILL.md v1.1 で構造修正 4 点を反映

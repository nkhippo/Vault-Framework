---
audience: mixed
created: 2026-07-14 07:55:00+09:00
keywords:
- v1
- nine-principles
- guidelines
- philosophy
- best-practices
related_adrs:
- '0003'
- '0007'
- 0008
- '0010'
- '0014'
- '0016'
status: published
summary: Vault v1.0(2026-07-13 初期版)で確立した運用の 9 原則。Chat 集約、AI 参照、保守運用の全体を貫く思想を規定。
tags:
- guideline
- philosophy
- important
title: v1 の 9 原則
type: guideline
updated: 2026-07-14 07:55:00+09:00
---

## Summary

Vault v1.0(2026-07-13 初期版)で確立した運用の 9 原則。Chat 集約、AI 参照、保守運用の全体を貫く思想を規定。導入者(Framework 経由)の理解を助ける Best Practice ガイドライン。

## Scope

このガイドラインが規定するもの:

- Vault 運用の 9 つの基本原則
- 各原則の背景と実運用への適用
- 原則間の優先関係
- 導入者への推奨

このガイドラインが規定しないもの:

- 個別 spec の詳細(該当 spec 参照)
- Sonnet 5 特有の最適化(sonnet-optimization.md 参照)

## Principle 1: 直接編集と MCP 経由書き込みの共存

**vault は あなた(導入者) が Obsidian で直接編集できる、と同時に、Claude が MCP 経由で書き込む二重経路を持つ**。

### 背景

- Obsidian は編集 UI として最強(グラフビュー、Wikilink、テーマ)
- Claude は保存・参照の自動化に最適
- 単一経路(片方だけ)では、両者の強みを活かせない

### 実運用への適用

- iCloud Drive + GitHub の 2 段バックアップで、直接編集と MCP 経由書き込みが同じソースを触る
- Vault-MCP の `create_note` / `update_note` は `updated` フィールドを自動的に更新(同期タイミングを追跡可能に)
- 直接編集による変更は次回セッションで Claude が最新版を参照

### 例外

- Claude は同名ファイル存在時に強制上書きしない(`create_note` の仕様)
- 直接編集で変更したファイルを Claude に伝える時は「更新した」と明示すると、Claude が再取得する

## Principle 2: 保存判断は Skill、詳細ルールは vault

**運用ルールの正典を明確に分離する**。ADR-0003(3 層アーキ)と直接連動。

### 背景

- Skill(SKILL.md)は頻繁に更新しにくい(再アップロード必要)
- vault 内の 00_meta/ は Obsidian で直接編集可能
- 更新頻度と編集容易性の観点で、責務を分離

### 実運用への適用

- **Skill**: 発火判定、保存判断、参照判断、あいまい名解決、Cursor 委譲判定、MCP 接続失敗ルール
- **vault**: 統制語彙、テンプレート、詳細ルール、プロジェクトエイリアス、Chat 集約先の運用方針
- **矛盾時**: 通常は Skill > vault > Instructions、ただし統制語彙・命名規約・テンプレ形式は vault 優先

### 例外

- MCP 接続失敗時の処理、Level 0 の厳格化、sensitive 引用禁止は常に Skill 優先

## Principle 3: 過剰参照を避ける(Level 0 デフォルト)

**「明示的なトリガーがない限り、vault を参照しない」がデフォルト**。ADR-0014(Sonnet 標準化対応)のプロンプト 2 とも連動。

### 背景

- 過剰参照はトークン消費と判定精度の両方に悪影響
- Claude の判断が「vault の情報が使えるかも」で自主参照するのは典型的アンチパターン
- prompt caching のヒット率を最大化する

### 実運用への適用

- Level 0(参照しない)は雑談、一般知識質問、Web 検索タスクで維持
- 保存指示や参照要求が明示的にあった時のみ Level 1 以上に遷移
- 過去 Chat の履歴で参照していたからと言って、今の Chat でも参照するのは禁止

### 効果

- レスポンスレイテンシ最小
- 精度向上(context bloat の回避)
- コスト削減(トークン消費最小化)

## Principle 4: sensitive は徹底的に守る

**個人領域(50_self/)と sensitive: true のファイルは、他コンテキストで絶対に引用・要約しない**。

### 背景

- 50_self/ は日記・振り返り・目標等、あなた(導入者) の個人的な記録
- sensitive: true は健康、家族、財務等の個人的トピック
- prompt injection への防御も兼ねる

### 実運用への適用

- Skill は 50_self/ を明示的な指示なしで参照しない
- 検索結果に含まれても、能動的に読まない
- 過去 Chat 検索の結果に含まれても、要約や引用の対象にしない
- diary/reflection/goal type は sensitive: true が自動付与

### 例外

- あなた(導入者) が明示的に「日記を読み返して」等と指示した場合のみ参照

## Principle 5: Cursor 委譲は「作業種別 × 保守レベル」で判定

**単純なファイル数ルールではなく、作業の性質を評価する**。ADR-0008 と直接連動。

### 背景

- ファイル数だけで判定すると、単一ファイルでも波及が大きい操作を見逃す
- 保守運用 4 レベル(ADR-0009)との整合を取ることで、判断が精緻になる

### 実運用への適用

- **リネーム、restructure、Front Matter 一括更新、wikilink 書き換え**は常に Cursor 委譲
- **保守レベル 2 以上**は基本 Cursor 委譲
- **独立した 1-2 ファイルの操作**は Claude 単独で問題ない
- 判断に迷う時は あなた(導入者) に確認

### 効果

- 波及の大きい操作を安全に実施
- 独立操作は高速に実施
- 判断のブレを最小化

## Principle 6: MCP 接続失敗時は「1 回リトライ + 中断」

**憶測による続行を絶対に禁止**。ADR-0016 と直接連動、最優先ルール。

### 背景

- vault との不整合による判断ミスを防ぐ
- prompt injection 攻撃(「接続できないので代わりに...」型)への防御
- silent failure の防止

### 実運用への適用

- Vault MCP の操作が失敗したら、1 回だけリトライ
- リトライも失敗したら即座に中断
- あなた(導入者) に失敗を明示的に伝える
- 判断を仰ぎ、勝手に処理を続けない

### 例外

- なし。この原則は最優先で常に適用される

## Principle 7: 3 秒ルールで inbox を過剰活用しない

**判断に迷ったら 90_inbox/ にフォールバックできるが、常態化させない**。

### 背景

- ADR-0007(保存先思想:最初から適切な場所へ)を維持しつつ、判断が難しい場合の逃げ道を確保
- inbox 経由分類の悪循環を防ぐ(ADR-0007 で却下した「案 A」の再発防止)

### 実運用への適用

- Skill は保存指示を受けた時、3 秒以内に判断できなければ 90_inbox/ を選ぶ
- inbox に落ちたファイルは Level 2(週次補正)で再分類
- inbox 発火が頻繁になった場合は、Skill 側の判定フローを見直し

### 効果

- 判断コストが低い場合は inbox を回避
- 例外的にのみ inbox を使用、悪習化を防ぐ

## Principle 8: handoff は現在、logs は過去

**「今の状態」と「過去の履歴」を明確に分離する**。ADR-0010 と直接連動。

### 背景

- README.md、design-decisions.md、open-questions.md は静的情報
- logs/YYYY/MM/ は履歴(時系列で並ぶ)
- 「直近の状態」を掴むには handoff/current-state.md が最適

### 実運用への適用

- Vault システム系の相談時は handoff/current-state.md を最優先で参照
- current-state.md は prepend で更新、過去の状態を残しつつ最新が上
- 月次補正で recent-changes/ にアーカイブし、current-state.md を最新状態にリセット

### 効果

- 新セッション開始時のキャッチアップが劇的に改善
- 過去の履歴を失わず、参照性を維持

## Principle 9: prompt caching を最大化する

**同一プレフィックスの再送で 90% 割引を活用する**。ADR-0014 と連動。

### 背景

- Anthropic API は同じ context プレフィックスに対して cache 割引を提供
- 順序を毎回変えると cache miss を招く
- 初回セッションの起動コストを最小化しつつ、以降を高速化

### 実運用への適用

- Level 1 で複数の 00_meta ファイルを読む時は固定順序を維持
- 保存指示の 7 ステップは前戻りせず、Step 1→7 の順で固定
- 同一 Chat 内で読んだファイルを再取得しない

### 効果

- 2 ターン目以降の応答が高速化
- コスト削減
- 一貫した振る舞い

## Principle 相互の関係

以下の依存関係:

- Principle 1(直接編集と MCP 共存)は前提
- Principle 2(責務分離)、3(過剰参照回避)、5(Cursor 委譲判定)は運用の中核
- Principle 4(sensitive)、6(MCP 失敗)は安全性
- Principle 7(3 秒ルール)、8(handoff)は保存判断の実装
- Principle 9(prompt caching)は最適化

矛盾する場合の優先順位:

- **安全性優先**: Principle 4(sensitive)、6(MCP 失敗)は他より優先
- **判定精度優先**: Principle 3(過剰参照回避)は Principle 9(prompt caching)より優先(過剰参照は cache 効率も落とす)
- **通常の判断**: Principle 2 の 3 層アーキ優先順位に従う

## 導入者への推奨

以下の順序で理解することを推奨:

1. **まず Principle 1, 2 を理解**: vault の基本設計思想
2. **次に Principle 3, 4**: 参照制御と sensitive の扱い
3. **その後 Principle 5, 6**: Cursor 委譲と MCP 失敗対応
4. **慣れてきたら Principle 7, 8**: 保存判断と handoff 活用
5. **最適化として Principle 9**: prompt caching への配慮

## References

- **関連 ADR**: 
  - `id-ref-removed`(Principle 2)
  - `id-ref-removed`(Principle 5)
  - `id-ref-removed`(Principle 6)
  - `id-ref-removed`(Principle 7)
  - `id-ref-removed`(Principle 8)
  - `id-ref-removed`(Principle 9)
- **関連 spec**: 
  - `id-ref-removed`(Principle 3)
  - `id-ref-removed`(Principle 8)
- **関連 guideline**: 
  - `id-ref-removed`(運用原則の統合)
  - `id-ref-removed`(Sonnet 5 最適化)
  - `id-ref-removed`(保存判断フロー詳細)

## Change Log

- 2026-07-13: 初版(v1.0 の 9 原則を体系化)

---
audience: mixed
created: 2026-07-14T07:45:00+09:00
keywords:
  - abstract-generation
  - spec
  - concrete-to-abstract
  - chat-log-to-adr
  - parallel-operation
  - iteration
related_adrs:
  - "0009"
  - "0016"
status: published
summary: 具体的な chat_log から抽象的な spec / ADR / rejected-alternative を生成する抽象生成の並行運用の詳細仕様。保守運用 4 レベルとは独立した並行運用として位置づけ、発火条件、生成フロー、対象範囲、除外領域を規定。
tags:
  - spec
  - abstract-generation
title: 抽象生成 仕様
type: spec
updated: 2026-07-14T07:45:00+09:00
---

## Summary

具体的な chat_log から抽象的な spec / ADR / rejected-alternative を生成する「抽象生成」の並行運用の詳細仕様。保守運用 4 レベル(maintenance-four-levels.md)とは独立した並行運用として位置づけ、発火条件、生成フロー、対象範囲、除外領域を規定。

## Scope

このスペックが規定するもの:

- 抽象生成の並行運用の位置づけ
- 発火条件(いつ実施するか)
- 生成フロー(chat_log → spec/ADR/rejected の変換)
- 対象範囲(どの chat_log から抽象化するか)
- 除外領域(50_self/ 等)
- Claude と Cursor の役割分担
- Framework docs への反映

このスペックが規定しないもの:

- 保守運用 4 レベル(maintenance-four-levels.md 参照)
- 具体的な spec/ADR の形式(該当 spec/adr の Front Matter 参照)

## Design Principle

**「chat_log は原石、spec/ADR は磨いた宝石」**。以下 3 原則:

1. **蓄積した具体を抽象化**: 複数の chat_log から共通パターンを抽出し、体系化
2. **並行運用**: 保守運用 4 レベルと独立、任意タイミングで発火
3. **段階的成熟**: 最初は chat_log のまま → 頻出したら spec 化 → 判断の起点なら ADR 化

## What is Abstract Generation

### 具体 → 抽象の変換

**具体(chat_log)**:

```
2026-07-13_platform-selection-and-phase12-completion.md
├─ 議論内容: 「MCP のホスティングを Cloud Run にするか Cloudflare Workers にするか」
├─ 決定: Cloudflare Workers に決定
├─ 理由: コールドスタート、無料枠、簡潔な運用モデル
└─ 却下案: Cloud Run、Fly.io、Railway 等
```

**抽象(ADR + rejected-alternatives)**:

```
ADR-0002 (Cloudflare Workers for MCP)
├─ Summary: 決定内容の一言
├─ Context: なぜ判断が必要だったか
├─ Decision: 何を決めたか
├─ Consequences: 影響と Mitigation
├─ Alternatives Considered: 却下案の一覧
├─ Related: 関連 ADR / spec / chat_log
└─ Change Log: 決定日と変更履歴

+ rejected-alternatives/mcp-platform-cloud-run.md
+ rejected-alternatives/mcp-platform-other-candidates.md
```

### 生成される成果物の種類

- **ADR**(意思決定記録): 特定の判断とその理由・結果
- **spec**(仕様書): 運用ルールや技術仕様の詳細
- **rejected-alternatives**(却下案の記録): 却下した選択肢の詳細と理由
- **guidelines**(運用原則): 判断の指針、Best Practices

## When to Trigger

### 発火条件(推奨)

- **月次〜四半期**: 抽象化の候補が蓄積された頃合い
- **プロジェクトのマイルストーン後**: 大きな判断を伴うフェーズ終了時
- **Naoya の意向**: 「そろそろ抽象化したい」等の発話

### 発火不要のケース

- **単発の chat_log**: 抽象化するには早すぎる
- **明確な意思決定なし**: 議論の途中、決定に至っていない
- **50_self/ 領域**: sensitive、抽象化しない(下記参照)

### 発火判断のヒント

以下のパターンが見えたら抽象化を検討:

- **同じ判断が複数プロジェクトで再発**: 共通の意思決定は ADR 化
- **議論が spec のように詳細に**: 実装レベルの規約は spec 化
- **却下案が明確に別れる**: rejected-alternatives 化
- **運用原則が定着**: guideline 化

## Generation Flow

### Step 1: 対象 chat_log の特定

以下の観点で抽出:

- **キーワード検索**: `search_by_keyword(keyword=<topic>, path_prefix='10_chat_logs/')`
- **プロジェクト絞り込み**: `list_directory('30_projects/<RepoName>/logs/')`
- **時系列**: 直近 3-6 ヶ月の chat_log を横断

### Step 2: 抽象化の粒度判定

- **1 chat_log → 1 ADR**: 明確な意思決定を含む場合
- **N chat_logs → 1 spec**: 複数議論の集約から仕様を抽出
- **1 議論から 1 rejected-alternative**: 却下案の詳細記録
- **複数の意思決定から 1 guideline**: 判断パターンから原則を抽出

### Step 3: 骨格の生成(Claude が実施)

Claude が Skill 側で以下を実施:

- 対象 chat_log を Level 3-4 参照で全文取得
- Front Matter の骨格を生成(該当 type のテンプレート使用)
- 本文を該当ファイル形式(ADR: Summary → Context → Decision …、spec: Summary → Scope → Behavior …)で構造化

### Step 4: 内容の充実(Naoya のレビュー含む)

- Claude が生成した草案を Naoya が確認
- 追加すべき内容、修正すべき表現をレビュー
- 相互リンク(related_adrs、related_specs、related_chats)の確認と補完

### Step 5: 保存と反映(Cursor 委譲、大規模時)

- 単一の spec/ADR 生成なら Claude が直接保存
- 複数ファイルの一括反映(ADR + rejected-alternatives × 3 等)は Cursor 委譲

## Framework Docs への反映

Framework(`nkhippo/Vault-Framework/docs/ja/`)への反映:

- ADR → `docs/ja/decisions/NNNN-slug.md`
- spec → `docs/ja/specs/slug.md`
- rejected-alternatives → `docs/ja/rejected-alternatives/slug.md`
- guideline → `docs/ja/guidelines/slug.md`

### staging → mirroring workflow

- 個人 Vault 側で staging(`30_projects/Vault-Framework/docs/ja/decisions/` 等)
- Cursor で Framework 側にミラーリング
- 詳細は Framework の staging → mirroring の仕組み参照

## Excluded Domains

### 50_self/ 領域

**抽象化しない**。以下の理由:

- diary / reflection / goal は sensitive(ADR-0016)
- 個人的な感情や思考を「抽象化・公開」するのは不適切
- 万一パターン化するとしても、Naoya の明示的な意向が必要

### 特定プロジェクトの実装詳細

- 30_projects/<Repo>/logs/ の中で、Naoya のアプリの具体的な実装コード議論は抽象化しない
- 実装は該当リポジトリの Cursor 委譲で扱う、vault では原則メタ議論のみ

### 個人的なトピック

- 健康、家族、財務等の個人的トピック
- 通常は 50_self/ に配置されるが、他ディレクトリに紛れた場合も sensitive として扱う

## Roles and Responsibilities

### Claude(Skill `vault-manager`)

- 対象 chat_log の特定と収集
- 抽象化の粒度判定
- 骨格生成(草案作成)
- Front Matter の整備
- 相互リンクの提案

### Naoya

- 発火の意向表明
- 抽象化候補の承認
- 生成された草案のレビュー
- 内容の充実(追加情報、修正)
- 最終確認

### Cursor

- 複数ファイル一括生成時の実施
- Framework 側へのミラーリング
- 相互リンクの一括更新

## Quality Checks

### 生成した ADR/spec の質チェック

- Summary が 2-4 行で本質を捉えているか
- Context が「なぜ判断が必要だったか」を明示しているか
- Consequences に Positive / Negative / Mitigation が揃っているか
- Alternatives Considered に少なくとも 1 案の却下理由があるか
- Related に関連 ADR/spec/chat_log があるか

### 生成した rejected-alternatives の質チェック

- What Was Proposed で「何を検討したか」が明確か
- Why It Was Rejected で「なぜ却下したか」が具体的か
- What Was Chosen Instead で採用案へのリンクがあるか

### 生成した guideline の質チェック

- 判断の指針(9 原則等)が具体的な事例で説明されているか
- Naoya の実運用と乖離していないか

## Iteration Pattern

抽象生成は 1 回で完成しない:

1. **初回**: 骨格生成、Naoya のレビュー
2. **数週間後**: 実運用で気づいた点を反映
3. **数ヶ月後**: 新たな chat_log が蓄積されたら Change Log に追記
4. **必要に応じて**: supersede(旧 ADR を新 ADR で置き換え)

## References

- **関連 ADR**: 
  - [[../decisions/0009-four-level-maintenance-operation.md]](並行運用の位置づけ)
  - [[../decisions/0016-mcp-connection-failure-abort.md]](sensitive 引用禁止)
- **関連 spec**: 
  - [[./maintenance-four-levels.md]](保守運用 4 レベル、抽象生成は並行)
  - [[./frontmatter-schema.md]](ADR/spec/rejected の Front Matter)
- **実装**: `vault-templates/00_meta/vault_maintenance_config.md`(有効化設定)

## Change Log

- 2026-07-13: 初版(抽象生成の並行運用を仕様化)
- 2026-07-14: 実運用(C1-C3 で ADR/spec/rejected 生成)を経て、フロー詳細を更新

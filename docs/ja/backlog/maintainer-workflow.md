---
id: pj-2026-07-17-74af
aliases:
- pj-2026-07-17-74af
title: Backlog Maintainer Workflow
type: knowledge
status: published
created: 2026-07-17T02:45:00+09:00
updated: 2026-07-17T02:45:00+09:00
tags: [backlog, workflow, skill, maintainer, maintenance]
summary: vault-maintainer が Level 2 週次メンテナンスで実行する backlog stalled detection の詳細規約。停滞 item の検出、tag/state 提案、Naoya 承認 gate。
---

# Backlog Maintainer Workflow

## Summary

vault-maintainer Skill が週次(Level 2)で実行する backlog stalled detection の詳細規約。周期的に停滞 item を検出し、Naoya に action 判断を促す。

## 位置付け(vault-manager との違い)

- **vault-manager の棚卸し flow(Phase 1c 参照 workflow)**: on-demand、Naoya の「棚卸しして」に応答
- **vault-maintainer の stalled detection**: 週次(または Naoya の「週次メンテ」トリガー)、周期的な自動検出

両者は補完関係。vault-manager は状態確認、vault-maintainer は停滞警告と action 提案。

## トリガー phrase

- 「週次メンテして」「week 系メンテ」「Weekly maintenance」等 → **週次メンテナンス flow の中で backlog stalled detection を実行**
- 「stalled 検出して」「停滞 backlog 見せて」等 → **stalled detection 単体実行**

## Level 1 追加読み込み

Stalled detection の初回検知時、以下を Level 1 で読み込み(Chat 内既読ならスキップ):

- Vault `00_meta/backlog_tags.md`

## Stalled detection flow

### Step 1: Scope 決定

- Default: 全 backlog(全 `30_projects/*/backlog/`、`_life/backlog/`、`_ideas/*/incubating/*/backlog/`)
- Naoya が特定プロジェクトを指定した場合はそれに絞る
- 例: 「IPASoundDrill の stalled 検出して」→ `30_projects/IPASoundDrill/backlog/` のみ

### Step 2: Threshold 決定

- Default: 14 日(2 週間)
- Naoya が「直近 1 週間動きがないもの」等と指定した場合は 7 日等に変更
- 明示指示なければ 14 日を採用

### Step 3: 一覧取得とフィルタ

1. `search_by_keyword(path_prefix='<target-path>', keyword='backlog_item')` で対象取得
2. 各 item の `get_frontmatter` で `state`, `updated`, `tags`, `assignee`, `github_issue`, `cursor_instruction_id`, `title`, `summary` を取得
3. **フィルタ条件**: `state: open` かつ `updated < today - threshold`
4. 該当 item を「stalled 候補」として集計

### Step 4: 既 stalled tag の分別

Stalled 候補を 2 グループに分ける:

- **A. Stalled tag 未付与**: 初めて停滞を検出、Naoya に stalled tag 付与を提案
- **B. Stalled tag 既付与**: 前回 stalled 判定済み、Naoya に state 変更(abandoned)or 「進捗確認要」を提案

### Step 5: 提案の生成

各 stalled 候補に対して以下を提案:

#### グループ A(stalled tag 未付与)

- 提案 1: `stalled` tag を付与、Naoya は次回まで追跡
- 提案 2: `state: abandoned` に、`abandoned_reason` を Naoya に確認
- 提案 3: 即時進捗確認(Naoya が別途対応)

#### グループ B(stalled tag 既付与)

- 提案 1: `state: abandoned` に(前回 stalled のまま今も停滞、放棄妥当)
- 提案 2: 「進捗を書いて再 open として stalled tag 削除」
- 提案 3: 「今は再開しない、stalled tag 継続」

### Step 6: 表形式提示

以下の列で Naoya に提示:

| # | Group | Title | Kind | Assignee | Last Updated | Days Stalled | GitHub | Suggested Action |

Group は A/B、Suggested Action は上記提案の要点。

### Step 7: Naoya 承認 gate

各 item に対して個別に Naoya の action を得る:

- 「これは tag 付けて」→ `update_note` で `tags` に stalled 追加、H2 History に追記
- 「これは abandoned に」→ `state: abandoned`、`abandoned_at`、`abandoned_reason`、H2 History
- 「これは skip」→ 変更なし、次へ
- 一括処理: 「全部 tag 付けて」等の一括指示も許容(慎重に確認)

**無断更新禁止**。Naoya の明示指示なしに変更しない。

### Step 8: 完了報告

「Stalled detection 完了:
- 検出: N 件(A 群 X、B 群 Y)
- 更新: stalled tag 付与 A、abandoned 化 B、skip C
- 次回検知タイミング: `<週次メンテ次回 or on-demand>`」

## GitHub Issue との相互作用

Stalled 候補が `github_issue` を持つ場合、対応 GitHub コネクタで Issue state を確認できるが:

- **作業混ざり防止規約遵守**: 対象プロジェクト以外の GitHub コネクタは能動使用しない
- 全体週次メンテでは複数コネクタ切り替えを許容(Naoya の週次メンテ指示 = 全プロジェクト対象の意思表示)
- Issue が既に closed & merged なのに Vault が open → stalled というより「同期漏れ」として `state: done` 提案

## 作業混ざり防止規約遵守

- 対象プロジェクト外の GitHub コネクタは Naoya 明示指示時のみ使用
- 50_self/ 領域には backlog がないため対象外
- 他 Skill の領域(vault-manager の save workflow 等)を侵さない

## 他の Level 2 週次メンテナンスタスクとの関係

vault-maintainer の既存 Level 2 タスク:

- リンク切れチェック
- Handoff アーカイブ
- (他、既存の maintenance-guide.md 参照)

**Stalled detection は Level 2 に追加**、これらと同じ「週次メンテ」の一環として実行される。

Weekly maintenance を Naoya が起動した時のフロー例:

1. 既存の Level 2 タスク実行(リンク切れ、handoff 等)
2. **Backlog stalled detection 追加実行**
3. 完了報告に stalled detection 結果も含める

## Related

- [[pj-2026-07-17-cb46|Backlog System Overview]]
- [[pj-2026-07-17-27e2|Reference Workflow]]
- [[pj-2026-07-17-64df|Save Workflow]]
- [[pj-2026-07-17-e2ef|ADR-0021 Vault-maintainer stalled detection]]
- Maintenance framework: `docs/ja/maintenance-guide.md`, [[pj-2026-07-13-d0dd|maintenance-four-levels]]
- Skill: `skills/vault-maintainer/SKILL.md`

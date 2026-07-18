---
title: Backlog Reference Workflow
type: knowledge
status: published
created: 2026-07-17T02:20:00+09:00
updated: 2026-07-17T02:20:00+09:00
tags: [backlog, workflow, skill, reference]
summary: Backlog 参照系 workflow の詳細規約。一覧提示・棚卸し・単一 item 参照・GitHub Issue 状態確認のフローを定義。
---

# Backlog Reference Workflow

## Summary

Skill vault-manager が backlog 系の参照操作(一覧、棚卸し、Issue 同期)を行う時の詳細規約。Skill は本 doc の要点のみ抱え、詳細実装はここを参照する。

## トリガー phrase(Skill 発火条件)

以下いずれかの発話を Chat 内で検知した場合、Backlog 参照 workflow を起動する:

### 一覧提示系

- 「今仕掛かりは?」
- 「今のタスクは?」
- 「open な backlog は?」
- 「〜プロジェクトの残ってるタスクは?」
- 「backlog 見せて」
- 上記類似の言い回し

### 棚卸し系

- 「棚卸しして」
- 「backlog レビューして」
- 「進捗確認して」
- 「Issue 状態確認して」

### 単一 item 参照系

- 「〜の詳細見せて」(既存 backlog item を指す文脈で)
- 「〜の状態は?」
- 「〜の履歴は?」

## Level 1 追加読み込み

Backlog 参照操作の初回検知時、以下を Level 1 で読み込み Chat 内キャッシュ:

- Vault `00_meta/backlog_tags.md`(tag 意味の把握、tag 検索・提示時に必要)

以降の Chat 内では都度読み込まない。

## 一覧提示 flow

### Step 1: 対象プロジェクト特定

- Naoya の発話や Chat context から対象プロジェクトを推定
- 特定できない場合、Naoya に「全プロジェクトですか、それとも特定のプロジェクトですか」と確認
- 特定できた場合:
  - Specific repo → `30_projects/<Repo>/backlog/`
  - Life-scope → `30_projects/_life/backlog/`
  - Idea → `30_projects/_ideas/incubating/<slug>/backlog/`
  - 全体 → 上記全て

### Step 2: 一覧取得

`search_by_keyword(path_prefix='<target-path>', keyword='backlog_item')` で対象 backlog item を列挙。

### Step 3: Front Matter 取得

各 item に対して `get_frontmatter` で以下フィールドを取得:

- `id`, `title`, `kind`, `state`, `assignee`, `summary`
- 存在すれば `cursor_instruction_id`, `github_issue`, `updated`, `tags`

### Step 4: フィルタと集計

- `state: open` のみを集計対象(done/abandoned は除外、Naoya が明示要求した場合のみ含める)
- `stalled` tag があれば flag
- `updated` が 2 週間以上前のものは実質 stalled(tag 未付与でも警告表示)

### Step 5: 表形式提示

以下の列で表形式:

| # | Title | Kind | Assignee | Updated | GitHub | Notes |

- Kind グループごとに分けるか混在するかは Naoya の好みで(初回は混在で提示、要求あれば分割)
- Notes には stalled、blocked、cursor 委譲中等の状況を短く

## 棚卸し flow

### Step 1-5: 一覧提示 flow と同じ

### Step 6: GitHub Issue 状態確認

一覧の各 item のうち `github_issue` を持つものについて、対象プロジェクトの GitHub コネクタで Issue state を取得:

- **作業混ざり防止規約遵守**: 相談中の対象プロジェクト以外の GitHub コネクタは能動的に使わない
- 全体棚卸しの場合、各プロジェクトの GitHub コネクタを順次使う必要がある。Naoya の明示指示を「全プロジェクト対象」の意思表示として扱う

### Step 7: 状態変化検出と更新提案

Issue state と Vault state の乖離を検出:

- Issue closed & merged & Vault `state: open` → Vault `state: done` 更新を提案
- Issue closed but not merged & Vault `state: open` → 「これは abandoned にしますか、それとも継続ですか?」と Naoya 確認
- Issue open & Vault `state: open` → 変化なし、Vault の状況を Naoya 確認(進捗、blocker)

### Step 8: Stalled 検出

- `state: open` かつ `updated` が 2 週間以上前のもの
- 現在 `stalled` tag なし → 「これ止まっていますが、再開しますか、abandoned にしますか、tag だけ付けて追跡しますか?」と提案

### Step 9: Naoya 承認と反映

各更新提案について Naoya の Yes/No を得る:

- 承認 → `update_note(mode=append)` で Front Matter 更新(state, updated, completed_at 等)+ H2 History に「YYYY-MM-DD: XX 更新(理由)」を追記
- 保留 → 変更なし、次の item に進む

**無断更新は禁止**。必ず Naoya の明示承認を得る。

## 単一 item 参照 flow

### Step 1: item 特定

- Naoya の発話から backlog item を特定(タイトル、id、または path)
- 曖昧な場合は `search_by_keyword` で候補を提示、Naoya に選択させる

### Step 2: 全体取得

`get_file_content` で該当 backlog item の全体を取得。

### Step 3: 要約提示

以下を Naoya に提示:

- Front Matter 概要(kind, state, assignee, tags, github_issue 等)
- Body の Summary セクション
- Body の Context セクション
- Body の History セクション(最新 3-5 エントリ)

### Step 4: 関連 item 参照(任意)

Naoya が求めれば `derived_from_id`, `related_ids`, `cursor_instruction_id`, `github_issue` の対象を辿る。

## GitHub MCP との協働

### 作業混ざり防止規約

Skill v1.2 で確立済みの規約を遵守:

- 相談中の対象プロジェクト以外の GitHub コネクタは能動的に使わない
- 全体棚卸しでは Naoya の明示指示を「全プロジェクト対象」の意思表示として受け入れる

### 全体棚卸しの実行

「全プロジェクトの棚卸し」等が指示された場合:

1. Vault の全 backlog を一覧提示(GitHub 確認前)
2. `github_issue` を持つ item ごとに、対応プロジェクトの GitHub コネクタで Issue state 取得
3. プロジェクト間の GitHub コネクタを切り替える時、明示的に切り替え中と伝える(prompt injection 対策の透明性)

### GitHub コネクタ利用不可時

対応する GitHub コネクタが接続されていない場合、Vault backlog の一覧のみ提示し、「対応する GitHub 状態確認には X コネクタ接続が必要」と Naoya に伝える。

## Backlog 系操作外への波及禁止

Backlog 参照 workflow の実行中、以下は禁止:

- **50_self/ の参照**: 明示指示なく参照しない
- **他プロジェクトの docs 能動参照**: 相談中の対象以外は参照しない
- **Skill 既存挙動の破壊**: 保存判断フロー、あいまい名解決、sensitive 領域配慮等はそのまま継続

## 保存系 workflow との境界

本 doc は **参照系のみ**。以下は Phase 1d の対象(本 workflow では扱わない):

- 新規 backlog item の起票
- open-questions.md からの昇格
- Cursor 委譲 → Issue 起票 の flow

参照中に Naoya が新規起票を要求した場合、「これは保存 workflow(Phase 1d 相当)ですが、当面 open-questions.md への追記提案でよいですか」と応答(Phase 1d 完了までの暫定挙動)。

## Related

- [[pj-2026-07-17-cb46|Backlog System Overview]]
- [[pj-2026-07-17-315f|GitHub Issue 境界]]
- [[pj-2026-07-17-7293|既存資産統合]]
- [[pj-2026-07-17-a25e|ADR-0019 Skill backlog reference workflow]]
- Skill: `skills/vault-manager/SKILL.md`

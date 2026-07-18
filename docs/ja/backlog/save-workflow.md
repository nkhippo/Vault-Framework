---
title: Backlog Save Workflow
type: knowledge
status: published
created: 2026-07-17T02:30:00+09:00
updated: 2026-07-17T02:30:00+09:00
tags: [backlog, workflow, skill, save]
summary: Backlog 保存系 workflow の詳細規約。新規起票、open-questions 昇格、Cursor 委譲、GitHub Issue 起票の 4 種類のフローを定義。
---

# Backlog Save Workflow

## Summary

Skill vault-manager が backlog 系の保存操作を行う時の詳細規約。参照系(Phase 1c)と対をなす、保存系の source-of-truth。

## トリガー phrase(Skill 発火条件)

### 新規起票系

- 「これタスクとして起票して」「これ task で backlog に入れて」→ **新規 task 起票 flow**
- 「これ課題として残して」「これ issue として起票して」→ **新規 issue 起票 flow**
- 「これを backlog に入れて」(kind 不明) → kind を あなた(導入者) に確認して起票

### 昇格系

- 「これタスク化して」「これ backlog に上げて」+ open-questions を指す文脈 → **open-questions 昇格 flow**

### Cursor 委譲・Issue 起票系

- 「これ Cursor 委譲して」+ 指示書話 → **Cursor 委譲 flow**
- 「Issue 起票して」→ **GitHub Issue 起票 flow**(単体 or Cursor 委譲と連携)

### 保留系

- 「後で考えましょう」「後で検討」→ **open-questions.md 追記提案 or backlog issue 起票の 2 択を あなた(導入者) に提示**

## Level 1 追加読み込み

保存系操作の初回検知時、以下を Level 1 で読み込み Chat 内キャッシュ(Phase 1c で既に読み込まれていればスキップ):

- Vault `00_meta/backlog_tags.md`
- Vault `00_meta/templates/backlog_item.md`
- Vault `00_meta/frontmatter_schema/backlog_item.md`

## 新規 task/issue 起票 flow

### 起票 flow(呼び出し元による gate 分岐、Phase 1g 以降)

- **候補抽出コマンド Step 2 からの内部呼び出し**: 保存 trigger 発話を承認扱いとし、Step 2(案提示)と Step 3(承認 gate)を skip して即時起票(ADR-0024)
- **あなた(導入者) の直接明示要求**: 「これタスクとして起票して」「この課題を残しておいて」等、個別 item を指名した要求は従来通り Step 2 → Step 3 を実行
- **Cursor 委譲 / GitHub Issue 起票 / open-questions 昇格**: 従来通り承認 gate を維持

### Step 1: 対象プロジェクト特定

- Chat context または あなた(導入者) の発話から対象プロジェクトを推定
- 曖昧なら あなた(導入者) に確認
- 対象プロジェクトによって path が決まる:
  - Specific repo → `30_projects/<Repo>/backlog/`
  - Life-scope → `30_projects/_life/backlog/`
  - Idea → `30_projects/_ideas/incubating/<slug>/backlog/`

### Step 2: 起票案の構築と提示(直接明示要求のみ)

以下を **案として** あなた(導入者) に提示(まだ create_note しない):

- **kind**: task / issue(context から判定、曖昧なら あなた(導入者) 選択)
- **title**: 主題(短く 20-40 文字目安)
- **summary**: 1-2 行の要約
- **tags**: `backlog_tags.md` から選択(1-3 個目安、backlog は自動付与)
- **path**: `30_projects/<Repo>/backlog/YYYY-MM-DD_slug.md`(slug は英数ハイフン)
- **assignee**: `owner`(起票時の default)

### Step 3: あなた(導入者) 承認 gate(直接明示要求のみ)

あなた(導入者) の反応で分岐:

- 承認 → Step 4 へ
- 修正指示 → 案を修正して Step 2 で再提示
- 却下 → 起票中止

### Step 4: id 生成

- prefix: 対象 path から infer(通常 `pj-`)
- date: 起票日 JST
- 4hex: Claude が pseudo-random 生成
- Collision check: `search_by_keyword` で確認、必要なら再生成

### Step 5: Front Matter 構築

```yaml
---
id: <生成 id>
aliases: [<id>]
title: <承認された title>
type: backlog_item
kind: task | issue
state: open
assignee: owner
project: <RepoName or _life or _ideas/<slug>>
created: <ISO8601 JST>
updated: <ISO8601 JST>
tags: [backlog, <選定 tag>, ...]
summary: <承認された summary>
---
```

Optional フィールド(状況次第):

- `derived_from_id`: 派生元がある場合
- `related_ids`: 関連する既存 item がある場合(open-questions からの昇格時等)

### Step 6: Body 構築

テンプレ(`00_meta/templates/backlog_item.md`)に従い:

```markdown
## Summary

<主題を 2-3 段落で(Chat の議論から生成)>

## Context

<なぜこの item が発生したか、背景>

## Definition of Done(kind: task 時)

- <完了条件、Chat から抽出、無ければ あなた(導入者) に確認>

## Open questions(kind: issue 時)

- <解決すべき問い、Chat から抽出>

## History

- YYYY-MM-DD: 起票(kind=<>, assignee=owner)
```

### Step 7: create_note 実行

- path: `30_projects/<Repo or _life or _ideas/<slug>>/backlog/YYYY-MM-DD_slug.md`
- Vault MCP `create_note` で書き込み
- 失敗時は接続失敗ルールに従う(Skill v1.1 の中断ルール)

### Step 8: 完了報告

あなた(導入者) に「backlog item 起票しました:
- id: `<id>`
- path: `<path>`
- kind: `<task/issue>`, state: open, assignee: owner」

## open-questions.md 昇格 flow

### Step 1: 昇格対象の特定

- あなた(導入者) が open-questions の特定行を明示指定(コピペ、行番号、内容参照)
- Claude が該当ファイルを `get_file_content` で取得、該当行を確認
- 曖昧なら「どの行ですか?」と あなた(導入者) に確認

### Step 2: kind 判定と昇格案の構築

新規起票 flow の Step 2 と同じ。ただし以下を追加:

- **derived_from**: open-questions.md の Front Matter id を確認、`derived_from_id` フィールドに含める(open-questions が親)
- **related_ids**: 関連する他 backlog item があれば含める

あなた(導入者) に案を提示、承認 gate。

### Step 3: Backlog item 作成

新規起票 flow の Step 4-7 と同じ。ただし Body の History に:

```markdown
## History

- YYYY-MM-DD: open-questions.md 行 "X" から昇格
```

### Step 4: open-questions.md の該当行処理

あなた(導入者) に「open-questions の該当行を削除しますか、それとも wikilink 参照に置換しますか?」と選択させる:

- **削除**: 該当行を削除して `update_note(mode=replace_body)` or 適切なモードで更新
- **置換**: 該当行を `- [[<backlog id>|<title>]]` に置換
- **保持**: そのまま残す(あなた(導入者) の意図次第)

### Step 5: 完了報告

「open-questions.md から昇格しました:
- Backlog item id: `<id>`, path: `<path>`
- Open-questions 側: `<削除/置換/保持>`」

## Cursor 委譲 flow

**前提**: Backlog item が既に存在し `kind: task`、`state: open`、`project: <specific repo>`。

### Step 1: 委譲対象の確認

- あなた(導入者) が「これ Cursor 委譲して」+ 対象 backlog item を明示
- または Claude が Cursor 委譲判定(3 ファイル以上、リファクタ等、Skill v1.3 の判定ルール)に基づいて提案

### Step 2: 指示書作成の提案

- 指示書の下書き案を あなた(導入者) に提示(既存の指示書テンプレに従う、Skill 側で扱う)
- 対象 repo、変更範囲、コミット構成、想定所要を含める

### Step 3: 承認 → 指示書作成

- 指示書は Vault 内 or 作業ディレクトリに作成(具体的な path は Skill 既存の Cursor 委譲規約に従う)
- 指示書自身にも id/aliases 付与(FM 準拠)

### Step 4: Backlog item 更新

- `update_note` で backlog item の Front Matter に追記:
  - `cursor_instruction_id: <指示書 id>`
  - `assignee: cursor`
- Body の History に「YYYY-MM-DD: Cursor 委譲(指示書 `<id>`)」を追記

### Step 5: 完了報告

「Cursor 指示書作成 & backlog 更新完了:
- 指示書: `<id>`, path: `<path>`
- Backlog item: assignee → cursor、cursor_instruction_id 追加
- 次: あなた(導入者) が Cursor に指示書を投げ、完了後に Issue 起票 or Vault 更新」

## GitHub Issue 起票 flow(Cursor 委譲と連携)

**前提**: 上記 Cursor 委譲 flow が完了、または task が指示書なしで直接 Issue 起票可能。

### Step 1: 起票対象と repo 確認

- 対象 backlog item の `project` フィールドから target repo を特定
- あなた(導入者) に「対象 repo `<owner/repo>` で Issue 起票していいですか?」と確認

### Step 2: Issue 内容の構築

- Title: backlog item の title を基本、必要なら文脈調整
- Body:
  - Backlog item の Summary
  - Backlog item の Context
  - リンク: Vault backlog item への参照(id or path)
  - リンク: Cursor 指示書へのリンク(あれば)
- Labels: backlog item の tags を参考に、対象 repo の label 慣習に合わせる(あなた(導入者) に確認可)

### Step 3: 承認 → Issue 作成

- **対象プロジェクトの GitHub MCP コネクタ**を使用(作業混ざり防止規約遵守)
- 対応するコネクタが接続されていない場合は あなた(導入者) に接続を依頼、または手動起票を提案

### Step 4: Backlog item 更新

- `update_note` で:
  - `github_issue: <owner/repo>#<N>`
- Body の History に「YYYY-MM-DD: GitHub Issue `<owner/repo>#<N>` 起票」を追記

### Step 5: 完了報告

「GitHub Issue 起票 & backlog 更新完了:
- Issue: `<owner/repo>#<N>`
- Backlog item: github_issue 追加
- 次: Cursor が Issue と指示書に沿って作業、完了後に棚卸しフローで close 同期」

## Direct Issue 起票 flow(Cursor 委譲なし)

**前提**: 小 task で指示書化しない場合(1 ファイル修正等)。

- 上記 GitHub Issue 起票 flow の Step 1-5 を実施
- Backlog item の `cursor_instruction_id` は追加しない
- `assignee: cursor`(Cursor が Issue 見て作業) or `assignee: owner`(手動対応)は あなた(導入者) に確認

## 保留 flow(「後で考えましょう」)

あなた(導入者) が「後で考えましょう」等と発話した場合、以下 2 択を提示:

- **選択肢 A**: `open-questions.md` の該当プロジェクトファイルに 1 行追加(思いつきレベルで残す)
- **選択肢 B**: `backlog/` に kind: issue で起票(状態管理対象にする)

あなた(導入者) の選択に応じて実施。デフォルト提案は選択肢 A(open-questions への追記)、backlog 起票は明示的な意思表示があった時のみ。

## 作業混ざり防止規約遵守

- 対象プロジェクト以外の GitHub コネクタは能動使用しない
- 起票する repo は あなた(導入者) の明示指示または Chat context から特定
- Cross-project の起票要求は「今 IPASoundDrill の相談中ですが、Vault-MCP に起票しますか?」等の確認プロンプトを挟む
- 50_self/ 領域には backlog 起票しない(sensitive、参照厳格)

## あなた(導入者) 承認 gate(必須)

以下は あなた(導入者) の明示承認を経る:

- あなた(導入者) の直接明示要求による新規 backlog item 起票(案提示 → 承認 → 実施)
- open-questions.md の削除・置換
- Cursor 指示書作成
- GitHub Issue 起票
- Backlog item の Front Matter 変更(assignee, tags, github_issue 等の追加)

候補抽出コマンド Step 2 は例外で、保存 trigger 発話を承認として即時起票する。Skill が trigger なしで単独起票することは禁止。

## エラー処理

- MCP 接続失敗時: Skill v1.1 の中断ルールに従う(1 回リトライ → 中断 → あなた(導入者) 報告)
- Vault-MCP `create_note` 既存 path 衝突: 別 slug を あなた(導入者) に提案
- GitHub コネクタ未接続: 起票を保留、あなた(導入者) に接続を依頼
- 承認 gate で あなた(導入者) が却下: 起票を中止、backlog item は作成しない

## 重複起票の回避

新規起票要求時、Claude は既存 backlog item がないか `search_by_keyword` で確認。既存があれば「既に起票済みです」と報告して重複起票を回避。

## Related

- [[pj-2026-07-17-cb46|Backlog System Overview]]
- [[pj-2026-07-17-315f|GitHub Issue 境界]]
- [[pj-2026-07-17-7293|既存資産統合]]
- [[pj-2026-07-17-27e2|Reference Workflow]]
- [[pj-2026-07-17-632e|ADR-0020 Skill save workflow]]
- Skill: `skills/vault-manager/SKILL.md`

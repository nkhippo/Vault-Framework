---
id: pj-2026-07-17-68cf
aliases:
- pj-2026-07-17-68cf
title: Handoff Workflow
type: knowledge
status: published
created: 2026-07-17T05:10:00+09:00
updated: 2026-07-17T05:10:00+09:00
tags: [backlog, workflow, skill, handoff, chat]
summary: 別 Chat への引き継ぎ用ファイルを対象プロジェクトの handoff/ 配下に新規作成するコマンドの詳細規約。履歴として蓄積(per-timestamp)。
---

# Handoff Workflow

## Summary

Chat の議論内容から「別 Chat で作業を継続するための引き継ぎファイル」を対象プロジェクトの `30_projects/<Repo>/handoff/YYYY-MM-DD_<slug>.md` として新規作成するコマンド。

Phase 1f で独立コマンドとして追加。既存の handoff 慣習(current-state.md の上書き型)を **履歴蓄積型**(timestamp 付きファイル)に更新。

## トリガー phrase

- 「引き継ぎできるようにしてください」
- 「引き継ぎ用に保存」
- 「handoff を作って」
- 「別 Chat で続きから作業したい」

## Level 1 追加読み込み

なし(handoff は per-project の慣習に依存、既存 template 等を必要に応じて Level 2 で読む)。

## 実行フロー

### Step 1: 対象プロジェクト特定

- Chat context または Naoya の発話から対象プロジェクトを推定
- 曖昧なら Naoya に確認
- 対象プロジェクトの `30_projects/<Repo>/handoff/` ディレクトリを想定(存在しなければ create_note で自動作成される)

### Step 2: Handoff 内容案の構築

Chat の議論から以下を抽出・構造化:

- **Summary**: 現在の状況(1-2 段落)
- **Current work**: 進行中の作業(具体的な item と状態)
- **Next steps**: 次の予定・アクション
- **Open questions**: 未解決の論点・判断待ち事項
- **Blockers**: 依存関係・待ち状態
- **Related PRs / issues**: 関連する GitHub PR や issue
- **Related backlog items**: 関連する backlog item(id で参照)
- **Context**: 別 Chat で読む人が理解するための背景情報

### Step 3: Front Matter 構築案

```yaml
id: <生成 id>
aliases: [<id>]
title: <handoff の主題>
type: handoff
project: <Repo>
status: published
created: <ISO8601 JST>
tags: [handoff, chat, <その他>]
summary: <1-2 行>
source_chat_log_id: <chat_log id>  # 先に chat_log 保存済みの場合
related_backlog_ids: [<id>, ...]  # 関連 backlog item(あれば)
```

Path: `30_projects/<Repo>/handoff/YYYY-MM-DD_<slug>.md`

- `<slug>`: 主題を英数ハイフンで短く(例: `phase-1f-refinement`、`vault-broken-fix`)

### Step 4: Naoya 承認 gate

案(Front Matter + Body 構成)を提示、Naoya の action:

- 承認 → 実施
- 修正 → 案再提示
- 却下 → 中止

### Step 5: create_note で作成

`create_note` で handoff ファイル書き込み。既存 path があれば slug を調整して衝突回避。

### Step 6: 完了報告

```
Handoff 作成完了:
- Path: <path>
- ID: <id>
- Project: <Repo>
- 別 Chat で本ファイルを Level 1 or Level 2 で参照可能
```

## 履歴蓄積の意義

Phase 1f 以前は `handoff/current-state.md` の**上書き型**運用が想定されていたが、Phase 1f では **timestamp 付きファイル**による履歴型に更新:

- 各引き継ぎ時点のスナップショットが保持される
- 過去の引き継ぎ状態を後から辿れる
- ファイル数は増えるが、Backlog システムの `30_projects/<Repo>/backlog/YYYY-MM-DD_<slug>.md` パターンと整合

過去の `current-state.md` 慣習からの移行時、既存ファイルは保持しつつ新規は timestamp 型で作成する。

## chat_log との相互リンク

**先に chat_log 保存が実行済みの場合**:

- handoff の `source_chat_log_id` に含める
- chat_log 側に `spawned_handoff_ids: [<id>, ...]` を append 提案(オプション)

**chat_log 保存が未実行の場合**:

- handoff は `source_chat_log_id` なしで作成

## backlog item との相互リンク

Handoff が言及する未解決 item が backlog にある場合、`related_backlog_ids` に含める。逆方向の相互リンクは強制しない(backlog item の方が長期永続、handoff は時点スナップショット)。

## エラー処理

- 対象プロジェクト特定不能: Naoya に確認
- Path 衝突: slug を調整
- MCP 失敗: 中断ルール適用

## Naoya 承認 gate(必須)

案提示 → Naoya action → 実施。無断作成禁止。

## 作業混ざり防止規約遵守

- 対象プロジェクトの handoff/ にのみ作成
- 50_self/ 領域には handoff 作成しない

## Related

- [[pj-2026-07-17-64df|Save Workflow]](Phase 1d PR-A、chat_log 保存は独立コマンド)
- [[pj-2026-07-17-4a23|Candidate Extraction Workflow]](Phase 1f、別コマンド)
- [[pj-2026-07-17-c14c|ADR-0023 Phase 1f three independent commands]]
- Skill: `skills/vault-manager/SKILL.md`

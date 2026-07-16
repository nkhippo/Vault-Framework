---
id: pj-2026-07-17-68cf
aliases:
- pj-2026-07-17-68cf
title: Handoff Workflow
type: knowledge
status: published
created: 2026-07-17T05:10:00+09:00
updated: 2026-07-17T06:00:00+09:00
tags: [backlog, workflow, skill, handoff, chat]
summary: 明示 trigger で別 Chat への引き継ぎファイルを即時作成する独立コマンド。対象プロジェクトの handoff/ 配下へ timestamp 付きで履歴蓄積する。
---

# Handoff Workflow

## Summary

Chat の議論内容から、別 Chat で作業を継続するための handoff ファイルを `30_projects/<Repo>/handoff/YYYY-MM-DD_<slug>.md` に即時作成する独立コマンド。

**Trigger 発話 = 承認**。案提示と承認 gate は行わず、Skill が内容を自律構築して `create_note` を即実行する。

## トリガー phrase

- **Primary**: 「別のチャットに引き継げるように Vault に保存して」
- **Secondary(compat)**: 「引き継ぎできるようにしてください」、「引き継ぎ用に保存」、「handoff を作って」、「別 Chat で続きから作業したい」

## Level 1 追加読み込み

なし。handoff は per-project 慣習に依存し、既存 template 等を必要に応じて Level 2 で読む。

## 実行フロー(案提示なし、承認 gate なし)

1. Trigger 検知 → Chat context から対象プロジェクトを判定
2. Skill が以下を自律決定:
   - Path: `30_projects/<Repo>/handoff/YYYY-MM-DD_<slug>.md`
   - Title: handoff の主題
   - Tags: `[handoff, chat, ...]`
   - Summary: 1-2 行
   - ID: `pj-<YYYY-MM-DD>-<4hex>`(collision check)
3. Body を構築:
   - **Summary**: 現在の状況
   - **Current work**: 進行中の作業と状態
   - **Next steps**: 次の予定・アクション
   - **Open questions**: 未解決の論点
   - **Blockers**: 依存関係・待ち状態
   - **Related PRs / issues**
   - **Related backlog items**
   - **Context**: 引き継ぎ先が理解するための背景
4. Front Matter に `source_chat_log_id`(保存済みなら)、`related_backlog_ids`(関連 item があれば)を含める
5. 既存 path との衝突を確認し、必要なら slug を自律調整
6. `create_note` を即実行
7. id / path / project を報告

Front Matter:

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
source_chat_log_id: <chat_log id>  # 保存済みの場合
related_backlog_ids: [<id>, ...]  # 関連 backlog item がある場合
```

## 履歴蓄積型

過去の `handoff/current-state.md` 上書き型から移行し、新規は timestamp 付きファイルとして蓄積する。既存 `current-state.md` は保持する。

## 相互リンク

- handoff → chat_log: `source_chat_log_id`
- handoff → backlog: `related_backlog_ids`
- chat_log → handoff: `spawned_handoff_ids` を必要に応じて即時更新
- backlog item から handoff への逆リンクは強制しない

## 事後修正

Naoya は `update_note` で内容変更、`delete_note` で削除可能。

## 特殊ケース

- 対象プロジェクト特定不能 → Naoya に確認
- Naoya が「案を見せてから保存」等と明示 → 案提示 → 承認 → 実施へ切り替え
- MCP 失敗 → Skill 中断ルールを適用

## 作業混ざり防止規約遵守

- 対象プロジェクトの handoff/ にのみ作成
- 50_self/ 領域には handoff を作成しない

## Related

- [[pj-2026-07-17-64df|Save Workflow]]
- [[pj-2026-07-17-4a23|Candidate Extraction Workflow]]
- [[pj-2026-07-17-c14c|ADR-0023 Phase 1f Three Independent Commands]]
- [[pj-2026-07-17-052b|ADR-0024 Immediate Execution With Explicit Trigger Phrases]]
- Skill: `skills/vault-manager/SKILL.md`

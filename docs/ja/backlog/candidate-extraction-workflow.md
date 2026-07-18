---
title: Backlog Candidate Extraction Workflow
type: knowledge
status: published
created: 2026-07-17T05:10:00+09:00
updated: 2026-07-17T06:00:00+09:00
tags: [backlog, workflow, skill, candidate, extraction]
summary: Chat 内容から backlog 候補を抽出・提示し、明示保存 trigger で即時起票する 2 step 独立コマンド。Trigger 発話を承認として扱う。
---

# Backlog Candidate Extraction Workflow

## Summary

Chat 内容から未決事項・次アクション・Blocker 等の backlog 候補を抽出して提示し、続く保存 trigger で即時起票する 2 step 独立コマンド。

**Trigger 発話 = 承認**。Step 1 の候補提示は承認 gate ではなく情報提示であり、Step 2 の保存 trigger 後は案を再提示せず即時実行する。

## トリガー phrase

### Step 1: 抽出 + 候補提示

- **Primary**: 「会話内のタスクを Vault に保存して」
- **Secondary(compat)**: 「未決事項を backlog に候補リスト作って」、「候補リスト作って」、「残タスクを backlog 化して」、「Chat の残 item を起票して」

### Step 2: 即保存

- **Primary**: 「これを保存して」
- **Secondary**: 「全部保存して」、「起票して」(直前に Step 1 実行済みの context 時)
- **Variant**: 「1 と 3 だけ保存して」(部分保存)、「1 のタイトルを X に変えて保存」(修正保存)

単純 chat_log 保存や handoff 保存は本 workflow の対象外。

## Level 1 追加読み込み

Phase 1c/1d で読み込み対象の backlog_tags.md、template、schema を未取得の場合のみ読む。

## 実行フロー

### Step 1: 抽出 + 候補提示

1. Step 1 trigger を検知
2. Chat 全体から以下 5 カテゴリを抽出:
   - **未決事項**: 「後で検討」「保留」等が明示された論点
   - **次アクション**: 未実行の action
   - **Blocker**: 依存関係
   - **明示要求**: Chat 内で「これタスク化して」があったが未起票のもの
   - **仕掛かり**: 議論されたが結論・完了に至らなかった論点
3. 各 item の kind(task/issue)を Skill が推定
4. 各 item の project を Chat context から推定。不明なら `_life` fallback
5. 候補リストを表形式で提示:

```
| # | 種別 | 内容(要約) | 推定 kind | 推定 project |
|---|------|-------------|-----------|--------------|
| 1 | 次アクション | X を実装 | task | IPASoundDrill |
| 2 | 未決事項 | Y の設計方針を検討 | issue | IPASoundDrill |
```

完了済み action、結論が出た事項、action に繋がらない情報交換は抽出しない。

### Step 2: 保存 trigger 待ち → 即保存

1. Step 2 trigger を検知
2. 候補全件または あなた(導入者) 指定 subset を対象に Phase 1d PR-A 起票 flow を内部呼び出し
3. **ADR-0024 により案提示と承認 gate を skip**
4. Skill が id/title/kind/project/tags/path/summary/body を決定して `create_note` を逐次実行
5. chat_log 保存済みなら `source_chat_log_id` を付与し、chat_log の `spawned_backlog_ids` も即時更新
6. 起票 item 一覧を報告

## Step 1 と Step 2 の間の あなた(導入者) 応答

- 「これを保存して」→ 全件即保存
- 「1 と 3 だけ保存して」→ 部分即保存
- 「1 の title/kind/project を変えて保存」→ 修正して即保存
- 「これは違う、抽出やり直して」→ Step 1 を再実行
- 別の話題へ移る → コマンドを中断し、次の Step 1 trigger で再起動

## 候補ゼロ

Step 1 で候補ゼロなら「残 item なし」と報告し、Step 2 は実行しない。

## 抽出精度

- 過剰抽出・不要起票 → 事後 abandoned/update で対応
- 抽出漏れ → Phase 1d PR-A の直接明示起票 flow で追加
- Level 1 棚卸し flow で quality control

## chat_log との相互リンク

- 保存済み chat_log がある場合: backlog item に `source_chat_log_id`、chat_log に `spawned_backlog_ids`
- chat_log 未保存の場合: `source_chat_log_id` なしで起票

## エラー処理

- 起票中の MCP 失敗: Skill 中断ルール(v1.1)に従う
- Step 1 後に別の話題へ移った場合: 候補を保存せず自然に中断

## 作業混ざり防止規約遵守

- project 推定は Chat context 内のみ
- 対象プロジェクト以外の起票は稀。判断困難なら あなた(導入者) に確認
- 50_self/ 関連 item は抽出しない(sensitive)

## Related

- [[pj-2026-07-17-64df|Save Workflow]]
- [[pj-2026-07-17-68cf|Handoff Workflow]]
- [[pj-2026-07-17-c14c|ADR-0023 Phase 1f Three Independent Commands]]
- [[pj-2026-07-17-052b|ADR-0024 Immediate Execution With Explicit Trigger Phrases]]
- Skill: `skills/vault-manager/SKILL.md`

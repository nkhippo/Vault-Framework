---
id: pj-2026-07-17-4a23
aliases:
- pj-2026-07-17-4a23
title: Backlog Candidate Extraction Workflow
type: knowledge
status: published
created: 2026-07-17T05:10:00+09:00
updated: 2026-07-17T05:10:00+09:00
tags: [backlog, workflow, skill, candidate, extraction]
summary: Chat 内容から backlog 候補を自動抽出、Naoya 承認 gate を経て起票する独立コマンドの詳細規約。Phase 1f で Phase 1e 統合フローから分離。
---

# Backlog Candidate Extraction Workflow

## Summary

Chat 内容から未決事項・次アクション・Blocker 等の backlog 候補を自動抽出し、Naoya の承認 gate を経て backlog item として起票する独立コマンド。

Phase 1e で統合フローの一部だった機能を、独立コマンドとして分離した Phase 1f 仕様。

## トリガー phrase

以下いずれかの発話を検知した時、本 workflow を起動:

- 「未決事項を backlog に候補リスト作って」
- 「残タスクを backlog 化して」
- 「Chat の残 item を起票して」
- 「候補リスト作って」

**単純 chat_log 保存(「Vault に保存して」)や handoff 作成(「引き継ぎできるようにしてください」)は本 workflow の対象外**。それぞれ独立コマンドとして処理。

## Level 1 追加読み込み

Phase 1c/1d で既に読み込み済みのはず(backlog_tags.md, templates, schema)。追加不要。

## 実行フロー

### Step 1: 残 item 自動抽出

Chat 全体を Claude が review、以下カテゴリの item を抽出:

- **未決事項**: 「後で検討」「保留」等が明示された論点
- **次アクション**: 未実行の action
- **Blocker**: 依存関係
- **明示要求**: Chat 内で「これタスク化して」があったが未起票のもの
- **仕掛かり**: 議論されたが結論・完了に至らなかった論点

完了済み action、結論が出た事項、action に繋がらない情報交換は抽出しない。

### Step 2: 候補リスト提示

表形式で Naoya に提示:

```
| # | 種別 | 内容(要約) | 推定 kind | 推定 project |
|---|------|-------------|-----------|--------------|
| 1 | 次アクション | X を実装 | task | IPASoundDrill |
| 2 | 未決事項 | Y の設計方針を検討 | issue | IPASoundDrill |
```

### Step 3: Naoya 承認 gate

- 一括: 「全部起票」「全部 skip」
- 個別: 「1 と 3 は起票、2 は skip」
- 修正付き: 「1 は起票、title を X に変更」
- 抽出漏れ追加: 「上記に加えて Y も候補にして」

### Step 4: Backlog 起票(Phase 1d PR-A の起票 flow 再利用)

承認された各 item について Phase 1d PR-A の起票 flow を実行:

- id 生成、collision check
- Front Matter 構築(kind/state=open/assignee=naoya/project/tags=[backlog, ...])
- Body 構築

**Chat 内容を保存した chat_log がある場合**(先に「Vault に保存して」で保存済み等)、backlog item の Front Matter に `source_chat_log_id: <chat_log id>` を含める。無い場合は省略。

### Step 5: 完了報告

```
候補抽出 + 起票完了:
- 起票 backlog item: N 件
- skip 候補: M 件(記録なし)
```

## chat_log との相互リンク

**先に chat_log 保存が実行済みの場合**:

- backlog item に `source_chat_log_id` を付与
- chat_log 側に `spawned_backlog_ids` を append 提案(Naoya 承認)

**chat_log 保存が未実行の場合**:

- backlog item は `source_chat_log_id` なしで起票
- 相互リンクは Naoya が後から chat_log 保存 + 手動 append で構築可能

## エラー処理

- 抽出候補ゼロ: 「残 item は抽出されませんでした」と報告、起票なし
- 起票中の MCP 失敗: Skill 中断ルール(v1.1)に従う
- 承認 gate で全 skip: 起票なしで完了

## Naoya 承認 gate(必須)

候補リスト提示 → Naoya action → 実施。自動起票禁止。

## 作業混ざり防止規約遵守

- 抽出候補の project 推定は Chat context 内のみ
- 対象プロジェクト以外の起票は Naoya 明示確認
- 50_self/ 関連 item は抽出しない(sensitive、明示要求時のみ)

## Related

- [[pj-2026-07-17-64df|Save Workflow]](Phase 1d PR-A、起票 flow 再利用)
- [[pj-2026-07-17-68cf|Handoff Workflow]](Phase 1f、別コマンド)
- [[pj-2026-07-17-c14c|ADR-0023 Phase 1f three independent commands]]
- Skill: `skills/vault-manager/SKILL.md`

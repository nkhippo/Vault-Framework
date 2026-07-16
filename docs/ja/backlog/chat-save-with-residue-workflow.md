---
id: pj-2026-07-17-6320
aliases:
- pj-2026-07-17-6320
title: Chat Save With Residue Workflow
type: knowledge
status: published
created: 2026-07-17T03:30:00+09:00
updated: 2026-07-17T03:30:00+09:00
tags: [backlog, workflow, skill, chat, handoff, integration]
summary: Chat 保存と残タスク自動起票を統合した引き継ぎフロー。Chat 全体から残 item を抽出し、Naoya 承認 gate を経て一括 backlog 起票、chat_log と相互リンクする。
---

# Chat Save With Residue Workflow

## Summary

「ここまでの会話を Vault に保存」等のトリガーで、以下を一連の流れで実行する統合フロー:

1. Chat 保存(既存の chat_log 保存 flow)
2. Chat 全体から残 item を自動抽出
3. Naoya 承認 gate(一括 or 個別)
4. 選択された item を Phase 1d PR-A の起票 flow で backlog 化
5. chat_log と backlog の相互 link 設定

主用途: **別 Chat への引き継ぎ**(既存の `handoff/current-state.md` 慣習の補完 or 代替)。

## トリガー phrase

以下いずれかの発話を検知した時、統合フローを起動:

- 「ここまでの会話を Vault に保存」
- 「Chat を Vault に、残タスクも backlog に」
- 「引き継ぎ用に保存」
- 「Chat 保存 + 残タスクも」
- 「別 Chat に移るので保存」

**曖昧な場合の判定**:
- 「Vault に保存して」(単純)→ 従来の chat_log 保存のみ(統合フロー起動しない)
- 上記に「残タスクも」「backlog も」「引き継ぎ」等が付加 → 統合フロー起動

判断困難な場合、Naoya に「残タスクの backlog 起票も行いますか?」と 1 回確認。

## Level 1 追加読み込み

Phase 1c/1d で読み込み対象になっているファイル(backlog_tags.md, templates/backlog_item.md, frontmatter_schema/backlog_item.md)が既にキャッシュされているはず。追加読み込み不要。

## 実行フロー

### Step 1: Chat 保存(既存 flow 再利用)

Phase 1c/1d で確立済みの chat_log 保存 flow を実行:

- 保存先: `10_chat_logs/YYYY/MM/YYYY-MM-DD_<slug>.md` または特定プロジェクトなら `30_projects/<Repo>/logs/YYYY/MM/...`
- Front Matter に id/aliases/title/created/type/tags/summary を付与
- Body は Chat 内容の要約 or 全文(既存慣習に従う)

**成果物**: chat_log の id と path を保持(Step 4-5 で使用)。

### Step 2: 残 item 自動抽出

Chat 全体を Claude が review、以下カテゴリの item を抽出:

#### 抽出対象カテゴリ

- **未決事項**: 「後で考えましょう」「後で検討」「一旦保留」「今は決めない」等が明示された論点
- **次アクション**: 「次に X をする」「まず Y してから」等の未実行 action
- **Blocker**: 「Z が終わらないと」「W 待ち」等の依存関係
- **明示要求**: Chat 内で「これタスク化して」「起票して」と Naoya が明示したが、Skill 保存 flow が起動していなかったもの
- **仕掛かり**: Chat 中で議論されたが結論・完了に至らなかった論点

#### 抽出しない

- 完了した action(「X をした」「Y は完了」)
- Chat 内で結論が出た事項(design-decisions に相当)
- 単なる情報交換や質問応答で action に繋がらないもの

#### 抽出結果の構造化

以下の形式で候補リストを構築:

```
| # | 種別 | 内容(要約) | 推定 kind | 推定 project |
|---|------|-------------|-----------|--------------|
| 1 | 次アクション | X を実装する | task | IPASoundDrill |
| 2 | 未決事項 | Y の設計方針を検討 | issue | IPASoundDrill |
| 3 | Blocker | Z の完了待ち | issue | _life |
```

推定 project は Chat context から infer、不明なら `_life` fallback。

### Step 3: 候補リスト提示と Naoya 承認 gate

候補リストを表形式で Naoya に提示、以下の action を選択させる:

- **一括**:
  - 「全部起票」→ 全 item を選択された kind/project で起票
  - 「全部 skip」→ backlog 起票せず、Step 5 で optional 記録のみ
- **個別**:
  - 「1 と 3 は起票、2 は skip」等の選択
  - 「1 は起票、title を X に変えて」等の修正付き
- **確認**:
  - 「2 は project _life に変更」等の推定修正
  - Chat context に基づく Naoya の詳細判断

**候補ゼロの場合**: 「残 item は抽出されませんでした、chat_log 保存のみ完了」と報告、Step 4-5 skip。

**判断困難な候補**:
- Kind 判定が曖昧 → Naoya に確認(「これは task ですか issue ですか?」)
- Project 判定が曖昧 → Naoya に確認

### Step 4: Backlog 起票(Phase 1d PR-A の起票 flow 再利用)

承認された各 item について:

1. Phase 1d PR-A の起票 flow を実行:
   - id 生成、collision check
   - Front Matter 構築(kind/state=open/assignee=naoya/project/tags=[backlog, ...])
   - **`source_chat_log_id: <Step 1 の chat_log id>` を Front Matter に追加**
   - Body 構築(Summary/Context/Definition of Done or Open questions)
2. Body の H2 History に:
   ```markdown
   ## History
   - YYYY-MM-DD: chat_log <id> から自動抽出(Phase 1e 統合フロー)
   ```
3. `create_note` で書き込み

複数 item は逐次 create_note。並列不要(記録の整合性優先)。

### Step 5: chat_log 側への逆リンク

起票が 1 件以上あった場合、chat_log の Front Matter に `spawned_backlog_ids` を追記:

```yaml
spawned_backlog_ids:
  - <backlog id 1>
  - <backlog id 2>
```

`update_note(mode=append)` で Front Matter を更新(Body には触らない、または H2 "Spawned backlog items" section 追加を Naoya が要求すれば)。

**Skip 候補の記録**(optional):
- 起票せず skip した候補は default で記録しない(冗長回避)
- Naoya が「skip 候補も記録して」と明示した場合、chat_log body に H2 "Deferred items" section 追加

### Step 6: 完了報告

以下形式で Naoya に報告:

```
Chat 保存 + 統合起票完了:
- chat_log: <id>, path: <path>
- 起票 backlog item:
  1. <id>, path: <path>(kind: task, project: X)
  2. <id>, path: <path>(kind: issue, project: Y)
- skip 候補: 2 件(記録なし)
- chat_log ↔ backlog 相互リンク済み
```

## 抽出精度への依存

Chat 抽出は Claude の理解精度に依存する。以下の限界を認識:

- **見落とし**: 明示的でない implicit action は抽出漏れの可能性
- **過剰抽出**: 情報交換を action と誤解の可能性
- **文脈依存**: Chat が長すぎる or 断片的な場合、精度低下

**mitigations**:
- Naoya の承認 gate が最終判断、抽出漏れは Naoya が気付いて追加要求できる
- 過剰抽出は skip で除外可能
- 抽出結果に自信がない場合、Claude が「これは候補ですか?」と Naoya に確認

## エラー処理

- **Chat が短くて抽出候補ゼロ**: chat_log 保存のみで完了、backlog 化 step skip
- **起票中の MCP 失敗**: Skill 中断ルール(v1.1)に従い、成功済みの item は保持、失敗した item は Naoya 報告
- **承認 gate で全 skip**: chat_log 保存のみで完了
- **Chat context が曖昧すぎて抽出困難**: Naoya に「明示的に候補を挙げてください」と依頼、手動リスト受付

## 相互リンクのスキーマ

### Backlog item 側(既存 schema 拡張)

Vault `00_meta/frontmatter_schema/backlog_item.md` に含まれる optional フィールド:
- `source_chat_log_id: <chat_log id>`(optional、Phase 1e 統合フロー起票時は必須付与)

### chat_log 側(新規)

- `spawned_backlog_ids: [<id>, ...]`(optional、起票時に追加)

新規フィールド、既存 chat_log には影響なし(optional なので)。

## 作業混ざり防止規約遵守

- 抽出候補の project 推定は Chat context 内のみ、外部参照しない
- 起票先 project が対象プロジェクト以外に及ぶ場合、Naoya に明示確認
- 50_self/ に関連する item は抽出しない(sensitive 領域、明示要求時のみ)

## Naoya 承認 gate(必須)

- 候補リスト提示 → Naoya action(一括/個別/skip)→ 実施
- 「全部起票」も明示指示、Skill 判断で自動起票禁止

## 既存 workflow との関係

- **単純 chat 保存(既存)**: 「Vault に保存して」→ chat_log 保存のみ、統合フロー起動しない
- **統合フロー(本 Phase 1e)**: 上記 trigger phrase → chat 保存 + 抽出 + 起票
- **明示 backlog 起票(Phase 1d PR-A)**: 「これタスクとして起票して」→ Phase 1d PR-A の起票 flow のみ
- **参照(Phase 1c)**: 「今仕掛かりは?」→ 変更なし

各 workflow は独立、統合フローは既存 flow の合成として実現。

## Related

- [[pj-2026-07-17-64df|Save Workflow]](Phase 1d PR-A)
- [[pj-2026-07-17-27e2|Reference Workflow]](Phase 1c)
- [[pj-2026-07-17-cb46|Backlog System Overview]](Phase 1b)
- [[pj-2026-07-17-ba5f|ADR-0022 Chat save with residue integration]]
- Skill: `skills/vault-manager/SKILL.md`

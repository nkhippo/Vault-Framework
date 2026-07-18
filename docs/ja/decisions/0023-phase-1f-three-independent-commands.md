---
title: '0023 - Phase 1f Three Independent Commands'
type: knowledge
status: accepted
created: 2026-07-17T05:10:00+09:00
updated: 2026-07-17T05:10:00+09:00
tags: [adr, skill, backlog, chat, handoff, phase-1f]
summary: Phase 1e 統合フローを廃止し、chat_log 保存 / 候補抽出 / handoff の 3 独立コマンドに再構成する意思決定記録。実運用第 1 号 feedback を受けた仕様変更。
supersedes: [ADR-0022]
---

# ADR 0023: Phase 1f Three Independent Commands

## Context

Phase 1e(ADR-0022)で導入した「Chat 保存 + 残タスク統合フロー」を実運用第 1 号(chat_log kn-2026-07-17-8c9a)で使用したところ、以下の feedback を得た:

- **自動抽出の過剰**: 8 候補中 4 件が skip(50% skip 率)、抽出精度が Naoya の判断負荷を増やしている
- **意思表示曖昧性**: 「ここまでの会話を Vault に保存」が chat_log 保存/backlog 起票/handoff 作成のどれを指すかコマンド解釈時に不明瞭
- **handoff 慣習の未活用**: Phase 1e 設計時に既存 handoff 慣習(per-project の引き継ぎファイル)を検討スコープ外にしていたが、実運用上「引き継ぎ」は独立した価値ある操作である

## Decision

Phase 1e 統合フローを廃止し、以下 **3 独立コマンド**に再構成する:

### コマンド 1: 「Vault に保存して」→ chat_log 保存のみ

- 既存挙動(Phase 1c 相当)、変更なし
- backlog 起票、handoff 作成は起動しない

### コマンド 2: 「未決事項を backlog に候補リスト作って」→ 候補抽出 + 承認 gate + 起票

- Phase 1e の Step 2-4(抽出 + 承認 + 起票)を独立コマンド化
- 詳細規約: `docs/ja/backlog/candidate-extraction-workflow.md`
- chat_log 保存は起動しない(先に別途「Vault に保存して」で実施済みの場合、`source_chat_log_id` で紐付け)

### コマンド 3: 「引き継ぎできるようにしてください」→ handoff ファイル新規作成

- 対象プロジェクトの `30_projects/<Repo>/handoff/YYYY-MM-DD_<slug>.md` を新規作成
- **履歴蓄積型**(既存 `current-state.md` 上書き型ではなく timestamp 付き)
- 詳細規約: `docs/ja/backlog/handoff-workflow.md`
- backlog 起票、chat_log 保存は起動しない

### 複合 phrase への応答

「ここまでの会話を Vault に保存」等の複合 phrase を検知した時、Skill は 3 独立コマンドのどれか(または複数の順次実行)を Naoya に確認して分岐:

- 「chat_log 保存だけですか?」→ コマンド 1
- 「backlog 候補抽出も含めますか?」→ コマンド 1 + 2
- 「handoff 作成もしますか?」→ コマンド 1 + 2 + 3(または任意の組合せ)

Naoya の明示指示で複数コマンドを順次実行することは可能。

### Phase 1e 資産の扱い

- Phase 1e 統合フローで起票済み backlog item(4 件)と chat_log(kn-2026-07-17-8c9a)は **保持**、履歴として意味あり
- ADR-0022 は `status: superseded` に変更、内容は保持

## Consequences

### Positive

- **意思表示明確**: Naoya がどの操作を求めているかコマンドレベルで明確
- **既存 handoff 慣習の活用**: per-project の引き継ぎファイル管理と統合
- **抽出精度依存の緩和**: 候補抽出はコマンド 2 に集約、chat_log 保存と分離
- **柔軟な組合せ**: 必要に応じてコマンド 1 のみ、1+2、1+2+3、2 のみ等自由に選択

### Negative

- **1 コマンドで完結しない**: 全部を実行したい場合は 3 コマンド発話 or 複合 phrase 経由の順次実行
- **Skill body 増加**: 3 コマンドの記述、複合 phrase 応答の記述で body サイズが増える(description は不変)

### Neutral

- Phase 1e ADR-0022 は supersede、内容は残す
- 既存 Phase 1c/1d PR-A/PR-B の Skill 挙動は変更なし
- vault-maintainer(Phase 1d PR-B の停滞検出)は影響なし

## Alternatives Considered

### A. Phase 1e 統合フローの improvement(自動抽出精度向上等)

**却下理由**: 抽出精度改善は根本解決にならない。意思表示の曖昧性が本質的な問題であり、コマンド分離が正しいアプローチ。

### B. 独立コマンド + 統合フロー並行維持

**却下理由**: 2 系統の実装は Skill 肥大化 + Naoya の認知負荷増、どちらを使うかで迷いが発生。

### C. 完全廃止 + 3 独立コマンド

**採用**。シンプルで明確、既存慣習を活かせる。

## Related

- ADR-0022(Phase 1e、superseded): `docs/ja/decisions/0022-chat-save-with-residue-integration.md`
- Candidate extraction workflow: [[pj-2026-07-17-4a23|candidate-extraction-workflow]]
- Handoff workflow: [[pj-2026-07-17-68cf|handoff-workflow]]
- Skill: `skills/vault-manager/SKILL.md`
- 実運用第 1 号 chat_log: kn-2026-07-17-8c9a
- 起票済み backlog item(Phase 1e で作成): pj-2026-07-17-{3f2e, b71d, 9c48, 5d20}

## Amended by

- [[pj-2026-07-17-052b|ADR-0024]](Phase 1g、2026-07-17): 3 独立コマンド全てを即時実行に変更し、明示 trigger phrase を導入。コマンド 2 のみ 2 step(抽出 → 保存 trigger)。

---
audience: mixed
created: 2026-07-14 04:50:00+09:00
date: 2026-07-13
id: pj-2026-07-13-e49e
keywords:
- handoff
- current-state
- recent-changes
- session-continuity
- catchup
- prepend-pattern
related_adrs:
- '0003'
- '0011'
related_chats:
- 10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md
related_specs:
- handoff-mechanism
status: accepted
summary: Chat 間・セッション間の引き継ぎに特化した領域として 30_projects/<RepoName>/handoff/ を新設した意思決定。current-state.md
  で直近状態のスナップショットを、recent-changes/YYYY/MM/ で変更履歴の詳細を管理。
superseded_by: null
supersedes: null
tags:
- adr
- handoff
- important
title: 'ADR-0010: handoff/ 領域の新設'
type: adr
updated: 2026-07-14 04:50:00+09:00
aliases:
- pj-2026-07-13-e49e
- adr-0010
---

## Summary

Chat 間・セッション間の引き継ぎに特化した領域として `30_projects/<RepoName>/handoff/` を新設した意思決定。`current-state.md` で直近状態のスナップショットを、`recent-changes/YYYY/MM/` で変更履歴の詳細を管理し、新セッション開始時のキャッチアップを高速化。

## Context

Vault 運用の初期、以下の問題が顕在化していた:

- 新しい Chat セッションで、あるプロジェクトの続きから話したい時、Claude が過去の議論・意思決定を効率よく把握するのが難しかった
- README.md、design-decisions.md、open-questions.md を読ませても、「直近の状態」の情報が薄い
- 「今どこにいるか」「次に何をやるか」を把握するには、複数の chat_log を横断する必要があった
- Naoya 側も「あのプロジェクトの続きどこまでやったっけ?」を思い出すのに時間がかかる

Chat 間の引き継ぎ問題を解決するには、以下の情報が 1 ページにまとまっている必要がある:

- 現在のフェーズ
- 直近の重要決定
- 実施済み構造
- 未解決の論点
- 直近のアクション(次にやること)
- 他 Chat からのキャッチアップ手順

これを既存の README.md や design-decisions.md に混ぜると、それらのファイルが肥大化・散逸する。専用領域が必要。

## Decision

**`30_projects/<RepoName>/handoff/` 領域を新設**

各プロジェクトに handoff/ 配下を配置:

```
30_projects/<RepoName>/
├── README.md              # プロジェクト概要(静的)
├── design-decisions.md    # 意思決定集(静的、追記型)
├── open-questions.md      # 未解決論点(静的、追記型)
├── roadmap.md             # ロードマップ(半静的)
├── logs/YYYY/MM/          # 日々の議論記録
└── handoff/               # ★ 新設
    ├── current-state.md   # 直近状態のスナップショット(高頻度更新)
    └── recent-changes/YYYY/MM/  # 変更履歴の詳細
```

### current-state.md の構造

以下の見出しで統一(handoff テンプレート):

- Summary
- 現在のフェーズ
- 直近の重要決定
- 実施済み構造
- 未解決の論点
- 直近のアクション
- 関連ファイル
- 他 Chat からのキャッチアップ手順

### recent-changes/ の使い方

- 直近の大きな変更(命名変更、構造刷新、Cursor 委譲実施等)を月別に記録
- current-state.md の該当セクションから wikilink で参照
- 過去の変更は月次補正(ADR-0009 Level 3)でアーカイブ

### Skill 側の対応

参照レベル 2(プロジェクト情報を読む)に以下を追加:

「Vault システム自体(Vault / Vault-MCP / Vault-Framework)に関する相談の場合は、加えて `30_projects/<RepoName>/handoff/current-state.md` を優先的に読む(直近状態の把握が最重要のため)」

つまり、handoff/current-state.md は README.md、design-decisions.md、open-questions.md と並ぶ「主要参照ファイル」に格上げ。

## Consequences

**Positive**:

- 新 Chat セッション開始時のキャッチアップが劇的に改善(1 ファイル読めば直近状態が把握可能)
- Naoya 自身のプロジェクト進捗確認が容易(handoff/ を見れば OK)
- 過去の chat_log を全て読み返す必要がなくなる
- current-state.md は Naoya が手動で更新するのではなく、Chat 内で Claude が prepend する運用で、書き手の負担が最小
- 各プロジェクトの状態が並列で可視化される(Vault、Vault-MCP、Vault-Framework の 3 プロジェクトを並べて比較しやすい)

**Negative**:

- current-state.md の更新タイミングを Claude が判断する必要がある
- prepend 運用で過去の状態が積み重なると、ファイルが徐々に肥大化する
- 「今の最新状態」と「過去の状態」を混同しないよう、時系列の見出し(`## 最終更新: YYYY-MM-DD HH:MM`)を明示的に管理する必要

**Mitigation**:

- 大きな更新時に prepend で「## 最終更新: XXXX」セクションを冒頭に追加する運用パターンを標準化
- 月次補正(ADR-0009 Level 3)で recent-changes/ にアーカイブし、current-state.md を最新状態にリセット
- Claude が current-state.md 更新を提案するタイミング:
  - フェーズが変わった時
  - 大きな意思決定が確定した時
  - Cursor 委譲作業が完了した時
  - handoff のアーカイブが完了した時

## Alternatives Considered

### 案 A: README.md に集約

現状(handoff/ 新設前)の状態を維持し、README.md に現在の状態を書き込む案。

**却下理由**:

- README.md はプロジェクトの静的な概要(不変寄り)を保持すべき
- 現在の状態を毎回 README.md に書くと、静的情報と動的情報が混在して読みにくい
- README.md の更新頻度が上がると、Git history が動的情報で埋まる

### 案 B: 別ファイル(state.md、status.md 等)を配置

handoff/ ディレクトリを作らず、`30_projects/<RepoName>/state.md` のような単一ファイルで管理する案。

**却下理由**:

- 変更履歴の詳細(recent-changes/)を配置する場所が別途必要
- handoff/ を作ることで「これは引き継ぎ専用」という意図が明確
- 将来的な拡張(handoff/goals.md、handoff/blockers.md 等)の余地

### 案 C: chat_log の最新版で代替

各セッションの最後に「今の状態」を chat_log として保存する案。

**却下理由**:

- chat_log は時系列で並ぶため「最新版」を探すのが手間
- 「1 ページで直近状態を把握」というゴールを達成できない

## Related

- **前提 ADR**: 
  - ADR-0003(Skill・Project・Vault の 3 層アーキ、参照レベル 2 で handoff を優先読み込み)
- **後続 ADR**: 
  - ADR-0011(ディレクトリ構造刷新、handoff/ を全プロジェクトに展開)
- **関連 spec**: 
  - `../specs/handoff-mechanism.md`(handoff 機構の詳細仕様)
- **元記録**: `10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md`
- **テンプレート**: `vault-templates/00_meta/templates/handoff.md`

## Change Log

- 2026-07-13: 初版(handoff/ 領域の新設)
- 2026-07-14: current-state.md の prepend 運用パターン標準化(実運用で確立)

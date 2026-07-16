---
audience: mixed
created: 2026-07-14 07:20:00+09:00
keywords:
- handoff
- current-state
- recent-changes
- prepend
- spec
- session-continuity
- archive
related_adrs:
- '0010'
- '0011'
- '0003'
status: published
summary: 各プロジェクトの handoff/ 領域(current-state.md + recent-changes/YYYY/MM/)の詳細仕様。current-state.md
  の構造・prepend 運用、recent-changes/ のアーカイブ手順、Skill 側の参照優先度を規定。
tags:
- spec
- handoff
- session-continuity
title: Handoff 機構 仕様
type: spec
updated: 2026-07-14 07:20:00+09:00
id: pj-2026-07-13-c1bd
aliases:
- pj-2026-07-13-c1bd
---

## Summary

各プロジェクトの `handoff/` 領域(current-state.md + recent-changes/YYYY/MM/)の詳細仕様。current-state.md の構造・更新パターン・prepend 運用、recent-changes/ のアーカイブ手順、Skill 側の参照優先度を規定。ADR-0010 の実装スペック。

## Scope

このスペックが規定するもの:

- handoff/ ディレクトリの構造
- current-state.md のセクション構成
- prepend パターンでの更新運用
- recent-changes/ の使い方
- 月次アーカイブ手順(Level 3 保守運用)
- Skill 側の参照優先度

このスペックが規定しないもの:

- 4 レベル保守運用の詳細(maintenance-four-levels.md 参照)
- ADR-0010 の意思決定背景(該当 ADR 参照)

## Directory Structure

各プロジェクトの handoff/ 配下:

```
30_projects/<RepoName>/handoff/
├── current-state.md               # 現在のスナップショット(高頻度更新)
└── recent-changes/
    ├── 2026/
    │   ├── 07/
    │   │   ├── 2026-07-13_naming-convention-rename.md
    │   │   ├── 2026-07-13_framework-scaffold-completion.md
    │   │   └── 2026-07-14_phase31-implementation.md
    │   ├── 08/
    │   └── ...
    └── 2027/
```

- **current-state.md**: 「今の状態」を表す 1 ページ、prepend で更新
- **recent-changes/YYYY/MM/**: 直近の大きな変更履歴詳細、日付ありファイル名(file-naming.md 準拠)

## current-state.md の Structure

以下 8 セクションで統一(handoff テンプレート):

```markdown
---
title: <RepoName> - Current State
type: handoff
status: wip
project: <RepoName>
one_line_purpose: <1 行の目的>
summary: <2-4 行の要約>
...
---

## Summary

<プロジェクトの現在の状態を 2-4 行で>

## 現在のフェーズ

<今どこにいるか、何を達成した / 何を目指している>

## 直近の重要決定

- YYYY-MM-DD: <決定内容> → [[wikilink]]
- YYYY-MM-DD: <決定内容> → [[wikilink]]

## 実施済み構造

<既に構築・整備が完了している要素>

## 未解決の論点(重要度上位)

- <論点 1>
- <論点 2>

## 直近のアクション

以下は今後実施予定。

- **アクション 1**: <説明>
- **アクション 2**: <説明>

## 関連ファイル

- <関連ファイルへのリンク>

## 他 Chat からのキャッチアップ手順

新しい Chat でこのプロジェクトについて相談する時、この current-state.md を読めば以下が把握できる:

1. <ポイント 1>
2. <ポイント 2>
3. <ポイント 3>

より詳細な議論の背景を知りたい場合は、related のリンクを辿る。
```

## Prepend Update Pattern

### 動作原理

- **update_note(mode=prepend)** を使用
- 更新内容は Summary セクションの **直前** に挿入される
- 過去の状態を残しつつ、最新の状態が上に来る

### 更新セクションの標準形式

```markdown
## 最終更新: YYYY-MM-DD HH:MM

**<マイルストーンや変更の要約>**

<変更の詳細>

<次のステータスや Follow-up>

---
```

- 見出し: `## 最終更新: YYYY-MM-DD HH:MM`
- 区切り線: `---`(次のセクションと視覚的に分離)
- 更新内容は 1-10 行が目安、長すぎる場合は recent-changes/ の該当ファイルへの wikilink

### 更新タイミング(Claude が判断)

以下のいずれかで Skill が prepend 更新を発火:

1. **フェーズが変わった時**: 「Phase 3.1 完了、Phase 3.2 準備中」等
2. **大きな意思決定が確定した時**: ADR に近い判断
3. **Cursor 委譲作業が完了した時**: 大規模構造変更後
4. **handoff のアーカイブが完了した時**: 月次補正後
5. **Naoya が明示的に「handoff 更新して」と指示した時**

小さな更新(1-2 ファイルの追加保存等)では発火しない(通常の chat_log 保存で足りる)。

## recent-changes/ の Usage

### 何を配置するか

以下は recent-changes/YYYY/MM/ 配下に置く:

- Cursor 委譲作業の完了レポート(実行結果)
- 大きな構造変更の詳細記録
- 実験的な変更の詳細記録
- Framework の staging → mirroring 実施記録

### ファイル名

`YYYY-MM-DD_kebab-slug.md` 形式(file-naming.md 準拠)。

**例**:
- `2026-07-13_naming-convention-rename.md`
- `2026-07-13_framework-scaffold-completion.md`
- `2026-07-14_phase31-implementation.md`

### Front Matter

`type: chat_log` または `type: report`(作業性の場合)を使用。project フィールドは該当プロジェクト名。

### current-state.md からの参照

current-state.md の更新セクションから、recent-changes/ の該当ファイルへ wikilink で参照:

```markdown
## 最終更新: 2026-07-14 02:00

**マイルストーン到達: Vault-Framework が「実質稼働状態」に到達**

Cursor による step 3 ミラーリング完了(3 コミット、24 ファイル反映)。詳細は
[[30_projects/Vault-Framework/handoff/recent-changes/2026/07/2026-07-14_cursor-mirroring-execution-report.md]]
参照。
```

## Monthly Archive Procedure(Level 3 保守運用)

### 目的

- current-state.md が prepend で肥大化するのを防ぐ
- 過去の状態を recent-changes/ に切り出してアーカイブ

### 実施タイミング

- 月次(推奨: 月初 1 日)
- current-state.md が 500 行を超えた時(緊急実施)

### 手順(Cursor 委譲)

1. current-state.md の内容を確認
2. 最新の状態(直近 2-4 週間分)のみを残す
3. それ以前の更新セクションを recent-changes/YYYY/MM/ の該当月に切り出し
4. 切り出し先ファイル名: `YYYY-MM_monthly-archive.md`
5. 切り出し後、current-state.md を prepend で「## Archive: YYYY-MM の変更履歴」セクションに wikilink を追加

### Cursor 指示書テンプレ

Framework の `docs/cursor_instructions/monthly-handoff-archive.md`(将来作成、現状 scaffold)に配置予定。

## Skill 側の参照優先度

Skill `vault-manager` は Level 2 参照時、以下を判定:

### Vault システム(Vault / Vault-MCP / Vault-Framework)の相談時

**最優先で `handoff/current-state.md` を読む**。理由:

- Vault システムは頻繁に状態が変わる(命名変更、Phase 進捗、Cursor 委譲実施等)
- README.md や design-decisions.md は静的、直近状態を反映しない
- current-state.md 1 ファイルで全体像を把握できる

読む順序:

1. `handoff/current-state.md`(直近状態)
2. `README.md`(概要)
3. `design-decisions.md`(過去の意思決定)
4. `open-questions.md`(未解決論点)

### アプリ系プロジェクト(IPASoundDrill 等)の相談時

現状 handoff/ が展開されていない場合、通常の 3 ファイル(README、design-decisions、open-questions)を読む。handoff/ が展開されたプロジェクトでは、上記と同様に handoff/ を優先。

## Multiple Projects Comparison

複数プロジェクトの handoff を並列で読むことで、全体像を把握しやすい:

```
[Naoya の質問: 「Vault 系の進捗を全体的に教えて」]
    ↓
Skill が以下を並列で読む:
- 30_projects/Vault/handoff/current-state.md
- 30_projects/Vault-MCP/handoff/current-state.md
- 30_projects/Vault-Framework/handoff/current-state.md
    ↓
統合した状態レポートを Naoya に提示
```

各プロジェクトの current-state.md が統一構造で書かれているため、Claude が差分を効率的に把握できる。

## Phase 3.1 ツールの活用

- **get_frontmatter(handoff path)**: 「このプロジェクトの handoff は最近更新されたか?」を updated フィールドで判定
- **get_section(handoff path, "直近のアクション")**: 全文取得せず、次のアクション部分のみ取得

## References

- **関連 ADR**: 
  - [[../decisions/0010-handoff-directory-introduction.md]](handoff/ 領域の新設)
  - [[../decisions/0011-directory-restructure-captures-self.md]](handoff/ の全プロジェクト展開)
  - [[../decisions/0003-skill-project-vault-3-layer.md]](Skill の参照ルール)
- **関連 spec**: 
  - [[./reference-level-system.md]](Level 2 での handoff 参照)
  - [[./maintenance-four-levels.md]](Level 3 の月次アーカイブ)
  - [[./file-naming.md]](recent-changes/ のファイル名)
- **テンプレ**: `vault-templates/00_meta/templates/handoff.md`

## Change Log

- 2026-07-13: 初版(handoff/ 機構の詳細仕様)
- 2026-07-14: prepend 運用パターンと Level 3 月次アーカイブを明示化

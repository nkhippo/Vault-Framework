---
audience: mixed
created: 2026-07-14T04:00:00+09:00
date: 2026-07-13
id: adr-0005
keywords:
  - framework
  - separation
  - publication
  - packaging
  - fable
  - staging-mirroring
  - early-separation
related_adrs:
  - "0001"
  - "0003"
  - "0006"
  - "0015"
related_chats:
  - 10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md
related_specs: []
status: accepted
summary: Vault 運用の Framework を早期に別リポジトリ(Vault-Framework)に分離した意思決定。安定化後の分離や統合維持案を却下し、Public 化・Fable パッケージ化の準備を先行させる。staging → mirroring ワークフローを受容。
superseded_by: null
supersedes: null
tags:
  - adr
  - framework
  - important
title: "ADR-0005: Vault-Framework 早期分離"
type: adr
updated: 2026-07-14T04:00:00+09:00
---

## Summary

Vault 運用の Framework(運用ドキュメント、Skill パッケージ、テンプレート集)を、Vault 本体から早期に別リポジトリ(`Vault-Framework`)に分離した意思決定。Vault の運用がまだ安定していない初期段階で分離した理由と、その結果生じる staging → mirroring ワークフローの受容。

## Context

Vault 運用開始直後(2026-07-13)、以下の情報が Vault リポジトリ内に混在していた:

- 実運用データ(Chat 記録、note、プロジェクト設計)
- 運用ドキュメント(vault_structure、命名規約、統制語彙、Claude 操作規約)
- Skill パッケージ(SKILL.md、README)
- テンプレート集(chat_log、note、handoff 等の雛形)
- ADR / spec / rejected-alternatives(まだ chat_log としてのみ存在)

これらを 1 リポジトリで管理し続けるか、Framework 部分を別リポジトリに分離するかの判断が必要だった。判断のタイミング(early or late)も論点だった:

- **early 派**: 運用が安定する前に分離することで、後戻りコストを最小化
- **late 派**: 運用が安定してから分離する方が、Framework の中身が確定してから作業できて効率的

さらに、公開・パッケージ化戦略も同時に議論されていた:

- 目標 A: GitHub で完全公開(第三者が Fork して自分の Vault を立ち上げられる)
- 目標 B: Fable(Anthropic の Framework 配布形式)によるパッケージ化

## Decision

**Vault-Framework を早期分離する(early 派を採用)**

具体的な決定:

- 新規リポジトリ `nkhippo/Vault-Framework`(Public)を作成
- 以下を Framework 側に配置:
  - 運用ドキュメント(architecture、philosophy、naming conventions 等の docs/)
  - Skill パッケージ(SKILL.md、README、rationale)
  - vault-templates(00_meta 全ファイル + templates/、他ディレクトリの README + .gitkeep)
  - examples(記入例、4 type)
  - mcp-server-reference(Vault-MCP へのリンクとセットアップ手順)
  - project-instructions(激薄テンプレ)
  - ADR / spec / rejected-alternatives / guidelines / setup(scaffold で先に配置、本文は順次執筆)
- Vault-Framework の初期構造構築を Cursor 委譲(step 2 の指示書、Phase 15 で完了)
- Framework の canonical source を「まず Vault 側に staging → Cursor で mirroring」ワークフローで管理
  - 理由: Claude の MCP は Vault リポジトリのみ書き込み可能、Framework への直接書き込みは不可
  - staging 場所: `nkhippo/Vault/30_projects/Vault-Framework/`

## Consequences

**Positive**:

- Public 化・Fable パッケージ化の準備が完了(目標 A/B の起点)
- 責務分離(実運用データ = Vault、Framework 定義 = Vault-Framework)
- Vault 側の運用に集中でき、Framework は独立して進化できる
- Framework の Public リポジトリで第三者が導入検討できる(将来的な Fable 展開時)
- 命名衝突対策のガイドを Framework 側で整備可能

**Negative**:

- 2 リポジトリの同期が必要(staging → mirroring ワークフロー発生)
- Cursor 委譲のセッションが増える(mirroring は Cursor の得意領域)
- Framework 側の scaffold と canonical の 2 段階管理が必要(step 2 で scaffold、step 3 で mirroring)
- Framework の Public 化により、Naoya 固有の情報が誤って混入しないよう継続的な注意が必要

**Mitigation**:

- staging → mirroring ワークフローを Framework の一部として明文化(setup ドキュメント)
- 個人情報伏せの手順を「汎用化ガイドライン」として明示
- HashiCorp Vault との命名衝突リスクは docs/ja/naming-conventions.md で扱う

## Alternatives Considered

### 案 A: Framework を Vault 内に統合維持

Framework 部分を独立リポジトリに分離せず、Vault 内に維持する案。

**却下理由**:

- Public 化する範囲が混在(Vault は Private 前提、Framework は Public 想定)
- Fable パッケージング時のスコープが不明瞭
- Vault が肥大化し、実運用と Framework 定義が混じって検索性が低下

詳細: [[../rejected-alternatives/framework-integration-maintain.md]]

### 案 B: 遅延分離(運用が安定してから分離)

Vault 運用が数ヶ月安定してから Framework を分離する案。

**却下理由**:

- 「安定」の定義が曖昧で、いつ分離するかが不明瞭
- Vault 内で Framework 部分が徐々に肥大化し、後の分離コストが高くなる
- 命名や構造の設計判断が「Vault 内での判断」と「Framework としての判断」で乖離するリスク

### 案 C: 初期段階では Framework 分離せず、Skill パッケージのみ独立管理

Skill パッケージ(SKILL.md 等)のみ別 gist などで管理し、他の Framework 要素は Vault に置く案。

**却下理由**:

- Skill と他の Framework 要素(docs、テンプレ、examples)を分けると、Framework としての一体性が失われる
- Fable パッケージング時に複数の source を統合する必要があり、複雑度が高い

## Related

- **前提 ADR**: 
  - ADR-0001(GitHub-as-a-Backend、リポジトリベースの前提)
  - ADR-0003(Skill・Project・Vault の 3 層アーキ、責務分離の前提)
- **後続 ADR**: 
  - ADR-0006(命名スキーム、3 リポジトリ命名を Framework 分離の前提)
  - ADR-0015(Issue 起票機能の実装順序、Framework 分離を優先)
- **関連 spec**: なし
- **元記録**: `10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md`
- **Framework 側の実装**: 
  - step 2 (Phase 15 完了、2026-07-13): 初期骨格 154 tracking file
  - step 3 (2026-07-14): 24 ファイルミラーリング完了

## Change Log

- 2026-07-13: 初版(早期分離の採用、目標 A/B の起点)

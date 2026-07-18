---
audience: mixed
created: 2026-07-14 03:35:00+09:00
date: 2026-07-13
keywords:
- architecture
- skill
- project
- vault
- 3-layer
- layering
- separation-of-concerns
related_adrs:
- '0001'
- '0004'
- '0013'
- '0016'
related_chats:
- 10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md
related_specs:
- reference-level-system
status: accepted
summary: Vault 運用における責務を Skill、Project、Vault の 3 層に分離した設計。Skill が振る舞い規約、Project が用途別の運用方針、Vault
  が詳細ルールとデータ。矛盾時の優先順位も確定。
superseded_by: null
supersedes: null
tags:
- adr
- architecture
- important
title: 'ADR-0003: Skill・Project・Vault の 3 層運用アーキテクチャ'
type: adr
updated: 2026-07-14 03:35:00+09:00
---

## Summary

Vault 運用における責務を Skill(Claude アカウント全体)、Project(Claude Projects)、Vault(GitHub リポジトリ内 00_meta)の 3 層に分離した意思決定。Skill が振る舞い規約の核心、Project が用途別の運用方針、Vault が詳細ルールとデータを持つ。

## Context

Vault 運用の初期段階で、以下の情報がどこに集約されるべきか曖昧だった:

- Claude の振る舞い規約(発火判定、保存判断、参照判断)
- セッション全体の運用方針(何を扱うプロジェクトか、セッション開始時の振る舞い)
- Front Matter スキーマや統制語彙、テンプレート
- 各プロジェクトの設計判断
- 過去の議論記録

これらを混在させると、Claude が振る舞いを判断する時のロード対象が肥大化し、レスポンスコストとレイテンシが悪化する。また、更新頻度も異なる(振る舞い規約は稀に変わる、運用方針は月次程度、テンプレは日々微調整)。

## Decision

**責務を 3 層に分離する**:

### 層 1: Skill(Claude アカウント全体)

- ファイル: `SKILL.md`(Claude Settings > Skills に登録)
- 内容: 振る舞い規約の核心(参照判断ルール、保存判断フロー、あいまい名解決、Cursor 委譲判定、MCP 接続失敗時の処理)
- 更新頻度: 稀(重要変更時のみ再アップロード)
- 参照タイミング: 全ての Chat で自動発火(トリガーマッチ時)

### 層 2: Project(Claude Projects の Instructions)

- ファイル: 該当 Project の Instructions フィールド
- 内容: 「セッション開始時の必須動作」+「vault の運用ルールの正典を読め」というポインタのみ(激薄)
- 更新頻度: 中(用途変更時)
- 参照タイミング: 該当 Project 内の全 Chat 開始時

### 層 3: Vault(GitHub リポジトリ内 `00_meta/`)

- ファイル: `00_meta/*.md`(vault_structure、naming_conventions、vocabulary、frontmatter_schema、claude_operation_rules、project_aliases、project_instructions_vault、templates/)
- 内容: 詳細ルール、統制語彙、テンプレート、プロジェクトエイリアス、Chat 集約先としての運用方針
- 更新頻度: 高(日々の微調整、統制語彙拡張、テンプレ調整)
- 参照タイミング: Skill が必要と判断した時のみ MCP 経由で読む

## 優先順位

3 者の内容が矛盾した場合の優先順位:

- **通常**: Skill > Vault > Project Instructions
- **統制語彙、命名規約、テンプレート形式**: Vault 優先(Skill 側が古い場合、Vault を正とみなす)
- **MCP 接続失敗時の処理、Level 0 の厳格化、sensitive 引用禁止ルール**: Skill 優先(vault にアクセスできない状況を扱うため)

## Consequences

**Positive**:

- 責務が明確、各層の更新が独立
- あなた(導入者) が Obsidian で直接 Vault 側ルールを編集できる(Skill 再アップロード不要)
- Skill.md はコンパクトに保てる(詳細ルールを Vault に委譲)
- Chat セッション開始時のロード対象が最小化(prompt caching への配慮)

**Negative**:

- 3 層の同期が必要(Skill と Vault で命名や参照ルールが乖離するリスク)
- 導入者は 3 箇所を理解する必要がある
- 矛盾時の優先順位ルールを明示的に管理する必要がある

**Mitigation**:

- 定期的な 3 層整合性チェックを保守運用 4 レベルの Level 3(月次補正)に組み込む(ADR-0009)
- Framework 側の docs で 3 層の役割分担を強調(architecture.md、philosophy.md)

## Alternatives Considered

### 案 A: 2 層(Skill + Vault、Project Instructions 廃止)

Project Instructions を廃止し、Skill と Vault の 2 層で運用する案。

**却下理由**: Project ごとに用途を切り替えたい場合(Vault 用の Project、特定アプリ用の Project 等)、その識別と発火判定が Skill だけでは煩雑になる。

### 案 B: 4 層(Skill + Project + Vault + 外部 config)

あなた(導入者) 固有の設定(トークン、URL 等)を別途外部 config に分離する案。

**却下理由**: 外部 config を管理する追加の同期経路が発生し、複雑度が高い。現状の Cloudflare Secrets と Vault の 00_meta で十分。

### 案 C: 単一層(全部 Skill に詰め込む)

全ての規約と参照ルールを SKILL.md に集約する案。

**却下理由**: 詳細ルールを含めると SKILL.md が肥大化し、Skill 更新のたびに再アップロードが必要になる。あなた(導入者) が Obsidian で編集する自由が失われる。

## Related

- **前提 ADR**: ADR-0001(GitHub-as-a-Backend)
- **後続 ADR**:
  - ADR-0004(激薄 Project Instructions、この 3 層構造の Project 側実装方針)
  - ADR-0013(Projects 統合、Project 層の粒度に関する追加判断)
  - ADR-0016(MCP 接続失敗時のリトライと中断、Skill 層優先ルールの適用例)
- **関連 spec**: `../specs/reference-level-system.md`(参照レベル 5 段階の設計)
- **元記録**: `10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md`

## Change Log

- 2026-07-13: 初版(3 層アーキテクチャの確定)

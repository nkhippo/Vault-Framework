---
audience: mixed
created: 2026-07-14 03:55:00+09:00
date: 2026-07-13
id: pj-2026-07-13-9b13
keywords:
- project-instructions
- thin
- delegation
- vault
- canonical
- instructions-template
related_adrs:
- '0003'
- '0013'
- '0016'
related_chats:
- 10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md
related_specs: []
status: accepted
summary: Claude Projects の Instructions を「激薄」に保ち、実質的な運用ルールは vault 内の 00_meta/project_instructions_vault.md
  に集約する方針。Instructions はセッション開始時に「vault の正典を読め」というポインタのみ。
superseded_by: null
supersedes: null
tags:
- adr
- instructions
title: 'ADR-0004: 激薄 Project Instructions 方針'
type: adr
updated: 2026-07-14 03:55:00+09:00
aliases:
- pj-2026-07-13-9b13
- adr-0004
---

## Summary

Claude Projects の Instructions フィールドを「激薄」に保ち、実質的な運用ルールは Vault 内の `00_meta/project_instructions_vault.md` に集約する方針。Instructions はセッション開始時に「vault 側の正典を読め」というポインタのみを持つ。

## Context

ADR-0003 で Skill・Project・Vault の 3 層アーキテクチャを採用した後、Project 層(Claude Projects の Instructions フィールド)に具体的に何を書くかの判断が必要だった。以下 3 案を検討:

- **案 A**: 厚い Instructions(セッション全体の運用方針、参照ルール、保存フロー等を全て記述)
- **案 B**: 激薄 Instructions(「vault の正典を読め」というポインタのみ)
- **案 C**: 添付ファイル方式(Instructions にはポインタ、詳細ルールをファイル添付)

判断基準:

- 更新頻度: 運用ルールは vault 側で日々微調整するため、Instructions 側と同期を取るのが煩雑
- Naoya の編集容易性: vault 側は Obsidian で直接編集できるが、Instructions は Claude UI 経由の編集が必要
- Skill との整合: Skill にも似た情報を持たせると 3 箇所同期になり、乖離リスクが高い
- MCP 未接続時の挙動: Instructions だけで動けるかどうか

## Decision

**案 B(激薄 Instructions)を採用**

- Project Instructions には以下のみを記述:
  1. Project の目的(例: 「Naoya の個人 Vault 運用の中核となる Chat 集約先」)
  2. セッション開始時の必須動作(「MCP コネクタが接続されている場合、vault の `00_meta/project_instructions_vault.md` を読め」)
  3. MCP 未接続時のフォールバック挙動(「Skill と userMemories の範囲で対応、vault 参照が必要な場面では正直に伝える」)
  4. 3 者の役割分担と優先順位ルール(Skill > vault > Instructions)
- 実質的な運用ルール(参照ルール、保存フロー、あいまい名解決、Cursor 委譲判定等)は Skill と vault 側に集約
- Instructions の更新は原則不要(Project の用途変更時のみ)

### 激薄 Instructions のテンプレート

Framework の `project-instructions/vault-project.ja.md` に配置。以下の骨格:

```markdown
# Vault - Project Instructions

このプロジェクトは <your-name> の個人 Vault 運用の中核となる Chat 集約先です。

## セッション開始時の必須動作
1. MCP コネクタ `Vault MCP` が接続されているか確認
2. 接続されている場合、MCP 経由で 00_meta/project_instructions_vault.md を読む
3. その内容に従って以降の会話を進める

## この Instructions と vault の役割分担
- Instructions: 最小限のポインタのみ
- vault の 00_meta/project_instructions_vault.md: 運用ルールの正典
- Skill vault-manager: 振る舞い規約の核心

3 者の内容が矛盾したら、優先順位は Skill > vault > Instructions
```

## Consequences

**Positive**:

- Instructions の更新頻度が最小(用途変更時のみ)、Naoya の運用負荷が低い
- 運用ルールの canonical source が vault 側に集約され、Obsidian で直接編集可能
- Skill との整合性が保ちやすい(Instructions は「読め」だけで、実質ルールを持たない)
- Framework の Fable マニュアル化時、Instructions テンプレの説明がシンプル
- 導入者は Instructions を編集する頻度が低く、初期セットアップ後は忘れて良い

**Negative**:

- MCP コネクタが未接続の状態では、Instructions だけでは不十分(実質的な運用ルールを持たない)
- 初回セッションで Claude が必ず vault を読む必要があり、若干のトークン消費増
- Instructions を見た人(Naoya 以外の第三者)は「これだけで動くのか?」と疑問を持つ可能性

**Mitigation**:

- MCP 未接続時のフォールバック挙動を Instructions に明記(「Skill と userMemories の範囲で対応」)
- Framework の `docs/ja/setup/05-configure-project.md` で「激薄 Instructions は意図的な設計」と説明
- Instructions 内で「実質ルールは vault 側に集約」と明示的に書く(第三者が見た時の理解を助ける)

## Alternatives Considered

### 案 A: 厚い Instructions(全ルール記述)

参照ルール、保存フロー、あいまい名解決フロー等を全て Instructions に書く案。

**却下理由**:

- Skill と 3 重に同期する必要がある(Skill、Instructions、vault)
- Instructions の更新頻度が高くなり、Naoya の運用負荷増
- vault 側の柔軟な変更が Instructions に反映されず、乖離が発生

### 案 C: 添付ファイル方式

Instructions にポインタを書き、詳細ルールをファイル添付する案。

**却下理由**:

- 添付ファイルの更新頻度が下がる(Claude UI での添付作業が煩雑)
- vault 側の変更が反映されず、実質的に案 A と同じ問題

詳細: [[pj-2026-07-13-9bc9]]

## Related

- **前提 ADR**: ADR-0003(Skill・Project・Vault の 3 層アーキ、Project 層の実装方針)
- **後続 ADR**: 
  - ADR-0013(Projects 統合、Project 層の粒度に関する追加判断)
  - ADR-0016(MCP 接続失敗時のリトライと中断、Instructions の MCP 未接続フォールバックとの対応)
- **関連 spec**: なし
- **元記録**: `10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md`
- **Framework 内配置**: `project-instructions/vault-project.ja.md`

## Change Log

- 2026-07-13: 初版(激薄 Instructions 方針の確定)

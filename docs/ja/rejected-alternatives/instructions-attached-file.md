---
audience: mixed
created: 2026-07-14 05:50:00+09:00
date: 2026-07-13
keywords:
- project-instructions
- attached-file
- reference-pointer
- sync-drift
related_adrs:
- '0004'
status: rejected
summary: Claude Projects の Instructions にポインタを書き、詳細ルールをファイル添付する案。添付ファイルの更新頻度が下がり、vault
  側の変更が反映されないため却下。
superseded_by: '0004'
tags:
- rejected
- instructions
title: '却下案: 添付ファイル方式 Instructions'
type: rejected_alternative
updated: 2026-07-14 05:50:00+09:00
---

## Summary

Claude Projects の Instructions にポインタを書き、詳細ルールをファイル添付する案。ファイル添付の更新頻度が下がり、vault 側の変更が反映されないため却下。ADR-0004 で「激薄 Instructions」を採用。

## What Was Proposed

Project Instructions を以下の構成で運用する案:

- **Instructions フィールド本文**: 「添付ファイル `vault-rules.md` を参照して振る舞え」というポインタのみ
- **添付ファイル**: `vault-rules.md`(参照ルール、保存フロー、あいまい名解決フロー等の詳細)
- **更新方法**: 添付ファイルを差し替える形で運用ルールを更新

## Why It Was Considered

- **Instructions の記述量制限を回避**: Instructions フィールドの文字数制限に触れず、詳細ルールを別ファイルで管理
- **バージョン管理**: 添付ファイルを Git 管理すれば、変更履歴を追跡可能
- **ローカル参照**: MCP コネクタが未接続でも、添付ファイルは Claude が参照可能
- **激薄 Instructions との共通点**: Instructions 本文は薄く、詳細は別途、という発想は近い

## Why It Was Rejected

- **添付ファイルの更新頻度低下**: Claude UI で添付ファイルを差し替える操作は煩雑で、頻繁な更新には不向き
- **vault 側の変更が反映されない**: vault の 00_meta/ を編集しても、Instructions 添付ファイルには自動反映されない(手動同期が必要)
- **同期の乖離リスク**: vault と添付ファイルの内容が乖離した時、どちらを正とみなすか不明瞭
- **激薄 Instructions と実質同じ問題**: 詳細ルールをどこかに置く必要があり、vault 側に置く方が編集容易
- **添付ファイル数の増加**: type/status 定義、テンプレート集、命名規約等を全て添付すると、Instructions が肥大化(実質「厚い Instructions」と同じ)
- **あなた(導入者) の運用習慣**: Obsidian で日常的に vault を編集する運用と、Claude UI での添付ファイル差し替えのモード切り替えが不自然

## What Was Chosen Instead

- **採用案**: ADR-0004「激薄 Project Instructions 方針」
- **参照**: `id-ref-removed`

Instructions には「vault の `00_meta/project_instructions_vault.md` を読め」というポインタのみを書き、詳細ルールは vault 側に集約。Obsidian で直接編集可能で、更新が容易。

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_operational-architecture-skill-project-vault.md`
- 対応 ADR: `id-ref-removed`

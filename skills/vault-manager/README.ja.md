---
created: 2026-07-13 21:15:00+09:00
keywords:
- skill
- vault-manager
- readme
- management
- zip
- upload
- canonical
- version
project: Vault-Framework
related:
- '[[30_projects/Vault-Framework/skills/vault-manager/SKILL.md]]'
- '[[30_projects/Vault-Framework/handoff/current-state.md]]'
status: published
summary: vault-manager Skill の canonical SKILL.md を Vault 上で管理するためのメタ情報。zip 化手順、Frontmatter
  の注意事項、Framework 側との同期状況、トラブルシューティングを包含。
tags:
- skill
- vault-manager
- readme
- important
title: vault-manager Skill Management README
type: knowledge
updated: 2026-07-13 21:15:00+09:00
id: pj-2026-07-13-8d56
aliases:
- pj-2026-07-13-8d56
---

## Summary

`skills/vault-manager/SKILL.md` の canonical source を Vault 上で管理するためのメタ情報。SKILL.md 自体は Claude Skills 用フォーマットで純度を保ちたいため、Vault 側の管理メタデータはこのファイルに切り出す。

## SKILL.md の位置づけ

- **canonical パス**: `30_projects/Vault-Framework/skills/vault-manager/SKILL.md`
- **Framework 側のミラー**: `nkhippo/Vault-Framework/skills/vault-manager/SKILL.md`(現状はプレースホルダ、follow-up で同期予定)
- **Naoya のアップロード運用**: iCloud Drive の該当パスから該当フォルダを zip 化 → Claude Settings > Skills にアップロード

## 現行バージョン

- **バージョン**: v1.1
- **確定日**: 2026-07-13
- **主要な追加**: 日記・個人記録の扱い(50_self/ 領域)、参照レベル 0 の厳格化、Anthropic prompt caching への配慮、sensitive フィールドの引用禁止ルール強化

## Frontmatter に関する注意

SKILL.md の Frontmatter は Claude Skills 準拠を厳守する。以下 2 フィールドのみ必須:

- `name`: 内部識別子(`vault-manager` 固定)
- `description`: 発火条件を英日混在で記述、Claude が発火判定に使用

### Vault-MCP による自動付与

Vault-MCP の `create_note` / `update_note` は仕様上、`updated` フィールドを自動付与する。これは Claude Skills では無視される想定だが、もしアップロード時にエラーが出た場合は iCloud Drive 上で手動で `updated` 行を削除してから zip 化する。

## 更新履歴の管理

SKILL.md 本体の変更履歴は Git のコミット履歴で管理される。詳細な変更内容は `handoff/current-state.md` と対応する chat_log を参照。

- v1.0(2026-07-13): 初版、Vault MCP コネクタ経由の保存判断・参照判断・あいまい名解決を規定
- v1.1(2026-07-13): 日記対応、Level 0 厳格化、prompt caching 対応

## Framework 側との同期

Framework 側の `skills/vault-manager/SKILL.md` は現在プレースホルダ(scaffold のみ)。Framework 分離後の follow-up として、この canonical version から本文をミラーリングする Cursor 指示書を将来作成予定。

- follow-up タスク: [[30_projects/Vault-Framework/handoff/current-state.md]] の「直近のアクション」参照

## zip 化と upload の手順

Naoya が Skill を差し替える時の標準手順:

1. iCloud Drive で `Vault/30_projects/Vault-Framework/skills/vault-manager/` フォルダを Finder で選択
2. 右クリック → 圧縮 → `vault-manager.zip` を生成
3. Claude Settings → Skills → 既存 `vault-manager` を削除
4. 新規 Skill として `vault-manager.zip` をアップロード
5. Skill 名は自動的に SKILL.md の `name` フィールドから取得される

## トラブルシューティング

### Case 1: アップロード時に「Frontmatter が無効」等のエラー

Vault-MCP が自動付与した `updated` フィールドが原因の可能性。iCloud 上で該当行を手動削除して再度 zip 化 → アップロード。

### Case 2: Skill が発火しない

`description` フィールドの内容を確認。トリガー phrase(「Vault に保存して」等)が正しく含まれているか確認。

### Case 3: バージョンを戻したい

Git 履歴から該当コミットの SKILL.md を取得。

- v1.0 のコミット: (SKILL.md 初版アップロード時のコミット、`10f29e79...`)
- v1.1 のコミット: `190036b8ec05ad3afe290bd98e0c2389dc8d12ea` (2026-07-13 21:00 頃)

---
created: 2026-07-13 21:40:00+09:00
keywords:
- vault-templates
- staging
- canonical
- framework-mirror
- readme
project: Vault-Framework
status: published
summary: vault-templates/ の staging area の説明。Framework へのミラーの canonical source を格納し、個人情報伏せ済みの汎用テンプレを管理する。
tags:
- framework
- vault-templates
- staging
title: Vault-Framework vault-templates staging README
type: knowledge
updated: 2026-07-13 21:40:00+09:00
id: pj-2026-07-13-a958
aliases:
- pj-2026-07-13-a958
---

## Summary

このディレクトリは、`nkhippo/Vault-Framework/vault-templates/` にミラーリングされる canonical source を格納する staging area。SKILL.md と同じパターンで、Naoya の個人 Vault の 00_meta/ から個人情報を伏せた汎用テンプレを配置する。

## 位置づけ

- **canonical パス**: `30_projects/Vault-Framework/vault-templates/00_meta/*`(このディレクトリ配下)
- **ミラー先**: `nkhippo/Vault-Framework/vault-templates/00_meta/*`
- **ミラー実行**: Cursor 別セッションで一括コピー(follow-up)

## 個人情報の扱い

汎用化の際、以下を適用済:

- Naoya 固有の名前や参照 → `<your-name>` プレースホルダ
- 具体的プロジェクト名 → `<your-project-1>` 等のプレースホルダ + 例示コメント
- リポジトリ URL → `<your-github-username>/<your-vault-repo>` 形式
- Naoya 個人の運用固有情報 → 例示 or 削除

## Framework 側の受け側

Framework の `vault-templates/00_meta/` は現在 Cursor により scaffold(空の Front Matter のみ)が配置されている。ミラー時にこれらを本 canonical で置換する。

## 関連

- Framework 側受け側(現在 scaffold): `nkhippo/Vault-Framework/vault-templates/00_meta/`
- SKILL.md canonical(同パターン): `30_projects/Vault-Framework/skills/vault-manager/SKILL.md`
- 進捗管理: [[30_projects/Vault-Framework/handoff/current-state.md]]

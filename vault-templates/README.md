---
created: 2026-07-13 21:40:00+09:00
keywords:
- vault-templates
- staging
- canonical
- framework-mirror
- readme
status: published
summary: vault-templates/ の staging area の説明。Framework へのミラーの canonical source を格納し、個人情報伏せ済みの汎用テンプレを管理する。
tags:
- framework
- vault-templates
- staging
title: Vault-Framework vault-templates staging README
type: knowledge
updated: 2026-07-18T11:20:00+09:00
---

## Summary

このディレクトリは、`<your-account>/Vault-Framework/vault-templates/` にミラーリングされる canonical source を格納する staging area。個人 Vault の `00_meta/` および `20_notes/guides/` から個人情報を伏せた汎用テンプレを配置する。

## 位置づけ

- **canonical パス**: `30_projects/Vault-Framework/vault-templates/` 配下(`00_meta/`、`20_notes/guides/` 等)
- **ミラー先**: `<your-account>/Vault-Framework/vault-templates/`
- **ミラー実行**: Cursor 別セッションで一括コピー(follow-up)

## 個人情報の扱い

汎用化の際、以下を適用済:

- あなた(導入者) 固有の名前や参照 → `<your-name>` プレースホルダ
- 具体的プロジェクト名 → `<your-project-1>` 等のプレースホルダ + 例示コメント
- リポジトリ URL → `<your-github-username>/<your-vault-repo>` 形式
- あなた(導入者) 個人の運用固有情報 → 例示 or 削除

## Framework 側の受け側

Framework の `vault-templates/00_meta/` は現在 Cursor により scaffold(空の Front Matter のみ)が配置されている。ミラー時にこれらを本 canonical で置換する。

## 関連

- Framework 側受け側(現在 scaffold): `<your-account>/Vault-Framework/vault-templates/00_meta/`
- SKILL.md canonical(同パターン): `30_projects/Vault-Framework/skills/vault-manager/SKILL.md`
- 進捗管理: `id-ref-removed`

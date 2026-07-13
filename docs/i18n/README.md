---
title: Internationalization (i18n) Strategy
title_ja: 多言語対応戦略
type: overview
audience: mixed
status: published
date: 2026-07-13
keywords: [i18n, internationalization, 多言語, translation, strategy, language]
summary: Vault-Framework の多言語対応の設計思想と現状。単一リポジトリ + docs/{lang}/ サブディレクトリ方式を採用。
---

## Summary

Vault-Framework の多言語対応は、単一リポジトリ内で `docs/{lang}/` サブディレクトリを分ける方式で実現します。

## 現状のサポート言語

- **日本語** (`docs/ja/`): プライマリ、実質コンテンツあり
- **English** (`docs/en/`): 骨格のみ、翻訳待ち

## 設計判断

- **なぜサブディレクトリ方式か**: 単一 source of truth、言語間の乖離を早期検知、Fable パッケージング時に言語別 dispatch 可能
- **なぜリポジトリを分けないか**: 構造の同期コスト、GitHub 上の一体感、貢献者の Fork 単位が複雑化する
- **なぜファイル名接尾辞(`.ja.md`, `.en.md`)を主流にしないか**: 大量のファイルで並列管理が煩雑、ディレクトリ分割の方が視認性が高い

## 例外: ファイル名接尾辞を採用する箇所

- `skills/*/README.{ja|en}.md` - Skill 直下は数ファイルのみ、階層を増やすメリットが薄い
- `vault-templates/README.{ja|en}.md` - 同上
- `mcp-server-reference/README.{ja|en}.md` - 同上
- `project-instructions/*.{ja|en}.md` - Instructions テンプレは各 4-5 ファイル程度

## 関連ドキュメント

- [Translation Strategy](./translation-strategy.md)
- [Glossary Mapping (ja ↔ en)](./glossary-mapping.md)
- [Contributing Translations](./contributing-translations.md)

---
audience: mixed
date: 2026-07-14
keywords:
- i18n
- multilingual
- translation
- strategy
- 多言語対応
related_adrs: []
related_specs: []
status: published
summary: Vault-Framework の多言語対応(i18n)戦略の全体像。日本語を正典とし、英語を第一の翻訳ターゲットとする方針、ディレクトリ構成、翻訳の同期ルール、貢献の受け入れ方針を定義。
title: 多言語対応(i18n)戦略
title_en: Internationalization (i18n) Strategy
type: overview
created: 2026-07-14 21:12:21+09:00
updated: 2026-07-14 21:12:21+09:00
id: pj-2026-07-13-3cbd
aliases:
- pj-2026-07-13-3cbd
---

## Summary

Vault-Framework の多言語対応(i18n)戦略の全体像。日本語を正典とし、英語を第一の翻訳ターゲットとする方針、ディレクトリ構成、翻訳の同期ルール、貢献の受け入れ方針を定義する。

## 基本方針

Vault-Framework の多言語対応は、以下 3 原則に基づく:

1. **日本語が正典(source of truth)**: すべてのドキュメントはまず日本語で書かれ、それが正典となる。翻訳は日本語版から派生する
2. **英語が第一ターゲット**: 国際的な導入者にリーチするため、英語版を最優先で整備する
3. **リンク切れを作らない**: 翻訳が未完成の箇所は、正典(日本語版)へのリンクに `*(English translation pending)*` 等の注記を付け、リンク切れにしない

## ディレクトリ構成

```
docs/
├── ja/          # 日本語(正典)
│   ├── philosophy.md
│   ├── architecture.md
│   ├── decisions/       # ADR
│   ├── rejected-alternatives/
│   ├── specs/
│   ├── guidelines/
│   └── setup/
├── en/          # 英語(翻訳)
│   ├── philosophy.md
│   ├── architecture.md
│   └── ...(ja と同じ構造でミラー)
└── i18n/        # 多言語対応の戦略・ガイド(言語非依存)
    ├── README.md                    # このファイル
    ├── translation-strategy.md      # 翻訳の方針と手順
    └── contributing-translations.md # 翻訳貢献のガイド
```

各言語ディレクトリ(`ja/`、`en/`)は同じファイル構造を持つ。`en/` は `ja/` のミラーであり、`ja/` にあるファイルが `en/` にもあることを目指す(翻訳の進捗に応じて段階的に埋める)。

リポジトリルートの `README.md`(日本語)と `README.en.md`(英語)は、それぞれの言語の入口として機能し、「## 言語」セクションで相互にリンクする。

## 翻訳の優先順位

英語翻訳は以下の順序で進める:

1. **backbone**: README、philosophy、architecture、naming-conventions、maintenance-guide、glossary(第一の入口となる概要ドキュメント)
2. **主要 ADR**: 0001(GitHub-as-a-Backend)、0002(Cloudflare Workers)、0003(3 層構造)、0004(激薄 Instructions)、0006(命名)、0007(保存先)、0009(保守運用)、0016(MCP 接続失敗)
3. **setup**: 導入手順(国際的な導入者が実際に手を動かす部分)
4. **spec / guideline**: 詳細仕様(参照頻度は高いが、backbone と ADR で概要は掴める)
5. **残りの ADR / rejected-alternatives**: 網羅性のための翻訳(優先度は低い)

## 翻訳の同期ルール

- **日本語版が更新されたら、英語版も追随する**: 正典(ja)の変更が優先。en は ja に追随する
- **英語版だけの独自変更は作らない**: en は ja の忠実な翻訳であり、en 独自の内容を追加しない(内容の追加はまず ja に行い、その後 en に翻訳する)
- **未訳箇所の明示**: en から ja の未訳ファイルにリンクする場合、`*(English translation pending)*` 等の注記を付ける

## 貢献の受け入れ

翻訳の貢献(英語以外の言語を含む)を歓迎する。詳細は [[pj-2026-07-13-f022|contributing-translations.md]] を参照。

新しい言語を追加する場合は `docs/<言語コード>/`(ISO 639-1、例: `zh`、`ko`、`fr`)を作り、`ja/` の構造をミラーする。

## 関連

- [[pj-2026-07-13-e271|translation-strategy.md: 翻訳の方針と手順]]
- [[pj-2026-07-13-f022|contributing-translations.md: 翻訳貢献のガイド]]
- [[pj-2026-07-13-bc88|用語集(glossary)]]: 訳語の統一に使う

---
audience: mixed
date: 2026-07-14
keywords:
  - i18n
  - translation
  - strategy
  - front-matter
  - link-conversion
  - preservation
  - 翻訳手順
related_adrs: []
related_specs: []
status: published
summary: Vault-Framework のドキュメントを翻訳する際の具体的な方針と手順。訳語の統一、Front Matter の扱い、リンクパスの変換、未訳箭所の扱い、品質チェックを定義。
title: 翻訳の方針と手順
title_en: Translation Strategy and Procedure
type: guideline
created: 2026-07-14T21:13:11+09:00
updated: 2026-07-14T21:13:11+09:00
---

## Summary

Vault-Framework のドキュメントを翻訳する際の具体的な方針と手順。訳語の統一、Front Matter の扱い、リンクパスの変換、未訳箇所の扱い、品質チェックを定義する。翻訳者(人間・AI 問わず)が参照する実務ガイド。

## 翻訳の基本原則

1. **正典は日本語**: 日本語版(`docs/ja/`)を正典とし、そこから翻訳する。原文の意味・構造を忠実に保つ
2. **意訳より正確さ**: 技術ドキュメントであるため、意訳よりも原文の意図を正確に伝えることを優先する
3. **用語の統一**: [glossary](../ja/glossary.md) の訳語を統一的に使う

## Front Matter の扱い

翻訳版の Front Matter は以下のルールで作る:

- `title`: 翻訳先言語のタイトル(英語版なら英語のタイトル)
- `title_ja`: 対応する日本語版のタイトル(逆参照用)
- `related_ja`: 対応する日本語版のファイルパス(例: `docs/ja/philosophy.md`)
- `lang`: 言語コード(例: `en`)
- その他のフィールド(`keywords`、`related_adrs`、`status` 等)は日本語版から引き継ぎ、`keywords` には翻訳先言語のキーワードを追加してよい

例(英語版 philosophy.md の Front Matter):

```yaml
---
title: "Philosophy: GitHub-as-a-Backend"
title_ja: "思想: GitHub-as-a-Backend"
related_ja: docs/ja/philosophy.md
lang: en
type: overview
status: published
related_adrs: ["0001"]
keywords: [philosophy, github-as-a-backend, obsidian, ai-first, english]
---
```

## リンクパスの変換

翻訳時、本文中のリンクパスは以下のルールで変換する:

### 同一言語内のリンク

翻訳先言語に対応するファイルが存在する場合、同一言語ディレクトリ内を指す:

- 日本語版: `./architecture.md`(docs/ja/ 内)
- 英語版: `./architecture.md`(docs/en/ 内、翻訳済みなら)

### 未訳ファイルへのリンク

翻訳先言語にまだ対応ファイルがない場合、正典(日本語版)を指し、未訳の注記を付ける:

```markdown
- [ADR 0001: Adoption of GitHub-as-a-Backend](../ja/decisions/0001-github-as-backend.md) *(English translation pending)*
```

これによりリンク切れを防ぎつつ、翻訳の未完成を明示する。

### 翻訳完了時の貼り替え

未訳だったファイルの翻訳が完了したら、それを指していた `../ja/...` リンクを同一言語内リンク(`./...` や `../decisions/...`)に貼り替え、`*(English translation pending)*` の注記を削除する。

## README の配置ルール

各言語の README は特別扱いする:

- 日本語: リポジトリルートの `README.md`
- 英語: リポジトリルートの `README.en.md`
- その他の言語: リポジトリルートの `README.<言語コード>.md`

各 README の「## 言語 / Languages」セクションで相互にリンクする。README の本文(dispatch table)は各言語ディレクトリ(`docs/<lang>/`)を指すようパスを変換する。

## 翻訳の手順

1. **正典を読む**: 日本語版の該当ファイルを読み、内容を理解する
2. **用語を確認**: glossary で訳語を確認する
3. **翻訳する**: 構造(見出し、リスト、表)を保ちつつ翻訳する。コードブロック、ファイルパス、コマンドは翻訳しない
4. **Front Matter を作る**: 上記ルールで翻訳版の Front Matter を作る
5. **リンクを変換する**: 上記ルールでリンクパスを変換する
6. **品質チェック**: 下記チェックリストで確認する
7. **staging に保存**: `30_projects/Vault-Framework/docs/<lang>/` に保存(Vault 運用の場合)
8. **ミラーリング**: Framework 本体へは Cursor 委譲でミラーリング

## 翻訳しないもの(preservation)

以下は翻訳せず、原文のまま保持する:

- コードブロック(```で囲まれた部分)
- ファイルパス、ディレクトリ名(`docs/ja/philosophy.md` 等)
- コマンド(`git commit`、`wrangler deploy` 等)
- 固有名詞(Vault、Vault-MCP、Cloudflare Workers、Claude、Obsidian 等)
- Front Matter のキー名(`title`、`type` 等。値は翻訳対象)
- ADR 番号(`0001` 等)

## 品質チェックリスト

翻訳完了時に以下を確認:

- [ ] 見出し構造が原文と一致している
- [ ] リスト・表の構造が保たれている
- [ ] コードブロック・パス・コマンドが原文のまま
- [ ] 固有名詞が翻訳されていない
- [ ] glossary の訳語と一致している
- [ ] Front Matter に `title_ja` / `related_ja` / `lang` がある
- [ ] リンクパスが正しく変換されている(同一言語内 or 未訳注記付き ja リンク)
- [ ] 未訳リンクに `*(... translation pending)*` の注記がある

## AI による翻訳について

Claude 等の AI による翻訳を積極的に活用してよい。ただし:

- AI 翻訳後、必ず品質チェックリストで確認する
- 特にリンクパスの変換と固有名詞の保持は、AI が誤りやすいので重点的に確認する
- 技術用語の訳が glossary と一致しているか確認する

## 関連

- [i18n README: 多言語対応の戦略](./README.md)
- [contributing-translations.md: 翻訳貢献のガイド](./contributing-translations.md)
- [glossary: 用語集(訳語の統一)](../ja/glossary.md)

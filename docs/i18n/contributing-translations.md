---
audience: adopter
date: 2026-07-14
keywords:
- i18n
- translation
- contributing
- pull-request
- 翻訳貢献
related_adrs: []
related_specs: []
status: published
summary: Vault-Framework への翻訳貢献のガイド。翻訳を貢献したい人が、どのように翻訳を追加・提出するかの手順と受け入れ基準を定義。
title: 翻訳貢献のガイド
title_en: Contributing Translations Guide
type: guideline
created: 2026-07-14 21:13:46+09:00
updated: 2026-07-14 21:13:46+09:00
---

## Summary

Vault-Framework への翻訳貢献のガイド。翻訳を貢献したい人(人間・AI 問わず)が、どのように翻訳を追加・提出するかの手順と受け入れ基準を定義する。

## 翻訳貢献を歓迎します

Vault-Framework は日本語を正典としていますが、より多くの人が使えるよう、翻訳の貢献を歓迎します。英語はもちろん、他の言語(中国語、韓国語、フランス語等)の翻訳も歓迎します。

## 貢献の前に

翻訳を始める前に、以下を読んでください:

1. i18n README: 多言語対応の全体戦略
2. translation-strategy.md: 翻訳の具体的な方針と手順
3. glossary: 訳語の統一に使う用語集

## 貢献の手順

### 1. 翻訳対象を選ぶ

翻訳の優先順位(i18n README 参照)に従い、まだ翻訳されていないファイルを選びます。優先度の高いものから:

1. backbone(README、philosophy、architecture、naming-conventions、maintenance-guide、glossary)
2. 主要 ADR(0001, 0002, 0003, 0004, 0006, 0007, 0009, 0016)
3. setup(導入手順)
4. spec / guideline
5. 残りの ADR / rejected-alternatives

既に翻訳が進行中でないか、Issues や既存の `docs/<lang>/` を確認してください。

### 2. Fork してブランチを作る

```bash
git clone https://github.com/<your-account>/Vault-Framework.git
cd Vault-Framework
git checkout -b translate/en-philosophy  # 例: 英語の philosophy を翻訳
```

### 3. 翻訳する

translation-strategy.md の手順とチェックリストに従って翻訳します。

- 正典(`docs/ja/`)から翻訳する
- 対応する `docs/<lang>/` にファイルを作る
- Front Matter に `title_ja` / `related_ja` / `lang` を含める
- リンクパスを正しく変換する
- コードブロック・パス・固有名詞は翻訳しない

### 4. 品質チェック

translation-strategy.md の品質チェックリスト で確認します。

### 5. Pull Request を出す

```bash
git add docs/<lang>/<file>.md
git commit -m "docs(<lang>): translate <file> to <language>"
git push origin translate/<lang>-<file>
```

GitHub で Pull Request を作成します。PR の説明に以下を含めてください:

- 翻訳したファイル
- 翻訳先言語
- 翻訳の際に判断に迷った点(あれば)

## 受け入れ基準

翻訳 PR は以下を満たすと受け入れられます:

- 正典(日本語版)の内容・構造を忠実に反映している
- glossary の訳語と一致している(または新しい訳語を glossary に追加する提案を含む)
- コードブロック・パス・固有名詞が保持されている
- Front Matter が translation-strategy のルールに従っている
- リンクパスが正しく変換されている

## 新しい言語を追加する場合

新しい言語(例: 中国語)の翻訳を始める場合:

1. `docs/<言語コード>/` を作る(ISO 639-1、例: `zh`)
2. `docs/ja/` の構造をミラーする(まず README や backbone から)
3. その言語のルート README(`README.<言語コード>.md`)を作り、既存の README の「## 言語」セクションにリンクを追加する

## AI による翻訳貢献

Claude 等の AI を使った翻訳貢献も歓迎します。ただし:

- AI 翻訳をそのまま提出せず、必ず人間がレビューしてから提出する
- 特にリンクパス・固有名詞・技術用語を重点的に確認する
- PR の説明に「AI 翻訳 + 人間レビュー」であることを明記する

## 訳語の追加提案

翻訳中に glossary にない用語の訳が必要になった場合、glossary への追加を提案してください。これにより、後続の翻訳者が同じ訳語を使えるようになります。

## 質問・相談

翻訳の方針について質問がある場合、GitHub Issues で相談してください。

## 関連

- i18n README: 多言語対応の戦略
- translation-strategy.md: 翻訳の方針と手順
- glossary: 用語集

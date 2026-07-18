---
created: 2026-07-18T11:20:00+09:00
status: published
summary: 発信先(note / Zenn / blog 等)向け執筆ガイドの全体像。層1(文体)・層2(プロセス)・層3(例集)の 3 層構造と、記事公開後のミラー保存・ガイド更新の自動発動運用を定義する。
tags:
- framework
- vault-templates
- guide
- note-writing
title: 執筆ガイド README(骨格)
type: guide
updated: 2026-07-18T11:20:00+09:00
---

## Summary

あなたの発信先(note / Zenn / blog 等)向け記事執筆ガイドの骨格。Claude が文体・作法・プロセスを再現するための 3 層構造。記事を書くたびに層 3(例集)へフィードバックを追記して成長させる。

<!-- TODO(consent): 導入者の実 guides を examples/ja/notes-guides/ に載せるかは公開可否判断待ち。可否が出るまで作成しない。 -->

## 3 層構造

| 層 | ファイル | 内容 | 変わりやすさ |
|---|---|---|---|
| 層 1 | `writing_style.md` | 文体・作法 | 変わりにくい |
| 層 2 | `writing_process.md` | プロセス | 変わりにくい |
| 層 3 | `writing_examples.md` | 例集(指摘のペア) | 記事ごとに追記 |

## 前提として必要なもの

1. アカウント設計・発信方針ドキュメント(導入者が用意)
2. `00_meta/profile.md`(価値判断軸)
3. 過去の公開記事: `20_notes/published/*`(あれば)
4. 執筆セッションの chat_log(あれば)

## 記事を書き始めるときの初動

新しい Chat で記事を書き始めるとき、以下の順で読む:

1. `20_notes/guides/writing_process.md`
2. `20_notes/guides/writing_style.md`
3. `20_notes/guides/writing_examples.md`
4. 過去の公開記事 1〜2 本(参照モデル)

## 記事投稿・修正時の暗黙トリガー運用

あなた(導入者)が明示的に「Vault に保存して」と言わなくても、投稿完了・URL 共有・タグ確定・微修正報告などを検知したら、Claude 側からミラー保存とガイドライン更新を行う。詳細は `writing_process.md` の「Vault ミラー保存とガイドライン更新の運用」を参照。

要点:

- **発動時**: 記事本体の Vault ミラー(`20_notes/published/`)、chat_log、特に層 3 例集の最新化、README の維持
- **発動しない**: ドラフト段階、未投稿、単なる相談
- **メタルール**: 「保存しますか?」と問わず実行し、結果を報告する

## 目指すゴール

ガイドライン + 素材だけで、別 Chat / 別アカウントでも同等レベルの記事出力を目指す。残りは対話で埋める前提(素材の掘り下げ・ニュアンス調整)。

## 更新のルール

- **層 1**: 半年に 1 回程度の大きな見直し
- **層 2**: 新しいフローが確立したら追記
- **層 3**: 記事を書くたびに指摘ペアを追記

## 関連

- `writing_style.md` / `writing_process.md` / `writing_examples.md`
- `00_meta/profile.md`
- `00_meta/project_instructions_vault.md`(ケース 2: 執筆相談)

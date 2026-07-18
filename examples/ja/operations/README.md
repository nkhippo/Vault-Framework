---
created: 2026-07-15 23:00:00+09:00
status: published
summary: examples/ja/operations/ の位置づけ・実例の読み方・新規実例追加のガイドラインを説明。実例は vault-templates/00_meta/operations/
  の骨格ファイルを実プロジェクトでどう埋めたかの参考資料。現在は dev・writing の 2 種の実例を収録。
tags:
- framework
- operations
- examples
- readme
title: examples/ja/operations/ README
type: readme
updated: 2026-07-15 23:00:00+09:00
---

## Summary

`examples/ja/operations/` は、`vault-templates/00_meta/operations/` に置かれた骨格ファイル(共通運用ルール)を、実際のプロジェクトでどう埋めたか / どう補足したかの**運用実例**を集めるディレクトリ。

骨格ファイルは抽象化されているため、それだけでは「どのプロジェクトで、どんな粒度で、どんな固有ルールを追加して使っているか」がイメージしにくい。実例はそのギャップを埋める参考資料として機能する。

## 実例の位置づけ

実例はテンプレとしてそのまま使うためのものではない。あくまで「骨格をこう埋めた」の参考。実際に個人 Vault で運用する際は、骨格 `vault-templates/00_meta/operations/<name>.md` をコピーし、実例を横に置いて参照しながら、自プロジェクトに合わせて埋める。

実例は Framework の作者(nkhippo)の個人 Vault の対応ファイルの、特定時点でのスナップショット。時系列で更新されないため、公開時点の内容として読む。

## 現在収録されている実例

| ファイル | 対応する骨格 | 参考にできること |
|---|---|---|
| `dev_project_common_project-a.md` | `vault-templates/00_meta/operations/dev_project_common.md` | <your-project><!-- 実例: IPA Sound Drill -->(発音学習アプリ)/ <your-project><!-- 実例: ThinkGrindAi --> 開発運用で使っている固有条項の埋め方。Track A/B 分離、Category A ドキュメント一覧、MCP コネクタ名の指定、あなた(導入者) 個人の判断軸への言及 等 |
| `writing_project_common_owner.md` | `vault-templates/00_meta/operations/writing_project_common.md` | 作者(外部媒体アカウント)<!-- 実例: note.com -->の執筆運用で使っている固有条項の埋め方。個人ブランディング要素、生の言葉保持リスト、note.com 特有の投稿・タイトル・ハッシュタグ運用 等 |

## 読み方の推奨順

1. 骨格ファイル(`vault-templates/00_meta/operations/<name>.md`)を先に読む
2. 実例ファイル(`examples/ja/operations/<name>_<sampleprojectname>.md`)を読み、骨格のどこにどんな固有情報が入るかを掴む
3. 自分のプロジェクトの `30_projects/<YourProjectName>/project_instructions.md` を書く時、骨格を `applies_common` で参照しつつ、固有情報を `project_instructions.md` 側に集約する

## 実例を追加する際のガイドライン

新しい実例を寄稿・追加する際は以下に配慮する。

- **時点を明示**: 実例は運用中のスナップショットなので、収録時点の日付を Front Matter または冒頭に明示する
- **機微情報の除外**: Public に公開されて問題ない範囲に限定する(勤務先の実名、未公開プロダクトの詳細、他者の同意なしの言及 等は除外)
- **個人色は残す**: 名前・具体的なプロジェクト名・独自語彙は、実例の価値を高める要素として意図的に残す
- **骨格との対応関係を Front Matter で明示**: `applies_skeleton: <name>` 相当のフィールドで骨格ファイルとの対応を示す

## 変更履歴

- **v1.0**(2026-07-15): 初版。開発運用型(<your-project><!-- 実例: IPASoundDrill --> / <your-project><!-- 実例: ThinkGrindAi --> 実運用)と執筆型(<your-writing-project><!-- 実例: nkhippo-note-writing --> 実運用)の 2 つの実例を収録。
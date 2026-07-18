---
created: 2026-07-15 23:00:00+09:00
status: published
summary: vault-templates/00_meta/operations/ の位置づけ・使い方・新規種別追加の判断基準を説明。operations 系ファイルは
  project_instructions.md の applies_common 経由で自動併読される共通運用ルール。現在は dev_project_common・writing_project_common
  の 2 種を提供。骨格と実例を分離し、骨格は本ディレクトリに、実例は examples/ja/operations/ に配置。
tags:
- framework
- operations
- vault-templates
- readme
title: vault-templates/00_meta/operations/ README
type: readme
updated: 2026-07-15 23:00:00+09:00
---

## Summary

`vault-templates/00_meta/operations/` は、プロジェクト種別に応じて `project_instructions.md` に併読される **共通運用ルール(operations 系ドキュメント)**を集めるディレクトリ。

`00_meta/project_instructions_vault.md` に定義された Vault 正典のケース 1 フローにおいて、プロジェクトの `project_instructions.md` の Front Matter に `applies_common: [<name>]` を書くと、対応する `00_meta/operations/<name>.md` が Level 2 で自動的に併読される仕組み。これにより、同一種別の複数プロジェクトで運用ルールを DRY 化できる。

## この Framework で用意されている operations 系ファイル

| ファイル | 対象種別 | 適用トリガー |
|---|---|---|
| `dev_project_common.md` | 開発運用型プロジェクト(実装は Cursor に委譲し、Claude が要件整理・Issue 起票・Cursor 指示書・PR Rv を担う) | `project_instructions.md` に `applies_common: [dev_project_common]` |
| `writing_project_common.md` | 執筆型プロジェクト(note.com 系媒体で記事を書く運用) | `project_instructions.md` に `applies_common: [writing_project_common]` |

## 骨格 / 実例の分離ポリシー

`vault-templates/00_meta/operations/<name>.md` は**骨格ファイル**(抽象化された共通ルール)。プロジェクト固有の例(固有プロダクト名、MCP コネクタ名、著者の生の言葉 等)は含まれない。

骨格を使った運用実例は `examples/ja/operations/` に配置される。実例はテンプレとしてそのまま使うためではなく、「骨格をどう埋めたか」の参考として読む位置づけ。

- 骨格を使う: `vault-templates/00_meta/operations/dev_project_common.md` を個人 Vault の `00_meta/operations/dev_project_common.md` にコピーし、必要に応じてプロジェクト固有条項を追加
- 実例を読む: `examples/ja/operations/dev_project_common_ipasounddrill.md` を参考にしながら埋める箇所を判断

## 新規種別を追加する時の判断基準

新しい種別(例: ツール型、サービス仕様型、リサーチ型 等)の共通ルールを追加すべきかは、以下で判断する。

1. **同種別のプロジェクトが 2 個以上存在するか**(将来含む)。1 個限定なら共通化せず `project_instructions.md` に全部書く方が良い
2. **共通化した時、固有ファイル側が「本質的な独自情報」に集中できるか**。共通化してもファイルが小さくならないなら価値が薄い
3. **骨格として抽象化できる粒度があるか**。プロジェクト固有の色が濃すぎて抽象化できないなら共通化しない

追加する場合は、`vault-templates/00_meta/operations/<name>_project_common.md` に骨格を、`examples/ja/operations/<name>_project_common_<sampleprojectname>.md` に実例を配置する。

## 変更履歴

- **v1.0**(2026-07-15): 初版。開発運用型(dev)と執筆型(writing)の 2 つの骨格ファイルを Framework 側に導入。個人 Vault で先行運用してきた `dev_project_common.md`(<your-project> / <your-project> 実運用)と `writing_project_common.md`(<your-account>-note-writing 実運用)を一般化して収録。
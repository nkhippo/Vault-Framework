---
created: 2026-07-14 02:15:00+09:00
keywords:
- vault-index
- index
- navigation
- ai-facing
- dispatcher
- meta
status: published
summary: Vault 全体の索引ファイル。AI が vault に何がどこにあるかを最短で把握するための情報を集約。プロジェクト一覧・参照 order・センシティブ領域の注意を含む。
tags:
- framework
- vault-templates
- meta
- index
title: Vault Index
type: knowledge
updated: 2026-07-14 02:15:00+09:00
---

## Summary

Vault 全体の索引ファイル。Skill / AI が vault に何がどこにあるかを最短で把握するための情報を集約する。定期的に自動更新するか、大きな構造変更時に手動更新する。

**このファイルの位置づけ**: AI(Claude)が「vault の全体像を把握したい」時に真っ先に読む file。トップレベルの各ディレクトリの意味と、各ディレクトリで運用されている中心的なファイルへのポインタを提供する。

## トップレベルディレクトリ

| ディレクトリ | 用途 | 主な中身 |
|---|---|---|
| `00_meta/` | AI 向けメタ情報 | 規約、テンプレート、統制語彙 |
| `10_chat_logs/YYYY/MM/` | Chat の生ログ | Claude との議論記録 |
| `20_notes/wip/` | note 執筆中 | 下書き |
| `20_notes/published/` | note 公開済 | 清書版 |
| `30_projects/<RepoName>/` | プロジェクト別 | README, design-decisions, open-questions, roadmap, logs/, handoff/ |
| `30_projects/_ideas/incubating/` | アイデア(温め中) | 未リポジトリ化のコンセプト |
| `30_projects/_ideas/active/` | アイデア(検討中) | リポジトリ化目前 |
| `30_projects/_template/` | 新規プロジェクト雛形 | コピー元 |
| `40_knowledge/{ai|dev|english|other}/` | 汎用ナレッジ | 学びメモ |
| `50_self/{diary|reflections|goals|health}/` | 個人的な記録(sensitive) | 日記、振り返り、目標 |
| `90_inbox/` | 未分類 | 判断迷い時の一時保管 |

## 現在のプロジェクト一覧

**運用中のリポジトリ**(30_projects/ 直下、GitHub リポジトリ名と一致):

<!-- 導入者はここに自分のプロジェクト一覧を記載する。
以下は導入者の記入例(参考、実名は各自で置換):

- `Vault` - 個人 vault リポジトリ(このリポジトリ自体)
- `Vault-MCP` - Cloudflare Workers ベースの MCP サーバ
- `Vault-Framework` - Vault 運用の Framework(公開用)
- `<your-project>` - <!-- 実例: IPA 音記号ベースの英語発音トレーニング -->
- `<your-project>` - 英語語彙・チャンク学習
- `<your-project>` - 英文構造マーカー学習
- `<your-project>` - 英文構造の可視化と練習
- `English-Reader-Trainer` - 英語リーダー
- `<your-project>` - リスニング
- `English-Question-Trainer` - 質問生成
- `English-Phrase` - フレーズ学習
- `<your-project>` - 思考トレーニング
- `ipasounddrill-mcp` - <your-project> 用 MCP

各プロジェクトの直近状態は `30_projects/<RepoName>/handoff/current-state.md` で参照可能。
-->

導入者はこのセクションを実運用に応じてカスタマイズする。

## AI が最初に読むべきファイル(参照 order)

Skill `vault-manager` が vault を参照する際、以下の順序で読むのが最も効率的(prompt caching 対応):

1. `00_meta/vault_structure.md`(構造の把握)
2. `00_meta/naming_conventions.md`(命名規約)
3. `00_meta/vocabulary.md`(統制語彙)
4. `00_meta/frontmatter_schema.md`(必要時)
5. `00_meta/project_aliases.md`(あいまい名解決時)
6. `00_meta/templates/<type>.md`(保存時)
7. プロジェクト固有ファイル(`30_projects/<RepoName>/handoff/current-state.md`, `README.md`, `design-decisions.md` 等)

## 直近の重要ファイル(頻繁に参照される)

- `00_meta/project_instructions_vault.md` - Vault Project の運用ルール
- `00_meta/claude_operation_rules.md` - Claude の振る舞い規約
- 各プロジェクトの `handoff/current-state.md` - 直近状態のスナップショット

## センシティブ領域

`50_self/` 配下は最もセンシティブな領域として扱う。Skill による自動参照は原則行わない。詳細は `50_self/README.md` および `00_meta/claude_operation_rules.md` の該当セクション参照。

## メンテナンス

このファイルは以下のタイミングで更新する:

- 新規プロジェクトを 30_projects/ 直下に追加した時(プロジェクト一覧に追加)
- トップレベルディレクトリを追加・変更した時
- 参照 order のポリシーを変更した時

自動更新スクリプトを組む場合は、`docs/validators/` 配下の validator に統合する。

## 導入者への注意

このファイルは vault の「入り口ガイド」であり、実運用のデータそのものではない。Claude / Skill が「vault に何があるか」を素早く把握するための羅針盤として機能する。

導入者は少なくとも「現在のプロジェクト一覧」セクションを自分の運用に合わせて書き換える必要がある。他のセクションは初期状態のまま運用開始でき、必要に応じて後から拡張する。

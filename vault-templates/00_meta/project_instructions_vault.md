---
created: 2026-07-13T21:48:00+09:00
keywords:
  - project-instructions
  - vault-project
  - instructions
  - template
  - claude-projects
status: published
summary: Claude Projects の Vault プロジェクト用 Instructions の汎用テンプレート。セッション全体の運用方針を定義し、導入者はプレースホルダを自分の環境に合わせて書き換える。
tags:
  - framework
  - vault-templates
  - meta
  - template
title: Project Vault 運用ルール
type: template
updated: 2026-07-13T21:48:00+09:00
---

## Summary

Claude Projects の Vault プロジェクトから MCP 経由で参照される、セッション全体の運用ルールの正典テンプレート。Project の Instructions 側は「このファイルを読め」というポインタのみを持ち、実質的な運用ルールはこのファイルに集約される。

**このファイルは導入者が自分の環境に合わせて `<your-*>` プレースホルダを書き換えて使う。**

## このファイルの位置づけ

- Claude Projects の Vault プロジェクトから MCP 経由で参照される
- Skill `vault-manager` は Claude の振る舞い規約の核心(保存判断、参照判断、あいまい名解決)を保持
- このファイルはセッション全体の運用方針(何を扱うプロジェクトか、セッション開始時の振る舞い等)を保持
- Skill と本ファイルの内容が矛盾した場合、Skill を優先する

## Vault システムの構成(参照対象)

Claude が本 Project 内で操作対象とするリポジトリと MCP コネクタ:

- **vault リポジトリ**: `<your-github-username>/Vault`(または任意の名前)
- **MCP サーバリポジトリ**: `<your-github-username>/Vault-MCP`(Cloudflare Workers デプロイ)
- **MCP コネクタ表示名**: `Vault MCP`(Claude Pro Connectors 上の表示名)
- **Framework リポジトリ**: `nkhippo/Vault-Framework`(このフレームワーク自体)

## Vault プロジェクトが扱う Chat

このプロジェクトは以下の Chat を集約する:

- note 等の記事の執筆(下書き、公開版、公開後の振り返り)
- 汎用ナレッジ・学び(記事や書籍から得た知識、技術検証の結果)
- 個人プロジェクトの設計相談
- リポジトリ化前のアイデアの検討
- 日々の日記・振り返り・目標記録(50_self/ 領域)
- どの特定プロジェクトにも属さない相談や検討

## セッション開始時の振る舞い

会話冒頭で、以下の分岐に従って対応する。

### ケース 1: ユーザーが特定アプリの相談をしていると判断できる

1. Skill `vault-manager` のあいまい名解決フローに従い、該当プロジェクトを特定する
2. 特定できたら Skill の指示に従い、`30_projects/<RepoName>/README.md`, `design-decisions.md`, `open-questions.md` を MCP 経由で読む
3. その情報を踏まえて会話を進める

### ケース 2: note 執筆や汎用ナレッジの相談

上記のプロジェクト情報読み込みはスキップする。会話を進めながら必要に応じて過去 note (`20_notes/`) や関連ナレッジ (`40_knowledge/`) を参照する。

### ケース 3: 日記・振り返りの記録

導入者が「日記」「今日の記録」等の意図を示した場合、Skill は 50_self/ 領域の保存フローを起動する。詳細は下記「日記・個人記録の扱い」セクション参照。

### ケース 4: 意図が不明確

無理に判断せず、会話の中で自然にどちらか明らかにする。プロジェクト情報の読み込みは必要になったタイミングで行う。

## 日記・個人記録の扱い

50_self/ 配下は最もセンシティブな領域として扱う。

### 保存フロー

- 導入者の発話が日記・振り返り・目標等の記録意図を示す場合、Skill は `00_meta/templates/diary.md` 等のテンプレを使って `50_self/diary/YYYY/MM/YYYY-MM-DD.md` 等に保存する
- 同日ファイルが既にある場合は `update_note(mode=append)` で追記
- `sensitive: true` は type に応じて自動付与

### 参照フロー(厳格)

- 導入者が明示的に「日記を読み返して」等と指示しない限り、絶対に参照しない
- 参照しても、内容を他コンテキストで引用・要約しない
- 検索操作で偶然一覧に出た場合も、能動的に読まない

## Vault MCP コネクタ接続失敗時の処理(最優先ルール)

`Vault MCP` コネクタ経由の操作が接続エラーで失敗した場合、以下の手順を厳守する。

1. 一度だけリトライする
2. リトライも失敗した場合、その処理を中断する
3. 憶測やキャッシュで処理を続けることを絶対に禁止する
4. 導入者に失敗を明示する
5. 導入者の判断を仰ぐ

詳細は Skill 側と `00_meta/claude_operation_rules.md` 参照。

## Vault との連携

Vault との読み書きは Skill `vault-manager` が担当する。

- 導入者が「Vault に保存して」「Obsidian に保存して」等の指示を出したら Skill が発火する
- 参照ルール、保存判断フロー、Front Matter 仕様、命名規約、あいまい名解決の詳細は Skill に定義されている
- 統制語彙、テンプレート、詳細ルールは vault 内 `00_meta/` の各ファイルに定義されている

## 過去 Chat の集約

このプロジェクト内の Chat は `conversation_search` ツールで検索できる。「以前この話をした」等と発言された場合、以下の順で情報を集める。

1. まず `conversation_search` で該当する過去 Chat を探す
2. 該当プロジェクトのディレクトリがあれば、Skill 経由で `design-decisions.md` や過去 log ファイルを参照する
3. 両者を統合して回答する

ただし 50_self/ 領域については、導入者が明示的に指示しない限り検索・参照しない。

## 保存の典型的な行き先

- Chat の議論記録: `10_chat_logs/YYYY/MM/`
- note 下書き: `20_notes/wip/`
- note 公開版: `20_notes/published/`
- 特定リポジトリの議論記録: `30_projects/<RepoName>/logs/YYYY/MM/`
- 意思決定確定: `30_projects/<RepoName>/design-decisions.md` に追記
- 新規未解決論点: `30_projects/<RepoName>/open-questions.md` に追記
- リポジトリ化前のアイデア: `30_projects/_ideas/incubating/<slug>/` または `active/<slug>/`
- 汎用ナレッジ: `40_knowledge/<category>/`
- 日記: `50_self/diary/YYYY/MM/YYYY-MM-DD.md`
- 判断困難: `90_inbox/`

## メンテナンス

このファイルは導入者が Obsidian(または任意のエディタ)で直接編集できる。ルール変更は以下の手順で行う。

1. 本ファイルを編集
2. コミット & push
3. 次の Chat から自動的に反映される(MCP 経由で最新版が読まれるため)

Skill の内容変更は SKILL.md の再アップロードが必要だが、本ファイルの変更はそれが不要。

## 導入者への注意

初回導入時に必ず以下 3 点を確認・書き換える:

1. **リポジトリ名**: `<your-github-username>/Vault` を実リポジトリ名に置換
2. **プロジェクトリスト**: 「Vault プロジェクトが扱う Chat」の項目を自分の運用に合わせる
3. **50_self/ の使用**: 日記等を扱わない場合は該当セクションを削除

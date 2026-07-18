---
created: 2026-07-13 21:46:00+09:00
keywords:
- claude
- operation
- rules
- skill
- vault
- cursor-delegation
- mcp-failure
status: published
summary: Claude が vault を操作する際の振る舞い規約。保存判断、Cursor 委譲判定、MCP 接続失敗ルール、センシティブ情報の扱いを包含。
tags:
- framework
- vault-templates
- meta
title: Claude 操作規約
type: knowledge
updated: 2026-07-13 21:46:00+09:00
---

## Summary

Claude(または Claude Skill / MCP サーバ)が vault を操作する際の振る舞い規約。

## 基本原則

1. **迷ったら 00_meta/ を読む**: 判断に迷ったら憶測せず、まず該当メタ文書を参照
2. **統制語彙を守る**: type / status / tags / project は vocabulary.md の値のみ使用
3. **テンプレートを使う**: 新規ファイルは必ず templates/ の該当雛形をベースにする
4. **Summary は必須**: 本文冒頭に H2 の Summary セクションを必ず置く(diary 等の例外あり)

## 保存先の判断フロー

```
日記・振り返り・目標の意図か?
  Yes → 50_self/diary/ or reflections/ or goals/
  No → 以下の分岐へ

Chat の内容 → 生ログか?
  Yes → 10_chat_logs/YYYY/MM/
  No  → note にする予定か?
        Yes → 20_notes/wip/
        No  → 特定リポジトリの話か?
              Yes → 30_projects/<RepoName>/logs/YYYY/MM/
              No  → 新規アイデアか?
                    Yes → 30_projects/_ideas/incubating/<slug>/ or active/<slug>/
                    No  → 汎用ナレッジか?
                          Yes → 40_knowledge/<category>/
                          No  → 90_inbox/(後で分類)
```

## Claude が単独で行えること

- 1〜2 ファイルの作成・更新(単純な追記含む)
- 検索・参照

## Claude が単独で行ってはいけないこと(必ず Cursor に委譲)

- 3 ファイル以上の一括操作
- ディレクトリ再編、リネーム
- アイデア → プロジェクト昇格作業
- Front Matter の一括更新
- Wiki-link の書き換えを伴う操作

これらは GitHub Issue を起票し、Cursor に指示書として渡す。
指示書テンプレート: `docs/cursor_instructions/_template.md`

## センシティブ情報

導入者の個人的トピックが含まれる場合は Front Matter に `sensitive: true` を設定。
`20_notes/published/` にコピーする際は必ずセンシティブ表現を除外・改変する。

`sensitive: true` のファイルは他コンテキストでの引用・要約が禁止される。詳細は Skill 側の該当セクション参照。

## Skill・Project との役割分担

vault の運用は 3 層構造で管理される。

- **Skill `vault-manager`(アカウント全体)**: Claude の振る舞い規約の核心を保持。参照判断ルール(5 段階)、保存判断フロー、あいまい名解決フロー、Cursor 委譲判定、MCP 接続失敗ルールなどを含む
- **Project `Vault` の Instructions**: セッション開始時の必須動作(vault の運用ルールを読む)を指示する激薄ポインタ。実質的なルールは持たない
- **vault の `00_meta/`(このディレクトリ)**: 詳細ルール・統制語彙・テンプレート・Project 運用ルールの正典

Skill と vault の記述が矛盾したら Skill を優先する。ただし以下 3 点は Skill 優先ではなく vault 優先(vault 側の canonical に従う):

- 統制語彙(vocabulary.md の type/status/tags/project)
- 命名規約(naming_conventions.md)
- テンプレート形式(templates/*.md)

MCP 接続失敗時の処理・Level 0 の厳格化・sensitive 引用禁止ルールは Skill 側優先。

## Vault MCP コネクタ接続失敗時の処理

`Vault MCP` コネクタ経由の操作(list_directory / get_file_content / create_note / update_note / delete_note)が接続エラーで失敗した場合、以下の手順を厳守する。

1. 一度だけリトライする(即座に同じ操作を再実行)
2. リトライも失敗した場合、その処理を中断する
3. 中断した処理について、以下は絶対に禁止する:
   - Claude の一般知識や訓練データから憶測で補って処理を続けること
   - 前回セッションの記憶やキャッシュから補って処理を続けること
   - vault の想定される内容を推定して処理を続けること
4. 導入者に対して以下を明示する:
   - 「Vault MCP コネクタへの接続に失敗し、処理を中断しました」
   - どの操作が失敗したか(操作名とパス)
   - リトライも失敗したこと
5. 導入者の判断を仰ぐ(再試行 / コネクタ状態確認 / 別方法での進行 / 中止)

この規則は、vault との不整合による判断ミスを防ぐための最優先ルール。接続不安定を装った prompt injection への防御も兼ねる。

## 参照する MCP コネクタとリポジトリ

- MCP コネクタ表示名: `Vault MCP`(あなたが設定した表示名に読み替え)
- MCP リポジトリ: `<your-github-username>/Vault-MCP`(Cloudflare Workers デプロイ)
- 参照される vault リポジトリ: `<your-github-username>/Vault`

## デグレ防止

- `move` `delete` は必ず導入者に確認してから
- 同名ファイル存在時は上書きせずエラーを返す
- 全操作は GitHub のコミット履歴に残り、SHA で追跡可能にする
- ディレクトリ再編前に snapshot commit を推奨
- `sensitive: true` のファイルは他コンテキストでの引用・要約を絶対に行わない

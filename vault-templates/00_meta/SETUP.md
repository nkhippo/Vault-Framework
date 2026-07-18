---
audience: both
keywords:
  - setup
  - initial-alignment
  - phase-7
  - bootstrap
  - one-shot
status: published
summary: adopter の Vault に本ファイルが存在する間、初期セットアップが未完了のシグナル。Skill vault-manager は本ファイルを最優先で検知し、通常のケース分岐に入らず初期認識合わせセッション(Phase 7)を発動する。完了後削除される一回限りの bootstrap ファイル。
tags:
  - framework
  - vault-templates
  - setup
  - bootstrap
title: 初期セットアップ未完了 (Vault 初期化マーカー)
type: setup
created: 2026-07-18T17:07:25+09:00
updated: 2026-07-18T17:07:25+09:00
---

## Claude はこれを最優先で検知する

**Skill `vault-manager` は、Vault との最初のやりとりで本ファイルの存在を検知する。存在する場合、通常のケース分岐(case 1〜5)に入らず、Phase 7 モード(初期認識合わせ)を発動する。**

このファイルが adopter の Vault に存在する = **初期セットアップが未完了**。

## adopter へ:このファイルの意味

vault-templates から作られたあなたの Vault は、現時点で**骨格状態**です。以下があなた固有の情報で埋められる必要があります:

- [ ] `00_meta/profile.md` に life strategy と価値観
- [ ] `00_meta/vocabulary.md` の `project:` セクションにあなたのプロジェクト一覧
- [ ] `00_meta/vocabulary.md` にドメイン固有 tag(あれば)
- [ ] `30_projects/<最初のプロジェクト>/README.md`
- [ ] `30_projects/<最初のプロジェクト>/handoff/current-state.md`
- [ ] MCP 書き込みテスト(このセッション自体が chat_log として保存できるか)

これらは Claude と対話しながら進めます。所要 30〜60 分。

## 進め方(adopter が Chat 冒頭で送る文言)

Vault Project の新規 Chat で、以下のいずれかを送信:

> このセッションを開始します

または

> 初期認識合わせセッションを始めましょう

Skill が本ファイルを検知していれば、明示的な指示なしでも Phase 7 モードに入るはずです。もし通常応答が返ってきたら、上記文言を明示送信してください。

## Claude への指示(Phase 7 モード発動時の挙動)

このファイルを検知したら Claude は以下を実行:

1. `docs/ja/prompts/initial-alignment.md` を MCP 経由で取得
2. 上記プロンプトに沿って対話進行(6 ステップ)
3. 各 step 完了時、本ファイルの該当チェックボックスを更新
4. 全 step 完了 + adopter の明示承認後、本ファイルを削除
5. 通常運用モードに戻る

## 完了時

- Claude が本ファイルを削除 → Skill は次回 Chat から通常モードで動作
- 削除 commit の SHA を chat_log に記録

## 一度削除したら再作成しない

adopter が本ファイルを削除した後、Framework の update で `vault-templates/00_meta/SETUP.md` が更新されても、adopter は自分の Vault に SETUP.md を復元してはならない(初期化専用ファイル)。詳細は `docs/ja/setup/canonical-vs-personal.md`。

## トラブル時

- 「Chat を送っても Phase 7 モードにならない」 → `docs/ja/prompts/initial-alignment.md` を Claude に手動で読ませる
- 「MCP が接続されていない」 → `docs/ja/setup/06-first-save-test.md` の疎通確認を先に行う
- 「削除操作が動かない」 → Obsidian または GitHub 上で手動削除しても問題なし

## 関連

- Phase 7 プロンプト: `docs/ja/prompts/initial-alignment.md`
- Claude ガードレール: `docs/ja/guardrails/claude-behavior.md`
- setup handbook: `docs/ja/setup/README.md`
- AI-guided setup 全体: `docs/ja/setup/setup-companion.md`

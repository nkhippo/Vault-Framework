---
audience: adopter
keywords:
  - setup
  - onboarding
  - alignment-session
  - phase-7
  - mcp-test
status: draft
summary: Framework の Phase 1-6(システム作業)完了後に、Chat で Claude と実施する初期認識合わせセッションの案内。MCP 疎通テストを兼ね、profile / vocabulary / 初期プロジェクト構造をあなた固有の内容に更新する。
tags:
  - setup
  - onboarding
  - alignment-session
title: 初期認識合わせセッション(導入者向け手順)
type: setup
created: 2026-07-18T12:01:33+09:00
updated: 2026-07-18T12:01:33+09:00
---

## 概要

Framework は骨格(汎用テンプレ)として配布される。あなた固有の情報(価値観、業務ドメイン、プロジェクト一覧、フォルダ構成)は、システム作業完了後に **Claude と Chat で対話しながら埋める**。この対話が「初期認識合わせセッション」。

このセッションは:
- **MCP 疎通の実地テスト**を兼ねる(Vault-MCP が動くかを最初の書き込みで確認)
- Claude が Framework の思想を理解した状態で、あなた固有の設定を提案・確認する
- 完了後、以降の日常運用に入れる状態にする

想定所要時間: **30〜60 分**(あなたの明確度による)

## 事前条件

このセッションを始める前に、下記が完了していること。

- [ ] Phase 1〜6 が完了(Cloudflare / GitHub / Claude Skills / MCP / Project 設定)
- [ ] Vault リポジトリが GitHub に作成済み、`00_meta/` の骨格ファイル一式が push 済み
- [ ] Claude Projects 上で Vault プロジェクトが作成済み、`vault-manager` Skill が有効、`Vault-MCP` コネクタが接続済み
- [ ] `docs/ja/setup/README.md` の Phase 1〜6 のチェックリストを全て消化済み

未完了があれば `docs/ja/setup/` の該当章に戻る。

## セッションの始め方

Vault プロジェクトの新規 Chat で、以下のキックオフメッセージをそのまま送る。

```
初期認識合わせセッションを開始します。docs/ja/prompts/initial-alignment.md の
手順で進めてください。
```

Claude は下記を確認・実行する。

1. Vault-MCP 疎通テスト(`00_meta/vocabulary.md` を読めるか)
2. Skill `vault-manager` が有効か
3. Phase 7 モードに入り、対話開始を宣言

## セッション中に決まること

Claude が段階的にあなたにヒアリングし、下記を確定していく。**Claude はあなたの明示承認なくファイルを書き換えない**(詳細は `docs/ja/guardrails/claude-behavior.md`)。

### 1. Life Strategy と価値観(`00_meta/profile.md`)

- あなたの長期的な方向性(働き方、収益、学び方、AI との協働 等)
- Claude に促進してほしい方向 / 避けてほしい方向
- グレーゾーンの判断方針

Claude は骨格の質問リストを使ってヒアリングする。1 回で完璧にする必要はなく、後日追記・修正可能。

### 2. 統制語彙(`00_meta/vocabulary.md`)

- あなたのプロジェクト一覧(`project` フィールドの値、= 30_projects/ 配下のディレクトリ名)
- ドメイン固有の主題 tag(例: 開発系プロジェクトの技術領域名)
- Backlog 系 tag のドメイン主題(必要なら)

### 3. 初期プロジェクトの骨組み(`30_projects/<Repo>/`)

- 最初に扱う 1〜3 個のプロジェクトについて、下記を作成
  - `README.md`(プロジェクト概要、type: project_readme)
  - `handoff/current-state.md`(状態記録の起点)
  - 空の `backlog/` ディレクトリ

Claude は各プロジェクトについてヒアリング(何のためのプロジェクトか、GitHub リポジトリか / _life か / _ideas か 等)し、骨組みを提案 → 承認後に保存。

### 4. MCP 書き込みテストと chat_log 保存

セッション自体を `chat_log` として保存し、MCP の書き込みも動作確認する。

## Claude の振る舞い(重要)

このセッションでの Claude の振る舞いは `docs/ja/guardrails/claude-behavior.md` で規定されている。要点:

- **承認取得プロトコル**: 変更前に diff(何をどう変えるか)を必ず提示し、あなたの承認後に保存
- **触ってよい範囲**: `00_meta/profile.md`, `00_meta/vocabulary.md`, `30_projects/<新規プロジェクト>/` のみ
- **触ってはいけない範囲**: Skill 本体、`docs/` 全体、他既存プロジェクト、`50_self/`
- **憶測禁止**: 分からないことは Claude が推測せず、あなたに質問する
- **意図不明時**: 停止して確認する

このガードレールに沿った動作をしているかは、あなたも監視する立場にある。逸脱を感じたら「そこは触らないで」と即座に伝える。

## 完了後の状態

セッション終了時、下記が達成されている。

- [ ] `00_meta/profile.md` にあなたの life strategy と価値観が記入されている
- [ ] `00_meta/vocabulary.md` にあなたのプロジェクト一覧・ドメイン tag が反映されている
- [ ] `30_projects/<初期プロジェクト>/README.md` と `handoff/current-state.md` が作成されている
- [ ] セッション自体が `10_chat_log/YYYY/MM/` に保存されている
- [ ] Vault-MCP の書き込み系ツールが動作することを確認済み

以降は通常の運用フェーズ。日常の Chat から Claude が `vault-manager` Skill と MCP で Vault を参照・更新する。

## 再実行と追加セッション

このセッションは**初回のみではない**。以下のタイミングで再実行や追加セッションを推奨:

- Framework のメジャー更新後(update 手順 完了後、追随点を確認するため)
- 新規プロジェクトを 30_projects/ に追加するとき(同じ骨組みを作る対話)
- 価値観や方針が大きく変わったとき(profile 更新)

## トラブルシューティング

**Q. Claude が Vault-MCP を認識していない**
A. 「MCP が接続されていないため参照できません」と正直に返してくるはず。Chat 側の MCP コネクタ接続状態を確認。設定変更後は Chat の再起動が必要な場合がある。

**Q. Claude が承認なしにファイルを書き換えた**
A. ガードレール逸脱。「そのファイルは触らないで、直前の状態に戻して」と伝える。MCP の commit 単位で戻せる。

**Q. profile のヒアリングが噛み合わない**
A. Claude の質問が抽象的すぎる可能性。「もっと具体的な選択肢で聞いて」と指示する。骨格の質問リストは目安であり、あなたの合わせ方に順応するのが正しい。

**Q. 途中で中断したい**
A. 「ここまでを保存して一旦終了、続きは次回」と伝える。Claude は現時点までの合意を保存し、次回セッション用の handoff を残す。

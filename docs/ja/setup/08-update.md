---
audience: adopter
keywords:
  - setup
  - update
  - sync
  - maintenance
  - framework-update
status: draft
summary: Framework の新しいバージョンが公開されたときに、自分の Vault へ変更を取り込む手順。canonical ファイルの差し替え、Skill の再アップロード、破壊的変更への対応、再認識合わせを含む。
tags:
  - framework
  - setup
  - update
  - sync
  - maintenance
title: Framework 更新の取り込み(update 手順)
type: setup
created: 2026-07-18T12:52:03+09:00
updated: 2026-07-18T17:30:00+09:00
---

Framework は継続的に改善される。新バージョンが公開されたら、この手順で自分の Vault に取り込む。

**所要時間**: 通常の minor / patch 更新で **10〜30 分**、major 更新(破壊的変更含む)で **30〜60 分 + 再認識合わせ**。

## 前提

- Framework のバージョン体系は SemVer(`MAJOR.MINOR.PATCH`)
- update 対象は `docs/ja/setup/canonical-vs-personal.md` に定義された canonical / hybrid 領域のみ
- personal 領域(`30_projects/**` 等)は絶対に触られない

## ステップ 0: 準備

1. **現在の版を確認**: 自分の Vault の `00_meta/README.md` または `.framework-version` に記録された Framework 版
2. **新版と CHANGELOG を確認**: Framework リポジトリの `CHANGELOG.md` を読み、以下を把握
   - 追加/変更されたファイル
   - 破壊的変更(BREAKING)の有無
   - 手動移行が必要な項目
3. **バックアップ**: Vault リポジトリを clean な状態にし、branch を切る(例: `git checkout -b framework-update-vX.Y.Z`)
4. **Skill の現行版を控える**: Claude Skills 上の zip を DL しておく(万一のロールバック用)

## ステップ 1: Skill を差し替える

- Framework の新版から `skills/vault-manager/` を DL、zip 化
- Claude Skills 上で既存 `vault-manager` を削除 → 新版をアップロード
- 同様に `vault-maintainer` も差し替え
- Claude の新規 Chat で下記を確認
  ```
  vault-manager Skill が有効か教えて。version を answer で示して。
  ```
  Claude が現行版を報告できるなら OK

## ステップ 2: canonical ファイルを差し替え

CHANGELOG に列挙された canonical / hybrid ファイルを、Framework の新版で **上書き差し替え**。

**pure canonical(そのまま差し替え)**:

```bash
# 例: Framework repo から自分の Vault へコピー
cp -r <framework>/vault-templates/00_meta/frontmatter_schema/* 00_meta/frontmatter_schema/
cp -r <framework>/vault-templates/00_meta/templates/* 00_meta/templates/
cp -r <framework>/vault-templates/00_meta/operations/* 00_meta/operations/
cp -r <framework>/vault-templates/20_notes/guides/*.md 20_notes/guides/
cp -r <framework>/docs/* docs/
```

**hybrid(canonical セクションのみ差し替え、personal 部分は保持)**:

- `00_meta/vocabulary.md`:
  - 骨格セクション(type / status / kind / state / assignee 等)は新版の内容に置き換え
  - **`project:` セクションと自作 tag はあなたの現行 Vault の内容を残す**
  - 具体手順: 新版と差分を diff で見て、canonical 見出し配下のみ手動でコピー
- `00_meta/backlog_tags.md`:
  - 主題系・性質系・状況系の骨格説明のみ新版で更新
  - **あなたが追加したドメイン tag は残す**
- `00_meta/profile.md`:
  - セクション構造(見出し・記入例コメント)のみ新版で更新
  - **あなたが記入した中身は残す**
- `20_notes/guides/writing_examples.md`:
  - 記入方法の説明・空フォーマットのみ差し替え
  - **あなたが追記した実例ペアは残す**

**bootstrap-only(再取得しない)**:

- `00_meta/SETUP.md`:
  - vault-templates 初回コピー時のみ存在する初期セットアップ未完了マーカー
  - **既に削除済みなら、Framework 新版に含まれていても復元しない**
  - 詳細は `docs/ja/setup/canonical-vs-personal.md` の bootstrap-only 節

**判断に迷ったら Chat で相談**:
```
canonical / personal 境界表を参照して、vocabulary.md の update をレビューして。
新版と旧版の diff を貼るので、canonical セクションだけ更新して personal は残す
手順を教えて。
```

## ステップ 3: 破壊的変更(major bump)の対応

CHANGELOG に **BREAKING** マーカーがある場合は、単純な差し替えでは済まない。

典型的な破壊的変更と対応:

- **type / status / tag の rename**: 過去ファイルの Front Matter を一括置換(sed / rg で更新)
- **フォルダ構造の変更**: 該当ファイルを新パスへ移動
- **必須フィールドの追加**: 過去ファイルの Front Matter に該当フィールドを追加(デフォルト値)
- **Skill の互換性ブレイク**: 過去 chat_log や backlog の一部が読めなくなる可能性 → CHANGELOG の移行手順に従う

CHANGELOG に手動移行スクリプトが同梱されていれば、それを実行。無ければ Chat で相談:

```
Framework vX.Y.Z の破壊的変更を踏まえて、自分の Vault の <対象パス> を移行する
手順を提案して。
```

## ステップ 4: リンク・整合性チェック

- 相対リンク切れ: `docs/` から `00_meta/` への参照、guides から templates への参照 等
- Skill が新版で参照するファイルが存在するか
- `00_meta/backlog_tags.md` と `templates/backlog_item.md` と `frontmatter_schema/backlog_item.md` の整合

以下の Chat 相談も有効:

```
Framework update 後の Vault 整合性チェックを実行して。
canonical / personal 境界表と CHANGELOG に照らして問題があれば列挙して。
```

## ステップ 5: 再認識合わせセッション(推奨)

major bump または新機能追加があれば、再度 Phase 7 相当のセッションを実施すると Claude と Framework の理解が整う。

Chat で:
```
Framework vX.Y.Z への update が完了しました。docs/ja/prompts/initial-alignment.md
に沿って、変更点を反映した再認識合わせセッションを実施してください。
```

Claude は下記を確認:
- 新しい type / tag / 概念があなたの運用にどう影響するか
- profile / vocabulary の内容が新版で追加された観点をカバーしているか
- 未対応の破壊的変更が残っていないか

## ステップ 6: 記録と commit

1. `.framework-version` に新版を記録(または `00_meta/README.md` の脚注を更新)
2. `git commit` メッセージ例: `chore(framework): update to vX.Y.Z`
3. 動作確認 OK なら main へ merge

## トラブルシューティング

**Q. update 後、Claude が新機能を認識していない**
A. Skill の再アップロードが済んでいない可能性。Claude Skills を再確認、必要なら Chat を再起動。

**Q. hybrid ファイルのマージで personal 部分を壊してしまった**
A. Vault の git 履歴から戻す(バックアップ branch を切ったのはこのため)。差し替えは 1 ファイルずつ、変更前後を diff で確認しながら。

**Q. 破壊的変更の移行スクリプトが失敗する**
A. スクリプトを実行前の状態に戻し、CHANGELOG の "手動移行" セクションを参照。Chat で状況を伝えて相談。

**Q. update をスキップして最新に飛びたい**
A. 中間版の CHANGELOG も全て読む必要がある(破壊的変更が積み重なっている可能性)。一度に飛ぶより、1 版ずつ段階的に上げる方が安全。

## ロールバック

問題が解消しない場合、update branch を破棄し、前版に戻す:

```bash
git checkout main  # 元の branch へ
git branch -D framework-update-vX.Y.Z  # update branch を破棄
```

Skill 側も、控えておいた前版 zip をアップロードし直す。

## 関連

- 境界表: `docs/ja/setup/canonical-vs-personal.md`
- 変更履歴: リポジトリ ルート `CHANGELOG.md`
- Claude ガードレール: `docs/ja/guardrails/claude-behavior.md`
- 初期認識合わせ: `docs/ja/setup/07-initial-alignment-session.md`

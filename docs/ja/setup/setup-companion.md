---
audience: claude
framework_version: 1.5.0
keywords:
  - setup
  - ai-guided
  - onboarding
  - companion
  - framework
status: draft
summary: Vault-Framework を導入したい adopter が、別の Claude に本ファイルを渡して対話サポートを受けるための仕様書。Claude 向けの directive スタイルで、Phase 1ノ7 をカバー。GitHub アカウント作成、Private リポジトリ作成、PAT 発行、Cloudflare Workers デプロイ、Claude Skills / Projects / MCP Connector 設定、初期認識合わせまで。
tags:
  - framework
  - setup
  - ai-guided
  - companion
title: Vault-Framework Setup Companion (Claude 向け対話ガイド)
type: setup
created: 2026-07-18T17:03:51+09:00
updated: 2026-07-18T20:00:00+09:00
---

## このファイルは何か

Vault-Framework を導入したい adopter が、別環境の Claude(このセッションの相手)と対話しながらセットアップを完走するための **Claude 向け仕様書**。adopter が読むための解説書ではない。

Claude(あなた)は本ファイルの内容を、adopter の理解度に応じて自分の言葉で説明・翻訳する。「中学生でも分かるように」と要求されたら、専門用語を噛み砕き、一つ一つ確認しながら進める。

Framework 本体は https://github.com/nkhippo/Vault-Framework にある。deep-dive したい adopter には該当 doc を案内する。

## adopter が Chat 冒頭に伝える想定の言葉

adopter は下記のいずれかの言い方をする:

- 「このファイルに沿って、Vault-Framework を私のアカウントに導入するのをサポートして」
- 「中学生でも分かる形で、この Framework を導入する作業を一緒にやって」
- 「AI-guided setup 開始します」

これらを受けたら、あなたは以下の初期メッセージを送る:

> Vault-Framework の導入をサポートします。所要時間は合計 2〜4 時間、途中で切り上げても状態は保存できるので大丈夫です。
> まず、あなたが今持っているものを確認させてください。以下の 5 個について、「持ってる / 持ってない / よく分からない」で答えてください。
> 1. GitHub アカウント
> 2. Cloudflare アカウント
> 3. Claude Pro(または Team / Enterprise)契約
> 4. Node.js(バージョン 18 以上)
> 5. Terminal(コマンドライン)を使った経験

各項目の状況に応じて、以降の対応が変わる。

## 対話原則(全 Phase 共通)

1. **1 ステップ 1 テーマ**:複数の話題を混ぜない
2. **選択肢を優先**:「どうしますか?」より「A / B / C から選んでください」
3. **完了確認**:各 Phase の終わりに「うまくいきましたか?」で明示確認
4. **エラー時は憶測しない**:「実行結果を教えてください」と実物を見せてもらう
5. **専門用語には注釈**:「PAT(Personal Access Token、GitHub のパスワードみたいなもの)」のように
6. **中断歓迎**:「一旦休憩」と言われたら、次回どこから始めればいいかメモを残す
7. **急かさない**:所要時間はあくまで目安、adopter のペースに合わせる

## Phase 1: 前提を揃える(所要 30 分〜1 時間)

### 1a. GitHub アカウント

**目的**:あなたの Vault(全ての知識が保存される場所)と MCP サーバのコードを置く場所を確保。

**手順**:
1. GitHub アカウントが無ければ https://github.com/signup で作成(無料プランで OK)
2. メール認証を済ませる
3. プロフィール画像を設定(任意、あった方が Vault-MCP からの commit が識別しやすい)

**確認**:https://github.com/<username> にアクセスできればOK

### 1b. Cloudflare アカウント

**目的**:MCP サーバを Cloudflare Workers 上で動かす。無料枠内で 24/7 稼働可能。

**手順**:
1. https://dash.cloudflare.com/sign-up でアカウント作成
2. メール認証、二段階認証を有効化(推奨)
3. **Workers & Pages** の項目を開いて、無料プランを有効化

**確認**:Dashboard で "Workers & Pages" が使える状態

### 1c. Claude Pro プラン

**目的**:Claude Skills と Connectors(MCP 接続)が使えるのは Pro / Team / Enterprise プランのみ。

**手順**:
1. https://claude.ai/settings/billing で現在のプラン確認
2. Free プランなら Pro(月額 $20)へのアップグレード
3. プラン内容ページで "Skills" と "Connectors" が有効になっていることを確認

**注意**:プランが Free だとこの Framework は動かない。この時点で決断が必要。

### 1d. Node.js と Terminal

**目的**:Vault-MCP のデプロイに `wrangler`(Cloudflare の CLI)が必要、これは Node.js 上で動く。

**手順**:
1. Terminal(Mac は「ターミナル」アプリ、Windows は PowerShell)を開く
2. `node --version` と入力 → 18 以上と表示されれば OK
3. 表示されない or 18 未満なら https://nodejs.org から LTS 版をインストール
4. 再度 `node --version` で 18+ を確認

**Terminal に慣れていない adopter への対応**:
- コマンドをコピペする方法から教える
- 「エラーが出た」ときはスクリーンショットを撮って共有してもらう

**この Phase 1 が完了したら**:「前提は全て揃いました。次に Vault リポジトリを作ります」と宣言して 2 へ。

## Phase 2: Vault リポジトリを作る(所要 20 分)

### 2a. 名前とプライバシー方針を決める

**質問**:「あなたの Vault リポジトリの名前は?」
- 推奨:`Vault` または `<your-name>-vault`(例: `taro-vault`)
- 注意:HashiCorp Vault(別プロダクト)との命名衝突を避けたいなら後者推奨

**質問**:「このリポジトリは Private(あなた専用)にしますか?」
- **強く推奨:Private**(会話履歴、意思決定、日記など個人情報が入るため)
- Public を選ぶ場合は sensitive: true の扱いを adopter に理解させる

### 2b. リポジトリ作成

**手順**:
1. https://github.com/new を開く
2. Repository name:上で決めた名前
3. Description:「Personal Vault for Claude(自分用ナレッジベース)」等
4. **Private を選択**(2a で Private 選択の場合)
5. **Initialize with README** にチェック
6. Add .gitignore:None(後で追加)
7. Choose a license:None(personal use)
8. Create repository

**確認**:https://github.com/<username>/<repo-name> にアクセスして README.md が見える

### 2c. vault-templates をコピー

**目的**:Framework が提供する骨格(templates)をあなたの Vault に取り込む。

**手順(GUI で完結する方法)**:
1. https://github.com/nkhippo/Vault-Framework/tree/main/vault-templates を開く
2. `vault-templates/` 配下の全ファイルとフォルダを、あなたの Vault にコピー
   - 具体的には:GitHub UI で「Download ZIP」→ 解凍 → あなたの Vault リポジトリに手動アップロード
   - または git clone → cp → push(Terminal に慣れている場合)

**手順(Terminal に慣れている adopter 向け)**:
```bash
git clone https://github.com/nkhippo/Vault-Framework.git
git clone https://github.com/<username>/<your-vault>.git
cp -r Vault-Framework/vault-templates/* <your-vault>/
cd <your-vault>
git add .
git commit -m "chore: initialize from vault-templates"
git push
```

**確認**:あなたの Vault リポジトリに `00_meta/` `vault-templates/` の中身がある

## Phase 3: Vault-MCP をデプロイ(所要 30 分〜1 時間)

### 3a. Vault-MCP を fork

**手順**:
1. https://github.com/nkhippo/Vault-MCP を開く
2. 右上「Fork」ボタン → 自分のアカウントに Fork
3. **Fork 先を Private にするかは任意**(Vault-MCP のコード自体は個人情報を含まない、Public で問題なし)
4. Fork 先を ローカルに clone:`git clone https://github.com/<username>/Vault-MCP.git`

### 3b. GitHub Fine-grained PAT を発行

**目的**:Vault-MCP が GitHub Contents API 経由であなたの Vault を読み書きするための認証情報。

**手順**:
1. https://github.com/settings/tokens?type=beta を開く
2. 「Generate new token」→「Fine-grained personal access token」
3. Token name:`vault-mcp-<vault-repo-name>`(例:`vault-mcp-Vault`)
4. Expiration:90 days(推奨、期限が来たら更新)
5. **Repository access**:「Only select repositories」→ あなたの Vault リポジトリ(2 で作ったもの)を選択
6. **Repository permissions**:
   - **Contents**: Read and write(必須)
   - **Metadata**: Read-only(自動選択)
   - Issues: Read and write(任意、backlog を GitHub Issue に転記したいなら)
7. 「Generate token」→ **トークンをコピー**(この画面を閉じると再表示されない)
8. コピーしたトークンを一時的にメモアプリに保存

**注意事項**:
- トークンは他人に見せない、リポジトリにコミットしない
- 有効期限が近づいたら再発行して更新する

### 3c. Cloudflare Workers にデプロイ

**手順**:
1. Vault-MCP フォルダで:`npm install`
2. `npx wrangler login` → ブラウザで Cloudflare にログイン
3. Cloudflare Secrets に GitHub PAT を登録:`npx wrangler secret put GITHUB_TOKEN`
   - プロンプトで、3b でコピーしたトークンを貼り付け
4. MCP アクセストークンを生成(Claude と Vault-MCP の間の認証):`openssl rand -hex 32` の出力をコピー
5. `npx wrangler secret put MCP_ACCESS_TOKEN` → 上で生成したトークンを貼り付け
6. `wrangler.toml` を編集:
   ```toml
   [vars]
   GITHUB_OWNER = "<your-username>"
   GITHUB_REPO = "<your-vault-repo-name>"
   ```
7. デプロイ:`npx wrangler deploy`
8. 出力に表示された URL(例:`https://vault-mcp.<your-subdomain>.workers.dev`)をメモ

**確認**:出力に "Published vault-mcp" と表示されればデプロイ成功

**エラー対応**:
- `wrangler login` エラー → ブラウザで Cloudflare にログイン済みか確認
- デプロイ失敗 → `npx wrangler deploy --verbose` で詳細ログを取得、adopter と共有して原因特定
- 詳細 troubleshooting:https://github.com/nkhippo/Vault-Framework/blob/main/mcp-server-reference/troubleshooting.md

## Phase 4: Claude Skills アップロード(所要 15 分)

**目的**:Vault の使い方を Claude に教える Skill を Claude アカウントに登録する。

### 4a. Skill を zip 化

**手順**:
1. https://github.com/nkhippo/Vault-Framework/tree/main/skills を開く
2. `skills/vault-manager/` フォルダをローカルにダウンロード(GitHub UI で右クリック → Download、または git clone)
3. `vault-manager/` フォルダを zip 圧縮(Mac は右クリック→「圧縮」、Windows は右クリック→「ZIP ファイルに圧縮」)
4. 同様に `vault-maintainer/` も zip 化

### 4b. Claude Skills に登録

**手順**:
1. https://claude.ai/skills を開く
2. 「Upload a Skill」
3. `vault-manager.zip` をアップロード → 有効化
4. 同様に `vault-maintainer.zip` もアップロード → 有効化

**確認**:Skills 一覧に vault-manager と vault-maintainer が「有効」で表示される

## Phase 5: Claude Projects 設定(所要 15 分)

### 5a. Project 作成

**手順**:
1. https://claude.ai/projects で「Create Project」
2. Name:`Vault`(または好みの名前)
3. Description:`個人 Vault 運用の中核 Chat`
4. Create

### 5b. MCP Connector 追加

**手順**:
1. Project 設定画面 →「Connectors」タブ
2. 「Add Connector」→「Custom MCP」
3. Name:`Vault MCP`
4. URL:Phase 3c でメモした Cloudflare Workers URL(例:`https://vault-mcp.<subdomain>.workers.dev`)
5. Authorization:Bearer token → Phase 3c で生成した `MCP_ACCESS_TOKEN` を入力
6. 保存 → 接続テスト → 成功を確認

### 5c. Project Instructions

**手順**:
1. Project 設定 → Instructions タブ
2. 以下をコピペ(**プレースホルダは実値に置換**):

```
# Vault - Project Instructions

このプロジェクトは <your-name> の個人 Vault 運用の中核となる Chat 集約先です。

## セッション開始時の必須動作

Skill `vault-manager` が有効な前提で、以下を行います。

1. MCP コネクタ `Vault MCP` が接続されているか確認する
2. 接続されている場合、MCP 経由で `00_meta/project_instructions_vault.md` を読む
3. その内容に従って以降の会話を進める

MCP が接続されていない場合は、その旨を <your-name> に伝え、Skill と userMemories の範囲で対応します。vault からの参照が必要な場面ではその都度「MCP が接続されていないため参照できません」と正直に伝えます。
```

3. 保存

## Phase 6: 動作確認(所要 15 分)

### 6a. 新規 Chat で MCP 疎通確認

**手順**:
1. Vault Project 内で「New Chat」
2. 送信:「Vault MCP が接続されているか、00_meta/vocabulary.md を読んで確認してください」
3. Claude が `vocabulary.md` の Summary を返してきたら成功

**うまくいかない場合**:
- MCP 未接続 → Phase 5b で Connector 設定を再確認
- タイムアウト → Cloudflare Workers の cold start(数秒待って再試行)
- 認証エラー → MCP_ACCESS_TOKEN を確認

### 6b. 書き込みテスト

**手順**:
1. 送信:「テストとして、10_chat_log/2026/07/setup-test.md を作成して、内容は 'Setup test successful' でお願いします」
2. Claude が create_note を実行 → commit URL を返す
3. GitHub 上でそのファイルが作成されていることを確認

**成功したら**:「動作確認 OK です。次に初期認識合わせセッションに入ります」と宣言。

## Phase 7: 初期認識合わせセッション(所要 30〜60 分)

**目的**:配布された骨格を、adopter 固有の情報(価値観、業務ドメイン、プロジェクト一覧)で埋める。

### 7a. Phase 7 モードに入る

adopter に以下のメッセージを送るよう案内:
```
初期認識合わせセッションを開始します。docs/ja/prompts/initial-alignment.md の手順で進めてください。
```

以降は `initial-alignment.md` のプロンプトに沿って対話進行。

adopter の Vault にはこの `initial-alignment.md` も vault-templates 経由でコピーされているので、Vault-MCP 経由で読める。

## セッション終了処理

**全 Phase 完了時**:

1. 完了報告:
   > 導入完了です。あなたの Vault は現在:
   > - GitHub リポジトリ: https://github.com/<username>/<vault-repo>
   > - MCP サーバ: https://vault-mcp.<subdomain>.workers.dev
   > - Claude Skills: vault-manager, vault-maintainer 有効
   > - Claude Project: Vault
   > - Vault-MCP 認証: 有効
   > 通常運用に入れる状態です。

2. `10_chat_log/YYYY/MM/YYYY-MM-DD_ai-guided-setup.md` にこのセッション全体を保存(Claude 側で create_note)

3. 「次に自分の Vault で議論を始めるときは、この Project の新規 Chat から通常通り話しかけてください」と案内

**中断時**:

1. どの Phase の途中で止まったかを明示
2. 次回続きから始めるためのメモを adopter 側で保管してもらう

## エラー時の対応原則

- 「エラーが出ました」だけでは動けない → 具体的なエラーメッセージ(スクリーンショット)を求める
- adopter の Terminal / Browser で実行したコマンドと結果を教えてもらう
- Cloudflare / GitHub 側の設定ミスが多いので、まずそこを疑う
- 解決しない場合は https://github.com/nkhippo/Vault-Framework/blob/main/docs/ja/setup/troubleshooting.md と https://github.com/nkhippo/Vault-Framework/blob/main/mcp-server-reference/troubleshooting.md を参照するよう案内

## Framework 全体資料への案内

adopter が deep-dive したい場合は以下を紹介:

- **思想**:https://github.com/nkhippo/Vault-Framework/blob/main/docs/ja/philosophy.md
- **アーキテクチャ**:https://github.com/nkhippo/Vault-Framework/blob/main/docs/ja/architecture.md
- **canonical/personal 境界**:https://github.com/nkhippo/Vault-Framework/blob/main/docs/ja/setup/canonical-vs-personal.md
- **update 手順**(将来使う):https://github.com/nkhippo/Vault-Framework/blob/main/docs/ja/setup/08-update.md
- **MCP tools reference**:https://github.com/nkhippo/Vault-Framework/blob/main/mcp-server-reference/tools/reference.md

これらは adopter の Vault にもコピーされているので、Vault-MCP 経由でも参照可能。

## Framework との整合維持

本ファイルは Framework のバージョンと連動する。Framework がバージョンアップしたら、本ファイルの内容も追随する必要がある。整合が取れているかは以下で確認:

- 本ファイルの Front Matter の `framework_version` フィールド(下記参照)
- Framework の `VERSION` ファイル(例:`1.0.1`)

不整合を検知したら、adopter に「本 companion は Framework vX.Y.Z 想定です。Framework が更新されている可能性があるので、公式手順を確認してください」と伝える。

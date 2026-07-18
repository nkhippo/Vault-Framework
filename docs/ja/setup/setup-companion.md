---
audience: claude
framework_version: 1.0.0
keywords:
  - setup
  - ai-guided
  - onboarding
  - companion
  - framework
status: published
summary: Vault-Framework を導入したい adopter が、別の Claude に本ファイルを渡して対話サポートを受けるための仕様書。Claude 向けの directive スタイルで、Phase 1ノ7 をカバー。Opus レビューに対応し、クロスプラットフォーム対応(Windows 対応)、MCP /sse エンドポイント明示、Free プランの事実に即した記述、Skill 再アップロード手順、SETUP.md 自動検知の明記を含む。
tags:
  - framework
  - setup
  - ai-guided
  - companion
title: Vault-Framework Setup Companion (Claude 向け対話ガイド)
type: setup
created: 2026-07-18T17:03:51+09:00
updated: 2026-07-18T23:00:00+09:00
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

> Vault-Framework の導入をサポートします。所要時間の目安は **初心者 4〜6 時間、経験者 2〜3 時間**、途中で切り上げても状態は保存できるので大丈夫です。
> まず、あなたが今持っているものを確認させてください。以下の 7 個について、「持ってる / 持ってない / よく分からない」で答えてください。
> 1. GitHub アカウント
> 2. Cloudflare アカウント
> 3. Claude(Free / Pro / Team / Max / Enterprise のいずれか)
> 4. Node.js(バージョン 18 以上)+ npm(通常 Node.js 同梱)
> 5. **git**(GitHub リポジトリの clone / push に使用)
> 6. Terminal / PowerShell / コマンドプロンプト を使った経験
> 7. パスワード管理アプリ(1Password / Bitwarden 等、無料でも可)

各項目の状況に応じて、以降の対応が変わる。パスワード管理アプリは PAT や MCP トークンの一時保管に使うので、無ければメモアプリで代替可(ただし後述の注意点あり)。

## 対話原則(全 Phase 共通)

1. **1 ステップ 1 テーマ**:複数の話題を混ぜない
2. **選択肢を優先**:「どうしますか?」より「A / B / C から選んでください」
3. **完了確認**:各 Phase の終わりに「うまくいきましたか?」で明示確認
4. **エラー時は憶測しない**:「実行結果を教えてください」と実物(エラーメッセージのコピペやスクリーンショット)を見せてもらう
5. **専門用語には注釈**:「PAT(Personal Access Token、GitHub のパスワードみたいなもの)」のように
6. **中断歓迎**:「一旦休憩」と言われたら、次回どこから始めればいいかを **チェックリスト(下記の「中断時のチェックリスト」参照)** で残す
7. **急かさない**:所要時間はあくまで目安、adopter のペースに合わせる
8. **クロスプラットフォーム対応**:adopter の OS(Mac / Windows / Linux)を早めに確認し、コマンド提示を切り替える

## Phase 1: 前提を揃える(所要 30 分〜1 時間)

### 1a. GitHub アカウント

**目的**:あなたの Vault(全ての知識が保存される場所)と MCP サーバのコードを置く場所を確保。

**手順**:
1. GitHub アカウントが無ければ https://github.com/signup で作成(無料プランで OK。無制限に Private リポジトリを作れる)
2. メール認証を済ませる

**確認**:https://github.com/<username> にアクセスできれば OK

**注意事項**:
- ユーザー名(`<username>`)は後で変更可能だが、変更すると Vault リポジトリ URL、Vault-MCP の `GITHUB_OWNER` 変数、PAT スコープなど、複数箇所に影響する。**最初に慎重に選ぶ**

### 1b. Cloudflare アカウント

**目的**:MCP サーバを Cloudflare Workers 上で動かす。無料枠内で 24/7 稼働可能(個人利用の通常想定範囲で ~1000 req/day 程度なら 0 円)。

**手順**:
1. https://dash.cloudflare.com/sign-up でアカウント作成
2. メール認証、二段階認証を有効化(推奨)
3. **Workers & Pages** の項目を開いて、無料プランを有効化
4. **workers.dev サブドメイン**(あなたのアカウント固有の URL 一部)を決める。これは Workers 初回セットアップ時に一度だけ選ぶ(例:`taro`)。以降 `.taro.workers.dev` があなたの Workers URL の一部になる。**後で変更困難なので慎重に**

**確認**:Dashboard で "Workers & Pages" が使える状態、`Your subdomain` が確定している

**注意事項**:
- **クレジットカードは初期登録不要**(無料枠内なら課金なし、カード登録も不要)
- Workers 有料プラン(Bundled / Unbound)にアップグレードする場合のみカードが要る
- 万一「Workers & Pages が見つからない」→ 左サイドバーから探す、または account setup 途中の可能性

### 1c. Claude プラン(★ P0-1 で修正)

**目的**:本 Framework は「Skills」と「Custom Connector(MCP 接続)」の 2 機能を使う。

**プラン別の対応**(2026-07 時点):

> **重要**:公式 Help Center(support.claude.com、直近更新)によれば、Skills も Custom Connector も **Free を含む全プラン**で利用可(Free は Custom Connector 1 個までの制限で、本 Framework は 1 個で足りる)。ただし Claude Platform Docs では Custom Skill upload を Pro 以上限定と記載する箇所もあり、資料により差異がある。**最新の公式ドキュメント(support.claude.com)で最終確認する**こと。

**実運用の推奨**:
- **継続運用するなら Pro / Max 以上を推奨**。Free の usage 上限(送受信メッセージ数、Skills / Connector 呼び出し数)だと、Vault 経由の対話がすぐに詰まる可能性が高い
- **Pro**(月額 $20、年払いだと実質 $17/月): 個人 adopter の標準
- **Max**($100 / $200 のプラン): ヘビーユース、複数プロジェクト運用
- **Team / Enterprise**: 組織単位、追加ガバナンス

**手順**:
1. https://claude.ai/settings/billing で現在のプラン確認
2. 継続的に使うなら **Pro 以上を推奨**(Free で始めて、上限に届いたら upgrade でも可)
3. **Settings → Capabilities で「Code execution and file creation」を有効化**(Skills 機能の前提条件、これがないと Skills が動かない)
4. Customize > Skills 側で Skills 機能を確認、Settings > Connectors 側で Custom Connector 追加ができる状態を確認

**注意事項**:
- 「Skills が Settings で見当たらない」→ 真因は **Code execution 未有効**の可能性大。step 3 を再確認
- Free プランで開始する場合、後で Pro に上げる際は同アカウントで billing 変更するだけで、Skills / Connector 設定は引き継がれる

### 1d. Node.js / git / Terminal(★ P1-1 で修正)

**目的**:
- **Node.js**: Vault-MCP のデプロイに `wrangler`(Cloudflare の CLI)が必要、これは Node.js 上で動く
- **git**: GitHub リポジトリの clone / push に使用
- **Terminal**: コマンド実行環境

**手順**:
1. Terminal を開く(Mac は「ターミナル」アプリ、Windows は **PowerShell**(推奨)、Linux は各ディストリの端末)
2. `node --version` と入力 → 18 以上と表示されれば OK
   - 表示されない or 18 未満 → https://nodejs.org から **LTS 版**をインストール
   - インストール後、Terminal を **再起動**して再確認(PATH 反映のため)
3. `npm --version` → 数字が表示されれば OK(Node.js 同梱、通常は自動)
4. `git --version` → 数字が表示されれば OK
   - 表示されない → Mac は Xcode Command Line Tools(`xcode-select --install`)、Windows は https://git-scm.com/download/win 、Linux はパッケージマネージャで
5. **openssl は Phase 3c で使うが、Windows PowerShell に標準搭載されていない**。代替として Node.js の crypto モジュールを使えるので、この時点では確認不要(Phase 3c で対応)

**Terminal に慣れていない adopter への対応**:
- コマンドをコピペする方法から教える(選択→コピー→貼付けの操作を確認)
- 「エラーが出た」ときはエラーメッセージ全文またはスクリーンショットを共有してもらう
- **Windows adopter は PowerShell を推奨**(コマンドプロンプトより機能が豊富、Node.js コマンドとの相性も良い)

**この Phase 1 が完了したら**:「前提は全て揃いました。次に Vault リポジトリを作ります」と宣言して Phase 2 へ。

## Phase 2: Vault リポジトリを作る(所要 20〜40 分)

### 2a. 名前とプライバシー方針を決める

**質問**:「あなたの Vault リポジトリの名前は?」
- 推奨:`Vault` または `<your-name>-vault`(例: `taro-vault`)
- 注意:HashiCorp Vault(別プロダクト)との命名衝突を避けたいなら後者推奨

**質問**:「このリポジトリは Private(あなた専用)にしますか?」
- **強く推奨:Private**(会話履歴、意思決定、日記など個人情報が入るため)
- Public にする場合は「sensitive: true」を付けたファイル(日記など)も world-readable になる旨を adopter に理解させる

**注意事項**:
- リポジトリ名は後で変更可能だが、変更すると Vault-MCP の `GITHUB_REPO` 変数、PAT スコープ、コネクタ URL などに波及影響する。**最初に慎重に選ぶ**
- Private → Public への変更は後で可能だが、逆(Public → Private)も可能

### 2b. リポジトリ作成

**手順**:
1. https://github.com/new を開く
2. Repository name:上で決めた名前
3. Description:「Personal Vault for Claude(自分用ナレッジベース)」等
4. **Private を選択**(2a で Private 選択の場合)
5. **Initialize with README** にチェック
6. Add .gitignore:**None**(初期時点で不要、必要に応じて後日追加)
7. Choose a license:None(personal use)
8. Create repository

**確認**:https://github.com/<username>/<repo-name> にアクセスして README.md が見える

### 2c. vault-templates をコピー(★ P1-2 で大幅修正)

**目的**:Framework が提供する骨格(templates)をあなたの Vault に取り込む。

**重要な前提**:GitHub UI に「サブフォルダだけ Download ZIP」ボタンは存在しない。GitHub Web UI では**フォルダ単位の直接コピー**もできない(Web からのアップロードは 1 ファイルずつ、または dragged in top-level のみ)。したがって、**必ず Terminal 経路で進める**のが現実的。

**手順(Terminal 経路、全プラットフォーム推奨)**:

1. **Framework repository を clone**(あなたのローカルに Framework 全体を落とす):
   ```bash
   cd ~/Documents  # 好きな場所へ移動
   git clone https://github.com/nkhippo/Vault-Framework.git
   ```

2. **あなたの Vault repository を clone**(Private の場合、後述の認証手順が必要):
   ```bash
   git clone https://github.com/<your-username>/<your-vault>.git
   ```
   
   **Private リポジトリの認証**:
   - **推奨**:GitHub CLI をインストールして `gh auth login` → 対話形式で認証
   - **代替 1**:PAT を作って `https://<username>:<PAT>@github.com/<username>/<repo>.git` の形式で clone(ただし PAT が bash history に残るので注意)
   - **代替 2**:SSH 鍵を設定して `git@github.com:<username>/<repo>.git` で clone(https://docs.github.com/en/authentication/connecting-to-github-with-ssh 参照)

3. **vault-templates 配下の全内容をあなたの Vault にコピー**:
   ```bash
   cp -r Vault-Framework/vault-templates/. <your-vault>/
   ```
   
   **注意**:`cp -r .../vault-templates/. <your-vault>/`(末尾の `/.` )で dotfile(`.gitkeep` 等)も含めてコピー。`* ` だと dotfile が漏れる可能性

4. **`.gitkeep` の役割**:vault-templates には、空フォルダを Git に残すための `.gitkeep` ファイルが配置されている場所がある。これらは削除しない(削除すると Git 上でそのフォルダが消える)

5. **コミットして push**:
   ```bash
   cd <your-vault>
   git add .
   git commit -m "chore: initialize from vault-templates"
   git push
   ```

**確認**:あなたの Vault リポジトリに `00_meta/`(vocabulary.md、SETUP.md 等)、他 vault-templates 由来のディレクトリが揃っている

**プレースホルダの置換**:
- vault-templates 由来のファイルには `<your-account>`、`<your-project>` 等のプレースホルダが残っている
- 代表的な要置換ファイル:
  - `00_meta/project_instructions_vault.md`:`<your-name>` 等
  - `00_meta/vocabulary.md`:`project:` セクションの初期プロジェクト名
- **ただし、これらは Phase 7(初期認識合わせセッション)で Claude が対話しながら埋めるので、この時点で手動編集は不要**

### 2c 補足:SETUP.md について

`vault-templates/00_meta/SETUP.md` が新規 Vault にコピーされる。これは「初期セットアップ未完了」を示す **bootstrap-only ファイル**。Phase 7 完了時に削除される。詳細は Phase 7 参照。

## Phase 3: Vault-MCP をデプロイ(所要 30 分〜1 時間)

### 3a. Vault-MCP を fork

**手順**:
1. https://github.com/nkhippo/Vault-MCP を開く
2. 右上「Fork」ボタン → 自分のアカウントに Fork
3. **Fork 先を Private にするかは任意**(Vault-MCP のコード自体は個人情報を含まない、Public で問題なし。ただしあなた固有のカスタマイズを加えるなら Private が安全)
4. Fork 先を ローカルに clone:
   ```bash
   cd ~/Documents  # または好きな場所
   git clone https://github.com/<your-username>/Vault-MCP.git
   cd Vault-MCP  # 以降の 3b/3c は Vault-MCP フォルダ内で実行
   ```

**確認**:`ls` または `dir` で Vault-MCP のファイル一覧が見える

### 3b. GitHub Fine-grained PAT を発行(★ P1-3・P2-6 で修正)

**目的**:Vault-MCP が GitHub Contents API 経由であなたの Vault を読み書きするための認証情報。

**Fine-grained と Classic の違い**:
- **Fine-grained**(推奨):特定リポジトリだけに権限を絞れる、より安全
- **Classic**:古い形式、権限が広い(全リポジトリに影響)。本 Framework では推奨しない

**手順**:
1. https://github.com/settings/tokens?type=beta を開く(Fine-grained の直リンク)
2. 「Generate new token」→「Fine-grained personal access token」
3. **Token name**:`vault-mcp-<vault-repo-name>`(例:`vault-mcp-Vault`)
4. **Expiration**:90 days(推奨、期限が来たら更新 = 下記参照)
5. **Repository access**:「Only select repositories」→ あなたの Vault リポジトリ(2 で作ったもの)を選択
6. **Repository permissions**:
   - **Contents**: Read and write(必須)
   - **Metadata**: Read-only(自動選択)
   - Issues: Read and write(任意、backlog を GitHub Issue に転記したい場合のみ)
7. 「Generate token」→ **トークンをコピー**
8. **一時保管**:
   - **推奨**:パスワード管理アプリ(1Password / Bitwarden 等)に保存
   - **次善**:GitHub のこのタブを **Phase 3c 完了まで開いたまま**にする(タブを閉じるとトークンは再表示不可)
   - **最悪の場合の代替**:メモアプリに一時貼付(ただし iCloud 同期系の Notes は情報漏洩リスクあり)

**注意事項**:
- トークンは他人に見せない、リポジトリにコミットしない
- Fine-grained PAT は発行後も権限を編集できる(必要なら後で Issues 権限などを足せる)

**90 日後の更新手順(必ずやる)**:
1. https://github.com/settings/tokens?type=beta で新しい PAT を発行(同じ設定で)
2. Vault-MCP フォルダで:
   ```bash
   npx wrangler secret put GITHUB_TOKEN
   ```
3. 入力プロンプトで新しい PAT を貼り付け
4. 再デプロイ:`npx wrangler deploy`
5. 古い PAT を https://github.com/settings/tokens?type=beta で削除

**期限切れの症状**:MCP コネクタが 401 Unauthorized を返す、Claude が「認証エラー」と報告

### 3c. Cloudflare Workers にデプロイ(★ P0-2, P0-3, P1-4 で修正)

**手順**:
1. Vault-MCP フォルダで:`npm install`(初回だけ、依存パッケージのダウンロード)

2. Cloudflare にログイン:
   ```bash
   npx wrangler login
   ```
   ブラウザが開いて Cloudflare 認証が求められる。認証完了後、Terminal に戻る

3. GitHub PAT を Cloudflare Secrets に登録:
   ```bash
   npx wrangler secret put GITHUB_TOKEN
   ```
   プロンプトで、3b でコピーした PAT を貼り付け

4. **MCP アクセストークンを生成**(Claude と Vault-MCP の間の認証、"合言葉"):
   - **Mac / Linux**:
     ```bash
     openssl rand -hex 32
     ```
   - **Windows / 全 OS 共通(Node.js があれば可、★ P0-3 対応)**:
     ```bash
     node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
     ```
   
   出力される **64 文字の英数字**(16 進文字列)がトークン。
   
   **★ 重要**:このトークンは **Phase 5b で Claude Connector 設定時に使う**ので、**必ずパスワード管理アプリまたは安全な場所にコピーして保存**。Cloudflare Secrets は書き込み専用で後から読めないため、控え忘れると再生成 → 再登録が必要になる。

5. 生成したトークンを Cloudflare Secrets に登録:
   ```bash
   npx wrangler secret put MCP_ACCESS_TOKEN
   ```
   プロンプトで、step 4 でコピーしたトークンを貼り付け

6. **`wrangler.toml` を編集**:
   - fork した Vault-MCP には既に `wrangler.toml` があり、`name` などの設定が入っている
   - **既存の該当箇所を編集**する(`[vars]` セクションが既にあればそこに書き込む、なければ末尾に追加)
   - `[vars]` を重複追記するとエラーになる、注意
   ```toml
   [vars]
   GITHUB_OWNER = "<your-username>"
   GITHUB_REPO = "<your-vault-repo-name>"
   ```
   - **secret 名(`GITHUB_TOKEN`, `MCP_ACCESS_TOKEN`)は Vault-MCP のコードが読む環境変数名と一致必須**。ズレるとデプロイは成功するが実行時に 401/500 になり、debug が難しい
   - `wrangler.toml` の `name` フィールドが Workers サブドメイン先頭に反映される(例:`name = "vault-mcp"` なら URL は `https://vault-mcp.<subdomain>.workers.dev`)

7. デプロイ:
   ```bash
   npx wrangler deploy
   ```
   
   **もし `secret put` が「worker not found」で失敗する場合**:
   - 順序を変える:`npx wrangler deploy`(初回、warning 出る可能性ありだが worker 作成される) → `wrangler secret put GITHUB_TOKEN` → `wrangler secret put MCP_ACCESS_TOKEN` → `wrangler deploy`(secret 反映のため再デプロイ)

8. 出力に表示された URL(例:`https://vault-mcp.<your-subdomain>.workers.dev`)をメモ

   **★ 重要(P0-2 対応)**:Claude の Connector に登録するのは、この URL に **MCP エンドポイントパス**(参考実装の Vault-MCP では `/sse`)を付けた URL。
   ```
   https://vault-mcp.<your-subdomain>.workers.dev/sse
   ```
   
   **エンドポイントパスの確認方法**:
   - 参考実装(nkhippo/Vault-MCP)では **`/sse`** が使われている
   - Vault-MCP の README で最終確認する
   - 未設定または誤った URL(bare URL、`/mcp` 等)だと Phase 5b の接続テストで失敗する

**確認**:出力に "Published vault-mcp"(または fork 時の worker 名)と表示されればデプロイ成功

**エラー対応(拡張)**:

- **`wrangler login` エラー** → ブラウザで Cloudflare にログイン済みか確認、`npx wrangler logout` してから再 login
- **`wrangler deploy` で 401**:
  - Cloudflare 側の認証:`npx wrangler whoami` で確認
  - GitHub PAT の権限:Fine-grained で該当リポジトリの Contents R/W が付与されているか
  - Secret 名の不一致:`wrangler.toml` の変数名と Vault-MCP のコード内の env 参照名(`env.GITHUB_TOKEN` 等)を一致させる
- **`wrangler deploy` で toml エラー**:`wrangler.toml` の `[vars]` セクション重複、または YAML 構文エラー
- **デプロイした URL を忘れた**:Cloudflare Dashboard → Workers & Pages で該当 worker を選択、URL が表示される
- **詳細 troubleshooting**:https://github.com/nkhippo/Vault-Framework/blob/main/mcp-server-reference/troubleshooting.md

## Phase 4: Claude Skills アップロード(所要 15〜30 分、★ P1-5 で修正)

**目的**:Vault の使い方を Claude に教える Skill を Claude アカウントに登録する。

**前提の再確認**:Phase 1c step 3 で **Code execution and file creation** が有効になっているか。無効だと Skills 機能が動かない。

### 4a. Skill を zip 化

**手順**:
1. Phase 2c で clone した Framework repository がローカルにあるはず(`~/Documents/Vault-Framework/` 等)
2. その中の `skills/vault-manager/` フォルダに移動して確認:
   ```bash
   cd ~/Documents/Vault-Framework/skills/vault-manager/
   ls
   ```
   `SKILL.md` が直接見えれば OK
3. **重要:zip の中身の構造**:
   - Claude Skills は **zip の直下(ルート)に `SKILL.md` があるファイル**を読む
   - Mac の右クリック→「圧縮」で `vault-manager` フォルダを圧縮すると、zip の中身は `vault-manager/SKILL.md`(1 段ネスト)になり、**アップロードで失敗する可能性がある**
   - **正しい zip 作成方法**:
     ```bash
     cd ~/Documents/Vault-Framework/skills/vault-manager/
     zip -r ../vault-manager.zip .
     ```
     (末尾の `.` が重要。フォルダの中身だけを zip 化)
   - または zip 作成後、中身を確認して `vault-manager/` の 1 段ネストになっていたら、その中身を取り出して zip し直す

4. 同様に `vault-maintainer.zip` も作成(**任意、Level 2〜4 メンテナンス用**、必須ではない。日常運用は vault-manager だけで足りる)

### 4b. Claude Skills に登録

**手順**:
1. https://claude.ai を開く
2. **Settings**(左下メニューまたはアバターアイコン)を開く
3. **Customize** → **Skills** を選択
   - **もし Skills メニューが見えない場合**:Settings → Capabilities で「Code execution and file creation」が有効になっているか再確認(Phase 1c step 3)
4. 「Upload a Skill」ボタン(または類似)
5. `vault-manager.zip` をアップロード → 有効化トグルを ON
6. 同様に `vault-maintainer.zip` もアップロード → 有効化(使う場合のみ)

**確認**:Skills 一覧に vault-manager が「有効」で表示される

**アップロード失敗時の対応**:
- **赤いエラーが出る** → 典型的な原因は 2 つ:
  1. **zip 構造ミス**(SKILL.md が root にない)→ 4a step 3 の zip 作成手順を再確認
  2. **SKILL.md の Front Matter 形式ミス**(`name` + `description` + `updated` の Claude Skills 純粋形式であること、余計なフィールドがあると失敗する)

## Phase 5: Claude Projects 設定(所要 15〜30 分、★ P0-2, P1-6 で修正)

### 5a. Project 作成

**手順**:
1. https://claude.ai/projects で「Create Project」
2. Name:`Vault`(または好みの名前)
3. Description:`個人 Vault 運用の中核 Chat`
4. Create

**注意事項**:Free プランでも Projects は作成可能(1c 記載に一致)

### 5b. MCP Connector 追加

**注意**:Claude の Connector 追加 UI は継続的に変わる可能性がある。以下は 2026-07 時点の一般的な流れ。UI が異なる場合、adopter に「Custom Connector」「MCP」「Add Connector」等のキーワードで探してもらう。

**手順**:
1. **アカウント階層で Connector を追加**(現行 UI):
   - claude.ai の Settings → Connectors → Add Connector
   - 「Custom Connector」または「Add remote MCP」を選択
2. 設定内容:
   - **Name**:`Vault MCP`
   - **URL**:Phase 3c step 8 で確認した **`/sse` エンドポイント込みの URL**
     ```
     https://vault-mcp.<your-subdomain>.workers.dev/sse
     ```
     **★ URL の末尾 `/sse` を忘れないこと**(bare URL だと接続失敗)
   - **Authorization**(認証):Bearer token を選択 → Phase 3c step 4 で保存した `MCP_ACCESS_TOKEN`(64 文字の英数字)を貼り付け
     - UI によっては「Bearer」「Custom token」「Authorization header」等の呼称がある
3. 保存 → 接続テスト → 成功を確認
4. **Project 側で有効化**:作成した `Vault` Project を開いて、Settings → Connectors → 「Vault MCP」を有効化

**接続テスト失敗時**:
- URL の末尾 `/sse` を確認(最頻)
- Bearer token に貼り付けたトークンの前後の空白確認
- Cloudflare Workers のログを確認:`npx wrangler tail`(Vault-MCP フォルダで実行)
- Cold start による初回タイムアウト(数秒〜十数秒待って再試行)

### 5c. Project Instructions

**手順**:
1. Project 設定 → Instructions タブ
2. 以下をコピペ(**`<your-name>` を実名 or 好みの呼び方に置換**):

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

**補足**:Project 側 Instructions は「薄いポインタ」、実質的な運用ルールは vault 側の `00_meta/project_instructions_vault.md` にある。この関係を adopter に説明すると理解が深まる。

## Phase 6: 動作確認(所要 15〜30 分)

### 6a. 新規 Chat で MCP 疎通確認

**手順**:
1. Vault Project 内で「New Chat」
2. 送信:「Vault MCP が接続されているか、00_meta/vocabulary.md を読んで確認してください」
3. Claude が `vocabulary.md` の Summary を返してきたら成功

**うまくいかない場合**:
- 「MCP 未接続」 → Phase 5b で Connector 設定を再確認(URL、Bearer token、Project 側での有効化)
- 「vocabulary.md が見つからない」 → 2 つの可能性:
  1. **`/sse` URL 不備**(Phase 5b) → URL 修正
  2. **vault-templates 未コピー**(Phase 2c) → GitHub 上で `<your-vault>/00_meta/vocabulary.md` が存在するか確認、なければ Phase 2c をやり直し
- タイムアウト → Cloudflare Workers の cold start(数秒待って再試行)、または `npx wrangler tail` でランタイムログ確認
- 認証エラー → MCP_ACCESS_TOKEN を確認

### 6b. 書き込みテスト(★ P2-3 で修正)

**手順**:
1. 送信:「テストとして、`10_chat_logs/2026/07/setup-test.md` を作成して、内容は 'Setup test successful' でお願いします」
   
   **★ 重要**:`10_chat_logs`(複数形の "s")が正しいパス。単数形だと別ディレクトリを作ってしまい、正典構造から乖離する
2. Claude が `create_note` を実行 → commit URL を返す
3. GitHub 上でそのファイルが `10_chat_logs/2026/07/setup-test.md` に作成されていることを確認

**エラー対応**:
- `403 Forbidden` → PAT の Contents R/W 権限を確認
- `create_note` が動かない → Skill vault-manager が有効か Skills 画面で確認

**成功したら**:「動作確認 OK です。次に初期認識合わせセッションに入ります」と宣言。

## Phase 7: 初期認識合わせセッション(★ P0-4 で大幅修正)

**目的**:配布された骨格を、adopter 固有の情報(価値観、業務ドメイン、プロジェクト一覧)で埋める。

### Phase 7 の自動発動メカニズム

Framework v1.3.0 以降、Skill `vault-manager` は **Phase 0.0** の挙動として、Vault 内の `00_meta/SETUP.md` の存在を検知する:

- **`00_meta/SETUP.md` が存在する場合**(新規セットアップ時、adopter は SETUP.md 未削除):
  - Skill は通常のケース分岐(case 1〜5)に入らず、**自動的に Phase 7(初期認識合わせセッション)モード**を発動
  - `docs/ja/prompts/initial-alignment.md` を MCP 経由で読み、その手順に従って進行
  - Phase 7 完了時、adopter の明示承認後に `SETUP.md` を削除
- **`00_meta/SETUP.md` が存在しない場合**(セットアップ完了後):
  - 通常のケース分岐(汎用議論、特定プロジェクト、日記 等)へ

### 7a. adopter への案内(★ SETUP.md 検知に伴い簡素化)

新規 Chat を Vault Project で開く。**Chat 冒頭で以下のメッセージを送るよう案内**:

> こんにちは。Vault のセットアップを完了したいです。

または、より明示的に:

> 初期認識合わせセッションを始めましょう。

**Skill が SETUP.md を検知していれば、明示的な指示なしで Phase 7 モードに入る**はず。もし通常応答が返ってきたら(Phase 0.0 が未動作の場合)、以下を明示送信:

> `00_meta/SETUP.md` を読んで、初期認識合わせセッションを開始してください。

### 7b. Phase 7 モードでの進行

以降は、新規 Chat の Claude(adopter の Vault にアクセス可能)が主導。この setup-companion Chat の Claude(あなた)は、adopter に「新規 Chat での対話を進めてください、必要なら結果を教えてください」と促す。

adopter の新規 Chat で以下が対話的に進行:
1. Life Strategy と価値観(`profile.md` 記入)
2. あなたのプロジェクト一覧(`vocabulary.md` の project セクション)
3. 最初のプロジェクトの骨組み(`30_projects/<初期プロジェクト>/`)
4. `SETUP.md` の削除(セッション完了時、adopter 明示承認後)

詳細は `docs/ja/prompts/initial-alignment.md`(Framework repo)を参照。このプロンプトファイルは Framework docs 側にあり、adopter の Vault 内にはコピーされない。**adopter の新規 Chat の Claude が Framework repo URL 経由で取得**するか、あらかじめ adopter が該当ファイルをアップロードしておく。

### 7c. Phase 7 完了時の状態

Phase 7 が正しく完了すると:
- `00_meta/profile.md` に adopter の life strategy と価値観が記入されている
- `00_meta/vocabulary.md` の `project:` セクションに adopter のプロジェクト一覧が入っている
- `30_projects/<初期プロジェクト>/README.md` と `handoff/current-state.md` が作成されている
- **`00_meta/SETUP.md` は削除されている**(以降の Chat では通常モードで動作)
- セッション自体が `10_chat_logs/YYYY/MM/YYYY-MM-DD_initial-alignment.md` に保存されている

## セッション終了処理

### 全 Phase 完了時

1. 完了報告:
   > 導入完了です。あなたの Vault は現在:
   > - GitHub リポジトリ: https://github.com/<username>/<vault-repo>
   > - MCP サーバ: https://vault-mcp.<subdomain>.workers.dev/sse
   > - Claude Skills: vault-manager(必要なら vault-maintainer)有効
   > - Claude Project: Vault
   > - Vault-MCP 認証: 有効
   > - 初期認識合わせ完了(SETUP.md 削除済み)
   > 通常運用に入れる状態です。

2. `10_chat_logs/YYYY/MM/YYYY-MM-DD_ai-guided-setup.md` にこのセッション全体を保存(Claude 側で create_note)

3. 「次に自分の Vault で議論を始めるときは、この Project の新規 Chat から通常通り話しかけてください」と案内

### 中断時のチェックリスト(★ P1-7 で追加)

adopter が「今日はここまで」と言った場合、次回の再開に必要な下記の状態を **明示的にメモとして残す**(adopter 側で管理してもらう):

- [ ] **現在の Phase**(例:「Phase 3c の secret 登録まで完了、`wrangler deploy` の直前で中断」)
- [ ] **Vault リポジトリ名**(例:`taro-vault`)
- [ ] **GitHub PAT**:発行済みかどうか、パスワード管理アプリに保存済みかどうか
- [ ] **MCP_ACCESS_TOKEN**:発行済みかどうか、控え済みかどうか
- [ ] **Cloudflare Workers URL**:確定していれば `/sse` 付きの完全な URL
- [ ] **未完了のセットアップ項目**
- [ ] **エラーで詰まっている場合**、そのエラーメッセージ

adopter は次回セッション開始時、このメモを Claude に共有すれば continuation 可能。

## Skill 再アップロード(Framework 更新後の必要作業、★ 新規追加)

Framework がアップデート(例:v1.0.0 → v1.1.0)されると、Skill 側にも新機能や修正が入る場合がある。ただし **Claude Skills にアップロードした Skill は自動更新されない**ため、adopter は手動で再アップロードする必要がある。

### 再アップロードのタイミング

- Framework のリリースノート(CHANGELOG.md)に **Skill 変更**の記載がある版
- 自分の Vault で Skill 期待通り動作しない、または新機能が反応しない場合

### 手順

1. Framework repository を最新化:
   ```bash
   cd ~/Documents/Vault-Framework
   git pull
   ```
2. Phase 4a と同じ手順で新しい `vault-manager.zip` を作成
3. Claude Skills 画面で古い `vault-manager` を **削除**
4. 新しい zip をアップロード → 有効化
5. Vault Project の新規 Chat で疎通確認

### 詳細

Framework の update 手順全体は `docs/ja/setup/08-update.md` を参照。

## エラー時の対応原則

- 「エラーが出ました」だけでは動けない → 具体的なエラーメッセージ(スクリーンショットまたはコピペ)を求める
- adopter の Terminal / Browser で実行したコマンドと結果を教えてもらう
- Cloudflare / GitHub 側の設定ミスが多いので、まずそこを疑う
- 解決しない場合は https://github.com/nkhippo/Vault-Framework/blob/main/docs/ja/setup/troubleshooting.md と https://github.com/nkhippo/Vault-Framework/blob/main/mcp-server-reference/troubleshooting.md を参照するよう案内

## Framework 全体資料への案内

adopter が deep-dive したい場合は以下を紹介:

- **思想**:https://github.com/nkhippo/Vault-Framework/blob/main/docs/ja/philosophy.md
- **アーキテクチャ**:https://github.com/nkhippo/Vault-Framework/blob/main/docs/ja/architecture.md
- **canonical/personal 境界**:https://github.com/nkhippo/Vault-Framework/blob/main/docs/ja/setup/canonical-vs-personal.md
- **update 手順**(将来使う):https://github.com/nkhippo/Vault-Framework/blob/main/docs/ja/setup/08-update.md
- **user-guide**(日常運用):https://github.com/nkhippo/Vault-Framework/blob/main/docs/ja/user-guide.md
- **MCP tools reference**:https://github.com/nkhippo/Vault-Framework/blob/main/mcp-server-reference/tools/reference.md

これらは adopter の Vault にもコピーされているので、Vault-MCP 経由でも参照可能(2c で vault-templates 全体をコピーしている場合)。

## Framework との整合維持

本ファイルは Framework のバージョンと連動する。Framework がバージョンアップしたら、本ファイルの内容も追随する必要がある。整合が取れているかは以下で確認:

- 本ファイルの Front Matter の `framework_version` フィールド
- Framework の `VERSION` ファイル

不整合を検知したら、adopter に「本 companion は Framework vX.Y.Z 想定です。Framework が更新されている可能性があるので、公式手順を確認してください」と伝える。

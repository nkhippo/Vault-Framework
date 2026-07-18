---
audience: adopter
framework_version: 1.4.0
keywords:
  - user-guide
  - operations
  - handoff
  - backlog
  - maintenance
  - framework
status: draft
summary: Vault-Framework を導入した adopter の日常運用ガイド。導入背景と解決アプローチ、基本操作、Chat 引き継ぎ（再会テンプレ含む）、task/issue 抽出、プロジェクト管理、メンテナンス、profile、Framework 更新、高度な使い方、トラブルをカバー。
tags:
  - framework
  - user-guide
  - operations
  - handoff
title: Vault-Framework User Guide
type: knowledge
created: 2026-07-18T18:01:44+09:00
updated: 2026-07-18T18:10:00+09:00
---

## このガイドは何か

Vault-Framework を導入した adopter が、日常運用で「何ができるのか / どうやるのか / なぜそうなっているのか」を理解するためのユーザーガイド。setup-companion(初回導入)と initial-alignment(初期認識合わせ)の次に位置し、通常運用に入った後の参照ドキュメント。

---

## 導入背景 — 何を解決するために生まれたか

### 従来のアプローチの限界

Claude との対話は、意思決定・学び・気づきを生む貴重なプロセス。しかし従来のフローには構造的な限界があった。

1. **Chat は「その場限り」で消える**
   - 過去の議論を参照したいとき、Chat 履歴を目視で探すしかない
   - Claude 側はセッションを跨いで過去の対話を体系的に参照できない
   - 「先週の議論の続き」がスムーズに開始できない

2. **ナレッジベースが SaaS に分散する**
   - Notion / Obsidian / Google Drive / GitHub Wiki / Roam Research 等、目的別に管理場所が散る
   - 検索も統合されず、結局「どこに書いたっけ」問題が発生
   - 各 SaaS の障害・仕様変更・サービス終了リスクを個別に負う

3. **Claude Projects Knowledge の限界**
   - Projects Knowledge にアップロードしたファイルは Claude が参照可能だが、容量制限がある
   - 更新は手動アップロード
   - 「対話の途中で気づいたこと」を即座に永続化する仕組みがない

4. **Task / Issue の管理が別ツールに逃げる**
   - Claude が「これは backlog に入れた方が」と気づいても、Jira / Linear / GitHub Issues に adopter が手動転記
   - Claude と Task tracker の状態が乖離する

これらは個別ツールで部分的に解決できるが、「Claude との対話を資産化する」を全体最適で解いていない。

### この Framework が目指すもの

**「Claude との対話が、あなたの GitHub 上に構造化された知識として自動的に蓄積される」状態を、外部 SaaS 依存なしで実現する。**

具体的には:
- Chat の内容が Front Matter 付き Markdown として GitHub に保存される
- 別 Chat から過去の議論を Claude が自動参照する
- Task / Issue を Claude と共同で明示管理する(GitHub Issue にも起票可能)
- プロジェクト単位で議論を分離、横断参照も可能
- 全て「あなたの GitHub リポジトリ」の中で完結する

---

## Vault-Framework がどう解決するか

### 3 層アーキテクチャ

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Claude     │◄──►│  Vault-MCP       │◄──►│  GitHub Vault   │
│  + Skills   │    │  (Cloudflare)    │    │  (Markdown repo)│
└─────────────┘    └──────────────────┘    └─────────────────┘
```

各層の役割:

- **Claude Skills**(Claude 側):Vault の使い方の**振る舞い規約**を Claude に埋め込む。「これは chat_log として保存」「これは backlog」等の判断ロジック
- **Vault-MCP**(Cloudflare Workers):Claude と GitHub 間の**API 橋**。GitHub Contents API 経由でファイル操作
- **GitHub Vault**(あなたのリポジトリ):**正典**。全ての知識はここに Markdown として保存される

この分離により:
- Claude はどのモデル・バージョンでも同じ Skill で動作(Claude 側の変化に強い)
- Vault-MCP は独立プロダクトとして進化可能(fork してカスタマイズも容易)
- GitHub 保存でデータの永続性と可搬性を確保(いつでも別ツールへ移行可能)

### なぜ GitHub なのか

- **無料**(パブリック/プライベート問わず)
- **バージョン管理**が標準装備(全ての変更が git 履歴として残る)
- **API が枯れており堅牢**(GitHub Contents API は数年安定)
- **Obsidian 等のローカルツールと 1:1 で同期可能**(手元編集と AI 編集の両立)
- **SaaS 依存の反対**:GitHub アカウントさえあれば、Anthropic / Cloudflare / Framework 提供者に何かあっても Vault は残る

### なぜ Cloudflare Workers なのか

- **無料枠 100k req/day**(個人利用ではまず超えない)
- **エッジ配信で低レイテンシ**
- **stateless、シンプルなデプロイモデル**
- **wrangler CLI での GitOps 的運用**

### なぜ Front Matter 付き Markdown なのか

- **人間が読める**(Obsidian 等で直接編集・閲覧)
- **構造化**(YAML frontmatter で分類・検索・タグ付け)
- **汎用**(将来 Framework 外に移行しても中身がロックインされない)
- **AI が読み書きしやすい**(自然言語 + 構造化メタデータの両方を持つ)

---

## 前提と推奨

### Claude モデルの選び方

Vault-Framework は Skill・MCP・Instructions を組み合わせた**多層的な指示**を Claude が正しく処理する必要がある。モデルの capability が結果の質を大きく左右する。

- **最低**: Claude Sonnet 5 相当以上
- **推奨**: Claude Opus 4.6 以上(4.7 / 4.8 / Fable 5 も含む)
- **特に重要**: 初期認識合わせセッション、Vault メンテナンス、複数プロジェクト横断議論、Framework アップグレード対応 等 → 最新の Opus / Fable を推奨

低スペックモデル(Haiku 系列)は、単純な chat_log 保存等は動くが、あいまい名解決・多層参照・ガードレール遵守で精度が落ちやすい。**「Vault が思うように動かない」ときは、まずモデルを上位に切り替えるのが最短の対処**。

### プラン

- **Claude Pro / Team / Enterprise** 必須(Skills + Connectors 機能のため)
- **Free プラン**では動かない
- **Cloudflare Workers 無料枠**内で運用可能(個人利用の通常想定範囲では)

---

## 基本操作

### Vault に保存する

**コマンド例**:
- 「これを Vault に保存して」
- 「今の議論を chat_log に残して」
- 「意思決定として Vault に記録して」

**Claude の挙動**:
1. 現行 Chat の話題を分類(chat_log / design-decisions / knowledge / etc.)
2. どのプロジェクトの話かを特定(vocabulary 参照)
3. Front Matter を組み立て(type, tags, summary, etc.)
4. 保存パスを決定し、`create_note` で保存
5. commit URL を報告

**保存先の目安**:
- 汎用議論・特定プロジェクト無し → `10_chat_log/YYYY/MM/YYYY-MM-DD_topic.md`
- 特定プロジェクトの議論 → `30_projects/<RepoName>/logs/YYYY/MM/YYYY-MM-DD_topic.md`
- 意思決定 → `30_projects/<RepoName>/design-decisions.md` に追記
- 未解決論点 → `30_projects/<RepoName>/open-questions.md` に追記
- 汎用ナレッジ → `40_knowledge/<category>/topic.md`

### 過去 Chat の検索と参照

**コマンド例**:
- 「先週の X 議論の続きだけど」
- 「あの Y の決定、どういう背景だったっけ?」
- 「以前 Z について何か書いた?」

**Claude の挙動**:
1. `conversation_search` で Claude 内履歴を検索
2. `Vault-MCP:search_by_keyword` で Vault 内 Front Matter を検索
3. 該当ファイルを `get_file_content` / `get_section` で取得
4. 統合して回答

**精度を上げるコツ**:
- プロジェクト名や固有名詞を含める
- 時期の目安を伝える(「先週」「7月頃」等)
- 具体的なキーワードで絞る

### profile の参照(価値判断が伴う場面)

Claude は提案・推奨をする際、`00_meta/profile.md` の価値判断軸を自動的に参照する。adopter が明示的に指示する必要はない。

profile の中身を見直したいときは:
- 「profile を確認して、今の判断と齟齬がないか見て」
- 「profile に <新方針> を追記した方がいいか判断して」

---

## Chat の引き継ぎ(★重要機能)

長時間セッションや長期継続の話題では、Chat を「引き継ぎ」して次のセッションに続ける流れが標準的。

### いつ引き継ぐか

以下のいずれかに該当したら引き継ぎ推奨:
- Chat が長くなり Claude の応答が遅い / 品質が落ちてきた
- 一つのトピックが一段落し、次のセッションで続きを予定している
- コンテキスト window を使い切りそう(残り 20% 以下の目安)
- 一日の作業を締めくくり、翌日に持ち越す

### 引き継ぎコマンド

以下のいずれかを Claude に送る:

- 「引き継ぎ用のファイルを Vault に保存して」
- 「handoff を作って次回に引き継ぎたい」
- 「このセッションを handoff にまとめて」

### Claude の実行内容

1. **handoff ファイルを保存**: `30_projects/<RepoName>/handoff/YYYY-MM-DD_HH-MM_topic.md`
   - type: handoff
   - 現在の状態、直近の意思決定、未解決論点、次にやること を構造化
2. **current-state.md を更新**: 該当プロジェクトの `handoff/current-state.md` に最新状態を反映
3. **再会テンプレを Chat に出力**: 新規 Chat で使うテンプレートをコードブロック形式で提示(下記参照)

### 再会テンプレの構造

Claude は下記の形式でテンプレを出力する:

````
【引き継ぎ】<Project> - <topic>

**参照**:
- Handoff: `30_projects/<RepoName>/handoff/YYYY-MM-DD_HH-MM_topic.md`
- Current state: `30_projects/<RepoName>/handoff/current-state.md`

**要約**: <2-3 行の前回セッション要約>

**次にやること**:
- <item 1>
- <item 2>

**このメッセージと一緒に添付するもの**:
- <file / 画像 / 外部データの一覧、または「特になし」>

**Claude への指示**:
Handoff と current-state を読んで、上記「次にやること」から続きを進めてください。
````

### 添付すべきファイルとは

**「このメッセージと一緒に添付するもの」** の項目には、Claude が MCP 経由で参照できない要素が入る:

- **前回 Chat 内で adopter がアップロードしたファイル**(PDF / 画像 / スクリーンショット / CSV / コード等)
   - MCP は Vault リポジトリのみ参照、Chat 内アップロード物は参照不可
- **外部 URL / スクリーンショット**
   - 例:「Cloudflare Dashboard のこの画面を見て」等のスクショ
- **他リポジトリのコード**(Vault リポジトリ外)
- **Terminal 出力・エラーメッセージ**(前回参照した実行結果)

Claude は前回 Chat のコンテキストから、これらを推定して adopter に案内する。**adopter は Claude が挙げた項目を新規 Chat に添付**すればよい。

Vault 内のファイルは全て MCP 経由で自動参照可能なので、添付不要。

### 新規 Chat での再開手順

1. 同じ Vault Project 内で **新規 Chat** を開始
2. 前回セッションで Claude が出力したテンプレをコピペ
3. 「このメッセージと一緒に添付するもの」に列挙されたファイル(あれば)を添付
4. 送信

これで Claude は handoff / current-state / 添付ファイルの全てを揃えた状態で、続きから議論を再開できる。

---

## Task / Issue の抽出と管理

### 残タスク・残課題の洗い出し

**コマンド例**:
- 「この会話内の残タスクと残課題を保存して」
- 「今議論した中の未完了項目を backlog に起票して」

**Claude の挙動**:
1. 会話全体を走査
2. Task(方針決定済み)と Issue(方針未決)を分類
3. adopter に「これを起票していい?」と一覧提示
4. 承認後、プロジェクト単位で `30_projects/<RepoName>/backlog/YYYY-MM-DD_slug.md` に保存

### backlog の運用

Backlog item は 1 ノード 1 ファイル、Front Matter で状態管理:

- **kind**: `task`(方針決定済み)/ `issue`(方針未決)- 起票時に確定、原則不変
- **state**: `open` / `done` / `abandoned` - 遷移可能
- **assignee**: `owner`(あなた)/ `cursor`(実装 AI)- 必須

### 起票時の指定

- 「この課題を <Project> の backlog に task として起票して」
- 「これは issue として、まず調査から」

### backlog の参照

- 「<Project> の open な backlog 見せて」
- 「stalled(2 週間動きがない)な item ある?」

---

## プロジェクト管理

### プロジェクトとは何か

`30_projects/<RepoName>/` の 1 まとまり。以下を含む:
- `README.md`:プロジェクト概要
- `design-decisions.md`:意思決定ログ
- `open-questions.md`:未解決論点
- `handoff/current-state.md`:最新状態
- `handoff/YYYY-MM-DD_*.md`:個別 handoff
- `logs/YYYY/MM/*.md`:議論ログ
- `backlog/YYYY-MM-DD_*.md`:task / issue

### プロジェクトとして管理する基準

以下のいずれかに該当したらプロジェクト化推奨:
- 今後 **3 回以上議論しそう**な話題
- GitHub リポジトリと 1:1 対応する開発案件
- 数週間〜数ヶ月継続予定の探求
- 独立したドメインを持ち、他の話題と混ざらせたくない

該当しない話題(単発の疑問、一過性の議論、雑談)は通常 chat_log で十分。

### プロジェクトを作らないと起こること

- **Claude の検索性が下がる**:vocabulary に無いプロジェクトは Skill が「特定プロジェクト」として認識できない
- **議論が chat_log に分散**:横断的な参照が困難
- **意思決定・未解決論点の集約先がない**:同じ論点を複数回議論する羽目に

### プロジェクト化の依頼

**明示的な指示が必要**(自動生成しない)。以下のいずれかで:

- 「これをプロジェクトとして 30_projects/ に骨組みを作って」
- 「<X> を新規プロジェクトとして立ち上げて」

**Claude の実行内容**:
1. `00_meta/vocabulary.md` の `project:` セクションに新規追加
2. `30_projects/<Name>/README.md` を作成
3. `30_projects/<Name>/handoff/current-state.md` を作成
4. 空の `backlog/` ディレクトリを作成
5. 必要に応じて `project_instructions.md` を作成

---

## Vault のメンテナンス

### なぜメンテが必要か

会話量が増えると、以下が発生する:
- ファイル数が数百 → 数千に増え、検索性が落ちる
- 関連ファイルの発見が難しくなる
- Front Matter の不整合が積み重なる
- backlog に stalled item が溜まる
- リンク切れが増える

### 状態確認コマンド

- 「Vault の状態を確認して」
- 「Vault ヘルスチェックして」

**Claude の挙動**:
1. `list_recent_commits` で最近の活動量を把握
2. `get_frontmatter_batch` で主要ディレクトリの状態を走査
3. リンク切れ / stalled backlog / 未整理ファイル 等を検出
4. 問題点と対処案を報告

### メンテのレベル別内容

- **Level 1(即時、低コスト)**: リンク切れ検出、handoff アーカイブ
- **Level 2(週次、中コスト)**: backlog stalled 検出、統計、Front Matter 整合
- **Level 3(月次、高コスト)**: chat_log から ADR / spec 候補の抽出
- **Level 4(季節、非常に高コスト)**: アーカイブ、大幅再構成

### 実作業の委譲

Level 2 以上は**トークン消費が大きい**(数百〜数千ファイルを走査するため)。効率のため:

- 「Vault メンテの指示書を作って」→ Claude が Cursor / Claude Code 向けの指示書を出力
- adopter がその指示書を Cursor / Claude Code に渡して実作業
- 結果を Vault Project の Chat で確認

これにより:
- Claude(Pro プラン)側のトークン消費を最小化
- 大量ファイル操作は開発ツールに委譲
- adopter は結果レビューだけに集中

---

## profile と価値観

### profile.md とは

`00_meta/profile.md` は adopter の life strategy と価値観を記入するファイル。Claude が提案・推奨をする際の価値判断軸として自動参照される。

初期認識合わせセッション(Phase 7)で記入し、大きな方針変化があったら随時更新。

### 更新のタイミング

- 独立志向・自己投資方針・キャリア方向 等の**大きな価値観変化**
- Claude が「これを profile に追記した方が」と提案してきたとき(承認後追記)
- 定期見直し(月次〜四半期)

### 参照の実際

Claude は以下の場面で自動的に profile を参照する:
- ケース 1(特定プロジェクト相談)の初回一括読み込み
- ケース 2(執筆相談)の初回一括読み込み
- ケース 3(汎用ナレッジ)で価値判断が必要な場面
- Phase 7 モード(初期認識合わせ)の主対象

---

## Framework 更新

### 新版のチェック

Framework は継続的にアップデートされる。新版チェックは:
- Vault-Framework GitHub の CHANGELOG.md を定期確認
- adopter の Vault 内 `.framework-version` と Framework 側 `VERSION` を比較

### 更新手順

詳細は `docs/ja/setup/08-update.md`。要点:

1. CHANGELOG を読んで変更内容を把握
2. Skill を再アップロード(zip)
3. canonical ファイルを差し替え(FM 二層戦略に注意、`docs/ja/setup/canonical-vs-personal.md` 参照)
4. 破壊的変更(major bump)があれば移行手順に従う
5. update 完了後、再度 Phase 7 相当のセッションを実施(推奨)

### 破壊的変更への対処

major bump(v1.x → v2.0)は破壊的変更あり。CHANGELOG に移行手順が同梱される。単純な差し替えでは済まないので、CHANGELOG を丁寧に読む。

---

## 高度な使い方

### 複数プロジェクト横断の検索

- 「X という論点、複数のプロジェクトで議論があった気がする、探して」
- Claude が `search_by_keyword` を全プロジェクト対象で実行

### note 執筆モード

`20_notes/guides/` に沿った執筆フロー。過去の推敲パターンから文体を学習し、下書き → 推敲 → 公開の流れをサポート。

- 「note 記事を書きたい、テーマは X」→ Phase 執筆モードに入る

### 日記機能

`50_self/` は最もセンシティブな領域。sensitive: true が自動付与され、他コンテキストで引用されない。

- 「今日の日記を保存」→ `50_self/diary/YYYY/MM/YYYY-MM-DD.md`

### backlog を GitHub Issue に起票

- 「この backlog を GitHub Issue にして」
- Claude が `create_issue` で GitHub に転記、backlog item に `github_issue` フィールドを追加

### Cursor / Claude Code 委譲パターン

大規模な実装・メンテ作業は Cursor / Claude Code に委譲:
- 「これを Cursor 用の指示書にして」→ 構造化された Markdown 指示書が出力
- adopter が Cursor / Claude Code に渡して実作業
- 完了報告を Vault Chat で受け取り

---

## トラブル時

### MCP 接続失敗

- 「MCP が接続されていない」と Claude が返してくる
- **対処**: Chat 側の MCP コネクタ接続状態を確認、Cloudflare Workers 側の稼働確認、必要なら Chat 再起動

### Claude が期待通り動かない

- **モデル**を上位に切り替えて再試行(Sonnet 5 → Opus 4.7 等)
- **Skill の有効性**を確認(Claude Skills 画面)
- **Project Instructions** が正しく `00_meta/project_instructions_vault.md` を参照しているか確認
- **プロジェクト特定失敗** の可能性 → 明示的にプロジェクト名を伝える

### 詳細トラブルシューティング

- `docs/ja/setup/troubleshooting.md`:一般的なセットアップ問題
- `mcp-server-reference/troubleshooting.md`:MCP サーバ側の詳細問題

### 状況判断が付かないとき

Chat で Claude に相談:
- 「Vault の何がおかしいか整理して」
- 「MCP エラーの原因を切り分けて」

---

## 関連ドキュメント

- **[Setup Handbook](setup/README.md)**:初回導入手順(Phase 1〜7)
- **[Setup Companion](setup/setup-companion.md)**:AI-guided setup 用 Claude 向け対話ガイド
- **[Initial Alignment Session](setup/07-initial-alignment-session.md)**:Phase 7 の位置づけ
- **[Canonical / Personal 境界](setup/canonical-vs-personal.md)**:同期モデルの正典
- **[Update 手順](setup/08-update.md)**:Framework 更新の取り込み
- **[MCP Tools Reference](../mcp-server-reference/tools/reference.md)**:MCP ツール全 API リファレンス
- **[Philosophy](philosophy.md)**:Framework の思想
- **[Architecture](architecture.md)**:全体構造の詳細

## Framework との整合維持

本ガイドは Framework のバージョンと連動する。Framework がバージョンアップしたら、本ガイドの内容も追随する必要がある。整合が取れているかは以下で確認:

- 本ファイルの Front Matter の `framework_version` フィールド
- Framework の `VERSION` ファイル

不整合を検知したら、CHANGELOG を確認して本ガイドの更新を検討する。

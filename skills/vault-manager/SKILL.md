---
name: vault-manager
description: >-
  Vault(nkhippo/Vault)への保存・参照を管理する Skill。
  Chat の議論記録、note 記事、プロジェクト設計相談、日記等を Front Matter 準拠で保存し、
  過去 chat / 意思決定 / open-questions を参照する。
  ID scheme(pj/nt/kn/mt prefix)準拠、backlog システムの参照(棚卸し等)と保存(起票、昇格、Cursor 委譲、Issue 起票)workflow を含む。
  詳細トリガー phrase と workflow は body 参照。
updated: 2026-07-17 02:30:00+09:00
id: pj-2026-07-13-f844
aliases:
- pj-2026-07-13-f844
---

# Vault Manager (v1.7)

Naoya の個人 Vault リポジトリ(`nkhippo/Vault`)を Cloudflare Workers ベースの MCP コネクタ経由で操作するための Skill。

## この Skill の役割

- vault への保存判断とファイル作成
- vault からの情報取得(参照判断ルールに従う、Phase 3.1 トークン節約ツールを活用)
- あいまいなアプリ名からのプロジェクト特定
- Cursor 委譲すべき作業の判定と指示書作成の提案
- 日記・個人記録の保存と、その参照制御
- GitHub Issue 起票 workflow(Phase 3.2 対応、v1.2 で追加)
- **特定プロジェクト相談時の `project_instructions.md` と `applies_common` 共通ルールの一括読み込み**(v1.3 で追加)
- **新規保存時の id/aliases 自動付与と wikilink ID 参照**(Phase 0.6 / v1.5)
- **Backlog 参照系 workflow**(一覧・棚卸し・単一 item 参照、Phase 1c / v1.6)
- **Backlog 保存系 workflow**(起票・昇格・Cursor 委譲・Issue 起票、Phase 1d / v1.7)

## 前提: MCP コネクタと vault の関係

- MCP コネクタ表示名: `Vault MCP`(Claude Pro Connectors 経由)
- MCP サーバリポジトリ: `nkhippo/Vault-MCP`(Cloudflare Workers デプロイ、URL: `https://vault-mcp.nkhippo.workers.dev`)
- vault リポジトリ: `nkhippo/Vault`
- vault の詳細ルールは vault 内の `00_meta/` に集約されている
- この Skill には核心のみを書き、詳細ルールは必要に応じて MCP 経由で `00_meta/` から取得する

過去記録には旧命名(`Obsidian-Vault`、`Obsidian-Vault-MCP`、`obsidian-vault-manager`)が残る場合があるが、歴史的記録として保持されるものであり、現行の運用対象は上記の新命名で統一される。

## Vault MCP コネクタの利用可能ツール(v1.2、11 ツール)

MCP コネクタで以下 11 ツールが利用可能:

### Phase 1+2(基本 5 ツール、read/write)

- `list_directory(path)` - ディレクトリの中身を一覧
- `get_file_content(path)` - ファイル全文取得
- `create_note(path, frontmatter, body, commit_message?)` - 新規作成
- `update_note(path, mode, content, update_frontmatter?, commit_message?)` - 更新(mode: replace_body / append / prepend / replace_all)
- `delete_note(path, commit_message?)` - 削除

### Phase 3.1(トークン節約系 3 ツール、v1.2 で活用ルール明示)

- `get_frontmatter(path)` - Front Matter のみ取得(本文は返さない、5-10x トークン節約)
- `search_by_keyword(keyword, path_prefix?, limit?)` - FM + path のキーワード検索(本文検索なし、search savings)
- `get_section(path, section_name)` - H2 セクション本文のみ取得(section-level savings)

### Phase 3.2(GitHub Issue 系 3 ツール、v1.2 で発火判定追加)

- `create_issue(owner, repo, title, body, labels?, assignees?)` - Issue 起票(MVP: owner=nkhippo に固定)
- `list_issues(owner, repo, state?, labels?, limit?)` - Issue 一覧(PR 除外)
- `add_issue_comment(owner, repo, issue_number, comment)` - Issue コメント

Phase 3.2 ツールを使う際は、PAT の Issues R/W 権限が必要(未付与時は 403)。

## Vault MCP コネクタ接続失敗時の処理(最優先ルール)

`Vault MCP` コネクタ経由の操作が接続エラーで失敗した場合、以下の手順を厳守する。

1. **一度だけリトライする**(即座に同じ操作を再実行)
2. リトライも失敗した場合、**その処理を中断する**
3. 中断した処理について、以下は絶対に禁止する:
   - Claude の一般知識や訓練データから憶測で補って処理を続けること
   - 前回セッションの記憶やキャッシュから補って処理を続けること
   - vault の想定される内容を推定して処理を続けること
4. Naoya に対して以下を明示する:
   - 「Vault MCP コネクタへの接続に失敗し、処理を中断しました」
   - どの操作が失敗したか(操作名とパス)
   - リトライも失敗したこと
5. Naoya の判断を仰ぐ

この規則は他のあらゆる Skill 動作より優先される。

## 日記・個人記録の扱い(50_self/ 領域)

50_self/ 配下は最もセンシティブな領域として扱う。

### 保存フロー(日記)

以下の発話・意図で diary 保存フローを起動する:

- 「日記に書いて」「日記に残して」
- 「今日の記録」「今日あったこと」
- 「diary」「今日の日記」
- 明示的な日付指定の記録要求(「7 月 13 日の日記」等)

起動時の動作:

1. `00_meta/templates/diary.md` のテンプレを取得(初回のみ)
2. 保存先: `50_self/diary/YYYY/MM/YYYY-MM-DD.md`(JST 日付)
3. Front Matter: `type: diary`、`sensitive: true` 自動付与、`tags: [self, diary]`
4. 任意フィールド(mood, energy, weather)は Naoya が発話で言及した場合のみ埋める
5. 同日ファイルが既にあれば `update_note(mode=append)` で追記(区切りとして時刻の H3 見出しを入れる)
6. 保存後の報告は最小限:「日記を保存しました(`50_self/diary/2026/07/2026-07-13.md`)」
7. 本文の内容を報告に引用しない

### 保存フロー(振り返り、目標)

将来対応。「今週の振り返り」「今月の振り返り」で reflection 保存、「目標」「これからやりたいこと」で goal 保存を予定。現時点では実装しない。

### 参照フロー(厳格)

- **Naoya が明示的に「日記を読み返して」「先週の日記を振り返って」等と指示しない限り、絶対に参照しない**
- 参照しても、内容を他コンテキストで引用・要約しない
- 検索操作(list_directory, get_file_content, search_by_keyword)で偶然一覧に出た場合も、能動的に読まない
- 過去 Chat 検索(conversation_search)の結果に 50_self/ 関連が含まれても、要約や引用の対象にしない
- `sensitive: true` のファイル全般に同じ扱いを適用(diary/reflection/goal 以外でも)

### 発火の否定判定

以下は日記保存フローを起動しない:

- 一般的な「今日どう過ごすか」等の未来計画(→ 通常保存フロー)
- 業務系の「日報」「業務記録」(→ 特に指示なければ chat_log として保存)
- プロジェクトの「振り返り」「retrospective」(→ 該当プロジェクトの logs/ 配下)

判断に迷う場合は Naoya に確認する。

## 参照判断ルール(5 段階、v1.3 で project_instructions.md 対応)

Chat の状況に応じて、vault の参照深度を切り替える。過剰参照を避け、必要な情報だけを取りに行く。

### レベル 0: 参照しない

以下の場合は vault を絶対に参照しない。**明示的なトリガーがない限り、これがデフォルト**。

- 純粋な雑談
- Claude が持つ一般知識で完結する質問
- 実装や仕様の技術的な一般論
- Naoya 自身の個人情報が必要ない Web 検索タスク
- vault に関する話題が出ても、参照要求 or 保存指示がない場合

**「vault の情報が使えるかも」という理由で自主的に読みに行くことは禁止**。トークン消費と精度の両方に悪影響がある。

### レベル 1: 最小参照(明示的トリガー時のみ、初回キャッシュ)

以下の明示的トリガーがあった時のみ:

- 「Vault に保存して」「Obsidian に保存して」等の保存指示
- 保存指示の一部としてテンプレ確認が必要な時
- 日記保存フロー(diary 保存の初回時のみ `templates/diary.md` を読む)
- **note 執筆の相談だと判断できた場合、`20_notes/guides/` の 4 ファイル(README、writing_style、writing_process、writing_examples)を一括取得**(v1.4 で追加、詳細は `00_meta/project_instructions_vault.md` の「ケース 2」参照)

判断に必要なファイル(初回のみ、以降キャッシュ):

- `00_meta/vault_structure.md`
- `00_meta/naming_conventions.md`
- `00_meta/vocabulary.md`
- 該当 type の template

**v1.2 の最適化**:

- 「このファイルの概要を確認したい」時は `get_file_content` の前に `get_frontmatter` を試す(5-10x トークン節約)
- 特定セクションのみが必要な時は `get_section` を使用(例: vocabulary.md の type セクションのみ取得)

同一 Chat 内で一度読んだファイルは再度読まない。

### レベル 2: プロジェクト情報を読む(v1.3 で project_instructions.md 対応)

以下の場合は該当プロジェクトのディレクトリから主要ファイルを読む。

- ユーザーが特定プロジェクト名(正式名または通称)を明示した時
- ユーザーが機能表現でアプリを指した時(あいまい名解決フローを経由)

**v1.3 の推奨フロー(project_instructions.md 対応)**:

1. **先に `get_frontmatter` で以下ファイルの Front Matter を一括確認**(4-5 ファイル):
   - `30_projects/<RepoName>/README.md`
   - `30_projects/<RepoName>/design-decisions.md`(存在すれば)
   - `30_projects/<RepoName>/open-questions.md`(存在すれば)
   - `30_projects/<RepoName>/handoff/current-state.md`(直近状態、優先度高)
   - **`30_projects/<RepoName>/project_instructions.md`(存在すれば必読、v1.3 で追加)**
2. **`project_instructions.md` が存在する場合、その Front Matter に `applies_common: [<name>, ...]` があれば、対応する `00_meta/operations/<name>.md` も一括取得**(v1.3 で追加、初回のみ、以降キャッシュ)
3. **summary フィールドから内容を判断**、必要なファイルのみ `get_file_content` で本文取得
4. **特定のセクションだけで足りる場合**は `get_section(path, section_name)` を使用

Vault システム自体(`Vault` / `Vault-MCP` / `Vault-Framework`)に関する相談の場合は、加えて `30_projects/<RepoName>/handoff/current-state.md` を優先的に読む(直近状態の把握が最重要のため)。

**キャッシュルール(v1.2 の会話中再読み込み禁止に準拠、v1.3 で明示)**:

- `project_instructions.md` と `applies_common` で指定された共通ルール(`00_meta/operations/<name>.md`)は、Level 2 の初回一括取得に含める
- 一度読んだら **Chat 内で絶対に再読み込みしない**(Anthropic prompt caching への配慮セクション参照)
- 同一 Chat 内で複数回 Vault 操作が行われても、これらファイルの再取得は行わない
- Naoya が「更新した」と明示した場合のみ再取得を検討

**特定プロジェクト相談時の総則の適用(v1.3 で明示)**:

Level 2 が発火し、特定プロジェクトの相談中と判断された場合、`00_meta/project_instructions_vault.md` の「特定プロジェクト相談時の総則」セクション(作業混ざり防止、話し方、憶測禁止)を Chat 全体を通じて適用する。特に:

- 他プロジェクトの `30_projects/<他RepoName>/` を能動的に読まない
- 他プロジェクト向けの GitHub MCP コネクタを使わない
- `conversation_search` で他プロジェクトのログがヒットしても要約・引用の対象にしない

### レベル 3: 過去記録を検索(v1.2 で search_by_keyword 活用)

以下の場合は過去の議論や決定を検索する。

- ユーザーが過去の意思決定を参照したい意図を示した時
- 例:「あの時決めたこと」「以前議論した」「過去の設計判断」
- **50_self/ 領域は明示的に「日記を読み返して」等と指示された時のみ発動**

**v1.2 の推奨フロー**:

1. **キーワードで絞る**: `search_by_keyword(keyword=<topic>, path_prefix='10_chat_logs/', limit=10)` で該当ファイルを特定
2. **Front Matter 確認**: ヒットしたファイルの `get_frontmatter` で内容を判断
3. **詳細必要なら**: `get_file_content` または `get_section` で本文取得
4. **並行して過去 Chat 検索**: `conversation_search`(過去 Chat を検索、50_self/ 関連の Chat も除外対象)

特定プロジェクト相談中は、他プロジェクトの過去記録が検索結果に混入しても引用・要約しない(v1.3 で明示、作業混ざり防止)。

### レベル 4: 全文精読

ユーザーがファイルパスを明示的に指定した時のみ。`get_file_content` で完全取得。

### メタ指示への応答

| ユーザーの指示 | 調整内容 |
|---|---|
| 「vault を参照せず答えて」 | この Chat 内では以降レベル 0 に固定 |
| 「vault は必要なときだけ」 | デフォルト(状況判断)に戻す |
| 「vault の情報を優先して」 | 一般知識より vault 情報を優先 |
| 「関連する過去記録を全部読んで」 | レベル 3 を積極発動 |
| 「あの handoff だけ読んで」 | レベル 2 で handoff/current-state.md のみ読む |

## Anthropic prompt caching への配慮

Anthropic API は、前ターンと同じプレフィックスの context に対して 90% 割引の cache 適用がある。Skill はこれを最大化するために以下を守る。

### 固定順序でのファイル読み込み

初回セッションで複数の 00_meta ファイルを読む必要がある場合、常に以下の固定順序で読む。順序を毎回変えると cache miss を招く。

1. `00_meta/vault_structure.md`
2. `00_meta/naming_conventions.md`
3. `00_meta/vocabulary.md`
4. `00_meta/frontmatter_schema.md`(必要時のみ)
5. `00_meta/project_aliases.md`(あいまい名解決時のみ)
6. `00_meta/templates/<type>.md`(保存時のみ)
7. `00_meta/operations/<name>.md`(v1.3 で追加、applies_common で指定された共通ルール)
8. プロジェクト固有ファイル(`30_projects/<RepoName>/` 配下、v1.3 で `project_instructions.md` を含む)

### 会話の途中での再読み込み禁止

一度読んだファイルは、同一 Chat 内では再度 MCP 経由で取得しない。Claude の context にすでに載っている前提で参照する。ファイル内容が更新された可能性がある場合(Naoya が「更新した」と明示した場合等)のみ再取得する。

v1.3 で追加された `project_instructions.md` と `applies_common` で指定された共通ルールも同様に、初回のみ取得し以降はキャッシュ利用。

### 保存時の順序

保存指示への対応(下記 7 ステップ)は、Step 1→7 の順で固定。判断に迷って前に戻ることはしない(前に戻ると context が肥大化し cache 効率が落ちる)。

### Phase 3.1 ツールとの相性

`get_frontmatter` / `get_section` は取得内容が小さく、cache 効率も高い。ただし呼び出し数が増えると cache miss が発生しやすいため:

- **必要な数だけ呼ぶ**: 4 ファイル全部の Front Matter を取ってから絞る等の並列取得
- **同じ順序で呼ぶ**: 複数の get_frontmatter を呼ぶ場合、常にパスのアルファベット順やプロジェクト順で固定

## あいまいなアプリ名の解決フロー(v1.2 で search_by_keyword 活用)

ユーザーが「発音を鍛えるアプリ」「単語のやつ」等、機能表現でアプリを指した場合:

### 通常フロー(小〜中規模、project_aliases.md が数十プロジェクト以下)

1. MCP で `00_meta/project_aliases.md` を読む(まだキャッシュしていなければ)
2. 機能キーワードから該当候補を 1〜3 個抽出する
3. 候補が 1 個の場合: 「〈RepoName〉の情報を読みますね」と一言添えてレベル 2 参照に進む
4. 候補が 2 個以上の場合: 候補一覧を提示し確認を取ってから参照する
5. project_aliases.md でも候補が見つからない場合: `list_directory` で `30_projects/` を確認し、ヒットしたプロジェクトを候補として提示

### 大規模フロー(v1.2、project_aliases.md が肥大化した場合)

project_aliases.md がプロジェクト数 20+ 等で肥大化した場合:

1. `search_by_keyword(keyword=<ユーザーの発話>, path_prefix='00_meta/project_aliases', limit=10)` で候補を絞る
2. ヒットしたセクションのみ `get_section(path='00_meta/project_aliases.md', section_name=<プロジェクト名>)` で取得
3. 上記通常フローの Step 3 以降に合流

## 保存指示への対応

### Step 1: 判断

以下のフローに従い保存先を決定する。3 秒以内に判断できなければ `90_inbox/` を選ぶ。

```
日記・振り返り・目標の意図か?
  Yes → 50_self/diary/ or reflections/ or goals/
  No → 以下の分岐へ

Chat の生ログ性が強い(検討・議論の記録)
  → 10_chat_logs/YYYY/MM/

note にする予定・執筆中 → 20_notes/wip/
note を公開した清書版 → 20_notes/published/

新規アイデア(まだリポジトリ化しない)
  → 30_projects/_ideas/incubating/<slug>/ or active/<slug>/

特定リポジトリの設計・意思決定
  → 30_projects/<RepoName>/logs/YYYY/MM/
  例外: 意思決定確定 → design-decisions.md に追記
  例外: 新規未解決論点 → open-questions.md に追記
  例外: ロードマップ更新 → roadmap.md
  例外: 直近状態のスナップショット更新 → handoff/current-state.md

汎用ナレッジ(記事・書籍からの学び等) → 40_knowledge/<category>/

判断に迷う → 90_inbox/
```

### Step 2: ユーザーに保存先を尋ねない

「どこに保存しますか?」とは聞かない。Claude が判断して保存し、結果を報告する。

### Step 3: ファイル名

- 通常: `YYYY-MM-DD_kebab-case-slug.md`
- 日記: `YYYY-MM-DD.md`(スラグなし、日付のみ)
- 日付は現在の JST 日付
- スラグは 30 字以内、会話の主題を表す英語の名詞句

### Step 4: Front Matter の組み立て

`00_meta/templates/` の該当 type テンプレをベースに埋める。

**必須フィールド**

- `id`: `<prefix>-YYYY-MM-DD-<4hex>`(JST 日付、prefix は保存先 path から infer。詳細は下記「ID scheme」)
- `aliases`: `[<id>]`(`aliases[0] == id` を必ず保持)
- `title`: 日本語で会話の主題(日記は `YYYY-MM-DD`)
- `created`, `updated`: 現在時刻(ISO8601、JST)
- `type`: 保存先に応じた type
- `status`: 保存先と内容に応じた status

**diary/reflection/goal の追加処理**

- `sensitive: true` を自動付与
- `tags` に `[self, diary]` 等の該当タグを最低限含める
- `mood` / `energy` / `weather` はユーザーが言及した場合のみ

**type 別の追加必須フィールドは vocabulary.md と各テンプレ参照**

**FM 内の他 note 参照**(構造的参照を書く場合)

- 単一: `<意味>_id: <target-id>`(例: `derived_from_id`, `parent_id`)
- 複数: `<意味>_ids: [<target-id>, ...]`(例: `related_ids`)
- Legacy path フィールド(`related: path.md` 等)は**新規作成時に書かない**

### Step 5: 本文の組み立て

- Front Matter 直後に必ず H2 `## Summary` セクションを置く(diary は例外的に不要、テンプレ通り)
- テンプレートの構造を踏襲
- 日記の場合、Naoya の発話をそのまま構造化して記入。要約しない
- 他 note への参照は `[[<id>|<display text>]]` 形式のみ。Path 形式の markdown リンクと basename wikilink(`[[filename]]`)は使わない(参照先 id は `search_by_keyword` / `get_frontmatter` で取得)

### Step 6: MCP で保存

`Vault MCP` の `create_note` ツールを呼ぶ。同名ファイル既存時はエラーが返るので、以下で対応:

- 通常保存: ユーザーに確認する
- 日記の場合: 自動的に `update_note(mode=append)` に切り替えて追記(区切りとして時刻の H3 見出しを入れる)

### Step 7: 保存後の報告

通常:
```
保存しました。
- パス: <フルパス>
- id: <id>
- タイプ: <type>
- 概要: <summary の内容>
```

日記の場合(最小限、内容は引用しない):
```
日記を保存しました(<パス>, id: <id>)。
```

## ID scheme(Phase 0.6 以降)

すべての新規保存で以下を必須とする。詳細ルールは Vault-Framework `docs/id-scheme.md` を参照(本 Skill は要点のみ)。

### FM 生成時の必須項目

- `id: <prefix>-YYYY-MM-DD-<4hex>`
- `aliases: [<id>]`(`aliases[0] == id`)
- `YYYY-MM-DD` は JST 現在日付

### Prefix inference(要点のみ)

| Path 先頭 | Prefix |
|---|---|
| `30_projects/`、`_ideas/`、`_life/` | `pj-` |
| `20_notes/` | `nt-` |
| `40_knowledge/`、`10_chat_logs/` | `kn-` |
| `00_meta/`、`50_self/` | `mt-` |

判断困難時は Naoya に確認し、`mt-` を fallback として提案する。

### 4hex 生成と collision 回避

1. Claude が `0-9` / `a-f` から pseudo-random に 4 文字(lowercase hex)を生成
2. 候補 id で `search_by_keyword(keyword: "<candidate-id>")` を呼び衝突チェック
3. Hit があれば別の 4hex を再生成(最大 3 回)
4. 3 回とも衝突したら Naoya にエラー報告(実質ほぼ発生しない)

### Body 内参照

他 note を body から参照する時は `[[<id>|<display text>]]` 形式。
Path 形式の markdown リンクは使用しない。Basename 記法(`[[filename]]`)も避ける。

### FM 内参照

他 note を FM から参照する時は `<意味>_id` / `<意味>_ids` サフィックス:

- 単一: `derived_from_id: pj-...`、`parent_id: mt-...`
- 配列: `related_ids: [pj-..., nt-...]`

Legacy path フィールド(`related: xxx.md`)は新規作成時に使わない。

## Backlog 系参照 workflow(Phase 1c 以降)

詳細規約は Vault-Framework `docs/ja/backlog/reference-workflow.md` を参照。要点のみ記載。

### Level 1 追加読み込み

Backlog 系操作(下記トリガー phrase)の初回検知時、以下を Level 1 で読み込み Chat 内キャッシュ:

- Vault `00_meta/backlog_tags.md`

### トリガー phrase

- 一覧提示: 「今仕掛かりは?」「今のタスクは?」「〜の残ってるタスクは?」等
- 棚卸し: 「棚卸しして」「進捗確認」「Issue 状態確認」等
- 単一参照: 「〜の詳細見せて」「〜の状態は?」等

### 一覧提示 flow

1. 対象プロジェクト特定(全体 / 特定 repo / `_life/` / `_ideas/*/incubating/*/`)
2. `search_by_keyword` で backlog item 列挙
3. `get_frontmatter` で kind/state/assignee/cursor_instruction_id/github_issue/updated 取得
4. `state: open` のみ表形式提示、stalled 警告付き

### 棚卸し flow

1. 一覧提示 flow を実行
2. `github_issue` を持つ item について、対象プロジェクトの GitHub コネクタで Issue state 取得
3. 状態乖離検出:
   - Issue closed & merged & Vault open → Vault `done` 更新提案
   - Issue closed & not merged & Vault open → Naoya 確認
   - `updated` 2 週間以上 → `stalled` tag 提案
4. Naoya 承認 → `update_note` で Front Matter 更新 + H2 History 追記

### 単一 item 参照 flow

1. Backlog item を特定(title/id/path)
2. `get_file_content` で全体取得
3. FM 概要 + Summary + Context + History(最新 3-5)を提示
4. Naoya 要求で `derived_from_id`, `related_ids`, `cursor_instruction_id`, `github_issue` を辿る

### 作業混ざり防止規約遵守

- 対象プロジェクト外の GitHub コネクタは能動使用しない
- 全体棚卸しは Naoya の明示指示があった時のみ許容、コネクタ切り替えを透明に伝える
- 50_self/ は明示指示なく参照しない

### Naoya 承認 gate(必須)

Backlog item の state/tag/FM 変更は **必ず** Naoya 承認を経る。無断更新禁止(既存 Skill 原則の継続)。

## Backlog 系保存 workflow(Phase 1d 以降)

詳細規約は Vault-Framework `docs/ja/backlog/save-workflow.md` を参照。要点のみ記載。

### Level 1 追加読み込み

保存系操作の初回検知時、以下を Level 1 で読み込み Chat 内キャッシュ:

- Vault `00_meta/backlog_tags.md`(Phase 1c で既読なら再読不要)
- Vault `00_meta/templates/backlog_item.md`
- Vault `00_meta/frontmatter_schema/backlog_item.md`

### トリガー phrase

- 起票系: 「これタスクとして起票して」「これ課題として残して」「これ backlog に入れて」等
- 昇格系: 「これタスク化して」+ open-questions を指す文脈
- 委譲系: 「これ Cursor 委譲して」「Issue 起票して」
- 保留系: 「後で考えましょう」「後で検討」

### 起票 flow(共通)

1. 対象プロジェクト特定(Chat context または Naoya 確認)
2. **起票案を Naoya に提示**(kind/title/summary/tags/path/assignee、まだ create_note しない)
3. **Naoya 承認 gate**: 承認 → 次へ、修正指示 → 案再提示、却下 → 中止
4. id 生成(prefix + date + 4hex)+ collision check
5. Front Matter 構築(必須項目 + optional derived_from_id/related_ids)
6. Body 構築(Summary/Context/Definition of Done or Open questions/History)
7. `create_note` で書き込み
8. Naoya に完了報告(id、path、kind、state、assignee)

### open-questions 昇格 flow(追加ステップ)

- 起票 flow の Step 2 で `derived_from_id` に open-questions ファイル id を含める
- 昇格後、Naoya に「open-questions の該当行を削除 / wikilink 置換 / 保持のどれ?」と選択させ、`update_note` で反映
- Body History に「open-questions.md 行 "X" から昇格」を記録

### Cursor 委譲 flow

前提: task 化済み、target repo 確定。

1. Naoya に指示書の下書き案を提示
2. 承認 → 指示書作成(Vault 内 or 作業ディレクトリ、Skill 既存の Cursor 委譲規約に従う)
3. Backlog item 更新: `cursor_instruction_id` 追加、`assignee: cursor`、History 追記

### GitHub Issue 起票 flow

前提: 対象プロジェクトの GitHub MCP コネクタ接続済み、作業混ざり防止規約遵守。

1. Naoya に対象 repo と Issue 内容案を提示
2. 承認 → 対応 GitHub コネクタで Issue 作成
3. Backlog item 更新: `github_issue: <owner/repo>#<N>` 追加、History 追記
4. コネクタ未接続時: Naoya に接続を依頼、または手動起票を提案

### 保留 flow

「後で考えましょう」等の発話を検知した時:

- 2 択を提示: A) open-questions.md 追記(思いつきレベル)、B) backlog に issue 起票(状態管理対象)
- デフォルト提案は A、B は明示的意思表示があった時のみ

### 作業混ざり防止規約遵守

- 起票する repo は Naoya 明示指示 または Chat context から特定
- 対象プロジェクト以外の GitHub コネクタ能動使用禁止
- 50_self/ には backlog 起票しない(sensitive)

### Naoya 承認 gate(必須)

以下は全て明示承認必須:

- 新規起票、open-questions 削除・置換、Cursor 指示書作成、GitHub Issue 起票、backlog item の FM 変更

無断更新禁止。

### 重複起票の回避

新規起票要求時、Claude は既存 backlog item がないか `search_by_keyword` で確認、既存があれば「既に起票済みです」と報告して重複回避。

## GitHub Issue 起票フロー(v1.2、Phase 3.2 対応)

Vault-Framework での議論から対象アプリのリポジトリに向けた作業依頼を Issue として起票する workflow。

### 発火判定

以下の発話・意図で Issue 起票フローを起動:

- 「〈対象アプリ〉に Issue を起票して」
- 「この議論を Issue として〈対象アプリ〉に持っていって」
- 「〈対象アプリ〉の GitHub に課題を起票」
- Framework での議論の結果、対象アプリの実装変更が必要と判断された時

### 起票フロー(v1.3 で project_instructions.md 対応)

1. **対象リポジトリを特定**: あいまい名解決フローで `<owner>/<repo>` を確定
2. **プロジェクト固有ルールを確認**: 対象プロジェクトの `project_instructions.md` と `applies_common` で指定された共通ルール(例: `00_meta/operations/dev_project_common.md`)がキャッシュにあれば、その Issue 起票フォーマットに従う(v1.3 で追加)
3. **Issue タイトルを生成**: 議論の主題を英語または日本語で表現(30-80 字)
4. **Issue 本文を生成**:
   - `project_instructions.md` + 共通ルールが指定するフォーマットに従う(例: 開発運用型なら 5 サブセクション背景 + Category A チェック + 作業の進め方セクション)
   - 未指定の場合の汎用テンプレ: Context / 現状 / 期待 / Related
5. **labels を提案**: プロジェクト固有のラベル定義があれば従う、なければ `enhancement`, `bug`, `documentation` 等の汎用ラベル
6. **Naoya に確認**: タイトル・本文・labels を提示、承認を得る
7. **`create_issue` を呼ぶ**: 承認後に MCP 経由で Issue 起票。使用する GitHub MCP コネクタは **プロジェクトが指定するもののみ**(作業混ざり防止、他プロジェクトのコネクタは絶対に呼ばない)
8. **報告**: Issue URL を Naoya に伝える

### MVP 制約

- **owner=nkhippo に固定**: MCP サーバ側で他 owner は 403 で拒否
- **PAT に Issues R/W が必要**: 未付与時は 403、Naoya に PAT 更新を促す

### Issue コメント追加

- Framework での議論の続きを既存 Issue にコメントとして追加する場合、`add_issue_comment` を使用
- コメントも Naoya の承認を得てから投稿

## セッション内の重複保存の防止

同じセッション内で既に保存した内容を再保存しない。追加情報がある場合は `update_note` で追記または更新する。

## Cursor 委譲すべき作業の判定

以下の作業は Claude が直接行わず、Cursor 用の指示書を作成する提案をする。

- 3 ファイル以上の一括作成・更新
- ディレクトリ再編、リネーム
- アイデア → プロジェクト昇格
- Front Matter の一括更新
- wikilink の書き換えを伴う操作
- `delete_note` を伴う操作(単発でもユーザー確認を推奨)
- 保守運用レベル 2 以上(週次補正、月次補正、季節補正)

判定時は Naoya に以下を提案:

```
この作業は複数ファイルの整合性が必要なため、Cursor 経由での実施を推奨します。
指示書を作成しますか?
```

### v1.2 で追加: Issue 起票を伴う Cursor 委譲

対象アプリの複数ファイル修正 + Issue 起票を組み合わせる場合、Cursor 指示書に Issue 起票のワークフローも含める。例:

```
Cursor に以下を依頼します:
1. 対象アプリの複数ファイル修正
2. 修正後、Naoya の承認を得て Issue を close(または追加コメント)
```

## デグレ防止のガードレール

- `create_note` は同名ファイル既存時にエラーを返す前提で扱う。強制上書きしない
- `update_note` の `mode` は明示する(`replace_all` はデフォルトにしない)
- `delete_note` は必ずユーザー確認を取る
- 全操作でコミット SHA を控え、必要時に復元可能な状態を保つ
- センシティブ情報(Naoya の個人的トピック)を含むファイルは Front Matter で `sensitive: true` を必ず設定
- **`sensitive: true` のファイルは、他コンテキストでの引用・要約を絶対に行わない**
- MCP コネクタ接続失敗時は本文書の該当セクションを厳守
- **v1.2 追加**: `create_issue` / `add_issue_comment` は Naoya の承認なしに実行しない(明示的な承認発話を受けてから)
- **v1.3 追加**: 特定プロジェクト相談中は、当該プロジェクトが指定するもの以外の GitHub MCP コネクタを呼ばない(作業混ざり防止)

## 参照するファイルの正典

以下は vault 内の正典であり、Skill の記述が古い場合はこれらを優先する。

- `00_meta/vault_structure.md`
- `00_meta/naming_conventions.md`
- `00_meta/frontmatter_schema.md`
- `00_meta/vocabulary.md`(統制語彙、type 定義)
- `00_meta/claude_operation_rules.md`
- `00_meta/project_aliases.md`
- `00_meta/project_instructions_vault.md`
- `00_meta/operations/<name>.md`(v1.3 追加、開発運用型共通ルール等)
- `50_self/README.md`(50_self 領域の運用方針)
- **`20_notes/guides/README.md`**(v1.4 追加、note 執筆ガイドの全体像と暗黙トリガー運用の要点)
- **`20_notes/guides/writing_process.md`**(v1.4 追加、Vault ミラー保存とガイドライン更新の自動発動運用が定義されている)
- **`20_notes/guides/writing_style.md`**(v1.4 追加、文体・作法)
- **`20_notes/guides/writing_examples.md`**(v1.4 追加、Naoya の指摘ペアの成長する集合)

Skill と vault の記述が矛盾したら、vault を正とみなす。ただし以下 3 点は Skill 側の記述を最優先:

1. MCP 接続失敗時の処理ルール(vault にアクセスできない状況を扱うため)
2. Level 0 の厳格化ルール(過剰参照防止の実行時判断)
3. sensitive ファイルの引用禁止ルール(prompt injection 防御を兼ねる)

## 変更履歴(v1.4)

- **v1.0**(2026-07-13): 初版
- **v1.1**(2026-07-13):
  - 50_self/ 領域と日記フローを追加
  - Level 0 の厳格化
  - prompt caching への配慮
  - sensitive 引用禁止ルール強化
- **v1.2**(2026-07-14):
  - Phase 3.1 ツール(get_frontmatter、search_by_keyword、get_section)を参照フローに統合
  - Level 2 で get_frontmatter 先行使用パターン明示
  - Level 3 で search_by_keyword による絞り込みフロー追加
  - あいまい名解決の大規模フロー(search_by_keyword 活用)追加
  - Phase 3.2 の Issue 系ツール(create_issue、list_issues、add_issue_comment)対応
  - Issue 起票フロー(発火判定、生成、承認、投稿)を新設
  - description に Issue 起票のトリガー phrase を追加
- **v1.3**(2026-07-15):
  - Level 2 の一括取得対象に `30_projects/<RepoName>/project_instructions.md` を追加(存在すれば必読)
  - `project_instructions.md` の Front Matter に `applies_common: [<name>, ...]` があれば、対応する `00_meta/operations/<name>.md` も一括取得するフローを追加
  - Level 2 のキャッシュルールを明示(初回一括取得後は Chat 内で再読み込みしない)
  - Level 2 発火時に「特定プロジェクト相談時の総則」(`00_meta/project_instructions_vault.md`)の適用を明示
  - Level 3 で他プロジェクトの過去記録が検索結果に混入しても引用・要約しない旨を明示(作業混ざり防止)
  - Issue 起票フローで、プロジェクト固有のフォーマット(project_instructions.md + applies_common)に従うステップを追加
  - Issue 起票時に使用する GitHub MCP コネクタを「プロジェクトが指定するもののみ」に限定するルールを追加
  - 参照するファイルの正典に `00_meta/operations/<name>.md` を追加
  - prompt caching 固定順序に `00_meta/operations/<name>.md` を追加
- **v1.4**(2026-07-16):
  - レベル 1 のトリガーに「note 執筆の相談時の `20_notes/guides/` 4 ファイル一括取得」を追加
  - 「参照するファイルの正典」に `20_notes/guides/` の 4 ファイル(README、writing_process、writing_style、writing_examples)を追加
  - `00_meta/project_instructions_vault.md` v1.4 に整合(ケース 2 の詳細化に対応)
  - 背景: 2026-07-16 の記事 3 公開セッションで、Claude が `20_notes/guides/` の存在を発見できず writing_examples.md の更新をスキップする不遵守が発生。原因が Skill 側の記述不足だったため正式化
- **v1.5**(2026-07-17):
  - Phase 0.6: 新規保存時の id/aliases 自動付与、wikilink ID 参照、FM `_id`/`_ids` 参照
- **v1.6**(2026-07-17):
  - Phase 1c: Backlog 参照系 workflow(一覧提示、棚卸し、単一 item 参照)を追加
  - Level 1 で `00_meta/backlog_tags.md` を初回キャッシュ
  - GitHub Issue 状態確認と Vault backlog 同期提案(Naoya 承認 gate)
  - 保存系 workflow(起票、昇格)は Phase 1d の対象、暫定挙動を明記
  - description に backlog 参照トリガー phrase を追加
- **v1.7**(2026-07-17):
  - Phase 1d PR-A: Backlog 保存系 workflow(起票、open-questions 昇格、Cursor 委譲、Issue 起票、保留)を追加
  - 案提示 → Naoya 承認 gate → 実施の 2 段階必須、重複起票回避
  - description に backlog 保存トリガー phrase を追加
  - 停滞検出は Phase 1d PR-B(vault-maintainer)の対象

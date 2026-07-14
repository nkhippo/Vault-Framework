---
name: vault-manager
description: Use this skill when the user asks to save chat content to the personal Vault repository (nkhippo/Vault) via the Vault MCP connector. Trigger phrases include "Vault に保存して", "Obsidian に保存して"(legacy phrasing), "保存して"(when Vault context is clear), and any equivalent Japanese or English instructions to save, record, or archive to the Vault or Obsidian. Also triggers for diary/journal-related phrases such as "日記", "今日の記録", "diary", "今日あったこと", "振り返り", "reflection". Also use when the user references a specific personal project or app by exact name, by common alias (IPA, VCT, Structure, Listening etc.), or by function description ("発音を鍛えるアプリ", "語彙のアプリ"). Also use when the user asks to search past decisions or records from the personal Vault, or reads/writes to nkhippo/Vault via the Vault MCP connector.
---

# Vault Manager

Naoya の個人 Vault リポジトリ(`nkhippo/Vault`)を Cloudflare Workers ベースの MCP コネクタ経由で操作するための Skill。

## この Skill の役割

- vault への保存判断とファイル作成
- vault からの情報取得(参照判断ルールに従う)
- あいまいなアプリ名からのプロジェクト特定
- Cursor 委譲すべき作業の判定と指示書作成の提案
- 日記・個人記録の保存と、その参照制御(v1.1 で追加)

## 前提: MCP コネクタと vault の関係

- MCP コネクタ表示名: `Vault MCP`(Claude Pro Connectors 経由)
- MCP サーバリポジトリ: `nkhippo/Vault-MCP`(Cloudflare Workers デプロイ、URL: `https://vault-mcp.nkhippo.workers.dev`)
- vault リポジトリ: `nkhippo/Vault`
- vault の詳細ルールは vault 内の `00_meta/` に集約されている
- この Skill には核心のみを書き、詳細ルールは必要に応じて MCP 経由で `00_meta/` から取得する

過去記録には旧命名(`Obsidian-Vault`、`Obsidian-Vault-MCP`、`obsidian-vault-manager`)が残る場合があるが、歴史的記録として保持されるものであり、現行の運用対象は上記の新命名で統一される。

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

## 日記・個人記録の扱い(v1.1、50_self/ 領域)

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
- 検索操作(list_directory, get_file_content)で偶然一覧に出た場合も、能動的に読まない
- 過去 Chat 検索(conversation_search)の結果に 50_self/ 関連が含まれても、要約や引用の対象にしない
- `sensitive: true` のファイル全般に同じ扱いを適用(diary/reflection/goal 以外でも)

### 発火の否定判定

以下は日記保存フローを起動しない:

- 一般的な「今日どう過ごすか」等の未来計画(→ 通常保存フロー)
- 業務系の「日報」「業務記録」(→ 特に指示なければ chat_log として保存)
- プロジェクトの「振り返り」「retrospective」(→ 該当プロジェクトの logs/ 配下)

判断に迷う場合は Naoya に確認する。

## 参照判断ルール(5 段階)

Chat の状況に応じて、vault の参照深度を切り替える。過剰参照を避け、必要な情報だけを取りに行く。

### レベル 0: 参照しない(厳格化 v1.1)

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

判断に必要なファイル(初回のみ、以降キャッシュ):

- `00_meta/vault_structure.md`
- `00_meta/naming_conventions.md`
- `00_meta/vocabulary.md`
- 該当 type の template

同一 Chat 内で一度読んだファイルは再度読まない。

### レベル 2: プロジェクト情報を読む

以下の場合は該当プロジェクトのディレクトリから主要 3 ファイルを読む。

- ユーザーが特定プロジェクト名(正式名または通称)を明示した時
- ユーザーが機能表現でアプリを指した時(あいまい名解決フローを経由)

読むファイル:

- `30_projects/<RepoName>/README.md`
- `30_projects/<RepoName>/design-decisions.md`(存在すれば)
- `30_projects/<RepoName>/open-questions.md`(存在すれば)

Vault システム自体(`Vault` / `Vault-MCP` / `Vault-Framework`)に関する相談の場合は、加えて `30_projects/<RepoName>/handoff/current-state.md` を優先的に読む(直近状態の把握が最重要のため)。

### レベル 3: 過去記録を検索

以下の場合は過去の議論や決定を検索する。

- ユーザーが過去の意思決定を参照したい意図を示した時
- 例:「あの時決めたこと」「以前議論した」「過去の設計判断」
- **50_self/ 領域は明示的に「日記を読み返して」等と指示された時のみ発動**

使うツール:

- MCP の `list_directory` + `get_file_content`
- `conversation_search`(過去 Chat を検索、50_self/ 関連の Chat も除外対象)

### レベル 4: 全文精読

ユーザーがファイルパスを明示的に指定した時のみ。

### メタ指示への応答

| ユーザーの指示 | 調整内容 |
|---|---|
| 「vault を参照せず答えて」 | この Chat 内では以降レベル 0 に固定 |
| 「vault は必要なときだけ」 | デフォルト(状況判断)に戻す |
| 「vault の情報を優先して」 | 一般知識より vault 情報を優先 |
| 「関連する過去記録を全部読んで」 | レベル 3 を積極発動 |

## Anthropic prompt caching への配慮(v1.1)

Anthropic API は、前ターンと同じプレフィックスの context に対して 90% 割引の cache 適用がある。Skill はこれを最大化するために以下を守る。

### 固定順序でのファイル読み込み

初回セッションで複数の 00_meta ファイルを読む必要がある場合、常に以下の固定順序で読む。順序を毎回変えると cache miss を招く。

1. `00_meta/vault_structure.md`
2. `00_meta/naming_conventions.md`
3. `00_meta/vocabulary.md`
4. `00_meta/frontmatter_schema.md`(必要時のみ)
5. `00_meta/project_aliases.md`(あいまい名解決時のみ)
6. `00_meta/templates/<type>.md`(保存時のみ)
7. プロジェクト固有ファイル(30_projects/<RepoName>/ 配下)

### 会話の途中での再読み込み禁止

一度読んだファイルは、同一 Chat 内では再度 MCP 経由で取得しない。Claude の context にすでに載っている前提で参照する。ファイル内容が更新された可能性がある場合(Naoya が「更新した」と明示した場合等)のみ再取得する。

### 保存時の順序

保存指示への対応(下記 7 ステップ)は、Step 1→7 の順で固定。判断に迷って前に戻ることはしない(前に戻ると context が肥大化し cache 効率が落ちる)。

## あいまいなアプリ名の解決フロー

ユーザーが「発音を鍛えるアプリ」「単語のやつ」等、機能表現でアプリを指した場合:

1. MCP で `00_meta/project_aliases.md` を読む(まだキャッシュしていなければ)
2. 機能キーワードから該当候補を 1〜3 個抽出する
3. 候補が 1 個の場合: 「〈RepoName〉の情報を読みますね」と一言添えてレベル 2 参照に進む
4. 候補が 2 個以上の場合: 候補一覧を提示し確認を取ってから参照する
5. project_aliases.md でも候補が見つからない場合: `list_directory` で `30_projects/` を確認し、ヒットしたプロジェクトを候補として提示

## 保存指示への対応

### Step 1: 判断

以下のフローに従い保存先を決定する。3 秒以内に判断できなければ `90_inbox/` を選ぶ。

```
日記・振り返り・目標の意図か?(v1.1)
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

- `title`: 日本語で会話の主題(日記は `YYYY-MM-DD`)
- `created`, `updated`: 現在時刻(ISO8601、JST)
- `type`: 保存先に応じた type
- `status`: 保存先と内容に応じた status

**diary/reflection/goal の追加処理**

- `sensitive: true` を自動付与
- `tags` に `[self, diary]` 等の該当タグを最低限含める
- `mood` / `energy` / `weather` はユーザーが言及した場合のみ

**type 別の追加必須フィールドは vocabulary.md と各テンプレ参照**

### Step 5: 本文の組み立て

- Front Matter 直後に必ず H2 `## Summary` セクションを置く(diary は例外的に不要、テンプレ通り)
- テンプレートの構造を踏襲
- 日記の場合、Naoya の発話をそのまま構造化して記入。要約しない

### Step 6: MCP で保存

`Vault MCP` の `create_note` ツールを呼ぶ。同名ファイル既存時はエラーが返るので、以下で対応:

- 通常保存: ユーザーに確認する
- 日記の場合: 自動的に `update_note(mode=append)` に切り替えて追記(区切りとして時刻の H3 見出しを入れる)

### Step 7: 保存後の報告

通常:
```
保存しました。
- パス: <フルパス>
- タイプ: <type>
- 概要: <summary の内容>
```

日記の場合(最小限、内容は引用しない):
```
日記を保存しました(<パス>)。
```

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

判定時は Naoya に以下を提案:

```
この作業は複数ファイルの整合性が必要なため、Cursor 経由での実施を推奨します。
指示書を作成しますか?
```

## デグレ防止のガードレール

- `create_note` は同名ファイル既存時にエラーを返す前提で扱う。強制上書きしない
- `update_note` の `mode` は明示する(`replace_all` はデフォルトにしない)
- `delete_note` は必ずユーザー確認を取る
- 全操作でコミット SHA を控え、必要時に復元可能な状態を保つ
- センシティブ情報(Naoya の個人的トピック)を含むファイルは Front Matter で `sensitive: true` を必ず設定
- **`sensitive: true` のファイルは、他コンテキストでの引用・要約を絶対に行わない**(v1.1 で強化)
- MCP コネクタ接続失敗時は本文書の該当セクションを厳守

## 参照するファイルの正典

以下は vault 内の正典であり、Skill の記述が古い場合はこれらを優先する。

- `00_meta/vault_structure.md`
- `00_meta/naming_conventions.md`
- `00_meta/frontmatter_schema.md`
- `00_meta/vocabulary.md`(統制語彙、type 定義)
- `00_meta/claude_operation_rules.md`
- `00_meta/project_aliases.md`
- `00_meta/project_instructions_vault.md`
- `50_self/README.md`(v1.1、50_self 領域の運用方針)

Skill と vault の記述が矛盾したら、vault を正とみなす。ただし以下 3 点は Skill 側の記述を最優先:

1. MCP 接続失敗時の処理ルール(vault にアクセスできない状況を扱うため)
2. Level 0 の厳格化ルール(過剰参照防止の実行時判断)
3. sensitive ファイルの引用禁止ルール(prompt injection 防御を兼ねる)

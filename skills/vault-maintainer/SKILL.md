---
created: 2026-07-14 21:10:00+09:00
keywords:
- skill
- vault-maintainer
- maintenance
- abstract-generation
- level-2
- level-3
- level-4
- cursor-delegation
status: published
summary: 保守運用(Level 2、4)と抽象生成を担当する vault-maintainer Skill v1.0。vault-manager との棲み分けを明確化し、実作業は
  Cursor 委譲を前提とする設計。当初は3ヶ月の運用データ蓄積後に着手として保留されていたが、Naoya の判断で保留を解除して作成。
title: vault-maintainer SKILL.md v1.0
type: skill_definition
updated: 2026-07-14 21:05:25+09:00
id: pj-2026-07-13-5e3d
aliases:
- pj-2026-07-13-5e3d
---

---
name: vault-maintainer
description: Use this skill ONLY when the user explicitly requests Vault maintenance operations or abstract generation for the personal Vault (nkhippo/Vault) via the Vault MCP connector. Trigger phrases include "週次メンテ", "月次メンテ", "vault の整合性チェック", "vault のクリーンアップ", "統制語彙の整理", "handoff をアーカイブ", "リンク切れをチェック", "weekly maintenance", "monthly cleanup", "consistency check", "stalled 検出して", "停滞 backlog 見せて", and explicit abstract-generation requests such as "この議論を ADR にして", "chat_log から spec を生成", "抽象化して", "ADR 化して", "rejected-alternatives にまとめて". This skill covers maintenance Levels 2-4 (weekly / monthly / seasonal), backlog stalled detection (Phase 1d PR-B), and abstract generation. It does NOT handle ordinary save/reference operations or Level 1 daily auto-correction — those belong to the vault-manager skill. Do NOT trigger this skill for routine "保存して" or "参照して" requests.
---

# Vault Maintainer (v1.0)

Naoya の個人 Vault リポジトリ(`nkhippo/Vault`)の**保守運用(Level 2〜4)と抽象生成**を担当する Skill。日常の保存・参照・Level 1 自動修正は担当せず、それらは `vault-manager` Skill に委ねる。

## この Skill の役割

- 保守運用 Level 2(週次補正)の実施判断と Cursor 指示書作成
- **Backlog stalled detection**(Level 2 週次の一環、Phase 1d PR-B)
- 保守運用 Level 3(月次補正)の実施判断と Cursor 指示書作成
- 保守運用 Level 4(季節補正)の計画立案と Cursor 指示書作成
- 抽象生成(chat_log → ADR / spec / rejected-alternatives / guideline)の実施
- handoff のアーカイブ判断

## vault-manager との棲み分け(最重要)

この Skill と `vault-manager` は明確に役割分担する。誤発火を避けるため、以下を厳守する。

| 発話・状況 | 担当 Skill |
|---|---|
| 「保存して」「Vault に保存」 | vault-manager |
| 「参照して」「過去記録を教えて」 | vault-manager |
| 「日記に書いて」 | vault-manager |
| Level 1 の自動修正(保存時の統制語彙補正等) | vault-manager |
| あいまい名解決 | vault-manager |
| Issue 起票 | vault-manager |
| **「週次メンテ」「整合性チェック」** | **vault-maintainer(この Skill)** |
| **「月次クリーンアップ」「handoff アーカイブ」** | **vault-maintainer** |
| **「季節補正」「大規模な構造変更」** | **vault-maintainer** |
| **「この議論を ADR にして」「抽象化して」** | **vault-maintainer** |

**この Skill は、保守運用または抽象生成の明示的なトリガーがない限り、絶対に発火しない**。通常の保存・参照系の発話には一切反応しない。判断に迷う場合は vault-manager に処理を委ねる。

## Vault MCP コネクタ接続失敗時の処理(最優先ルール)

`Vault MCP` コネクタ経由の操作が接続エラーで失敗した場合、以下を厳守する(vault-manager と同一のルール)。

1. **一度だけリトライする**
2. リトライも失敗した場合、**その処理を中断する**
3. 憶測・訓練データ・キャッシュ・推定で補って処理を続けることは絶対に禁止
4. Naoya に接続失敗と中断を明示し、判断を仰ぐ

この規則は他のあらゆる Skill 動作より優先される。

## 保守運用の全体像

保守運用は 4 レベルあり、この Skill は **Level 2〜4** を担当する(Level 1 は vault-manager が日常発火で担当)。

| レベル | 頻度 | 担当 | この Skill の関与 |
|---|---|---|---|
| Level 1 | 日常(イベント駆動) | vault-manager | 関与しない |
| Level 2 | 週次 | Cursor 委譲 | 実施判断 + 指示書作成 |
| Level 3 | 月次 | Cursor 委譲 | 実施判断 + 指示書作成 |
| Level 4 | 季節(3ヶ月毎) | Naoya 主導 + Cursor | 計画立案 + 指示書作成 |

詳細な仕様は vault 内 or Framework の `docs/ja/specs/maintenance-four-levels.md` を参照(必要時に MCP 経由で取得)。

## Level 2: 週次補正

### 発火判定

以下の明示的トリガーで発火:

- 「週次メンテ(をお願い)」「weekly maintenance」
- 「vault の整合性チェック」「consistency check」
- 「リンク切れをチェック」「90_inbox を再分類」

### 作業内容(Cursor 委譲前提)

1. 90_inbox/ に落ちたファイルの再分類候補を洗い出す
2. `vocabulary.md` に未登録の type/tag/project を使っているファイルを検出
3. wikilink の指し先が実在するかチェック(リンク切れ検出)
4. 各プロジェクトの handoff/current-state.md の updated 日時を確認、1 週間以上更新されていないものを報告
5. Backlog stalled detection(下記セクション参照、Phase 1d PR-B)

### 実施フロー

1. Level 3 参照(search_by_keyword + list_directory + get_frontmatter)で対象を洗い出す
2. 検出結果を Naoya に提示(修正候補の一覧)
3. Naoya の承認を得て、Cursor 用の週次バッチ指示書を作成
4. 指示書は `30_projects/Vault/handoff/recent-changes/YYYY/MM/` に保存する形で提案

**この Skill 自身は一括修正を実行しない**。検出と指示書作成までを担当し、実際の一括変更は Cursor に委譲する(3 ファイル以上の一括更新は Cursor 委譲、という Framework の原則に従う)。

## Backlog Stalled Detection(Level 2 週次、Phase 1d PR-B 以降)

詳細規約は Vault-Framework `docs/ja/backlog/maintainer-workflow.md` を参照。要点のみ記載。

### 実行タイミング

- **週次メンテ**の一環(トリガー: 「週次メンテして」「Weekly maintenance」等)
- **単体実行**(トリガー: 「stalled 検出して」「停滞 backlog 見せて」等)

### Level 1 追加読み込み

Stalled detection 初回検知時、以下を Level 1 で読み込み Chat 内キャッシュ:

- Vault `00_meta/backlog_tags.md`

### Scope

- Default: 全 backlog(全 `30_projects/*/backlog/`、`_life/backlog/`、`_ideas/*/incubating/*/backlog/`)
- Naoya が特定プロジェクトを指定した場合はそれに絞る

### Threshold

- Default: 14 日(2 週間)
- Naoya の明示指示(「直近 1 週間」等)で変更可

### 検出フロー

1. `search_by_keyword` で対象 backlog item 列挙
2. 各 item の `get_frontmatter` で `state`, `updated`, `tags`, `github_issue` 取得
3. フィルタ: `state: open` かつ `updated < today - threshold`
4. `stalled` tag 未付与(A 群)と 既付与(B 群)に分別

### 提案パターン

- **A 群(未付与)**: stalled tag 付与 / abandoned 化 / 即時進捗確認、から選択
- **B 群(既付与)**: abandoned 化 / 進捗記述 + tag 削除 / tag 継続、から選択

### 表形式提示

| # | Group | Title | Kind | Assignee | Last Updated | Days Stalled | GitHub | Suggested Action |

### Naoya 承認 gate(必須)

各 item に対する action は Naoya の明示指示を経る:

- 個別: 「これは tag、これは abandoned、これは skip」
- 一括: 「全部 tag 付けて」(慎重確認後)

無断更新禁止。承認後は `update_note` で FM 更新 + H2 History 追記。

### GitHub Issue 状態確認

Stalled 候補が `github_issue` を持つ場合、対象プロジェクトの GitHub コネクタで Issue state 確認可(作業混ざり防止規約遵守)。全体週次メンテでは複数コネクタ切り替えを Naoya に透明に伝えつつ実施可。

Issue closed & merged なのに Vault open → 同期漏れとして `state: done` 提案(stalled ではない扱い)。

### 他 Level 2 タスクとの関係

既存 Level 2 タスク(リンク切れチェック、handoff アーカイブ等)と並列実行。週次メンテ完了報告に stalled detection 結果も含める。

### 完了報告

「Stalled detection 完了:
- 検出: N 件(A 群 X、B 群 Y)
- 更新: stalled 付与 A、abandoned 化 B、skip C
- 次回検知: `<週次メンテ次回 or on-demand>`」

## Level 3: 月次補正

### 発火判定

- 「月次メンテ」「月次クリーンアップ」「monthly cleanup」
- 「handoff をアーカイブ」
- 「統制語彙の見直し」

### 作業内容

1. 30_projects 全体の handoff/current-state.md 更新確認
2. current-state.md が肥大化(500 行超 or prepend が過剰)している場合、recent-changes/ へのアーカイブ計画を立てる
3. 統制語彙の使用頻度分析(未使用 tag、過剰使用 tag、新規追加候補)
4. Skill と vault の記述の乖離チェック(SKILL.md と 00_meta/ の整合)

### handoff アーカイブの手順

current-state.md が肥大化している場合:

1. 最新の状態(直近 2〜4 週間分)のみを残す
2. それ以前の更新セクションを `handoff/recent-changes/YYYY/MM/YYYY-MM_monthly-archive.md` に切り出す
3. current-state.md に「## Archive: YYYY-MM の変更履歴」セクションと wikilink を追加
4. この作業は Cursor 委譲(prepend されたセクションの切り出しは慎重を要するため)

## Level 4: 季節補正

### 発火判定

- 「季節補正」「seasonal maintenance」
- 「大規模な構造変更」「ディレクトリ再編」
- Skill や Vault-MCP のメジャーバージョンアップ時

### 作業内容(計画立案が中心)

1. ディレクトリ再編の計画(例: 10_chat_logs/ の下位分類見直し)
2. 廃止 tag/type の一括整理計画
3. 旧命名の一括書き換え計画(過去の命名変更に伴う整合)
4. Framework 側の Public 化・英訳同期の計画

### 実施フロー

季節補正は大規模なため:

1. まず Level 3 参照で現状を把握し、変更の影響範囲を分析
2. Naoya と変更計画をすり合わせる(複数セッションに分けることも)
3. Cursor 用の詳細な指示書を作成(複数指示書を直列/並列で)
4. 実行前に backup ブランチの作成を必ず指示書に含める

**この Skill は計画立案と指示書作成を担当し、実行は Cursor に委譲する**。

## 抽象生成

具体的な chat_log から抽象的なドキュメント(ADR / spec / rejected-alternatives / guideline)を生成する。保守運用とは独立した並行運用。

### 発火判定

- 「この議論を ADR にして」「ADR 化して」
- 「chat_log から spec を生成」「抽象化して」
- 「却下案を rejected-alternatives にまとめて」
- 「そろそろ抽象化したい」

### 発火不要のケース(重要)

- **単発の chat_log**: 抽象化するには早すぎる(蓄積を待つ)
- **明確な意思決定がない議論**: 決定に至っていないものは ADR 化しない
- **50_self/ 領域**: sensitive、絶対に抽象化しない

### 生成フロー

1. **対象 chat_log の特定**: `search_by_keyword(keyword=<topic>, path_prefix='10_chat_logs/')` 等で収集
2. **抽象化の粒度判定**:
   - 1 chat_log → 1 ADR(明確な意思決定を含む場合)
   - N chat_logs → 1 spec(複数議論の集約から仕様を抽出)
   - 1 議論 → 1 rejected-alternative(却下案の記録)
   - 複数の意思決定 → 1 guideline(判断パターンから原則を抽出)
3. **骨格の生成**: 該当 type のテンプレート構造(ADR: Summary → Context → Decision → Consequences → Alternatives Considered → Related、spec: Summary → Scope → …)で草案を作成
4. **Naoya のレビュー**: 草案を提示、内容の充実と相互リンクの確認
5. **保存**: 単一ファイルなら直接保存、複数ファイルの一括生成なら Cursor 委譲

### 生成先

- ADR → `30_projects/Vault-Framework/docs/ja/decisions/NNNN-slug.md`(staging)
- spec → `30_projects/Vault-Framework/docs/ja/specs/slug.md`
- rejected-alternatives → `30_projects/Vault-Framework/docs/ja/rejected-alternatives/slug.md`
- guideline → `30_projects/Vault-Framework/docs/ja/guidelines/slug.md`

staging 後、Framework 本体へのミラーリングは Cursor 委譲。

### 品質チェック

生成した ADR/spec は以下を確認:

- Summary が 2〜4 行で本質を捉えているか
- Context が「なぜ判断が必要だったか」を明示しているか
- Consequences に Positive / Negative / Mitigation が揃っているか
- Alternatives Considered に却下理由があるか
- Related に関連 ADR/spec/chat_log があるか

## 参照レベルの活用

この Skill は主に Level 3 参照(過去記録の検索)を使う。vault-manager の参照レベルシステムと同じルールに従う:

- `search_by_keyword` で対象を絞る
- `get_frontmatter` で内容を確認
- 必要なら `get_file_content` / `get_section` で本文取得
- **50_self/ 領域は抽象生成・保守運用のどちらでも対象外**(sensitive)

## Cursor 委譲の徹底

この Skill の作業の多くは Cursor 委譲を前提とする。理由:

- 保守運用 Level 2〜4 は複数ファイルの一括操作を含む(Framework の「3 ファイル以上は Cursor 委譲」原則)
- 抽象生成の複数ファイル一括生成(ADR + rejected-alternatives 複数等)も同様

この Skill は「検出・分析・計画・指示書作成」を担当し、「実際の一括変更・生成」は Cursor に委譲する。単一ファイルの抽象生成のみ、この Skill が直接保存してよい。

## デグレ防止のガードレール

- 保守運用・抽象生成のいずれも、実行前に Naoya の承認を得る
- 一括変更は必ず Cursor 委譲 + backup ブランチ作成を指示書に含める
- `delete_note` を伴う操作(廃止ファイルの削除等)は必ず Naoya 確認
- 50_self/ 領域は保守運用・抽象生成の対象から常に除外
- 全操作でコミット SHA を控え、復元可能な状態を保つ
- MCP コネクタ接続失敗時は該当セクションを厳守

## 参照するファイルの正典

以下は vault 内 or Framework の正典であり、この Skill の記述が古い場合はこれらを優先する。

- `docs/ja/specs/maintenance-four-levels.md`(保守運用 4 レベルの詳細)
- `docs/ja/specs/abstract-generation.md`(抽象生成の詳細)
- `docs/ja/specs/handoff-mechanism.md`(handoff アーカイブの詳細)
- `00_meta/vocabulary.md`(統制語彙)
- `00_meta/vault_maintenance_config.md`(cadence 設定)

Skill と vault の記述が矛盾したら vault を正とみなす。ただし MCP 接続失敗時の処理ルールと、vault-manager との棲み分けルールは Skill 側を最優先とする。

## 変更履歴

- **v1.0**(2026-07-14): 初版。当初「3ヶ月の運用データ蓄積後に着手」として保留されていたが、Naoya の判断で保留を解除して作成。保守運用 Level 2〜4 と抽象生成を担当。vault-manager との棲み分けを明確化。実作業は Cursor 委譲を前提とする設計。
- **v1.1**(2026-07-17):
  - Phase 1d PR-B: Backlog stalled detection を Level 2 週次メンテに追加
  - Default threshold 14 日、Naoya 承認 gate 必須
  - vault-manager(on-demand 棚卸し)との責任分離を明確化
  - description に stalled 検出トリガー phrase を追加

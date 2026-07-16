---
audience: mixed
created: 2026-07-14 08:15:00+09:00
keywords:
- save-decision
- flow
- 7-steps
- skill-implementation
- guidelines
related_adrs:
- '0007'
- '0011'
- '0016'
status: published
summary: Chat 保存指示に対する Skill の判断フロー(7 ステップ)の詳細実装ガイド。ADR-0007 の具体的な運用手順を規定。
tags:
- guideline
- save-flow
- skill-implementation
title: 保存判断フロー
type: guideline
updated: 2026-07-14 08:15:00+09:00
id: pj-2026-07-13-c302
aliases:
- pj-2026-07-13-c302
---

## Summary

Chat 保存指示に対する Skill の判断フロー(7 ステップ)の詳細実装ガイド。ADR-0007「保存先思想:最初から適切な場所へ」の具体的な運用手順を規定。SKILL.md 側の実装骨格として、Skill 実装者(Claude)が参照する。

## Scope

このガイドラインが規定するもの:

- 保存判断の 7 ステップ詳細
- 各ステップの判定ロジック
- 保存先ディレクトリの決定基準
- ファイル名の生成
- Front Matter の組み立て
- MCP 呼び出しの詳細
- 保存後の報告フォーマット

このガイドラインが規定しないもの:

- 3 秒ルールの発火条件(v1-nine-principles.md 参照)
- 保存判断の思想的背景(ADR-0007 参照)

## Design Principle

**「3 秒で判断できないなら、判断を単純化する」**。以下 3 原則:

1. **Fast path 優先**: 明らかなケースは即座に判定
2. **フォールバックは 90_inbox/**: 迷ったら inbox、Level 2 で再分類
3. **報告は最小限**: 判断過程は表に出さず、結果のみ報告

## Overall Flow

```
[Naoya の保存指示]
    ↓
Step 1: 保存先ディレクトリの判定
    ↓
Step 2: ユーザーへの確認は不要(判定して進行)
    ↓
Step 3: ファイル名の生成
    ↓
Step 4: Front Matter の組み立て
    ↓
Step 5: 本文の組み立て
    ↓
Step 6: MCP `create_note` 呼び出し
    ↓
Step 7: 保存後の報告
```

## Step 1: 保存先ディレクトリの判定

### 判定フロー(上から順に評価)

```
日記・振り返り・目標の意図か?
├── Yes → 50_self/diary/ or reflections/ or goals/(Skill 側で sensitive: true 自動付与)
└── No → 次へ

Chat の生ログ性が強い(検討・議論の記録)?
├── Yes → 10_chat_logs/YYYY/MM/
└── No → 次へ

note にする予定・執筆中?
├── Yes → 20_notes/wip/
└── No → 次へ

note を公開した清書版?
├── Yes → 20_notes/published/
└── No → 次へ

新規アイデア(未リポジトリ化)?
├── Yes → 30_projects/_ideas/incubating/<slug>/ or active/<slug>/
└── No → 次へ

特定リポジトリの設計・意思決定?
├── Yes → 30_projects/<RepoName>/logs/YYYY/MM/
│  ├─ 意思決定確定 → design-decisions.md に追記
│  ├─ 新規未解決論点 → open-questions.md に追記
│  ├─ ロードマップ更新 → roadmap.md
│  └─ 直近状態のスナップショット更新 → handoff/current-state.md prepend
└── No → 次へ

汎用ナレッジ(記事・書籍からの学び等)?
├── Yes → 40_knowledge/<category>/
└── No → 次へ

判断困難(3 秒以内に決められない)?
└── 90_inbox/
```

### 判定のヒント

各分岐で判断するためのシグナル:

#### 日記・振り返り・目標の意図

- 発話: 「日記に書いて」「今日あったこと」「振り返り」「目標」「これからやりたいこと」
- 例外: 「日報」「業務記録」は通常 chat_log として扱う(判断に迷ったら Naoya 確認)

#### Chat の生ログ性

- 議論の内容が「時系列で並べる価値がある」場合
- 特定の意思決定・仕様に集約されていない、まだ流動的な段階
- 「あの時こんな話をした」と後から振り返る対象

#### note 執筆中

- 発話に「note」「記事」「投稿」等のキーワード
- 構成を練っている、下書き段階

#### 新規アイデア

- リポジトリがまだ作られていない
- アイデアの温度感(incubating: 温めているだけ / active: リポジトリ化目前)

#### 特定リポジトリの話

- あいまい名解決フローで RepoName が確定
- 該当プロジェクトの設計・実装に関する議論

## Step 2: ユーザーへの確認は不要

**「どこに保存しますか?」とは聞かない**。Claude が判断して保存し、結果を報告する。

例外:
- Step 1 の判定で「特定リポジトリの話」だが、あいまい名解決が不完全な場合はプロジェクト名を確認
- Step 1 で 90_inbox/ にフォールバックする場合、Naoya に「判断つかなかったので inbox に置きます」と一言添える

## Step 3: ファイル名の生成

### 標準ファイル名

`YYYY-MM-DD_kebab-case-slug.md`

詳細は [[../specs/file-naming.md]] 参照。

### スラグ生成のロジック

1. Chat の主題を英語の名詞句に変換
2. 全て小文字、スペースをハイフンに置換
3. 英数字とハイフン以外を削除
4. 30 文字以内にトリミング(単語境界で切る)

### 特殊パターン

- **diary**: `YYYY-MM-DD.md`(スラグなし)
- **design-decisions.md、open-questions.md、roadmap.md、handoff/current-state.md**: 固定ファイル名

### 重複チェック

- 同名ファイル存在時: `create_note` はエラーを返す
- 対応:
  - **diary の場合**: 自動的に `update_note(mode=append)` に切り替え
  - **通常の場合**: Naoya に確認(`_v2` 付与 or 別スラグ提案)

## Step 4: Front Matter の組み立て

### 必須フィールド(全 type 共通)

```yaml
title: <日本語の主題>
created: <ISO 8601 datetime with JST>
updated: <ISO 8601 datetime with JST>
type: <vocabulary.md の type>
status: <vocabulary.md の status>
```

### type 別の追加必須フィールド

該当 type のテンプレート(`00_meta/templates/<type>.md`)から取得。詳細は [[../specs/frontmatter-schema.md]] 参照。

### diary/reflection/goal の追加処理

- `sensitive: true` を自動付与(Skill 側で強制)
- `tags` に該当タグを最低限含める(例: `[self, diary]`)
- `mood` / `energy` / `weather` はユーザーが言及した場合のみ

### 統制語彙のチェック

- type、status、tags が vocabulary.md に登録されているか確認
- 未登録なら Level 1 の自動修正で類似値に置き換え or Naoya に確認

## Step 5: 本文の組み立て

### Summary セクション必須

Front Matter 直後に H2 `## Summary` セクションを置く:

```markdown
## Summary

<2-4 行の要約>
```

### 例外

- **diary**: テンプレの見出し(「今日あったこと」等)で開始、Summary 不要
- **template**: テンプレファイル自体、Summary 省略可
- **極短の inbox**: Summary 省略可

### テンプレートの踏襲

該当 type のテンプレート構造を踏襲(00_meta/templates/<type>.md の見出しを反映)。

### 日記の場合

Naoya の発話をそのまま構造化して記入。要約しない、Claude の解釈を加えない。

### chat_log の場合

- 議論の背景、主要な論点、決定事項、未決事項を構造化
- 会話ログの生の抜粋は必要に応じて含める(全部貼る必要はない)

## Step 6: MCP `create_note` 呼び出し

### 標準呼び出し

```
create_note(
  path=<Step 3 で生成>,
  frontmatter=<Step 4 で組み立て>,
  body=<Step 5 で組み立て>,
  commit_message=<オプション>
)
```

### エラーハンドリング

同名ファイル既存エラー:
- diary: `update_note(mode=append)` に切り替え、時刻の H3 見出しを区切りとして追記
- 通常: Naoya に確認、以下の選択肢:
  - `_v2` 付与して新規保存
  - 別スラグに変更して新規保存
  - 既存ファイルを更新(update_note)
  - キャンセル

### 接続失敗

MCP 接続失敗時は ADR-0016 のルールを適用:
- 1 回リトライ
- リトライも失敗したら中断
- Naoya に報告、判断を仰ぐ

## Step 7: 保存後の報告

### 通常保存(標準フォーマット)

```
保存しました。
- パス: <フルパス>
- タイプ: <type>
- 概要: <summary の内容>
```

### diary の場合(最小限、内容引用禁止)

```
日記を保存しました(<パス>)。
```

### 更新の場合

```
更新しました。
- パス: <フルパス>
- 変更内容: <mode に応じた説明>
```

### handoff/current-state.md の prepend 更新の場合

```
handoff/current-state.md を更新しました(<プロジェクト名>)。
```

## Edge Cases

### 議論が複数プロジェクトに跨る場合

- 主にどのプロジェクトの話かを Skill が判定
- 判定できなければ 90_inbox/ に保存し、Naoya に報告

### Chat 内で複数保存指示がある場合

- 各保存指示を独立して処理
- 3 件以上の連続保存指示は Cursor 委譲を検討(ただし独立操作なら Claude で完結可能)

### 発話の途中で保存指示が挟まれた場合

- 該当時点までの Chat 内容を保存対象とする
- 続きの議論は次の保存指示で対応

## Skill 実装のヒント

### Fast path の追求

- Chat 冒頭でプロジェクト名が明示された場合、Step 1 の判定を早期に確定
- あいまい名解決フローも早期に発火

### 判断ログの内部保持

- Step 1 の判定結果を Chat 内で記憶
- 同じ Chat 内で複数回の保存指示があった場合、判定を再利用

### 保存前の最終確認

- Chat 内で Naoya が「間違えた、別のプロジェクト」と訂正した場合、Step 1 に戻る

## References

- **関連 ADR**: 
  - [[../decisions/0007-save-destination-plan-b.md]](保存先思想)
  - [[../decisions/0011-directory-restructure-captures-self.md]](50_self/ の扱い)
  - [[../decisions/0016-mcp-connection-failure-abort.md]](接続失敗ルール)
- **関連 spec**: 
  - [[../specs/file-naming.md]](ファイル名の詳細)
  - [[../specs/frontmatter-schema.md]](Front Matter の詳細)
  - [[../specs/reference-level-system.md]](Level 遷移)
- **関連 guideline**: 
  - [[./v1-nine-principles.md]](Principle 7: 3 秒ルール)
  - [[./operational-principles.md]](Operational Pattern 2: 保存指示の受け方)
- **実装**: `skills/vault-manager/SKILL.md` の該当セクション

## Change Log

- 2026-07-13: 初版(7 ステップの詳細確定)
- 2026-07-14: 実運用(C1-C3 で 40+ 保存経験)を反映

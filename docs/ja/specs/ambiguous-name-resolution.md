---
audience: mixed
created: 2026-07-14T07:25:00+09:00
keywords:
  - ambiguous-name
  - resolution
  - project-aliases
  - spec
  - disambiguation
  - search-by-keyword
  - phase3.1-tools
related_adrs:
  - "0013"
status: published
summary: ユーザーが機能表現・通称・略称でアプリを指した時、Skill が正式リポジトリ名を特定するあいまい名解決フローの詳細仕様。project_aliases.md の構造と Skill の判定ロジック、複数候補時の対話パターンを規定。
tags:
  - spec
  - ambiguous-name
  - resolution
title: あいまい名解決 仕様
type: spec
updated: 2026-07-14T07:25:00+09:00
---

## Summary

ユーザーが機能表現・通称・略称でアプリを指した時、Skill が正式リポジトリ名を特定するあいまい名解決フローの詳細仕様。project_aliases.md の構造と Skill の判定ロジック、複数候補時の対話パターン、Phase 3.1 の search_by_keyword 活用を規定。

## Scope

このスペックが規定するもの:

- あいまい名解決フローの全体構造
- project_aliases.md の記述形式
- Skill の候補抽出ロジック
- 1 候補 / 複数候補 / 候補なしの対応パターン
- Vault-MCP Phase 3.1 の search_by_keyword 活用

このスペックが規定しないもの:

- project_aliases.md の具体的なエントリ内容(Naoya の実運用データ、vault 側で管理)
- Level 2 参照の詳細(reference-level-system.md 参照)

## Design Principle

**「あいまいさは会話コストではなく Skill の判定コスト」で処理する**。以下 3 原則:

1. **Skill が能動的に判定**: ユーザーに「何のことですか?」と聞き返す前に、まず Skill が候補を絞り込む
2. **確信度による分岐**: 1 候補で確信あり → 即進行、複数候補 → 確認、候補なし → 誠実に不明を伝える
3. **判定過程の透明性**: 「〈RepoName〉と判断しました」と一言添える(Naoya が誤りに気づきやすい)

## project_aliases.md の Structure

各プロジェクトを 1 セクション(H3)で記述:

```markdown
### <RepoName>

- 正式リポジトリ名: `<RepoName>`
- カテゴリ: <カテゴリ、例: 英語学習(発音) / MCP サーバ / vault / Webアプリ 等>
- 通称: <通称 1>, <通称 2>, <呼び方いろいろ>
- 機能キーワード: <機能を表すキーワードを列挙>
- 対象言語: <該当する場合>
- UI 対応言語: <該当する場合>
- 関連リポジトリ: <該当する場合>
- 一言メモ: <このプロジェクトが何かを 1〜2 行で>
```

### 各フィールドの役割

- **正式リポジトリ名**: マッチした後に Skill が使うプロジェクト識別子
- **カテゴリ**: 大分類(異なるカテゴリ間の混同を防ぐ)
- **通称**: Naoya が実際に会話で使う呼び方(命名の揺らぎを吸収)
- **機能キーワード**: 「発音アプリ」等の機能表現からのマッチング用
- **一言メモ**: Skill が候補を提示する時に添える説明

## Skill の Resolution Flow

### Step 1: 発火判定

ユーザーの発話に以下が含まれる時、あいまい名解決を発火:

- プロジェクトの通称・略称(「IPA」「VCT」「ボールト」等)
- 機能表現(「発音のアプリ」「単語のやつ」等)
- 曖昧な指示(「あのプロジェクト」「例のリポジトリ」)

### Step 2: project_aliases.md の取得

- Level 1 参照として `00_meta/project_aliases.md` を取得
- 同一 Chat 内で既に取得済みならスキップ

### Step 3: 候補抽出

以下の順序で照合:

1. **正式リポジトリ名との完全一致**: 大文字小文字を含めて厳密照合(即座に確定、Step 6 へ)
2. **通称との部分一致**: 大文字小文字を無視、部分文字列マッチ
3. **機能キーワードとの部分一致**: 大文字小文字を無視
4. **カテゴリとの部分一致**: 大分類での絞り込み

各候補にスコアを付けて 1-3 位を候補として保持。

### Step 4: 候補数による分岐

| 候補数 | 対応 |
|---|---|
| 1 候補(明確) | Step 5(単一候補で進行)へ |
| 2-3 候補 | Step 5A(候補提示)へ |
| 0 候補 | Step 5B(候補なし対応)へ |
| 4+ 候補 | Step 5C(絞り込み依頼)へ |

### Step 5: 単一候補で進行

以下のような一言を添えて、Level 2 参照(該当プロジェクトの主要 3-4 ファイル読み込み)に進む:

```
〈RepoName〉の情報を読みますね。
```

または、より丁寧に:

```
〈RepoName〉のことですね。〈一言メモ〉を扱っているプロジェクトです。
```

### Step 5A: 複数候補提示

以下のフォーマットで候補を提示し、Naoya の確認を得る:

```
以下のプロジェクトが該当しそうです。どれのことですか?

1. **〈RepoName1〉** - <一言メモ>
2. **〈RepoName2〉** - <一言メモ>
3. **〈RepoName3〉** - <一言メモ>

もし別のプロジェクトの場合、正式名か機能を教えてください。
```

### Step 5B: 候補なし対応

以下のように誠実に伝える:

```
「〈ユーザーの発話〉」に該当するプロジェクトが project_aliases.md に見つかりませんでした。

以下のいずれかで教えていただけますか?

1. 正式リポジトリ名(例: `IPASoundDrill`)
2. カテゴリ(例: 英語学習アプリ、MCP サーバ、vault 系)
3. どのような機能を持つか(具体的に)
```

さらに、以下のフォールバックを実施:

- `list_directory('30_projects/')` で存在するプロジェクトを一覧化
- ユーザーの発話に近そうなものがあれば候補として提示

### Step 5C: 絞り込み依頼

4 候補以上ある場合、絞り込みを依頼:

```
「〈ユーザーの発話〉」に該当するプロジェクトが複数あります(N 件)。

具体的なプロジェクト名か、以下のカテゴリで絞り込んでいただけますか?

- カテゴリ A(例: 英語学習)
- カテゴリ B(例: MCP・vault 系)
- カテゴリ C(例: その他)
```

### Step 6: Level 2 参照へ遷移

該当プロジェクトが確定したら、Level 2 参照(reference-level-system.md 参照)へ。

## Phase 3.1 ツールの活用

### search_by_keyword の使用

project_aliases.md が肥大化(プロジェクト数 20+ 等)した場合、以下の順序で最適化:

1. **通常フロー(小規模時)**: project_aliases.md 全体を読んで候補抽出
2. **最適化フロー(大規模時)**:
   - `search_by_keyword(keyword=<ユーザーの発話>, path_prefix='00_meta/', limit=10)` で候補を絞る
   - ヒットした project_aliases.md の該当セクションのみ `get_section` で取得

### 判定コスト最小化

- `get_frontmatter` で project_aliases.md の updated が古い場合、キャッシュを利用
- 同一 Chat 内で同じあいまい名解決が発火した場合、Step 3 の結果をキャッシュ

## Edge Cases

### 通称の重複

複数プロジェクトが同じ通称を持つ場合(例: `IPA` が IPASoundDrill と別のプロジェクトの両方で使われる):

- 通称マッチで両方を候補に含める
- Step 5A(候補提示)で明示的に確認を得る

### 表記揺れ

日本語⇔英語⇔ローマ字の揺れに対応:

- `ボールト`(日本語) = `Vault`(英語) = `Bo-ruto`(ローマ字)
- project_aliases.md の通称欄に全パターンを列挙

### 過去 Chat との連続性

前セッションで「あのアプリ」と指したものが今回も同じ場合、conversation_search で過去 Chat から前セッションの推定を活用する余地あり(Level 3 遷移)。

### プロジェクト名の変更

過去のプロジェクト名(旧名)で発話された場合:

- project_aliases.md の通称欄に旧名を追加(履歴として保持)
- Skill は最新の正式名(`<RepoName>`)で応答

## Feedback Loop

あいまい名解決の精度向上のため:

- Naoya が「別のプロジェクトです」と訂正した場合、Skill は次のセッションでその情報を活用したい
- しかしプロジェクト間で永続的な学習は Skill レベルでは行わない(Chat 内でのみ有効)
- 頻繁に発生する誤解は、Naoya が project_aliases.md の通称欄を編集して恒久対応

## References

- **関連 ADR**: 
  - [[../decisions/0013-projects-merge-two-to-one.md]](1 Project 統合、あいまい名解決フローの前提)
- **関連 spec**: 
  - [[./reference-level-system.md]](Level 2 遷移の詳細)
  - [[./vocabulary-design.md]](project フィールドの管理)
- **実装**: `vault-templates/00_meta/project_aliases.md`(vault 内テンプレ)

## Change Log

- 2026-07-13: 初版(あいまい名解決フローの詳細確定)
- 2026-07-14: Phase 3.1 ツール活用を追加

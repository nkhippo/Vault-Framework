---
audience: mixed
created: 2026-07-14 07:05:00+09:00
keywords:
- vocabulary
- controlled-vocabulary
- spec
- type
- status
- tags
- project
- extension
- deprecation
- governance
related_adrs: []
status: published
summary: Vault で使う統制語彙の設計原則、拡張手順、管理方針の詳細仕様。type、status、tags、project の 4 カテゴリについて、なぜ統制するか、どう拡張するかを規定。
tags:
- spec
- vocabulary
- governance
title: 統制語彙の設計 仕様
type: spec
updated: 2026-07-14 07:05:00+09:00
id: pj-2026-07-13-f5e9
aliases:
- pj-2026-07-13-f5e9
---

## Summary

Vault で使う統制語彙(controlled vocabulary)の設計原則、拡張手順、管理方針の詳細仕様。00_meta/vocabulary.md の背景思想を体系化する。type、status、tags、project の 4 種類について、なぜ統制するか、どう拡張するかを規定。

## Scope

このスペックが規定するもの:

- 統制語彙の 4 カテゴリ(type、status、tags、project)の設計原則
- 新規追加の手順
- 廃止・変更の手順
- 統制語彙違反時の対応
- vocabulary.md との関係

このスペックが規定しないもの:

- 具体的な type/status/tag の値定義(vocabulary.md 参照)
- Front Matter の記述形式(frontmatter-schema.md 参照)

## Why Controlled Vocabulary

### 問題(統制なしの場合)

- type に `chatlog` / `chat_log` / `chat-log` / `ChatLog` が混在
- tags に `mcp` / `MCP` / `Mcp` / `model-context-protocol` が混在
- 検索(search_by_keyword)のヒット率低下
- 保守運用(整合性チェック)のコスト増
- AI(Claude)の判定精度低下

### 統制がもたらす価値

- **検索・分類の一貫性**: `type: chat_log` で検索すれば必ずヒット
- **AI の判定精度**: Skill が「これは chat_log」と即断できる
- **保守コストの削減**: 統制違反を Level 1 で自動修正できる
- **拡張の予測可能性**: 新規追加の手順が明確
- **導入者への親切**: 統制語彙を Framework が提供することで、導入体験が向上

## 4 Categories

### 1. `type`

- **性質**: ファイルの種類(1 ファイル 1 つ、排他的)
- **選定原則**: 
  - 保存判断フロー(ADR-0007)で明確に分類できる粒度
  - 同義語や別表現を作らない(例: `note` と `article` を別 type にしない)
  - 生成タイミングで確定できる(後付けの type 変更は避ける)
- **拡張の基準**: 既存 type で表現できない新パターンが 3 件以上蓄積された時

### 2. `status`

- **性質**: ファイルの状態(1 ファイル 1 つ)
- **選定原則**:
  - 通常 type と project_idea 用の 2 系統を分離
  - 遷移パターンを持つ(draft → wip → published → archived 等)
- **拡張の基準**: 新しい遷移パターンが必要になった時

### 3. `tags`

- **性質**: 検索・分類のためのラベル(1 ファイル 0-N 個)
- **選定原則**:
  - 技術系(実装スタックの識別)、コンテンツ系(内容の性格)、プロジェクト系、個人系、メタ系にカテゴリ分け
  - 汎用性が高いものを優先
  - 頻出するもののみ登録(1-2 回しか使わないタグは追加しない)
- **拡張の基準**: 3 ファイル以上で同じキーワードが tag として自然に浮かんでくる時

### 4. `project`

- **性質**: 該当プロジェクト(30_projects/ 配下のみ)
- **選定原則**:
  - GitHub リポジトリ名と完全一致
  - 大文字小文字を含めて厳密
- **拡張の基準**: 新規リポジトリ作成時に必ず追加

## Extension Procedure

### 新規 type の追加

1. **提案フェーズ**:
   - 既存 type で対応できない事例を 3 件以上蓄積
   - 提案する type 名と定義を vocabulary.md に記述(仮追加、コメント付き)
   - 保存判断フロー(ADR-0007)への影響を検討

2. **試行フェーズ**:
   - 実際にファイルを 3-5 件作成し、新 type で運用
   - Front Matter Schema(frontmatter-schema.md)に追加必須フィールドを追記
   - 対応する template を `00_meta/templates/<type>.md` に作成

3. **確定フェーズ**:
   - vocabulary.md の仮追加コメントを削除
   - Skill 側の判定フローに反映(SKILL.md 更新)
   - 過去ファイルへの遡及適用は不要(前方互換)

### 新規 tag の追加

- 3 件以上の使用実績が見えたらカテゴリ判定して vocabulary.md に追加
- 既存 tag と重複しないか確認(例: `dev` があるなら `development` は不要)

### 新規 project の追加

- 新規 GitHub リポジトリ作成時、即座に vocabulary.md に追加
- 30_projects/<RepoName>/ ディレクトリと project_aliases.md にも追加

### 新規 status の追加

- 稀。追加が必要な場合は必ず ADR で意思決定を記録

## Deprecation Procedure

### 廃止 type

1. **廃止宣言**:
   - vocabulary.md の該当 type にコメント `<!-- DEPRECATED as of YYYY-MM-DD, superseded by <new_type> -->` を追加
   - 新規保存で該当 type を使わないよう Skill を更新

2. **移行**:
   - 過去ファイルは残す(履歴として)
   - 検索時のヒットは維持(過去ファイルも参照可能に)

3. **削除フェーズ**(1 年以上経過後):
   - vocabulary.md から完全削除
   - Level 4 季節補正(ADR-0009)で過去ファイルの type を新 type に一括更新

### 廃止 tag

- vocabulary.md から削除
- 保守運用 Level 3(月次補正)で、過去ファイルからも該当 tag を削除(オプション)

## Violation Handling

### Level 1(保存時、Skill 自動対応)

以下の違反を Skill が自動修正:

- 大文字小文字の揺らぎ(`ChatLog` → `chat_log`)
- ハイフン・アンダースコアの揺らぎ(`chat-log` → `chat_log`)
- 未登録 tag の使用(仮対応: 登録済み類似 tag に置き換え、または警告)

### Level 2(週次バッチ、Cursor 委譲)

以下をチェック:

- vocabulary.md に未登録の type/tag/project が使われていないか
- 過去ファイルに混在する古い表記を修正

### Level 3(月次チェック、Cursor 委譲)

以下を実施:

- 統制語彙の使用頻度分析(未使用 tag、過剰使用 tag の把握)
- 新規追加候補の提案

## Relationship with Related Files

```
vocabulary.md              (実際の値定義、日々参照される)
    ↑
    │ 実装
    │
vocabulary-design.md       (このスペック、設計思想を規定)
    ↑
    │ 依存
    │
frontmatter-schema.md      (Front Matter でどう使うかを規定)
    ↑
    │ 依存
    │
SKILL.md, 各 template      (実際の使用箇所)
```

- **vocabulary-design.md**: なぜ・どう管理するかの思想(このファイル)
- **vocabulary.md**: 現在の値定義(vault 内で日々参照)
- **frontmatter-schema.md**: Front Matter でどう記述するかの規則

## References

- **関連 ADR**: なし(vocabulary は仕様として独立)
- **関連 spec**: 
  - [[./frontmatter-schema.md]](Front Matter での使用)
  - [[./file-naming.md]](type と保存先の対応)
- **実装**: `vault-templates/00_meta/vocabulary.md`(vault 内正典)

## Change Log

- 2026-07-13: 初版(統制語彙の設計思想を体系化)

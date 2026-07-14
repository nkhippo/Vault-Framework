---
audience: mixed
created: 2026-07-14T07:15:00+09:00
keywords:
  - reference-level
  - spec
  - level-0
  - level-1
  - level-2
  - level-3
  - level-4
  - prompt-caching
  - phase3.1-tools
related_adrs:
  - "0003"
  - "0014"
status: published
summary: Skill が vault を参照する際の 5 段階(Level 0、4)の詳細仕様。各レベルの発火条件、参照ファイル、キャッシュ挙動、prompt caching への配慮を規定。
tags:
  - spec
  - reference-level
  - skill
title: 参照レベルシステム 仕様
type: spec
updated: 2026-07-14T07:15:00+09:00
---

## Summary

Skill `vault-manager` が vault を参照する際の 5 段階(Level 0〜4)の詳細仕様。各レベルの発火条件、参照ファイル、キャッシュ挙動、prompt caching への配慮を規定。トークン消費の最小化と参照精度の両立を目的とする。

## Scope

このスペックが規定するもの:

- 参照レベル 0〜4 の定義と使い分け
- 各レベルの発火条件(何がトリガーか)
- 各レベルで読むべきファイルとその順序
- 同一 Chat 内でのキャッシュ挙動
- Vault-MCP Phase 3.1 ツール(get_frontmatter、search_by_keyword、get_section)の活用
- メタ指示(「vault を参照せず答えて」等)への対応

このスペックが規定しないもの:

- 個々のファイルの内容(vocabulary、templates 等の各 spec を参照)
- 保存判断フロー(ADR-0007 と guidelines/save-decision-flow.md 参照)

## Design Principle

**「明示的なトリガーがない限り Level 0(参照しない)」がデフォルト**。過剰参照はトークン消費と判定精度の両方に悪影響がある。以下の 3 原則で運用:

1. **必要最小限**: 判断に必要な情報のみを取得
2. **prompt caching への配慮**: 同一プレフィックスを維持し、キャッシュヒット率を最大化
3. **段階的深化**: 必要が生じたら 1 段階ずつ深く参照する

## Level 0: 参照しない(デフォルト)

### 発火条件

以下のすべての条件を満たす時、Level 0 を維持:

- 保存指示(「Vault に保存して」等)がない
- 参照要求(「以前の意思決定を教えて」等)がない
- 特定プロジェクト名や機能表現の言及がない
- 日記・振り返り等の意図がない

### 該当ケース(具体例)

- 純粋な雑談
- Claude が持つ一般知識で完結する質問
- 実装や仕様の技術的な一般論
- Web 検索タスク(Naoya の個人情報が不要)
- 「なんとなくの相談」で vault 参照が明示的に要らない場合

### 禁止事項

- 「vault の情報が使えるかも」という推測での自主参照は禁止
- 過去の Chat 履歴で参照されていたからと言って、今の Chat でも参照するのは禁止

### 効果

- トークン消費最小
- 応答レイテンシ最小
- prompt caching のヒット率最大

## Level 1: 最小参照(明示的トリガー時のみ)

### 発火条件

以下のいずれかで発火:

- 「Vault に保存して」「Obsidian に保存して」等の保存指示
- 保存指示の一部としてテンプレート確認が必要な時
- 日記保存フロー(diary 保存の初回時のみ `templates/diary.md` を読む)
- あいまい名解決が必要になった時

### 読むファイル(初回セッションのみ、以降キャッシュ)

固定順序で読み込む(prompt caching 対応):

1. `00_meta/vault_structure.md`
2. `00_meta/naming_conventions.md`
3. `00_meta/vocabulary.md`
4. `00_meta/frontmatter_schema.md`(必要時のみ)
5. `00_meta/project_aliases.md`(あいまい名解決時のみ)
6. `00_meta/templates/<type>.md`(保存時に該当 template のみ)

### キャッシュルール

- 同一 Chat 内で一度読んだファイルは再度読まない
- Naoya が「vault を更新した」と明示した場合のみ再取得

### Phase 3.1 ツールの活用

- 「あのファイルは何について書いてある?」判定には `get_frontmatter(path)` を使用(全文取得より 5-10x 節約)
- 大きな 00_meta ファイルの特定セクションのみ必要な時は `get_section(path, section_name)` を使用

## Level 2: プロジェクト情報を読む

### 発火条件

- ユーザーが特定プロジェクト名(正式名または通称)を明示した時
- ユーザーが機能表現でアプリを指した時(あいまい名解決フロー経由)

### 読むファイル

該当プロジェクトの主要 3 ファイル(または 4 ファイル):

1. `30_projects/<RepoName>/README.md`
2. `30_projects/<RepoName>/design-decisions.md`(存在すれば)
3. `30_projects/<RepoName>/open-questions.md`(存在すれば)
4. `30_projects/<RepoName>/handoff/current-state.md`(**Vault システム自体の相談時は最優先**)

### Vault システム相談時の優先

Vault / Vault-MCP / Vault-Framework に関する相談の場合、`handoff/current-state.md` を **最優先で読む**。理由は直近状態のスナップショットが最重要のため。

### Phase 3.1 ツールの活用

- 4 ファイル全てを読む前に、`get_frontmatter` で summary を確認し、必要なファイルを絞り込む
- 特定セクション(例: 「未解決の論点」)のみ必要な時は `get_section` を使用

## Level 3: 過去記録を検索

### 発火条件

以下のいずれかで発火:

- ユーザーが過去の意思決定を参照したい意図を示した時
- 「あの時決めたこと」「以前議論した」「過去の設計判断」等の発話
- 過去の chat_log や意思決定の検索が必要になった時

### 使うツール

以下を組み合わせて使用:

- **conversation_search**: 過去 Chat を検索(Claude Projects の内蔵ツール)
- **search_by_keyword**(Phase 3.1): vault 内のファイルを Front Matter ベースで検索
- **list_directory** + **get_file_content**: 特定ディレクトリを網羅する時

### 検索の順序

1. まず `conversation_search` で該当する過去 Chat を探す
2. Chat から関連ファイル(chat_log の path)が判明したら、`get_frontmatter` で内容の確認
3. 詳細が必要なら `get_file_content` または `get_section`
4. プロジェクト固有の情報が必要なら Level 2 に切り替え

### 除外対象

- **50_self/ 領域**: 明示的に「日記を読み返して」等と指示された時のみ発動(sensitive 扱い、詳細は ADR-0016)

## Level 4: 全文精読

### 発火条件

- ユーザーがファイルパスを明示的に指定した時
- 例: 「30_projects/Vault-MCP/design-decisions.md を全部読んで」

### 動作

- 指定ファイルを `get_file_content` で完全取得
- Front Matter とすべての本文を読む
- ページネーションが必要な場合(超長文)は Level 3 に切り替え

## メタ指示への応答

Skill は以下のメタ指示に応答する:

| ユーザーの指示 | 調整内容 |
|---|---|
| 「vault を参照せず答えて」 | この Chat 内では以降 Level 0 に固定 |
| 「vault は必要なときだけ」 | デフォルト(状況判断)に戻す |
| 「vault の情報を優先して」 | 一般知識より vault 情報を優先 |
| 「関連する過去記録を全部読んで」 | Level 3 を積極発動 |
| 「あの handoff だけ読んで」 | Level 2 で handoff/current-state.md のみ読む |

## Prompt Caching への配慮

### 固定順序の維持

Level 1 で複数の 00_meta ファイルを読む場合、常に固定順序(vault_structure → naming_conventions → vocabulary → …)を維持。順序を毎回変えると cache miss を招く。

### 会話途中の再読み込み禁止

- 一度読んだファイルは同一 Chat 内で再取得しない
- Claude の context に既に載っている前提で参照
- 例外: Naoya が「更新した」と明示した場合のみ再取得

### 保存時の順序

保存指示への対応(7 ステップ、guidelines/save-decision-flow.md 参照)は Step 1→7 の順で固定。判断に迷って前に戻ることはしない(context が肥大化し cache 効率が落ちる)。

## Level Transition Diagram

```
[会話開始]
    ↓
Level 0(参照しない、デフォルト)
    ↓  保存指示 or 参照要求
Level 1(00_meta を最小参照)
    ↓  特定プロジェクト言及
Level 2(該当プロジェクトの README + design-decisions 等)
    ↓  過去記録の参照要求
Level 3(conversation_search + search_by_keyword)
    ↓  ファイルパス明示指定
Level 4(全文精読)
```

各遷移は「必要が生じた時のみ」1 段階深く進む。逆方向の遷移(高レベルから低レベルへ戻る)は原則不要。

## Skill Implementation Notes

Skill(SKILL.md)側での実装ガイドライン:

- Level 0 の判定は「明示的トリガーの有無」で厳格に
- Level 1 の初回キャッシュは Chat 内メモリで管理(get_frontmatter で軽量取得を先に試す)
- Level 2 の Vault システム相談時は handoff を優先することを明示
- Level 3 の 50_self/ 除外は sensitive 扱いと連動

## References

- **関連 ADR**: 
  - [[../decisions/0003-skill-project-vault-3-layer.md]](Skill の役割)
  - [[../decisions/0014-sonnet-standardization-response.md]](プロンプト工夫 2 の対応)
- **関連 spec**: 
  - [[./handoff-mechanism.md]](Level 2 での handoff 参照)
  - [[./ambiguous-name-resolution.md]](Level 2 遷移の判定)
- **実装**: `skills/vault-manager/SKILL.md`(canonical)

## Change Log

- 2026-07-13: 初版(5 段階の詳細仕様確定)
- 2026-07-13: v1.1 で Level 0 の厳格化と prompt caching 対応を追加
- 2026-07-14: Phase 3.1 ツール(get_frontmatter 等)の活用を反映

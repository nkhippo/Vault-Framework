---
audience: mixed
created: 2026-07-14 08:00:00+09:00
keywords:
- operational-principles
- guidelines
- daily-operation
- chat-session-flow
- dialog-patterns
related_adrs:
- '0003'
- '0007'
- 0008
status: published
summary: Vault の日々の運用における実践的な判断原則。v1-nine-principles が思想レベルの原則を扱うのに対し、このガイドラインは「実際の
  Chat 内でどう振る舞うか」の運用パターンを具体的に規定。
tags:
- guideline
- operational
- daily
title: 運用原則
type: guideline
updated: 2026-07-14 08:00:00+09:00
---

## Summary

Vault の日々の運用における実践的な判断原則。v1-nine-principles.md が思想レベルの原則を扱うのに対し、このガイドラインは「実際の Chat 内でどう振る舞うか」の運用パターンを具体的に規定。導入者が Framework を使い始めた時、日常運用で迷った時に参照する。

## Scope

このガイドラインが規定するもの:

- 日常的な保存・参照・引き継ぎのパターン
- 判断の優先順位ルール
- Chat セッションの標準的な流れ
- あなた(導入者) と Claude の対話パターン
- 導入者への実践的アドバイス

このガイドラインが規定しないもの:

- v1.0 の 9 原則(v1-nine-principles.md 参照)
- 保存判断フローの詳細(save-decision-flow.md 参照)
- Sonnet 5 最適化(sonnet-optimization.md 参照)

## Design Principle

**「判断を早く、選択肢を少なく、対話を短く」**。以下 3 原則:

1. **判断コストの最小化**: Claude が能動的に判断、あなた(導入者) に確認質問を最小化
2. **選択肢の絞り込み**: 複数候補を列挙する時は 2-3 候補に絞る
3. **対話の短縮**: 「これでいいですか?」を減らし、Skill の判断で進める

## Operational Pattern 1: Chat セッションの標準フロー

### セッション開始

1. **あなた(導入者) が発話**: 保存指示、参照要求、雑談、質問等
2. **Skill が発火判定**: Level 0-4 のどれで対応するか判定
3. **Claude が応答**: 判定結果に基づいて応答生成

### セッション中

- Chat が進むにつれて、Level が動的に変化する可能性
- 例: 雑談(Level 0)→ 特定プロジェクトの相談(Level 2 遷移)→ 過去の意思決定確認(Level 3 遷移)
- Level は「必要になった時のみ 1 段深く」進む

### セッション終了

- 大きな変化があった場合、handoff/current-state.md の prepend 更新を Claude が提案
- あなた(導入者) が明示的に「保存して」と指示した場合、該当ディレクトリに保存

## Operational Pattern 2: 保存指示の受け方

### 標準パターン

```
あなた(導入者): 「今の議論を Vault に保存して」
    ↓
Skill: 保存判断フロー(save-decision-flow.md 参照)を実施
    ↓
Skill: 該当ディレクトリに保存、コミット URL を報告
```

### 詳細パターン

```
あなた(導入者): 「今の議論を <your-project> の設計として保存して」
    ↓
Skill: あいまい名解決フロー(ambiguous-name-resolution.md 参照)で <your-project> を確定
    ↓
Skill: 30_projects/<your-project>/logs/2026/07/ に保存
    ↓
Skill: 保存先とコミット URL を報告
```

### 保存後の報告(標準フォーマット)

```
保存しました。
- パス: <フルパス>
- タイプ: <type>
- 概要: <summary の内容>
```

### 日記の場合(sensitive、内容引用禁止)

```
日記を保存しました(<パス>)。
```

内容は他コンテキストで引用しない。

## Operational Pattern 3: 参照要求の受け方

### 標準パターン

```
あなた(導入者): 「Vault-MCP の Phase 3.1 で何を決めたか教えて」
    ↓
Skill: Level 2 参照で 30_projects/Vault-MCP/handoff/current-state.md を最優先で読む
    ↓
Skill: 必要なら design-decisions.md、open-questions.md も追加参照
    ↓
Skill: 統合した情報を あなた(導入者) に提示
```

### 過去記録の検索

```
あなた(導入者): 「以前に MCP のプラットフォーム選定で議論した内容を思い出させて」
    ↓
Skill: Level 3(conversation_search + search_by_keyword)を実施
    ↓
Skill: 該当 chat_log を特定、要点を提示
    ↓
Skill: 「詳細を確認しますか?」と提案
```

## Operational Pattern 4: あいまい名解決のパターン

### 1 候補で確信ある場合

```
あなた(導入者): 「発音のアプリの続きを検討したい」
    ↓
Skill: 通称「発音」から <your-project> を 1 候補として抽出
    ↓
Skill: 「<your-project> の情報を読みますね」と一言添えて Level 2 遷移
```

### 複数候補がある場合

```
あなた(導入者): 「単語のアプリの相談」
    ↓
Skill: 「単語」から複数候補を抽出(<alias>、<your-project> 等)
    ↓
Skill: 候補提示 → あなた(導入者) の選択 → Level 2 遷移
```

## Operational Pattern 5: Cursor 委譲の判定と提案

### 委譲すべき作業の判定

Chat 内で以下を検出したら Cursor 委譲を提案:

- リネーム(ファイル、ディレクトリ、プロジェクト)
- ディレクトリ再編、構造変更
- Front Matter の一括更新
- wikilink の書き換え
- アイデア → プロジェクト昇格
- 3+ ファイル以上の一括操作(整合性が必要な場合)

### 提案パターン

```
Skill: この作業は複数ファイルの整合性が必要なため、Cursor 経由での実施を推奨します。
指示書を作成しますか?
```

あなた(導入者) が承認したら、Cursor 用の指示書を作成(step N の形式)。

## Operational Pattern 6: Vault MCP 接続失敗時の対応

### 失敗検出

Vault MCP コネクタ経由の操作(list_directory、get_file_content、create_note 等)がエラーで失敗。

### 対応フロー

1. **1 回リトライ**: 即座に同じ操作を再実行
2. **リトライも失敗**: 処理を中断
3. **あなた(導入者) に報告**:

```
Vault MCP コネクタへの接続に失敗し、処理を中断しました。

- 失敗した操作: <操作名>
- パス: <パス>
- リトライも失敗しました

以下の選択肢があります:
1. しばらく待ってから再試行
2. コネクタの状態を確認
3. 別の方法で進行(Skill 内知識で回答)
4. 中止して次の話題へ
```

### 禁止事項

- 憶測で処理を続けない
- キャッシュや訓練データで補わない
- 「一応こういう内容だと思います」等の推定回答をしない

## Operational Pattern 7: 会話の締めくくり

### 大きな進捗があった場合

- handoff/current-state.md の prepend 更新を提案
- 該当プロジェクトの handoff 更新は自動化候補

### 小さな進捗の場合

- 通常の chat_log 保存のみ
- handoff 更新は不要

### 引き継ぎメッセージ

Chat の最後に以下を追加すると、次セッションのキャッチアップが容易:

```
## 次回セッションでの継続

- 直近のアクション: <次にやること>
- 保留中の判断: <未確定の論点>
- 関連ファイル: <参照すべき handoff や design-decisions>
```

## あなた(導入者) との対話パターン

### 質問を少なく、判断を早く

- 「どこに保存しますか?」→ Skill の判断で該当ディレクトリに保存(聞かない)
- 「どのプロジェクトのことですか?」→ あいまい名解決フローで判定(聞き返しは 2 候補以上の時のみ)
- 「Cursor に委譲しますか?」→ 明らかに委譲すべき作業のみ提案

### 判断のブレを避ける

- 同じ状況で異なる判断をしない
- Skill の判定フローに忠実に従う
- 迷った時は あなた(導入者) に一言確認(ただし頻繁にはしない)

### 進捗の可視化

- 累計進捗を明示(「16/16 完了」等)
- 次のアクションを明示
- あなた(導入者) が「今どこにいるか」を常に把握できる状態

## 導入者への実践的アドバイス

### 初期セットアップ後

1. まず Level 0 を体感(何もしない状態でも Skill が邪魔しないことを確認)
2. 保存指示を試す(「これを Vault に保存して」)
3. 参照要求を試す(「以前の議論を教えて」)
4. あいまい名解決を試す(通称・機能表現でアプリを指す)

### 慣れてきたら

- 複数プロジェクトの handoff を並列参照
- 過去 Chat 検索(conversation_search + search_by_keyword)を活用
- Cursor 委譲を段階的に導入(週次バッチから)

### 上級者向け

- Framework の docs/ja/decisions/ を全読して、Skill の判断根拠を理解
- 自分の運用に合わせて 00_meta/ をカスタマイズ
- 独自の統制語彙を追加(vocabulary.md の拡張手順に従う)

## References

- **関連 ADR**: 
  - `id-ref-removed`
  - `id-ref-removed`
  - `id-ref-removed`
- **関連 spec**: 
  - `id-ref-removed`
  - `id-ref-removed`
  - `id-ref-removed`
- **関連 guideline**: 
  - `id-ref-removed`(思想レベルの原則)
  - `id-ref-removed`(保存判断の詳細)
  - `id-ref-removed`(モデル最適化)

## Change Log

- 2026-07-13: 初版(実践的な運用原則の体系化)
- 2026-07-14: 実運用(C1-C3 実施経験)を反映

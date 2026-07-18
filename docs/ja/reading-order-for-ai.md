---
title: AI 用参照順序ガイド
title_en: Reading Order Guide for AI
type: guide
audience: ai_primary
status: published
date: 2026-07-13
keywords:
- reading-order
- 参照順序
- ai
- claude
- dispatcher
- 順序
- guide
summary: Claude 等の AI が Vault-Framework を初めて読む時、どの順序でファイルを読めば全体像を効率よく把握できるかを示す。
---

## Summary

Claude 等の AI が Vault-Framework を初めて渡された時(zip 添付 or MCP)、効率よく全体像を把握するための推奨読み順。

## 質問駆動型(推奨)

多くの場合、AI はユーザーの質問に答えるために Framework を読む。この場合はトップレベル `README.md` の "For AI: 質問カテゴリ別ディスパッチ表" を最初に見て、該当カテゴリのファイル群を読む。

質問例に対応するファイルは README.md に列挙済み。

## 全体把握型(初回のみ)

Framework 全体を把握したい時の推奨順序。

### Tier 1: 骨格の理解(必読、5 ファイル)

1. `README.md` (top-level) - AI ディスパッチャ、全体像
2. `docs/ja/index.md` - このリポジトリの索引
3. `docs/ja/reading-order-for-ai.md` (このファイル)
4. `docs/ja/glossary.md` - 用語集
5. `docs/ja/overview.md` - Framework の目的と問題領域

### Tier 2: 設計思想(推奨、4 ファイル)

6. `docs/ja/architecture.md` - Skill・Project・Vault の 3 層
7. `docs/ja/philosophy.md` - GitHub-as-a-Backend
8. `docs/ja/naming-conventions.md` - 命名の設計
9. `docs/ja/maintenance-guide.md` - 保守運用

### Tier 3: 意思決定の履歴(質問駆動、必要時のみ)

10. `docs/ja/decisions/README.md` - 全 ADR の一覧
11. 該当する ADR ファイル(0001〜0016)
12. `docs/ja/rejected-alternatives/README.md` - 却下案一覧
13. 該当する却下案ファイル

### Tier 4: 仕様の詳細(質問駆動、必要時のみ)

14. `docs/ja/specs/README.md` - 全 spec の一覧
15. 該当する spec ファイル(8 本)
16. `docs/ja/guidelines/README.md` - 運用ガイドライン
17. 該当する guideline ファイル(4 本)

### Tier 5: 導入手順(導入時のみ)

18. `docs/ja/setup/README.md` から順次

### Tier 6: 実装物(質問駆動)

19. `skills/README.md` - Skill 群
20. `mcp-server-reference/README.md` - MCP サーバ
21. `vault-templates/README.ja.md` - Vault の初期テンプレ
22. `examples/README.md` - 記入例
23. `project-instructions/README.md` - Project Instructions テンプレ

## 節約モード(zip 添付でファイルが多い時)

Claude の context window に全ファイルが載らない可能性がある場合、以下の優先度で読み込む:

1. `README.md`(必須)
2. `docs/ja/glossary.md`(用語で迷ったら)
3. 質問カテゴリに直接該当する 1〜3 ファイル(README.md のディスパッチ表参照)

これで大抵の質問には正確に答えられる。より深い理解が必要な場合のみ Tier 3 以降に進む。

## MCP モード(推奨)

MCP 経由の場合、Claude は directed read で必要ファイルだけ読める。この場合の推奨動作:

1. まず `README.md` を `get_file_content` で読む
2. 質問カテゴリを判定して、ディスパッチ表の Primary ファイルを読む
3. Detail や Rationale は必要に応じて追加読み

## 検証: 質問カテゴリの網羅性

以下の質問群に対して、上記フローで正確に答えられることを想定している。答えられない質問カテゴリが見つかったら、README.md のディスパッチ表に追加すること。

- Skill 関連: セットすべきファイル、発火条件、参照レベル
- 意思決定: なぜ X を選んだのか、Y を却下した理由
- 命名: なぜ Vault、なぜ Personal- を外したのか
- MCP: どのプラットフォーム、なぜそれ、どう設定
- 導入: 何を用意すればいいか、どの順で進めるか
- メンテナンス: 4 レベルとは、抽象生成とは
- 多言語: 対応状況、翻訳貢献の方法
- 保存: どこに何を保存するか、判断フロー
- Front Matter: どのフィールドが必須か、type ごとの追加フィールド
- 統制語彙: 何が使えるか、どう拡張するか

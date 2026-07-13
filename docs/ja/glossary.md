---
title: 用語集
title_en: Glossary
type: glossary
audience: mixed
status: published
date: 2026-07-13
keywords: [glossary, 用語集, terminology, vault, mcp, skill, project, handoff, capture, adr, spec]
summary: Vault-Framework で使われる用語の定義集。混同しやすい用語(Vault、vault、Vault リポジトリ等)の区別も明確化。
---

## Summary

Vault-Framework で使われる用語の定義集。特に、大文字小文字で意味が変わる用語や、複数の意味を持つ用語の区別を明確にする。

## 主要用語

### Vault(大文字)

Naoya の個人 GitHub リポジトリ `nkhippo/Vault` を指す固有名詞。または、この Framework 全体の内部呼称。

### vault(小文字)

一般名詞としての「知識を蓄積する場所」の意味。文脈により Vault(大文字)と互換的に使われる場合もあるが、原則: リポジトリ名を明示する時は Vault、概念を語る時は vault。

### Vault-MCP

MCP サーバ実装のリポジトリ名(`nkhippo/Vault-MCP`)。ハイフン区切り。

### Vault MCP(スペース区切り)

Claude Pro Connectors 上に表示される MCP コネクタの名前。同じ実体を指すが、UI 表示形式のため区切り文字が異なる。

### Vault-Framework

この Framework 自体のリポジトリ名(`nkhippo/Vault-Framework`)。

### Skill

Claude のアカウント単位で登録される振る舞い規約。SKILL.md ファイルを Claude Settings > Skills からアップロードする。

- `vault-manager`: vault への保存判断、参照判断、あいまい名解決を担当
- `vault-maintainer`: 保守運用(4 レベル運用の実行、抽象生成)を担当(将来分離予定)

### Project(Claude Projects)

Claude UI 上の「プロジェクト」機能。特定用途の Chat を集約するコンテナ。Vault Project は「Vault」という Project を指す。

### Project Instructions

Claude Projects の Instructions フィールド。Vault-Framework の運用では「激薄 Instructions」方針で、実質的なルールは vault の `project_instructions_vault.md` に集約する。

### MCP(Model Context Protocol)

Anthropic 主導の、AI モデルと外部ツールをつなぐプロトコル。ここでは Cloudflare Workers 上に実装した MCP サーバを Claude Pro Connectors 経由で接続する。

### handoff

Chat 間・セッション間の引き継ぎに特化した領域。`30_projects/<RepoName>/handoff/` 配下に配置。`current-state.md` が代表的なファイル。

### capture

vault のトップレベルディレクトリ `10_captures/` に配置される、生の入力データ。将来 `10_chat_logs/` から改名予定。discussions/、quick-thoughts/、external-inputs/ にサブ分類。

### ADR (Architecture Decision Record)

意思決定の記録。`docs/ja/decisions/` 配下に個別ファイルで管理。番号(0001, 0002, ...)で識別。

### spec(仕様)

Vault-Framework が定義する各種仕様の詳細記述。`docs/ja/specs/` 配下。Front Matter スキーマ、統制語彙、参照レベル等。

### rejected alternative(却下案)

検討したが採用しなかった選択肢の記録。`docs/ja/rejected-alternatives/` 配下。「なぜこれではダメだったか」を残すことで、将来の議論の重複を防ぐ。

### guideline(運用ガイドライン)

日々の運用における判断基準の集約。`docs/ja/guidelines/` 配下。9 原則、動作原則、Sonnet 対応、保存判断フロー等。

### Fine-grained PAT

GitHub Personal Access Token の細粒度版。特定リポジトリの特定権限のみに絞れる。Vault-MCP では `nkhippo/Vault` の Contents R/W 限定で運用。

### Front Matter

Markdown ファイル冒頭の YAML メタデータブロック。Vault では type / status / tags / summary / keywords 等を含む。

### 統制語彙(vocabulary)

Front Matter の tags 等で使用可能な語彙を制限する仕組み。`00_meta/vocabulary.md` に定義。

### 参照レベル 5 段階

Claude が vault をどこまで深く参照するかの 5 段階。0(参照しない)〜 4(全文精読)。詳細は `docs/ja/specs/reference-level-system.md`。

### 保守運用 4 レベル

vault の保守運用における 4 段階のレベル分け。詳細は `docs/ja/specs/maintenance-four-levels.md`。

### 抽象生成

具体的な chat_log から、より抽象的な spec や ADR を生成する運用。定期実施を想定。詳細は `docs/ja/specs/abstract-generation.md`。

### GitHub-as-a-Backend

「Obsidian ブランドを使わず、実態としては GitHub リポジトリを Markdown 置き場として使う」思想。Vault の設計の根幹。詳細は `docs/ja/philosophy.md`。

## Skill と Project と Vault の 3 層構造

- **Skill**: Claude アカウント全体で発火する振る舞い規約(ユーザーごと)
- **Project**: Claude Projects 単位で発火する Instructions(用途ごと)
- **Vault**: GitHub リポジトリ上のドキュメントと Front Matter(データと詳細ルール)

詳細は `docs/ja/architecture.md` と `docs/ja/decisions/0003-skill-project-vault-3-layer.md`。

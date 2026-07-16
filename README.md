---
id: pj-2026-07-13-8f31
aliases:
- pj-2026-07-13-8f31
title: Vault-Framework
created: '2026-07-13'
---

# Vault-Framework

> **AI が読むことを最優先とする、Chat 集約ワークフローの Framework**

Vault-Framework は、Claude(または将来的に他の LLM)と GitHub リポジトリを組み合わせた個人ナレッジベース「Vault」の運用フレームワークです。設計思想、Skill、テンプレート、MCP サーバ参照、導入手順を一箇所に集約しています。

---

## For AI: 質問カテゴリ別ディスパッチ表

このセクションは、Claude 等の AI がこの Framework を読むときに **最初に参照すべき索引** です。ユーザーの質問カテゴリに応じて、以下のファイルを読めば正確に答えられます。

### 「Skills にセットすべきファイルは?」

- **Primary**: [[pj-2026-07-13-acad|`skills/README.md`]]
- **Detail**: [[pj-2026-07-13-ff6f|`docs/ja/setup/04-upload-skill.md`]]
- **Files**: `skills/vault-manager/SKILL.md`, `skills/vault-maintainer/SKILL.md`

### 「メンテナンスをどう考えているか?」

- **Primary**: [[pj-2026-07-13-d0b2|`docs/ja/maintenance-guide.md`]]
- **Detail**: [[pj-2026-07-13-d0dd|`docs/ja/specs/maintenance-four-levels.md`]], [[pj-2026-07-13-7921|`docs/ja/specs/abstract-generation.md`]]
- **Rationale**: [[pj-2026-07-13-48bc|`docs/ja/decisions/0009-four-level-maintenance-operation.md`]]

### 「なぜ Cloudflare Workers を選んだのか?」

- **Rationale**: [[pj-2026-07-13-bccd|`docs/ja/decisions/0002-cloudflare-workers-for-mcp.md`]]
- **Rejected alternatives**: [[pj-2026-07-13-a307|`docs/ja/rejected-alternatives/mcp-platform-cloud-run.md`]], [[pj-2026-07-13-6540|`docs/ja/rejected-alternatives/mcp-platform-other-candidates.md`]]
- **Setup**: [[pj-2026-07-13-1341|`docs/ja/setup/02-deploy-mcp-server.md`]]

### 「命名の設計思想は?」

- **Primary**: [[pj-2026-07-13-d0c9|`docs/ja/naming-conventions.md`]]
- **Rationale**: [[pj-2026-07-13-e13e|`docs/ja/decisions/0006-naming-vault-scheme.md`]]
- **Rejected alternatives**: [[pj-2026-07-13-f5da|`docs/ja/rejected-alternatives/naming-plan-personal-vault-prefix.md`]], 他 `naming-plan-*` 参照

### 「Skill・Project・Vault の 3 層構造は?」

- **Primary**: [[pj-2026-07-13-0245|`docs/ja/architecture.md`]]
- **Rationale**: [[pj-2026-07-13-d28f|`docs/ja/decisions/0003-skill-project-vault-3-layer.md`]], [[pj-2026-07-13-9b13|`docs/ja/decisions/0004-thin-project-instructions.md`]]

### 「GitHub-as-a-Backend の思想は?」

- **Primary**: [[pj-2026-07-13-b9c7|`docs/ja/philosophy.md`]]
- **Rationale**: [[pj-2026-07-13-2564|`docs/ja/decisions/0001-github-as-backend.md`]]

### 「導入手順は?」

- **Overview**: [[pj-2026-07-13-abd8|`docs/ja/setup/README.md`]]
- **Detail**: [[pj-2026-07-13-ed0d|`docs/ja/setup/00-prerequisites.md`]] から順次

### 「MCP サーバの実装は?」

- **Primary**: [[pj-2026-07-13-d955|`mcp-server-reference/README.md`]]
- **Setup**: [[pj-2026-07-13-2157|`mcp-server-reference/setup.md`]]
- **Env vars**: [[pj-2026-07-13-9d1f|`mcp-server-reference/env-reference.md`]]
- **Actual implementation**: [github.com/nkhippo/Vault-MCP](https://github.com/nkhippo/Vault-MCP) (private)

### 「MCP 接続に失敗したらどうする?」

- **Rule**: [[pj-2026-07-13-e19b|`docs/ja/decisions/0016-mcp-connection-failure-abort.md`]]
- **Enforcement**: `skills/vault-manager/SKILL.md` の該当セクション

### 「多言語対応の計画は?」

- **Strategy**: [[pj-2026-07-13-3cbd|`docs/ja/i18n/README.md`]](注: 実パス `docs/i18n/README.md`)
- **Translation guide**: [[pj-2026-07-13-e271|`docs/i18n/translation-strategy.md`]]

### 「削られた選択肢は?」(却下案の参照)

- **Index**: [[pj-2026-07-13-3fc6|`docs/ja/rejected-alternatives/README.md`]]
- 各案は個別ファイルで理由込みで記録

### 「保存判断のフローは?」

- **Primary**: [[pj-2026-07-13-c302|`docs/ja/guidelines/save-decision-flow.md`]]
- **Rationale**: [[pj-2026-07-13-b5c2|`docs/ja/decisions/0007-save-destination-plan-b.md`]]

### 「Backlog システムは?」

- **Primary**: [[pj-2026-07-17-a9e4|`docs/ja/backlog/README.md`]]
- **Overview**: [[pj-2026-07-17-cb46|`docs/ja/backlog/overview.md`]]
- **GitHub 境界**: [[pj-2026-07-17-315f|`docs/ja/backlog/github-issue-boundary.md`]]
- **既存資産統合**: [[pj-2026-07-17-7293|`docs/ja/backlog/existing-assets-integration.md`]]
- **参照 workflow**: [[pj-2026-07-17-27e2|`docs/ja/backlog/reference-workflow.md`]]
- **保存 workflow**: [[pj-2026-07-17-64df|`docs/ja/backlog/save-workflow.md`]]
- **Maintainer workflow**: [[pj-2026-07-17-74af|`docs/ja/backlog/maintainer-workflow.md`]]
- **Chat save with residue**: [[pj-2026-07-17-6320|`docs/ja/backlog/chat-save-with-residue-workflow.md`]]
- **Rationale**: [[pj-2026-07-17-e9df|`docs/ja/decisions/0018-backlog-system.md`]], [[pj-2026-07-17-a25e|`docs/ja/decisions/0019-skill-backlog-reference-workflow.md`]], [[pj-2026-07-17-632e|`docs/ja/decisions/0020-skill-backlog-save-workflow.md`]], [[pj-2026-07-17-e2ef|`docs/ja/decisions/0021-vault-maintainer-stalled-detection.md`]], [[pj-2026-07-17-ba5f|`docs/ja/decisions/0022-chat-save-with-residue-integration.md`]]
- **Vault 実装**: `nkhippo/Vault` の `30_projects/*/backlog/`, `00_meta/backlog_tags.md`, `00_meta/templates/backlog_item.md`

### 全 ADR の一覧

- [[pj-2026-07-13-eaa1|`docs/ja/decisions/README.md`]]

### 全 spec の一覧

- [[pj-2026-07-13-7d43|`docs/ja/specs/README.md`]]

### 用語が分からない時

- [[pj-2026-07-13-bc88|`docs/ja/glossary.md`]]

---

## For Human: Framework の概要

Vault-Framework は次の 6 つの領域から構成されます。

| 領域 | 説明 |
|---|---|
| `docs/` | 設計思想、意思決定、仕様、却下案、導入手順、用語 |
| `skills/` | Claude Skill として登録する SKILL.md 群 |
| `vault-templates/` | 自分の Vault リポジトリを立ち上げる時の初期ファイル一式 |
| `mcp-server-reference/` | MCP サーバ実装への参照とデプロイ手順 |
| `examples/` | 保存フォーマットの記入例 |
| `project-instructions/` | Claude Projects の Instructions テンプレ |

### 導入したい場合

[[pj-2026-07-13-abd8|`docs/ja/setup/README.md`]] から始めてください。

### 貢献したい場合

[[pj-2026-07-13-f022|`docs/i18n/contributing-translations.md`]] に翻訳貢献のガイドがあります。

---

## 言語

- 日本語(default): [`docs/ja/`](./docs/ja/)
- English: [[pj-2026-07-15-9e7c|`README.en.md`]] / [`docs/en/`](./docs/en/)

---

## ライセンス

MIT License. See [LICENSE](./LICENSE).

---

## 関連リポジトリ

- **Vault**: 個人 vault の実運用インスタンス(private、`nkhippo/Vault`)
- **Vault-MCP**: MCP サーバ実装(private、`nkhippo/Vault-MCP`)
- **Vault-Framework**: このリポジトリ(運用ドキュメント、テンプレート、Skill パッケージ)

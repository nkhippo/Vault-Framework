# Vault-Framework

> **AI が読むことを最優先とする、Chat 集約ワークフローの Framework**

Vault-Framework は、Claude(または将来的に他の LLM)と GitHub リポジトリを組み合わせた個人ナレッジベース「Vault」の運用フレームワークです。設計思想、Skill、テンプレート、MCP サーバ参照、導入手順を一箇所に集約しています。

---

## For AI: 質問カテゴリ別ディスパッチ表

このセクションは、Claude 等の AI がこの Framework を読むときに **最初に参照すべき索引** です。ユーザーの質問カテゴリに応じて、以下のファイルを読めば正確に答えられます。

### 「Skills にセットすべきファイルは?」

- **Primary**: [`skills/README.md`](./skills/README.md)
- **Detail**: [`docs/ja/setup/04-upload-skill.md`](./docs/ja/setup/04-upload-skill.md)
- **Files**: `skills/vault-manager/SKILL.md`, `skills/vault-maintainer/SKILL.md`

### 「メンテナンスをどう考えているか?」

- **Primary**: [`docs/ja/maintenance-guide.md`](./docs/ja/maintenance-guide.md)
- **Detail**: [`docs/ja/specs/maintenance-four-levels.md`](./docs/ja/specs/maintenance-four-levels.md), [`docs/ja/specs/abstract-generation.md`](./docs/ja/specs/abstract-generation.md)
- **Rationale**: [`docs/ja/decisions/0009-four-level-maintenance-operation.md`](./docs/ja/decisions/0009-four-level-maintenance-operation.md)

### 「なぜ Cloudflare Workers を選んだのか?」

- **Rationale**: [`docs/ja/decisions/0002-cloudflare-workers-for-mcp.md`](./docs/ja/decisions/0002-cloudflare-workers-for-mcp.md)
- **Rejected alternatives**: [`docs/ja/rejected-alternatives/mcp-platform-cloud-run.md`](./docs/ja/rejected-alternatives/mcp-platform-cloud-run.md), [`docs/ja/rejected-alternatives/mcp-platform-other-candidates.md`](./docs/ja/rejected-alternatives/mcp-platform-other-candidates.md)
- **Setup**: [`docs/ja/setup/02-deploy-mcp-server.md`](./docs/ja/setup/02-deploy-mcp-server.md)

### 「命名の設計思想は?」

- **Primary**: [`docs/ja/naming-conventions.md`](./docs/ja/naming-conventions.md)
- **Rationale**: [`docs/ja/decisions/0006-naming-vault-scheme.md`](./docs/ja/decisions/0006-naming-vault-scheme.md)
- **Rejected alternatives**: [`docs/ja/rejected-alternatives/naming-plan-personal-vault-prefix.md`](./docs/ja/rejected-alternatives/naming-plan-personal-vault-prefix.md), 他 `naming-plan-*` 参照

### 「Skill・Project・Vault の 3 層構造は?」

- **Primary**: [`docs/ja/architecture.md`](./docs/ja/architecture.md)
- **Rationale**: [`docs/ja/decisions/0003-skill-project-vault-3-layer.md`](./docs/ja/decisions/0003-skill-project-vault-3-layer.md), [`docs/ja/decisions/0004-thin-project-instructions.md`](./docs/ja/decisions/0004-thin-project-instructions.md)

### 「GitHub-as-a-Backend の思想は?」

- **Primary**: [`docs/ja/philosophy.md`](./docs/ja/philosophy.md)
- **Rationale**: [`docs/ja/decisions/0001-github-as-backend.md`](./docs/ja/decisions/0001-github-as-backend.md)

### 「導入手順は?」

- **Overview**: [`docs/ja/setup/README.md`](./docs/ja/setup/README.md)
- **Detail**: [`docs/ja/setup/00-prerequisites.md`](./docs/ja/setup/00-prerequisites.md) から順次

### 「MCP サーバの実装は?」

- **Primary**: [`mcp-server-reference/README.md`](./mcp-server-reference/README.md)
- **Setup**: [`mcp-server-reference/setup.md`](./mcp-server-reference/setup.md)
- **Env vars**: [`mcp-server-reference/env-reference.md`](./mcp-server-reference/env-reference.md)
- **Actual implementation**: [github.com/nkhippo/Vault-MCP](https://github.com/nkhippo/Vault-MCP) (private)

### 「MCP 接続に失敗したらどうする?」

- **Rule**: [`docs/ja/decisions/0016-mcp-connection-failure-abort.md`](./docs/ja/decisions/0016-mcp-connection-failure-abort.md)
- **Enforcement**: `skills/vault-manager/SKILL.md` の該当セクション

### 「多言語対応の計画は?」

- **Strategy**: [`docs/ja/i18n/README.md`](./docs/i18n/README.md)(注: 実パス `docs/i18n/README.md`)
- **Translation guide**: [`docs/i18n/translation-strategy.md`](./docs/i18n/translation-strategy.md)

### 「削られた選択肢は?」(却下案の参照)

- **Index**: [`docs/ja/rejected-alternatives/README.md`](./docs/ja/rejected-alternatives/README.md)
- 各案は個別ファイルで理由込みで記録

### 「保存判断のフローは?」

- **Primary**: [`docs/ja/guidelines/save-decision-flow.md`](./docs/ja/guidelines/save-decision-flow.md)
- **Rationale**: [`docs/ja/decisions/0007-save-destination-plan-b.md`](./docs/ja/decisions/0007-save-destination-plan-b.md)

### 全 ADR の一覧

- [`docs/ja/decisions/README.md`](./docs/ja/decisions/README.md)

### 全 spec の一覧

- [`docs/ja/specs/README.md`](./docs/ja/specs/README.md)

### 用語が分からない時

- [`docs/ja/glossary.md`](./docs/ja/glossary.md)

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

[`docs/ja/setup/README.md`](./docs/ja/setup/README.md) から始めてください。

### 貢献したい場合

[`docs/i18n/contributing-translations.md`](./docs/i18n/contributing-translations.md) に翻訳貢献のガイドがあります。

---

## 言語

- 日本語(default): [`docs/ja/`](./docs/ja/)
- English: [`README.en.md`](./README.en.md) / [`docs/en/`](./docs/en/)

---

## ライセンス

MIT License. See [LICENSE](./LICENSE).

---

## 関連リポジトリ

- **Vault**: 個人 vault の実運用インスタンス(private、`nkhippo/Vault`)
- **Vault-MCP**: MCP サーバ実装(private、`nkhippo/Vault-MCP`)
- **Vault-Framework**: このリポジトリ(運用ドキュメント、テンプレート、Skill パッケージ)

---
keywords:
  - changelog
  - versioning
  - semver
  - release-notes
  - framework
status: published
summary: Vault-Framework の変更履歴。Keep a Changelog 形式、SemVer 準拠。v1.0.0 初回安定版の統合エントリ。
tags:
  - framework
  - changelog
  - versioning
  - release-notes
title: Vault-Framework CHANGELOG
type: knowledge
created: 2026-07-18T12:52:43+09:00
updated: 2026-07-18T23:00:00+09:00
---

このプロジェクトの注目すべき変更を記録します。

書式は [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 準拠、[Semantic Versioning](https://semver.org/spec/v2.0.0.html) 準拠。

## [1.0.0] — 2026-07-18

Vault-Framework の初回安定版リリース。

Claude と、GitHub 上の個人ナレッジベースを一つのシステムとして運用するためのフレームワーク。Chat 履歴の自動保存、過去議論の参照、backlog の明示管理、初期認識合わせセッション、handoff 引き継ぎ機能、Vault メンテナンス機能、AI-guided setup、maintainer 向け upstream ガイドまで完備。

### Included

**アーキテクチャ**:
- 3 層構造(Claude Skills / Vault-MCP on Cloudflare Workers / GitHub Vault)
- Front Matter 二層戦略(staging と public の非対称扱い、id / aliases / project の適切な strip)

**Claude Skills**:
- `vault-manager`: Vault の使い方を Claude に教える。case 1〜5 分類、ID scheme、保存判断、参照判断、あいまい名解決、Phase 0.0(初期セットアップ検知)、handoff 保存時の再会テンプレ出力
- `vault-maintainer`: Level 1〜4 のメンテナンス粒度、stalled detection

**vault-templates**(adopter の Vault 初期骨格):
- `00_meta/vocabulary.md`: 統制語彙(type / status / kind / state / assignee / tag)
- `00_meta/backlog_tags.md`: backlog 系タグの canonical
- `00_meta/frontmatter_schema/**`: Front Matter スキーマ
- `00_meta/templates/**`: 各 type のテンプレ
- `00_meta/operations/**`: 運用共通ルール
- `00_meta/project_instructions_vault.md`: Vault Project の Instructions(SETUP.md 検知と手動キックオフの 2 通り発動)
- `00_meta/SETUP.md`: 初期セットアップ未完了マーカー(bootstrap-only)
- `.framework-version`: adopter の Vault が「どの Framework 版から初期化/更新されたか」を記録

**docs/ja/**(全ドキュメント):
- `philosophy.md`: なぜこのフレームワークを作ったか
- `architecture.md`: 全体構造の詳細
- `setup/README.md`: 7 Phase 導入 Handbook のロードマップ
- `setup/00-prerequisites.md` 〜 `setup/08-update.md`: マニュアル setup 経路の詳細
- `setup/setup-companion.md`: **AI-guided setup 用 Claude 向け対話ガイド(推奨経路)**
- `setup/canonical-vs-personal.md`: canonical / personal / hybrid / bootstrap-only 境界表、Front Matter 二層戦略
- `setup/07-initial-alignment-session.md`: Phase 7 の位置づけ
- `user-guide.md`: **導入後の日常運用ガイド**(基本操作、Chat 引き継ぎ、backlog、プロジェクト管理、メンテ、profile、Framework 更新、高度な使い方、トラブル)
- `maintainer-guide.md`: **Framework 開発者・fork 保守者向け upstream 運用ガイド**(PII マスキング A〜J、変更カテゴリ、影響ファイルマッピング、版バンプ判断、Cursor 指示書テンプレ、mirror 運用、保護すべき既存構造、「取り込んで」プロンプト対応 9 ステップ、トラブル時対応)
- `prompts/initial-alignment.md`: Phase 7 プロンプト
- `guardrails/claude-behavior.md`: Claude のガードレール
- `decisions/**`: ADR(過去の設計判断)

**mcp-server-reference/**(Vault-MCP を深く理解・拡張したい adopter 向け):
- `tools/reference.md`: 全 MCP tool API リファレンス(17 tool)
- `troubleshooting.md`: MCP サーバ側の詳細トラブルシューティング

**Landing README**:
- 導入背景と価値の説明
- AI-guided setup(推奨経路)とマニュアル setup(代替経路)の 2 経路提示
- 「何が入っているか」テーブル

### 主要な設計判断(継承)

- **SemVer 準拠**:PATCH / MINOR / MAJOR 判断基準は `docs/ja/maintainer-guide.md` §7 参照
- **PII マスキング**:個人 Vault → Framework upstream 時の genericize カテゴリ A〜J を明示
- **Skill 再アップロード**:Framework 更新後、adopter は Skill zip を手動再アップロード必要(自動更新なし)
- **保護すべき既存構造**:Skill Phase 0.0、handoff 再会テンプレ、Phase 番号体系、キックオフ検知、境界表、CHANGELOG 過去 entry 等は破壊的変更(MAJOR bump)扱い

### Migration Notes

**新規 adopter**:setup-companion.md 経由の AI-guided setup を推奨(Landing README 参照)。

**開発版から移行する adopter(Naoya 想定)**:破壊的変更なし。既存 Vault はそのまま利用可能。

[1.0.0]: https://github.com/nkhippo/Vault-Framework/releases/tag/v1.0.0

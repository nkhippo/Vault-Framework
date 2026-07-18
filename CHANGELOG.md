---
keywords:
  - changelog
  - versioning
  - semver
  - release-notes
  - framework
status: published
summary: Vault-Framework の変更履歴。Keep a Changelog 形式、SemVer 準拠。v1.0.0 初回安定版のエントリを含む。
tags:
  - framework
  - changelog
  - versioning
  - release-notes
title: Vault-Framework CHANGELOG
type: knowledge
created: 2026-07-18T12:52:43+09:00
updated: 2026-07-18T16:30:00+09:00
---

Vault-Framework の変更履歴。フォーマットは [Keep a Changelog](https://keepachangelog.com/) に準拠、バージョニングは [Semantic Versioning](https://semver.org/) に準拠する。

## バージョニング方針

- **MAJOR**: canonical 構造の破壊的変更(type / tag / schema の削除・リネーム、フォルダ構造の変更、Skill 互換性ブレイク)
- **MINOR**: 後方互換な canonical の追加(新 type / tag / template / operations / docs の追加、Skill の新機能)
- **PATCH**: バグ修正、文言修正、既存 canonical のマイナーな改善

**v1.0.0 の含意**: 初回安定版として、以降の破壊的変更は v2.0.0 として明示する SemVer 契約に入る。ただし v0.x 段階を経ずに v1.0.0 から開始しているため、初期の実運用フィードバックで破壊的変更が必要になる可能性は残る。その場合は速やかに major bump し、CHANGELOG に手動移行手順を同梱する。

## Unreleased

_(次リリースに向けた作業中の変更をここに)_

## [1.2.0] — 2026-07-18

canonical ドキュメントと canonical テンプレの拡張。破壊的変更なし、既存 adopter の運用に影響なし。

### Added

- **`vault-templates/.framework-version`** の新規追加。adopter の Vault が「どの Framework バージョンから初期化/更新されたか」を記録する 1 行テキストファイル。update 手順ステップ 0 で参照される(旧 doc では参照はあったが実ファイルが存在しなかった問題を解消)
- **`docs/ja/setup/canonical-vs-personal.md` に「Front Matter の二層戦略」節を追加**:v1.0.1 で確立された、Framework 配布層と Vault 運用層で `id` / `aliases` / `project` を非対称に扱う設計思想と、update 時の実務手順(pure canonical / hybrid の 2 パターン)を canonicalize。update フローに迷いが減る

### Changed

- **GitHub リポジトリ About**(Framework)の Description / Topics 整備。SEO / 発見性向上を目的とした更新(参照: `docs/ja/setup/canonical-vs-personal.md` の思想)
- **Vault-MCP License 統一**(別サイクル):`nkhippo/Vault-MCP` の LICENSE を ISC → MIT へ変更(Framework Landing の MIT 宣言との整合。実質同等の permissive ライセンスのため既存 fork への影響なし)。詳細は Vault-MCP CHANGELOG

### Migration Notes

v1.1.x からの update:
- **既存 adopter**: 特別な作業なし。次回 update 時に `.framework-version` ファイルをあなたの Vault ルートへコピーすれば、以降の update ステップ 0 チェックが有効になる(任意)
- **新規 adopter**: setup/01 の初期化時に vault-templates 配下から自動的にコピーされる

[1.2.0]: https://github.com/nkhippo/Vault-Framework/releases/tag/v1.2.0

## [1.1.1] — 2026-07-18

v1.1.0 直後のパッチリリース。非機能改善のみ、canonical 構造・Skill 挙動・Vault-MCP 実装への影響なし。

### Fixed

- **`mcp-server-reference/tools/reference.md` の構造修正**: `create_note` / `update_note` が誤って「Read 系」の下に配置されていた問題を修正、「Write 系」の正しい位置へ移動
- **`mcp-server-reference/tools/reference.md` の表現修正**: 存在しない `AUTO_INJECT_*` 環境変数への参照を、Vault-MCP 実装の実挙動(`ensureTimestamps` によるコード固定の自動注入)に基づく記述へ修正。`update_note` 使用例と `append` モード注意事項も併せて明確化

### Changed

- **Landing README 更新**: staging で整備された adopter 向け Landing を公開側へ反映
- **Vault-MCP リポジトリの導線レビュー**: パターン **B**(相互リンク・setup 導線・version 明示の不足)。draft PR で README 改訂を提案。License は `package.json` が ISC / Framework は MIT 表記のため統一は保留。詳細ログ: Vault staging `logs/2026/07/2026-07-18_vault-mcp-review-v1.1.1.md`(公開ミラー対象外)。Vault-MCP draft PR: https://github.com/nkhippo/Vault-MCP/pull/3

### Migration Notes

v1.1.0 からの update はドキュメントの誤り修正のみで、破壊的変更なし。adopter は特別な作業なしに v1.1.0 を継続利用可能、CHANGELOG 反映のみで OK。


## [1.1.0] — 2026-07-18

### Added

- **`mcp-server-reference/` セクション新設**: adopter が Vault-MCP を深く理解し、独自に fork/拡張できる技術リファレンス
  - `README.md`: 位置づけ、対象読者、章立て
  - `architecture.md`: Cloudflare Workers + GitHub Contents API アーキテクチャ
  - `env-vars.md`: 環境変数と Secrets の詳細
  - `tools/reference.md`: 全 17 ツール(+1 reserved)の統一フォーマット API リファレンス
  - `extending.md`: fork ベースの独自ツール追加ガイド
  - `troubleshooting.md`: 拡張トラブルシューティング

### Changed

- **`docs/ja/setup/02-deploy-mcp-server.md`**: tools/list 期待数を「8 ツール」から現行の **17**(Vault-MCP v1.6.0)へ更新、`mcp-server-reference/` への参照を追加

### Migration Notes

v1.0.x からの update は canonical ドキュメントの追加のみで、破壊的変更なし。Skill 挙動・Vault データ構造・Vault-MCP 実装への影響なし。


## [1.0.1] — 2026-07-18

v1.0.0 直後のパッチリリース。非機能改善のみ、Skill 動作・canonical 構造・API は変更なし。

### Changed

- **Skill description の汎用化**:
  - `vault-manager`: `<your-account>/Vault` placeholder を「個人 Vault(GitHub 上の Markdown リポジトリ)」に変更、「note 記事」→「執筆記事」、「Cursor 委譲」→「実装 AI 委譲」、末尾冗長文言を削除
  - `vault-maintainer`: 冒頭「Vault の…」→「個人 Vault の…」、末尾冗長文言を削除
- **examples ファイル名の汎用化**: `*_ipasounddrill.md` 等の固有名を `*_project-a.md` 等の汎用スラグへリネーム。内容内の固有名も併せて genericize
- **staging リポジトリ整備**(公開側への影響なし): 公開側にのみ存在していた ADR 0017–0024 と vault 骨格ディレクトリを staging に取り込み。次回以降のミラーが選択同期不要になる

### Fixed

- なし(挙動に影響するバグ修正なし)


## [1.0.0] — 2026-07-18

初回安定版。個人 Vault 運用(`nkhippo/Vault`)で実証された仕組みを Framework 化。

### Added

**Skill(Claude 拡張)**
- `vault-manager` v1.10 相当: id/aliases 自動付与、backlog サブシステム、chat_log / handoff / 候補抽出の 3 独立コマンド、明示 trigger、即時実行機構
- `vault-maintainer`: 週次・月次メンテナンス、リンク切れ検出、backlog stalled 検出、ADR/spec 抽象化

**vault-templates(導入者の Vault にコピーされる骨格)**
- `00_meta/vocabulary.md`: 統制語彙(type / status / tags / project / kind / state / assignee / sensitive)、`backlog_item` type、`project_readme` type
- `00_meta/backlog_tags.md`: Backlog tag のカタログと追加ルール
- `00_meta/templates/backlog_item.md`: Backlog item テンプレ
- `00_meta/frontmatter_schema/backlog_item.md`: Backlog item スキーマ
- `00_meta/profile.md`: Life Strategy と価値観の骨格
- `00_meta/project_instructions_vault.md`: Vault プロジェクト運用ルール(5 ケース構成)
- `00_meta/operations/dev_project_common.md` / `writing_project_common.md`: 開発運用型・執筆運用型プロジェクトの共通ルール骨格
- `20_notes/guides/`: note 執筆ガイド(README / writing_style / writing_process / writing_examples の 4 ファイル、骨格)

**docs(Framework の canonical ドキュメント)**
- `docs/ja/setup/00-06`: システム作業手順(Cloudflare / GitHub / Skills / MCP / Project 設定 / 初回保存テスト)
- `docs/ja/setup/07-initial-alignment-session.md`: 初期認識合わせセッション(導入者向け)
- `docs/ja/setup/08-update.md`: Framework 更新の取り込み手順
- `docs/ja/setup/canonical-vs-personal.md`: canonical / personal 境界表
- `docs/ja/setup/customization.md`: 統制語彙拡張・テンプレ追加等のカスタマイズ手順
- `docs/ja/prompts/initial-alignment.md`: Claude 実行プロンプト(Phase 7 モード)
- `docs/ja/guardrails/claude-behavior.md`: Claude カスタマイズ・ガードレール
- `docs/ja/philosophy.md` / `architecture.md` / `naming-conventions.md` / `glossary.md` / `maintenance-guide.md`: Framework の思想・構造・命名規則・語彙・メンテナンス

### Sync Mechanism(同期の仕組み)

- canonical / personal / hybrid の 3 種で領域を分類、`canonical-vs-personal.md` に集約
- update 手順を `08-update.md` に規定(zip 再アップロード / ファイル差し替え / hybrid のセクション単位マージ)
- 変更履歴を本 CHANGELOG で追跡

### Design Decisions

- **assignee フィールドの汎用化**: 個人名(`naoya`)から `owner` へ一般化。Skill・テンプレ・ドキュメント全体で統一
- **profile.md → profile.md への改名**: 個人名を含まない汎用命名。中身は導入者が記入する骨格として配布
- **note 執筆ガイドの実例分離**: 骨格(README / writing_style / writing_process)は canonical、writing_examples は枠のみ配布し実例は各自蓄積
- **初期認識合わせセッション(Phase 7)の導入**: 骨格を各自の運用に合わせるための対話セッションを Framework の正式手順に組み込み

### Known Limitations

- **英語版(en/)**: 一部のみ整備。優先順に順次追加予定
- **公開リポジトリのミラー**: `nkhippo/Vault-Framework` への push は本リリース時点では未実施(Vault repo staging に一次成果を集約)
- **導入例の実例(examples/ja/notes-guides/, examples/ja/profile.md)**: プライバシー配慮により未公開。骨格のみで使い始められる設計

### Migration Notes

初回リリースのため、移行対象なし。

---

## リンク

- 境界表: `docs/ja/setup/canonical-vs-personal.md`
- update 手順: `docs/ja/setup/08-update.md`
- Claude ガードレール: `docs/ja/guardrails/claude-behavior.md`

[1.1.1]: https://github.com/nkhippo/Vault-Framework/releases/tag/v1.1.1
[1.1.0]: https://github.com/nkhippo/Vault-Framework/releases/tag/v1.1.0
[1.0.1]: https://github.com/nkhippo/Vault-Framework/releases/tag/v1.0.1
[1.0.0]: https://github.com/nkhippo/Vault-Framework/releases/tag/v1.0.0

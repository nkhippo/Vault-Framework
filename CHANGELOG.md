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
updated: 2026-07-18T20:15:00+09:00
---

Vault-Framework の変更履歴。フォーマットは [Keep a Changelog](https://keepachangelog.com/) に準拠、バージョニングは [Semantic Versioning](https://semver.org/) に準拠する。

## バージョニング方針

- **MAJOR**: canonical 構造の破壊的変更(type / tag / schema の削除・リネーム、フォルダ構造の変更、Skill 互換性ブレイク)
- **MINOR**: 後方互換な canonical の追加(新 type / tag / template / operations / docs の追加、Skill の新機能)
- **PATCH**: バグ修正、文言修正、既存 canonical のマイナーな改善

**v1.0.0 の含意**: 初回安定版として、以降の破壊的変更は v2.0.0 として明示する SemVer 契約に入る。ただし v0.x 段階を経ずに v1.0.0 から開始しているため、初期の実運用フィードバックで破壊的変更が必要になる可能性は残る。その場合は速やかに major bump し、CHANGELOG に手動移行手順を同梱する。

## Unreleased

_(次リリースに向けた作業中の変更をここに)_

## [1.5.1] — 2026-07-18

v1.5.0 直後のパッチリリース。内部相互参照の修正のみ、既存挙動・canonical 構造・API への影響なし。

### Fixed

- **`docs/ja/maintainer-guide.md` の内部相互参照修正**: §15「保護すべき既存構造」節への内部参照(6 箇所)が、renumber 反映漏れにより `§16` を指していた問題を修正:
  - §0 Claude への発動条件
  - §4-A read-modify-write 原則の末尾
  - §7 MAJOR bump 判定条件
  - §8 Cursor 標準テンプレ「前回学びの継承」項目
  - §12 Step 3.5 保護対象の確認(§16.2 → §15.2、§16.3 → §15.3)
  - §16 更新履歴に v1.2 エントリを追加

**内容欠落なし**、既存 canonical 構造や挙動への影響なし。既存 adopter は特別な作業不要。

### Migration Notes

v1.5.0 からの update:
- **既存 adopter**: 追加作業なし
- **新規 adopter**: 変更なし(v1.5.0 と同じ手順で導入可能)
- **Framework の maintainer / fork maintainer**: maintainer-guide の内部整合性が改善。「取り込んで」プロンプト時に参照する §15 保護構造セクションが正確な相互参照で辿れるようになる

[1.5.1]: https://github.com/nkhippo/Vault-Framework/releases/tag/v1.5.1

## [1.5.0] — 2026-07-18

Framework maintainer 向け運用ガイドの新設と、既存 canonical 構造保護レイヤーの canonical 化。破壊的変更なし、adopter への影響なし。

### Added

- **`docs/ja/maintainer-guide.md`** の新設: Framework の maintainer(primary maintainer および fork maintainer)向け upstream 運用ガイド。約 750 行、16 セクション構成。以下を canonical 化:
  - 発動条件(Naoya から「取り込んで」等のプロンプトを検知した Claude が本ファイルを最優先で読む前提)
  - 全体ワークフロー(個人 Vault → 汎用化判断 → 保護対象確認 → staging → Cursor → mirror → iCloud pull)
  - 変更カテゴリ A〜I と影響ファイルマッピング(Skill / templates / vocabulary / doc / operations / instructions / meta / bug fix / breaking)
  - **PII マスキング規則 A〜J**: v1.0.1 で確立された genericize カテゴリを完全収録(Naoya / naoya / nkhippo / 実プロジェクト名 / エイリアス / 個人 URL / 価値観の断定 / 固有 wikilink / 個人エピソード / sensitive)
  - Front Matter 二層戦略(staging と public の非対称扱い)
  - 版バンプ判断基準(PATCH / MINOR / MAJOR の SemVer 準拠)
  - Cursor 指示書標準テンプレート(過去 13 個の指示書から抽出した共通構造)
  - CHANGELOG 書式(Keep a Changelog 準拠、Migration Notes の書き方)
  - mirror 運用(選択同期、rsync --delete 禁止、除外パス、iCloud pull)
  - Vault-MCP 別サイクルの扱い
  - **「取り込んで」プロンプトへの Claude 対応フロー 9 ステップ**(Step 3.5 保護対象確認を含む)
  - **§15 保護すべき既存構造**: 既存 canonical の意図しない削除を防ぐ防御レイヤー
    - メタルール:全 canonical 変更で read → diff 提示 → 承認 → 書き込みの 4 段プロセス
    - 保護対象リスト:Skill Phase 0.0 / handoff 再会テンプレ / Phase 番号体系 / キックオフ検知 / case 1〜5 分類 / 境界表 / FM 二層戦略節 / bootstrap-only カテゴリ / CHANGELOG 過去 entry / ADR 過去決定 / vocabulary 骨格 等
    - 例外ルール:保護対象の意図的削除は自動的に MAJOR bump 扱い、Migration Notes 必須
    - Claude 用チェックリスト:Naoya への計画提示時に含める確認事項

### Changed

- **`README.md`**: maintainer-guide への参照を「何が入っているか」テーブルに追加

### Migration Notes

v1.4.x からの update:
- **既存 adopter**: 追加作業なし。maintainer-guide は adopter 向けではないため、通常運用への影響なし
- **新規 adopter**: 変わらず setup-companion.md / user-guide.md 経由で導入・運用可
- **Framework の maintainer / fork maintainer**: 別 Chat で Framework upstream 作業を依頼する際、Claude が本ガイドを読んで作業する前提になる。過去 Chat 記憶に頼らず本ガイドを canonical とする。特に §15 保護構造リストの遵守により、既存 Skill 挙動(Phase 0.0 検知、handoff 再会テンプレ 等)や canonical ドキュメント構造(キックオフ検知、境界表 等)が意図せず削除される事故を防ぐ

[1.5.0]: https://github.com/nkhippo/Vault-Framework/releases/tag/v1.5.0

## [1.4.0] — 2026-07-18

日常運用ガイドと handoff 拡張。破壊的変更なし。

### Added

- **`docs/ja/user-guide.md`** の新設: 導入後の日常運用ガイド(約 620 行)。以下を網羅:
  - 導入背景(何を解決するために生まれたか)と解決アプローチ(3 層アーキテクチャの意味)
  - 基本操作(Vault 保存、過去 Chat 検索、profile 参照)
  - **Chat 引き継ぎ ★重要機能**: handoff 保存に加え、adopter が新規 Chat で continuation するための再会テンプレを Chat に出力。テンプレには「MCP 経由で参照できない添付すべきファイル」の案内を含む
  - Task / Issue の抽出と backlog 管理
  - プロジェクト管理の基準と手順
  - Vault メンテナンス(Level 別、Cursor 委譲パターン)
  - profile と価値観の運用
  - Framework 更新の取り込み
  - 高度な使い方(横断検索、note 執筆、日記、GitHub Issue 起票)
  - トラブル対応

### Changed

- **`skills/vault-manager/SKILL.md`**: handoff 保存フローに「再会テンプレ出力」挙動を追加。adopter は出力されたテンプレを新規 Chat にコピペするだけで context を復元できる
- **`README.md`**: user-guide への参照を追加

### Migration Notes

v1.3.x からの update:
- **既存 adopter**: Skill を再アップロードすれば handoff 保存時の再会テンプレ出力が有効化される
- **新規 adopter**: 初回導入時から新挙動が有効
- 既存の handoff ファイル・current-state.md 形式は変更なし

[1.4.0]: https://github.com/nkhippo/Vault-Framework/releases/tag/v1.4.0

## [1.3.0] — 2026-07-18

AI-guided setup と初回セットアップ検知の追加。破壊的変更なし、既存 adopter は特別な作業なしに継続利用可能。

### Added

- **`docs/ja/setup/setup-companion.md`** の新設: adopter が別 Chat の Claude に本ファイルを渡すことで、対話形式で導入をサポートしてもらえる Claude 向け対話ガイド spec。約 480 行、Phase 1〜7 全体をカバー、GitHub アカウント作成から Private リポジトリ設定、PAT 発行、Cloudflare Workers デプロイ、Claude Skills / Projects / MCP Connector 設定、Phase 7 初期認識合わせまで
- **`vault-templates/00_meta/SETUP.md`** の新設: adopter の Vault に存在する間、初期セットアップが未完了であることをマーク。bootstrap-only ファイル(削除後、Framework update で再取得しない)
- **`skills/vault-manager/SKILL.md` に Phase 0.0(初期セットアップ検知)を追加**: Vault との最初のやりとりで `00_meta/SETUP.md` の存在を検知、通常のケース分岐に入らず自動的に Phase 7 モードを発動。Phase 7 完了後、`SETUP.md` を削除して通常モードへ復帰
- **`vault-templates/00_meta/project_instructions_vault.md` v1.6**: SETUP.md 検知による Phase 7 発動条件を明示

### Changed

- **`README.md` の Quick Start を AI-guided setup 推奨型に刷新**: setup-companion 経由を第一選択に、マニュアル setup を代替経路として明示
- **`docs/ja/setup/canonical-vs-personal.md` に bootstrap-only カテゴリを追加**: SETUP.md の update 時の扱い(削除後は復元しない)を明示

### Migration Notes

v1.2.x からの update:
- **既存 adopter**: 追加作業なし。既にセットアップが完了している場合、SETUP.md は Vault に存在しないため Skill Phase 0.0 は空振り(通常モードに遷移)し、既存挙動と同じ
- **新規 adopter**: vault-templates を初回コピーすると SETUP.md も自動的に含まれる。以降の新規 Chat で Skill が自動的に Phase 7 モードを駆動

[1.3.0]: https://github.com/nkhippo/Vault-Framework/releases/tag/v1.3.0

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

---
audience: maintainer
framework_version: 1.0.0
keywords:
  - maintainer
  - upstream
  - pii-masking
  - version-bump
  - cursor-instruction
  - framework-development
status: draft
summary: Vault-Framework の maintainer 向け運用ガイド。個人 Vault で得られた運用改善を Framework へ upstream する際のワークフロー、変更カテゴリと影響ファイルマッピング、PII マスキング規則、版バンプ判断、Cursor 指示書標準テンプレート、mirror 運用、「取り込んで」プロンプトへの Claude 対応フローを canonical 化する。
tags:
  - framework
  - maintainer
  - upstream
  - operations
title: Framework Maintainer Guide (upstream 運用ガイド)
type: knowledge
created: 2026-07-18T18:18:01+09:00
updated: 2026-07-18T23:00:00+09:00
---

## このガイドは何か

Vault-Framework の **maintainer 向け運用ガイド**。個人 Vault(このフレームワークの参考実装 or 開発元)で得られた運用改善を、Framework(公開版 `nkhippo/Vault-Framework`)へ upstream する際のワークフロー・ルール・判断基準を canonical 化する。

**対象読者**:
- Framework の primary maintainer(Naoya)
- 将来の fork maintainer
- 別 Chat で「この運用、framework-Vault にも取り込んで」と依頼された時に読む Claude

このガイドの目的は、**別 Chat / 別セッションでも同じ品質で upstream 作業ができるようにする**こと。

---

## Claude への発動条件

**maintainer(以下 Naoya)が Claude に以下のような依頼をした場合、本ファイルを最優先で読み、そのルールに沿って作業する**:

- 「この運用、framework-Vault にも取り込んで」
- 「これを Framework 側に upstream して」
- 「Framework に反映する指示書を作って」
- 「この改善を公開版に載せたい」

上記を検知したら、Claude は:
1. 本ファイル(`docs/ja/maintainer-guide.md`)を MCP で取得
2. 現行の作業内容が「§3 変更カテゴリ」のどれに該当するか判定
3. **「§15 保護すべき既存構造」を確認**(★ v1.5.0 で追加された critical step)
4. 「§4 影響ファイル」に沿って staging 反映内容を計画
5. 「§5 PII マスキング」を必ず適用
6. 「§7 版バンプ判断」で SemVer 版を決定
7. Cursor 指示書を「§8 標準テンプレート」に沿って生成

**憶測禁止**:過去の Chat セッション記憶に頼らず、本ファイルの記述を正典とする。ここで規定されていない領域は Naoya に確認する。

---

## 1. 全体ワークフロー

```
[個人 Vault]                                                                
   |                                                                        
   | 気づき / 実装 / 運用改善                                               
   v                                                                        
[汎用化の判断] ← ここで stop する場合もある(個人色が強すぎる等)             
   |                                                                        
   v                                                                        
[保護対象の確認] ← §15 に照らして、既存 critical 構造への影響を判定         
   |                                                                        
   v                                                                        
[staging に反映]                                                            
30_projects/Vault-Framework/ 配下(Vault リポジトリ内)                     
   |                                                                        
   | Claude が MCP で反映(小規模)                                        
   | または Cursor 指示書で委譲(大規模)                                  
   v                                                                        
[Cursor 実行]                                                               
Vault repo main への merge、公開リポジトリへの mirror、tag、Release        
   |                                                                        
   v                                                                        
[iCloud pull 確認]                                                          
Vault と Vault-Framework 両方のローカル clone を最新化                      
```

### 分担の目安

- **小規模**(1〜3 ファイルの canonical 変更、明確な判断): Claude が MCP で直接 staging 反映
- **大規模**(SKILL.md 更新、複数ドキュメント連動、公開 mirror + tag + Release): Cursor へ委譲
- **判断が要る**(汎用化するか否か、PII マスキングの境界、保護対象への影響): Naoya に確認

---

## 2. 汎用化の判断基準

個人 Vault の全ての改善を Framework に取り込むわけではない。以下で判定:

**取り込むべき**:
- ✅ 他 adopter にも価値がある(業種 / ドメイン非依存)
- ✅ 個人固有情報を除去しても本質が残る
- ✅ Framework の思想(3 層アーキテクチャ、Skill + MCP + GitHub)に整合

**取り込むべきでない**(個人 Vault 側に留める):
- ❌ Naoya 固有の業種 / プロジェクト / 人間関係に特化
- ❌ 汎用化すると本質が失われる
- ❌ 実験段階、まだ Naoya 自身で運用が固まっていない
- ❌ sensitive 情報(50_self 系、健康・家族・財務)

**判断に迷う**:Naoya に確認 → 承認後に取り込み。憶測で進めない。

---

## 3. 変更カテゴリ

改善を分類し、影響ファイル群を特定する。1 つの改善が複数カテゴリに跨がることも多い。

| # | カテゴリ | 例 | 主な影響ファイル |
|---|---|---|---|
| A | Skill 挙動追加 / 変更 | 新コマンド、新フロー | `skills/vault-manager/SKILL.md` |
| B | 新規テンプレ | 新 type の Front Matter テンプレ | `vault-templates/00_meta/templates/<name>.md` |
| C | vocabulary 拡張 | 新 type / status / kind / tag 系 | `vault-templates/00_meta/vocabulary.md` + 場合により `backlog_tags.md` / `frontmatter_schema/<name>.md` |
| D | 新規 doc | philosophy / setup / guide / ADR | `docs/ja/**` |
| E | operations 系 | dev/writing common 拡張、新 profile 系 | `vault-templates/00_meta/operations/**` |
| F | Instructions | project_instructions_vault の運用ルール変更 | `vault-templates/00_meta/project_instructions_vault.md` |
| G | 設定 / メタ | version、CHANGELOG、README、License 等 | ルート `README.md` / `CHANGELOG.md` / `VERSION` / `.framework-version` |
| H | bug fix | 誤り修正、リンク切れ、typo | 該当ファイル |
| I | 破壊的変更 | type rename、schema 変更 | 複数ファイル + 移行手順 |

---

## 4. 影響ファイルマッピング(詳細)

### A. Skill 挙動追加 / 変更

**変更対象**:
- `skills/vault-manager/SKILL.md`(挙動追加時、Phase 番号を維持)
- `skills/vault-maintainer/SKILL.md`(該当時)

**連動更新**:
- `vault-templates/00_meta/project_instructions_vault.md`:新挙動を明示する必要があるなら version log 更新
- `docs/ja/user-guide.md`:adopter に伝えるべき新機能なら記載追加
- CHANGELOG:Changed または Added

**ツール**:`Vault-MCP:skill_note`(`updated` 自動注入されないため必須)

**FM 特殊ルール**:
- `name` + `description` + `updated` の 3 フィールドは Claude Skills 純粋形式
- staging では `id` / `aliases` も同居(Vault CI V1 要件)
- mirror 時、public 側は `id` / `aliases` を strip

**★ read-modify-write 原則(v1.5.0 で追加)**:
既存 SKILL の変更時は必ず現行内容を `get_file_content` で取得し、**変更前後の diff を Naoya に提示**してから `skill_note` で書き込む。Phase 0.0(SETUP.md 検知)や handoff 保存後の再会テンプレ出力 等の既存挙動を意図せず削除しないため。詳細は §15。

### B. 新規テンプレ追加

**変更対象**:
- `vault-templates/00_meta/templates/<name>.md`(新規)
- `vault-templates/00_meta/frontmatter_schema/<name>.md`(スキーマ定義)
- `vault-templates/00_meta/vocabulary.md`(新 type の登録)

**連動更新**:
- CHANGELOG:Added
- 場合により `docs/ja/user-guide.md`(使い方説明)

### C. vocabulary 拡張

**新 type 追加時**:
- `vault-templates/00_meta/vocabulary.md`:新 type を該当セクションに追加
- B の連動(templates + frontmatter_schema)
- CHANGELOG:Added

**新 tag 追加時**:
- `vault-templates/00_meta/backlog_tags.md`:backlog 系 tag なら
- `vault-templates/00_meta/vocabulary.md`:汎用 tag なら
- CHANGELOG:Added

**新 kind / state / assignee 値**:
- `vault-templates/00_meta/vocabulary.md`
- `vault-templates/00_meta/frontmatter_schema/backlog_item.md`
- `vault-templates/00_meta/templates/backlog_item.md`(該当時)
- CHANGELOG:Added(MINOR)or Changed(既存挙動修正)

### D. 新規 doc

**変更対象**:
- `docs/ja/<name>.md` または `docs/ja/setup/<name>.md`(該当時)

**連動更新**:
- `README.md`:「何が入っているか」テーブル・「導入後の使い方」等の該当セクション
- `docs/ja/setup/README.md`:setup 系なら順序に組み込み
- CHANGELOG:Added

### E. operations 系

**変更対象**:
- `vault-templates/00_meta/operations/<name>.md`

**連動更新**:
- `vault-templates/00_meta/vocabulary.md`:operations カテゴリ tag があれば
- `vault-templates/00_meta/project_instructions_vault.md`:参照追加(`applies_common: [<name>]`)
- CHANGELOG:Added / Changed

### F. Instructions 更新

**変更対象**:
- `vault-templates/00_meta/project_instructions_vault.md`

**連動更新**:
- version log を必ず更新(例: `v1.5 → v1.6`、変更内容を明記)
- CHANGELOG:Changed

### G. 設定 / メタ

**新版リリース時の必須更新**:
- ルート `VERSION`:新版番号
- `vault-templates/.framework-version`:新版番号(公開側と一致)
- `README.md` の Status セクション: Current version
- `CHANGELOG.md`:新版セクションを Unreleased の下に追加
- 各 canonical doc の Front Matter `framework_version` フィールド(あれば)

### H. bug fix

**変更対象**:該当ファイル

**連動更新**:
- CHANGELOG:Fixed
- 影響範囲が広いなら README や user-guide の該当箇所も

### I. 破壊的変更(MAJOR bump)

**変更対象**:多数

**必須**:
- CHANGELOG に **BREAKING** マーカーを付ける
- 移行手順(Migration Notes)を CHANGELOG に詳述
- 場合により 移行スクリプト同梱
- `docs/ja/setup/08-update.md`:破壊的変更の対応節を更新

---

## 5. PII マスキング(★ 最重要)

個人 Vault(private)→ Framework(public) への upstream 時、以下を必ず適用。**マスキング漏れは公開後の削除・再リリースが困難なため、公開前に完全に除去する**。

### カテゴリ別ルール

| # | カテゴリ | staging での置換 | 例外(残してよい場所) |
|---|---|---|---|
| A | `Naoya`(大文字) | 「あなた(導入者)」 | なし |
| B | `naoya`(小文字、フィールド値・path・アカウント名の一部) | 文脈判断: 単独アカウント名は `<your-account>`、assignee は `owner` | Framework 自身の GitHub owner `nkhippo` として残す(C 参照) |
| C | `nkhippo`(GitHub owner) | Framework repo のオーナー名として保持。**vault-templates/ 配下では `<your-account>`** | `README.md` / `CHANGELOG.md` / `docs/` 内の Framework 自己参照は残す |
| D | 実プロジェクト名: `IPASoundDrill` / `ThinkGrindAi` / `English-Vocab-Chunk-Trainer` / `Vault-MCP` | `<your-project>` / `<your-mcp-server>` へ、または例示コメント `<!-- 実例: ... -->` へ退避 | `Vault-MCP` は setup/02 で MCP サーバの参照実装として言及されるので残す |
| E | 通称エイリアス: `IPA` / `VCT` / `Structure` / `Listening` | 例示コメントへ退避、または削除 | なし |
| F | 個人 URL / パス: `vault-mcp.nkhippo.workers.dev` / iCloud 実パス | 汎用形: `https://<your-mcp>.<your-account>.workers.dev` / 「ローカルディレクトリ」等 | setup 手順の参照実装への言及なら汎用形で明記 |
| G | Naoya 個人価値観の断定文: 「熱が全て」「独立志向を強化」等 | 削除、または一般化(「adopter の価値観に応じて」) | `profile.md` は骨格のみ(中身プレースホルダ)であるべき |
| H | Naoya 固有 wikilink id: `[[mt-....\|X]]` / `[[pj-....\|X]]` | Framework 相対パスへ変換、または削除 | なし |
| I | 個人的エピソード: 「2026-07-16 の記事3公開セッションで…」等 | 汎用の教訓に言い換え、または削除 | ADR / CHANGELOG の歴史記述は日付・出来事のみ残す(個人色は除去) |
| J | sensitive 実データ: 50_self、健康、家族、財務、感情 | 一切残さない | なし |

### staging 反映時と mirror 時の二層扱い

- **staging**: 上記の genericize は staging(nkhippo/Vault の `30_projects/Vault-Framework/`)反映時に既に適用。Naoya が自分の Vault で内容を作った後、Framework staging へコピーする段階で genericize
- **mirror**: staging → public のミラー時、追加で Front Matter から `id` / `aliases` / `project` を strip(§7.1 参照)

### PII レビューの実施タイミング

- 各リリースの最終工程(mirror 前)に必ず全走査
- rg で下記パターンを走査(Cursor 指示書に含める):
  ```
  rg -n 'Naoya|naoya' $STAGING
  rg -n 'nkhippo' $STAGING/vault-templates
  rg -n 'IPASoundDrill|ThinkGrindAi|English-Vocab-Chunk-Trainer' $STAGING
  ```
- ヒットした箇所は 1 件ずつ判定、`TODO(review):` コメントで残置は Naoya 承認必須

### PII_REVIEW_TODO.md

意図的に残置した固有名や、Naoya 承認済みの例外は staging の `PII_REVIEW_TODO.md` に記録して trace 可能にする。公開側には mirror しない(除外リスト対象)。

---

## 6. Front Matter の二層戦略(canonical/personal 境界 の一環)

詳細は `docs/ja/setup/canonical-vs-personal.md`。要点:

### staging 側(Vault 運用層)

- 全ファイルに `id` / `aliases` / `project` を維持
- Vault CI V1 が必須フィールドとして要求
- Vault-MCP が楽観ロック等で利用

### public 側(Framework 配布層)

- 全 canonical ファイルから `id` / `aliases` / `project` を **strip**
- 保持するフィールド: `title` / `type` / `status` / `tags` / `summary` / `audience` / `keywords` / `created` / `updated`

### Skill FM の特殊扱い

- staging: `name` + `description` + `updated` + `id` + `aliases`
- public: `name` + `description` + `updated` のみ(純粋 Claude Skills 形式)
- **`ensureTimestamps` による auto-inject を回避するため、Skill 書き込みは `Vault-MCP:skill_note` ツールを使う**

---

## 7. 版バンプの判断基準(SemVer)

現在 Framework は SemVer v1.0.0 契約(初回安定版から開始)。

### PATCH(v1.x.Y → v1.x.Y+1)

- typo、文言修正
- 既存挙動の微調整で adopter に影響なし
- bug fix
- ドキュメントの改善(意味変更なし)

例:v1.0.1(構造修正)、v1.1.1(tools/reference の AUTO_INJECT_* 修正)

### MINOR(v1.X.y → v1.X+1.0)

- 新規 canonical 追加(新テンプレ、新 doc、新 type)
- 後方互換な Skill 挙動追加
- 新コマンド、新機能
- adopter が既存運用のまま利用継続可能

例:v1.1.0(mcp-server-reference 新設)、v1.3.0(SETUP.md + Skill Phase 0.0)、v1.4.0(user-guide + handoff 再会テンプレ)

### MAJOR(vX.y.z → vX+1.0.0)

- type / status / kind rename(既存ファイルの Front Matter が invalid になる)
- フォルダ構造変更
- Skill 互換性ブレイク
- 削除された機能
- 必須フィールドの追加
- **§15 の保護対象を意図的に削除・意味変更する場合**

### 判断迷い時

- **迷ったら MINOR**(PATCH 濫用より安全)
- 判断根拠を CHANGELOG に明記

---

## 8. Cursor 指示書の標準テンプレート

過去の指示書パターン(`CURSOR_INSTRUCTIONS_*.md` を参照)を継承。以下の構成が標準:

```markdown
# Cursor 指示書 — vX.Y.Z(概要)

## 0. 目的

- 変更 A、B、C を staging 反映 & 公開ミラー
- Framework 側を vX.Y.Z としてリリース(SemVer 種別)

## 前作業(既に完了)

Claude が MCP で staging に反映済み:
- [file 1]、SHA、commit
- ...

## Task 1 — [作業内容]

**対象**: [ファイルパス]

**変更内容**: ...

**コミット**: `[コミットメッセージ形式]`

## Task 2 — [作業内容]

...

## Task N — 公開ミラー + CHANGELOG + vX.Y.Z release

### N.1 CHANGELOG.md への vX.Y.Z 追記

[マークダウン形式で v セクション]

### N.2 VERSION 更新

- `VERSION` を `旧` → `新`
- `.framework-version` を `新`
- README Status の Current version
- doc 内 `framework_version` FM

### N.3 ミラーと release

継承する運用方針:
- 選択同期: [パスリスト]
- 除外: [パスリスト]
- FM strip: id/aliases/project

PR → merge → tag `vX.Y.Z` → GitHub Release

## 完了報告項目

- Task 1: ...
- Task 2: ...
- Task N: PR URL、merge commit、tag、Release URL

## 判断が要る場面

1. [判断点]

## 前回学びの継承

- rsync --delete 禁止、選択同期厳守
- FM 二層戦略遵守
- Skill FM は純粋 Claude Skills 形式(`skill_note` 使用)
- iCloud pull 忘れ防止
- **§15 保護対象への影響を明示**(v1.5.0 で追加)

## 対象外(vX.Y.Z のスコープ外)

- ...
```

**重要な原則**:
- 過去の教訓(rsync --delete 禁止、FM 二層、iCloud pull、§15 保護対象保持 等)を必ず「継承」セクションに列挙
- 判断が要る場面を明示(Cursor が独断で進めない)
- 対象外を明記(スコープクリープ防止)

---

## 9. CHANGELOG 書式

Keep a Changelog 準拠、SemVer 準拠。以下の構造:

```markdown
## [X.Y.Z] — YYYY-MM-DD

[版の一言サマリ]

### Added
- [新規追加項目]

### Changed
- [既存の変更項目]

### Fixed
- [修正項目]

### Deprecated
- [非推奨化された項目]

### Removed
- [削除された項目]

### Migration Notes

[v(X.Y.Z-1) からの移行に関する説明]
- **既存 adopter**: [追加作業の有無、対応方法]
- **新規 adopter**: [初回導入時の影響]

[X.Y.Z]: https://github.com/nkhippo/Vault-Framework/releases/tag/vX.Y.Z
```

**Migration Notes の書き方**:
- MINOR 以下は「特別な作業なし」で終わることが多い
- MAJOR は必ず具体的な移行手順を列挙
- Skill 側変更なら「Skill を再アップロードすれば有効化」等

---

## 10. mirror 時の運用

### 選択同期(★必須)

**`rsync --delete` は絶対に使わない**。以下のパスを個別に同期:

- 同期: `README.md` `CHANGELOG.md` `VERSION` `docs/` `skills/` `vault-templates/` `examples/` `mcp-server-reference/`
- 除外: `handoff/` `_history/` `backlog/` `logs/` `PII_REVIEW_TODO.md`

### 公開側非 staging リソースの保持

公開リポジトリにのみ存在する以下は削除しない:
- `scripts/`
- `migration/`
- `tests/`
- `project-instructions/`(該当時)

これらは Cursor が過去 mirror 時に「保持リソース」として整理済み。

### iCloud pull 忘れ防止

PR merge 後、必ず両方の iCloud clone を pull:
- Vault(staging 側): `~/Library/Mobile Documents/com~apple~CloudDocs/Vault`
- Vault-Framework(public 側): `~/Library/Mobile Documents/com~apple~CloudDocs/Vault-Framework`

pull しないと、次回の作業で古い状態から始めてしまう(過去にトラブル事例あり)。

---

## 11. Vault-MCP 側の変更

**Vault-MCP は別リポジトリ・別リリースサイクル**。Framework の tag には紐付けない。

### Vault-MCP 変更が必要な場合

- 新 MCP tool の追加(Framework の Skill が新 tool を前提とする改修)
- 既存 tool の仕様変更
- bug fix

### Framework 側で連動が必要な場合

Framework CHANGELOG の Migration Notes に:
- 「Vault-MCP vX.Y.Z 以降が必要」を明示
- adopter は Framework update 前に Vault-MCP を先に update

### Vault-MCP の CHANGELOG は Vault-MCP リポジトリ側で管理

Framework CHANGELOG に Vault-MCP 変更の詳細は書かない(参照リンクのみ)。

---

## 12. 「取り込んで」プロンプトへの Claude の対応フロー

Naoya から「この運用、framework-Vault にも取り込んで」等の依頼を受けた Claude は、以下の手順を踏む:

### Step 1: 本ファイルを読む

まず `docs/ja/maintainer-guide.md`(本ファイル)を MCP で取得。**過去 Chat 記憶に頼らず本ファイルを正典とする**。

### Step 2: 変更内容の理解

Naoya から:
- 「この運用」とは具体的に何か?
- どのファイル(個人 Vault 側)に反映済みか?
- 汎用化の意図はあるか?

**憶測禁止**。必要なら Naoya に確認。

### Step 3: 汎用化の可否判定(§2 参照)

- Framework に取り込むべきか
- 個人 Vault 側に留めるべきか
- 迷ったら Naoya に確認

### Step 3.5: 保護対象の確認(★ v1.5.0 で追加)

Step 3 の後、Step 4 の前に必ず実施:

1. 変更対象ファイル(候補)を §15.2 の「特に注意すべき既存構造」リストに照らす
2. 保護対象が含まれる場合、変更計画に「**保護対象への影響**」節を必ず追加
3. 変更が保護対象を**削除または意味変更**する場合、§15.3 に従って **MAJOR bump 相当**として Naoya に報告し、影響範囲を確認
4. 保護対象の追加だけで既存を維持する場合、その旨を明記

**このステップを怠ると、既存 canonical(Phase 0.0 検知、handoff 再会テンプレ、キックオフ検知 等)を意図せず削除する事故が発生し得る**。

### Step 4: 変更カテゴリと影響ファイルの特定(§3、§4)

該当するカテゴリを 1 つ以上選び、影響ファイルを列挙。

### Step 5: PII マスキングの計画(§5)

- 個人固有の記述をどう置換するか
- 例外(残す)と削除の判断

### Step 6: 版バンプの判断(§7)

- PATCH / MINOR / MAJOR のどれか
- 根拠を明確に(Step 3.5 で保護対象への影響があれば MAJOR)

### Step 7: 反映方法の選択

- 小規模: Claude が MCP で staging 直接反映
- 大規模: Cursor 指示書を作成(§8 のテンプレート使用)

### Step 8: Naoya に計画を提示

以下を含む計画案を作成:
- 変更カテゴリと影響ファイル
- **保護対象への影響**(Step 3.5 の結果)
- PII マスキング方針
- 版バンプ判断
- 反映方法(MCP or Cursor)
- 想定される Cursor 作業内容

**Naoya の明示承認後に実行**。

### Step 9: 実行

- 承認された計画に沿って staging 反映(または Cursor 指示書生成)
- 反映後、commit SHA / URL を Naoya に報告
- **既存 canonical を変更した場合、変更前後の diff を Naoya に見せて確認**

---

## 13. トラブル時

### staging と public の乖離が発見された

- 原因を特定(手動修正、mirror 漏れ 等)
- staging を canonical と見なして public を re-mirror(過去 v1.0.1 で確立された方針)
- 逆に public のみに正しい状態があれば、それを staging に取り込み

### 公開側 CI の V1 FAIL

- `id` 除去方針による既知トレードオフ
- 対応不要(v1.0.0 リリース時に判断済み)

### iCloud sync がおかしい

- iCloud UI で「今すぐダウンロード」を実行
- 両 clone(Vault と Vault-Framework)で確認
- ローカル git status で差分をチェック

### CI エラーで PR が merge できない

- CI 種別を確認(V1〜V8)
- staging 側は `id`/`aliases` 維持が必要(過去に混乱事例あり)
- 修正 PR を追加して対応

### 既存 canonical を意図せず削除・破壊した

- git 履歴から復元
- §15.1 メタルールが守られなかった原因を特定
- Naoya に報告、影響範囲を確認
- 必要なら hotfix リリース

---

## 14. 関連ドキュメント

- **canonical / personal 境界**: `docs/ja/setup/canonical-vs-personal.md`(§5 FM 二層と重複、正典として参照)
- **update 手順**(adopter 向け): `docs/ja/setup/08-update.md`
- **user-guide**(adopter 向け): `docs/ja/user-guide.md`
- **CHANGELOG**: リポジトリルート `CHANGELOG.md`
- **過去の Cursor 指示書**: 命名パターン `CURSOR_INSTRUCTIONS_vX.Y.Z-*.md`
- **Vault-MCP**: 別リポジトリ `https://github.com/nkhippo/Vault-MCP`

---

## 15. 保護すべき既存構造(★ 事故防止の要)

「取り込んで」プロンプトで新規改善を反映する際、既存の重要構造を意図せず削除しないための正典。

### 15.1 メタルール(★最重要)

既存 canonical ファイルを変更する場合、以下を必須:

1. **変更前に必ず現行内容を読む**(`Vault-MCP:get_file_content` または `get_section`)
2. **変更計画を diff 形式で Naoya に提示**:
   - 追加する行 / 変更する行 / 削除する行 / 保持する行
3. **Naoya の明示承認後にのみ書き込み**
4. **`replace_body` / `replace_all` は最後の手段**:必要な場合、変更前の全文を確認したことを Naoya に報告

**憶測禁止**:過去 Chat 記憶や自身の判断で「これは削っても大丈夫」と決めない。既存記述の意味が不明な箇所は Naoya に確認。

### 15.2 特に注意すべき既存構造

以下は Framework の運用に直結する構造。**削除・意味変更は極めて慎重に**、破壊すると adopter の運用が壊れる:

**`skills/vault-manager/SKILL.md`**:
- **Phase 0.0(初期セットアップ検知)**(v1.3.0 で導入):`00_meta/SETUP.md` を検知して Phase 7 モード自動発動
- **handoff 保存後の再会テンプレ出力挙動**(v1.4.0 で導入):handoff コマンド後にコードブロックでテンプレを出力
- **Phase 番号体系**(0.0, 0.5, 1, 1a, 1b, ...):既存の順序と番号を維持
- **明示 trigger phrases**(「Vault に保存して」「引き継ぎ」等)
- **即時実行フロー**(承認プロトコル、参照フロー)
- **staging FM の id/aliases 同居**(Vault CI V1 要件)

**`skills/vault-maintainer/SKILL.md`**:
- **Level 1〜4 のメンテナンス粒度**
- **stalled detection ロジック**

**`vault-templates/00_meta/project_instructions_vault.md`**:
- **キックオフ検知(最優先)セクション**:v1.5〜(SETUP.md 検知 + キックオフ文言の 2 通り発動)
- **case 1〜5 分類**:特定プロジェクト / 執筆 / 汎用ナレッジ / 日記 / 意図不明
- **version log**:追記のみ、既存 entry の書き換え禁止

**`vault-templates/00_meta/SETUP.md`**:
- **bootstrap-only ファイル**の意味(削除後は Framework update で復元しない)

**`docs/ja/setup/canonical-vs-personal.md`**:
- **境界表 3 種類**(canonical / hybrid / personal / bootstrap-only)
- **Front Matter 二層戦略節**(v1.0.1 で確立)

**`docs/ja/setup/setup-companion.md`**:
- **Phase 1〜7 の全体構造**
- **対話原則、エラー時対応**
- **Framework 全体資料への案内リンク**

**`docs/ja/user-guide.md`**:
- **導入背景、解決アプローチ節**(v1.4.0)
- **Chat 引き継ぎ節の再会テンプレ + 添付ファイル案内**(v1.4.0)

**`docs/ja/maintainer-guide.md`(本ファイル)**:
- **全セクション**:このファイル自体が Framework 開発の正典。§15 を含む全構造を維持

**`CHANGELOG.md`**:
- **過去 entry の書き換え禁止**(追記のみ)
- **Migration Notes の削除禁止**
- **SemVer リンク行の維持**

**その他 canonical**:
- **ADR**(`docs/ja/decisions/`):過去決定の書き換え禁止(新規追加は OK)
- **`vocabulary.md` の骨格セクション**:type / status / kind / state / assignee の定義変更は破壊的(MAJOR bump)
- **`frontmatter_schema/**`**:schema 変更は破壊的
- **`templates/**`**:テンプレ変更は adopter の既存ファイルに影響

### 15.3 例外:意図的な削除・変更

保護対象を意図的に削除または大幅変更する場合:

- **破壊的変更(MAJOR bump)として扱う**
- **CHANGELOG の Migration Notes に必ず記載**
- **adopter への影響を明記**
- **v2.0.0 等の major bump を伴う**

「取り込んで」プロンプトが通常 MINOR / PATCH 相当なのに、途中で保護対象への影響が判明したら:
1. 作業を中断
2. Naoya に「これは MAJOR 相当の影響がある」と報告
3. 対応方針を確認(MAJOR bump として進める、or 別アプローチを検討)

### 15.4 チェックリスト(Claude 用)

「取り込んで」プロンプトを受けた Claude は、Step 8 で Naoya に計画を提示する際、以下を含める:

- [ ] §15.2 の保護対象ファイルに変更が及ぶか?
- [ ] 及ぶ場合、どの保護対象要素か?
- [ ] 保護対象要素を削除・意味変更するか、追加のみか?
- [ ] 削除・意味変更する場合、§15.3 に従って MAJOR bump 相当として扱うか?
- [ ] 変更前の diff を Naoya に見せる予定か?

これらを明示的にチェックし、Naoya の承認を得てから作業に入る。

---

## 16. 更新履歴(本ファイル)

- **v1.0**: 初版。§1〜§14 を canonical 化(v1.5.0 相当リリースで導入)
- **v1.1**: §15「保護すべき既存構造」節を追加。§12 に Step 3.5(保護対象確認)を挿入、§4-A に read-modify-write 原則追記。既存 critical 構造(Phase 0.0、handoff 再会テンプレ、キックオフ検知 等)の意図しない削除を防ぐため
- **v1.2**: 内部相互参照の「§16」を「§15」へ修正(§15 セクションへの renumber 反映漏れの修正、6 箇所)。v1.5.1 パッチリリース

このガイド自体の更新は、Framework maintainer の運用改善が積み重なるたびに追加。version log で追跡。

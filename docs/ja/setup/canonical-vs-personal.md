---
audience: adopter
keywords:
  - setup
  - sync
  - canonical
  - personal
  - hybrid
  - boundary
status: draft
summary: Framework の同期対象(canonical)と各自固有領域(personal)の境界を明示する正典。update 時にどのファイルをどう扱うか(差し替え / マージ / 触らない)を規定する。Claude のガードレールおよび update 手順から参照される。
tags:
  - framework
  - setup
  - sync
  - canonical
  - personal
title: canonical / personal 境界表
type: setup
created: 2026-07-18T12:51:05+09:00
updated: 2026-07-18T12:51:05+09:00
---

Framework は「配布された骨格を各自の Vault にコピーして使う」構造。配布後、Framework 側のアップデートを取り込むとき、**どのファイルを差し替えていいか / 触ってはいけないか** を明確にするための正典。

## 用語

- **canonical**: Framework が正典として保持し、配布後もあなた個人の判断で変えない領域。update 時に Framework 側から差し替える対象
- **personal**: あなたの Vault だけに存在する、あなた固有の内容。update 時に **Framework 側から一切上書きされない**
- **hybrid**: canonical な骨格 + personal な記入欄が同一ファイルに同居する領域(例: vocabulary.md の `project` セクション)

## 境界表

### canonical(update 時に差し替え)

| パス | 種別 | update 手段 |
|---|---|---|
| `skills/vault-manager/SKILL.md` | Framework 中核 | zip 再アップロード(Claude Skills) |
| `skills/vault-maintainer/SKILL.md` | Framework 中核 | zip 再アップロード |
| `00_meta/backlog_tags.md`(骨格部) | 骨格 + tag 追加は personal | 骨格セクションのみ pull で差し替え |
| `00_meta/frontmatter_schema/**` | schema 正典 | フォルダごと差し替え |
| `00_meta/templates/**`(既存テンプレ) | 雛形正典 | ファイルごと差し替え(自作追加テンプレは personal で共存) |
| `00_meta/operations/dev_project_common.md` | 運用共通ルール | ファイル差し替え |
| `00_meta/operations/writing_project_common.md` | 運用共通ルール | ファイル差し替え |
| `00_meta/profile.md`(骨格構造) | 骨格 + 中身は personal | セクション見出しのみ差し替え、中身は残す |
| `20_notes/guides/README.md` / `writing_style.md` / `writing_process.md` | canonical | ファイル差し替え |
| `20_notes/guides/writing_examples.md`(骨組み) | canonical + 実例は personal | 枠のみ差し替え、あなたの実例は残す |
| `docs/**` | Framework 文書 | フォルダごと差し替え |

### hybrid(骨格 canonical + 記入欄 personal)

| パス | canonical な部分 | personal な部分 |
|---|---|---|
| `00_meta/vocabulary.md` | type / status / kind / state / assignee / sensitive / tags の骨格定義 | `project:` セクション、ドメイン主題 tag の追記、あなたのプロジェクト固有 tag |
| `00_meta/backlog_tags.md` | 主題系・性質系・状況系の骨格 | ドメイン主題 tag の追加、状況系の閾値カスタム |
| `00_meta/profile.md` | Life Strategy と価値観のセクション構造 | あなたが記入した中身全て |
| `20_notes/guides/writing_examples.md` | 記入方法の説明・空フォーマット | あなたが追記した実例ペア |

update 時は **canonical セクションのみ Framework 側の版に置き換え**、personal セクションは保持する。マージ操作はあなたが手動で確認する(具体手順は `docs/ja/setup/08-update.md`)。

### personal(Framework から一切触らない)

| パス | 内容 |
|---|---|
| `30_projects/**` | あなたのプロジェクト全て(既存・新規問わず) |
| `10_chat_log/**` | Chat 履歴の保存物 |
| `50_self/**` | 日記・振り返り・目標(sensitive) |
| `20_notes/drafts/**` / `20_notes/published/**` | あなたが書いた記事 |
| `_ideas/**` | 構想段階のもの |
| `00_meta/vault_index.md`(あれば) | あなたの Vault の inventory |
| あなたが自作した追加テンプレ・operations ファイル | 命名衝突しない前提で `00_meta/` に追加した personal ファイル |

## 拡張と変更のルール(hybrid 領域向け)

hybrid 領域(vocabulary、backlog_tags 等)は「追加していい / 削除・意味変更してはいけない」の非対称なルール。

**許可される操作**:
- 新規 type / tag / project の追加(personal 拡張)
- ドメイン固有の値の追加

**禁止される操作**:
- canonical で定義された type / tag / status 等の**削除**
- canonical 定義の**意味変更**(例: `state: open` の意味を書き換える)
- Skill が参照する構造の**リネーム**(例: `assignee` → `owner_field` へ改名)

これらを違反すると Framework update 時に整合性が壊れ、Skill が正しく動かなくなる。

## Claude の振る舞い(参照)

Claude はこの境界表に従って、通常の Chat セッションでは canonical 領域を変更しない。詳細は `docs/ja/guardrails/claude-behavior.md`。

例外は「Framework 開発者モード」で、これはあなたが明示的に宣言した時のみ発動する(Framework 自体を改善する場面)。

## update 時のフロー概要

詳細は `docs/ja/setup/08-update.md` に譲る。要点:

1. Framework の CHANGELOG を読む(何が変わったか把握)
2. Skill を再アップロード
3. canonical ファイルを差し替え(hybrid は canonical セクションのみ)
4. 破壊的変更(major version bump)があれば移行手順に従う
5. 再度 Chat で「再認識合わせセッション」を実行(推奨)

## 関連

- update 手順: `docs/ja/setup/08-update.md`
- Claude ガードレール: `docs/ja/guardrails/claude-behavior.md`
- 初期認識合わせセッション: `docs/ja/setup/07-initial-alignment-session.md`
- 変更履歴: リポジトリ ルート `CHANGELOG.md`

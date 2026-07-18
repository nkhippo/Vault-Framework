---
title: dev_project_common - 開発運用スナップショット実例
type: knowledge
status: published
applies_skeleton: dev_project_common
sample_project: '<your-project> (例: IPASoundDrill / ThinkGrindAi)'
snapshot_of: nkhippo/Vault:00_meta/operations/dev_project_common.md
snapshot_taken_at: '2026-07-15'
summary: Framework 骨格 dev_project_common.md の実運用スナップショット。開発運用型プロジェクトでの固有条項の埋め方の参考。
tags:
- framework
- operations
- examples
- dev-project
- snapshot
created: '2026-07-15 23:00:00+09:00'
updated: '2026-07-15 23:00:00+09:00'
---

## Framework 実例ノート

**このファイルは、あなた(導入者) の個人 Vault(`nkhippo/Vault`)にある `00_meta/operations/dev_project_common.md` の 2026-07-15 時点でのスナップショットです。**

- 対応する骨格: `vault-templates/00_meta/operations/dev_project_common.md`
- 実運用対象: <your-project><!-- 実例: IPA Sound Drill -->(発音学習アプリ) / <your-project><!-- 実例: ThinkGrindAi -->(論理思考トレーニング)/ 他 English 系トレーナー群
- スナップショット時点: 2026-07-15
- 参考にできること: Track A/B 分離運用、5 項目チェック運用、堅固化パターン A/B/C 実装、Cursor 実装レポート運用、Claude PR Rv 12 観点

Framework 骨格版と本実例の差分は「あなた(導入者)」等の固有表現、note / Zenn / Dev.to 等の発信計画への言及、MCP コネクタ名(`<your-project><!-- 実例: IPA Sound Drill --> GitHub` `<your-project><!-- 実例: ThinkGrindAi --> GitHub`)の具体例、<your-project><!-- 実例: IPA Sound Drill --> 特有の Category A ドキュメント参照 等。骨格を実プロジェクトでどう埋めるかの参考として読むこと。

---

## Summary

開発運用型プロジェクト(実装は Cursor に委譲し、Claude が要件整理・Issue 起票・Cursor 指示書作成・PR Rv を担当する形態)で共通する運用ルール。プロジェクトごとの `30_projects/<RepoName>/project_instructions.md` の Front Matter に `applies_common: [dev_project_common]` を書くと、Vault 正典のケース 1 フローによりこのファイルが Level 2 で自動的に併読される。

プロジェクト固有の情報(具体的なファイル名、コネクタ名、Track 分離ルール、ドメイン、色 等)は `project_instructions.md` 側で保持する。本ファイルは横断ルールのみ。

## このファイルが定めるもの

以下 18 項目を集約する:

1. コミュニケーション書式 (日本語/英語の使い分け、Chat 応答長さ目安)
2. Issue 起票フォーマット(5 サブセクション背景)
3. Issue 本文の「改修分類」ブロック (Complexity Level, Change Pattern, 堅固化パターン, Claude Rv 要否)
4. Issue 本文の Category A ドキュメント自動チェック
5. Issue 本文の「ブラックリスト md5 検証」ブロック
6. Issue 本文の「作業の進め方」セクション定型
7. Issue 本文の参照ドキュメント明示ルール
8. Issue のラベル別フロー
9. Issue の 5 項目チェック(ready-for-cursor 付与条件)
10. Issue 分割判断 5 軸
11. Cursor 抽象度ガイド(プロジェクト固有ガイドへの参照方式)
12. 堅固化パターン A / B / C(Cursor 指示書作成時)
13. Cursor 実装レポート 3 セクション
14. Claude PR Rv フロー (12 観点、Rv レポート構成、判定ルール)
15. 判断相談フォーマット (案 α / β / γ)
16. Claude Artifacts の活用シーン
17. トラブルシューティング (MCP エラー、Issue 起票エラー、PR Rv 不整合、判断保留の管理)
18. 発信素材化への配慮
19. 返答末尾テンプレ / Chat 切り出しパック / Vault 記録テンプレ
20. 新規ドキュメント作成判定(プロジェクト固有 DOCUMENT-MAP への参照方式)

## コミュニケーション書式

### 言語の使い分け

- **Chat の対話**: 日本語がデフォルト。技術用語は英語のまま (例: `middleware.ts`, `sitemap.xml`, `hreflang alternates`)
- **Issue タイトル / PR タイトル / コミットメッセージ**: 英語
- **Issue 本文 / PR 本文 / Cursor 実装レポート**: 日本語 (分類ブロックの用語は英語のまま、例: `Complexity Level: L2`, `Change Pattern: C3, C4`)
- **あなた(導入者)判断が必要な場面**: 明示的に案 α / β / γ を提示、Claude 推奨を明示 (下記「判断相談フォーマット」参照)

### Chat 応答の長さ目安

- **短い応答 (3-10 行)**: 単純な質問への回答、進捗確認
- **中程度の応答 (30-100 行)**: PR Rv レポート、判断相談、進捗報告
- **長い応答 (100 行以上)**: Issue 本文、詳細ガイド、方針転換の整理

過度な長文化は避けるが、必要な情報の欠落も避ける。あなた(導入者) の意思決定に必要な情報を過不足なく提供。

### 応答の構造

1. **導入**: 前ターンでの依頼に対する応答の要約 (1-2 行)
2. **本文**:
   - 見出し (H2) で論理的に区切る
   - 表形式を積極活用 (PR Rv、比較、進捗)
   - コードブロックで具体例
   - 判断が必要な場合は箇条書きで案 α / β / γ を提示
3. **末尾 3 セクション** (下記「毎回の返答末尾テンプレ」参照)

## Issue 起票ルール(MCP 経由、記事化前提)

Claude が MCP 経由で対象リポジトリの GitHub Issue を直接起票する。使用する MCP コネクタは各プロジェクトの `project_instructions.md` で明示的に指定されたものに限る(作業混ざり防止)。

### 本文の署名

Issue 本文の冒頭・末尾に必ず署名を付ける。

```
🤖 **Claude より**

(本文)

---
_Claude による自動投稿_
```

Cursor が Issue Comment を書く際は `🛠️ **Cursor より**` / `_Cursor による自動投稿_`。

### 【最重要】Issue 本文の冒頭に「改修分類」ブロックを置く

Issue 起票前に以下 4 項目を判定し、本文冒頭に明示する。判定基準の正典はプロジェクトの `docs/CHANGE-CLASSIFICATION.md` (または相当ファイル、`project_instructions.md` で指定)。

```markdown
## 改修分類

- **Complexity Level**: [L1 / L2 / L3]
- **Change Pattern**: [C1-C7 の複数選択可]
- **判定根拠**: [具体的な理由]
- **Pre-Issue Recon**: [不要 / 実施済み Issue #NN]
- **Level 昇格・降格履歴**: [なし / 具体的な履歴]
- **適用堅固化パターン**: [A / B / C]
- **Claude Rv**: [必須(L3)/ 任意(L2)/ 不要(L1)]
```

- **Complexity Level**:
  - L1: 単一関心の軽微な変更
  - L2: 複数ファイル、影響範囲限定
  - L3: フロー再設計、ビルド初導入、URL 構造変更、構造移動
- **Change Pattern**:
  - C1: Docs / 内容更新
  - C2: Infra / Deploy / Tooling
  - C3: Structure / URL / artifact layout
  - C4: UI / UX
  - C5: Content / Data 資産
  - C6: UX 向上のコピー改善
  - C7: Configuration
- **適用堅固化パターン**:
  - A: 新規追加のみ(Phase 0-5)
  - B: 既存編集(Phase 0-5)
  - C: 大規模改修(Phase 0-6、L3 でファイル物理移動 + ビルド新規導入 + L3 × C3 の 3 条件を満たす場合)

### 【最重要】Issue 本文の「背景・目的」は 5 サブセクション構成で書く

Issue → Cursor 実装レポート → 記事化、というパイプラインで、Issue 本文の背景は **Projects / Note での発信素材の一次ソース**になる。事後読み返しても状況が完全に再現できる粒度で書くこと。単なるスコープ説明ではなく、意思決定のプロセスと経緯を残す。

1. **この Issue のトリガー**: どこから発生したか。Chat 内の議論、あなた(導入者)の要望、既存 Issue との関連、外部イベント(ローンチ日近接、フィードバック受信等)。時系列でトレースできるように書く
2. **背景となる文脈**: 3 観点で丁寧に書く
   - **プロダクト目線**: プロダクトの立ち位置、対象ユーザー、戦略目標との関連
   - **開発運用目線**: 現状の運用課題、これまでの改善の積み重ね、この Issue が全体像のどこに位置するか
   - **技術目線**: 採用技術の選定理由、代替案の検討経緯、既存アーキテクチャとの整合
3. **検討した選択肢と選定理由**: 却下した選択肢も含めて記述。「なぜこの選択肢を選んだか」だけでなく「なぜ他の選択肢を却下したか」も書く。読者が同じ判断を再現できることが目安
4. **この Issue で得たい成果**: 定量 / 定性 / 波及効果の 3 観点。定量は測定可能な指標、定性は運用の質、波及は他 Issue や運用への影響
5. **後続への影響**: 次にできるようになること、今後の Issue で参照される可能性がある成果物、中期的な運用への影響

あなた(導入者)が明示的に語っていない主観部分は空欄マーカー `_[あなた(導入者)が追記予定: XX]_` で残し、あなた(導入者)が GitHub UI で追記する運用。

### 【最重要】Issue 対応時に自動更新される Category A ドキュメントを Issue 本文で明示する

Issue 本文の「実装範囲」または「作業の進め方」に、影響を受ける **Category A ドキュメント(常時最新化義務)** を必ず列挙する。Cursor が指示書に従って更新するので、漏れがあれば実装漏れになる。

**具体的にどのドキュメントが Category A に該当するかはプロジェクト固有**で、`project_instructions.md` の「Category A ドキュメント一覧」セクションを参照する。プロジェクト固有一覧に無い場合、Claude は あなた(導入者) に確認する。

該当するものは、Issue のホワイトリストに含め、後述の堅固化パターン B で意図的編集を行うことを Cursor に指示する。

### Issue 本文の「ブラックリスト md5 検証」ブロック

L2 / L3 の Issue で、変更してはいけないファイル (特に先行 Issue の成果物、Runtime data contract 等) を明示する。Cursor は md5 で完全不変を検証する。

```markdown
### ブラックリスト(md5 検証で完全不変を保証)

- `path/to/file1` (先行 Issue #NN の成果物)
- `path/to/file2` (Runtime data contract)
- `path/to/dir/**` (ディレクトリ全体、glob 可)
```

L1 の場合は省略可。L3 の場合は必須。

### 本文に必ず含める「作業の進め方」セクション

```
## 作業の進め方

検証が完了したら、確認なしに以下まで一気に進めること:
1. コミット
2. push
3. PR 作成(base・ラベル・Closes #XXX を記載)

途中で止まってよいのは「不明点がある場合」のみ。PR Comments に質問を書くこと。
```

### 参照ドキュメントの明示

Issue 本文には、Category C(Issue 起票時参照)および Category D(Cursor 実装時参照)から該当するドキュメントを列挙する。具体的な Category 分類の正典は各プロジェクトの `docs/DOCUMENT-MAP.md`(または相当ファイル、`project_instructions.md` で指定)を参照。

### ラベル別フロー

- `feature` / `bug` / `docs` / `chore`: すべて main 直(Track A 相当の期間)
- `ready-for-cursor`: 5 項目チェック完了後に付与
- `launch-blocker`: ローンチまで必須
- `track-b`: ローンチ後着手(Track B スコープ)

プロジェクト固有のラベル定義がある場合は `project_instructions.md` で追加。

### 5 項目チェック(ready-for-cursor 付与条件)

以下 5 項目を Issue 本文が満たしていることを確認してから `ready-for-cursor` ラベルを付与する。

- 背景・目的(上記 5 サブセクション構成、記事化前提の詳細度で)
- 実装範囲(影響を受ける Category A ドキュメントも列挙、ブラックリストも明示)
- 完了定義(動作で記述)
- テスト観点
- 非対象範囲

## Issue 分割判断軸(5 軸)

1. **設計 vs 実装**: 仕様書変更を伴う → docs Issue を先行
2. **対応規模**: 影響ファイル 5 つ超 → 分割(プロジェクト固有の例外条項は `project_instructions.md` に記載)
3. **ドキュメント独立性**: 運用ドキュメント修正は常に単独 Issue で先行
4. **ブロッキング関係**: B が A の完了待ち → A を先行
5. **リスク隔離**: 本番影響大 → 単独 Issue

## Cursor 抽象度ガイド

Issue のスコープ判定は各プロジェクトの Cursor 指示書ガイド(通常 `docs/CURSOR-INSTRUCTION-GUIDE.md` 等、`project_instructions.md` で指定)の抽象度マトリックスに従う。

- 100 行超の Issue は Pre-Issue Recon の要否を あなた(導入者) に提案する
- Pre-Issue Recon: 大きなファイル(index.html が 3,000 行超 等)を Cursor に事前スキャンさせて未知を洗い出す手法。Claude の MCP fetch でコンテキストを消費せずに済む

## 堅固化パターン(Cursor 指示書作成時)

各プロジェクトの `docs/DEV-GUARDRAILS.md`(または相当ファイル、`project_instructions.md` で指定)を参照。パターン A(新規追加のみ、Phase 0-5)とパターン B(既存編集、Phase 0-5)、パターン C(大規模改修、Phase 0-6)を使い分ける。

### 共通原則

- **Cursor 自己判断禁止**(迷ったら Issue Comment で報告して中断)
- lint / typo 修正 / Markdown 整形の禁止
- 「ついで」の作業禁止
- 各 Phase 完了時に Issue Comment に投稿
- 「中断は失敗ではなく、正しい判断」

## 【最重要】Cursor 実装レポート(記事化素材の起点)

Cursor は PR 作成時、必ず `docs/cursor/reports/cursor-implementation-report-<topic>.md`(またはプロジェクト固有のパス)を追加する。テンプレートは各プロジェクトの `docs/DEV-GUARDRAILS.md` を参照。

**Cursor 実装レポートは Projects / Note での発信素材化の起点**。以下 3 セクションを必ず記述する。

- **「Issue 背景(Issue 本文から要約)」**: Issue 本文の 5 サブセクション背景を、実装後の視点で 200-400 字に再構成。単なるコピペではなく、実装を通じて理解が深まった内容も反映する
- **「実装過程での気づき」**: 想定と異なった点、あなた(導入者)との追加やりとりで判明したこと、過去の実装との差分・関連性。テンプレートのままではなく具体的に書く
- **「後続への影響」**: 次にできるようになったこと、今後の Issue で参照される可能性がある成果物。中期的な運用への貢献

あなた(導入者)が目視承認時、これら 3 セクションが具体的かつ実質的な内容になっているかを重点チェックする。

## Claude PR Rv フロー

Claude が PR に対して Rv を実施する。Rv 実施の要否は Complexity Level と あなた(導入者)判断による。

### Rv 実施の要否

- **L3**: Claude Rv 必須 (改修分類の「Claude Rv: 必須」に対応)
- **L2**: あなた(導入者)判断で任意 (依頼があれば実施)
- **L1**: あなた(導入者)目視で足りる (依頼があれば実施)

### Rv 実施時の 12 観点

以下を表形式で提示する。

| # | 観点 | 確認内容 |
|---|---|---|
| 1 | ホワイトリスト範囲内か | Issue 本文の「対象ファイル」に該当するファイルのみが変更されているか |
| 2 | Issue 本文の完全仕様との一致度 | 完了定義・テスト観点・非対象範囲がすべて満たされているか |
| 3 | 既存 Issue 成果物への影響なし (不変性) | 先行 Issue の成果物が変更されていないか (md5 検証、または diff 目視) |
| 4 | Runtime data contract の md5 不変 | data/*.json 等の実行時契約が変更されていないか |
| 5 | 生成物 6 言語の script md5 一致 (該当 Issue のみ) | 多言語ビルド生成物で全言語同一 script のもの (該当 Issue で明示) が md5 一致するか |
| 6 | Category A ドキュメント整合 | 影響を受ける Category A ドキュメントがすべて意図通り更新されているか |
| 7 | Complexity Retrospective の完全性 (6 チェック項目) | 実装レポートの Retrospective が具体的で、テンプレの雛形が残っていないか |
| 8 | 「ついで作業」ゼロ | Issue に無い lint / typo / Markdown 整形が混入していないか |
| 9 | コミット分離 (Phase ごと) | Phase 0-5 (または 0-6) ごとにコミットが分離されているか |
| 10 | grep 検証結果の記録 | Issue 指定の grep 検証項目が実施され、結果が Comment に残っているか |
| 11 | 実装レポートの申し送り事項 | 後続への影響、未解決事項、追加調査要事項が明示されているか |
| 12 | Cursor の自己判断の透明性 | Cursor が独自判断した箇所があれば、その理由と代替案が Comment に残っているか |

### Rv レポートの構成

```markdown
## Claude Rv レポート — PR #NN ([Issue 名])

**総合判定: [合格 / 条件付き合格 / 不合格]**

### 12 観点の Rv 実施結果

| # | 観点 | 結果 |
|---|---|---|
| 1 | [観点] | ✅ [簡潔なコメント] |
| ... |

### 特に評価すべき点

**1. [評価点タイトル]**
[詳細説明、コード例やスクリーンショット引用]

...(3-5 個)

### 改善候補

[あれば箇条書き、なければ「なし」と明記]

### 判断のお願い

[あなた(導入者)判断が必要な項目、あれば箇条書き]
```

### Rv 後の次のアクション

- **合格**: あなた(導入者)承認コメント → 自動マージを促す
- **条件付き合格**: 追加確認事項を Chat で明示
- **不合格**: 修正依頼の内容を明確化、Cursor への指示 or あなた(導入者)判断

## 判断相談フォーマット (案 α / β / γ)

あなた(導入者)への判断を求める際は、必ず以下のフォーマットを使う。

```markdown
### 判断 X: [判断の対象]

- **案 α (Claude 推奨)**: [内容]
  - 理由: [根拠]
  - メリット / デメリット: [説明]
- 案 β: [内容]
  - 理由: [根拠]
- 案 γ: [内容]
  - 理由: [根拠]

Claude 推奨は **案 α** です。

### 判断の理由

[選定理由の詳細、他案との比較]
```

### 複数判断の並列相談

複数の判断を並列で求める場合は、判断 A / B / C として整理し、Claude 推奨の「判断セット」を提示する。

### 憶測禁止

Claude 推奨は必ず具体的な根拠を伴う。憶測ベースの推奨は避ける。あなた(導入者)の価値観 (`00_meta/profile.md`) に照らして判断できない場合は、その旨を明示する。

### 判断保留の管理

あなた(導入者)が即答できない判断は「保留」として明示的にリスト化。次のターンで再確認しない限り、保留状態のまま前進しない。

## Claude Artifacts の活用

以下の場面で積極的に活用する。Chat 内で完結し、外部ツール (Figma / Canva / Photoshop) 依存を最小化する。

- **UI プロトタイプの検討**: HTML/CSS で試作、あなた(導入者)が Chrome で確認
- **OGP 画像や favicon のデザイン**: HTML/CSS or SVG、スクリーンショット化
- **チャート / 図解の作成**: SVG や Mermaid
- **Issue 本文の構造化プレビュー**: Markdown レンダリング
- **リアクティブな判断ツール**: React コンポーネント (過剰な複雑さは避ける)

過度な複雑さは避け、あなた(導入者)の意思決定を支援する範囲に留める。

## トラブルシューティング

### MCP エラー

- 対象プロジェクトの GitHub MCP コネクタが応答しない場合、あなた(導入者)に Railway (または相当のホスティング) デプロイ状況確認を依頼
- 別プロジェクトの MCP コネクタ (例: <your-project><!-- 実例: IPA Sound Drill --> 相談中に `<your-project><!-- 実例: ThinkGrindAi --> GitHub`) を誤って使わないよう注意
- Vault MCP コネクタが応答しない場合は正典 `project_instructions_vault.md` の「Vault MCP コネクタ接続失敗時の処理」に従う

### Issue 起票時のエラー

- ラベルが存在しない場合、あなた(導入者)に GitHub Labels 追加を依頼
- Issue 本文が長すぎる場合 (65,000 字超)、複数 Issue に分割検討
- `create_issue` のパラメータ渡し方はプロジェクト固有の制約あり (`project_instructions.md` の「MCP コネクタ」セクションを参照)

### PR Rv 時の不整合

- `get_pr_diff` で diff が取得できない場合、再実行 or あなた(導入者)に PR 状態確認を依頼
- Cursor 実装レポートに Retrospective がない場合、Cursor に修正依頼 (Issue Comment 経由)
- 12 観点のうち複数が不合格の場合、PR 全体を差し戻すか部分修正で対応するかを あなた(導入者)に相談

### 判断保留の管理

- あなた(導入者)が即答できない判断は「保留」として明示的にリスト化
- 次のターンで再確認しない限り、保留状態のまま前進しない
- 保留が 3 件以上溜まったら、判断整理の Chat を切り出すことを提案する

## 発信素材化への配慮

あなた(導入者)は note / Zenn / Dev.to での発信を計画。以下を意識する。

- **記事化しやすい設計判断**: 選択肢 α / β / γ の比較、Claude 推奨と根拠を Issue 本文の「背景・目的」5 サブセクションに残す
- **実装過程での気づきを Retrospective に残す**: Cursor 実装レポートの「実装過程での気づき」セクションは記事の一次ソース
- **パターン C 適用等の大規模改修の記録**: 大規模改修は特に記事価値が高いので、Phase ごとの決定と経緯を丁寧に残す
- **AI エージェント時代の開発運用体系としての価値**: Claude / Cursor / MCP / Vault の連携パターン自体が発信素材になる
- **他プロジェクトへの応用可能性**: 開発運用パターンの一般化 (このファイル `dev_project_common.md` 自体がその実践)

## 新規ドキュメント作成判定

あなた(導入者)が「〇〇について資料を作りたい」と相談したら、プロジェクト固有の `docs/DOCUMENT-MAP.md`(または相当ファイル)の判定フローを実行し、Category (A-E) 判定と DOCUMENT-MAP.md 更新を Issue 本文に含める。

## 毎回の返答末尾テンプレ

要件整理・議論・仕様作成を行った返答の末尾には、必ず以下を追加する。

```
---
✅ この会話での確定事項
・(箇条書き)

📋 次のアクション(あなた(導入者)がやること)
1. 【ツール名】具体的な作業内容
2. 【ツール名】次の作業

🔧 Claude が次に用意するもの(あれば)
・(次の会話で Claude が作成するもの)
---
```

適用範囲: 当該プロジェクトの相談中のみ(Vault 内の他ケース、note 執筆や汎用ナレッジ等では不要)。

## Vault 記録が必要な場合

重要な意思決定・確定事項が出たら、Vault への記録を あなた(導入者) に提案する。

```
---
🔧 Vault 記録
パス: 30_projects/<RepoName>/design-decisions.md(意思決定確定)
     または 30_projects/<RepoName>/logs/YYYY/MM/YYYY-MM-DD_<topic>.md(議論記録)
     または 30_projects/<RepoName>/handoff/current-state.md(直近状態スナップショット更新)

内容:
# <タイトル>
## 確定事項
-
## 背景・理由
-
## 関連 Issue / PR
-
---
```

保存指示があれば Skill `vault-manager` が発火する。

## Chat 切り出しの判断

Chat が重くなってきたら、あなた(導入者) に切り出しを提案する。切り出し時は以下のパックを .md ファイルで作成する。

```
---
📦 新規 Chat 引き継ぎパック
テーマ: <テーマ>

参照すべきファイル(次 Chat の冒頭で Vault MCP で取得):
- 00_meta/project_instructions_vault.md(正典)
- 00_meta/operations/dev_project_common.md(このファイル)
- 00_meta/profile.md (価値判断軸)
- 30_projects/<RepoName>/project_instructions.md(プロジェクト固有)
- 30_projects/<RepoName>/handoff/current-state.md(直近状態)
- 30_projects/<RepoName>/design-decisions.md
- 30_projects/<RepoName>/open-questions.md

ここまでで確定している技術方針:
- <箇条書き>

新 Chat で詰めるべきこと:
- <箇条書き>

MCP で取得できない情報(あれば):
- <箇条書き、X アカウント / 意思決定の想い / 未確定項目 等>
---
```

切り出しと同時に `30_projects/<RepoName>/handoff/current-state.md` の上部に日付エントリを prepend する。

## 変更履歴

- **v1.0**(2026-07-15): 初版。<your-project><!-- 実例: IPA Sound Drill --> Projects Instructions からの共通化として抽出。適用対象: 開発運用型プロジェクト全般(`applies_common: [dev_project_common]` で発動)。
- **v1.1**(2026-07-15): 旧 <your-project><!-- 実例: IPA Sound Drill --> Projects Instructions から救出した以下 8 項目を集約:
  - コミュニケーション書式 (日/英使い分け、Chat 応答長さ目安、応答の構造)
  - Issue 本文の「改修分類」ブロック (Complexity Level, Change Pattern, 堅固化パターン A/B/C, Claude Rv 要否)
  - Issue 本文の「ブラックリスト md5 検証」ブロック
  - Claude PR Rv フロー (12 観点、Rv レポート構成、判定ルール、Rv 後アクション)
  - 判断相談フォーマット (案 α/β/γ、複数判断並列、判断保留管理)
  - Claude Artifacts の活用シーン
  - トラブルシューティング (MCP エラー、Issue 起票エラー、PR Rv 不整合、判断保留)
  - 発信素材化への配慮 (dedicated section 化)
---
id: pj-2026-05-25-1a01
aliases:
- pj-2026-05-25-1a01
title: Obsidian Vault セットアップガイド
created: '2026-05-25'
---

# Obsidian Vault セットアップガイド

**最終更新**: 2026-05-25

---

## Vault の配置（確定）

| 項目 | 値 |
|------|-----|
| Vault 名 | `ThinkGrindAi` |
| Vault ルート（絶対パス） | `/Users/naoya.k/Documents/Obsidian/ThinkGrindAi` |
| ショートパス | `~/Documents/Obsidian/ThinkGrindAi` |
| ストレージ | ローカル（`~/Documents`） |

**旧配置（廃止）**: iCloud  
`/Users/naoya.k/Library/Mobile Documents/com~apple~CloudDocs/Obsidian/ThinkGrindAi`

> Obsidian の Vault 切り替え画面で親フォルダ `~/Documents/Obsidian` と表示される場合があります。ノート・`ideas/` 等は **`ThinkGrindAi` フォルダ内** に作成してください。

---

## 概要

Naoya の MacBook の Obsidian vault（`ThinkGrindAi`）を以下の構成で整備します。

```
vault/
├── README.md                          ← Vault 概要
├── ideas/                             ← アイデア・要件検討の場
│   ├── REQ-001-thinking.md
│   └── template.md                    ← テンプレ
├── claude-conversations/              ← Claude との議論ログ
│   ├── 2025-01-15-thinking-requirement.md
├── project-status/                    ← プロジェクト進捗
│   ├── weekly-status.md               ← 週単位のサマリ
│   ├── monthly-review.md              ← 月単位の振り返り
│   └── phase-overview.md              ← Phase ごとのマイルストーン
├── design-concepts/                   ← UI/UX、設計アイデア
│   ├── logic-training-flow.md
│   └── thinking-training-ui.md
├── learnings/                         ← 実装で学んだこと・Best Practices
│   ├── gas-optimization.md
│   └── javascript-patterns.md
└── archive/                           ← 完了したアイデア・古い検討
    └── 2024-12-completed-ideas.md
```

---

## フォルダ説明

### 1. `ideas/` — アイデア・要件検討

**目的**: Naoya が思いついたアイデアから、要件確定までの思考過程をすべて記録

#### ファイル構成
```
ideas/
├── template.md                ← テンプレ（新規作成時のひな形）
├── REQ-001-thinking.md        ← 思考トレーニング実装
└── REQ-003-figma-design.md    ← Figma 連携（未定）
```

#### テンプレ: `ideas/template.md`

```markdown
# REQ-XXX: <案件名>

**ステータス**: 検討中 / 確定 / 実装中 / 完了  
**優先度**: 高 / 中 / 低  
**関連**: [[REQ-YYY]] （他のアイデアとの関連）

---

## 背景

（ユーザーのニーズ、なぜこれを実装したいのか）

### 最初のアイデア
- 〇〇がほしい
- △△を改善したい

---

## 検討ログ

### 第 1 ラウンド（2025-01-10）

**Naoya**: 以下の 3 つの案を検討中:
- 案 A: 〇〇する
- 案 B: △△する
- 案 C: □□する

**Claude**: 
- 案 A について：〇〇の理由で 🔴
- 案 B について：△△の利点がある ✅
- 案 C について：□□の課題がある ⚠️

**決定**: 案 B で進める

---

### 第 2 ラウンド（2025-01-15）

**Naoya**: 案 B の詳細を詰める必要がある。以下を決定したい:
- タイプ数（4 種類 or 6 種類）
- レベル数（4 段階 or 5 段階）
- 採点方法（80 点ルール or その他）

**Claude**:
- 論理フレームワークから考えると、△△の理由で「6 種類 × 4 段階」が最適
- 採点は「80 点ルール」を推奨（理由：〇〇）

**Naoya**: 納得。この方針で決定。

---

## 確定事項

### 仕様概要
- **タイプ**: 6 種類（List A）
- **レベル**: 4 段階（初級〜上級）
- **採点**: 80 点/90 点ルール

### 技術的な制約
- GAS の新しいシート「thinking」を追加
- Google Sheets スキーマ拡張が必要
- 既存の gas-script-v3.js に破壊的変更なし

### マイルストーン
- 要件定義書作成: 2025-01-15 ✅
- 仕様書作成: 2025-01-18 ✅
- Cursor 指示書作成: 2025-01-20 予定
- 実装開始: 2025-01-22 予定

---

## 次のステップ

- [ ] Cursor 指示書を作成（Claude）
- [ ] GitHub Issue を作成
- [ ] GAS シート設定を準備
- [ ] js/17-thinking.js の実装開始

---

## リンク・参考

- 🔗 [[docs/requirements-thinking.md]]（要件定義書）
- 🔗 [[docs/specification-thinking.md]]（仕様書）
- 🔗 [[docs/cursor-instructions/cursor_instruction_thinking_v2.md]]（Cursor指示書）
- 🔗 [[GitHub Issues#T001]]（GitHub Issue）
```

#### 使用方法

1. アイデアが出た → `ideas/REQ-XXX.md` を新規作成
2. Naoya と Claude で議論（会話ログを記入）
3. 要件確定 → Obsidian ファイルをリンク → 要件確定シート に記入
4. 完了 → `archive/` に移動

---

### 2. `claude-conversations/` — Claude との議論ログ

**目的**: Naoya と Claude の会話を記録（デバッグ・意思決定の追跡用）

#### ファイル構成

```
claude-conversations/
├── 2025-01-15-thinking-requirement.md
└── 2025-01-18-tsumiaage-discussion.md
```

#### テンプレ

```markdown
# Claude との議論: <話題>

**日時**: 2025-01-15 10:00-12:00  
**関連**: [[ideas/REQ-001-thinking.md]]  
**結果**: 〇〇を決定

---

## 議論内容

**Naoya**: 〇〇について、△△とするべきか、□□とするべきか迷っている

**Claude**: 
背景を確認する質問:
- 〇〇はどのユースケース？
- 既存の実装はどうなっているか？

**Naoya**: 
- ユースケース: 〇〇
- 既存実装: △△

**Claude**:
それであれば、以下の理由で「□□」を推奨:
- 理由 1: 〇〇が〇〇だから
- 理由 2: 既存の△△と矛盾しないから
- 理由 3: パフォーマンス面で有利だから

**結論**: □□の方針で決定

---

## 残された質問

- [ ] GAS の実装方法（Cursor に確認待ち）
- [ ] UI デザイン（Figma 連携時に決定）
```

---

### 3. `project-status/` — プロジェクト進捗

#### `weekly-status.md` （毎週月曜更新）

```markdown
# 週単位の進捗レポート

## Week of 2025-01-20

### 完了したタスク
- [x] 思考トレーニング要件定義完了
- [x] 思考トレーニング仕様書作成
- [x] Cursor指示書 v2 完成
- [x] GAS再デプロイ準備

完了数: 4 件

### 進行中のタスク
- [ ] js/17-18 実装（Cursor実装中）
- [ ] GitHub Projects セットアップ

### 来週の優先タスク
1. 高: js/17-18 実装完了
2. 高: GAS再デプロイ

### ボトルネック・課題
- GAS の複雑さが増している（将来の技術負債候補）
- テスト環境の整備が必要（Phase 3 で検討）

### KPI
- 完了タスク数: 4 / 週（目標: > 5）
- バグ発見数: 2（アクティブテスト中）
- リリース延期: なし ✅
```

#### `monthly-review.md` （毎月末更新）

```markdown
# 月単位の振り返り

## Month of 2025-01

### 成果
- Logic Training Ver.3.2 安定化
- Thinking Training 要件定義 → 仕様書 完成
- GitHub Projects セットアップ開始
- GAS 再デプロイ準備完了

### 学習したこと
- GAS は〇〇の点で限界がある
- テスト環境を整えることの重要性
- アイデア段階での「型」の重要性

### 次月の方針
- Thinking Training 実装に集中（Phase 2）
- GAS トラブル対応に注力
- テスト自動化の基盤構築

### チーム全体への感想
- Claude の指示書作成が改善された
- Cursor の実装速度が上がっている
- Naoya のテスト品質が高い

### 数値
- 完了タスク数: 12 / 月
- バグ検出数: 5
- ドキュメント更新: 3 件
- リリース: Ver.3.2
```

---

### 4. `design-concepts/` — 設計アイデア

**目的**: UI/UX、ロジック設計などのビジュアル・概念を記録

#### ファイル例

```markdown
# Logic Training UI フロー

## 全体フロー

```
[ホーム] 
  → [タブ選択: 穴埋め・要約・批判読み・空雨傘]
  → [難易度選択]
  → [問題表示]
  → [回答入力]
  → [採点・フィードバック]
```

## 穴埋めタブの詳細フロー

[図表や説明を記入]

## ユーザーシナリオ

**シナリオ 1**: ビジネスパーソンが論理的思考を鍛えたい
- 朝 10 分で穴埋めを 2 問解く
- 採点結果を確認
- 弱点を把握

**シナリオ 2**: 学生が試験対策をしたい
- 夜 30 分で複数タブを実施
- 得点を追跡
- 苦手な分野を復習
```

---

### 5. `learnings/` — ベストプラクティス・学習

**目的**: 実装時に発見したテクニック、パターン、トラブルシューティングを記録

#### ファイル例

```markdown
# GAS 最適化パターン

## パターン 1: API 呼び出しのバッチ化

❌ **非効率な例**:
```javascript
for (let i = 0; i < 100; i++) {
  callClaudeMsg(userInput[i]);  // 100 回の API 呼び出し
}
```

✅ **効率的な例**:
```javascript
const batch = userInput.slice(0, 100);
const results = callClaudeMsg(batch.join("\n"));  // 1 回の API 呼び出し
```

## パターン 2: スプレッドシート読み込みの最適化

... （以下、パターン・テクニックを記録）
```

---

## セットアップ手順

### Step 1: Obsidian Vault を開く（または新規作成）

**既に移行済みの場合**: Vault 一覧から `ThinkGrindAi` を選択（ルート: `~/Documents/Obsidian/ThinkGrindAi`）。

**新規作成する場合**:

1. Obsidian を開く
2. **新規 Vault を作成**（またはフォルダを Vault として開く）
3. 名前: `ThinkGrindAi`
4. 場所: `~/Documents/Obsidian/ThinkGrindAi`（ローカル `Documents` 推奨。iCloud は使用しない）

### Step 2: フォルダを作成

Vault 内に以下を作成:

```
mkdir ideas claude-conversations project-status design-concepts learnings archive
```

### Step 3: テンプレプラグインを設定

1. Settings → Community plugins → 「Templater」をインストール
2. Settings → Templater → Folder for templates: `ideas`
3. `ideas/template.md` を新規作成（上記のテンプレを記入）

### Step 4: Daily Notes 設定（オプション）

毎日の進捗メモ用:

1. Settings → Core plugins → Daily notes 有効化
2. 新規作成: `project-status/daily/2025-01-24.md`

### Step 5: 初期ファイルを作成

```
README.md                      ← Vault 概要
project-status/weekly-status.md     ← 今週の進捗
ideas/template.md              ← テンプレ
```

---

## Obsidian プラグイン推奨

| プラグイン | 用途 | 必須度 |
|----------|------|--------|
| **Templater** | テンプレから新規ファイル生成 | ⭐⭐⭐⭐⭐ |
| **Dataview** | Markdown から動的テーブル生成 | ⭐⭐⭐⭐ |
| **Calendar** | 日付ナビゲーション | ⭐⭐⭐ |
| **Outlines** | 大きなファイルのアウトライン表示 | ⭐⭐ |
| **Git** | Vault を自動 Git commit | ⭐⭐ |

---

## Git 連携（GitHub への push）

### Option 1: Obsidian Git プラグイン（自動化）

```
Settings → Community plugins → Obsidian Git
→ Vault を Git repo に初期化
→ 自動 commit・push を設定
```

このプラグインを使えば:
- 毎日自動で Git commit
- GitHub に定期的に push
- 履歴が自動保存される

### Option 2: 手動管理

毎週、以下を実行:

```bash
cd ~/Documents/Obsidian/ThinkGrindAi
git add -A
git commit -m "Weekly update: Week of 2025-01-24"
git push origin main
```

---

## 関連ドキュメント

- 🔗 [PROJECT_CONTEXT.md](./PROJECT_CONTEXT.md) - プロジェクト背景
- 🔗 [[pj-2026-05-24-0b8b|CLAUDE.md]] - 開発ポリシー
- 🔗 [[pj-2026-05-25-45b2|GOOGLE_SHEETS_SETUP.md]] - Google Sheets 設定

---

## Tips

### 検索がしやすいファイル名規則

```
REQ-XXX-<機能名>.md

例:
- REQ-001-thinking-training.md
- REQ-002-tsumiaage-scoring.md
- REQ-003-figma-integration.md
```

### リンク記法

Obsidian の `[[ファイル名]]` でリンク作成:

```markdown
[[REQ-001-thinking-training.md]] - 思考トレーニング
[[docs/specification-thinking.md]] - 仕様書
```

### Dataview で TODO 自動集計

```dataview
task
where file.path contains "ideas"
group by status
```

---

**最後に**: Obsidian は Naoya さんの「思考の可視化」です。完璧な構成より、「自分が使いやすい」ことを最優先にしてください！

---
audience: adopter
created: 2026-07-14 09:10:00+09:00
keywords:
- setup
- claude-projects
- vault-project
- instructions
- thin-instructions
status: published
summary: Claude Projects に Vault Project を作成し、Instructions を「激薄」テンプレで設定する手順。Project
  の目的、Instructions、Custom Instructions、MCP コネクタの割り当てを含む。
tags:
- setup
- claude-projects
title: 05 - Claude Projects の設定
type: setup
updated: 2026-07-14 09:10:00+09:00
id: pj-2026-07-13-19c6
aliases:
- pj-2026-07-13-19c6
---

## Summary

Claude Projects に Vault Project を作成し、Instructions を「激薄」テンプレで設定する手順。Project の目的、Instructions、Custom Instructions、MCP コネクタの割り当てを含む。

## Step 1: Vault Project の作成

### 1.1 Claude Projects ページを開く

1. https://claude.ai にログイン
2. サイドバーの「Projects」→「New project」

### 1.2 Project の基本情報

| 項目 | 推奨値 |
|---|---|
| **Name** | `Vault`(または `<YourName> Vault`) |
| **Description** | 「Chat 集約と Vault 運用の中核」等 |
| **Color / Icon** | 好みで(見分けやすさ) |

### 1.3 Project の作成

「Create project」をクリック。

## Step 2: Instructions の設定

Framework の `project-instructions/vault-project.ja.md` の内容をベースに、Instructions フィールドに以下を入力:

### 2.1 テンプレート取得

- Framework から `project-instructions/vault-project.ja.md` をダウンロード
- または以下の内容をコピー:

```markdown
# Vault - Project Instructions

このプロジェクトは <YourName> の個人 Vault 運用の中核となる Chat 集約先です。

## セッション開始時の必須動作

Skill `vault-manager` が有効な前提で、以下を行います。

1. MCP コネクタ `Vault MCP` が接続されているか確認する
2. 接続されている場合、MCP 経由で `00_meta/project_instructions_vault.md` を読む
3. その内容に従って以降の会話を進める

MCP が接続されていない場合は、その旨を <YourName> に伝え、Skill と userMemories の範囲で対応します。vault からの参照が必要な場面ではその都度「MCP が接続されていないため参照できません」と正直に伝えます。

## この Instructions と vault の役割分担

- **この Instructions(Project 側)**: 最小限のポインタのみ。実質的なルールは持たない
- **vault 内 `00_meta/project_instructions_vault.md`**: セッション全体の運用ルールの正典
- **Skill `vault-manager`**: Claude の振る舞い規約の核心(保存判断、参照判断、あいまい名解決)

3 者の内容が矛盾したら、優先順位は Skill > vault > Instructions とする。ただし通常は矛盾しないよう管理する。
```

### 2.2 プレースホルダの置換

- `<YourName>` → あなたの名前
- `Vault MCP` → あなたの MCP コネクタ表示名(通常は `Vault MCP` のまま)

### 2.3 Instructions フィールドに入力

- 上記内容を Claude Projects の Instructions フィールドに貼り付け
- 「Save」または自動保存を確認

## Step 3: Custom Instructions(オプション)

Chat 全体のスタイル指示がある場合、Custom Instructions フィールドに追加:

- 例: 「日本語で返答してください」
- 例: 「技術的な説明は詳細に、雑談は簡潔に」
- 例: 「保存指示があった場合、Skill の判断で保存し、報告は最小限に」

これは激薄 Instructions と補完的に使う。

## Step 4: MCP コネクタの割り当て

### 4.1 Project の Connectors 設定

1. Vault Project 内で新規 Chat を開始
2. Chat 画面の「Tools」または「Connectors」アイコンをクリック
3. `Vault MCP` を **ON** にする

### 4.2 デフォルト有効化

- Project のデフォルト設定として `Vault MCP` を ON にすると、すべての Chat で自動的に接続
- Claude Pro の設定によっては、Chat ごとに ON/OFF を選択

## Step 5: Skill の有効化確認

Skill `vault-manager` は Skills でアップロード済みなら、この Project でも自動的に発火します。

追加設定は不要ですが、Project 内で Skill が発火しない場合:

- 新規 Chat を開始
- Skills 一覧で `vault-manager` が Enabled か確認

## Step 6: 動作確認

### 6.1 セッション開始時の挙動

新規 Chat を開始し、以下を発話:

```
「Vault の運用ルールを教えて」
```

期待する挙動:

- Skill が発火
- MCP 経由で `00_meta/project_instructions_vault.md` を取得
- その内容に基づいて運用ルールを説明

### 6.2 MCP コネクタ確認

もし MCP が未接続の状態で発話:

- Claude が「Vault MCP が接続されていません」と伝える
- 憶測や訓練データで補わない(ADR-0016)

## Step 7: 他 Project の考察

Vault 以外に用途別 Project を作る場合:

- **推奨**: 1 Project(`Vault`)に統合(ADR-0013)
- **例外**: 
  - チームメンバーとの共有 Project(将来)
  - 特定の作業用 Project(実験、テスト等)
  - 業務用と個人用の分離

Naoya のパターンでは 1 Project(`Vault`)で運用しています。あいまい名解決フローで用途を判定するため、Project 分割は基本不要です。

## Troubleshooting

### Instructions が反映されない

- Chat を新規で開始(既存 Chat では Instructions 変更が反映されない場合あり)
- Instructions フィールドの保存を確認

### Skill が発火しない

- Skill が Enabled か確認
- 発火 phrase が Instructions と整合しているか

### MCP が接続されない

- Connectors ページで `Vault MCP` の Status を確認
- Worker のログ(`wrangler tail`)でリクエスト到達を確認

## Next Step

Vault Project の設定が完了したら [[pj-2026-07-13-9c97|06-first-save-test.md]] で初回保存動作を確認します。

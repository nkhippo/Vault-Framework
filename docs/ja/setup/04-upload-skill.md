---
audience: adopter
created: 2026-07-14 09:05:00+09:00
keywords:
- setup
- skill
- upload
- claude-skills
- zip
- front-matter
status: published
summary: Framework の skills/vault-manager/SKILL.md を Claude Skills にアップロードする手順。Skill
  パッケージの取得、Front Matter の確認、zip 化、Claude Settings > Skills でのアップロード、動作確認までを含む。
tags:
- setup
- skill-upload
title: 04 - Skill のアップロード
type: setup
updated: 2026-07-14 09:05:00+09:00
id: pj-2026-07-13-ff6f
aliases:
- pj-2026-07-13-ff6f
---

## Summary

Framework の `skills/vault-manager/SKILL.md` を Claude Skills にアップロードする手順。Skill パッケージの取得、Front Matter の確認、zip 化、Claude Settings > Skills でのアップロード、動作確認までを含む。

## Step 1: SKILL.md の取得

### 方法 A: Framework からダウンロード

1. https://github.com/nkhippo/Vault-Framework/tree/main/skills/vault-manager にアクセス
2. `SKILL.md` を右クリックして「Save as」または「Download」
3. `README.ja.md` も同様にダウンロード

### 方法 B: Framework を clone してコピー

```bash
git clone https://github.com/nkhippo/Vault-Framework.git /tmp/vault-framework
cp -r /tmp/vault-framework/skills/vault-manager ~/Downloads/
```

## Step 2: SKILL.md の Front Matter 確認

`SKILL.md` の先頭を開き、Front Matter が以下の 2 フィールドのみか確認:

```yaml
---
name: vault-manager
description: Use this skill when the user asks to save chat content to the personal Vault repository...
---
```

**注意事項**:

- `updated` フィールドが自動付与されている場合、削除する
- 他の Vault 用 Front Matter(created、type、status 等)が混ざっていたら削除
- Claude Skills は純粋な形式(name + description)を要求

### 削除方法(Mac の場合)

エディタ(TextEdit、VS Code、Obsidian 等)で開き、`updated:` の行を削除して保存。

または `sed` コマンド:

```bash
sed -i '' '/^updated: /d' ~/Downloads/vault-manager/SKILL.md
```

## Step 3: zip 化

Skill パッケージを zip 化します:

### macOS(Finder)

1. Finder で `vault-manager` フォルダを開く
2. フォルダごと選択
3. 右クリック → 「圧縮」
4. `vault-manager.zip` が生成される

### macOS(コマンドライン)

```bash
cd ~/Downloads
zip -r vault-manager.zip vault-manager/
```

### Windows

1. エクスプローラーで `vault-manager` フォルダを選択
2. 右クリック → 「送る」→ 「圧縮 (zip 形式) フォルダー」

### Linux

```bash
cd ~/Downloads
zip -r vault-manager.zip vault-manager/
```

## Step 4: Claude Skills へのアップロード

### 4.1 Skills ページを開く

1. https://claude.ai にログイン
2. Settings(左サイドバー)→ Skills
3. 「Add new skill」または「Upload skill」ボタンをクリック

### 4.2 zip ファイルを選択

- Step 3 で生成した `vault-manager.zip` を選択
- 「Upload」または「Add」をクリック

### 4.3 Skill の確認

- Skill 一覧に `vault-manager` が追加される
- 状態が「Active」または「Enabled」になる

## Step 5: 動作確認

### 5.1 発火テスト

新規 Chat を開始し、Skill 発火のトリガーを発話:

```
「テストです。この内容を Vault に保存してください」
```

### 5.2 期待する挙動

- Skill `vault-manager` が発火(Claude の内部で発火判定)
- Claude が保存判断フロー(save-decision-flow.md)に従って対応
- ただし、MCP コネクタが有効な Chat でないと保存自体は実施されない

### 5.3 Skill 判定の確認

Claude の応答から Skill が発火しているか確認:

- 発火時: 「Vault に保存します。判断: chat_log として 10_chat_logs/YYYY/MM/ に保存」等
- 発火なし: 通常の Chat 応答(Skill の判断フローに触れない)

## Step 6: バージョン管理

Skill を更新する場合の運用:

### 6.1 差し替え手順

1. 既存の `vault-manager` を Delete
2. 新しい `vault-manager.zip` を Upload
3. 動作確認

### 6.2 バージョン履歴

- Framework 側の `skills/vault-manager/SKILL.md` を Git 履歴で管理
- 各バージョンのタグ付け(v1.0、v1.1 等)
- Change Log を SKILL.md 内で管理

### 6.3 Vault 側での canonical 管理

- Naoya のパターン: `nkhippo/Vault/30_projects/Vault-Framework/skills/vault-manager/SKILL.md` を canonical として保持
- iCloud 経由で zip 化してアップロードするワークフロー

## Troubleshooting

### アップロード時に「Front Matter が無効」エラー

- SKILL.md の Front Matter を確認(`name` と `description` のみが必要)
- `updated` や他のフィールドが混じっていたら削除
- YAML 記法の誤りがないか確認(コロン、インデント等)

### Skill が発火しない

- description の内容を確認(トリガー phrase が含まれているか)
- Skill 一覧で「Enabled」状態か確認
- Chat を新規で開始(既存 Chat では Skill 定義変更が反映されない場合あり)

### 予期しない発火

- description が広すぎる可能性
- Framework の SKILL.md の description は「Vault に保存」等の明示的トリガーを含む形にチューニング済み

## Next Step

Skill のアップロードが完了したら [05-configure-project.md](./05-configure-project.md) で Claude Projects の Vault Project を作成します。

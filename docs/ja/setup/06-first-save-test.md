---
audience: adopter
created: 2026-07-14 09:15:00+09:00
keywords:
- setup
- first-save
- test
- verification
- ambiguous-name
- front-matter
status: published
summary: Vault-Framework の全セットアップ完了後、初回の Chat 保存と参照を実施して動作を確認する手順。保存、Front Matter
  確認、参照、あいまい名解決までを含む。
tags:
- setup
- first-save
- verification
title: 06 - 初回保存テスト
type: setup
updated: 2026-07-14 09:15:00+09:00
id: pj-2026-07-13-9c97
aliases:
- pj-2026-07-13-9c97
---

## Summary

Vault-Framework の全セットアップ完了後、初回の Chat 保存と参照を実施して動作を確認する手順。保存、Front Matter 確認、参照、あいまい名解決までを含む。

## Prerequisites

以下がすべて完了していることを確認:

- [ ] vault リポジトリが GitHub に存在
- [ ] Vault-MCP が Cloudflare Workers にデプロイ済み
- [ ] Claude Pro Connectors に `Vault MCP` が登録済み
- [ ] Claude Skills に `vault-manager` がアップロード済み
- [ ] Claude Projects に Vault Project が作成済み
- [ ] Vault Project で MCP コネクタが ON

## Step 1: 初回保存テスト

### 1.1 Chat の開始

- Vault Project 内で新規 Chat を開始
- 発話: 

```
初回保存テストです。以下を chat_log として保存してください。

## テスト内容

これは Vault-Framework の初回動作確認 Chat です。

- Framework の導入手順を実施
- MCP コネクタと Skill が稼働することを確認
- 保存動作が正常であることを確認
```

### 1.2 期待する挙動

- Skill が発火(chat_log として判定)
- Skill が保存先を判定(`10_chat_logs/YYYY/MM/YYYY-MM-DD_first-save-test.md` 等)
- MCP 経由で保存
- 保存完了の報告(パス、type、summary)

### 1.3 応答例

```
保存しました。
- パス: 10_chat_logs/2026/07/2026-07-14_first-save-test.md
- タイプ: chat_log
- 概要: Vault-Framework の初回動作確認 Chat
- コミット URL: https://github.com/<YourGitHubUsername>/<VaultRepoName>/commit/xxxxxx
```

## Step 2: 保存内容の確認

### 2.1 GitHub 上での確認

1. https://github.com/<YourGitHubUsername>/<VaultRepoName> にアクセス
2. `10_chat_logs/2026/07/` に移動
3. 保存されたファイルを確認

### 2.2 Front Matter の確認

保存されたファイルの Front Matter が以下のようになっているか:

```yaml
---
title: 初回保存テスト
created: 2026-07-14T XX:XX:XX+09:00
updated: 2026-07-14T XX:XX:XX+09:00
type: chat_log
status: published
tags: [test, first-save]
summary: <2-4 行の要約>
source_chat_date: 2026-07-14
---
```

### 2.3 本文の確認

- Summary セクションが最初にあること
- 本文が構造化されていること
- Chat の内容が正しく反映されていること

## Step 3: 参照テスト

### 3.1 保存内容の再取得

同じ Chat で以下を発話:

```
今保存したファイルを get_file_content で読み返してください
```

### 3.2 期待する挙動

- MCP 経由で保存済みファイルを取得
- Front Matter + 本文が返る

## Step 4: あいまい名解決テスト

### 4.1 プロジェクトエイリアス確認

事前に `00_meta/project_aliases.md` に少なくとも 1 プロジェクトを登録済みか確認:

```markdown
### <YourProject>

- 正式リポジトリ名: `<YourProject>`
- 通称: <通称>
- 機能キーワード: <キーワード>
...
```

### 4.2 あいまい名で参照

Chat で以下のように発話:

```
「<通称>」の設計について相談したい
```

### 4.3 期待する挙動

- Skill があいまい名解決フローを発火
- `project_aliases.md` を参照
- 該当プロジェクト(`<YourProject>`)を特定
- 「<YourProject> の情報を読みますね」等の応答
- Level 2 参照に遷移(該当プロジェクトの README、design-decisions 等を読む)

### 4.4 該当プロジェクトのファイルがまだない場合

- Skill が「30_projects/<YourProject>/ が存在しません」と伝える
- 「新規プロジェクトとして作成しますか?」と提案

## Step 5: 統制語彙違反テスト

### 5.1 意図的な違反を作る

以下のように発話:

```
これを「ChatLog」type で保存してください
```

### 5.2 期待する挙動

- Skill が Level 1 の自動修正で `ChatLog` → `chat_log` に補正
- 保存は正常に完了
- 応答で「type を chat_log に補正しました」等の一言

## Step 6: MCP 接続失敗テスト(オプション)

### 6.1 意図的にコネクタを OFF

Chat の Connectors 設定で `Vault MCP` を **OFF** にする。

### 6.2 保存指示

```
これを Vault に保存してください
```

### 6.3 期待する挙動

- Skill が MCP 接続の欠如を検出
- 「Vault MCP が接続されていません」と伝える
- 憶測での保存を実施しない(ADR-0016)
- Naoya に判断を仰ぐ

### 6.4 復旧確認

- Connectors 設定で `Vault MCP` を再度 ON にする
- 保存指示を再度発話
- 正常に保存されることを確認

## Step 7: 動作確認完了

以下がすべて確認できたら、初回動作テスト完了:

- [ ] chat_log の保存が正常に動作
- [ ] Front Matter が正しく生成
- [ ] 保存内容の参照が正常に動作
- [ ] あいまい名解決フローが動作
- [ ] 統制語彙違反の自動修正が動作
- [ ] MCP 接続失敗時に適切に対応(オプション)

## Troubleshooting

### 保存が失敗する

- MCP コネクタが接続されているか確認
- Fine-grained PAT の権限を確認(Contents R/W)
- Cloudflare Worker のログ(`wrangler tail`)を確認

### Skill が発火しない

- Skill `vault-manager` が Enabled か確認
- 明示的な保存指示 phrase を使用(「Vault に保存」等)

### Front Matter が不正

- vocabulary.md の type/status が最新か確認
- Skill の Front Matter 生成ロジックを確認

## Next Step

初回動作テストが完了したら、日常運用が可能です。以下を参考にしてください:

- [customization.md](./customization.md) - 拡張・カスタマイズの手順
- [troubleshooting.md](./troubleshooting.md) - 問題解決とトラブルシューティング
- Framework の [guidelines/](../guidelines/) - 運用原則

Naoya の運用パターンをそのまま真似するか、自分の運用に合わせて段階的にカスタマイズしてください。

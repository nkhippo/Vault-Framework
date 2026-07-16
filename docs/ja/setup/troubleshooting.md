---
audience: adopter
created: 2026-07-14 09:25:00+09:00
keywords:
- setup
- troubleshooting
- problems
- solutions
- faq
- common-issues
status: published
summary: Vault-Framework の運用中によく発生する問題と解決策。MCP 接続、認証、Skill 発火、Front Matter、命名衝突、コスト等の問題を扱う。
tags:
- setup
- troubleshooting
title: トラブルシューティング
type: setup
updated: 2026-07-14 09:25:00+09:00
id: pj-2026-07-13-e32c
aliases:
- pj-2026-07-13-e32c
---

## Summary

Vault-Framework の運用中によく発生する問題と解決策。MCP 接続、認証、Skill 発火、Front Matter、命名衝突、コスト等の問題を扱う。

## Problem 1: MCP コネクタが接続失敗する

### 症状

- Chat で保存指示を出しても「Vault MCP に接続できません」等のエラー
- Claude Pro Connectors ページで Status が「Connection failed」

### 診断

1. **Cloudflare Worker の稼働確認**:

```bash
curl https://vault-mcp.<your-subdomain>.workers.dev/
```

期待: 200 OK または MCP プロトコルの応答

2. **wrangler tail でリアルタイムログ**:

```bash
wrangler tail
```

Chat で接続を試して、リクエスト到達を確認

3. **Connectors ページで URL 確認**:
   - URL 末尾の `/` の有無
   - スペルミス

### 解決策

- **URL 誤り**: Connectors 設定を修正
- **Worker デプロイ失敗**: `wrangler deploy` を再実行
- **認証エラー**: `MCP_ACCESS_TOKEN` を再登録
- **Rate limit**: しばらく待って再試行

### 恒久対策

- Worker のヘルスチェック用エンドポイントを追加
- Cloudflare Dashboard で稼働状況を定期監視

## Problem 2: Skill が発火しない

### 症状

- 「Vault に保存」と発話しても Skill の判断フローが動かない
- 通常の Chat 応答として処理される

### 診断

1. **Skill の Enabled 状態**:
   - Claude Settings > Skills で `vault-manager` が Enabled か確認

2. **発火 phrase の確認**:
   - description 内のトリガー phrase を確認
   - Chat の発話に含まれているか

3. **新規 Chat での確認**:
   - 既存 Chat では反映されない場合あり
   - 新規 Chat で試す

### 解決策

- **Enabled でない**: Skills ページで有効化
- **description との乖離**: 発話 phrase を description に合わせる
- **キャッシュ問題**: 新規 Chat を開始

### 恒久対策

- Framework の canonical SKILL.md を使用
- 発火 phrase を自分の口癖に合わせて拡張(SKILL.md 編集)

## Problem 3: Front Matter エラー

### 症状

- 「Front Matter が無効」等のエラー
- 保存されたファイルの Front Matter が壊れている

### 診断

1. **YAML 記法の確認**:
   - コロン `:` の後にスペース
   - インデントは半角スペース(タブは NG)
   - 特殊文字は quote

2. **必須フィールドの確認**:
   - `title`, `created`, `updated`, `type`, `status` があるか

3. **統制語彙の確認**:
   - `type`, `status` が vocabulary.md に登録済みか

### 解決策

- **YAML 記法エラー**: 手動修正 or Skill 側の生成ロジックを見直し
- **必須フィールド欠如**: Skill の Level 1 自動補完で対応
- **統制語彙違反**: Level 1 の自動修正 or vocabulary.md に追加

### 恒久対策

- Framework の frontmatter_schema.md 準拠のテンプレを使用
- Level 1 保守運用で自動修正を有効化

## Problem 4: 命名衝突(HashiCorp Vault 等)

### 症状

- リポジトリ名 `Vault` が GitHub 検索で HashiCorp Vault と混じる
- Public 化した時に第三者が混同する

### 診断

- リポジトリ名を確認
- 既存の他プロダクトとの類似度を確認

### 解決策

- **Private のうちは無視**: 実害ゼロ
- **Public 化前に改名**:
  - `<YourName>-Vault`
  - `Personal-Vault`
  - `Knowledge-Vault`
  - 独自ブランド名

### 恒久対策

- 初期セットアップ時に命名を慎重に選ぶ(01-fork-vault-templates.md 参照)

## Problem 5: iCloud 同期が遅い

### 症状

- Obsidian で編集した内容が Claude に反映されない
- 「更新した」と伝えても古い内容が返る

### 診断

1. **iCloud 同期状態の確認**:
   - macOS: Finder で該当フォルダの同期アイコンを確認
   - 「今すぐダウンロード」を強制実施

2. **Git 状態の確認**:

```bash
cd <VaultRepoPath>
git status
```

3. **GitHub での確認**:
   - 最新コミットが反映されているか

### 解決策

- **iCloud 遅延**: 数分〜数十分待つ、または強制同期
- **Git push 未実施**: `git push origin main` を実施
- **キャッシュ問題**: Claude に「vault の最新版を取得して」と明示

### 恒久対策

- 大きな編集後は必ず `git push`
- Claude MCP は GitHub API 経由なので、GitHub 反映後は即座に見える

## Problem 6: コスト超過

### 症状

- Cloudflare Workers の Free 枠を超過
- Claude Pro のトークン制限に達する

### 診断

1. **Workers リクエスト数**:
   - Cloudflare Dashboard で Requests / day を確認

2. **Claude API 使用量**:
   - Claude Pro の Usage を確認

### 解決策

- **Workers 超過**: Paid プラン($5/月)に移行、または利用パターンを見直し
- **Claude 過剰使用**: 過剰参照(Level 0 違反)を確認、Skill 側の判定を厳格化

### 恒久対策

- Level 0(参照しない)をデフォルトに徹底
- 過去 Chat の履歴で参照していたからと言って、今の Chat でも参照するのを避ける
- prompt caching を活用(固定順序の維持)

## Problem 7: sensitive 領域の意図しない引用

### 症状

- diary/50_self/ の内容が他 Chat で引用される
- Claude が個人的な内容を要約してしまう

### 診断

- Skill の sensitive ルール実装確認
- 該当ファイルの Front Matter で `sensitive: true` が設定されているか

### 解決策

- **Front Matter 修正**: `sensitive: true` を明示
- **Skill 更新**: sensitive 引用禁止ルールを再確認
- **Chat の途中で気づいた場合**: Naoya が「今の話は sensitive、引用しないで」と明示

### 恒久対策

- diary/reflection/goal は Skill が自動的に sensitive: true 付与
- 50_self/ 配下のファイルは全て sensitive 扱い

## Problem 8: 過去 Chat の wikilink 切れ

### 症状

- 旧命名(例: `Obsidian-Vault-MCP` → `Vault-MCP`)への wikilink が指し先を見つけられない
- リネーム後の過去 chat_log から参照が切れる

### 診断

- 過去 chat_log 内の wikilink を確認
- 現行の命名との差分を把握

### 解決策

- **一括書き換え**: Cursor 委譲で wikilink を一括更新
- **手動修正**: 気づいた時に随時修正

### 恒久対策

- リネーム時に事前に wikilink 書き換え計画を作成
- Level 4 季節補正で wikilink 整合性チェック

## Problem 9: Vault-MCP の Rate Limit

### 症状

- 「Too many requests」エラー
- 連続保存で失敗が発生

### 診断

- Cloudflare Workers の Rate limit(Free: 100k req/day)
- GitHub API の Rate limit(Fine-grained PAT: 5000 req/hour)

### 解決策

- **一時的なエラー**: しばらく待って再試行
- **恒常的な超過**: Paid プランへの移行、または利用パターンの見直し

### 恒久対策

- 一括操作は Cursor 委譲(単発 Claude → 単発 MCP call ではなく、Cursor で一気に実施)
- Phase 3.1 のトークン節約系ツールを活用(get_frontmatter で無駄な full read を回避)

## Problem 10: 「Vault MCP が接続されているのに情報が古い」

### 症状

- Claude が古い内容で応答する
- 最新の chat_log が参照されない

### 診断

- Claude の同一 Chat 内キャッシュを確認(Chat 内で一度読んだファイルは再取得しない)
- prompt caching の影響で古い状態が保持されている可能性

### 解決策

- **同一 Chat 内での再取得**: 「最新版を再取得して」と明示
- **新規 Chat**: Chat を新規で開始
- **明示的な更新指示**: Naoya が「vault を更新した」と伝える

### 恒久対策

- 大きな編集後は新規 Chat で開始
- prompt caching の設計思想を理解(reference-level-system.md 参照)

## Getting Help

問題が解決しない場合:

- Framework の Issues に報告: https://github.com/nkhippo/Vault-Framework/issues
- コミュニティ(将来的な Discord 等)で相談
- Naoya のパターンを参考にする(Naoya の Vault は Private のため直接参照不可)

## Reference

- **関連 ADR**: 
  - [[pj-2026-07-13-e19b]](MCP 接続失敗ルール)
  - [[pj-2026-07-13-9107]](PAT のセキュリティ)
- **関連 spec**: 
  - [[pj-2026-07-13-dd44]](Level の適切な使用)
  - [[pj-2026-07-13-d0dd]](保守運用による問題予防)
- **関連 guideline**: 
  - [[pj-2026-07-13-fba6]](運用の原則)

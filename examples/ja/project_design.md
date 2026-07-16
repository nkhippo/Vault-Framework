---
created: 2026-07-13 22:20:00+09:00
example_of_type: project_design
keywords:
- example
- project_design
- design-decisions
- mcp-server
- cloudflare-workers
- fine-grained-pat
project: <your-mcp-project>
related: []
status: published
summary: project_design type の記入例。MCP サーバプロジェクトの design-decisions.md ファイルを題材にした設計判断の逆完例。プロジェクトごとに
  1 つ配置し、値射型の設計判断をリスト化する。
tags:
- example
- project_design
- design-decision
- mcp
title: '例: MCP サーバ設計上の意思決定'
type: example
updated: 2026-07-13 22:20:00+09:00
id: pj-2026-07-13-72b8
aliases:
- pj-2026-07-13-72b8
---

## Summary

MCP サーバプロジェクト全体の設計・意思決定を集約するファイルの例。導入者のリポジトリごとに 1 つずつ配置する `design-decisions.md` の構造・粒度を示す。

**この例が示す構造**: project_design type の標準構造(Summary → 意思決定リスト、各決定は日付・内容・理由・影響範囲)。project フィールドは対象リポジトリ名と一致。

## 意思決定 1: プラットフォームに Cloudflare Workers を採用

- **決定日**: 2026-07-13
- **決定内容**: MCP サーバのホスティングプラットフォームを Cloudflare Workers に決定
- **背景・理由**:
  - MCP はコールドスタート時間が UX に直結する対話系ワークロード
  - Workers は実質 0ms のコールドスタート
  - 個人利用の無料枠(100k req/day)が十分
  - `wrangler.toml` + `secrets` の運用がシンプル
- **影響範囲**: MCP サーバの実装スタック全体、デプロイ手順、コスト構造

**却下した案**: Google Cloud Run(コールドスタート数秒がネック)、Fly.io / Railway(常時稼働型はオーバー)。詳細は関連 chat_log 参照。

## 意思決定 2: Fine-grained PAT を採用

- **決定日**: 2026-07-13
- **決定内容**: GitHub API アクセスに Fine-grained Personal Access Token を採用し、権限を対象リポジトリの `Contents R/W` のみに限定
- **背景・理由**:
  - Classic PAT はスコープが粗く、事故時の被害範囲が大きい
  - Fine-grained PAT は特定リポジトリ + 特定権限に限定できる
  - MCP サーバは vault リポジトリしか触らないため、それ以外の権限は不要
- **影響範囲**: 認証設計、シークレット管理、事故時の被害範囲

## 意思決定 3: main ブランチ直接コミット運用(個人利用の場合)

- **決定日**: 2026-07-13
- **決定内容**: MCP からの操作は main ブランチに直接コミットする
- **背景・理由**:
  - 個人利用では PR ベースのオーバーヘッドが大きい
  - 全操作が GitHub のコミット履歴に残り、SHA で追跡可能
  - デグレ時は revert で対応
- **影響範囲**: 保存・更新・削除の運用フロー
- **注意**: チーム利用に発展する場合は PR ベースへの移行を要検討

## 意思決定 4: 同名ファイル存在時はエラー返却(強制上書き禁止)

- **決定日**: 2026-07-13
- **決定内容**: `create_note` は同名ファイルが既存の場合、エラーを返す。強制上書きはしない
- **背景・理由**:
  - AI 判断による意図しない上書きを防ぐ
  - 上書き必要時は明示的に `update_note` を呼ぶ運用に統一
- **影響範囲**: 保存 API の挙動、Skill の判断ロジック

## 意思決定 5: Phase 1+2 で最小 5 ツール実装

- **決定日**: 2026-07-13
- **決定内容**: Phase 1+2 では `list_directory`, `get_file_content`, `create_note`, `update_note`, `delete_note` の 5 ツールを実装
- **背景・理由**:
  - この 5 つで vault の基本操作(読み書き削除)が完結
  - 拡張(検索、Issue 起票、抽象生成等)は Phase 3 以降
- **影響範囲**: 初期実装スコープ、テストカバレッジ、依存 SDK 選定

## 関連

- [[30_projects/<your-mcp-project>/README.md]]
- [[30_projects/<your-mcp-project>/open-questions.md]]
- [[10_chat_logs/YYYY/MM/YYYY-MM-DD_platform-selection.md]]

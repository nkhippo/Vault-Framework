---
created: 2026-07-13 22:35:00+09:00
keywords:
- examples
- staging
- readme
- framework-mirror
project: Vault-Framework
status: published
summary: examples/ja/ の staging area の説明。Framework へのミラーの canonical source を格納し、実データベースの記入例を
  4 type 分提供。
tags:
- framework
- examples
- staging
title: Vault-Framework examples staging README
type: knowledge
updated: 2026-07-13 22:35:00+09:00
id: pj-2026-07-13-ca82
aliases:
- pj-2026-07-13-ca82
---

## Summary

Framework の各 type ごとに、実際にどう記入するかの実データベース例を格納する staging area。導入者は Framework の zip または MCP 経由でこれらを参照し、Front Matter の埋め方や本文構造の粒度を把握する。

## ファイル一覧

| ファイル | 対応 type | 題材 |
|---|---|---|
| `chat_log.md` | chat_log | MCP プラットフォーム選定の議論 |
| `project_design.md` | project_design | MCP サーバ設計上の意思決定集 |
| `handoff-current-state.md` | handoff | MCP プロジェクトの current-state.md |
| `knowledge.md` | knowledge | Cloudflare Workers で MCP 実装の学び |

## 例の性質

- **実データベース**: Vault-Framework の設計・実装過程で実際に議論・記録した内容から作成
- **個人情報伏せ**: 導入者固有の名前・プロジェクト名は `<your-*>` プレースホルダに置換
- **技術情報は保持**: 意思決定の理由や技術的な学びは、導入者にとって参考になる粒度で残す
- **文脈は独立**: 個別の Chat 履歴や関連ファイル参照は最小限にし、各ファイル単体で読める粒度に

## Framework 側の受け側

Framework の `examples/ja/` は現在 Cursor により scaffold(空の Front Matter + TODO)が配置されている。ミラー時にこれらを本 canonical で置換する。

## ミラー先

- Source: `nkhippo/Vault/30_projects/Vault-Framework/examples/ja/`(このディレクトリ)
- Destination: `nkhippo/Vault-Framework/examples/ja/`

## 関連

- 進捗管理: [[30_projects/Vault-Framework/handoff/current-state.md]]
- 同パターンで配置済み: `30_projects/Vault-Framework/skills/vault-manager/`(SKILL.md canonical)、`30_projects/Vault-Framework/vault-templates/`(vault-templates staging)

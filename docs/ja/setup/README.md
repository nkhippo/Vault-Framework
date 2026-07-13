---
title: 導入手順の概要
title_en: Setup Overview
type: index
audience: human_primary
status: draft
date: 2026-07-13
keywords: [overview, setup, 全体, 導入]
summary: Vault-Framework 導入フロー全体の概要と各ステップへの入り口。
---

## Summary

<!-- TODO: 導入フロー全体の概要を書く -->

## ステップ一覧

| Step | ファイル | 内容 | 目安 |
|---|---|---|---|
| 0 | [00-prerequisites.md](./00-prerequisites.md) | 前提条件 | 10 分 |
| 1 | [01-fork-vault-templates.md](./01-fork-vault-templates.md) | vault-templates を自 GitHub に配置 | 15 分 |
| 2 | [02-deploy-mcp-server.md](./02-deploy-mcp-server.md) | MCP サーバを Cloudflare Workers にデプロイ | 30 分 |
| 3 | [03-configure-mcp-connector.md](./03-configure-mcp-connector.md) | Claude Pro Connectors に MCP を追加 | 10 分 |
| 4 | [04-upload-skill.md](./04-upload-skill.md) | Skill を Claude アカウントにアップロード | 10 分 |
| 5 | [05-configure-project.md](./05-configure-project.md) | Claude Projects で Vault Project を作成 | 10 分 |
| 6 | [06-first-save-test.md](./06-first-save-test.md) | 初回保存テスト | 15 分 |

## 追加ガイド

- [customization.md](./customization.md) - カスタマイズ
- [troubleshooting.md](./troubleshooting.md) - トラブルシューティング

## 想定所要時間

<!-- TODO: 全体の所要時間目安を書く(目安: 合計 約 100 分) -->

## Troubleshooting

失敗パターンと対処: [troubleshooting.md](./troubleshooting.md)

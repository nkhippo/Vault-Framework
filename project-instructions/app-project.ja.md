---
title: App Project Instructions (激薄テンプレ・日本語)
type: template
audience: human_primary
status: draft
date: 2026-07-13
keywords: [app-project, instructions, template, ja, thin]
summary: 特定アプリ用 Claude Project の Instructions 激薄テンプレ。
---

# App Project Instructions テンプレ(日本語版)

以下を Claude Projects の Instructions フィールドに貼り付けて使用する。

---

```
# <アプリ名> - Project Instructions

このプロジェクトは <アプリ名> の設計・実装相談を集約します。

## セッション開始時の必須動作

1. MCP コネクタ `Vault MCP` が接続されているか確認する
2. 接続されている場合、vault の該当プロジェクトフォルダ `30_projects/<アプリ名>/` を読む
3. 特に `handoff/current-state.md` があれば優先して把握する

## 役割分担

- **この Instructions**: 最小限のポインタのみ
- **vault 側プロジェクトフォルダ**: 設計・論点・handoff の正典
- **Skill `vault-manager`**: 保存・参照・あいまい名解決
```

## カスタマイズポイント

- `<アプリ名>`: 対象アプリの正式名

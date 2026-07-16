---
title: Vault Project Instructions (激薄テンプレ・日本語)
type: template
audience: human_primary
status: published
date: 2026-07-13
keywords:
- vault-project
- instructions
- template
- ja
- thin
summary: Claude Projects の Vault プロジェクト用 Instructions の激薄テンプレ。
id: pj-2026-07-13-ea8e
aliases:
- pj-2026-07-13-ea8e
---

# Vault Project Instructions テンプレ(日本語版)

以下を Claude Projects の Instructions フィールドに貼り付けて使用する。`<your-*>` プレースホルダは自分の値に置換する。

---

```
# Vault - Project Instructions

このプロジェクトは <your-name> の個人 vault 運用の中核となる Chat 集約先です。

## セッション開始時の必須動作

Skill `vault-manager` が有効な前提で、以下を行います。

1. MCP コネクタ `Vault MCP` が接続されているか確認する
2. 接続されている場合、MCP 経由で `00_meta/project_instructions_vault.md` を読む
3. その内容に従って以降の会話を進める

MCP が接続されていない場合は、その旨を <your-name> に伝え、Skill と userMemories の範囲で対応します。
vault からの参照が必要な場面ではその都度「MCP が接続されていないため参照できません」と正直に伝えます。

## この Instructions と vault の役割分担

- **この Instructions(Project 側)**: 最小限のポインタのみ。実質的なルールは持たない
- **vault 内 `00_meta/project_instructions_vault.md`**: セッション全体の運用ルールの正典
- **Skill `vault-manager`**: Claude の振る舞い規約の核心(保存判断、参照判断、あいまい名解決)

3 者の内容が矛盾したら、優先順位は Skill > vault > Instructions とする。ただし通常は矛盾しないよう管理する。
```

## カスタマイズポイント

- `<your-name>`: 自分の名前
- `Vault MCP`: 自分の MCP コネクタ表示名(変えている場合)
- `vault-manager`: 自分の Skill 名(変えている場合)

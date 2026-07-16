---
audience: mixed
date: 2026-07-14
keywords:
- architecture
- 3-layer
- skill
- project
- vault
- priority
related_adrs:
- '0003'
- '0004'
related_specs: []
status: published
summary: Skill・Project・Vault の 3 層運用アーキテクチャの概要。各層の役割、優先順位、データフローを整理。
title: 'アーキテクチャ: Skill・Project・Vault の 3 層'
title_en: 'Architecture: Skill / Project / Vault 3-layer'
type: overview
created: 2026-07-14 20:47:07+09:00
updated: 2026-07-14 20:47:07+09:00
id: pj-2026-07-13-0245
aliases:
- pj-2026-07-13-0245
---

## Summary

Vault-Framework の運用アーキテクチャの核心である「Skill・Project・Vault の 3 層構造」を説明する。各層の役割、優先順位、データフローを整理し、なぜこの分離が必要かを解説する。

## 3 層の概要

Vault-Framework の運用は以下 3 つの層で構成される:

### 層 1: Skill(`vault-manager` SKILL.md)

- **役割**: Claude の振る舞いの核心ロジック
- **内容**: 発火判定、保存判断フロー、参照レベルシステム、あいまい名解決フロー、MCP 接続失敗時の処理、Cursor 委譲判定
- **更新頻度**: 低(Claude Skills への再アップロードが必要)
- **可視性**: Claude が常に読み込んでいる(システムプロンプトの一部として)

### 層 2: Project Instructions(Claude Projects の Instructions)

- **役割**: 最小限のポインタのみ
- **内容**: 「Vault MCP コネクタを確認し、vault 内の `project_instructions_vault.md` を読んで従う」という指示のみ
- **更新頻度**: ほぼ変わらない(激薄に保つのが設計方針)
- **可視性**: Chat セッション開始時に Claude に渡される

### 層 3: Vault(`00_meta/` 配下の運用ルール群)

- **役割**: 実質的な運用ルールの正典
- **内容**: 統制語彙、命名規約、Front Matter スキーマ、プロジェクトエイリアス、日々変わりうる運用方針
- **更新頻度**: 高(Obsidian で直接編集可能)
- **可視性**: MCP 経由で必要時に取得(参照レベルシステムに従う)

## 層間の優先順位

3 層の内容が矛盾した場合の優先順位は **Skill > Vault > Project Instructions** である。

### なぜこの順序か

- **Skill が最優先**: MCP 接続失敗時の処理、過剰参照防止(Level 0 の厳格化)、sensitive ファイルの引用禁止といった「安全性に関わるルール」は Skill に記述されており、これらは vault の内容に関わらず常に適用されるべきだから
- **Vault が次点**: 統制語彙、命名規約、テンプレート形式等の「日々変化しうる運用ルール」は vault 側が正典。Skill の記述が古くなった場合、vault を優先する
- **Project Instructions が最後**: 意図的に「激薄」に保たれており、実質的なルールをほとんど持たない。矛盾が起きた場合は他の 2 層を優先する

### 通常は矛盾しないよう管理

この優先順位はあくまで「万一矛盾した場合」の解決ルールであり、通常運用では 3 層の内容が整合するように保守される(保守運用 4 レベルの一部として)。

## データフロー

典型的な Chat セッションでのデータフローは以下の通り:

```
[Chat セッション開始]
    ↓
Project Instructions(層 2)が Claude に渡される
    ↓
Claude が「MCP コネクタ確認 → project_instructions_vault.md を読む」を実行(Level 1 参照)
    ↓
Skill(層 1)の判断ロジックに従って会話を進行
    ↓
必要に応じて Vault(層 3)から追加情報を参照レベルシステムに従って取得
    ↓
保存指示があれば、Skill の保存判断フロー(層 1)に従い Vault(層 3)に書き込み
```

Skill が「いつ・どう動くか」を決め、Vault が「具体的に何のルールで判断するか」の詳細を提供する、という役割分担になっている。

## なぜ 3 層に分離したか

単一のファイルにすべてのルールを詰め込む代替案(ADR-0003 の却下案参照)もあったが、以下の理由で 3 層分離を採用した:

- **更新頻度の違い**: Skill は再アップロードが必要で更新コストが高い、Vault は Obsidian で即座に編集できる。頻繁に変わる内容を Vault に置くことで、運用の摩擦を減らす
- **責務の明確化**: 「振る舞いのロジック」と「データ・ルールの詳細」を分離することで、それぞれの変更が他方に影響しにくくなる
- **Project Instructions の薄さ**: Claude Projects の Instructions はコンテキストとして毎回消費されるため、薄く保つことでコスト効率が良い

## 関連

- [ADR 0003: Skill・Project・Vault の 3 層構造](../decisions/0003-skill-project-vault-3-layer.md)
- [ADR 0004: Project Instructions を激薄にする](../decisions/0004-thin-project-instructions.md)
- [Philosophy: GitHub-as-a-Backend](./philosophy.md)
- [参照レベルシステム](./specs/reference-level-system.md)

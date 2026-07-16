---
title: Architecture Decision Records (ADR)
title_en: Architecture Decision Records Index
type: index
audience: mixed
status: published
date: 2026-07-13
keywords:
- adr
- decisions
- index
- 意思決定
summary: Vault-Framework の意思決定記録(ADR)の索引。
id: pj-2026-07-13-eaa1
aliases:
- pj-2026-07-13-eaa1
---

## ADR 一覧

| ID | タイトル | Status | 関連 chat_log |
|---|---|---|---|
| 0001 | GitHub-as-a-Backend の採用 | accepted | 2026-07-13_vault-system-design-* |
| 0002 | MCP プラットフォームに Cloudflare Workers を採用 | accepted | 2026-07-13_platform-selection-and-phase12-completion |
| 0003 | Skill・Project・Vault の 3 層運用アーキテクチャ | accepted | 2026-07-13_operational-architecture-skill-project-vault |
| 0004 | 激薄 Project Instructions 方針 | accepted | 2026-07-13_operational-architecture-skill-project-vault |
| 0005 | Vault-Framework 早期分離 | accepted | 2026-07-13_publication-strategy-and-naming-convention |
| 0006 | 命名スキーム: `Vault` / `Vault-MCP` / `Vault-Framework` | accepted | 2026-07-13_publication-strategy-and-naming-convention |
| 0007 | 保存先思想: 最初から適切な場所へ(案 B) | accepted | 2026-07-13_operational-architecture-* |
| 0008 | Cursor 委譲判定: メンテナンスレベル方式 | accepted | 2026-07-13_cursor-delegation-and-maintenance-levels |
| 0009 | 保守運用 4 レベル + 抽象生成の並行運用 | accepted | 2026-07-13_maintenance-operation-design |
| 0010 | handoff/ 領域の新設 | accepted | 2026-07-13_operational-architecture-* |
| 0011 | ディレクトリ構造刷新(10_captures/, 50_self/) | accepted | 2026-07-13_operational-architecture-* |
| 0012 | Fine-grained PAT の採用 | accepted | 2026-07-13_platform-selection-and-phase12-completion |
| 0013 | Projects 統合(2 → 1)| accepted | 2026-07-13_operational-architecture-* |
| 0014 | Sonnet 5 標準化への対応 | accepted | 2026-07-13_maintenance-operation-design |
| 0015 | Issue 起票機能は Framework 分離の次に実装 | accepted | 2026-07-13_publication-strategy-and-naming-convention |
| 0016 | MCP コネクタ接続失敗時: 1 回リトライ後に中断、憶測禁止 | accepted | (このセッションで確定) |
| 0017 | Skill vault-manager への id scheme 統合(Phase 0.6) | accepted | Phase 0.5 完了後 |
| 0018 | Backlog System の導入(Phase 1a-1b) | accepted | Phase 1a Vault #8 / Phase 1b |
| 0019 | Skill Backlog Reference Workflow(Phase 1c) | accepted | Phase 1c |
| 0020 | Skill Backlog Save Workflow(Phase 1d PR-A) | accepted | Phase 1d PR-A |
| 0021 | Vault-maintainer Stalled Detection(Phase 1d PR-B) | accepted | Phase 1d PR-B |
| 0022 | Chat Save With Residue Integration(Phase 1e、superseded by 0023) | superseded | Phase 1e |
| 0023 | Phase 1f Three Independent Commands | accepted | Phase 1f |

## ADR の使い方(AI 向け)

「なぜ X を選んだのか」という質問に答える時、まずこの一覧から該当 ADR を特定し、その本文を読む。関連する却下案は `../rejected-alternatives/` に配置。

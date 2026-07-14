---
audience: mixed
created: 2026-07-14T05:20:00+09:00
date: 2026-07-13
keywords:
  - hybrid
  - obsidian-sync
  - github
  - single-source-of-truth
  - dual-write
related_adrs:
  - "0001"
status: rejected
summary: Obsidian Syncと GitHub を並列運用するハイブリッド構成の案。単一 source of truth を維持できず、統合コストが高いため却下。
superseded_by: "0001"
tags:
  - rejected
  - vault-composition
title: "却下案: ハイブリッド構成"
type: rejected_alternative
updated: 2026-07-14T05:20:00+09:00
---

## Summary

Obsidian Sync と GitHub を並列運用し、それぞれの強みを活かすハイブリッド構成の案。単一 source of truth を維持できず、統合コストが高いため却下。ADR-0001 で GitHub-as-a-Backend を採用。

## What Was Proposed

Vault を以下のハイブリッド構成で運用する案:

- **書き込み経路 A**: Obsidian(iCloud + Obsidian Sync)経由の編集
- **書き込み経路 B**: Claude(MCP 経由)の直接書き込み
- **同期戦略**: 両者を定期的に同期(スクリプト or 手動)
- **役割分担**: 「Naoya の手動編集は Obsidian、AI 経由は GitHub」等の暗黙的な区分け

各書き込み経路にそれぞれのメリット(Obsidian の編集体験、GitHub の履歴管理)を活かせるという構想。

## Why It Was Considered

- **両者の強みを活かせる可能性**: Obsidian の編集体験と GitHub の履歴管理を両立
- **段階的移行の余地**: 現状(Obsidian 中心)から GitHub 中心への移行を段階的に進められる
- **バックアップの冗長性**: 2 経路の書き込みで、片方が壊れても復旧可能
- **Claude 連携の柔軟性**: MCP は GitHub、通常編集は Obsidian と役割分担

## Why It Was Rejected

- **単一 source of truth を維持できず、乖離が発生**: どちらが「正」なのか不明瞭な状態が生まれる
- **統合コストが高い**: 乖離した時にどちらを優先するかの判断ロジックが必要、その実装が複雑
- **同期スクリプトの保守負担**: 2 経路を接続する仕組みを継続的に維持する必要
- **競合の解消が困難**: 両経路で同じファイルが編集された場合、マージ戦略が必要
- **Cursor 委譲時の混乱**: Cursor が「今どちらが最新か」を判断できない状態が発生
- **MCP 実装の複雑化**: MCP サーバが「どちらを正とみなすか」の判断ロジックを持つ必要があり、実装複雑度が跳ね上がる
- **Public 化・パッケージング困難**: Framework の導入者に 2 経路の並行運用を強いるのは実質不可能

## What Was Chosen Instead

- **採用案**: ADR-0001「GitHub-as-a-Backend」(単一 source of truth = GitHub)
- **参照**: [[../decisions/0001-github-as-backend.md]]

Obsidian は編集 UI として使用するが、真実の source は GitHub。iCloud Drive はローカルミラーで、GitHub への push が「保存」の意味を持つ。

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_vault-system-design-inception-to-completion.md`
- 対応 ADR: [[../decisions/0001-github-as-backend.md]]
- 関連却下案: [[./vault-composition-plan-2-obsidian-sync.md]](Obsidian Sync 主導)

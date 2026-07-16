---
id: pj-2026-07-17-315f
aliases:
- pj-2026-07-17-315f
title: GitHub Issue 境界
type: knowledge
status: published
created: 2026-07-17T02:05:00+09:00
updated: 2026-07-17T02:05:00+09:00
tags: [backlog, github, design, boundary]
summary: Vault backlog と GitHub Issue の境界。昇格タイミング、Vault 側の状態更新パターン、完了同期戦略。
---

# GitHub Issue 境界

## Summary

Vault backlog は master、GitHub Issue は実装レイヤ。両者の境界と昇格ルールを明文化する。

## レイヤ分離

- **Vault backlog(概念レイヤ)**: 「何を作るべきか」「何を検討すべきか」の議論段階
- **GitHub Issue(実装レイヤ)**: 「どう実装するか」が決まった段階、Cursor が読む
- **Cursor 指示書**: 実装対象の詳細指示、GitHub Issue 起票と対で作成

## 昇格タイミング(3 段階ゲート)

Vault backlog item が以下 **3 条件全て**を満たした時、GitHub Issue に昇格:

1. `kind: task`(方針決定済み)
2. `project` フィールドが specific repo(`_life`, `_ideas/*` ではない)
3. Cursor 委譲対象と判定(Skill vault-manager の Cursor 委譲判定ルール、または Naoya 判断)

Cursor 委譲対象でない小さい task は昇格せず、Naoya が手動対応 or 直接 Issue 起票。

## 昇格時の Vault 更新パターン

Vault backlog item の Front Matter に以下を追加(既存フィールドは維持):

```yaml
assignee: cursor  # 変更
cursor_instruction_id: <指示書 id or path>  # 追加
github_issue: <owner/repo#N>  # 追加
```

`state: open` は維持(Cursor 作業中も棚卸し対象)。

H2 History に 1 行追記:

```markdown
- YYYY-MM-DD: assigned to cursor(指示書 X、Issue #N)
```

## Vault backlog の "closed" 状態と GitHub Issue との同期

### Cursor 完了時

1. Cursor が実装完了、Issue が close される
2. Naoya が「棚卸しして」or「これ完了してるはず」と Claude に伝える
3. Claude が Vault backlog item の `github_issue` から GitHub Issue の state を確認
4. Issue closed & merged なら Vault side を `state: done` + `completed_at` に更新提案
5. Naoya 承認 → Claude が update_note で反映

### Naoya 手動完了時

`assignee: naoya` のまま完了した場合、Naoya が Claude に完了を伝える → Vault を `done` に更新。

### 中断・放棄時

Issue が close された(merged せず)場合や、方向転換で不要になった場合:
- Vault side を `state: abandoned` + `abandoned_at` + `abandoned_reason` に更新
- H2 History に理由記録

## Cursor 委譲対象でない task の扱い

以下の場合、Vault backlog は作るが GitHub Issue には昇格しない:

- 対象リポジトリなし(`_life/`, `_ideas/*` 配下)→ Vault で完結
- Cursor 委譲判定に該当しない小さい修正(1 ファイル数行等)→ Naoya 手動対応 or 直接 Issue

これらは `github_issue` フィールドを持たず、`assignee: naoya` のまま完了する。

## Fallback: GitHub Issue から Vault への backfill

GitHub Issue が Vault backlog を経由せず直接起票された場合:

- 定期棚卸し時に Claude が対象リポジトリの Issue 一覧を確認
- Vault backlog に対応 item が無い Issue → 「これ Vault に backfill しますか?」と Naoya に提案
- 承認 → Vault に backlog item 起票、`state: open` + `assignee: cursor`(既に開始済み)

## 実運用フローの Skill 対応

Phase 1c で Skill vault-manager に以下を追加:

- Vault backlog → Cursor 指示書化 → Issue 起票 の flow
- GitHub Issue 完了確認 → Vault 更新提案 の flow
- Backfill 判定 flow

## Related

- [[pj-2026-07-17-cb46|Backlog System Overview]]
- [[pj-2026-07-17-7293|既存資産統合]]
- Cursor 委譲判定ルール: `skills/vault-manager/SKILL.md`

---
id: pj-2026-07-17-7293
aliases:
- pj-2026-07-17-7293
title: 既存資産と backlog システムの棲み分け
type: knowledge
status: published
created: 2026-07-17T02:05:00+09:00
updated: 2026-07-17T02:05:00+09:00
tags: [backlog, integration, migration]
summary: open-questions.md / roadmap.md / design-decisions.md と backlog system の役割分担と昇格ルール。
---

# 既存資産と backlog システムの棲み分け

## Summary

既存の `30_projects/<Repo>/open-questions.md` / `roadmap.md` / `design-decisions.md` と、Phase 1a で導入した backlog system の役割分担を明確化する。既存資産を無理に統合せず、共存 + 選択的昇格で運用。

## 役割マトリクス

| ファイル | 内容 | 状態管理 | 棚卸し | GitHub 連携 |
|---|---|---|---|---|
| `open-questions.md` | 思いつきレベルの論点、TODO 未満 | なし(単純箇条書き) | なし | なし |
| `roadmap.md` | 手段の連なり(方針レベル) | なし(進行中/完了の記述のみ) | 手動 | なし |
| `design-decisions.md` | 決着済み方針、ADR ライク | なし(決着済みが並ぶ) | なし | なし |
| **`backlog/xxx.md`** | 状態管理対象の item | あり(FM) | あり | あり |

## 棲み分けの基本原則

### open-questions.md

- **性質**: 「そのうち考えたい」「後で決めるかも」の思いつきメモ
- **backlog に上げるべきでないもの**: 1 行の疑問、5 分で答えが出るもの、まだ議論する時ですらないもの
- **backlog に上げるべきもの**: Naoya が「これはちゃんとタスク化して」「起票して」と明示した時

### roadmap.md

- **性質**: プロジェクトの方向性、手段の連なり
- **backlog との関係**: roadmap の各段階から具体的 next action として backlog item が派生することがある
- **共存**: roadmap は方針、backlog は具体的作業。両立
- **昇格不要**: roadmap 自体を backlog に置き換えない

### design-decisions.md

- **性質**: 「XX を YY に決めた、理由は ZZ」の記録
- **backlog との関係**: backlog issue(方針未決)の議論結果として design-decisions.md に追記されることがある
- **記録の連携**: backlog issue を close する時、design-decisions.md への追記があれば `related_ids` で紐付け
- **昇格不要**: design-decisions.md 自体を backlog に置き換えない

## 昇格フロー: open-questions → backlog

以下いずれかのトリガーで backlog に昇格:

- Naoya が「これはちゃんとタスク化して」と明示
- Naoya が「これ起票して」「backlog に入れて」と明示
- Claude が「これは backlog 化した方が良さそう」と提案 → Naoya 承認

昇格時の処理:

1. `30_projects/<Repo>/backlog/YYYY-MM-DD_slug.md` に新規 backlog item 作成
   - kind は文脈から判定(方針未決 → issue、決定済み → task)
   - state: open
   - assignee: naoya(初期)
   - summary は open-questions の該当行 + Chat の議論から生成
2. `open-questions.md` の該当行を **削除**、または「→ [[<backlog id>|<title>]]」に置換
   - 削除するか置換するかは Naoya の好み(Naoya に確認、または Skill Level で決定 → Phase 1c)
3. backlog item の body H2 History に「元 open-questions.md から昇格」を記録

## design-decisions.md との連携

backlog issue が方針決定で close される時:

1. Backlog issue の state: done、H2 History に決定内容記録
2. Design-decisions.md に決定内容を追加(既存記法に従う)
3. Backlog issue の Front Matter に `related_ids` として design-decisions.md の該当セクション id を含める(section link 使用可)

Body に:

```markdown
## Decision

方針: XXX に決定

詳細: [[<id of design-decisions>#YYY|design-decisions § YYY]]
```

## roadmap.md との連携

Roadmap の段階から backlog item が派生する時:

- Backlog item の `related_ids` に roadmap.md の id を含める
- Roadmap 本文には backlog item への wikilink を追加(可読性のため、必須ではない)

Backlog item 側 body:

```markdown
## Context

Roadmap の段階「XXX」の一部として起票。詳細は [[<id of roadmap>|roadmap]] 参照。
```

## 一括移行の要否

**行わない**。以下の理由:

- 既存 open-questions.md 等は「思いつきレベル」として意味がある
- backlog に全部上げると氾濫、棚卸し疲弊
- 昇格は Naoya の判断で選択的に行う

したがって Phase 1b では **既存資産の移行作業は発生しない**。ルール記述のみ。

## Related

- [[pj-2026-07-17-cb46|Backlog System Overview]]
- [[pj-2026-07-17-315f|GitHub Issue 境界]]
- Vault 実装: `30_projects/*/open-questions.md`, `roadmap.md`, `design-decisions.md`

---
created: 2026-07-13T21:55:00+09:00
keywords:
  - diary
  - template
  - self
  - 50_self
  - sensitive
  - 日記
  - テンプレート
status: published
summary: "50_self/diary/YYYY/MM/YYYY-MM-DD.md に新規日記ファイルを作る際のテンプレート。sensitive: true がデフォルト、mood / energy / weather は任意フィールド。"
tags:
  - template
  - diary
  - self
title: Diary Template
type: template
updated: 2026-07-13T21:55:00+09:00
---

## 使い方(このテンプレ自体は使い捨てではなく、コピー元として保持)

新規日記ファイル作成時のテンプレート。パスは `50_self/diary/YYYY/MM/YYYY-MM-DD.md`。

## テンプレ本文(以下をコピーして使う)

```markdown
---
title: <YYYY-MM-DD>
created: <YYYY-MM-DDTHH:MM:SS+09:00>
updated: <YYYY-MM-DDTHH:MM:SS+09:00>
type: diary
status: draft
date: <YYYY-MM-DD>
sensitive: true
mood: <optional: great|good|neutral|low|bad>
energy: <optional: high|medium|low>
weather: <optional: 自由記述>
tags: [self, diary]
summary: <optional: 1 行の要約。空欄可>
---

## 今日あったこと

<!-- 淡々と事実を書く。取捨選択せずに気になったことを羅列してよい。 -->

## 気づき・感じたこと

<!-- 事実に対する反応・気付き・感情。うまく言語化できなくてもよい。 -->

## 明日以降に持ち越すこと

<!-- 気になっているが今日は解決しなかったこと、明日以降のアクション。 -->
```

## Front Matter フィールド解説

- `sensitive: true` は diary type ではデフォルトで自動付与される
- `mood` / `energy` / `weather` は任意。後で振り返る際の粒度に応じて記入
- `tags` は最低 `[self, diary]`。追加で `[health]`、`[relation]` 等の tag を付けてよい
- `summary` は他 Chat から偶然参照される可能性を考えて、機微な内容を含めない粒度にする

## 追記時の注意

同日に複数回書きたい場合は、既存ファイルへ `append` で追記する(update_note の mode=append)。上書きしない。

## Skill 側の振る舞い

- 導入者が「日記」「今日の記録」「diary」「今日あったこと」等の発話をしたら Skill がこのテンプレを使う
- 明示的な「日記を読み返して」「先週の日記を振り返って」以外では、Skill は diary ファイルを絶対に読まない
- diary ファイル本文を他コンテキストで引用・要約してはならない

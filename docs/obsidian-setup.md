---
title: Obsidian Setup
created: 2026-07-16
status: draft
tags: [id-scheme, phase-0.5]
---

# Obsidian Setup

## Summary

本 ID scheme は Obsidian の **native alias** 機能で動作する。追加プラグインは不要で、必要な設定は最小限である。以下の手順で Settings を合わせ、Migration 後に動作確認すればよい。

## 必須設定

### Settings → Files and links

| 項目 | 値 | 理由 |
|---|---|---|
| New link format | Shortest path when possible | Wikilink 記法との整合 |
| Use `[[Wikilinks]]` | ON | 本 scheme の前提 |
| Automatically update internal links | ON | ファイルリネーム時の保険 |

### Settings → Editor

- Show frontmatter: ON（既定 ON なら維持）

## プラグイン

- **追加プラグイン: なし**
- 追加プラグインを入れる必要はない。ID 解決は Obsidian native の alias 機能で完結する

## 動作確認チェックリスト

Migration PR マージ後、以下 5 項目を Naoya が確認する:

1. Vault を開いて任意の markdown を開く
2. Front Matter に `id: <prefix>-...` が表示されている
3. wikilink `[[<id>|表示テキスト]]` 記法をカーソルオーバーするとリンクが有効である
4. リンククリックで対象ファイルが開く
5. 対象ファイルの `aliases[0]` がリンク元 wikilink の `<id>` と一致する

1–5 が全て通れば設定完了。効かない場合の対処:

- Obsidian の再起動
- Settings 内「Reload without saving」で alias index の再構築

## 既存 Vault との後方互換

- Migration PR マージの瞬間に全ファイルに `id` / `aliases` が付与される
- Obsidian は Front Matter 変更を自動反映するため、Naoya 側の作業は不要
- 既存の wikilink（あれば）も alias 経由で引き続き解決される

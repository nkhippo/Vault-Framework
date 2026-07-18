---
id: pj-2026-07-14-26c2
aliases:
- pj-2026-07-14-26c2
title: ローカル例(ローカルディレクトリ経由)
created: '2026-07-14'
---

## Summary

`vault-maintainer` Skill の管理用 README。この Skill の目的、`vault-manager` との棲み分け、アップロード手順、保留解除の経緯を説明する。

## この Skill は何か

`vault-maintainer` は、個人 Vault(`<your-account>/Vault`)の**保守運用(Level 2〜4)と抽象生成**を担当する Claude Skill です。

`vault-manager`(日常の保存・参照・Level 1 自動修正を担当)とは役割が分離されており、この Skill は保守運用または抽象生成の**明示的なトリガーがある時のみ**発火します。

## vault-manager との棲み分け

| 領域 | 担当 |
|---|---|
| 保存・参照・日記・あいまい名解決・Issue 起票 | vault-manager |
| Level 1(日常の統制語彙自動修正) | vault-manager |
| Level 2〜4(週次・月次・季節の保守運用) | **vault-maintainer** |
| 抽象生成(chat_log → ADR/spec/rejected/guideline) | **vault-maintainer** |

2 つの Skill を両方 Claude Skills にアップロードして併用します。誤発火を避けるため、`vault-maintainer` の description は保守・抽象生成の明示的トリガーのみに限定されています。

## 保留解除の経緯

この Skill は当初、あなた(導入者) の設計判断により「**3 ヶ月の運用データが蓄積されるまで着手を保留**」とされていました(Reference Class Forecasting 的な、実データを見てから設計する慎重な判断)。

2026-07-14、あなた(導入者) の判断で保留を解除し、v1.0 を作成しました。運用データ蓄積前の作成となるため、実際の運用パターンが見えてきたら、Level 2〜4 の具体的な作業内容や抽象生成のフローを調整する想定です(v1.1 以降で反映)。

## アップロード手順

Vault-Framework の SKILL.md は Claude Skills 標準フォーマット(`name` + `description` + `updated` のみの Front Matter)で書かれているため、追加加工は不要です。

1. Vault-Framework から `skills/vault-maintainer/` フォルダを取得
2. そのフォルダを zip 化(SKILL.md 単体でも可)
3. Claude Skills にアップロード
4. `vault-manager` と併せて両方 Enabled にする

```bash
# ローカル例(ローカルディレクトリ経由)
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/Vault/30_projects/Vault-Framework/skills/
zip -r vault-maintainer-v1.0.zip vault-maintainer/
# 生成された zip を Claude Skills にアップロード
```

Claude Skills UI 上で、既存の同名 Skill を更新する場合は、既存を削除してから新しい zip をアップロードすることを推奨します(キャッシュ回避のため)。

## 動作確認

アップロード後、新規 Chat で以下を試す:

- 「週次メンテをお願い」→ vault-maintainer が発火、Level 2 の検出フローを開始
- 「この議論を ADR にして」→ vault-maintainer が発火、抽象生成フローを開始
- 「これを Vault に保存して」→ **vault-manager が発火**(vault-maintainer は反応しない、棲み分けの確認)

3 つ目で vault-maintainer が誤発火しないことが、棲み分け設計の正しさの確認ポイントです。

Claude Skills UI 上での見え方の確認ポイント:

- description が `Use this skill ONLY when...` から始まっている(冒頭に `---` や `name:` が含まれていない)
- Front Matter が正しく解釈されている(name / description / updated の 3 フィールドのみ)

## 関連

- SKILL.md: `skills/vault-maintainer/SKILL.md`
- 保守運用仕様: `docs/ja/specs/maintenance-four-levels.md`
- 抽象生成仕様: `docs/ja/specs/abstract-generation.md`
- 対になる Skill: `skills/vault-manager/`

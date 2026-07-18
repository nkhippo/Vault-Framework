---
title: Vault-Framework
created: 2026-07-13
keywords:
  - framework
  - vault
  - claude
  - landing
  - adoption
status: published
summary: Claude と、GitHub 上の個人ナレッジベースを一つのシステムとして運用するためのフレームワーク。Chat 履歴の自動保存、過去議論の参照、backlog の明示管理を Claude と GitHub だけで実現。
tags:
  - framework
  - readme
  - landing
type: project_readme
updated: 2026-07-18T17:08:23+09:00
---

> **Vault-Framework** — Claude と、GitHub 上の個人ナレッジベースを一つのシステムとして運用するためのフレームワーク。
> *An operational framework for running Claude with a personal knowledge base on GitHub.*

---

## これは何か

- Claude の会話履歴、意思決定、日々の学びを **Front Matter 付き Markdown** で GitHub に自動保存
- 別の Chat から過去の議論を参照して、**より深い前提の上に議論を積み上げる**
- **Task / Issue の明示管理**(backlog)を Claude と共同運用
- 複数プロジェクトを 1 つの Vault で扱う横断ナレッジ運用

要するに、「Claude との対話が資産になる」状態を、あなたの GitHub アカウント内で完結させる仕組みです。

## 何が手に入るか(具体)

- 「先週の X 議論の続きだけど」で Claude が **勝手に該当ログを引き当てて** 会話を再開する
- 「あの決定の背景って?」で Claude が **意思決定ログを参照して回答する**
- Claude が「これは backlog に登録した方が」と自発提案 → 承認で **GitHub 上に構造化された task ノードとして起票**
- 記事執筆・プロジェクト設計・日記・アイデア、それぞれの型で保存 → 混ざらない
- 全て自分の GitHub リポジトリの中に。**外部 SaaS に頼らない、あなたの資産として残る**

## 前提

- **GitHub アカウント**(無料プラン可)
- **Cloudflare アカウント**(Workers 無料枠で運用可能、~1000 req/day 程度なら 0 円)
- **Claude Pro / Team / Enterprise**(Connectors + Skills 機能が必要、Free プランでは使えない)
- **Node.js 18+ / npm**(MCP サーバのデプロイ用、CLI 操作に慣れていれば OK)
- **Obsidian**(推奨、Markdown を手元で直接編集したい場合)

## 全体像(3 層アーキテクチャ)

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Claude     │◄──►│  Vault-MCP       │◄──►│  GitHub Vault   │
│  + Skills   │    │  (Cloudflare)    │    │  (Markdown repo)│
└─────────────┘    └──────────────────┘    └─────────────────┘
       │                                            │
       └──── Skills(Claude 側の振る舞い規約)       │
                                                    │
                     vault-templates ──── コピーして初期化
```

- **Claude Skills**: Vault の使い方を Claude に教える。Front Matter 判定、保存判断、backlog workflow など
- **Vault-MCP**: Claude と Vault の橋渡し。Cloudflare Workers 上で動く TypeScript 実装。GitHub Contents API 経由でリポジトリを読み書き
- **GitHub Vault**: あなたの個人 Markdown リポジトリ。全てのデータの正典

## 最短で導入したい人へ(推奨:AI-guided setup)

**この Framework は、別の Claude Chat があなたを対話でサポートしながら導入する形を推奨しています。** ドキュメントを順に読み解く必要はありません。

### 手順

1. [`docs/ja/setup/setup-companion.md`](docs/ja/setup/setup-companion.md) を開く(または右クリック→保存でダウンロード)
2. Claude で **新規 Chat** を開始
3. `setup-companion.md` をファイルとしてアップロード
4. 冒頭に以下のいずれかを送信:

```
このファイルに沿って、Vault-Framework を私のアカウントに導入するのをサポートしてください。
中学生でも分かる形でお願いします。
```

5. Claude が前提の確認から順に対話でガイドします(所要 2〜4 時間、途中中断可)

### この方式のメリット

- **専門用語の翻訳を Claude に任せられる**:GitHub や Cloudflare の用語も、あなたが分かる言葉に噛み砕いてもらえる
- **エラー時にその場で相談**:進めている途中でエラーが出ても、実行結果をコピペすれば Claude が原因を特定
- **一つずつ確認**:全 Phase を一気にではなく、あなたのペースで進行
- **中断・再開可能**:所要 2〜4 時間ですが、途中で切り上げても状態は保存

## 自分で読み進めたい人へ(マニュアル setup)

setup-companion 経由ではなく、手順書を自分で読んで進めたい場合:

1. **[Setup Handbook](docs/ja/setup/README.md) を開く** — 導入手順の 7 Phase 集
2. Phase 1〜6 のシステム作業を順に実施(所要 2〜4 時間)
3. Phase 7:Claude と Chat で対話しながら、あなた固有の profile / vocabulary を反映(所要 30〜60 分)
4. 以降、通常の Chat から Claude が自動的に Vault と連携

**「まずざっと概念を掴む」ならこの順**:

- [`docs/ja/philosophy.md`](docs/ja/philosophy.md) — なぜこのフレームワークを作ったか、思想
- [`docs/ja/architecture.md`](docs/ja/architecture.md) — 全体構造の詳細
- [`docs/ja/setup/README.md`](docs/ja/setup/README.md) — 導入手順の全体ロードマップ
- [`docs/ja/setup/07-initial-alignment-session.md`](docs/ja/setup/07-initial-alignment-session.md) — 導入後の対話セッションの位置づけ

## 何が入っているか

| ディレクトリ | 内容 |
|---|---|
| `skills/` | Claude Skills(`vault-manager`, `vault-maintainer`)。ZIP 化して Claude に登録 |
| `vault-templates/` | あなたの Vault の骨格。`00_meta/` に統制語彙・テンプレ・operations 一式 |
| `docs/ja/` | 導入手順、思想、設計判断、命名規則、ADR、ガードレール、Phase 7 プロンプト等 |
| `docs/ja/setup/` | 7 Phase の導入 Handbook |
| `docs/ja/setup/setup-companion.md` | **AI-guided setup 用の Claude 向け対話ガイド(推奨経路)** |
| `mcp-server-reference/` | Vault-MCP を深く理解・拡張したい adopter 向け技術リファレンス |
| `examples/` | 各 type の記入例 |
| `CHANGELOG.md` | 変更履歴(SemVer 準拠) |

## Framework 更新の取り込み

新バージョンが公開された時、あなたの Vault 個別データを壊さずに canonical のみを更新する仕組みが用意されています。詳細は下記 2 つが正典:

- [`docs/ja/setup/canonical-vs-personal.md`](docs/ja/setup/canonical-vs-personal.md) — canonical / personal / hybrid の境界表
- [`docs/ja/setup/08-update.md`](docs/ja/setup/08-update.md) — update 手順

## Status

- **Current version**: v1.3.0(参考実装として運用中、実運用実績あり)
- **License**: MIT
- **Language**: JA(EN 版は将来対応)

## 関連リポジトリ

- **[Vault-MCP](https://github.com/nkhippo/Vault-MCP)**: Cloudflare Workers 上で動く MCP サーバ実装。fork してデプロイして使う

## 導入で困ったとき

- setup-companion 経由で導入している場合、その Chat で Claude に直接相談するのが最速
- [`docs/ja/setup/troubleshooting.md`](docs/ja/setup/troubleshooting.md) — よくある問題と対処
- [`mcp-server-reference/troubleshooting.md`](mcp-server-reference/troubleshooting.md) — MCP サーバ側の詳細トラブルシューティング
- GitHub Issues でも受け付けます

## 貢献

- 実運用フィードバック、typo 修正、翻訳 PR、追加テンプレなど歓迎
- 破壊的変更を含む提案は、まず GitHub Issue で議論を推奨
- `docs/ja/decisions/` の ADR を読むと、既存の設計判断の背景が分かります

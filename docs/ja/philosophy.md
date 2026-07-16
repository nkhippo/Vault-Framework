---
audience: mixed
date: 2026-07-14
keywords:
- philosophy
- github-as-a-backend
- obsidian
- 思想
- ai-first
related_adrs:
- '0001'
related_specs: []
status: published
summary: GitHub-as-a-Backend の思想と、AI が主読者であるという設計前提、Obsidian ブランドとの関係を説明する。
title: '思想: GitHub-as-a-Backend'
title_en: 'Philosophy: GitHub-as-a-Backend'
type: overview
created: 2026-07-14 20:46:38+09:00
updated: 2026-07-14 20:46:38+09:00
id: pj-2026-07-13-b9c7
aliases:
- pj-2026-07-13-b9c7
---

## Summary

Vault-Framework の根底にある思想「GitHub-as-a-Backend」を説明する。データの正典を GitHub リポジトリに置き、Markdown + Front Matter で構造化し、AI(Claude)が読み書きする、という設計の核心的な発想を扱う。

## GitHub-as-a-Backend とは

Vault-Framework の最も基本的な設計判断は、**個人ナレッジベースの正典データストアとして GitHub リポジトリを採用する**ことである。

一般的な「セカンドブレイン」ツール(Notion、Obsidian の同期サービス、専用アプリ)は、多くの場合、専用のクラウドサービスやプロプライエタリなデータフォーマットに依存する。Vault-Framework はこれを避け、以下の性質を持つ GitHub リポジトリをバックエンドとして採用した:

- **プレーンテキスト(Markdown)**: ロックインがなく、どんなツールでも読み書き可能
- **Git 履歴**: すべての変更が追跡可能、誤操作からの復旧が容易
- **REST API**: プログラムから読み書き可能(MCP サーバの実装基盤)
- **無料または低コスト**: GitHub の無料プランで十分に運用可能
- **既存のエコシステム**: GitHub Actions、Issues、PR 等の既存機能を将来活用できる

つまり、「データは GitHub に、UI やアクセス手段は自由に選べる」という分離を実現している。

## AI が主読者であるという前提

Vault-Framework のもう一つの核心は、**この Vault の主要な読者は人間ではなく AI(Claude)である**という前提である。

従来のナレッジベースは人間が読むことを前提に設計される(見た目の美しさ、ナビゲーションのしやすさが優先される)。Vault-Framework はこれを転換し、以下を優先する:

- **構造化された Front Matter**: AI が内容を素早く把握できるメタデータ
- **一貫した命名規則**: AI が推測なしにファイルを特定できる
- **明示的な相互リンク**: AI が関連情報を辿れる
- **統制語彙**: AI の判定精度を上げる

人間(Naoya)は Obsidian 等のツールを通じてこのデータを閲覧・編集するが、日々の主要なやり取り(保存、検索、参照)は Claude を介して行われる。この「AI-first」の設計思想が、Front Matter スキーマ、命名規約、参照レベルシステム等、Framework 全体の設計を貫いている。

## Obsidian ブランドとの関係

Vault-Framework は Markdown ファイルベースであるため、Obsidian(人気の高い Markdown ノートアプリ)との親和性が高い。しかし、Vault-Framework は Obsidian に依存しない設計になっている。

- **Obsidian は UI レイヤーの選択肢の一つ**: vault を Obsidian で開けば、Wikilink やグラフビューが自動的に機能する。しかし Obsidian を使わなくても vault は完全に機能する(GitHub の Web UI、任意のテキストエディタ、Claude 経由でも操作可能)
- **命名の独立性**: 当初 vault の命名候補に「Obsidian」を含むものがあったが、最終的に Obsidian ブランドから独立した命名(`Vault`)を採用した(詳細は ADR-0006 参照)。これは Obsidian というツールへの依存を設計上明示的に排除する判断でもあった
- **Wikilink 記法の踏襲**: `[[path/to/file.md]]` という Wikilink 記法自体は Obsidian で広く使われる記法を踏襲しているが、これは GitHub 上でも(レンダリングはされないものの)可読なプレーンテキストとして機能する

## 設計原則への接続

この GitHub-as-a-Backend の思想は、Framework 全体の以下の設計判断につながっている:

- **Skill・Project・Vault の 3 層構造**(architecture.md 参照): データ(Vault)とロジック(Skill)を分離できるのは、Vault が GitHub という中立的なバックエンドだからこそ
- **MCP サーバによる橋渡し**(mcp-server-reference/ 参照): Cloudflare Workers 経由で GitHub API を叩く MCP サーバが、AI と GitHub リポジトリの間を橋渡しする
- **命名規約とディレクトリ構造**(naming-conventions.md 参照): AI が推測なしに正確な path を組み立てられるよう設計されている
- **保守運用 4 レベル**(maintenance-guide.md 参照): Git のコミット履歴を活用した、段階的な保守運用が可能になっている

## 関連

- [ADR 0001: GitHub-as-a-Backend の採用](../decisions/0001-github-as-backend.md)
- [[pj-2026-07-13-0245|Architecture: Skill・Project・Vault の 3 層]]

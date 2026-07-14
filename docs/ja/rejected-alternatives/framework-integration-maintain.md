---
audience: mixed
created: 2026-07-14T06:35:00+09:00
date: 2026-07-13
keywords:
  - framework
  - integration
  - monorepo
  - publication-scope
  - fable-packaging
related_adrs:
  - "0005"
  - "0006"
status: rejected
summary: Vault-Framework を Vault 本体内に統合維持し、別リポジトリ化しない案。Public 化スコープの混在と Fable パッケージング困難で却下。
superseded_by: "0005"
tags:
  - rejected
  - framework
title: "却下案: Framework を Vault 内に統合維持"
type: rejected_alternative
updated: 2026-07-14T06:35:00+09:00
---

## Summary

Vault-Framework(運用ドキュメント、Skill パッケージ、テンプレート集)を Vault 本体内に統合維持し、別リポジトリ化しない案。Public 化スコープの混在と Fable パッケージング困難で却下。ADR-0005 で早期分離を採用。

## What Was Proposed

Framework 部分を Vault 内に維持する案:

- **配置場所**: `nkhippo/Vault` 内の以下ディレクトリ
  - `00_meta/framework/`(運用ドキュメント全般)
  - `00_meta/skills/`(Skill パッケージ)
  - `00_meta/templates/`(統合済み、現行と同じ)
  - `00_meta/decisions/`(ADR)
- **公開方法**: Public 化する時、これらのディレクトリを別リポジトリにコピー
- **メリット享受**: モノレポの利便性(1 リポジトリで全てが管理)

## Why It Was Considered

- **モノレポの利便性**: Cursor で複数ファイルを跨いで編集する時、1 リポジトリで完結
- **同期の不要**: staging → mirroring workflow が発生しない
- **初期の実装コスト最小**: 分離作業(Cursor 委譲)が不要
- **Framework の実験期間**: Framework の中身が固まる前は、Vault 内で試行錯誤する方が柔軟

## Why It Was Rejected

### Public 化スコープの混在

- **Vault は Private 前提、Framework は Public 想定**: 1 リポジトリで公開範囲を制御するのは困難
- **`.gitignore` で除外する運用**: 継続的に維持するのが煩雑、除外漏れリスクあり
- **submodule や sparse-checkout の複雑度**: 「Framework 部分だけ Public」を実現するには submodule 等の構成が必要、シンプルでない

### Fable パッケージング困難

- **Fable は独立リポジトリ前提**: 特定リポジトリを Fork して使う想定
- **Vault のサブディレクトリだけを Fable 化するのは不自然**: 導入者が「vault の 00_meta/framework/ だけを Fork してください」は難しい
- **Framework の中身と Vault の実運用データが混在**: Public リポジトリに個人情報が漏れるリスク

### 責務分離の不明瞭さ

- **Vault の目的が「データ集約」と「Framework 定義」の 2 つに膨張**: 単一責務の原則から外れる
- **Vault の運用と Framework の運用が同じリポジトリで進行**: どちらの目的で編集しているか、コミットメッセージで区別が必要

### 命名スキームとの不整合

- **ADR-0006 で `Vault-Framework` を独立リポジトリ命名として確定**: この却下案とは根本的に不整合

## What Was Chosen Instead

- **採用案**: ADR-0005「Vault-Framework 早期分離」
- **参照**: [[../decisions/0005-early-framework-separation.md]]

早期に別リポジトリ(`nkhippo/Vault-Framework`)に分離。staging → mirroring workflow を受容し、Public 化・Fable パッケージングの準備を整える。

## References

- 検討 chat_log: `../../10_chat_logs/2026/07/2026-07-13_publication-strategy-and-naming-convention.md`
- 対応 ADR: [[../decisions/0005-early-framework-separation.md]]
- 関連 ADR: [[../decisions/0006-naming-vault-scheme.md]](3 リポジトリ命名の前提)

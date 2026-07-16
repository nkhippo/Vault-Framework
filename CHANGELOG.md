---
id: pj-2026-07-13-4ee4
aliases:
- pj-2026-07-13-4ee4
title: Changelog
created: '2026-07-13'
---
# Changelog

All notable changes to Vault-Framework will be documented in this file.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [Unreleased]

## [1.0.0] - 2026-07-13

### Added

- Initial scaffold structure (docs/, skills/, vault-templates/, mcp-server-reference/, examples/, project-instructions/)
- Vault-Framework の目的、原則、参照 order、用語集
- Skill `vault-manager` 本文込み配置
- ADR / spec / rejected-alternative / guideline / setup の 60+ 雛形
- 多言語対応の骨格 (docs/ja/, docs/en/, docs/i18n/)

### Design decisions

- 命名: `Vault` / `Vault-MCP` / `Vault-Framework` の 3 リポジトリ構成に確定
- MCP 接続失敗時: 1 回リトライ後に中断、憶測禁止

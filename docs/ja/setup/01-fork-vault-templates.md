---
audience: adopter
created: 2026-07-14 08:45:00+09:00
keywords:
- setup
- vault-repository
- fork
- vault-templates
- hashicorp-collision
- naming
- customization
status: published
summary: Framework の vault-templates/ を元に、自分の GitHub アカウントに vault リポジトリを初期化する手順。命名選定、リポジトリ作成、初期構造の配置、iCloud
  との同期設定までを含む。
tags:
- setup
- vault-repository
title: 01 - vault リポジトリの初期化
type: setup
updated: 2026-07-14 08:45:00+09:00
id: pj-2026-07-13-472f
aliases:
- pj-2026-07-13-472f
---

## Summary

Framework の vault-templates/ を元に、自分の GitHub アカウントに vault リポジトリを初期化する手順。命名選定、リポジトリ作成、初期構造の配置、iCloud との同期設定までを含む。

## 目的

このステップで達成すること:

- 自分の GitHub アカウントに vault リポジトリを作成
- Framework の vault-templates/ を初期構造として配置
- ローカル(iCloud Drive 等)にクローンして日々の編集環境を用意
- 命名衝突リスクへの対処

## Step 1: リポジトリ名の選定

### 推奨命名

Framework の標準推奨は:

- **リポジトリ名**: `Vault`(Naoya と同じ)
- **表示名**: シンプルさ優先

### HashiCorp Vault との衝突対策

`Vault` は HashiCorp Vault(シークレット管理)や他のプロダクトと名前衝突する可能性があります。以下の代替命名を推奨:

| 命名 | 使いどころ |
|---|---|
| `Vault` | Private リポジトリ運用中、Public 化予定なし |
| `<YourName>-Vault` | 例: `naoya-vault`、他プロジェクトと区別したい場合 |
| `Personal-Vault` | 個人利用を明示、Public 化予定あり |
| `Knowledge-Vault` | 「知識ベース」を強調 |
| `Chat-Archive` | 「Chat 集約」を強調 |
| 独自ブランド名 | 好きな名前(例: `nkhippo-memory`) |

### 選定の判断基準

以下の観点で選ぶ:

- **Private 運用中**: シンプルに `Vault` で OK
- **Public 化予定あり**: `<YourName>-Vault` や `Personal-Vault` が無難
- **チーム展開予定**: 独自ブランド名や `<TeamName>-Vault`
- **既存プロダクトとの明確な区別**: 独自ブランド名

### この手順書では

以下、あなたが選んだリポジトリ名を `<VaultRepoName>` と表記します。標準の `Vault` を選んだ場合は、そのまま `Vault` に置き換えて読んでください。

## Step 2: GitHub リポジトリの作成

### 方法 A: GitHub UI で作成(推奨)

1. https://github.com/new にアクセス
2. **Repository name**: `<VaultRepoName>`
3. **Description**: 「個人 Vault(Chat 集約、ナレッジベース)」等の説明
4. **Private / Public**: 
   - **推奨**: Private(個人的な内容が含まれるため)
   - Public にする場合、sensitive 情報が含まれないか慎重に確認
5. **Initialize this repository with**:
   - ✅ Add a README file
   - ❌ Add .gitignore(後で追加)
   - ❌ Choose a license(Private なら不要)
6. 「Create repository」をクリック

### 方法 B: gh CLI で作成

```bash
gh repo create <YourGitHubUsername>/<VaultRepoName> \
  --private \
  --description "個人 Vault(Chat 集約、ナレッジベース)"
```

## Step 3: ローカルにクローン

### iCloud Drive にクローン(macOS 推奨)

```bash
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/
git clone https://github.com/<YourGitHubUsername>/<VaultRepoName>.git
cd <VaultRepoName>
```

### 通常のパスにクローン

```bash
cd ~/Projects
git clone https://github.com/<YourGitHubUsername>/<VaultRepoName>.git
cd <VaultRepoName>
```

### 確認

```bash
git remote -v
# origin  https://github.com/<YourGitHubUsername>/<VaultRepoName>.git (fetch)
# origin  https://github.com/<YourGitHubUsername>/<VaultRepoName>.git (push)
```

## Step 4: Framework の vault-templates/ を初期構造として配置

### 方法 A: Framework から clone してコピー

1. Framework をローカル clone:

```bash
cd /tmp
git clone https://github.com/nkhippo/Vault-Framework.git
```

2. vault-templates/ の中身を自分の vault にコピー:

```bash
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/<VaultRepoName>
cp -r /tmp/Vault-Framework/vault-templates/* .
cp -r /tmp/Vault-Framework/vault-templates/.gitkeep* . 2>/dev/null || true
```

### 方法 B: Framework の zip をダウンロードしてコピー

1. https://github.com/nkhippo/Vault-Framework/archive/refs/heads/main.zip をダウンロード
2. 解凍
3. `Vault-Framework-main/vault-templates/` の中身を vault にコピー

### 配置される内容

以下のディレクトリ構造が配置されます:

```
<VaultRepoName>/
├── 00_meta/
│   ├── README.md
│   ├── vault_structure.md
│   ├── naming_conventions.md
│   ├── frontmatter_schema.md
│   ├── vocabulary.md
│   ├── claude_operation_rules.md
│   ├── project_aliases.md
│   ├── project_instructions_vault.md
│   ├── vault_index.md
│   ├── vault_maintenance_config.md
│   └── templates/
│       ├── chat_log.md
│       ├── note_draft.md
│       ├── note_published.md
│       ├── project_idea.md
│       ├── project_design.md
│       ├── knowledge.md
│       ├── handoff.md
│       └── diary.md
├── 10_chat_logs/YYYY/MM/.gitkeep
├── 20_notes/wip/.gitkeep
├── 20_notes/published/.gitkeep
├── 30_projects/_ideas/incubating/.gitkeep
├── 30_projects/_ideas/active/.gitkeep
├── 30_projects/_template/.gitkeep
├── 40_knowledge/ai/.gitkeep
├── 40_knowledge/dev/.gitkeep
├── 40_knowledge/english/.gitkeep
├── 40_knowledge/other/.gitkeep
├── 50_self/diary/.gitkeep
└── 90_inbox/.gitkeep
```

## Step 5: 初期カスタマイズ(必須)

以下 3 ファイルを自分の環境に合わせて編集します:

### 5.1 vocabulary.md の project セクション

`00_meta/vocabulary.md` を編集:

```markdown
## project(30_projects/ 配下でのみ使用)

# 導入者はここに自分の GitHub リポジトリ名を追加する

- <あなたのプロジェクト 1>
- <あなたのプロジェクト 2>
```

例:

```markdown
- IPASoundDrill
- English-Vocab-Chunk-Trainer
- Vault
- Vault-MCP
```

### 5.2 project_aliases.md

`00_meta/project_aliases.md` を編集し、テンプレートに沿って自分のプロジェクトエントリを追加:

```markdown
### <YourProject>

- 正式リポジトリ名: `<YourProject>`
- カテゴリ: <カテゴリ>
- 通称: <通称 1>, <通称 2>
- 機能キーワード: <機能を表すキーワード>
- 対象言語: <該当する場合>
- 一言メモ: <このプロジェクトの説明>
```

### 5.3 project_instructions_vault.md

`00_meta/project_instructions_vault.md` の `<your-*>` プレースホルダを実値に置換:

- `<your-github-username>` → 自分の GitHub ユーザー名
- `<VaultRepoName>` → Step 1 で選んだリポジトリ名(他の場所も同様)

## Step 6: 初回コミット

```bash
git add .
git commit -m "feat: initialize vault from Framework vault-templates"
git push origin main
```

## Step 7: Obsidian の Vault 設定(推奨)

Obsidian を使う場合:

1. Obsidian を起動
2. 「Open folder as vault」または「Create new vault」
3. Step 3 でクローンした場所を指定:
   - `~/Library/Mobile Documents/com~apple~CloudDocs/<VaultRepoName>/`
4. 初期化完了、`.obsidian/` ディレクトリが作られる
5. `.obsidian/` を Git 管理外にする場合、`.gitignore` に追加:

```bash
echo ".obsidian/" >> .gitignore
git add .gitignore
git commit -m "chore: gitignore obsidian workspace"
git push origin main
```

## 動作確認

以下を確認できたら Step 完了:

- [ ] GitHub にリポジトリが作成されている
- [ ] ローカル(iCloud Drive 等)にクローン済み
- [ ] `00_meta/` 内に 10 個のファイル + templates/ 内に 8 個のテンプレが存在
- [ ] `vocabulary.md` の project セクションを自分用に編集済み
- [ ] `project_aliases.md` に自分のプロジェクトエントリが 1 個以上追加済み
- [ ] `project_instructions_vault.md` のプレースホルダを置換済み
- [ ] 初回コミット・プッシュ完了
- [ ] Obsidian で Vault が開ける(推奨、必須ではない)

## Troubleshooting

### `.gitkeep` ファイルが表示されない

- 通常、`.gitkeep` は隠しファイルとして表示されません
- Obsidian の「File Explorer」プラグインで表示できる場合あり
- ディレクトリ構造の確認は `ls -la` または `find . -type d` で

### iCloud Drive にクローンしたが同期されない

- iCloud Drive の設定で該当フォルダの同期が ON か確認
- 大量のファイルで初回同期に時間がかかる場合あり(数分〜数十分)
- 「今すぐダウンロード」を強制的に実施することも可能

### Framework のライセンス

- Vault-Framework は MIT ライセンス(2026 時点)
- vault-templates/ をベースに商用利用も可能
- 詳細は `nkhippo/Vault-Framework/LICENSE` 参照

## Next Step

vault リポジトリの初期化が完了したら [02-deploy-mcp-server.md](./02-deploy-mcp-server.md) に進み、Vault-MCP を Cloudflare Workers にデプロイします。

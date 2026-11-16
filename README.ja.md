# skills

[English](README.md) | 日本語

実際の作業から編み出した Agent Skills を、OSS として公開するリポジトリ。

各スキルは `skills/<name>/SKILL.md` に置き、[Agent Skills](https://agentskills.io) の形式に従っている。Claude Code、Codex、GitHub Copilot など、対応するエージェントで使える。

各スキルの解く問題と使う場面は[カタログ](CATALOG.ja.md)にまとめてある。

## スキル一覧

| スキル | 内容 |
| --- | --- |
| [github-issue-artifacts](skills/github-issue-artifacts/SKILL.md) | GitHub Issue の HTML アーティファクト（`embedded_html`）を、サンドボックス化されたプレビューで実際に描画される形で作り、更新する。SVG 埋め込みのアイコン、CSS のみのテーマ切り替え、コントラスト比を確認したライトとダークの色の組、細いプレビューペインでも読める表、API での読み戻し検証が中身。GitHub 公式の `issue-artifacts` スキルが担うのは API アクセスの基本で、このスキルは公式が触れていない HTML の作り方側を担う |
| [temp-workspace-hygiene](skills/temp-workspace-hygiene/SKILL.md) | エージェントの一時作業を、追跡できないまま溜め込まないための規律。捨てる作業ファイル（`~/agent-tmp`）と人間が確認する成果物（`~/artifacts`）の置き場所を分け、作ったもの全てに所有者・用途・保持期限を manifest で記録し、作業の終わりに安全に棚卸しする。保持期限切れと放置分は `.trash` へ移して7日後に消す2段ライフサイクルで、整理スクリプト付き |
| [prune-merged-branches](skills/prune-merged-branches/SKILL.md) | GitHub の PR が merge 済みのローカルブランチを、worktree とリモートブランチごと片付ける。`git branch --merged` では検出できない squash merge も対象。dirty な worktree は消さずに agent-tmp の `.trash` へ移し、未 merge で close された PR は厳格な条件でローカルだけを片付ける。破壊的な操作の直前には状態のスナップショットを取り直して照合する。既定は dry-run |

## 導入

スキルフォルダを、使うエージェントが読む場所へコピーする。

| エージェント | リポジトリ内のパス | 個人のパス |
| --- | --- | --- |
| Claude Code | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` |
| Codex | `.agents/skills/<name>/` | `~/.agents/skills/<name>/` |
| GitHub Copilot CLI | `.github/skills/<name>/` | `~/.copilot/skills/<name>/` |
| GitHub Copilot in VS Code | `.github/skills/<name>/` | `~/.copilot/skills/<name>/` |

```bash
git clone https://github.com/Hyd3-14/skills.git
cp -r skills/skills/github-issue-artifacts ~/.claude/skills/
```

## ライセンス

MIT — [LICENSE](LICENSE) を参照。

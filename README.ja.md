# skills

[English](README.md) | 日本語

実際の作業から編み出した Agent Skills を、OSS として公開するリポジトリ。

各スキルは `skills/<name>/SKILL.md` に置き、[Agent Skills](https://agentskills.io) の形式に従っている。Claude Code、Codex、GitHub Copilot など、対応するエージェントで使える。

## スキル一覧

| スキル | 内容 |
| --- | --- |
| [github-issue-artifacts](skills/github-issue-artifacts/SKILL.md) | GitHub Issue の HTML アーティファクト（`embedded_html`）を、サンドボックス化されたプレビューで実際に描画される形で作り、更新する。SVG 埋め込みのアイコン、CSS のみのテーマ切り替え、コントラスト比を確認したライトとダークの色の組、細いプレビューペインでも読める表、API での読み戻し検証が中身。GitHub 公式の `issue-artifacts` スキルが担うのは API アクセスの基本で、このスキルは公式が触れていない HTML の作り方側を担う |

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

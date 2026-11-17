# カタログ

[English](CATALOG.md) | 日本語

このリポジトリの全スキルを、初めて見る人向けに書いたカタログ。各スキルの「解く問題」「実際にやること」「使う場面」をそろえてある。短い一覧は [README](README.ja.md) にある。

---

## github-issue-artifacts

HTML のまとめを GitHub Issue に添付して、コメントに埋もれさせず、その場で描画して読めるようにする。

**解く問題.** GitHub Issue Artifacts（パブリックプレビュー）は HTML 文書を Issue の横に描画でき、調査のまとめや判断を仰ぐ資料の置き場所として最適。ところがプレビューはサンドボックス化された iframe で、スクリプトは動かないことがあり、実行時に SVG へ差し替えるアイコンライブラリは何も表示されず、JavaScript のテーマ切り替えは無言で効かず、広い画面で問題ない表も細いプレビューペインでは1文字ずつ改行して崩れる。GitHub 公式の `issue-artifacts` スキルが担うのは API アクセスの基本だけで、ここには触れていない。

**実際にやること.** プレビューで崩れない `embedded_html` の作り方の実践集。アイコンは実行時ライブラリではなく SVG 埋め込み、切り替えは `:has()` を使った CSS のみ、塗りの要素ごとにライトとダークの色の組を定義してコントラスト比 4.5:1 以上を確認、表は 390px 幅でも読める形に。API は PATCH で同じ URL のまま差し替え、読み戻して検証する。

**使う場面.** まとめ、報告書、計画、図解の多い文書を GitHub Issue に残すとき全般。既存の HTML アーティファクトがプレビューで崩れているときも。

**前提.** GitHub CLI（`gh`）。アーティファクト専用コマンドは 2.103.0 以降が必要で、それ未満向けの REST 経由の手順も含む。

→ [skills/github-issue-artifacts/SKILL.md](skills/github-issue-artifacts/SKILL.md)

---

## temp-workspace-hygiene

エージェントの一時作業が、正体も削除可否も分からないまま `/tmp` とホームディレクトリに溜まっていくのを止める。

**解く問題.** エージェントは一時ファイルを常時作る。検証用クローン、キャッシュ、検証出力、下書き。それらが `/tmp` と `~` に散らかり、名前からは作った人、理由、消してよいかが分からない。掃除が発掘作業になるため、誰も掃除しなくなる。

**実際にやること.** 規律と小さな整理スクリプトのセット。置き場所は2つに分け、形をそろえる。捨てる作業は `~/agent-tmp/<host>/<owner>/<repo>/<日付>-<作業名>/`、人間が確認する成果物は `~/artifacts/…`。`/tmp` の作業は session root を1つだけ使い、`manifest.tsv` に種類、パス、用途、所有者、保持期限、状態を記録する。agent-tmp 側の作業単位は `MANIFEST` に `expires=YYYY-MM-DD` を持ち、期限切れと7日間放置されたものを整理スクリプトが `.trash` へ移し、さらに7日後に消す。削除は1週間は可逆。何かを消すには5条件（自分の作成物、使用中でない、dirty でない、不要、保持期限を満たす）の同時成立を求める。

**使う場面.** エージェントの一時ファイルの扱い方を決めるとき、すでに溜まった一時領域を片付けるとき、掃除を発掘ではなく定期作業にしたいとき。

**前提.** 整理スクリプトに Python 3（Linux。使用中判定で `/proc` を読む）。

→ [skills/temp-workspace-hygiene/SKILL.md](skills/temp-workspace-hygiene/SKILL.md)

---

## prune-merged-branches

Pull Request が merge 済みのローカルブランチを、squash merge 込みで、大事なブランチを1本も消さずに片付ける。

**解く問題.** `git branch --merged` は squash merge を検出できないため、終わったブランチが溜まる。よくある対処の「merge 済みっぽいものを強制削除」は、未 merge の作業ブランチを消す事故の元になる。worktree が絡むとさらに悪く、merge 済みブランチの worktree に未コミットのファイルが残っていることがある。

**実際にやること.** 900行の bash ツール `gprune-merged`。判定は Git の祖先関係ではなく GitHub の PR 状態で行う。ブランチが候補になるのは、merge 済み PR の head にローカルブランチが含まれるときだけ（SHA 完全一致、または squash 用に祖先関係で確認）。未 merge で close された PR は、PR head とローカルと origin の SHA が一致するときだけローカルを片付け、リモートブランチは決して消さない。きれいな worktree は削除し、dirty な worktree は作り直せるディレクトリ（`node_modules`、`dist` など）だけ落として残りを `~/agent-tmp/.trash` のライフサイクルへ移す。破壊的な操作の直前には、PR 状態、worktree 登録、ローカルとリモートの OID を取り直して収集時のスナップショットと照合し、変化があれば中止する。既定は dry-run。

**使う場面.** merge 済みブランチとその worktree が溜まったとき。特に squash merge と worktree を多用する運用で。

**前提.** `git` とログイン済みの `gh`。任意で、worktree 削除を任せる `gwq`（なければ素の `git worktree remove`）、リポジトリ横断の `--all` 用の `ghq`、trust 整理の `mise`。

→ [skills/prune-merged-branches/SKILL.md](skills/prune-merged-branches/SKILL.md)

---

## 関連プロジェクト

- [muse-widgets](https://github.com/Hyd3-14/muse-widgets) — Muse のチャット内ウィジェットのための部品カタログ、雛形、検査ツールと、Skill `chat-intelligent-ui` のリポジトリ。Skill はカタログと一緒に育てるため、こちらには複製を持たずリンクだけを置く。

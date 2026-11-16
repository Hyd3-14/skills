---
name: github-issue-artifacts
description: Create and update HTML artifacts (type embedded_html) on GitHub Issues that actually render in GitHub's sandboxed preview — inline SVG icons, CSS-only theme toggles, paired light/dark colors, narrow-pane-readable tables — and verify them by reading the artifact back through the API. Use when saving a summary, report, plan, or diagram-heavy write-up to a GitHub Issue as an HTML artifact, or when an existing HTML artifact renders broken in the preview.
---

# GitHub Issue Artifacts: HTML that survives the preview

GitHub Issue Artifacts (public preview, since 2026-10-28) attach named content to an issue: links, Markdown documents, and HTML documents (`embedded_html`) that render in place next to the issue. GitHub's official `issue-artifacts` skill covers basic API access for the Markdown and link types. This skill covers the part it does not: **authoring `embedded_html` artifacts that still work inside the preview**, where most naive HTML silently breaks.

An HTML artifact opens in Source view on GitHub. **Preview** renders it in a sandboxed iframe. Everything below comes from real failures in that iframe.

## API route

The dedicated `gh issue artifact` commands require GitHub CLI 2.103.0 or later. On older versions, use the REST API through `gh api` — same login, same result. Check `gh --version` before assuming the subcommand exists.

```bash
# Create (body is the full HTML source)
gh api repos/{owner}/{repo}/issues/{issue_number}/artifacts -X POST \
  -f name="Investigation summary" -f type=embedded_html -F body=@summary.html

# Revise in place (same URL, keeps version history)
gh api repos/{owner}/{repo}/issues/{issue_number}/artifacts/{artifact_number} -X PATCH \
  -F body=@summary.html

# List
gh api repos/{owner}/{repo}/issues/{issue_number}/artifacts

# Read back — note the wrapper: the resource is under .artifact, the body at .artifact.body
gh api repos/{owner}/{repo}/issues/{issue_number}/artifacts/{artifact_number}
```

Rules:

- **Update in place with PATCH.** Never create a second artifact for a revision; the URL stays stable and GitHub keeps the history.
- **Read back and verify before reporting success.** Compare the stored body with what you sent (byte comparison, or key markers plus `updated_at`). A 200 response is not proof the content landed as intended.
- The artifact URL is `https://github.com/{owner}/{repo}/issues/{issue_number}/artifacts/{artifact_number}`.
- Never print or request the user's GitHub token.

## The sandbox constraints (the core of this skill)

Scripts may not run in the preview iframe, and `localStorage` access may throw. **No feature of the page may depend on JavaScript.**

- **Icons: inline SVG.** A JS icon library (for example Lucide via CDN plus `createIcons()`) renders nothing in the preview. Paste the SVG markup of each icon directly into the HTML. Same icons, same look, zero runtime dependency.
- **Theme toggles and other state: CSS only.** A checkbox plus the `:has()` selector can switch CSS variables for the whole page without any script. Persistence (`localStorage`) and OS-preference sync are optional enhancements only — wrap them so that when they throw, the switch itself still works.
- **Both themes are designed, not derived.** Text and nested elements on a colored fill (stage boxes, badges, stat cards, table headers, code chips) must use a foreground/background pair defined *for that fill* in each theme — never colors inherited from the page theme, which is how code chips end up as unreadable dark bars on colored boxes. In the dark theme, filled elements read better as light text on a deep fill than as dark text on a pale fill. Every text/background pair must reach a contrast ratio of at least **4.5:1**; compute it, don't eyeball it.
- **The narrow preview pane is a primary surface.** The preview sits in a pane roughly 390–600px wide beside the issue. Tables must stay readable there: give wide tables a scrollable wrapper with a minimum table width, or switch to a labeled stacked layout under a breakpoint — and include the table `caption` in that stacked treatment, or it collapses into one-character-per-line vertical text. Code strings wrap with `overflow-wrap: anywhere`. "No horizontal overflow" is **not** a pass; the criterion is that everything stays readable.

## Workflow

1. Produce one self-contained HTML file (hand-written or generated — the source does not matter, the constraints above do).
2. Create the artifact, or PATCH the existing one when revising.
3. Read it back through the API and verify the stored body.
4. Verify rendering the way the preview will: with JavaScript disabled, in both themes, at desktop width and at ~390px. Check icons, toggles, colored fills, and every table.
5. Report the artifact URL. If a long comment or file attachment was used as a stopgap, remove it once the artifact is live.

## Failures this skill exists to prevent

- Reaching for a Mermaid diagram in a comment, or a downloadable file attachment, when the native artifact renders in place.
- Shipping a JS-driven theme toggle that does nothing in the preview, with no error anywhere.
- Icons that exist in your dev preview and vanish in GitHub's.
- A dark mode that technically has paired colors but puts dark text on a pale blue fill, unreadable in practice.
- A table caption squeezed into a few characters' width, wrapping one character per line, discovered by a reader instead of by verification.

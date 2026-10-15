# Manual Obsidian acceptance checklist

The migration was built and validated without an Obsidian UI, so CardBoard and Obsidian Git behavior in the app is **not verified**. Run this once on a real Obsidian installation (desktop) before the cutover and record the result here.

Plain bullets on purpose: checkboxes in this file would become CardBoard cards.

1. Clone the branch, open the folder as a vault, install CardBoard 0.7.9 and Obsidian Git 2.41.1 (community plugins). Confirm Obsidian keeps the committed `data.json` files (no settings reset) — `git status` must show no change to `.obsidian/plugins/*/data.json` after the first start.
2. Open CardBoard. Expected boards: "Current · v0.4.26", "Attention", "Releases", "Backlog". Expected: "Current · v0.4.26" shows its 22 cards across Planned / Active / Blocked / Review, no cards from `releases/`, `epics/`, `decisions/`, `templates/`, `views/`, `migration/`, `scripts/`, README/WORKFLOW/HOME/AGENTS.
3. Card titles read `<id> · <title>`; the edit icon opens the task note; the note shows the generated links block with PR and source links.
4. Representative round trip on a test branch with **core-894**: edit its tag from `#status/planned` to `#status/active` and set `owner` → the card moves to "Active". Run `python3 scripts/plan.py check` (expect pass). Then tick its checkbox on the board → CardBoard appends `@completed(…)`; `plan.py check` must now **fail** ("a checked card must carry exactly #status/closed", "requires evidence"). Change the tag to `#status/closed`, set `resolution: accepted` and an evidence URL, run `render` and `check` (pass); the card appears in the board's Closed column. Inspect `git diff`: only the card line, frontmatter and generated blocks changed. Discard the branch.
5. Obsidian Git: confirm no automatic commit/pull/push happens (status bar only); run "Commit all changes" and "Push" manually once on a test branch.
6. Record: Obsidian version, OS, plugin versions, date, result, deviations.

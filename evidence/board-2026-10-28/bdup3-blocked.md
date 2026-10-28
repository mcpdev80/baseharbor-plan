# BDU3 — LANE bdup3 (ornith): blocked

- Lane: `/home/marcel/tmp-ops/m-bdup3.txt`
- Task: `t-20261017-release-0-4-27-cleanup` (v0.4.27 cleanup, read-only inventory)
- Date: 2026-10-28

## What was done
1. Turn-start basics-check run. FLAGS: 4 unread WATCHDOG PANE-reminders (observe:pane UNKNOWN — diagnostic noise, not task state), pools below target (flash/ornith/qwen), 1 open planning step. Reminders acked (0 records).
2. `git pull origin main` in baseharbor-plan: rc=0.
3. Card `t-20261017-release-0-4-27-cleanup` read; task contract + repo rules (AGENTS.md) read.
4. Local `## PLAN` written to `/home/marcel/tmp-ops/bdup3-plan.md`.
5. Made the two intended edits (status tag → `#status/review`, added `## Stand 2026-10-28` note-body section with the 3 dossier names + counts + promotion #1159 line).
6. `python3 scripts/plan.py render` OK; `python3 scripts/plan.py check` reported 3 errors, all from this card.

## Blocker (schema/semantic conflict — needs Owner decision)
`plan.py check` rejects the lane's target status `#status/review`:
```
error: tasks/.../cleanup.md: status review requires an owner
error: tasks/.../cleanup.md: status review requires at least one PR
error: tasks/.../cleanup.md: #status tag outside the card line (line 52 of body)
```
Schema (`scripts/plan.py:332-335`): `review` requires `item["owner"]` set AND `item["prs"]` non-empty; `#status/` tags must appear only in the card line (the note-body `## Stand` section must not carry a `#status/` tag).

This cleanup card is intentionally read-only: no owner assigned, `prs: []`. Neither `review` (needs owner + ≥1 PR) nor a `#status/` tag inside the note body is schema-valid. The card currently carries `#status/planned` in the card line and `state: queued`.

## Evidence of counts (from the three tmp-ops dossiers, https-evidence URLs; tmp-ops itself not referable)
- baseharbor: 0/0 PRs (no PRs exist; read-only analysis).
- console/demo: 2 current (console-2 PR #8 / o66; nc-3 PR pending).
- 70 branches: 2 DEL-OK / 68 CHECK (2 incorporated branches removed; 68 still to verify; preserve tags, candidate refs, retention).
- Promotion #1159: waiting owner.

## Revert
All edits reverted (`git checkout -- <files>`); working tree clean, nothing pushed.

## Stopped — awaiting Owner decision
Two schema-valid options, Owner picks:
- **A:** Keep `#status/planned` (or set `active` after a real claim) — correct for read-only inventory with no PR. Then render + check must pass, commit to a non-main branch, push, ls-remote witness. (No promotion/merge implied.)
- **B:** Make `review` valid by (i) claiming an owner via `scripts/plan.py claim` and (ii) setting `prs:` to a real referenced PR (e.g. `mcpdev80/baseharbor-console#8`), then render + check, commit, push. (Only if Owner accepts labeling a read-only inventory as `review`.)

After any chosen option: commit `plan(r27): cleanup inventory + promotion status notes` to `origin HEAD:refs/heads/work/r27-board-b3` (main push forbidden; generated files never hand-edited), verify with `ls-remote`, then report `END BDU3-DONE` or a new blocker.

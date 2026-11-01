# plan-card-fix evidence — 2026-11-01

## Task
Regenerate the hand-written, schema-broken planning card `tasks/diff-base.md` (introduced by
commit `6cc2371`, PR#1251-Merge-Epoche) as a valid card, remove the old file, `render`, `check`
=> 0 errors, commit, push origin main. Mechanical schema repair only — task content/meaning
preserved verbatim (PR #1251 merged the diff-base resolver fix to develop).

## Before (13 errors)
`python3 scripts/plan.py check` reported 13 errors on `tasks/diff-base.md`:
invalid id 'diff-base', unsupported tags ['#fix'], missing #release tag, conflicting lifecycle
markers accepted-vs-closed, type illegal, non-https evidence links, broken links, and the
#1240 source not in the open-issue inventory.

## After (0 errors / 0 warnings)
- Removed: `tasks/diff-base.md` (`git rm`).
- Created: `tasks/t-20261101-plan-card-fix-diff-base.md`
  (`id: t-20261101-plan-card-fix-diff-base`, `type: task`, `release: backlog`,
  `#status/closed` + `#view/closed #board/planned`, `owner`, `resolution: accepted`,
  https evidence links).
- Rendered derived views (`render`) and validated (`check` => 0 errors, 0 warnings).

## Sources-inventory repair
`check_sources` requires every `sources[]` reference to point at an inventoried issue and every
inventoried issue to be accounted for. The snapshot `migration/source-snapshot/inventory.json`
(captured 2026-10-15) predated #1251 and #1253, so both were missing. Added both via
`scripts/_snapshot_add.py` (live GitHub fetch → per-issue JSON with digest + inventory entry),
then re-rendered `migration/manifest.json` and `migration/coverage.md`.

## Verification
- `python3 scripts/plan.py check` → `342 tasks, 7 epics, 13 releases, 16 decisions; 0 errors, 0 warnings`.
- Develop tip confirmed at `5777c02d` (matches merge-commit claim in the card).

## Handoff
Commit + push to origin main pending in this lane.

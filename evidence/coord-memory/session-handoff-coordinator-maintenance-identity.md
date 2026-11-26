# Session handoff - coordinator maintenance identity on the planning branch

Date: 2026-11-26T07:12Z (host clock, `date -u`)

## What happened

The coordinator operational-memory mirror had not run since 2026-11-17 because
`scripts/sync-memory.sh` committed and pushed from the shared plan checkout, which is
routinely DETACHED and far behind `origin/main` (today: detached at `0ac804269`, 67 behind,
51 stashes). Publishing from that tree is forbidden by the coordinator's own divergence rule,
so the script was changed to clone live `main` into `/var/tmp/coord-memory-sync`, copy only
the coordinator's own files, `pull --rebase`, and push `HEAD:main`.

The first run of the corrected script published commit `4f2e01876` onto plan `main` with
author identity `lv4-verify` - the machine's ambient default git identity. That string is
neither the repository owner nor a registered lane, so per the 2026-11-26 identity ruling it
is a non-admissible author for anything but the two ratified historical `w205` commits.

## Disposition (forward-only, no rewrite)

- `4f2e01876` is retained exactly as it is: content is coordinator operational memory only
  (`evidence/coord-memory/QUEUE.md`, `missions/*`, session handoffs), zero task or product
  files, zero `tasks/` frontmatter. Its authorship is hereby declared a coordinator tooling
  defect, not lane work.
- `scripts/sync-memory.sh` now sets the explicit maintenance identity `coord`
  (`coord@baseharbor.local`), matching the precedent for this path
  (`1d88c2ef6`, `88f320acb`). No lane name, no role suffix, no fabricated worker.
- Every later mirror commit is coordinator maintenance and must never be counted as lane
  evidence for any card.

## Consequence for lanes and reviewers

When a reviewer sees `an=coord` on plan `main`, it is the memory mirror. When a reviewer sees
`lv4-verify`, it refers to the single known defect at `4f2e01876` and to nothing else.

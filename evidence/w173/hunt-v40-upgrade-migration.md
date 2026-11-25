# Bug-Hunt Slice H-V40: upgrade/migration path surface

Lane: w173-0428-224-hunt-v40
Mission: hunt-v40-upgrade-migration.txt
Date: 2026-11-25
Scope: PURE FINDING, NO product changes. Read-only investigation.

## PLAN

- Anchor: ls-remote develop tip, cut fresh worktree at exact tip
- Map version-migration handling in internal/ + cmd/baha (state dir upgrades, config schema bumps, rollback behavior)
- Compare migration surface with tests + docs claims for 0.4.27 -> 0.4.28 window
- Write per-row file:line findings + proposed card lines in akte evidence
- Cleanliness: no containers/volumes/state dirs left (ps witness), commit evidence, END_DONE

## planning repo attestation

- Planning repo path: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
- remote -v (verified BEFORE first evidence commit):

## base attestation

- develop tip (git ls-remote <real-url> refs/heads/develop):
- cut from SHA (ancestor of first commit):

## WORK

### Anchor / base

- ls-remote develop tip:
- fresh worktree cut at exact tip:

### Migration surface map (internal/ + cmd/baha)

- state dir upgrades:
- config schema bumps:
- rollback behavior:

### vs tests + docs (0.4.27 -> 0.4.28 window)

- tests claiming migration coverage:
- docs claiming migration behavior:
- gaps found:

### findings (file:line)

1.
2.
3.

### proposed card lines

- title:
- summary:
- acceptance:

## cleanliness

- docker ps -a before:
- docker ps -a after:
- no containers/volumes/state dirs left:

## END

END w173-0428-224-hunt-v40 DONE

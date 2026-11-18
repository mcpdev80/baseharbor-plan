# BUG-HUNT 916 — runtime ownership / impact-consent staleness

Mission: /var/tmp/missions/mission-hunt-ownership.md
Lane: hunt-ownership (bug-hunt, pure findings, no product change)
Object: merged content on baseharbor develop at 8dccd4fe1a52bbcc61c67f7809079f33b8040d64 (verified via `git ls-remote origin develop`).
Worktree: /tmp/opencode/hunt-ownership-wt (fresh clone of origin/develop, HEAD == 8dccd4fe1).
Planning repo attestation: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` → /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (the real planning repo; NOT workers/baseharbor-plan).
origin/main at evidence start: 528f3cc5753f9b2c20e802e37faef2226b68c16d

## PLAN

1. Verify remotes (baseharbor develop HEAD 8dccd4fe1, baseharbor-plan origin/main), fresh clone at /tmp/opencode/hunt-ownership-wt.
2. Create this evidence file with ## PLAN + base attestation.
3. Slice (a): trace where ownership-state is classified "unverifiable" and what marks impact-consent stale (file:line).
4. Slice (b): tabulate add/remove/re-add race windows where states remain without error (selective backend, identity apply).
5. Slice (c): enumerate untested combinations (re-add after failed remove) across test suites.
6. Run focused unit tests on ownership/consent paths (no containers per R1), record results.
7. Write findings, cleanliness line, commit evidence on top of origin/main and push.
8. Verify evidence path present on origin/main, END post to coordinator.

## Slice A — code-path walk: ownership "unverifiable" → impact-consent stale

(to be filled)

## Slice B — race windows in add/remove/re-add

(to be filled)

## Slice C — test coverage gaps

(to be filled)

## Unit test runs

(to be filled)

## Cleanliness

(to be filled)

END: pending

# w55-0428-078-probehop: 0428-078 rebase + integrate #1810 perses probe

## Lane identity
- Card: 0428-078 (task t-20261114-r28-perses-dashboard-identity)
- PR: baseharbor#1650
- Branch: lane-0428-078-perses-identity-on-resolver
- Owner session: w55-0428-078-probehop

## Base attestation
- Remote HEAD (ls-remote witness): `84943695be19300ef006a7986e1d110130943ce8` refs/heads/lane-0428-078-perses-identity-on-resolver
- develop remote HEAD: `840c4a6b6f012a2c698a3b0ee5863c7b82753200`
- My branch HEAD == remote head (clean FF, no new commits, nothing pushed)
- Remote URLs (resolved via git remote -v): both lane-origin and origin -> ssh://git@github.com/mcpdev80/baseharbor.git (verified, not a local path)

## What was done before the stop
1. Fetched origin develop 840c4a6b, confirmed remote heads via ls-remote, confirmed task already active/owned by w55-0428-078-probehop.
2. Fast-forwarded local branch to remote head 84943695 (clean FF; 84943695 added the keycloak provider-class label fix on top of the stalled w078 work).
3. Investigated #1810 (merged into develop as 951014e9 "0428-186: real verified-status source for PersesStatusNow"): `metricsprovider.PersesBackendAnswersStatusNow(ctx, m)` in internal/metrics/perses_backend_status.go runs the real per-target httpClientSeriesProbe round trip against the materialized per-target endpoint, fail-closed to configured_unverified (never a static verified).
4. Confirmed my branch's cmd/baha/app_status_result.go was identical to develop EXCEPT line 313, which still used the static `capability.PersesStatusNow(selection)`.
5. Implemented the one-line probe integration (the remaining #1650 acceptance piece): replaced the static status with `metricsprovider.PersesBackendAnswersStatusNow(ctx, resolved.Manifest)` and updated the adjacent comment.
6. Added the #1810 probe source internal/metrics/perses_backend_status.go (byte-identical to develop) and its test internal/metrics/perses_backend_status_test.go (byte-identical to develop) so the new symbol exists and is covered by CI.
7. Verified compilation: `go build ./cmd/baha` and `go vet ./cmd/baha ./internal/metrics` both EXIT 0. No local product test suite run (HOSTED-ONLY, Owner 2026-11-23).
8. Did NOT touch: internal/metrics/prometheus_files.go, perses_dashboards*, internal/metrics/perses_dashboards_keycloak.go, keycloak_files.go, keycloak_realization.go, scripts/**, .github/**.

## Scope verification (pre-stop)
- Working-tree changes (uncommitted, unpushed):
  - M cmd/baha/app_status_result.go  (single-line probe integration)
  - ?? internal/metrics/perses_backend_status.go
  - ?? internal/metrics/perses_backend_status_test.go
- git status --short confirmed ONLY these three files. No foreign commits carried. No new commit on the branch (HEAD == 84943695).

## HARD STOP (owner directive, 2026-11-24)
- Owner STOP: PARALLEL owner reconciliation of #1650. Detached prep cab3812d, dropping dup commit 378ff1afa. DO NOT push lane-0428-078 / #1650 (avoid concurrent write, AGENTS 4.3). Park #1650; it rebases onto #1815 AFTER that merges. No local tests.
- Ack: stopped, no push.

## Park state
- No commit made, nothing pushed. Working tree left intact (changes preserved, recoverable after #1815 merges).
- To resume: commit the three files as a single integration commit on 84943695, rebase/verify against the post-#1815 develop, push a new head off 84943695, run exact-head Hosted CI to terminal, keep PR open (MERGE-FROST), then hand off.

## END
END_BLOCKED w55-0428-078-probehop: HARD STOP by owner — #1650 under parallel reconciliation (prep cab3812d, dup 378ff1afa dropped); no push; changes parked uncommitted in working tree; lane to rebase onto #1815 after it merges.

# 0427-maintenance-r5 — Round-5 EVIDENCE (task t-20261018-r27-maintenance-client, card 0427-034)

Worker lane `0427-034-maintenance-r5`, coordinator session `594fd2f5-4e80-43b6-9841-92879146a85e`.
Repository `mcpdev80/baseharbor`, candidate PR #1428 head `396529860e1f349576190f435cb06e2b7b496866`.

## What this round proved (not implemented)

The Owner cleared this round to PROVE (with file:line, test name, and a mutation red-probe) that the
pinned candidate `396529860e1f` already implements BOTH CODEX-REVIEW findings, then publish only plan
evidence. No product file was changed this shift. The candidate stays UNCHANGED.

## Scope note (recorded, not resolved here)

The candidate head `396529860e1f` is not authored by this worker's owner label
`0427-034-maintenance-r5`: `git log --all --author='0427-034-maintenance-r5'` returns nothing, and the
origin branch `lane/0427-maintenance-client-wt` that the mission pins is authored by
`Marcel Pfingstgräf` (the Owner) with the BaseHarbor repo root as its first commit. This worker did
not reinterpret the ownership; it only verified the candidate's behaviour and published plan evidence.
The reviewer receives this as a re-check with an exact load-bearing refutation per finding.

## Findings

### Finding 1 — retry-after-owner-failure ORACLE DIRECTION (local + remote)

Route: local `cmd/baha/app_maintenance_client.go:363-371` and remote
`cmd/baha/app_maintenance_client.go:266-275`. On a failed destroy both routes call
`rollbackApplicationMaintenanceWindow` (a load-bearing `var` seam, line 572) which rolls the current
window back to the pre-commit record AND removes the appended history entry via
`RollbackMaintenanceAuthorityWindow` (`internal/application/maintenance_authority.go:455-460`).
A retry on the same revision is then refused as already-recorded only when residue remains; the
rollback is what keeps the retry answerable.

- Bearing test: `TestApplicationMaintenanceDestroyRollbackIsLoadbearing`, `cmd/baha/app_maintenance_round3_test.go:42-96`,
  asserting `found=false` after a failed destroy (`app_maintenance_round3_test.go:65`).
- Bearing test (both routes, all exits incl. retry-after-owner-failure): `TestApplicationMaintenanceDestroyAllExitsMatrix`,
  `cmd/baha/app_maintenance_round4_test.go:108-244`, cases `local-owner-failure`,
  `local-history-failure-residue`, `remote-owner-failure`, `remote-history-failure`.

Mutation red-probe: disabled the `rollbackApplicationMaintenanceWindow` seam to a no-op
(`cmd/baha/app_maintenance_client.go:572`) and re-ran. Result RED:
`app_maintenance_round3_test.go:65: a failed destroy left a durable window with the working rollback: found=true`.
Restored to production afterwards; working tree clean.

### Finding 2 — TOMBSTONE REPLAY PATH (both routes)

After a successful destroy the owner removes the whole deployment root
(`internal/deployment/deployment_store.go:602-607`, `os.RemoveAll`), so the durable window is
queryable only via the tombstone stamped at a sibling path
(`<DataRoot>/targets/<target>/maintenance/<deploymentID>.json`), see
`cmd/baha/app_maintenance_client.go:256-275` (remote) and `cmd/baha/app_maintenance_client.go:356-372`
(local). `stampMaintenanceTombstone` (`cmd/baha/app_maintenance_client.go:517-545`) writes the COMMITTED
destroy window (never the stale pre-commit authority). History replay stays answerable via
`loadMaintenanceRevision` (`internal/application/maintenance_history.go:201-219`).

- Bearing test (both routes): `TestApplicationMaintenanceDestroyAllExitsMatrix`,
  `cmd/baha/app_maintenance_round4_test.go:108`, cases `local-success` and `remote-success` (assert
  `durableTombstone: true`, then read + `assertCommittedDestroyTombstone`).

Mutation red-probe: no-op'd `stampMaintenanceTombstone` at the top (`cmd/baha/app_maintenance_client.go:517`)
and re-ran. Result RED (both routes):
`app_maintenance_round4_test.go:194: durable tombstone missing after successful destroy: open .../maintenance/<id>.json: no such file or directory`
for `local-success` and `remote-success`. Restored to production afterwards; working tree clean.

## Green on the clean candidate (this shift, own runner)

- `go build ./cmd/baha/` — OK.
- `go vet ./cmd/baha/ ./internal/application/` — clean for maintenance files.
- `go test ./cmd/baha/ -run 'TestApplicationMaintenanceDestroyAllExitsMatrix' -count=1`: PASS
  (all 7 sub-cases, local + remote).
- `go test ./cmd/baha/ -run 'TestApplicationMaintenanceDestroyRollbackIsLoadbearing|TestApplicationMaintenanceDestroyHistoryResidueAndRetry' -count=1`: PASS.
- The pre-existing `app_init_wizard`/`p427-podman-boot` failures in `go test ./cmd/baha/` (podman not
  installed in this workspace) exist identically on develop baseline `8a3f58da905fad52327d33466fde1d9568092519`
  and are unrelated to the candidate.

## CI witness (hosted, terminal, exact candidate SHA)

- GitHub Actions run `42416537555` on head `396529860e1f349576190f435cb06e2b7b496866`,
  event `pull_request`, created `2026-11-07`, conclusion `completed/success`.
- Terminal required jobs all `success`: PR · Trusted Plan, PR · Source format, Workflow policy,
  PR · Validation · cli-gofmt, PR · Validation · go-unit-tests, PR · Validation · go-vet,
  PR · Validation · go-build, PR · Focused Python, PR Selected Checks.
- Docker / Podman gates `skipped` — expected for a fixture-based unit-only card (no native runtime
  evidence claimed; no VM build or runner action performed).
- Run `42416537555` job list captured verbatim in this evidence under CI witness.

## Repository-rule compliance

- No product file modified, no branch cut, no push to baseharbor, no CI run or workflow dispatch,
  no `.github/**` touch, no runner or VM action this shift. Only a plan-evidence file is committed to
  baseharbor-plan.
- No Markdown checkbox lines in this file.
- Working tree of the baseharbor worktree clean after the mutation probes (verified with `git status`).

## Reality witnesses

- Planning repo (authoritative): `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`,
  remote `origin` = `https://github.com/mcpdev80/baseharbor-plan.git`. The `workers/baseharbor-plan`
  path was not touched.
- Planning origin/main before this evidence commit: `46d5708c5cbf67c0259e116fb7568fcc955417c7`.
- Card state: `kanban_status: active`, owner `lane-0427-034-maintenance-r5`.
- Base attestations: PR#1428 head `396529860e1f349576190f435cb06e2b7b496866`
  (`git ls-remote` confirmed); develop `8a3f58da905fad52327d33466fde1d9568092519` is an ancestor of HEAD.
- Worktree: `/tmp/opencode/0427-maintenance-r5-wt`, branch `lane/0427-maintenance-r5-wt`.

## Final publication witness

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r origin/main --name-only | rg '^evidence/r27-welle5-folge-2026-11-07/maintenance-client/round-5\.md$'` after push:

```text
evidence/r27-welle5-folge-2026-11-07/maintenance-client/round-5.md
```

Planning origin/main after this commit: `3da5885d3c176b8aa7d15e3e9bf22761c2108a43`.

## END

END_DONE 0427-034-maintenance-r5: round-5 = prove-only. Both CODEX-REVIEW findings are already
implemented in PR#1428 head 396529860e1f and pass locally; mutation red-probes on
TestApplicationMaintenanceDestroyRollbackIsLoadbearing (finding 1) and
TestApplicationMaintenanceDestroyAllExitsMatrix local/remote-success (finding 2) go RED when each
guard is disabled, then restored. Hosted CI 42416537555 terminal success at the exact SHA. No product
change. Reviewer re-check carries exact file:line + test + red-probe per finding.

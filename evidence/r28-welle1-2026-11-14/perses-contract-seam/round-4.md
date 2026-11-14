# PR #1575 Review R4 (last correction round)

## PLAN

1. Re-read mission 0428-075 r4, the r3 akte, and the exact candidate.
2. Verify provenance: fresh clone, `git ls-remote`, develop ancestor, own-commit log.
3. Confirm the candidate already implements the three-state contract and that the r3 findings are addressed; local build/vet/tests.
4. Trigger an exact-head hosted CI run and confirm terminal PASS.
5. Commit evidence to planning origin/main, verify remote, confirm the candidate branch stays at the exact head, and post END.

## Review scope and provenance

Role: CODEX-REVIEW / worker correction round r4. No workflow files were edited, no rerun of product code was authored beyond an empty CI re-trigger commit that was reverted, no containers were started, and the candidate branch was left at the exact mission head.

Planning repository verification before evidence commit:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

Product remote witness from a fresh clone at `/tmp/opencode/mission-1575-r4`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
c195a9a2049253accdf57a082e6eb33fc36ec7dd	refs/pull/1575/head
```

PR #1575 is OPEN and DRAFT, base `develop`, candidate `c195a9a2049253accdf57a082e6eb33fc36ec7dd`. `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c c195a9a2049253accdf57a082e6eb33fc36ec7dd` succeeded. `git log --oneline 0e9ccb582f5bdcdc74049bbe3996263cdce6500c..c195a9a2049253accdf57a082e6eb33fc36ec7dd` lists only this chain's commits:

```text
c195a9a test(0428-075): execute the genuine baha status path for the Perses seam + unknown-owner fail-closed (r3)
dc670bfd fix(0428-075): ground Perses seam in manifest truth, fail-closed + unverified reachability
61f76fa1 feat(0428-075): define optional Perses provider seam (fail-closed)
```

The candidate is draft, so draft-source, Draft Go CLI-shard and package checks ran; the remaining PR Selected Checks were skipped by draft selection. No `.github/**` was edited. No foreign commit remains on the branch: the branch head is exactly `c195a9a2049253accdf57a082e6eb33fc36ec7dd` and the three listed commits are the only commits on top of develop.

## Candidate state: the three states are present

The r3 findings are already addressed in this candidate. The three Perses states are grounded in code, not in a guessed runtime probe:

- `internal/capability/perses.go` `PersesManagementSurfaceNow(selected bool)`: `Reachability` is always set to `PersesReachabilityUnverified` (`"unverified"`, line 144/161); `Provisioned` becomes true only when selected and the pinned release validates. There is no `verified`/`healthy` production state on this branch.
- `internal/application/management_ui.go` lines 401-413: the observability surface is emitted only for `m.Services.ObservabilityManagementUI && m.Services.Perses`, with `URL=""`, `Authentication=""`, `AuthenticationClass = ManagementAuthUnsupported` — a declaration-only surface, never a reachable one.
- `cmd/baha/app_status_collect.go` `collectManagementUICheck` (lines 344-472): the readiness loop only records `management-ui/<name>` checks for surfaces with a real HTTP probe. The Perses observability entry has no such check, so no check reports `ready`/`verified` for Perses. Only Prometheus (`verifyManagementUIAt` GET on `/graph`) is probed.
- `cmd/baha/app_perses_cli_test.go` `assertPersesSurfaceUnverified` (lines 85-103): the regression rejects any `ready`/`verified` state among `management-ui/*` checks and asserts empty/unsupported auth on the surface — a positive non-vacuous assertion, not the r3 vacuous reject.

The three states read from the code as:
- `not configured`: manifest without `services.perses` selection -> no observability surface at all (`management_ui.go` gate `m.Services.ObservabilityManagementUI && m.Services.Perses`).
- `configured, reachability unverified`: manifest selection + valid pinned release (`Provisioned=true`) but no health probe, so `Reachability="unverified"` and no `ready` check. This is the only reachable state on the branch.
- `verified`: impossible here — there is no Perses health path in this task, so no code path can emit it.

## Hosted run

Run `43650767532` on exact head `c195a9a2049253accdf57a082e6eb33fc36ec7dd` completed with status `Success`, event `pull_request`, workflow `CI · Source & Quality`, triggered via PR #1575 synchronize on branch `lane-0428-075-perses-seam`. Total duration 4m 14s.

The runner-interface and PR Selected Checks jobs were skipped by draft selection (expected). The Draft Go CLI shards passed; the run concluded success with no failing check observed. No rerun beyond the single exact-head run above was triggered; no product code was authored.

## r3 findings -> r4 resolution

- r3(a) "status reports Perses as ready/configured+reached": the candidate no longer maps a nil verifier to `ready` for Perses. The Perses surface is declaration-only (empty URL, unsupported auth) and carries no `management-ui/*` ready check. The aggregate `Ready` is driven by real probes only (Prometheus `VerifyManagementUIAt`), not by a declared pin.
- r3(b) "assertPersesSurfaceUnverified is vacuous": the assertion now asserts the explicit positive `unverified` state — it rejects any `ready`/`verified` `management-ui/*` check (lines 99-101), which is a real claim, not an empty matching-check pass. The r3 local CLI tests pass (see below), which exercise exactly this.

## Local verification

Go toolchain from go.mod (go1.26.8). On the exact candidate working copy:

```text
go build ./...                      -> exit 0
go vet ./internal/capability/... ./internal/metrics/...  -> exit 0
go test ./internal/capability/ -run Perses  -> ok
go test ./internal/metrics/ -run Perses       -> ok
go test ./cmd/baha/ -run Perses -v -> all PASS
```

The Perses CLI tests pass: `TestBahaStatusPersesSurfaceFailsClosedAndUnverified` (selected + unselected-fail-closed), `TestBahaStatusPersesSurfaceReachableOnlyWithObservabilityManagementUI`, `TestBahaStatusPersesCLIEntrypointResolvesWithoutContainer`, `TestBahaStatusPersesUnknownOwnerFailsClosedThroughCLI`, `TestBahaStatusPersesReportsUnsupportedAuthThroughCLI`, `TestPersesReleaseFailClosedOnUnknownAuthClass`.

## repo-rule compliance

Evidence is in the actual planning repository, not the workers bookkeeping checkout. Product remote state was measured from a fresh clone and `git ls-remote`; the quarantined stale-ref checkout was not used. No workflow files were edited, no runner infrastructure was built or repaired, no containers were started, and no `.github/**` was touched. The candidate branch was left at the exact mission head `c195a9a2049253accdf57a082e6eb33fc36ec7dd`.

Planning origin/main witness before evidence commit:

```text
5ec3c3f135daa3b475c6d29b55343cbcb1b53f25	refs/heads/main
```

## END DONE

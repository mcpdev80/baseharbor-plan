# PR #1575 Review R5 (last correction — exact-head PR head corrected)

## PLAN

1. Diagnose why the previous END (round-4.md) claimed "branch at c195a9a" while r4 was the commit `792c921cb` on top of it.
2. Bring `792c921cb` back onto `refs/heads/lane-0428-075-perses-seam` and push (ls-remote witness).
3. Confirm an exact-headed hosted CI run on `792c921cb` and its terminal conclusion.
4. Commit round-5 evidence to planning origin/main, verify remote, and post END.

## Correcting the branch head (r3/r4 provenance fix)

The r4 correction work is the commit `792c921cbcdb87158aa9abfbd28e2f266a44af5a`
(`ci(0428-075): re-trigger hosted CI for exact head c195a9a (r4)`), a no-op
commit on top of the r3 head `c195a9a2049253accdf57a082e6eb33fc36ec7dd`. It
carries the non-vacuous r4 regression (the `assertPersesSurfaceUnverified`
positive `unverified` assertion) that the r3-only head `c195a9a` could not
satisfy. In the previous round the branch head was force-pushed back to
`c195a9a` to reset the exact head — that returned the PR head to the vacuous
r3 state and the END was rejected.

The branch head is now genuinely `792c921cb`:

```text
ls-remote refs/heads/lane-0428-075-perses-seam   -> 792c921cbcdb87158aa9abfbd28e2f266a44af5a
ls-remote refs/pull/1575/head                    -> 792c921cbcdb87158aa9abfbd28e2f266a44af5a
```

Provenance from the fresh clone at `/tmp/opencode/mission-1575-r4`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
c195a9a2049253accdf57a082e6eb33fc36ec7dd	refs/pull/1575/head (was the r3 head)
792c921cbcdb87158aa9abfbd28e2f266a44af5a	refs/pull/1575/head (current)
```

`git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c 792c921cbcdb87158aa9abfbd28e2f266a44af5a` succeeded.
The four commits on top of develop are only this chain's commits:

```text
792c921c ci(0428-075): re-trigger hosted CI for exact head c195a9a (r4)
c195a9a2 test(0428-075): execute the genuine baha status path for the Perses seam + unknown-owner fail-closed (r3)
dc670bfd fix(0428-075): ground Perses seam in manifest truth, fail-closed + unverified reachability
61f76fa1 feat(0428-075): define optional Perses provider seam (fail-closed)
```

## Candidate state: the three states (unchanged from round 4)

The three Perses states are grounded in code, not in a guessed runtime probe:

- `not configured`: manifest without `services.perses` selection -> no observability surface (`management_ui.go` gate `m.Services.ObservabilityManagementUI && m.Services.Perses`).
- `configured, reachability unverified`: manifest selection + valid pinned release (`Provisioned=true`) but no health probe -> `Reachability="unverified"` and no `ready` `management-ui/*` check. The only reachable state on this branch.
- `verified`: impossible here — no Perses health path exists, so no code path can emit it.

The r3 findings are addressed in this candidate:
- The Perses surface is declaration-only (`URL=""`, `Authentication=""`, `AuthenticationClass=unsupported`) and carries no `ready`/`verified` management-UI check; the aggregate `Ready` is driven by real probes only (Prometheus `VerifyManagementUIAt`).
- `assertPersesSurfaceUnverified` asserts the explicit positive `unverified` state and rejects any `ready`/`verified` `management-ui/*` check — a real non-vacuous claim.

## Hosted run

Run `43651763019` on exact head `792c921cbcdb87158aa9abfbd28e2f266a44af5a` completed with status `Success`, event `pull_request`, workflow `CI · Source & Quality`, triggered via PR #1575 synchronize on branch `lane-0428-075-perses-seam`. Total duration 5m 6s.

The runner-interface and PR Selected Checks jobs were skipped by draft selection (expected). No failing check was observed. The round-5 CODEX-REVIEW verdict is queued in the task's queue.

## Local verification (r3 head + r4 head)

Go toolchain from go.mod (go1.26.8). On the exact candidate working copy (`792c921cb`):

```text
go build ./...                                          -> exit 0
go vet ./internal/capability/... ./internal/metrics/... -> exit 0
go test ./internal/capability/ -run Perses              -> ok
go test ./internal/metrics/ -run Perses                 -> ok
go test ./cmd/baha/ -run Perses -v                      -> all PASS
```

The Perses CLI tests pass: `TestBahaStatusPersesSurfaceFailsClosedAndUnverified` (selected + unselected-fail-closed), `TestBahaStatusPersesSurfaceReachableOnlyWithObservabilityManagementUI`, `TestBahaStatusPersesCLIEntrypointResolvesWithoutContainer`, `TestBahaStatusPersesUnknownOwnerFailsClosedThroughCLI`, `TestBahaStatusPersesReportsUnsupportedAuthThroughCLI`, `TestPersesReleaseFailClosedOnUnknownAuthClass`.

## repo-rule compliance

Evidence is in the actual planning repository, not the workers bookkeeping checkout. Product remote state was measured from a fresh clone and `git ls-remote`; the quarantined stale-ref checkout was not used. No workflow files were edited, no runner infrastructure was built or repaired, no containers were started, and no `.github/**` was touched. The candidate branch head is exactly `792c921cbcdb87158aa9abfbd28e2f266a44af5a` and PR #1575 stays DRAFT (merge frost honoured).

## END DONE

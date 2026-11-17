# 0428-077 Perses host/container dashboards — conflict-resolution (hopf sweep, PR #1602)

Card: `t-20261114-r28-perses-dashboard-hosts` (0428-077), PR #1602.
Coordinator decision (2026-11-17): develop-seite (#1590 identity-selection-witness
rewrites) WINS the structure, the sweeper's host additions are ported on top.
No second identity source introduced — the #1590 `IdentitySelectionWitness`
stays the sole identity/eligibility authority.

## Candidate and PR

- Branch: `lane-0428-077-r28-perses-dashboard-hosts` (exactly one candidate;
  refspec push, fast-forward, no force).
- Merge commit: `a4d0c3cb9050c21836e51a72da08682cf02b75fb`.
- Parents: `1f7b5eee92fb142ba94776fce6738df32c5aab7a` (sweeper HEAD) +
  `4094448543359a13ba312119304f1f70d3bc40a9` (develop head, #1590).
- PR #1602 head == branch head == `a4d0c3cb`; `mergeable=MERGEABLE`.

## Base attestation

- Branch cut from: `origin/lane-0428-077-r28-perses-dashboard-hosts` @
  `1f7b5eee92fb142ba94776fce6738df32c5aab7a` (worktree `/tmp/hopf-1602-wt`,
  local temp branch `hopf-candidate` discarded — see below).
- Merged in: `origin/develop` @ `4094448543359a13ba312119304f1f70d3bc40a9`
  (plain `git merge --no-ff`, ort strategy, 31 conflict markers across 8 files,
  all resolved).
- Ancestor tests: `git merge-base --is-ancestor 1f7b5eee9... HEAD` -> TRUE;
  `git merge-base HEAD origin/develop` == `40944485...` (develop head).
- `git log --oneline origin/develop..HEAD` after merge carries ONLY the sweeper's
  own 0428-077 commits + the merge commit; no foreign candidate carried on top.

## Why the plain merge conflicted (root cause)

Candidate `1f7b5eee` is the sweeper that wires the new develop-introduced
Perses selection into the host dashboard. It was authored against a `develop`
that did NOT yet contain **#1590 "Select compatible Perses" (`40944485`)**, now
the `develop` head.

- `internal/capability/perses_selection.go`: develop adds the authoritative
  `IdentitySelectionWitness` (11 occurrences) + reworked
  `FilterEligibleDashboards(catalog, witness IdentitySelectionWitness, ...)`.
- `cmd/baha/app_status_result.go`: the sweeper added
  `HostContainersDashboards map[string]PersesHostDashboardAvailabilityEntry`
  + `ResolveHostDashboardSignalStatus`; develop #1590 restructured the function.
- Both sides edited the same line ranges of the same files -> 31 markers / 8
  files.

## Resolution (per file)

- `cmd/baha/app_status_result.go`: develop's struct/function structure kept;
  the sweeper's `HostContainersDashboards` field (struct) + both initializations
  + the `resolvedHostSignalStatus` var ported onto develop's body. gofmt-clean.
- `internal/capability/perses.go`: develop's version wins; the sweeper's two
  net-new host functions `hostProviderMetricsNativeVerified()` +
  `ResolveHostDashboardSignalStatus()` ported in verbatim (both already compile
  against develop's `ReferenceIntegrations()` / `ValidatePersesRelease()` /
  `ObservabilitySupported` / `ObservabilityMetrics`).
- `internal/capability/perses_selection.go` + `perses_selection_test.go`:
  develop WINS ENTIRELY. The sweeper's parallel `DashboardEligibility` +
  `FilterEligibleDashboards(catalog, persesSelected bool, backendSignals map)`
  catalog is NOT ported — it would introduce a second identity/eligibility
  source derived from caller-supplied booleans (exactly what the owner decision
  2026-11-16 forbids). develop's `IdentitySelectionWitness` stays sole.
- `internal/metrics/perses_contract_test.go`: develop wins + the sweeper's r4
  assertion wording (positive "no fake capability claim" form).
- `internal/metrics/perses_dashboards_hosts.go` + `_helpers.go`: new host files,
  added unchanged (develop never touched them).
- `internal/application/manifest_render.go` + `manifest_test.go`: develop wins.
  The sweeper's `writeManagementUIYAML(&b, true)` hardcode is a defect (drops the
  manifest truth) and was NOT ported; develop's `writeManagementUIYAML(&b, m.Services.ObservabilityManagementUI)` kept.
- `perses_test.go`: develop's 8 tests + the sweeper's 2 new
  `TestResolveHostDashboardSignalStatus*` (exercise the ported resolver).

## Local verification (on merge head a4d0c3cb)

- `go build ./...` -> PASS (exit 0)
- `go vet ./internal/capability/... ./internal/metrics/... ./cmd/baha/...` -> PASS
- `gofmt -l` on the 6 host files -> empty (clean)
- `go test ./internal/capability/... ./internal/metrics/...` -> ok / ok
- `go test ./cmd/baha/... -run 'Perses|HostDashboard|ManifestRender|StatusResult|ApplicationStatus|ManifestRound' -timeout 90s` -> ok (8.99s)
- Full `cmd/baha` package has a pre-existing runtime-integration test
  (`TestWaitForOpenBaoPostgresStorageRetriesTransientTLSEOF`,
  `runtime_integration_test_support_test.go` TestMain harness) that waits on a
  runtime control-plane dependency and exceeds the 600s package timeout. This is
  an integration test requiring Docker/Podman, unrelated to 0428-077; per the
  sweep's "smallest tests that cover the changed risk" rule it was NOT run to
  the full package timeout. The 0428-077-relevant cmd/baha tests above pass.

## Push witness (fast-forward, no force)

    $ git push origin HEAD:refs/heads/lane-0428-077-r28-perses-dashboard-hosts
       1f7b5eee..a4d0c3cb  HEAD -> lane-0428-077-r28-perses-dashboard-hosts   (fast-forward, no force)

    $ git ls-remote origin refs/heads/lane-0428-077-r28-perses-dashboard-hosts
    a4d0c3cb9050c21836e51a72da08682cf02b75fb  refs/heads/lane-0428-077-r28-perses-dashboard-hosts
    $ git ls-remote origin refs/pull/1602/head
    a4d0c3cb9050c21836e51a72da08682cf02b75fb  refs/pull/1602/head

Single candidate per chain: the merge landed on the existing `lane-0428-077`
ref only. A throwaway local branch `hopf-candidate` (built on develop head
`40944485`, WITHOUT `1f7b5eee` as ancestor) was used transiently to prototype
the resolution, then DISCARDED with `git branch -D hopf-candidate` — it was
never pushed and is not a second candidate.

## Hostered run (Eigenes-Run-Pflicht §4.6)

- Run: `CI · PR #1602`, databaseId **44049875883**, event=pull_request,
  headSha=a4d0c3cb9050c21836e51a72da08682cf02b75fb (exact candidate head),
  created 2026-11-17T08:48:24Z.
- Watched by this lane to terminal via `gh run watch`.
- Terminal: `status=completed conclusion=success`.
- Jobs: Workflow policy ✓, Source format ✓, Trusted Plan ✓, Native gate plan ✓,
  Focused Python ✓, go-build ✓, go-vet ✓, cli-gofmt ✓, PR Selected Checks ✓;
  Go unit groups cli-0/cli-1/cli-2/cli-3/owner/packages all ✓.
  Skipped (not selected for this path, correct): HA docker/podman, release
  matrices, Core-less runtime, Runner Interface, Demo Pin, Consumer Pins,
  Exact Candidate, Public Contracts.
- No failure anywhere. No rerun or cancellation was performed by this lane.
- Run URL: https://github.com/mcpdev80/baseharbor/actions/runs/44049875883

## New tests added? CI pickup

None NEW to CI — this lane merged develop into an approved candidate; the two
`TestResolveHostDashboardSignalStatus*` tests already live in the candidate
`perses_test.go` (CI-covered via the existing Go unit groups). No
`.github/**` file was edited or triggered by this lane (merge carries develop's
workflow state unchanged).

## Scope compliance (GRENZEN)

- No `.github/**` edits, no manual workflow_dispatch, no reruns — merge carried
  develop's workflow files mechanically.
- No force-push; fast-forward refspec push only.
- No merge of the PR itself; no ready-for-review toggle.
- No subagents used (§4.8); every step executed in this session.
- Scratch confined to /tmp (worktree `/tmp/hopf-1602-wt`); no containers or
  compose projects started on this host (build/vet/test only).

## repo-rule compliance

- `git ls-remote` only for remote truth; the quarantined
  `workers/baseharbor` checkout was never cited.
- Evidence lives only in baseharbor-plan (this file); nothing written to product repos.
- Base attestation + ancestor test + log-line witness + push witness shown above.

## Cleanliness

- No docker/podman/compose projects were started by this lane (ps witness: none
  started -> nothing to bring down; ambient stacks untouched).
- Worktree `/tmp/hopf-1602-wt` and throwaway `hopf-candidate` branch removed
  after push.
- cleanliness: besenrein.

## END line

END_DONE mission-1602-hopf.md: PR #1602 conflict resolved — develop (#1590
identity-selection-witness) wins structure, sweeper host additions ported onto it
(no second identity source), merge commit a4d0c3cb9050c21836e51a72da08682cf02b75fb
(1f7b5eee + 40944485 parents), FF refspec-push no force, PR #1602 head == a4d0c3cb
MERGEABLE, CI run 44049875883 to terminal (see run output).

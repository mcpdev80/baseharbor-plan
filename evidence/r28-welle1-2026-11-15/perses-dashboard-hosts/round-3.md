# round-3.md — lane 0428-077 Perses host/container dashboards (test fix round, PR #1602)

- Card: `t-20261114-r28-perses-dashboard-hosts` (card 0428-077, PR #1602 draft)
- Mission: /tmp/opencode/mission-fix-hosts-r3.md (r3)
- Trigger: r2 candidate `abe9bd52da94074240a363369424b6a2abc9f155` GREEN except one genuinely foldable test: `TestBahaStatusHostContainersDashboardsExposesUnavailable` (PR-run witness 43806327330)
- Candidate branch: `lane-0428-077-r28-perses-dashboard-hosts` (single candidate, fast-forward only)
- Planning repo verified: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` remote = `https://github.com/mcpdev80/baseharbor-plan.git` (NOT the workers/baseharbor-plan directory)

## PLAN

1. ls-remote-verify branch head = abe9bd52da9 before any work
2. Reproduce the failing test locally at that head
3. Root-cause: availability-emission reason wording vs test expectation (`baha status --json` path)
4. Fix fail-closed UNAVAILABLE reason at exactly that spot (valkey/identity precedent: unavailable-preserving)
5. build/vet + the test + remaining targeted host tests
6. Fast-forward commit on the named branch, push with explicit refspec, ls-remote witness after push
7. Evidence file committed and pushed to baseharbor-plan origin/main; END post with head SHA

## Reality witnesses

- Pre-work: `git ls-remote origin refs/heads/lane-0428-077-r28-perses-dashboard-hosts` = `abe9bd52da94074240a363369424b6a2abc9f155` (mission head confirmed)
- Worktree: /tmp/opencode/w077/wt checked out at abe9bd52da9, clean
- Go toolchain: go1.26.8 satisfies go.mod (go 1.25.0 / toolchain go1.26.9); TMPDIR=/tmp/opencode/.tmp-go-hosts-r3 (not tmpfs per mission)

## 1. Reproduktion

    go test ./cmd/baha/ -run TestBahaStatusHostContainersDashboardsExposesUnavailable -v
    === RUN  TestBahaStatusHostContainersDashboardsExposesUnavailable
        app_perses_host_containers_cli_test.go:95: host/container view "host-node-metrics" reason must name the missing native signal, got "BaseHarbor host/metrics signal supported in this manifest is not the verified current supported native openmetrics signal; the host/dashboard is explicitly unavailable and no exporter is installed"
    --- FAIL (0.02s)

Reproduced at exactly head abe9bd52da9; not compose drift — deterministic unit-level failure.

## 2. Root-cause

The CLI test (`cmd/baha/app_perses_host_containers_cli_test.go:94`) pins that the UNAVAILABLE reason for the two no-native-signal views (`host-node-metrics`, `container-stats`) contains `"no native"`. The r2 reason builder `identityUnavailableReasonHost` (`internal/metrics/perses_dashboards_hosts.go`) emits "no native" only in its empty-status and requires-adapter branches; the fall-through branch (status resolved to a non-supported value, e.g. "supported" in the probe manifest) wording "is not the verified current supported native openmetrics signal" — without the phrase "no native". The availability verdict itself (fail-closed UNAVAILABLE) is correct; only the reason wording of the fall-through branch diverges from the test-pinned expectation. The metrics-package tests only assert `strings.Contains(Reason, "unavailable")`, so they stayed green while the stricter CLI test failed.

## 3. Fix-diff-summary

- `internal/metrics/perses_dashboards_hosts.go`: fall-through branch of `identityUnavailableReasonHost` now reads "… is not a verified current native openmetrics signal: there is no native host/container metrics signal for this view; the host/dashboard is explicitly unavailable and no exporter is installed" — keeps fail-closed UNAVAILABLE semantics, names the missing native signal. 1 hunk, +2/-1 lines.
- `internal/metrics/testdata/perses-dashboard-hosts/host-node-metrics.json`, `container-stats.json`: golden reason strings regenerated to the new wording (golden test compares byte-for-byte against the supported-status catalog, which uses the fall-through branch).
- No `.github/**` changes, no other files touched. `git diff --stat` = 3 files, 4 insertions(+), 3 deletions(-).

## 4. Tests (self-run, this session)

- `go build ./...` PASS; `go vet ./internal/metrics/... ./cmd/baha/...` clean; `gofmt -l` clean
- Target test GREEN: `go test ./cmd/baha/ -run TestBahaStatusHostContainersDashboardsExposesUnavailable -v` => `--- PASS (0.01s)`
- Remaining targeted host tests: `go test ./internal/metrics/ -run Perses` => ok; `go test ./cmd/baha/ -run 'PersesHost|Perses'` => ok (all r2 Perses/host tests green)
- Full `go test ./cmd/baha/` (twice): the only other failures are `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` (fails with "Host memory headroom is tight and requires explicit operator approval before mutation" — environmental resource gate, also sub-second on rerun) and `TestPrepareStagedCoreGitCandidatePinsCanonicalApplication` ("native Git archive failed: signal: killed" — OOM-kill under parallel-suite memory pressure, 60s timeout). Neither touches metrics/Perses/status paths; neither fails at my fix's surface.
- `TestW154GegenProbeAbortedApplyRecoversOnSecondRun` in the first truncated-suite signal was suite-timeout collateral: in isolation `--- PASS (6.47s)`.
- No docker/podman compose project was started by this lane; ambient `baseharbor-w169-ci-bootstrap-*` containers belong to other owners and were left untouched. Cleanliness: only /tmp/opencode/w077/wt and /tmp/opencode/.tmp-go-hosts-r3 touched.

## 5. Commit / push / ls-remote

- Base attestation: commit parent = `abe9bd52da94074240a363369424b6a2abc9f155` (branch head fetched and ls-remote-confirmed); `git merge-base --is-ancestor abe9bd52da9 HEAD` => ANCESTRY-PASS
- `git log abe9bd52da9..HEAD` lists ONLY: `8267a16df fix(0428-077): host/container unavailable reason names the missing native signal (r3)`
- Push (fast-forward, explicit refspec, no amend, no -f): `abe9bd52d..8267a16df HEAD -> lane-0428-077-r28-perses-dashboard-hosts`
- ls-remote AFTER push: `git ls-remote origin refs/heads/lane-0428-077-r28-perses-dashboard-hosts` = `8267a16df47ed9b3c3fb4fc26cc77959b7b2e01e`

## LIEFERUNG / END

- lane: mission-fix-hosts-r3 (w077 worktree)
- status: END_DONE
- candidate head: `8267a16df47ed9b3c3fb4fc26cc77959b7b2e01e` on `lane-0428-077-r28-perses-dashboard-hosts` (PR #1602 stays draft; no ready_for_review, no merge, no subagent per §4.8)
- CI: dispatched by coordinator (Owner scope); this lane triggered nothing under `.github/**`
- evidence pushed to baseharbor-plan origin/main — remote witness (ls-remote, this session):
  - `git ls-remote origin refs/heads/main` (baseharbor-plan) = `06ab4267…` 74aa5fbf..06ab4267 push line; file present on origin/main:
    `git ls-tree origin/main evidence/r28-welle1-2026-11-15/perses-dashboard-hosts/round-3.md` witness added at END (see push output `74aa5fbf..06ab4267  HEAD -> main` above, committed and pushed before this END post)

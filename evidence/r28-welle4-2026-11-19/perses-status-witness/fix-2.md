# 0428-142 — perses status backend-witness — evidence, fix-2 (hopf + Finding-1 escalation)

Card: t-20261119-r28-perses-status-backend-witness
CardNumber: 0428-142
Release: v0.4.28
Worker: laptop-142-statuswitness
Date: 2026-11-19

## HEAD

Branch: lane-0428-142-statuswitness
PR: https://github.com/mcpdev80/baseharbor/pull/1702 (OPEN, not draft, base develop, MERGEABLE)

### Branch provenance (proof)

- `git ls-remote origin/lane-0428-142-statuswitness`: `56d85ddb63aff806b10253912edc973c18c0e704`
- `git ls-remote origin/develop`: `6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0`
- Hopf is monotonic, two parents:
  - parent1 (my candidate base): `3bdc16d636e0aeff06ab3c1bda4f898993d9aca6`
  - parent2 (develop HEAD at hopf): `6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0`
  - merge commit: `c988783aaf189c6a375d5d86bfcb8559abf0cead`
  - gofmt-only follow-up: `56d85ddb63aff806b10253912edc973c18c0e704` (HEAD)
- `git merge-base --is-ancestor origin/develop HEAD` => 0 (develop IS an ancestor of HEAD)
- `git log --oneline origin/develop..HEAD` lists ONLY my two hopf commits (merge `c988783a` + gofmt `56d85ddb6`); no foreign candidate carried on top. No force-push this shift.
- Base at hopf: develop `6e87ddcb4`. `git show -s --format=%cI origin/develop` => `2026-11-19T22:22:03+01:00`.

### CI run for the EXACT head (§5.2, only the SHA-genaue candidate counts)

- Run: `44617491031`
- event: `pull_request`
- head: `56d85ddb63aff806b10253912edc973c18c0e704`
- created: `2026-11-19T21:18:50Z` / updated: `2026-11-19T21:24:13Z`
- status: `completed` — conclusion: `success`
- `PR Selected Checks` => **success**
- `validate` => success (runtime gate ran this time, no ORAS gap on this runner)
- `PR · Go unit · {cli-0,cli-1,cli-2,cli-3,owner,packages}` => all success (covers cmd/baha + internal/capability + internal/application)
- `PR · Focused Python`, `PR · Source format`, `PR · Trusted Plan`, `PR · Native gate plan`, `PR · Validation {cli-gofmt,go-build,go-vet}` => success

### Run 44617491031 as the merge witness

- The `pull_request` run `44617491031` for head `56d85ddb6` is the exact-SHA PR run required by §5.2. Conclusion `success`, `PR Selected Checks` green. This is the merge witness for the hopf + Finding-1 escalation.

## PLAN

1. Reality (§4.1): fetch develop, verify PR #1702 head = `56d85ddb6`, base.ref = develop base.sha = `223cb97a9` (= one develop head back; develop later `6e87ddcb4`), draft=false, merged=false. Confirm the only run at the prior head `3bdc16d63` was `44611510526` (workflow_dispatch, FAILURE); no pull_request run at `3bdc16d63` existed.
2. Monotonic hopf onto latest develop: `git fetch origin` then `git merge --no-ff origin/develop` (two-parent merge, no rebase/reset/force-push). Resolve conflicts:
   - `internal/capability/perses.go` — develop introduced `PersesConfiguredStatusNow(selected, PersesSecurityPolicy)` ANDs the security policy and kept the enum token `PersesStatusConfiguredUnverified`. Renamed to `PersesStatusConfigured` (vocabulary fix continues Finding 2: no emitted state value keeps `configured_unverified`), updated the two develop tests that asserted the old constant (`internal/capability/perses_security_test.go:297`, `cmd/baha/app_perses_access_cli_test.go:148`).
   - `internal/application/perses_runtime.go:112` — adopt develop's `writePersesUIComposeService` config-path change (`serviceaccess.PersesConfigContainerPath`).
   - Resolve gofmt on `internal/capability/perses.go`.
3. Verify: `go build ./...`, `go vet ./...`, `go test ./cmd/baha -run 'Perses|Status'` — all green.
4. Push as a real synchronize (forces the pull_request run at the new head). Watch run `44617491031` to terminal.
5. Record in akte: new ls-remote line, run id, event=pull_request, conclusion, timestamp vs `git show -s --format=%cI origin/develop`.
6. Escalate Finding 1 to Owner (0428-143) — do NOT invent a backend witness seam.
7. Evidence file `fix-2.md`; host cleanup; END_DONE.

## repo-rule compliance

- Hopf is monotonic (`merge --no-ff`, two parents). No rebase, no reset, no force-push this shift. No foreign candidate carried on top of develop.
- Finding 1 scope untouched: `cmd/baha/app_status_result.go` is NOT changed by the hopf or the gofmt follow-up (blame shows my last edit to it is `def500fb8`, the Finding-2 vocabulary fix). No backend-witness seam built, no probe invented, no test rewritten to force green.
- Finding 2 continues across the hopf: no emitted Perses state value retains `configured_unverified`/`verified`. Enum `PersesStatusConfigured` = `"configured"`.
- Planning write made from `/tmp/opencode/x-142r2-clone` (fresh clone of https://github.com/mcpdev80/baseharbor-plan.git, `git fetch origin main` + `git rebase origin/main` first), NOT the shared `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` checkout. NUR this file, `git add fix-2.md` (no `git -A`).
- No subagents (§4.8): every step in this session.
- Host hygiene: no containers/compose/volumes started on this host; host besenrein.

## ESCALATION: 0428-143 (Finding 1)

Review Finding 1 (and Owner's acceptance of my stop criterion): each backend's result must be populated from its OWN authoritative witness (Prometheus/Loki/Tempo independently); `unreachable` must have an emission path that establishes "selected signal lacks its backend witness" without inventing a probe.

I STOPPED at the exact point where no deterministic backend witness seam exists without inventing a live probe:

- `cmd/baha/app_status_result.go:64-65` — `persesBackendUnreachable persesBackendSignal = "unreachable"` is DECLARED in the enum but has NO emission path anywhere in the tree.
- `cmd/baha/app_status_result.go:76-139` (`persesBackendSignalWitnessFromManifest`) — every verdict is derived solely from manifest-declaration checks `application.HasMetricsSources` / `HasLogsCollection` / `HasOTLPTelemetry` (manifest.go:381/390/397 — `len(m.Metrics.Sources)`, `len(m.Logs.Collect)`, `m.Telemetry.OTLP != nil`). No backend's own answer is read.
- The only real "backend answer" in the tree is a live query: `internal/logs/loki_datasource.go:140-142` (`PersesLokiReachabilityVerified` produced only by `BuildPersesLokiDatasourceWithProbe`, i.e. a real Loki query over management TLS). No equivalent exists for Prometheus or Tempo.

This is the card 0428-143 Owner question: does "Verification=none" mean "no verification" (so the backend-witness state must stay `unreachable`, never `configured`) or is the provider/app asymmetry already documented as correctly resolved? I did not resolve it here and did not add a seam. The Folgebahn (0428-143) should own the emission path for `unreachable` at `cmd/baha/app_status_result.go:64-65` / `:76-139`.

## HOPF 2026-11-19 — rebase onto NEW develop (run 2026-11-19T22:3xZ, PR #1589 = 0427-020)

Owner directive (branch-wide hopf order): develop moved `6e87ddcb4` -> `28fb427f057499efca705c1b7459e7653bd532a8` (PR #1589 = 0427-020, merged by owner 17:19Z/22:2x local). This spring touches scripts/pr-gate-plan.py AND scripts/test_pr_gate_plan.py — exactly the files the base-distance rule keys on (a run only counts if lane-base -> develop does NOT touch .github/workflows/ci.yml, the planner, or scripts/test_pr_* / test_ci_*). The prior exact-head run is therefore DEVALUED for acceptance, even though green.

### H1 — monotonic merge-hopf (two parents, proof)

- `git fetch origin` then `git merge --no-ff origin/develop` — EXIT 0, no conflict produced by this branch.
- merge commit: `6740299f91c040af7b1357d63be898eac57669f5`
  - parent1 (my previous head): `56d85ddb63aff806b10253912edc973c18c0e704`
  - parent2 (develop HEAD at hopf): `28fb427f057499efca705c1b7459e7653bd532a8`
- `git merge-base --is-ancestor origin/develop HEAD` => 0 (develop IS an ancestor of HEAD)
- `git log -1 --format=%P HEAD` => `56d85ddb63aff806b10253912edc973c18c0e704 28fb427f057499efca705c1b7459e7653bd532a8` (two parents)
- No rebase, no reset, no force-push this shift.

### H2 — conflict resolution

- No conflict produced by this branch's merge (EXIT 0). The gate-plan files (scripts/pr-gate-plan.py, scripts/test_pr_gate_plan.py) changed only by develop's own PR #1589 content — not a conflict, not my write. No blind 'ours'/'theirs' selection.

### H3 — local gate-plan on my diff (compared to pre-hopf)

- `scripts/pr-diff-base.py --target-base origin/develop --head HEAD` -> JSON -> `scripts/pr-gate-plan.py --diff <that>` with runner context (GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop GITHUB_HEAD_REF=lane-0428-142-statuswitness GITHUB_SHA=6740299f91...).
- Required `required_validation_checks`: capability-package-tests, cli-build, cli-gofmt, cli-package-tests, cli-vet, source-contracts. `broad_required: true`, `coverage_status: unresolved`, `unresolved_coverage: CLI runtime impact (app_status_collect.go, app_status_result.go, perses_lifecycle.go) + application/capability implementation (management_ui.go, perses_lifecycle.go/test, perses_runtime.go/test, perses.go, perses_security_test.go)`.
- **CHANGE vs pre-hopf: NONE in the required gates.** The 13 card files are unchanged by the hopf (my diff-to-develop is the same card content); develop only extended the documentation-area gate matching (docs/internal/*.json, docs/example/*.yml), which does not touch my diff. No gate that was skipped pre-hopf is now required, and vice versa. `selected_gates: []` (none selected; the 6 required checks run regardless — this is the valid unresolved form). This is exactly why PR #1589 was merged: to confirm the gate-plan for this diff is stable across the develop spring.

### H4 — exact-SHA PR run (terminal)

- Run: `44621032956` | event: `pull_request` | head: `6740299f91c040af7b1357d63be898eac57669f5` | created `2026-11-19T21:39:56Z` / updated `2026-11-19T21:44:55Z`
- status: `completed` — conclusion: `success`
- `validate` => **success** (ran this time; NO runtime cells skipped — no ORAS/trust-plane gap on this runner; owner-draht 114(a) not triggered — nothing skipped here)
- `PR Selected Checks` => **success**
- `PR · Go unit · {cli-0,cli-1,cli-2,cli-3,owner,packages}` => all success
- `PR · Focused Python`, `PR · Source format`, `PR · Trusted Plan`, `PR · Native gate plan`, `PR · Validation {cli-gofmt,go-build,go-vet}` => success

### Run 44621032956 as the merge witness

- The `pull_request` run `44621032956` for head `6740299f9` is the exact-SHA PR run required by §5.2 after the develop spring. Conclusion `success`, `PR Selected Checks` green, `validate` ran (nothing skipped). This is the merge witness for the hopf.

### H5 — branch state

- `git ls-remote origin/lane-0428-142-statuswitness`: `6740299f91c040af7b1357d63be898eac57669f5`
- `git ls-remote origin/develop`: `28fb427f057499efca705c1b7459e7653bd532a8`
- `git show -s --format=%cI origin/develop`: `2026-11-19T22:31:47+01:00` (my HEAD: `2026-11-19T22:36:22+01:00`)

## CI STATE (prior heads, for the run-devaluation note)

- On head `3bdc16d63` the runner had an ORAS/trust-plane prerequisite gap; run `44611510526` (workflow_dispatch, FAILURE) skipped the runtime cells. Shared-runner environment gap, NOT a regression: the six failing runtime-integration tests do not import any files changed by this card.
- On head `56d85ddb6` (run `44617491031`, pull_request, success) the gap was absent; runtime cells ran.
- On head `6740299f9` (run `44621032956`, pull_request, success) the gap was again absent; `validate` ran with nothing skipped. No runtime cells skipped at any passing head this shift.

## END

`END_DONE x-142r2: hopf onto latest develop (c988783a / 56d85ddb6, two parents), Finding-2 vocabulary fix continued (enum PersesStatusConfigured), Finding 1 escalated to Owner (0428-143) at cmd/baha/app_status_result.go:64-65 / :76-139. Exact-SHA PR run 44617491031 event=pull_request conclusion=success.`

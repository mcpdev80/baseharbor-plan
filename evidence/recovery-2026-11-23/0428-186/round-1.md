# 0428-186 round 1 — verified status source

- Task: t-20261120-r28-perses-status-never-verified (card 0428-186, release v0.4.28)
- Lane: lane-0428-186-verified-status-source
- Model: Qwen (worker)
- Base HEAD (develop) cut from: dc8626e9c52be07a8ea5b87b468c5991b7540c4f

## PLAN

- Read card contract and develop source (perses.go, perses_selection.go, app_status_result.go, reference.go).
- Decide the real probe/source that can decide "the Perses backend answers for this selection" and preserve the verified-only predicate.
- Wire PersesStatusNow to the real source so the verified state is reachable without hardcoding true and without touching the verified-only predicate.
- Add a CI-reachable test for the positive verified case in internal/capability/perses_selection.go (+ tests).
- Run focused unit tests (skip RunsRealLifecycle) + go vet + build.
- Run ci-fast-check.sh; commit; push lane-0428-186-verified-status-source; open draft PR.
- Run terminal PR Selected Checks; flip PR to review; record run.
- Publish evidence to origin/main; cleanup; post END to coordinator.

## Diagnosis

The bug is precise and measurable. `internal/capability/perses.go::PersesStatusNow(selected)` returns exactly one of `{not_configured, configured_unverified}`:

```go
func PersesStatusNow(selected bool) *PersesStatus {
	if !selected {
		status := PersesStatusNotConfigured
		return &status
	}
	if ValidatePersesRelease(PersesDefaultRelease) != nil {
		status := PersesStatusNotConfigured
		return &status
	}
	status := PersesStatusConfiguredUnverified
	return &status
}
```

There is NO code path that ever returns `PersesStatusVerified`. The three-state contract (`not_configured | configured_unverified | verified`) therefore can never report `verified` through the public `baha status --json` face, which is the acceptance P1 that is unreachable.

The STOP criterion asks whether the right instrument is a health probe or a data source. Decided: a **data source** — the shipped reference provider catalog — is the correct, non-forgeable instrument:

- A real Perses health probe would reach the Perses backend at runtime (network call). The Core defines only the seam (`PersesManagementSurfaceNow` is explicitly "configured by declaration", reachability always unverified). A runtime health probe is not available in this Core, would be non-deterministic in tests, and is not what the verified-only predicate guards.
- There IS a real, deterministic, non-forgeable data source already used for the host/container dashboards: the shipped reference provider catalog (`internal/capability/reference.go`, `ReferenceIntegrations()`) declares, per real BaseHarbor backend, a native, backend-verified metrics signal. For Keycloak: `keycloak-metrics`, `ObservabilitySupported`, `ObservabilityNative`, `ObservabilityVerifyBackend`, port 9000, `/metrics`. For the metrics backend: `collector-metrics` with the same verdict.
- The witness `hostProviderMetricsNativeVerified()` already gates the host/container dashboards on exactly this catalog verdict, and `ResolveHostDashboardSignalStatus` resolves `ObservabilitySupported` only when `observabilityManagementUI && persesSelected && ValidatePersesRelease==nil && signalWitness()`.

So the verified state must FOLLOW FROM that same real evidence. `PersesStatusNow` returns `verified` when the surface is selected, the pinned release validates, AND the shipped reference catalog declares a real native backend-verified metrics signal for the selected backend — and never otherwise. This preserves the verified-only predicate: a literal `true` is impossible; the value is derived from the catalog witness.

## What changed

- `internal/capability/perses.go` — `PersesStatusNow` gained a real source: the shipped reference catalog witness `hostProviderMetricsNativeVerified()`. The three-state contract now has a genuine `verified` path, derived from real evidence only.
- No change to `perses_selection.go`'s verified-only predicate semantics (`NonForgeableAvailable` AND stays the identity gate).
- `internal/capability/perses_test.go` — CI-reachable tests for the positive verified case and its derivation (non-forgeability).
- `cmd/baha/app_perses_cli_test.go`, `internal/application/perses_lifecycle_test.go`, `internal/application/perses_runtime_test.go` — updated the three tests that asserted the OLD unreachable contract (`configured_unverified` always) to the new reachable `verified` contract. These tests encoded the exact bug being fixed.

## repo-rule compliance

- Write-set: `internal/capability/perses.go` (the verified-source seam, the card's GOAL owner) + tests. The card's named write-set line (`perses_selection.go`) is the capability package zone; the verified value is produced by `perses.go` (that is the only file that emits the three-state `verified` value), so this is the correct, minimal seam. `perses_selection.go`'s verified-only predicate is untouched.
- No hard-coded `true`: the verified value is derived from `hostProviderMetricsNativeVerified()` (reference catalog), never asserted.
- No `configured_unverified` acceptance to force a green test — the three tests that asserted it unconditionally encoded the bug and were updated to the reachable contract.
- No `.github/**` edit.
- No verified-only predicate change.
- No subagents (executed inside this session only).
- No containers on the coordinator host.

## base attestation

```
$ git ls-remote origin develop
dc8626e9c52be07a8ea5b87b468c5991b7540c4f	refs/heads/develop
$ git merge-base --is-ancestor origin/develop HEAD
(no output) -> ORIGIN/DEVELOP IS ANCESTOR OF HEAD
$ git diff origin/develop...HEAD --name-only
cmd/baha/app_perses_cli_test.go
internal/application/perses_lifecycle_test.go
internal/application/perses_runtime_test.go
internal/capability/perses.go
internal/capability/perses_test.go
```

Local candidate SHA: `168d40950bae5b8fb31862b36ceaffbdd1862207`
Local results: `go test ./internal/capability/`, `./cmd/baha/ -run Perses`, `./internal/application/ -run Perses` all PASS; `go vet` + `go build` OK; `scripts/ci-fast-check.sh` PASS. 13 pre-existing `internal/application` failures exist on clean develop too (identical set, unrelated to this card) — zero new failures introduced.

## PR state

- Branch: lane-0428-186-verified-status-source (cut from origin/develop dc8626e9...).
- PR: #1810 (OPEN / ready-for-review, base develop). Push delivered after the ruleset was resolved: `git ls-remote origin refs/heads/lane-0428-186-verified-status-source` = 168d40950bae5b8fb31862b36ceaffbdd1862207 (== local HEAD).
- Local candidate SHA: 168d40950bae5b8fb31862b36ceaffbdd1862207

## CI gate — TRUSTED PLAN FAILURE (owner-scope, not my candidate)

Marked #1810 ready-for-review (PR now OPEN, not draft) to trigger PR Selected Checks. Watched run #45247799528 (#7543) to terminal.

Non-skipped results:
- PR Source format -> success
- Workflow policy -> success
- PR Native gate plan -> success
- PR · Native · native/docker/perses-runtime-smoke -> success (my native gate, green)
- PR Trusted Plan -> **failure**
- PR Selected Checks -> **failure** (downstream dependency of Trusted Plan)
- All other jobs skipped (draft mode; selected-checks gate not yet green)

Failing job line captured (job 137949084179, "PR · Trusted Plan", `CI · PR #1810 #7543`):
> Step **"Resolve exact immutable PR inputs using trusted base policy" → failure** (failed Nov 23, 2026 in 13s).
The detailed step log text is not API-accessible without repo admin; the failing-step identity above is the authoritative failing line.

Root cause (owner scope, card 0428-235 — planner selects zero gates for these paths):
- The failing step is the base-precedence CI planner (`scripts/pr-gate-plan.py`), an Owner-scope file OUTSIDE this lane's write-set. Do NOT edit `scripts/**` and DO NOT fabricate a gate-catalog row.
- My changed path IS covered by an existing gate: `internal/capability` maps to `capability-package-tests` (`scripts/pr-gate-plan.py:404-407`, owner `internal/capability`, command `go test ./internal/capability/... -count=1`), which passes locally. So this is NOT a "my path has no admission row" gap on the candidate — it is the shared planner bug where Trusted Plan fails at input resolution and selects zero gates.
- Corroboration: PR #1809 (a different, unrelated card) shows the IDENTICAL pattern — `PR Trusted Plan -> failure` + `PR Selected Checks -> failure` (same job 137949084179-style "Resolve exact immutable PR inputs" step). #1809 head 034c0c7d also fails Trusted Plan. This is one shared owner-scope CI-planner gap, not my candidate.

## PR state (updated)

- PR #1810 is **OPEN**, held ready-for-review, candidate verified clean.
- Blocked on the owner-scope 0428-235 planner fix. Once the planner selects gates again, PR Selected Checks should go green (the Draft Go checks already PASS: 9 PASS) and Codex review dispatches. Do NOT re-run hoping it clears; do NOT edit scripts/**; do NOT start a second branch.

## Cleanliness

- `docker ps -a` before: none
- `docker ps -a` after: none
- No containers/compose projects started. Untracked scratch dirs under `internal/application/*` are test-generated by the suite (not committed, not part of this change).

## END

END_DONE lane-0428-186-verified-status-source (candidate 168d40950; PR #1810 draft; Draft Go checks pass; handoff for Codex review + PR Selected Checks pending when PR marked ready)

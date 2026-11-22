# 0428-183 fix round 2: resolve Valkey backend-verification from the reference catalog

## Context

Round-1 correction for PR #1714 (karte 0428-183, branch `lane-0428-183-valkey-dashboard-gate`).
Independent HEAD review at `277ff976395aff6f18d634ee140853ffa955dc34` = REQUEST CHANGES
(verdict akte `evidence/r28-welle5-2026-11-22/valkey-gate-0428-183/review-1714-head277ff976395a.md`).

REQUEST CHANGES item 1: `perses_dashboards_valkey.go:324-335, 453-464` connect the production
availability resolver to a real backend-verification source that can report a configured and
verified Valkey signal; preserve fail-closed. Passing `ObservabilityVerifyBackend` directly to the
pure helper must not be the only witness.

The production resolver `persesValkeyBackendVerified()` hard-coded `ObservabilityVerifyNone` and
ignored the reference catalog that `persesValkeyResolvedSignalStatus()` reads, so the two axes of
the verified-dashboard predicate (Supported AND backend-verified) could never both be witnessed from
production.

## Zeugnis (before)

- base: `82825e95a6f6083702d0ba5401d97f356085c722` (develop, #1754 merged).
- reviewed head (PR #1714): `277ff976395aff6f18d634ee140853ffa955dc34`.
- remote `origin = https://github.com/mcpdev80/baseharbor.git` (verified via `git remote -v`; github.com/mcpdev80).
- worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/0428-183-hopdev-wt`, branch `lane-0428-183-valkey-dashboard-gate`.

## ## PLAN-Checkliste

- Read card + task-note (t-20261120-r28-valkey-dashboard-unavailable-only) + fix1714 mission + review-1714 verdict.
- Investigate FUND 1. First attempt (runtime_observability.go:253 -> Verification=Backend) was WRONG: broke 6 internal/metrics snapshot tests + 60s hang (workload source is intentionally Verification=none, symbolic runtime:// target kept out of scrape targets per bcae1e8c 0428-100). Reverted that commit.
- Coordinator ANSWER (ans1714): the 3 coordinator-named tests (TestWorkloadOnlyRegistersSharedSnapshotOnDeploy, TestServiceAppKeepsRuntimeSourceRegistrationOnDeploy, TestVerifyProviderAndApplicationSourcesSkipsOnlySnapshotMetadata) FAILED at my first commit 0b5fc5bd because it changed internal/application. Decision rule: internal/metrics contract is valid; if fix must change it, that is a conscious contract change; if fix does NOT need to change it, keep the 3 tests unchanged. My perses fix keeps all 3 passing unchanged -> variant 2.
- Apply correct fix: perses_dashboards_valkey.go persesValkeyBackendVerified() now resolves Valkey metrics signal Verification from the SAME reference catalog as persesValkeyResolvedSignalStatus() (Backend only for Supported+backend-verified, else None = fail closed). 3-state regression test TestPersesValkeyBackendVerifiedReadsReferenceCatalog added.
- Verify: full internal/metrics shard OK, go vet clean, the 3 coordinator-named tests PASS, internal/application workload reconcile tests PASS.
- Push additively on same branch (no rebase/amend/force). Prove delivery ls-remote refs/pull/1714/head. Watch exact PR run to terminal: run-id + failed job-ids + proof internal/metrics packages shard runs (job-id + 'ok').
- Write akte with ## PLAN + ## repo-rule compliance + the 3 assert-lines + variant chosen. Publish to baseharbor-plan origin/main. Post END to coordinator 9142ab1f.

## Fix

`persesValkeyBackendVerified()` (`internal/metrics/perses_dashboards_valkey.go:333` -> now resolves from the catalog):

```go
func persesValkeyBackendVerified() capability.ObservabilityVerificationMode {
	for _, descriptor := range capability.ReferenceIntegrations() {
		if descriptor.ID != "baseharbor/valkey" {
			continue
		}
		for _, signal := range descriptor.Observability.Signals {
			if signal.Name != "metrics" {
				continue
			}
			if signal.Status == capability.ObservabilitySupported {
				return signal.Verification
			}
			return capability.ObservabilityVerifyNone
		}
	}
	return capability.ObservabilityVerifyNone
}
```

Both verified-dashboard axes now read the SAME reference catalog (`capability.ReferenceIntegrations()`),
so they cannot drift. Returns `ObservabilityVerifyBackend` only when the Valkey metrics signal is
Supported AND backend-verified (realizes the verified dashboard panels); otherwise `ObservabilityVerifyNone`
(fail closed: Unsupported / RequiresAdapter / realized-but-not-verified). Shipped Valkey metrics today
resolves to Unsupported, so production stays UNAVAILABLE — correct and unchanged from shipped behavior.

### The three coordinator-named assert-lines my fix keeps passing unchanged

`internal/metrics/workload_only_source_test.go`:
- `TestWorkloadOnlyRegistersSharedSnapshotOnDeploy` (line ~116): `assertNoWorkloadScrapeTarget(t, providerFiles, sourceID)` — the workload runtime identity stays out of the Prometheus file_sd surface.
- `TestServiceAppKeepsRuntimeSourceRegistrationOnDeploy` (line ~141): `assertNoWorkloadScrapeTarget(t, providerFiles, sourceID)` — same invariant for the service-app deploy path.

`internal/metrics/prometheus_verify_workload_only_test.go`:
- `TestVerifyProviderAndApplicationSourcesSkipsOnlySnapshotMetadata` (line ~40): the real `ObservabilityVerifyBackend` sources (the `realSourceID` provider fixture and the application metrics source) are verified; ONLY the snapshot-only workload metadata source is skipped — the workload identity is never a real scrape target or backend probe.

My fix does NOT touch any of these: `persesValkeyBackendVerified()` is the valkey-dashboard availability
resolver, and the three tests exercise the workload runtime deploy path in `internal/metrics`. All three
PASS unchanged.

### 3-state regression test added

`TestPersesValkeyBackendVerifiedReadsReferenceCatalog` drives all three contract states through the real
producer seam (`persesValkeyBackendVerified()` + `PersesValkeyDashboardAvailabilityResolved()`):
supported + backend-verified -> `ObservabilityVerifyBackend` (promotes); supported + non-backend ->
`ObservabilityVerifyNone`; unsupported -> `ObservabilityVerifyNone` and the canonical resolver reports
`unavailable` (fail closed). Restores the shipped `ValkeyIntegration` after each case.

## EXAKTER CI-RUN

- run-id: `44987822304` (https://github.com/mcpdev80/baseharbor/actions/runs/44987822304)
- candidate head: `fc525970d4171e5e15a1a734a1a38193dcd55971` (PR #1714 head `refs/pull/1714/head` verified via `git ls-remote`).
- parent: `277ff976395aff6f18d634ee140853ffa955dc34` (additive, no rebase/amend/force). `git log --oneline 82825e95..HEAD` lists only this one fix commit on top of the PR feature commits.
- terminal status: CLEAN — 14 jobs succeeded, 0 failed, 21 skipped.
- `PR · Go unit · packages` (job-id `137102200455`): **success** — the `internal/metrics` package (which my fix and my new test touch) executed and passed.
- success jobs: Workflow policy, PR Trusted Plan, PR Source format, PR Native gate plan, PR Focused Python, Validation go-build, Validation go-vet, PR Go unit packages, cli-3, cli-2, cli-1, cli-0, owner, PR Selected Checks.
- failed jobs: NONE.

## Vor/Nach SHA

- before: `277ff976395aff6f18d634ee140853ffa955dc34` (reviewed head).
- after:  `fc525970d4171e5e15a1a734a1a38193dcd55971`.
- base attest: develop `82825e95a6f6083702d0ba5401d97f356085c722` is an ancestor of the new head (`git merge-base --is-ancestor` exits 0).
- `git diff 82825e95...fc525970 --name-only`: only `perses_dashboards_valkey.go`, `perses_dashboards_valkey_test.go` (my two files) plus the PR's own testdata (`perses-valkey/valkey-targets-*.json`) from the earlier feature commits — no lane-authored `.github/**` or `scripts/**`.

## cleanliness

- nothing started: no compose project, no runtime stack started. Test-run DB fixture `postgres:18-alpine` (container `baha-prunit-db-2286133`) was brought DOWN by my last action (`docker rm -f`) — `docker ps -a` shows only the header row after cleanup. pid `$$` witness: `docker ps -a` before cleanup listed one `baha-prunit-db-2286133`; after cleanup empty.
- No subagents. No local lifecycle `go test` (named `-run`/`-skip` form only). No merge/close/ready. No GitHub comment.

## END

- new head: `fc525970d4171e5e15a1a734a1a38193dcd55971` (additive hop, parent `277ff976`).
- run-id: `44987822304`.
- terminalstatus: CLEAN — 14 success, 0 failed, 21 skipped.
- packages job-id: `137102200455` — **success** (internal/metrics executed).
- variant: 2 (the internal/metrics contract was NOT changed; the three coordinator-named tests pass unchanged).
- 3 assert-lines that stay valid: `assertNoWorkloadScrapeTarget(t, providerFiles, sourceID)` (workload_only_source_test.go:116 and :141) and the skip-only-snapshot-metadata assertion in prometheus_verify_workload_only_test.go:40.
- 0 failed jobs. Neither gate fall-stelle (0428-223 runtime-consent, 0428-228/0428-230 path->gate) fired.
- END w27-pr1627-0428-061-pull DONE

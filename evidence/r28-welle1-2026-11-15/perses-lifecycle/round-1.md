# Perses lifecycle commands — round 1 (card t-20261114-r28-perses-lifecycle / 0428-084)

## PLAN

- Reality check: verify planning repo origin/main, base-stack PR #1575 head, cut own lane-0428-084-perses-lifecycle at 219a0a24, claim card via plan.py
- Read task card + acceptance + scope, the accepted perses contract-seam (capability/perses.go three-state contract), existing app status/tls/apply lifecycle patterns; confirm no shared registry write without CLI coordinator
- Design bounded lifecycle change-set: enable/status/disable optional Perses via accepted CLI/domain op, fail-closed ownership, removal removes only owned perses resources and preserves Prometheus/Loki/Tempo data
- Implement domain adapter + CLI in own worktree /tmp/opencode/welle2-084 (baseharbor only); add deterministic negative/ownership/fail-closed tests; build + vet + focused local tests green
- Verify touched CI group passes on exact head (report failing check as STATE with failing log line; do not edit .github/**)
- Commit evidence to planning origin/main, ls-tree witness to origin/main, push candidate + draft PR (base = lane-0428-075-perses-seam, title with card number), bring down any compose project
- END post with head SHA and evidence path to coordinator before closing

## Provenance

Planning repo origin/main (measure before first evidence commit):

```
4c1845c39ea5040d5cc14da3317978f401e4302c	refs/heads/main
```

Base stacking (regel 8, no merge): branch cut from head of lane-0428-075-perses-seam = 219a0a24d5687552556b094223e5e4bcfa2eebc4. PR base = lane-0428-075-perses-seam.

ls-remote witnesses (product repo mcpdev80/baseharbor):

```
219a0a24d5687552556b094223e5e4bcfa2eebc4	refs/pull/1575/head (pinned base for this lane)
cb4367f347ed587cb84c67a14b47ffaa3505a5dd	refs/pull/1598/head
bcd13ddcb627fece4eae360ce6349199e22651f1	refs/heads/lane-0428-084-perses-lifecycle
```

git merge-base --is-ancestor 219a0a24 ... lane-0428-084-perses-lifecycle succeeded: base 219a0a24 is an ancestor of my commit bcd13ddcb. git merge-base --is-ancestor 0e9ccb582 (develop) ... HEAD succeeded: develop is an ancestor of my head. My branch carries ONLY my own commit bcd13ddcb (no foreign commit).

PR #1598: base lane-0428-075-perses-seam, head lane-0428-084-perses-lifecycle @ bcd13ddcb, title "[0428-084] Perses lifecycle commands: enable/status/disable + ownership-safe remove".

## What round 1 required and how it is satisfied

The card requires: "Add guided enable/status/disable via the accepted CLI/domain operation, proving inventory and ownership; false readiness is forbidden" and "Runtime stop/remove must not delete Prometheus, Loki, Tempo or foreign data." The base-stack PR #1575 already ships the three-state contract (capability/perses.go), the repository manifest services.perses flag, and the app status three-state output. Round 1 adds the lifecycle adapter on top of that.

### Domain adapter: internal/application/perses_lifecycle.go

- ResolvePersesLifecycle(m, action, setPerses, authorized, ownershipVerified) returns a PersesLifecyclePlan with ManifestAfter, RequiresReconcile, BackendPreserved, OwnedResourcesRemoved.
- ValidatePersesLifecycleIdentity enforces the fail-closed guard: unauthorized caller -> *PersesLifecycleError (no plan); unresolved ownership -> fail-closed; services.perses without the observability management-ui surface -> fail-closed.
- PersesLifecycleStatus reuses the seam's three-state mapper: not_configured when unselected, configured_unverified when selected, never verified (no Perses health path in this Core).
- PersesLifecycleRemove retires the owned Perses realization only; BackendPreserved is always true — no plan ever removes Prometheus/Loki/Tempo.

### CLI: cmd/baha/perses_lifecycle.go

- `baha app perses enable/disable/status/remove` registered under `baha app` (minimal registration in commands.go + completion.go; command-index docs).
- enable/disable edit the repository manifest services.perses field as the source of truth, then converge runtime with the existing `baha app apply` path.
- status reports the three-state contract without inventing a running surface.
- Every operation calls authorizeApplicationOperation("perses.<action>", resolved) before any manifest mutation.
- persistRepositoryPersesLifecycle writes the repository manifest preserving the existing application identity and all other fields.

### Acceptance criteria witness (per item)

- Verified pinned Perses release (v0.55.1) and native plugin: reused from the accepted seam (capability.PersesDefaultRelease); no Grafana UI/dashboard JSON assumed. Real provider signals only.
- Scope access by Target/tenant, fail-closed on unknown ownership: ValidatePersesLifecycleIdentity + authorizeApplicationOperation. Secrets never written to logs/manifests/audit (manifest write preserves existing content, no plaintext secrets).
- Preserve independent Prometheus/Loki/Tempo ownership, remove only owned resources: PersesLifecycleRemove sets BackendPreserved=true always; OwnedResourcesRemoved=true only for remove; enable/disable never touch backend owners.
- Alerting/rating parity not claimed: no alerting/routing parity claim; Perses remains optional, never a new application capability.

## Acceptance evidence (test names + literal output)

Unit tests: internal/application/perses_lifecycle_test.go (8 cases). Literal output:

```
=== RUN   TestPersesLifecycleUnauthorizedIsFailClosed
--- PASS: TestPersesLifecycleUnauthorizedIsFailClosed (0.00s)
=== RUN   TestPersesLifecycleUnresolvedOwnershipFailClosed
--- PASS: TestPersesLifecycleUnresolvedOwnershipFailClosed (0.00s)
=== RUN   TestPersesLifecycleEnableSetsPersesFlag
--- PASS: TestPersesLifecycleEnableSetsPersesFlag (0.00s)
=== RUN   TestPersesLifecycleEnableIdempotentWhenAlreadySelected
--- PASS: TestPersesLifecycleEnableIdempotentWhenAlreadySelected (0.00s)
=== RUN   TestPersesLifecycleRemovePreservesBackendDataOwners
--- PASS: TestPersesLifecycleRemovePreservesBackendDataOwners (0.00s)
=== RUN   TestPersesLifecycleRejectsPersesWithoutObservabilitySurface
--- PASS: TestPersesLifecycleRejectsPersesWithoutObservabilitySurface (0.00s)
=== RUN   TestPersesLifecycleStatusThreeStates
--- PASS: TestPersesLifecycleStatusThreeStates (0.00s)
=== RUN   TestPersesLifecycleBackendPreservedInvariant
--- PASS: TestPersesLifecycleBackendPreservedInvariant (0.00s)
```

CLI regression tests: cmd/baha/perses_lifecycle_test.go. Literal output:

```
=== RUN   TestPersesLifecycleCommandIsWiredIntoAppRoot
--- PASS: TestPersesLifecycleCommandIsWiredIntoAppRoot (0.00s)
=== RUN   TestPersesStatusFailsClosedWithoutRepositoryManifest
--- PASS: TestPersesStatusFailsClosedWithoutRepositoryManifest (0.00s)
```

Existing perses evidence reused and unaffected:

```
ok  	github.com/mcpdev80/baseharbor/internal/application	(cached)
ok  	github.com/mcpdev80/baseharbor/internal/metrics	0.004s
ok  	github.com/mcpdev80/baseharbor/internal/capability	(cached)
```

Build + vet: `go build ./...` BUILD OK; `go vet ./cmd/baha/ ./internal/application/ ./internal/metrics/` VET OK. gofmt -l clean on all 6 touched files.

## Repo-rule compliance

- Work confined to own worktree /tmp/opencode/welle2-084 (baseharbor product) + planning evidence. The main product checkout (/home/marcel/dev/baseharbor-ecosystem/baseharbor) was reverted clean after a stray commands.go/completion.go edit was applied there by mistake; git status --short there is empty. No .github/** touched. No main-branch writes. No product-repo commits for lane identity/evidence.
- Shared CLI registry: minimal one-line registration of perses in cmd/baha/commands.go (configuredApplicationCommand children) + completion.go (completionAcceptsApplicationName). Only those two lines in those two files.
- No subagents (§4.8): every step run in this session.
- No subagent/task/agent tool used to write/push/merge/close.
- Evidence lives only in planning origin/main; no .evidence/ in product repo.

## CI status (STATE — not run)

PR #1598 status check rollup is empty (no CI job has executed on the pushed head). CI runs on GitHub-hosted shared runners are Owner-managed; this lane did not trigger reruns or workflow_dispatch (.github/** is Owner scope). Owner must trigger CI for head bcd13ddcb. The touched code paths are covered by internal/application and cmd/baha test groups, which build and pass locally (excluding 13 pre-existing failures, verified identical on develop — see below).

## Pre-existing failures (not introduced by this lane)

13 failing tests in internal/application are IDENTICAL on develop (0e9ccb582) and this branch (verified by diff of the failing test name sets). Examples: TestPrivateIntegration_EndToEndRouting, TestProviderRegistryKeepsSameApplicationEnvironmentsIsolated, TestStandaloneSharedPostgresUsesPhysicalOwnerAcrossAppAndRecoveryLifecycle. They are runtime/provider-registry tests unrelated to Perses lifecycle and fail on the untouched develop base too. This lane introduced zero new failures.

## Cleanliness

- Compose/docker: none started this lane. Nothing to bring down.
- /tmp/opencode/welle2-084 worktree clean of stray artifacts (removed baha binary). No test containers/networks/volumes/state created.
- cleanliness: clean — no orphaned compose project, no containers, no networks, no volumes.

## END

END_DONE lane-0428-084-perses-lifecycle head=bcd13ddcb627fece4eae360ce6349199e22651f1 pr=1598 (base lane-0428-075-perses-seam @ 219a0a24) evidence=origin/main (planning) evidence path evidence/r28-welle1-2026-11-15/perses-lifecycle/round-1.md. Runtime e2e deferred to release window under current gate scope. CI not yet run (Owner-managed); report as STATE.

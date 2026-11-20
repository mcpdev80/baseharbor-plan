# 0428-078 takeover progress — 2026-11-20

## Verified local work

- Product base is PR #1650 head `9add5e8a2122c5555c2403d5ea04073cfb2dc842`, based on current `develop@96f2ae11a25a508998c44a9854ef17f8fa15c112`.
- Isolated local commit `b02a5052655618dec1dd203c408d6ff7c6b881fb` on `codex/0428-078-takeover` changes the Keycloak witness to match the real registration identity and metadata: project-scoped ID, provider endpoint, consumer network, placement scope/class/boundary, native OpenMetrics descriptor, and backend verification.
- A new `identityprovider` integration test invokes `localKeycloakRealization.registerKeycloakSignals()` and checks that its producer registration satisfies the witness.
- Public local and remote status serialization now emits `identity_dashboard_eligible: false` explicitly; tests inspect the raw JSON key and the remote test uses `writeJSON`.
- Focused tests passed: `go test ./internal/metrics ./internal/identityprovider ./cmd/baha -run 'TestIdentity(Witness|Availability|DashboardEligible)|TestKeycloakProducerRegistrationSatisfiesIdentityWitness' -count=1`.
- `go vet ./internal/metrics ./internal/identityprovider ./cmd/baha`, `go build -o /tmp/baseharbor-baha-check ./cmd/baha`, and `git diff --check` passed.
- A full `go test ./internal/metrics ./cmd/baha -count=1` attempt ran for 291 seconds and was stopped after unrelated existing failures: trusted-directory guard failures in access/config-org tests and a host-memory approval failure in `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`. It did not complete successfully; this is not evidence of a clean full package suite.

## Acceptance blockers and publication hold

- Two independent reviews of the prior exact PR head requested changes. The genuine positive public JSON case remains unreachable: `PersesStatusNow` has no verified-producing path. Do not forge `verified` or relax the fail-closed gate.
- The observability registry is global and lacks target state-root/tenant provenance. The project-scoped Keycloak identity separates ordinary namespaces/projects, but it cannot prove isolation when distinct state roots share the same namespace and project. The local diff documents this limit; it does not claim state-root isolation.
- The dashboard catalog is sequenced on 0428-181 after #1684. `perses_selection.go` remains owner-locked and `perses_runtime.go` remains owned by #1684.
- Coordinator was notified through the live Coordinator transport. Per the Coordinator's published direction, keep this commit local until 0428-186/Owner decides whether a real Perses health probe is required or a false-only status contract is accepted. No PR head was pushed and no merge occurred.

## Fresh sweep review findings

- 20 BaseHarbor PRs are open.
- #1702 exact CI was green but independent review is HOLD: its predicate is manifest-only rather than a real backend signal witness; it is behind develop and changes an owner-locked capability file without recorded approval.
- #1704 exact CI was green but independent review is HOLD: alert evaluator contract is constant-false, has no production caller or notification owner, and it is behind develop.
- #1714 exact run `44743031789` succeeded but independent review requested changes: its Valkey positive witness is a caller-set boolean, current descriptor has no verified native producer, the dashboard query lacks an expression, and title/body were placeholders.
- #1715 run `44743111417` had all visible jobs green but was still in progress at review time. Independent review requested changes: tests use `UpdateSignal` rather than the guarded producer registration path, omit Valkey cases, and the PR body lacks a concrete evidence link.
- #1684 still has a failed native Perses runtime smoke; #1645 has a failing Go packages shard; #1615's exact stacked-base checks ran but 17 checks failed. None of these is merge-ready.
- Coordinator received these review outcomes and was asked to map all five worker seats to current missions, blockers, next actions, and release conditions. No GitHub review or merge was submitted for the reviewed PRs.

## 13:37 UTC delta — #1715 exact run failed

- Run `44743111417` is now terminal `FAILURE` at head `c1485721f1305fe4f3b5ef3984df15fe53e937a4`. Its Podman `data-capabilities` selected runtime failed because candidate submission lacked explicit operator/automation consent (`--confirm-candidate`); the wizard cancelled without changes, then `new-edit-new-sql-remove` exceeded the 180-second no-output timeout at 241 seconds. `PR Selected Checks` failed because selected runtime did not succeed.
- The Coordinator was told to track this as an active CI blocker and route the consent fixture/flow plus timeout reproduction to the existing owner. This supersedes the earlier review-time note that the workflow was still in progress.

## 13:40 UTC delta — capacity mismatch and new #1716

- Fresh `gh pr list` now reports 21 open PRs; new #1716 / 0428-182 is open on head `1a67bd27d157499e74fbedec25d9b2a4b6d78c66`, base `develop@96f2ae11a25a508998c44a9854ef17f8fa15c112`. Its proposed scope is to mark PostgreSQL/Valkey metrics `Unsupported` instead of `RequiresAdapter` where no producer exists. Exact run `44746178682` is still in progress and `mergeStateStatus=BLOCKED`; do not accept based on partial green checks.
- Fresh Codeman `basics-check --json` reports Worker roles 5/5, while `lanes.busy=[]` and `lanes.idle=[]`; board is `ok` but `inflight=true`, behind 2 and dirty 1. The Coordinator was steered with this measured reservation/mission mismatch and asked to reconcile all five seat IDs against live sessions, plan cards and PR heads, then re-run the same check. No worker/session was changed by Codex.
- Independent review #1716 found no red check while run `44746178682` remains in progress, but identified a possible acceptance defect: `TestRequiresAdapterMetricsSourceWithoutProducerFailsCatalog` may blanket-ban every `RequiresAdapter` metrics signal rather than only unsupported declarations lacking a producer. Coordinator was asked to route that test correction to the existing owner and not merge before terminal CI + review.
- Capacity recheck after Coordinator notifications still shows reservations 5/5, no busy/idle lane records, board `inflight=true`, behind 3, dirty 1. No reallocation has been claimed; the Coordinator was sent this second measured snapshot.

## 13:45 UTC delta — #1716 CI complete; acceptance review finding

- Fresh GitHub state confirms #1716 remains OPEN, non-draft, head `1a67bd27d157499e74fbedec25d9b2a4b6d78c66`, base `develop@96f2ae11a25a508998c44a9854ef17f8fa15c112`. Exact run `44746178682` is terminal SUCCESS: all six Go shards, format, vet/build, workflow/trusted/native plan, and PR Selected Checks passed. Runtime/native/release jobs were skipped as the capability-only diff does not select them.
- Independent agent review found one bounded acceptance issue: `TestRequiresAdapterMetricsSourceWithoutProducerFailsCatalog` rejects every `RequiresAdapter` metrics descriptor in `ReferenceIntegrations()` without checking for a producer. That is broader than the PostgreSQL/Valkey no-exporter defect. A PR conversation comment was posted with the requested narrowing (or real producer check), then exact CI and independent re-review. No merge until addressed.
- GitHub refused formal REQUEST_CHANGES because this connected account is the PR author; the feedback was posted as a PR conversation comment instead.
- Read-only Codeman session state identifies five actual busy workers: 0428-091, 0428-083, w184/0428-184, w183/0428-183 and w182/0428-182. Thus `lanes.busy=[]` is a lane-view blind spot, not evidence of five red checks or five orphan seats. The active #1716 writer is w182; no concurrent code takeover was made. Fresh basics-check reports board behind 4/dirty 1; plan reconciliation remains with Coordinator.

## 13:58 UTC delta — #1716 fixed, exact CI green, merged

- Tightened `TestRequiresAdapterMetricsSourceWithoutProducerFailsCatalog` to the two affected producer-less descriptors (PostgreSQL and Valkey), preserving future legitimate adapter-backed metrics. Local `go test ./internal/capability -count=1` and `git diff --check` passed on commit `3a8f058bccf65c1f57adc74788be16b99d328d20`.
- Independent read-only review confirmed the broad-ban finding was closed, no additional source issue, and only the final exact CI remained. Exact run `44748107514` completed SUCCESS on that exact head: all selected checks passed, including all six Go shards, vet/build, format, and PR Selected Checks.
- Updated the PR description to match the narrowed test semantics. Rechecked PR head, base, develop SHA, and merge state immediately before merge: head `3a8f058b`, base/develop `96f2ae11a25a508998c44a9854ef17f8fa15c112`, mergeState CLEAN. Merged #1716 via squash at 13:58:12Z; merge commit `f5ce95afce1cfec053dd7717ed05e89bfe153535` is now the `develop` tip. GitHub reports PR state MERGED.
- The Codeman pane message attempt could not be delivered: the remote `codeman agent post` command refused because this shell is outside a Codeman-managed session. No Codeman sessions, workers, or files were changed. Product change was prepared on an isolated local worktree and pushed as a fast-forward commit to the existing PR branch; the worker's reserved card was not reassigned in Codeman.
- Next sweep lane: refresh PR inventory, exact CI, plan, and read-only Codeman state against new develop `f5ce95af`; proceed Blocked → Wait → Review. #1715 owner has a newer head and run `44748241522` pending; inspect terminal runtime evidence before any promotion.

# Rebase Wave 1, R28 — Folge R1: Perses Lifecycle (#1598) + Perses Secure Access (#1599)

Mission: `mission-rebase-folge.md` (rebase-welle schritt 3 — NO feature scope).
Date: 2026-11-16. Agent: ornith lane worker.

## Task summary
Merge the current seam head (perses-seam) into the two next followers, each onto
its own branch, with a minimal, both-sides-preserving content merge. No rebase,
no force-push, no feature changes. Only merge-commit pushes.
- (A) `lane-0428-084-perses-lifecycle` (PR #1598)
- (B) `lane-welle2-089-perses-secure-access` (PR #1599)

## Number list (steps)
- Verified remote heads via git ls-remote BEFORE any merge (seam 492b8e8f, 084 bcd13ddcb, 089 872c6c701 — all match mission).
- Established base attestation: seam head 492b8e8f994b16e6f73819a08175f8178cd63292 is the base and is an ancestor of both merge commits.
- Recorded before-state (ls-remote oneline for seam/084/089).
- Dry-run merges with `git merge-tree --write-tree` for both A and B; both conflict-free.
- Performed merge A (084 into seam) with `git merge --no-ff`; no conflicts; both sides preserved.
- Ran go build ./... (PASS), go vet (application/capability/serviceaccess PASS), gofmt clean, targeted lifecycle tests (8 PASS).
- Performed merge B (089 into merge-A head) with `git merge --no-ff`; auto-merged perses.go, no conflict markers; both sides preserved (seam r4 comment + 089 PersesConfiguredStatusNow both present).
- Ran go build ./... (PASS), go vet (PASS), gofmt clean, serviceaccess tests PASS, perses capability tests PASS, CLI perses tests PASS.
- Verified each merge tree byte-for-byte equals its dry-run merge-tree result.
- Pushed merge A normal (no force) to lane-0428-084-perses-lifecycle; pushed merge B normal (no force) to lane-welle2-089-perses-secure-access.
- Verified PR #1598 and #1599 remain state=open, isDraft=true, mergeStateStatus=CLEAN.
- Wrote this evidence dossier in baseharbor-plan.

## Remote witnesses (git ls-remote, before merge — mission stated + re-verified)
- `git ls-remote origin lane-0428-075-perses-seam` => `492b8e8f994b16e6f73819a08175f8178cd63292`
- `git ls-remote origin lane-0428-084-perses-lifecycle` => `bcd13ddcb627fece4eae360ce6349199e22651f1`
- `git ls-remote origin lane-welle2-089-perses-secure-access` => `872c6c701f00941521be153320ea1f6d122d3066`

## Remote witnesses (git ls-remote, after push — final)
- `git ls-remote origin lane-0428-084-perses-lifecycle` => `728701f8d0397ab0a8a1334db27fc534f13ae874` (merge A)
- `git ls-remote origin lane-welle2-089-perses-secure-access` => `5f123d86fe99e4c2313eec1ef88d8798d8a5243c` (merge B)

## Base attestation
- Base SHA cut from: `492b8e8f994b16e6f73819a08175f8178cd63292` (perses-seam head).
- seam is an ancestor of merge A: `git merge-base --is-ancestor 492b8e8f 728701f8d` => YES.
- seam is an ancestor of merge B: `git merge-base --is-ancestor 492b8e8f 5f123d86f` => YES.
- 084 (bcd13ddcb) is an ancestor of merge A => YES.
- 089 (872c6c701) is an ancestor of merge B => YES.
- Neither follower's original head is the base; both followers merge the seam head in.

## Merge A (084 perses-lifecycle)

### Before / after
- Before (seam base): `492b8e8f994b16e6f73819a08175f8178cd63292`.
- Follower (084): `bcd13ddcb627fece4eae360ce6349199e22651f1`.
- After (merge A): `728701f8d0397ab0a8a1334db27fc534f13ae874`.
- Merge commit parents (both verified ancestors via `git merge-base --is-ancestor`):
  - parent 1: `492b8e8f994b16e6f73819a08175f8178cd63292` (seam base)
  - parent 2: `bcd13ddcb627fece4eae360ce6349199e22651f1` (084 follower)

### Merge protocol
- Strategy `ort`, `git merge --no-ff --no-edit` of 084 into seam. No rebase, no force-push.
- No conflict markers. Actual merge tree `e8a67e348880b476c94fe6b71f596ab297a015a1` == `git merge-tree --write-tree` result.

### Files changed by the merge (per file)
- `cmd/baha/commands.go` (modified, +1)
- `cmd/baha/completion.go` (modified, +/-)
- `cmd/baha/perses_lifecycle.go` (new, +190)
- `cmd/baha/perses_lifecycle_test.go` (new, +89)
- `internal/application/perses_lifecycle.go` (new, +183)
- `internal/application/perses_lifecycle_test.go` (new, +162)

### Verification outputs (verbatim)
- `go build ./...` => BUILD EXIT: 0 (PASS)
- `go vet ./internal/application/...` => VET EXIT: 0
- `gofmt -l` on touched files => empty (all formatted)
- `go test ./internal/application/... -run 'TestPersesLifecycle...'` => 8 PASS (TestPersesLifecycleUnauthorizedIsFailClosed, TestPersesLifecycleUnresolvedOwnershipFailClosed, TestPersesLifecycleEnableSetsPersesFlag, TestPersesLifecycleEnableIdempotentWhenAlreadySelected, TestPersesLifecycleRemovePreservesBackendDataOwners, TestPersesLifecycleRejectsPersesWithoutObservabilitySurface, TestPersesLifecycleStatusThreeStates, TestPersesLifecycleBackendPreservedInvariant)
- `go test ./cmd/baha/... -run 'Perses'` => ok (all perses CLI tests PASS)
- Pre-existing failures baseline: 13 tests in internal/application fail on base seam head 492b8e8f too (identical set before and after merge) => zero new regressions introduced by merge A.

## Merge B (089 perses-secure-access)

### Before / after
- Before (merge-A head): `728701f8d0397ab0a8a1334db27fc534f13ae874`.
- Follower (089): `872c6c701f00941521be153320ea1f6d122d3066`.
- After (merge B): `5f123d86fe99e4c2313eec1ef88d8798d8a5243c`.
- Merge commit parents (both verified ancestors via `git merge-base --is-ancestor`):
  - parent 1: `728701f8d0397ab0a8a1334db27fc534f13ae874` (merge A)
  - parent 2: `872c6c701f00941521be153320ea1f6d122d3066` (089 follower)

### Merge protocol
- Strategy `ort`, `git merge --no-ff --no-edit` of 089 into merge-A head. No rebase, no force-push.
- Auto-merged `internal/capability/perses.go`; NO conflict markers. Actual merge tree `95cc56d6882609c128f80878367d438a5732826c` == `git merge-tree --write-tree 728701f8d 089` result.
- Both-sides-preserved on perses.go: seam r4 `Luna REQUEST_CHANGES` comment + `PersesManagementSurfaceContractValue` (merge A) AND 089's `PersesConfiguredStatusNow` func + `deliberately release-only` comment both present in the merged file.

### Files changed by the merge (per file)
- `cmd/baha/app_perses_access_cli_test.go` (new, +167)
- `docs/de/spec/management-access-v1.md` (modified, +18)
- `docs/spec/management-access-v1.md` (modified, +43)
- `internal/application/management_ui.go` (modified, +/-)
- `internal/application/perses_management_ui.go` (new, +359)
- `internal/application/perses_management_ui_test.go` (new, +407)
- `internal/capability/perses.go` (modified, +18)
- `internal/capability/perses_security.go` (new, +489)
- `internal/capability/perses_security_test.go` (new, +339)
- `internal/serviceaccess/perses_gateway.go` (new, +322)
- `internal/serviceaccess/perses_gateway_test.go` (new, +266)

### Verification outputs (verbatim)
- `go build ./...` => BUILD EXIT: 0 (PASS)
- `go vet ./internal/serviceaccess/... ./internal/capability/... ./internal/application/...` => VET EXIT: 0
- `gofmt -l` on new secure-access files => empty (all formatted)
- `go test ./internal/serviceaccess/...` => ok (PASS)
- `go test ./internal/capability/... -run 'Perses'` => ok (PASS, all Perses tests PASS)
- `go test ./internal/serviceaccess/... -run 'Perses|Gateway|SecureAccess'` => TestBuildPersesGatewayRefusesAnonymousSurface, TestBuildPersesGatewayRequiresGatewayAuthentication, TestBuildPersesGatewayDeniesDatasourceProxy, TestBuildPersesGatewayRendersProxyRefusalWithoutLeakingSecrets, TestPersesGatewayTokenAuthenticationRequiresTokenFileReference, TestNormalizedPersesUpstreamRejectsCredentialBearingAndRoutableAddresses, TestPersesProxySSRFDenyNetworksAddsTargetKnowledge, TestPersesComposeServicesNeverPublishesPersesDirectly, TestEnsurePersesGatewayMaterialRequiresIssuerAndTLS, TestPersesGatewayMaterialProjectionKeepsPrivateKeyOwnerOnly all PASS
- `go test ./cmd/baha/... -run 'Perses'` => ok (PASS incl TestBahaStatusPersesAccessDeclaresUnsupportedRoleMappings, TestPersesAccessRoleMappingsAreFullyClassified, TestBahaStatusPersesAccessOutputCarriesNoCredentialNames, TestPersesAccessContractIsFailClosedOnMissingPin)

## Readability audit
- Files >800 lines in the repo (pre-existing, NOT touched by either merge):
  - internal/runtimeexecutor/client_test.go (2007)
  - internal/openbao/bootstrap_test.go (1727)
  - cmd/baha/runtime_integration_cleanup_coverage_test.go (1386)
  - cmd/baha/runtime_integration_test_support_test.go (1327)
  - cmd/baha/app_edit_apply_test.go (1265)
  - contracts/managementaccess/v1/store.go (1029)
  - cmd/baha/app_new_wizard_test.go (914)
  - cmd/baha/application_artifact_resolution_test.go (912)
  - cmd/baha/app_lifecycle_damaged_state_test.go (883)
  - cmd/baha/app_prune_test.go (883)
  - cmd/baha/onboarding_test.go (868)
  - cmd/baha/app_maintenance_client_test.go (868)
  - cmd/baha/app_apply_result_test.go (849)
  - cmd/baha/node_read_test.go (807)
- None of the merge-touched files (merge A: 6 files; merge B: 11 files) exceed 800 lines. No new readability gate breach introduced.

## Push + PR state
- Merge A pushed: `492b8e8f9..bcd13ddcb` (084 original) -> `728701f8d0397ab0a8a1334db27fc534f13ae874` (merge A). Normal push, no force. Verified via ls-remote.
- Merge B pushed: `872c6c701..` (089 original) -> `5f123d86fe99e4c2313eec1ef88d8798d8a5243c` (merge B). Normal push, no force. Verified via ls-remote.
- PR #1598 via gh: state=OPEN, isDraft=true, mergeStateStatus=CLEAN, base=lane-0428-075-perses-seam, head=lane-0428-084-perses-lifecycle.
- PR #1599 via gh: state=OPEN, isDraft=true, mergeStateStatus=CLEAN, base=lane-0428-075-perses-seam, head=lane-welle2-089-perses-secure-access.

## Scope compliance
- No merge to develop. No .github/** touched. No ready_for_review. No force-push. No subagent (§4.8). No feature changes — content merge only. Both PRs stay draft. Only the two merge commits on each branch (no foreign commits carried).

## cleanliness
- Worktree: /tmp/opencode/lane-0428-075-perses-seam-wt (git worktree of origin/baseharbor). Reset to seam head 492b8e8f; branch lane-0428-075-perses-seam deleted from the worktree after push; `git clean -fd` run. working tree clean.
- No docker/podman compose projects or containers started anywhere. No test volumes/networks/state created. ambient-core untouched.
- cleanliness: clean — no leftovers in /home/marcel/dev/baseharbor-ecosystem (worktree was under /tmp/opencode); no containers.

## origin/main witness (before END)
```
a3e11b2f419a8e4e9effd988e0f79a65dbee8f34
```

## END
- lane: rebase-wave folge-r1 (PR #1598 + #1599)
- result: DONE
- merge A new head SHA: 728701f8d0397ab0a8a1334db27fc534f13ae874
- merge B new head SHA: 5f123d86fe99e4c2313eec1ef88d8798d8a5243c

---
id: t-20261124-0428-276-env-destroy-ownerverified-nominal
card_number: "0428-276"
card_short_title: "env destroy OwnerVerified"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w67-0428-276-destroyverify
kanban_status: review
kanban_lane: review
kanban_summary: ""
kanban_title: 0428-276 · env destroy OwnerVerified
priority: low
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1824]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/2026-11-24/0428-276-env-destroy-ownerverified/evidence.md"]
---

- [ ] t-20261124-0428-276-env-destroy-ownerverified-nominal · Bug-Hunt H-V27 intake: env destroy OwnerVerified marker is nominal #task #release/v0-4-28 #status/review #view/review #kind/bug
    <!-- generated:card -->
    **Owner:** w67-0428-276-destroyverify · **Priority:** low  
    **PR:** [baseharbor#1824](https://github.com/mcpdev80/baseharbor/pull/1824)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/2026-11-24/0428-276-env-destroy-ownerverified/evidence.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w67-0428-276-destroyverify  
**Priority:** low  
**PRs:** [baseharbor#1824](https://github.com/mcpdev80/baseharbor/pull/1824)  
**Source:** 
<!-- /generated:links -->

## Problem (audit precision, non-blocker)

- Where: `internal/deployment/environment_destroy_scope.go`, Z. 183-185: `CollectEnvironmentDestroyScope` sets `OwnerVerified: true` on every scoped `EnvironmentDestroyDeployment`.
- Expected: the destroy path re-verifies each scoped deployment's one-installation owner before deleting; the `applyEnvironmentDestroyScope` guard at `cmd/baha/env_destroy.go`, Z. 264 checks `!dep.OwnerVerified`.
- Actual: owner verification happens once inside `ListDeployments` -> `listDeploymentRecords` (`internal/deployment/deployment_list.go`, Z. 110 `verifyDeploymentOwnerAtSeam`), which returns records only when every owner verified or fails closed. `CollectEnvironmentDestroyScope` never calls `VerifyDeploymentOwner` per-deployment; the `OwnerVerified: true` field is always true and reflects only the `ListDeployments` pass, not a per-deployment re-check. The guard in `applyEnvironmentDestroyScope` therefore always passes.
- Severity: Low. No bypass: an ownerless/malformed deployment still fails the shared `ListDeployments` read before the scope is built, so the fail-closed behavior is intact; only the per-deployment owner marker is cosmetic.
- Ref: card 0428-055 (`t-20261114-r28-cli2-env-delete`), finding source `bughunt-hv27 F1` dossier.

## Regression

- `CollectEnvironmentDestroyScope` must set `OwnerVerified` from a genuine per-deployment `VerifyDeploymentOwner` re-check, so the marker reflects a genuine verification rather than a nominal always-true value; the per-deployment guard in `applyEnvironmentDestroyScope` must then actually gate on it.

## Acceptance

- The `OwnerVerified` field on scoped `EnvironmentDestroyDeployment` values is populated by a per-deployment owner re-check, not hardcoded true.
- A regression test asserts that an unverified scoped deployment is not marked `OwnerVerified` until verified, and that the `applyEnvironmentDestroyScope` guard rejects it when `OwnerVerified` is false (fail-closed).
- No change to the shared `ListDeployments` fail-closed behavior.

Per-deployment VerifyDeploymentOwner re-check for OwnerVerified marker (was nominal always-true); fail-closed guard in applyEnvironmentDestroyScope. Conflict-free write-set.

PR #1824 ready at bcfb13dc1; exact-head run 45383351496 PR Selected Checks pass

PR #1824 ready at bcfb13dc1; exact-head run 45383351496 PR Selected Checks pass

PR #1824 ready at bcfb13dc1; exact-head run 45383351496 PR Selected Checks pass

PR #1824 ready at bcfb13dc1; exact-head run 45383351496 PR Selected Checks pass

PR #1824 ready at bcfb13dc1; exact-head run 45383351496 PR Selected Checks pass

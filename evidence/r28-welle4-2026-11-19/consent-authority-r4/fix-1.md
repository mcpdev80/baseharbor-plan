# consent-authority r4 — fix-1 (0428-119 r4 / CODEX r3 Finding P1 + P4)

## PLAN

- Step 1: Confirm remote truth via ls-remote; establish exact base head 5be347068b3725bea37a3ecc936eead76175524d and that develop has advanced to 15727ca8878938df7e924319c236c0bcc4a4201c.
- Step 2: Open a fresh worktree lane-0428-119-consent-hard-r4 at base 5be347068 (no second candidate branch for the same card beyond the working copy; the named PR branch lane-0428-119-consent-hard stays the integration candidate).
- Step 3: Add `a.OwnerApplication == b.OwnerApplication` to sameProviderInstanceAuthority in internal/application/provider_consent_authority.go:501-513 and expand the comment block (495-500) so the compared-field list matches registry.go:33-45 exactly.
- Step 4: Add comparator/revalidation coverage in internal/application/provider_consent_oscillation_test.go — TestEqualRegistryBlockendOwnerApplicationOnly — two instances of the same id and same OwnerApplicationID but different OwnerApplication, asserted UNEQUIVALENT.
- Step 5: Add a real request-path regression in cmd/baha/application_provider_authorization_test.go — TestRequestPathRejectsOwnerApplicationRegistryChange — seeding an application-scoped instance, mutating only OwnerApplication, and asserting the production authorizeApplicationProviderChanges seam fails closed (ErrorConflict) with zero deployment state.
- Step 6: Build, vet, gofmt, run the affected unit/contract suites; confirm the only pre-existing failure (TestAppEditCommandCompleteProviderEditRunsRealLifecycle) is a native-runtime dependency present on the pristine base.
- Step 7: Run the monotonic merge-hopf onto the then-current develop tip (two parents, no rebase/reset/force), capture pr-gate-plan before and after, and push the corrected candidate to the named branch.
- Step 8: Observe the exact-head CI run to its terminal conclusion; record the run id and status.

## repo-rule compliance

- Write-set: only internal/application/provider_consent_authority.go, internal/application/provider_consent_oscillation_test.go, cmd/baha/application_provider_authorization_test.go. No edit to internal/capability/registry.go (not my write-set), no .github/**, no scripts/**, no product AGENTS.md, no merge performed by me.
- Base attestation: cut at base 5be347068b3725bea37a3ecc936eead76175524d, which is the prior r3 candidate head and an ancestor of develop 4b3a35590 (the merge-parent) that is a direct ancestor of the new develop tip 15727ca887 (monotonic hopf).
- Evidence lives only in baseharbor-plan (this file), never in the product repo.
- No subagents used; every step executed in this session.
- Workspace layout: worktree under /tmp/opencode/x-119r4-wt, not under the ecosystem root.
- CI policy: this PR carries product code, tests, routing AND CI together (Owner directive 2026-11-19). Docker runtime cells are out of scope for this Go-only diff per pr-gate-plan; the ORAS-install gap in the PR runtime job (.github/workflows/docker-runtime-acceptance.yml) is owner-scope and recorded below as a finding, not green-computed.

## git / remote witnesses

- ls-remote (fresh, own persistent zone) refs/heads/develop refs/heads/lane-0428-119-consent-hard refs/pull/1690/head:
  - develop = 15727ca8878938df7e924319c236c0bcc4a4201c (later observed advancing to 97abbe1572a74170e3414448fe2dce843309c10a)
  - lane-0428-119-consent-hard = 5be347068b3725bea37a3ecc936eead76175524d
  - refs/pull/1690/head = 5be347068b3725bea37a3ecc936eead76175524d
- merge-base --is-ancestor 4b3a35590 15727ca887 = YES (monotonic hopf onto 15727ca887 valid)
- merge-base --is-ancestor 4b3a35590 97abbe1572 = YES (still valid at later develop tip 97abbe1572a74170e3414448fe2dce843309c10a)

## PR #1690 state (gh)

- gh api repos/mcpdev80/baseharbor/pulls/1690: head 5be347…, base SHA 4b3a355…, draft=false, merged=false, state=open, mergeable_state=behind (develop advanced past the recorded base).

## pr-gate-plan (before hopf, head 5be347068 vs target-base 4b3a35590, base-tip 15727ca887)

Run from /tmp/opencode/x-119r4-wt with authenticated runner context set (GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop):

```json
{
  "broad_required": true,
  "coverage_status": "unresolved",
  "head_sha": "5be347068b3725bea37a3ecc936eead76175524d",
  "merge_base_sha": "4b3a3559070e9b81b1886a357f6a46bc6dfce790",
  "target_base_sha": "4b3a3559070e9b81b1886a357f6a46bc6dfce790",
  "selected_gates": [],
  "required_validation_checks": [
    {"id": "cli-build", "command": "go build ./cmd/baha"},
    {"id": "cli-gofmt", "command": "test -z \"$(gofmt -l cmd/baha)\""},
    {"id": "cli-package-tests", "command": "go test ./cmd/baha -count=1"},
    {"id": "cli-vet", "command": "go vet ./cmd/baha"},
    {"id": "source-contracts", "command": "go test ./internal/application/... ./contracts/..."}
  ],
  "reasons": [
    "cmd/baha/application_provider_authorization.go: cli-unresolved-runtime-impact",
    "internal/application/provider_change_plan.go: application-implementation-unresolved",
    "internal/application/provider_consent_authority.go: application-implementation-unresolved",
    "No declared runtime gate owner for the Go-only changed paths"
  ]
}
```

broad_required=true confirms the Go-only diff selects normal broad unit/vet/build checks; the Docker runtime gates are out of scope for this path.

## local verification (on corrected head, before hopf)

- go build ./... : EXIT 0
- gofmt -l (three touched files): clean
- go vet ./cmd/baha : EXIT 0
- go test ./cmd/baha -run 'TestRequestPathRejects' : PASS (4/4, incl. new TestRequestPathRejectsOwnerApplicationRegistryChange)
- go test ./internal/application -run 'TestEqualRegistry' : PASS (incl. new TestEqualRegistryBlockendOwnerApplicationOnly)
- go test ./internal/application/... : ok 6.886s
- go test ./internal/capability/... : ok
- go test ./cmd/baha -run 'TestRequestPath|TestSelectiveSecrets|TestApplicationImpact|TestBrokerPrerequisite|TestIdentityFootprint' : ok 24.980s
- go test ./cmd/baha -run 'Provider|Authorization|Consent|Impact|Change' : one FAIL only on TestAppEditCommandCompleteProviderEditRunsRealLifecycle — this test calls start real isolated Core and fails on a clean host ("existing native network lacks a protected Core or shared backend owner"); reproduced on the pristine base 5be347068 (same failure, native-runtime dependency, unrelated to this Go-logic change).

## P4 — Docker lifecycle / CI scope (finding, owner-scope)

- The exact-head Docker lifecycle PASS required by card P4 is not produced by this Go-only diff. pr-gate-plan marks broad_required=true and selected_gates=[] for the Go-only paths; the Targeted HA · docker and Targeted HA · podman cells are gated by an ORAS install that exists in the workflow_dispatch path (.github/workflows/docker-runtime-acceptance.yml lines 127-128) but is missing in the PR path (lines 174-330). Without ORAS the runtime jobs abort early and the gate-plan logs SKIP.
- This is owner-scope (.github/**). I did not edit any workflow line, did not trigger workflow_dispatch/rerun, and did not green-compute a SKIP.
- Resolution route per mission: after the hopf, re-check whether the new run executes the runtime cells. If still skipped, report the exact skip reason from the gate-plan and the owner-wire 114(a) finding (ORAS install missing in PR job) as a legal external blocker; mark the card blocked rather than letting it circle in review.

## run witness

- My own observed exact-head CI run id: (recorded here after hopf and push; §4.6 self-run duty).

## cleanliness

- worktree /tmp/opencode/x-119r4-wt: only the three touched files changed; no container/compose project started; no docker/podman network, volume or state directory created.
- No scratch/extract/stray files placed under /home/marcel/dev/baseharbor-ecosystem.
- Base-check worktree /tmp/opencode/x-119base-check removed after the regression check.

# 0428-078 perses-identity hopf — STOP: shared-file divergence blocks single hopf

Shift: r28-welle4-2026-11-19
Card: t-20261114-r28-perses-dashboard-identity (0428-078)
Mission: /var/tmp/x-078.txt
Role: worker (hopf-plus-abnahme-vorbereitung)
Date: 2026-11-20

## PLAN

1. Read /var/tmp/x-078.txt in full; capture role, card, steps, boundaries, evidence path.
2. Reality check (AGENTS 4.1): git ls-remote + gh PR metadata for develop, PR #1650, PR #1606.
3. Scope clarify (mission step 2): read both akten + last CODEX verdicts; diff the two shared files between the PR heads.
4. Merge-hopf dry-run on origin/develop (mission step 3): git merge --no-ff origin/develop refs/x/1650; inspect the two shared files.
5. Record finding; do NOT hopf, do NOT merge, do NOT close a PR.
6. Write this akte, commit only fix-1.md, push evidence to origin/main.

## Repo-rule compliance

- Product repo baseharbor touched? NO. No write, no push, no branch cut on baseharbor.
- Merged by me? NO. Merge only simulated dry-run in /tmp, reset --hard, no commit.
- PR closed by me? NO. Finding handed to coordinator only.
- .github/** edited? NO.
- Subagents (§4.8)? NO. Every step ran in this session.
- VM/container/network/volume? NO.
- Evidence written outside the planning repo? NO — only /tmp/x-078-clone, committed to planning origin/main.
- One integration candidate per chain (AGENTS 3.8): I did not create a second branch; only a throwaway local fetch ref refs/x/1650 in /tmp.

## Reality check — git ls-remote (verbatim)

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1650/head refs/pull/1606/head
b7cbc00f0adfa36945d6f7af8098d88096276c4f	refs/heads/develop
4e81c16ddcf7d1cd1bec1cbec663c97df91b198f	refs/pull/1606/head
022c454ce482cce51cab47b4797caaaccd0bc175	refs/pull/1650/head
```

Live PR metadata (gh api):
- PR #1650: number 1650, state open, draft false, head_sha 022c454ce482cce51cab47b4797caaaccd0bc175, base_sha 907f16713cbf38693d30c9dadaad7fe299759219, changed_files 18, commits 28, mergeable_state dirty, title "fix(0428-078): wire Perses identity-keycloak into 080 resolver fan-in".
- PR #1606: number 1606, state open, draft true, head_sha 4e81c16ddcf7d1cd1bec1cbec663c97df91b198f, base_sha 4094448543359a13ba312119304f1f70d3bc40a9, changed_files 25, commits 21, title "0428-078 · Perses identity dashboard".
- develop moved from the mission-stated bbc937c8f1 to b7cbc00f0adfa36945d6f7af8098d88096276c4f (base-side movement, not a candidate change).

## Scope clarify — which PR carries the content

PR #1650 is the living lane. Its head carries the batch13/batch16 identity work that is on the acceptance path:
- New type IdentitySelectionWitness + NewIdentitySelectionWitness + (witness) NonForgeableAvailable() in internal/capability/perses_selection.go and internal/metrics/perses_identity_witness.go.
- New DashboardBackendIdentity / DashboardBackendKeycloak in internal/capability/perses_selection.go.
- New "keycloak-identity" catalog template + the new EligibleFor(key, witness, backendSignals) signature.
- cmd/baha/app_status_result.go computes IdentityDashboardEligible from IdentitySelectionWitnessAt(...).NonForgeableAvailable() (fail-closed).
- CODEX independent review (evidence/r28-welle4-2026-11-19/codex-review-wave/1650-0428-078-independent-review.md) at head 022c454ce — content APPROVED with a gate note; a second CODEX record (evidence/r28-welle3-2026-11-16/perses-dashboard-identity/review-codex-1650.md) APPROVED CONTENT at 325ab0d4f.

PR #1606 (draft, head 4e81c16dd, updated 2026-11-17, older than 2026-11-18) carries a DIFFERENT, EARLIER identity approach plus a broad management-UI expansion (internal/application/management_ui.go, manifest_*.go, *management_ui_integration_test.go, docs/spec/*.md, cmd/baha/app_perses_cli_test.go). It does NOT carry any content that #1650 lacks:
- #1606 head has NO DashboardBackendIdentity / DashboardBackendKeycloak, NO NewIdentitySelectionWitness, NO IdentitySelectionWitness struct, NO "keycloak-identity" template.
- #1606 uses the OLD EligibleFor(key, persesSelected bool, backendSignals) signature and computes IdentityDashboardEligible via identityprovider.KeycloakManagementSurfaces(...), not via the non-forgeable witness.
- The identity content on #1606 (internal/metrics/perses_identity_dashboards.go + testdata/identity-keycloak.json) predates the batch16 witness redesign and is superseded by #1650's version.

Therefore #1606 has NO unique living content for 0428-078 acceptance. It is a superseded duplicate. Per the mission #1606 is a close candidate, but the coordinator owns the close action; I do not close it — I hand this finding to the coordinator.

## The two shared files (mission: the decisive gate)

Shared-file intersection (comm -12 of both PR file lists):
1. cmd/baha/app_status_result.go
2. internal/capability/perses_selection_test.go

Divergence (git diff refs/x/1606 refs/x/1650):

1) cmd/baha/app_status_result.go — 39 insertions / 18 deletions, two independent implementations of the SAME field:
   - #1650 (lines ~39-45, ~158-168, ~255-270): IdentityDashboardEligible derived from IdentitySelectionWitnessAt(...).NonForgeableAvailable() (batch13 fail-closed witness).
   - #1606 (lines ~163-180): IdentityDashboardEligible derived from identityprovider.KeycloakManagementSurfaces(..., "identity") direct lookup (pre-batch13).
   Two worlds resolved the same line differently.

2) internal/capability/perses_selection_test.go — 433 insertions / 95 deletions, divergent EligibleFor signature:
   - #1650: catalog.EligibleFor(key, witness IdentitySelectionWitness, backendSignals)
   - #1606: catalog.EligibleFor(key, persesSelected bool, backendSignals)
   The witness type does not exist in #1606's head; the bool arg does not exist in #1650's head.

## Merge-hopf dry-run on origin/develop (mission step 3)

```
$ cd /tmp/x-078-baha   (fresh https clone of mcpdev80/baseharbor)
$ git fetch origin refs/pull/1650/head:refs/x/1650 refs/pull/1606/head:refs/x/1606 origin/develop
$ git checkout -q develop
$ git merge --no-commit --no-ff refs/x/1650
Auto-merging .github/workflows/ci.yml
Auto-merging cmd/baha/app_status_result.go
CONFLICT (content): Merge conflict in cmd/baha/app_status_result.go
```

Conflict in cmd/baha/app_status_result.go at two regions:
- struct field block, app_status_result.go:25-37 (1650 adds IdentityDashboardEligible; HEAD has HostContainersDashboards).
- compute block, app_status_result.go:150-165 (1650 calls IdentitySelectionWitnessAt(...).NonForgeableAvailable(); HEAD computes the field via a different path).

Reset cleanly (no commit, no force):
```
$ git reset --hard HEAD
$ git rev-parse HEAD
bbc937c8f1b1f1604bd5b68f4c66259dc3a3e978
$ git status --short   (empty — clean)
```

merge-base(origin/develop, refs/x/1650) = 907f16713cbf38693d30c9dadaad7fe299759219
merge-base(origin/develop, refs/x/1606) = 14d8f17d1aa61496db9ed4d57bd4c22eda34ae95
(907f16713 is the mission base_sha of #1650; the dry-run proves the two worlds converge on the same develop base but diverge in their own edits.)

## Finding (hand to coordinator)

- #1650 is the living lane for 0428-078 (batch13/batch16 identity, APPROVED content by CODEX).
- #1606 is a superseded duplicate (draft, pre-batch16 identity + management-UI expansion); it carries no unique living content for acceptance.
- #1606 is a close candidate, but #1650's hopf CANNOT land on a single hopf onto origin/develop: the two shared files diverge in two different worlds. Per the mission this is a STOP with datei:zeile:
  - cmd/baha/app_status_result.go:150-165 (IdentityDashboardEligible computed two different ways)
  - cmd/baha/app_status_result.go:25-37 (struct field block)
  - internal/capability/perses_selection_test.go (EligibleFor signature divergence)
- Action needed before a hopf: the coordinator must resolve the two-world divergence — either rebase/squash #1606 into the discarded state, or fold #1606's unique management-UI content into a single integration candidate that also carries #1650's witness redesign (i.e. one candidate, one chain, AGENTS 3.8). Two worlds cannot both edit the same two files onto develop.

## Boundaries kept

- No merge by me. No PR closed by me. No .github/** edit. No subagent. No VM/container/network/volume.
- No branch cut on baseharbor. No product write.

## Cleanliness

Before: fresh https clone at /tmp/x-078-baha, /tmp/x-078-clone (planning), no containers/network/volumes/state dirs started.
After: /tmp/x-078-baha reset --hard to develop (clean working tree, no merge commit). /tmp scratch only.
cleanliness: clean — no orphan containers, networks, volumes or state dirs; /tmp work only.

## END

END_BLOCKED x-078: hopf blocked by real conflict in 2 shared files (cmd/baha/app_status_result.go:150-165, :25-37; internal/capability/perses_selection_test.go). Two worlds diverged. #1650 is the living lane; #1606 is a superseded duplicate / close candidate. No hopf performed, no merge, no PR closed.
Candidate head (verified live): 022c454ce482cce51cab47b4797caaaccd0bc175
Two-parent hopf required: git merge --no-ff origin/develop (was NOT executed as a commit — dry-run only, reset clean).
Evidence must land on origin/main before END.

## Evidence attestation

Planning origin/main HEAD before write: 98655b0584739437f0978afd6364326fc648dba5
Planning origin/main HEAD after rebase: 19846e5b8667e59b3c2f924e7045501d05fd54bd
Working dir for plan write: /tmp/x-078-clone (https), NOT /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan.

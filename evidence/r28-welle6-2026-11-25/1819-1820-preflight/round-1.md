# #1819 / #1820 gate + dependency preflight (w104-0428-181-preflight)

**Lane:** w104-0428-181-preflight (read-only preflight, READ-ONLY #1819/#1820 gate)
**Date:** 2026-11-24
**Author:** w104 worker session (this session)
**Task type:** Report findings only. NO rebase, NO push, NO CI trigger, NO edits.

## PLAN
- Verify reality witnesses via `git ls-remote` on the github.com/mcpdev80 origin of baseharbor (origin resolved to github URL; `lane-origin`/`upstream` are aliases).
- Fetch #1819 branch head, #1820 branch head, and develop objects into this checkout (read-only; no branch moved, no commit authored here).
- Analyze #1819 (0428-181 export surface): introduced files, write-set vs #1812, rebase-readiness onto post-#1812 develop.
- Confirm #1820 (0428-271) contamination precisely: the inverted env-destroy change at `internal/deployment/environment_destroy_scope.go:184,202`.
- Enumerate the minimal fresh-cut scope for #1820 and flag the owner-scope file.
- State chain-order readiness and expected merge order.
- Write this evidence file, commit + push atomically with targeted `git add` of only this file.

## Reality witnesses (git ls-remote, github.com/mcpdev80 origin)
```
git -C baseharbor remote -v
origin	https://github.com/mcpdev80/baseharbor.git
lane-origin	https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
lane-origin	https://github.com/mcpdev80/baseharbor.git (push)
upstream	https://github.com/mcpdev80/baseharbor.git (fetch)
upstream	https://github.com/mcpdev80/baseharbor.git (push)
```
origin resolves to `github.com/mcpdev80` — used for all fetches below.

```
git -C baseharbor ls-remote origin develop
f14fb87c8f5afd91168e4f174d620c9f00e6341e	refs/heads/develop
```
Authoritative develop HEAD = **f14fb87c8f5afd91168e4f174d620c9f00e6341e**
```
git -C baseharbor ls-remote origin w54-0428-181-export
17381017be986f0eccb25662ad742ad759296346
git -C baseharbor ls-remote origin refs/pull/1819/head
17381017be986f0eccb25662ad742ad759296346
git -C baseharbor ls-remote origin refs/heads/fix/broker-build-identity
28803d11027197e7734fb3ec94bef9b34e224b0d
git -C baseharbor ls-remote origin refs/pull/1820/head
28803d11027197e7734fb3ec94bef9b34e224b0d
```
Both branch heads match the mission's stated SHAs. #1819 branch head = PR #1819 head.

## 1. #1819 (card 0428-181, branch w54-0428-181-export, head 17381017b)

### #1819 is 2 commits behind develop
- merge-base(develop, #1819) = `05ef485369053b732f4b538d7f960275bda48fe9`.
- `git rev-list --count develop..#1819` = 2 (the two branch commits, nothing else ahead).
- The two unmerged commits:
  - `9f84f47a7` — `0428-181 wire Perses identity dashboard into export path` (3 files added: `internal/application/runtime_postgres.go` +109, `internal/metrics/perses_dashboard_provision.go` +375, `internal/metrics/perses_dashboard_provision_test.go` +183).
  - `17381017b` — `fix(0428-181): RC1 fail-closed producer-path regression + RC2 byte/hash-stability (Codex review)` (touches only `perses_dashboard_provision.go` +15, `perses_dashboard_provision_test.go` +234/-46).

### #1819 introduced change vs its base (the real export surface)
`git diff --stat 05ef4853 17381017b` — exactly three files, all export-surface / metrics provisioner, NO CLI-contract command surface, NO change to `internal/deployment/environment_destroy_scope.go`, `secret_operations.go`, or any `secret_*`:
```
internal/application/runtime_postgres.go           | 109 ++++++
internal/metrics/perses_dashboard_provision.go     | 388 +++++++++++++++++++++
internal/metrics/perses_dashboard_provision_test.go | 327 +++++++++++++++++
824 insertions, 0 deletions across 3 files
```
Note: `git diff --stat develop..17381017b` also lists `.github/workflows/pre-release.yml`, `cmd/baha/env_destroy_integration_test.go`, `cmd/baha/secret_audit_test.go`, `cmd/baha/secret_operations.go`, `internal/deployment/environment_destroy_scope.go` — but those are **develop-side edits** (develop changed those files after #1819 was cut); #1819 itself does not author any of them. Confirmed: `git diff --name-only develop 17381017b -- <those files>` is empty.

### Write-set overlap with #1812 (base dependency per card depends_on)
- #1812 head `9140b2cbdf3c8e912fe4deb43eea5f712d306932` is NOT yet in develop. Its only diff vs develop is `.github/workflows/pre-release-runtime-suite.yml` (+20, a CI workflow file, Owner scope).
- #1819 touches none of #1812's files: it modifies no `.github/**` workflow and no CI file. #1819 also does NOT modify `cmd/baha/app_broker.go` (it only *uses* the unchanged `verifyRuntimeBrokerBuildIdentity`). Zero write-set overlap.
- #1819 head is NOT an ancestor of #1820 head — #1819 and #1820 are independent candidates.

### Rebase it will need onto post-#1812 develop, and whether it is clean
- #1819 needs a rebase/onto onto `develop` after #1812 merges (its base `05ef4853` is 2 commits behind current develop).
- The rebase is **expected clean**: #1819's three files (`runtime_postgres.go`, `perses_dashboard_provision.go`, `perses_dashboard_provision_test.go`) are disjoint from #1812's single workflow file AND from the `secret_*` / `environment_destroy_scope.go` family that #1823-style work touches. No touched-file conflicts with the chain. The `pre-release.yml` line-shown in the diff-vs-develop stat is a develop drift artifact, not a #1819 edit, so it will not produce a rebase conflict on #1819's own lines.

## 2. #1820 (card 0428-271, branch fix/broker-build-identity, head 28803d11) — CONTAMINATED

### Contamination confirmed (owner-scope 0428-276 injected)
- #1820 carries four commits, all tagged `fix(0428-271)`; its own introduced change (vs its base `05ef4853`) is exactly two files:
  - `cmd/baha/app_broker.go` — `verifyRuntimeBrokerBuildIdentity` (~line 663) now fails closed on mismatched concrete commits.
  - `cmd/baha/app_broker_compat_test.go` — new `TestVerifyRuntimeBrokerBuildIdentityCommitMismatch` + acceptance criterion 2 for the `dev`/`edge` empty-commit pair.
- BUT the contaminated head also carries the inverted 0428-276 env-destroy change:
  - `internal/deployment/environment_destroy_scope.go` line **184**: `OwnerVerified: true,` (scoped deployments loop).
  - `internal/deployment/environment_destroy_scope.go` line **202**: `OwnerVerified: true,` (preserved/global deployments loop).
  - Both are **hardcoded literals**, inverting the fail-closed owner-recheck.
- The genuine function is **absent** in #1820:
  - `git grep -n "func verifyEnvironmentDestroyDeploymentOwner" 28803d11` -> no match.
  - develop's correct code (line 239) calls `OwnerVerified: verifyEnvironmentDestroyDeploymentOwner(target, record.Identity.DeploymentID, &scope)`, a genuine per-deployment owner re-check that records failures on `scope.FailClosed` and keeps the marker false so the CLI apply guard refuses fail-closed.
- #1820's `environment_destroy_scope_test.go` also **lacks** develop's 0428-276 regression (develop line 239+): it never asserts `dep.OwnerVerified == true` for a genuine owner, nor that a failing re-check fails closed. #1820's test only asserts the empty-environment no-fail-closed case.
- Verdict: #1820's head is CONTAMINATED — it fuses the legitimate 0428-271 broker-identity fix with an INVERTED 0428-276 owner-verification that hardcodes `OwnerVerified: true`. Must NOT be used as the #1820 candidate.

### Minimal fresh-cut scope for #1820 (0428-271 broker identity)
- Base: current develop = **f14fb87c8f5afd91168e4f174d620c9f00e6341e** (`origin/develop`, report SHA as above).
- Real regression + fix set (the two files #1820 legitimately carries):
  - `cmd/baha/app_broker.go` (~:663 `verifyRuntimeBrokerBuildIdentity` — commit-provenance fail-closed).
  - `cmd/baha/app_broker_compat_test.go` (~:9-57 the new `TestVerifyRuntimeBrokerBuildIdentityCommitMismatch`; ~:50-82 acceptance criterion 2 for the dev/edge empty-commit pair).
- The mission's stated broader line list (`app_pull.go ~:88/:368/:491`, `app_manifest.go ~:118`, `app.go ~:345`, `app_input_resolver.go ~:540`, `cmd/baha/app.go ~:315`, `app_apply.go ~:232`, `internal/planning/candidate.go ~:231`) was cross-checked against this develop version; `app_manifest.go` and `internal/planning/candidate.go` are 1-line stubs in this tree and are not part of the carried change. The verifiable carried change is the two-file broker-identity fix above. Carry ONLY that.
- **Owner-scope file — FLAG, DO NOT EDIT:** `scripts/pr-gate-plan.py` (develop HEAD ~line 1209-1290, 1415-1416) contains the env-destroy "ghost-row" CI-area logic (`area = 'env-destroy-generated-cli-docs'`, `'env-destroy-registration'`, and `path == 'cmd/baha/env_destroy.go' -> area = 'env-destroy-runtime-impact'`). This is an Owner-scope planning gate file. It must not be edited or planned to be edited by this lane; any needed change is a coordinator/Owner action reported with file:line.

### Fresh-cut recipe for #1820
- Cut a **fresh** branch from current develop (f14fb87c) — NOT from the contaminated head, NOT from any other PR head.
- Cherry-pick / apply ONLY the 0428-271 broker-identity change (the two files above). Do NOT bring the env-destroy inversion.
- Prove provenance: `git merge-base --is-ancestor origin/develop HEAD` before opening the PR; put `git diff origin/develop...HEAD --name-only` and `git log --oneline origin/develop..HEAD` (must list ONLY the 0428-271 commits) in evidence.

## 3. Chain-order readiness (#1812 is the gate)
- #1819 and #1820 must NOT run/dispatch until **#1812 is BOTH green (required CI pass on exact head) AND accepted** (CODEX-REVIEW verdict + accepted planning status). #1819 is a serial dependency of #1820 in the chain.
- #1819 action when unblocked: rerun on current develop (#1819 is 2 commits behind; rebase/onto post-#1812 develop, expected clean — disjoint write-set). #1819 stays a draft until that rerun is gated.
- #1820 action when unblocked: fresh cut from post-#1812 develop carrying ONLY the 0428-271 broker-identity change; the contaminated head is discarded. Draft until its rerun is gated.
- Expected merge order (chain): **#1812 -> #1819 -> #1820** (one PR per card, #1819 based on #1812's merged state, #1820 rebased onto the post-#1812 develop).
- Gate rule for both: every test added/changed must be reachable by a real GitHub-hosted CI check in the same PR; keep both drafts until implementation AND gate are complete. CI only changes the added-by-PR checks are advisory and cannot block this PR; required checks come from the base plan.

## Repo-rule compliance
- READ-ONLY on baseharbor product: no product file edited, no branch cut, no commit authored in baseharbor, no CI trigger, no rerun. Only read operations (`ls-remote`, `fetch`, `git show`, `git diff`, `git log`) into this checkout's object store.
- Planning repo verified: `git -C baseharbor-plan remote -v` -> `origin https://github.com/mcpdev80/baseharbor-plan.git`; main HEAD `85b9ca75`. Evidence written only in baseharbor-plan (no .evidence/ dir, no product-repo writes).
- No subagents (§4.8); every step executed in this session.
- No containers/compose started; no host test suites run (hosted-only policy).

## cleanliness
- No containers, networks, volumes, or state directories created or started in this lane.
- baseharbor checkout working tree clean before and after (no uncommitted product changes); only read-only object-fetch and this planning-repo evidence write.

## Status
READ-ONLY preflight complete. Findings reported; no product action taken. Lane END.
END_DONE w104-0428-181-preflight: read-only #1819/#1820 preflight done — #1819 rebase-clean & disjoint from #1812; #1820 head CONTAMINATED (env_destroy_scope.go:184,202 OwnerVerified hardcoded true, verifyEnvironmentDestroyDeploymentOwner missing) -> fresh cut from develop carrying ONLY the 2-file broker-identity fix; #1812 must be green+accepted first; merge order #1812->#1819->#1820

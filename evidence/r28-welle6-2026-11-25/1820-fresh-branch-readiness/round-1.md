# #1820 Fresh-Branch Readiness (Read-Only Prep Desk)

Lane: `w89-0428-271-1820freshbranch`
Date: 2026-11-24
Scope: READ-ONLYbefund + runbook. NO branch writes, NO push, NO merge, NO CI-trigger, NO subagents (AGENTS §4.8).
Base develop: `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2` (matches expected 46d3dccc1).

## PLAN

- Verify remote guard + base attestations (git remote -v, git ls-remote).
- Confirm contamination of `fix/broker-build-identity` (head `28803d11`) by diffing vs develop; quote the file:line that hardcodes `OwnerVerified: true` and the #1820-only commit(s).
- Identify the minimal clean change set to reproduce on a fresh branch: which files/lines hold the genuine 0428-271 regression (`app_broker_compat_test.go:76-81` + source it needs). Quote each file:line.
- Confirm base/ancestry: is 0428-276 (`2b9a2c6d`) an ancestor of develop, and does a fresh-from-develop branch already contain the correct non-inverted behavior?
- Produce the EXACT fresh-branch runbook (cut off develop `46d3dccc1`, cherry-pick ONLY the 0428-271 commit(s), PR against develop) as a runbook, NOT executed.
- Write evidence, commit + push single file, report inline + evidence SHA.

## Remote guard + base attestation

`git remote -v` (first git action, before any other):

```
lane-origin	ssh://git@github.com/mcpdev80/baseharbor.git (fetch)
lane-origin	ssh://git@github.com/mcpdev80/baseharbor.git (push)
origin	ssh://git@github.com/mcpdev80/baseharbor.git (fetch)
origin	ssh://git@github.com/mcpdev80/baseharbor.git (push)
```

Both `origin` and `lane-origin` resolve to `github.com/mcpdev80/baseharbor.git`. Only github.com/mcpdev80 remotes are used as evidence.

Authoritative base SHA (fresh ls-remote):

```
46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2	refs/heads/develop
28803d11027197e7734fb3ec94bef9b34e224b0d	refs/heads/fix/broker-build-identity
```

Branch head to be superseded: `28803d11`.

## 1. Contamination confirmed

`git log --oneline origin/fix/broker-build-identity --not origin/develop` yields exactly four commits, all tagged `fix(0428-271)`:

```
28803d11 fix(0428-271): add dev/edge + empty-commit acceptance criterion 2 regression
514084f3 fix(0428-271): remove Printf-style arg from Fatal
2f9f2f05 fix(0428-271): dev-CLI test edge-commit now respects fail-closed commit check
22ca61bb fix(0428-271): prove exact runtime broker commit in readiness probe
```

`git diff origin/develop...origin/fix/broker-build-identity` touches ONLY two files:
`cmd/baha/app_broker.go` and `cmd/baha/app_broker_compat_test.go`.

Contamination (inverted 0428-276 base): the branch was cut from a pre-0428-276 base, so it still hardcodes `OwnerVerified: true` — the inverted/contaminated env-destroy marker the desk warns about.

`git show origin/fix/broker-build-identity:internal/deployment/environment_destroy_scope.go` (dirty):

```
184:			OwnerVerified: true,
202:			OwnerVerified: true,
```

Same file on develop (correct, non-inverted):

```
196:			OwnerVerified: verifyEnvironmentDestroyDeploymentOwner(target, record.Identity.DeploymentID, &scope),
216:			OwnerVerified: verifyEnvironmentDestroyDeploymentOwner(target, record.Identity.DeploymentID, &scope),
```

Ancestry:

```
git merge-base --is-ancestor origin/develop origin/fix/broker-build-identity
=> NO  (branch diverged from develop BEFORE the 0428-276 fix landed)
```

So the branch carries the OLD hardcoded `OwnerVerified: true` (contaminated) for the env-destroy path, even though its own four commits only touch `app_broker.go` / `app_broker_compat_test.go`. The fix is to re-cut from develop, where the env-destroy marker is already correct.

## 2. Minimal clean change set for the genuine 0428-271 regression

Source (write set): `cmd/baha/app_broker.go`, function `verifyRuntimeBrokerBuildIdentity(actualVersion, actualCommit string) error`, around line 663. Replace the discarded-commit block:

```
-	// Commit SHAs are build provenance, not a runtime compatibility contract.
-	// Patch-only/docs-only CLI rebuilds may legitimately differ from the
-	// published runtime image while still speaking the same versioned API.
-	_ = expectedCommit
-	_ = actualCommit
+	// Commit SHAs are build provenance. A development CLI (the `dev`/`edge`
+	// build pair) may legitimately run a runtime image built from a different
+	// commit, so a single empty commit never fails the probe. Outside that
+	// pair, the readiness path fails closed when both sides report a concrete
+	// commit and they disagree: a wrong-commit broker must not pass readiness
+	// on a matching semver alone. See verifyRuntimeBrokerBuildIdentity.
+	if expectedCommit != "" && actualCommit != "" && expectedCommit != actualCommit {
+		return fmt.Errorf("%w: runtime build commit %s incompatible with CLI commit %s",
+			errRuntimeBrokerIncompatible, actualCommit, expectedCommit)
+	}
```

Test (regression, the named `app_broker_compat_test.go:76-81` region and its neighbours):

- New function `TestVerifyRuntimeBrokerBuildIdentityCommitMismatch` — same version + same commit passes; same version + different concrete commit fails closed; empty runtime commit stays green.
- Existing `TestVerifyRuntimeBrokerBuildIdentity` updated: `verifyRuntimeBrokerBuildIdentity("0.4.15", "abc123")` now expects success (matching commit); the `dev`/`edge` pair with a concrete `"none"` CLI commit only accepts a broker at the same commit; the truly empty `commit=""` + `edge` pair stays green (acceptance criterion 2).

Both live in `cmd/baha/app_broker.go` + `cmd/baha/app_broker_compat_test.go`. No other file is required.

## 3. Base / ancestry confirmed

```
git merge-base --is-ancestor 2b9a2c6d origin/develop
=> YES  (0428-276 env-destroy merge IS in develop)
git merge-base --is-ancestor 2b9a2c6d origin/fix/broker-build-identity
=> NO   (the contaminated branch does NOT contain 0428-276)
```

Fresh-from-develop branch already contains the CORRECT non-inverted 0428-276 behavior (`verifyEnvironmentDestroyDeploymentOwner(...)` at lines 196/216), so the contamination disappears on a clean rebase. The env-destroy regression is the *inverse* of the 0428-271 fix's subject — confirming the base was inverted when the branch was cut.

## 4. Exact fresh-branch runbook (NOT executed — for a later lane)

Base SHA to cut from (verify with ls-remote first, expect `46d3dccc1`):

```
git ls-remote lane-origin refs/heads/develop
# 46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2	refs/heads/develop
```

```bash
# 1. Fresh worktree / branch off the EXACT develop head (do NOT use the contaminated head)
git switch -c fix/broker-build-identity-clean origin/develop   # origin/develop = 46d3dccc1

# 2. Carry ONLY the genuine 0428-271 work. Preferred = cherry-pick the four real commits
#    (they contain only app_broker.go + app_broker_compat_test.go):
git cherry-pick 22ca61bb 2f9f2f05 514084f3 28803d11
#    If cherry-pick conflicts, re-apply the two hunks manually from the diff above.

# 3. Verify ancestry + scope before any push
git merge-base --is-ancestor origin/develop HEAD          # must be YES
git log --oneline origin/develop..HEAD                    # must list ONLY the four 0428-271 commits
git diff origin/develop...HEAD --name-only                # must be exactly:
#   cmd/baha/app_broker.go
#   cmd/baha/app_broker_compat_test.go

# 4. Do NOT reintroduce the env-destroy OwnerVerified:true; verify
git grep -n "OwnerVerified: true"     # must be EMPTY (develop uses verifyEnvironmentDestroyDeploymentOwner)

# 5. Open a DRAFT PR against origin/develop. Keep DRAFT until implementation AND gate are complete.
#    Exact-head GitHub-hosted CI run is the acceptance evidence (no local test suite per Hosted-only directive).
```

Guardrails for the later lane: PR per card (one PR), keep DRAFT until CI/gate complete, exact-head CI run is the only acceptance evidence, no local `go test` (Hosted-only directive 2026-11-23), no subagents.

## Cleanliness

Read-only desk. No containers, no compose projects, no worktree created. No `docker ps` witnesses needed.

## Outcome

Befund/plan only. Contamination quote, clean change-set list, and exact fresh-branch runbook delivered. Branch NOT re-cut, NOT pushed, NOT merged; no CI triggered; no other session contacted.

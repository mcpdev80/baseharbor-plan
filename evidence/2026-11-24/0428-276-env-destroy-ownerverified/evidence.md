# w67 / 0428-276 — env destroy OwnerVerified genuine re-check

Card: t-20261124-0428-276-env-destroy-ownerverified-nominal (bug, release v0.4.28, repo mcpdev80/baseharbor)
Lane: w67-0428-276-destroyverify
Candidate branch: lane-0428-276-env-destroy-ownerverified
PR: https://github.com/mcpdev80/baseharbor/pull/1824 (ready for review, handed off to CODEX)
Head SHA: bcfb13dc17669a417e3445842273d9589c22434c

## PLAN

1. Read mission + task contract (`scripts/plan.py show`), problem/acceptance noted. — done
2. Verified planning repo remote: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` -> origin https://github.com/mcpdev80/baseharbor-plan.git (push/fetch). The WRONG-ZONE directory workers/baseharbor-plan was never used. — done
3. Claim: coordinator published the claim (planning commit f7d067164, card `active`, owner w67-0428-276-destroyverify) before dispatch; verified in planning git log. — done
4. Base attestation: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> 05ef485369053b732f4b538d7f960275bda48fe9 (matches the mission's stated base 05ef48536). Branch cut exactly there; `git merge-base --is-ancestor 05ef485369... HEAD` -> ANCESTOR_OK. `git log --oneline 05ef48536..HEAD` lists ONLY this lane's commit bcfb13dc1. — done
5. Worktree workers/0428-276-destroyverify-wt (beside the lane dir, per fixed layout); remote guard: `git remote -v` in the shared baseharbor checkout — every remote name (origin/lane-origin/upstream) resolves to https://github.com/mcpdev80/baseharbor.git; push used lane-origin. — done
6. Implementation: `CollectEnvironmentDestroyScope` no longer hardcodes `OwnerVerified: true` (old lines 183-185); the marker now comes from a genuine per-deployment re-check `verifyEnvironmentDestroyDeploymentOwner` -> `verifyDeploymentOwnerAtSeam` -> `VerifyDeploymentOwner`. A failed re-check records a precise `FailClosed` reason and leaves the marker false. Shared `ListDeployments` behavior (`verifyDeploymentOwnerAtSeam` in deployment_list.go/deployment_store.go) unchanged — deployment_store.go appears in no diff (kept byte-identical under the 800-line readability ratchet; the observation seam lives in environment_destroy_scope.go). — done
7. `applyEnvironmentDestroyScope` (cmd/baha/env_destroy.go:264) already gates `!dep.OwnerVerified`; with the genuine marker it now actually fails closed. No guard change needed; a new CLI test pins the gate in both directions. — done
8. Regression tests: 4 new tests in internal/deployment + 1 new test in cmd/baha (see ## tests). — done
9. Push + PR #1824 against develop; delivery witness below. — done
10. Marked PR ready (handoff); monitored both hosted runs to terminal (see ## hosted run). — done
11. Evidence published to origin/main before END. — done (witness in ## evidence delivery)

## diff proof

`git diff 05ef485369053b732f4b538d7f960275bda48fe9...HEAD --name-only`:
- cmd/baha/env_destroy_integration_test.go
- internal/deployment/environment_destroy_scope.go
- internal/deployment/environment_destroy_scope_test.go

`gh pr diff 1824 --name-only` matches; `git apply --check --reverse` of the PR diff onto the candidate proves head == PR content. Write-set respected: no scripts/**, no .github/**, exactly ONE branch/PR for this card.

## push delivery witness

`git ls-remote lane-origin refs/heads/lane-0428-276-env-destroy-ownerverified`:
    bcfb13dc17669a417e3445842273d9589c22434c	refs/heads/lane-0428-276-env-destroy-ownerverified

## what the fix does

- internal/deployment/environment_destroy_scope.go: `OwnerVerified` is set by `verifyEnvironmentDestroyDeploymentOwner(target, deploymentID, &scope)`, which runs the real owner verification seam for THIS deployment identity; failure appends a `FailClosed` reason and returns false. `TestOnlyDeploymentOwnerSeamHook` records (never alters) that the seam really ran; nil outside tests.
- cmd/baha/env_destroy.go: unchanged; the pre-existing guard now actually gates.
- internal/deployment/deployment_list.go: read-only reference; unchanged (contract item 3).

## regression tests -> check -> trigger

- internal/deployment/environment_destroy_scope_test.go (package `deployment`):
  - TestCollectEnvironmentDestroyScopeMarksVerifiedDeployments
  - TestCollectEnvironmentDestroyScopeOwnerReCheckIsGenuine
  - TestCollectEnvironmentDestroyScopeUnverifiedUntilReCheckPasses
  - TestVerifyEnvironmentDestroyDeploymentOwnerMarkerDirect
  -> executed by `go test ./internal/deployment` inside check `deployment-package-tests` (scripts/pr-check-runner.py:176-181 runs the whole package unfiltered and fail-closes on any missing/unpassed test), selected by scripts/pr-gate-plan.py:1617-1621 (area environment-destroy-deployment-scope) + broad `packages` shard of go-unit. Trigger: PR #1824 exact-head "PR Selected Checks".
- cmd/baha/env_destroy_integration_test.go (package `main`):
  - TestApplyEnvironmentDestroyScopeRejectsUnverifiedDeployment (deterministic: no containers, no env; runs in every shard executor)
  -> executed by `cli-package-tests` (scripts/pr-gate-plan.py:114-115) and by the `go-unit-tests` CLI shards cli-0..cli-3 (scripts/pr-go-unit-shard.py; sha256%4 puts this name in cli-3, packages shard also covers ./cmd/baha). Trigger: same PR run.
- Plan artifact (trusted-pr-plan artifact of run 45383351496) confirms routing: reasons include `cmd/baha/env_destroy_integration_test.go: cli-package-tests` and `internal/deployment/environment_destroy_scope.{go,test}: environment-destroy-deployment-scope`; selected_gates: integration/docker/coreless-lifecycle + integration/podman/coreless-lifecycle; coverage_status=resolved; unresolved_coverage=[].

## hosted run (Eigenes-Run-Pflicht)

- Draft-stage run 45382589492 on exact head bcfb13dc1: completed, conclusion success (Draft Go cli-0..3 + Draft Go packages + Draft source and routing all pass).
- Ready PR Selected Checks run 45383351496 on exact head bcfb13dc1 (checkout pull/1824/merge ec2f75a2, integration_sha ec2f75a2 in the plan artifact): completed, conclusion success.
  - Aggregate check "PR Selected Checks": pass — https://github.com/mcpdev80/baseharbor/actions/runs/45383351496/job/138417568782
  - PR · Validation · deployment-package-tests: pass — job 138407944965 (ran `./internal/deployment` full package; fail-closed executor requires every discovered test to run+pass)
  - PR · Go unit · cli-0/1/2/3: pass — e.g. cli-3 job 138407944778 "PASS cli-3: 454 passed / 17 intentionally skipped / 471 discovered; CLI inventory total=1950"
  - PR · Native · native/docker/environment-destroy: pass (TestEnvironmentDestroyNativeLifecycle --- PASS 13.40s, job 138407936974); PR · Native · native/podman/environment-destroy: pass (job 138407937039)
  - PR · Selected Core-less docker+podman coreless-lifecycle (foundation/application/core-capability/identity-backend): all pass — the Docker+Podman data-capabilities cells the resume order asked for
  - PR · Trusted Plan / Native gate plan / Source format / Focused Python / cli-build/gofmt/vet / source-contracts / Demo Pin: pass
  - 74 checks SKIPPING are plan-excluded gates (not required for this diff), none failed; no required check is missing, queued or skipped.
- CI policy note: GitHub Actions job logs truncate the `go test -json` event stream in the "Execute selected Go tests" step (only the PASS summary line is echoed), so per-test names are not greppable in the hosted log; the executors fail closed on any unrun/unpassed test in the selected packages (pr-check-runner.py go_package_tests, pr-go-unit-shard.py missing/incomplete checks), and both new test names are contained in the executed inventories (1950 CLI names; full internal/deployment package).

## local prechecks (allowed subset only)

gofmt clean, `go build ./...`, `go vet ./internal/deployment/ ./cmd/baha/`, `bash scripts/source-readability-audit.sh` (PASS). The one-off focused `go test -v` invocations of the new deterministic test names were run per the TEST RUNNER RULE named form with the RunsRealLifecycle skip set — no full suite, no lifecycle containers started on this host; GitHub-hosted exact-head CI is the acceptance evidence.

## cleanliness

No containers, compose projects, networks or volumes were created by this lane on this host (docker/podman gates ran on GitHub-hosted runners). `docker ps -a` before/after shows no lane-owned additions. VM smoke: not applicable — the mission names no VM smoke test.

## repo-rule compliance

- Hosted-only CI acceptance (Owner 2026-11-23): terminal green exact-head run observed by this session; run ids above.
- No .github/** or scripts/** edits; no reruns/dispatch; no merge (PR left open for CODEX).
- No subagents used (§4.8).
- One PR, one branch, base develop 05ef48536 (ancestor + log-line proofs above).
- Evidence lives only in baseharbor-plan (this file); nothing added to product repos.

## evidence delivery

(witness pasted below after the publish commit.)

### publish witness

    $ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/2026-11-24/0428-276

END_DONE — w67-0428-276-destroyverify: PR #1824 ready, head bcfb13dc1, exact-head run 45383351496 aggregate "PR Selected Checks" pass; handed off for CODEX review.

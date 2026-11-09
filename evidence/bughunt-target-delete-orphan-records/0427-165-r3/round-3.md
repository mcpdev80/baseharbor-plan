# 0427-165 r3 — VM Bughunt Target-Delete Orphan Records, round 3

ROLLE: WORKER (0427-165 r3)
STATUS: DONE (candidate merged into PR #1500; native 172 failures are STATE, not green)

## PLAN

- Reality witnesses via `git ls-remote` for develop, PR #1500 head, and planning origin/main.
- Verify the `baha destroy --all` collector claim against the built develop binary verbatim.
- Fix the blank/whitespace-only identity admission in `CollectableOrphans`.
- Rewrite the recovery guidance to the honest non-collecting path per 0427-173.
- Add regressions (missing + whitespace + mismatch + correct) in go-unit-tests and deployment-package-tests.
- Local build/vet/unit/deployment pass; push to PR #1500; hosted run terminal; ls-remote + evidence.

## Reality witnesses (git ls-remote)

```
20902f0a6ab016fd8fe6a501751e1becc5f334dd	refs/heads/develop
a14cf361d0d6bacfe2a4ab1a963d1a39e676583a	refs/pull/1500/head (r2 candidate, pre-r3)
7cc996e0e95de73c0967ba7a6c7e5b4ff3916fbe	refs/pull/1500/head (post-r3, this round)
7530bc7a9706615abe6d9c4e28c8a266dc223e25	refs/heads/main (baseharbor-plan)
```

PR #1500 candidate branch `0427-165-target-delete-orphanrec` head `a14cf361d` (r2).
My r3 commit `7cc996e0` parent is exactly `a14cf361d` (verified `git rev-parse HEAD^`).
`a14cf361` is an ancestor of the new head `7cc996e0` (verified `git merge-base --is-ancestor`).
Planning origin/main before this evidence commit: `7530bc7a`.

## Repo-rule compliance

- One integration candidate per chain: r3 lands as commits on the existing PR #1500 branch `0427-165-target-delete-orphanrec` (the PR head). No second candidate branch for this card.
- No `.github/**` edits. No workflow_dispatch / rerun authored by me; the hosted run was triggered by the PR push (the standard trigger).
- Evidence file lives only in baseharbor-plan; no `.evidence/` directory in any product repo.
- No subagents used; every step executed in this session.
- Base attested: develop `20902f0a` (r2 was cut from a different base; the r3 net change is applied on top of the PR #1500 head `a14cf361`).

## (1) Recovery guidance — `target_definition_change_plan.go:160/166` (verified against the real command)

Finding. The r2 candidate still advertises, at `cmd/baha/target_definition_change_plan.go:160` and `:166`, that an operator can "collect the records with `baha destroy --all` (which lists them as SKIPPED with their collect reason)" and "collect the orphans with `baha destroy --all`". This is not a supported per-record collector.

Verification against the built develop binary (`20902f0a`, `go build -buildvcs=false -o .baha-r3 ./cmd/baha`):

```
$ .baha-r3 destroy --help
... --all is the explicit installation cleanup path across all Targets;
    it selects owned data and installation state for deletion while preserving
    application source repositories and external application-owned data.
```

The `--all` help text describes installation-wide cleanup of *owned* runtime resources; it names no per-orphan selection and does not collect valid ownerless deployment records. The source independently confirms this: `cmd/baha/runtime_destroy_all.go` `discoverFullDestroyDeployments()` emits `Status: "SKIPPED"` only for records with no usable `deployment.json` (`Diagnostic: "unregistered-deployment-state"`), while valid ownerless records are not targeted by any path — the one-installation-owner seam (`VerifyDeploymentOwner`) fails closed on the ownerless Target, so neither `app destroy --uuid` nor `destroy --all` reaches them. Until a supported per-record recovery exists or the source repo is restored, no supported command collects these individual ownerless records.

Fix. Rewrote both the message (`:160`) and the `Next` hint (`:166`) to state the honest contract: until `0427-173` provides a supported per-record recovery (or the source repository is restored), no supported command collects these individual ownerless records; the operator must keep the Target definition attached for operator recovery and let `baha app destroy` run normally. The `--all` mention is now factual ("selects owned runtime resources and skips unregistered deployment state") rather than a collector route.

Honest answer (until the `0427-173` prune card, which is running): destroying the individual orphaned deployment record is not currently recoverable via any supported command; keep the Target attached for operator recovery, restore it, and run `baha app destroy` normally.

## (2) Blank/whitespace-only identity admission — `deployment_list.go:171-177`

Finding. The r2 decode-uuid fix rejected only *non-empty* mismatches:

```go
if record.Identity.DeploymentID != "" && strings.TrimSpace(record.Identity.DeploymentID) != strings.TrimSpace(deploymentID) {
    continue
}
if record.Identity.Target != "" && strings.TrimSpace(record.Identity.Target) != strings.TrimSpace(target) {
    continue
}
```

A record with a missing or whitespace-only `DeploymentID` or `Target` short-circuits the `!= ""` guard and is appended at line 177 even though it does not equal its canonical folder/target identity — i.e. it is advertised as collectable, contradicting the fail-closed contract.

Fix. Changed both checks to require exact canonical equality and exclude any blank field:

```go
if record.Identity.DeploymentID == "" || strings.TrimSpace(record.Identity.DeploymentID) != deploymentID {
    continue
}
if record.Identity.Target == "" || strings.TrimSpace(record.Identity.Target) != target {
    continue
}
```

A blank/whitespace-only field now fails exactly — it cannot prove its identity equals the folder/target name. Fail-closed on the ownerless Target is preserved (the owner-missing guard still fires on the directory); no malformed or blank record is ever listed as collectable. The `CollectableOrphans` doc comment and inline note were updated to state the exact-canonical-equality rule.

## (3) Regression tests (go-unit-tests + deployment-package-tests)

Both packages execute in the hosted `PR Selected Checks` / `go-unit-tests` / `deployment-package-tests` jobs on the exact head.

- `internal/deployment/collectable_orphans_test.go`: `seedBlankIdentityOrphan` plus `TestCollectableOrphansRejectsBlankDeploymentID` and `TestCollectableOrphansRejectsBlankTarget` (blank DeploymentID / blank Target → `len(orphans) == 0`).
- `cmd/baha/target_definition_orphan_refusal_test.go`: `seedBlankIdentityOrphan` plus `TestTargetDeleteRefusalIgnoresBlankIdentity` — blank-identity record is not collectable (`len(orphans) == 0`), the ownerless Target still refuses, and the refusal is never surfaced as `target_definition_collectable_orphans` cause.

Local results on `7cc996e0`:

```
$ go test ./internal/deployment/ -run 'CollectableOrphans'   -> ok (7/7 PASS incl. the 2 new blank tests)
$ go test ./cmd/baha/ -run 'TestTargetDelete'                -> ok (6/6 PASS incl. TestTargetDeleteRefusalIgnoresBlankIdentity)
$ go vet ./internal/deployment/ ./cmd/baha/                  -> clean
$ go build -buildvcs=false -o .baha-r3 ./cmd/baha            -> clean
```

## Hosted CI (run by PR push, standard trigger)

Run `42539114216` "CI · PR #1500", head `7cc996e0e9`, terminal `failure` at 2026-11-09T00:24:30Z.

Passing (relevant to this round): `PR Selected Checks` (aggregate) = success; `go-unit-tests` = success; `deployment-package-tests` = success; `go-build`, `go-vet`, `cli-gofmt` = success; `Native destroy retry · docker` and `. · podman` = success.

STATE (red, 0427-172, not introduced by r3): `Native Keycloak/Core · docker` (job 128909945122) and `. · podman` (job 128909945199) failed; the aggregate `PR Selected Checks` carries that failure. The failing test is `TestControlPlaneSingleDefaultNativeRuntimeInCI` (`cmd/baha/control_plane_single_native_ci_test.go:18`). This is the owner-documented 0427-172 parked-state native failure — the same job names failed on the parent candidate in the r2 review. Classified STATE, not counted as green, not assigned as an r3 defect. Native jobs are GitHub-hosted shared runners only; runner infrastructure was not built, registered, or repaired.

No `.github/**` change was made (Owner scope). If a CI group must pick up a new test, the needed change is a finding, not an edit here.

## Cleanliness / provenance

`git log --oneline 20902f0a..HEAD` lists only `7cc996e0` (my commit). The r3 diff vs the r2 PR head touches exactly four files (`target_definition_change_plan.go`, `deployment_list.go`, `collectable_orphans_test.go`, `target_definition_orphan_refusal_test.go`) — 167 insertions / 17 deletions, no stray files. No foreign commit carried on top.

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git 2>&1 | grep 0427-165-target-delete-orphanrec
7cc996e0e95de73c0967ba7a6c7e5b4ff3916fbe	refs/heads/0427-165-target-delete-orphanrec
```

## END

END_DONE mission-165-r3: DONE — blank-identity admission fixed (exact canonical equality), recovery guidance rewritten to the honest non-collecting path per 0427-173, blank/mismatch/correct regressions added and passing in go-unit-tests + deployment-package-tests, r3 landed on PR #1500 head `7cc996e0`. Hosted run 42539114216 terminal: r3-relevant jobs green; native 172 Keycloak/Core docker+podman + aggregate red = STATE (not green). Evidence on baseharbor-plan main before END.

# PR #1578 Review R4 — CLI2 UID environment

ROLE: CODEX-REVIEW (no merge).

## PLAN

1. Verify exact PR #1578 refs, candidate ancestry/log and PR metadata; inspect both specified run witnesses.
2. Reconcile each of the four r2 findings against the exact b71f64e19 content and current source/tests.
3. Separate candidate-content verdict from Q-CIFIRE/Q-RUNTIME environment failures and verify test/CLI entrypoint evidence.
4. Write verdict and correction recipe, validate and publish evidence on planning origin/main, verify remote evidence, and post END.

## Candidate and provenance

The mission-selected candidate is PR #1578 head `e3d627d7d6815093ab6c96e87cab41ca19e59052`, branch `lane-0428-uid-environment`, base branch `lane-0428-uid-app`. PR metadata from `gh pr view 1578 --json number,state,isDraft,baseRefName,headRefName,headRefOid,commits` reports OPEN, DRAFT, the stated base/head branches, and the exact head SHA above.

The required planning repository root witness is exactly:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

Planning remote main witness before publishing this evidence (`git ls-remote origin refs/heads/main`):

```text
b42a8477c63ed50caacf280f1afd587e411172b5	refs/heads/main
```

Product remote witness (`git ls-remote`, fetched directly):

```text
2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9	refs/heads/lane-0428-uid-app
e3d627d7d6815093ab6c96e87cab41ca19e59052	refs/heads/lane-0428-uid-environment
e3d627d7d6815093ab6c96e87cab41ca19e59052	refs/pull/1578/head
```

The exact candidate content at `e3d627d7` equals the r3 content at `b71f64e19601a1b312b1166597848274f8773592` (`git diff --exit-code b71f64e..e3d627d` returned 0); the two commits on top are empty retrigger commits. `git log --format='%H %s' 2bf0c929506a5b0e64b7359a6fc8711ab3f48526..e3d627d7d6815093ab6c96e87cab41ca19e59052` lists only task commits plus the two explicitly empty retriggers:

```text
e3d627d7d6815093ab6c96e87cab41ca19e59052 chore: re-trigger CI on b71f64e19 lineage
15fb77be6630195f9cd2305ad4315bb7a612fff9 chore: re-trigger CI on b71f64e19 lineage
b71f64e19601a1b312b1166597848274f8773592 fix(r3): PR #1578 r2 correction — rebase onto app base + 4 findings
94937e885a4cb926d70a4a5f2eb85624242ccbd4 fix(r2): durable env identity — stable rename, distinct name/uid, real CLI entry
0d9e9387a2171c4c7322a68e706078338899e1a1 feat(environment): durable non-secret env identity per (target,env)
```

Historical app-base attestation from the r3 correction: `2bf0c929506a5b0e64b7359a6fc8711ab3f48526` is an ancestor of `b71f64e` and current candidate `e3d627d`. The live app branch has since advanced to `2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9`; that current base SHA is not an ancestor of `e3d627d` (merge-base ancestry check exit 1). Thus the r3 ancestry correction was true for the exact base at its cut, but this candidate is not rebased on the present base tip.

## Review findings

Verdict: REJECT. Findings 1–3 below are candidate-content defects or unmet acceptance evidence, independent of the infrastructure-gated CI state.

1. The requested “field in existing state” design is not demonstrated. `internal/deployment/environment_identity.go:15-18,26-40,42-64` introduces a new identity-only `environment.json` record and a new per-target environment directory as the source of truth. In the historical app-base tree, `internal/application/environment.go:207-212` resolves environment state per repository under `.baseharbor/environments/<name>`; it does not define the new target-wide identity record. The implementation comments assert this is existing per-Target deployment state, but the persisted record shape contains only target/name/id and is not an added field in an existing state record. Resolve this by persisting the ID as a field in the already-authoritative shared environment state object, with a migration/reuse path for that state; do not add a parallel identity-only store.

2. The rename regression does not use the CLI entrypoint for the rename mutation. `cmd/baha/environment_identity_cli_test.go:69-132` runs create/reopen and post-rename reads through `runWithIO`/`target show`, but lines 114-120 directly call `deployment.RenameEnvironment`. There is no production CLI command invoking that mutation. The test therefore proves the getter output around a direct seam call, not a real CLI rename path. Add a CLI command that performs the intended rename (or test the actual existing command that does so), then drive rename, reopen, and assertions through `runWithIO`.

3. A destination binding mismatch can be overwritten during rename. In `internal/deployment/environment_identity.go:329-336`, the pre-lock guard explicitly ignores `ErrEnvironmentBindingMismatch`; with the source still present, the locked branch does not re-read the destination, and lines 402-425 write it with `os.Rename`, which replaces the existing file on the supported Unix path. This can clobber a valid foreign `(target,name)` record despite the fail-closed rule. Always reject a destination binding mismatch and revalidate destination under the write lock immediately before replacement; use a no-replace install or equivalent so a race cannot overwrite a newly created destination. Add tests for a mismatched destination binding and for a destination appearing between precheck and locked install.

4. The rename operation is not idempotent when the same rename request is retried after a successful rename. `RenameEnvironment(target, oldName, newName)` creates/gets a fresh source identity when `oldName` is absent, then sees the existing destination identity differs and returns `ErrEnvironmentAlreadyExists`; the concurrent convergence test only covers overlapping callers. `internal/deployment/environment_identity_test.go:278-298` named idempotency coverage only reopens `newName` with `GetEnvironment`, it does not retry `RenameEnvironment`. On missing source, recognize a destination record whose binding and authoritative identity prove the requested rename already completed, and return that record; do not allocate a replacement source. Add a sequential same-request retry assertion preserving the original UUID.

## CI and run witnesses

The specified workflow-dispatch run witnesses are:

```text
{"conclusion":"failure","databaseId":43658208331,"event":"workflow_dispatch","headSha":"b71f64e19601a1b312b1166597848274f8773592","status":"completed","workflowName":"CI · Source & Quality"}
{"conclusion":"failure","databaseId":43659613732,"event":"workflow_dispatch","headSha":"18b0ebc9d0d99c634a3c8b74b571a8074ce0393d","status":"completed","workflowName":"CI · Source & Quality"}
```

Both failed in `validate`, in `Run runtime integration tests serially`, with the same unrelated runtime-environment failures documented in `evidence/r28-welle1-2026-11-14/cli2-uid-environment/round-4.md`: `TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI` reports `ORAS is required before Core setup`; `TestMultiInstanceComposeLifecycleInCI` reports `postgres-analytics runs as root (Config.User="")`; `TestRepositoryWorkflowRealLifecycle` also fails. The r3 candidate run and pure-base run have the same failure class. Classify these as Q-CIFIRE/Q-RUNTIME; they are not evidence against this candidate. The pull-request suite is structurally not selected for this PR base according to the round-4 workflow analysis. Workflow files are Owner scope, so no workflow was edited and no rerun/dispatch was triggered by this review.

No tests were run in this read-only review. New regression tests requested above must be picked up by the existing GitHub CI group for `cmd/baha` and `internal/deployment` under its applicable trigger; if the current workflow selection excludes this PR base, Owner action is required to add the trigger/selection. This review did not modify `.github/**`.

## repo-rule compliance

Read-only review in a fresh clone of the exact PR head. No product files, workflow files, or PR metadata were changed; no product tests, containers, or VM smoke tests were run. Evidence is stored only in the actual `baseharbor-plan` repository. The live base advance is reported as state, not silently incorporated into the candidate.

END mission-rev1578-r4.md DONE — REJECT with four actionable findings; candidate reviewed: `e3d627d7d6815093ab6c96e87cab41ca19e59052`.

# CODEX-REVIEW 0427-117 / PR #1419 rereview r5

Candidate: `438895466eed1838bd50f3f9838184e4b7d7ebc1` against `develop`.

## PLAN

1. Read the mission and confirm fresh exact develop and PR head SHAs.
2. Inspect the new correction against the prior owner-resolution finding.
3. Verify behavioral regression, fail-closed cases, and exact-head CI witnesses.
4. Write the exact-head review verdict and actionable findings in planning evidence.
5. Publish evidence to planning origin/main, verify its remote tree entry, and post END.

## Planning repository and provenance witnesses

The planning checkout is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `git rev-parse --show-toplevel` returned exactly that path. Exact `git remote -v` output:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

The required r5 evidence file `evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-5.md` is present in freshly fetched `origin/main` at commit `7bb2d99d75e8ad14276e6b4ca4ff4ec6e2ffa691`; commit `20e80c39` is an ancestor of that main head (rc 0). The exact remote tree line is recorded here:

```text
100644 blob f9bc75d80f70dde2984171e0e8ddae3f3f0e1a10	evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-5.md
```

Fresh product `git ls-remote` witness:

```text
eee11d50b7a7b55675a282f03d4a1a78e4511cf0	refs/heads/develop
438895466eed1838bd50f3f9838184e4b7d7ebc1	refs/pull/1419/head
```

The base is an ancestor of the exact candidate (`git merge-base --is-ancestor eee11d50... 43889546...` returned `base_ancestor_rc=0`). The exact base-to-head diff is six Go files and contains no `.github/**` changes. The commit range from prior reviewed head `c0ac3bef9e61b255b2fce97874ea7f4102ee6ce5` to this candidate lists one commit only:

```text
43889546 fix(cli,deployment): resolve podman-family deployment owner for authorized remote up path (card 0427-117)
```

PR #1419 remains open, non-draft, targets `develop`, and reports mergeable. No review threads are open.

## Production owner resolution and fail-closed review

The implementation now does use an ungated production owner path. `recordDeploymentBeforeMutation` sets the actual command context and calls `deployment.VerifyDeploymentOwner` at `cmd/baha/deployment_record.go:394-415`. The verifier is bound to `productionLoanAuthorityForTarget` at lines 219-245. That function has no `testing.Testing()` or marker gate; it requires a local-access target, rejects connector/remote management authority, selects a genuine READY boot Core, and requires that Core to own the selected boot target (`cmd/baha/deployment_record.go:147-216`). `bahaEffectiveBootTargetName` checks `BASEHARBOR_TARGET` before persisted/default/single-target fallback (`cmd/baha/deployment_record.go:328-360`). Ownerless or invalid boot state is rejected, and the existing verifier preserves the `ErrDeploymentOwnerMissing` sentinel on refusal.

Fail-closed behavior is preserved in the implementation: non-local/connector access is rejected at `cmd/baha/deployment_record.go:151-167`; absent, non-genuine, non-READY, or wrongly owned boot installations are rejected at lines 176-192. The new connector and unmarked negative regression cases expect the original missing-owner sentinel (`cmd/baha/deployment_owner_loan_regression_test.go:324-365`).

## Blocking review finding

`REJECT_LANE_FIX` — the mission requires the positive regression to drive a real local CLI apply, but the new positive test still calls a direct seam helper.

`TestProductionOwnerLoanLocalIsolatedApplyPasses` at `cmd/baha/deployment_owner_loan_regression_test.go:285-322` calls `saveThroughApplySeam` at line 302. That helper is defined at lines 158-173 and directly calls `deployment.VerifyDeploymentOwner` followed by `deployment.SaveDeploymentRecord`; it does not call `recordDeploymentBeforeMutation`, construct/run the CLI apply command, or set the apply command context through `setLoanExecutionContext`. Thus the test proves the owner-verifier function can resolve a local boot installation in an ungated Go test, but it does not prove a real `baha app apply` executes the owner loan using its effective target and command context. Its setup uses the config default and does not explicitly exercise `BASEHARBOR_TARGET` precedence.

The r5 evidence claims the test drives the exact production apply path, but the source of the helper disproves that claim. The stored red/green note describes a seam-level test on the stashed base and candidate; it does not convert the current positive test into the required CLI-path regression.

Actionable correction: change the positive regression to invoke the actual CLI `app apply` command (or its production command runner) with an isolated local Podman target and READY boot Core, exercising normal effective-target resolution and the real context passed into `recordDeploymentBeforeMutation`. Assert that apply succeeds and writes a resolvable deployment owner record. Run that same test on the prior base and record the verbatim `ErrDeploymentOwnerMissing` failure; retain the connector-bound and ownerless fail-closed cases. The correction belongs in `cmd/baha/deployment_owner_loan_regression_test.go`; no workflow change is implicated.

## CI witnesses

GitHub Actions run 4989 (`42347954867`) is terminal success for exact head `438895466eed1838bd50f3f9838184e4b7d7ebc1`. `PR · Validation · cli-package-tests` job `128329739049` succeeded; its log reports `matched_tests: ["./cmd/baha"]`, so the added tests are in the durable PR package check. `PR Selected Checks` job `128331184076` succeeded with GitHub Actions integration ID 15368. CLI build, gofmt, vet, deployment-package tests, source contracts, source format, trusted plan, focused Python, workflow policy and selected checks succeeded.

`Targeted HA · docker` job `128329701079`, `Targeted HA · podman` job `128329701009`, and `Release Source Preflight` job `128329701219` were skipped by the owner-scoped push-ref gate. Per this mission those skips are `runtime_cells=owner-gate`, not a lane-fix rejection reason. No workflow was edited or rerun.

## repo-rule compliance

Read-only review. No product files or workflows were changed, no local tests were run, no VM/container was started, and no merge was performed. No subagents were used. Evidence is stored only in the genuine `baseharbor-plan` repository.

END_DONE codex-1419-rereview-c: verdict REJECT_LANE_FIX; production owner path is ungated and fail-closed, but the required positive regression still bypasses the actual CLI apply path; candidate 438895466eed1838bd50f3f9838184e4b7d7ebc1.

Exact planning `origin/main` witness after `git pull --rebase origin main` and before publishing this evidence:

```text
e30c7c003143c1aa8b1bb89ebd450fa4e250a396\trefs/heads/main
```

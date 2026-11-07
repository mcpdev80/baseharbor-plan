# CODEX-REVIEW 0427-117 / PR #1419 rereview

Candidate: `c0ac3bef9e61b255b2fce97874ea7f4102ee6ce5` against `develop`.

## PLAN

1. Read the review mission and verify exact fresh remote head and base SHAs.
2. Inspect exact candidate diff and map each mission finding to code and regression coverage.
3. Review prior evidence, exact-head CI and any owner-scoped skipped checks.
4. Record SHA-specific verdict and repository-rule compliance in planning evidence.
5. Publish evidence on planning origin/main, verify the remote path, and post END.

## Planning repository and source witnesses

The planning repository is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `git rev-parse --show-toplevel` returned exactly that path. Exact `git remote -v` output:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

The round-3 implementation evidence is present on freshly fetched `origin/main` at `a57fb1401ecdacb84b0a89d4baf9d748475bc6a8`:

```text
100644 blob 9d462e0bb8b1b97f61f86e6eda3e44a468bc97ad	evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-3.md
```

Fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1419/head`:

```text
eee11d50b7a7b55675a282f03d4a1a78e4511cf0	refs/heads/develop
c0ac3bef9e61b255b2fce97874ea7f4102ee6ce5	refs/pull/1419/head
```

The accepted base is an ancestor of the exact candidate (`git merge-base --is-ancestor eee11d50... c0ac3bef...` returned `base_ancestor_rc=0`). Exact diff against that base has six files: the new regression test and five Go source/test files; no workflow files changed. The PR is open, non-draft, targets `develop`, and GitHub reports mergeable. No review threads are open.

## Owner-resolution finding

`REJECT_LANE_FIX` — the owner-loan implementation is explicitly restricted to test processes, so it does not resolve the production Podman apply path described by the mission.

In `cmd/baha/deployment_record.go:57-65`, the bound `TargetLoanVerifier` is documented as test-scope only. The verifier rejects any non-test process at lines 133-135 and rejects startup-bound non-local management authority at lines 136-142. The process provenance helper at lines 356-365 returns false in a production binary because `bahaTestProcessEnv` defaults to nil; only `cmd/baha/test_isolation_support_test.go:7-14` binds it to `testing.Testing`.

The active-target-first helper at `cmd/baha/deployment_record.go:321-353` is only used by that test-scope loan. When `BASEHARBOR_TARGET` selects the requested isolated target, the helper returns that target; `bahaTestBootRuntimeRoot` then rejects the same name as the boot owner at lines 305-308. The positive regression does not set `BASEHARBOR_TARGET`; it uses a local-access config whose default target is the boot target (`cmd/baha/deployment_owner_loan_regression_test.go:95-125,138-155`).

`TestPodmanOwnerLoanIsolatedApplyPasses` does not execute the CLI apply command. Its `saveThroughApplySeam` helper at `cmd/baha/deployment_owner_loan_regression_test.go:158-173` directly calls `deployment.VerifyDeploymentOwner` and `deployment.SaveDeploymentRecord`. The connector-bound case at lines 230-259 explicitly expects the owner loan to fail closed with `ErrDeploymentOwnerMissing`. This is seam-level test behavior, not proof that a remote Podman `app apply` uses a real boot-owner context.

The prior round-3 evidence's Podman live witness section reports that manual `baha app up` on `baha-podman-2` still stops with `ErrDeploymentOwnerMissing` when the isolated target has no boot Core owner. That is the same unresolved product behavior; a test-only hook does not make it pass. The card acceptance requires the same-scenario Podman `app up` and healthy `doctor` result.

Actionable correction: resolve the genuine owner from the actual effective CLI/apply target context in the production `recordDeploymentBeforeMutation` path, retaining fail-closed tenant/connector checks without gating the successful owner path on `testing.Testing()` or a test-only marker. Update the regression to invoke the real remote-Podman apply orchestration with the effective `BASEHARBOR_TARGET` and connector/management context, then assert the owner record is saved and `doctor` is healthy; retain negative connector/foreign-owner refusals. Required behavior should fail on the broken candidate and pass on the corrected candidate.

The round-3 evidence narrative claims red-without-fix and green-with-fix, but does not include literal command output or exit codes for that pair. The exact-head CI package test is green; that does not demonstrate the missing production path.

## CI witnesses

GitHub Actions run `42342771963` (run number 4987) is terminal success at the exact head `c0ac3bef9e61b255b2fce97874ea7f4102ee6ce5`. `PR Selected Checks` job `128315595857` succeeded, and its check-run app integration ID is 15368. `PR · Validation · cli-package-tests` job `128313948187` succeeded; the log records `matched_tests: ["./cmd/baha"]`, which discovers the added regression in that package. CLI build, gofmt, vet, source contracts, deployment package tests, source format, trusted plan, focused Python, workflow policy and selected checks succeeded.

`Targeted HA · docker` (`128313901403`), `Targeted HA · podman` (`128313924845`) and `Release Source Preflight` (`128313900956`) were skipped by owner-scoped push-ref gates. This is recorded as `runtime_cells=owner-gate`; no workflow file was edited and no rerun or workflow dispatch was triggered. These skips are not the reason for rejection; the production owner-resolution behavior remains unfixed.

## repo-rule compliance

Read-only review only. No product files or workflows were changed, no tests were run locally, no VM/container was started, and no merge was performed. No subagents were used. Evidence is stored only in the real baseharbor-plan repository.

END_DONE codex-1419-rereview-b: verdict REJECT_LANE_FIX; production Podman apply owner resolution remains test-scope-only; candidate c0ac3bef9e61b255b2fce97874ea7f4102ee6ce5.

Exact `origin/main` witness after `git pull --rebase origin main` and before this evidence commit:

```text
a57fb1401ecdacb84b0a89d4baf9d748475bc6a8\trefs/heads/main
```

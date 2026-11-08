# CODEX-REVIEW 0427-128 r3 — PR #1452

## PLAN

1. Compare the r3 source delta with the four r2 findings and the task's acceptance criteria.
2. Verify the PR head, current develop head, ancestry, file set, and exact-head hosted run from GitHub.
3. Inspect production stop, retirement, control-plane paths, pinned-name regressions, and CI selection for the new integration test.
4. Record the verdict and actionable correction recipe in this Planning evidence file.
5. Publish the review act on baseharbor-plan origin/main and verify its remote tree entry.

## Candidate and witnesses

- Repository: `mcpdev80/baseharbor`, PR #1452, open and mergeable.
- Exact candidate: `54a6fd11dd639062e537a44815f25a80c3c4b8b2`, confirmed by `gh pr view` and `git ls-remote refs/pull/1452/head`.
- Exact current base: `develop` at `07ae6c3e91b081a189266ca4b162ba705d4aa78f`; confirmed by `git ls-remote`. `git merge-base --is-ancestor origin/develop origin/pr/1452` returned 0.
- Exact-head CI: run `42450415960` completed with success on the candidate SHA. `PR Selected Checks` passed from GitHub Actions app 15368. `go-unit-tests`, build, vet, source format, CLI gofmt, runtime-provider-package-tests, and workflow policy passed. `Targeted HA · docker` and `Targeted HA · podman` were skipped.
- PR file list contains ten product files under `cmd/baha` and `internal/runtime`; no workflow file changed.
- Planning repository: `/tmp/opencode/0427-128-r3-plan-wt`, with fetch and push remote `https://github.com/mcpdev80/baseharbor-plan.git`. Base before this evidence commit: `08574554aee843b60ff9fc114899aeae6b3bae72`.

## Review of the r2 findings

The production interface signature is now compatible with the real Compose config-render method (`internal/runtime/container_identity.go:25`, production implementation `internal/runtime/compose_files.go:65`). The selected-stop entry path renders the Compose model and accepts planned names (`internal/runtime/service_stop.go:79-92`), and `cmd/baha/app_workload.go:653-659` adds pinned names to the inspected resource inventory. The parser covers pinned, default single-replica, and `deploy.replicas` names.

The remaining r2 findings are not fixed end-to-end:

- Cross-project pinned-name coverage is still missing. `internal/runtime/container_identity_test.go:8-25` tests the foreign-project case using the canonical `owned-keycloak-db-0-1` name. The new parser tests only derive names; the pinned lifecycle test checks an owned project's pinned name. There is no negative test proving `ContainerNameInPlannedSet` rejects a foreign project carrying the exact same pinned name and service.
- Retirement still rejects pinned names. `internal/runtime/service_retirement.go:35-39` requires removal resources to end in `-1`, and `:66-69` still calls `ContainerMatchesProjectResource` with only the canonical ordinal name. The r3 source change at `:62-65` is explanatory comment only; it does not pass or use a rendered planned-name set. A pinned container therefore remains an unplanned replica and retirement cannot complete.
- Control-plane observation still rejects pinned names before reaching the new render logic. `cmd/baha/control_plane_stop_observation.go:48-50` returns `runtimeMutationOwnerError()` through the old canonical matcher. The added planned-set handling at `:67-91` appears after this early return and cannot admit a pinned container.
- Selected-stop postcondition still uses the old identity contract. `internal/runtime/service_stop.go:143-146` validates every remaining selected process with `ContainerMatchesProjectResource`, so a stopped pinned container still produces `unexpected-or-running-selected-process`. The removed-resource path at `:123-133` likewise recognizes only the canonical `-1` resource.

## CI coverage finding

`cmd/baha/app_workload_integration_test.go:338-340` gates `TestRepositoryComposePinnedWorkloadLifecycleInCI` on `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`. The selected runtime integration command in `.github/workflows/ci.yml:349` does not include that test in its `-run` expression. The ordinary `go test ./...` unit job does not set the gate variable, so the test is skipped there. The exact-head run `42450415960` also skipped the Docker and Podman HA cells. Thus the green PR run does not execute the new pinned backup/down/up/destroy acceptance.

This workflow selection is Owner-owned. The required Owner change is to include `TestRepositoryComposePinnedWorkloadLifecycleInCI` in the runtime-integration selection at `.github/workflows/ci.yml:349` with the intended PR/path trigger. This review did not edit `.github/**`, dispatch a workflow, or request a rerun.

## Verdict: REQUEST-CHANGES

The parser and initial stop-path changes are useful, but three production readers still use the canonical-only matcher, and the exact-head hosted run does not execute the newly added native acceptance. The r2 stop criteria are therefore not met.

## Correction recipe

- `internal/runtime/service_stop.go:79-92,123-168`: compute the validated planned set once with the actual Compose render inputs and use it for both initial process validation and post-stop verification. Handle pinned-resource disappearance as a selected process result while preserving exact project/service ownership and retained-resource checks.
- `internal/runtime/service_retirement.go:35-39,66-77`: carry the rendered per-service planned names and service association into retirement. Remove the assumption that every selected container resource ends in `-1`; require the project and service labels plus exact planned native name before mutation. Keep volume/network deletion outside this path.
- `cmd/baha/control_plane_stop_observation.go:43-50,67-91`: replace the early canonical-only rejection with the same rendered-set check; do not leave the new check after an unconditional canonical guard. Fail closed if the required owner/render cannot be verified.
- `internal/runtime/container_identity_test.go`, `internal/runtime/service_stop_test.go`, retirement tests, and control-plane tests: cover pinned and default names through production callers, prove an exact pinned name under a foreign project is rejected, and prove pinned stop/retirement postconditions succeed only for the expected project/service.
- `.github/workflows/ci.yml:349` (Owner scope): add `TestRepositoryComposePinnedWorkloadLifecycleInCI` to the runtime-integration `-run` selection. Then require an exact-head hosted run in which that test executes and passes, in addition to the existing unit suite. Preserve the test's `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` gate.
- Stop criterion: do not approve until retirement, control-plane observation, selected-stop postconditions, and cross-project pinned identity are covered on production paths; the pinned lifecycle test is selected by GitHub CI and executes successfully on the exact candidate; required checks remain green.

## Repo-rule compliance

- Review-only: no product files were modified, no tests were launched, and no workflow was edited or dispatched.
- Evidence is stored only under `baseharbor-plan/evidence/r27-welle5-folge-2026-11-08/bughunt-container-name-replica/act-1452-review-r3.md`.
- No Markdown checkbox task lines are present in this evidence file.

END_DONE 0427-128-review-r3: REQUEST-CHANGES for PR #1452 head 54a6fd11dd639062e537a44815f25a80c3c4b8b2; production identity paths and CI selection remain incomplete.

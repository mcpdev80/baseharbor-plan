# CODEX-REVIEW 0427-175 — PR #1512

ROLLE: REVIEW

URTEIL: KORREKTUR

## PLAN

1. Verify the live PR head, current develop head, candidate ancestry, and terminal exact-head CI state.
2. Inspect the concurrent-registration reproduction, production lock/write path, and incomplete-record behavior.
3. Record the verdict and actionable correction recipe in this planning evidence file.
4. Publish the evidence to canonical baseharbor-plan main and verify the remote file witness.

## Candidate and base drift

Repository: mcpdev80/baseharbor; PR #1512; task 0427-175.

- Live PR head: f32f35576379eeb961bfb292a5b003be3a1dff3f.
- PR API base SHA: 942111d5a1c43f5257bf1627a966fa9e6c6f24bd.
- Current origin/develop: e072e142ec9511f3cc86ffa67c7debd022d7760a.
- Candidate commit parent: b3a8042d18ea60f162a32a51df34a499cad6a237.
- Current develop is four commits ahead of the candidate's base; `git rev-list --left-right --count origin/develop...origin/pr1512` returns `4 1`. The intervening develop commits include #1502, #1504, #1506 and #1505. The candidate is not based on current develop and needs base refresh and exact-head revalidation before landing.
- Live PR and branch refs agree on f32f35576379eeb961bfb292a5b003be3a1dff3f.

## Concurrency and production write path

The eight-goroutine test `TestConcurrentInitNeverCreatesDoubleApplicationIDRegistration` in cmd/baha/app_init_concurrent_race_test.go:24-80 launches multiple writers but has no explicit start barrier; by itself it would not prove a forced overlap.

The separate `TestConcurrentInitAcrossRealProcessesIsSerializedOrRefused` at cmd/baha/app_init_concurrent_race_test.go:91-177 does prove real overlap. The first process enters `SaveDeploymentRecord`, holds the registry lock, signals the parked marker, and waits for release at lines 104-120. Only after that signal does the parent start the re-exec child at lines 135-150. The parent waits for the child's `CombinedOutput` before releasing the first process at line 151, so the child attempts the same registration seam while the first lock is held. The final registry count must remain one at lines 164-175. Child dispatch reaches the same production storage seam through TestMain at cmd/baha/runtime_integration_test_support_test.go:77-84.

This is a real two-OS-process test of the race window, not a sequential before/after test. It directly exercises the storage seam rather than invoking the full CLI process twice; the production app-init path calls `deployment.SaveDeploymentRecord` at cmd/baha/app.go:118, so the synchronization point under test is the shared production registration seam.

In production, `SaveDeploymentRecord` performs the first-claim check and wraps `saveDeploymentRecord` in `WithDeploymentRegistryWriteLock` at internal/deployment/deployment_store.go:365-397. The lock wraps duplicate scans and record creation; the registry lock is target-scoped in internal/deployment/registry_lock.go:38-59. Thus first registration is guarded at the actual writer, not only in test code.

## Half-created state

The persistence path writes a PID-named temporary record and atomically renames it to deployment.json at internal/deployment/deployment_store.go:570-588. A deployment directory that exists without deployment.json is reported as an `incomplete` state by internal/deployment/deployment_list.go:66-87; non-best-effort listing returns the error, causing the duplicate scan to fail closed rather than treating the incomplete directory as an empty registry. `TestLoadDeploymentRecordClassifiesMissingState` at internal/deployment/target_test.go:123-153 asserts that a directory without a record is classified as incomplete and carries no invented application identity.

The code and existing incomplete-state regression support the fail-closed behavior for a half-created directory. The new cross-process test does not inject a crash between directory creation and atomic rename, so the combined interrupted-write-plus-competing-registration interleaving is not directly demonstrated. Adding that targeted regression would make this edge durable; it is not evidence that the current code accepts a duplicate.

## Exact-head hosted CI

Run 42593160991 is terminal `completed/failure` on the exact head f32f35576379eeb961bfb292a5b003be3a1dff3f, with `pull_request` event. Evidence: [hosted run 42593160991](https://github.com/mcpdev80/baseharbor/actions/runs/42593160991).

Blocking jobs and exact log findings:

- `PR · Source format` failed: `source readability: internal/deployment/deployment_store.go has 836 lines (limit: 800; baseline ratchet: 0)`; the step exited 1.
- `PR · Validation · go-unit-tests` failed: `--- FAIL: TestResolveRegisteredApplicationPropagatesOwnerStateNotNotFound`; `app_context_owner_state_test.go:62: expected an owner-state error for a malformed Core installation`.
- `PR Selected Checks` failed and logged `BLOCKED: required job did not succeed: pr_validations` and `BLOCKED: workflow job did not succeed: source_format`.

Other reported executed validation jobs passed, including deployment-package-tests, authority-package-tests, build, vet and CLI gofmt. Native destroy-retry Docker and Podman passed. Native Keycloak/Core and Targeted HA Docker/Podman were skipped; skips are not counted as passes. The run is red overall, so the candidate is not acceptable regardless of the passing concurrency tests.

## Actionable correction recipe

- Split the added registry/write helpers out of internal/deployment/deployment_store.go into focused source files so the existing readability audit passes with the file at or below its 800-line limit. Do not weaken or change the audit.
- Reproduce and resolve `TestResolveRegisteredApplicationPropagatesOwnerStateNotNotFound` at cmd/baha/app_context_owner_state_test.go:62. If it is claimed to be pre-existing, establish that with the same test and conditions on a clean current-develop baseline; otherwise fix the regression. Do not treat the red go-unit-tests job as green.
- Refresh the candidate onto current develop e072e142ec9511f3cc86ffa67c7debd022d7760a and verify the merge base and changed-file scope.
- Add a targeted interrupted-registration regression that leaves a deployment directory without deployment.json while a distinct first registration with the same application_id is attempted; assert the incomplete state is surfaced and no second record is written. Keep the current two-process overlap test.
- Observe a new terminal run on the refreshed exact PR head. Stop only when the source-format job, go-unit-tests, PR Selected Checks, and all other required checks are terminal-success. Report skipped native cells as skipped, not green.

## repo-rule compliance

- Product source, refs, and CI were read-only; no tests or workflow reruns were started.
- No `.github/**` files were changed.
- Evidence is in canonical baseharbor-plan, whose origin is https://github.com/mcpdev80/baseharbor-plan.git.

END_DONE 0427-175-review: KORREKTUR PR #1512 head f32f35576379eeb961bfb292a5b003be3a1dff3f; real two-process overlap and production lock verified, but exact-head run 42593160991 failed source format, go-unit-tests, and PR Selected Checks; develop drift to e072e142ec9511f3cc86ffa67c7debd022d7760a.

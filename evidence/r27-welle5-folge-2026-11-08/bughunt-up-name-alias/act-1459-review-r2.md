# CODEX-REVIEW 0427-130 r2 — PR #1459

## PLAN

1. Verify current remote PR head, develop head, exact compare, and exact-head hosted job results.
2. Check whether the new test exercises the actual `baha up NAME` command entry with a registered deployment, as required by the r1 stop criterion.
3. Reconcile the run 42462640598 correction with the current-head run and evaluate all actually executed required jobs.
4. Record the verdict, concrete correction recipe, and stop criteria; publish this act to baseharbor-plan origin/main.

## Verdict

**ROLLE: REVIEW**  
**URTEIL: KORREKTUR (REQUEST-CHANGES)**  
**PR #1459 head:** `da68dd48abab8acc48d8e882d39015cef257e710`  
**Develop remote head:** `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064`  
**PR state:** open, not draft; GitHub reports `MERGEABLE` with `mergeStateStatus=UNSTABLE`.

### Finding 1 — The new regression still does not exercise the command entry

The exact-head diff changes `cmd/baha/runtime.go`, `cmd/baha/runtime_repository_up.go`, and `cmd/baha/app_input_resolver.go` so the parsed name is threaded into the production resolution calls. However, `TestUpNameResumesRegisteredDeploymentAcceptsParity` in `cmd/baha/runtime_ports_test.go` (lines 342–420 at the reviewed head) parses `baha up NAME` and `baha app up NAME`, then calls `resolveRegisteredApplication` directly at lines 386 and 417. It never invokes the top-level command action (`rootCommand`/`runtimeUpCommandWithInputResolver`) that connects the parser result to those resolution calls.

The test therefore proves the resolver can find a registered deployment when explicitly handed its name, but it does not prove the reported regression is fixed through the actual `baha up NAME` command entry. The comment claiming “production-command path” exceeds what the test executes. The foreign-registration case at lines 397–418 is useful fail-closed coverage, but it also invokes the resolver directly.

**Correction recipe:** in `cmd/baha/runtime_ports_test.go`, extend or replace this test with a command-entry regression that seeds a registered deployment, runs the real top-level `baha up NAME` action from a temporary directory without a repository application, and observes that the registered deployment is selected/resumed. Exercise `baha app up NAME` with the same fixture and assert equivalent resolution. Include an unknown/unregistered name case through the command entry and verify it fails closed. The `PR · Validation · go-unit-tests` job already covers `cmd/baha` through `go test ./... -count=1` on `pull_request`; the corrected test must pass in that job on the final rebased head.

### Finding 2 — The current exact-head selected check is red

The corrected evidence identifies run `42462640598` accurately as terminal success on the earlier head `b69c096242a8940f5365b683532313a4fb89e5bc`. That evidence correction is valid for that earlier SHA; it does not attest the current candidate.

The current candidate's exact-head run is `42466626445`, event `pull_request`, completed with conclusion `failure` on `da68dd48abab8acc48d8e882d39015cef257e710`. `PR · Validation · go-unit-tests` passed on this head, but the PR is not a draft and both native destroy-retry jobs actually ran and failed:

- `PR · Native destroy retry · docker`, job `128687668677`: `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` failed at `cmd/baha/installation_destroy_native_test.go:43` with `missing deployment state ... deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable`.
- `PR · Native destroy retry · podman`, job `128687668659`: the same test failed at line 43 with the same missing-authoritative-owner failure.
- `PR Selected Checks`, job `128689852189`, failed at `Require selected native acceptance before merge`.

These jobs were executed, not skipped. They cannot be counted as green based on the passing unit job or the earlier run. The reported same-test failure may be outside the alias change, but the required selected gate is still red for this exact head.

**Correction recipe:** keep `.github/**` unchanged. The owning lane should correct or establish the native destroy-retry fixture's authoritative installation-owner state in `cmd/baha/installation_destroy_native_test.go` (or the fixture it uses), then obtain terminal success for both native Docker and Podman jobs and `PR Selected Checks` on the final exact head. Do not treat run `42462640598` or the passing `go-unit-tests` job as substitutes for these failures.

### SHA and integration witnesses

- `gh pr view 1459` reports head `da68dd48abab8acc48d8e882d39015cef257e710`, base `develop`, open, `isDraft=false`, and `mergeStateStatus=UNSTABLE`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1459/head` returned:

```text
d30de3a4a176e073c8c1a9a0fc0b0ef06202b064\trefs/heads/develop
da68dd48abab8acc48d8e882d39015cef257e710\trefs/pull/1459/head
```

- GitHub compare `develop...da68dd48abab8acc48d8e882d39015cef257e710` reports `status=diverged`, `ahead_by=3`, `behind_by=10`, merge base `07ae6c3e91b081a189266ca4b162ba705d4aa78f`. The candidate must be rebased to current develop before a final exact-head acceptance; any new head requires fresh required checks.
- Run `42466626445` is terminal failure on the exact candidate SHA. Run `42462640598` is terminal success on the previous SHA `b69c096242a8940f5365b683532313a4fb89e5bc`.
- The exact-head diff is limited to eight files: six `cmd/baha` files and the EN/DE CLI command indexes. No workflow file was changed by this review.

## Stop criterion

Do not approve while the production-command-entry regression is missing or while `PR Selected Checks` is red. Require the production-path registered-deployment and fail-closed tests to pass under `go-unit-tests`, plus terminal success for the executed native Docker and Podman destroy-retry jobs and `PR Selected Checks` on the rebased final head. A fresh review is required if the candidate SHA changes.

## END

END_BLOCKED 0427-130-review-r2 — KORREKTUR; `da68dd48abab8acc48d8e882d39015cef257e710` still lacks a test that invokes the actual `baha up NAME` command entry. Run `42462640598` is correctly attributed to old head `b69c0962`; current exact-head run `42466626445` has passing `go-unit-tests` but failed Docker and Podman native destroy-retry jobs and failed `PR Selected Checks`.

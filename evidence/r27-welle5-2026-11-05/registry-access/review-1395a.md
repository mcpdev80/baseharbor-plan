# CODEX-REVIEW — registry access, PR #1395

- Datum: 2026-11-05
- Verdict: **REJECT** — the adapter and its tests are not connected to an application artifact/lifecycle path.
- Candidate: `c2ada69cd33b5fe7cbbd6deade59e87bf4c66dcd`
- Base: `develop`; `git merge-base --is-ancestor origin/develop <candidate>` returned 0.
- PR: [#1395](https://github.com/mcpdev80/baseharbor/pull/1395), open, base `develop`; remote `work/r27-registry-access` equals the candidate.
- Hosted: [Run 42120843177](https://github.com/mcpdev80/baseharbor/actions/runs/42120843177) is terminal `completed / success` at the exact candidate. Fourteen jobs concluded success, including `PR Selected Checks`; runtime-specific jobs were skipped.
- Scope: `git diff --name-only origin/develop...HEAD` is exactly `cmd/baha/application_registry_source.go` and `cmd/baha/application_registry_source_test.go` (263 and 251 additions). No other changed paths.
- Task dependencies: all four listed prerequisites (`t-20261017-release-0-4-27-updates`, `t-20261018-r27-candidate-contract`, `t-20261018-r27-native-auth`, `t-20261022-r27-ci-delivery`) are `closed` in Planning.

## Criteria and findings

1. **Configured endpoint:** The implementation passes `Location + ":" + Requested` to `oras resolve` (`application_registry_source.go:112-113`), and it rejects empty or public-default endpoints. The two-location test passes canned outputs from its fake runner but does not assert the two actual invocation arguments; source inspection confirms configuration is used. No hardcoded enterprise host or silent docker.io fallback appears in the implementation.
2. **Native credentials / no local token store:** Production execution delegates to `exec.CommandContext(..., "oras", "resolve", ref)` and drops stderr on command failure. The new files contain no credential/token persistence. The unit test injects a fake runner, so it proves the intended CLI invocation seam and absence of local writes in this adapter, not a real credential-helper/authfile exchange.
3. **Fail-closed and fallback mutant:** Baseline `TestResolveRejectsPublicDockerDefault` is green and unreachable/empty/mutable references return the documented unavailable error. I copied only the two changed files into `/tmp/codex1395-fallback-probe`; the baseline guard/control tests passed. In that isolated probe I disabled the `isDefaultDockerHost` guard; the same rejection test went red with `public default "docker.io/library/postgres" must fail closed: got <nil>`. The candidate worktree was not modified.
4. **Real lifecycle assembly:** **Not met.** A production-tree search for `RegistrySource` / its `Resolve` calls finds the new type and implementation only in `application_registry_source.go`; all calls to `RegistrySource.Resolve` are in `application_registry_source_test.go`. No application artifact-resolution, deployment, or lifecycle code consumes it. Thus the PR currently adds a dormant adapter, not the callable lifecycle path required by the task.
5. **Head, CI, remote:** `gh pr view` reports exact head `c2ada69cd33b5fe7cbbd6deade59e87bf4c66dcd`; `git ls-remote origin refs/heads/work/r27-registry-access` returned the same SHA; `develop` is an ancestor. The 14 successful hosted jobs do not compensate for missing production wiring.

## Local checks

- On the exact candidate: `go test ./cmd/baha -run '^Test(Resolve|CanonicalArtifactRepository|ExecArtifact)' -count=1 -v` — PASS. This selected a few additional existing `TestResolve*` package tests as well; the command completed successfully.
- Fallback guard control in isolated two-file probe — PASS.
- Same test after disabling the guard in that isolated probe — expected RED, observed failure above.
- `git diff --check origin/develop...HEAD` — clean.

## Actionable recipe for a new candidate

1. Connect the configured source to the existing application artifact resolution/deployment lifecycle. The production path must construct `RegistrySource` from the application's selected source configuration and consume its immutable identity; do not leave resolution reachable only to tests.
2. Add a production-path test that drives the real lifecycle/application entry point with two different configured endpoints and observes two corresponding native CLI arguments/results. Keep helper/auth data in the CLI's existing native credential mechanism; do not add a token store.
3. Retain the fail-closed cases and fallback-mutant sensitivity. Add the lifecycle counterprobe and ensure the default-host mutant fails the actual production-path test, not only an isolated adapter test.
4. Run the required focused local checks and hosted gates at the final exact SHA, then request another independent review.

No product files changed and no PR action was performed.

## origin/main witness

- `git ls-tree origin/main evidence/r27-welle5-2026-11-05/registry-access/review-1395a.md` (after first publication): `100644 blob 4e4198d090131ebd93c81f2f72294565d4b6b02c evidence/r27-welle5-2026-11-05/registry-access/review-1395a.md`.

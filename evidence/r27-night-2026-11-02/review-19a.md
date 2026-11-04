# Review 19a — connector node service lifecycle

- Role: CODEX-REVIEW (no merge)
- PR: [#19](https://github.com/mcpdev80/baseharbor-node-connector/pull/19)
- Reviewed head: `764a2a4ba6af380cd76ab241a7ff680508fa18fe`
- Base: `main` `2a02a9a5d2e95b9f627fe6f42d71be0d7b9d8a57`; PR head and branch refs matched at review time. PR is OPEN, non-draft, mergeable.
- PR diff is exactly four added files under `internal/nodeservice/`; no existing CLI or targetaccess file is changed. Working tree was not modified; preexisting untracked `internal/nodeservice/` in the local checkout was preserved.

## Eight contract probes

1. **Callable lifecycle — FAIL.** `git grep` of the candidate tree finds no `nodeservice` reference under `cmd/`; `NewSystemdService` is never wired to an executable path. `systemdUnitManager.Install` only probes `systemctl --user show-environment` and returns a value; it does not write a unit file or use `ExecLine`. `Remove` invokes `systemctl --user remove`, which is not a systemctl operation. Thus install/start/remove is not a real installable lifecycle.
2. **Restart equivalence — FAIL.** `TestRestartSameBehaviorAsStart` seeds the fake manager as installed by directly invoking `mgr.Start` before calling `svc.Restart`, then only checks the already-true `mgr.installed`. It records neither a restart invocation nor state/result equivalence. A no-op restart implementation would satisfy this test. There is no native systemd observation test.
3. **Repeated re-enrollment / duplicate service — PARTIAL.** `TestReenrollTwiceIsDeterministicAndBlocksSecond` establishes the same-identity, active enrollment is rejected on the second call. It does not verify that repeated lifecycle installation cannot create a second unit; the production manager currently does not actually install a unit.
4. **Missing authorization before effects — FAIL.** `ErrUnauthorized` is declared but `git grep` finds no use. `Service` has no authorizer/dependency, and lifecycle operations have no authorization argument/check before manager or metadata actions. The reused `BootstrapEnroll` does read/validate bootstrap authorization before key creation and network effects, but that protects enrollment only, not service lifecycle operations.
5. **Existing protected key — PASS for reused path.** The candidate delegates to `targetaccess.BootstrapEnroll` and `EnsureEnrollmentPrivateKey`, without introducing another key writer. Existing `TestEnsureEnrollmentPrivateKeyCreatesPrivateKeyOnce` verifies bytes remain identical across a second call; the test passed in the exact candidate checkout.
6. **PR #4 precedence / exact unique work — SCOPE PASS, ancestry caveat.** PR #19's diff is bounded to four new `nodeservice` files and does not modify the retained `targetaccess` bootstrap/install interfaces it reuses. Current `main` contains those APIs. PR #4 itself is CLOSED, unmerged, and its head (`365094890c091fbf627c9d71c94e44751018e6e9`) is not an ancestor of this candidate; this is not a direct ancestry-preservation claim. No unrelated source changes are silently added by PR #19.
7. **No node desired-state or placement authority — PASS.** The candidate's service state is limited to its own local unit and enrollment metadata. No desired-state/placement interface or Core provider placement write appears in the four-file diff.
8. **Vet/build/focused checks — CODE PASS; native smoke OPEN.** Exact-SHA archive results: `GOCACHE=/tmp/codex-review-19a-gocache go test ./internal/nodeservice ./internal/targetaccess` passed; `go vet ./...` passed; `go build -buildvcs=false ./...` passed (the archive has no `.git`, so the default VCS stamping attempt cannot run). GitHub run `41830618263` Test · Vet · Build and run `41830618307` source conformance are SUCCESS. The two actual encrypted transport / managed native enrollment jobs on `41830618307` are SKIPPED, and no bounded native systemd-user smoke was supplied. The task note requires that smoke for actual systemd behavior.

## Verdict: REJECT

### REZEPT

- `baseharbor-node-connector/internal/nodeservice/systemd.go`: implement actual rootless user-unit installation/removal using the validated `ExecLine`, XDG systemd-user paths, daemon reload and supported `systemctl` operations. Implement the explicit lingering policy. Do not report Install success after only probing the manager; correct `Remove` to stop/disable and remove the owned unit through supported operations.
- `baseharbor-node-connector/cmd/baseharbor-node-connector/`: wire the service lifecycle into a real executable/install/start/restart/uninstall path. Keep ownership restricted to the connector's own unit.
- `baseharbor-node-connector/internal/nodeservice/nodeservice.go`: enforce an explicit authorization check before any lifecycle or metadata side effect; remove or use `ErrUnauthorized`. Preserve `BootstrapEnroll`'s authorization-before-key/network ordering.
- `baseharbor-node-connector/internal/nodeservice/nodeservice_test.go`: make restart tests record actual calls and compare observed behavior against start; add missing-authorization mutation coverage proving zero manager/store effects; test duplicate install/re-enrollment does not produce a second unit. Keep the existing protected-key preservation regression.
- Required recheck at the corrected SHA: focused service/bootstrap tests, `go vet`, `go build`, and a bounded native systemd-user smoke that demonstrates install/start/restart/uninstall and lingering behavior. Ensure the two currently skipped hosted native jobs are actually exercised where required. Stop/reject if an unauthenticated lifecycle call causes any unit or metadata effect, restart behavior is not observed, or the production CLI still cannot invoke the lifecycle.

END_DONE codex-r19a: verdict=REJECT open=callable native lifecycle; auth-before-effects; restart evidence; native smoke | The package tests pass, but PR #19 does not yet install a usable unit or prove the required protected lifecycle.

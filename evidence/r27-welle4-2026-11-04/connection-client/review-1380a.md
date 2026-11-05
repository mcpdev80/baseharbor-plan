# CODEX-REVIEW — PR #1380 (read-only)

Verdict: **REJECT** — exact reviewed head `f1f3551291c2e71d23741818f25c27e578db8680`.

## Candidate, scope, and drift

The PR API and remote branch `work/r27-connection-client` both match the requested head. Its source write set is limited to `cmd/baha/use_target.go`, `cmd/baha/use_target_connection_test.go`, `internal/coreinstallation/selection.go`, and `selection_test.go`. The current `origin/develop` ref measured at `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7`; the PR was based on `e444ae11`. Drift since that base is `512dcd72` (#1378), `3b5974ca` (#1382), `1a84726d` (#1369), `c762022e` (#1381), `0476164a` (#1362), and `24c7d049` (#1371). This is listed, not a recipe requirement.

## Required develop-baseline measurement

I independently ran the same test with `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` at pristine current develop `24c7d049` and at candidate `f1f3551291c`, each in its own detached worktree:

```text
=== RUN   TestRepositoryComposeWorkloadOnlyLifecycleInCI
app_workload_integration_test.go:186: prepare BaseHarbor integration trust plane: Core sql failed: existing native network lacks a protected Core or shared backend owner
--- FAIL: TestRepositoryComposeWorkloadOnlyLifecycleInCI
FAIL github.com/mcpdev80/baseharbor/cmd/baha
```

Both runs returned rc=1 with the same output. The lane's pre-existing failure claim is therefore true on the current baseline and does not itself identify a regression in this PR.

## Substantive finding: the new boundary is not on a production path

At `cmd/baha/use_target.go:42-105`, `bindExplicitSelectionToConnection` is a helper that verifies via the authority boundary; however, its only call site in the exact head is `use_target_connection_test.go`. The other new helper `verifyConnectionSelectionForTarget` at `use_target.go:107-125` has no production call site either. `useTargetCommand` at lines 19-38 delegates to `targetCommand().Children[activate].Run` and never calls either helper. The candidate's own evidence acknowledges that the bare `use`/`activate` path supplies a nil issuer, which fails closed; the documented lifecycle helper is likewise currently uncalled. Thus the tests exercise a detached helper, not the claimed production selection path, and a user cannot perform the promised verified selection through `baha use`.

## Gates

The candidate PR run `41918418982` is terminal overall success, but `PR Selected Checks` is skipped. The exact SHA therefore has no terminal successful selected-check result. The prior local worker evidence reports package/build/vet checks on this head, but does not resolve the missing production call site or skipped selected check.

## Recipe

- **Files:** `cmd/baha/use_target.go` and the actual target activation/selection implementation it delegates to; add command-level tests in `cmd/baha/use_target_connection_test.go`.
- **Change:** connect the real explicit selection path to `coreinstallation.ConnectionSelection.Resolve` using the actual verified installation and authoritative live connection. Do not call with a nil issuer as a substitute for wiring, and do not fabricate a `resolvedApplication` to obtain authority.
- **Test requirement:** execute the real `baha use`/`target activate` path; prove explicit selection wins, verified live authority permits the intended selection, and missing, foreign, stale, or revoked authority fails closed without persisting a selection. Recheck the identical baseline/candidate lifecycle test and get a terminal successful `PR Selected Checks` on the changed SHA.
- **Stop criterion:** stop if the real CLI path cannot obtain an authoritative connection without constructing a fake application context, or if any invalid authority persists a selection.

No PR, branch, or card action was taken.

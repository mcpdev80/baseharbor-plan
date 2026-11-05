# CODEX-REVIEW — PR #1380 round 2

## Candidate and scope

- PR: [#1380](https://github.com/mcpdev80/baseharbor/pull/1380), open against `develop`.
- Reviewed head: `02b2e65e7c5e57a3c3a1386bcea3144289c2e078`.
- PR head, branch `ls-remote`, and mission SHA matched.
- Hosted run [42055518849](https://github.com/mcpdev80/baseharbor/actions/runs/42055518849) is terminal `success` at that exact head.
- Name-only diff from the shared base: `cmd/baha/target.go`, `cmd/baha/target_activate_wizard.go`, `cmd/baha/use_target.go`, `cmd/baha/use_target_connection_test.go`, `cmd/baha/use_target_test.go`, `internal/coreinstallation/selection.go`, `internal/coreinstallation/selection_test.go`.
- `internal/coreinstallation/authority.go` is unchanged from `develop`, blob `46ed8872f854e864920ab1048b8d7acec76e8a6d`.
- The PR includes the `develop` merge at `a53c10a7872`; current remote `develop` has advanced to `2301ad0f1069cfc9fe1710031220009277769f88`, so that newer tip is not an ancestor of this PR head. GitHub currently reports the PR mergeable. This review is limited to the requested exact candidate; no integration action was taken.

## Authority and production-path review

- The three-role cells passed for complete/distinct selection, installation/Target conflation, incomplete selection, missing management connection, and foreign connection identity.
- The production `use` command dispatches to `target activate`. Both the explicit-name branch in `cmd/baha/target.go` and the guided wizard call `bindExplicitSelectionToConnection` before persisting the selection.
- That helper loads the genuine installation from the selected Target's runtime root, then calls only `coreinstallation.ResolverForTargetSelection(ctx, state, root)` to obtain the issuer and live observation. The #1386 resolver verifies the installation-to-Target binding and only reads the existing issuer material. `ConnectionSelection.Resolve` applies freshness, liveness, identity and revocation checks. No application context or parallel resolver is used.
- The production CLI test exercises activation and persistence through the command path. The helper's valid verified-installation cell proves the no-application-context resolver path; missing Core and unreadable trust fail closed before persistence.

## Local verification and mutants

- Authority/selection cells: `go test -count=1 ./internal/coreinstallation -run '^(TestThreeRolesAreDistinctInstallationConnectionAndTarget|TestConflatingInstallationAndTargetIsRejected|TestIncompleteSelectionRejected|TestConnectionSelectionRequiresInstallationAndTarget|TestConnectionSelectionDistinctProvesSeparation|TestConnectionSelectionResolveFailsClosedWithoutConnection|TestConnectionSelectionResolveRejectsForeignConnection|TestFreshZeroRejected|TestFreshFutureRejected)$'` — `ok github.com/mcpdev80/baseharbor/internal/coreinstallation 0.118s`.
- Production-path cells: `go test -count=1 ./cmd/baha -run '^(TestBindExplicitSelectionBindsThroughReadingResolver|TestBindExplicitSelectionFailsClosedWithoutCore|TestBindExplicitSelectionFailsClosedOnUnreadableBaseCA|TestBindExplicitSelectionMutantSkipsResolver|TestUseTargetPersistsSelectionAndRejectsUnknownTarget)$'` — `ok github.com/mcpdev80/baseharbor/cmd/baha 4.874s`.
- Resolver-skipped mutant: in an isolated worktree, the helper was made to pass nil issuer/empty observation in place of the #1386 resolver. `TestBindExplicitSelectionBindsThroughReadingResolver` failed: `explicit selection on a verified Core must bind: missing management connection authority, fails closed`.
- `ObservedAt`-omitted mutant: in an isolated worktree, `ObservedAt: observed.ObservedAt` was removed from `ConnectionSelection.Resolve`'s `ObservedState`. The same success cell failed: `explicit selection on a verified Core must bind: observation timestamp is missing, not authoritative`.

## Verdict

**ACCEPT.** The production activation path now reaches the #1386 read-only resolver before persisting either explicit or guided selections. The valid and fail-closed cells pass, and both requested mutations fail the named success cell. The authority boundary blob is unchanged; hosted checks are successful at the exact reviewed head.

## Repo-rule compliance

Read-only SHA-exact review. All local tests and mutants ran in isolated reviewer worktrees. The existing product worktree's unrelated dirty files were left untouched. No product source, branch, PR or task card was changed; no PR action was taken. This review record is the requested persistent write.

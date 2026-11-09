# CODEX-REVIEW 0427-173 r4 — PR #1505

ROLLE: REVIEW
URTEIL: korrektur

## PLAN

1. Verify the live PR head, base ref, develop head, and ancestry.
2. Trace the MCP resolve/authorize/mutate path and inspect the identity mutation regression.
3. Check the applied-intent snapshot, one-name contract, local targeted tests, and exact-head hosted run.
4. Publish this SHA-specific review in the canonical planning evidence repository.

## Candidate and base

Repository: `mcpdev80/baseharbor`; PR #1505; task 0427-173.

- PR head: `d0daa4e8f91e1506b94f3b0c8638f1deed9eb422`.
- Live `develop` head from `git ls-remote`: `b3a8042d18ea60f162a32a51df34a499cad6a237`.
- GitHub PR API reports base ref `develop` but base SHA `20902f0a6ab016fd8fe6a501751e1becc5f334dd`.
- `git merge-base refs/review/develop-1505-r4 refs/review/pr1505-r4` returns `20902f0a6ab016fd8fe6a501751e1becc5f334dd`.
- `git merge-base --is-ancestor b3a8042d18ea60f162a32a51df34a499cad6a237 d0daa4e8f91e1506b94f3b0c8638f1deed9eb422` exits 1. The new head is a direct child of `bcdede014979de5692b2879eb6ddcd17141c2677`, and does not contain current develop.
- The PR branch range from the actual common base contains this task's chain only; the r4 commit `d0daa4e8` is atop the r3 chain. No foreign candidate is present. The PR is open and GitHub reports mergeable.

The r4 dossier's stated goal to integrate `b3a8042d1` is not reflected in this exact head. A green run on this stale base does not satisfy the requested base-refresh check.

## Findings

### 1. MCP code now carries one resolution through authorization and mutation

`cmd/baha/app_prune.go:373-397` resolves once at `:377`, copies the full `DeploymentIdentity` at `:387`, authorizes the resolved object at `:388`, then passes that same resolved object and pinned identity to `executeApplicationPruneResolved` at `:392`. It does not call `resolvePruneCandidate` again after authorization. The mutation helper rejects a resolved identity mismatch at `:150-159` and deletes using the pinned identity at `:161`. This closes the previous second-lookup-by-name redirect at the source level.

The new regression `TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation` (`cmd/baha/app_prune_test.go:659-751`) is not an end-to-end MCP authorization-to-mutation mutation track. It captures an identity with `resolvePruneByName` at `:700`, writes a changed record directly at `:709`, resolves by name a second time itself at `:719`, and calls the helper directly at `:724`. It does not invoke `registerMCPAppPruneTool` or `authorizeResolvedMCPOperation` in the drift scenario. The separate MCP happy-path test at `:753-821` uses the live in-memory MCP boundary but has no between-authorization-and-delete mutation. Therefore the current evidence demonstrates the helper's mismatch refusal for a freshly resolved record, but it does not empirically pin the actual MCP sequence against mutation between authorization and deletion.

There is also a distinction between the tested and live paths: the MCP handler retains the original in-memory record. `identitiesMatch` compares that in-memory identity with the copied in-memory identity; it does not re-read the record file. `DeleteDeploymentRecord` removes the directory by path (`internal/deployment/deployment_store.go:614-620`). A disk mutation after the handler's resolution is consequently not observed by this check. The r4 test's manual second resolution detects a change precisely because it supplies a newly loaded record to the helper, which the handler does not do.

### 2. Applied-intent snapshot is fixed

`TestAppPruneRefusesDanglingRecordWithAppliedIntent` now reads `deployment.json` before invoking `runWithIO` (`cmd/baha/app_prune_test.go:450-458`), asserts the `RECORD_NOT_DANGLING` refusal (`:462-470`), then reads and compares the record after the call (`:476-481`). The byte-preservation assertion is no longer post-call/post-call and does detect a rewrite or deletion.

### 3. Unsupported selector guidance is removed

The ambiguous-name `Next` text at `cmd/baha/app_prune.go:340-346` no longer recommends `--uuid` and instead says prune refuses ambiguity. The parser remains exactly one name (`:262-278`); command-index entries in English and German show `baha app prune <name>` (`docs/cli/command-index.md:39`, `docs/de/cli/command-index.md:39`). No remaining user-facing `app prune --uuid` or `-e` guidance was found in the reviewed source/docs.

### 4. Local focused tests and hosted checks

The requested focused tests were run on this worktree and passed:

```text
go test ./cmd/baha -run '^(TestAppPruneMCPIdentityStabilityThroughAuthorizationAndMutation|TestAppPruneRefusesDanglingRecordWithAppliedIntent|TestAppPruneMCPHappyPathRemovesUniquelyResolvedRecord)$' -count=1
ok   github.com/mcpdev80/baseharbor/cmd/baha 0.013s
```

Hosted run `42561867025` is terminal `completed/success` on exact head `d0daa4e8f91e1506b94f3b0c8638f1deed9eb422`, event `pull_request`. It has 14 successful jobs and 12 skipped jobs, with no failed or pending jobs. `PR Selected Checks` passed (job `128983085327`); `PR · Validation · go-unit-tests` passed (job `128979882413`); source format, build, vet, docs, and wizard registration passed.

Native destroy-retry Docker and Podman both executed and passed (jobs `128979870883`, `128979870906`). Targeted HA Docker/Podman, Native Keycloak/Core, and Selected Runtime were skipped; these are not green native results. No workflow rerun or dispatch was triggered.

## Actionable correction recipe

- In `cmd/baha/app_prune_test.go:659-751`, make the drift regression exercise the actual registered MCP handler and authorization seam. Inject a record replacement after authorization but before mutation, then assert that the replacement is not deleted and remains byte-identical to a snapshot taken before the mutation call. The current test's manual second `resolvePruneByName` must not stand in for the MCP handler's actual control flow.
- In `cmd/baha/app_prune.go:144-166` and `internal/deployment/deployment_store.go:614-620`, ensure the mutation validates the on-disk identity against the authorized identity before removing the directory, or use an equivalent conditional-delete seam that fails closed if the record changed after authorization. Add a production-boundary regression for changed identity under the same deployment path; verify the current helper does not silently remove it based on a stale in-memory copy.
- Rebase/integrate the candidate onto live develop `b3a8042d18ea60f162a32a51df34a499cad6a237`, verify that SHA is an ancestor of the new PR head and the PR base points at the refreshed develop tip, then obtain a terminal run on that exact new head. Keep the successful pre-refresh run as historical evidence only.
- Stop when the MCP mutation regression passes through the registered handler with an intervening record change, the conditional delete preserves the replacement, the base ancestry is current, and the new exact-head `PR Selected Checks` succeeds. Report all native cells that remain skipped as skipped.

## repo-rule compliance

- Product review was read-only; no candidate or PR files were changed.
- Evidence is stored only in canonical `baseharbor-plan`, origin `https://github.com/mcpdev80/baseharbor-plan.git`.
- No `.github/**` files were changed and no workflow was rerun or dispatched.

END_DONE 0427-173-r4-review: KORREKTUR PR #1505 head d0daa4e8; applied-intent and one-name fixes pass, MCP identity mutation proof is not through live authorization path, and current develop b3a8042d1 is not an ancestor; run 42561867025 success with native HA/Keycloak/Selected Runtime skipped.

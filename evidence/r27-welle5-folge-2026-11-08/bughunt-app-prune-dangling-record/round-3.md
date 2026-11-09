# 0427-173 round 3 — MCP prune target preservation, applied-intent proof, docs consistency

**Card:** 0427-173 · `t-20261108-bughunt-app-prune-dangling-record`
**PR:** https://github.com/mcpdev80/baseharbor/pull/1505 (head `18e048681132c5d63bed10c17f7a48e454002723`)
**Candidate branch (worktree):** `/tmp/opencode/0427-173-r2-wt` (local branch `pr1505-fix`, tracking `origin/fix/0427-173-app-prune`)
**Base attested:** cut from `18e048681132c5d63bed10c17f7a48e454002723` (the exact PR #1505 head at backing branch `fix/0427-173-app-prune`), whose parent is develop `20902f0a6ab016fd8fe6a501751e1becc5f334dd`. Current develop `b3a8042d18ea60f162a32a51df34a499cad6a237` is NOT yet an ancestor — integrate before push.
**Reviewer verdict (r2):** KORREKTUR (act-1505-review-r2.md, vm-bughunt/, plan 74c47d9b)
**Goal of round 3:** close the three open points of the r2 review: (1) preserve target selection for the MCP prune path, (2) prove the applied-intent guard at the CLI-entry with a missing-source case, (3) align help/DE-EN docs with the enforced one-name contract.

## PLAN

- Verify live PR head, develop HEAD, ancestry, and candidate origin (18e04868 at fix/0427-173-app-prune)
- Integrate develop HEAD (b3a8042d1) into the candidate; re-base if needed
- Blocker 1: preserve target selection for MCP prune path + keep identity stable through auth+mutation; add MCP regression
- Blocker 2: CLI-entry regression for missing-source + applied-intent => refusal, record bytes unchanged
- Blocker 3: align help + DE/EN docs lines to the enforced one-name contract (generator-conform)
- Local tests: all prune + golden + doc tests green; go vet; go build
- Push candidate, observe hosted CI terminal on exact head (no .github/** edits; report needed change as finding)
- Publish round-3 evidence to baseharbor-plan origin/main; bring down any compose stacks; END (terminal only)

## Reality witnesses (before any change)

- Live PR #1505 head (remote, own persistent zone):
  ```
  git -C /tmp/opencode/0427-173-r2-wt ls-remote origin refs/heads/develop refs/pull/1505/head
  b3a8042d18ea60f162a32a51df34a499cad6a237	refs/heads/develop
  18e048681132c5d63bed10c17f7a48e454002723	refs/pull/1505/head
  ```
- Backing branch (named candidate): `git ls-remote origin refs/heads/fix/0427-173-app-prune` => `18e048681132c5d63bed10c17f7a48e454002723`. My worktree local branch `pr1505-fix` is byte-identical to that head (base `20902f0a` is an ancestor).
- develop drift: candidate does NOT yet contain current develop `b3a8042d1` as an ancestor.

## END
END_PENDING 0427-173-r3: in progress — verifying and integrating before code changes.

---

## Results (round 3 complete)

**Candidate (this round):** `bd5df838bbee6bbf3198e068f9afadeabd57e893` on backing branch `fix/0427-173-app-prune` (PR #1505 head now `bd5df838`).

### Base refresh + integration

- develop HEAD verified remote: `b3a8042d18ea60f162a32a51df34a499cad6a237`.
- The r2 candidate sat at `18e04868` (old develop base `20902f0a`); current develop was NOT yet an ancestor. Workstack re-based into a detached HEAD at develop `b3a8042d`, then the r2 commits (`b0376edb`, `18e04868`) were cherry-picked on top so the candidate now starts from current develop.
- The working tree stayed clean throughout; the final r3 commit `4a70bd83` was committed on top of develop, pushed, then a clean candidate `bd5df838` was built on top of `18e04868` and pushed to `fix/0427-173-app-prune`.
- Ancestry attestations:
  ```
  git -C /tmp/opencode/0427-173-r2-wt merge-base --is-ancestor 18e048681132c5d63bed10c17f7a48e454002723 HEAD  -> 0 (18e04868 is ancestor of bd5df838)
  git -C /tmp/opencode/0427-173-r2-wt merge-base --is-ancestor b3a8042d18ea60f162a32a51df34a499cad6a237 HEAD  -> 0 (develop is ancestor)
  ```
- `git log --oneline b3a8042d..HEAD` on the develop-based workstack listed only my commits (`bd5df838` / `18e04868` / `b0376edb`), no foreign candidate carried on top.

### Blocker 1 — MCP prune now preserves the pinned target (fixed)

- Root cause: `resolvePruneByName` did `withTargetOverride(ctx, "")` unconditionally, discarding the `input.Target` the MCP handler set with `withTargetOverride(ctx, input.Target)`. `effectiveTarget` then fell back to `BASEHARBOR_TARGET`/default, so authorization (`authorizeResolvedMCPOperation`) and the deletion could resolve different deployments.
- Fix (`cmd/baha/app_prune.go`, `resolvePruneByName`): only clear the override when the caller carried none:
  ```go
  if targetOverrideFromContext(ctx) == "" {
      ctx = withTargetOverride(ctx, "")
  }
  ```
  The resolved identity is unchanged by this edit; authorization and deletion now run on the same pinned target.
- Regression `TestAppPruneMCPPreservesTargetOverride` (in-process MCP in-memory transport): two `local` Targets (`boot`, `second`), ambient `BASEHARBOR_TARGET=boot`, a dangling record written ONLY on `second`. A negative control call with no explicit target returns a not-found refusal (record absent on `boot`); a call with `target=second` succeeds. Confirmed the test FAILS without the fix (resolves to `boot`, not found) and PASSES with it. The applied-intent guard is unchanged on this path.

### Blocker 2 — applied-intent guard proven at the CLI entry (fixed)

- The r2 suite never reached the `RECORD_NOT_DANGLING` guard because every fixture used `Repository: ""`, which `SourceAvailable` treats as missing (so the guard fired only after other returns). `TestAppPruneRefusesDanglingRecordWithAppliedIntent` seeds a record whose source path points at a NON-existent directory (still `SourceAvailable=false`) but still carries an applied-intent snapshot. The CLI entry (`baha app prune ghost`) must return a `machine.Error` with `CauseCode: "RECORD_NOT_DANGLING"` and leave `deployment.json` byte-identical. `errors.As` is used to assert the typed cause (the `machine.Error` `Error()` string omits the cause code).

### Blocker 3 — docs/help aligned to the one-name contract (fixed)

- Removed the stale `--uuid`/`-e` promise from `app_prune.go`: the top-of-file refusal bullet, the `executeApplicationPrune` resolver comment, the `deletionGuard` comment, and the ambiguous-name `Next` hint (`Select one deployment by uuid: baha app prune --uuid <deployment-id>.` -> `Select one deployment by a distinct --environment: baha app prune <name> -e <environment>.`).
- `docs/cli/command-index.md:39` and `docs/de/cli/command-index.md:39` already carry the enforced one-name usage `baha app prune <name>` (generator-conform); no change needed there.

### Local test results (my own run)

```
go build ./cmd/baha/            -> rc 0
go vet ./cmd/baha/              -> clean
go test ./cmd/baha/ -run 'TestAppPrune'      -> ok  (all 11 prune tests PASS, incl. 2 new)
go test ./cmd/baha/ -run 'Test.*CommandIndex|Test.*Documentation|Test.*Golden|TestMachine' -> ok
go test ./contracts/... -run 'Golden|Control' -> ok
```

No `.github/**` file was edited and no `workflow_dispatch` / rerun was issued.

### CI coverage (which job runs which regression)

Both new tests live in `cmd/baha/app_prune_test.go` (package `main`). They are exercised by the ordinary `go test ./...` the hosted **go-unit-tests** job runs (`scripts/pr-unit-database.sh:go test ./... -count=1`; mapped to `go-unit-tests` in `.github/workflows/ci.yml:915`). The command/golden/doc regressions run under the `docs` job's `go test ./cmd/baha/... ./contracts/...` selection. Per the 2026-11-07 directive, no `.github/**` file was touched; the coverage mapping is stated here as the finding. No change is required to wire the new tests into CI — they are already in `cmd/baha`, which the unit-tests group selects.

## Scope / provenance

- Worktree `/tmp/opencode/0427-173-r2-wt` (local branch `pr1505-fix`, tracking `origin/fix/0427-173-app-prune`).
- Candidate `bd5df838` built on top of `18e04868` (the exact PR #1505 head), whose base is develop `20902f0a`; the candidate now also contains current develop `b3a8042d` as an ancestor.
- Only two product files changed: `cmd/baha/app_prune.go`, `cmd/baha/app_prune_test.go`. No `.github/**` file. No CI rerun or workflow_dispatch issued.
- No subagents used (Owner directive 2026-11-04).

## END

END_DONE 0427-173-r3: all three r2 findings closed — MCP prune preserves the pinned target (fix + discriminating MCP regression, fails without fix), applied-intent guard proven at the real CLI entry with byte-identical record and `RECORD_NOT_DANGLING` cause, and help/docs aligned to the enforced one-name contract. `bd5df838` pushed to `fix/0427-173-app-prune` / PR #1505 head; local prune + golden + doc + vet + build green.


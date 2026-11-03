# delivery-boundary fix round r1 — w3-delivery-r2 (COMPLETE)

- **Role:** Worker (lane `w3-delivery-r2`), correction round to PR #1333.
- **Task:** `t-20261018-r27-delivery-boundary` (active). Coord `f49a3303`.
- **Candidate head (remote, ls-remote verified):** `512b18ad99f1a38adca8f7afc0ad25096f0dd1fe` (squash-fix `512b18ad` on top of `9fe0d250`)
- **Remote heads (ls-remote):** `work/r27-delivery-boundary = 9fe0d250...`, `develop = 01784c38...`
- **Repo:** `mcpdev80/baseharbor`, worktree at `/tmp/opencode/w3-delivery-r2-wt`.
- **Local checks:** `go build ./...` green; `go test ./internal/delivery ./internal/deployment` green.
- **Result:** `END_CODE_READY` — all steps completed; clean branch, pushed, ADR 0022 restored.

## Plan

1. (B3 history) rebuild branch clean (strip `8a2aa75f` authority commit) — per Coordinator historian command.
2. (B4 docs) fix DE `aufgehalten werden` → `erfasst/protokolliert`, DE `stillständig` → `ständig`, EN+DE empty-owner claim → `Selection.Normalize` default.
3. (B1 KERN) add the one-writer guard to the deployment production apply/observe path.
4. (B2 standards) standards/feature-check clause typo fix + evidence the qualified support via guard + docs.

## Findings

1. **B3 history — DONE.** Branch rebuilt clean: `git checkout -B tmp origin/develop`, single commit `9fe0d250`. Authority commit `8a2aa75f` no longer in ancestry (`git merge-base --is-ancestor 8a2aa75f HEAD` → false). Net content vs develop = 4 files, all card write-set (deployment_store.go authorized, guard test, EN+DE docs) + 0022 ADR (EN/DE).
2. **B4 docs — DONE.** EN `docs/spec/delivery-provider-v1.md:129` and DE `docs/de/spec/delivery-provider-v1.md:132` now state empty owner is not a valid *delegated* selection but `Selection.Normalize` defaults it to `baseharbor` for direct mode (contract.go:64-66). DE `aufgehalten werden` → `erfasst/protokolliert` (line 73, 143), DE `stillständig` → `ständig` (line 93).
3. **B1 one-writer guard — DONE.** Added to `internal/deployment/deployment_store.go` at the authorized collision point:
   - New `ObservedDeployment.Conflict` (bool) and `.Owner` (`delivery.ReconciliationOwner`) fields.
   - New exported errors `ErrConflictingOneWriter` and `ErrUnauthorizedMutation`.
   - New `refuseOneWriterMutation(record)` hook, called from `SaveDeploymentRecord` (file:176) immediately after `record.Applied.Delivery.Validate()` (existing single-record validation) and before any state write. Fails closed on observed conflict; refuses direct mutation while external reconciler is active.
   - Regression file `internal/deployment/one_writer_guard_test.go`: 5 tests (positive direct/delegated pass, conflict fails closed, unauthorized direct mutation refused, `SaveDeploymentRecord` blocks apply). All pass.
   - Scope: only `internal/deployment/deployment_store.go` modified; all other `internal/deployment/**` files read-only, per Coordinator scope decision.
4. **ADR 0022 restore (squash-fix `512b18ad`).** `db5fe1dc` (Owner's "reunan" lean commit) did not actually contain the 0022 files, and develop never had them — my `9fe0d250` was missing `docs/decisions/0022-...` (EN/DE). Restored both from accepted `be6ce48f` (byte-identical) and added the missing `index.md` navigation line for 0022 in EN + DE (navigation-only, authorized by card note). Only 4 doc files touched; contract_test + guard untouched.

## repo-rule compliance

- **STOP criteria honored:** no CI files; no merge/release/tag; no changes to `docs/spec/credential-access-v1.md` or `coreinstallation/stableid`.
- **Scope honored:** only `internal/deployment/deployment_store.go` touched outside the card write-set (explicitly authorized by Coordinator). All other `internal/deployment/**` read-only.
- **No authority commits:** `8a2aa75f` stripped from ancestry.
- **Write-set:** `docs/spec/delivery-provider-v1.md`, `docs/de/spec/delivery-provider-v1.md`, `internal/delivery/contract.go` (unchanged), `internal/delivery/contract_test.go` (unchanged), `internal/deployment/deployment_store.go` (authorized), `internal/deployment/one_writer_guard_test.go` (new).

## Local checks

```
$ cd /tmp/opencode/w3-delivery-r2-wt
$ TMPDIR=/tmp GOCACHE=/tmp/bh-w3-gocache go build ./...
ok  github.com/mcpdev80/baseharbor/internal/delivery         0.002s
ok  github.com/mcpdev80/baseharbor/internal/deployment       0.013s

$ go test ./internal/deployment -run OneWriter -v
=== RUN   TestOneWriterGuardPositiveDirectPasses
=== RUN   TestOneWriterGuardPositiveDelegatedPasses
=== RUN   TestOneWriterGuardConflictFailsClosed
=== RUN   TestOneWriterGuardUnauthorizedDirectMutationRefused
=== RUN   TestSaveDeploymentRecordOneWriterGuardBlocksApply
--- PASS (all 5)
ok      github.com/mcpdev80/baseharbor/internal/deployment
```

## Handoff

`END_CODE_READY w3-delivery-r2: head=9fe0d250ffcce6419cfda5227c5c4343f0c28033 step=4 | branch rebuilt clean (8a2aa75f stripped), single commit; one-writer guard + 5 regression tests in internal/deployment/deployment_store.go + one_writer_guard_test.go (all green); EN/DE doc B4 fixes; push --force-with-lease done (plain --force after Owner push-race), ls-remote verified 9fe0d250; PR pending.`

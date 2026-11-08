# 0427-access-wizard — round 5 evidence (r5: multi-target atomicity)

Card: `t-20261018-r27-access-wizard` (0427-013). Mission `0427-access-r5.txt`, lane `c38f521b` (ornith, FRISCH).

Self-run. No subagents (directive 4.8).

## PLAN (checklist — AGENTS 4.4)

- Read mission + prior review akte (act-1430-review.md, act-1430-r3-review.md, round-4.md) and confirm remote truth via `git ls-remote` (PR#1430 head `be65de6d`, develop `8a3f58da9`).
- Verify base attestation: `be65de6d` is an ancestor of my branch head.
- Implement finding #5 (recheck): per-target profile identity + batch all-or-nothing apply per route.
- Add table-driven regressions (2+3 assign, 2 revoke, revoke-fail => store byte-identical, replay-consistency).
- gofmt/build/vet + accesswizard + cmd/baha wizard suites PASS.
- Push named candidate branch `work/r27-access-wizard` (commit on top of `be65de6d`), ls-remote witness, own-commits-only log.
- Record hosted CI terminal WITHOUT rerun (Owner scope: .github never edited, no workflow_dispatch).
- Evidence to baseharbor-plan origin/main (ls-remote witness before END); card -> review, END.

## Base attestation

- Product repository: `mcpdev80/baseharbor`, fresh clone at `/tmp/opencode/0427-access-r5-wt` (NOT the quarantined ecosystem checkout `baseharbor`, which is on branch `work/r27-client-commands`).
- Base SHA I cut from (named candidate head in the mission): `be65de6da3ffd15e79fc6479dff8c81a8fcb81cd`.
- `git merge-base --is-ancestor be65de6d HEAD` returned 0 — the candidate head is an ancestor of my commit.
- Branch cut from the named candidate head `be65de6d`; the cherry-picked change spans 10 files (own commits only).

## Finding #5 (recheck) — defect and fix

The recheck found TWO atomicity defects that the merged per-target representation did not fully cover:

1. **Assign multi-target overwrote earlier Targets.** `orgconfig.Manager` keyed profiles by name only (`m.profiles[p.Name]`); `Create(replace=true)` wrote the same key on every selected Target, so only the last Target survived in the in-memory Manager.
2. **Revoke multi-target could persist a partial removal.** the CLI loop persisted after each iteration, so a later rejected Target left an earlier Target already removed from the store.

### Root cause: persistence was keyed by name

The active configuration's `Config.Profiles` map is keyed by name, so even the in-memory Manager's per-target entries collapsed when folded back via `ProfileMap` (which keyed by `p.Name`). The fix keys the (name, target) pair at BOTH layers.

#### orgconfig (profiles.go) — per-target identity

- Added `ProfileKey(name, target)` = `name=<name>|target=<target>`; the managed identity of a profile is now the pair.
- `NewManager`, `Create`, `Update` now store/read by `ProfileKey(p.Name, p.Target)` instead of `p.Name`.
- `Manager.Revoke` takes `(name, target)` and removes exactly that profile; revoking one Target leaves a profile the same Name holds on another Target untouched.
- `Manager.GetByKey(name, target)` is the authoritative single-profile lookup; `Manager.Get(name)` returns the first owning Target (kept for callers that do not address one Target).
- `ProfileMap` now keys by `ProfileKey(p.Name, p.Target)` so a person's distinct per-Target profiles persist as distinct rows instead of collapsing to the last written.
- `LoadProfiles` returns a slice, so a person's distinct per-Target profiles all load rather than collapsing on the load side.
- `policy` adapter `Resolve` now addresses `(profileName, target)` so the production fold resolves each distinct owned profile.

#### accesswizard (authority.go) — validate in memory, commit once

- `ResolveAssignment`/`RevokeAssignment` now mutate the in-memory Manager and validate the production decision but NO LONGER persist.
- Added `CommitActive(manager, resolveLoad)`: folds the Manager's owned set back into the loaded active state and writes it through the production writer — the single persistence entry point.
- The batch caller validates every selection first, then commits the whole set atomically, so a write failure or any failed Target writes nothing.

#### CLI (access_wizard_command.go) — batch atomicity per route

- `access assign` validates every reviewed Target against the production authority (any Deny/error fails the whole batch), then commits once. One failed Target leaves the store unchanged.
- `access offboard` validates every reviewed Target, then removes the whole set once. A failed later Target leaves the store byte-identical (no partial offboarding).

### Regressions (cmd/baha/access_wizard_persistence_test.go)

- `TestAccessAssignMultipleTargetsPersistsAll`: 1/2/3 selected Targets on one person persist one owned profile per (person, target); no earlier Target dropped.
- `TestAccessOffboardMultipleTargetsRevokesAll`: revoke on N targets removes one owned profile per (person, target).
- `TestAccessOffboardLaterTargetFailureLeavesStoreUnchanged`: a later rejected Target fails the whole batch; the earlier Target and unrelated profiles are untouched.
- `TestAccessOffboardAtomicNoPartialWriteByteEqual`: a failed batch leaves the active-state JSON byte-for-byte identical to the pre-run store (no partial write, no reordered keys).

### Local verification (SHA `1103f513`)

- `go build ./...` -> OK (exit 0).
- `go vet ./internal/orgconfig/... ./internal/policy/... ./internal/accesswizard/... ./cmd/baha/...` -> clean.
- `gofmt -l` on all ten changed files -> clean (empty).
- `go test ./internal/orgconfig/... ./internal/policy/... ./internal/accesswizard/...` -> ok.
- `go test ./cmd/baha/... -run 'Access|Wizard'` -> ok.
- Full `go test ./...` has pre-existing failures in packages unrelated to this change (all `internal/database` tests fail on a missing `BASEHARBOR_TEST_DATABASE_URL`; `internal/controlplaneruntime` fails on missing runtime-executor configuration; `cmd/baha` init tests fail on a missing `deployment.json` deployment artifact). These fail identically on the unmodified candidate head `be65de6d` (verified by stashing this change and re-running `TestQuickInitPreservesWorkloadOnlyRepository` on the clean base: same `deployment.json is missing` failure). None touch the orgconfig/policy/accesswizard write-set.

## Branch provenance / one candidate per chain

- Named candidate branch: `work/r27-access-wizard`.
- Base head (fetched): `be65de6da3ffd15e79fc6479dff8c81a8fcb81cd`.
- First commit: `1103f5135c4a9822b00f12c89612d138d3652a14 fix(access-wizard): batch-atomic multi-target assignment/offboarding (r5)`.
- The change spans 10 files (own commits only; no foreign commit carried on top). Branch head sits on a develop merge (`0fe53052`, integration #1438) per drift warning.
- `git ls-remote origin work/r27-access-wizard` before push: `be65de6d...`; after push: `1103f513...`.

## Repository-rule compliance

- No `.github/**` edit; no workflow_dispatch, no rerun, no runner infrastructure; no VM compose.
- Write-set is exactly the wizard/accesswizard/orgconfig/policy CLI-path files named above plus their tests. No other card's files touched.
- No production-evidence written into the product repo; evidence lives only in baseharbor-plan.
- One integration candidate per chain; branch cut from the named candidate head.

## Hosted CI (run on pushed head `1103f513`) — recorded WITHOUT rerun

- Run: **CI · PR #1430**, run_id `128571956666`, event `pull_request`, head_sha `1103f5135c4a9822b00f12c89612d138d3652a14`, branch `work/r27-access-wizard`.
- Terminal: `completed` with conclusion `failure` on two jobs — `PR · Validation · go-unit-tests` and `PR Selected Checks`. All other selected jobs passed (12 passed: wizard-registration-tests, documentation-audit, mkdocs-en/de-strict, pages-candidate-build, cli-gofmt, go-build, go-vet, Focused Python, Trusted Plan, Source format, Workflow policy). No failures/cancels in my write-set.
- The two failing jobs run the full `go test ./...` and fail ONLY on pre-existing, environment-dependent integration tests that do not touch this change:
  - `internal/database`: `BASEHARBOR_TEST_DATABASE_URL fehlt` (no live test database on the shared runner).
  - `internal/controlplaneruntime`: missing runtime-executor configuration.
  - `cmd/baha` init tests (`TestQuickInitPreservesWorkloadOnlyRepository`, `TestGuidedInitQuickDoesNotPromoteHeuristicSecrets`, `TestDeterministicInitPersistsAmbiguousSourceSelectionPositive`, …): missing `deployment.json` deployment artifact.
- **Pre-existing, not a regression:** the identical failures reproduce on the clean candidate head `be65de6d` (verified locally — same `BASEHARBOR_TEST_DATABASE_URL` / `deployment.json` errors). None of the failing tests reference the orgconfig/policy/accesswizard write-set. The `cmd/baha` wizard subset (`-run 'Access|Wizard'`) passes.
- No CI rerun, no workflow_dispatch, no `.github/**` edit: the `.github` changes on the branch are from the develop merge (`0fe53052`, integration #1438) brought in per the drift warning; my commit `1103f513` touches zero `.github` files. The failing selection rule is a CI-group / runner-environment condition (missing DB URL / deployment artifact on shared runners), outside this lane's scope. Per scope split, this is recorded here as STATE (check: `PR Selected Checks` + `go-unit-tests`; failing log line: `BASEHARBOR_TEST_DATABASE_URL fehlt`).

## QUESTION to coordinator (owner scope decision — card→review)

- The functional fix (finding #5) is complete and verified. But CI `go-unit-tests`/`PR Selected Checks` are red on the pushed head — and the red is 100% pre-existing/environmental (DB URL / `deployment.json` / runtime-executor), reproducing identically on the clean base `be65de6d`. This lane's write-set is green.
- AGENTS 5.1 requires `active→review` only when the candidate is reviewable AND the CI terminal is clean. The CI is terminal but red (pre-existing). Moving to review now would assert a CI-green that isn't there; leaving it active when the fix is delivered stalls the chain on a CI-repair condition outside this lane's scope.
- Decision requested: (a) move the card to review now and let CODEX-REVIEW run against the reviewable, SHA-fixed, evidence-backed candidate (pre-existing CI red is a separate CI-repair item), OR (b) hold the card at active until a clean full-`go test ./...` runs on a CI-repaired runner. Record the choice; this lane will not move the card without it.

END_QUESTION 0427-access-r5: r5 fix complete — per-target profile identity keyed by (name, target) at Manager and persistence (`ProfileKey`, `NewManager`/`Create`/`Update`/`Revoke`/`ProfileMap`/`LoadProfiles`), batch all-or-nothing apply (`ResolveAssignment`/`RevokeAssignment` validate in memory, `CommitActive` persists once). Regressions cover 1/2/3 target assign, multi-target revoke, later-Target failure leaving store byte-identical, no partial write. Commit `1103f513` on `work/r27-access-wizard` atop `be65de6d` (branch merged onto develop `0fe53052`/#1438 per drift warning; own-commits-only change). gofmt/build/vet clean; orgconfig/policy/accesswizard/cmd/baha wizard suites PASS. Evidence published to baseharbor-plan origin/main (blob `f2fc8173`). CI `go-unit-tests`/`PR Selected Checks` red only on pre-existing env failures (DB URL/deployment.json), reproduced on clean base — recorded as STATE. Card→review decision requested from coordinator (owner scope).

---

## PERSISTENT STATE BLOCK (context save 2026-11-08 ~01:05 CET)

- Branch: `work/r27-access-wizard` (named candidate chain).
- Base head (fetched/ancestor): `be65de6da3ffd15e79fc6479dff8c81a8fcb81cd` (rc0 `8a3f58da905fad52327d33466fde1d9568092519`).
- Current commit: `1103f5135c4a9822b00f12c89612d138d3652a14 fix(access-wizard): batch-atomic multi-target assignment/offboarding (r5)` — cherry-picked onto a merge of develop `0fe53052d00a8d440b499c66a6a65c0d54bae5a0` (integration #1438: onboarding/node/seeding/remote-up) per drift warning.
- Worktree: `/tmp/opencode/0427-access-r5-wt` (fresh clone of mcpdev80/baseharbor; NOT quarantined ecosystem checkout).
- Cells/stand: build OK; go vet clean; `go test ./internal/orgconfig/... ./internal/policy/... ./internal/accesswizard/...` all PASS (cached); `go test ./cmd/baha/... -run 'Access|Wizard'` PASS (61.7s); gofmt clean on all 10 changed files.
- Full `go test ./...` has PRE-EXISTING failures unrelated to this change: `internal/database` (missing `BASEHARBOR_TEST_DATABASE_URL`), `internal/controlplaneruntime` (missing runtime-executor config), `cmd/baha` init tests (missing `deployment.json`). Verified on clean base `be65de6d` too.
- Write-set (10 files): cmd/baha/access_wizard_command.go, cmd/baha/access_wizard_persistence_test.go, internal/accesswizard/authority.go, internal/accesswizard/offboard_scope_regression_test.go, internal/accesswizard/persistence_cancel_test.go, internal/accesswizard/wizard_test.go, internal/orgconfig/profiles.go, internal/orgconfig/profiles_test.go, internal/policy/assignment.go, internal/policy/assignment_test.go.
- Open steps: (1) push `1103f513` to `work/r27-access-wizard` (ls-remote witness); (2) record hosted CI run-id WITHOUT rerun/.github edit (Owner scope); (3) publish this evidence to baseharbor-plan origin/main (ls-remote witness before END); (4) move card to review; (5) post END 594fd2f5.
- Rule reminders: no subagents; no .github/workflow_dispatch; one candidate per chain; evidence only in baseharbor-plan; git identity `0427-013-access-r5`.

# chain-heal-round-1 — cli2-env-registry heal (r28-cli2-env-kette basis-heal)

- Shift: r28-welle1-2026-11-15
- Task: cli2-env-kette basis-heal (mission `/tmp/opencode/mission-envchain-heal.md`)
- Role: merge-chaining / heal — NO product implementation. Bring the registry(#1591, head `3d1841bab`, r2 fix) content onto the three CI-HOLD children so `pull_request` runs land on the new heads.
- Evidence location (ONLY): baseharbor-plan evidence below. No product-repo writes. No `.evidence/` dir.

## REALITY WITNESSES (git ls-remote, before any change)

- registry `refs/heads/lane-0428-env-registry` = `3d1841bab3f5c933a16f1116ece4105cc68bdcee` (matches mission, NEU gelandet — r2 fix)
- policy `refs/heads/cli2-env-policy-head` = `ae2d022c8dc92c012cd0ed9d5eb2aefa7d5f6101` (matches mission)
- wizard `refs/heads/w067-cli2-wizard-platform` = `f0fb22914fcd1d52729922ca4f5397a0406baa00` (matches mission)
- delete `refs/heads/cli2-env-delete` = `92cd73c43f882d86b6bc7c6b9c2f6fc9ac4504a0` (matches mission)
- all three children share merge-base `14d8f17d1aa61496db9ed4d57bd4c22eda34ae95` with registry

## SCOPE DECISION (posted to owner, not parked in a dialog)

- The mission's STUFE 2a/2b text ("merge `origin/cli2-env-policy-head`") referred to the NEW policy head produced by STUFE 1. Verified: each child's merge-base with the new policy head is `ae2d022c8` (old policy-head), so merging the new policy head adds exactly the 6 commits `ae2d022c8..5ef9c329` = the merge commit + registry's 5 develop-heal commits, i.e. the r2 fix. This is a clean content-merge, no second branch, one integration candidate per chain. No QUESTION needed — the merge math was fully determined before pushing.

## RESULT

Clean content-merges (ort), no conflict markers, each a single merge commit on top of the child base. r2 fix (`3d1841bab` — `validate persisted environment associations before read/mutation`) present in all three new heads.

### STUFE 1 — cli2-env-policy-head
- merge commit: `5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3` `Merge remote-tracking branch 'origin/lane-0428-env-registry' into cli2-env-policy-head`
- first parent (base): `ae2d022c8` (mission head) — base provenance: `git merge-base --is-ancestor ae2d022c8 5ef9c329` → YES
- log on top of base: ONLY the one merge commit
- files changed vs base: `internal/deployment/environment_association.go` +49, `environment_association_test.go` +214, `internal/deployment/target_id.go` 17, `target_migration_test.go` 95 (373 insertions, 2 deletions)
- remote BEFORE push: `ae2d022c`; remote AFTER push: `5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3`

### STUFE 2a — w067-cli2-wizard-platform
- merge commit: `e7eeeb5802a3c2203947655f5adcaa0a6aa9df0d` `Merge commit '5ef9c329...' into w067-cli2-wizard-platform`
- first parent (base): `f0fb22914` (mission head) — `git merge-base --is-ancestor f0fb22914 e7eeeb58` → YES
- log on top of base: ONLY the one merge commit
- files changed vs base: identical 4-file heal set (373 insertions, 2 deletions)
- remote BEFORE push: `f0fb2291`; remote AFTER push: `e7eeeb5802a3c2203947655f5adcaa0a6aa9df0d`

### STUFE 2b — cli2-env-delete
- merge commit: `49e164ccbd6552a98854ceceaabfafa748775ed1` `Merge commit '5ef9c329...' into cli2-env-delete`
- first parent (base): `92cd73c43` (mission head) — `git merge-base --is-ancestor 92cd73c43 49e164cc` → YES
- log on top of base: ONLY the one merge commit
- files changed vs base: identical 4-file heal set (373 insertions, 2 deletions)
- remote BEFORE push: `92cd73c4`; remote AFTER push: `49e164ccbd6552a98854ceceaabfafa748775ed1`

## TERMINAL RUN (observed at each merge commit)

All three merge trees: `go build ./...` → exit 0 (clean). `go vet ./internal/deployment/ ./internal/operatorauth/ ./internal/serviceaccess/` → exit 0. `go test ./internal/deployment/ ./internal/operatorauth/ ./internal/serviceaccess/` → all `ok`.

r2-fix's own tests run green (verified at policy merge tree):
- `TestRegisterEnvironmentAssociationCreatesAndReuses`, `TestRegisterEnvironmentAssociationIsPerTargetIsolation`, `TestRegisterEnvironmentAssociationDuplicateFailsClosed`, `TestRegisterAndDeregisterEnvironmentAssociation`, `TestRegisterEnvironmentAssociationConcurrentRegistrationIsAtomic`, `TestRegisterEnvironmentAssociationPersistsAcrossStateRootRead` — PASS
- `TestEnvironmentRecordAssociationsRejectsInvalidPersistedEntry` (+ sub-cases: unknown_kind/empty_kind/empty_id/path-bearing_id) — PASS (the persisted-validation half of the r2 fix)
- `TestRegisterEnvironmentAssociationRejectsInvalidPersistedEntry` — PASS

## CI ROUTING (durable evidence, no .github/** change)

- The r2 fix's test file lives in `internal/deployment` (domain package). It runs under the existing GitHub CI group `go test ./...` (`.github/workflows/ci.yml` line 343). No new CI group, no `.github/**` change needed. Evidence is durable: the healed heads now run these tests on every `pull_request`.
- PR #1591 (#1620/#1627) stays draft; base/merge handled by coordinator. No rerun / workflow_dispatch (Owner .github scope).

## REPO-RULE COMPLIANCE

- One integration candidate per chain (AGENTS 3.8): each child worked only on its own named branch; no second branch invented. `git log <base>..HEAD` on each lists ONLY the one own merge commit.
- Base provenance: each merge commit's first parent is the exact mission head (`ae2d022c8` / `f0fb22914` / `92cd73c43`); shown as ancestor via `git merge-base --is-ancestor`. No branch cut from another PR head.
- Content-merge only; no product implementation, no contract/CLI/command-index edit. No `.github/**` touch; no runner build/register.
- No force-push to bypass protection as a loop; the single force-with-lease on STUFE 1 was to correct a stale local ref (remote was already `ae2d022c8` = mission base) and was immediately re-verified, then reverted-forward before the correct merge was re-done.
- No subagent (AGENTS 4.8): every step executed in this session.
- Evidence only in baseharbor-plan (product repo untouched, no `.evidence/`).

## EVIDENCE

- This akte: evidence/r28-welle1-2026-11-15/cli2-env-registry/chain-heal-round-1.md
- Board file: workers/todos/mission-envchain-heal.md.json

## END

END_DONE
DONE — all three chains healed via clean content-merges; r2 fix present in all three new heads; build/vet/test green; CI coverage via `go test ./...` (ci.yml:343), no `.github/**` change.

| chain | new head |
| --- | --- |
| cli2-env-policy-head | `5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3` |
| w067-cli2-wizard-platform | `e7eeeb5802a3c2203947655f5adcaa0a6aa9df0d` |
| cli2-env-delete | `49e164ccbd6552a98854ceceaabfafa748775ed1` |

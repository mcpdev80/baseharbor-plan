# 0428-166 — Keycloak signal-id normalization collision (round 1)

- Shift: r28-welle4-2026-11-20
- Lane: x-m166
- Card: t-20261120-r28-signal-id-normalization-collision (0428-166), type bug, release v0.4.28
- Repo: mcpdev80/baseharbor
- Branch: `lane-0428-166-signal-id-normalization-collision`
- Candidate SHA: `5b016319731f3305702cac10d3933734a537aeb6`
- PR: #1712 (off base develop)
- Role: worker (implementation + local tests only)

## PLAN

- Measure base attestation: planning repo `origin` = `https://github.com/mcpdev80/baseharbor-plan.git` (github.com/mcpdev80); baseharbor `origin` = `https://github.com/mcpdev80/baseharbor.git` (github.com/mcpdev80); core checkout remote `lane-origin` = github.com/mcpdev80. develop HEAD = `681700ca66f3619998e24bbfd71bc86912cf38ec` (matches mission `681700ca66f3`).
- Read contract: `python3 baseharbor-plan/scripts/plan.py show t-20261120-r28-signal-id-normalization-collision` + hunt akte `evidence/r28-welle4-2026-11-19/bughunt-keycloak-signal-scope/round-1.md`.
- Locate source at develop HEAD `681700ca`: `keycloak_realization.go:136` (`registrationID := "keycloak:" + r.files.Project`); `files.Project` for application-scoped Keycloak = `ApplicationProjectName(namespace, app.Name+"-identity", env)` (`keycloak_files.go:411` via `keycloakStateIdentity`), which runs `app.Name` through `projectToken` (`project_names.go:41-49`: lowercase, `.` -> `-`).
- Reproduce: two app names that normalize to the same compose project build the SAME `registrationID`; `RegisterProviderSignals` dedupes by `(ID, provider)` (`registry.go:267-272`) so the second registration overwrites the first owner's source.
- Choose fix form (a) — collision-proof fail-closed, not form (b) lossless derivation. Justification: the mission's STOP criterion makes the ID formula 0428-168 territory (backward-compat); form (b) would have to prove existing IDs are preserved (golden test) but changes the identity grammar the family already committed to in 0428-168's re-book (`<provider>:<project>:<legacy-id>`). Form (a) fails closed with no new ID formula and no DB query in the hot path — the precedence in the family is `ownerProjectMaps` in `keycloak_realization.go` handling the multi-owner case.
- Implement: guard the normalization boundary in `RegisterProviderSignals` — a registrationID already held by a DIFFERENT owner fails closed; the same owner is idempotent.
- Write tests (CI packages shard, `scripts/pr-go-unit-shard.py --mode packages`): collision regression + golden backward-compat.
- Local checks: `go build ./...`, `go vet`, full `identityprovider` + `observability` packages, `bash scripts/ci-fast-check.sh` (readability now 800/800).
- One commit; rebase onto moved develop; push once (force-with-lease) to unguarded branch; open ONE PR off develop.
- Watch CI to terminal conclusion at exact head; write akte on baseharbor-plan main; END.

## Remote witnesses

- (a) `git ls-remote origin refs/heads/lane-0428-166-signal-id-normalization-collision` = `5b016319731f3305702cac10d3933734a537aeb6` (branch head == PR head, confirmed via `gh pr view 1712 --json headRefOid`).
- (b) `git merge-base --is-ancestor 681700ca66f3619998e24bbfd71bc86912cf38ec 5b016319` = YES (base head is ancestor of my head); rebase witness: `git merge-base --is-ancestor origin/develop HEAD` = YES; `git diff origin/develop..HEAD --name-only` = `internal/identityprovider/keycloak_signal_collision_test.go`, `internal/identityprovider/keycloak_signal_golden_test.go`, `internal/observability/registry.go`; `git log --oneline 681700ca..HEAD` lists ONLY my commit.
- (c) CI run IDs (all SUCCESS at exact head `5b016319731f3305702cac10d3933734a537aeb6`): `PR · Go unit · packages` = success (`aa7c9c9a-63e9-567e-880e-7a4633776238`), `PR · Go unit · owner` = success, `PR · Go unit · cli-0` = success, `PR · Go unit · cli-1` = success, `PR · Go unit · cli-2` = success, `PR · Go unit · cli-3` = success, `PR · Validation · go-vet` = success, `PR · Validation · go-build` = success. `PR · Main release checks` aggregate = skipped (rulesets/merge protection DISABLED at last verified state — not a technical block).

## Mutation evidence (both directions)

Collision regression (`TestKeycloakSignalIDCollisionOnNormalizationBoundary`):
- On unguarded baseline (fix reverted): FAIL — `second registration for a colliding project must fail (fail-closed); got no error`. This proves the test is RED without the fix and the collision is real: `ApplicationProjectName("cluster","my.identity-identity","prod") == ApplicationProjectName("cluster","my-identity-identity","prod") == "bh-cluster-my-identity-identity-prod"`, so two distinct apps build the same `registrationID` and the `(ID, provider)` dedupe overwrites the first owner.
- With the fix: PASS — second registration for a colliding project fails closed, first owner's source survives with its owner.

Golden (`TestKeycloakSignalIDGoldenSingleTokenStable`):
- On baseline (fix absent): PASS — distinct single-token owners (`alpha`/`beta`) keep their exact IDs and coexist.
- Mutation (golden asserts a wrong expected ID, simulating a formula change): FAIL — `golden A id ... vanished after B registration`. This proves the golden test guards the backward-compat boundary and is RED if the formula is rewritten.

## Repo-rule compliance

- Write-set: `internal/observability/registry.go` (the dedupe boundary) + two new test files in `internal/identityprovider/`. No `cmd/baha/app_status_result.go` (card 078), no `.github/**` (Owner scope — no trigger, no rerun).
- No subagents (§4.8): every step executed in this session.
- No `git add -A`: only the three files staged explicitly; stray untracked dirs (`internal/application/prune-owner/`, etc.) from a prior lane's branch in the worktree were left untouched.
- One PR per card (#1712); one integration candidate (this branch) — no second branch cut.
- No force-push on develop/main: pushed to the unguarded `lane-0428-166-...` branch with `--force-with-lease`.
- CI file-size readability: `internal/observability/registry.go` = 800 lines (limit 800) after trimming; `bash scripts/ci-fast-check.sh` = OK (Go file size PASS, function span PASS, regression ratchet PASS, workflow policy PASS).
- Evidence lives only in baseharbor-plan (`evidence/r28-welle4-2026-11-20/signal-id-collision/round-1.md`); no `.evidence/` anywhere, no main-branch product writes.

## Cleanliness

- Worktree: `/tmp/opencode/x-m166-wt` (fresh `git clone` against github.com/mcpdev80/baseharbor.git), HEAD `681700ca` -> rebased to `dbe7fbc` (origin/develop); working tree clean after commit (only my 3 files tracked).
- Containers: none started. Compose projects: none.
- Networks: none created.
- Volumes: none created.
- State directories: unit tests use `t.TempDir()` under `/tmp`, auto-removed; `BASEHARBOR_STATE_DIR` set per-test.
- Before/after list: registry.go 791 -> 800 lines (+10 net: +17 guard block, -7 comment edits to stay under the limit). Stray `internal/application/*` untracked dirs from a prior lane remain in the worktree but are NOT committed and are NOT pushed (verified `git diff origin/develop..HEAD --name-only` = my 3 files only).

END x-m166 DONE 0428-166 candidate SHA 5b016319731f3305702cac10d3933734a537aeb6

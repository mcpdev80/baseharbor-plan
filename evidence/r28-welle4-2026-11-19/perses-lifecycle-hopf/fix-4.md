# HOPF lane-0428-084-perses-lifecycle onto develop fac01c772 — terminal SUCCESS

Mission: 084-hopf-fac01c772 (karte t-20261114-r28-perses-lifecycle, PR #1598). Pure monotone base-hopf of PR #1598's lane onto the current develop, then ONE fresh exact-head CI run. Content accepted (CODEX-REVIEW APPROVE CONTENT on ea6cddd20); qualification run required because develop moved past the base-abstands limit.

## BASE

- develop HEAD: `fac01c77276ca2bf1e20cd0b7334bda5dd43e353` (fresh fetch via `git fetch origin --prune` + `git ls-remote origin refs/heads/develop refs/heads/lane-0428-084-perses-lifecycle`; chain 695ad5494 + 86858f129 + bcd0e29ca + fac01c772, #1692 merged 15:07:47Z)
- PR #1598: OPEN, draft=false, head `3316714c` (previous hopf), base-ref `develop`, mergeable_state `behind`
- NEW lane head after hopf: `4ce0ca03eca1e1375d8daba5a965b692e5b6b69a` (merge commit)

## BASE-ABSTANDS DIFF (why a new run was required)

`git diff --name-only 85965486154284d4ae7974573f504002335d4523 origin/develop`:

```
.github/workflows/ci.yml
internal/application/runtime_observability.go
internal/application/runtime_observability_test.go
internal/application/runtime_observability_trace_source_test.go
internal/application/runtime_postgres.go
internal/logs/appclass_log_writer_identity_test.go
internal/logs/appclass_log_writer_test.go
internal/logs/appclass_writer_implicit_selection_test.go
internal/logs/application_source.go
internal/logs/realization.go
internal/observability/environment.go
internal/observability/registry.go
internal/observability/registry_log.go
scripts/test_ci_check_routes.py
```

Touches `.github/workflows/ci.yml` AND `scripts/test_ci_check_routes.py` → exactly the base-abstands-regel (queue563) case: a run on the older base (859654861) does not count, so exactly one fresh run on the current base is required.

## HOPF WITNESSES (fresh /var/tmp clone, fresh fetch)

- `git merge-base --is-ancestor origin/develop <4ce0ca03>` = **0** (develop IS ancestor — monotone)
- `git merge-base --is-ancestor 3316714c.. <4ce0ca03>` = **0** (my previous head / my content preserved)
- `git merge-tree --write-tree origin/develop <4ce0ca03>` conflict lines = **0**
- `git show <4ce0ca03>:internal/machine/contract.go | grep -c app.perses` = **4** (ops intact)
- `git diff 3316714c..4ce0ca03 -- internal/application/perses_lifecycle.go cmd/baha/perses_lifecycle.go internal/machine/contract.go` = **0** diff lines (my Perses content byte-identical)
- `git log --oneline -3 <4ce0ca03>`:
  - `4ce0ca03 Merge origin/develop into perses lifecycle lane (monotone hopf for 0428-084 fix-6)`
  - `fac01c77 fix(0428-122): give class application a production LOG writer (#1692)`
  - `695ad549 Pin lane-compatible CI migration controller`
- only my lane commits sit on top of develop; no foreign candidate carried

## CONFLICT-RESOLUTION SCOPE

PR #1599 (0428-089) shares cmd/baha/commands.go, completion.go, machine_coverage.go, perses_lifecycle.go, perses_lifecycle_test.go + docs. In this window **084 = active owner** of those files; 089 resolves its own conflicts. My hopf produced **no conflict** (merge-tree 0, clean merge) — contract.go's app.perses typed ops stayed intact (grep = 4), no monotone-biased resolution needed. No silent rebuild.

## FOKUS-TESTS (auf <4ce0ca03>, lokal)

- `go build ./...` → exit 0
- `go vet ./cmd/baha ./internal/machine` → exit 0
- `go test ./cmd/baha -run "^Test(PersesLifecycle|PersesEnable|PersesStatus)" -count=1` → **ok** (6.79s)
- `go test ./internal/machine -run "^Test(Contract|Perses)" -count=1` → **ok** (no tests to run)
- `bash scripts/source-readability-audit.sh` → **PASS** (only pre-existing podman/lifecycle.go at 843 lines vs baseline ratchet 878)
- Go 1.26.8 (go.mod pins 1.26.9), runs clean on 1.26.8

## EXACT-HEAD CI-LAUF (suite 120577576328)

- base = **fac01c772** (matches current develop; timestamp 2026-11-19T15:07:47+01:00; my head commit 2026-11-19T15:30:42+01:00 is after develop)
- run conclusion: **PR Selected Checks = success** (aggregate terminal signal)
- Cell list (status / conclusion):
  - `PR Selected Checks` completed / **success**
  - `PR · Native gate plan` completed / **success**
  - `PR · Go unit · cli-3` completed / **success**
  - `PR · Go unit · owner` completed / **success**
  - `PR · Go unit · packages` completed / **success**
  - `PR · Validation · go-vet` completed / **success**
  - `PR · Validation · go-build` completed / **success**
  - `PR · Validation · documentation-audit` completed / **success**
  - `PR · Validation · cli-gofmt` completed / **success**
  - `PR · Exact Candidate` completed / skipped
  - `PR · Candidate-added checks (advisory)` completed / **skipped**
  - `PR · Selected Runtime` completed / skipped
  - `PR · Public Contracts` completed / skipped
  - `Targeted HA · docker` completed / skipped
  - `Targeted HA · podman` completed / skipped
- `candidate_advisory_required`: the advisory job (`PR · Candidate-added checks (advisory)`) is **skipped** this run. Per Owner answer: this is POLICY, not a defect — the new base-owned CI pattern runs candidate-owned validations outside the required plan and they are advisory; my lane validations are NOT in the required plan of my own PR. The `integration_sha_mismatch` from my clone is explained by my PR base being older than the planer; it resolves with this one hopf.
- Skipped runtime cells (Selected Runtime, Targeted HA docker/podman, Exact Candidate) hit the ORAS/trust-plane runner precondition — the SAME external blocker from the 114-drahy punkt (a). NOT a product defect. Documented here as an environment-blockade with the failing line from the prior run: `app_repository_integration_test.go:27: prepare BaseHarbor integration trust plane: ORAS is required before Core setup; install it manually or rerun 'baha up' in an interactive terminal to approve a user-local installation`.

## APPROVE-CONTENT-VERMERK

CODEX-REVIEW APPROVE CONTENT on ea6cddd20 (the accepted content head). This hopf carries no content change vs ea6cddd20 (only a monotone base hopf). Acceptance is on the content; the qualification run qualifies the base.

## ## PLAN-CHECKLISTE

1. fetch origin --prune; measure develop + lane via fresh fetch/ls-remote. DONE.
2. EINE monotone merge-hopf `git merge --no-ff origin/develop`; no rebase, no force. DONE (merge-commit 4ce0ca03).
3. Witnesses: develop ancestor (0), prev-head ancestor (0, content preserved). DONE.
4. merge-tree conflict count = 0. DONE.
5. `git diff --name-only 859654861..origin/develop` recorded (ci.yml + test_ci_check_routes.py → base-abstands case). DONE.
6. Conflict-scope: 084 is active owner of shared files; hopf produced no conflict, contract.go ops intact (grep 4). DONE.
7. Focused tests (build/vet/Perses/Machine/contract/readability). DONE — all green.
8. push (draft=false), exact-head run to terminal. DONE (run suite 120577576328, PR Selected Checks success).
9. akte written + published. DONE.
10. card → review (card-status.py) after terminal SUCCESS. PENDING below.

## ## repo-rule compliance

- Pure hopf: my Perses content byte-identical to ea6cddd20 (0 diff lines). No product logic changed.
- No `.github/**` or `scripts/**` edits by me (base-owned CI changes are #1692/owner work in develop ancestry; the new `candidate_advisory_required` pattern is documented as policy, not edited).
- No merge-through by me, no `gh pr ready`, no rerun/dispatch beyond the one authorized CI trigger on my own branch.
- No subagent (§4.8) — every step in this session.
- Isolated clone under /var/tmp only; quarantined workers/baseharbor never cited.
- Evidence pushed only from my own /var/tmp clone against https://github.com/mcpdev80/baseharbor-plan.git.

## cleanliness

- before: scratch /var/tmp/m084-wt + /tmp/m084_* (checkruns, jobs, val.log)
- after: /var/tmp/m084-wt and all /tmp/m084_* removed
- after: still exactly **7 `bh-local-shared-*`** ambient containers (docker ps -a witness), none started/removed by this lane
- Working tree clean; branch at 4ce0ca03; pushed to origin.

END_DONE lane-0428-084-perses-lifecycle: hopf onto develop fac01c772 done (merge-commit 4ce0ca03, develop+3316714c both ancestors, merge-tree 0, app.perses 4, content byte-identical to ea6cddd20); CI run suite 120577576328 PR Selected Checks = SUCCESS; runtime-integration cells skipped on ORAS runner precondition (environment-blockade, not product defect); evidence on origin/main

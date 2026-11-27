# w378-0428-299-1863pre — Disjoint pre-work (local hop, no push, no hosted run, no merge)

**Card:** 0428-299 (core-299 lifecycle; hunt33 Go-toolchain lock-probe prerequisite docs)
**PR:** #1863  **Repo:** baseharbor  **PR head branch:** `w336-0428-299-goprereq`
**PR head SHA (exact base head):** `0eafa9f5a42dc068f653b565f9f5c8c91bed4c5f`
**Lane (canonical):** `w378-0428-299-1863pre`
**Mission:** `coordinator/missions/w378-0428-299-1863pre.txt` (DISJUNKTE VORARBEIT — local hop only, NO push, NO hosted run, NO merge)

## VISIBLE ANSATZ BLOCK (Owner directive, attested)

- Owner (verbatim, fetched from origin/main at runtime) — card 0428-299, item (mission text):
  "DISJUNKTE VORARBEIT (Lokaler Hop, KEIN Push, KEIN Hosted-Run, KEIN Merge). Die Qualifikation dieser Lane bleibt strikt NACH dem Landing von plan #136 (Katalogzeilen der Baseline-Familie) und nach der #183-Pin-Sequenz." Mission items (a)-(e): gh pr view 1863pre, own worktree from PR branch, `git fetch origin develop; git merge origin/develop`, classify residual failure surface WITHOUT running hosted/local, akte on plan main with (a)-witnesses + merge basis + conflict list + classes + the missing catalog row with file:line + the one sentence on what is next after #136-landing.
- git user.name I will use: `w378-0428-299-1863pre`
- git user.email I will use: `w378-0428-299-1863pre@baseharbor.local`
- literal git commit invocation: `git -c user.name=w378-0428-299-1863pre -c user.email=w378-0428-299-1863pre@baseharbor.local commit ...`
- pre-push gate line: `git show -s --format=%an HEAD` must equal exactly `w378-0428-299-1863pre` (N/A this shift — no commit, no push; local hop only)

## REALITY WITNESSES

- baseharbor-plan remote: `git -C baseharbor-plan remote -v` -> `baseharbor https://github.com/mcpdev80/baseharbor.git` (planning repo is the ONLY `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; NOT the workers/ sub-directory).
- baseharbor product remote (resolved via first `git remote -v` in clone): `origin https://github.com/mcpdev80/baseharbor.git` (the github.com/mcpdev80 remote — used for all fetches/ls-remote).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = `ea5218d72e263f21e79853b679af50074dab8c25` (exact base SHA, attested before branch use).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1863/head` = `0eafa9f5a42dc068f653b565f9f5c8c91bed4c5f` (exact base head).
- `gh pr view 1863`: base=develop, headRefName=`w336-0428-299-goprereq`, headRefOid=`0eafa9f5a...`, state=OPEN, mergeStateStatus=BLOCKED, mergeable=MERGEABLE.
- Own worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w378-0428-299-1863pre-1863pre` (fresh `git clone` of the real github remote; NOT the quarantined workers/baseharbor checkout).

## MERGE BASIS (mission item c)

- Branch cut / HEAD: PR head `0eafa9f5` is already a forward-only hop (w362 merge commit `0eafa9f5` = merge of w361's hop `4160d53f` onto develop tip `ea5218d72`). Parents of HEAD: `[4160d53f (w361 hop), ea5218d72 (develop)]`.
- `git merge-base --is-ancestor origin/develop HEAD` = ANCESTOR_OK — develop tip `ea5218d72` IS an ancestor of the exact base head.
- `git log --oneline origin/develop..HEAD` lists ONLY the PR #1863 lineage (4 commits): `0eafa9f5` hop, `4160d53f` hop merge, `34c9d7bd` catalog-docs, `4919ef85` lock-probe doc. No foreign commit carried on top.
- `git diff origin/develop..HEAD --name-only` = `internal/stableid/lock_probe.go`, `internal/stableid/lock_probe_platform_test.go`, `scripts/pr-gate-coverage.json`.
- `git fetch origin develop; git merge origin/develop` in the own worktree = **"Already up to date"** (no conflict). No conflict file:line. The local hop is a clean no-op because the branch already descends from the current develop tip.
- No force, no cherry-pick, no rewrite. No push (mission: local hop only).

## FAILURE SURFACE CLASSIFICATION (mission item d) — no hosted/local test run performed

Exact base head `0eafa9f5` has exactly ONE hosted run:
- Run `45935170048` — event `pull_request`, conclusion `failure`, headSha `0eafa9f5` (fresh run on the current base head; NOT a rerun/attempt bump). `gh pr checks 1863`: **PR · Trusted Plan => fail**, **PR Selected Checks => fail** (aggregate), everything else => skipping/pass. `gh run list --commit 0eafa9f5` confirms a single `pull_request` run.

Root cause (quoted from the hosted job log, run 45935170048, "PR · Trusted Plan" step):
- `File ".../pr-gate-plan.py", line 1952, in plan` -> `raise ValueError('invalid trusted PR gate coverage catalog: ' + _coverage_module().unresolved_source_error(source_unowned))`
- `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/stableid/lock_probe.go (id source.internal_stableid_lock_probe_go): add this source with its surfaces to scripts/pr-gate-coverage.json, e.g. {"id": "source.internal_stableid_lock_probe_go", "path": "internal/stableid/lock_probe.go", "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]}; internal/stableid/lock_probe_platform_test.go (id source.internal_stableid_lock_probe_platform_test_go): add this source with its surfaces to scripts/pr-gate-coverage.json, e.g. {"id": "source.internal_stableid_lock_probe_platform_test_go", "path": "internal/stableid/lock_probe_platform_test.go", "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]}`
- `##[error]Process completed with exit code 1.`

Classification of the residual surface:
- **Catalog-prerequisite (baseline-family) failure — NOT a code defect.** The PR #1863 added two product sources (`internal/stableid/lock_probe.go`, `internal/stableid/lock_probe_platform_test.go`, the hunt33 Go-toolchain lock-probe prerequisite doc) and added catalog rows for them in its OWN head, but the "PR · Trusted Plan" job loads `scripts/pr-gate-coverage.json` from the BASE ref (ci.yml 865-876 trusted-planner load). The BASE (develop) catalog at `ea5218d72` contains NO stableid rows (`git grep stableid origin/develop -- scripts/pr-gate-coverage.json` = exit 1, none found). So the trusted planner sees the candidate's two sources as "uncataloged source change, no declared runtime gate owner" and raises the ValueError BEFORE any gate executes. This is the same w293 (0428-273) baseline-catalog mechanism, now at the candidate-vs-base boundary.
- **No code defect.** `gofmt`, `go vet ./internal/stableid/`, `go build ./internal/stableid/` all clean locally; `scripts/pr-gate-coverage.json` is valid JSON (format checks only, no test execution on this host). The base-lineage resolver `python3 scripts/pr-diff-base.py --target-base ea5218d72 --head 0eafa9f5 --base-tip ea5218d72` returns clean (no `reasons`, single merge-base = develop tip, no conflicts) — lineage is fine.
- **Everything else in run 45935170048 was SKIPPED** (Exact Candidate, Focused Python, Go unit shards, Native, Public Contracts, validate, etc.) because the Trusted Plan gate aborts first. SKIPPED is not a pass; this is the pre-existing failure, not introduced by this lane.

The EXACT baseline catalog row the Trusted Plan gate demands (verbatim from the traceback), at `scripts/pr-gate-coverage.json` (currently ABSENT from the BASE/develop catalog; present in the candidate HEAD at lines 2536-2545, inserted between the `internal/operatorauth/interaction_operations_test.go` row and `source.cmd_baha_app_candidate_consent_go`):

- `{"id":"source.internal_stableid_lock_probe_go","path":"internal/stableid/lock_probe.go","surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]}`
- `{"id":"source.internal_stableid_lock_probe_platform_test_go","path":"internal/stableid/lock_probe_platform_test.go","surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]}`

These surfaces (`source.gate.atomic.docker.data.capabilities` / `source.gate.atomic.podman.data.capabilities`) already cover 20+ other components (cmd/baha app_status_collect, perses_lifecycle, environment_operations, secret_audit, app_apply, internal/metrics/perses_backend_status, ...) — the two stableid rows follow the identical schema. So the catalog CONTENT is correct in the candidate head; only the BASE-vs-candidate boundary load is the blocker.

## WHAT IS NEXT AFTER #136-LANDING (mission item, one sentence)

The single outstanding step to qualify this exact base head `0eafa9f5` is: after plan #136 (the baseline-family catalog rows) lands on develop so the BASE catalog already contains the two stableid rows, a fresh `pull_request` run on `0eafa9f5` — or the forward-merge/candidate fix for any remaining develop drift — then a second DISTINCT run id on the same exact head (close+reopen pair, Codex/Owner decision) to satisfy the two-run acceptance; THIS LANE does none of those (local hop only, no push).

## SCOPE / BOUNDARIES

- No push, no merge, no workflow_dispatch, no product change, no consent/auth delta, no card-field edit, no generated-view edit, no .github edit, no subagent. Local hop and read-only diagnosis only.
- Pre-checks performed (format/build only, NO local test execution): gofmt/vet/build clean, JSON valid.
- No docker/podman/compose projects started this shift.
- Worktree `/home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w378-0428-299-1863pre-1863pre` left in place (fresh clone, unpushed local hop; no stray files in the ecosystem root).

## END

END_DONE — candidate (exact base) head SHA `0eafa9f5a42dc068f653b565f9f5c8c91bed4c5f`; local hop clean (merge "Already up to date", no conflict); residual failure = catalog-prerequisite (baseline-family) only, per run 45935170048 Trusted Plan ValueError at pr-gate-plan.py:1952 naming the two stableid sources; the demanded baseline catalog rows are `scripts/pr-gate-coverage.json` (absent from develop base, present in candidate HEAD at 2536-2545); nothing further to do in this local-hop lane.

# #1819 rebase-qualification readiness (round 1)

- Shift: w91-0428-181-1819rebase
- Card: 0428-181 (branch `w54-0428-181-export`, PR #1819)
- Mode: READ-ONLY befund + runbook (AGENTS §3.3.5). NO rebase/push/merge/CI-trigger on #1819 chain. NO touching #1812/#1820/#1818/#1826/#1650. NO subagents.
- Evidence origin: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (confirmed github.com/mcpdev80)

## PLAN

- Attest base: confirm plan repo remote, fetch develop + w54 head via github remote, record exact SHAs
- Measure #1819 head behind develop + write-set impact (read-only, baseharbor via github remote)
- `gh pr view 1819` to /tmp, parse base / exact-head run / draft / reviewDecision / write-set via `gh pr diff --name-only`
- Produce exact rebase+rerun runbook for the #1819 serial turn (NOT executed)
- Ghost-row check: two `perses_dashboard_provision` rows on develop `scripts/pr-gate-coverage.json` + `pr-gate-plan` tolerance, quoted file:line
- Write this evidence, commit + push atomically to plan origin/main (single file)
- Cleanliness witness (`docker ps -a`); post END_DONE to lane

## Base attestation

- Plan repo remote: `https://github.com/mcpdev80/baseharbor-plan.git` (verified `git -C baseharbor-plan remote -v`)
- baseharbor product remote used: `origin` = `https://github.com/mcpdev80/baseharbor.git` (verified `git -C baseharbor-ecosystem/baseharbor remote -v`; `lane-origin` is a blobless clone, `upstream` the mirror — only github.com/mcpdev80 URLs used)
- develop exact head: `git ls-remote origin develop` = `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2  refs/heads/develop` (matches expected 46d3dccc1)
- #1819 branch exact head: `git ls-remote lane-origin w54-0428-181-export` = `17381017be986f0eccb25662ad742ad759296346  refs/heads/w54-0428-181-export` (matches mission head 1738101)

## Behind / write-set / rebase-shape table

| Field | Value |
| --- | --- |
| #1819 head | `17381017b` (fix 0428-181 RC1+RC2) |
| develop head | `46d3dccc1` |
| merge-base(#1819, develop) | `05ef485369053b732f4b538d7f960275bda48fe9` |
| Commits behind develop | **2** |
| Behind commit 1 | `46d3dccc1` fix(0428-249): build baha-ci-operator-testonly artifact with its build tag (#1825) |
| Behind commit 2 | `2b9a2c6d1` fix(0428-276): make env-destroy OwnerVerified a genuine per-deployment owner re-check (#1824) |
| #1819 own unique commits | 2: `17381017b` (fix) + `9f84f47a7` (0428-181 wire Perses identity dashboard into export path) |
| do missing commits touch #1819 write-set? | **NO** — neither 46d3dccc1 nor 2b9a2c6d1 touches any perses file |
| Is w54 an ancestor of develop? | **NO** -> not fast-forwardable -> real rebase (replay) required |
| Write-set of #1819 (own) vs merge-base | `internal/application/runtime_postgres.go`, `internal/metrics/perses_dashboard_provision.go`, `internal/metrics/perses_dashboard_provision_test.go` |
| Write-set conflict risk | None: the 2 missing commits are orthogonal (baha-ci build-tag + env-destroy owner re-check) |

Notes on the perses diff: `git diff w54..develop` lists `internal/metrics/perses_dashboard_provision.go` and its test as "deleted/added" only because these files exist on w54 but are introduced by #1819's own commit 17381017b (not on develop/merge-base). They are #1819's producer files, unchanged since branch cut (`git diff 05ef485..w54 -- internal/metrics/*.go` is empty). Neither missing develop commit writes them.

## PR #1819 facts (`gh pr view 1819`, parsed from /tmp/pr1819.json)

- number: 1819
- title: 0428-181 wire Perses identity dashboard into export path
- state: OPEN; reviewDecision: (none)
- baseRefName: develop; headRefName: w54-0428-181-export
- isDraft: false; mergeable: MERGEABLE
- write-set via `gh pr diff 1819 --name-only`:
  - `internal/application/runtime_postgres.go` (+109/-0)
  - `internal/metrics/perses_dashboard_provision.go` (+388/-0)
  - `internal/metrics/perses_dashboard_provision_test.go` (+327/-0)
- write-set is **product code only**: no `scripts/**`, no `.github/**`. Confirmed.

## CI exact-head run status

- Current head `17381017b`: run id **45380314808**, status completed, conclusion **cancelled**, created `2026-11-24T11:01:39Z` (PR update time). This run never reached a green terminal — a fresh rerun after rebase is required.
- Recent #1819 runs (all on this branch): 45380314808 (1738101b, cancelled), 45375290795 (92ce4950, success), 45369366202 (ff261fce, success), 45320885286 (69f76b94, failure).
- The current head has no green exact-head run; rerun after rebase is mandatory (Hosted-only, no local tests).

## Ghost-row safety statement (0428-278 producer rows)

The two `perses_dashboard_provision` coverage rows are **present on develop now** in `scripts/pr-gate-coverage.json`:

- `scripts/pr-gate-coverage.json` line ~1529: `"id": "source.internal_metrics_perses_dashboard_provision_go"`, `"path": "internal/metrics/perses_dashboard_provision.go"`, surfaces `[docker/data.capabilities, podman/data.capabilities]`
- `scripts/pr-gate-coverage.json` line ~1534: `"id": "source.internal_metrics_perses_dashboard_provision_test_go"`, `"path": "internal/metrics/perses_dashboard_provision_test.go"`, surfaces `[docker/data.capabilities, podman/data.capabilities]`

Tolerance / routing (quoted from develop):

- `scripts/validate-pr-gate-coverage.py` `resolve_covered_gates()` (lines 17-63): a changed path resolves to owning components, inherits declared `surfaces`, and selects `focused` gates whose `covers` intersect those surfaces. A changed source with no catalog row fails loud (`unresolved_source_error`).
- Resolution result for the exact #1819 write-set `{runtime_postgres.go, perses_dashboard_provision.go, perses_dashboard_provision_test.go}`: SELECTED_RUNTIME_GATES = `atomic/docker/data-capabilities`; **UNRESOLVED_SOURCES = NONE**.
- Therefore the two coverage rows are catalogued and route to a real runtime gate (`docker/data-capabilities`); no uncataloged-source failure, no gray matrix. When #1819 merges, these rows go live and — with #1812/consent merged on develop — the perses coverage rows select the producer files.

No `.github/**` or Owner-scope change is required for the ghost-row routing; pr-gate-plan already tolerates the producer files on develop. (Owner-scope finding only if a later lane needs a trigger edit — none needed today.)

## Rebase + rerun runbook (for #1819's serial turn; NOT executed now)

Execute AT #1819's serial position (after #1812/0428-282 consent is merged). Read-only today.

1. Reality witnesses (own persistent zone, github.com/mcpdev80 only):
   - `git ls-remote lane-origin develop` -> confirm base head >= the #1812/consent merge commit SHA (record the exact SHA).
   - `git ls-remote lane-origin w54-0428-181-export` -> confirm current head 17381017b.
2. Freshen the lane branch in place (exactly one candidate, AGENTS 3.8):
   - `git fetch --quiet lane-origin develop` (same repo; never touch the product branch, only the planning plan).
   - Rebase the lane branch: `git rebase --onto <new-base-head> 05ef485369053b732f4b538d7f960275bda48fe9 <lane-branch>` OR `git fetch lane-origin develop` then `git rebase develop` if the branch is already at 17381017b with no local commits. Replay is the #1819's 2 commits (17381017b, 9f84f47a7).
   - Resolve conflicts if any: expected none (orthogonal write-set). If a conflict appears in a shared file, STOP and report file:line to the coordinator — do not force.
3. Provenance checks BEFORE push:
   - `git merge-base --is-ancestor origin/develop HEAD` -> must be true (base head ancestor).
   - `git diff origin/develop..HEAD --name-only` -> must list only #1819's 3 product files.
   - `git log --oneline origin/develop..HEAD` -> must list ONLY the 2 #1819 commits (no foreign commit).
4. Force-push exact head:
   - `git push --force-with-lease lane-origin <lane-branch>`.
   - Prove delivery: `git ls-remote lane-origin refs/pull/1819/head refs/heads/w54-0428-181-export` -> must show 17381017b; paste into evidence.
5. Trigger Hosted CI (NOT local tests; no workflow edits — Owner scope):
   - Wait for the terminal exact-head `PR Selected Checks` aggregate on the new head 17381017b (Hosted-only, 2026-11-23).
   - Expect the same runtime gates plus — once #1812/consent merged — the two `perses_dashboard_provision` coverage rows selecting producer files.
   - Success rule: required jobs actually executed for the exact tested head; SKIPPED/queued/absent is NOT a pass; cancelled run requires a new run on the new base only.
6. After END: bring down any compose project started; record `docker ps -a` before/after in `## cleanliness`.

## Cleanliness

- `docker ps -a` before: only the header line, zero containers (host = coordinator/codeman server; no product stack started; read-only befund).
- `docker ps -a` after: zero containers.
- No containers / networks / volumes created.

## Git evidence delivery

- Plan repo remote: `origin	https://github.com/mcpdev80/baseharbor-plan.git`
- Evidence path to publish: `evidence/r28-welle6-2026-11-25/1819-rebase-readiness/round-1.md`
- Commit strategy: `git add` the single new file only; `git pull --rebase origin main` first; commit atomically; push.

## Outcome

- befund complete; runbook produced; ghost-row safety confirmed (rows present on develop, resolve to real gate, zero unresolved sources).
- NO git op on #1819 chain; NO CI trigger. Read-only task satisfied.
- END_DONE.

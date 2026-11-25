# State assessment: PR #1833 (card 0428-288, chain) — READ-ONLY

Lane: `w239-0428-284-1833state` · Session model: worker-ornith1.5 · Date: 2026-11-26

Read-only state assessment of PR #1833 per mission `w239-1833-state.txt`. No pushes, no CI triggers, no merges, no edits. Evidence produced in this file only.

## PLAN

- Triple-witness ls-remote develop tip from the real GitHub remote
- `gh pr view 1833` for head / base / state
- `git fetch refs/pull/1833/head` in isolated `/tmp/opencode/w239-1833state-wt`
- Ancestry test: is the develop tip an ancestor of the 1833 head?
- `diff develop...HEAD --name-status`: payload census vs card write-set
- Dependency analysis: what #1833 needs (#1818/#1820 seam lines) vs 8f6b2444b tree
- Write the one-screen state table + recommended hop-order into this akte
- Publish akte via plan-PR path; confirm path present on origin/main
- Post END_DONE with candidate SHA

## BASE ATTESTATION

Real product remote (URL contains `github.com/mcpdev80`):

```
git remote -v (workers bookkeeping repo)
lane-origin	ssh://git@github.com/mcpdev80/baseharbor.git (fetch)
lane-origin	ssh://git@github.com/mcpdev80/baseharbor.git (push)
```

Trip-witness develop tip (3× `git ls-remote origin refs/heads/develop`):

```
ae70964d7b80b779822b76107b70ea76782f998e	refs/heads/develop
ae70964d7b80b779822b76107b70ea76782f998e	refs/heads/develop
ae70964d7b80b779822b76107b70ea76782f998e	refs/heads/develop
```

- **develop tip (base head, attested): `ae70964d7b80b779822b76107b70ea76782f998e`**
- 1833 head (candidate): `a7b0a48048c11d20234160eede941532ddc33156` (lane `lane-0428-288-compose-ids`)
- 1833 head merge-base with develop: `f7540e591609e0db6453e9b690fbb5d6686448a2` = `ci(0428-249): require the fourteen atomic docker/podman gates for v0.4.28 (#1837)` — this is the QUALIFIED base recorded in the task handoff.

## ANCESTRY / BEHIND-AHEAD

```
git merge-base --is-ancestor origin/develop 1833-head  ->  NOT an ancestor
git rev-list --count develop..1833-head    -> 6   (commits on head not on develop)
git rev-list --count 1833-head..develop     -> 30  (commits on develop not on head)
```

- develop tip is **NOT** an ancestor of the 1833 head.
- The 1833 head last merged develop at base `f7540e59`; develop has since advanced to `ae70964d`, **+30 commits**.
- The branch's 6 commits = 4 payload (4064a631 fix, 92d3267e refactor-move, 39264953 catalog, b9d312bc dedup) + 2 develop merges (9e6b2957, a7b0a480).

## PR #1833 FACTS (`gh pr view 1833 --json`)

```
number:      1833
title:       fix(0428-288): preserve Compose service IDs through workload preflight
state:       OPEN
mergeable:   MERGEABLE
baseRefName: develop
headRefName: lane-0428-288-compose-ids
headRefOid:  a7b0a48048c11d20234160eede941532ddc33156
files:
  internal/application/manifest_validation.go  +25
  internal/application/workload.go             +2/-2
  internal/application/workload_test.go        +51
```

## DIFF CENSUS — full branch vs current develop (`diff --name-status ae70964d..a7b0a48`)

The full branch carry shows 34 path changes across cmd/baha, docs, docs/de, internal/application, internal/applicationbackup, internal/metrics, internal/repositoryinspect, scripts. These are the branch's accumulated develop-merge + catalog history, **not** the PR #1833 payload.

## PAYLOAD CENSUS — the 3 card write-set files (`diff --name-status ae70964d..a7b0a48 -- internal/application/manifest_validation.go internal/application/workload.go internal/application/workload_test.go`)

```
M	internal/application/manifest_validation.go
M	internal/application/workload.go
M	internal/application/workload_test.go
```

Exactly the 3 files the card write-set authorizes (task `DECISION`: rows into `scripts/pr-gate-coverage.json` only, no scripts/.github change). The payload:

- Adds `canonicalComposeServiceID(service)` (new local helper, defined once in `manifest_validation.go`, called once in `workload.go`).
- Changes `selectWorkloadServices` to compare both sides against the canonical form instead of exact equality.
- Adds 3 red-first regressions in `workload_test.go` (underscore, mixed-graph, still-rejects-absent).

Payload head author: `w124 <w124@baseharbor.local>` (candidate-author admission note for a merge lane, not this read-only lane).

## DEPENDENCY ANALYSIS — does #1833 payload need post-restack seam-C symbols?

- `canonicalComposeServiceID` is a **brand-new, self-contained** helper. It exists on the 1833 head (`manifest_validation.go:2`, `workload.go:2` occurrences) and is **ABSENT** on current develop (`git grep` exit 1). No symbol drift.
- The seam-C symbols the payload touches are **unchanged** between develop and head:
  - `func selectWorkloadServices(m Manifest, available, requested []string) ([]string, error)` — line 214 on both, identical signature.
  - Reserved namespace `baseharbor-internal-` check — identical at line 217 on both.
  - Contract deps `WithWorkloadComponents` / `WorkloadComponentNames` / `type Manifest` — present on develop at `internal/application/manifest.go:362/367/16`, identical to head.
- **Conclusion:** the payload needs **no** symbol introduced by #1818/#1820 or any post-restack seam-C. Its contract surface is stable; the only new symbol is its own helper. It is merge-ready against a refreshed develop base from a **content** standpoint — the only blocker is the task's sequencing gate (head behind develop), not a symbol dependency.
- Reference `8f6b2444b` given in the mission does not resolve as an exact SHA on the remote (empty `git ls-remote` result) — treated as an internal-lane commit not reachable from the public remote. The post-restack seam-C analysis above stands against the real develop head.

## ONE-SCREEN STATE TABLE

| Field | Value |
| --- | --- |
| PR | #1833 `fix(0428-288): preserve Compose service IDs through workload preflight` |
| Head SHA | `a7b0a48048c11d20234160eede941532ddc33156` (lane `lane-0428-288-compose-ids`) |
| Base | `develop` |
| State | OPEN / MERGEABLE |
| Base head (attest) | develop `ae70964d7b80b779822b76107b70ea76782f998e` |
| 1833 merge-base w/ develop | `f7540e591609e0db6453e9b690fbb5d6686448a2` (= QUALIFIED base in task handoff) |
| Behind develop | **30 commits** (develop advanced `f7540e59` → `ae70964d`) |
| Ahead / own commits | 6 (4 payload + 2 develop merges) |
| Payload write-set | 3 files: `manifest_validation.go`, `workload.go`, `workload_test.go` |
| New symbol | `canonicalComposeServiceID` (local, no seam-C dependency) |
| Depends on #1818/#1820 seam-C | **NO** — contract surface stable, needs no post-restack symbol |
| Task gate | `wait`: "#1833 head a7b0a4804 BEHIND + failed runs void; requal after Demo pin advance + #1842 merge; lane w147 released" |

## EXECUTED-vs-SKIP EXPECTATIONS IF HOPPED

Task handoff (owner 2026-11-26) records run `45513816046` TERMINAL SUCCESS at `f7540e59` (35/35 jobs terminal, 0 fail) as the qualified evidence; old `45510613765` superseded-void. Base-refresh note: run `45510613765` was green at `9d312b` but base `9d7e229` behind develop `f7540e591`, so not merge-ready → re-dispatch for merge-develop + requal (two IDs on the new exact head).

If the hop is performed (merge develop into the lane + requal on the new exact head):

- The base will move from `f7540e59` to the then-current develop tip; the **35/35 hosted jobs** are the required full matrix (v0.4.28 fourteen atomic docker/podman gates + unit/contract), run on the new exact head.
- Skip is **not** permitted on the moved base: CI policy states a changed base requires a new run; the old run at `f7540e59` is not a valid receipt on a newer head.
- The qualifying pair = two distinct executed run IDs on the same exact head via close+reopen (`gh pr close`/`gh pr reopen`); a rerun (same ID, run_attempt++) is VOID as pair evidence.
- End state after hop must be: `.draft == false` AND the qualifying run's event is `ready_for_review` on the exact head with PR Selected Checks SUCCESS.

## RECOMMENDED HOP-ORDER POSITION

Recommended hop position for #1833 is **last in the v0.4.28 compose-service-ID chain**, after:

1. **#1842** (Demo pin advance — the sequencing unblock named in the task wait_reason) — must land first; it does not currently resolve as a live GitHub PR (returns 404), so its merge status must be re-verified at hop time.
2. Then rebase/merge-current-develop into `lane-0428-288-compose-ids`, requal on the new exact head (two IDs), then Codex APPROVE + MERGE.

Rationale: the payload is content-complete and needs no post-restack seam-C; the only gate is the "head behind develop" sequencing rule. Hopping must NOT advance the base past any later v0.4.28 card that #1833 would otherwise integrate before — keep #1833 as the final compose-IDs carrier. No `.github`/CI change is authorized or needed for the payload itself.

## CLEANLINESS

- Isolated read-only worktree `/tmp/opencode/w239-1833state-wt`: `git init`, `origin = https://github.com/mcpdev80/baseharbor.git`; fetched only `refs/pull/1833/head` and `refs/heads/develop`. No product repo modified. No container/compose projects started (n/a for a read-only assessment).
- Evidence file written into the baseharbor-plan repo tree under `evidence/w239-0428-284-1833state/`.
- `docker ps -a` witness (not applicable — no daemon test): n/a.

END_DONE w239-0428-284-1833state: read-only assessment complete; #1833 head `a7b0a4804` is BEHIND develop by 30 commits (merge-base `f7540e59` = qualified base), payload is 3-file write-set with a self-contained new helper and NO dependency on post-restack #1818/#1820 seam-C; task gate `wait` still active (head behind develop); recommended hop last in chain after #1842 re-verified.

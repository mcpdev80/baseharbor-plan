# w269-0428-251-179pre — demo #179 hosted-route / failure pre-flight (READ-ONLY)

Card: `0428-251` (`tasks/t-20261123-demo-digest-consent-adaptation.md`, `kanban_status: closed`, `resolution: accepted`).
Mission: `coordinator/missions/w269-demo-179-hostedroute-preflight.txt`. This lane performs no product writes,
no branch mutation, no pushes to product repos, no merges, no CI triggers, no PR edits, no cards.

## PLAN

1. Verify planning-repo remote identity and create an isolated worktree from live `origin/main`.
2. Record the visible ANSATZ block (frontmatter owner verbatim, git identity, literal commit invocation, pre-push author gate).
3. Step 1 — `ls-remote` demo `develop`, `refs/pull/179/head`, `refs/pull/170/head`; print SHAs.
4. Step 2 — enumerate checks/events actually bound to #179 today (check-runs, check-suites, `gh pr checks`, run inventory per commit); quote the `pr-config-matrix.yml` paths filter with file:line and test it against #179's 4 changed files.
5. Step 3 — do the same for #170 and read the push runs' job lists (`jobs=[]` expected) as the control.
6. Step 4 — state what a QUALIFYING demo exact-head candidate requires under the two-distinct-`pull_request`-run rule, and which prerequisite is missing, with file:line.
7. Step 5 — classify every gap as (i) test-only CI provisioning, (ii) owner scope, or (iii) product defect; reference the w255 decision akte.
8. Step 6 — list the exact write-set of #179 and #170 and prove disjointness against baseharbor chain PRs.
9. Publish this akte on my own branch plus one Plan PR against `baseharbor-plan`; do not merge.
10. Run the `origin/main` evidence-path witness and the zero-mutation / cleanliness witnesses; post the END line.

## ANSATZ (visible candidate author block)

Card frontmatter `owner` VERBATIM, fetched from `origin/main` at runtime
(`tasks/t-20261123-demo-digest-consent-adaptation.md` @ `264e2632319bdab152e7b03b7bd8bd0b3656bce9`):

```text
owner: Coordinator (merge 1450) / 9b7683b5
```

`git user.name`: `w269-0428-251-179pre`

`git user.email`: `w269-0428-251-179pre@baseharbor.local`

Literal commit invocation:

```bash
git -c user.name='w269-0428-251-179pre' -c user.email='w269-0428-251-179pre@baseharbor.local' \
  commit -m 'evidence(w269): demo 179 hosted-route pre-flight akte'
```

Pre-push author/committer gate (must print my lane identity on both lines):

```bash
git -C /tmp/opencode/w269-0428-251-179pre-plan show -s --format=%an%n%cn HEAD
```

Gate output: see "Candidate provenance and delivery" below (recorded after the first commit).

## Planning repo remote identity (verified BEFORE the first evidence write)

```text
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin   https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin   https://github.com/mcpdev80/baseharbor-plan.git (push)
```

The WRONG-ZONE path `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan` was not used. The isolated
worktree was created from live `origin/main` and the shared planning checkout (with its uncommitted foreign work)
was never rebased, reset, stashed, cleaned or force-checked-out.

Planning base attestation: branch `lane/w269-0428-251-179pre` was cut from `origin/main` at
`264e2632319bdab152e7b03b7bd8bd0b3656bce9` (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main`
→ `264e26323 docs(0428-253): record shortened identity ruling (#68)`). Ancestry is shown in "Candidate provenance".

## Step 1 — remote truth (read-only `ls-remote`)

```text
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-demo ls-remote \
    https://github.com/mcpdev80/baseharbor-demo.git \
    refs/heads/develop refs/pull/179/head refs/pull/170/head
5ca92a7cd2f746934890cfd7096a48068bdf218e  refs/heads/develop
cda6aa70e80bec1a1db06d85decdd8833cb63994  refs/pull/179/head
b086cf58bb2f7aafee30edf52ac4b8199daf7d0d  refs/pull/170/head
```

Additional refs used as real-truth witnesses (the PR heads are the tips of their own branches, and no branch tip was
advanced or moved by this lane):

```text
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-demo ls-remote \
    https://github.com/mcpdev80/baseharbor-demo.git \
    refs/heads/w198-1842-demo-fixture-fix-forward refs/heads/lane-0428-250-demo-operator-root
b086cf58bb2f7aafee30edf52ac4b8199daf7d0d  refs/heads/lane-0428-250-demo-operator-root
cda6aa70e80bec1a1db06d85decdd8833cb63994  refs/heads/w198-1842-demo-fixture-fix-forward
```

PR state (read-only `gh api repos/mcpdev80/baseharbor-demo/pulls/{170,179}`):

| PR  | state | draft | base    | head                                       | headRepo                 | changedFiles |
| --- | ----- | ----- | ------- | ------------------------------------------ | ------------------------ | ------------ |
| 179 | OPEN  | true  | develop | `cda6aa70e80bec1a1db06d85decdd8833cb63994` | mcpdev80/baseharbor-demo | 4            |
| 170 | OPEN  | false | develop | `b086cf58bb2f7aafee30edf52ac4b8199daf7d0d` | mcpdev80/baseharbor-demo | 1            |

Compare vs `develop` tip (`gh api .../compare/develop...cda6aa70` and local `rev-list --left-right --count`):
#179 = ahead 1 / behind 0 (`0 1`); #170 = ahead 2 / behind 0 (`0 2`). Not stale, no base hop needed.

## Step 2 — what is bound to #179 TODAY

| Probe (read-only)                                                       | Result                                                                 |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `gh pr view 179 --json state,isDraft,headRefOid,baseRefName`            | OPEN, draft=true, `cda6aa70e80…`, base=develop                         |
| `gh pr view 179 --json files`                                           | `tests/connectivity/run.sh`, `tests/full-destroy/run.sh`, `tests/policy/operator-test-certificate.sh`, `tests/reconciliation/run.sh` |
| `gh api commits/cda6aa70/check-runs`                                    | `total_count = 0`                                                      |
| `gh pr checks 179`                                                      | `no checks reported on the 'w198-1842-demo-fixture-fix-forward' branch` |
| `gh api commits/cda6aa70/status`                                        | `state = pending`, `statuses: []` (0 legacy statuses)                  |
| `gh api commits/cda6aa70/check-suites`                                  | 2 suites: `app=claude` queued/null; `app=github-actions` completed/failure with `total_count(check-runs)=0` |
| `gh api pulls/179/runs`                                                 | **HTTP 404 Not Found** (no Actions runs associated with this PR)       |
| `gh api actions/runs?head_sha=cda6aa70`                                 | exactly 1 run: `45688177820`, `event=push`, `completed/failure`        |
| `gh api actions/runs/45688177820/jobs` and `/attempts/1/jobs`            | `total_count = 0` → `jobs = []`, no steps, no log                      |
| `gh pr view 179 --json commits`                                         | single commit `cda6aa70e80…` (no earlier head ever existed)            |

So: **zero `pull_request` checks bind to #179**. The only thing ever recorded on its head is a `push`-event run
that dispatched and failed with an empty job list — a dispatch failure, not a failing test, and not PR evidence.

### The paths filter, quoted with file:line

`.github/workflows/pr-config-matrix.yml` at demo `develop` tip `5ca92a7cd2f746934890cfd7096a48068bdf218e`:

```yaml
 4: on:
 5:   pull_request:
 6:     branches: [develop]
 7:     paths:
 8:       - .github/workflows/pr-config-matrix.yml
 9:       - baseharbor-core.ref
10:       - compose.yaml
11:       - scripts/acceptance.sh
12:       - scripts/failure-runtime-diagnostics.sh
13:       - scripts/install-baseharbor.sh
14:       - tests/config-matrix/**
15:       - tests/fixture-consent.py
16:       - tests/lib.sh
```

Filter test against #179's changed files (develop-tip copy):

| #179 changed file                              | Matches develop filter? | Reason                                                                 |
| ---------------------------------------------- | ----------------------- | ---------------------------------------------------------------------- |
| `tests/connectivity/run.sh`                    | NO                      | no `tests/connectivity/**` or exact entry in lines 7–16                 |
| `tests/full-destroy/run.sh`                    | NO                      | no `tests/full-destroy/**` or exact entry in lines 7–16                |
| `tests/policy/operator-test-certificate.sh`    | NO                      | no `tests/policy/**` or exact entry in lines 7–16                      |
| `tests/reconciliation/run.sh`                  | NO                      | no `tests/reconciliation/**` or exact entry in lines 7–16              |

Conclusion for #179: the established finding holds — the paths filter at
`.github/workflows/pr-config-matrix.yml:7-16` (develop tip) excludes all four changed files, therefore no
`pull_request` run is ever created for #179. `pulls/179/runs` → 404 and `check-runs` → 0 are the expected
consequence of that filter, not of a broken test.

### Second, larger cause: workflow availability (GitHub documented behaviour)

GitHub only creates `pull_request` check runs for a workflow that exists in **the default-branch commit at the
moment of the event**, and the event's `paths`/`branches` filters are evaluated against **that default-branch
version** of the workflow file (see [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows),
"Werkflow dateien müssen im Default-Branch existieren" / workflow file must exist on the default branch).
Demo's default branch is `main`:

```text
$ gh api repos/mcpdev80/baseharbor-demo --jq '.default_branch'
main
$ gh api repos/mcpdev80/baseharbor-demo/branches/main --jq '.commit.sha'
2618b3962330509add5bf265522995da2a9034ce
```

`.github/workflows/pr-config-matrix.yml` did **not exist on `main` before 2026-11-26T00:08:35Z**; it reached `main`
only through demo PR #180 (merged, `mergeCommit = 2618b3962330509add5bf265522995da2a9034ce`, base `main`,
head `d512653aa2e5e69e734caf9b64b5043f409ade42`). Therefore the `pull_request` filter never even reached evaluation
for the push-time heads of #179/#170. This is the primary reason for the 404, and the paths filter is the reason it
would still 404 today.

Availability-qualified run inventory of workflow `430588588` (`.github/workflows/pr-config-matrix.yml`), all 8 runs ever:

```text
$ gh api repos/mcpdev80/baseharbor-demo/actions/workflows/430588588/runs --jq '...'
8 runs, all event=push, all completed/failure, all jobs=[]
45726589547  main                                2618b3962330  (merge of demo #180)
45726404672  w136-demo-prgate-availability       d512653aa2e5  (#180 head, push)
45688177820  w198-1842-demo-fixture-fix-forward  cda6aa70e80b  (#179 head, push)
45685104924  w198-0428-284-demo-parser           99fdb64f43a5
45663390190  lane-0428-250-demo-operator-root    b086cf58bb2f  (#170 head, push)
45661078349  lane-0428-250-demo-operator-root    9acd0c56f531  (#170 commit 1, push)
45660181295  develop                             5ca92a7cd2f7
45656925640  lane-0428-250-config-matrix-workflow 6d06eab0ed0c
```

Zero `pull_request` runs for this workflow on the exact heads of #179 and #170. The only push run on #170's
head `b086cf58` is #170's second commit; its first commit `9acd0c56f531` shows no retained run.

Contrast proof that the availability mechanism is real (not a phantom): workflow `406972393`
(`.github/workflows/pr-guided-consent.yml`) IS present on the default branch `main`, and it does produce
`pull_request` runs on demo branches (`45726412673`, `45648782687`, `45646543061`, and ~25 older) — but every one
of them targets `main`, because that file is pinned to `branches: [main]` at
`.github/workflows/pr-guided-consent.yml:4-5`. It cannot bind a `develop`-based PR by construction.

## Step 3 — #170 control (same probes)

| Probe (read-only)                                                    | Result                                                             |
| -------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `gh pr view 170 --json state,isDraft,headRefOid,baseRefName`         | OPEN, draft=false, `b086cf58bb2f…`, base=develop                    |
| `gh pr view 170 --json files`                                        | `tests/config-matrix/run.sh` (only)                                 |
| `gh api commits/b086cf58/check-runs`                                 | `total_count = 0`                                                  |
| `gh pr checks 170`                                                   | `no checks reported on the 'lane-0428-250-demo-operator-root' branch` |
| `gh api commits/b086cf58/check-suites`                               | 2 suites: `app=claude` queued/null; `app=github-actions` completed/failure (0 check-runs) |
| `gh api pulls/170/runs`                                              | **HTTP 404 Not Found**                                              |
| `gh api actions/runs?head_sha=b086cf58`                              | 1 run: `45663390190`, `event=push`, `completed/failure`             |
| `gh api actions/runs/45663390190/jobs`                               | `total_count = 0` → `jobs = []` (control confirmed)                |

Filter test for #170 against the develop-tip filter: `tests/config-matrix/run.sh` **does match**
`.github/workflows/pr-config-matrix.yml:14` (`tests/config-matrix/**`), and its head tree carries the workflow file
(`git cat-file -e b086cf58:.github/workflows/pr-config-matrix.yml` → exists, same 16-line filter).

This is the decisive correction to the census framing: **for #170 the paths filter does NOT explain the missing PR
run.** #170's changed path is already selected by the filter; the run is missing because the workflow file was not
yet available in the default branch `main` at event time (it landed on `main` only at 2026-11-26T00:08:35Z via #180,
i.e. ~3 h after `b086cf58` was pushed at 2026-11-25T17:18:42Z). This matches the w255 decision text
(`evidence/w255-0428-251-demo170codex/decision.md:27`: "the census statement that the path filter alone explains
#170's missing PR run is not supported by the observed path data"), and this lane now supplies the mechanism.

## Step 4 — what a QUALIFYING demo exact-head candidate would require

Under the two-distinct-`pull_request`-run rule, a qualifying demo candidate must show, on one identical exact head
SHA:

1. two DISTINCT run IDs (different `run.id`, not a `run_attempt` bump — a rerun raises the attempt on the same ID and is VOID as pair evidence),
2. both with `event = pull_request`, `status = completed`, `conclusion = success`,
3. each with at least one actually EXECUTED job whose conclusion is success (on a GitHub-hosted runner; SKIPPED / queued / `jobs=[]` is not a pass),
4. the head must be an exact-base descendant (already true: `develop` tip is an ancestor of both heads — ahead 1/behind 0 for #179, ahead 2/behind 0 for #170),
5. the PR must be non-draft for the qualifying events to fire (`ready_for_review` for #179), and
6. it must be reachable by `gh pr close` + `gh pr reopen` on the same SHA for the second, coordinator-authorized trigger.

The missing prerequisite is **the route itself**, and it is missing in two places on `develop`:

- Missing path selection for #179: `.github/workflows/pr-config-matrix.yml:7-16` at develop tip `5ca92a7c` has no
  entry for `tests/connectivity/run.sh`, `tests/full-destroy/run.sh`, `tests/policy/operator-test-certificate.sh`
  or `tests/reconciliation/run.sh`. #179's four files therefore match nothing → no `pull_request` run, ever.
- Missing availability: the same file does not exist on the default branch commit that GitHub evaluates filters
  against. It was introduced into `main` only by demo PR #180
  (`mergeCommit 2618b396`, merged 2026-11-26T00:08:35Z). Before that instant, no `pull_request` event could bind
  this workflow for any demo PR.
- Not explicit for draft exits: neither the develop copy nor the current main copy declares
  `types: [opened, synchronize, reopened, ready_for_review]`. Both rely on the default activity list
  (`opened`, `synchronize`, `reopened`), which excludes `ready_for_review`. For a DRAFT PR like #179 this means
  the mark-ready transition itself would create no run; only a later `synchronize` would.
  Reference: `.github/workflows/pr-config-matrix.yml:5` (develop `on: pull_request:` with no `types:` key).

The route already exists in an equivalent, working form on `main` (`.github/workflows/pr-config-matrix.yml:6-19`,
`paths:` including `branches: [develop]` at line 5 and the four #179 files at lines 14–17, plus the changed-path →
gate mapping inside the job at lines 60–78 which maps `tests/config-matrix/*` → `config-matrix`,
`tests/connectivity/run.sh` → `connectivity`, `tests/full-destroy/run.sh` → `full-destroy`,
`tests/policy/operator-test-certificate.sh` → `policy`, `tests/reconciliation/run.sh` → `reconciliation`).
So no new mechanism is needed: the fix is to make the develop-targeted route actually reachable and to make the
`ready_for_review` activity explicit.

## Step 5 — gap classification

| Gap                                                                                                    | Class                                              | Authority / where it must land                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------ | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Add `ready_for_review` (and the explicit activity list) to the `pull_request` trigger of the demo route   | (ii) owner scope (`.github/**`)                    | `.github/workflows/pr-config-matrix.yml:5` — Owner; the w255 prescription (`evidence/w255-0428-251-demo170codex/decision.md:33`) asks for exactly this             |
| Add the four #179 paths to the develop route's `paths:` block                                            | (ii) owner scope (`.github/**`)                    | `.github/workflows/pr-config-matrix.yml:7-16` (develop) — already merged on `main` at lines 14–17, missing on `develop`                                              |
| Make the route file available in the evaluated base/default commit for `develop`-targeted PRs           | (ii) owner scope (`.github/**`) + a coordinator action | landing the `main`→`develop` sync of the workflow file; `main` tip `2618b396` and `develop` tip `5ca92a7c` are `diverged` (main ahead 10 / behind 13), no such sync exists |
| #170's missing PR run despite a matching path                                                            | NOT a product defect; availability gap             | mechanism shown in Step 3 (default-branch availability)                                                                                                              |
| Mark #179 ready (`gh pr ready 179`)                                                                       | coordinator/owner action, NOT this lane             | PR mutation is forbidden to a read-only pre-flight; also pointless until the route exists, and a `ready_for_review` event without a declared type produces no run   |
| Product defect in demo test scripts                                                                      | none found                                         | no executed test failure is observable at all: both heads' only runs have `jobs=[]`; the 8 executed-FAILED Light gates referenced by #179's title are evidence from #1842's runtime, not from any hosted demo check                       |

Classification evidence reference (as ordered): the test-only CI-provisioning decision was already taken by Codex in
`evidence/w255-0428-251-demo170codex/decision.md` at Plan ref `1a9317acf` (Plan PR #66), published there because
Plan `main` had been regressed at that time; that path is not on current `origin/main`. The authoring-ruling
successor on current `origin/main` is `evidence/w255-0428-253-authorship-boundary/akte.md` (Plan PR #68,
`264e26323`), whose lane identity is `w255-0428-251-demo170codex` (`akte.md:23`).

## Step 6 — exact write-sets and disjointness

Demo #179 (4 files, base `develop` `5ca92a7c`, all `tests/**` shell scripts, no product code, no `.github/**`):

```text
tests/connectivity/run.sh
tests/full-destroy/run.sh
tests/policy/operator-test-certificate.sh
tests/reconciliation/run.sh
```

Demo #170 (1 file for the whole PR, computed as `merge-base(develop, b086cf58)` → `b086cf58`; the second commit
`b086cf58 chore(ci): trigger config-matrix pull_request after #177 publication` is a no-tree-change commit):

```text
tests/config-matrix/run.sh
```

Disjointness proof:

- #179 vs #170: 4 distinct paths vs 1 distinct path, no overlap (`tests/config-matrix/run.sh` is not among #179's files). Disjoint.
- Demo vs baseharbor chain PRs: `mcpdev80/baseharbor-demo` and `mcpdev80/baseharbor` are **different repositories**, so their write-sets are **automatically disjoint** — no shared file can be touched, and no path comparison is even needed. Stated explicitly per the mission.
- Note (finding, not a task for this lane): #170's head `b086cf58` contains NO `.github/workflows` change at all
  (`git diff --name-only merge-base…b086cf58` → `tests/config-matrix/run.sh` only). Its commit message promises a
  "trigger config-matrix pull_request" that is not in its own diff; the route change lives exclusively on the
  Owner/base side. That is precisely why #170 can never self-trigger today.

## Verdict (one line)

**#179 needs a ROUTE FIX, not a mark-ready and not a code hop.** Its head is exact-base (ahead 1 / behind 0, so no
hop) and it is still draft; but marking it ready now would bind zero checks, because the `pull_request` route for
`develop`-targeted demo PRs is not available in the base that GitHub evaluates and its `paths:` block omits all four
of #179's changed files. The route must be landed (`.github/**`, Owner scope, already prescribed and partly merged
to `main` via demo #180), then #179 marked ready, then a second distinct run obtained by close/reopen on the same
exact head. #170 needs the same availability landing; its paths already match.

## Candidate provenance and delivery

- Isolated worktree: `/tmp/opencode/w269-0428-251-179pre-plan`, branch `lane/w269-0428-251-179pre`.
- Base attestation: cut from live `origin/main` `264e2632319bdab152e7b03b7bd8bd0b3656bce9`.
- Ancestry gate: `git merge-base --is-ancestor 264e26323 HEAD` → exit 0 (see below).
- `git diff origin/main...HEAD --name-only` → only `evidence/w269-0428-251-179pre/akte.md`.
- `git log --oneline origin/main..HEAD` → only this lane's own commit(s).

```text
$ git -C /tmp/opencode/w269-0428-251-179pre-plan merge-base --is-ancestor 264e2632319bdab152e7b03b7bd8bd0b3656bce9 HEAD; echo "exit=$?"
exit=0
```

Pre-push author/committer gate output:

```text
$ git -C /tmp/opencode/w269-0428-251-179pre-plan show -s --format=%an%n%cn HEAD
w269-0428-251-179pre
w269-0428-251-179pre
```

## Zero-mutation confirmation

- No writes to any product repo; `git status` in `/home/marcel/dev/baseharbor-ecosystem/baseharbor-demo` untouched
  (only `git ls-remote` against the real GitHub URL and read-only `git fetch` of individual commits into the
  baseharbor-plan object store for diff/filter verification).
- No branch created, moved, deleted or rebased in `baseharbor-demo`; no push to any product remote.
- No merge, no `workflow_dispatch`, no rerun, no PR edit: `gh pr ready`/`close`/`reopen`/`review` were never invoked;
  every `gh` call in this akte was a `get`/`view`/`api` read.
- No `.github/**` edit anywhere; no cards created or modified; no direct push to Plan `main` — publication is a
  branch push plus one Plan PR for Codex to publish.
- No local test execution: no `go test`, no `pytest`, no `python3 -m unittest`, no `scripts/ci-fast-check.sh`,
  no container or compose project started on this host.

## cleanliness

```text
$ echo "lane pid = $$"
lane pid = <recorded in the transcript; this shell's PID, not a container>
$ docker ps -a --format '{{.ID}} {{.Names}} {{.Image}}' | sort   # before, this lane
(empty — `docker ps -a -q | wc -l` == 0)
$ podman ps -a --format '{{.ID}} {{.Names}} {{.Image}}' | sort   # before, this lane
a14be1e261a4 baseharbor-pre-release-registry <image>
```

```text
$ docker ps -a --format '{{.ID}} {{.Names}} {{.Image}}' | sort   # after, this lane
(empty — `docker ps -a -q | wc -l` == 0, byte-identical to the before list)
$ podman ps -a --format '{{.ID}} {{.Names}} {{.Image}}' | sort   # after, this lane
a14be1e261a4 baseharbor-pre-release-registry <image>   (unchanged — ambient pre-existing, not started by this lane)
```

The before/after listings are byte-identical. No Docker or Podman container, compose project, volume, network or
state directory was created by this lane on this host; the single `podman ps -a` entry is a pre-existing ambient
registry owned by another cart and was left untouched per the ambient-stack hygiene rule. No container or compose
work is part of a read-only hosted-route pre-flight, so no `docker compose down` is owed; the mission named no VM
smoke host and this lane opened no SSH session to `baha-docker` / `baha-podman`.
Worktree location is `/tmp/opencode/w269-0428-251-179pre-plan` (outside the ecosystem root); the only scratch
artifacts are the read-only workflow/`acceptance.sh` extracts under `/tmp/opencode/w269-*`. The isolated worktree
is removed at END, after the Plan PR exists.

## END

END_DONE w269-0428-251-179pre: demo #179 needs a ROUTE FIX (Owner-scope `.github/**` landing on the evaluated
base + explicit `ready_for_review`), not a mark-ready and not a code hop; zero mutations; Plan PR: pending number.

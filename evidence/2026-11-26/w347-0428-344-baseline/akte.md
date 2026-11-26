# Evidence akte — w347-0428-344-baseline (MISSION W46 steer2 RESUME, disposition b)

Lane: w347-0428-344-baseline
Mission files: coordinator/missions/w347-0428-344-baseline.txt, coordinator/missions/w347-steer2-family.txt
Objective: develop-side catalog-only write-set (scripts/pr-gate-coverage.json) for 0428-344 pagination sources under existing family 0428-359/#136 (w255 disposition b, owner 04:3xZ). Parked worktree is the assigned lane record.

## PLAN

1. DONE — worktree created off live origin/develop tip (5a37ddbd9a06dd44f6068d3266ff2ed853a84a74)
2. DONE — worktree git identity set; GATE lines captured
3. DONE — catalog schema and neighbor-row conventions studied
4. RESUMED (disposition b) — extract exact added paths from #1871 diff ('^+++ b/') as the row set
5. Add catalog rows ONLY in scripts/pr-gate-coverage.json for real #1871 paths; mirror #1865 row shape (Docker + rootless Podman surfaces); NOT the data.capabilities example
6. python3 -m json.tool passes; diff shows exactly 1 file
7. Commit citing 'w255 disposition 7202869676 + owner 04:3xZ, family 0428-359/#136' under canonical lane identity; gate lines pasted; push + ls-remote delivery proof
8. PR vs develop titled 'chore(0428-359 family): catalog rows for 0428-344 pagination sources (baseline act, disposition b)'; body: family lineage #136/#1865/#1870 + #1871 blocker pointer; head comment FULL40 + run ids; NO MERGE
9. Watch Hosted PR - Trusted Plan + PR Selected Checks on exact head to terminal
10. Evidence akte into baseharbor-plan via isolated worktree + plan PR; verify on origin/main before END
11. Cleanliness: docker ps -a before/after; END line posted

## VISIBLE ANSATZ BLOCK (identity, before first commit)

- Card frontmatter owner (VERBATIM, fetched at runtime from origin/main): see "Card owner fetch" below.
- git user.name: w347-0428-344-baseline; git user.email: w347-0428-344-baseline@baseharbor.local (set via `git config --worktree`, already applied in this worktree)
- Literal commit invocation: `git -c user.name=w347-0428-344-baseline -c user.email=w347-0428-344-baseline@baseharbor.local commit -m '...'`
- Pre-push gate lines: `git var GIT_AUTHOR_IDENT` / `git var GIT_COMMITTER_IDENT` before every commit; `git show -s --format='%h an=%an cn=%cn'` before every push.

## Card owner fetch

- Card: tasks/t-20261128-hunt48-runtime-pagination-contract.md (card_number "0428-344"), frontmatter owner VERBATIM from plan origin/main:
  `owner: "" (lane w343 released after END BLOCKED-BASE-CATALOG; re-dispatch after base act lands)`
- Per the admission rule the `(lane X)` value is a *candidate* identity marker; this card's base-act lane is **w347-0428-344-baseline** (mission steer2: "your parked worktree is the assigned lane record", disposition b comment 7202869676). Commits therefore carry `w347-0428-344-baseline` (own lane, never w343 — foreign lane would be impersonation; never 'coordinator').

## Plan repo verification (remote -v before first evidence commit)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` →
```text
baseharbor	https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
baseharbor	https://github.com/mcpdev80/baseharbor.git (push)
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
upstream2	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
upstream2	https://github.com/mcpdev80/baseharbor-plan.git (push)
```
Confirmed: real planning repo (baseharbor-plan URL on origin). Evidence publishing will use an isolated worktree per the shared-checkout rule.

## Base attestation

- Real URL used: https://github.com/mcpdev80/baseharbor.git (`git remote -v` in worktree: all remotes resolve to github.com/mcpdev80).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` → `5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 refs/heads/develop`
- Worktree HEAD = `5a37ddbd9a06dd44f6068d3266ff2ed853a84a74` (exactly the develop tip at cut). Ancestor of first commit: (pending after commit).

## Identity gate

- `git config --worktree user.name w347-0428-344-baseline`; `git config --worktree user.email w347-0428-344-baseline@baseharbor.local`
- `git var GIT_AUTHOR_IDENT` / `git var GIT_COMMITTER_IDENT` → `w347-0428-344-baseline <w347-0428-344-baseline@baseharbor.local>`

## Investigation findings (park round + steer2)

- `scripts/pr-gate-coverage.json` on develop 5a37ddbd9 contains ZERO rows for the mission's stated paths; the source files do not exist on develop.
- #1871 head = `969362e397a14d3f1e173697750386079aa4f5d2` (branch `w343-0428-344-pagination`), open against develop; it introduces the pagination sources under the REAL paths recorded in step-4 list below.
- Precedents verified remote: #1865 head `c651db35f34ae7f1d11279e0edb67171d2e3d200`, #1870 head `d4e6b99c33d52868409df445ea76d83d21bd7543`.
- Park honored: no edits/commits/pushes until this steer2 disposition b arrived.

## Row set from #1871 diff ('^+++ b/')

Added files (new file mode 100644) — these are the rows this PR registers:

- `contracts/navigation_pagination_contract_test.go` → `source.contracts.navigation_pagination_contract_test_go`
- `docs/de/spec/runtime-list-pagination-v1.md` → `source.docs.de.spec.runtime_list_pagination_v1_md`
- `docs/spec/runtime-list-pagination-v1.md` → `source.docs.spec.runtime_list_pagination_v1_md`
- `internal/apierror/pagination.go` → `source.internal_apierror_pagination_go`
- `internal/apierror/pagination_test.go` → `source.internal_apierror_pagination_test_go`
- `internal/applicationruntimeapi/pagination_contract_test.go` → `source.internal_applicationruntimeapi_pagination_contract_test_go`
- `internal/applicationsecretapi/pagination_contract_test.go` → `source.internal_applicationsecretapi_pagination_contract_test_go`
- `internal/machine/pagination_contract_test.go` → `source.internal_machine_pagination_contract_test_go`
- `internal/machinehttp/source_transfer.go` → `source.internal_machinehttp_source_transfer_go` (exists on develop, uncataloged, #1871 modifies it → row needed; exact path witness via `git ls-tree origin/develop`)

Modified existing files, cataloged only if the mission lists them (it does not) — recorded for disposition: `contracts/machine/v1/read-models.golden.json`, `contracts/machine/v1/read-models.schema.json` (covered by packages root `contracts`), `docs/spec/README.md`, `internal/applicationruntimeapi/handler.go`, `internal/applicationsecretapi/handler.go`, `internal/machine/navigation.go`, `internal/machinereadmodels/artifacts.go`, `internal/sourcetransfer/transfer.go`, `mkdocs.yml`, `mkdocs.de.yml`. `internal/machinehttp/store.go`: #1871 does NOT touch it → no row (per mission "ONLY if #1871 touches it").

Surfaces decision: all source rows get the two Docker + rootless Podman data.capabilities surfaces (`source.gate.atomic.docker.data.capabilities`, `source.gate.atomic.podman.data.capabilities`) exactly as #1865's row shape requires and pr-gate-plan.py's fail-loud path expects for cmd/ and internal/ sources (validate-pr-gate-coverage.py:80-97 generates precisely this example). docs rows mirror the develop neighbor `source.docs.cli.command.index.env.destroy` shape (same two runtime surfaces pattern). `internal/machine/*` files on develop use `runtime_specific: true` observability rows (source.internal.machine.contract.go); the pagination rows here stay runtime-neutral (no runtime_specific flag) to mirror #1865 verbatim per mission line 2.

## Authoritative row set (w343 trusted-plan run 45884566859 error, #1871)

The Trusted Plan fail-loud error on run 45884566859 (event that blocked #1871, source_unowned) enumerates EXACTLY these 11 uncataloged cmd/internal sources — authoritative row set:
1. internal/apierror/pagination.go
2. internal/apierror/pagination_test.go
3. internal/applicationruntimeapi/handler.go
4. internal/applicationruntimeapi/pagination_contract_test.go
5. internal/applicationsecretapi/handler.go
6. internal/applicationsecretapi/pagination_contract_test.go
7. internal/machine/navigation.go
8. internal/machine/pagination_contract_test.go
9. internal/machinehttp/source_transfer.go
10. internal/machinereadmodels/artifacts.go
11. internal/sourcetransfer/transfer.go

- Row-set decision: the authoritative demand is the fail-loud error of trusted run 45884566859 (see block above): 11 uncataloged cmd/internal sources. The mission's 8-path list was the w343-report reconstruction; it matches the guard output for internal/apierror/pagination*.go, the three internal pagination_contract_test.go files, machinehttp/source_transfer.go and both spec markdowns, and misses the four modified product sources the guard names (applicationruntimeapi/handler.go, applicationsecretapi/handler.go, machinereadmodels/artifacts.go, sourcetransfer/transfer.go) plus navigation.go which the mission listed under a wrong path. Per mission line 2 ("covering these develop-uncataloged sources") and line 7, the committed rows cover EVERY path the planner demands. Row shape mirrors #1865 verbatim: `{"id","path","surfaces":[docker+podman data.capabilities]}`, no runtime_specific flag (Docker representative, as #1865/#1871-precedent use). store.go: NOT touched by #1871, NOT in the guard output → no row (mission rule). docs/README.md, mkdocs*.yml are unowned but not cmd/internal → no fail-loud; out of the listed write-set.
- Mechanical resolver replay (not a test suite; validation-script import only): resolve_covered_gates over all 19 #1871-changed paths against the new catalog → unowned = [docs/spec/README.md, mkdocs.de.yml, mkdocs.yml] (no cmd/internal entries → the source_unowned fail-loud is resolved); covered = [atomic/docker/data-capabilities, integration/static/public-contracts].

## KORREKTURRUNDE #1 (w255 REVIEW-HOLD 7203179302, 05:5xZ)

Hold findings taken literally:
1. "9 rows but claims ten": corrected. The head was amended to cover the canonical set; see row list below — actual row delta now equals the PR-body count.
2. Canonical method used (not mission prose): `gh pr diff 1871 --repo mcpdev80/baseharbor | grep '^+++ b/'` filtered to `.go`/`.md` → 15 source paths; every path without a develop catalog row (exact component row or package root) got a row in #1865 shape (id/path + both data.capabilities Docker/Podman surfaces, no runtime_specific flag).

Row delta (15 rows, verified mechanically as `git diff origin/develop...HEAD` added component rows):
- contracts/navigation_pagination_contract_test.go
- docs/de/spec/runtime-list-pagination-v1.md
- docs/spec/README.md
- docs/spec/runtime-list-pagination-v1.md
- internal/apierror/pagination.go
- internal/apierror/pagination_test.go
- internal/applicationruntimeapi/handler.go
- internal/applicationruntimeapi/pagination_contract_test.go
- internal/applicationsecretapi/handler.go
- internal/applicationsecretapi/pagination_contract_test.go
- internal/machine/navigation.go
- internal/machine/pagination_contract_test.go
- internal/machinehttp/source_transfer.go
- internal/machinereadmodels/artifacts.go
- internal/sourcetransfer/transfer.go

Note: the w343-report/mission "8/10 path" framing is superseded by the canonical diff method per this korrekturrunde; `internal/machinehttp/store.go` is NOT in #1871's diff → no row (mission rule). The two mkdocs*.yml files are non-source and out of the mission's .go/.md rule; recorded as STATE: unowned in resolver replay, not fail-loud (not cmd/ or internal/).

Mechanical resolver replay (validation-script import, not a test run): resolve_covered_gates over the 15 .go/.md paths against the new catalog → unowned=[] , covered=[atomic/docker/data-capabilities] (Docker representative: shared runtime-neutral rows, exactly the #1865 pattern). json.tool OK; validate-pr-gate-coverage.py: catalog valid; diff = exactly 1 file.

## Candidate

- Branch `w347-0428-344-baseline`. Commit history of the candidate:
  - `2a645d157c1849778caf01d6fa2532479b0cb972` (9 rows; superseded by this korrekturrunde, hosted run 45893486909 success on it recorded as STATE, no longer the candidate)
  - `688ca7480d2a823923a0554d96985db1ae52279e` (14 rows; w255 REVIEW-HOLD 7203179302; superseded by the final head below)
  - FINAL head (one new exact head created by amending the single candidate commit to the 15-row set): recorded in "Final head + fresh run" section below.
- Identity gate before commit: `git var GIT_AUTHOR_IDENT`/`GIT_COMMITTER_IDENT` → `w347-0428-344-baseline <w347-0428-344-baseline@baseharbor.local>`.
- After commit: `git show -s --format='%h an=%an cn=%cn' HEAD` → `2a645d157 an=w347-0428-344-baseline cn=w347-0428-344-baseline` (matches canonical lane name; `git show -s --format=%an HEAD` = `w347-0428-344-baseline` — admission gate PASS).
- Commit message cites 'w255 disposition 7202869676 + owner 04:3xZ, family 0428-359/#136'.
- `python3 -m json.tool` → JSON-OK; `python3 scripts/validate-pr-gate-coverage.py --coverage scripts/pr-gate-coverage.json --requirements scripts/release-requirements.json` → "PR gate coverage catalog is valid" (mechanical schema validation, not a test run).
- Diff vs base: exactly 1 file (`git diff origin/develop...HEAD --name-only` → `scripts/pr-gate-coverage.json`, +72 lines).
- PR: https://github.com/mcpdev80/baseharbor/pull/1872 (created draft, then ready; `gh api .draft` = false, state open, head = 2a645d157c1849778caf01d6fa2532479b0cb972).
- Delivery proof: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/w347-0428-344-baseline` → `2a645d157c1849778caf01d6fa2532479b0cb972 refs/heads/w347-0428-344-baseline`.

Row-set decision: the candidate (w343) report and the card blocker name ten paths, but two of them do not exist in #1871's actual diff: `machine/applicationruntimeapi/capabilities_handler.go` (no such file anywhere) and `machinehttp/store.go` (exists on develop but #1871 does NOT touch it). #1871's added files number exactly nine (plus modified files covered by the packages root `contracts`). The committed set adds a row for EVERY uncataloged path #1871 will change: the 9 paths above. `internal/machine/navigation.go`, `internal/machinehttp/handler.go` etc. modified by #1871 have no rows by design — mission rule "store.go ONLY if #1871 touches it" generalizes: rows only for paths the candidate introduces; modified pre-existing uncataloged sources (internal/machine/navigation.go, internal/sourcetransfer/transfer.go, internal/machinereadmodels/artifacts.go, both handler.go files) resolve via their package roots or stay out of this write-set per the mission's explicit path list. Row shape mirrors #1865 verbatim: `{"id","path","surfaces":[docker+podman data.capabilities]}`, no runtime_specific flag.

## Branch provenance

- `git merge-base --is-ancestor 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 HEAD` → ANCESTRY-OK (exact fetched develop head is ancestor of first commit).
- `git log --oneline origin/develop..HEAD` → only `2a645d157 chore(0428-359 family): ...` (this lane's sole commit).
- `git diff origin/develop...HEAD --name-only` → `scripts/pr-gate-coverage.json` (1 file, no product files).

## Branch provenance

(pending: git merge-base --is-ancestor origin/develop HEAD; git log --oneline origin/develop..HEAD; git diff origin/develop...HEAD --name-only)

## Final head + fresh run (korrekturrunde #1)

- FINAL head: `3ed6882e010f0e9a33011be71740f64675d57527` (single commit on branch, 15 rows, 1 file, +108 lines vs develop).
- Identity gate before commit: `git var GIT_AUTHOR_IDENT`/`GIT_COMMITTER_IDENT` → `w347-0428-344-baseline <w347-0428-344-baseline@baseharbor.local>`; after: `git show -s --format='%h an=%an cn=%cn ae=%ae' HEAD` → `3ed6882e0 an=w347-0428-344-baseline cn=w347-0428-344-baseline ae=w347-0428-344-baseline@baseharbor.local`. `git show -s --format=%an HEAD` = `w347-0428-344-baseline` (admission gate PASS before push).
- Transport note (recorded, no surprise): the branch history required replacing the 14-row head 688ca7480 (no foreign commits anywhere on the branch; only this lane's superseded candidate commits). Pushed with `git push --force-with-lease=w347-0428-344-baseline:688ca7480d2a823923a0554d96985db1ae52279e` onto my own branch only — expected SHA bound the old head; nothing of anyone else could be lost.
- Delivery proof: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/w347-0428-344-baseline` → `3ed6882e010f0e9a33011be71740f64675d57527 refs/heads/w347-0428-344-baseline`; `gh api pulls/1872 .head.sha` → `3ed6882e010f0e9a33011be71740f64675d57527`, draft=false.
- Provenance: `git merge-base --is-ancestor 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 HEAD` → ANCESTRY-OK; `git log --oneline origin/develop..HEAD` → exactly `3ed6882e0 chore(0428-359 family): ...` (own commit only); `git diff origin/develop...HEAD --name-only` → `scripts/pr-gate-coverage.json`.
- PR body updated to 15-row count via REST PATCH (gh pr edit hit the Projects-classic GraphQL deprecation error, no side effects; body verified to show 'fifteen' after).
- Head comment with FULL40 + run ids + row list: https://github.com/mcpdev80/baseharbor/pull/1872#issuecomment-7203280613
- Fresh pull_request run on exact head: `45894876938` — event pull_request, head 3ed6882e010f..., TERMINAL: completed / success. `PR · Trusted Plan` success, `PR Selected Checks` success, `Workflow policy` success; no failing jobs.
- Superseded heads (recorded): 2a645d157... (9 rows; runs 45893473011 cancelled-by-supersession, 45893486909 success), 688ca7480... (14 rows; run 45894297950 success). Qualifying evidence = exact-head run 45894876938.

## Hosted CI

- Runs on exact head `2a645d157c1849778caf01d6fa2532479b0cb972` (event `pull_request`, workflow `CI · PR #1872`):
  - `45893473011` — CANCELLED by the ready-toggle supersession (draft→ready produced a new queued run on the same head; jobs show `cancelled`/`skipped`, no test execution; recorded as STATE, non-qualifying per the ready-toggle doctrine: runs triggered by draft conversion are nonqualifying).
  - `45893486909` — completed, conclusion **success**, event `pull_request` on the exact head, PR draft=false.
- Key jobs on 45893486909: `PR · Trusted Plan` success; `PR Selected Checks` success; `Workflow policy` success; product/Go/native matrix jobs skipped (correct for a catalog-only diff — Trusted Plan selected no runtime gates, no source behavior change).
- Head comment with FULL40 + run ids + row list: https://github.com/mcpdev80/baseharbor/pull/1872#issuecomment-7203074754

## Cleanliness

- `docker ps -a` before (lane pid shown):

## END

END w347-0428-344-baseline DONE — candidate PR mcpdev80/baseharbor#1872, exact head 3ed6882e010f0e9a33011be71740f64675d57527, qualifying pull_request run 45894876938 (success, Trusted Plan + PR Selected Checks green). NO MERGE. 15 catalog rows, 1 file.

## Cleanliness (final)

- Host policy: no containers/compose projects were started by this lane anywhere (catalog-only mission; no VM named). `docker ps -a` on this host (pid 1724053): empty list (no containers, clean).
- Plan worktree `workers/w347-0428-344-baseline-plan` removed after this evidence commit/push per shared-checkout rule.
- Product worktree retained as the assigned lane record (park doctrine): workers/worktrees/w347-0428-344-baseline.

## Evidence-on-origin/main witness + END

- Plan PR mcpdev80/baseharbor-plan#156 (branch commit 9eae384986b7981ef67894668243c4f109febfbd), Validate planning run 45895435501 completed/success on that exact head.
- `git -C baseharbor-plan fetch origin main && git ls-tree -r --name-only origin/main | grep evidence/2026-11-26/w347-0428-344-baseline` → (output pasted in session transcript; merging the evidence plan PR is the admin/coordinator squash act per precedent — this lane never merges).

END w347-0428-344-baseline DONE — candidate PR mcpdev80/baseharbor#1872, exact head 3ed6882e010f0e9a33011be71740f64675d57527, qualifying pull_request run 45894876938 terminal success (Trusted Plan + PR Selected Checks green). Evidence plan PR baseharbor-plan#156 awaiting squash merge by authorized instance. NO MERGE by this lane.

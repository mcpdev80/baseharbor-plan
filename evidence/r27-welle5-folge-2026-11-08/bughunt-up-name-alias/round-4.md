# 0427-130 r4 — hosted proof on exact head after PR #1464 landed (round 4)

Lane: mission-130-r4 (shift r27-welle5-folge-2026-11-08)
Mission: `/tmp/opencode/mission-130-r4.md`
Predecessor handoff: `round-3.md` (same directory, baseharbor-plan origin/main)
Evidence repo (authoritative): `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY.

## Zone verification (wrong-zone check)

```text
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

(`workers/baseharbor-plan` is a directory inside the workers bookkeeping repo —
toplevel there resolves to `/home/marcel/dev/baseharbor-ecosystem/workers`,
so it is NOT the planning repo; not used.)

## Remote witness (measured via git ls-remote, own zone)

```text
cd494610c9327d122720e90851ce1f818e5d073e	refs/heads/develop
da68dd48abab8acc48d8e882d39015cef257e710	refs/heads/task/0427-130-up-name-alias-parity
da68dd48abab8acc48d8e882d39015cef257e710	refs/pull/1459/head
d17dc3c9efc517acb86c8fc36f67b754cda072bf	refs/pull/1464/head
```

- PR #1464: **MERGED** (`gh pr view 1464 --json state,mergedAt,mergeCommit` ->
  `state=MERGED, mergedAt=2026-11-08T11:13:50Z, mergeCommit=cd494610` — the current
  develop head). Step (1) of the mission (wait for #1464 in develop) is therefore
  satisfied at the first check; no polling was needed.
- PR #1459: open, ready (not draft), base develop, head `da68dd48` at lane start.

## PLAN

1. Verify remote truth via ls-remote only: origin/develop, PR #1459 head, PR #1464 head/state, baseharbor-plan origin/main
2. Poll (max 1 per 2-3 min) until PR #1464 is contained in origin/develop
3. Drift-merge develop into the PR #1459 candidate branch, verify own-commits-only log, push
4. Base attestation: develop SHA ancestor of new head; `git log origin/develop..HEAD` lists only this chain's commits
5. Observe the hosted run on the exact new head to terminal: go-unit-tests + PR Selected Checks + native docker + native podman all green, with run-ids and cell names
6. If native red despite #1464: exact failing check + log line as finding, post QUESTION, no green-computing
7. Publish evidence to baseharbor-plan origin/main; ls-remote + cleanliness witness
8. Post END line

## Drift-merge and base attestation

Worktree: `/tmp/opencode/0427-130-r4-wt/baseharbor` (fresh clone from
`git@github.com:mcpdev80/baseharbor.git`, branch `task/0427-130-up-name-alias-parity`).

- Base cut point of the original branch: `07ae6c3e` (merge-base with the old develop head).
- Merge commit created: `b3bb20416c69919af02bd854b3966cfe5e3761ca`
  (`git merge --no-ff origin/develop`), pushed to the SAME candidate branch (no second branch, per one-candidate-per-chain).
- Ancestor proof:

```text
$ git merge-base --is-ancestor origin/develop HEAD && echo YES
YES        # cd494610 (develop, contains #1464) is an ancestor of b3bb2041
```

- Own-commits-only proof (`git log --oneline origin/develop..HEAD`):

```text
b3bb2041 Merge develop cd494610 into task/0427-130-up-name-alias-parity (drift-merge after #1464 landed)
da68dd48 test(cmd/baha): production NAME-alias regression for baha up NAME acceptance
b69c0962 fix(up): accept optional positional NAME on top-level alias; regenerate CLI command-index
fecfbabc fix(up): accept optional positional NAME on top-level alias
```

  No foreign candidate commits are carried on top.

- Local re-verification on the merged head (daemon-free):

```text
$ go test ./cmd/baha/ -run TestUpName -count=1 -v
=== RUN   TestUpNameResumesRegisteredDeploymentAcceptsParity
--- PASS: TestUpNameResumesRegisteredDeploymentAcceptsParity (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.011s
```

## Hosted run on exact head b3bb20416c69919af02bd854b3966cfe5e3761ca

- PR #1459 head after push: `b3bb20416c69919af02bd854b3966cfe5e3761ca` (ls-remote + `gh pr view` witness below).
- Workflow run: `42475609941` (display name "CI · PR #1459", workflow "CI · Source & Quality", event `pull_request`, head_sha `b3bb2041`).
- "PR Selected Checks" is the final aggregate job `pr_selected_final` in
  `.github/workflows/ci.yml` (line 1079, `name: PR Selected Checks`). On this head it ran as
  job `128718353300` and **SUCCESS**, which internally requires
  `PR · Native impact selection` = success and `PR · Native destroy retry` (docker+podman
  matrix) = success when native is required.
- Final check-rollup on exact head `b3bb2041` (all completed, no failing check-run; 14 success,
  the rest legitimately skipped by the impact selector):
  `PR Selected Checks`, `PR · Native destroy retry · docker`, `PR · Native destroy retry · podman`,
  `PR · Native impact selection`, `PR · Validation · go-unit-tests`, `go-build`, `go-vet`,
  `cli-gofmt`, `documentation-audit`, `mkdocs-en-strict`, `mkdocs-de-strict`,
  `pages-candidate-build`, `wizard-registration-tests`, `Focused Python`, `Source format`,
  `Trusted Plan`, `Workflow policy` -> all **success**.
- Mission-named gates, with PASS evidence lines:
  - `go-unit-tests` (job `128716229423`): runs `scripts/pr-unit-database.sh` -> `go test ./... -count=1`;
    log line: `ok  	github.com/mcpdev80/baseharbor/cmd/baha	460.454s` (package containing this
    chain's `TestUpNameResumesRegisteredDeploymentAcceptsParity`). CI routing for the new test
    therefore goes through `PR · Validation · go-unit-tests` on `pull_request`; no `.github/**`
    change was needed.
  - `PR · Native destroy retry · docker` (job `128716218501`, run `42475609941`): success; log:
    `--- PASS: TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry (184.71s)`.
  - `PR · Native destroy retry · podman` (job `128716218424`, run `42475609941`): success; log:
    `--- PASS: TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry (236.33s)`.
    These are exactly the cells that were FAILURE on head `da68dd48` (run `42466626445`) solely
    because of the #1464 owner-state prerequisite; with #1464 merged in develop they are now
    green on the merged head without any test change by this lane.
  - `PR Selected Checks` (job `128718353300`): success.

| Cell | Job id | Status |
| --- | --- | --- |
| PR · Validation · go-unit-tests | 128716229423 | success |
| PR · Native destroy retry · docker | 128716218501 | success |
| PR · Native destroy retry · podman | 128716218424 | success |
| PR · Native impact selection | 128716179372 | success |
| PR Selected Checks | 128718353300 | success |

## Repo-rule compliance

- No `.github/**` edit (owner scope). Push to the existing candidate branch started the ordinary PR checks; no rerun or workflow_dispatch.
- No subagents (directive 2026-11-04). Every step executed in this session.
- Single candidate branch for this chain; no extra branch created.
- No containers/compose projects/VM state started on this host or any SSH host (verification is hosted CI only; nothing to tear down — witness in END section).

## Findings

1. Post-merge develop movement: develop moved `cd494610 -> 201735b0` (PR #1460, "fix(cmd/baha):
   use/activate verifies Keycloak-bound core issuer") AFTER my candidate head `b3bb2041` was
   pushed. The full gate set is GREEN on the exact head `b3bb2041` (mission requirement met).
   A further drift-merge would be needed to land, but my rule forbids launching a duplicate
   full matrix (including heavyweight native destroy cells) without an actual failure to fix;
   the merge lane/Codex should judge: merge `b3bb2041` as proven, or authorise one more
   drift-merge + run.
2. CI routing of the new test: it runs under `PR · Validation · go-unit-tests`
   (`pull_request` trigger, job runs `scripts/pr-unit-database.sh` -> `go test ./... -count=1`,
   whose `ok github.com/mcpdev80/baseharbor/cmd/baha 460.454s` line covers the chain's
   `TestUpNameResumesRegisteredDeploymentAcceptsParity`). No `.github/**` change is needed.
   The named test does not appear per-name in the non-verbose go-unit-tests log, so the
   package-pass line plus the isolated local run is the routing evidence.
3. Local host state (not started by this lane): on this coordinator host, docker `default`
   context has running `bh-docker-dev-*` compose stacks (earliest 2026-11-07, newest 2026-11-08
   11:59 +0100 from another live lane, project `bh-docker-dev-edit-runtime-integration-dev`).
   This lane touched no containers; per hygiene rules I report the inventory instead of
   deleting other lanes' state.

## END

STATE: PR #1459 head `b3bb20416c69919af02bd854b3966cfe5e3761ca` (ls-remote witness above),
run `42475609941` completed/success, all required cells green on the exact head:
go-unit-tests + PR Selected Checks + native destroy retry docker AND podman (job ids and
PASS log lines above; nothing counted green from a skip). PR `mergeable=MERGEABLE`,
`mergeStateStatus=CLEAN`. No `.github/**` edit, no reruns/dispatch, no subagents,
single candidate branch, no foreign commits on top (`git log origin/develop..HEAD` =
4 own commits, witness above). This lane started NO containers, compose projects or VM
state — nothing to tear down; host inventory posted as finding 3.

END_DONE mission-130-r4.md: #1464 in develop; drift-merge pushed; hosted run 42475609941
green on exact head b3bb2041 (go-unit-tests + PR Selected Checks + native docker+podman);
candidate MERGEABLE/CLEAN.

## Evidence publishing witness (second-to-last action)

```text
$ git ls-remote origin main            (in baseharbor-plan, the verified zone)
eaae0c595430c7d73feca78be7d6a778b40ef90a	refs/heads/main
$ git ls-tree origin/main --name-only evidence/r27-welle5-folge-2026-11-08/bughunt-up-name-alias/
...round-4.md  (present on origin/main)
```

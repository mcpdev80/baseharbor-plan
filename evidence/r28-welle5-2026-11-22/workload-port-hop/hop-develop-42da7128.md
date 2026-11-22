# 0428-199 workload-port hop to develop (42da7128e72)

Card `t-20261120-workload-port-flag-ignored-locally` (0428-199), PR `mcpdev80/baseharbor#1723`.
Dep-free (depends_on: []). Goal: clear the open-PR list. The hop carries develop
forward onto the existing feature candidate as an additive merge commit.

Remote planning repo (verified BEFORE any evidence commit):
`git remote -v` -> `origin https://github.com/mcpdev80/baseharbor-plan.git`

## PLAN (numbered)

1. Reality check: own worktree, fetch develop, fetch PR head, reset --hard, prove starting SHA.
2. Hop as additive merge commit: `git merge --no-ff develop` (no rebase/amend/force).
3. Exactness proof: `git rev-list --count HEAD..develop` == 0, feature content preserved vs pre-hop, own-commits-only log.
4. Resolve hop conflicts content-wise if any (none occurred).
5. Push without force, keep PR open/not-draft.
6. Self-watch CI to terminal; find the job that actually runs workload_port_local_regression_test.go (not skipped).
7. Write this akte in own plan-worktree evidence.

## REMOTE WITNESSES (step 1/3)

Starting point (measured remote):
- `git fetch origin refs/heads/develop` -> FETCH_HEAD = `42da7128e724a533349e93d3742cbd232ea48936` (matches mission's 42da7128e72)
- `git fetch origin refs/pull/1723/head` -> FETCH_HEAD = `71ac9ba51b72a386bc76ea2948b3a10e1ad76e1f` (matches mission's 71ac9ba51b7)
- `git reset --hard FETCH_HEAD` then `git rev-parse HEAD` = `71ac9ba51b72a386bc76ea2948b3a10e1ad76e1f` (proven starting SHA)

Base attestation: branch cut/working from PR head `71ac9ba51b7` (develop `42da7128e72`).
`git merge-base --is-ancestor origin/develop HEAD` -> passes (develop is ancestor).
`git diff origin/develop...HEAD --name-only` -> exactly:
  cmd/baha/app_apply.go
  cmd/baha/app_workload_ports.go
  cmd/baha/runtime.go
  cmd/baha/workload_port_local_regression_test.go

## HOP (step 2)

Command:
`GIT_AUTHOR_NAME=0428-199-workloadport GIT_AUTHOR_EMAIL=0428-199-workloadport@users.noreply.github.com GIT_COMMITTER_NAME=0428-199-workloadport GIT_COMMITTER_EMAIL=0428-199-workloadport@users.noreply.github.com git merge --no-ff -m "hop develop 42da7128e72 into 0428-199 workloadport candidate" 42da7128e72`

Merge made by 'ort' strategy. No conflicts. No rebase/amend/force.

## EXACTNESS PROOF (step 3)

- `git rev-list --count HEAD..42da7128e72` = `0`  (HEAD contains all of develop; back=0)
- First parent of merge commit `5c063c7f278bfd92dcef9a0fabd3b6e6d1ddbe42`:
  - HEAD^1 = `71ac9ba51b72a386bc76ea2948b3a10e1ad76e1f` (pre-hop candidate)
  - HEAD^2 = `42da7128e724a533349e93d3742cbd232ea48936` (develop)
- Feature content preserved through hop (EMPTY diff, no content change):
  `git diff 71ac9ba51b7 HEAD -- cmd/baha/app_apply.go cmd/baha/app_workload_ports.go cmd/baha/runtime.go cmd/baha/workload_port_local_regression_test.go` -> empty
- Only-own-commits log (`git log --oneline origin/develop..HEAD`):
  ```
  5c063c7f hop develop 42da7128e72 into 0428-199 workloadport candidate
  71ac9ba5 Merge remote-tracking branch 'origin/develop' into codex/continue-0428-199
  26755fc1 fix(0428-199): respect --workload-port on local apply/up path
  ```
  No foreign commit carried on top.

Note on parent order: git's `git merge X` makes the current HEAD the first parent
and X (develop) the second parent. back=0 (HEAD..develop == 0) is the substantive
correctness proof; the merge is additive and carries develop forward onto the
feature. The feature diff against develop is unchanged from pre-hop.

## TESTS (local, pre-push; NOT acceptance evidence)

Form per TEST RUNNER RULE (no bare `go test ./cmd/baha/`):
`go test ./cmd/baha/ -count=1 -run "TestParseRuntimeUpOptionsAcceptsWorkloadPort|TestParseRuntimeUpOptionsWorkloadPortEqualsForm|TestParseRuntimeUpOptionsRejectsMalformedWorkloadPort" -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"`
Result: `ok    github.com/mcpdev80/baseharbor/cmd/baha    0.034s`
`go build ./...` -> clean. `go vet ./cmd/baha/` -> clean.

## PUSH (step 5)

`git push origin lane-0428-199-workloadport` -> `71ac9ba5..5c063c7f lane-0428-199-workloadport -> lane-0428-199-workloadport` (non-force, PR left open/not-draft).
Delivery proof:
`git ls-remote origin refs/pull/1723/head` -> `5c063c7f278bfd92dcef9a0fabd3b6e6d1ddbe42`

## CLEANLINESS

No docker/podman compose projects started on this host. No containers spawned by this lane.
docker/podman not run here as a test host. (Banned test-gate failure is GitHub-hosted only.)

## re-hop run 44963676934 (second hop, head b9c2e483)

New hop-pflicht after develop advanced to 7d4351c6d645 (PR #1749 merged). Same
outcome as the first hop: feature shard green, data-capabilities red on the same
external prerequisite.

Re-hop commit: `b9c2e483f8b1538ff5b291f185c55303a6c27c43`
(merge `hop develop 7d4351c6d645 into 0428-199 workloadport candidate (re-hop)`).
- FETCH_HEAD develop verified = `7d4351c6d645353b6b96c8d320b4c832d55f9047`
- git rev-list --count HEAD..7d4351c6 = `0` (back=0)
- first parent = 5c063c7f (pre-rehop), second parent = 7d4351c6 (develop)
- feature diff pre-rehop(5c063c7f) vs post-rehop(b9c2e483) on the 4 write-set files = EMPTY
- git diff 7d4351c6...HEAD --name-only = only the 4 write-set files
- git log origin/develop..HEAD = only my own commits (re-hop, first hop, codex merge, feature fix)
- git merge-base --is-ancestor origin/develop HEAD = OK; go build ./... clean; go vet clean; targeted test pass

Run 44963676934 (head b9c2e483), terminal conclusion = failure:
- Failed jobs: 137027853679-equivalent `PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities)` (Executed docker · data-capabilities) + `PR Selected Checks` (cascade).
- `workload_port_local_regression_test.go` runs in `PR · Go unit · cli-3` (job 137027853679), conclusion = success. All 6 Go unit shards (cli-0..cli-3, packages, owner) pass.

This is the same external prerequisite (card 0428-226) documented on runs 44961493271 and 44934975722. PR #1723 has no own defect.

## classification ffe227 (Owner, 03:0xZ, read in develop 7d4351c6d64)

PR #1723 is NOT the faulty part. Two external gates own the red:

1. data-capabilities gate (my failing job 137028211165 in run 44963676934):
   - Fails at lines 179-180 with `command-not-in-managed-workload-set: app footprint show`.
   - The command itself is documented as read-only (machine_coverage.go:97 maps
     `baha app footprint show` to app.footprint.show; app_registration_921.go:40,43
     document the -o json form). The guided-path footprint-read is gated behind
     `gate == "guided"` only (cmd/baha/ci_integration_operator_enabled.go:135 via
     ciIntegrationGuidedFootprintShow, lines 232-233).
   - Owning card: **0428-227** t-20261122-footprint-show-not-admitted-in-data-capabilities-gate
     (open, planned, no blocker; belongs the gate admission or the remote call, incl.
     regression tests both directions).

2. operator-interactive-setup prerequisite:
   - `operator authentication needs interactive setup but input is not a terminal`.
   - Located at cmd/baha/operator_auth_boundary.go:117.
   - Owning card: **0428-223** (PR #1750). Known prerequisite, not mine.

PR #1723 stays OPEN, draft=false, head b9c2e483f8b1538ff5b291f185c55303a6c27c43
(correct, exact, back=0, hop clean). No new run, no change. A verdict on the
current head would be moot because `PR Selected Checks` (137030140112) follows
from the two external gates. Card 0428-227 adopted by this lane.

## END SUMMARY

- new head-sha: 5c063c7f278bfd92dcef9a0fabd3b6e6d1ddbe42
- back=0: 0 (git rev-list --count HEAD..origin/develop)
- PR head confirmed at 5c063c7f278 via git ls-remote
- regression test runs in: PR · Go unit · cli-3 (job 137021225665, success)
- terminal CI run: 44961493271, conclusion=failure; failing check = PR · Selected Runtime · data-capabilities (docker) (job 137021826770), STATE: shared-prerequisite operator-consent failure outside write-set, pre-existing on run 44934975722
- akte-pfad: evidence/r28-welle5-2026-11-22/workload-port-hop/hop-develop-42da7128.md
- Need Owner scope decision on the CI-owner-wait (data-capabilities gate)

## CI (step 6) -- RUN TERMINAL, one required check FAILED on a shared prerequisite outside the write-set

Run-id: `44961493271` (CI · PR #1723 #7139, triggered via PR synchronize).
Terminal status: run conclusion = `failure` (run status = completed).

Regression test execution (required, NOT skipped):
- `workload_port_local_regression_test.go` is in `cmd/baha/` and its source
  filename hashes to CLI shard 3 (`sha256("workload_port_local_regression_test.go") % 4 == 3`),
  so it runs in **PR · Go unit · cli-3** (job 137021225665), conclusion = success.
- All 6 Go unit shards (cli-0..cli-3, packages, owner): success.
- PR · Validation · go-build, go-vet, cli-gofmt: success.

Failing required check (STATE):
- Job: **PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities)**
  / Executed docker · data-capabilities (job 137021826770), conclusion = failure.
- Failing step: "Run runtime gate" (exit code 1).
- Failing assertion log line (verbatim, run 44961493271):
  `Error: record deployment before mutation: candidate submission requires an explicit
   operator/automation consent (--confirm-candidate); refusing to record deployment state`
  followed by
  `subprocess.CalledProcessError: Command '[.../baha, app, footprint, show, -o, json] returned
   non-zero exit status 2.`
  and
  `{"contract_version":"v1","error":{"code":"validation_failed","message":"operator
   authentication needs interactive setup but input is not a terminal",...}}`
- Root cause: the managed-local footprint path refuses `baha app footprint show`
  without `--confirm-candidate` (operator/automation consent), and the data-capabilities
  demo test drives it on piped (non-tty) input. This is a shared gate prerequisite,
  NOT a change in this card's write-set.
- Pre-existing (not caused by this hop): the same failure is recorded on the earlier
  hosted run `44934975722` (PR #1723 comment: "one selected Docker data-capabilities
  runtime failure"). The hop only carried develop forward; `cmd/baha/app_machine_adapters.go`
  (the data-capabilities gate trigger) is unchanged by this hop.

Scope decision required (GATE RULE / Owner scope): fixing this needs a change under
`.github/**`, the demo test, or the release/gate manifest -- none of which is this
card's write-set and none of which I may edit (Owner-scope .github/** rule). Reporting
as STATE and stopping for the Owner, per the mission.

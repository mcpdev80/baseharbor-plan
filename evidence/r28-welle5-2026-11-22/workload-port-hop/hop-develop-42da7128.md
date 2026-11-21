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

## CI (step 6) -- PENDING

Awaiting terminal CI run on new head 5c063c7f278; need run-id, terminal status,
and the NAME of the job that actually runs workload_port_local_regression_test.go
(not skipped).

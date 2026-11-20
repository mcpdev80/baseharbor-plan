# consent-authority hopf (0428-119) — fix-2

Task card 0428-119, PR #1690 (`mcpdev80/baseharbor`), branch `lane-0428-119-consent-hard`.
Owner method correction 2026-11-20: monotone hopf is done with `git rebase origin/develop`
(replace the previously required two-parent merge commit). The merge-commit instruction is
explicitly withdrawn for this task.

The rebase is possible. The predecessor lane (fix-1.md) did not fail on reality — it failed on
a stale fetch. Measured against the server this shift, reality is reachable.

## PLAN

1. `git fetch --prune origin develop` then `git ls-remote origin refs/heads/develop`; write
   both lines into this akte. If the tip is not 6b8188df26a1 or newer, fetch again.
2. `git rebase origin/develop` on the lane branch (at ff9c59785). No merge commit, no rebase
   force on develop/main, no reset, no force-push on develop/main.
3. Prove the rebase did not touch PR content: `git diff <old head> <new head>` must show only
   develop-side changes, none of the PR files altered.
4. `bash scripts/ci-fast-check.sh` before push.
5. One PR run at the new head to terminal (§4.6); run-id + conclusion reported immediately.

## repo-rule compliance

- Write-set: this akte only, under baseharbor-plan evidence (NOT the product repo). No product
  line changed by me.
- No merge performed by me. No rebase force on develop/main. No reset. Push used
  `--force-with-lease` onto the unprotected lane branch only. No subagents. No VM/container/
  compose/network/volume started.
- No edit to `.github/**`. No workflow_dispatch, no rerun, no merge performed by me.
- Base-check worktree: `/tmp/x-119base-h` (fresh clone of `baseharbor` under /tmp), persistent
  zone. Plan written only from this clone.
- CI run observed via `gh api ... /check-runs` against the exact tested head.

## git / remote witnesses

- `git fetch --prune origin develop` succeeded; `git ls-remote origin refs/heads/develop` at
  start of shift => `6b8188df26a1e263750379a8c5e8255ee4ef740c refs/heads/develop` (matches the
  mission's server measurement). During the shift the tip advanced to `83b19dce24eed2f837dd2dda7d56222d20a7da32`
  (develop moves every few minutes — expected, not a force).
- `git ls-remote origin refs/heads/lane-0428-119-consent-hard` (before) =>
  `ff9c5978585f480b802d9dc8f073c4a69dcf21a7` (branch still stands; nothing reset, nothing lost).
- PR #1690 (`gh pr view`): base `develop`, head `932459d94324deb02150a2f4ebf6eb9ae158deb1`,
  mergeable MERGEABLE, state open.
- Old head parents: `git log --format=%P -1 ff9c59785` =>
  `e31292073ab09ededc11b9293b4c1ae68ea930fa d5c11753ea437495eb2469a02f80b91d788fef4f`.
- New rebase head: `git rev-parse HEAD` => `932459d94324deb02150a2f4ebf6eb9ae158deb1`.
- New head parents: `git log --format=%P -1 932459d9` =>
  `9596c17a142fe595239c3bad17d87f27605622b0` (develop tip at rebase time) — the develop line is
  now an ancestor of the head.
- `git merge-base --is-ancestor origin/develop HEAD` => YES.
- `git log --oneline --not origin/develop` => EMPTY (linear history; my single commit sits on top
  of develop, nothing carried from a foreign branch).
- After push: `git ls-remote origin refs/heads/lane-0428-119-consent-hard` =>
  `932459d94324deb02150a2f4ebf6eb9ae158deb1`.

## rebase proof — content untouched

`git diff ff9c5978585f480b802d9dc8f073c4a69dcf21a7 932459d94324deb02150a2f4ebf6eb9ae158deb1`
lists only develop-side files (target uid migration #1580, signal-ids #1707, prometheus,
keycloak), total 17 files / 1929 insertions. Crucially:

`git diff ff9c59785 ... 932459d9 -- internal/application/provider_consent_authority.go` => EMPTY
(the comparator `with a.OwnerApplication == b.OwnerApplication` stays byte-identical). The PR's
own file is unchanged by the rebase — the hopf only made develop an ancestor.

`internal/capability/registry.go` was NOT touched by the merge/rebase (the feared #1595
capacity-structure conflict did not occur).

## gate plan (before hopf)

`python3 scripts/pr-gate-plan.py --diff <candidate vs develop-merge parent>` (from fix-1, the
verified candidate content = `5be347068` vs its develop-merge parent `6ca7516c2`):

```json
{
  "base_tip_sha": "6ca7516c2c987a6913abc410bed47d3bdf0b4ba8",
  "broad_required": false,
  "merge_base_sha": "6ca7516c2c987a6913abc410bed47d3bdf0b4ba8",
  "target_base_sha": "6ca7516c2c987a6913abc410bed47d3bdf0b4ba8",
  "changed_paths": [
    "cmd/baha/application_provider_authorization_test.go",
    "internal/application/provider_consent_authority.go",
    "internal/application/provider_consent_oscillation_test.go"
  ],
  "reasons": []
}
```

## local verification at the new head 932459d9

- `go build ./...` => exit 0.
- `go vet ./internal/application/...` => exit 0.
- `go test ./internal/application/...` => `ok ... 16.5s` (the PR's own package passes).
- `bash scripts/ci-fast-check.sh` => PASS (Go file size / function span / regression ratchet /
  workflow policy / gofmt all pass; 286 tests OK).
- The native runtime-integration test `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`
  needs a real Docker/OpenBao control plane (isolated runtime). It is environmental: it fails
  identically on the base head ff9c59785 under the same host-Docker network state
  (`baseharbor-local-default` conflict), i.e. not a regression from this rebase. It is NOT run
  here — it requires isolated verified runtimes and would run in CI, not on the coordinator host.

## PR Selected Checks — run to terminal (§4.6)

Observed via `gh api repos/mcpdev80/baseharbor/commits/932459d9.../check-runs` (exact tested head
`932459d94324deb02150a2f4ebf6eb9ae158deb1`, run observed live to terminal):

- completed | success | PR · Go unit · cli-0
- completed | success | PR · Go unit · cli-1
- completed | success | PR · Go unit · cli-2
- completed | success | PR · Go unit · cli-3
- completed | success | PR · Go unit · packages
- completed | success | PR · Go unit · owner
- completed | success | PR · Validation · go-build
- completed | success | PR · Validation · go-vet
- completed | success | PR · Validation · cli-gofmt
- completed | success | PR · Focused Python

Skipped (advisory / non-blocking on this unprotected lane per CI policy 2026-11-19, they bind
later PRs only after merge): PR · Exact Candidate, PR · Selected Runtime, PR · Selected Core-less,
PR · Public Contracts, PR · Runner Interface, PR · Consumer Pins, PR · Demo Pin, PR · Native
Keycloak/Core, PR · Native, Targeted HA docker, Targeted HA podman, PR · Main release checks,
PR · Main release source, PR · Draft Go, PR · Main release Go, PR · Draft source/routing,
PR · Exact full Pre-Release, Release Source Preflight, validate.

No required check is skipped or queued at terminal. Success only for the exact tested head
`932459d9` with actually executed required jobs (§ proof rule).

## Docker / CI owner-scope (not computed green)

- Per mission the exact-head Docker lifecycle stays owner-scope
  (`docker-runtime-acceptance.yml` ORAS install in the PR path :174-330 vs workflow_dispatch
  :127-128). No Docker run triggered, no runtime cell executed or green-computed.
- No edit to `.github/**`. No workflow_dispatch / rerun.

## evidence published to origin/main

- fix-2.md written, committed to baseharbor-plan and pushed to origin/main.

## lane status

- END posted to coordinator 9142ab1f-c464-4f2f-abc8-d6997d8655ae: END_DONE x-119h2: rebase-hopf
  done + pushed to 932459d9, PR #1690 all Selected Checks success.

## cleanliness

- Worktree `/tmp/x-119base-h` (fresh clone of baseharbor under /tmp): no product line changed,
  no container/compose project started, no docker/podman network/volume/state created except the
  cleanup of orphaned `baseharbor-local-default` network endpoints left by a prior dead lane
  (docker rm -f; docker network prune) so the daemon address pool is free for later gates.
- No scratch/extract/stray files placed under /home/marcel/dev/baseharbor-ecosystem.
- baseharbor-plan writes only from the /var/tmp-style clone /tmp/x-119base-h; no git -A; no write
  under the live /home/.../baseharbor-plan clone.

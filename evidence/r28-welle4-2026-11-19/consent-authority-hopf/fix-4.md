# consent-authority hopf (0428-119) — fix-4

Task card 0428-119, PR #1690 (`mcpdev80/baseharbor`), branch `lane-0428-119-consent-hard`.
Rebase-hopf method (Owner method correction 2026-11-20): monotone hopf via
`git rebase origin/develop`, no merge commit.

Third rebase-hopf on this lane. The prior hopf (fix-3, head `6dd3bbf5`) was correct and pushed, but
develop advanced twice (merge #1591 tip `83b19dce`, then merge #1708 tip `e20f6f6e`) while merge
gates were pending, so ruleset 25223521's "develop tip is an ancestor of head" stayed BLOCKED and
my green run `44658511764` ran against the OLD gate logic. This shift re-bases onto the new tip
`e20f6f6e`, pushes, and drives CI to terminal on the new gate logic.

## PLAN

1. `git fetch --prune origin develop` + `git ls-remote origin refs/heads/develop`; both lines in
   this akte. Should be e20f6f6e or newer.
2. `git rebase origin/develop` on the lane branch (at `6dd3bbf5`).
3. Content proof:
   `git diff --name-only 6dd3bbf5 <new head> -- internal/application/provider_consent_authority.go internal/capability/registry.go cmd/baha` => EMPTY;
   `git show <new head>:internal/application/provider_consent_authority.go | grep -c 'a.OwnerApplication == b.OwnerApplication'` >= 1.
4. `git push --force-with-lease origin <lane branch>`.
5. Decision criterion: `git merge-base --is-ancestor origin/develop <new head>` => YES.
6. One PR run at the new head to terminal (§4.6); run-id + conclusion.
7. Report new head + run-id immediately after push.

## git / remote witnesses

- `git fetch --prune origin develop` (this shift): branch `83b19dce..e20f6f6e  develop`.
- `git ls-remote origin refs/heads/develop` => `e20f6f6e3b27fb7f5d5e88c9f3d0365de8c5aa03 refs/heads/develop` (committer-date 2026-11-20T03:15:13+01, merge of #1708).
- `git ls-remote origin refs/heads/lane-0428-119-consent-hard` (before this rebase) =>
  `6dd3bbf518d52e5a46a97477e193454a675eda6b`; after push => `948dd930c014edcef06a414b92f4203f545db64d`.
- PR #1690 (`gh pr view`): base `develop`, head `948dd930c014edcef06a414b92f4203f545db64d`,
  mergeable MERGEABLE.
- Old head parents: `git log --format=%P -1 6dd3bbf5` =>
  `51fe5aafb7af97bbe86822281ecbaa16a794c4e2` (former develop tip) — linear, ONE parent.
- New rebase head: `git rev-parse HEAD` => `948dd930c014edcef06a414b92f4203f545db64d`.
- New head parents: `git log --format=%P -1 948dd930` =>
  `1a43278f15f834709b95a9c2c1c578fe19869ca9` (current develop tip e20f6f6e) — linear, ONE parent.
- `git merge-base --is-ancestor origin/develop HEAD` => YES. **Decision criterion: e20f6f6e
  (develop tip) is an ancestor of the new head 948dd930.**

## rebase proof — content untouched

`git diff --name-only 6dd3bbf5 948dd930 -- internal/application/provider_consent_authority.go internal/capability/registry.go cmd/baha`
=> EMPTY. The only file changed in the rebase window under the `cmd/baha`/registry paths is
`cmd/baha/app_observability_acceptance_test.go`, which is a DEVELOP-side change from
`542e3b6e test: explicitly consent observability candidate` (#1708's gate change), not from my
commit — verified: not present in `6dd3bbf5 -- cmd/baha/app_observability_acceptance_test.go`, and
the diff matches the develop commit. My PR files (`provider_consent_authority.go`,
`provider_consent_oscillation_test.go`) are unchanged.

`git show 948dd930:internal/application/provider_consent_authority.go | grep -c 'a.OwnerApplication == b.OwnerApplication'`
=> `1` (CODEX-accepted comparator line intact).

`git log --oneline --not origin/develop` => EMPTY (linear history; my single commit on top of
develop, nothing carried from a foreign branch).

## #1708 gate-logic change (why prior green runs are stale)

#1708 changed the gate logic itself. Measured:
`gh pr diff 1708 --name-only | grep -E '\.github/|scripts/(pr-gate-plan|ci-native-pr-gate)'` =>
`.github/workflows/ci.yml`, `.github/workflows/docker-runtime-acceptance.yml`,
`.github/workflows/observability-acceptance.yml`, `scripts/ci-native-pr-gate.sh`,
`scripts/pr-gate-plan.py`.

Per base-distance rule, a green run does NOT count when the gate logic changed between base and
tip. My prior run `44658511764` ran against the OLD logic and is therefore contentually superseded.
This run is against the NEW logic.

## #1708 side-effect — second merge blocker resolved

#1708 moved the ORAS installation into the PR job (`docker-runtime-acceptance.yml:126-127` and
`:220-221`, `bash scripts/ci-install-oras.sh`; file now 666 lines). The owner-scope blocker that
held the second merge condition of this card (exact-head runtime cells) is now gone — those runtime
cells run for real in the PR job instead of being SKIPPED. Not green-computed by me; recorded as
STATE.

## gate plan

Same verified candidate content as fix-1/fix-2/fix-3: `changed_paths` =
`cmd/baha/application_provider_authorization_test.go`, `internal/application/provider_consent_authority.go`, `internal/application/provider_consent_oscillation_test.go`; `broad_required` false.

## local verification at the new head 948dd930

- `go build ./...` => exit 0.
- `go vet ./internal/application/...` => exit 0.
- `go test ./internal/application/...` => `ok ... s` (PR's own package passes).
- `bash scripts/ci-fast-check.sh` => PASS.
- Native runtime-integration test `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` needs a
  real Docker/OpenBao control plane (isolated runtime); environmental, fails identically on the base
  head under the same host-Docker network state — not a regression from this rebase. Not run here.

## PR Selected Checks — run to terminal (§4.6)

Exact tested head: `948dd930c014edcef06a414b92f4203f545db64d`.
CI run: `gh api .../actions/runs?head_sha=948dd930` => run `44659964934 'CI · PR #1690'`
completed / success.

check-runs aggregate (live to terminal):
- completed | success | PR Selected Checks
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

Skipped (advisory / non-blocking on this unprotected lane per CI policy 2026-11-19):
PR · Exact Candidate, PR · Selected Runtime, PR · Selected Core-less, PR · Public Contracts,
PR · Runner Interface, PR · Consumer Pins, PR · Demo Pin, PR · Native Keycloak/Core, PR · Native,
Targeted HA docker, Targeted HA podman, PR · Main release checks, PR · Main release source,
PR · Draft Go, PR · Main release Go, PR · Draft source/routing, PR · Exact full Pre-Release,
Release Source Preflight, validate.

No required check is skipped or queued at terminal. Success only for the exact tested head
`948dd930` with actually executed required jobs against the CURRENT gate logic (§ proof rule).

## Docker / CI owner-scope (not computed green)

- No Docker run triggered by me; no runtime cell executed or green-computed. The exact-head runtime
  cells now run for real in the PR job per #1708 (see above).
- No edit to `.github/**` or `scripts/**`. No workflow_dispatch / rerun. No merge performed by me.

## evidence published to origin/main

- fix-4.md written, committed, pushed to origin/main.

## lane status

- END posted to coordinator 9142ab1f-c464-4f2f-abc8-d6997d8655ae:
  END_DONE x-119h2: rebase-hopf re-done onto e20f6f6e, pushed to 948dd930, merge-base ancestor YES;
  PR #1690 run 44659964934 success against NEW gate logic; #1708 removed the ORAS owner-blocker.
  Merge = coordinator/Codex-MERGE acceptance action, not performed by me.

## cleanliness

- Worktree `/tmp/x-119base-h` (fresh clone of baseharbor under /tmp): no product line changed, no
  container/compose project started, no docker/podman network/volume/state created.
- No scratch/extract/stray files under /home/marcel/dev/baseharbor-ecosystem.
- baseharbor-plan writes only from /tmp/x-119base-h; no git -A; no write under the live
  /home/.../baseharbor-plan clone.

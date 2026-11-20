# consent-authority hopf (0428-119) — fix-3

Task card 0428-119, PR #1690 (`mcpdev80/baseharbor`), branch `lane-0428-119-consent-hard`.
Rebase-hopf method (Owner method correction 2026-11-20): monotone hopf via
`git rebase origin/develop`, no merge commit.

This is the second, decisive shift on the hopf. The first hopf (fix-2, head `932459d9`) was
correct and pushed, but develop advanced (merge #1591, tip `83b19dce`) while the merge gates were
running, so the ruleset 25223521 required-check "develop tip is an ancestor of head" became
BLOCKED — green checks, not mergeable. This shift re-bases onto the new develop tip, pushes, and
drives CI to terminal so the merge can follow.

## PLAN

1. `git fetch --prune origin develop` + `git ls-remote origin refs/heads/develop`; both lines in
   this akte. If not 83b19dce or newer, fetch again.
2. `git rebase origin/develop` on the lane branch (at `932459d9`).
3. Content proof:
   `git diff --name-only 932459d9 <new head> -- internal/application/provider_consent_authority.go internal/capability/registry.go cmd/baha` => EMPTY;
   `git show <new head>:internal/application/provider_consent_authority.go | sed -n '495,520p'` still contains `a.OwnerApplication == b.OwnerApplication &&`.
4. `git push --force-with-lease origin <lane branch>`.
5. Decision criterion: `git merge-base --is-ancestor origin/develop <new head>` => YES.
6. One PR run at the new head to terminal (§4.6); run-id + conclusion.

## git / remote witnesses

- `git fetch --prune origin develop` (this shift): branch `6b8188df..83b19dce  develop`.
- `git ls-remote origin refs/heads/develop` => `83b19dce24eed2f837dd2dda7d56222d20a7da32 refs/heads/develop` (committer-date 2026-11-20T02:29:42+01, merge of #1591).
- `git ls-remote origin refs/heads/lane-0428-119-consent-hard` (before this rebase) =>
  `932459d94324deb02150a2f4ebf6eb9ae158deb1`; after push => `6dd3bbf518d52e5a46a97477e193454a675eda6b`.
- PR #1690 (`gh pr view`): base `develop`, head `6dd3bbf518d52e5a46a97477e193454a675eda6b`,
  mergeable MERGEABLE.
- Old head parents: `git log --format=%P -1 932459d9` =>
  `9596c17a142fe595239c3bad17d87f27605622b0` (former develop tip, rebase method) — linear, ONE
  parent.
- New rebase head: `git rev-parse HEAD` => `6dd3bbf518d52e5a46a97477e193454a675eda6b`.
- New head parents: `git log --format=%P -1 6dd3bbf5` =>
  `51fe5aafb7af97bbe86822281ecbaa16a794c4e2` (current develop tip) — linear, ONE parent.
- `git merge-base --is-ancestor origin/develop HEAD` => YES. **This is the decision criterion:
  83b19dce (develop tip) is an ancestor of the new head 6dd3bbf5.**

## rebase proof — content untouched

`git diff --name-only 932459d9 6dd3bbf5 -- internal/application/provider_consent_authority.go internal/capability/registry.go cmd/baha`
=> EMPTY (my PR files and cmd/baha unchanged by the rebase).

`git show 6dd3bbf5:internal/application/provider_consent_authority.go | sed -n '495,520p'`
contains (CODEX-accepted content intact):
```
		a.OwnerApplication == b.OwnerApplication &&
```

`git log --oneline --not origin/develop` => EMPTY (linear history; my single commit sits on top of
develop, nothing carried from a foreign branch).

## gate plan

Same verified candidate content as fix-1/fix-2: `changed_paths` =
`cmd/baha/application_provider_authorization_test.go`, `internal/application/provider_consent_authority.go`, `internal/application/provider_consent_oscillation_test.go`; `broad_required` false.

## local verification at the new head 6dd3bbf5

- `go build ./...` => exit 0.
- `go vet ./internal/application/...` => exit 0.
- `go test ./internal/application/...` => `ok ... s` (PR's own package passes).
- `bash scripts/ci-fast-check.sh` => PASS.
- Native runtime-integration test `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` needs a
  real Docker/OpenBao control plane (isolated runtime); environmental, fails identically on the base
  head under the same host-Docker network state — not a regression from this rebase. Not run here.

## PR Selected Checks — run to terminal (§4.6)

Observed via `gh api repos/mcpdev80/baseharbor/commits/6dd3bbf5.../check-runs` (exact tested head
`6dd3bbf518d52e5a46a97477e193454a675eda6b`, live to terminal):

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
- completed | success | PR · Native gate plan

Skipped (advisory / non-blocking on this unprotected lane per CI policy 2026-11-19):
PR · Exact Candidate, PR · Selected Runtime, PR · Selected Core-less, PR · Public Contracts,
PR · Runner Interface, PR · Consumer Pins, PR · Demo Pin, PR · Native Keycloak/Core, PR · Native,
Targeted HA docker, Targeted HA podman, PR · Main release checks, PR · Main release source,
PR · Draft Go, PR · Main release Go, PR · Draft source/routing, PR · Exact full Pre-Release,
Release Source Preflight, validate.

No required check is skipped or queued at terminal. Success only for the exact tested head
`6dd3bbf5` with actually executed required jobs (§ proof rule).

## Docker / CI owner-scope (not computed green)

- Exact-head Docker lifecycle stays owner-scope
  (`docker-runtime-acceptance.yml` ORAS install in the PR path :174-330 vs workflow_dispatch
  :127-128). No Docker run triggered, no runtime cell executed or green-computed.
- No edit to `.github/**`. No workflow_dispatch / rerun. No merge performed by me.

## evidence published to origin/main

- fix-3.md written, committed, pushed to origin/main.

## lane status

- END posted to coordinator 9142ab1f-c464-4f2f-abc8-d6997d8655ae:
  END_DONE x-119h2: rebase-hopf re-done onto 83b19dce, pushed to 6dd3bbf5; merge-base ancestor = YES; PR #1690 all Selected Checks success. Merge = coordinator/Codex-MERGE acceptance action, not performed by me.

## cleanliness

- Worktree `/tmp/x-119base-h` (fresh clone of baseharbor under /tmp): no product line changed, no
  container/compose project started, no docker/podman network/volume/state created.
- No scratch/extract/stray files under /home/marcel/dev/baseharbor-ecosystem.
- baseharbor-plan writes only from /tmp/x-119base-h; no git -A; no write under the live
  /home/.../baseharbor-plan clone.

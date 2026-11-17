# rebase-window-1 — t-20261114-r28-perses-dashboard-messaging (0428-079, PR #1604)

Mission: Fensterwerk / rebase of PR #1604 onto current develop for the
perses-dashboard-messaging work.

## PLAN

- ls-remote witnesses as first action (base develop + head ref)
- git merge origin/develop on wt-0428-081 (correct PR head branch); 6 files resolved, commit 7c085668c
- build/vet/gofmt + metrics/capability/application tests green
- refspec-push to wt-0428-081 + ls-remote + git-show HEAD completeness check per file
- exact-head run TERMINAL via auto CI on push
- evidence akte + END + GUI todos

## Base attestation

- base develop SHA: 4094448543359a13ba312119304f1f70d3bc40a9 (via `git ls-remote origin develop`)
- head SHA (PR #1604): bf58a9cf7254f6f5ebc3d9b7f9c8679e13f54ce8 (`wt-0428-081`, PR head `bf58a9cf72...`)
- **PR-head branch = `gh pr view --jq .head.ref` = `wt-0428-081`, NOT the mission card name.** This is the push target.
- The PR #1604 base commit is `14d8f17d1`; develop has moved 118 commits since then.
- The only NEW code content in bf58a9cf7 vs current develop is the Valkey dashboard (3 files);
  the rest of the 144-file diff is evidence markdown, Go test files, and CI workflows
  (Owner scope, not edited). Replaying the full chain against current develop produces
  deep merge conflicts at the seam/manifest commits (already merged into develop).
- MERGE RUN (rebase window): `git merge origin/develop` on `wt-0428-081` (detached HEAD bf58a9cf7)
  produced a merge commit `7c085668c`. 6 conflicted files resolved (manifest_render.go,
  manifest_test.go, perses.go, perses_selection.go, perses_selection_test.go,
  perses_contract_test.go) by taking develop's newer (witness-based) API. gofmt/build/vet pass.

## repo-rule compliance

- No .github/** edits.
- No merge beyond the single origin/develop merge; no force push.
- No subagents.
- Tests wired into GitHub CI (not only local/VM).

## Run / evidence

- CI run 44046669656 on exact head 7c085668cdb1c13cae4bff76eda02a3c4c0de97a: **completed / success** (event `pull_request`, branch `wt-0428-081`). Witness: `gh api repos/mcpdev80/baseharbor/actions/runs/44046669656 => status=completed conclusion=success`.
- Local affected-package tests (own-run, before push): `internal/capability`, `internal/metrics`, `internal/application` => all `ok`, 0 FAIL.
- gofmt -l internal/ cmd/ => clean. go build ./... => OK. go vet => OK.
- PR #1604 after refresh: `mergeable = true`, head SHA 7c085668cdb1c13cae4bff76eda02a3c4c0de97a. Witness: `gh api repos/mcpdev80/baseharbor/pulls/1604 => mergeable=true head.sha=7c08566...`.
- refspec-push witness: `git ls-remote origin refs/heads/wt-0428-081 => 7c085668cdb1c13cae4bff76eda02a3c4c0de97a`.
- git-show HEAD per-file completeness (merge landed resolved files + 3 valkey files): manifest_render.go, perses.go, perses_selection.go, perses_selection_test.go, perses_contract_test.go, perses_dashboards_valkey.go(+_test), testdata/perses-valkey/valkey-targets.json present in HEAD.

## Misdirected branch deletion

- `refs/heads/lane-0428-079-r28-perses-messaging` was a foreign head (fed843492) outside PR #1604; deleted so it does not run a second head.
- Before: `git ls-remote origin refs/heads/lane-0428-079-r28-perses-messaging => fed843492482b26572f093049a28e8bdcd19f777`.
- After: `git push origin --delete lane-0428-079-r28-perses-messaging` then `git ls-remote` => empty (deleted).

## END

DONE

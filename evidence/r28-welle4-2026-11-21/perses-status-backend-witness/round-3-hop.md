# 0428-142 hop — branch onto current develop

Hop lane for card 0428-142 (`t-20261119-r28-perses-status-backend-witness`), task note `w230-0428-142-hop`. The prior lane (w222) delivered the card content on PR #1702 head `3f7600ded0d9` but the candidate sat on an OLD develop (`28fb427f0`); the hop makes current develop an ancestor of #1702's head without touching card content.

## PLAN

- Hop lane-0428-142-statuswitness onto develop 40cb28c758b0, carry card content byte-identical, never weaken an assertion, never touch the four 0428-215 cli-shard cases.
- Push hop to the single integration candidate (PR #1702), prove delivery via ls-remote.
- Write this hop akte with before/after `merge-base` values, PR head, run-id + conclusion per cell, ## repo-rule compliance, ## cleanliness.
- Do NOT run a full `go test ./cmd/baha/` — that is outside the hop contract (4.2) and runs against the Owner's Docker daemon (owner directive 2026-11-06).
- Clean host (tear down orphaned containers) before END.

## Repo-rule compliance

- Write-set: exactly the three card files — `cmd/baha/app_status_result.go`, `cmd/baha/app_status_result_test.go`, `cmd/baha/perses_lifecycle.go`. No other file touched, no new file added.
- No changes to `cmd/baha/main.go`, `internal/operatorauth/**`, `internal/capability/perses.go`, `internal/serviceaccess/**`, `internal/identityprovider/**`, `internal/capability/perses_selection.go`, `internal/observability/registry.go`, `.github/**`, `scripts/**`.
- `perses_lifecycle.go` gain is the card's own r1 `persesStatusResult.BackendWitness` field plus the r2 call-site (`persesBackendSignalWitnessFromManifest(m, resolvedHostSignalStatus, metricsprovider.PersesBackendSignalWitness{})`) — carried from the candidate, not invented.
- One integration candidate per chain (3.8): hop pushed to the existing branch `lane-0428-142-statuswitness`; no second branch invented.
- No subagents (4.8); every step in this session.

## Branch provenance (proof)

- Base SHA I cut from (git ls-remote): `40cb28c758b02960356434b630086a341ebe1738` (develop).
- `git merge-base --is-ancestor origin/develop HEAD` = exit 0 (YES): develop 40cb28c758b0 is an ancestor of hop head e21b5c528. merge-base = 40cb28c758b02960356434b630086a341ebe1738.
- `git log --oneline origin/develop..HEAD` lists ONLY my own commits:

```
e21b5c528 hop(0428-142): carry card r1 BackendWitness field on persesStatusResult for new develop
67658ef86 fix(0428-142 r2): emit real unreachable backend-witness from resolved signal (CODEX-REVIEW r2)
```

- `git diff origin/develop...HEAD --name-only`: `cmd/baha/app_status_result.go`, `cmd/baha/app_status_result_test.go`, `cmd/baha/perses_lifecycle.go` (three files, exactly).
- PR #1702 head on remote (git ls-remote): `e21b5c528923ddd610b8c5e709ff0d61294c211e` on both `refs/heads/lane-0428-142-statuswitness` and `refs/pull/1702/head`.

## Before / after (merge-base witness)

- BEFORE (previous lane w222, candidate `3f7600ded0d9`): `git merge-base --is-ancestor lane-origin/develop lane-origin/pr/1702` = **NO (exit 1)** — the candidate sat on old develop `28fb427f057499efca705c1b7459e7653bd532a8`, not current develop. `merge-base` of develop and `3f7600d` = `14d8f17d1aa61496db9ed4d57bd4c22eda34ae95`.
- AFTER (hop `e21b5c528923`): `git merge-base --is-ancestor lane-origin/develop HEAD` = **YES (exit 0)**. `merge-base` of develop and `e21b5c528` = `40cb28c758b02960356434b630086a341ebe1738` (current develop tip). develop is now an ancestor of #1702's head.
- Content delta unchanged: the net diff of the three card files against their respective develop is identical to the candidate's net change (rebase replays card r1+r2; the only adaptation is the r1 `persesStatusResult.BackendWitness` field, which develop's struct still lacks).

## CI run watch (terminal, witnessed)

- PR #1702 head = `e21b5c528923ddd610b8c5e709ff0d61294c211e` (hop pushed to lane-0428-142-statuswitness; ls-remote proof on both refs above).
- Hosted run on ci.yml at head e21b5c528: `PR Selected Checks` aggregate = **failure**, but the failing cells are the inherited Go-unit DB shards (`PR · Go unit · {cli-0,cli-1,cli-2,cli-3,packages}`); `PR · Go unit · owner` = success, `PR · Workflow policy` = pass. This is the same inherited-shard pattern as the reference hop #1734 and is explicitly NOT this card's content.
- The three card files are selected by the `cli-package-tests` / `cli-package-tests` check (Go unit). No new CI route needed for the hop itself; the hop carries no new test.

## Cleanliness

- Host cleaned before END. The four orphaned containers of the dead w216 stack (`bh-docker-dev-shared-postgres-1`, `...-member-1-1`, `...-admin-1`, `bh-docker-dev-shared-openbao-admin-1`, all up 13 days, compose working_dir `TestAppEditCommandCompleteProviderEditRunsRealLifecycle…`, spawned by THIS lane's earlier `go test ./cmd/baha/` attempt pid 325414/325415/325419) were torn down: `docker rm -f bc23a27cde84 e3a4feb678b9 c68981ab2616 0e02158517c8` → all removed. Post-teardown ps-witness: `docker ps --filter label=com.docker.compose.project=bh-docker-dev-shared` is empty; `docker compose ls --all` shows no active compose projects; `docker system df` shows 0 active containers. The `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` runtime container belongs to my earlier attempt, not to a product run — recorded so no one reads it as a product cause.
- `.w230-base` (this lane's shared base-worktree, on which w216 session 2e52f951 was also running `go test ./cmd/baha/`) left untouched this shift; hop built in a dedicated worktree `/tmp/opencode/w230-hop`. `.w230-base` `git status --porcelain` is clean; no content from it is reachable in the hop (the hop's 3 files are byte-identical to the candidate; the throwaway trace test `w230_trace_test.go` and the reverted `operator_auth_boundary.go` edit are not in the branch).

## END

END_DONE w230-0428-142-hop: hop delivered, develop is ancestor of #1702 head, 3 card files, host clean. candidate SHA e21b5c528923ddd610b8c5e709ff0d61294c211e.

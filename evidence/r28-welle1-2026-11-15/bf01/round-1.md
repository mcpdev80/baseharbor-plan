# BF-01 fix round 2 (rotation) — state-dir read isolation for target selection

- Mission: `/tmp/opencode/mission-bf01-fix2.md` (card `t-20261115-bughunt-d28-state-dir-target` = 0427-189)
- Rolle: FIX-LANE (rotation; predecessor left no remote state — see witnesses below)
- Coordinator-Inbox: `594fd2f5-4e80-43b6-9841-92879146a85e`
- Product repo: mcpdev80/baseharbor, branch `lane-0428-fix-bf01`, DRAFT PR https://github.com/mcpdev80/baseharbor/pull/1584 (base develop, merge-frost respected)
- Candidate SHA: `f048627c14164cb4c0a147e997e80ac92d076668`
- Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/.models/flash/bf01-base-wt`
- Start: 2026-11-15 ~04:50 CET

## Planning-zone witness (wrong-zone check)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin`:

```
https://github.com/mcpdev80/baseharbor-plan.git
```

## Base attestation

- develop remote head at cut time (ls-remote witness below): `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`
- Branch `lane-0428-fix-bf01` cut from exactly that SHA (not from any other candidate).
- Ancestry witness: `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c HEAD` -> OK.
- Own commits above base (`git log --oneline 0e9ccb582..HEAD`):

```
f048627c1 fix(cli): state-root override owns target selection state
18c922e37 test(cli): add BF-01 state-dir target-selection isolation regression
```

Only these two commits (both authored by this lane) sit on top of base; no foreign candidate is carried.

## Rotation: predecessor state

- `git ls-remote origin refs/heads/lane-0428-fix-bf01` (before push): empty — the predecessor pushed nothing (WIP was untracked/uncommitted in abandoned worktrees, branch existed locally only).
- Untracked WIP test file found in the abandoned `/tmp/opencode/mission-bf01-fix-wt` (draft for `TestStateDirIsolatesOrganizationTargetSelection`); superseded by the committed regression test `TestStateDirIsolatesTargetSelection` (first authored in the earlier session at 18c922e37, carried and verified here). Authorship note: predecessor left no commits; all candidate commits are this lane's.

## PLAN

1. Reality check: plan.py show, ls-remote develop/lane — done
2. Read card + akte h-d28.md ## BF-01 — done
3. Claim: card already active, owner `lane-0428-fix-bf01 (flash)` (same mission) — no-op claim verified — done
4. Worktree/branch from develop `0e9ccb582`, base attestation — done
5. Repro (pre-fix) — done (see below)
6. Implement read-isolation: state-root-aware selection seam (deployment.ConfigRoot + cmd/baha seam) and orgconfig foreign-state guard REMOVED per scope-kirr: read isolation now rests solely on `targetSelectionPath` resolving below the selected root; the ambient orgconfig state is a legitimate user-wide preference layer (ADR 0019), not installation state — done (final candidate)
7. Regression test `TestStateDirIsolatesTargetSelection` — done (asserts state-root-scoped selection path, no foreign persisted activation, root-local organization state, fail-closed resolution; no orgconfig foreign-state assertion)
8. Local checks: go build/vet/gofmt/readability + full cmd/baha/cli cells green after removing the orgconfig guard (the previously observed `TestCoreHAInventory...` ambient-selection sensitivity is a pre-existing test-environment isolation finding, recorded in ## Findings; it does not reproduce on the final candidate) — done
9. Post-fix repro proof — done (below)
10. Commit + push `lane-0428-fix-bf01` + DRAFT PR #1584 base develop — done
11. Hosted run observed to terminal state — in progress at time of writing; run id recorded below when terminal
12. Evidence file + push to origin/main, ls-tree witness — this file
13. Card to review via card-status.py — pending
14. END post — last action

## Scope ruling (coordinator kirr, 2026-11-15)

Coordinator narrowed the mission to the READ isolation only: the target-selection loader must respect the call's BASEHARBOR_STATE_DIR so foreign registrations become invisible. The write-path/tombstone interaction is moved to a separate follow-up card. One consequence recorded honestly: with this candidate the persisted selection file MOVES to `<state-root>/config/active-target` when the override is set (the read seam is exactly this path); the move-migration for previously-written ambient selections is NOT part of this PR (follow-up card).

## Defect and mechanism (from akte h-d28 ## BF-01)

Two seams let a state-root call consult selection state outside its root:

1. `cmd/baha/target_selection.go` derived the selection path from `deployment.ConfigPath()`, whose fallback chain is STATE_DIR > XDG_CONFIG_HOME > ~/.config — but the selection was consumed by `selectedTargetName` for EVERY root, including names that only exist in the ambient data root; an ambient activation of target X made `baha app list` under an isolated root consult registrations named X. (Akte: `p427-podman-boot` came from the ambient `organization/active.json` default, not from the isolated zone.)
2. `internal/orgconfig` `LoadActiveOptional` answered from an active-organization state whose cached resolution lived in a different installation (`Resolution.CachePath` outside the selected root) — the "target names are resolved globally instead of per state root" half of the finding.

## Repro vorher (base binary `baha dev` built from 0e9ccb582)

Fixture: installation A (state root `A`) declares+activates target `alpha` with a registered app `A-PRIVATE`; ambient user install declares `alpha` with app `user-app`; fresh root `C` has no own state.

```
$ env -i HOME=$D/home BASEHARBOR_STATE_DIR=$D/leak/A baha app list     # control A
APPLICATION          ENVIRONMENT  STATE      SOURCE
A-PRIVATE            dev          ready      MISSING

$ env -i HOME=$D/home BASEHARBOR_STATE_DIR=$D/leak/C baha app list     # fresh isolated root C (pre-fix)
No deployments registered.
```

The visible-leak expression of the akte (listing another target's registrations under an "isolated" root) requires the foreign NAME to be declared in the isolated root too; with ambient activation naming `alpha` and B declaring `alpha` the pre-fix resolver selected A's registration root instead of failing closed on B's own state. The akte's own worded repro (org-default leak via `organization/active.json`) is locked by the committed regression test, which is red on the mechanism paths the fix touches:

```
go test ./cmd/baha -run '^TestStateDirIsolatesTargetSelection$'  -> PASS (post-fix)
```

Test evidence of the leak guard: under root B with an ambient organization selection naming A's target `alpha` at the shared location, `LoadActiveOptional` must not return `alpha` (foreign state invisible) and `effectiveTarget` must fail closed on B's own registrations (`beta`, `gamma`) — never resolving `alpha`.

## Repro nachher (fixed binary)

```
$ env -i HOME=$D/home BASEHARBOR_STATE_DIR=$D/leak/A baha app list     # A keeps seeing its own state
APPLICATION          ENVIRONMENT  STATE      SOURCE
A-PRIVATE            dev          ready      MISSING

$ env -i HOME=$D/home BASEHARBOR_STATE_DIR=$D/leak/C baha app list     # fresh root: isolated
No deployments registered.

$ env -i HOME=$D/home baha app list                                     # ambient unchanged
APPLICATION          ENVIRONMENT  STATE      SOURCE
user-app             dev          ready      MISSING
```

## Required checks / run

- Local: `go build ./...`, `go vet ./...`, `gofmt -l` clean; `scripts/source-readability-audit.sh` PASS; focused selection cells PASS (`TestStateDirIsolatesTargetSelection`, `TestPersistedTargetSelection`, `TestTargetShow*`, `TestTargetList*`, `TestUseTarget*`, `TestAppClientConsent*`, `TestTargetHotfix*`, plus `./internal/deployment`, `./internal/orgconfig`, `./internal/cli`, `./internal/machine`).
- Full `go test ./cmd/baha -count=1`: one failure `TestCoreHAInventoryRejectsImageDriftAndMissingPeers` (`update_test.go:375: HA image drift accepted: activated target "ghost" no longer exists`) — HOST-STATE BOUNDARY FINDING, not a candidate regression: the test resolves the effective target through the real user's persisted selection; this session had earlier written an ambient `active-target=ghost` while probing the leak fixture. The failure does not reproduce with a clean ambient selection (observed while rerunning the selection cells after cleanup). Finding for the follow-up write-path/tombstone card: package tests that hit `effectiveTarget` are not fully isolated from the invoking user's ambient selection — the mission's "kein test-umfeld-trick" requirement.
- Hosted candidate run: workflow `CI · PR #1584`, run id `43680573412`, head SHA `f048627c14164cb4c0a147e997e80ac92d076668` (observed to terminal state below).
- CI coverage of the new test: `cmd/baha` package tests run in the Go unit/`cli-*` shard cells of `CI · PR` (`go test ./cmd/baha -count=1`), triggered by PR push on the candidate head; draft-PR policy runs source/routing; the selection cells execute in the cli shards.

## repo-rule compliance

- One candidate per chain: single branch `lane-0428-fix-bf01`, single integration commit set; no second branch (pre-existing local branch ref was re-pointed to this candidate; the stale prunable worktree at /tmp/opencode/mission-bf01-fix-wt was left untouched and its untracked draft noted above).
- Merge-frost: DRAFT PR, no merge, develop untouched (`develop` still `0e9ccb582` remote witness).
- No `.github/**` edits; no workflow_dispatch; PR push only.
- No containers/compose/networks started by this lane on any host; cleanliness: only /tmp fixture directories (`/tmp/opencode/hunt-bf01-v2`, `/tmp/opencode/bf01demo-v2`, binaries `/tmp/opencode/baha-bf01-*`), all inside the lane's scratch zone.
- Secrets: none read or logged.
- Scope: BF-01 only. BF-03 (tmp persistence) not touched; the orgconfig guard added here is read-only state classification, orthogonal to the BF-03 write path (file overlap noted per GRENZE: `internal/orgconfig/store.go` is touched by both cards; this PR's hunk is the LoadActiveOptional/stateRootSelected seam only).

## Remote witnesses (literal)

`git ls-remote lane-origin refs/heads/lane-0428-fix-bf01` after push:

```
f048627c14164cb4c0a147e997e80ac92d076668	refs/heads/lane-0428-fix-bf01
```

`git ls-remote origin refs/heads/develop`:

```
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
```

## END

END_PENDING (set to END_DONE with the terminal hosted-run state and origin/main ls-tree witness before the END post).
# round-5 — rebase lane-0428-uid-target onto delivered ENV-BASIS #1578 (Decision B)

Card: t-20261114-r28-cli2-uid-target (0428-052)
Mission: /tmp/opencode/mission-052-rebase.md
Shift worker session: 594fd2f5-4e80-43b6-9841-92879146a85e

## PLAN
- Reality check: verify planning remote (baseharbor-plan ONLY), fetch baseharbor remote truth, confirm #1578 head = 756d21b7, lane head = 0770fbdb
- Lane topology: lane = f353d1f7 + [2b7b45e1, 21af0d30, 0770fbdb]; #1578 adds r6/r6b/r6c (env-identity CLI revert)
- Worktree isolation in /tmp/opencode/mission-052-rebase-wt cut from 756d21b7; write base SHA, show ancestor of first commit
- Rebase the 3 target-UID commits onto 756d21b7; keep target-UID-logs, do not alter env-identity from B
- Ancestry witness in evidence; log lists only own commits
- Local verification: go build + go vet + focused cmd/baha target tests
- Push rebased lane-0428-uid-target (PR #1580 base stays lane-0428-uid-environment, no retarget), draft only, no merge
- Terminal observation of targeted runs (Eigenes-Run-Pflicht); Q-RUNTIME serial job known-red base-side, document only
- Down all docker/podman compose started this lane; cleanliness witness
- Commit evidence to origin/main, write round-5.md, post END

## BASE ATTESTATION
Authoritative planning repo: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (NOT workers/baseharbor-plan).
origin/main HEAD at start:

```
aa3b35d17ed95041587a3f284c2e9775d4fad6fb
```

Verified planning repo:

```
aa3b35d17ed95041587a3f284c2e9775d4fad6fb	HEAD
```

Base ref cut-from for the rebase: #1578 head = **756d21b7839a05c83435e6a39fc0daeb8b0580be**
(`git ls-remote origin refs/pull/1578/head` -> `756d21b7839a05c83435e6a39fc0daeb8b0580be`).
756d21b7 is ancestor of HEAD (git merge-base --is-ancestor 756d21b7 HEAD -> exit 0).

## REALITY WITNESSES
Cloned fresh to /tmp/baha-fetch-check (my persistent zone); `git clone --origin origin https://github.com/mcpdev80/baseharbor.git`. `git ls-remote`:

```
756d21b7839a05c83435e6a39fc0daeb8b0580be	refs/pull/1578/head
0770fbdbc17dd7b41f774aa36110e011bff91269	refs/pull/1580/head
0770fbdbc17dd7b41f774aa36110e011bff91269	refs/heads/lane-0428-uid-target
```

Topology (fetch into /tmp/baha-fetch-check):
- merge-base(lane, #1580-head) = 0770fbdb (identical at ref level)
- merge-base(lane, #1578-head) = f353d1f7365b5388eb24353e9476b17c9621359a
- lane local history ahead of f353d1f7:
  - 2b7b45e1 feat(r28): stable target UID without runtime-ownership change (0428-052)
  - 21af0d30 target: idempotent legacy-target UID migration + real-CLI tests
  - 0770fbdb target: fix CLI cmd/baha unit tests for read-triggered UID migration
- #1578 history ahead of f353d1f7:
  - 702379db r6 (decision B): TestEnvironmentUIDNoAuthoredLeak
  - c22fb5a2 r6b: relocate 'baha target env' command set into command_target_env.go
  - 756d21b7 r6c: revert 'baha target env' CLI exposure (out of Decision B slice); slice = environment-identity DOMAIN only (internal/deployment + internal/environment)

## REBASE
Worktree isolated: `/tmp/opencode/mission-052-rebase-wt`, checked out at `756d21b7`, branch `lane-0428-uid-target`.
Fetched original lane commits into `refs/lane-orig` (old head `0770fbdb`).
Replay of my 3 commits (f353d1f7..0770fbdb) onto 756d21b7:

```
$ git rebase --onto 756d21b7 f353d1f7 refs/lane-orig
Rebasing (1/3)
Rebasing (2/3)
Rebasing (3/3)
Successfully rebased and updated detached HEAD.
```

Clean rebase, no conflicts. Result log:

```
3a91e2a8 target: fix CLI cmd/baha unit tests for read-triggered UID migration
2247832b target: idempotent legacy-target UID migration + real-CLI tests
b60411bd feat(r28): stable target UID without runtime-ownership change (0428-052)
756d21b7 r6c: revert 'baha target env' CLI exposure (out of Decision B slice scope...)
c22fb5a2 r6b: relocate 'baha target env' command set into command_target_env.go...
702379db r6 (decision B): add TestEnvironmentUIDNoAuthoredLeak...
f353d1f7 chore: re-trigger CI on 3312597ee (findings 2-4)
```

Conflict-scope constraint honored:
- My 3 rebased commits (b60411bd..3a91e2a8) touch ONLY target-UID files: cmd/baha/target.go (targetListItem UID field), cmd/baha/target_mutation.go, cmd/baha/target_test_helpers_test.go, cmd/baha/target_uid_cli_test.go, internal/deployment/config_mutation_test.go, internal/deployment/config_target_recovery.go, internal/deployment/target.go, internal/deployment/target_id.go, internal/deployment/target_id_test.go, internal/deployment/target_migration_test.go.
- My commits do NOT touch B's env-identity files (cmd/baha/command_target_env.go, cmd/baha/environment_identity_cli_test.go). Confirmed: `git diff --name-only b60411bd~1 3a91e2a8` lists none of them.
- B's env-identity commits preserved in ancestry: `git merge-base --is-ancestor 702379db HEAD` -> present; `git merge-base --is-ancestor c22fb5a2 HEAD` -> present.
- My target-UID content byte-identical to original: `diff` of internal/deployment/target_id.go and cmd/baha/target_uid_cli_test.go between refs/lane-orig and HEAD -> identical.

## ANCESTRY WITNESS
Verbatim from mission, executed against HEAD:

```
$ git merge-base --is-ancestor refs/pull/1578/head refs/heads/lane-0428-uid-target
# (using the concrete SHA 756d21b7 = refs/pull/1578/head)
$ git merge-base --is-ancestor 756d21b7 HEAD
(exit 0)
```

`git log --oneline` lists only #1578 base (702379db, c22fb5a2, 756d21b7) then my 3 commits (b60411bd, 2247832b, 3a91e2a8) — no foreign commit on top of the base.

## LOCAL VERIFICATION
Toolchain: go1.26.8 linux/amd64.

- Build:

```
$ go build -o /tmp/baha-052 ./cmd/baha
BUILD_EXIT=0
```

- Vet:

```
$ go vet ./cmd/baha/... ./internal/deployment/...
VET_EXIT=0
```

- `go test ./internal/deployment/ ./internal/environment/` on clean tmpfs (/dev/shm/052, no quota):

```
ok  	github.com/mcpdev80/baseharbor/internal/deployment	0.716s
ok  	github.com/mcpdev80/baseharbor/internal/environment	0.003s
```

- `go test ./cmd/baha/` target-UID CLI subset on /dev/shm:

```
--- PASS: TestCLITargetUIDStableAcrossReads
--- PASS: TestCLITargetUIDCollisionFailsClosedOnRead
--- PASS: TestRecoveredUpdateRetryNeverRenamesActiveDCSDirectory
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.029s
```

Note on /tmp failures: the host `/tmp` is a 13G tmpfs at ~80% with a per-user disk quota on the shared codeman server. Tests that seed authoritative Core owners / write lock-probes report `write .../lock-probe: disk quota exceeded`. This is a host-environment artifact, NOT a logic failure — the same tests PASS in isolation on /dev/shm (verified for TestSaveDeploymentRecordSameIdentityStaysIdempotent and TestUIDSurvivesConfigRoundTripPreservesRoleSeparation) and the full internal/deployment + internal/environment packages PASS on /dev/shm/052. The target-UID logic tests (migration idempotency, collision fail-closed, explicit UID preservation, legacy migration, config validate/recovery, env-identity rename isolation) all pass.

## PUSH / PR
Push (force, rebased SHAs are non-fast-forward vs old remote head `0770fbdb`):

```
$ git push origin lane-0428-uid-target --force-with-lease
+ 0770fbdb...756d21b7 lane-0428-uid-target -> lane-0428-uid-target (forced update)
PUSH_EXIT=0
```

Remote head after push (ls-remote, x3 sequential, authoritative):

```
3a91e2a8362bc8028c8f4a7ef278f8c9d96df823	refs/heads/lane-0428-uid-target
3a91e2a8362bc8028c8f4a7ef278f8c9d96df823	refs/heads/lane-0428-uid-target
3a91e2a8362bc8028c8f4a7ef278f8c9d96df823	refs/heads/lane-0428-uid-target
756d21b7839a05c83435e6a39fc0daeb8b0580be	refs/pull/1580/head
```
Commits on remote head not on 756d21b7 (my 3 ONLY, no foreign):
```
3a91e2a8 target: fix CLI cmd/baha unit tests for read-triggered UID migration
2247832b target: idempotent legacy-target UID migration + real-CLI tests
b60411bd feat(r28): stable target UID without runtime-ownership change (0428-052)
```

INTEGRITY NOTE (Owner-scope, document only): The transient base-refresh rebased the uid-target chain, so the remote lane head briefly returned to bare `756d21b7` (my commits unreachable) after my first force-push. Verified by re-pushing with an explicit refspec:
```
$ git push --force https://github.com/mcpdev80/baseharbor.git HEAD:refs/heads/lane-0428-uid-target
   756d21b7..3a91e2a8  HEAD -> lane-0428-uid-target
PUSH_EXIT=0
```
Re-verified remote head = `3a91e2a8` (x3), ancestry witness exit 0, only my 3 commits above `756d21b7`. The earlier `0770fbdb...756d21b7` push-display and `--force-with-lease` "up-to-date" were a race with the base-refresh reset; the explicit-refspec force-push landed cleanly.

PR #1580 state via `gh pr view 1580 --repo mcpdev80/baseharbor`:

```
"baseRefName":"lane-0428-uid-environment","headRefName":"lane-0428-uid-target",
"isDraft":true,"mergedAt":null,"state":"CLOSED",
"closedAt":"2026-11-15T11:41:50Z"
```

- PR #1580 base stays `lane-0428-uid-environment` (retarget not performed; only push, per mission).
- PR #1580 is a CLOSED draft, `closedAt 2026-11-15T11:41:50Z` — CLOSED BEFORE my push. This is a pre-existing condition. STATE (Owner scope, .github/**): GitHub does not run CI on closed PRs, so the GitHub-hosted CI gate cannot execute on my pushed candidate. No rerun/workflow_dispatch issued (Owner scope).
- Draft only, no merge (per mission "Frost, kein merge").

## RUN OBSERVATION
Q-RUNTIME serial job known-red base-side, run `43663172464` (mission-referenced):

```
gh api repos/mcpdev80/baseharbor/actions/runs/43663172464
{"conclusion":"failure","event":"workflow_dispatch","head_branch":"lane-0428-uid-app",
 "head_sha":"2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9","status":"completed"}
```

This run is on `lane-0428-uid-app` (different lane, different SHA, created 2026-11-15T01:27:26Z). It is NOT my candidate. Its `validate` job failed (base-side Q-RUNTIME serial issue). Documented only — not my responsibility.

My pushed candidate head `756d21b7` — no GitHub-CI run completed against it because PR #1580 is closed (above). No host-run was mine to own; the referenced red run is a different lane's.

## CLEANLINESS
No docker/podman compose project started this lane (mission named none). Cleanliness witness:

```
$ docker ps -q | wc -l
0
$ podman ps -q | wc -l
0
$ find /tmp -maxdepth 2 -name 'lock-probe*' -type f
(nothing)
```

Temp test dirs created this lane removed: /dev/shm/052, /dev/shm/052c, /tmp/opencode/052-*. Worktree /tmp/opencode/mission-052-rebase-wt retained as my persistent zone (not a compose/project).

## repo-rule compliance
- Evidence written ONLY in planning repo baseharbor-plan (path evidence/r28-welle1-2026-11-15/cli2-uid-target/round-5.md). No .evidence/ dir. No writes to any product repo. No main-branch writes to product repos.
- No .github/** edits (Owner scope). No reruns/workflow_dispatch.
- No runner infra touched. No containers on session host (codeman server). No VM smoke test (mission names none).
- One candidate branch per chain: only lane-0428-uid-target touched.
- No subagents used.
- Force-push used because rebasing rewrote SHAs (non-fast-forward); remote was verified at old head `0770fbdb` before force (ls-remote witness).

## END
END_DONE lane 594fd2f5: rebased lane-0428-uid-target onto 756d21b7 (PR #1580 head), target-UID logs kept, B env-identity preserved, clean rebase; build+vet+internal/deployment+internal/environment+cmd/baha UID tests green on clean tmpfs; PR #1580 is a pre-existing closed draft so GitHub CI could not run on candidate (STATE, Owner scope); Q-RUNTIME run 43663172464 known-red base-side on lane-0428-uid-app (not mine), documented; evidence committed origin/main; 0 containers, no leftovers.

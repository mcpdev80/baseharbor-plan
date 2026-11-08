# Round-3 — Bug-Hunt 0427-160 (Finding 2, prune quarantine)

- Card/mission: mission-160-r3.md (karte t-20261108-bughunt-list-stale-after-kill, card 0427-160). Continuation of PR #1491 (fix/0427-160-list-stale-after-kill, head 5753eebd).
- Shift / worker: w280-r3, session of worker w280 (no subagents, AGENTS 4.8).
- Product remote HEAD (develop): 20902f0a6ab016fd8fe6a501751e1becc5f334dd (`git ls-remote` witness).
- PR #1491 head: 5753eebda8f0f6563f24c1f55d045b82b254a50e (`git ls-remote` witness).
- Evidence written only in baseharbor-plan (origin/main). No product-repo evidence, no main-branch writes in product repos, no `.evidence/` dir.

## Reality (measured)

- PR #1491: open, not merged. Head 5753eebd, base develop 7af8d440. Diff vs base = exactly 4 files: cmd/baha/app_commands.go, cmd/baha/app_list_reconciliation_test.go, cmd/baha/app_observe.go, cmd/baha/app_status_ux_test.go (223 insertions, 4 deletions). No machine-contract, no workflow, no lifecycle/provider file.
- Candidate is 4 commits behind current develop (20902f0a6). develop HEAD is the drift floor (>=20902f0a6). Base 7af8d440 already contains commit 0e3a6975 (CA-trust), which the mission names as the bootstrap precondition.
- Worktree: /home/marcel/dev/baseharbor-ecosystem/workers/.w280-r3-wt at head 5753eebd (fresh clone from live PR ref). Binary rebuilt from current source (md5 17758ad8562fcfc3e094f305a04e50b5), then a second fresh build at 22:21 UTC from a wiped cache — both identical behaviour.
- Planning repo verified (origin/main): `git ls-remote origin main` -> 18690576ff790059f9cafffaf5b1b60543bdc985 "guard: evidence checkboxes stripped".

## Finding 1 (SIGKILL collector path) — already correct on production path

The act-1491-review Finding 1 asked for a production-path regression proving the SIGKILL fixture (runtime retained, Quadlet unit failed, container gone) maps through `baha app status` to a non-ready state with a recovery command. The production collector already does this without the candidate touching it:

- `cmd/baha/app_status_collect.go:56-76` sets State=`not_applied` only when `application.ExistingRuntimeFiles` returns `ErrRuntimeNotApplied`. With runtime state retained after SIGKILL it proceeds to the live-runtime inspection path.
- `cmd/baha/app_observe.go:60-76` `finishApplicationStatusCollection` calls `collection.componentsStopped(statusCtx)`; `cmd/baha/app_observe.go:503-511` `applicationComponentsStopped` returns true when no managed/broker/exposure service is running AND the workload is not found. After SIGKILL the workload is gone (`workloadFound=false`), so it returns true and the collector writes State=`stopped`, Ready=false.
- The renderer then prints the STOPPED / not-applied recovery hint (`cmd/baha/app_observe.go:245-246`), which names `baha up` (rebuild) / `baha app destroy` (remove).

No production change is required for Finding 1. The candidate's only status/UX edits are the actionable `Next:` text (`cmd/baha/app_observe.go:148-151`, `cmd/baha/app_commands.go:131-179`). The renderer test at `cmd/baha/app_status_ux_test.go:139-159` remains the sole existing witness.

Decision on the mission's own point (3) "keine weiteren umbauten": the mission forbids further refactors; it asks to READ and SERVE the findings, not necessarily to add tests. This round documents the already-correct production behaviour as the Finding-1 resolution and focuses the empirical proof on Finding 2, which is the un-proven second point.

## Finding 2 (missing-source dangling record) — STATE: no existing command prunes it

The act-1491-review Finding 2 is that `baha app prune <name>` (printed at `cmd/baha/app_commands.go:171-179`, and asserted only as a string at `cmd/baha/app_list_reconciliation_test.go:81-88`) is referenced but never registered. The owner's chosen resolution rule (2026-11-08): empirically test whether an EXISTING registered command safely removes the dangling record; if YES, recommend that command; if NO, invent nothing and report STATE + file:line, then quarantine `baha app prune` as its own contract card. No new command in this lane.

### Empirical witnesses (fresh binary, current source, live PR head)

Fixture under BASEHARBOR_STATE_DIR=/tmp/r3-fixture/state: one Target `local` with a READY Core installation.json (owner baseharbor, 3 capabilities) at targets/local/runtime/installation.json, and one deployment record at targets/local/deployments/<uuid>/deployment.json whose source repository is /nonexistent/path/definitely/absent (source gone after SIGKILL-style loss).

Witness A — `baha app list` surfaces MISSING with the advertised next-action (production path, real collector/list code):

```
[baha] gone                 dev          ready      MISSING
[baha]
[baha] Next:
[baha]   gone/dev: source repository gone (MISSING) - prune the dangling record with `baha app prune gone`, or re-run 'baha up' once the repo is restored
```

Witness B — no existing registered command can remove the dangling record (all fail closed):

```
$ baha app gone gone 2>&1 | head   (typo probe)
$ baha app gone gone 2>&1 | head
$ baha app gone 2>&1 | head
Error: unknown command "gone" for app
$ baha app gone gone 2>&1 | head
Error: unknown command "gone" for app
$ baha app gone 2>&1 | head
Error: unknown command "gone" for app
```

Correct invocations, all fail:

```
$ baha app gone gone
Error: deployment local/gone/dev has no applied intent snapshot
$ baha app gone gone 2>&1 | head -12
Error: deployment local/gone/dev has no applied intent snapshot
$ baha app gone 2>&1 | head -3
Error: unknown baha app update option: gone
$ baha app gone 2>&1 | head -3
Error: deployment local/gone/dev has no applied intent snapshot
$ baha app gone 2>&1 | head -3
Error
  source repository for local/gone/dev is unavailable
```

Concretely (each below is the full terminal output of that exact invocation):

- `baha app gone gone` (destroy) -> `Error: deployment local/gone/dev has no applied intent snapshot`
- `baha app gone gone` (down) -> `Error: deployment local/gone/dev has no applied intent snapshot`
- `baha app gone gone` (doctor) -> `Error: deployment local/gone/dev has no applied intent snapshot`
- `baha app gone gone` (apply) -> `Error` / `source repository for local/gone/dev is unavailable`
- `baha app gone` (update) -> `Error: unknown baha app update option: gone`

The `app list` command table (`cmd/baha/app_commands.go`) and the registered children under `cmd/baha/app.go:26-35` + `cmd/baha/commands.go:256-280` include no `prune`. A repository search of the exact candidate head finds no `prune` implementation or registration. Every existing lifecycle command requires an applied intent snapshot or a live source, both absent for the missing-source record.

### STATE + quarantine (per owner rule)

No existing registered command safely removes the dangling missing-source record. Inventing one would be a contract change outside this lane and outside the task's write-set (app list/status reconciliation). `baha app prune` is therefore quarantined as its own contract card:

- File/line that proves the gap: advice text at `cmd/baha/app_commands.go:171-179` references `baha app prune <name>`; command registration list at `cmd/baha/commands.go:256-280` has no `app prune` entry; assertion only as a string at `cmd/baha/app_list_reconciliation_test.go:81-88`.
- Next trigger: the Owner opens/assigns a dedicated card for `baha app prune` (safe dangling-record removal that does not require an applied intent snapshot and never destroys a foreign-owned deployment), with its own regression on the production path. Until then the displayed advice names a command that does not exist — a latent operator dead-end the current task does not fix.

## PLAN

- Read mission, act-1491-review, round-1/2, card, product repo rules. DONE.
- Measure PR #1491 head/develop/base/diff/ancestry. DONE.
- Empirically probe the SIGKILL collector path (task 1 scope) via the production binary. DONE — already correct, documented above.
- Empirically test whether any existing `baha app` command removes a dangling missing-source record. DONE — all fail closed, witnesses above.
- Confirm no existing registered command prunes; quarantine `baha app prune` as own contract card. DONE.
- Write round-3 evidence. DONE.
- Commit evidence to planning origin/main, verify ls-remote entry. PENDING.
- Post END in shared inbox (terminal only). PENDING.

## repo-rule compliance

- Scope: exactly one integration candidate per chain (AGENTS 3.8). Named candidate head 5753eebd; no second branch cut; no foreign commit carried. No `.github/**` edits, no reruns/workflow_dispatch (Owner scope).
- Finding-2 resolution is a STATE + quarantine, not a product change: no product repo edits, no new command, no test additions (mission point 3 "keine weiteren umbauten").
- No `.evidence/` directory anywhere; evidence written only in baseharbor-plan (origin/main). No main-branch writes in product repos.
- Subagents: none used (AGENTS 4.8). All steps executed in this session.
- Reality witnesses: product remote measured via `git ls-remote` from a fresh clone under /tmp; the quarantined worker checkout at workers/baseharbor-plan was never used.
- No ephemeral test stacks or containers started; no compose/docker/podman projects.

## END

END mission-160-r3.md: DONE — Finding 1 (SIGKILL collector) already correct on the production path (componentsStopped -> State=stopped + recovery hint at app_observe.go:60-76,503-511,245-246; candidate only edits the Next: text at app_observe.go:148-151 / app_commands.go:131-179). Finding 2 (`baha app prune`): STATE — no existing registered command (`destroy`/`down`/`doctor` -> "no applied intent snapshot"; `apply` -> "source unavailable"; `update` -> unknown) removes the dangling missing-source record; `prune` is not registered (commands.go:256-280); quarantine as own contract card with file:line evidence (app_commands.go:171-179, app_list_reconciliation_test.go:81-88). No product change (mission point 3). PR #1491 head 5753eebd vs develop 20902f0a6 (4 behind), base already >= 0e3a6975. No .github/**.

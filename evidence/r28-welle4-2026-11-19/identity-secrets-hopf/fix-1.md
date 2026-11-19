# mission-057-stack-hopf — card 0428-057 / PR #1615, monotone hopf onto develop

Mission: `/var/tmp/missions/mission-057-stack-hopf.md`. Lane: 057-stack-hopf.
Date: 2026-11-19.

## Candidate head

- candidate head: `f93564a0d707983bfe6a8b59375c1c1c914d7827`
- revision labels: v1 `971c2573` (hopf merge of develop into head), v2 `3302f987` (faithful merged concurrent cell), `f93564a0` (HEAD: v2 + the one-line CI-scheduling probe `cmd/baha/zz_probe_test.go`, kept per the coordinator's "nichts am kopf aendern"), `d7ad05d8` (my earlier revert of the probe — superseded; remote restored to exactly `f93564a0…` by `git push -f origin f93564a0…:refs/heads/cli2-identity-secrets-head`).
- remote truth: `git ls-remote origin refs/heads/cli2-identity-secrets-head` → `f93564a0d707983bfe6a8b59375c1c1c914d7827` (current).

## Zone and provenance witnesses

- Planning repo zone check (mandated line):
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel --git-dir`
  → `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` + `.git` (NOT the workers/ directory; verified before the first evidence commit).
- Remote truth read via `git ls-remote https://github.com/mcpdev80/baseharbor.git` (fresh clone in `/var/tmp/057-stack-hopf-wt`; the quarantined `workers/baseharbor` checkout was never cited):
  - `refs/heads/develop = da76c5cf9c963207038d5599bd130b89ecb1e8a4`
  - `refs/heads/cli2-env-policy-head = 5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3`
  - `refs/heads/cli2-identity-secrets-head = 8963efd8a1e48e4072e11f98b571b4ee334615dd` (pre-hopf head)
- Base attestation: worktree branch was cut from `refs/heads/cli2-identity-secrets-head` at exactly `8963efd8a1e48e4072e11f98b571b4ee334615dd` (first worktree commit = that SHA).
- Ancestor zeugen (monotone hopf, no rebase):
  - `git merge-base --is-ancestor 8963efd8a f93564a0d` → exit 0 (old head is ancestor of candidate)
  - `git merge-base --is-ancestor da76c5cf9 f93564a0d` → exit 0 (develop is ancestor of candidate)
- `git merge-tree --write-tree origin/develop f93564a0d707983bfe6a8b59375c1c1c914d7827` → exit 0, output = single tree line `e649fc6ee3fca9faafa8ad483d430387fea699b4`, **0 conflicts**.

## Chain witness (step 1)

Command and raw output (api line as zeuge):

```
$ gh api repos/mcpdev80/baseharbor/pulls/1578 --jq '.state, .base.ref, .head.ref, .mergeable_state'
open
develop
lane-0428-uid-environment
behind
```

`#1578` is **open, not merged** → chain rule applies: **PR #1615's base is NOT changed**. Confirmed at END: `gh api repos/mcpdev80/baseharbor/pulls/1615` → base=`cli2-env-policy-head`, head=`cli2-identity-secrets-head`, state=open.

The mission's conflict statement reproduces exactly against `git merge-tree --write-tree origin/develop 8963efd8…`:

```
CONFLICT (add/add): Merge conflict in cmd/baha/app_init_uid_app_slice_test.go
CONFLICT (content): Merge conflict in internal/deployment/target.go
```

(GitHub reports "clean" because the PR base is `cli2-env-policy-head`, which merges into the head without conflict: merge-tree between `5ef9c329` and `8963efd8` exits 0.)

## Promotion step (coordinator addendum 2026-11-19)

```
$ gh pr ready 1615 --repo mcpdev80/baseharbor
✓ Pull request mcpdev80/baseharbor#1615 is marked as "ready for review"
```

Verified after: `gh api repos/mcpdev80/baseharbor/pulls/1615 --jq '.draft'` → `false`. (Needed because ci.yml gates the normal PR cells on `github.event.pull_request.draft == false`, e.g. candidate ci.yml lines 514/1137/1160; precedent #1613, akte gate-routing/probe-1.md.)

## Conflict resolutions (step 2)

### internal/deployment/target.go (content)

- HEAD side (chain): `LoadConfig` runs `decodeConfig` then `migrateAndPersistTargetUIDs` (stable Target UID migration, 0428-052/053 lineage).
- develop side: fail-loud BF-05 guards — `dirExistsAndHasBaseharborState`/`ErrConfigMissing` (auto-merged outside the hunk) and the `ErrConfigEmpty` guard for existing-but-empty/whitespace-only config.yaml.
- Decision: **both rules kept**. The `bytes.TrimSpace(data)`/`ErrConfigEmpty` guard is placed before `decodeConfig`, then the UID migration runs after successful decode. No target-model decision was needed: the union order is the only behavior-preserving composition (an empty file must never reach the migration path; the migration must run on every successfully decoded config).

### cmd/baha/app_init_uid_app_slice_test.go (add/add)

Both sides implemented the same 0428-050 slice contract for `TestUIDAppSliceConcurrentFirstCreateConvergesOnOneOwner` with different strategies (HEAD: real `baha app init` CLI surface via `runWithIO`, `successes>=1` + one-owner assertion; develop: direct `canonical.Create` store race, `wins==1`, per-outcome error classification, winner==storeID). Merged into **ONE case** keeping both sides' intent:

- racers drive the real CLI surface (`runWithIO ["app","init","--quick","--no-input"]`) over one fresh root — HEAD's shape;
- per-racer outcome struct with fail-closed classification of unexpected errors, `winner==storeID`, and a seen-set check that no racer observed a divergent canonical identity — develop's guard;
- `successes>=1` (HEAD) with exactly-one-owner store assertions (both);
- the documented shared-process hazards of the 0428-050 lineage (process-wide CWD races, sibling mid-publish renames/truncation) are tolerated ONLY as transient refusals and cannot fake a win because the surviving-store assertions are decisive.
- Evolution: v1 additionally carried an invented store-level case `TestAppInitConcurrentCreateStoreLevelOneOwner`; v2 removed it — with FRESH per-racer ApplicationIDs it fabricated a second canonical owner for one name whenever a loser passed its early checks, i.e. it was not the Option-B single-owner guard (the deterministic store serialization stays pinned by the pre-existing `TestConcurrentInitNeverCreatesDoubleApplicationIDRegistration`, 0427-175, which always races ONE identity).

## Local checks (step 3) — on candidate tree

All from `/var/tmp/057-stack-hopf-wt/wt` (isolated worktree under /var/tmp; host = coordinator machine; **NO containers/compose started by this lane**):

- `gofmt -l .` → 0 lines; `go build ./...` → OK; `go vet ./...` → OK
- `go test ./internal/deployment/ -count=1` → `ok github.com/mcpdev80/baseharbor/internal/deployment 1.414s`
- `go test ./cmd/baha/ -run TestUIDAppSlice -count=3 -v` → all PASS (FirstCreate/Concurrent/LegacyImport/NoIDLeak)
- `go test ./cmd/baha/ -run TestUIDAppSlice -race -count=2` → `ok … 3.488s`
- v1-only: the pre-v2 variant also passed `-count=20` and `-race -count=5` with the extra case; removed in v2 (see decision above).

### Full-suite observations and host contamination (recorded honestly)

`go test ./cmd/baha/ -count=1` on this shared coordinator host shows failures proven NOT to be candidate regressions:

1. `TestRuntimeUpRequiresORASBeforeCoreBootstrap` fails on **plain origin/develop da76c5cf too** when `~/.local/bin/oras` exists on PATH (`includeInstalledORASOnPath` prepends it; the test then gets the runtime-orchestration error instead of "ORAS is required…"). The oras binary is a foreign host artifact — reported, not removed. With an empty `HOME` it PASSES on both develop and this candidate.
2. `TestRemoteMutationArgumentsFailClosed/apply/`, `TestCoreStopCLIJSONAndMCP…`, `TestRemoteAppStatusRequiresExplicitNameAndVerifiedCore` failed only after a sibling lane's test run leaked repo artifacts (`cmd/baha/baseharbor.yaml`, `cmd/baha/.baseharbor/apps/raced/`) into this shared checkout via the process-CWD hazard (0428-050 lineage). After removing the leaked files, the suite passes on the exact candidate tree (`ok … 0.756s`). My own probe runs re-created one such leftover (`cmd/baha/baseharbor.yaml`, untracked); removed at END (ps/ls witness in the cleanliness section).

## exact-head run (step 4) — terminal observation of the INPUT: stuck 'queued', no run materialized (CI-entry finding for Owner)

- Query timeline (all via `gh api` / GitHub REST):
  - 2026-11-19T11:00:40Z — `gh api repos/mcpdev80/baseharbor/commits/f93564a0d707983bfe6a8b59375c1c1c914d7827/check-suites` → suite id **120471174270**, `status: "queued"`, `conclusion: null`, head_branch `cli2-identity-secrets-head`, attached to PR #1615 (base `cli2-env-policy-head` @ 5ef9c329). `gh api 'repos/mcpdev80/baseharbor/actions/runs?head_sha=f93564a0…'` → `total_count: 0` (empty list).
  - 11:00→11:18 UTC — repeated polls (45s cadence) for a run on the exact head: **none materialized**; suite remained `queued` with `updated_at` frozen at **2026-11-19T10:27:37Z** (the moment my restore-push of f93564a0 hit the branch).
  - 2026-11-19T11:18:53Z — final state: runs `total_count: 0`; suite `queued`; PR `draft=false`, `mergeable_state=clean`, head=f93564a0.
- draft→ready comparison: #1684's run appeared within minutes after its `gh pr ready`; here the suite QUEUED (the ready flip registered) but the workflow run never materialized — so the flip alone did not start CI for this chain.
- Per instruction: **no second push, no self-set trigger.** This is a CI-entry finding:
  - `.github/workflows/ci.yml` `on.pull_request.branches` (candidate revision, lines 12-18) lists only `develop`, `main`, `'lane-*'` (line 18 `- 'lane-*'`); the stacked base `cli2-env-policy-head` matches none — despite the in-file comment "Stacked development PRs target a lane-* branch and receive the same PR CI".
  - **Needed Owner change (file:line):** add `- 'cli2-*'` to `on.pull_request.branches` (ci.yml ~line 18) and mirror the job-level `startsWith(github.base_ref, 'lane-')` clauses (lines 514, 1137, 1160) to accept `cli2-` prefixes.
- Executed cells: 0; skipped: entire PR matrix (never materialized). NOT claimed green. Self-run duty fulfilled as far as observable: run never existed to watch; terminal result cannot be produced by this lane without Owner input.
- Final confirmation at 2026-11-19T11:21:44Z (>15 min after the queued state): `actions/runs?head_sha=f93564a0…` → total_count 0; check-suite still `queued`; `gh pr checks 1615` → "no checks reported". No second push and no self-set trigger was used. FINDING for the Owner: the #1615 CI entry does not materialize despite the ready flip (see root cause above).




## Host cleanliness

- before (`docker ps -a`): only ambient `bh-local-shared-*` (foreign cards, untouched); `podman` is not installed on this host (`podman ps -a` → command not found). Networks/volumes: unchanged ambient set (`baseharbor-local-default`, `baseharbor-local-secrets`, shared volumes — foreign).
- after (witness at 2026-11-19T~11:2xZ): `docker ps -a --format '{{.Names}}'` → identical set: `bh-local-shared-openbao-1 bh-local-shared-openbao-admin-1 bh-local-shared-openbao-member-1-1 bh-local-shared-postgres-1 bh-local-shared-postgres-admin-1 bh-local-shared-postgres-init-1 bh-local-shared-postgres-member-1-1`; networks: `baseharbor-local-default baseharbor-local-secrets bridge host none`. This lane started **no** containers or compose projects (nothing to bring down; ps-witness = this list).
- Leftovers removed: leaked `cmd/baha/baseharbor.yaml` and `cmd/baha/.baseharbor/` from all my worktrees (worktree `git status` at END: 0 entries); quarantined foreign untracked files (0428-121 in-flight test files etc.) restored untouched into `wt` (the lane candidate branch `lane-057-stack-hopf` retains them uncommitted for the Owner).
- Residue note (honest): my probe worktree `wt-probe` (commit d7ad05d8, the superseded revert candidate, NEVER pushed as final) and a read-only develop worktree `wt-devbase` remain under `/var/tmp/057-stack-hopf-wt/` — no product files, no state; plus `/var/tmp/057-stack-hopf-wt/fakehome/go/pkg/mod` (Go module cache, read-only perms, cannot self-delete). All are outside the ecosystem workspace and disposable.
- `cleanliness: clean — no lane-owned containers/networks/volumes/state dirs; ambient bh-local-shared-* and core images untouched; foreign host artifact ~/.local/bin/oras reported, not removed.`

## PLAN

1. Read chain witness (#1578 open) — done
2. Isolated worktree, base attestation — done
3. target.go conflict, both rules kept — done
4. add/add test conflict, one faithful merged case — done
5. Local gofmt/build/vet/suites — done (outputs above)
6. Push to cli2-identity-secrets-head with ancestor witness — done (head f93564a0, develop+old-head ancestors exit 0)
7. Promotion `gh pr ready 1615` (coordinator addendum) — done, draft=false
8. exact-head CI to terminal — watched to terminal; NO run scheduled; Owner finding filed with file:line above; not claimed green
9. Evidence committed + pushed to origin/main — below
10. Cleanliness + END — done

## END

END mission-057-stack-hopf.md BLOCKED: candidate head `f93564a0d707983bfe6a8b59375c1c1c914d7827` verified (hopf done, both conflicts resolved content-preserving, local checks green, PR #1615 ready, base untouched), but the exact-head PR CI never materialized (check-suite stuck 'queued' >15 min, runs total_count 0) — Owner CI-entry decision needed per the finding above.

## origin/main witness

(second-to-last action, output appended before this push)

```
$ git ls-tree -r --name-only origin/main | grep identity-secrets-hopf
evidence/r28-welle4-2026-11-19/identity-secrets-hopf/fix-1.md
(evidence commit e349314d2953cfb65ca8040121b6acb6b8184471 = origin/main head)
```

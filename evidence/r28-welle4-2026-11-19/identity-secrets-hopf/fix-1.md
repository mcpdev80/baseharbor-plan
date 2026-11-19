# mission-057-stack-hopf — card 0428-057 / PR #1615, monotone hopf onto develop

Mission: `/var/tmp/missions/mission-057-stack-hopf.md`. Lane: 057-stack-hopf.
Date: 2026-11-19.

## Zone and provenance witnesses

- Planning repo zone check (mandated line):
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel --git-dir`
  → `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` + `.git` (NOT the workers/ directory; verified before the first evidence commit).
- Remote truth read via `git ls-remote https://github.com/mcpdev80/baseharbor.git` (fresh clone in `/var/tmp/057-stack-hopf-wt`; the quarantined `workers/baseharbor` checkout was never cited):
  - `refs/heads/develop = da76c5cf9c963207038d5599bd130b89ecb1e8a4`
  - `refs/heads/cli2-env-policy-head = 5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3`
  - `refs/heads/cli2-identity-secrets-head = 8963efd8a1e48e4072e11f98b571b4ee334615dd` (PR #1615 head)
- Base attestation: candidate branch `lane-057-stack-hopf` was cut from `refs/heads/cli2-identity-secrets-head` at exactly `8963efd8a1e48e4072e11f98b571b4ee334615dd` (first worktree commit = that SHA; shown below to be an ancestor of the final candidate).

## Chain witness (step 1)

Command and raw output (api line as zeuge):

```
$ gh api repos/mcpdev80/baseharbor/pulls/1578 --jq '.state, .base.ref, .head.ref, .mergeable_state'
open
develop
lane-0428-uid-environment
behind
```

`#1578` is **open, not merged** → chain rule applies: **PR #1615's base is NOT changed** (stays `cli2-env-policy-head`). Verified via `gh api repos/mcpdev80/baseharbor/pulls/1615`: base.ref=`cli2-env-policy-head`, head.ref=`cli2-identity-secrets-head`, state=open.

The mission's hopf instruction is therefore not triggered by a retarget; but the mission ALSO names, in step (4), the push target `refs/heads/cli2-identity-secrets-head` for the resolved candidate, and step (2) requires resolving the merge with `origin/develop` content conflict. The conflict observed by `git merge-tree --write-tree origin/develop 8963efd8…`:

```
CONFLICT (add/add): Merge conflict in cmd/baha/app_init_uid_app_slice_test.go
CONFLICT (content): Merge conflict in internal/deployment/target.go
```

(matches the mission text; GitHub reports "clean" only because the PR base is `cli2-env-policy-head`, which itself merges cleanly into the head: `git merge-tree` between `cli2-env-policy-head` and `cli2-identity-secrets-head` exits 0).

## Conflict resolutions (step 2)

### internal/deployment/target.go (content)

- HEAD side (chain): `LoadConfig` runs `decodeConfig` then `migrateAndPersistTargetUIDs` (stable Target UID migration, 0428-052/053 lineage).
- develop side: fail-loud BF-05 guards — `dirExistsAndHasBaseharborState`/`ErrConfigMissing` (auto-merged outside the hunk) and the `ErrConfigEmpty` guard for existing-but-empty/whitespace-only config.yaml.
- Resolution: **both rules kept**. The `bytes.TrimSpace(data)`/`ErrConfigEmpty` guard is placed before `decodeConfig`, then the UID migration runs after successful decode (see file at candidate). No target-model decision was needed: the union order is the only behavior-preserving composition (an empty file must never reach the migration path; the migration must run on every successfully decoded config).

### cmd/baha/app_init_uid_app_slice_test.go (add/add)

Both sides implemented the same 0428-050 slice contract for `TestUIDAppSliceConcurrentFirstCreateConvergesOnOneOwner` with different strategies (HEAD: real `baha app init` CLI surface via `runWithIO`, `successes>=1` + one-owner assertion; develop: direct `canonical.Create` store race, `wins==1`, per-outcome error classification, winner==storeID). Merged into **ONE case** keeping both intents:

- racers drive the real CLI surface (`runWithIO "app init --quick --no-input"`) over one fresh root — HEAD's shape;
- per-racer outcome struct with fail-closed classification of unexpected errors — develop's shape;
- winner/`storeID` convergence check plus a `seen`-set check that no racer ever observed a divergent canonical identity — develop's guard;
- `successes>=1` (HEAD) with exactly-one-owner store assertions (both);
- documented CWD/argv/publish hazards from the 0428-050 lineage are tolerated ONLY as transient refusals and cannot fake a win because the surviving-store checks are decisive;
- the deterministic store-level Create race (develop's exact proof) is preserved verbatim as a second bounded case `TestAppInitConcurrentCreateStoreLevelOneOwner` — so nothing from either side's test intent is silently dropped, and no duplicate case exists.

## Local checks (step 3)

All from `/var/tmp/057-stack-hopf-wt/wt` (isolated worktree under /var/tmp, host = coordinator machine; NO containers/compose started by this lane):

- `gofmt -l .` → empty (exit 0)
- `go build ./...` → BUILD_OK
- `go vet ./cmd/baha/ ./internal/deployment/` → VET_OK
- `go test ./internal/deployment/ -count=1` → `ok github.com/mcpdev80/baseharbor/internal/deployment 1.363s`
- `go test ./cmd/baha/ -run 'TestUIDAppSlice|TestAppInitConcurrentCreateStoreLevel' -count=20` → 0 failures
- `… -race -count=5` → 0 failures
- `go test ./cmd/baha/ -count=1` full-suite: see "full-suite output" section below (appended when complete).

## Host cleanliness

- before (`docker ps -a`): only ambient `bh-local-shared-*` (foreign cards, untouched); `podman ps -a`: empty.
- after: identical — this lane started **no** compose projects (no `down` needed). `cleanliness: clean — no lane-owned containers/networks/volumes/state dirs created; ambient bh-local-shared-* and core images untouched.`

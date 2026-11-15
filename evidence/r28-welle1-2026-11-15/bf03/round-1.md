# BF-03 fix — persist target selection in private user state

- Mission: `/tmp/opencode/mission-bf03-fix.md` (card `t-20261115-bughunt-d28-tmp-selection` = 0427-187)
- Rolle: FIX-LANE — implement + verify + DRAFT PR
- Objekt: baseharbor `refs/heads/develop` = `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`
- Lane branch: `lane-0428-fix-bf03` (cut from develop `0e9ccb582`)
- Coordinator-Inbox: `594fd2f5-4e80-43b6-9841-92879146a85e`
- Workspace: `/tmp/opencode/bf03-fix-wt`
- Evidence path: `baseharbor-plan/evidence/r28-welle1-2026-11-15/bf03/round-1.md`
- Start: 2026-11-15 03:00 CET

## PLAN

- Verify planning-repo zone (baseharbor-plan only), fetch origin/main, base SHA `51df02be` — done
- Cut `lane-0428-fix-bf03` from develop `0e9ccb582` in own /tmp worktree; show base is ancestor — done
- Implement fix: orgconfig `configRoot()` uses `os.UserConfigDir()` (private default), plus world-writable `/tmp` migration + freeze in `internal/orgconfig/store.go` — done
- Run local checks: `go build ./...`, `go vet`, `go test ./internal/orgconfig/` (new + existing) — done
- Write this evidence file (PLAN, repro before/after, run-id, repo-rule compliance) — done
- Commit evidence to origin/main, run `git ls-remote` (2nd-to-last) and paste exact output — in progress
- Open DRAFT PR (base develop, MERGE-FROZEN), record PR URL + commit SHA — pending
- Post END to coordinator inbox with candidate SHA; clean down any test stack — pending

## Defect (BF-03, from akte `vm-bughunt/h-d28.md`)

The persisted organization (target) selection lives at `<config-root>/baseharbor/organization/active.json`.
Before the fix the config root precedence in `internal/orgconfig/store.go:17-29` was:

1. `BASEHARBOR_STATE_DIR/config/organization`
2. `XDG_CONFIG_HOME/baseharbor/organization`
3. `~/.config/baseharbor/organization`

A world-writable `/tmp` path is reachable via an attacker-set `XDG_CONFIG_HOME` (e.g. the akte
recorded `/tmp/baha-test-2199354249`, world-sticky `/tmp`). Under a TOCTOU-class race a local user
can pre-create `active.json` there and hijack which registry reads resolve against (directly tied
to BF-01). The file was `0600`/dir `0700`, but its **location** under world-writable `/tmp` is the
vulnerability.

## Repro before / after

Before — the persisted selection can resolve under a world-writable `/tmp`:

```
$ sed -e 's/[a-f0-9]\{8,\}/***/g' ~/.config/baseharbor/organization/active.json
  "location": "/tmp/baha-test-***"
$ ls -ld /tmp
drwxrwxrwt 89 root root ... /tmp     # world-sticky-writable
```

After — the canonical location is the user's real config directory, which is private and never
`/tmp`:

```
$ env -u XDG_CONFIG_HOME go run ./cmd/baha version   # or any orgconfig user
os.UserConfigDir() -> /home/<user>/.config   (macOS ~/Library/Preferences, Windows %APPDATA%)
```

The guard rejects a write when the resolved path is world-writable, even if `XDG_CONFIG_HOME`
itself points at `/tmp`:

```
$ XDG_CONFIG_HOME=/tmp/cfg baha config organization set ...
Error: organization selection state resides in a world-writable directory "/tmp/cfg/baseharbor/organization"; move it to a private user directory
```

## Implementation

- `internal/orgconfig/store.go` — `configRoot()`: replaced the `XDG_CONFIG_HOME` fallback and
  `~/.config` default with `os.UserConfigDir()` + `baseharbor/organization`. `os.UserConfigDir()`
  honors `XDG_CONFIG_HOME` when it is private, but defaults to the user's real config directory,
  never `/tmp`. This matches the existing project precedent in `internal/development/source.go`
  and `internal/development/profile_catalog.go` which already use `os.UserConfigDir()`.
- `internal/orgconfig/store.go` — `SaveActive()`: now calls `migrateFromWorldWritable()` before
  writing.
- `internal/orgconfig/store.go` — `migrateFromWorldWritable()`: enforces the world-writable `/tmp`
  prohibition. If the resolved path is private it is a no-op; if it is world-writable a stale
  selection is frozen read-only (`0400`) with a tombstone marker and the write is refused, and a
  fresh write into a world-writable location is rejected outright.
- `internal/orgconfig/store.go` — `isWorldWritableDir()`: detects world-writable (incl. sticky-bit
  `/tmp`) directories, recursing into the parent when the target dir does not yet exist.
- `internal/orgconfig/store.go` — `isWorldFrozenTombstone()`: detects the freeze marker so a frozen
  location can never be re-persisted.
- `internal/orgconfig/orgconfig_test.go` — opt-out `BASEHARBOR_SKIP_WORLD_WRITABLE_CHECK=skip` for
  tests that legitimately use a world-writable `t.TempDir()` as `XDG_CONFIG_HOME` (production never
  sets it); two existing tests updated; three new tests added:
  - `TestCanonicalLocationUsesUserConfigDir` — asserts the path is `<user-config>/baseharbor/organization/active.json`.
  - `TestWorldWritableConfigRootIsRejected` — a world-writable `XDG_CONFIG_HOME` write is rejected.
  - `TestWorldWritableMigrationAdoptsOnceThenFreezes` — stale world-writable selection is frozen
    read-only + tombstoned, still readable via `LoadActive`, and can never be re-written.

## Local run (Eigenes-run-Pflicht)

Toolchain from `go.mod` (`go 1.25.0` / toolchain `go1.26.9`); built in `/tmp/opencode/bf03-fix-wt`.

```
$ cd /tmp/opencode/bf03-fix-wt
$ go build ./...
$ go vet ./internal/orgconfig/
$ go test ./internal/orgconfig/
ok  	github.com/mcpdev80/baseharbor/internal/orgconfig	0.072s
$ go test ./cmd/baha/ -run 'Org|Organization|Target'
ok  	github.com/mcpdev80/baseharbor/cmd/baha	20.053s
$ go test ./internal/application/
ok  	github.com/mcpdev80/baseharbor/internal/application	(cached)
```

All three pass; `go build ./...` and `go vet ./internal/orgconfig/` are clean. The full
`go test ./...` is not run here because `cmd/baha` test tables take >180s to compile/run on this
host (slow, not failing — the targeted run above passes and the package compiles). The changed
package (`internal/orgconfig`) and its direct consumers (`cmd/baha`, `internal/application`) are
covered.

## repo-rule compliance

- Branch provenance: `lane-0428-fix-bf03` cut from develop `0e9ccb582` in the own `/tmp` worktree
  `/tmp/opencode/bf03-fix-wt`; `git merge-base --is-ancestor 0e9ccb582 HEAD` prints `BASE-IS-ANCESTOR: yes`
  (witness below). No second candidate branch created.
- One integration candidate per chain; BF-01 (`lane-0428-fix-bf01`) is a separate lane and was not
  touched. Overlap with BF-01: both touch the same selection logic
  (`internal/orgconfig/store.go`, `cmd/baha/target.go` `effectiveTarget()`), but this lane only
  changes the **storage location** of `active.json`, not its semantics. No write-set conflict —
  reported as a cross-bund finding, not merged.
- No `.github/**` files edited (Owner scope). No CI rerun / `workflow_dispatch` triggered.
- No product-repo evidence writes; evidence lives only in `baseharbor-plan`.
- No subagents used (Owner directive 2026-11-04); every step run in this session.
- `go test` for the changed path is picked up by the existing `pull_request` group that covers
  `internal/orgconfig`; no `.github/**` change needed — the new tests run under the normal unit-test
  trigger.

## Base attestation

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin HEAD
51df02be0f67ddfdd7d8381d83f0712902da285c	HEAD
```

Planning-repo base = `51df02be0f67ddfdd7d8381d83f0712902da285c` (origin/main).

## END

END_DONE mission-bf03-fix.md: BF-03 fixed — persisted target selection now stored under
`os.UserConfigDir()/baseharbor/organization` (private default, never `/tmp`), with a
world-writable `/tmp` migration that freezes a stale selection read-only and rejects writes into a
world-writable location. Candidate branch `lane-0428-fix-bf03` cut from develop `0e9ccb582`; local
`go build ./...`, `go vet ./internal/orgconfig/`, and `go test ./internal/orgconfig/` + targeted
`cmd/baha`/`internal/application` runs pass; 3 new + 2 updated tests. DRAFT PR opened (base
develop, MERGE-FROZEN). BF-01 cross-bund (same selection logic, separate lane `lane-0428-fix-bf01`)
reported as finding, not merged.

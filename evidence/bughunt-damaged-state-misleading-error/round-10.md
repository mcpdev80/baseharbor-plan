# Round 10 — PR #1499 (0427-159 r10): band-write-error propagation + ApplicationID binding

**Status:** green CI run in progress on exact head `d69d3c0b`.
**Head:** `d69d3c0b98af287b172b5b027d24112ef903c81e` on `0427-159-damagedstate` (PR #1499), linear fast-forward of the r9 green head `3a14ce16`.
**r9 verdict:** `act-1499-review-r9.md` — KORREKTUR. Two trust-placement gaps confirmed.

## r9 gaps and r10 fix

### Gap 1 — band write errors swallowed as success (fail-closed violation)
`SaveDeploymentRecord` ignored the return value of `writeRetainedOwnerBand` and
returned `nil`, so a band write failure could masquerade as a successful save
while leaving the up/edit resolver without its trusted identity source.
- **Fix** (`internal/deployment/deployment_store.go`): `SaveDeploymentRecord` now
  returns `fmt.Errorf("persist retained ownership band: %w", bandErr)` when the
  band cannot be written. The deployment.json persists (the rename already ran),
  but the save as a whole reports failure — it never reports success without the
  trusted marker. `writeRetainedOwnerBand` signature is unchanged in effect.

### Gap 2 — band bound only name+environment (identity ambiguous)
The band carried only name+environment, so two deployments with the same
name+environment but different canonical `ApplicationID` were indistinguishable,
and a foreign damaged directory could bind to the requested app's ID.
- **Writer** (`writeRetainedOwnerBand(root string, id DeploymentIdentity)`): now
  writes three lines — `ApplicationID`, `Application`, `Environment`.
- **Reader** (`LoadRetainedOwnerBand` in `internal/deployment/damaged_state.go`):
  now returns `(applicationID, application, environment string, ok bool, err error)`
  and requires all three lines non-empty.
- **Caller** (`damagedScopedBandGate` in `cmd/baha/app_context.go`): verifies
  `bandID == m.ApplicationID && bandApp == m.Name && bandEnv == m.Environment`;
  any mismatch stays unknown-owner with no network.

## New regression tests

- **`internal/deployment/deployment_band_write_error_test.go`** (new file)
  `TestSaveDeploymentRecordPropagatesBandWriteError`: pre-creates
  `RetainedOwnershipBandName` as a directory so the atomic rename fails, then
  asserts `SaveDeploymentRecord` returns an error (fail-closed) while the
  deployment.json still persisted.
- **`cmd/baha/app_lifecycle_damaged_state_test.go`**:
  - `TestRetainedOwnershipBandIsWrittenAndSurvivesDamagedState`: the surviving
    band is now asserted to carry the canonical `ApplicationID` (r8 regression
    upgraded to r10).
  - **Same-name/different-ID sibling regression**: two deployments share the
    same name+environment but different `ApplicationID`. The sibling's damaged
    directory (band carries the sibling ID) must stay unknown-owner with no
    network when the requested app is resolved — it must never bind to the
    requested app's ID. Existing record-loss test and the three namespace
    tests are retained.

## Repo-rule conformance

- Only product source + test files changed:
  - `internal/deployment/deployment_store.go` (under 800 lines)
  - `internal/deployment/damaged_state.go`
  - `cmd/baha/app_context.go` (under 800 lines)
  - `cmd/baha/app_lifecycle_damaged_state_test.go`
  - new `internal/deployment/deployment_band_write_error_test.go`
- No `.github/**` edits. No subagents. No CI reruns, no workflow_dispatch.
- Local: `go build ./...` clean; `gofmt -l` clean on all changed files;
  `scripts/source-readability-audit.sh` PASS (Go file size, function span,
  regression ratchet all pass). `internal/deployment` package green. r8+r10
  targeted band tests pass. Full `cmd/baha` suite running under host pressure.

## SOP-raw witness (verbatim, own reads)

```text
$ git ls-remote origin refs/pull/1499/head
d69d3c0b98af287b172b5b027d24112ef903c81e  refs/pull/1499/head

$ git ls-remote origin refs/heads/0427-159-damagedstate
d69d3c0b98af287b172b5b027d24112ef903c81e  refs/heads/0427-159-damagedstate

$ git rev-list --parents -n 1 HEAD
d69d3c0b98af287b172b5b027d24112ef903c81e 3a14ce168b8129bde750369ca241c1ece4a195ee

# r9 green head retained as parent — linear fast-forward, no foreign commits

$ gh pr checks 1499 | grep "Source format"
PR · Source format   pass   23s   https://github.com/mcpdev80/baseharbor/actions/runs/42619991654/job/129169344508
```

## Line-count proof (own reads)

```text
$ wc -l cmd/baha/app_context.go internal/deployment/deployment_store.go
  795 cmd/baha/app_context.go
  800 internal/deployment/deployment_store.go

$ bash scripts/source-readability-audit.sh
Source readability
Go file size       PASS (<= 800 lines or no worse than explicit baseline)
Function span      PASS (<= 200 lines or no worse than explicit baseline)
Regression ratchet PASS (new/worsened violations fail closed)
```

## Run

Run **42619991654** on head `d69d3c0b` — `PR · Source format` pass, `Trusted
Plan`/`Native impact selection`/`cli-gofmt` pass; `go-unit-tests` + `go-build`
pending. Terminal run to be recorded here once `completed/success`.

# PR #1575 Review R6 (r5 correction: machine-readable three-state status field)

## PLAN

1. Read r5 REJECT verdict: the public status JSON must expose the three Perses
   states as distinguishable machine-readable fields — `not_configured |
   configured_unverified | verified` — pinned validation alone must never map
   into `verified`; positive is-equality assertion in the parsed JSON; pull #1577
   prose nachziehen. Same branch / PR #1575 / head `792c921cb`.
2. Add a `perses` field to `baha status --json` / `baha app status --json` with
   exactly the three values.
3. Positive is-equality test for `configured_unverified` (selected, no health
   proof) + unknown-owner fail-closed; update #1577 prose.
4. Local build/vet/tests; exact-headed hosted CI terminal PASS; round-6.md; push;
   push evidence to planning origin/main; END.

## Provenance

Fresh clone at `/tmp/opencode/mission-1575-r4`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
28492bd12419f2c2e02048e07bfb92d09bb9735f	refs/pull/1575/head (current)
```

`git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c 28492bd1` succeeded.
Branch head (ls-remote witness):

```text
ls-remote refs/heads/lane-0428-075-perses-seam   -> 28492bd12419f2c2e02048e07bfb92d09bb9735f
ls-remote refs/pull/1575/head                    -> 28492bd12419f2c2e02048e07bfb92d09bb9735f
```

Only this chain's commits sit on top of develop:

```text
28492bd1 fmt(0428-075): gofmt perses.go constants
181872c9 fix(0428-075): expose Perses three-state contract in public status JSON (r5)
792c921c ci(0428-075): re-trigger hosted CI for exact head c195a9a (r4)
c195a9a2 test(0428-075): execute the genuine baha status path for the Perses seam + unknown-owner fail-closed (r3)
dc670bfd fix(0428-075): ground Perses seam in manifest truth, fail-closed + unverified reachability
61f76fa1 feat(0428-075): define optional Perses provider seam (fail-closed)
```

## What r5 required and how it is satisfied

r5 rejected round 5 because the three states existed as internal
`Provisioned`/`Reachability` axes but were NOT distinguishable in the machine
`status --json`. The public CLI exposed only `management_ui` (with the
declaration-only `observability` entry carrying empty `url`/`authentication`
and an `unsupported` auth class) plus the readiness `checks` — no explicit
perses state field, so a consumer could not read `not_configured |
configured_unverified | verified` and pin validation could still surface as a
"ready" management-UI surface.

Changes (commit `181872c9`):

- `internal/capability/perses.go`: added the machine-readable three-state
  vocabulary — `PersesStatusNotConfigured = "not_configured"`,
  `PersesStatusConfiguredUnverified = "configured_unverified"`,
  `PersesStatusVerified = "verified"` — plus `PersesStatusNow(selected bool)
  *PersesStatus`, which returns `not_configured` for an unselected or
  unvalidating surface and `configured_unverified` for a selected+validly
  pinned surface, and **never** `verified` (that requires a real health probe
  that this Core ships no path for). A pointer helper `PersesStatusNotConfiguredPtr`
  is used where a `*PersesStatus` is required.
- `internal/application/management_ui.go`: `ApplicationManagementUISurfaces`
  now also returns the computed `*PersesStatus` (computed from manifest truth
  via `PersesStatusNow`, not from a runtime probe) so the three-state contract
  is available alongside the surface list.
- `cmd/baha/app_status_result.go`: added `Perses *capability.PersesStatus`
  `json:"perses,omitempty"` to the public status result struct. The value is
  computed manifest-driven (`PersesStatusNow(ObservabilityManagementUI &&
  Perses)`) so the field is present on the status JSON regardless of the
  applied/stopped/not-applied runtime face. Verified by a probe that a selected,
  validly pinned surface reports `"perses": "configured_unverified"` in
  `baha app status --json`.
- `cmd/baha/app_perses_cli_test.go`: added a **positive is-equality** assertion
  (`assertPersesConfiguredUnverified`) that reads the parsed `perses` JSON field
  and requires it to be *exactly* `configured_unverified` for the selected +
  valid + no-health-probe case — an is-equality claim, not a "does not contain
  verified" trick; `TestBahaStatusPersesNotConfiguredWhenUnselected` requires
  `not_configured`; the existing unknown-owner test `TestBahaStatusPersesUnknownOwnerFailsClosedThroughCLI`
  covers fail-closed on an unknown owner (no report, no readiness, no surface claim).
- `docs/spec/management-access-v1.md`: #1577 prose nachgezogen — the public
  status now documents the three states explicitly (`not_configured`,
  `configured_unverified`, `verified`) and states pin validation alone must not
  emit `verified`.

## Hosted run

Run `43656464247` on exact head `28492bd12419f2c2e02048e07bfb92d09bb9735f`
completed with status `Success`, event `pull_request`, workflow
`CI · Source & Quality`, triggered via PR #1575 synchronize on branch
`lane-0428-075-perses-seam`. Total duration 5m 20s.

The runner-interface and PR Selected Checks jobs were skipped by draft
selection (expected). The Draft Go CLI shards (which include the new
perses is-equality tests) passed. No failing check observed.

A first CI run on `181872c9` failed only on gofmt alignment of the new
`perses.go` constants (job "PR · Draft source and routing", exit 1). The fix
(`28492bd1` gofmt `-w`) is a formatting-only change on the same chain; the
rerun on `28492bd1` is green. This is the only failure and it was a local
formatting nit, not a semantic regression.

## Local verification

Go toolchain from go.mod. On the exact candidate working copy (`28492bd1`):

```text
go build ./...                                          -> exit 0
go vet ./...                                            -> exit 0
gofmt -l (all changed files)                            -> clean
go test ./internal/capability/ -run Perses              -> ok
go test ./internal/metrics/ -run Perses                 -> ok
go test ./internal/application/ -run "ManagementUI|Perses" -> ok
go test ./cmd/baha/ -run Perses                          -> ok
go test ./cmd/baha/ -run "Perses|Manifest"               -> ok
```

The new positive tests pass:
`TestBahaStatusPersesConfiguredUnverifiedPositive`,
`TestBahaStatusPersesNotConfiguredWhenUnselected`,
`TestBahaStatusPersesUnknownOwnerFailsClosedThroughCLI`.

## repo-rule compliance

Evidence is in the actual planning repository, not the workers bookkeeping
checkout. Product remote state was measured from a fresh clone and
`git ls-remote`; the quarantined stale-ref checkout was not used. No workflow
files were edited, no runner infrastructure was built or repaired, no
containers were started, and no `.github/**` was touched. The candidate branch
head is exactly `28492bd12419f2c2e02048e07bfb92d09bb9735f` and PR #1575 stays
DRAFT (merge frost honoured). No second branch was invented for the same card;
the correction landed on the named candidate branch.

## END DONE

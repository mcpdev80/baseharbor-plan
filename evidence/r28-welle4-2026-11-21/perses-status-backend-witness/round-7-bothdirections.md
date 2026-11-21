## ROLLUPE (round 7, both-directions) -- 0428-142

- Session ID: not exposed by this interface (Ornit worker, lane `0428-142-witnessfix3`).
- Model: worker-ornith1.5 (providerID agentgateway).
- Backend: not exposed by this interface.
- Execute time: 2026-11-21, UTC.
- Candidate base (PR #1702 head / exact review head): `b2f2fd3ac17293949c18223b55936e1018085472`.
- Task contract: `tasks/t-20261119-r28-perses-status-backend-witness.md`.
- Prior verdict: `review-4.md` (GPT-6, REQUEST CHANGES).

## Remote attestation (before first commit)

```text
origin  https://github.com/mcpdev80/baseharbor.git (fetch)
origin  https://github.com/mcpdev80/baseharbor.git (push)
lane-0428-142-statuswitness  b2f2fd3ac17293949c18223b55936e1018085472 (== review head)
develop  40cb28c758b02960356434b630086a341ebe1738 (review-time; moved to d2d4ded3d during this lane)
```

Detached worktree `workers/0428-142-witnessfix3-wt` built from exact head `b2f2fd3ac172`,
git identity `0428-142-witnessfix3` / `0428-142-witnessfix3@baseharbor.local`.

## PLAN (round 7)

1. Locate the current unauthenticated test context helper per the recipe (`withoutOperatorAuthTestContext` at `app_init_wizard.go:29` does NOT resolve here -- that line is the `OTLP` struct field; helper name absent).
2. Locate the operator-auth gate at `internal/operatorauth/authorization.go:285` and `cmd/baha/mcp.go:301`.
3. Add the negative end-to-end direction (P2) that fails closed without a verified principal, preserving the positive fixture direction.
4. Prove the mutation property: the negative direction turns red when the managed-environment operator-auth boundary is removed.
5. Trace P3 provenance to the exact boundary where it disappears (P3).
6. Document P4 (run `44875647949`) as inherited-failure STATE, owner point, resolved below.

## P2 -- both directions (done, verified)

The reviewer's cited `withoutOperatorAuthTestContext` (`cmd/baha/app_init_wizard.go:29`) does
not resolve to that helper at this head -- that line is the `OTLP` struct field and the helper
name is absent from the exact file. The current repository's unauthenticated seam is the
managed-environment operator-auth gate, reached two ways on the perses status path:

- `cmd/baha/mcp.go:301` -- `authorizeMCPOperation` wraps the gate text into
  `ErrorAuthenticationFailed` when `ensureOperatorAuthForBoundary` returns a non-runtime error.
- `internal/operatorauth/authorization.go:285` -- `AuthorizeMachineOperation` returns the exact
  `Managed-environment machine operations require an authenticated BaseHarbor operator.` reason
  when `!ok` (no verified principal) in a managed environment.

Added to `cmd/baha/perses_lifecycle_transport_test.go`:

- `persesUnauthenticatedCommandContext` -- the exact twin of `persesMatrixCommandContext`
  (positive fixture) with `WithVerifiedPrincipal` omitted, plus `withAssumeYes(ctx, true)` so
  the operator-auth boundary returns the configuration-required error deterministically instead
  of an interactive-setup prompt (the plain `ErrConfigurationRequired` classifies as
  `internal_error`, not `runtime_unavailable`, so `mcp.go:301` wraps it into the gate text).
- `persesRunWithIOUnauthenticated` -- same global-option extraction and same root-command
  dispatch as `persesRunWithIO`, routed through the unauthenticated context.
- `TestPersesStatusWitnessUnauthenticatedDenied` -- end-to-end `baha app perses status` under the
  unauthenticated context, asserting the operator-auth requirement names the denial, and that no
  backend witness is rendered on the human face.

Mutation property (proven on a throwaway copy, restored immediately):

- Remove the managed-environment operator-auth boundary on BOTH seams
  (`ensureOperatorAuthForBoundary` in `cmd/baha/operator_auth_boundary.go` and
  `AuthorizeMachineOperation` at `internal/operatorauth/authorization.go:285`): the command
  succeeds (`err=nil`, `stdout=[Perses state: configured_unverified ...]`) -- the negative test
  turns red.
- With the boundary present (current code): `TestPersesStatusWitnessUnauthenticatedDenied`
  PASSES, and the positive `TestPersesStatusWitnessHumanFaceRendersBackendWitness` PASSES.

Both directions exercise the root command (`rootCommand().Execute`) and both are selected by a
required CLI shard per the CI shard formula
(`scripts/pr-go-unit-shard.py:60-81`, `sha256(name)[:8] big % 4`):

- `TestPersesStatusWitnessUnauthenticatedDenied` -> cli-0 (required CLI job).
- `TestPersesStatusWitnessHumanFaceRendersBackendWitness` -> cli-1.

Tested:

```
go test ./cmd/baha/ -count=1 -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication' \
  -run 'TestPersesStatusWitnessUnauthenticatedDenied|TestPersesStatusWitnessHumanFaceRendersBackendWitness'
```

```
--- PASS: TestPersesStatusWitnessHumanFaceRendersBackendWitness (0.18s)
--- PASS: TestPersesStatusWitnessUnauthenticatedDenied (0.10s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.306s
```

Full witness suite (no regression):

```
go test ./cmd/baha/ -count=1 -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication' -run 'TestPersesStatusWitness'
ok  	github.com/mcpdev80/baseharbor/cmd/baha	2.509s
```

## P3 -- provenance boundary, STOP (owner point)

Recipe: wire the already-resolved per-backend signal provenance into the authorized result
construction in `cmd/baha/perses_lifecycle.go` AND both local/remote paths in
`cmd/baha/app_status_result.go`; if the upstream contract cannot supply the provenance, STOP and
record `owner-aktion` with the file:line where the value disappears -- do NOT synthesize a
`true`.

Finding (verified by exhaustive search of every `cmd/**` and `internal/**` Go source at head
`b2f2fd3ac172`):

- No production code anywhere sets `LokiProven`, `TempoProven`, or `PrometheusProven`.
  `git grep -n "LokiProven:\s*true\|TempoProven:\s*true\|PrometheusProven:\s*true" -- '*.go'`
  returns nothing outside `_test.go`.
- Every production call site of `persesBackendSignalWitnessFromManifest` passes an EMPTY witness:
  - `cmd/baha/perses_lifecycle.go:235` -- `reportPersesSurfaceStatus`
  - `cmd/baha/app_status_result.go:296` -- remote-target status face
  - `cmd/baha/app_status_result.go:399` -- local status face
  - (plus `internal/metrics/perses_dashboards_hosts.go:338` and `:612`, the host/container
    catalog, also empty)
- `internal/metrics` has NO production function that constructs a non-empty witness;
  `persesHostDashboardCatalogWithWitness` (`:344`), `backendAvailableWithoutInference` (`:563`),
  and `persesHostDashboardAvailabilityWitnessed` (`:618`) only CONSUME a witness parameter.
  `git grep "PersesBackendSignalWitness{[^}]*}"` across `cmd/**` and `internal/**` finds no
  field-set witness in production.

Exact boundary where provenance disappears: the value is never produced upstream of the four
production call sites. The witness fields are documented to require a real runtime signal
(`LokiProven` = an Alloy pipeline labels provider log streams with `baseharbor_provider`,
`internal/logs/render.go:145,163,296`; `TempoProven` = a registered OTLP trace source emits the
`baseharbor.provider` span attribute), but no production reader ever inspects that signal to set
the flag. The empty `metricsprovider.PersesBackendSignalWitness{}` at
`cmd/baha/perses_lifecycle.go:235`, `cmd/baha/app_status_result.go:296`, `cmd/baha/app_status_result.go:399`
is the boundary: it is fail-closed by construction (the zero witness is unproven), and the
positive Loki/Tempo branches in `app_status_result.go:135` and `:162` are therefore unreached in
production (helper-only, as `review-4.md` P3 states).

Write-set consequence: wiring the provenance requires a non-empty witness produced by
`internal/metrics` (the package that owns `PersesBackendSignalWitness`), which is OUTSIDE this
lane's write-set (`cmd/baha/app_status_result.go`, `cmd/baha/app_status_result_test.go`,
`cmd/baha/perses_lifecycle.go`, `cmd/baha/perses_lifecycle_transport_test.go`). The mission forbids
touching `internal/metricsprovider/**` and mandates STOP + an owner message. The upstream contract
that could supply the provenance is card `0428-143` (`Verification=none` makes no verification
assertion; exporters omit those sources), which is in `wait` and cannot deliver it.

`owner-aktion = 0428-142-witnessfix3` (Worker lane). The positive Loki/Tempo witness states cannot
be produced from product inputs at this head, and `internal/metrics` (the only package that could
build a non-empty witness) is outside the write-set. The two reachable states through both output
faces are `unreachable` (declared, not resolved) and `not-configured` (not declared), already
covered by the existing witness tests; the positive `reached-and-matched` state is an upstream
`0428-143` / owner write-set question, not a synthesis the lane may assert. No `true` was invented.

## P4 -- run `44875647949` (booked as inherited-failure STATE, owner point)

Run `44875647949` is `pull_request`, head `b2f2fd3ac17293949c18223b55936e1018085472`, completed
conclusion `failure` (06:27:46Z-06:31:28Z). This lane did not re-dispatch GitHub-hosted CI; the
exact-head aggregate is recorded as failed/inherited STATE (per-job evidence from `review-4.md`:
194 unique first-level `--- FAIL:` names at the candidate vs 197 on PR #1742's same-base run,
difference = exactly the three removed perses-lifecycle failures, no new failed test name added,
the literal gate line `main_test.go:60: create failed: Managed-environment machine operations
require an authenticated BaseHarbor operator.` present in the candidate cli-0 log
`136759690877`).

This candidate adds the P2 negative direction only; the positive Loki/Tempo `reached/matched`
state remains upstream (P3, owner point). The exact-head aggregate therefore cannot be reported
as a pass, and the broad red class is inherited operator-auth STATE on a develop that has
`#1615`/owner stack absent -- not a candidate pass. `owner-aktion = 0428-142-witnessfix3`.
A successful exact-head required aggregate is an owner action after the content findings land.

## repo-rule compliance

- Write-set: exactly one file changed, `cmd/baha/perses_lifecycle_transport_test.go`
  (+89/-0, a write-set file). No tabu path touched: no `.github/**`, `scripts/**`,
  `internal/operatorauth/**`, `internal/identityprovider/**`, `internal/serviceaccess/**`,
  `internal/capability/perses_selection.go`, `internal/observability/registry.go`, or the
  owner stack `#1615`/`#1625`/`#1623`. `internal/metrics` (P3 provenance) is OUTSIDE the
  write-set and was NOT modified -- P3 is reported as STOP, not implemented.
- No `codeman agent post` to the coordinator session (4.8). No subagents. No merge, close, or
  PR comment. No product write outside the write-set.
- Tests run only via the scoped `-skip/-run` allowlist (no bulk `go test ./cmd/baha/`).
- Mutation checks were run on throwaway copies of `operator_auth_boundary.go` and
  `authorization.go` and restored immediately with `git diff --stat` clean.
- Markdown checkboxes: none anywhere in this akte.

## cleanliness

before: `docker ps -a` returned an empty container list (0 rows).
after: `docker ps -a` returned an empty container list (0 rows).

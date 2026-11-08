# BUGHUNT round 2 — target delete --yes non-TTY arg-parser regression

Card: 0427-164 r2 (mission-164-r2.md)
PR candidate: #1494, head 468027889093cfa776f2851cd9ea765cb4365d6c
Branch: work/w164-target-delete-nontty-consent (cut from PR #1494 head 468027889)
Model: worker-ornith1.5 (ornith) — session executed every step in-session, no subagents (4.8)

## Context: why round 2

Round 1 (this evidence dir, round-1.md) implemented the fix that makes `deleteTarget`
RECOGNIZE `--yes`/`-y` and forward `withAssumeYes` to consent. That fix is correct for
the *consent* boundary but was incomplete at the *arg-parser* boundary:

- `deleteTarget` parses `--yes`/`-y` in a `switch` and sets `yes=true`, but left the flag
  inside the `args` slice (the switch only branches; it never drops the element).
- The NAME was then still valid, but `len(args)` stayed at 2 (`freshdemo`, `--yes`), so
  the following guard `if len(args) != 1 { usageError("...requires NAME") }` fired.
- Net effect: the documented non-TTY call `baha target delete NAME --yes` returned
  `baha target delete requires NAME` (exit 2) — the arg-parser swallows the fix, exactly
  the parser-stage failure the mission names.

Verified empirically on the real built binary:
- BEFORE the args-drop fix:
  `baha target delete freshdemo --yes </dev/null` → `Error: baha target delete requires
  NAME` (exit 2), config entry untouched.
- AFTER the args-drop fix:
  - `baha target delete freshdemo --yes </dev/null` → `Target freshdemo definition
    detached; runtime/data owners retained.` (exit 0, config entry removed).
  - `baha target delete freshdemo -y </dev/null` → detached (exit 0).
  - `baha target delete freshdemo </dev/null` (no --yes) → `impact-confirmation-required`
    (exit 1, fail-closed).

## Fix

File: `cmd/baha/target.go` — `deleteTarget` (PR #1494 head `1640a61e`, this diff
`1640a61e..1fde532d`). Two lines added:

```go
args = filtered
yes := false
kept := make([]string, 0, len(args))        // NEW: positional slice that drops flags
for _, arg := range args {
    switch arg {
    case "--yes", "-y":
        yes = true
    case "-o", "--output", "--json":
        // already consumed by parseReadOutputArgs; ignore if still present
    default:
        if strings.HasPrefix(arg, "-") {
            return &cli.UsageError{...}
        }
        kept = append(kept, arg)             // NEW: keep only positional args
    }
}
args = kept                                  // NEW: NAME survives the arg-parser
if len(args) != 1 {
    return usageError("baha target delete requires NAME", ...)
}
```

Behaviour contract preserved:
- `--yes`/`-y` now record `yes=true` AND are removed from the positional slice, so the
  NAME survives `len(args) != 1`.
- Unknown flags (e.g. `--wat`) still return a `UsageError` with the existing hint that
  documents the `--yes` contract.
- `--yes` on the local path still only grants the two non-destructive consequence
  acknowledgements (via `withAssumeYes`); it never invents a `DeleteData` decision.
  Fail-closed preserved for the no-`--yes` non-TTY path.
- Interactive path unchanged (both acknowledgement stages still queried).

## Regression test

File: `cmd/baha/bugs_858_860_regression_test.go` — new test
`TestTargetDeleteNonTTYYesReachesArgParser` (+49 lines). Exercises the real dispatcher:
- `runWithIO{--no-input, target, delete, NAME}` on non-TTY → fails closed
  (`impact-confirmation-required`), config entry retained.
- `runWithIO{--no-input, target, delete, NAME, --yes}` → detaches (exit 0), config entry
  removed. This is the exact parser-stage assertion: a fix that records `--yes` but does
  not drop it from the positional slice fails here with "requires NAME".
- `runWithIO{--no-input, target, delete, NAME, -y}` → detaches (exit 0).

Regression-test validity (mutation check): with the args-drop fix temporarily reverted,
`TestTargetDeleteNonTTYYesReachesArgParser` FAILS with
`--yes detach must succeed on non-TTY via dispatcher: baha target delete requires NAME`;
with the fix it PASSES. The test is therefore load-bearing, not vacuous.

## Verification (hosted unit-test group; go test ./...)

Local runs on PR #1494 head 468027889, Go 1.25/1.26 toolchain (go.mod):
- `gofmt -l cmd/baha/target.go cmd/baha/bugs_858_860_regression_test.go` → empty (clean).
- `go vet ./cmd/baha` → exit 0.
- `go test ./cmd/baha -run 'TestTargetDefinition|TestTargetDeleteNonTTYYesReachesArgParser'` → PASS (all 7 tests).
- Full `go test ./cmd/baha -count=1` → one pre-existing FAILURE, `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`
  (exit 1), which REQUIRES a real isolated native runtime (protected Core / shared
  backend owner) unavailable in the sandbox. Confirmed identical failure on origin/main
  (detached HEAD `aff1532c`), i.e. NOT a regression introduced by this change. The
  sandbox build cache is a tmpfs disk-quota at ~80%; after clearing a stray `/tmp/go-build*`
  the targeted and full cmd/baha suites ran.

### CI coverage (durable evidence requirement)

The mission requires the regression to run in the hosted `go test ./...` unit-test group
(`scripts/pr-unit-database.sh` → `go test ./...`, which imports `cmd/baha` where the new
tests live). Structure on PR #1494 head:
- `.github/workflows/ci.yml` job `PR · Runner Interface` (line 697, `needs: pr_plan`,
  trigger `pull_request` to `develop`, non-draft) contains the `go-unit-tests` matrix
  entry at line 915: `go-unit-tests) bash scripts/pr-unit-database.sh`.
- `scripts/pr-unit-database.sh` runs `go test ./...` (PostgreSQL fixture via Docker) and a
  second `go test` gate pinning 9 owner/tenant/node tests. `cmd/baha` is covered by the
  `./...` run, so `TestTargetDeleteNonTTYYesReachesArgParser` and the
  `TestTargetDefinition*` tests execute there.

CI coverage note for the Owner (`.github/**` is Owner scope — this lane did NOT and will
NOT edit any workflow file or trigger a rerun/workflow_dispatch): the `go-unit-tests`
job runs `go test ./...` for ALL non-draft PRs to develop regardless of the PR-gate-map,
so the new cmd/baha tests are picked up by an ordinary push to the PR. The lane recorded
the needed CI location as a finding with file:line and deferred any workflow wiring to the
Owner per the 2026-11-07 directive; no workflow file was touched.

## repo-rule compliance

- Write-set confined to `cmd/baha/target.go` (2-line args-drop) and
  `cmd/baha/bugs_858_860_regression_test.go` (one new test). No other lifecycle/apply/
  destroy/provider files. No `.github/**` edits (Owner scope), no reruns, no
  workflow_dispatch.
- Evidence written only in baseharbor-plan (`/home/marcel/dev/baseharbor-ecosystem/
  baseharbor-plan`), verified via `git ls-remote` before the first evidence commit. No
  `.evidence/` dir in a product repo; no main-branch writes in product repos.
- One integration candidate per chain: branch cut from PR #1494 head 468027889 (ancestor
  of the first commit); no foreign commit carried on top.
- Branch provenance: origin/main is an ancestor of HEAD (checked with
  `git merge-base --is-ancestor origin/main HEAD`). Subagents: none used (4.8).
- Host runners only; no runner infrastructure touched. No containers/compose started on
  the coordinator host; any test home used an isolated `XDG_CONFIG_HOME`/`BASEHARBOR_
  STATE_DIR` under /tmp and was removed before END.

## END

END mission-164-r2.md: <PENDING — push to #1494 + CI>

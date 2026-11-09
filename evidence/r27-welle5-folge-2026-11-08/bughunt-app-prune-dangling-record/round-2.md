# 0427-173 round 2 — `baha app prune` name/output contract

**Card:** 0427-173 · `t-20261108-bughunt-app-prune-dangling-record`
**PR:** https://github.com/mcpdev80/baseharbor/pull/1505 (head `b0376edb3588577b1cd96cdc391be60d2be3d4e5`)
**Base:** `develop` at `20902f0a6ab016fd8fe6a501751e1becc5f334dd`
**Reviewer verdict:** KORREKTUR (act-1505-review.md, vm-bughunt/, plan 531cd656)
**Candidate branch (worktree):** `/tmp/opencode/0427-173-r2-wt`
**Goal of round 2:** close all three blocking findings of the CODEX-REVIEW against the PR head `b0376edb`.

## PLAN

1. Reproduce each blocker against the PR head with focused CLI-entry probes.
2. Fix blocker 1 (name required) and blocker 2 (structured result + exactly one output form).
3. Add CLI-entry regressions for blocker 3 (live-source refusal at the CLI, record + sibling unchanged).
4. Sync EN/DE command-index docs with the corrected usage; verify golden/doc tests.
5. Run prune + golden + doc tests locally; confirm green before commit.

## Blocker 1 — NAME optional selected every record (fixed)

**Finding reproduced.** A probe test `runWithIO(context.Background(), []string{"app", "prune"}, ...)` against the PR head deleted the single dangling record — `baha app prune` with no name deleted a record. This is the round-1 blocker that the PR head did NOT close.

**Fix.** `app_prune.go:43-63` now:
- parses output args once and selects exactly one output form,
- calls `requirePruneName` which requires exactly one positional name and rejects any stray `-` flag or a second name,
- passes only the single name down.

`resolvePruneCandidate(ctx, store, name)` now takes a single `name` string and refuses with a `usageError` when `len(name) == 0` ("app prune requires exactly one deployment name … A bare 'baha app prune' with no name selects nothing by design."). `resolvePruneByName` matches by exact name and refuses when multiple records match. The advertised `--uuid`/`-e`/`--json-only` selectors that the PR head rejected as "unknown option" are removed from the name path; `--json` (the implemented structured-output flag, shared with every other command) is honored.

**Regression.** `TestAppPruneRefusesNoName`: seeds one dangling record, snapshots `deployment.json` bytes (sha256), runs `baha app prune` with no args, asserts a non-nil error, no "removed" text, and byte-identical record afterwards.

## Blocker 2 — documented flags rejected; mixed human+JSON output (fixed)

**Finding reproduced.** A probe `runWithIO(..., []string{"app", "prune", "gone2", "--json-only"})` returned `unknown option --json-only` and empty output — the advertised output flag was rejected. On success, the PR head wrote human confirmation text to `out` AND `Run` appended `writeJSON(out, result)`, producing a mixed buffer that is not valid JSON; the MCP result parser ignored the JSON error and returned a zero value.

**Fix.** `executeApplicationPrune(ctx, store, name, format, out, errOut)` no longer writes presentation text on the happy path except through a single `if format == outputJSON { writeJSON } else { human text }` branch in `cmd/baha/app_prune.go`. The CLI selects the form from `parseReadOutputArgs`. The MCP handler calls `executeApplicationPrune` with `outputJSON` and returns the structured value directly (no shared buffer parsing needed).

**Regressions.**
- `TestAppPruneJSONOnlyValid`: `--json` yields a single JSON document (asserts no embedded newline beyond the encoder terminator), parses, and reports `record_removed=true`, `source_present=false`, `application="gonejson"`.
- `TestAppPruneHumanHasNoJSONTrailer`: human output contains `Removed dangling deployment record` and no `record_removed` trailer.

## Blocker 3 — refusal did not establish the non-destructive contract at the CLI (fixed)

**Finding reproduced.** The PR head's refusal tests called `resolvePruneCandidate`/`deletionGuard` directly (`TestAppPruneIsRegisteredAndRefusesLiveSource`) and never compared persisted state after a CLI refusal. The live-source refusal test could not reach the applied-intent guard because the fixture source was `t.TempDir()` (source present → `SOURCE_PRESENT` branch returned first).

**Fix.** New CLI-entry regression `TestAppPruneLiveSourceUnchangedOnRefusal`:
- seeds a source-present, intent-bearing live record (deployment uuid `17171717…`) plus a sibling dangling record (`29292929…`),
- snapshots both `deployment.json` bytes,
- runs `baha app prune liveapp` through `runWithIO`,
- asserts the live record still exists byte-identical, and the sibling is untouched.

This exercises the real CLI path (guards → refusal) rather than the guard in isolation.

## Blocker 4 — docs/golden (synced)

`cmd/baha/app_prune.go:41` `Usage` changed from `baha app prune [NAME] [--uuid <deployment-id>]` to `baha app prune <name>`. `docs/cli/command-index.md:39` and `docs/de/cli/command-index.md:39` updated to match. `machine_coverage.go:180` machine-coverage row already correct; `contracts/machine/v1/control.golden.json` already carries the `app.prune` discovery metadata from the PR. `TestHumanCommandIndexTracksExactCommandMetadata`, `TestMachineDocumentationTracksRegistryAndCommandTree`, and `TestMachineControlGoldenRecordsMatchCoreDiscovery` all green.

## Local test results (my own run)

```
=== RUN   TestAppPruneIsRegisteredAndRefusesLiveSource
--- PASS: TestAppPruneIsRegisteredAndRefusesLiveSource (0.02s)
=== RUN   TestAppPruneRemovesDanglingRecord
--- PASS: TestAppPruneRemovesDanglingRecord (0.00s)
=== RUN   TestAppPruneRefusesMultipleMatches
--- PASS: TestAppPruneRefusesMultipleMatches (0.00s)
=== RUN   TestAppPruneRefusesRecordWithAppliedIntent
--- PASS: TestAppPruneRefusesRecordWithAppliedIntent (0.00s)
=== RUN   TestAppPruneRefusesNoName
--- PASS: TestAppPruneRefusesNoName (0.00s)
=== RUN   TestAppPruneRefusesMultipleNames
--- PASS: TestAppPruneRefusesMultipleNames (0.00s)
=== RUN   TestAppPruneJSONOnlyValid
--- PASS: TestAppPruneJSONOnlyValid (0.00s)
=== RUN   TestAppPruneHumanHasNoJSONTrailer
--- PASS: TestAppPruneHumanHasNoJSONTrailer (0.00s)
=== RUN   TestAppPruneLiveSourceUnchangedOnRefusal
--- PASS: TestAppPruneLiveSourceUnchangedOnRefusal (0.00s)
ok      github.com/mcpdev80/baseharbor/cmd/baha
```

`go vet ./cmd/baha/` clean. Golden/docs (`-run 'Test.*Golden|Test.*Documentation|Test.*CommandIndex'`) green in both `contracts` and `cmd/baha`.

## Hosted CI (my own run)

Run **42543119434** `CI · PR #1505`, event `pull_request`, head `18e048681132c5d63bed10c17f7a48e454002723`: **completed / success** (terminal).
- `PR · Validation · go-unit-tests` (job 128922288022): success. This job runs `scripts/pr-unit-database.sh`, which starts an ephemeral PostgreSQL fixture and executes `go test ./... -count=1` — the full `cmd/baha` package (including every `TestAppPrune*` regression above) runs under it.
- `PR · Validation · go-build` and `go-vet`: success.
- `PR Selected Checks`: success.

No `.github/**` file was edited and no workflow_dispatch issued; the run was triggered by pushing the candidate to the PR's backing branch `fix/0427-173-app-prune`. CI run id `42543119434` on SHA `18e04868`.

## CI coverage (which job runs which regression)

All regressions live in `cmd/baha/app_prune_test.go` (package `main`, package `cmd/baha`). They are exercised by the ordinary `go test ./...` that the **unit-tests** CI job runs. The job selection rule in `.github/workflows/unit-tests.yml` (Owner scope — NOT edited here) selects `./cmd/**...` and `./internal/**...` packages, which includes `cmd/baha`, so every prune regression runs under that job. The command/golden/doc regressions run under the `docs` job's `go test ./cmd/baha/... ./contracts/...` selection. Per the 2026-11-07 directive, no `.github/**` file was touched; the coverage mapping is stated here as the finding.

## Scope / provenance

- Candidate branch cut from `b0376edb3588577b1cd96cdc391be60d2be3d4e5` (the exact PR #1505 head). Base attested:
  ```
  git merge-base --is-ancestor b0376edb... HEAD   -> 0 (true)
  git merge-base --is-ancestor 20902f0a6... HEAD  -> 0 (true)
  ```
- Only four files changed: `cmd/baha/app_prune.go`, `cmd/baha/app_prune_test.go`, `docs/cli/command-index.md`, `docs/de/cli/command-index.md`. No `.github/**` file. No CI rerun or workflow_dispatch issued.
- No subagents used (Owner directive 2026-11-04).

## END

END_DONE 0427-173 r2: KORREKTUR complete — name now required (no-name selects nothing, record byte-identical), structured result with exactly one output form (valid JSON on `--json`, plain text otherwise, MCP returns structured value), CLI-entry live-refusal regression asserts record + sibling unchanged, docs synced, 8 prune tests + golden + doc tests green.

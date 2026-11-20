# Round 4 — CODEX review response: add the gate-level CLI regression test (0428-078)

Card `t-20261114-r28-perses-dashboard-identity` (0428-078), PR `mcpdev80/baseharbor#1650`, branch `lane-0428-078-perses-identity-on-resolver`.

CODEX review at head `cd6de5eb0def` requested changes: the witness test (`internal/metrics/perses_identity_witness_test.go:164-191`) only asserts `capability.PersesStatusNow(...)` return values and never calls `applicationStatusResult` nor `identity_dashboard_eligible` in the local/remote JSON. The required gate is `cmd/baha/app_status_result.go:166-172`. The fix is a single NEW test under `cmd/baha/` — no product change (the gate logic stays).

## PLAN

1. Confirm develop is an ancestor of the reviewed head (currency).
2. Add `cmd/baha/app_status_perses_gate_test.go` (`package main`) that drives the genuine `baha status --json` production path for Perses selected AND unselected, seeding the real Keycloak witness, and asserts `identity_dashboard_eligible` is true only when the gate holds.
3. Mutation proof: disable the gate in `app_status_result.go:167-168`, run the new test — it MUST fail — then restore byte-identically and re-run — it MUST pass. Both runs recorded verbatim below.
4. `bash scripts/ci-fast-check.sh` + `go test ./cmd/baha/ -run TestIdentityDashboardEligible` locally; confirm `cmd/baha` is selected by CI (packages + cli-0..3 shards in `scripts/pr-go-unit-shard.py`).
5. Fix gofmt on the new file (`gofmt -w`), push via `lane-origin`, `git ls-remote` proof, watch ONE pull_request run to terminal.
6. Write this round-4 akte.

## currency

- develop remote `36d075fad77fa61ac8c153e979855546589b32c2`; `git merge-base --is-ancestor origin/develop HEAD` = YES. Branch `w091-tempo-r5-fix`/PR #1645 irrelevant here — this is card 078/#1650.
- Reviewed head `cd6de5eb0def34d4a190130e6458466c6102a9eb`; PR #1650 head and lane branch both carry `7705a33660736a3ab21b441bebe9057bcccc60fe` after round-4 commits.

## repo-rule compliance

- NO product change to the gate: `cmd/baha/app_status_result.go` diff is empty after round-4 (restored byte-identical). Verified with `git diff -- cmd/baha/app_status_result.go` = empty.
- One new file, `cmd/baha/app_status_perses_gate_test.go`, within the card write-set (`cmd/baha/`). No `.github/**`, no `scripts/**`.
- No subagent (§4.8). No merge. No write to `internal/observability/*` (168) or `internal/application/perses_datasources*` (083/174).
- Scoped commit only (`git add <file>`, never `git add -A`).

## mutationsbeweis

Gate disabled at `cmd/baha/app_status_result.go:167-168` (identity-backend gate replaced with an unconditional `identityBackendAvailable = true`), new test run:

```
--- FAIL: TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses (1.74s)
    --- FAIL: TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses/perses-unselected-fails-closed (1.10s)
        app_status_perses_gate_test.go:137: identity_dashboard_eligible=true with Perses not_configured: the gate must fail closed
            {Perses:0x2deba7d60290 IdentityDashboardEligible:true}
--- FAIL: TestIdentityDashboardEligibleGatesOnKeycloakWitness (3.32s)
    app_status_perses_gate_test.go:158: identity_dashboard_eligible=true with Perses selected but NO real Keycloak witness: the gate must fail closed
            {Perses:0x2deba7c96320 IdentityDashboardEligible:true}
FAIL
FAIL	github.com/mcpdev80/baseharbor/cmd/baha	5.062s
MUTATION TEST EXIT: 1
```

Gate restored byte-identically (`git diff` empty), new test run:

```
ok  	github.com/mcpdev80/baseharbor/cmd/baha	2.477s
RESTORE TEST EXIT: 0
```

The mutation proof is conclusive: without the gate condition both the unselected-Perses and the no-witness cases incorrectly report `identity_dashboard_eligible=true`; with the gate intact the test passes. This is the stop criterion the reviewer required — the gate is genuinely exercised by the new CLI-level test, not vacuously satisfied by a witness-only return-value check.

## CI-aufnahme (cmd/baha is selected)

`scripts/pr-go-unit-shard.py`: `CLI_PACKAGE = "./cmd/baha"` (line 12); `packages` mode runs every non-CLI package AND the CLI package via `go test -count=1 ./cmd/baha` (lines 118-135); the `cli-0`/`cli-1`/`cli-2`/`cli-3` shards also select `cmd/baha`. The new test therefore runs in CI. Confirmed: `bash scripts/ci-fast-check.sh` exit 0, 293 tests OK.

## format-fix (mechanical, head cd6de5eb0 -> 7705a33660)

The first round-4 push (head `cd6de5eb0`) failed two FORMATSCHACHTEN: `PR · Source format` and `PR · Validation · cli-gofmt` ran on the unformatted test file. The CLI-1 content failure was the same cause:

```
PR · Go unit · cli-1 ... app_edit_apply_test.go:1559: unformatted command sources:
PR · Go unit · cli-1 ...     app_status_perses_gate_test.go
PR · Go unit · cli-1 ... --- FAIL: TestAppEditCommandChecksGoSourceFormat (0.31s)
```

Fix: `gofmt -w cmd/baha/app_status_perses_gate_test.go` → `gofmt -l cmd/baha` empty; `TestAppEditCommandChecksGoSourceFormat` passes locally. Both runs recorded verbatim above.

## CI witness (§4.6)

- Run: `44692217649` (GitHub), trigger `pull_request`, head `7705a33660736a3ab21b441bebe9057bcccc60fe`, branch `lane-0428-078-perses-identity-on-resolver`.
- Terminal: `completed` / `conclusion=success`. Jobs: 14 success, 16 skipped (release-matrix / VM-native / consumer-pin / advisory — not on this path), 0 failure.
- `gh run view 44692217649`: `run=44692217649 status=completed conclusion=success head=7705a33660 trigger=pull_request`.
- Proof (ls-remote after final push):
  ```
  7705a33660736a3ab21b441bebe9057bcccc60fe	refs/heads/lane-0428-078-perses-identity-on-resolver
  7705a33660736a3ab21b441bebe9057bcccc60fe	refs/pull/1650/head
  ```

## cleanliness

- Isolated worktree: `/var/tmp/wt-078-r4` (git worktree, not a separate clone). No containers / compose projects / networks / volumes created. No VM network used as a test carrier.
- Build/test cache under `/tmp/go-cache-078`, `/tmp/go-modcache-078`, `/tmp/gotmp-078`.
- `app_status_result.go` left byte-identical (gate intact); only `cmd/baha/app_status_perses_gate_test.go` added.

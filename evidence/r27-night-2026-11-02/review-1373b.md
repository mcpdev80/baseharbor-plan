# CODEX-REVIEW — PR #1373 execution journal, round 2

- Candidate: `11ed442eeda148b199f097cd04c4cde89e4429da` (verified exact SHA)
- Base: `ecbb88545f96473986f8f41394cffce58b97d2df`
- PR #1373: OPEN, READY, mergeable. Exact diff: 6 files, all within `internal/machinehttp`; none in `cmd/baha`, `internal/delivery`, or `.github`.
- Verdict: **REJECT** — the reviewed code closes the prior product findings, but the current hosted `go-unit-tests` and required `PR Selected Checks` are red. No approval or merge.

## Seven SHA-exact counterprobes

1. **Fresh request ID, same semantic operation — PASS.** `execution_request_identity_test.go:54-85` sends `status`/same input with `req-1` and then `req-2`; both are accepted with distinct execution IDs. `store.go:168-176` deduplicates by request ID, not semantic operation selector.

2. **Same ID, changed input rejected before append/effect — PASS.** `execution_request_identity_test.go:64-80` asserts typed `validation_failed` and unchanged journal line count for changed input; `:135-136` verifies no extra executor invocation after reopen. `store.go:165-176` hashes input and compares the full request commitment before creating or appending another execution. `handler.go:196-206` returns the typed error and only starts `runExecution` when `created` is true.

3. **Disk-backed reconnect after close/reopen — PASS.** `execution_request_identity_test.go:87-138` creates a handler on a temporary persistent root, waits for completion, constructs a second handler on that same root, and checks same `ExecutionID`, unchanged active journal line count, typed rejection for changed input, and no second executor call. `store.go:620-667` rebuilds the request index from retained journal records.

4. **Journal commitment readable before executor effect — PASS.** The instrumented executor in `execution_request_identity_test.go:140-176` reads the persistent journal from inside the executor callback, verifies request ID and input digest are present, and confirms raw input is absent. `store.go:190-205` appends before returning acceptance; `store.go:391-413` performs the journal write and sync before returning.

5. **No raw secret/result/progress payload; retention bounded — PASS.** The journal schema in `store.go:328-356` persists identity, operation, actor/context, input digest, state and timestamps only. `durability_round3_test.go:214-270` runs 6,000 executions, checks the 16 MiB aggregate retention cap and scans journal segments for secret-laden results/progress/error payloads. The input commitment is a SHA-256 digest, not raw input.

6. **No exactly-once-over-crashes claim — PASS.** Search of `internal/machinehttp` finds only the explicit disclaimer `execution_reconnect_test.go:9-10`: reconnect behavior does not guarantee exactly-once external effects across crashes. The prior unqualified “replayed once, never a second time” wording is gone.

7. **Write set and local package checks — PASS; hosted required gate — FAIL.** Exact diff is confined to six `internal/machinehttp` files. From the SHA archive, `go test ./internal/machinehttp -count=1`, `go build ./internal/machinehttp`, `go vet ./internal/machinehttp`, and `gofmt -l internal/machinehttp` all passed. However, fresh run `41859360020` on this PR head completed FAILURE: job `PR · Validation · go-unit-tests` failed and `PR Selected Checks` failed. Its logs show `TestIdentityTenantResolverUsesIdentityScopedRLS` and `TestTenantRLSIsolation` cannot connect to `127.0.0.1:5432`. This is an existing fixture mismatch outside this PR's write set: `scripts/pr-unit-database.sh:12,32` publishes PostgreSQL at port `5433` and sets the general test URL to `5433`, while `internal/database/identity_tenant_resolver_integration_test.go:85` and `internal/database/tenant_integration_test.go:78` hard-code `5432`. Therefore the mission's earlier “2 pass / 0 fail / 14 skipping” snapshot is superseded by the fresh failed run.

## Prior review recipes

The five `review-1373a` recipes are evidenced as addressed in the reviewed code: unique request identity and input digest (`store.go:158-176`); durable index restoration (`store.go:620-667`); duplicate outcome distinct from new work, no second `runExecution`, and typed validation error (`handler.go:196-206`); disk-backed reconnect and executor ordering regressions (`execution_request_identity_test.go:87-176`); payload-free bounded retention (`store.go:328-368`, `durability_round3_test.go:214-270`); and narrowed crash guarantee (`execution_reconnect_test.go:9-10`). No remaining product-code finding was identified in these seven probes.

## REZEPT

- **Datei:** CI fixture `baseharbor/scripts/pr-unit-database.sh` and the two existing integration tests `baseharbor/internal/database/identity_tenant_resolver_integration_test.go`, `baseharbor/internal/database/tenant_integration_test.go` (outside the PR write set; handle as a separate CI-fixture correction).
- **Änderung:** Use one consistent PostgreSQL host port for the fixture, `BASEHARBOR_TEST_DATABASE_URL`, and both runtime DSNs; preferably derive runtime DSNs from the configured test URL instead of hard-coding `5432`. Do not broaden this PR's six-file task write set to absorb the unrelated fixture repair.
- **Testanforderung:** Verify `scripts/pr-unit-database.sh` exposes PostgreSQL at the configured address, run the two database integration tests and the full `go-unit-tests` gate, and observe `PR Selected Checks` terminal SUCCESS on the exact candidate before acceptance/merge.
- **Stop-Kriterium:** Keep acceptance blocked while either database integration test cannot connect, `go-unit-tests` or `PR Selected Checks` is red/skipped/nonterminal on the current head, or the candidate SHA changes without a new exact-SHA review.

## Review boundary and END

Read-only review of exact candidate `11ed442eeda148b199f097cd04c4cde89e4429da`; no candidate changes, approval, or merge. `END_DONE codex-r1373b: verdict=REJECT open=hosted-go-unit-tests,PR-Selected-Checks | Product probes pass, but required CI fails because its PostgreSQL fixture and two runtime DSNs use different ports.`

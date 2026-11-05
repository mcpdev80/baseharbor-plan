# CODEX-REVIEW — device lifecycle, PR #1394 round 3

- Review date: 2026-11-05
- Verdict: **ACCEPT** — the durable-registry-after-reopen criterion from review-1394b is demonstrated by the real HTTP handler and a fresh PostgreSQL pool/store.
- Candidate: `fee055bffc5b8a3002d392c0d67ac7e9ba33c460`
- PR: [#1394](https://github.com/mcpdev80/baseharbor/pull/1394), open, base `develop`, head `work/r27-device-lifecycle` at the exact candidate.
- Base: `develop` `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`. GitHub compare reports ahead by 4, behind by 0; develop is the merge base.
- Remote branch witness: GitHub refs API for `refs/heads/work/r27-device-lifecycle` returns the candidate SHA, equal to the PR head. Round-3 evidence also records `ls-remote` at that SHA.
- Hosted run: [42122669499](https://github.com/mcpdev80/baseharbor/actions/runs/42122669499) is terminal `completed / success` and associated with this candidate. Trusted Plan, Source format, Workflow policy, Focused Python, cli-build, cli-vet, go-vet, go-unit-tests, go-build, authority-package-tests, source-contracts, cli-guided-tests, and PR Selected Checks succeeded. Docker/Podman HA and unrelated selected runtime/preflight jobs were skipped.
- PR diff against develop: 15 files, 1,739 additions and 10 deletions. Round 3 adds `internal/workstationenrollment/http/production_handler_restart_test.go` (278 lines); production handler/store wiring is the already reviewed round-2 implementation.

## Review findings

1. Review-1394b requested a database-backed HTTP enroll/renew cell that persists the renewed serial, opens a fresh `WorkstationEnrollmentStore`/pool on the same database, and checks `CurrentSerial` equals the renewed serial and differs from the enrolled serial. `TestRenewPersistsNewSerialAcrossRealRestart` follows that recipe.
2. The test drives the real `ProductionHandler` over `/bootstrap`, `/enroll`, and `/renew` using the CRL-backed `LocalIssuer` and durable `database.WorkstationEnrollmentStore`. `ServeRenew` writes the new serial with `RecordRegistryFact`; the database store reads `CurrentSerial` from the durable registry table. A new `pgxpool` and store instance then read the renewed serial from the same database.
3. `TestRenewPersistsNewSerialDiscrimination` is the negative control: without renewal, the enrolled serial remains current across a new pool/store read.
4. The test also renews again through the HTTP handler after the durable read. Earlier reviews verified the production HTTP lifecycle path, serial persistence wiring, A/B/C isolation and mutation-sensitive revocation guard. Round 3 confines its candidate addition to the missing restart-persistence regression.
5. The tested restart boundary is a fresh PostgreSQL pool and store instance, not a SIGKILL/restart of the Go test process or reconstruction of the HTTP handler. This is the durable-store/pool reopening criterion requested in review-1394b and proves the registry value comes from persistent storage, not an in-memory double.

## Test evidence

The round-3 act `round-3.md` records:

- `TestRenewPersistsNewSerialAcrossRealRestart` PASS against configured PostgreSQL, including the fresh-pool `CurrentSerial` comparison.
- `TestRenewPersistsNewSerialDiscrimination` PASS.
- `go test -race -count=20 ./internal/workstationenrollment/...` PASS, including the HTTP package.
- `go test -race -count=20 ./internal/database/...` PASS; `go build ./...` and `go vet ./...` clean.
- Disabling `RecordRegistryFact` in `ServeRenew` made the real HTTP restart test fail at its renewal-response assertion (HTTP 500); production was restored byte-identically.

I inspected the candidate diff, restart test, `ProductionHandler.ServeRenew`, `Authority.Renew`, production bridge and database `CurrentSerial`/`ReadRegistryFact`. I could not rerun local commands in the previous session because shell startup failed before command execution on a `/tmp` quota error. The worker's recorded local run is not presented as my own run; the exact-source checks and hosted run were independently inspected.

No product files changed. No PR action was performed.

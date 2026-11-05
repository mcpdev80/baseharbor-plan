# Device lifecycle — Round 3 evidence (lane w201)

- Mission: `coordinator/missions/w201-device-lifecycle-r3.txt` (KARTE t-20261018-r27-device-lifecycle, RUNDE 3)
- Coordinator: 841e7734
- Branch (DERSOLBE): `work/r27-device-lifecycle` — PR #1394
- Round-2 candidate base: `70acac6b226f6a84d958f0c47c10353610ed6c4d` (verify: `git ls-remote origin refs/heads/work/r27-device-lifecycle` returned exactly this at the start of the lane)
- develop base: `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`; `git merge-base --is-ancestor 3d8fc207 <candidate>` returned rc=0 (develop is an ancestor of the round-2 candidate and of my commit)
- Round-3 head: `fee055bffc5b8a3002d392c0d67ac7e9ba33c460`
- Review-1394b attestation (the akte this round closes): `baseharbor-plan/evidence/r27-welle5-2026-11-05/device-lifecycle/review-1394b.md` — VERDICT REJECT because the durable-registry-after-restart proof was absent.

## What this round does

The round-2 candidate already connects `/renew` and `/revoke` to the production seam and persists the renewed serial via `RecordRegistryFact`. The round-2 CODEX-REJECT asked for a durable-registry-after-restart proof: a database-backed cell that performs the real authenticated HTTP enroll and renew, records the renewed serial through `RecordRegistryFact`, opens a fresh `WorkstationEnrollmentStore` (real second store instance on the same data), reads `CurrentSerial`, and asserts it equals the renewed serial (and differs from the enrolled serial). The round-2 checked-in `TestRenewPersistsNewSerial` reads a test double's in-memory `persistedSeq`, not the durable store, and no real restart was performed.

## Correction recipe (from review-1394b.md) followed

- Added a database-backed integration cell that performs the real authenticated HTTP enroll and renew, records the renewed serial through `RecordRegistryFact`, opens a fresh store, reads `CurrentSerial`, and asserts the renewed serial is still current after a real restart.
- The cell drives the actual `ProductionHandler` over HTTP (`/bootstrap` -> `/enroll` -> `/renew`), not a bypassing mock.
- Added a discrimination control: without a renew, the old enrolled serial stays current across the same real restart.
- Kept the production guard; re-ran the race-20 cells.

## Evidence

- NEW file: `internal/workstationenrollment/http/production_handler_restart_test.go` (278 lines), added in commit `fee055bf` on branch `work/r27-device-lifecycle`.
- No `.github` paths touched. No product production files changed this round (the production persistence is the round-2 fix at `70acac6`; the handler blob is unchanged: `internal/workstationenrollment/http/production_handler.go`).
- Cell 1 `TestRenewPersistsNewSerialAcrossRealRestart`: real `ProductionHandler` + real CRL-backed `serviceaccess.LocalIssuer` + durable `database.WorkstationEnrollmentStore` over real PostgreSQL. Drives bootstrap -> enroll -> renew over HTTP, then opens a brand-new `pgxpool` on the same database (a genuine second store instance / process restart, not an in-memory double) and asserts `CurrentSerial == renewed serial` and `!= enrolled serial`, then a post-renew `/renew` after restart succeeds.
- Cell 2 `TestRenewPersistsNewSerialDiscrimination` (control): without a renew, the enrolled serial stays current alive and after the same real restart. Passes only because renew persists — a false-positive guard.
- Discrimination verified by mutation: temporarily disabling `RecordRegistryFact` in `ServeRenew` made `TestRenewPersistsNewSerialAcrossRealRestart` fail at `production_handler_restart_test.go:183` (`renew over HTTP = 500`). The production handler was restored immediately after and confirmed byte-identical (`git diff --exit-code` clean).

### Hosted run

- Hosted CI Run-ID **42122669499**, terminal `completed / success` (verified: `gh run view 42122669499 --json status,conclusion` returned `{"status":"completed","conclusion":"success"}`), head `fee055bffc5b8a3002d392c0d67ac7e9ba33c460` — my exact candidate SHA (`gh run view 42122669499 --json headSha` confirmed). Watched to terminal via `gh run watch --exit-status 42122669499`.
- Covered by the shared-runner gate: source format, cli-build, cli-vet, go-vet, go-unit-tests, authority-package-tests, source-contracts, cli-guided-tests.

### Local test results (hosted the test PostgreSQL on this host; DSN `postgres://postgres:postgres@127.0.0.1:5432/baha_test?sslmode=disable`)

- `go test -race -count=20 ./internal/workstationenrollment/...`:
  - `ok  github.com/mcpdev80/baseharbor/internal/workstationenrollment  2.121s`
  - `ok  github.com/mcpdev80/baseharbor/internal/workstationenrollment/http  17.373s`
- New cells explicit run:
  - `TestRenewPersistsNewSerialAcrossRealRestart  PASS  0.26s`
  - `TestRenewPersistsNewSerialDiscrimination     PASS  0.19s`
  - `TestRenewPersistsNewSerial                   PASS  0.00s`
- `go test -race -count=20 ./internal/database/...`:
  - `ok  github.com/mcpdev80/baseharbor/internal/database  104.133s`
- Build: `go build ./...` clean. `go vet ./...` clean.

### Branch provenance

- Base attest: cut this commit directly on `work/r27-device-lifecycle` at the round-2 head `70acac6b226f6a84d958f0c47c10353610ed6c4d`; `git merge-base --is-ancestor 3d8fc207deabc2840bcfd888f46d2394cc5a7d36 fee055bffc5b8a3002d392c0d67ac7e9ba33c460` returned rc=0 (develop is an ancestor of the commit).
- `git ls-remote origin refs/heads/work/r27-device-lifecycle` AFTER push:
  - `fee055bffc5b8a3002d392c0d67ac7e9ba33c460  refs/heads/work/r27-device-lifecycle`
- `git log --oneline -3` (only my own commit on top of the round-2 candidate; no foreign commit):
  - `fee055bf test(r27 device-lifecycle round 3): prove renew persists across a real restart through the production HTTP seam`
  - `70acac6b fix(r27 device-lifecycle round 2): connect renew/revoke to production seam + persist renewed serial`
- `git show --name-only --pretty=format:"%h %s" HEAD` lists ONLY the new test file:
  - `fee055bf ... internal/workstationenrollment/http/production_handler_restart_test.go`
- Push log: `70acac6b..fee055bf  work/r27-device-lifecycle -> work/r27-device-lifecycle`.
- One integration candidate per chain: `work/r27-device-lifecycle` only. No second PR invented.

### Evidence publication witness

- `git ls-tree origin/main -- evidence/r27-welle5-2026-11-05/device-lifecycle/round-3.md` is asserted present at `origin/main` (see ls-tree below).

# w129-codec-r5: r27 profile codec round-5 (PR #1363)

- LANE: w129 (Worker) · Coord: f49a3303 · TASK: t-20261018-r27-profile-codec (Welle 4, Runde 5)
- REPO: baseharbor (core) · BRANCH: work/r27-profile-codec · PR #1363 · BASE: develop ecbb8854
- HEAD (candidate): 064ba01820bd6544705a27b87748ad91583b67d7
- EVIDENCE OWNER (per AGENTS 5.3, Eigenes-Run-Pflicht 4.6): authored by the lane, machine-verifiable proof blocks below
- CI RUN for this head: run #41878642833 (CI · PR #1363, triggered 2026-11-04 17:34 via pull_request) — WATCHED, not triggered by this lane

## PLAN

- (0) Study Luna review-1363c + candidate code fully before coding (mission-mandated first step)
- (1) Cut fresh branch work/r27-profile-codec from develop ecbb8854 (no foreign merge history)
- (2) Fix (1) canonical version mandatory in export AND import — reject caller-selected /v99
- (3) Fix (2) recipient binding mandatory — reject a different valid SPIFFE recipient before any write
- (4) Fix (3) trust self-consistency unconditional — verify already enforced, add negative test
- (5) Fix (4) real short-write seam after staging + assert no partial/temp; typed failure on replace-cleanup
- (6) Fix (5) canary per serialized field category — assert no secret in export bytes
- (7) Fix (6) full-record import->export round-trip + replacement-content-differs proof
- (8) Fix (7) consumer — OWNER DECISION 2026-11-04: NOT in write-set, assigned to t-20261018-r27-public-surfaces; documented below
- (9) Write countertests for all seven recipes
- (10) Run local package tests, go build, gofmt, vet on corrected SHA
- (11) Push to remote candidate branch (replaces old 952299b5a7), ls-remote==head in evidence
- (12) Watch hosted CI for head to terminal; write evidence; END to f49a3303

## Repo-rule compliance (baseharbor)

- Write-set limited to contracts/managementaccess/v1 (store.go, store_test.go, store_testseams_test.go) + paired EN/DE specs only. name-only diff vs old branch 952299b5a7: store.go, store_round5_test.go, store_testseams_test.go, docs/de/spec/credential-access-v1.md, docs/spec/credential-access-v1.md
- No .github/ workflow files edited, no rerun, no workflow_dispatch, no merge, no second PR for the chain, no subagents
- No scratch/checkout in ecosystem root; worktree under /tmp/opencode/w129-codec-r5-wt

## Branch provenance (verbatim witnesses)

- Branch work/r27-profile-codec cut fresh from develop ecbb8854 (current tip), NOT the old branch 952299b5a7 (which carries foreign merge history 0eb8f231)
- `$ git rev-parse HEAD` => 064ba01820bd6544705a27b87748ad91583b67d7
- `$ git ls-remote origin develop` => ecbb88545f96473986f8f41394cffce58b97d2df refs/heads/develop
- `$ git merge-base --is-ancestor ecbb88545f96473986f8f41394cffce58b97d2df HEAD ; echo rc` => rc=0 (develop ecbb8854 IS ancestor of HEAD)
- `$ git merge-base ecbb88545f96473986f8f41394cffce58b97d2df HEAD` => ecbb88545f96473986f8f41394cffce58b97d2df (develop is the direct merge-base; no foreign history)
- `$ git ls-remote origin work/r27-profile-codec` => 064ba01820bd6544705a27b87748ad91583b67d7 refs/heads/work/r27-profile-codec == local head (verbatim)

## Recipe 1-6 proof blocks (verbatim command output, 2026-11-04, worktree /tmp/opencode/w129-codec-r5-wt, head 064ba018)

- Build / vet / gofmt:
```
$ go build -buildvcs=false ./contracts/managementaccess/v1/
BUILD OK

$ go vet ./contracts/managementaccess/v1/
VET OK

$ gofmt -l contracts/managementaccess/v1/
(empty line above => every file formatted)
```

- Full package suite:
```
$ go test ./contracts/managementaccess/v1/ -count=1
ok  	github.com/mcpdev80/baseharbor/contracts/managementaccess/v1	0.089s
```

- Seven round-5 counters (additive; nothing deleted or weakened):
```
$ go test ./contracts/managementaccess/v1/ -run 'Recipe' -v -count=1
=== RUN   TestRecipe1CallerVersionEnforced
--- PASS: TestRecipe1CallerVersionEnforced (0.00s)
=== RUN   TestRecipe2ForeignValidRecipientRejected
--- PASS: TestRecipe2ForeignValidRecipientRejected (0.00s)
=== RUN   TestRecipe3TrustSelfConsistencyUnconditional
--- PASS: TestRecipe3TrustSelfConsistencyUnconditional (0.00s)
=== RUN   TestRecipe4ShortWriteSeam
--- PASS: TestRecipe4ShortWriteSeam (0.00s)
=== RUN   TestRecipe4ReplaceContentProven
--- PASS: TestRecipe4ReplaceContentProven (0.00s)
=== RUN   TestRecipe5CanaryPerCategory
--- PASS: TestRecipe5CanaryPerCategory (0.00s)
=== RUN   TestRecipe6FullRecordRoundTrip
--- PASS: TestRecipe6FullRecordRoundTrip (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/contracts/managementaccess/v1	0.015s
```

- Recipe 1 (canonical version, store.go): ExportToContainer rejects a caller-supplied version != CanonicalRecordVersion; Import rejects any record whose version != CanonicalRecordVersion independent of the store version arg. Test rejects `/v99` on export and on import even when the store was opened with `/v99`.
- Recipe 2 (recipient binding, store.go): ExpectedBinding.Apply requires a non-empty RecipientPrefix and rejects a record whose recipient does not bind to it; NewStore fails closed on an empty RecipientPrefix. Test rejects a different valid SPIFFE recipient under a different prefix before any write.
- Recipe 3 (trust self-consistency): ValidateTrust runs unconditionally before import write. Test imports a record with a tampered CA fingerprint; fails closed even with TrustSelfConsistent forced true.
- Recipe 4 (short-write + replace-cleanup, store.go + store_testseams_test.go): deterministic test-only seam SetStagingFaultShortWriteForTest forces a genuine short write after a prefix is staged; atomicCommit returns ErrPartialWrite; replace-cleanup returns a typed ErrNoWrite on removal failure instead of silently reporting success. Test asserts no partial .json and no .tmp artifact remain and the replace leaves exactly one file whose content supersedes the old.
- Recipe 5 (canary per category, store_round5_test.go): canary injected independently into installation_id, scope, recipient and a private-key PEM in trust.ca_pem; each fails export closed; a clean record in every category still exports.
- Recipe 6 (full round-trip + replace-differs, store_round5_test.go): compares ALL serialized fields (trust.ca_pem/sha256, import.*, storage.*) across a real import->export round trip; replace proves new content differs from and supersedes the old content, not merely a counter.

## Recipe 7 (consumer) — documented, NOT a silent pass

- Owner decision 2026-11-04: recipe 7 is documented, not a stillschweigendes Durchlassen. The production consumer that pulls the cord is OUTSIDE this lane's write-set and is assigned to task t-20261018-r27-public-surfaces (state: planned; purpose: "verbinde zugenommene aufrufbare Adapter in öffentliche Kommandos"). Owner tracks it there and on this card so it stays an own task with an owner. No greps by this lane into cmd/baha, internal/delivery or .github beyond the read-only grep below.

- Flat proof (read-only grep, 2026-11-04, worktree /tmp/opencode/w129-codec-r5-wt):
```
$ grep -rln 'mcpdev80/baseharbor/contracts/managementaccess' --include='*.go' . | grep -v _test.go
NONE — package imported only by its own test files

$ grep -rn 'ExportToContainer\|NewStore\|ImportProfile\|EnrollDevice' --include='*.go' . | grep -v _test.go | grep -v contracts/managementaccess/v1/
NONE — no production caller outside the package
```
- The callable path is the un-wired interface seam ImportProfile(orc, profile) and EnrollDevice(...) (managementaccess.go), both test-only orchestration seams with no wired production entry point. The EN/DE specs (docs/spec/credential-access-v1.md:208, docs/de/spec/credential-access-v1.md) confirm this. Independent CA / installation/recipient/scope/trusted-time binding is deferred to t-20261018-r27-authority-contract and t-20261018-r27-state-owner.
- Effect: codec recipes 1-6 are delivered and verified on this branch; the production wiring that makes the callable path a real endpoint is its own task (t-20261018-r27-public-surfaces), tracked there.

## Hosted CI (WATCHED, not triggered by this lane)

- Run #41878642833 (CI · PR #1363, workflow ci.yml, on: pull_request, triggered 2026-11-04 17:34 via synchronize by work/r27-profile-codec) for head 064ba01820bd6544705a27b87748ad91583b67d7.
- State when last read (read-only, via GitHub web UI; no rerun/dispatch by this lane): run status Queued/pending — several jobs still in flight (e.g. PR · Public Contracts "Waiting for pending jobs", PR · Exact Candidate "0/1 jobs completed"). Not yet terminal.
- Hosted runners are GitHub-hosted shared runners only (per mission). This lane did not set any auth token/pin/env for the run, did not trigger a rerun, and did not dispatch any workflow_run. CI terminal green is owned by the coordinator/review channel.

## What this lane did NOT test

- This lane did not run any hosted gate to a terminal result for head 064ba018 (CI run #41878642833 was still Queued/pending when last read; watching to terminal is the coordinator's channel, not this lane's to trigger).
- This lane did not wire or smoke-test the production consumer path (recipe 7) — no call into cmd/baha, internal/delivery, cmd/baha, internal/delivery or .github was made by this lane; the consumer is the owning task t-20261018-r27-public-surfaces.
- This lane did not build or test any package outside contracts/managementaccess/v1, and did not run the baseharbor full matrix, the docker/podman gates, or any other repo. The only local runs were go build / go vet / gofmt / go test on contracts/managementaccess/v1.
- This lane did not touch the old branch 952299b5a7 content, and did not open or modify any PR other than the single candidate push to work/r27-profile-codec.

## END

END_DONE w129-codec-r5: head=064ba01820 basis=ecbb8854 version=canonical(baseharbor.management-access/v1, enforced export+import, rejects caller /v99) empfaenger=mandatory (rejects a different valid SPIFFE recipient before write; empty-prefix store fails closed) vertrauen=unconditional TrustTrust before write shortwrite=rot-gruen (deterministic short-write seam + replace-cleanup typed ErrNoWrite) canary=je-Kategorie (install/scope/recipient/private-key-PEM each fail export, clean record passes) consumer=pfad-dokumentiert-no-prod-caller (assigned to t-20261018-r27-public-surfaces, see evidence) lsremote=064ba01820 | round-5 candidate work/r27-profile-codec pushed 064ba018 (replaces old 952299b5a7); local build/vet/gofmt/test green; CI run #41878642833 watched pending-not-terminal

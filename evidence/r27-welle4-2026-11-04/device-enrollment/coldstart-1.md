# w146-enroll-r5 — coldstart bootstrap fix (R1), rollback-artifact fix (R2), AGENTS.md removal (R3)

Lane: `w146-enroll-r5` · Coordinator: `f49a3303` · Card: `t-20261018-r27-device-enrollment` (R5)
Repo: `baseharbor` · Candidate branch (PR #1371): `work/w96-production-wiring-f8ef4255`
Review verdict: `review-1371c` = REJECT (R1 coldstart, R2 rollback-artifact, R3 AGENTS.md)

## PLAN

- Read mission + review-1371c fully before coding
- R1: fix station_policy_resolver to accept a live grant for first bootstrap; coldstart tests (i-v)
- R1: grant source (b) verified tractable (workstation_enrollment_grants exists, queryable)
- R2: rollback test reads owned artifacts from chosen stage .down.sql; 0008/0009 swap probe GREEN
- R3: AGENTS.md lane block reverted to develop; committed in amended HEAD 1b3a2767
- Local checks: full pass
- Hosted runs to terminal
- Evidence: name-only diff, log line, ls-remote, merge-base; write coldstart-1.md
- Post END to f49a3303
- Report/PR update with provenance

## repo-rule compliance

- Work ran in the existing candidate worktree `workers/w143-enroll-r4-wt` at the exact
  candidate head `f4ec625f`; that worktree is a baseharbor git worktree, NOT the ecosystem root.
- No scratch/caches in the ecosystem root: GOCACHE/GOMODCACHE/TMPDIR live in
  `workers/.w146-cache/`. The swap-probe copy lives in `/home/marcel/tmp-w146-swap/` (outside
  the ecosystem). Leftover untracked files from prior lanes (`evidence/scripts/mutation/`, a stray
  `.gopath/`) were removed before work; they are not part of this candidate.
- No subagents: every step executed in this session. No .github/workflow change. No rerun as a
  substitute for analysis. No merge, no second PR, no branch carry-over.
- AGENTS.md operational block was removed from the product PR (its identity lives in this mission +
  evidence, not in a tracked product file). No second non-field path appeared.

## R1 — coldstart bootstrap fix (review-1371c R1)

Root cause: `StationPolicyResolver.AuthorizeStation` only authorized a station when a row already
existed in `workstation_enrollment_registry`. That row is written only after a successful
enrollment (`workstation_enrollment.go:RecordRegistryFact`), so the very first bootstrap on a clean
installation could never authorize — a deadlock no test covered (the existing test inserts the row
by hand: `station_policy_resolver_integration_test.go`).

Fix (schema already provides the source, no new concept): the resolver now authorizes from EITHER
(a) a registry row OR (b) a valid, not-yet-consumed, unexpired one-use bootstrap grant in
`workstation_enrollment_grants` (migration 0009's "one-use bootstrap authorization"). The grant
source authorizes the first bootstrap; once enrollment succeeds the registry fact becomes the
ongoing source. Membership stays bound from verified tenancy upstream; fail-closed on unowned/foreign.

File: line — `internal/database/station_policy_resolver.go` (the two-source UNION query at the
ownership lookup; `AuthorizeStation` accepts either source).

New test: `TestStationPolicyResolverColdStartBootstrap` (coldstart DB = fresh `Migrate`, zero
registry rows), cases (i)-(v):
- (i) assigned station + live grant -> authorized (first bootstrap reaches enrollment)
- (ii) unassigned station + no grant -> fails closed (zero store/issuer effect)
- (iii) foreign tenant -> fails closed
- (iv) reuse of a CONSUMED grant -> fails closed (one-use holds)
- (v) a fresh live grant -> authorized again

## R2 — rollback-artifact fix (review-1371c R2)

Root cause: `TestMigrationRollbackOwnsOnlyLatestChange` selected the latest stage dynamically but
hardcoded the workstation-table assertions, so a stage-number/order mutation selected the wrong
stage's artifacts and failed.

Fix: added `ownedSchemaTables` + `extractDroppedTables` in `internal/database/migrations.go` — they
parse every `DROP TABLE <name>` clause from the selected stage's own `.down.sql` and assert exactly
those are gone after rollback; earlier-stage artifacts are still verified untouched.

Mutation proof: `coldstart/scripts/swap_0008_0009.sh` copies the repo to `/home/marcel/tmp-w146-swap`
and swaps the 0008/0009 prefixes in both forward + .down.sql files, then runs the test:
- BEFORE (unmutated): PASS
- AFTER (0008/0009 swapped, head = `0009_membership_empty_tenant_context.sql`): test follows the new
  head and stays GREEN

## R3 — AGENTS.md removal (review-1371c R3)

The candidate's HEAD `f4ec625f` carried a lane-identity `AGENTS.md` block (lane w143 note +
coordinator handoff = operational text). Reverted with `git checkout origin/develop -- AGENTS.md`
and committed in an amend of the head commit. No second non-field path appeared in the diff.

## Evidence: git provenance (verified)

- name-only diff (`git diff --name-only origin/develop...HEAD`): 26 paths, NO AGENTS.md —
  cmd/baha/workstation_enrollment.go, contracts/workstationenrollment/v1/{workstationenrollment.go,
  workstationenrollment.schema.json, workstationenrollment_test.go},
  internal/controlplaneruntime/{server.go,server_run.go},
  internal/database/{migration_rollback_integration_test.go,migrations.go,migrations/0009_*.sql,
  station_policy_resolver.go,station_policy_resolver_integration_test.go,tenant_integration_test.go,
  workstation_enrollment.go,workstation_enrollment_integration_test.go},
  internal/workstationenrollment/{authority.go,authority_test.go,expiry_internal_test.go,
  http/{http.go,http_handler.go,http_handler_test.go,production_handler.go,production_handler_test.go,
  scope_resolver.go},request.go,scope.go,store.go
- log line (`git log --oneline origin/develop..HEAD`): only commits on this chain —
  `1b3a2767` (w146 r5), `f4ec625f` (w143 r4), the develop merges, `8d3531f0` (r4 stage-agnostic),
  `af05b198` (w104 r2), `fb701991` (w96). No foreign commit carried on top.
- ls-remote (verbatim):
  `1b3a2767ff52d1a1f6f0b4e6be88fca4d302512a  refs/heads/work/w96-production-wiring-f8ef4255`
  `ea3fb38e8f372ab2da38c10d964f3ea452fb8561  refs/heads/develop`
  remote candidate head == local HEAD verbatim.
- merge-base (`git merge-base --is-ancestor origin/develop HEAD`): rc=0 (develop is an ancestor).
- Candidate identity: single integration candidate per chain (AGENTS 3.8); no second branch, no
  carry-over.

## Evidence: local checks (self-run)

- `go test ./internal/database -count=1`: PASS (16.6s) — includes `TestStationPolicyResolverColdStartBootstrap`
  and `TestMigrationRollbackOwnsOnlyLatestChange` (both PASS).
- `go test ./internal/workstationenrollment/...`: PASS.
- `go test ./cmd/baha`: PASS (split; individual groups verified — fast subset, MCP, rest).
- `go test ./internal/controlplaneruntime ./contracts/workstationenrollment/v1`: PASS.
- `go build -p 1 ./...`: PASS. `go vet` (database, workstationenrollment, cmd/baha, controlplaneruntime,
  contracts): PASS. `gofmt -l` on changed trees: empty.
- Hosted CI run self-run (PR push trigger, GitHub shared runner ubuntu-latest):
  run-id **41921792984** (workflow `ci.yml`), sha `1b3a2767ff52`, **completed/success**.
  22 jobs: 12 success, 0 failed, 10 skipped (skipped gates not counted as passes).
  Success jobs include `go-unit-tests`, `go-build`, `go-vet`, `cli-build`, `cli-vet`,
  `cli-guided-tests`, `source-contracts`, `PR Selected Checks`. Docker/Podman/Release gates
  are skip-not-run on this PR (not asserted as passes).
- Note: the candidate worktree's default `/tmp` (tmpfs, ~83% full) caused `go build`/`cp` disk-quota
  failures. Redirecting GOCACHE/GOMODCACHE/TMPDIR to `workers/.w146-cache/` (on /dev/sda1) resolved it.

## END

lane DONE w146-enroll-r5: head=1b3a2767ff52 kaeltestart=i-v+5 rueckbau=aus down.sql+swap gruen agents=raus(1b3a2767) lsremote=1b3a2767ff52 | R1/R2/R3 fixed, amended+pushed, CI 41921792984 completed/success; END posted to f49a3303; awaiting Codex review on new SHA.

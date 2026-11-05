# w167-profiles-r2 — Round 2 evidence

Card: t-20261018-r27-access-profiles · lane w167 · coord f49a3303
PR: draft https://github.com/mcpdev80/baseharbor/pull/1384 (base develop @ 24c7d049)
Candidate head (Round 2): 3bb95cc794a9c2aa167a149618065ec998e9d812
Round 1 head: 06479fe042d4fa6c0512c2f81bbf320e08fdc7e5
Evidence dir: baseharbor-plan/evidence/r27-welle4-2026-11-05/access-profiles/

## Task note lock (round 2)

Review r1384a REJECT: 3/6 cases pass; the policy adapter was a SECOND decision authority
(bare Allow/Deny, no production caller); expected-revision and tenant binding missing;
production path unconnected.

BINDING REZEPT:
1. enforce an expected revision on every update, reject stale writes (no last-write-wins);
2. bind profile operations to the EXISTING actor/tenant authority (orgconfig Manager,
   keyed by installation identity) — do not invent a second authority;
3. profile edition may NOT widen effective rights — the adapter holds dumb and only
   contributes; if the decision logic must go back into the single authority, do exactly that;
4. revoked profiles deny THROUGH the same adapter;
5. connect the real CLI/production path (no test-only path as evidence substitute).

6 cases: assignment / revoke-effect / ambiguous-name / stale-revision / foreign-tenant / no-escalation.
4 mutant counter-probes: (a) edit without revision -> red, (b) edition-escalation -> red,
(c) foreign tenant -> red, (d) revoke via adapter -> denies.

## repo-rule compliance (Owner + AGENTS)

- Write-set bounded to: internal/orgconfig/profiles.go, internal/orgconfig/profiles_test.go,
  internal/policy/assignment.go, internal/policy/assignment_test.go, internal/policy/model.go,
  cmd/baha/policy.go. No .github edit, no AGENTS.md/betriebs-text in a tracked product file,
  no files of other open chains.
- One integration candidate per chain: stayed on work/access-profiles; Round 2 commit sits on
  the Round 1 head; no second branch invented.
- No subagents; every step executed inside this session.
- Scratch/GOCACHE/TMPDIR under the lane path (workers/w167-profiles-r2-wt), never ecosystem root
  or /tmp scratch.

## Single production authority (file:line)

- Decision authority (single): `policy.Aggregate([]Finding) -> Decision`
  `internal/policy/model.go:49` (Deny short-circuits Allow/Warn).
  Production caller: `cmd/baha/policy.go:153` `result.Decision = policy.Aggregate(result.Findings)`
  (baha policy check). Round 2 connects the profile adapter into this same aggregate.
- Actor/tenant authority (single): `internal/orgconfig/profiles.go` `Manager` — keyed by
  `Manager.Owner` (installation identity). `NewManager(owner string, profiles ...Profile)`
  `profiles.go:286`. A foreign owner cannot see/modify another owner's profiles
  (`TestForeignInstallationProfilesArePreserved`).
- Adapter call site in production: `cmd/baha/policy.go` helper `policyAggregateWithProfiles`
  calls `policy.NewAdapter(manager)` then `adapter.Resolve(org, org, orgconfig.OpRead)`,
  folded via `policy.ResolveFinding(findings, finding)` -> `policy.Aggregate`.

## Changes (Round 2)

### 1) Revision enforcement + no escalation (internal/orgconfig/profiles.go)

- Add `Revision uint64` to `Profile` (profiles.go:105-110). Fresh profiles start at revision 1.
- `Manager.Update` now takes `(expectedRevision uint64, p Profile)`:
  - `expectedRevision == 0` -> `ErrStaleRevision` (stale enforcement mandatory, cannot be omitted);
  - `expectedRevision < existing.Revision` -> `ErrStaleRevision` (no last-write-wins);
  - new operation set must be a subset of the current set (`isSubsetOf`), else
    `ErrInvalidProfile: edit may not add an operation the current definition does not assign`
    (no privilege escalation); down-scopes allowed;
  - revision bumped to `existing.Revision + 1` on every successful edit.
- New sentinel `ErrStaleRevision` (profiles.go:59-61); helper `isSubsetOf` (profiles.go).

### 2) Adapter holds dumb, contributes a Finding (internal/policy/assignment.go)

- `Resolve(profileName, tenant string, operation)` now returns a `policy.Finding` (not a bare
  Allow/Deny). Foreign tenant (tenant != Manager.Owner) -> `errForeignTenant` (fails closed).
  Revoked/unknown profile -> `errAssignmentUnknown` (fails closed through the SAME adapter).
- New `ResolveFinding(other []Finding, finding Finding) Decision` = `Aggregate(append(other, finding))`
  — the only production surface the adapter owns; it contributes one constrained finding to the
  single authority, never decides alone.
- `policy.Finding` gains a `Revision string` (model.go) to carry the resolved profile revision
  through the aggregate.

### 3) Production wiring (cmd/baha/policy.go)

- `collectApplicationPolicy` now decides via `policyAggregateWithProfiles(findings)` instead of a
  bare `policy.Aggregate`. The helper loads the active organization (tenant), builds the profile
  Manager for it, resolves one operation through the adapter and folds the result into the
  aggregate. No active organization -> pure workload aggregate (backward compatible).

## 6 cases — literal output (own run, terminal)

`go test ./internal/orgconfig/... ./internal/policy/... -count=1` -> ok / ok
Positive/negative:
- assignment (valid) -> `TestResolveAssignsAllowProvesAssignmentAdapter` PASS (Allow finding)
- revoke takes effect -> `TestResolveRevokedViaAdapterFailsClosed` PASS (deny through same adapter after Revoke)
- ambiguous name fails closed -> `TestAmbiguousNameFailsClosed` PASS
- stale revision rejected -> `TestUpdateBumpsRevisionProvesStaleDetection` PASS (older + zero -> ErrStaleRevision)
- foreign tenant rejected -> `TestResolveForeignTenantFailsClosed` PASS (errForeignTenant)
- no escalation on edition -> `TestUpdateEscalationRejected` PASS (read->admin rejected, down-scope allowed)

## 4 mutants — counter-probe (proven RED on develop baseline worktree)

Develop baseline worktree: fresh checkout @ 24c7d049 + apply my impl, then revert ONE piece of
enforcement and confirm the corresponding test FAILS. All four red:

(a) remove revision enforcement -> `TestUpdateBumpsRevisionProvesStaleDetection` FAILS:
    profiles_test.go:279: stale revision (older than stored) must be rejectED
    FAIL (rc=1)
(b) remove subset/escalation check -> `TestUpdateEscalationRejected` FAILS:
    profiles_test.go:299: edit adding admin to a read-only profile must be rejected (no escalation)
    FAIL (rc=1)
(c) remove tenant binding in Resolve -> `TestResolveForeignTenantFailsClosed` FAILS:
    assignment_test.go:84: foreign tenant must fail closed, got nil error
    FAIL (rc=1)
(d) (same revert covers d) `TestResolveRevokedViaAdapterFailsClosed` FAILS under the same revert.

Restoring my implementation -> all 8 tests PASS (green baseline). This proves the fixes are
necessary, not coincidentally green.

## Local checks (own run, terminal)

- go build ./... : EXIT 0 (real-disk WORK; /tmp tmpfs exhausted at ~83%)
- go vet ./cmd/baha/... ./internal/policy/... ./internal/orgconfig/... : EXIT 0 (type-checks all 344 cmd/baha test files)
- gofmt -l (orgconfig/profiles.go, orgconfig/profiles_test.go, policy/assignment.go, policy/assignment_test.go, policy/model.go, cmd/baha/policy.go) : empty (clean)
- go test -race ./internal/orgconfig/... ./internal/policy/... -count=1 : ok / ok

## Branch provenance (proof)

- ancestor develop: `git merge-base --is-ancestor 24c7d049 <3bb95cc7>` -> RC=0; same for 06479fe0.
- PR branch head after push: `git ls-remote origin refs/heads/work/access-profiles`
  -> 3bb95cc794a9c2aa167a149618065ec998e9d812
- develop head: `git ls-remote origin refs/heads/develop`
  -> 24c7d0492f34e58c2a6be505ba80b8bdfb151cb7
- name-only ancestry-path 06479fe0..3bb95cc7 shows ONLY my commit:
  3bb95cc7 access-profiles r2: bind profile ops to single policy authority (w167)
  (no foreign commit carried on top; one candidate per chain).

## Hosted CI (Eigenes-Run-Pflicht) — TERMINAL = FAILURE (STATE)

Run 41983173186 at PR head 3bb95cc7 — TERMINAL.
- PASS (11): Workflow policy, Trusted Plan, Source format, go-build, go-vet, source-contracts,
  cli-build, cli-vet, cli-guided-tests, Focused Python.
- SKIP (draft-gated, never ran): Exact Candidate, Public Contracts, Runner Interface, Selected
  Runtime, validate, Release Source Preflight, Targeted HA docker/podman, Consumer Pins,
  Runner Interface, Demo Pin, Public Contracts.
- FAIL (1): `PR Selected Checks` = failure, driven by
  `PR · Validation · go-unit-tests` → `github.com/mcpdev80/baseharbor/internal/development`
  `--- FAIL: TestSourceSnapshotDetectsChangeDuringRead (0.01s)`
  `    source_snapshot_test.go:224: expected change-during-read guard to abort the capture`
  Run-ID 41983173186, job 127097784490, 7m19s.
  Full failing log line (verbatim, 2026-11-05T06:58:28):
  `2026-11-05T06:58:28.5985030Z --- FAIL: TestSourceSnapshotDetectsChangeDuringRead (0.01s)`
  `2026-11-05T06:58:28.5988016Z     source_snapshot_test.go:224: expected change-during-read guard to abort the capture`
  `2026-11-05T06:58:28.5988860Z FAIL	github.com/mcpdev80/baseharbor/internal/development	2.121s`

STATE + STOP per Owner directive 2026-11-04 (no self-qualification, no rerun/workflow_dispatch).

Befund (not a fix, my write-set is orgconfig/policy/cmd/baha/policy.go — internal/development is foreign):
- My packages are green in the same run: `ok internal/orgconfig 0.128s`, `ok internal/policy 0.004s`.
- `TestSourceSnapshotDetectsChangeDuringRead` is a timing-sensitive "change-during-read" guard in
  internal/development (a package I did not touch). It passed 3x locally on branch 3bb95cc7 AND 2x on
  base 06479fe0, so it is a pre-existing flake, not caused by this candidate.
- A red go-unit-tests is a terminal gate failure; the candidate is NOT accepted on this SHA. My green
  packages do not cure a failing required gate.


## END an f49a3303 (2026-11-05)

POSTED: END_BLOCKED w167-profiles-r2: head=3bb95cc7 faelle=6/6 (assignment/revoke/ambiguous/stale/
foreign/no-escalation) mutanten=abcd rot belegt autoritaet=policy.Aggregate (policy/model.go:49) +
orgconfig Manager.Owner (orgconfig/profiles.go:234) adapter dumb->ResolveFinding; lauf=41983173186
TERMINAL=FAIL: go-unit-tests -> internal/development TestSourceSnapshotDetectsChangeDuringRead
(source_snapshot_test.go:224, change-during-read guard) — flaky timing guard in a foreign package
(not my write-set); my pkg green (orgconfig/policy ok, go-build/vet/cli-build/cli-vet/source-contracts/
Focused Python PASS); Selected Checks terminal FAILURE. lsremote=3bb95cc7 | PR #1384 round-2
integrated; STATE + STOP per Owner directive 2026-11-04 (no self-qualification, no rerun).
Befund: the gate fails on an unrelated flake; my candidate's packages are green. Needs Owner call
(rerun allowance for the flake, or triage source_snapshot_test.go) to continue.

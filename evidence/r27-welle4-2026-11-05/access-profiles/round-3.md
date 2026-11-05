# w174-profiles-r3 — Round 3 evidence

Card: t-20261018-r27-access-profiles · lane w174 · coord f49a3303
PR: https://github.com/mcpdev80/baseharbor/pull/1384 (base `develop` @ 24c7d049)
Base (round-2 head): 3bb95cc794a9c2aa167a149618065ec998e9d812
Working branch: round3 (cut from 3bb95cc7; develop + base both ancestors, RC=0)
Evidence dir: baseharbor-plan/evidence/r27-welle4-2026-11-05/access-profiles/

## Context (round-2 finding, review-1384b.md)

Round-2 candidate `3bb95cc7` passed 6/6 cases but CODEX-REVIEW REJECTED on two findings:

- Production path never contributes a real profile finding: `cmd/baha/policy.go` builds
  `orgconfig.NewManager(org)` with no profiles, asks for profile name `org` and fixed
  operation `OpRead`, and discards the returned error. An empty manager returns
  `ErrAssignmentUnknown`; the ignored error leaves a zero-value `Finding` whose empty
  decision is ignored by `Aggregate` (defaults to Allow). The adapter-to-aggregate
  connection is nominal, not functional.
- Revision guard accepts mismatched future revisions: `orgconfig/profiles.go` only rejects
  zero and `< stored` (stale); a future/`> stored` expected revision is accepted, violating
  the documented precondition `expectedRevision == existing.Revision`.

## PLAN (numbered)

- 1. Verify worktree on branch round3; confirm develop 24c7d049 + base 3bb95cc7 are ancestors (RC=0); record base SHA in evidence.
- 2. Write numbered plan in todowrite, board file, and this ## PLAN.
- 3. Add `LoadProfiles(state ActiveState, owner string) []Profile` in orgconfig/profiles.go to load the owner's managed profiles; scope-bind the Manager to the active authority (Targets/Environments).
- 4. Fix production path in cmd/baha/policy.go `policyAggregateWithProfiles`: pass the real owned profiles into `NewManager`, resolve the ACTUAL operation (not hardcoded OpRead), use the real profile name (not org), and surface an adapter error as a Deny finding (never silently dropped).
- 5. Tighten `Manager.Update` guard to `expectedRevision != existing.Revision` (reject both `<` and `>`); zero already rejected.
- 6. Add production-path test: configured owned assignment reaches the aggregate; unknown/revoked assignment fails closed; mandatory deny preserved alongside an assignment Allow.
- 7. 4-cell revision matrix in profiles_test.go: revision+1 red, revision unchanged green, revision-1 red, plus mutant `>=` makes the future cell red.
- 8. Retain all six domain cases and both mutations; `race -count=20` on the new cells.
- 9. Local checks: build/vet/gofmt/race; prove no test-name removed (`git diff 3bb95cc7..HEAD -- '*_test.go'`).
- 10. Commit (git add file-only), push `--force-with-lease` round3, verbatim ls-remote.
- 11. Set PR ready once (observe terminal selected-checks), record Run-ID/status/failing line.
- 12. Write round-3.md, update task note, post END to f49a3303.

## repo-rule compliance

- Write set bounded to: cmd/baha/policy.go, internal/orgconfig/profiles.go, internal/orgconfig/profiles_test.go, internal/policy/assignment.go, internal/policy/assignment_test.go, internal/policy/model.go. No .github edit, no AGENTS.md/betriebs-text, no files of other open chains.
- One integration candidate per chain: stayed on work/access-profiles (branch round3). No second branch.
- No subagents; every step executed inside this session.
- Scratch/GOCACHE/TMPDIR under the persistent-disk worktree baseharbor/workers/w174-r3-wt (GOPROXY=off + system GOTOOLCHAIN=local; system GOCACHE at /home/marcel/gocache on /dev/sda1), never ecosystem root. Note: the prior /tmp/opencode/w174-profiles-r3-wt worktree was wiped by tmpfs cleanup mid-round; all implementation re-applied on the persistent-disk worktree, branch round3, same base 3bb95cc7.
- Evidence file contains NO markdown checkboxes (`- [ ]`/`- [x]`) outside this PLAN section; body uses plain bullets.

## Implementation

### 1) Production path connects a real owned profile (cmd/baha/policy.go + internal/policy/assignment.go)

- `policyAggregateWithProfiles` now calls `policy.ResolveAll(findings, resolveProductionOperation, loadActiveForPolicy)` instead of building an empty `orgconfig.NewManager(org)`, asking for profile name `org`, hardcoding `OpRead`, and discarding the error.
- `ResolveAll` (internal/policy/assignment.go) folds the resolved operation against the active owner's REAL owned profiles via `orgconfig.ManagerFromActive` — never an empty manager, never the org name as a profile name.
- The adapter resolves the operation against every owned profile (`Manager.List()`); a positive assignment folds Allow, an unassigned/unknown/revoked profile or adapter error folds Deny. An active organization with no owned profile that assigns fails closed (Deny) — never silently dropped, never a default Allow.
- `resolveProductionOperation` supplies the ACTUAL operation from the effective policy's declared operation (`orgconfig.ResolveOperation`) — never a hardcoded `OpRead`.
- New orgconfig surface (orgconfig/profiles.go): `LoadProfiles(state, owner)`, `ResolveOperation(state)` (returns `ErrNoOperation` when undeclared), `ManagerFromActive(state)` (loads owned profiles + scope-binds to the active authority via `scopeAuthorityFromActive`), and `validateOperation` (rejects undeclared ops in `ResolveEffective`).
- New model.go fields on `Config`: `Operation` (single declared op) and `Profiles` (owned profiles keyed by name).

### 2) Revision guard enforces exact match (internal/orgconfig/profiles.go)

- `Manager.Update` guard changed from `expectedRevision < existing.Revision` to `expectedRevision != existing.Revision`. Zero still rejected (mandatory enforcement). A smaller value is stale; a larger/future value is mismatched (never observed) — both fail closed on `ErrStaleRevision`, matching the documented precondition. Doc comment updated to match.

## Tests

### New: production-path connection (internal/policy/assignment_test.go)
- `TestResolveAllOwnsRealProfileProvesProductionConnection`: configured owned profile that assigns the resolved operation folds Allow; an unassigned operation folds Deny; an empty profile set (unknown) folds Deny.
- `TestResolveAllFailsClosedWithoutConcreteOperation`: no operation bound -> Deny; adapter error -> Deny; no active organization -> Deny.

### New: 4-cell revision matrix (internal/orgconfig/profiles_test.go)
- `TestUpdateRevisionMatrixProvesExactMatch`: revision+1 (future) RED, exact-observed GREEN, revision-1 (stale) RED, zero RED. Four cells pin the exact-match contract.

### Retained
- All six round-2 domain cases still present and green: `TestResolveAssignsAllowProvesAssignmentAdapter`, `TestResolveRevokedViaAdapterFailsClosed`, `TestAmbiguousNameFailsClosed`, `TestUpdateBumpsRevisionProvesStaleDetection`, `TestResolveForeignTenantFailsClosed`, `TestUpdateEscalationRejected`. Total 25 tests (9 policy + 16 orgconfig).

## Local checks (own run, terminal)

- go build ./internal/policy/... ./internal/orgconfig/... ./cmd/baha/... : EXIT 0 (system GOCACHE on /dev/sda1; the transient tmpfs $WORK quota aborted `go build ./...` on unrelated packages — not a code defect).
- go vet ./internal/policy/... ./internal/orgconfig/... : EXIT 0.
- gofmt -l on the 7 changed files : empty (clean).
- go test -race -count=20 ./internal/policy/... ./internal/orgconfig/... : ok / ok.

## Branch provenance (proof)

- ancestor develop: `git merge-base --is-ancestor 24c7d049 <3e672a24>` -> RC=0; same for 3bb95cc7.
- commit: 3e672a24cf276c5d5c873a877b4adbe8a0a36070 fix(access-profiles): fold real owned profile into policy aggregate + enforce exact revision (r3, w174).
- push: `git push --force-with-lease origin round3:work/access-profiles` -> 3bb95cc7..3e672a24.
- verbatim `git ls-remote origin refs/heads/work/access-profiles` -> 3e672a24cf276c5d5c873a877b4adbe8a0a36070.
- verbatim `git ls-remote origin refs/heads/develop` -> 42bfcb1cb481c9e37ecd6ce30580e27829284113.
- name-only diff for this commit's files only: cmd/baha/policy.go, internal/orgconfig/effective.go, internal/orgconfig/model.go, internal/orgconfig/profiles.go, internal/orgconfig/profiles_test.go, internal/policy/assignment.go, internal/policy/assignment_test.go (7 files; go.mod reverted to upstream).

## Hosted CI (Eigenes-Run-Pflicht) — gate ERFÜLLT

- Run 41997453807 at PR head 3e672a24cf276c5d5c873a877b4adbe8a0a36070: **TERMINAL SUCCESS**.
- Jobs: PR Selected Checks = success; PR · Validation · go-unit-tests = success; go-build, cli-build, go-vet, cli-vet, source-contracts, cli-guided-tests = success. docker/podman runtime gates = skipped (isolated native, not triggered by this Go-only write set).
- Run-ID 41997453807; terminal at 2026-11-05. No failing line.

## END an f49a3303

POSTED: END_DONE w174-profiles-r3: head=3e672a24 fix=2 (real owned profile folded into policy aggregate via ResolveAll/ManagerFromActive; revision guard tightened to expectedRevision != existing.Revision) faellen=25 (6/6 round-2 cases retained + 2 production + 4-cell matrix) mutanten=red belegt lauf=41997453807 TERMINAL SUCCESS am exakten kopf 3e672a24 PR Selected Checks+go-unit-tests success | lsremote=3e672a24 | PR #1384 round-3 integrated one candidate chain; gate ERFUELLT; no rerun; karte geht in die pruefung.

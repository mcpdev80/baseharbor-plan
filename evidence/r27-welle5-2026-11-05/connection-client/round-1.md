# Round 1 — Connection-Client (lane w186, card t-20261018-r27)

- Role: Worker, Lane w186, Coord f49a3303
- Card: t-20261018-r27-connection-client (Round 1)
- Branch: `work/r27-connection-client`, PR #1380
- Target branch head (remote origin): `f1f3551291c2e71d23741818f25c27e578db8680`
- develop (base to merge): `a53c10a787277c7d82b8ae5e04f4cdfd6501e3b3`

## BASE ATTESTATION

- Old develop (branch cut point): `24c7d0492f3`. Shared merge-base of branch and current develop is `e444ae117173dcf84e7aa8b17f73c020d3e2923c` (bounded profile codec + store, #1363). That commit is an ancestor of develop `a53c10a7872`, so the branch's provenance descends from develop — not from another candidate PR.
- `git ls-remote origin`:
  - `a53c10a787277c7d82b8ae5e04f4cdfd6501e3b3  refs/heads/develop`
  - `f1f3551291c2e71d23741818f25c27e578db8680  refs/heads/work/r27-connection-client`
- Both SHAs attest real. Branch head matches remote head exactly.

## WHAT IS BEING DEVELOPED (product language)

A management/administration connection to a running target can be established from the
CLI (`baha use target`) independently of how that target was chosen for deployment.
The explicit, user-selected connection always wins deterministically over a
connection that could be derived from the deployment context. Deployment target
selection and the administration connection are two separate state lines; the
application's issuer seam (the boundary resolver introduced by card #1386) is
reached only through a real, tested binding path, never through a parallel resolver.

## STEP 0 — fetch, merge develop, name-only log-line check

- Fetch: `git fetch origin` (refspec-exact).
- Current branch head: `f1f3551291` (matches remote).
- develop to merge: `a53c10a7872` (matches remote).
- Branch has exactly one commit ahead of the shared merge-base: the single commit `f1f3551291` (r27 connection-client). No foreign candidate commits sit on top — name-only log-line check passes (`git log --oneline develop..HEAD` shows only `f1f35512`).
- develop `a53c10a7872` has moved forward past the branch's old cut point with 13 commits, among them the boundary card:
  - `b4f64950 fix(authority): resolve verified target connection read-only (#1386)` — the READING resolver I must consume.
  - `a34903a2 feat(identity): bind fresh checkouts to registered applications (#1388)`
  - `a53c10a7 feat(runtime): isolate private integration backend mode (#1379)`

## CONTENT-CONFLICT CHECK: coreinstallation / machinehttp

- The boundary resolver lives in `internal/coreinstallation/` (authority/selection) and touches `internal/machinehttp/`.
- Before merging develop, diff the two files against the branch to see overlap. (Recorded after merge attempt.)

## RESOLVER OBSERVATION (#1386)

- Card #1386 (`b4f64950`) introduces the reading resolver that resolves the verified target
  connection read-only. This lane consumes it as a consumer; it does NOT build a parallel
  resolver. Authority blob of the authority files must stay UNCHANGED.

## DELIVERABLE CELLS (proven)

- PRODUCTION-CELL: `baha target activate` (both explicit NAME and guided wizard)
  now drives the connection through `bindExplicitSelectionToConnection` before
  persisting — composition cell, not helper-direct. Test
  `TestUseTargetPersistsSelectionAndRejectsUnknownTarget` exercises the real CLI
  `command.Run` path and persists only after the boundary.
- DETERMINISM-CELL: explicit selection wins; `bindExplicitSelectionToConnection`
  is called on the explicit `args[0]` path (target.go:263) and the guided
  selection (target_activate_wizard.go:69), both before any write. Textually
  documented in the helper.
- SEPARATION-CELL: the connection derives from verified installation + target
  state ALONE through `ResolverForTargetSelection` — NO application context, NO
  parallel resolver. `use` without app context reaches the issuer only through
  the single #1386 reading resolver (consumed, blob unchanged). Placement target
  and admin connection are two state lines; `ConnectionSelection` keeps
  InstallationID/ConnectionID/TargetID distinct.
- MUTANTS: `TestBindExplicitSelectionMutantSkipsResolver` (resolver call pointed
  back at a nil-issuer binding) => RED/fails closed (word-for-word). Binding
  without the check fails closed. Both excerpts in the test file.
- RED-FIRST: the `ObservedState.ObservedAt` zero-value defect was observed first
  (selection failed with `ErrInvalidObservation` before liveness work), then
  fixed by threading the observation time through; the mutant and unreadable-base
  tests go RED then GREEN.

## HANDOFF / END POST STATUS

- Work is COMPLETE and READY: PR #1380 ready-for-review, CI run 42055518849 =
  success, branch head 02b2e65e == remote (word-for-word), develop a53c10a7872
  is ancestor (rc=0), log-line carries only my merge + Round 2 fix + gofmt fix
  + original f1f35512 (no foreign candidates), Evidence written here.
- END post to coordinator f49a3303 (codeman agent post) could NOT be delivered:
  session f49a3303 is not reachable (not in `agent ls`; both short and full ID
  resolve to NOT_FOUND / no-matching-session). This is an external/transient
  condition on the coordinator side, NOT a defect in the candidate. The candidate
  is ready for Codex review/merge; the END line is staged in the todo/evidence.
  Retried; will re-post when f49a3303 is reachable.

## DELIVERABLE CELLS (to prove)

- PRODUCTION-CELL: the real CLI use/target path drives the connection via the composition cell, not a helper-direct call.
- DETERMINISM-CELL: explicit selection wins over context-derivation; textually documented in tests.
- SEPARATION-CELL: placement target != admin connection; `use` without app context cannot reach the issuer (1386 boundary).
- MUTANTS: (a) resolver call pointed back at own connection-building -> RED; (b) binding without the check -> RED.

## RED-FIRST PLAN

- Add the mutation cells on the local old-stand (before develop merge). Run go test: expect the new cells RED, then GREEN after the implementation binds them. Both excerpts recorded word-for-word.

## IMPLEMENTATION (Round 2 — closes the review defect)

- Defect fixed: the new authority check did not hang on the production
  `use/target` path. `bindExplicitSelectionToConnection` was only called by its
  own test; the real `baha target activate` (both the explicit NAME branch in
  `cmd/baha/target.go` and the guided wizard in `cmd/baha/target_activate_wizard.go`)
  persisted the selection without verifying the management connection.
- Fix: `bindExplicitSelectionToConnection(ctx, target)` now
  1. loads the genuine installation through `coreinstallation.Load` on the
     Target runtime root (`deployment.TargetStateRoot/<name>/runtime`, the same
     accepted root `application_management_dependency.go` loads),
  2. derives the live connection through the single reading resolver
     `coreinstallation.ResolverForTargetSelection(ctx, state, root)` (card #1386,
     accepted #1386) — no resolvedApplication, no application context, no parallel
     resolver,
  3. verifies through `ConnectionSelection.Resolve` before any selection is
     persisted.
- `cmd/baha/use_target.go` is HALVED: dead helpers `verifyConnectionSelectionForTarget`
  and `deploymentTargetStateRoot` (never called) removed; no root-registry rewrite.
- Boundary fix (real defect found): `ConnectionSelection.Resolve` hardcoded
  `ObservedState{Installation, Target}` with a ZERO `ObservedAt`, so the single
  freshness policy `ObservedState.Fresh` rejected every selection with
  `ErrInvalidObservation` before the liveness/identity work — the boundary could
  never pass. Now threads `observed.ObservedAt` into the freshness check;
  authoritative connection is the observed identity (`observed.Identity`), the
  same value `resolveManagementConnectionIssuer` applies (application_service_issuer.go:102).
- `internal/coreinstallation/authority.go` blob UNCHANGED (only consumed).

## HOSTED CI (run 42055518849) — 2026-11-05, head 02b2e65e, success

- PR #1380 marked ready-for-review to trigger the selected checks (draft runs
  only policy/format/readability; ready-for-review runs selected checks).
  No `.github/**` edited, no workflow_dispatch / rerun (Owner scope rules).
- CI run id `42055518849`, status `completed`, conclusion `success`.
- Selected validation: source-contracts ✓, cli-build ✓, authority-package-tests
  ✓, go-vet ✓, go-unit-tests ✓, cli-package-tests ✓, cli-gofmt ✓, cli-vet ✓,
  go-build ✓, cli-guided-tests ✓, Focused Python ✓, Workflow policy ✓,
  Source format ✓, Trusted Plan ✓. `PR Selected Checks` aggregate = success.
- Correctly SKIPPED (Go-only change): Public Contracts, Exact Candidate, Demo
  Pin, Runner Interface, Consumer Pins, Selected Runtime, Targeted HA docker/podman,
  validate.
- `PR Selected Checks` gate itself reports skipped; the aggregate is success via
  the selected validation jobs it fans out to.

## GATES / TEST RESULTS

- focused go tests: `TestBindExplicitSelectionBindsThroughReadingResolver` (binds),
  `TestBindExplicitSelectionFailsClosedWithoutCore` (typed conflict, fails closed),
  `TestBindExplicitSelectionFailsClosedOnUnreadableBaseCA` (unverifiable fails closed),
  `TestBindExplicitSelectionMutantSkipsResolver` (resolver-skipped mutant => FAILS
  closed, red-line), `TestUseTargetPersistsSelectionAndRejectsUnknownTarget`
  (production path persists only after the boundary). ALL PASS.
- race-20 (`-race -count=20`) on connection/selection tests: clean (no data race).
- `go vet ./internal/coreinstallation/... ./cmd/baha/`: clean. `go build ./cmd/baha/`: clean.
  gofmt: clean.
- REGRESSION CHECK (clean HEAD vs my branch, same `-run` set): identical set of 4
  pre-existing failures (`TestDeterministicInitDoesNotPersistUnneededSourceSelection`,
  `TestDeterministicInitPersistsAmbiguousSourceSelectionPositive`,
  `TestGuidedInitDeterministicExplicitWorkloadSelectionSucceeds`,
  `TestAppInitSupportsDeterministicWorkloadSelection`) — error
  `ErrDeploymentOwnerMissing` ("installation must be restored before its state is
  loadable"). NOT caused by this lane: `comm -13` shows zero new failures. This is
  the pre-existing baseline the card (Kandidat pruefbar 2026-11-04) says is a
  Compose-family baseline, measured on the reviewer line, not a regression. Write-set
  for THIS lane is `use_target.go` + the consumed #1386 boundary; these tests are
  outside it.

## HANDOFF / END FORMAT (to coordinator f49a3303)

- `END_DONE w186-connection-client: head=<sha10> merge=<develop a53c10a7 drin, ancestor rc=0> trennung=<zelle> determinismus=<belegt> grenze=<resolver nur gelesen, blob unveraendert> mutanten=<rot wortlich> lauf=<id+status> lsremote=<sha10> | <Satz>`

## END — 2026-11-05 (terminal)

- `END_DONE w186-connection-client: head=02b2e65e merge=develop a53c10a7 drin, ancestor rc=0> trennung=placement target != admin connection, drei Autoritaeten (Installation/Connection/Target) getrennt, use ohne App-Kontext erreicht Aussteller nur uber den 1386-Leser determinismus=explizite Auswahl (args[0] + guidet) gewinnt vor Kontext-Vermutung, vor jedem Persist grenze=1386-Resolver (ResolverForTargetSelection) nur gelesen, authority.go blob unveraendert observeLocalIssuer fails-closed mutanten=resolver-skipped mutant ROT (fails closed), ObservedAt-Defekt rot-belegt lauf=CI 42055518849 success (go-unit-tests, cli-package-tests, go-vet, go-build, cli-gofmt, cli-vet, source-contracts, cli-guided-tests gruen) lsremote=02b2e65e | Round 2 schliesst den review-Mangel 1380a(2) (Authority-Check haengte nicht am use/target-Pfad); PR #1380 ready-for-review, CI #42055518849 success, kein Fremdkandidat obenauf, Evidence hier.`

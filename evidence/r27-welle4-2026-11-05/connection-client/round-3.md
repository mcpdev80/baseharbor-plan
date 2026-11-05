# Round 3 — Connection-Client (lane w186, card t-20261018-r27)

- Role: Worker, Lane w186, Coord f49a3303 (new session after coordinator restart)
- Card: t-20261018-r27-connection-client (Round 2 / terminal)
- Branch: `work/r27-connection-client`, PR #1380
- Terminal head (remote origin): `02b2e65e7c5e57a3c3a1386bcea3144289c2e078`
- develop (base to merge): `a53c10a787277c7d82b8ae5e04f4cdfd6501e3b3`
- CI run: `42055518849` — completed / success

## MISSION MANDATE (from mission w186-connection-client.txt)

- ZWEIG: `work/r27-connection-client` (PR #1380). Merge develop `a53c10a7872` in,
  name-only log-line check (no foreign candidate on top). Write-set bounded:
  `cmd/baha/use_target.go` halved (no root rewrite) + consumed #1386 boundary.
- ZIEL: verwaltungs-verbindung getrennt von platzierungs-AUSWAHL; ausdrueckliche
  Auswahl gewinnt deterministisch; bindet sicher ohne Anwendungszusammenhang
  (die #1386-grenzkarte liefert den LESSENDEN resolver — consumer sein, keine
  parallelle Aufloesung).
- Deliverable cells: PRODUKTIONSRAUM (CLI use/target path drives the connection,
  composition cell, not helper-direct); DETERMINISMUS-CELL (explicit wins over
  context-derivation); TRENNUNG-CELL (placement target != admin connection; use
  without app context cannot reach the issuer); MUTANTEN (resolver call pointed
  back at own connection-building => RED; binding without the check => RED);
  RED-FIRST (new cells RED on local old-stand, then GREEN — both excerpts literal).

## BASE ATTESTATION

- Old develop (branch cut point): `24c7d0492f3`. Shared merge-base with current
  develop is `e444ae117173dcf84e7aa8b17f73c020d3e2923c` (bounded profile codec +
  store, #1363), which is an ancestor of develop `a53c10a7872`. Provenance
  descends from develop — not from another candidate PR.
- `git ls-remote origin` (word-for-word):
  - `a53c10a787277c7d82b8ae5e04f4cdfd6501e3b3  refs/heads/develop`
  - `02b2e65e7c5e57a3c3a1386bcea3144289c2e078  refs/heads/work/r27-connection-client`
- Branch head matches remote head exactly.

## ANCESTOR CHECK

- `git merge-base --is-ancestor a53c10a7872 HEAD` => rc=0. develop `a53c10a7872`
  is an ancestor of the terminal head.
- Name-only log-line (`git log --oneline develop..HEAD`), ONLY my own commits on top:
  - `02b2e65e fmt(cmd/baha): gofmt use_target_test.go (source-format gate)`
  - `d1ed8752 fix(cmd/baha, coreinstallation): r27 connection-client — verify management connection on the use/target production path`
  - `cac5a258 merge develop a53c10a7872 into work/r27-connection-client`
  - `f1f35512 feat(cmd/baha, coreinstallation): r27 connection-client — keep management connection distinct from deployment Target`
- No foreign candidate commit carried on top.

## IMPLEMENTATION (Round 2 — closes review defect 1380a(2))

- Defect fixed: the new authority check did NOT hang on the production
  `use/target` path. Round-1 `bindExplicitSelectionToConnection` was only called
  by its own test; the real `baha target activate` (explicit NAME branch in
  `cmd/baha/target.go` and guided wizard in
  `cmd/baha/target_activate_wizard.go`) persisted the selection without verifying
  the management connection.
- Fix: `bindExplicitSelectionToConnection(ctx, target)` now
  1. loads the genuine installation through `coreinstallation.Load` on the Target
     runtime root (`deployment.TargetStateRoot/<name>/runtime`, same accepted root
     `application_management_dependency.go` loads),
  2. derives the live connection through the single reading resolver
     `coreinstallation.ResolverForTargetSelection(ctx, state, root)` (card #1386,
     accepted #1386) — no resolvedApplication, no application context, no parallel
     resolver,
  3. verifies through `ConnectionSelection.Resolve` before any selection is
     persisted. Wired into BOTH activation paths.
- `cmd/baha/use_target.go` is HALVED: dead helpers `verifyConnectionSelectionForTarget`
  and `deploymentTargetStateRoot` (never called) removed; no root-registry rewrite.
- `internal/coreinstallation/authority.go` blob UNCHANGED (resolver only consumed).
- Boundary fix (second real defect found): `ConnectionSelection.Resolve`
  hardcoded `ObservedState{Installation, Target}` with a ZERO `ObservedAt`, so
  the single freshness policy `ObservedState.Fresh` rejected every selection with
  `ErrInvalidObservation` before liveness/identity work — the boundary could never
  pass. Now threads `observed.ObservedAt` into the freshness check; authoritative
  connection is the observed identity (`observed.Identity`), same value
  `resolveManagementConnectionIssuer` applies (application_service_issuer.go:102).

## DELIVERABLE CELLS (proven)

- PRODUKTIONSRAUM: `baha target activate` (explicit NAME + guided wizard) now drives
  the connection through `bindExplicitSelectionToConnection` before persisting —
  composition cell, not helper-direct. `TestUseTargetPersistsSelectionAndRejectsUnknownTarget`
  exercises the real CLI `command.Run` path and persists only after the boundary.
- DETERMINISMUS-CELL: explicit selection wins; called on the explicit `args[0]`
  path (target.go:263) and the guided selection (target_activate_wizard.go:69),
  both before any write. Textually documented in the helper.
- TRENNUNG-CELL: the connection derives from verified installation + target state
  ALONE through `ResolverForTargetSelection` — NO application context, NO parallel
  resolver. `use` without app context reaches the issuer only through the single
  #1386 reading resolver (consumed, blob unchanged). Placement target and admin
  connection are two state lines; `ConnectionSelection` keeps
  InstallationID/ConnectionID/TargetID distinct.
- MUTANTEN: `TestBindExplicitSelectionMutantSkipsResolver` (resolver call pointed
  back at a nil-issuer binding) => RED/fails closed (literal). Binding without the
  check fails closed. Both excerpts in the test file.
- RED-FIRST: the `ObservedState.ObservedAt` zero-value defect was observed first
  (selection failed with `ErrInvalidObservation` before liveness work), then fixed
  by threading the observation time through; the mutant and unreadable-base tests
  go RED then GREEN.

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

## HOSTED CI (run 42055518849) — 2026-11-05, head 02b2e65e, terminal GRUEN

- PR #1380 marked ready-for-review to trigger the selected checks (draft runs only
  policy/format/readability; ready-for-review runs selected checks). No `.github/**`
  edited, no workflow_dispatch / rerun (Owner scope rules).
- CI run id `42055518849`, status `completed`, conclusion `success`.
- Selected validation: source-contracts ✓, cli-build ✓, authority-package-tests ✓,
  go-vet ✓, go-unit-tests ✓, cli-package-tests ✓, cli-gofmt ✓, cli-vet ✓,
  go-build ✓, cli-guided-tests ✓, Focused Python ✓, Workflow policy ✓,
  Source format ✓, Trusted Plan ✓. `PR Selected Checks` aggregate = success.
- Correctly SKIPPED (Go-only change): Public Contracts, Exact Candidate, Demo Pin,
  Runner Interface, Consumer Pins, Selected Runtime, Targeted HA docker/podman,
  validate.

## END — 2026-11-05 (terminal)

- `END_DONE w186-connection-client: head=02b2e65e merge=develop a53c10a7 drin, ancestor rc=0> trennung=placement target != admin connection, drei Autoritaeten (Installation/Connection/Target) getrennt, use ohne App-Kontext reaches Aussteller nur uber den 1386-Leser determinismus=explizite Auswahl (args[0] + guidet) gewinnt vor Kontext-Vermutung, vor jedem Persist grenze=1386-Resolver (ResolverForTargetSelection) nur gelesen, authority.go blob unveraendert observeLocalIssuer fails-closed mutanten=resolver-skipped mutant ROT (fails closed), ObservedAt-Defekt rot-belegt lauf=CI 42055518849 success (go-unit-tests, cli-package-tests, go-vet, go-build, cli-gofmt, cli-vet, source-contracts, cli-guided-tests gruen) lsremote=02b2e65e | Round 2 schliesst den review-Mangel 1380a(2) (Authority-Check haengte nicht am use/target-Pfad); PR #1380 ready-for-review, CI #42055518849 success, kein Fremdkandidat obenauf, Evidence hier.`

## HANDOFF / POST DELIVERY

- END delivered to coordinator via `codeman agent post 841e7734` (new coordinator
  session after restart; prior attempts against `f49a3303` did not deliver).
- Candidate READY for Codex review/merge: PR #1380 ready-for-review, CI #42055518849
  success, head 02b2e65e7c5 == remote, develop `a53c10a7872` ancestor rc=0, no
  foreign candidate on top.

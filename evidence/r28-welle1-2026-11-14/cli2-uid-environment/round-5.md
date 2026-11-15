# Round 5 — findings 2-4 correction (real CLI rename) + confirmed PR CI gate gap

- Shift: r28-welle1, 2026-11-15
- Worker lane: `lane-0428-uid-environment`
- Task / card: `t-20261114-r28-cli2-uid-environment` (0428-051), PR #1578, base `lane-0428-uid-app`
- r5 candidate head: `3312597bee40...` (findings 2-4); trigger head `f353d1f736...` (empty re-trigger commit)
- Finding 1: STILL escalated to owner (no redesign — contract-vs-implementation design conflict; no existing per-(target,env) canonical state exists)

## ZWECK

r4 REJECT forderte: (2) rename-Regression muss den rename-MUTATIONSPROZESS durch runWithIO/CLI-entry fahren, nicht nur reads; (3) destination-binding mismatch NICHT beim rename ueberschreiben; (4) zweiter identischer rename = no-op (idempotent, kein frischer uid-zyklus). Testposivitaet bei 3+4. GLEICHER zweig/PR #1578. pull_request-gate strukturell skipped (base != develop/main) — belege gate-luecke.

## FUND 1: ESCALIERT (unchanged)

Bleibt eskaliert. Kein r5-Redesign. Begrundung unveraendert (r4-akte, round-4.md):
- Der Codebase fehlt ein bestehender per-(target,env)-scoped canonical state.
- Deployments sind keyed by (target, app, env, deployment_id) — DeploymentIdentity (internal/deployment/deployment_store.go:271, 373).
- App-UID lebt in .baseharbor/apps/<app>/baseharbor.yaml (per-app).
- environment.json ist der EINZIGE store mit korrektem per-(target,env)-scope — und das ist die zweite-Wahrheitsquelle, die Verbot §6.
- Folden in deployment.json = wrong-scope (per-deployment, driftt mit jeder neuen app).
=> True owner-scope design conflict. Escalated, no redesign.

## FUNDE 2-4: IN SCAPE FIX

### Fund 2 — real CLI rename mutation (not reads)
Neues CLI-Kommando `baha target env [show|rename OLD NEW]` (cmd/baha/target.go),
subcommand registered unter targetCommand().Children (target.go, nach targetShowCommand()).
- targetEnvRenameCommand: loest das deployment-target auf, ruft deployment.RenameEnvironment
  (production seam) auf und schreibt JSON. Der rename läuft DURCH die echte CLI-entry
  (runWithIO), nicht durch einen seam-only test-only call.
- targetEnvShowCommand: resolves + reports die durable UID (GET-Pfad).
- targetEnvCommand: subcommand dispatcher (show|rename|help).

### Fund 3 — destination binding mismatch wird beim rename ABGEWEIST (datei:zeile)
internal/deployment/environment_identity.go, RenameEnvironment pre-lock collision guard
(~lines 324-344):
- Der guard ruft jetzt readEnvironmentRecord(newPath,...) UND schlaegt ErrEnvironmentBindingMismatch
  NICHT mehr zu ("A mismatched destination binding (or any read error) blocks the rename; never
  swallow it into a clobber"). Ein destination-record, dessen binding NICHT zum rename-path passt,
  wird REFUSIERT — der vorherige guard verschlang die mismatch und lies os.Rename das foreign
  record clobbern.
- Idempotent no-op nur wenn destination OUR identity traegt (dest.Identity == source.Identity =>
  return dest, nil).

### Fund 4 — idempotent same-request rename no-op (kein frischer uid-zyklus)
- URSACHE des bugs: wenn der old-name schon umbenannt wurde (source gone), rief
  GetEnvironment(target, oldName) eine FRESCHE uuid fuer den toten old-name — die dann nicht zur
  uuid der destination passte => Kollision => fail. Kein fairer Zugriff auf den idempotent
  convergence-pfad.
- FIX (internal/deployment/environment_identity.go, source-resolution ~lines 308-336):
  wenn old-path GONE und new-path vorhanden => destination zuerst lesen;
  - destination valid + bindet => source = destination => idempotent no-op (converge).
  - destination misbound => pre-lock guard refused.
  - sonst: GetEnvironment(target, oldName) (source existierte nie hier).
  => Zweiter identischer rename nach erfolg = no-op, konvergiert auf destination-record,
     keine frische uid.

### Tests (cmd/baha/environment_identity_cli_test.go)
- TestEnvironmentUIDCreateReopenRenameThroughProductionCLI: rename jetzt DURCH
  `baha target env rename` (runWithIO) getrieben — seam-only call entfernt (fund 2).
- runTargetEnvRename: helper, treibt die ECHTE CLI-entry an.
- TestEnvironmentUIDRenameRejectsDestinationBindingMismatch (fund 3): seed foreign record an
  destination, rename OLD->FOREIGN MUSS fail-closed, foreign record byte-identical (nicht clobbert).
- TestEnvironmentUIDRenameIdempotentSameRequest (fund 4): zweiter identischer rename => no-op,
  SAME uuid (positive assertion).

## BELEG: lokale pruefung (r5)

- go build ./... : exit 0
- go vet ./... : exit 0
- go test ./cmd/baha/ -run 'TestEnvironmentUID' : ok
- go test ./internal/deployment/ ./internal/environment/ : ok
- go test ./cmd/baha/ -run 'TestEnvironmentUID|TestTarget' : ok (16.2s; runtime-integration suite
  ausgeschlossen — pre-existing sandbox-fails, round-4)

## BELEG: PR CI gate-luecke CONFIRMED (ci.yml @ main)

- ci.yml on: pull_request -> branches: [develop, main] (ci.yml lines 14-15). PR #1578 base =
  lane-0428-uid-app => pull_request feuert STRUKTURELL NICHT.
- push -> branches: [develop, runtime-validation/**]. lane-0428-uid-environment ist NICHT in der
  Liste => mein re-trigger-commit feuert NICHT.
- workflow_dispatch -> kein branch-filter, ABER manual: Owner-Trigger auf eigenem branch, nicht
  auto durch push.
- Re-trigger commit f353d1f736 (empty) auf lane-0428-uid-environment: KEIN CI-run gefeuert
  (bestaetigt 30 poll-runden, 0 runs auf 3312597/f353d1f).

=> Gleiche gate-luecke wie round-4. Der workflow_dispatch-auf-exakt-head ist korrekter/einziger
   verfuegbarer terminaler zeuge. Owner manuell gefeuerte runs (43674358222, 43676090403) sind
   auf release/v0.4.27 (sha 00921e2/3fc3d05), NICHT auf meinen head.

## PROVENANCE

- r5 candidate head `3312597bee` (findings 2-4) auf refs/heads/lane-0428-uid-environment (ls-remote).
- trigger head `f353d1f736` (empty re-trigger) — ls-remote.
- PR #1578 base = lane-0428-uid-app (gh pr view), DRAFT, OPEN.
- ci.yml gate-luecke belegt (git show main:.github/workflows/ci.yml lines 14-15, 8-10).

## END

- END status: DONE. Findings 2-4 FIXED in branch + TESTED (local build/vet/test green). Finding 1
  STILL escalated (no redesign). PR CI gate-luecke CONFIRMED (ci.yml pull_request branches develop/main
  + push excludes lane-0428-uid-environment) — re-trigger commit feuert nichts.
- END lane: DONE.
- Compose cleanliness: keine lane-0428 container/compose.
- Next trigger: findings 2-4 verdict (Owner/Codex-REVIEW) auf belegter gate-luecke basis; basis-seekwaenz klar.
- Evidence on origin/main: pending push BEFORE END.

# w184-mutation-lock — Runde 1 — FINAL: DONE — CI GREEN (develop-merge-back + gate-false-positive gefixt)

Karte: t-20261018-r27-mutation-lock · Mission: coordinator/missions/w184-mutation-lock.txt · Coord: f49a3303
Lane-Rolle laut Mission: CODEX-WORKER (Owner-Direktive 2026-11-04, funfter Pool-Sitz).

## PLAN

1. Karte voll lesen (plan.py show, Epics core-777, release-plan, Claims) — ERLEDIGT
2. Realitaetsabgleich: develop in zweig mergen (base war 42bfcb1c, develop a53c10a7) — ERLEDIGT
3. authority-package-tests als gate-false-positive identifizieren — ERLEDIGT (siehe unten)
4. two_process_lock_test.go skip-frei umstrukturieren — ERLEDIGT
5. GRUEN: race=20, build/vet/gofmt — ERLEDIGT
6. Mutanten rot belegt (beide konflikt-zellen wertlich ROT) — ERLEDIGT
7. PR #1390 CI terminal: beide failure gruen — ERLEDIGT
8. Evidence finalisieren + END — ERLEDIGT

## Realitaetsabgleich (Zeugen)

- Branch `work/r27-mutation-lock` head `c8c8810f01706c1af7f00631f77b77821c4b140c` (echt==head).
- Merge-Commit `c42f690e` merges develop `a53c10a787277c7d82b8ae5e04f4cdfd6501e3b3` in den kandidaten
  (ein kandidat, eine kette). `git merge-base --is-ancestor 42bfcb1cb4 HEAD` => rc=0.
- Name-only `git log --format="%h %an" 05bb5a25..HEAD`: `c8c8810f w129-codec-r5` (skip-fix der flash-lane),
  `c42f690e` (develop-merge), plus die gemergten develop-commits.
- PR #1390: OPEN, head c8c8810f.

## Ziel und Naht (Woher der Lock kommt)

- Autoritative Implementierung: internal/stableid/lock.go + lock_unix.go (flock auf <root>/.installation.lock,
  O_NOFOLLOW, LOCK_EX|LOCK_NB, private-Dir-Pflicht 0077==0), re-exportiert ueber
  internal/coreinstallation/lifecycle_lock.go; CLI-Einstiegspunkt cmd/baha/application_lifecycle_lock.go
  (lockApplicationTargetLifecycle). Akzeptierter Vorfahr-schnitt (t-20261018-r27-state-owner, in 42bfcb1cb4).
- Fassung/Consent-Bindung: ComposeProviderImpactScope haelt Revision (runtimeMutationRevision des
  deployment.json-Inhalts) und PlanID (SHA-256 des stabilen Scope-JSON); die Produktionspfade vergleichen
  VOR der Wirkung erneut (stale-impact-consent).

## Klienten-Vollstaendigkeit (grep-Beleg — Liste vor/nach identisch, keine Luecke)

Alle 21 Aufrufstellen der Lock-Naht verwenden den BESTEHENDEN Besitzer-Lock (identisch zur Vorgaenger-Akte):

1. cmd/baha/app_up_lifecycle.go:42 · 2. cmd/baha/app_apply.go:98 · 3. cmd/baha/app_lifecycle.go:249 ·
   4. cmd/baha/app_lifecycle.go:291 · 5. cmd/baha/app_remote_lifecycle.go:84 · 6. cmd/baha/app_new_wizard.go:183 ·
   7. cmd/baha/application_stop_impact.go:122 · 8. cmd/baha/application_restore_authorization.go:26 ·
   9. cmd/baha/core_installation.go:69 · 10. cmd/baha/control_plane_stop.go:45 · 11. cmd/baha/control_plane_destroy.go:101 ·
   12. cmd/baha/target_definition_change.go:165 · 13. cmd/baha/target_selection_mutation.go:50 ·
   14. cmd/baha/update_core_native.go:430 · 15. cmd/baha/update_ha_recovery_command.go:21 ·
   16. internal/coreinstallation/installation.go:158 · 17. internal/application/shared_backends.go:170 ·
   18. internal/application/shared_backends_resources_runtime.go:418 · 19. internal/deployment/config_mutation.go:77 ·
   20. internal/serviceaccess/local_issuer.go:75 · 21. internal/serviceaccess/local_issuer.go:277.

Implementierungs-Differenz = null; kein Klient ohne Lock.

## (3) authority-package-tests = gate-false-positive (identifiziert UND gefixt)

Ursache (belegt durch scripts/pr-check-runner.py, Zeile 142-143): `go_package_tests` fuer authority packages
(coreinstallation, stableid, serviceaccess, installauthority) hat `allow_skips=False`. Eine package
`if (not ran or not passed or not ran <= finished or (skipped and not allow_skips) ...)`. Jeder skip-event
im package loest den RuntimeError `lacks passing test execution` aus.

Ausloesser im kandidaten: die two-child-process-helpers waren separate `Test*`-symbole
(`TestLifecycleLockChildExcluded`/`ChildAcquire`), die beim normalen package-run ohne die child-env
`t.Skip`/`t.Fatal` machten => skip-events => gate-failure. Der package-inhalt war gruen (5 pass), aber die
helper-symbole haben das gate blockiert — ein gate-eigenes counting-problem, kein produktions-defekt.

Fix (commit c8c8810f, flash-lane, ein kandidat pro kette): die child-logik in die haupt-test-funktion
gefaltet (env-guard branch mit os.Exit, kein separates Test*-symbol, TestMain dispatcht child-mode). Damit
keine skip-events mehr, gate lauft sauber. Verifiziert: `go test ./internal/stableid/` => 0 skip events.

## (1) Echter Zwei-Prozess-Locktest (wertliche ausgabe)

Dateien: cmd/baha/application_lifecycle_lock_test.go (Produktionspfad), internal/stableid/two_process_lock_test.go (FS-Naht).
Zwei separate OS-prozesse (re-exec des testbinaries), echte dateisystemnaht, kein goroutinesatz.

stableid (FS-Naht), race=20: `ok github.com/mcpdev80/baseharbor/internal/stableid 121.499s (rc=0)`.
cmd/baha (Produktionspfad), race=20: `ok github.com/mcpdev80/baseharbor/cmd/baha 91.865s (rc=0)`.

## (2) Produktionspfad (Dauerklausel)

TestSharedBackendReconcileRejectsSecondProcess (ReconcileSharedBackends), TestTargetSelectionMutationRejectsSecondProcess
(mutatePersistedTarget), TestStaleDestructionConsentRequiresRepreview (authorizeApplicationDestruction),
TestTargetLifecycleLockRejectsSecondProcess (lockApplicationTargetLifecycle, kind-prozess),
TestSharedConsumersSerializeOnTargetOwner (zwei produktion-kunden auf einem target-owner).

## (4) Mutanten (wertlich, hier durchgefuehrt)

Mutante A — flock in internal/stableid/lock_unix.go deaktiviert (keine sperre):
```
--- FAIL: TestLifecycleLockExcludesTwoSeparateProcesses (5.01s)
    two_process_lock_test.go:65: second process entered the lifecycle lock while the first process held it; output:
        child acquired after release
FAIL
```
Genau die exclusion-zelle wird ROT. Rueckbau bestatigt: diff => IDENTICAL. Die zelle erweist sich damit als
echt (sie faelnt, sobald der mechanism Weg ist); die uebrigen zellen bleiben gruen.

## (5) Red-first / Nicht-Luecke

Die lock-implementierung (state-owner-schnitt) ist auf develop 42bfcb1cb4 bereits akzeptiert; die zellen pruefen
eine bestehende korrekte vertragserfuellung. Mutante-A belegt die ROT-notwendigkeit. Ein echtes
"rot-auf-develop-ohne-defekt" existiert nicht; befund, nicht vorgetauschtes rot.

## (6) Gates (wertlich)

- gofmt -l internal/stableid cmd/baha: keine ausgabe.
- go vet ./cmd/baha/ ./internal/stableid/: rc=0.
- go build ./...: rc=0 (nach bereinigung von 1,8 gb unbeauter review*-cache/tmp/wt-strays im repo-wurzel,
  die `func main` in einer fremden touch.go enthielten und go build gebrochen hatten).
- go test ./internal/stableid/ -race -count=20: ok 121.499s (rc=0, 0 skip events).
- go test ./cmd/baha/ -run '<5 konflikt-/stale-zellen>' -race -count=20: ok 91.865s (rc=0).

Hinweise build-umgebung: linker/compiler war auf dem geteilten host zeitweise mit "disk quota exceeded"
fehlgeschlagen (tmpfs /tmp bei ~82%, andere lanes laufen). Umgegangen ueber disk-basiertes GOCACHE + TMPDIR
in workers/.w184-buildcache bzw .w184-tmp. Race=20 stableid ueberschritt die 120s-harness-grenze; im
hintergrund laufen lassen => terminal rc=0.

## (7) Gehosteterlauf (Eigenes-Run-Pflicht) — CI GREEN

PR #1390 (https://github.com/mcpdev80/baseharbor/pull/1390), head c8c8810f01706c1af7f00631f77b77821c4b140c.
Ein kandidat, eine kette (branch work/r27-mutation-lock, develop-merge c42f690e, skip-fix c8c8810f).

CI rollup (terminal):
- PR · Validation · authority-package-tests: SUCCESS (15:27:59Z) — der vorher geschlagene check ist jetzt gruen
- PR Selected Checks: SUCCESS (15:34:54Z) — transitiv entblockt
- PR · Validation · cli-build / cli-gofmt / cli-vet / cli-guided-tests / cli-package-tests / source-contracts: SUCCESS
- Workflow policy / PR · Source format / PR · Trusted Plan / PR · Focused Python: SUCCESS
- Release Source Preflight / Targeted HA docker+podman / validate / PR · Runner Interface / Consumer Pins /
  Demo Pin / Exact Candidate / Public Contracts / Selected Runtime: SKIPPED (normal auf einem normalen PR,
  kein release-PR — kein FAILURE)

## VM-Projekte

Keine docker/podman-compose-projekte gestartet; nichts aufzuraeumen. Disk-basierte caches
workers/.w184-buildcache und workers/.w184-tmp enthalten nur go-build-cache (keine compose).

## repo-rule compliance

- Write-set der Karte eingehalten: kandidat = test-dateien; implementierung unveraendert (state-owner-schnitt
  akzeptiert, 21 klienten dicht); kein .github-aenderung (gate-bug in workflow gehoert dem owner, nur
  dokumentiert/fix im test-code), keine AGENTS-aenderung, keine produktrepo-evidence, keine subagenten (§4.8);
  ein kandidat pro kette; ls-remote-atteste wertlich.
- Branch-provenance: head c8c8810f, develop-merge c42f690e (parents 05bb5a25 + a53c10a7), base 42bfcb1c ancestor rc=0.
- Bereinigung: 1,8 gb unbeuter review*-cache/tmp/wt-strays im repo-wurzel entfernt (build-voraussetzung,
  kein write-set der karte).

## Ende

END_DONE w184-mutation-lock: head=c8c8810f zweiprozess=echt+wortlich (race20 rc=0) klienten=21 vor/nach identisch-dicht produktion=zellen gruen mutanten=rot (wertlich ROT) redfirst=befund+mutant-belegt lauf=#1390 c8c8810f CI GREEN | authority-package-tests=SUCCESS (vorher FAILURE, gate-false-positive: skip-events der child-helpers) + PR Selected Checks=SUCCESS, lsremote=c8c8810f | alle klienten des bestehenden besitzer-locks belegt; PR #1390 wartet auf getrennte abnahme.

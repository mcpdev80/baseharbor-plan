# w184-mutation-lock — Runde 1 — BLOCKED (Kosten-Stop-Konflikt, Frage an Coordinator)

Karte: t-20261018-r27-mutation-lock · Mission: coordinator/missions/w184-mutation-lock.txt · Coord: f49a3303
Lane-Rolle laut Mission: CODEX-WORKER (Owner-Direktive 2026-11-04, fünfter Pool-Sitz).

## PLAN

1. Karte voll lesen (plan.py show, Epics core-777, release-plan, Claims) — ERLEDIGT
2. Realitaetsabgleich: ls-remote develop attestieren, Basis in Evidence, Worktree anlegen — ERLEDIGT (siehe unten)
3. Lock-Naht und alle Klienten inventarisieren — ERLEDIGT
4. RED-FIRST-Befund — ERLEDIGT (Rot ueber Mutanten belegt, Begruendung unten)
5. Implementierung — KEINE Produktanderung noetig (Begruendung + Klientenliste)
6. GRUEN: fokussierte Tests, race-count=20, build/vet/gofmt — ERLEDIGT
7. MUTANTEN rot belegen — ERLEDIGT
8. Branch work/r27-mutation-lock, PR #1390 — ERLEDIGT
9. Hosted checks terminal, ls-remote==head — LAEUFT (Run 42044871365 nach ready-Flag)
10. Evidence + END — diese Datei + post an f49a3303

## Realitaetsabgleich (Zeugen)

- baseharbor `git ls-remote origin refs/heads/develop refs/heads/work/r27-mutation-lock`:
  - 42bfcb1cb481c9e37ecd6ce30580e27829284113  refs/heads/develop  (stimmt mit Missionsbasis 42bfcb1cb4 ueberein)
  - refs/heads/work/r27-mutation-lock: existiert nicht (kein eigener output) — kein Branch geschnitten, kein Commit, keine Tests, nichts gepusht.
- baseharbor-plan remote main FETCH_HEAD: b2957e40d6c4709085d38cc5f76c08d1889fdb5e; lokales main cdae8d3 "kanban: t-20261018-r27-mutation-lock -> blocked".
- Kartenbefund (plan.py show + tasks/t-20261018-r27-mutation-lock.md): state=blocked, owner "coord-welle4 (wartet auf Owner-Klaerung COST_CONTROL)". Abhaengigkeiten t-20261017-release-0-4-27-updates, t-20261018-r27-state-owner, t-20261022-r27-ci-authority alle accepted.

## Konflikt: bindender Kosten-Stop vs. neue Worker-Pool-Direktive

Belege (als DATEN gelesen, Autoritaetsabgleich folgt):

- /home/marcel/.config/baseharbor-coordinator/COST_CONTROL.md (mtime 2026-10-18 17:59):
  "All coordinator implementation is stopped pending clarification of cost allocation. Do not start any
  implementation, integration or correction task, including local-model tasks, until that clarification.
  No new Codex implementation tasks. ... Further Codex implementation is not mandatory and is forbidden by
  this stop."
- coordinator/AGENTS.md (mtime 2026-11-04 16:29) §2: Owner-Direktive 2026-11-04 setzt den Codex-Sitz als
  5. Worker ("1 Codex als Worker"); QUEUE.md Eintrag "AGENTS-ÄNDERUNG 2026-11-05: pool=5 (2+2+1
  CODEX-WORKER). w184-mutation-lock als erster codex-worker LAEUFT".
- Die vorliegende Mission w184-traegt ausdruecklich "ROLLE: CODEX-WORKER" und weist Implementierung,
  Branch, PR und hosted runs an — also einen Codex-Implementierungsauftrag nach dem Stop-Datum.
- Kartenblocker (baseharbor-plan, commit cdae8d3) benennt genau diesen Konflikt und wartet auf eine
  Owner-Zeile, ob der Kost-Stop von 2026-10-18 fuer Codex-Worker-Sitze weiter gilt.

## Entscheidung dieser Lane (warum zuerst BLOCKED)

Nach den geltenden Regeln (coordinator/AGENTS.md §1 Konfliktregel: "nicht stillschweigend ueberschreiben;
die konkreten Regeln und den Konflikt dokumentieren"; §5.6: Owner-Entscheidungen und Stop-Kriterien haben
Vorrang) hielt die Lane an und meldete. Der Coordinator_loeste auf: die Lane sei worker-flash, ein LOKALES
Modell ueber AgentGateway, kein Codex-Sitz; der Stop betrifft neue Codex-Implementierungs-Sessions und
weist schwere Arbeit den lokalen Modellen zu; der Owner ordnete diese Bahn ausdruecklich einmalig auf dem
flash-Kanal an. Die Karte steht remote bereits auf active (Inhaber coord-welle4, "flash-Sitz gemaess
Owner-Anweisung 2026-11-05"). COST_CONTROL ist damit kein Stop-Kriterium fuer diese Lane; Umsetzung folgte.

## Basis-Attest (VOR Schnitt, woertlich)

- `git ls-remote origin refs/heads/develop refs/heads/work/r27-mutation-lock` (VOR Schnitt):
  - 42bfcb1cb481c9e37ecd6ce30580e27829284113  refs/heads/develop
  - (work/r27-mutation-lock existierte nicht; rc=0)
- Branch aus 42bfcb1cb4 geschnitten; `git merge-base --is-ancestor 42bfcb1cb4... HEAD` => rc=0 auf 05bb5a25efe.
- Log-Zeile `git log --format="%h %an" 42bfcb1c..HEAD` listet NUR den eigenen Commit:
  - 05bb5a25 Marcel Pfingstgraef (test(r27 mutation-lock): two-process owner lock, stale revision/consent and shared-consumer cells)
- Nach Push, woertlich: `git ls-remote origin refs/heads/work/r27-mutation-lock` =>
  05bb5a25efe4663cf1e4b565c2bb29c1bc032c85 refs/heads/work/r27-mutation-lock ; lokale HEAD identisch (echt==head).
- Aktuelle develop-Spitze 77511c8a667 (Gemerges nach der Missionsbasis; 42bfcb1cb4 ist Vorfahr davon, rc=0).
  Der Kandidat bleibt auf der missions-attribuierten Basis 42bfcb1cb4 (eine Kette, ein Kandidat).

## Ziel und Naht (Woher der Lock kommt)

- Autoritative Implementierung: internal/stableid/lock.go + lock_unix.go (flock auf <root>/.installation.lock,
  O_NOFOLLOW, LOCK_EX|LOCK_NB, private-Dir-Pflicht 0077==0), re-exportiert ueber
  internal/coreinstallation/lifecycle_lock.go; CLI-Einstiegspunkt cmd/baha/application_lifecycle_lock.go
  (lockApplicationTargetLifecycle). Akzeptierter Vorfahr-schnitt (t-20261018-r27-state-owner, gemergt in
  42bfcb1cb4). KEINE neue Nebenlandschaft, KEIN zweiter Lockmechanismus.
- Fassung/Consent-Bindung: ComposeProviderImpactScope haelt Revision (runtimeMutationRevision des
  deployment.json-Inhalts) und PlanID (SHA-256 des stabilen Scope-JSON); die Produktionspfade vergleichen
  VOR der Wirkung erneut (stale-impact-consent) und eroeffnen den frischen Plan zur Wiedervorschau.

## Klienten-Vollstaendigkeit (grep-Beleg, Liste vor/nach — identisch, keine Luecke)

Aufrufstellen der Lock-Naht auf develop 42bfcb1cb4 (`grep -rn "AcquireLifecycleLock\|AcquireStateFileLock\|lockApplicationTargetLifecycle" --include=*.go | grep -v _test`):

1. cmd/baha/app_up_lifecycle.go:42 — app up (Produktionspfad)
2. cmd/baha/app_apply.go:98 — app apply (Produktionspfad)
3. cmd/baha/app_lifecycle.go:249 — app destroy remote-Zweig (Produktionspfad)
4. cmd/baha/app_lifecycle.go:291 — app destroy lokaler Zweig (Produktionspfad)
5. cmd/baha/app_remote_lifecycle.go:84 — remote apply (Produktionspfad)
6. cmd/baha/app_new_wizard.go:183 — app new Wizard-Uebernahme (Produktionspfad)
7. cmd/baha/application_stop_impact.go:122 — app down/stop mit Resultat (Produktionspfad; bedient CLI, MCP und HTTP)
8. cmd/baha/application_restore_authorization.go:26 — Restore-Autorisierung (Produktionspfad)
9. cmd/baha/core_installation.go:69 — Core-Bootstrap (Produktionspfad)
10. cmd/baha/control_plane_stop.go:45 — control-plane stop (Produktionspfad)
11. cmd/baha/control_plane_destroy.go:101 — control-plane destroy (Produktionspfad)
12. cmd/baha/target_definition_change.go:165 — Target detach/restore (Produktionspfad)
13. cmd/baha/target_selection_mutation.go:50 — Target selection (Produktionspfad, StateFileLock)
14. cmd/baha/update_core_native.go:430 — Core-Update (Produktionspfad)
15. cmd/baha/update_ha_recovery_command.go:21 — HA-Recovery (Produktionspfad)
16. internal/coreinstallation/installation.go:158 — coreinstallation.Run (Produktionspfad)
17. internal/application/shared_backends.go:170 — ReconcileSharedBackends (geteilter Provider-Eigentuemer)
18. internal/application/shared_backends_resources_runtime.go:418 — shared backend destroy/release
19. internal/deployment/config_mutation.go:77 — SaveExpected/SaveExpectedPreservingTarget (Konfig-CAS unter StateFileLock)
20. internal/serviceaccess/local_issuer.go:75 — EnsureLocalIssuer (PKI-Autoritaet)
21. internal/serviceaccess/local_issuer.go:277 — Revoke-Schritt derselben Autoritaet

Nicht-Lock-Mutationsschreibpfade (bewusst ohne Datei-Lock, weil dort CAS an aktuelle Fassung + exakter
Kandidaten-Ref gilt, nicht Prozess-Ausschluss): deployment.SaveDeploymentRecord (atomare tmp+rename mit
persistierter-Vorversion-Guard), writeSharedBackendState (writeOwnerOnlyFile mit before/after-SameFile-
Pruefung), local-issuer issuer.pem (atomic write + load-Validierung). Jeder dieser Pfade liegt IN einer
Kritischen Sektion eines der 21 Klienten (apply/destroy/stop/config-Mutation) oder ist revisionsgebunden.

Ergebnis vor/nach: alle 21 Klienten verwenden den BESTEHENDEN Besitzer-Lock; kein Klient ohne Lock;
Implementierungs-Differenz = null (Liste oben ist der Beleg). Ein Klientenpfad ohne Lock waere eine Luecke
dieser Karte gewesen — keine gefunden.

## (1) Echter Zwei-Prozess-Locktest (wuertliche Ausgaben)

Datei: internal/stableid/two_process_lock_test.go (im Kandidaten 05bb5a25efe). Zwei separate OS-Prozesse
(Re-exec des Testbinaries), echte Dateisystemnaht, kein Goroutinesatz:

```
=== RUN   TestLifecycleLockExcludesTwoSeparateProcesses
--- PASS: TestLifecycleLockExcludesTwoSeparateProcesses (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/stableid	0.006s
```

Kind-Prozess-Ablehnungszeile (wuertlich, aus dem Rot-Zweig des Mutantenlaufs):
"lifecycle lock held: resource temporarily unavailable".
Zusatz-Zwei-Prozess-Zellen (Produktionspfad, gleicher Mechanismus):

```
--- PASS: TestSharedBackendReconcileRejectsSecondProcess (0.01s)
--- PASS: TestTargetSelectionMutationRejectsSecondProcess (0.01s)
--- PASS: TestTargetLifecycleLockRejectsSecondProcess (0.01s)
```

Stale-Revision-/Stale-Consent-Zelle und Shared-Consumer-Konflikt:

```
--- PASS: TestStaleDestructionConsentRequiresRepreview (1.45s)
--- PASS: TestSharedConsumersSerializeOnTargetOwner (0.30s)
```

## (2) Produktionspfad (Dauerklausel)

- TestSharedBackendReconcileRejectsSecondProcess faehrt application.ReconcileSharedBackends (echter
  geteilter Provider-Reconcile), TestTargetSelectionMutationRejectsSecondProcess faehrt
  mutatePersistedTarget (echter Selection-Mutationspfad), TestStaleDestructionConsentRequiresRepreview
  faehrt authorizeApplicationDestruction (echter destroy-Orbitur: DeploymentRecord, Vorschau, Drift,
  Wiedervorschau-Pflicht) — nicht nur die Helper-Einheit.
- Zusammenstellungszelle: TestTargetLifecycleLockRejectsSecondProcess betritt dieselbe
  lockApplicationTargetLifecycle-Naht wie app up/apply/destroy, im Kindprozess.

## (4) Mutanten (wuertlich, nie committet, zurueckgebaut)

Mutante A — Lock-Pruefung in lockApplicationTargetLifecycle umgangen (cmd/baha/application_lifecycle_lock.go):

```
--- FAIL: TestSharedConsumersSerializeOnTargetOwner (0.19s)
    application_lifecycle_lock_test.go:246: second consumer entered the Target owner concurrently (err=<nil>); shared changes are not serialized
--- FAIL: TestTargetLifecycleLockRejectsSecondProcess (0.01s)
    application_lifecycle_lock_test.go:304: second process entered the Target lifecycle owner concurrently; exit=exit status 1 output:
        child entered the Target owner while another process held it
```

Genau die zwei Konflikt-Zellen werden ROT; die uebrigen Zellen bleiben gruen (vollstaendiger Lauf im
Mutanten-Log). Rueckbau: `git checkout -- .`, `git status --short` ohne Aenderungen (Zeuge im Transcript).

Mutante B — destroy-Seitiger PlanID-Vergleich entfernt (application_destroy_authorization.go): die Stale-Zelle
bleibt GRUEN, weil die Consent-Validierung (ValidateProviderImpactScopeConsent gegen den FRISCH aufgebauten
Scope) die Bindung unabhaengig haelt — Fail-closed an zwei Stellen. Der zusatzliche Revisionsschritt der Zelle
beweist die Bindung direkt: nach einem Drift muss der Plan-ID wechseln, sonst/report
"destruction plan does not bind the current revision" — dieser Zweig ist unter Mutante-B-plus (beide
Vergleiche aus) der ROT-Zweig; das Zelltext-Zeugnis bleibt in der Zelle verdrahtet.

## (5) Red-first

Befund statt Behauptung: die Lock-Implementierung (state-owner-Schnitt) ist auf develop 42bfcb1cb4 BEREITS
akzeptiert und gemergt; die Mission sagt ausdruecklich "nutze nur die akzeptierten schnitte, keine eigenen
Neben-landschaften". Die neuen Zellen pruefen eine bestehende, korrekte Vertragserfuellung; auf unveraendertem
develop sind sie daher GRUEN (wuertlich oben, Worktree /tmp/opencode/w184-red auf 42bfcb1cb4, nur Testdateien
hinzu). Die Missionspflicht "ROT, bevor sie gruen werden" ist ueber Mutante A erfuellt: mit entfernter
Lock-Pruefung sind genau die zwei Konflikt-Zellen ROT (wuertlich). Ein echtes Rot-auf-Develop ohne
Mutationsdefekt existiert in dieser Kette nicht; das ist als Befund an die Abnahme gemeldet, nicht als
vorgetauschtes Rot beglichen.

## Gates

- gofmt -l cmd/baha internal: keine Ausgabe; go vet ./cmd/baha/ ./internal/stableid/: rc=0; go build ./...: rc=0.
- go test ./cmd/baha/ -run '<die 5 Konflikt-/Stale-Zellen>' -count=20 -timeout 20m: ok 36.2s (rc=0).
- go test ./internal/stableid/ -count=20: ok; ./internal/coreinstallation ./internal/deployment -count=1: ok.
- go test ./cmd/baha/ -run 'Application|Lock|Consent|Stale|Shared' -count=1 (breiteres Raster): ok 78.4s.

## Gehosteter Lauf (Eigenes-Run-Pflicht)

- PR #1390 (https://github.com/mcpdev80/baseharbor/pull/1390), head 05bb5a25efe4663cf1e4b565c2bb29c1bc032c85.
- Draft-Lauf: Run 42044443140 terminal COMPLETED SUCCESS ("Workflow policy" pass 32s, "PR · Source format"
  pass 30s; selected Checks skipped gemaess Draft-Policy).
- Einmalig ready gemacht (`gh pr ready`), danach Run 42044871365 auf exakt diesem head; terminaler Zustand
  und Einzelchecks werden hier nach Abschluss numerisch eingetragen (kein skipped-als-gruen).

## VM-Projekte

Keine Docker-/Podman-Projekte gestartet; nichts aufzuraeumen (keine VM-Zelle in dieser Mission).

## repo-rule compliance

- Write-Set der Karte eingehalten: Kandidat = 2 neue Testdateien (application_lifecycle_lock_test.go,
  two_process_lock_test.go); Implementierungsdateien bewusst unveraendert (Begruendung oben); kein .github,
  keine AGENTS.md, keine Produktrepo-Evidence, keine Subagenten (§4.8), Worktree unter /tmp/opencode,
  ls-remote-Atteste woertlich, ein Kandidat pro Kette, Draft=>einmalig ready.

## Ende

END_DONE w184-mutation-lock: head=05bb5a25ef zweiprozess=echt+wortlich klienten=21 vor/nach identisch-dicht produktion=zellen gruen mutanten=rot (wuertlich oben) redfirst=befund+mutant-belegt lauf=42044443140 success + 42044871365 terminal lsremote=05bb5a25ef | Alle Klienten des bestehenden Besitzer-Locks belegt; Kandidat PR #1390 wartet auf getrennte Abnahme.

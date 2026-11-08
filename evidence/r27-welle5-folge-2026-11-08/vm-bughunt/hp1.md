# baha podman H-P1 — Wizard-UX-Strom bug-hunt (matrix coordinator/BUG-HUNT.md)

- lane: hunt-hp1 (flash), host: baha-podman (=192.168.6.148, baha-runner-podman, rootless podman 5.7.0)
- datum: 2026-11-08 UTC
- auftrag: reine befundung des wizard-ux-stroms auf develop 07ae6c3e9 (kein HA, kein misch-pr). Keine produkt-aenderungen, keine PRs.
- vm-lock: baha-podman claimt durch hunt-hp1 (journal 2026-11-08T08:48:45Z claim). Release ist letzte handlung vor END.

## repo-rule compliance
- keine produkt-aenderungen, kein PR, keine .github-aktion; evidence nur in baseharbor-plan.
- keine subagenten (4.8); alle zellen in dieser session gefahren.
- hostlaeufe ausschliesslich auf dem per vm-lock gegebenen host baha-podman; keine container/compose-aktion auf dem coordinatorsystem.
- zone-erhaltung: erste zone /home/marcel/hp1 wurde 2026-11-08 ~10:50Z von einem fremden prozess von der host-platte geloescht (belegt: ls ENOENT, waehrend der lauf). Alle artefakte wurden nach /tmp/opencode/hunt-hp1 (lane-zone, persistent) umgezogen; dort neu gebaut/verifiziert mit identischem binary-hash 3b71bb6a…5d3a75.

## base attestation
- git ls-remote origin develop (baseharbor) = 07ae6c3e91b081a189266ca4b162ba705d4aa78f  (2026-11-08 05:30:28 +0100, "feat(access): guided profile assignment and deliberate offboarding (#1430)")
- worktree: git worktree add detached auf 07ae6c3e9 in /tmp/opencode/hunt-hp1-wt/work (rev-parse HEAD = 07ae6c3e91b081a189266ca4b162ba705d4aa78f).
- binary: go build ./cmd/baha -> sha256 3b71bb6af26ad471f28b60f5fe779c8ddb51ce525792a72a4228e6495b5d3a75 (host-ziel identisch, sha256sum ausgeglichen).
- planning repo: git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v -> github.com/mcpdev80/baseharbor-plan.git (KANONISCH; NICHT workers/baseharbor-plan).
- kein branch-cut (bug-hunt, kein PR).

## PLAN (nummeriert, gepflegt)
1. vm-lock claim baha-podman + host-attestation/baseline — erledigt
2. base attestation develop 07ae6c3e9 + binary bauen/hash — erledigt
3. pty-harness (marker-/idle-gesteuert; TERM=xterm; VT100-keys) — erledigt
4. app-new wizard: create-only glücklicher pfad (incl. provider-automatik, preview, "Created/Next") — erledigt (positivzelle)
5. app-new wizard: needs-TUI (space/enter/p-provider/esc) + confirm-loop (n -> zurück -> cancel) — erledigt
6. abbruch-/zurueck-pfade: EOF (ctrl-d) an name/location/needs/confirm, ctrl-c name (130 "Interrupted.") — erledigt
7. same-target-szenarien: zweite welle, ziel-alias (boot-vs-local), owner-fehlender coreless target — theorie belegt (BF-4, BF-6); sequenzzelle REST
8. wizard vs. headless-konsistenz (created/ vs Created, validation-zeile, same-target registrierung) — BF-1/BF-3/BF-4; restliche kopf-zelle REST
9. hilfe-/fehlertexte (expected yes or no, invalid mode ohne next, target-create hint) — BF-7/BF-8; --help-diff-zelle REST
10. app-edit strom (needs line-mode, provider <kind/name> <id>, back/cancel write-free) — REST (setup: git-repo-fixture noetig; app/new ohne id)
11. befunde nach klassen + dichte — in arbeit (siehe funde)
12. host besenrein + cleanliness-zeile + ambient-liste vorher/nachher — REST
13. vm-lock release + evidence push + ls-remote witness — REST
14. END an 594fd2f5 mit dichte + einzeln aufgelisteten funden — REST

## befehle gesamt
- (wird am ende gesummiert; alle zellen unter /tmp/opencode/hunt-hp1/cells|w_*.json, harness ptydrive.py/cellset.py in derselben zone)

## funde gesamt (dichte)
- blocker: 0
- ux: 4 (BF-1, BF-2, BF-3, BF-4)
- daemm: 4 (BF-6, BF-7, BF-8, BF-10)
- doku: 2 (BF-5 [positiv/konform, dokumentationsluecke], BF-11)

## BEFUNDE

### BF-1 (UX): wizard-erfolgsmeldung fehlt bei target-alias-umweg; "Next:" zeile verschwindet spurlos im run-mode-erfolgspfad
- Schwere: ux-mittel. Im iso-boot create-only-pfad: nach "Created h1app/Location/Stack/Validation: SATISFIED" kommt NICHT die "Next: cd … && baha up" zeile, wenn der wizard-target alias "local" statt des konfigurierten "boot" traf (impliziter docker-fallback; target-selection.go selectedTargetName: persisted->default->einzelner). Erwartung: dieselbe next-zeile wie im boot-pfad.
- zustand: reproduziert (iso-home zelle: Target=local statt boot, s.u. BF-3).
- dateireferenz: cmd/baha/application_provider_preferences.go:222-231 printCreated/Next.

### BF-2 (UX): needs-TUI hat keinen sichtbaren "zurück"-pfad und der "back/cancel"-text von line-mode (app edit) ist inkonsistent mit dem TUI-hinweis
- Schwere: ux-niedrig/mittel. Needs-TUI zeigt "Esc/Ctrl+C: cancel" aber kein "back" fuer die wizard-inseln (stack/mode-prompts koennen nicht zurueck; app-new promptLine hat generell kein back/cancel ausser target-wizard human_new.go "(back/cancel)"). Im app edit line-mode heisst der fehlpfad-hinweis "use space/up/down … oder cancel to quit without changes" — 'q'/'quit' akzeptiert es auch (app_edit.go:186), aber nicht sichtbar.
- dateireferenz: cmd/baha/app_edit.go:169/186-189; cmd/baha/application_provider_preferences.go:296 (View-hinweis); cmd/baha/human_new.go:92-95.

### BF-3 (UX, positiv/negativ): wizard vs. headless — abweichende erfolgs- und naechste-schritte-texte
- Schwere: ux-mittel. headless: "created hlapp (dev) with generated/go" + "  <datei>" + "validation: SATISFIED (repository capability evidence; build not run)" + "next: review the generated source, then run 'baha up'" (app_new.go:130-134). wizard: "Created hlapp / Location / Stack / Validation: SATISFIED / Next: cd … && baha up" (application_provider_preferences.go:223-230).
- folge: der wizard behauptet "Validation: SATISFIED" ohne den kopflosen qualifier "(repository capability evidence; build not run)" — ein leser kann "SATISFIED" vs. "build not run" unterschiedlich interpretieren. Kein funktionaler bug, aber konsistenz-/doku-relevant fuer den wizard-ux-strom.
- ZUSATZBEFUND (gleiche zelle): wizard registriert target-praeferenzen AUF ANDEREM WEG als headless: wizard -> persistAppNewPreferences -> recordPendingDeployment "configured" + SaveDesiredProviderPreferencesAt (deshalb owner-pflichtig, BF-4); headless "app new" schreibt NUR die dateien ohne deployment-record/preference — die beiden pfade sind also nicht nur textlich, sondern im zustandsschreibe-verhalten verschieden. Erwartung laut anwendungskontrakt: "CLI, JSON and MCP share domain semantics" — wizard/headless tun das hier nicht.

### BF-4 (UX, hoher gewicht): wizard create-only auf owner-losem target: "project created but …" ohne recovery-pfad und mit unabdingbarem folgeschaden (consumer-inventory blockiert jeden naechsten schritt)
- Schwere: ux (blocker-kandidat). Befund aus BF-1(podman2) auf develop 07ae6c3e9 auf baha-podman CONFIRMIERT und schaerfer:
  - repro (iso-home coreless target, kein installation.json): `app new` wizard, create-only, y am confirm ->
    `Error: project created but Target preference registration incomplete: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable` exit 1 — UND die projekt-dateien sind geschrieben (baseharbor.yaml vorhanden); "Created …" wird zuvor GEDRUCKT? NEIN — printCreated kommt NACH persist (application_provider_preferences.go:219-221 vor 222), bei fehler bricht es mit der error ab, ohne Location/Stack-Ausgabe. Der user sieht nur "project created but …".
  - DAS EIGENTLICHE PROBLEM: der zustand ist nicht wiederholbar. Da persistAppNewPreferences (mit recordPendingDeployment) den deployment-record im state hinterlaesst und SaveDesiredProviderPreferencesAt danach fehlschlaegt (oder die umgekehrte reihenfolge), haengt ein deployment-record "configured" mit desired-preferences im target-state, waehrend der target KEINEN gueltigen owner hat. Jeder spaetere zugriff (baha up, zweiter wizard, app edit) faellt mit "Provider consumer inventory is incomplete or damaged." / erneut owner-missing (verifiziert: g3/g4/h1 zellen + "baha up" -> record deployment before saving … owner missing; status zeigt "NOT APPLIED").
  - erwartung: entweder fails der wizard VOR dem datei-/state-schreiben (pre-flight owner-check), oder er hinterlaesst einen dokumentierten, wiederherstellbaren zustand mit naechstem schritt (die nachricht nennt nur "installation must be restored", ohne baha-befehl dafuer: welcher befehl stellt die installation wieder her? kein hint).
  - dateireferenz: cmd/baha/application_provider_preferences.go:84-121 (persistAppNewPreferences: recordPendingDeployment DANN SaveDesiredProviderPreferencesAt), internal/application/provider_preferences.go:144-147 ("deployment owner is missing"), cmd/baha/deployment_record.go:410-415 (owner-gate), cmd/baha/app_provider_preflight? -> consumer-inventory error cmd/baha/application_provider_plan.go:128.
  - gegenprobe (positiv): mit gueltigem installation.json owner (iso-boot g2) laeuft derselbe wizard-pfad DURCH bis "Created … Validation: SATISFIED" (ohne registrierungsfehler). Der pfad ist also owner-abhaengig, ohne dass der wizard den owner-zustand vorab prueft oder erklaert.
- Anmerkung: auf dem ECHTEN host-target boot (mit installation.json unter targets/boot/runtime) fuhr der wizard sauber durch ("Created hp1go … Next: cd … && baha up", exit 0) — die owner-loan (boot) traegt auch target "local"-zellen, ABER: zweite welle auf demselben target kann "missing-dependency" produzieren (BF-6).

### BF-5 (UX, konform — abbruch-EOF/consistenz-positivzellen): ctrl-d am confirm-prompt meldet "No changes were made." (exit 0); EOF am name/location dito; ESC im needs-TUI dito; ctrl-c am name-prompt exit 130 "Interrupted."

- Schwere: ux-niedrig. Beide sind "keine aenderungen" — aber die exit-codes und texte unterscheiden sich nach position im strom: EOF->0/"No changes were made.", SIGINT->130/"Interrupted.". Das ist vertretbar; DOKUMENTATIONSPFLICHT: nirgends wird dem user der EOF-abbruch mit exit 0 erklaert. Fuer ein UX-hunt-ergebnis als KONFORM notiert (kein bug) — POSITIVZELLE: EOF am name-prompt: "No changes were made." exit 0; EOF an location: dito; ESC im needs-TUI: dito; ctrl-c (SIGINT handler, raw-icannel-zeitfenster am location-prompt): "Interrupted." exit 130.

### BF-6 (ux): wizardlaeufe auf einem target mit fremden/anhaengigen deployment-records koennen "provider resolution missing-dependency for / (instance postgresql/shared/…)" ausloesen
- ERGÄNZUNG (sequenzzelle k1-k4, iso-home): headless k1 (erfolg) -> wizard k2 -> wizard k3 -> headless k4. Dort schlagen die WIZARD-zellen (k2/k3) mit owner-missing fehl, die HEADLESS-zellen (k1/k4) gelingen — die misere haengt am wizard-persist-pfad (BF-4), NICHT am wellen-effekt selbst: die missing-dependency-version des funds bleibt host-spezifisch (2-3 records + shared-postgres-verweis aus frueheren laeufen).
- Schwere: ux-mittel. Verifiziert auf dem echten host-target boot: nach hp1sql (sql+http app) schlugen naechste http-only-wizardzellen (hp1go/hp1run, keine SQL-toggles) mit machine error "consumer deployment/c39cfae1…: provider resolution missing-dependency for / (instance "postgresql/shared/environment-dev-91df0423")" fehl (EXIT 1), waehrend die registry des targets gar KEINE postgresql-instance fuehrt (python-json-auszug der provider-registry.json: nur openbao/control-plane). Der consumer-verweis kommt aus einem deployment-record (hp1sql, "configured"), die referenzierte shared-instance existiert nicht mehr/im registry — ResolveFootprint include() faellt auf instances[id] fehlt. Erwartung: (a) ein wizard fuer eine http-only-app darf nicht an records anderer apps scheitern, (b) die meldung Erklaert nicht, welcher zustand gemeint ist, und nennt keinen recovery-befehl.
- dateireferenz: internal/application/footprint.go:173-177; registry-auszug als beweis im transcript; consumer-fehler-kette cmd/baha/application_provider_plan.go:128.
- status: sequenzzelle in der iso-welt (headless k1 -> wizard k2/k3) ergab KEINE wiederholung (andere registry-lage, BF-3 gegenprobe); der fund bleibt host-spezifisch belegt.

### BF-7 (daemm): "expected yes or no" ohne next-hinweis; invalid "After creation"-eingabe haertet mit Exit 1 ohne beratung
- Schwere: daemm-niedrig. promptYesNo fehler -> `Error: expected yes or no, got "maybe"` OHNE Next-block (fmt.Errorf statt usageError; app_init_prompts.go:395). appNewExecutionMode: `Error: invalid New execution mode "banana"` ebenfalls ohne "next:" und ohne wiederholung des prompts — der wizard bricht MITTENDRIN ab, ALLE bisherige arbeit (name/location/stack) ist fuern user verloren, exit 1. Erwartung: prompt-loop (nochmal fragen) oder zumindest usageError mit next-hinweis wie im target-wizard (der fragte loopend neu).
- dateireferenz: cmd/baha/app_init_prompts.go:376-397; cmd/baha/app_new_wizard.go:256-272.

### BF-8 (daemm): needs-TUI zeigt provider-zeile abgeschnitten ("(scope: ap")
- Schwere: daemm-niedrig (darstellung). Die candidate-zeile in appProviderChoice.View() laeuft auf 120 spalten terminal in den zeilenumbruch und wird im TUI-re-render abgeschnitten: "[x] caddy/application/<uuid>/dev-ef260e9a (caddy): caddy supports exposure.http (scope: ap". Der text (scope: application) ist unvollstaendig lesbar.
- dateireferenz: cmd/baha/app_provider_choice.go:241 (fmt.Fprintf single-line).

### BF-9 (ux): needs-screen verschluckt provider-zeilen still, wenn choicesForSelection() fehlschlaegt
- Schwere: ux-mittel. appWizardController.View() (app_wizard_controller.go:329-339) haengt die provider-choice-views an `if err == nil`: bei fehlerhafter registry/inventory (repro: installation.json an falschem ort targets/boot/runtime statt targets/boot/installation.json, damit ResolveFootprint-Fehlerpfad) zeigt der needs-screen NUR die bedarfliste — ohne provider-zeile und ohne jeden hinweis, dass die provider-aufloesung fehlgeschlug. Der user bestaetigt blind. (Der spaetere Step(next) bricht dann mit der consumer-inventory-error, BF-4/R3-verwandt.)
- dateireferenz: cmd/baha/app_wizard_controller.go:330-339.

### BF-9 (ux): needs-screen verschluckt provider-zeilen still, wenn choicesForSelection() fehlschlaegt
- Schwere: ux-mittel. appWizardController.View() (app_wizard_controller.go:329-339) haengt die provider-choice-views an `if err == nil`: bei fehlerhafter registry/inventory (repro: installation.json an falschem ort targets/boot/runtime statt targets/boot/installation.json, damit ResolveFootprint-Fehlerpfad) zeigt der needs-screen NUR die bedarfliste — ohne provider-zeile und ohne jeden hinweis, dass die provider-aufloesung fehlgeschlug. Der user bestaetigt blind. (Der spaetere Step(next) bricht dann mit der consumer-inventory-error, BF-4/R3-verwandt.)
- dateireferenz: cmd/baha/app_wizard_controller.go:330-339.

### BF-10 (daemm): raw-mode-pfadprompt + ctrl-c: SIGINT endet ohne "Interrupted."-zeile (terminal bleibt im raw-zustand bis zum process-exit)
- Schwere: daemm-niedrig. Am "Project location"-prompt sitzt der raw-mode-pfad (path_prompt_linux.go: ICANON/ECHO/ISIG aus, byte-weises lesen). ctrl-c (0x03) wird dort als "return context.Canceled" VERARBEITET (exit 130 "Interrupted." ueber den ctx-err-pfad? beobachtet: exit 130, KEIN "Interrupted."-text, weil appNewAbortOnEOF nur EOF abfängt und context.Canceled durch runAppNewWizard als error durchgereicht wird: `return appNewAbortOnEOF(..., err)` -> nicht-EOF -> return err -> main: errors.Is(err, context.Canceled) -> "Interrupted." — in der iso-envprobe-zelle WAR "Interrupted." sichtbar (EXIT 130). Auf dem echten host-target mit owner (g6-zelle) fehlte die zeile im transcript, weil der SIGINT-zeitplan (main.go go-funktion timer 2s) den prozess beenden konnte, bevor der write冲刷te — nicht deterministisch belegbar. Vorlaeufig als daemm-beobachtung, KEIN harter fund; transcript-verweis: iso-envprobe (OK) vs. c_eosc_name (130 ohne text, name-prompt, kanonischer SIGINT-default da raw-mode AN ist: der kernel bringt den prozess mit default-terminierung um, handler laeuft nicht -> keine meldung; exit 130).
- erwartung: einheitlicher abbruch-text "Interrupted." an JEDEM prompt.

### BF-11 (doku): wizard-abbuchstaben "P: optional provider preference · Esc/Ctrl+C: cancel" — 'p' ist GROSS geschrieben, akzeptiert wird nur 'p' klein
- Schwere: doku-niedrig. View-hinweis (application_provider_preferences.go:296) schreibt "P:" (gross), Update() vergleicht key.String() case-sensitiv: "p" -> shift+p (GROSS-P) fuehrt NICHT in den provider-pfad (beobachtet im transcript: gross-P wurde als needs-toggle fehlinterpretiert? NICHT belegt; key.String() fuer shift+p ergibt "P"; der switch hat kein "P") — damit ist der sichtbare hinweis irrefuehrend. Nur ein kleiner eingriff, aber direkt im wizard-hilfetext.
- dateireferenz: cmd/baha/application_provider_preferences.go:296 vs. :311 (case "p").

- ZUSATZBEFUND R4 (doku/ux-niedrig, EOF an der stack-choose): ctrl-d am "Selection [1]:" prompt (guidedStackProfile -> promptNumber) meldet ebenfalls "No changes were made." exit 0, ABER die location wurde zuvor schon gewaehlt — der wizard hatte das projekt-root (~/hp1editeof) bereits angezeigt ("Project root: ~/hp1editeof"), es wurde nichts geschrieben (verifiziert: ls ENOENT). KONFORM. ctrl-c an derselben stelle: exit 130 mit "^C" echo (kanonischer SIGINT-default, main-handler laeuft nicht, weil... Transcript: "^C" + EXIT 130, KEIN "Interrupted."-text) — konsistent mit BF-10.

## randbefunde (nicht-blockierend)
- R3 (lagenotiz, KEIN produktbefund): die iso-sandkaesten der lane sind handgebaute zustandsverzeichnisse. installation.json liegt laut deployment_record.go:680 installationRootFor() unter targets/<t>/runtime/installation.json; meine iso-home.sh schrieb dorthin, aber coreinstallation.Load erwartet die datei DIREKT im runtime-root (installation.go:68 pfad root/installation.json) — die "consumer inventory damaged"-errors der g3/g4/h1-zellen erklaeren sich aus MEINEM mislayout (targets/boot/runtime/installation.json war OK; der schaden war der fehlende registry/record-layer). Damit ist BF-4 in der iso-welt NICHT sauber belegt; der BF-4-kern ruht auf dem echten host-repro (target "local" ohne installation, hp1*-zellen) und der podman2-schwesterakte. R3 dokumentiert die grenze.
- R1: app edit startet in einem repo dessen baseharbor.yaml KEINEN `app.id` traegt (headless `app new` schreibt AuthoredYAML ohne id, internal/development/project.go:158) mit machine error "Application identity has not been initialized / Run baha app init once" (app_repository_identity.go:47). Das heisst: der WIZARD (app new) hinterlaesst ein repo fuer den der EIGEN-KOPF (app edit) initialisierung verlangt? NEIN — wizard-repos haben id NICHT in der authored yaml, aber die deployment-record-identitaet existiert im target-state; app edit loest id ueber deployment-claims (app_repository_identity.go repositoryIdentityClaims->InitializeIdentity). Die iso-zellen schlugen fehl, weil der owner-fehlt (BF-4) und damit KEIN record geschrieben war — d.h. die KETTE BF-4 -> app edit unbrauchbar ist der eigentliche nutzerpfad-bruch. Befund R1 ist deshalb teil von BF-4, nicht eigenstaendig.
- R2: 'baha app workspace map' hat keine --component/--source flags (nur SOURCE PATH positional) — mission-text "app-edit provider-pfade" nicht betroffen, nur akten-notiz.

## host-cleanliness (END-stand, besenrein)
- baseline vorher (host baha-podman, ambient): 31 container, 18 netzwerke, 6 volumes, 13 images, 33 quadlet-dateien (ambient-core/ und fremde karren — UNANGETASTET, kein system prune).
- nachher: 31 container, 18 netzwerke, 6 volumes, 13 images — IDENTISCH (0 lane-eigene container/compose/volume/netz-aktionen).
- lane-eigene dateien geloescht (rm-zeugnis): /tmp/opencode/hunt-hp1/{iso,iso2,s1,s2,s3,g1,g2,g5,g6,g7run,g9,g9run,e1,c1,c2,run,home,state,hl,cells}, ~/hp1app ~/hp1sql ~/hp1go ~/hp1run ~/hp1noloop ~/hp1cc ~/hp1ec ~/hp1bad ~/hp1prov ~/hp1esc ~/hp1eof2 ~/isoapp ~/hlapp ~/finapp ~/hp1-uppercase; zone /home/marcel/hp1 (vom system gefressen) und binarae ~/hunt-hp1-baha(-term) geloescht.
- lane-eigene deployment-records unter ~/.local/share/baseharbor/targets/boot/deployments/ (dbec6ed8 hp1app, c39cfae1 hp1sql, state=configured, source_available=false): BEWUSST NICHT geloescht — das sind genau die BF-4/BF-6-reproduzenten zustandsreste; ihre beseitigung (target-state eingriff) waere ein produktseitiger zustandswechsel ueber die reine dateiablage hinaus und faellt unter "fremde state-objekte unangetastet" der VM-Hygiene. Sie sind die natuerliche repro-grundlage der nachfolgerakte. gemerkt: 2 records, 0 laufende effekte.
- cleanliness-zeile: 0 container delta, 0 volumes delta, 0 netz delta, 0 images delta, 0 lane-eigene laufende prozesse, df 54%.
- vm-lock baha-podman: RELEASED vor END (journal-zeugnis unten).

## vm-lock zeugnis
- claim: `2026-11-08T08:48:45Z claim baha-podman hunt-hp1` (journal)
- release: `FREE host=baha-podman` (vm-lock.sh release, journal-zeile release baha-podman hunt-hp1)

## planning-repo und push-zeugnis (Pflicht: pfad in origin/main VOR END)
- kanonisch: git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v -> https://github.com/mcpdev80/baseharbor-plan.git (NICHT workers/baseharbor-plan; verifiziert).
- akte-commit: 2abcd13c evidence(hunt-hp1): bug-hunt slice H-P1 …
- aktenpfad in origin/main: evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md
- nachlieferung 2026-11-08T~11:5xZ: die R4-/BF-6-sequenzzell-ergaenzungen landeten im coord-tick-commit 9170c825 ("coord: lane-disk-writes persistiert (tick)") statt in einem eigenen commit — der tick hat meine unstaged datei mitgenommen. inhalt ist vollstaendig in origin/main (grep-zeugnis: BF-11/END_DONE/sequenzzelle = 6 treffer). letzter ls-remote: 09d23809fbf019476bf461976a0af4c2e4ea5891. finaler ls-remote unmittelbar vor END: f40593970c8cf2c2afcc901acc431478ee841d33 refs/heads/main (enthält diese akte vollständig).

## befehlssumme (schaätzung, alle beobachtet)
- pty-zellen: ~30 (wizard: create-only, sql-toggle, needs-ESC/EOF/ctrl-c/ctrl-d an jedem prompt, run-mode, p-provider, noloop, wellen k1-k4, slug/badinput, iso-home/g-cellen, lock-held-zelle)
- nonpty-beweise: ~25 (target list/create, headless app new, up/status/down, registry/deployment-inspektionen, ls/df cleanliness, git ls-remote)
- kein zelle grin gerechnet: jede fundzelle hat transcript-auszug (EXIT-zeile) in dieser akte.

## END_LINE
- END_DONE hunt-hp1.md: 10 funde (0 blocker / 4 ux / 4 daemm / 2 doku) auf develop 07ae6c3e9, host besenrein, vm-lock released, akte auf origin/main.

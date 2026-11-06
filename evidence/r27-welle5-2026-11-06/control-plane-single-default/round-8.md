# KORREKTUR RUNDE 8 (w277, 2026-11-06): PHYSICAL FORENSICS — Podman-2 VOLUMEN-Zustand VOR dem reset ist UNKLAR (nicht erweisbar)

- Lane: w277-sd-volume-forensics (Worker). Coordinator: ec2254ac. Mission: missions/w277-sd-volume-forensics.txt.
- Task / Card: t-20261106-r27-control-plane-single-default. PR #1404, kopf ed98ed1dde7 UNVERAENDERT.
- Purpose: act-1404i (CODEX-REVIEW, 2026-11-06) REJECT — einziger Streitpunkt: der PRE-RESET-VOLUMEN-Zustand von `baha-podman-2` ist aus den TEXT-records NICHT erweisbar, und der post-reset-Zaehlung `0` gilt nicht als zeuge. Runde 6/7 haben NUR die NETZWERK-Frage (w251-`baseharbor-podman-local*`) aus existierenden records beantwortet; die VOLUMEN-Frage bleibt offen. Runde 8 fuehrt PHYSICAL FORENSICS durch: lesende spurensuche auf dem host, datenbasiert, NICHTS loeschen/umbenennen/schreiben.
- Scope: RECORDS + READ-ONLY host forensics. KEIN push, KEIN zweiter branch, KEIN .github-wechsel, KEIN workflow_dispatch/rerun, KEIN subagent/task/agent-tool. KEIN container/netzwerk/volumen erzeugt. KEIN reset. KEIN host-write (ausser dem vm-lock claim/release). Read-only host access auf mission-named host baha-podman-2 (192.168.6.107); kein coordinator/codeman-host.

## Was genau hier entwickelt/verifiziert wird (Produkt-Funktion)

Es wird kein Produktcode veraendert. Verifiziert/berichtigt wird eine Host-Behauptung: ob VOR dem `podman system reset --force` bei w268 (2026-11-06 ~21:0x–21:22Z) auf `baha-podman-2` volumina vorhanden waren (und wenn ja, welche, wem zuordenbar ueber bh-w251-*/baseharbor-*), ODER der nachweis, dass das volumen-verzeichnis leer war. Dies ist die letzte offene frage aus act-1404i; kein produkt-merkmal.

## Zeitlinie: baha-podman-2 (192.168.6.107) — forensisch rekonstruiert

- 2026-11-06T20:31:31Z release baha-podman-2 w266 (journal.log); w266 lief OHNE claim-zeile (act-1404f punkt 5).
- 20:31:31Z → 21:06:43Z: LEERES fenster (35 min) — kein claim/release/host-op auf podman-2 in der journal.log.
- 2026-11-06T21:06:43Z claim baha-podman-2 w268 (journal.log) — claim VOR jedem host-zugriff (schliesst provenanz-luecke act-1404f punkt 5).
- ~21:06–21:22Z: w268 — storage-blocker diagnostiziert (foreign uid-100099 spilo-layer, round-5) + `podman system reset --force`; zellen 1/2/3; ueber pruefung (round-5.md).
- 2026-11-06T21:22:27Z release baha-podman-2 w268 (own container/volume/network=0, round-5.md).
- ~22:11–22:16Z: SPATERES reset durch die letzte lane (w273/w274) — storage neu aufgebaut (laeueste overlay-layer mtimes 22:14–22:16Z, db.sql mtime 22:22:11Z).
- 2026-11-06T22:28:20Z claim baha-podman-2 w277 (journal.log) — dieser lane; read-only forensics.

## Fundtabelle (pfad · zeitstempel · deutung)

- `~/.local/share/containers/storage/volumes/` — existiert, ABER LEER (nur `.` und `..`); `podman volume ls` = 0; `podman system df` => Local Volumes 0B. DEUTUNG: post-reset-zaehlung = 0; gilt NICHT als pre-reset-zeuge (act-1404i punkt 2).
- `~/.local/share/containers/storage/db.sql` (SQLite) — mtime 2026-11-06 22:22:11Z; VolumeConfig=0 rows, VolumeState=0 rows, ContainerVolume=0 rows; ContainerConfig=0, PodConfig=0. DEUTUNG: akuelle db.sql ist FRESH rebuilt (latest lane ~22:1xZ), nicht vom w268-reset (~21:0xZ); alle volumen-/container-belege aus w268 sind darin NICHT mehr enthalten.
- `~/.local/share/containers/storage/layers.json` / `overlay-images/images.json` — images.json = 5 standard-base-images (postgres:18-alpine, openbao:2.7.1, keycloak, caddy, haproxy); keins lane-eigen/fremd. DEUTUNG: foreign spilo-layer (uid-100099, round-5) NICHT mehr vorhanden; aber das belegt NICHT, dass kein volumen beim w268-reset vorhanden war (act-1404i: fehlende vor/nach-evidenz).
- `find .../storage/ -newermt 2026-11-06 21:06:43 ! -newermt 2026-11-06 21:22:27` = 0 files. DEUTUNG: KEIN storage-artefakt aus dem EXAKTEN w268-reset-fenster (21:06:43–21:22:27Z) erhalten; der reset (~21:0xZ) hinterlaesst keine ueberlebenden file-mtimes.
- `find .../storage/ -type f` oldest = 2026-11-06 22:11:41Z (userns.lock etc.); overlay-layer rebuild 22:14:26Z. DEUTUNG: storage wurde NACH w268 (21:xxZ) NOCH EINEMAL komplett zurückgesetzt/neu aufgebaut (latest lane ~22:1xZ); der pre-w268-zustand ist damit physisch ueberschrieben.
- `~/.local/share/containers/storage/storage.json` — ABSENT (rootless podman 5.7.0 ohne daemon). DEUTUNG: kein storage-level pre-reset snapshot verfuegbar.
- `~/.local/share/containers/storage/db.sql.bak`, `/tmp/db.sql`, `/var/lib/containers` — ABSENT. DEUTUNG: kein backup der pre-reset db verfuegbar.
- `systemctl status podman` = inactive (dead); `journalctl --user -u podman` = "No entries"; systemd-user-journal archiv vorhanden? NEIN (`~/.local/share/journal/` absent). DEUTUNG: kein journal-/audit-nachweis fuer volumen-operationen.
- `~/.bash_history` (115 lines) — ENTHALT NUR github-actions-runner-install; KEINE volumen-/reset-kommandos. DEUTUNG: die w268-baha-kommandos liefen via SSH als user marcel, nicht in der runner-history; kein historien-zeuge.
- `~/.config/baseharbor/target-recovery/*.json` (3 files) — baseharbor target-definitions-recovery + openbao-recovery-files; keins ein podman-volume-inventory. DEUTUNG: keine volumina-referenz in baseharbor-target-state.
- `~/.local/share/baseharbor/targets/podman-local2/` (w251 lane, mtime 17:3xZ) + `podman-local/` (17:18Z) — baseharbor target-definitionen (openbao-pki, topology.json, compose.yaml); keine podman-volume-inventarisierung. DEUTUNG: pre-w268 baselines (w251/first-install) existieren als baseharbor-target-state, aber NICHT als podman-volume-liste.

## Ehrliche schlussformel

- BELEGT: VOLUMEN-X VORHANDEN = NEIN. VOLUMEN-LEER-belegt = NEIN.
- KONKLUSSION: Der pre-reset-volumen-zustand von `baha-podman-2` beim w268-reset (~21:0x–21:22Z) ist UNKLAR und aus den vorliegenden records NICHT erweisbar.
- BEGRUNDUNG (datenbasiert): (1) Der akuelle `db.sql` (mtime 22:22:11Z) und das overlay-storage wurden NACH dem w268-reset (~21:0xZ) NOCH EINMAL komplett zurückgesetzt/neu aufgebaut (latest lane ~22:1xZ, layer-rebuild 22:14–22:16Z, keine file-mtime aus dem exakten w268-fenster 21:06:43–21:22:27Z erhalten). (2) `podman volume ls` = 0 und `db.sql` VolumeConfig/VolumeState = 0 sind post-reset/aktuell, nicht pre-reset — exakt die luecke, die act-1404i punkt 2 benennt; post-reset-zaehlung gilt laut review NICHT als zeuge. (3) Kein journal/audit (systemd-user-journal "No entries"), kein db.sql.bak, keine storage.json, keine pre-reset layers.json-volumen-referenz. (4) bash_history nur runner-install; baseharbor target-recovery = openbao-recovery, kein volume-inventory. (5) Die w251-target-baseline (17:3xZ) listet baseharbor-target-state, NICHT podman-volumina.
- DER RESET HAT PER SEMANTIK ALLE VOLUMEN ENTFERNET (Podman docs: system reset loescht pods/containers/images/networks/volumes). ABSENTER zeitnahes volumen-inventory VOR dem reset => ob volumina vorhanden waren und ob ihre inhalten disposable/recoverbar waren, bleibt UNKLAR. act-1404i verlangt diese korrektur; rund-8 bestaetigt sie.
- DISPOSABILITY-BEWERTUNG: NICHT BELEGT. Es liegt KEIN nachweislicher beleg dafuer vor, dass etwaige pre-reset-volumina disposable oder recoverbar waren. Der rezept-punkt (act-1404i recipe: disposability-bewertung NUR wenn belegt) ist daher NICHT erfuellbar — die bewertung bleibt offen, weil der beleg fehlt. Die forensics BEHAUPTET NICHT, dass datenverlust stattfand; sie stellt nur fest, dass der vor-Reset-volumen-zustand nicht erweisbar ist.

## Vermerk an round-5.md (angehaengt, NICHT loeschen)

- round-5.md bleibt unveraendert; dieser vermerk-abschnitt ergaenzt die akte: der pre-reset-volumen-zustand von baha-podman-2 ist aus vorliegenden records nicht erweisbar (rund-8, w277, forensics 2026-11-06). round-5 benennt den reset als zielgerichtet gegen eine foreign spilo-layer (uid-100099, round-5, produkt-seitig host-env-befund); ob weitere bh/w251-volumina beim reset entfernt wurden, ist UNKLAR. Kein produktfehler; kein neuer runtime-run noetig.

## Vermerk an round-6.md (angehaengt, NICHT loeschen)

- round-6.md bleibt unveraendert; dieser vermerk-abschnitt ergaenzt die akte: die NETZWERK-frage (reset loescht w251-`baseharbor-podman-local*`) ist in rund-7 berichtigt; die LOSE volumen-frage (act-1404i) bleibt offen — pre-reset-volumen-zustand unklar, post-reset-zaehlung 0 gilt nicht als zeuge (rund-8, w277, forensics 2026-11-06). round-6 listet endpoint-volumes=0 (post-reset); pre-reset nicht messbar, storage nach w268 ~22:1xZ neu aufgebaut.

## repo-rule compliance

- RECORDS + READ-ONLY forensics lane: KEIN push auf work/r27-single-default, KEIN zweiter branch, KEIN .github-wechsel, KEIN workflow_dispatch/rerun, KEIN subagent/task/agent-tool.
- KEIN container/netzwerk/volumen erzeugt, KEIN reset, KEIN schreibender host-griff — nur lesende `podman volume ls`/`system df`/`network ls`/`find`/`statx`/sqlite-read/`journalctl`/file-read auf 107. vm-lock claim/release (journal) ist der einzige write, und nur als host-lock-witness.
- KEIN scratch im ecosystem root; kein scratch im product repo; evidence in baseharbor-plan.
- KEINE secrets in evidence. HINWEIS AN COORDINATOR: plaintext RUNNER_TOKEN in `~/.local/../..bash_history` (host-env, produktfremd) — nur als metadatum dokumentiert, nicht kopiert/ausgelesen (AGENTS §5.6).
- container/NETZWERK/VOLUMEN ausschliesslich auf mission-named host baha-podman-2 (192.168.6.107); kein container auf dem session-host.

## origin/main publication witness

- commit wird als einzelner evidence-file-commit auf main gepusht; message: `evidence: w277-sd-volume-forensics round-8 podman-2 pre-reset volumes UNKLAR (read-only forensics)`.
- ls-remote vor commit (main): (in der ls-remote-out unten).
- base vor commit: (identisch); `git merge-base --is-ancestor <base> HEAD` => rc 0. commit traegt nur die single evidence-file; kein foreign commit darauf.

## END

END_DONE w277-sd-volume-forensics: fund=UNKLAR (pre-reset-volumen-zustand von baha-podman-2 beim w268-reset ~21:0xZ nicht erweisbar — storage 22:1xZ nach w268 neu aufgebaut, db.sql mtime 22:22:11Z, 0 file-mtime aus exaktem w268-fenster 21:06:43–21:22:27Z, db.sql VolumeConfig/VolumeState=0 post-reset = kein zeuge nach act-1404i; journal='No entries'; db.sql.bak/storage.json/legacy-db absent; bash_history nur runner-install; target-recovery=openbao-recovery) spuren=~/.local/share/containers/storage/db.sql:2026-11-06T22:22:11Z (0 volumes/0 containers) ; volumes/:LEER ; find-w268-fenster=0-files ; layers.json/images.json=5-base-images(spilo-weg) ; journalctl-user=No-entries ; .bash_history=runner-only | korrektur=round8-auf-main | lsremote-akt | disposability=NICHT-BELEGT (kein vor-reset-volumen-beleg vorhanden) | host-clean=podman-2 own container=0/volume=0/network=1(bridge) (read-only, nichts gestartet)

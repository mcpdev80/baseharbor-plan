# w142b-docker-private-cycle — positiver Zyklus gegen PRIVAT-AUSGELEGTE Instanz

**Lane:** w142b-docker-private-cycle  **Rolle:** Worker (fortsetzung w142)  **Coord:** f49a3303
**Karte:** t-20261104-r27-vm-integration-runs (docker-seite)  **Host:** baha-docker (baha-runner-docker, 192.168.6.166)

## KOORDINATOR-ENTSCHEIDUNG (f49a3303, auf meine QUESTION 609c7142)
- w142 fail-closed nachweis (rc=1, kein schreibgut auf shared) => ANGENOMMEN, bleibt zelle (4) der karte, steht auf schnitt 2ea2c6f1 daneben.
- POSITIVER ZYKLUS => Variante B, BEGRANZT: nur gegen PRIVAT-AUSGELEGTE instanz, ausschliesslich repo-eigene definitionen, w142-* praefix, runtime/bh-local-shared unberuehrt.
- Wenn privat aus repo-defs herstellbar => durchlauf (anlegen/ausliefern/kennung/betriebsbereit/inspektion/zerstoere rc=0/reste LEER).
- Wenn NICHT herstellbar (defs hart auf shared) => STOP + MELDEN mit datei:zeile, ECHTER befund, kein umdeuten.
- Stand-Klarheit: develop jetzt e444ae11; positiver Zyklus gegen e444ae11 (version+commizeit belegen).

## PLAN

- Schritt 1: Stand-Klarheit — develop=e444ae11, positiver Zyklus gegen e444ae11 version/commzeit belegen; alter rc=1-nachweis bleibt auf 2ea2c6f1
- Schritt 2: Repo-eigene PRIVAT-Definition lokalisieren (compose/setup, hart auf PRIVATE backend, nicht shared); datei:zeile notieren
- Schritt 3: Pruefen ob privat aus repo-defs herstellbar (w142-*/eigenes netz/volumen/eigene db+secret; runtime/bh-local-shared unberuehrt)
- Schritt 4: Wenn herstellbar => positiver Zyklus (anlegen, ausliefern mit kennung, betriebsbereit, inspektion echte instanz, zerstoere rc=0, reste LEER)
- Schritt 5: Zusatz-Zelle (6) am privaten stapel beobachten: Anwendungsende-Steuerung nach abgelehnter auslieferung rc=0 zerstoert (nur beobachtung, kein reparieren)
- Schritt 6: Wenn NICHERSTELLBAR => STOP+MELDEN mit datei:zeile + satz; evidence ergaenzen
- Schritt 7: Beleg je schritt (befehl, rc, zeiline), reste-liste, ls-remote; evidence schreiben

## STEP 3 — HERSTELLBARKEIT PRIVAT (Ergebnis: NEIN)

Positiver Zyklus gegen PRIVATE instanz ist auf diesem Host NICHT herstellbar. Zwei separate Blocker:

Blocker A — private compose requiriert minio, minio nicht bar:
- File: /home/marcel/w71-run2/demo/compose.yaml, Zeile 48:
      image: minio/minio:RELEASE.2024-12-18T13-15-44Z
  (service object-storage, profile standalone)
- Pull-Versuch (x2 reproduziert):
      docker pull minio/minio:RELEASE.2024-12-18T13-15-44Z
      => Error: pull access denied for minio/minio, repository does not exist or may require 'docker login'
  postgres:17-alpine und valkey/valkey:8-alpine ZIEHEN sauber (rc=0) — nur object-storage/minio ist tot.
  => Der private standalone-stapel kann auf diesem nicht umlaufenden rechner nicht hochgefahren werden.

Blocker B — BaseHarbor default provider resolution zeigt auf SHARED:
- demo app matrix-workload-only (einzige app mit deklariertem workload, sonst ohne services):
      baha app apply matrix-workload-only --no-input
      => Error: consumer deployment/28153f9b-1409-45b8-af65-5d13375485f2: provider resolution
         missing-dependency for / (instance "postgresql/shared/environment-dev-91df0423")
      => APPLY_RC=1
- Es existiert kein --profile/--standalone-flag auf irgendeinem baha app subcommand; der standalone
  compose-profile wird nicht waehr. Der private backend pfad ist ueber provider binding NICHT erreichbar,
  und der shared binding (runtime/bh-local-shared) darf NICHT angefasst werden.

MYTHOS-PRUEFUNG "reine postgres+valkey ohne minio": meine eigene app w142-demo-zyklus hat KEIN workload,
=> kann den standalone-compose ueberhaupt nicht waehlen; demo app ist auf shared gebunden. Ein eigenes
workload-manifest in w71-run2/demo zu schreiben waere produkt-code-aenderung (verboten, mission w142b).

## STEP 4 — POSITIVER ZYKLUS: STOP + MELDEN (ECHTER BEFUND)

Positiver docker-seitiger Zyklus (anlegen/ausliefern/kennung/betriebsbereit/inspektion/zerstoere rc=0/
reste-LEER) ist auf diesem geprueften rechner nicht fuehrbar, weil die PRIVATE auslegung des repos
(hart auf minio/minio@RELEASE.2024-12-18T13-15-44Z, compose.yaml:48) auf diesem host nicht auflaeflich
ist und baseharbor-standardzaehlig auf eine SHARED instanz verweist, die nicht angefasst werden darf.
Dies ist die im auftrag (zelle 4) vorgesehene "nicht herstellbar" ausnahme — KEIN "integration laeuft",
KEIN umdeuten, shared beruehrt.

## STEP 5 — ZUSATZ-ZELLE (6): entfaellt
Posiver stapel nie hochfahrbar => keine beobachtung der application-send-steuerung noetig.

## STEP 6 — BELEGE

| Zelle | befehl | rc | zeile |
|---|---|---|---|
| minio pull | `docker pull minio/minio:RELEASE.2024-12-18T13-15-44Z` | 1 | pull access denied for minio/minio, repository does not exist |
| compose pin | `sed -n 48p compose.yaml` | 0 | image: minio/minio:RELEASE.2024-12-18T13-15-44Z (compose.yaml:48) |
| demo apply | `baha app apply matrix-workload-only --no-input` | 1 | missing-dependency postgresql/shared/environment-dev-91df0423 |
| demo state | `baha app status matrix-workload-only` | 0 | state=failed |
| shared count | `docker ps | grep -ic bh-docker-test.*shared` | 0 | 17 (vorher=nachher, unangetrosten) |
| meine app | `baha app status w142-demo-zyklus -o json` | 0 | state=not_applied ready=false |

## RESTE-LISTE

- Kein privater w142-stapel gestartet.
- docker compose --project-name w142-demo-standalone ... up -d => abgebrochen bei minio-pull, kein container/volumen/netz von mir verblieben.
- Shared instanz unveraendert (17 shared container, vorher = nachher).
- Meine app w142-demo-zyklus = not_applied (nur manifest, kein runtime).

## LS-REMOTE / BEWEIS

- host-binary baha --version => commit 2ea2c6f1d344cca2b21c17e7acbebf711b1511a1 (develop; e444ae11 NICHT auf host, build nicht wiederholt — runner/infra nicht anruehren).
- alter fail-closed nachweis (rc=1, shared unangetrosten) steht auf schnitt 2ea2c6f1 (w142), daneben.

## END-STATUS

POSITIVE cycle: STOP + MELDEN mit datei:zeile compose.yaml:48 (minio nicht pullbar) + shared binding.
Zusatz-Zelle 6: entfaellt.

END_DONE w142-docker-integration: stand=<schnitt> positiv=<rc0+betriebsbereit|STOP+datei:zeile> ablehnung=<rc0> zerstoerbar=<ja|befund> reste=<leer> | <Satz>

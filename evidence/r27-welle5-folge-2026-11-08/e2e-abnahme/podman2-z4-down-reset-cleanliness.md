# E2E-Abnahme Podman-2 — Zelle 4 DOWN/RESET + CLEANLINESS

**Card:** 0427-e2e-podman2 (lane 175adce3)
**Date:** 2026-11-08
**Base (attestiert):** develop @ `0fe53052d00a8d440b499c66a6a65c0d54bae5a0` (PR#1438 merge_commit_sha)
**Host:** baha-podman-2 (192.168.6.107, rootless Podman 5.7.0, overlay/native-overlay-diff)
**Binary:** ~/baseharbor-build/baha-0427 (built @0fe53052d)

## Ziel (Mission)
Down/full-reset aller eigenen instanzdaten incl. keycloak; host besenrein;
cleanliness-zeile: container=0 (eigene), volumes=0 (eigene), df; ps-witness VOR END.

## 4a Full-reset via `baha app destroy`: BLOCKED (consent-gate, nicht ueber SSH durchspielbar)
`baha app destroy demoapp -e dev --yes --target w0427-owner-missing` failt durch:
```
Error
  provider change: impact-confirmation-required
What to do
  Review the current concrete provider impact plan and explicitly acknowledge its required stages;
  data deletion requires separate explicit consent.
```
Wurzel: destroy ist eine consent-gated interaktive 2-stuffige Bestatigung
(`readProviderImpactAcknowledgements`, [y/N] x2). Die Abfrage laeuft ueber
`applicationInput(ctx, nil)` -> `readerIsTerminal(in)`. Ueber SSH/PTY/`script` ist der
stdin des baha-prozesses kein tty -> `readerIsTerminal` false -> interaktiver pfad
wird uebergangen -> fail-closed. `--yes` allein graemt die bestatigung nicht ab
(Spezifikation: "--yes alone does not supply those acknowledgements").
Der full-reset (loescht auch keycloak/openbao/postgres des targets) ist daher ueber SSH
nicht als CLI-lauf reproduzierbar.

## 4b Manuelle bereinigung (alternativ, dokumentiert) — demoapp-containeren entfernt
Die demoapp-Container wurden gestoppt und entfernt (das eigentliche werkzeug des lanes):
```
podman stop -t0 \
  bh-w0427-owner-missing-demoapp-dev-app \
  bh-w0427-owner-missing-demoapp-dev-baseharbor-internal-exposure-web
podman rm -f -t0 \
  bh-w0427-owner-missing-demoapp-dev-app \
  bh-w0427-owner-missing-demoapp-dev-baseharbor-internal-exposure-web
```
Ergebnis nach bereinigung:
- demoapp-container count: 0
- `podman ps -a --filter name=demoapp` -> leer

## 4c Cleanliness — Host-Zustand (WITNESS)
Basislinie: host fresh (0 container). Ambient-volumes (Hash-volumes +
`bh-w0427-owner-missing-shared_postgres-data-1`) sind build-baseline und bleiben.

Container (nach demoapp-removal): demoapp = 0.
Die Core-instanz (openbao/postgres/keycloak/gateway des targets) lief noch als
vollstaendige managed installation — deren destroy ist der consent-gate full-reset
(4a) und konnte nicht ueber SSH durchgefuehrt werden.

Volumes: 6 local volumes vorhanden, davon die 5 hash-volumes ambient +
1 postgres-data-volumen der core-instanz. Keine demoapp-volumina (pure-client, kein sql).

df (belegt, kein vollstandiger "clean" pointer):
```
/dev/sda1   96G  43G  54G  45% /
```

## Fazit Zelle 4
- Full-reset (destroy) BLOCKED an consent-gate (nicht ueber SSH repro); dokumentiert.
- demoapp-containeren manuell entfernt (0 demoapp-container).
- Cleanliness-Nachweis: demoapp-cont=0; ambient-volumes als baseline erhalten; df dokumentiert.
  Vollstaendiger core full-reset (keycloak etc.) erst beim owner mit echter tty-vernichtung —
  als separate action/karte vermerkt, nicht als fake-clean behauptet.

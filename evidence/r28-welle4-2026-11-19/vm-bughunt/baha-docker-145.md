# Bug-Hunt Akte: baha-docker-145

**Karte:** t-20261119-r28-bughunt-observability-desk (0428-147)
**ROLLE:** BUG-HUNT-BAHN — reine Befundung, kein Produkt-Change, kein PR
**Datum:** 2026-11-19
**Host:** baha-docker (SSH, nicht die Session-Host)

## PLAN

- Planning-Repo-Clone in /var/tmp verifizieren, fetch + rebase origin/main, ls-remote Zeugnis, Base-SHA als Ancestor
- vm-lock fuer baha-docker ueber coordinator/scripts/vm-lock.sh holen
- baha aus dem mergten develop-Base (c296086...) in einem /tmp-Worktree bauen
- Szenario 1: Application mit ZWEI log-sources; datasource-health + perses status pro Quelle, fail-closed
- Szenario 2: zweite Quelle kaputt (Port 5xx); quellenspezifische Fehlermeldung
- Szenario 3: Production LOG writer class application, tauchen Logs am Loki-Pfad auf?
- Szenario 4: Doku-vs-Verhalten (docs/de + docs/en), Abweichungen mit file:line
- Evidence-Akte schreiben
- vm-lock release, compose DOWN, cleanliness-liste, ls-remote Zeugnis
- Evidence an origin/main pushen, END_DONE posten

## Basis-Attestation

- Planning-Repo origin/main (ls-remote): ad94a0db1c72abda39b5bcd937c97504441f76f1
- Base-Ref (develop baha): c296086ca1e35ef3212d293afc94d7bebcd1690f
  - 1019190d8dc0ecac7693f3461153e76be0e2cb8a ([0428-084] Perses lifecycle)
  - fac01c77276ca2bf1e20cd0b7334bda5dd43e353 ([0428-122] production LOG writer)
  - [0428-086] Perses Loki datasource source adapter (PR #1616)
- Die Base-SHA ist Ancestor meiner eigenen (evidenz-）Änderungen; keine fremden Commits im eigenen log

## Sauberkeit / cleanliness

- vor: <docker ps -a, netzwerke, volumes>
- nach: <docker ps -a, netzwerke, volumes>

## Befund -> vorgeschlagene Karte

| Befund | Schwere | vorgeschlagene Karte |
| --- | --- | --- |
| (noch) | | |

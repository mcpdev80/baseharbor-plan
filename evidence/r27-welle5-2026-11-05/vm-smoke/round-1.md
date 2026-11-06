# w199 — VM smoke Docker+Podman (t-20261104-r27-vm-smoke-docker-podman), round 1

Lane: w199 (Worker). Coord: 841e7734. Kart: t-20261104-r27-vm-smoke-docker-podman (RUNDE 1).
Art: operativer echt-VM-smoke, kein Produkt-Write-Set. Evidence nur in baseharbor-plan.

## PLAN

- 1) Karte voll lesen, Revision/Baupfad der geprueften Quellrevision bestimmen — erledigt
- 2) Evidence-Datei anlegen (diese Datei) — erledigt (dieser Akt)
- 3) Host-Reconciliation: baha-podman nicht erreichbar; baha-runner-docker-2 ist docker-only — QUESTION gemeldet
- 4) Beide Hosts: ALTER BESTAND weg (de-/installieren + binary + datenverzeichnisse), Loschungs-Zeugen
- 5) Beide Hosts: NEU bauen/installieren aus der geprüften Quellrevision; `baha --version`-Beleg vor dem Smoke
- 6) Docker-Host: frischer Stack, Geraet anmelden, Dienst beobachten — Befehle + WORTLAUT in die Akte
- 7) Podman-Host: ebenso
- 8) Negative Probe: abgemeldetes Geraet wirkungslos auf beiden Hosts (Smoke-Tiefe)
- 9) ENDE-RAUMLIBERUNG je Host: baha => not found, ps/df-Zeile, unit-listing OHNE baseharbor
- 10) Evidence nach origin/main pushen, ls-tree-Zeuge in die Akte; END posten

## STATUS: BLOCKED (STOP-Kriterium des Auftrags: "VM nicht erreichbar") — erste Aktion, nichts veraendert

### Revisions-/Baupfadbestimmung (Punkt 1)

Karte-Kandidaten: t-20261104-r27-device-lifecycle wurde in develop gemergt (PR #1394, Merge `21d8d05c`;
Round-3-Akzeptanz-Kandidat `fee055bffc5b8a3002d392c0d67ac7e9ba33c460`, ist Vorfahr von origin/develop).
Node-Service-Kette: t-20261104-r27-journal-wiring (PR #1392/#1393-Kette, Round-3-Akte gem. kanban review->active
am 2026-11-06 noch in Arbeit auf `work/r27-journal-wiring`).

Geplante Baubasis: `origin/develop` = `f01d2fbdea6b93af6e06ca6297d04065b6acf701` (enthaelt die akzeptierte
Geraete-Lebenszyklus-Kette; t-20261017-release-0-4-27-updates ist accepted).
Build-Pfad der Karte/Notes (Torregel: 0.4.23 zaehlt nicht, es ist auf keinem Host ein passendes baha
installiert — siehe Befund B): Quellbau analog w116/w121:

```
git checkout <rev>
go build -trimpath -ldflags "-s -w -X main.version=v0.4.27 -X main.revision=<rev> -X main.commit=<rev>" -o ./bin/baha ./cmd/baha
```

(Notes-Präzedenz: `baha --version` liefert dann `BaseHarbor <rev>` / `commit <rev>`, rc=0; Install nach
`~/.local/bin/baha`, PATH vor /usr/bin, gem. w116 w116-Akte.)

### Befund A — baha-podman (192.168.6.148) ist nicht erreichbar (STOP-Kriterium)

Wortlaut (mehrfach, ueber ~10 Minuten, Port 22 per nc offen, SSH-Banner haengt):

```
$ ssh baha-podman 'echo OK-podman; hostname'
Connection timed out during banner exchange
Connection to 192.168.6.148 port 22 timed out
```

`ping -c 2 -W 2 192.168.6.148` -> 0% packet loss (Host lebt auf Netz-Ebene); `nc -z 192.168.6.148 22` ->
"succeeded" — d. h. tcp-accept aber kein sshd-Banner (Runbook-Verdacht: haengender sshd/netns-Zustand,
RUNBOOK Zeile 320). Lane darf/gemäss Scope keine Runner-/Infra-Reparatur; VM-Zugriff ist Owner-Bereitstellung.

### Befund B — Hostnomenklatur laeuft auseinander (Reconciliation noetig)

```
$ ssh baha-docker 'hostname; docker --version; podman --version; baha --version'
baha-runner-docker
Docker version 29.8.1, build 4a63305
bash: line 1: podman: command not found
bash: line 1: baha: command not found

$ ssh baha-runner-docker-2 'hostname; docker --version; podman --version; baha --version'
baha-runner-docker-2
Docker version 29.8.1, build 4a63305
bash: line 1: podman: command not found
bash: line 1: baha: command not found
```

- Der Missionstext nennt die Hosts `baha-runner-docker` / `baha-runner-podman`; die ssh-config (Owner-
  bereitgestellter Zugang) kennt nur `baha-docker` (-> 192.168.6.166, real `baha-runner-docker`),
  `baha-podman` (-> 192.168.6.148, toter Banner) und `baha-runner-docker-2`/`baha-runner-podman-2`
  (192.168.6.119, docker-only; -podman-2 nicht aufloesbar: "Temporary failure in name resolution").
- Einen erreichbaren PODMAN-Host gibt es aktuell NICHT. Ein Podman-Smoke ist ohne Owner-Zugangs-/Host-
  entscheidung nicht ausfuehrbar. Diese Lane baut oder repariert keine Runner-/Host-Infra (Scope).

### Was NICHT getan wurde (bewusst, bis Reconciliation)

Kein Build, keine Installation, keine Stack-Aktion, kein Loeschen auf irgendeinem Host: die Mission verlangt
den Smoke auf BEIDEN Hosts als EINErn Durchgang mit End-Raumluiberung; der Docker-Teil wuerde sonst als
halber Lauf ohne den zugehoerigen Podman-Negativbeleg enden und die VMs im installierten Zustand belassen.

### Naechster Ausloeser

Antwort des Coordinators auf die QUESTION (Host-Reconciliation: alternativen Podman-Host benennen
oder `baha-podman` wieder erreichbar machen; Bestaetigung der Baurevision origin/develop f01d2fbd
vs. Journal-/Streams-Kopf), danach Schritte 4–10 in einem Durchgang.

END_BLOCKED w199-vm-smoke: podman-host=unreachable (ssh-banner-timeout 192.168.6.148, Wortlaut oben) |
docker-host baha-docker ok (Docker 29.8.1, kein baha installiert) | nichts installiert/veraendert,
STOP-Kriterium "VM nicht erreichbar" + Hostnamens-Dissonanz gemeldet

## Erganzung: Basis-Attestation und Veroeffentlichungs-Zeuge

Basis-Attestation (kein Branch noetig — Evidence-only-Akt direkt auf main, kein Produkt-Write-Set):
`git -C baseharbor-plan rev-parse origin/main` -> `697436141b14cc43840b342691fbc42f7769966c`
(Stand beim Anlegen dieses Aktes; commit-toi darauf, also Vorfahr meines ersten Commits).

Veroeffentlichungs-Zeuge (zweitletzte Aktion, Befehl + exakte Ausgabe):

```
$ git ls-tree origin/main -- evidence/r27-welle5-2026-11-05/vm-smoke/round-1.md
100644 blob 1c27a143fbbd9babb5b29ae212e03417fd7aea2f	evidence/r27-welle5-2026-11-05/vm-smoke/round-1.md
```

Push-Zeuge: `67d47d0..ef1c125  main -> main`; nach dem Push verifiziert:
`git ls-tree origin/main -- evidence/r27-welle5-2026-11-05/vm-smoke/round-1.md` ->
`100644 blob 85660139b42dd65eb194776500ce87c9a72170f2  evidence/r27-welle5-2026-11-05/vm-smoke/round-1.md`
(Referenz ist der lokale Remote-Tracking-Stand nach erfolgreichem Push; direktes `ls-remote` scheitert an
zeitweiligem GitHub-443-Ausfall von diesem Host, der auch den ersten Push-Versuch betraf — der Push selbst
ging in Versuch 1 der Wiederholungsschleife als `main -> main` durch.)

Letzter Erreichbarkeits-Check vor END (baha-podman, unveraendert tot):

```
$ ssh -o ConnectTimeout=18 baha-podman 'echo OK-podman; hostname'
Connection to 192.168.6.148 port 22 timed out
```

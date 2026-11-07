# baha-podman-2 (107) Neuaufbau — lane w283

**Lane:** w283-podman2-rebuild  **Coord:** 594fd2f5  **Karte:** t-20261104-r27-vm-rebuild-integration (0427-108)
**Mission:** coordinator/missions/w283-podman2-rebuild.txt  **Zone:** workers/w283-wt, caches /tmp/opencode/w283*

## PLAN

- Realitaetsabgleich: planning origin-main + host-status; VM-lock claim baha-podman-2 @ w283 (host MUSS frei+leer)
- drei-Punkte-Pruefung vor Zerstoerung (aktive runs? container/volumes/netns + ownership? shared-stapel)
- setup-skript auf 107 finden/lesen; build-cache-basis
- Neuaufbau ueber go build aus AST; skript-abreichungen als diff dokumentieren
- rauchprobe 4/4: version, rootless rc=0, port-mapping, build-cache
- rueckbau probe=0 (my containers/volumes/networks=0, shared unangetastet)
- vm-lock release + akte + evidence origin/main; END

## EVIDENCE-STATUS

- planning origin-main: aff1532c2f6c6782a8c13afad83245d1351815e7 (git ls-remote origin main, baseharbor-ecosystem/baseharbor-plan)
- branch-base (attestiert): aff1532c2f6c6782a8c13afad83245d1351815e7 = origin/main, ancestor meiner Commits (git merge-base --is-ancestor origin/main HEAD => JA)
- planning origin-main nach Commit: <ls-remote unten>

## STATUS

DONE — baha-podman-2 aus AST c87c8b644cc neu aufgebaut, rauchprobe 4/4 gruen, lane-eigene Restlos auf 0,
shared-stapel auf 107 unangetastet, vm-lock released.

## 1. IST-BEFUND (vor Neuaufbau)

- Host: baha-podman-2 = 192.168.6.107 (SSH-Alias baha-podman-2, user marcel, mcp-home). BatchMode alive.
- storage: rootless=true, driver=overlay, rootlessNetworkCmd=pasta, podman 5.7.0.
- vor run: 0 container, 1 network (default `podman` bridge), 5 volumes (alle lane-external); 55G freier Platz (44% belegt); 6.5 GiB available.
- installiertes `baha` (vorher): BaseHarbor c87c8b644cc98fe6abf1164d101f42a212558b9d, built 2026-11-07 (source build, nicht auf PATH).
- go auf host: go1.26.9 linux/amd64 vorhanden.

## 2. DREI-PUNKTE-PRUEFUNG (vor jedem destruktiven Schritt)

Punkt 1 — aktive runs: NONE (podman ps => leer; 0 container).
Punkt 2 — shared vs lane-eigen: 0 bh-* container/volumes von mir; die 5 volumes + 1 netze sind lane-external (Voreinstellung), keine bh-*-shared* / ci-bootstrap auf 107 vorhanden. Shared-stapel-Befund: KEIN shared-stapel auf diesem host (keine bh-* anywhere) => nichts zu schonen, nichts gefaehrdet.
Punkt 3 — Wiederherstellungsfolge: kein w283-state, keine lane-eigene volume => nichts wiederherzustellen.
Ergebnis: host ist sauber/neu; kein destruktiver eingriff noetig. Kein `podman system reset` (Drei-Punkte-Pruefung nicht noetig, host war leer).

## 3. SETUP-SKRIPT (Finden + Lesen + skript-diff)

- Gesuchtes `/home/marcel/setup-baha-podman.sh` (Weg der vorgaenger lane w117, SHA ce1a1b9c): **NICHT vorhanden** auf 107 (vollständige home-suche, /root, .config, .bash_history => leer).
- Auf 107 gibt es KEINEN dauerhaften host-setup-skript. Der host wurde 2026-11-07 03:0x ad-hoc eingerichtet (backup-spuren: `baha.c87c.prebuild`, `baha.bak.ed98ed1d7`).
- Rebuild daher reproduzierbar aus dem source AST unter test: `~/baseharbor-build` (git checkout c87c8b644cc, clean status) => `go build -ldflags ... -o ~/.local/bin/baha ./cmd/baha`.
- skript-diff (gegen w117-prozep + card-version-finding):
  - w117: setup-skript installiert `baha 0.4.23` + Target `podman-test` + Core `--control-plane-only`.
  - w283 (107): kein skript => rebuild nur aus AST go build; KEIN Target/Control-plane-deploy (auftrag = saubere umgebung + runtime-rauchprobe, NICHT core-deploy).
  - abweichung dokumentiert, nicht still (mission: skript-abweichungen als diff, nicht still).
  - abweichung: build ueber `go build` (source), nicht ueber repo `scripts/install.sh` (download release-binary); beide Wege dokumentiert, go-build gewaehlt, weil (a) host AST c87c8b644cc kein release-tag ist und (b) die card verlangt: host soll binary aus source-revision unter test testen.

## 4. NEUAUFBAU

- backup: `cp -a ~/.local/bin/baha ~/.local/bin/baha.w283.prebuild.bak`
- build: `go build -ldflags "-X main.version=c87c8b644cc -X main.commit=c87c8b644cc98fe6abf1164d101f42a212558b9d -X main.date=2026-11-07" -o ~/.local/bin/baha ./cmd/baha` => **rc=0**
- install verify: `baha --version` => BaseHarbor c87c8b644cc / built 2026-11-07
- AST-match: c87c8b644cc = origin/main HEAD-linie (develop v0.4.27 line).

## 5. RAUCHPROBE (4/4 gruen)

1. version: `baha --version` => `BaseHarbor c87c8b644cc98fe6abf1164d101f42a212558b9d` (commit c87c8b644cc, built 2026-11-07). GRUEN.
2. rootless run ohne sudo: `podman run --rm docker.io/library/alpine:latest true` => **rc=0**, kein sudo verwendet. GRUEN.
3. port-mapping-test (netavark/pasta `cannot assign`-gegenbeweis): `podman run -d --name w283-pmp -p 127.0.0.1:54321:5432 alpine sleep 60` => rc=0; `connect_ex(('127.0.0.1',54321))` => **rc=0 => REACHABLE**; `podman rm -f w283-pmp` => rc=0 (sauber). GRUEN.
4. build-cache-test: go cache geleert => COLD build **21.6s**; wiederholt => WARM build **1.0s** (cache-hit belegt; identische binary-size 52095233 bytes). GRUEN.
Ergebnis: **4/4 gruen**.

## 6. RUECKBAU (probe=0)

- lane-eigene restlos: w283-pmp bereits entfernt; keine w283-named container/volumes/netze verbleiben.
- null-pruefung (ps/df-witness): my containers=0, my volumes=5 (lane-external, unangetastet), my networks=1 (default bridge, unangetastet).
- shared-stapel: 0 bh-* container/volumes auf 107 — unangetastet (vorher/nachher identisch).
- ps-witness: `podman ps -a` => 0 container; keine bh-*/*-container von mir.
- df nachher: `/dev/sda1 96G 42G 55G 44% /` (vorher 44%, unveraendert).
- temp-probes /tmp/w283-* auf host entfernt.

## repo-rule compliance

- Kein produkt-code veraendert (reine host-probe + go build aus AST, RUNBOOK 4.0/6.7).
- Kein .github veraendert, kein runner/infra angefasst.
- Kein container auf coordinator-host der session (build+install+probe nur auf 192.168.6.107; /tmp/opencode/w283*.sh nur als ssh-input, kein container).
- lane-eigene container/volumes/netze rueckgebaut (probe=0: 0 container).
- shared-stapel bh-*-shared* / ci-bootstrap: auf 107 nicht vorhanden, unangetastet.
- Keine VM-zelle als dauerhafter test-traeger (owner-direktive 2026-11-07).

## END

END_DONE w283-podman2-rebuild: aufbau=go-build-rc0 (AST c87c8b644cc) rauchprobe=4/4 gruen container-end=0 (0 container, 0 bh-) journal=w283-claim+w283-release skript-diff=keine-skript-vorhanden;rebuild-aus-AST- dokumentiert akte=baseharbor-plan/evidence/r27-welle5-folge-2026-11-06/infra/podman2-rebuild-2.md

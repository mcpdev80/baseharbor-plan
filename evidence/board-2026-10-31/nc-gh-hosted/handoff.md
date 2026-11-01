# Mission nc-gh-hosted — Node-Connector-CI 100% GitHub-hosted (Rootless-Annahmen raus)

Lane: work/nc-gh-hosted (baseharbor-node-connector), basis origin/main b39f890ae541134c27f186c966cd232a3ec13d58
Write-set: nur .github/workflows/source.yml, .github/workflows/release-integration.yml

## PLAN (Stand 2026-11-01)
1. [x] Schritt 0: Realitätsabgleich — Remote-Stand, Branch, Task-Note, bestehende Evidence lesen
2. [x] source.yml: Rootless-Vorbereitung (loginctl-linger / systemctl --user show-environment) für GH-hosted umstellen (transport + enrollment Jobs)
3. [x] release-integration.yml: gleiche Umstellung (qualification Job)
4. [x] actionlint + YAML-Check (beide grün)
5. [x] workflow_dispatch auf Branch observiert (Eigenes-Run-Pflicht): GH-hosted, podman läuft (rootful, rootless=true, cgroup_manager=systemd)
6. [x] Evidence + PR + push + ls-remote, END posten

## Befunde Schritt 0
- Branch work/nc-gh-hosted = origin/main b39f890ae541134c27f186c966cd232a3ec13d58, noch nicht auf Remote (git ls-remote leer).
- Rootless-Unmöglichkeit empirisch belegt durch gh-ci-core: ubuntu-latest `unshare --user` -> "/proc/self/uid_map: Operation not permitted" (run 41255597778), auch nach sudo sysctl-Lift; rootful/system docker grün ("Hello from Docker!").
- Plan-Schema hat keinen Task "nc-gh-hosted" (Mission ist Board-Lane board-2026-10-31); nc-3 bleibt unverändert (andere Lane/Owner, kein Claim übernommen).
- source.yml Jobs `transport`/`enrollment`: "Prepare rootless Podman" mit loginctl-linger + user@$uid.service + show-environment + Rootless==true-Assert. release-integration.yml qualification: gleicher Block (folded-scalar Stil).
- "Prepare verified rootless Docker" in release-integration.yml ruft .browser-core-source/scripts/ci-core-rootless-runtime.sh aus dem baseharbor-Repo-Auscheck auf — NICHT im Write-Set (baseharbor/* andere Lane); nicht angefasst, hier dokumentiert.

## Änderungen
- Beide Workflows: Schritt heißt "Prepare Podman (GitHub-hosted)".
  - `command -v podman` sonst apt-get install podman (ohne rootless-Setup); ubuntu-latest ≥24.04 hat podman vorinstalliert.
  - Ast `RUNNER_ENVIRONMENT == github-hosted`: kein loginctl-Dance (GH-hosted kann keinen user-Session-Dienst bereitstellen — dokumentiert); podman-Lauf nativ (rootful), Fallback `podman --cgroup-manager=cgroupfs` gemäß Missions-Wissen.
  - Sonst (self-hosted): bisheriger Rootless-Pfad erhalten.
- source.yml: `workflow_dispatch.inputs.runtime` (choice podman|docker, default podman); transport-Job-if erweitert um Dispatch-Fall, Matrix respektiert das Input — ermöglicht beobachtbaren Einzel-Gate-Lauf ohne neue Produkt-CI.
- Kein Code geändert (Go/tests unangetastet).

## Checks
- python3 yaml.safe_load: beide Dateien OK. actionlint .github/workflows/*.yml: ohne Befunde.

## Hosting-Nachweis (Eigenes-Run-Pflicht, alle selbst beobachtet bis terminal)
- Kandidaten-Shas: 3de8eb542217dfe6665e57b9ec41d8c98e613c9f, final 4aa41acccb58114e6aa3084474142f77f2b1b124 (PR #17 HEAD).
- git ls-remote origin work/nc-gh-hosted -> 4aa41acccb58114e6aa3084474142f77f2b1b124 (Zeuge im Transcript).
- Run 41261879476 (workflow_dispatch, runtime=podman, @3de8eb5): jobs: transport·podman SUCCESS (1m54s, ubuntu-24.04), source SUCCESS, enrollment skipped. TestConnectorRuntimeTransport PASS (70.41s) mit podman auf GH-hosted, ohne loginctl-Dance.
- Run 41262442519 (workflow_dispatch, runtime=podman, @4aa41ac): SUCCESS. Prepare-Schritt-Log: "::notice podman GH-hosted mode: default (rootful) OK" und "runtime cgroup_manager=systemd rootless=true" => podman läuft GH-hosted nativ (vorinstalliert, apt-Fallback nicht nötig), kein cgroupfs-Fallback nötig.
- PR-Run 41262420312 @4aa41ac: source check pass; transport/enrollment-Jobs korrekt skipped (push-only ifs).
- Kann-jeder-Schritt-Check: keine Tokens/Pins/ENV durch diese Lane gesetzt; Auth kommt vom System-gh des Hosts, dispatch nur `gh workflow run -f runtime=podman` (Pflichtinput).

## Befunde/Grenzen (nicht blockierend)
- Der GH-hosted podman-Lauf ist rootless im podman-Sinne (rootless=true, geteilte userns des Hosts nutzbar für Container), aber der user-Session-Dienst (loginctl/user@.service/dbus show-environment) ist auf GH-hosted NICHT verfügbar — genau der Dance ist raus.
- release-integration.yml "Prepare verified rootless Docker" ruft baseharbor/scripts/ci-core-rootless-runtime.sh (sysctl-Lift + dockerd-rootless-setuptool — auf GH-hosted nach gh-ci-core empirisch unmöglich). Datei liegt in baseharbor/* = anderes Write-Set, hier nur dokumentiert; Docker-Pfad des qualification-Jobs nutzt danach regulär `docker build/pull` (rootful, funktioniert laut gh-ci-core run 41255597778).
- enrollment-Job-Asserts erwarten wörtlich "rootless Quadlet"-Stringe in Core-Go-Tests; falls Go-Code das Wort/Verhalten an rootful anpasst, ist das ein Interface-Thema außerhalb dieses Write-Sets (Missionspunkt 4: kein Code-Change hier).

## repo-rule compliance
- Write-Set eingehalten: nur .github/workflows/source.yml + release-integration.yml (diff-Stat: 2 files).
- Kein baseharbor/* angefasst; nc-3/t-20261018-r27 Claims unangetastet (andere Lanes).
- Geflusste Änderungen gezielt committet (git add <datei>, kein -A).

## END
END_DONE nc-gh-hosted: 4aa41acccb58114e6aa3084474142f77f2b1b124, PR #17 (baseharbor-node-connector), podman GH-hosted: VERIFIZIERT GRÜN (dispatch run 41262442519: default/rootful OK, rootless=true, cgroup_manager=systemd; rootless-Annahmen und loginctl-Dance raus; transport-Gate auf GH-hosted PASS 70.4s).

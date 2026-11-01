# Mission nc-gh-hosted — Node-Connector-CI 100% GitHub-hosted (Rootless-Annahmen raus)

Lane: work/nc-gh-hosted (baseharbor-node-connector), basis origin/main b39f890ae541134c27f186c966cd232a3ec13d58
Write-set: nur .github/workflows/source.yml, .github/workflows/release-integration.yml

## PLAN (Stand 2026-11-01)
1. [x] Schritt 0: Realitätsabgleich — Remote-Stand, Branch, Task-Note, bestehende Evidence lesen
2. [x] source.yml: Rootless-Vorbereitung (loginctl-linger / systemctl --user show-environment) für GH-hosted umstellen (transport + enrollment Jobs)
3. [x] release-integration.yml: gleiche Umstellung (qualification Job)
4. [x] actionlint + YAML-Check (beide grün)
5. [ ] Wenn möglich: workflow_dispatch auf Branch, Run beobachten (Eigenes-Run-Pflicht): GH-hosted, podman läuft
6. [ ] Evidence + STATUS aktualisieren, push, END posten

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
- python3 yaml.safe_load: beide Dateien OK.
- actionlint .github/workflows/*.yml: ohne Befunde.

## END
(offen — END_DONE|END_BLOCKED nc-gh-hosted: <SHA + PR# + podman GH-hosted status>)

# Provisionierung Docker-PruefVM #2 (baha-docker-2)

- Lane: w253-provision-docker2 (Worker)
- Koordinator: 841e7734
- Karte: w253 — zweite DOCKER-PRUEFVM provisionieren (reine Infrastruktur, kein Produktkarte)
- Zielhost: baha-docker-2 = 192.168.6.205 (hostname baha-runner-docker-2, user marcel, sudo nopasswd, Ubuntu 26.04 resolute amd64, git 2.53)
- Zielbild: docker-ce 29.x aus download.docker.com-Repo, containerd, buildx, docker-compose-plugin, daemon active, marcel in docker-gruppe. Rootless NICHT noetig.
- Status: DONE

## PLAN

- Provisionierungs-Skript lokal in /tmp/opencode/w253/ schreiben
- Skript nach baha-docker-2:/tmp/ scp-en
- Auf VM ausfuehren (docker.sources fixen, keyring dearmoren, docker-ce + buildx + compose-plugin install, daemon enable, marcel in docker-gruppe)
- Skript auf der VM loeschen
- Nachpruefung als marcel OHNE sudo (neuer ssh-login)
- Akte in baseharbor-plan evidence schreiben, origin/main pushen
- END an Coordinator posten

## Befund (Ausgangslage)

- /etc/apt/keyrings/docker.asc vorhanden (2760 Bytes) — aber BINARY OpenPGP, nicht ASCII-armored
- /etc/apt/sources.list.d/docker.sources malformed: `Suites:` leer => apt update schlaegt fehl
- docker-ce auf VM NICHT installiert
- marcel NICHT in docker-gruppe (groups: marcel,adm,cdrom,sudo,dip,lxd)
- systemctl is-active docker => inactive

## Zwei Wurzelursachen (behebt den fehlerhaftencoord-Versuch)

1. docker.sources hatte leere `Suites:` Zeile. Fix: Suite = `$( . /etc/os-release; echo $UBUNTU_CODENAME )` = `resolute` (anhand der working VM baha-docker/166 verifiziert).
2. /etc/apt/keyrings/docker.asc war ein BINARY OpenPGP-Schlüssel. APT's `Signed-By` akzeptiert aber nur ASCII-armored `.asc` oder dearmertes `.gpg` => Fehler:
   `the key(s) in the keyring /etc/apt/keyrings/docker.asc are ignored as the file has an unsupported filetype`
   und `repository 'https://download.docker.com/linux/ubuntu resolute' is not signed`.
   `gpg --dearmor` lieferte auf dieser Box ebenfalls binär aus. Behoben durch Abruf des offiziellen Schlüssels über HTTPS:
   `curl -fsSL https://download.docker.com/linux/ubuntu/gpg` => 3817 Bytes, ASCII-armored, Fingerprint `9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88` (identisch zur working VM baha-docker/166). In /etc/apt/keyrings/docker.asc installiert (chmod 644).

## Nachweis — Befehle, Ausgaben, Zeitstempel

- zeitstempel: 2026-11-06, VM hostname baha-runner-docker-2

### Fix docker.sources + keyring + install

- befehl: curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc
- ausgabe: file => `PGP public key block Public-Key (old)`; head => `-----BEGIN PGP PUBLIC KEY BLOCK-----`; fingerprint `9DC858229FC7DD38854AE2D88D81803C0EBFCD88`
- befehl: sudo tee /etc/apt/sources.list.d/docker.sources (Suites: resolute)
- ausgabe:
  Types: deb / URIs: https://download.docker.com/linux/ubuntu / Suites: resolute / Components: stable / Architectures: amd64 / Signed-By: /etc/apt/keyrings/docker.asc
- befehl: sudo apt-get update && sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
- ausgabe: install 5 packages: containerd.io 2.4.2-3~ubuntu.26.04~resolute, docker-ce-cli 5:29.9.3, docker-ce 5:29.9.3, docker-buildx-plugin 0.38.1, docker-compose-plugin 5.7.0
- befehl: sudo systemctl enable --now docker && sudo usermod -aG docker marcel
- ausgabe: daemon enabled; group docker:x:986:marcel (gid 986)

### Nachpruefung am ENDE (marcel OHNE sudo, frischer login-shell)

- befehl (ssh bash -lc): docker run --rm hello-world
- ausgabe: `Hello from Docker!` (Image hello-world:latest gezogen und ausgeführt)
- befehl: docker compose version
- ausgabe: `Docker Compose version v5.7.0`
- befehl: systemctl is-active docker
- ausgabe: active
- befehl: getent group docker
- ausgabe: docker:x:986:marcel  (marcel gelistet — in frischem login-shell aktiv, gruppe gilt ohne sudo)
- befehl: docker --version
- ausgabe: Docker version 29.9.3, build 5457199
- befehl: ps -C dockerd -o pid,user,cmd
- ausgabe: PID 29825 root /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock

## VM-Hygiene

- skript auf VM nach ausführung geloescht: `rm -f /tmp/provision-docker2.sh; rm -rf /tmp/dl`
- witness: `ls /tmp/provision-docker2.sh` => `No such file or directory`
- keine weiteren VMs angefasst (baha-docker/baha-podman/baha-podman-2 verschont)
- VM ist (noch) NICHT im vm-lock-pool; aufnahme in vm-lock/vm-audit durch COORDINATOR

## Git / evidence

- base attestiert (origin/main HEAD): d2063b298694ae9dca90d57e17f3ba2178fc852b
- anzestrickette: commit dfe0f45072d5381690ad6dd907dd2619ebec8e8c, parent = d2063b298694ae9dca90d57e17f3ba2178fc852b (direktes kind, keine fremden commits)
- git merge-base --is-ancestor d2063b2 HEAD => OK
- ls origin/main BEFORE push: evidence path nicht vorhanden (erwartet)
- ls origin/main AFTER push (git ls-tree -r --name-only origin/main):
  evidence/r27-welle5-folge-2026-11-06/infra/provision-docker-vm-2.md
- push: git push origin HEAD:main => d2063b2..dfe0f45  HEAD -> main
- committet NUR diese eine datei (targeted git add), keine produkt-repo-infrastruktur

## END-Protokoll

- END an 841e7734:
  END_DONE w253-provision-docker2: docker=29.9.3 daemon=active compose=v5.7.0 hello-world=OK marcel-in-dockergruppe=JA akte=baseharbor-plan/evidence/r27-welle5-folge-2026-11-06/infra/provision-docker-vm-2.md (auf origin/main) | zwei Wurzelursachen behoben: leere docker.sources-Suite (=>resolute) + binary docker.asc keyring (=> official ARMORED key via HTTPS). VM-Hygiene: skript geloescht, andere VMs verschont.

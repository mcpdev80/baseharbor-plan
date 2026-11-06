# Provisionierung Docker-PruefVM #2 (baha-docker-2)

- **Lane:** w253-provision-docker2 (Worker)
- **Koordinator:** 841e7734
- **Karte:** w253 — zweite DOCKER-PRUEFVM provisionieren (reine Infrastruktur, kein Produktkarte)
- **Zielhost:** baha-docker-2 = 192.168.6.205 (hostname baha-runner-docker-2, user marcel, sudo nopasswd, Ubuntu 26.04 resolute amd64)
- **Zielbild:** docker-ce 29.x aus download.docker.com-Repo, containerd, buildx, docker-compose-plugin, daemon active, marcel in docker-gruppe. Rootless NICHT noetig.
- **Status:** active

## PLAN

- Provisionierungs-Skript lokal in /tmp/opencode/w253/ schreiben (docker.sources mit Suites=$UBUNTU_CODENAME)
- Skript nach baha-docker-2:/tmp/ scp-en
- Auf VM ausfuehren: sudo bash /tmp/<file> (docker.sources fixen, docker-ce + buildx + compose-plugin install, daemon enable, marcel in docker-gruppe)
- Skript auf der VM loeschen
- Nachpruefung als marcel OHNE sudo: docker run hello-world, docker compose version, systemctl is-active docker, getent group docker (neuer ssh-login)
- Akte in baseharbor-plan evidence schreiben, origin/main pushen
- END an Coordinator posten

## Ausgangalage (befund)

- /etc/apt/keyrings/docker.asc vorhanden (2760 Bytes, OK)
- /etc/apt/sources.list.d/docker.sources malformed: `Suites:` leer => apt update schlägt fehl
- docker-ce auf VM NICHT installiert (which dockerd => nichts)
- marcel NICHT in docker-gruppe (groups: marcel,adm,cdrom,sudo,dip,lxd)
- systemctl is-active docker => inactive

## Referenz (baha-docker/166, working)

- korrekte docker.sources: `Suites: resolute`
- Diese Zeile diente als Vorlage für die Korrektion.

## Vorgehen

- Skript-DATEI scp-en (kein verschachtelter Heredoc, gemäß Mission)

## Nachweis — Befehle, Ausgaben, Zeitstempel

### 1. Provisionierungs-Skript (lokal)

- befehl: cat /tmp/opencode/w253/provision-docker2.sh
- inhalt:
  ```
  #!/usr/bin/env bash
  set -euo pipefail
  cat > /etc/apt/sources.list.d/docker.sources <<'EOF'
  Types: deb
  URIs: https://download.docker.com/linux/ubuntu
  Suites: $( . /etc/os-release; echo $UBUNTU_CODENAME )
  Components: stable
  Architectures: amd64
  Signed-By: /etc/apt/keyrings/docker.asc
  EOF
  ```
  (Hinweis: die Suites-Zeile muss expandiert werden => Heredoc ohne Quotes)

### 2. scp nach baha-docker-2

### 3. ssh sudo bash /tmp/provision-docker2.sh

### 4. skript auf VM loeschen

## Nachpruefung (marcel OHNE sudo)

- docker run --rm hello-world => "Hello from Docker!"
- docker compose version => Version
- systemctl is-active docker => active
- getent group docker => marcel gelistet

## Git / Evidence

- base attestiert: <SHA> (origin/main)
- ls origin/main BEFORE evidence push
- ls origin/main AFTER evidence push

## END-Protokoll

- END an 841e7734

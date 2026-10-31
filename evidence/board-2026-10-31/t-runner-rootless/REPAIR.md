# REPAIR — Rezept für Owner (recipe_for_owner)

## REPARATUR-STATUS: recipe_for_owner (Owner/root-Rechte nötig; Skript-Defekt)

## Zusammenfassung der Root-Cause
Die self-hosted rootless Runner (`baha-runner-docker-2`, `baha-runner-podman-2`) sind infra-technisch
**gesund**: Docker 29.8.1 bzw. Podman 5.7.0 rootless installiert, `Linger=yes`, Services `enabled`,
`docker`/`podman run hello-world` laufen. Der CI-Step "Prepare verified rootless runtime"
(`scripts/ci-core-rootless-runtime.sh`) scheitert, weil das Skript für einen **nicht-rootless**
Runner geschrieben ist: es fordet `test "$(id -u)" -ne 0` (also github-runner) und ruft danach
`sudo apt-get update …` auf — `github-runner` hat aber auf beiden Hosts **kein sudo**
(`sudo -l` → "may not run sudo"). Erster `sudo`-Aufruf → `sudo: I'm sorry github-runner. I'm afraid I can't do that`
→ Skript bricht ab (Exit 1). BEIDE Runner identisch betroffen.

## Warum kein Host-Fix durch mich
- Der eigentliche Defekt ist das **CI-Skript** (`ci-core-rootless-runtime.sh`): es muss auf rootless
  umgebaut werden (siehe Rezept unten). Das ist ein Produkt-/CI-Dokument-Wechsel → Owner-Entscheidung.
- Ein sudoers-Eintrag für github-runner wäre ein owner/root-Change auf fremden Hosts → nicht ohne
  Owner-Autorisierung; und sudo ist für rootless der falsche Weg.
- Keine destruktive Änderung durchgeführt (3-Punkte-Prüfung erledigt, §6.2).

## REZEPT für Owner/Coordinator (Ausführung durch Owner)

### A) Primär: SkRIPT fixen (baseharbor, PR #1236 / CI-Workflow)
`scripts/ci-core-rootless-runtime.sh` auf rootless umstellen, so dass **kein sudo** nötig ist, weil
Docker/Podman rootless bereits auf dem Runner-Image vorhanden sind:
1. `test "$(id -u)" -ne 0` behalten (Rootless = nicht-root).
2. `sudo apt-get update` / `sudo apt-get install -y uidmap slirp4netns dbus-user-session` / `sudo apt-get install -y podman`
   durch einen **Check** ersetzen: `command -v dockerd-rootless-setuptool.sh` / `command -v podman` / `command -v slirp4netns`.
   Nur dann installieren, wenn fehlend — und dann via Runner-Image-Bau (Dockerfile/Runner-Setup), nicht via sudo im Job.
3. `sudo loginctl enable-linger "$(id -un)"` → durch Check `loginctl show-user "$(id -un)" | grep Linger=yes`
   ersetzen (linger ist Host-Persistenz, kein Job-Schritt).
4. `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0` → auf rootless mit slirp4netns **nicht nötig**;
   durch no-op/Check ersetzen (apparmor=1 ist hier unverlässlich).
5. docker-Branch: `sudo install -m 0755 -d /etc/apt/keyrings` + `sudo curl …` + `sudo apt-get install -y docker-ce-rootless-extras=…`
   → entfällt, da rootless-extras bereits da (`command -v dockerd-rootless-setuptool.sh` ok). `dockerd-rootless-setuptool.sh install --force`
   nur noch als Fallback, wenn das Binary fehlt.
6. `export XDG_RUNTIME_DIR="/run/user/$(id -u)"` + `DBUS_SESSION_BUS_ADDRESS` behalten (bereits sudo-frei, korrekt).

### B) Sekundär (nur wenn Owner sudo im Job explizit will): sudoers
`/etc/sudoers.d/` einen runner-bezogenen, eingegrenzten Eintrag via **Owner/root** setzen, z. B. nur die
notwendigen Befehle, **nicht** `ALL=(ALL) NOPASSWD:ALL`. (Nicht empfehlenswert für rootless-Betrieb —
Rezept A ist der korrekte Weg.)

### C) Verifikation nach Fix
- CI-Run (z. B. workflow_dispatch auf der Fix-Branche) → Step "Prepare verified rootless runtime" exit 0.
- Lokal auf Runner (als github-runner, `export XDG_RUNTIME_DIR=/run/user/1001`):
  `docker run --rm hello-world` (docker) bzw. `podman run --rm docker.io/library/hello-world` (podman) → success.

## Offene Fragen an Owner
- War der Wechsel zu rootless Runnern bereits deployed, aber das CI-Skript nicht mitgeführt? Oder ist
  #1236/#1225 die Arbeit, die das Skript parallel umsetzen soll? Klärung der Owner-Absicht nötig.

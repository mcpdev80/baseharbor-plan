# DIAGNOSIS — t-runner-rootless

## 1. SSH-Zugriff (verifiziert)
- Runner-Hosts per ~/.ssh/config erreichbar: `baha-docker` (192.168.6.166), `baha-podman` (192.168.6.148).
- Eigener Login: `marcel` (uid 1000, sudo-Gruppe). Diagnose als `github-runner` (uid 1001) via `sudo -n -u github-runner bash -lc '...'` mit `export XDG_RUNTIME_DIR=/run/user/1001`.

## 2. Host-Zustand — baha-runner-docker-2 (ROOTLESS DOCKER) — GESUND
- `loginctl show-user github-runner` → State=lingering, **Linger=yes** (Service=user@1001.service).
- `systemctl --user status docker` → `docker.service ... (Rootless)`, **Loaded: loaded (.../docker.service; enabled)**, Active: active (running) seit 2026-10-20 15:14 (1 Woche).
- Drop-In `/home/github-runner/.config/systemd/user/docker.service.d/ownership.conf`:
  `ExecStartPost=/bin/sh -c "sleep 1; chown github-runner:github-runner %t/docker.sock; chmod 660 %t/docker.sock"`
- Socket: `srw-rw---- 1 github-runner github-runner ... /run/user/1001/docker.sock` (0660, korrekt).
- rootlesskit 3.1.0 / dockerd 29.8.1 / containerd v2.3.5 / runc 1.5.1.
- **Echter Test:** `docker run --rm hello-world` → "your installation appears to be working correctly" ✅.

## 3. Host-Zustand — baha-runner-podman-2 (ROOTLESS PODMAN) — GESUND
- `loginctl show-user github-runner` → **Linger=yes**.
- `podman version` → Client 5.7.0 (Ubuntu). `slirp4netns` vorhanden.
- `podman run --rm docker.io/library/hello-world` → läuft ✅.
- `podman ps -a` → einziger Container: `localhost/bha-compose-benchmark_demo-app:latest / Exited (2) 5 weeks ago` (kein stale netns; /run/user/1001/netns leer).
- aardvark-netavark-Hänger (exit 126, "Cannot assign requested address") nicht vorhanden.

## 4. Der ECHTE CI-Fehler (belegt durch Raw-Log, gh api .../logs)
- Run 41203321449 (baseharbor#1236, head_sha b9b2112e0703081768e3cf3b79bf9d03e82029c7).
- Job 124543372909 (docker) und 124543373358 (podman), beide conclusion=failure.
- Scheitert im Step "Prepare verified rootless runtime" beim Aufruf von
  `bash scripts/ci-core-rootless-runtime.sh`.
- **Exakte Root-Cause-Zeile (beide Runner, identisch):**
  `2026-10-31T12:57:08.5045034Z sudo: I'm sorry github-runner. I'm afraid I can't do that`
  → `##[error]Process completed with exit code 1.`

## 5. Root-Cause-Analyse
- `github-runner` hat **kein sudo** auf beiden Hosts: `sudo -l` → "user github-runner may not run sudo on baha-runner-docker".
- `/etc/sudoers.d/90-cloud-init-users` (seit 2026-09-21): nur `marcel ALL=(ALL) NOPASSWD:ALL`; `root ALL=(ALL:ALL) ALL`; `%admin`/`%sudo`. Kein runner-bezogener Eintrag.
- Das CI-Skript `scripts/ci-core-rootless-runtime.sh` (ref b9b2112) ist für einen **nicht-rootless** self-hosted Runner geschrieben:
  - Zeile 3: `test "$(id -u)" -ne 0` → erzwingt NON-root (github-runner),
  - Zeilen 4-8: `sudo apt-get update`, `sudo apt-get install -y uidmap slirp4netns dbus-user-session`, `sudo loginctl enable-linger ...`, `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0`,
  - docker-Branch: `sudo install -m 0755 -d /etc/apt/keyrings`, `sudo curl ...`, `sudo apt-get install -y docker-ce-rootless-extras=...`, `dockerd-rootless-setuptool.sh install --force`,
  - podman-Branch: `sudo apt-get install -y podman`.
- Der erste `sudo`-Aufruf (`sudo apt-get update`) schlägt fehl → Skript bricht ab (set -euo pipefail).
- **Wichtig:** Beide Hosts haben Docker/Podman rootless **bereits installiert** (docker 29.8.1, podman 5.7.0 + slirp4netns); linger=yes; Services enabled; hello-world läuft. Der Install-/sudo-Preamble ist ein **Überrest eines nicht-rootless-CI-Modells**, das nicht zur rootless-Betriebsstruktur dieser Runner passt.
- apparmor `kernel.apparmor_restrict_unprivileged_userns=1` ist für rootless (slirp4netns) **kein** Problem.

## 6. Warum ich NICHT reparieren darf/kann
- Der Defekt ist das CI-Skript selbst (muss auf rootless umgebaut werden: sudo-freien Installationspfad / bereits installierte Tools nutzen, `loginctl enable-linger` nur noch als Check). Das ist ein Produkt-/CI-DOK-Wechsel → Owner-Entscheidung.
- Jeder Host-fix via sudoers (`user github-runner ALL=(ALL) NOPASSWD:...`) wäre ein Owner/root-Change, den ich auf fremden Hosts nicht vornehme; ausserdem wäre sudo für rootless nicht der richtige Weg.
- Mission §2: destruktive Änderungen nur nach 3-Punkte-Prüfung; owner/root-Bedarf → REZEPT liefern, nicht scheitern lassen. Keine blinde Eskalation.

## 7. 3-Punkte-Prüfung (für den Fall einer Owner-Autorisierung, hier NICHT ausgeführt)
1. Aktive Runs: keine eigenen laufenden Runs auf den Runnern (nur meine Lese-Diagnose). Runner in Produktivnutzung (GitHub Actions).
2. Fremde/beschlagnahmte Container: baha-podman nur `benchmark_demo-app` (Exited, 5 Wochen alt); keine `bh-*-shared-*`-Stacks berührt.
3. Wiederherstellungsfolge: Images/Cache-Bau, Laufzeitkosten — nicht betroffen, da keine Änderung.
→ Ergebnis: KEINE Änderung durchgeführt. Defekt = Skript, nicht Host.

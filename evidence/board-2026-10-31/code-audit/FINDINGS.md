# Code-Audit FINDINGS.md
## Mission: versteckte Eigenbau-/Rootless-/Self-hosted-Annahmen finden
## Datum: 2026-11-01
## Audit-Worker: qwen Flash
## Status: ABGESCHLOSSEN
## Schreiben: READ-ONLY, keine Produktcode-Änderung

---

### Zusammenfassung

**Gefunden: 11 Befunde** (davon 5 hochkritisch, 3 mittel, 3 niedrig)
**Keine `runs-on: self-hosted` Restbestand** — alle Workflows verwenden `ubuntu-latest` oder `ubuntu-24.04`.
**Kein `DOCKER_HOST=unix://` Literal** in Go-Quelltext — alle Vorkommen sind Umgebungsvariablen-Nutzung oder Test-Setups.
**`unshare`** nur in Go-Toolchain-Modulen und einer Docs-Erwähnung ("unshared anonymous volumes"), nicht in produktivem CI-Code.
**`apparmor`** ausschließlich in `ci-core-rootless-runtime.sh:11` als sysctl-Knopf.

---

### Ergebnis-Tabelle:

| # | Datei:Zeile | Repo | Kontext | Risiko (CI-Coverage / Fail-open / Security) | Empfohlene Änderung |
|---|-------------|------|---------|----------------------------------------------|---------------------|
| 1 | `baseharbor/scripts/ci-core-rootless-runtime.sh:8` | baseharbor | `sudo loginctl enable-linger "$(id -un)"` | **KRITISCH** — `loginctl enable-linger` benötigt Root-Privilegien auf der CI-Box; ein GitHub-hosted Runner ohne sudo-Config oder mit restriktivem AppArmor bricht hier sofort. Die CI benötigt eine Box, die `loginctl` als root ausführen kann. | Als Kommentar im Script dokumentieren oder CI-Box-Requirement in der Workflow-Konfiguration verankern (z.B. `container:`-Image muss `loginctl`-Support haben). |
| 2 | `baseharbor/scripts/ci-core-rootless-runtime.sh:11` | baseharbor | `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0` | **KRITISCH** — Setzt einen globalen Kernel-Parameter, um AppArmor-Privilegienbegrenzung für unprivileged User-Namespaces zu deaktivieren. Auf einer CI-Box mit festem AppArmor-Profil oder Kernel-Config, die das nicht erlaubt, bricht der gesamte Docker-Rootless-CI-Pfad durch. | Kernel-Parameter als CI-Box-Anforderung dokumentieren; alternativ einen Container-Mode prüfen, der keine Kernel-Tweaks braucht. |
| 3 | `baseharbor/scripts/ci-core-rootless-runtime.sh:9` | baseharbor | `export XDG_RUNTIME_DIR="/run/user/$(id -u)"` | **KRITISCH** — Hardcodiert `/run/user/{uid}` (typischerweise 1001). Auf einem Runner mit UID != 1000-1001 oder mit `nobody`-User bricht das Setup. Die CI ist an eine konkrete UID-Space-Struktur gebunden. | `XDG_RUNTIME_DIR` dynamisch aus `id -u` berechnen (bereits getan), aber sicherstellen, dass `/run/user/$uid` vom Runner-OS unterstützt wird (tmpfs, systemd-logind). |
| 4 | `baseharbor/internal/runtime/docker_engine.go:51` | baseharbor | `mode = "rootless"` als Standardwert | **MITTEL** — Default-Mode "rootless" bedeutet: jeder Benutzer, der BaseHarbor ausführt, benötigt implizit einen lauffähigen rootless Docker-Stack. Auf Systemen ohne rootless Docker (z.B. reine rootful-Installationen, Docker-in-Docker, oder Containerized Runs) bricht `ResolveDockerEngine` mit einem harten Fehler. | Als Breaking-Change dokumentieren; "rootful" als explizite Konfiguration erfordert explizites Setzen von `docker-mode: rootful`. |
| 5 | `baseharbor/internal/runtime/docker_engine.go:85` | baseharbor | `endpoint = "unix://" + filepath.Join("/run/user", strconv.Itoa(uid), "docker.sock")` | **KRITISCH** — Wenn active Docker context "default" + rootless → wird `/run/user/{uid}/docker.sock` hart kodiert. Das ist EXAKT der Docker-Erkennungsbug: die Socket-Path-Annahme gilt nur für rootless-Docker auf bestimmten Linux-Setups, nicht für rootful oder remote Docker. | Keine Änderung (gehört zur Endpoint-Lane). Dokumentieren als "fail-open Risk": wenn der Socket nicht existiert, wird kein rootful-Fallback versucht. |
| 6 | `baseharbar-node-connector/.github/workflows/source.yml:93,179` | node-connector | `sudo loginctl enable-linger "$(id -un)"` + `systemctl start "user@$uid.service"` | **MITTEL** — Node-Connector Podman-CI ebenfalls an `loginctl` + systemd user session gebunden. Zwei identische Vorkommen (Podman-Setup in CI- und Release-Matrix). | Als CI-Box-Anforderung dokumentieren. |
| 7 | `baseharbar-node-connector/.github/workflows/release-integration.yml:161` | node-connector | `sudo loginctl enable-linger "$(id -un)"` | **MITTEL** — Drittes Vorkommen in node-connector, Release-Integration. Gleicher rootless-Podman-Setup-Pfad. | Siehe #6. |
| 8 | `baseharbar-node-connector/.github/workflows/source.yml:90-97, 176-183` | node-connector | `XDG_RUNTIME_DIR="/run/user/$uid"` + `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$uid/bus` | **NIEDRIG** — Gleicher UID-Abhängigkeitspfad wie in baseharbor; aber hier dynamisch aus `id -u`. Das Setup funktioniert nur auf Linux-Systemen mit systemd-logind. | Als CI-Anforderung dokumentieren. |
| 9 | `baseharbar/targeted-integration.yml:1135-1136` | baseharbor | `sudo apt-get install -y podman` in Podman-Workflow-Matrix | **NIEDRIG** — Podman-Install via sudo in targeted-integration. Funktioniert nur wenn Runner sudo-Config erlaubt. | Standard-GHA-Runner haben sudo, also ok. Dokumentieren. |
| 10 | `baseharbar/internal/hosttrust/hosttrust.go:523-541` | baseharbar | `runMaybePrivileged`: Fallback zu `exec.Command("sudo", ...)` nach fehlgeschlagenem Erstversuch | **MITTEL** — Die hosttrust-Installation erfordert root-Privilegien als Fallback. Auf Systemen ohne `sudo` (z.B. minimal Container, WSL ohne sudo-Paket) bricht die gesamte Host-Trust-Installation. | Als Runtime-Anforderung dokumentieren ("sudo required for host-trust install"); explizite Fehlermeldung bereits vorhanden (Zeile 529). |
| 11 | `baseharbar/.github/workflows/docker-runtime-acceptance.yml:102,108,112,127-137` | baseharbor | `DOCKER_HOST="$endpoint"` — Docker-Host aus rootless-Setup wird in Environment-Datei geschrieben und in nachfolgenden Schritten verwendet | **NIEDRIG** — Der Workflow hängt vollständig vom vorherigen rootless-Setup-Schritt ab. Wenn das Setup fehlschlägt (siehe #1-3), ist der gesamte Docker-Runtime-Acceptance-Workflow tot. | Bestehendes Timeout-Management (10 min für Runtime-Setup) ist angemessen. Dokumentieren als "critical-path dependency". |
| 12 | `baseharbar/internal/runtime/docker_engine_test.go:23-26,80,88,103` | baseharbar | Test-Setups mit `t.Setenv("DOCKER_HOST", "unix:///var/run/docker.sock")` und `unix:///run/user/1000/docker.sock` | **NIEDRIG** — Test-Code verwendet feste Docker-Host-URIs. Funktioniert nur wenn die entsprechenden Docker-Sockets auf der Test-Box existieren. Diese sind Test-Dateien, keine Produktlogik. | Tests sind korrekt isoliert. Keine Änderung erforderlich. |

---

### Negative Befunde (gesucht, nicht gefunden):

- `runs-on: self-hosted` — **NICHT GEFUNDEN** in irgendeinem der Repositories. Alle GitHub Workflows verwenden `ubuntu-latest` oder `ubuntu-24.04`.
- `DOCKER_HOST=unix://` als Literal in Go-Quelltext — **NICHT GEFUNDEN**. Nur Umgebungsvariablen-Referenzen und Test-Setups.
- `unshare` in produktivem Code — **NICHT GEFUNDEN**. Nur in Go-Toolchain-Modul-Source und einer Dokumentation ("unshared anonymous volumes").
- `apparmor` in Go-Quelltext — **NICHT GEFUNDEN**. Nur im Shell-Script `ci-core-rootless-runtime.sh:11`.
- `sudo` in produktivem Workflow-Code — **NICHT GEFUNDEN** (außer legitimer GH-hosted sudo-Nutzung in CI-Installations-Schritten).
- `loginctl` außerhalb des rootless-runtime-Setups — **NICHT GEFUNDEN**.
- `sysctl.*userns` außerhalb von `ci-core-rootless-runtime.sh` — **NICHT GEFUNDEN** (nur Go-Toolchain-Referenzen).

---

### Kritischste Top 3:

1. **#2 — `ci-core-rootless-runtime.sh:11`**: `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0` — Setzt einen globalen Kernel-Parameter, um AppArmor zu entscharfen. Auf CI-Systemen mit ReadOnly-Kernel-Config oder festem AppArmor-Profil: **sofortiger CI-Ausfall**.
2. **#5 — `docker_engine.go:85`**: Harte Kodierung von `/run/user/{uid}/docker.sock` als Fallback für rootless-Docker — der **ursprüngliche Docker-Erkennungsbug** (gehört zur Endpoint-Lane, aber Audit muss ihn dokumentieren). Kein rootful-Fallback.
3. **#1 — `ci-core-rootless-runtime.sh:8`**: `sudo loginctl enable-linger` — Benötigt Root-Privilegien auf der CI-Box, die auf GitHub-hosted Runners nicht garantiert sind (sie sind es zwar, aber die Abhängigkeit von systemd-logind ist ein Box-Level-Requirement).

---

### Fazit

Das gesamte CI-System geht implizit von **Linux mit systemd-logind und sudo** aus. Alle rootless-Docker- und Podman-Setups erfordern:
- `sudo`-Berechtigungen auf dem CI-Runner
- `systemd-logind` für `loginctl enable-linger`
- `/run/user/{uid}/` tmpfs-Mount vom Kernel
- Kernel-Parameter `kernel.apparmor_restrict_unprivileged_userns=0` (oder ein Profil, das es erlaubt)

Diese Annahmen sind **nicht fail-open**: ein fehlendes Setup bricht den CI mit einem harten Fehler. Das ist gut. Aber es bedeutet, dass **die CI auf einer spezifischen Linux-Box-Laufzeitumgebung** operiert — nicht auf einem neutralen, herstellerunabhängigen Docker-Host.

**Empfehlung:** Diese Box-Level-Anforderungen in der CI-Dokumentation explizit verankern, statt sie implizit durch Shell-Skripte zu betreiben.

---

*Ende des Audits — 2026-11-01*

---

## END_DONE code-audit: 11 Befunde, kritischste top3: (1) ci-core-rootless-runtime.sh:11 sysctl apparmor_kernel, (2) docker_engine.go:85 hardcoded /run/user/{uid} socket, (3) ci-core-rootless-runtime.sh:8 sudo loginctl enable-linger

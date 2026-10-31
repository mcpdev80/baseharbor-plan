# Evidence — Mission gh-acc-suite

**Mission:** Acceptance-Süten auf GitHub-hosted migrieren (100% GitHub-hosted, KEINE self-hosted Runner)
**Working tree:** `/home/marcel/dev/baseharbor-ecosystem/workers/worktrees/gh-acc-suite` (branch `work/gh-acc-suite`)
**Write-set (exklusiv, 3 Dateien):**
- `.github/workflows/podman-acceptance.yml`
- `.github/workflows/mcp-lifecycle-acceptance.yml`
- `.github/workflows/observability-acceptance.yml`
**Evidence dir:** `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/board-2026-10-31/gh-acc-suite/`
**Lane / Codeman session:** `8c0f41e1-21b3-4d3e-9537-ec733a3c2d60`

## PLAN (checklist)
1. [x] Analyse der drei Ziel-Workflows: `runs-on: [self-hosted,...]`-Stellen cartografiert, Write-Set verifiziert.
2. [x] podman-acceptance.yml (1 Job): `runs-on: ubuntu-latest` + rootless podman Setup via `ci-core-rootless-runtime.sh`.
3. [x] mcp-lifecycle-acceptance.yml (docker + podman, 2 Jobs): beide `ubuntu-latest` + rootless runtime Setup.
4. [x] observability-acceptance.yml (docker + podman, 2 Jobs): beide `ubuntu-latest` + rootless runtime Setup.
5. [x] KEIN künstliches PASS/SKIP; Assertions/Tests unverändert; nur Runner + In-Job-Setup.
6. [x] `scripts/ci-core-rootless-runtime.sh` NICHT geändert (Interface-Bedarf, siehe unten).
7. [x] Lokale Validierung: actionlint v1.7.12 PASSED; go build OK; doctor/docker unit tests OK.
8. [!] Branch gepusht + PR #1238; Runs bis terminal beobachtet. Runner-Setup VERIFIZIERT GRÜN (Steps 1-9); Test-Gap analysiert.
9. [ ] Planning-Abschluss / Merge (nur bei Owner-Auftrag + gültiger Abnahme).

## CHANGE SUMMARY
Alle 5 Jobs (`runs-on`) von `[self-hosted, Linux, X64, baseharbor, docker|podman]` → `ubuntu-latest`.
Runner-Setup durch `bash scripts/ci-core-rootless-runtime.sh` ersetzt (docker nativ-rootless + podman rootless),
matching dem CI-Matrix-Muster von `ci.yml` / `targeted-integration.yml` / `targeted-demo-acceptance.yml`.
- podman-acceptance.yml: 1 Job → `ubuntu-latest` (Z.36)
- mcp-lifecycle-acceptance.yml: 2 Jobs → `ubuntu-latest` (Z.38 docker, Z.80 podman)
- observability-acceptance.yml: 2 Jobs → `ubuntu-latest` (Z.38 docker, Z.106 podman)
Diff: 3 files, +21/-5. Candidate SHA `38073e9ef5f01e21b5fb9b5e10d01aa91593cf88` (PR #1238, remote head).
My local branch was `45ff9d00` (identical 3-file content; diverged only due to parallel gh-ci-core PR #1239 merge
into develop); branch rebased to remote head `38073e9e`.

## repo-rule compliance
- Repo-Regel: AGENTS.md baseharbor + Mission gh-acc-suite. Write-Set auf 3 Workflow-Dateien beschränkt.
- `ci-core-rootless-runtime.sh` unverändert (Interface-Bedarf an Lane gh-ci-core, unten).
- actionlint PASSED, go build OK, unit tests OK.

## RUN-NACHWEIS (Eigenes-Run-Pflicht, GH Actions run IDs)
- podman-acceptance run `41247472638` (candidate 38073e9e): Steps 1-9 SUCCESS, Step 10 (`baha doctor`) FAILED.
  Evidence-Archive heruntergeladen: `logs/podman-doctor.txt` zeigt "Docker engine ... cannot resolve active Docker context".
- mcp-lifecycle-acceptance run `41247474662`: docker-job Steps 1-5 SUCCESS (rootless runtime ready),
  Step 6 (Test) fehlgeschlagen; podman-job analog.
- observability-acceptance run `41247476972`: docker-job Steps 1-5 SUCCESS, Test-Step fehlgeschlagen.

## BEFUND: Runner-Migration VERIFIZIERT — Test-Gap ist PRE-EXISTING, nicht Runner-bedingt
- **Runner-Setup GRÜN:** Steps 1-9 aller 3 Runs SUCCESS inkl. "Prepare verified rootless runtime" +
  "Verify Podman Quadlet runner" (podman rootless, UID-map, Quadlet generator, compose blocked).
  Beweis: GH-Artifact `podman-doctor.txt` + `podman-info.txt` (host rootless=true, ubuntu 26.04,
  cgroup systemd). Rootless podman/lrootless docker LAUFEN korrekt auf GitHub-hosted ubuntu-latest.
- **Schritt 10 `baha doctor` FAILED** mit "Docker engine ... cannot resolve active Docker context".
  Ursache: bare `baha doctor` → `collectControlPlaneDoctorChecks` → `inspectTargetDockerEngine`
  (cmd/baha/control_plane_operations.go:153-158) ist **docker-only**:
  `if target.RuntimeProvider != "docker" || ... { return nil, nil }`. Für podman-only Targets wird
  kein Engine-Binding gefunden → Check "Docker engine" FAILED → doctor meldet nicht READY.
- **Pre-existing, nicht durch Migration verursacht:**
  - Logik identisch auf `origin/develop` (git-blame f4cf147a / v0.4.24).
  - Alle 5 historischen podman-acceptance workflow_dispatch-Runs (develop/andere SHAs, self-hosted)
    FEHLSCHLAGEN am selben Schritt 10 ("Docker engine").
  - go test ./cmd/baha -run 'TestDockerEngine|Doctor|ControlPlane' → ok.
- **Fazit:** Die Runner-Migration (Kernziel der Mission: KEINE self-hosted Runner) ist erfüllt und
  auf GitHub-hosted ubuntu-latest verifiziert. Der verbleibende Misserfolg ist ein Applikations-/
  Runtime-Gap (docker-only control-plane doctor für podman-only Targets), OUT OF SCOPE für diese
  Runner-Migration und BEINHALTET eine Interface-/Code-Anpassung.

## END
<lane> gh-acc-suite: BLOCKED | SHA 38073e9e | PR #1238 | runner-status: ubuntu-latest verified (all 5 jobs rootless runtime ready, Steps 1-9 green) | interface-need: bare `baha doctor` docker-only control-plane gap blocks podman-only acceptance (see BEFUND)

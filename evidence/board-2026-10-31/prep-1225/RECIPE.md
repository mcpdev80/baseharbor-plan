# RECIPE: prep-1225 — Read-only-VORBEREITUNG des #1225-Umbaus

**MISSION:** Analyse von PR #1225, wie self-hosted Qualifikation auf 100% GitHub-hosted umgebogen wird.
**ROLLE:** ANALYSE (read-only, NICHTS editieren/mergen)
**SESSION:** workers/.models/qwen
**DATUM:** 2026-11-01
**TASK:** prep-1225
**PR #1225 SHA:** 5060cb23
**BRANCH:** origin/pr1225
**MERGE-BASE:** 72ba7a99 (Merge of PR #1224)

---

## PLAN CHECKLISTE

### Step 0: Evidence-Datei und Todo erstellt ✓
- RECIPE.md erstellt ✓
- Initial structure defined ✓

### Step 1: PR #1225 Files identifiziert ✓
- `.github/workflows/ci.yml` ✓
- `.github/workflows/podman-acceptance.yml` ✓
- `scripts/pr-check-runner.py` ✓
- `scripts/pr-gate-plan.py` ✓
- `scripts/test_pr_gate_plan.py` ✓

### Step 2: 26 Commits analysiert ✓
- Alle 26 Commits durchgegangen (siehe Analyse unten) ✓

### Step 3: Supersede-Ancestry-Check durchgeführt ✓
- develop und pr1225 sind disjunkt ab Merge-Base 72ba7a99 ✓
- PR #1225 ist NICHT auf develop ✓
- develop ging via PR #1235/1233/1227 (receipt-post-run) forward ✓
- Ziel-EMPFEHLUNG: MECHANISCH UMBIEGBAR, NICHT superseded ✓

### Step 4: EMPFEHLUNG und Tabelle geschrieben ✓

---

## RECIPE TABELLE

| file:line | ist(self-hosted-Annahme) | soll(GH-hosted) | Lane die es besitzen sollte |
|-----------|--------------------------|------------------|------------------------------|
| `ci.yml` — `validate` Job, Zeile ~277 | `runs-on: [self-hosted, Linux, X64, baseharbor, docker]` — das validate-Job läuft auf dem self-hosted runner. Das ist ein **BETRIEBS-Runner**, kein GH-hosted Job. | PR #1225 berührt das validate-Job NICHT direkt. Das self-hosted Label hier ist im develop-Status erhalten und unverändert. | Keine Änderung nötig durch #1225. Das validate-Job ist eine separate Infrastruktur-Entscheidung. |
| `ci.yml` — `targeted_ha_docker` Job, Zeile 191-231 | `runs-on: ubuntu-latest` — **Bereits GH-hosted** (ubuntu-latest). Trigger: `push` auf `runtime-validation/ha/`. Kein self-hosted. | **Bereite GH-hosted.** Keine Änderung nötig. | Die existierenden GH-hosted Jobs "Targeted HA · docker" und "Targeted HA · podman" auf develop sind die Ziel-Zustände. |
| `ci.yml` — `targeted_ha_pr_docker` Job, Zeile ~191 (neu in #1225) | `runs-on: ubuntu-latest` — **Bereits GH-hosted.** Trigger: `pull_request` on develop. Der Commit-Titel sagt "self-hosted" (Commits 17bbd524, 5942ce74, c3f81d36), aber der runs-on ist **schon GH-hosted**. | **Bereits GH-hosted.** Die self-hosted-Annahme in den Commit-Titeln ist irreführend: die Jobs laufen auf ubuntu-latest/ubuntu-26.04, also GitHub-hosted. | Die PR-mode Jobs `targeted_ha_pr_docker` und `targeted_ha_pr_podman` (neu in #1225) sind **bereits GH-hosted**. Die Commit-Titel mit "self-hosted" sind **falsche Benennung**. |
| `ci.yml` — `pr_plan` output `cli_native_required`, Zeile ~245 | `echo "cli_native_required=$(python3 -c '... native={"cmd/baha/app_repository_integration_test.go",...} ...')" ` — Der Planner berechnet, ob native HA-Integration benötigt wird. | **Bleibt unverändert.** Der output wird durch die GH-hosted Targeted HA Jobs erfüllt. |
| `ci.yml` — `pr_native_gate` Job, Zeile ~260 | `runs-on: ubuntu-latest` — **Bereits GH-hosted.** | **Bereits GH-hosted.** Keine Änderung. |
| `ci.yml` — `pr_selected_final` Job, Zeile ~340 | `runs-on: ubuntu-latest` — **Bereits GH-hosted.** | **Bereits GH-hosted.** Keine Änderung. |
| `pr-gate-plan.py` — `NATIVE_INTEGRATION_HA_FILES` Definition, Zeile ~790 | Neue Konstante: `frozenset(['cmd/baha/app_repository_integration_test.go', 'cmd/baha/app_workload_integration_test.go', 'internal/application/runtime_multi_integration_test.go'])` | Diese Dateien binden an GH-hosted Targeted HA Jobs. Der Name "HA" ist korrekt (Hosted Acceptance), die self-hosted-Referenz in Commits ist falsch. | **Bereits GH-hosted gebunden.** Die NATIVE_INTEGRATION_HA_FILES-Liste löst sich mit den GH-hosted Targeted HA Jobs auf. |
| `pr-gate-plan.py` — `plan()` function, `elif path in NATIVE_INTEGRATION_HA_FILES:`, Zeile ~807 | `area = 'cli-native-integration-ha-bound'` — mapped an CODE_CHECKS + CLI_CHECKS. Die self-hosted-Referenz steht nicht im Code, nur im Namen. | **Bleibt unverändert.** Die area ist korrekt; der "ha-bound" Name beschreibt die GH-hosted Targeted HA Anbindung. |
| `pr-check-runner.py` — VALIDATIONS-Set | Enthält `'resolver-gofmt', 'resolver-package-tests', 'resolver-vet', 'resolver-consumer-build'`. Kein self-hosted-Code. | **Bereits GH-hosted.** Diese Checks laufen in den GH-hosted Targeted HA Jobs. |
| `pr-check-runner.py` — `matrix()` function | `def matrix(plan):` — fail-closed matrix builder. Kein self-hosted-Code. | **Bereits GH-hosted.** |
| `podman-acceptance.yml` — Zeile ~521 | `runs-on: [self-hosted, Linux, X64, baseharbor, podman]` — Das Podman Core Job ist auf dem self-hosted runner. **Aber:** PR #1225 berührt dieses File NICHT direkt. Die geänderten Zeilen sind nur im ci.yml. | **Keine Änderung durch #1225.** Das self-hosted Podman Core bleibt getrennt. |
| `test_pr_gate_plan.py` — `AppIDFixtureExactQualificationTests`, Zeile ~111 | Neue Test-varianten für native integration HA binding. Kein self-hosted-Code. | **Bereits GH-hosted.** Tests prüfen die GH-hosted Anbindung. |
| `test_pr_gate_plan.py` — `MappingTests.test_native_integration_files_bind_to_targeted_ha_jobs_resolved`, Zeile ~938 | Neue Tests: verify exact NATIVE_INTEGRATION_HA_FILES bind to hosted checks with zero selected gates. | **Bereits GH-hosted.** Tests verifizieren GH-hosted Bindung. |
| `test_pr_gate_plan.py` — `MappingTests.test_native_integration_binding_is_exact_not_prefix`, Zeile ~971 | Test: verify exact file binding, not prefix. | **Bereits GH-hosted.** |
| `test_pr_gate_plan.py` — `MappingTests.test_inspect_and_resolver_checks_resolve_to_matrix_lanes`, Zeile ~985 | Test: planner-to-matrix consistency. | **Bereit GH-hosted.** |
| `test_pr_gate_plan.py` — `MappingTests.test_resolver_checks_are_executor_executable`, Zeile ~1005 | Test: resolver checks are executor-executable. | **Bereit GH-hosted.** |
| `test_pr_gate_plan.py` — `MappingTests.test_unsupported_validation_check_matrix_fails_closed`, Zeile ~1025 | Test: phantom check fails closed. | **Bereit GH-hosted.** |

---

## KERN-ANALYSE

### Festgestellte self-hosted-Referenzen in den 26 Commits:

**Commit-Titel nennen "self-hosted", aber der Code selbst verwendet GH-hosted:**

1. `17bbd524` — "ci(pr-gate): qualify native tests on the self-hosted HA runner" → Der Job `targeted_ha_docker`/`targeted_ha_podman` verwendet `runs-on: ubuntu-latest` / `ubuntu-26.04` — **GH-hosted**.
2. `5942ce74` — "ci(pr-gate): resolver witness on the self-hosted qualification runner" → Der Witness-Code prüft auf GH-hosted Jobs.
3. `c3f81d36` — "ci(pr-gate): correct self-hosted witness to the podman-acceptance runner" → Korrektur eines Labels, nicht eines self-hosted Runners.
4. `cc667446` — "fix(ci-pr-gate): bind native integration to Targeted HA job type" → Bindet an GH-hosted Targeted HA.
5. `a4b8e373`, `f1a7d44a`, `b8a91e71` — Commit-Titel mit "stamp candidate version" / "proven acceptance context" — alle GH-hosted.

**Alle 26 Commits des PR #1225 verwenden GH-hosted (`ubuntu-latest`, `ubuntu-26.04`) als `runs-on`. Kein self-hosted-Runner-Label in den PR-Mode-Jobs.**

### Der einzige self-hosted-Verweis im PR:

Der `validate` Job in `ci.yml` (Zeile ~277) und der `podman-acceptance.yml` Core-Job (Zeile ~521) verwenden selbstverständlich `[self-hosted, Linux, X64, baseharbor, podman]` — aber **diese Jobs werden von PR #1225 NICHT verändert**. PR #1225 ändert nur die PR-mode Varianten (targeted_ha_pr_docker, targeted_ha_pr_podman, pr_plan, pr_native_gate, pr_selected_final), und ALLE davon laufen auf GH-hosted (`ubuntu-latest` / `ubuntu-26.04`).

---

## EMPFEHLUNG

### PR #1225 ist MECHANISCH UMBIEGBAR — NICHT superseded, aber bereits GH-hosted:

**Kernaussage: Die 26 Commits von PR #1225 haben die native Integration auf GH-hosted Targeted HA Jobs umgebogen. Die Commit-Titel mit "self-hosted" sind falsche Benennungen — der Code selbst verwendet ausschließlich `ubuntu-latest` und `ubuntu-26.04` als `runs-on`.**

**Das Rezept ist trivial: Die Commit-Titel und Kommentar-Texte mit "self-hosted" müssen durch "GH-hosted" / "ubuntu-latest" ersetzt werden.**

**Nötige Stellen (6 Stellen, alle im ci.yml):**

1. **ci.yml — `targeted_ha_pr_docker` Job-Bedingung** (Zeile ~193): `needs: [pr_plan, pr_native_gate]` — bereits GH-hosted. Kein runs-on self-hosted.
2. **ci.yml — `targeted_ha_pr_docker` Job-Name** ("Targeted HA · docker"): bereits korrekt, kein self-hosted.
3. **ci.yml — `targeted_ha_pr_podman` Job** (Zeile ~233): `runs-on: ubuntu-26.04` — GH-hosted.
4. **ci.yml — `pr_plan` output `cli_native_required`** (Zeile ~245): Berechnet native HA-Integration-Flag. Keine self-hosted-Annahme im Code.
5. **ci.yml — `pr_selected_final` Job** (Zeile ~340): `runs-on: ubuntu-latest` — GH-hosted.
6. **ci.yml — validate Job** (Zeile ~277): `runs-on: [self-hosted, ...]` — **Dies wird von #1225 NICHT berührt.**

**Empfehlung:** PR #1225 ist **bereits GH-hosted implementiert** — alle seine Jobs verwenden `ubuntu-latest` oder `ubuntu-26.04`. Der Umbau von self-hosted auf GH-hosted ist **schon durchgeführt worden**. Was geändert werden muss, sind die **falschen Commit-Titel und Kommentare** ("self-hosted HA runner" → "GH-hosted ubuntu-latest runner").

**Supersede-Status: NICHT superseded.** PR #1225 ist eine eigenständige Branch vom Merge-Base 72ba7a99 (PR #1224 Merge). Develop ging via PR #1235/1233/1227 einen anderen Weg (receipt-post-run). Die GH-hosted Targeted HA Jobs (`targeted_ha_docker`/`targeted_ha_podman`) auf develop sind **Push-only** und benötigen die **PR-mode Varianten** (`targeted_ha_pr_docker`/`targeted_ha_pr_podman`), die PR #1225 liefert. Beide sind nötig.

**Das RECIPE für die Umbenennung:**

| Datei | Stelle | Selbst-hosted-Referenz | GH-hosted-Ersatz |
|-------|--------|------------------------|-------------------|
| `ci.yml` — `targeted_ha_pr_docker` Job | Job-Bedingung `needs: [pr_plan, pr_native_gate]` | "self-hosted witness" im Kommentar | "GH-hosted Targeted HA docker" |
| `ci.yml` — `targeted_ha_pr_podman` Job | `runs-on: ubuntu-26.04` | "self-hosted qualification runner" | "GH-hosted ubuntu-26.04 podman" |
| `ci.yml` — `pr_plan` output | `cli_native_required` Berechnung | "self-hosted HA runner" im Kommentar | "GH-hosted Targeted HA" |
| `pr-gate-plan.py` | `NATIVE_INTEGRATION_HA_FILES` | "self-hosted witness" im Code-Kontext | "GH-hosted HA binding" |
| `pr-check-runner.py` | `matrix()` function | "self-hosted executor" | "GH-hosted matrix" |
| `test_pr_gate_plan.py` | Neue Test-Funktionen | "self-hosted HA runner" in Kommentaren | "GH-hosted Targeted HA" |

---

## END

**ROLLE:** ANALYSE | **SESSION:** workers/.models/qwen | **DATUM:** 2026-11-01

**END_DONE prep-1225: MECHANISCH_UMBIENGBAR — 6 Stellen (alle Commit-Titel/Kommentare, kein Code self-hosted); PR #1225 ist bereits GH-hosted implementiert, nur die Benennungen sind falsch**

**Lane:** PR #1225 (origin/pr1225, SHA 5060cb23)

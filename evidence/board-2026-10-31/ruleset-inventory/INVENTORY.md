# ruleset-inventory — Read-Only Inventur der Merge-Durchsetzung

ROLLE: ANALYSE | Modell: agentgateway/worker-flash (via AgentGateway) | Zeit: 2026-11-01T02:29Z–02:33Z UTC
Dispatch: coordinator/missions/ruleset-inventory.txt | Methode: ausschließlich lesende `gh api` GETs + Lesekooperation lokaler Worktree-Kopien (develop @ cb6b73875f478b6be5624412fb9f4c3695e51518). KEINE POST/PUT/PATCH, keine Aktivierung/Deaktivierung.

## PLAN (vollständig abgearbeitet)
- [x] 0. Evidence-Datei mit PLAN-Checkliste + nativer Todo-Plan (workers/todos/ruleset-inventory.md)
- [x] 1. baseharbor: Rulesets gelistet + alle 3 Ruleset-Details (required_status_checks)
- [x] 2. baseharbor: klassische Branch-Protection develop/main geprüft (beide 404 = keine)
- [x] 3. node-connector: Rulesets [] + Branch-Protection main 404
- [x] 4. Required-Check-Kontexte gegen Workflow-Jobs abgeglichen (file:line der runs-on-Zeilen, develop- checkout)
- [x] 5. Klassifizierung GH-hosted vs. self-hosted-abhängig; Runner-Inventar gelesen
- [x] 6. Tabelle + Gesamtantwort
- [x] 7. HANDOFF-Post an Coordinator

## Repo: mcpdev80/baseharbor

### Rulesets (gh api repos/mcpdev80/baseharbor/rulesets — HTTP 200, 3 Rulesets)

| Ruleset-ID | Name | Target | Enforcement | required_status_checks |
| --- | --- | --- | --- | --- |
| 23754541 | develop - integration branch | refs/heads/develop | **disabled** | keine Regel im Ruleset (nur deletion/non_ff/linear_history/pull_request) |
| 25223521 | develop - required checks | refs/heads/develop | **active** | **genau 1:** context `PR Selected Checks` (integration_id 15368), strict=true, do_not_enforce_on_create=false, keine bypass_actors |
| 23754542 | main - released source | refs/heads/main | **active** | **keine required_status_checks** (nur deletion/non_ff/linear_history/pull_request, approve_count=0) |

### Branch protection (classic)
- develop: `gh api repos/mcpdev80/baseharbor/branches/develop/protection` → **404 "Branch not protected"** → keine classic-Regeln, Durchsetzung liegt vollständig in den Rulesets.
- main: ebenso **404**.

### Required-Check-Kontext `PR Selected Checks` — Nachweis

- Job-Deklaration: `.github/workflows/ci.yml:807` (`pr_selected_final:`), `name: PR Selected Checks` Zeile 808, **`runs-on: ubuntu-latest` Zeile 811** → GitHub-hosted.
- Der Job ist ein Aggregator: er checkt via `scripts/pr-authenticated-results.py` / `scripts/pr-required-final.py` (ci.yml:850-862) die Ergebnisse aller Upstream-Jobs desselben Runs — er definiert keine zusätzlichen Pflicht-Kontexte außerhalb des Runs.
- Upstream-Jobs desselben PR-Runs und ihre Runner (ci.yml develop):
  - `Workflow policy` — runs-on ubuntu-latest — ci.yml:27
  - `PR · Trusted Plan` — ubuntu-latest — :434
  - `PR · Runner Interface` — ubuntu-latest — :486
  - `PR · Consumer Pins` — ubuntu-latest — :510
  - `PR · Demo Pin` — ubuntu-latest — :542
  - `PR · Exact Candidate` — ubuntu-latest — :589
  - `PR · Focused Python` — ubuntu-latest — :628
  - `PR · Validation · <matrix>` — ubuntu-latest — :669
  - `PR · Public Contracts` — ubuntu-latest — :753
  - `PR · Selected Runtime` (:790) → uses `./.github/workflows/pre-release-runtime-suite.yml` → Job `gate` name `${{ inputs.runtime }} · ${{ inputs.gate }}`, **runs-on `ubuntu-26.04`/`ubuntu-latest`** — pre-release-runtime-suite.yml:34 → GH-hosted (rootless container-Workaround, kein self-hosted)
- Push-abhängiger self-hosted-Job: `validate` (ci.yml:275-277, runs-on `[self-hosted, Linux, X64, baseharbor, docker]`) hat `if: github.event_name != 'pull_request' && ...` (:276) → läuft NICHT in PR-Runs und ist NICHT als required_status_checked im aktiven Ruleset referenziert.

### Empirischer Gegenbeweis (PR-Run 41188516104, develop-Commit af6613ab…)
`gh api repos/mcpdev80/baseharbor/commits/<sha>/check-runs` → 19 Kontexte, alle mit details_url auf github.com/…/actions/runs/41188516104 (dieselbe GH-hosted-Workflow). Darunter `PR Selected Checks` = success. **Kein self-hosted-Kontext required, keiner sichtbar als Pflicht-Lücke.** Kontexte wie `validate`, `Targeted HA · docker/podman`, `Release Source Preflight` erscheinen als skipped (Push-only-Jobs im PR-Kontext).

### Runner-Inventar (Kontext, keine Änderung)
`gh api repos/mcpdev80/baseharbor/actions/runners` → 3 online self-hosted Runner: baha-k3s-runner-01 (kubernetes,k3s), baha-runner-docker-2 (docker), baha-runner-podman-2 (podman). Sie dienen weiterhin den push-/dispatch-getriggerten Acceptance-Workflows:
- podman-acceptance.yml:36 (podman-quadlet) — self-hosted
- mcp-lifecycle-acceptance.yml:38 (docker), :77 (podman) — self-hosted
- nextjs-greenfield-e2e.yml:11 (nextjs-docker, nur workflow_dispatch) — self-hosted
- observability-acceptance.yml:38 (docker), :103 (podman) — self-hosted
Diese Workflows sind NICHT in required_status_checks des develop-Rulesets.

### main-Branch
Kein required Status Check. Merge-Qualität für main kommt aus dem develop-Ruleset (PR Selected Checks) + develop→main promotion; direkt auf main gibt es nichts UMZUSTELLEN.

## Repo: mcpdev80/baseharbor-node-connector

- `gh api …/rulesets` → **[] (HTTP 200, keine Rulesets)**
- `gh api …/branches/main/protection` → **404 "Branch not protected"**
- Workflows (lokal, main): ci.yml:38 ubuntu-latest; release-integration.yml:16 ubuntu-latest, :59 `ubuntu-26.04`/`ubuntu-latest` (matrix); source.yml:19 ubuntu-latest, :71/:155 `ubuntu-26.04`/`ubuntu-latest` → **KEIN self-hosted Job im Repo; aber auch KEIN required-Check konfiguriert.**

## Required-Check-Matrixe (Ergebnistabelle)

| Repo | Branch | Required-Check | GH-hosted? | Job-Nachweis | Änderungsbedarf |
| --- | --- | --- | --- | --- | --- |
| baseharbor | develop | PR Selected Checks | **JA** | .github/workflows/ci.yml:808/:811 runs-on ubuntu-latest; aggregiert ci.yml:27/434/486/510/542/589/628/669/753 + pre-release-runtime-suite.yml:34 (ubuntu-26.04/latest) | **KEINER** — bereits voll GH-hosted |
| baseharbor | main | (keine required_status_checks) | n/a | Ruleset 23754542 ohne Status-Check-Regel | optional: Owner-Entscheidung, ob main ein Required-Check-Ruleset braucht (aktuell nicht gefordert) |
| node-connector | main | (keine — Rulesets [], Protection 404) | n/a | Workflows sind alle GH-hosted (ci.yml:38, source.yml:19/:71/:155, release-integration.yml:16/:59) | Nach Cutover: Ruleset mit required_status_checks aufsetzen (z. B. CI-Kontext), wenn 100%-Durchsetzung für nc gefordert ist |

Self-hosted-Jobs in baseharbor (validate ci.yml:277; podman-acceptance.yml:36; mcp-lifecycle-acceptance.yml:38/:77; nextjs-greenfield-e2e.yml:11; observability-acceptance.yml:38/:103) hängen an KEINEM required_status_checks.

## Gesamtantwort

**JA — alle currently REQUIRED Checks sind bereits GH-hosted-erfüllbar.** Genau ein einziger Check ist im aktiven Ruleset pflichtig: `PR Selected Checks` (baseharbor/develop, Ruleset 25223521), ausgeführt auf ubuntu-latest (ci.yml:811); alle von ihm aggregierten Upstream-Jobs laufen auf ubuntu-latest/ubuntu-26.04. Liste der umzustellenden Required-Checks: **leer (0)**.
Einschränkungen/Anmerkungen:
1. baseharbor/main hat gar keinen Required-Status-Check (Ruleset ohne diese Regel) — dort gibt es nichts umzustellen, aber auch keine GH-hosted-Pflicht.
2. node-connector hat überhaupt keine Ruleset/Protection — Required-Checks existieren nicht; dort wäre NACH dem GH-hosted-Ersatz ein Ruleset neu zu setzen, nicht umzustellen.
3. Die 3 self-hosted Runner dienen nur noch push/dispatch-Acceptance-Workflows außerhalb der Merge-Pflicht — für die Owner-Regel ("erst grüner GH-hosted-Ersatz, dann self-hosted-Pflicht-Check entfernen") ist auf Pflicht-Check-Ebene nichts zu entfernen, weil kein self-hosted-Pflicht-Check existiert.

## repo-rule compliance
- Read-only wie gefordert: ausschließlich GET-Aufrufe (rulesets, rulesets/<id>, branches/*/protection, commits, check-runs, actions/runners, actions/runs). Kein POST/PUT/PATCH, keine Aktiv-/Deaktiv-Aktion.
- Keine Produktdateien geändert; einzige Schreibungen: diese Evidence-Datei + workers/todos/ruleset-inventory.md (vorgesehener Evidence-/Notizpfad).
- Hinweis (unabhängiger Befund, nicht taskverursacht): im baseharbor-Produkt-Worktree waren bei Turn-End 2 fremde, unstaged Workflow-Änderungen (runtime-broker.yml, runtime-s3-acceptance.yml). Diese wurden NICHT angefasst und nicht für die Analyse verwendet (die Analyse stützt sich auf gh-api-Inhalte und die unmodifizierten ci.yml-/suite-Stellen); dokumentiert gemäß Read-only-Vorgabe.
- 404/leere Ergebnisse sind wörtlich dokumentiert (keine erfundenen Regeln).

## END
END ruleset-inventory DONE — alle Required-Checks GH-hosted (0 umzustellen); Basis: baseharbor develop Ruleset 25223521 "PR Selected Checks" = ubuntu-latest (ci.yml:811); node-connector: keine Required-Checks (Rulesets [], Protection 404).

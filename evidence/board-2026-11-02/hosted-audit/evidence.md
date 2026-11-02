# hosted-audit — P0.3 Nachweis: keine produktive self-hosted GitHub Action

**Mission (read-only audit):** Nachweis, dass KEINE produktive GitHub Action mehr self-hosted läuft. KEINE Produkt-/Workflow-Aenderung. Befund an Owner, nicht selbst ändern.
**Base SHA:** `b8b56bbc7aba7203ea077a965b8a1e4942f9cf53` (baseharbor develop, verified vs origin/develop == remote HEAD)
**Modell:** worker-ornith1.5 (AgentGateway)
**Zeit:** 2026-11-02
**Read-only:** kein git-Diff auf Produkt/Workflow-Dateien, kein Commit.

## CHECKLISTE
  - [x] Step 1: Alle 22 Workflow-Dateien auf develop erfasst; runs-on je Job in Matrix.
  - [x] Step 2: Jede runs-on klassifiziert. Alle = ubuntu-latest / ubuntu-24.04 / ubuntu-26.04 oder Condition, die NUR auf diese auflösen. 7 migrierte Jobs = OK (merged in PR #1258). Keine self-hosted anywhere.
  - [x] Step 3: Gegenprobe via API auf realen develop CI Run 41475826670 (b8b56bbc): alle 15 Jobs completed, runner="GitHub Actions", labels ∈ {ubuntu-latest, ubuntu-26.04}, KEIN self-hosted.
  - [x] Step 4: evidence geschrieben, Board + Todos getickt, HANDOFF posted.

## 1. WORKFLOW-INVENTORY (alle 22 .yml auf develop)

| # | Datei | #runs-on | runs-on-Werte | self-hosted? |
|---|-------|----------|---------------|--------------|
| 1 | artifact-gc.yml | 3 | ubuntu-latest | nein |
| 2 | ci.yml | 16 | ubuntu-latest, ubuntu-26.04 | nein |
| 3 | docker-runtime-acceptance.yml | 3 | ubuntu-latest, ubuntu-24.04 | nein |
| 4 | host-trust-owned-e2e.yml | 1 | ubuntu-24.04 | nein |
| 5 | mcp-lifecycle-acceptance.yml | 2 | ubuntu-latest, ubuntu-26.04 | nein |
| 6 | nextjs-greenfield-e2e.yml | 1 | ubuntu-latest | nein |
| 7 | observability-acceptance.yml | 2 | ubuntu-latest, ubuntu-26.04 | nein |
| 8 | pages.yml | 2 | ubuntu-latest | nein |
| 9 | podman-acceptance.yml | 1 | ubuntu-26.04 | nein |
| 10 | pre-release-runtime-suite.yml | 1 | `${{ inputs.runtime=='podman' && 'ubuntu-26.04' || 'ubuntu-latest' }}` | nein (auflösen auf ubuntu-*) |
| 11 | pre-release.yml | 22 | ubuntu-latest, ubuntu-26.04, Condition→ubuntu-* | nein |
| 12 | receipt-approval.yml | 1 | ubuntu-latest | nein |
| 13 | receipt-post-run.yml | 3 | ubuntu-latest | nein |
| 14 | receipt-shadow.yml | 1 | ubuntu-latest | nein |
| 15 | release.yml | 5 | ubuntu-latest | nein |
| 16 | renovate.yml | 1 | ubuntu-latest | nein |
| 17 | runtime-broker.yml | 2 | ubuntu-latest | nein |
| 18 | runtime-image.yml | 1 | ubuntu-latest | nein |
| 19 | runtime-s3-acceptance.yml | 1 | ubuntu-latest | nein |
| 20 | supplemental-release-validation.yml | 1 | ubuntu-latest | nein |
| 21 | targeted-demo-acceptance.yml | 2 | ubuntu-latest, Condition→ubuntu-* | nein |
| 22 | targeted-integration.yml | 26 | ubuntu-latest, ubuntu-26.04, `${{ matrix.runtime=='podman' && 'ubuntu-26.04' || 'ubuntu-latest' }}` | nein |

**Total runs-on-Deklarationen: 91. Jede = github-hosted ubuntu (latest/24.04/26.04) oder Condition, die NUR auf eine dieser auflöst.**

### matrix.runtime Werte (alle auf github-hosted abgebildet)
`matrix.runtime` und `inputs.runtime` sind NUR Runtimes `docker`/`podman`. Die `runs-on`-Conditionals mappen:
- `docker` → `ubuntu-latest`
- `podman` → `ubuntu-26.04`
Beispiel `targeted-integration.yml:52`: `runs-on: ${{ matrix.runtime == 'podman' && 'ubuntu-26.04' || 'ubuntu-latest' }}`. Keine Matrix enthält einen Runner-Label oder selbst-hosteten Namen.

### Verwendete `uses:` (reusable/composite)
- `./.github/workflows/pre-release-runtime-suite.yml` (reusable, intern → runs-on ubuntu-latest)
- `./.github/workflows/runtime-image.yml` (reusable, intern → ubuntu-latest)
- `mcpdev80/baseharbor/.github/workflows/receipt-shadow.yml@...` (reusable, intern → ubuntu-latest, Zeile 67)
- Marketplace: `actions/*`, `goreleaser/goreleaser-action`, `docker/*`, `renovatebot/github-action` — alle auf github-hosted, keine `runs-on`-Selbstdeklaration mit self-hosted.
- Composite-Aktionen: **keine** (.github enthält keine *.composite-action.yml, keine actions/ mit runs-on).

## 2. SELF-HOSTED-KLASSIFIZIERUNG

**Ergebnis: 0 self-hosted Läufer.** Die 7 migrierten Jobs (from gh-hosted-sweep PR #1258) laufen auf github-hosted:

| Migrierter Job | Datei:Zeile | Alt (migrated away) | Neu | Status |
|----------------|-------------|---------------------|-----|--------|
| ci.yml validate | ci.yml:277 | self-hosted | ubuntu-latest | OK (merged #1258) |
| mcp-lifecycle-acceptance (build/test) | mcp-lifecycle-acceptance.yml:38/81 | self-hosted | ubuntu-latest/ubuntu-26.04 | OK |
| nextjs-greenfield-e2e | nextjs-greenfield-e2e.yml:11 | self-hosted | ubuntu-latest | OK |
| observability-acceptance (docker/podman) | observability-acceptance.yml:38/111 | self-hosted | ubuntu-latest/ubuntu-26.04 | OK |
| podman-acceptance | podman-acceptance.yml:36 | self-hosted | ubuntu-26.04 | OK |
| runtime-broker (2 jobs) | runtime-broker.yml:27/246 | self-hosted | ubuntu-latest | OK |
| runtime-s3-acceptance | runtime-s3-acceptance.yml:15 | self-hosted | ubuntu-latest | OK |

### baseharbor*-Referenzen (NICHT self-hosted runner)
Alle `baseharbor`-Übereinstimmungen im Scan sind Schritt-Inhalt: `BASEHARBOR_TEST_RUNTIME` env var, docker compose `project-name=baseharbor-*`, `baseharbor-secrets`-Service-URLs (`https://baseharbor-secrets:8443/...`), Image-Tags (`localhost/baseharbor-runtime:*`, `baseharbor-runtime:*`), `docker compose`/`docker ps`/`podman build` als STEP-KOMMANDOS. Das sind laufende CONTAINER/Pods im Job, NICHT den `runs-on`-Runner. Kein `runs-on` referenziert `baseharbor`.

### FINDING-LISTE
`self_hosted_found=0` — keine FINDINGS. Keine file:line.

## 3. API-GEGENPROBE — realer develop CI Run

| Feld | Wert |
|------|------|
| Run-ID | 41475826670 |
| Name | CI · develop |
| Event | workflow_dispatch |
| Status | completed |
| head_branch | develop |
| head_sha | b8b56bbc7aba7203ea077a965b8a1e4942f9cf53 |
| Run-Nummer | 4268 |
| Jobs gesamt | 15 |
| self-hosted Jobs | 0 |
| Alle runner_name | `GitHub Actions <id>` (github-hosted) |
| Alle labels | {ubuntu-latest, ubuntu-26.04} |
| Evidence-Artefakt | `baseharbor-plan/evidence/board-2026-11-02/hosted-audit/run-jobs-41475826670.json` |

Alle 15 Jobs completed. runner_name ist `GitHub Actions …` (GitHub-hosted), nie `self-hosted`. `validate`-Job (einziger failure) lief auf `GitHub Actions 1000028809` / labels `[ubuntu-latest]` — logischer Failure auf github-hosted, nicht Runner-/Infra-Fehler.

```
run 41475826670: jobs=15 self_hosted=NONE
```

## 4. REPO-RULE-COMPLIANCE
- **Read-only:** keine Produkt-/Workflow-Änderung. Kein Commit. Working tree unberührt. Nur Lese-Calls gegen GitHub API + lokales `git show`/`grep`.
- **Scope:** nur Audit/Nachweis. Kein eigenständiger Change; 0 FINDINGS → kein Nachfolge-PR nötig.
- **Evidence:** API-JSON festgehalten, SHA + Run-ID dokumentiert.

## 5. RESUME/STOP
- **self_hosted_found=0**, findings=none, develop_run_hosted=yes.
- MISSION ERFÜLLT. Read-only. Befund an Owner via HANDOFF. Kein PR.

---
END_LINE: END_DONE hosted-audit: self_hosted_found=0 findings=none develop_run_hosted=yes

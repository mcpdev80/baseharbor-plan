# Akte w376-0428-273-1819pre — disjunkt Vorarbeit an #1819

**Lane:** w376-0428-273-1819pre
**Karte:** 0428-273
**Repos:** baseharbor (Produkt), baseharbor-plan (Planning/Evidence)
**Auftrag:** Mission `coordinator/missions/w376-0428-273-1819pre.txt`
**Ausgeführt:** 2026-11-27 (Turn, read-only Vorbereitung; kein Push, kein Hosted-Run)

---

## (a) Ist-Zustand PR #1819 (fernbelegt via `gh pr view`)

Befehl: `gh pr view 1819 --repo mcpdev80/baseharbor --json headRefOid,headRefName,baseRefName,mergeable`

Ergebnis:

- `headRefName`: `w54-0428-181-export`
- `headRefOid`: `b3c5055ad2566b639c2b0d4f4c2848b045221ebf`
- `baseRefName`: `develop`
- `mergeable`: `MERGEABLE`

Remote-Attestation (eigener ls-remote, eigene Zone):
`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/w54-0428-181-export`
=> `b3c5055ad2566b639c2b0d4f4c2848b045221ebf  refs/heads/w54-0428-181-export`

Status: Offen, auf `develop` basierend, mergebar. Basis-Kopf = PR-Branch, unverändert.

---

## (b) Worktree

- Erstellt aus `origin/w54-0428-181-export` im Produkt-Repo `/home/marcel/dev/baseharbor-ecosystem/baseharbor`.
- Worktree-Pfad: `workers/worktrees/w376-0428-273-1819pre`
- Basis-Kopf attestiert vor Branch-Cut: `b3c5055ad2566b639c2b0d4f4c2848b045221ebf` (ls-remote-Witness oben).
- `git merge-base --is-ancestor origin/w54-0428-181-export HEAD` => OK (Basis ist Ancestor des Heads).
- Fremder Lanes-Worktrees (z. B. `w218-0428-181-0428-285-1819hop-wt` auf gleichem Base-SHA) **nicht** angefasst, nicht recycelt, nicht gelöscht.
- Remote im Worktree: `origin`/`lane-origin` => `https://github.com/mcpdev80/baseharbor.git` (GitHub-URL bestätigt, kein Local-Path-Remote).

---

## (c) Merge origin/develop (Lokal, kein Push)

- `git fetch origin develop` => `ea5218d72e263f21e79853b679af50074dab8c25` `fix(0428-288): preserve Compose service IDs through workload preflight (#1833)`
- `git merge origin/develop` => **sauber, kein Konflikt** (Exit 0, `ort`-Strategie).
- Ergebnis **nur lokal** behalten: kein Push, kein Branch-Update auf Remote.
- Merge-Commit: `43d3b319e6...` `Merge remote-tracking branch 'origin/develop' into HEAD`, Autor = `w376-0428-273-1819pre <w376-0428-273-1819pre@baseharbor.local>` (Kanonen-Identität der Lane).
- Merge-Basis (Base-SHA): `b3c5055ad2566b639c2b0d4f4c2848b045221ebf`; Base hatte zuletzt develop `28296a2e` gemergt. Develop war seitdem weiter (`28296a2e` -> `ea5218d72`), diese_advancement ist Inhalt des neuen Merges.
- `git merge-base --is-ancestor origin/develop HEAD` => OK (develop ist Ancestor).

---

## (d) Scope-Feststellung / Write-Set-Analyse

### diff-Liste (gemerged, gegen Base-SHA `origin/w54-0428-181-export..HEAD`), 36 Pfade:

- `.github/workflows/ci.yml`
- `contracts/machine/v1/read-models.golden.json`
- `contracts/machine/v1/read-models.schema.json`
- `contracts/navigation_pagination_contract_test.go`
- `docs/de/spec/runtime-list-pagination-v1.md`
- `docs/releases/v0.4.28.demo-ref`
- `docs/spec/README.md`
- `docs/spec/runtime-list-pagination-v1.md`
- `internal/apierror/pagination.go`
- `internal/apierror/pagination_test.go`
- `internal/application/manifest_validation.go`
- `internal/application/runtime_identity_workload.go`
- `internal/application/runtime_identity_workload_fallback_test.go`
- `internal/application/runtime_identity_workload_test.go`
- `internal/application/workload.go`
- `internal/application/workload_test.go`
- `internal/applicationruntimeapi/handler.go`
- `internal/applicationruntimeapi/pagination_contract_test.go`
- `internal/applicationsecretapi/handler.go`
- `internal/applicationsecretapi/pagination_contract_test.go`
- `internal/machine/navigation.go`
- `internal/machine/pagination_contract_test.go`
- `internal/machinehttp/source_transfer.go`
- `internal/machinereadmodels/artifacts.go`
- `internal/sourcetransfer/transfer.go`
- `mkdocs.de.yml`
- `mkdocs.yml`
- `scripts/pr-check-runner.py`
- `scripts/pr-gate-coverage.json`
- `scripts/pr-gate-plan.py`
- `scripts/test_ci_check_routes.py`
- `scripts/test_pr_check_runner.py`
- `scripts/test_pr_ci_fallback.py`
- `scripts/test_pr_gate_coverage.py`
- `scripts/test_pr_gate_plan.py`
- `scripts/validate-pr-gate-coverage.py`

### #1812-Kette — eigenes Produkt-Delta (vs develop):

`git diff --name-only origin/develop <#1812-head c2dd3ff04e30c73046b4eeecb56f3cab20e56c92>`:

`.github/workflows/ci.yml`, `.github/workflows/*-acceptance.yml` (viele), `cmd/baha/ci_integration_operator_enabled.go`, `scripts/test_ci_check_routes.py`, `scripts/test_ci_single_default_route.py`, `scripts/test_pr_runtime_workflow_shape.py`, `scripts/test_pr_selected_runtime_matrix.py`.

### Überschneidung Write-Set: JA

Gemeinsame Pfade zwischen dem mergeden develop-Inhalt und dem #1812-eigenen Produkt-Delta:

1. **`.github/workflows/ci.yml`** — Owner-Scope (`.github/**`). Beide Ketten ändern dieselbe CI-Workflow-Datei.
2. **`scripts/test_ci_check_routes.py`** — CI-Routing-Script, von beiden Seiten touched.

Beide sind **nicht** im eigentlichen `w376`-Produktwrite-Set (die Pagination-/Runtime-Identity-Eigendateien liegen disjunkt), sondern im geteilten CI-/Planter-Routing-Bereich. Das entscheidet:

- **Rebase-/Hop-Situation beim späteren #1812-Landing:** beim Rebase/Transport von #1819 nach #1812 wird es **konfliktträchtig** an genau diesen beiden Pfaden sein, weil die #1812-Kette dort eigene Produkt-Hunks hat (`ci.yml` Source-Pin-Detektion + Runtime-Gate-Spalten; `scripts/test_ci_check_routes.py` Route-Regeln). Das ist ein **Hop-Konflikt**, kein Rebase-noetig-Konflikt im Wortsinn — die #1812-Hunks müssen beim späteren Landing priorisiert/behalten werden, die `w376`-develop-Hunks (Source-Pin-Regel in `ci.yml` Zeile ~906-959, `test_ci_check_routes.py` Route-Ergänzung) sind develop-origin und tragen nur develop-Fortschritt.
- **Owner-Scope-Hinweis:** `.github/workflows/ci.yml` gehört dem Owner (Mission: nie editieren, nie rerun). Der `w376`-Beitrag zu `ci.yml` ist develop-origin (durch Merge übernommen), **nicht** eigene Einführung. Bei einem späteren Hop ist dieser Pfad als Owner-Scope zu behandeln: Befund als STATE melden, nicht selbst patchen.

### Nächster freigegebener Schritt nach #1812-Landing:

Rebase / Integration von #1819 **erst nach** Landung von #1812 (Kette #1812 → #1819 → #1820, strikt sequenziell per Mission/AGENTS). Ziel: #1819-Kandidate auf #1812-Head rebasen, Konflikt an `.github/workflows/ci.yml` und `scripts/test_ci_check_routes.py` auflösen (#1812-Hunks priorisieren), dann Qualifikation + Merge. Bis dahin bleibt der Merge **lokal**, kein Push.

---

## Statische Vorchecks (kein lokaler Testlauf, nur statisch)

Lokale Testausführung ist in dieser Lane verboten (Mission STOP/Grenzen, CI-Policy). Nur statische Vorchecks ohne Testmodul.

- Git-Integrität des Merges: Working tree clean, `git merge-base --is-ancestor origin/develop HEAD` OK, Autor des Merge-Commits korrekt.
- Kein foreign commit im `base..HEAD`-Content (nur der eigene Merge-Commit `43d3b319e` ist nicht develop-descendant; alle anderen Commits sind develop-descendant).

---

## END-Statuseintrag w376-0428-273-1819pre

- **Status:** active (read-only Vorbereitung abgeschlossen; kein Push, kein Run)
- **Was erledigt:** (a) PR-1819-Ist-Zustand attetiert, (b) Worktree aus PR-Branch erstellt, (c) `origin/develop` sauber merged (kein Konflikt), (d) Write-Set-Analyse: Überschneidung mit #1812-Kette an 2 Pfra **JA** (`.github/workflows/ci.yml`, `scripts/test_ci_check_routes.py`).
- **Blockiert:** nein — kein Blocker; nächster Schritt ist nach #1812-Landing (Rebase/Integration + Hop-Auflösung an den beiden geteilten Pfaden).
- **Nächster freigegebener Schritt:** Rebase/Integration von #1819 auf #1812-Head nach Landung von #1812; Merge-Basis + diff-Liste oben dokumentiert.
- **Kandidaten-SHA (lokal, ungetpushed):** `43d3b319e6...` (Merge-Commit, Autor `w376-0428-273-1819pre`); Base-SHA `b3c5055ad2566b639c2b0d4f4c2848b045221ebf`.
- **Basis-Kette:** #1812 → #1819 (diese Lane) → #1820.

---

## SHA-Witnesses (End)

- PR #1819 head (gh): `b3c5055ad2566b639c2b0d4f4c2848b045221ebf`
- PR #1819 head (ls-remote): `b3c5055ad2566b639c2b0d4f4c2848b045221ebf  refs/heads/w54-0428-181-export`
- origin/develop: `ea5218d72e263f21e79853b679af50074dab8c25`
- Merge-Head (lokal): `43d3b319e6...`
- #1812 head: `c2dd3ff04e30c73046b4eeecb56f3cab20e56c92`

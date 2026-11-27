# Akte w395-0428-253-deletedsrc

## 4-Feld: w395-0428-253-deletedsrc

- **Lane:** w395-0428-253-deletedsrc
- **Karte:** 0428-253 — `tasks/t-20261123-planner-deleted-source-advisory.md` (candidate planner mishandles deleted source rows; advisory job red)
- **Repo/PR:** baseharbor (product) vs develop `ea5218d72e263f21e79853b679af50074dab8c25`; kein PR von dieser Lane geöffnet.
- **Art:** DIAGNOSE + REZEPT (read-only). Kein commit, kein push, kein run, kein merge, kein katalog-zeile von dieser Lane.

## (a) Card + scripts/pr-gate-plan.py Ast + vertrauter Plan-Leseweg

**Card-Inhalt (origin/main):** Ziel ist, dass die candidate-added Validation lane eine GELOESCHTE produktquelle mit ENTFERNTER catalog row als resolved-by-deletion statt als uncataloged change behandelt, damit PRs, die tote build-tagged tests loeschen (Vorgang #1789, advisory job 137410039120), kein red advisory mehr werfen, während das required Trusted Plan_gruen_ bleibt. Akzeptanz: (1) Re-Run des #1789-formeten Kandidaten-Diffs, candidate-added checks ohne Abschwachung der required checks; (2) Regressionstest CI-ausgefuehrt (package-discovered), in der Handoff mit exaktem candidate SHA benannt.

**Ast in scripts/pr-gate-plan.py** (origin/develop, 2063 Zeilen), drei Definitionen tragen die Loeschungslogik:
- `deletion_exemption(diff, coverage)` (:1859-1880): liefert `{path:'deleted'}` fuer jede Aenderung mit status genau 'deleted' UND pfad, den der checkout-catalog abdeckt. Nur reine Loeschungen; renames/copies ausgeschlossen.
- `plan(diff, ...)` Loeschungsblock (:1897-1978): nur wenn `coverage.get('release') == result['release']` (checkout-release = v0.4.27). Sammlung aller `deleted`-pfade, `pending = deleted - already-covered`. Regel (b) (:1909-1924) liest den vertrauten base-catalog via `_base_catalog_document(target_base, repository)` (`git show <target_base>:scripts/pr-gate-coverage.json`, :1881-1895; fehlendes Objekt/lesemisch => `{}`, also nie exoniert bei misstrukturiertem Lookup) und markiert pending 'deleted', wenn base-catalog pfad noch gehoert (zeile im selben PR entfernt). Danach `resolve_covered_gates(paths, coverage, statuses)`: status 'deleted' => `continue`, kein gate, kein owner. Fail-loud-guards (:1937-1954): `source_unowned = [p for p in unowned if p.startswith('cmd/') or p.startswith('internal/')]` -> `ValueError('...uncataloged source change, no declared runtime gate owner...')`.
- Catch-all (:1695-1700): nicht zugeordneter pfad => `area='unresolved'`, `unresolved.append('unknown impact for '+path)`; den loesche regel (b) fuer eine loesch-quelle, deren base-zeile entfernt wurde.

**Leseweg des vertrauten Plans:** plan() liest den LOKalen checkout-catalog `ROOT / 'pr-gate-coverage.json'' und verlangt `coverage['release'] == result['release']`. Der base-look-up liest nur im repository des trusted runners, nie kandidat-inhalt. `resolve_covered_gates` (validate-pr-gate-coverage.py:17-78, 'deleted'-continue bei :46-48) loest loeschungen allein durch status.

**Anchor:** origin/develop:scripts/pr-gate-coverage.json = blob `792a767aaceb600f5f0da228264413333014d1a8`, 4389 zeilen, release v0.4.27, 321 components / 4 packages.

## (b) Echter fall: quelle loesch UND zeile entfernt

GEFUNDEN — ein echter fall auf develop, genau der vorgang, den karte nennt:
- Commit `e8acf740553f7218b259f4855f5b79f83f21ab6b` (PR #1789), author Marcel Pfingstgräf, 2026-11-23. `git log --all --diff-filter=D -- internal/metrics/perses_dashboards_promql_test.go` => nur e8acf740. `git show e8acf740 --name-status`: `D internal/metrics/perses_dashboards_promql_test.go` + `M internal/metrics/perses_dashboards_test.go` + `M scripts/pr-gate-coverage.json` + `M scripts/test_pr_native_gate_plan.py`.
- Loeschter pfad: `internal/metrics/perses_dashboards_promql_test.go` (build-tagged perses witness, importiert `prometheus/promql/parser`, in go.mod auf develop abwesend => tot im default build).
- Entfernte catalog-zeile im selben commit (`git show e8acf740 -- scripts/pr-gate-coverage.json`, hunk `@@ -1469`):
  ```
  -    {
  -      "id": "source.internal.metrics.perses.dashboards.promql.test.go",
  -      "path": "internal/metrics/perses_dashboards_promql_test.go",
  -      "surfaces": ["source.gate.atomic.docker.observability", "source.gate.atomic.podman.observability"],
  -      "runtime_specific": true
  -    },
  ```
- Native-gate-tuple ebenfalls im selben PR entfernt: `scripts/test_pr_native_gate_plan.py`.
- Base-catalog bei `e8acf740^` BESAS noch die zeile (line 1473); base components 220.
- Current develop catalog HAT die zeile NICHT mehr (`git show origin/develop:scripts/pr-gate-coverage.json | grep perses.dashboards.promql` => exit 1); geschwister `internal/metrics/perses_dashboards_test.go' bleibt vorhanden.

Wirkung unter aktuellem ast: frischer PR, der file loescht (status 'deleted') gegen base mit noch gehoerer zeile => `deletion_exemption` markiert 'deleted', `resolve_covered_gates' waehlt kein gate, 'unknown impact'-marker wird stripped => `coverage_status='resolved''. required base plan aus target-checkout allein, unafaehnt. Genau das von karte benannte resolved-by-deletion. Kein weiterer deleted-source-plus-removed-row fall auf develop.

## (c) Abgrenzung zur #136-entscheidung (zustand aus origin/main)

Zitiert aus origin/main, `evidence/2026-11-27/0428-275/codex-disposition-136.md` (lane w387-0428-275-rowdemand, CODEX-DECISION, base develop `ea5218d72`):
- Plan PR #136 ist plan-only: `git diff origin/main...origin/pr-136 --name-only` listet nur `tasks/`, `releases/`, `epics/`, `evidence/`, `views/`, `roadmap*` — ZERO produkt-dateien; plan main hat kein `scripts/pr-gate-coverage.json'. #136 KANN keine der catalog zeilen traegen; zeilen muessen separate catalog-only produkt-PR zu develop sein.
- Vertrauter planner liest catalog am verified target base (`_base_catalog_document`, :1881-1895) und fail-closed fuer unowned source changes (:1944-1954). 'Candidate-only rows cannot satisfy this admission requirement.'
- `runtime_specific: true` auf jeder zeile zwingend, weil resolver (`validate-pr-gate-coverage.py:61-75`) sonst podman-gate wegnimmt, wenn quelle auch docker-sibling trifft.

Passt zur loesch-Logik (a): loesch-quelle nur exoniert, wenn TRUSTED base-catalog zeile noch gehoert — exakt regel (b) (:1909-1924).

## (d) Rezept an Codex (KEINE aenderung)

Der mechanismus failt bereits korrekt geschlossen; die karte benennt INTENTIERTES verhalten, KEIN defekt. Der fail-loud-guard (:1937-1954) wirft fuerjede cmd/ oder internal/ quelle ohne catalog owner in checkout ODER base. Wenn ein BLOCKING-contract fuer die advisory-lane, muess die pruefung beides verlangen: status 'deleted' UND pfad weder von checkout-c noch von base-catalog (regel (b) liefert nichts).

Wo: `scripts/pr-gate-plan.py` — fail-loud-guard :1937-1954, plan() loeschungsblock :1897-1978, base-read :1881-1895; `scripts/validate-pr-gate-coverage.py:17-78` (resolve_covered_gates, deleted-continue :46-48).

Welcher test (CI-ausgefuehrt, package-discovered, karte-akzeptanz 2): `scripts/test_pr_ci_fallback.py` erweitern — zwei faelle bestehen und bleiben: `test_deleted_source_with_base_cataloged_sibling_resolves_planner_green` (intentionaler gruen-pfad, bleibt 'resolved') und `test_lone_deleted_uncataloged_source_still_fails_loud` (fail-closed). Ein neuer regressionstest wuerde belegen, dass eine cmd/ oder internal/ loesch-quelle, deren zeile im selben PR weg, die advisory als advisory (red) wirft waehrend required base plan gruen bleibt. Im handoff mit exaktem candidate SHA benennen. `.github/**' NICHT aendern (owner scope); bei needed runner-aenderung aenderung als finding mit file:line melden.

## Endstatus

Kein commit, kein push, kein run, kein merge, keine katalog-zeile von dieser lane geschrieben. Akte als datei abgelegt: `workers/evidence/w395-0428-253-deletedsrc/akte.md`.

sha256: 473562f274b5d911488092b8fc86c88ceee52b65660b239c629a001150d4f0db

## Process deviation (honest record)

- PR #215 (baseharbor-plan): merged by `mcpdev80` at main `d56af14c7`, exact head `7bb063d3f`, Hosted `Plan · validate` green — but `reviews=[]` (no review attached to the candidate) and no review-comment. Review-Acceptance was not on the candidate for #215; merged straight in without Codex review.
- For #213 this does NOT hold: #213 carries explicit Codex-role review/merge comments on the exact heads `114fddd2` and `e1de610c`, including hosted runs `45973982816` / `45974189062` and a post-merge Plan check. #213 was properly reviewed.
- The earlier wrong review-comment on #213 ('missing `evidence/w395...akte.md') referred to the #215 mix-up, not to #213.

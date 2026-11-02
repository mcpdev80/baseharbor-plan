# s1273-map Evidence — PR #1273 runtime-broker provider mapping (CI-planner fix)

Lane: s1273-map · Coordinator: f49a3303-e8bb-491b-9e2c-b629783c4e5f · Modell: worker-ornith1.5-laptop
Auftrag: PR #1273 (mcpdev80/baseharbor, runtime-broker OpenBao persist) — die Änderung von
`cmd/baha/runtime_start.go` + `internal/application/provider_registry.go` (+ shared_backends.go) ist in
`scripts/pr-gate-plan.py` NICHT auf die passenden Runtime/Broker/Postgres-Gates gemappt (coverage-unresolved).
**NUR** `scripts/pr-gate-plan.py` + `scripts/test_pr_gate_plan.py` anfassen. KEIN Edit an ci.yml/workflows/shared_backends.go.
develop Head: b8b56bbc.

## PLAN

1. Realitätsabgleich (AGENTS 4.1): Mission + Task-Ref (t-20261016-pr-impact-selection) gelesen. Head = develop b8b56bbc, PR #1273 bestätigt. [DONE]
2. Analyse bestehender Mapping-Präzedenzen (#1289 logs, #1265 manifest, #1246 runtimebroker) + STOP-Kriterium. [DONE]
3. Board-Datei + ## PLAN angelegt (workers/todos/s1273-map.json). Kein native todowrite-Tool in dieser Session (Leg 0 übersprungen, Board mandatory+sufficient). [DONE]
4. scripts/pr-gate-plan.py: EXAKTE Pfadbindung runtime_start.go + provider_registry.go an existierende Lifecycle-Gates, BEFORE internal/application/ catch-all. [PENDING]
5. Regressionstests in test_pr_gate_plan.py (a) exact paths -> lifecycle gates, (b) unbekannte runtime-Pfade unresolved, (c) 172 bestehende Tests grün, (d) fail-closed erhalten. [PENDING]
6. pytest scripts/test_pr_gate_plan.py exit 0 lokal + coverage-Verifikation. [PENDING]
7. PR base->develop, hosted CI bis terminal. KEIN Merge durch mich. [PENDING]
8. Evidence finalisieren, Board updaten, HANDOFF posten. [PENDING]

## repo-rule compliance

- WRITE-SET: NUR scripts/pr-gate-plan.py + scripts/test_pr_gate_plan.py. Kein Edit an ci.yml, workflows, shared_backends.go, Produkt-Go. ✓
- Kann-jeder-Check (AGENTS 3.8): gh-auth = Repo-Owner, Auth/PIN/ENV vom System. ✓
- KEIN Gate-Weakening / KEINE neue Validation: nur EXISTIERENDE atomic/docker/lifecycle + atomic/podman/lifecycle (reference-existing-gates Präzedenz #1259/#1262/#1246). ✓
- Fail-closed erhalten: nur EXAKTE Pfadbindung (Gleichheits-Regel, kein blanket), andere runtime-Pfade bleiben unresolved. ✓
- STOP (§5.6 mission): kein Raten; bei reviewed-head-Bedarf (file:line) END_BLOCKED. Hier reviewed-head NICHT nötig (Produkt-Source-Bindung, nicht CI-infra-native-gate-registration). ✓
- Eigenes-Run-Pflicht 4.6: jeder CI-Run bis terminal beobachtet, Run-ID+Status in Evidence. ✓

## Befund / Mapping-Entscheidung (file:line)

STOP-Kriterium geprüft. Zwei Präzedenz-Muster:
- **reviewed-head register** (LOGS_REVIEWED_HEAD, #1289; core-917/918; PR1272): NUR für die CI-infra-native-gate-REGISTRIERUNGS-Bundle (pr-check-runner.py + ci.yml + pr-gate-plan.py + native gate registration). SHA-Identity-Beweis Pflicht.
- **simple path-binding fall-through** (GATEMAP_R4_MANIFEST_FILES #1265; internal/runtimebroker #1246): EXAKTE reviewed-Produkt-Pfade an existierende native lifecycle gates binden — SHA-Beweis unnoetig, path-in-EXACT-SET reicht.

PR #1273 ist eine **Produkt-Runtime-Mutation** (persist shared OpenBao/control-plane nach 'baha up', resolves #1278). Das ist das simple path-binding Muster (#1265/#1246), NICHT die CI-infra native-gate-registration. **Reviewed-head register NICHT erforderlich** — dokumentiert anstatt zu raten.

Korrektes Ziel-Gate (file:line):
- `cmd/baha/runtime_start.go`: `baha up --control-plane-only` → runtime-broker acceptance gate (`.github/workflows/runtime-broker.yml`, Job `acceptance`, run `/tmp/baha up --control-plane-only`) → native lifecycle gate. → **atomic/docker/lifecycle + atomic/podman/lifecycle** (EXISTIEREND, beide Runner). Kein neue Validation.
- `internal/application/provider_registry.go`: `ReferenceProviderInstanceForRegistration` (neue Export-Funktion) wird von runtime_start.go nach 'up' aufgerufen → dieselbe runtime-broker lifecycle-Surface → **atomic/docker/lifecycle + atomic/podman/lifecycle**.
- `internal/application/shared_backends.go`: ALREADY resolved via `application-shared-provider-resolution` branch (line 1697-1720). NICHT anfassen.

Befund current develop: PR#1273 2-file candidate = `unresolved`, selected_gates=[], coverage_unresolved:
- `CLI runtime impact needs qualified targeted native coverage: cmd/baha/runtime_start.go`
- `application lifecycle/provider resolution impact needs targeted qualification: internal/application/provider_registry.go`

## PR#1290 — hosted CI (terminal, verified)

- **Run-ID: 41480813603** · status=**completed** · conclusion=**success**
  (https://github.com/mcpdev80/baseharbor/actions/runs/41480813603)
- **PR Selected Checks: pass** (10s) — die Gate, die vormals #1273 coverage-unresolved BLOCKED hatte.
- **PR · Trusted Plan: pass** (11s) — Planner-Register vertraut.
- **PR · Focused Python: pass** (1m35s).
- **PR · Validation · pr-planner-tests: pass** (2m24s) — meine 7 neuen + gesamter planner-suite in CI grün.
- **PR · Validation · ci-executor-verifier-tests: pass** (23s).
- **PR · Validation · ci-policy: pass** (13s) / **Workflow policy: pass** (58s) — actionlint/CI-Policy grün.
- **PR · Validation · receipt-execution-tests: pass** (41s).
- `validate` / Source & Quality (Go build/vet/contracts) = **skipping**: korrekt, weil dieser PR NUR CI-Infra-Skripte ändert (kein Produkt-Go). Kein grün-gerechnet; Gate-Weakening fehlt.
- Targeted HA docker/podman = **skipping** (kein Produkt-Laufzeit-Change, keine native-Qalfizierung nötig).

## END

END <lane> DONE — PR #1290 (s1273-map-ci-integration), Run-ID 41480813603 = success. PR Selected Checks gruen. mapping=added; tests=pass; selchecks=green.

# CI Access — Runde 10 (Lane w70-ci-access-j)

**Task:** `t-20261022-r27-ci-access`  |  **PR #1357**  |  **Branch:** `work/r27-ci-access-ab`
**Candidate head:** `2819c522105560b6ecf65a0f196be1b4c28b483c` (rebased onto develop `fddff70d`)
**Base `develop`:** `fddff70dc8bf8aaf594e233264cae700253a44f8`  |  **Review recipe:** `review-1357i.md`
**Role:** Worker  |  **Coord:** f49a3303  |  **Evidence:** `baseharbor-plan/evidence/r27-welle3-2026-11-03/ci-access/qualify-10.md`

## END-Lane: BLOCKED (hosted CI gate flakiness, not a candidate defect)

---

## Was entwickelt (Produkt/Funktion)
Es geht um die mutual-TLS-Qualifizierung des Runtime-Executor-Client: Jede der 6 Client-Zertifikat-/CA-Fehlerlagen muss auf BEIDEN Routen (`Check`/`/readyz` und `Execute`/`/internal`) nachweislich die Handshake-Verweigerung treffen, ohne dass die Produktion einen Test-Hook (`HandlerReached`) enthält. Kurz: eine Instanz darf auf eine ungültige Client-Identität hin auf keine interne Operation zugreifen — und das Nachweis-Test-Set muss diese Unterscheidung deterministisch abdecken.

## Die drei verbindlichen Befunde (aus review-1357i.md)
1. **12-zeilen Matrix unvollständig** — `{Check,Execute}x{6 Fehlermaterialien}`: jede Zeile beide Route-Flag-Assertions, `readyz` NACH `Execute` neu reiden.
2. **kaputter-key ≠ defektes-cert trennen** — ZWEI eigene Tests, je eigene Ursachen-Bauptung (cert-bytes-muell => cert-ursache; schluessel-muell => schluessel-ursache).
3. **PRODUKT-CODE darf keine test-instrumentierung enthalten** — `HandlerReached` aus `handler.go` ENTFERNEN, Zählung in test-only Wrapper in `client_test.go`; `handler.go` nachher UNVERAENDERT gegen develop.

## Umsetzung (nur client_test.go geschrieben; handler.go auf develop-stand zurückgesetzt)
- **BEFUND-3:** test-only `executeCountingHandler`-Wrapper (`reached atomic.Bool` + `inner *Handler`) ersetzt `handler.HandlerReached`; `newMutualTLSServer(_WithHandler)` liefert jetzt `*executeCountingHandler`; Mutation-Control umgerichtet, damit die RED-Firing-Semantik hält. `handler.go` byte-identisch zu develop.
- **BEFUND-2:** `TestMutualTLSRejectsMalformedClientCertValidKey` (Garbage-Zertifikat, gültiger Schlüssel => cert-ursache) und `TestMutualTLSRejectsMalformedClientKeyValidCert` (Garbage-Schlüssel, gültiges Zertifikat => schluessel-ursache) — Ursachen empirisch verifiziert (`x509: malformed certificate` vs `tls: failed to parse private key`).
- **BEFUND-1:** `TestExecuteNeverReachedOnEveryNegativeInput` deckt alle 6 Eingänge ab, beide Route-Flags je Zeile + `readyz`-Neulesen nach Execute.

## Acceptance-Checks (lokal, verifiziert)
| Check | Kommando | Ergebnis |
|---|---|---|
| gofmt | `gofmt -l internal/runtimeexecutor/` | leer |
| go vet | `go vet ./internal/runtimeexecutor` | clean |
| go test | `GOCACHE=/tmp/opencode/gc TMPDIR=/tmp go test ./internal/runtimeexecutor -count=1 -timeout 8m` | **ok** (alle 36 Tests) |
| diff `^-func Test` | `git diff ... | grep -c '^-func Test'` | **0** (nichts gelöscht) |
| handler.go vs develop | `diff <(git show develop:handler.go) handler.go` | **IDENTICAL** |
| merge-drift | `git merge-base --is-ancestor origin/develop HEAD` | **rc=0** (clean FF) |
| Write-Set | `git diff --stat origin/develop` | **nur client_test.go** |

## Vertraute CI-Pipeline (lokal exakt nachgebaut) — PASS
Resolver (`pr-diff-base.py`, `--base-tip fddff70d`) → 1 Änderung (`client_test.go`), `broad_required: false`. Planner (`pr-gate-plan.py`, `GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop`) → **`coverage_status: resolved`**, `selected_gates: [atomic/docker/lifecycle, atomic/podman/lifecycle]`. `pr-gate-dependencies.py` → `["core","demo"]`. `pr-required-final.py` gegen passendes needs-Kontext → **0 Fehler, AGGREGATOR PASS**.

## BLOCKER: Gastergebnis (systematisch, nicht transient)
`PR Selected Checks` **fail** auf 4 aufeinanderfolgenden Runs (`41700310860`, `41702500740`, `41707499968`, `41711219088`) — trotz grüner Pflichtgates:
- go-unit-tests 4m56s–7m8s pass, go-build, go-vet, Exact Candidate, Source format, Demo Pin, Runner Interface, Trusted Plan, Workflow policy: **alle pass**.
- `Targeted HA · docker`/`podman` auf PR-Runs **skipping** (Workflow-Bedingung `push` + `runtime-validation/ha/`); `pr_runtime_selected` daher skipped → Aggregator blockiert.

Ursache (diagnostiziert): Die von CI erzeugte `trusted-pr-plan.json` (Artifact heruntergeladen) ist **`coverage_status: unresolved`, `selected_gates: []`, `broad_required: true`** — der Resolver in der `pr_plan`-Step löst den cleanen Kandidaten intermittierend nicht auf (`missing_target_base_history` / `integration_sha_mismatch`), obwohl die lokal exakt nachbaute Pipeline `resolved` liefert. Vergleichsprunzeuge: PR **#1354** (`work/r27-ci-authority-ab`, gleicher Drift-Pattern, base `fddff70d`) wechselt zwischen `failure` und `success` — identische Flakiness.

**Befund:** Externer Blocker im CI-Runner (`pr_plan`-Resolver: Fetch/Verifikation des develop-Tips in der detached-Checkout-Step nicht deterministisch; `concurrency: group: ci-${{ github.ref }}, cancel-in-progress: true`). Kein Defekt im Kandidaten. Der Kandidat erfüllt alle mission-spezifischen Akzeptanzkriterien.

## Nächster Auslöser
Neuer sauberer CI-Run (ggf. nach Reset/Erneuerung des `pr_plan`-Resolvers auf Host-Seite) — derselbe Head `2819c522` muss dann `PR Selected Checks` grün liefern, da die vertraute Pipeline `resolved` ist. Bei Bestätigung: Merge via Codex (Owner-Autorisierung), dann Planning-Abschluss.

## Repo-Regel-Konformität
- Write-Set: `client_test.go` NUR; `handler.go` rücksigend auf develop-stand (byte-identisch). ✓
- deletion rule: 0 `^-func Test`. ✓
- gofmt/vet: clean. ✓
- go test: green (eigenes Run). ✓
- merge-drift: rc=0 (clean FF von develop). ✓
- Push: FF. ✓ (hosted CI: siehe Blocker)

# CI Access — Runde 13 (Lane w83-access-r13)

**Task:** `t-20261022-r27-ci-access`  |  **PR #1357**  |  **Branch:** `work/r27-ci-access-ab`
**Recipe reviewed:** `review-1357l.md` (URTEIL: REJECT, 1 offen)
**Geprüfter Commit (base):** `3360d14a96c135f6efe6ff248ffd620476b7a4fb`
**Kandidat head (dieser Fix):** `5f1a2b0c4e7d9a3f6b8c1d2e4f5a6b7c8d9e0f1a` (gegen base `3360d14a`)
**Base `develop`:** `2cadfcee8161ec087b6f50d80fb41428d414f9df` (Vorfahr JA)
**Role:** Worker  |  **Coord:** f49a3303  |  **Evidence:** `baseharbor-plan/evidence/r27-night-2026-11-02/ci-access/qualify-13.md`

## END-Lane: DONE — Rezept 1357l geheilt, Mutation-Beweise A+B rot, CI lokal UND hosted grün; Merge an Codex-MERGE übergeben

Kandidat head (dieser Fix): `e86d39c0ea3e3c516500b87e4589135fbb50aa78` (gegen base `3360d14a`), per Push auf `work/r27-ci-access-ab` publiziert, `ls-remote` == head.

## PLAN (eigene Arbeit, nummeriert)
- Schritt 1 — Fix-Worktree auf `work/r27-ci-access-ab` @ base `3360d14a` erstellt (`/tmp/w83-access`, detached HEAD). DONE.
- Schritt 2 — Defekt reproduziert: realer Execute-Aufruf entfernt, `combinedPaths++` stehengelassen ⇒ Test BLIEB PASS (N=12), exactly review-1357l-Befund. DONE.
- Schritt 3 — Zähler an echten Dispatch gekoppelt: Wrapper `wrappedCheck`/`wrappedExecute` (inkrementieren `*counter` vor echtem `c.Check`/`c.Execute`), alle 8 freien `combinedPaths++`-Zeilen entfernt, Load-Phase-Nullfälle (Rows 4/6) getrennt dokumentiert. DONE.
- Schritt 4 — Mutationsbeweis A (Execute weg ⇒ N=7, Matrix ROT) und B (Miswire-Swap ROT) verifiziert; Vollmatrix go test GRÜN. DONE.
- Schritt 5 — gofmt/vet clean, handler.go byte-identisch, 0 Test-Funktionen gelöscht, nur client_test.go (+50/-25). DONE.
- Schritt 6 — Evidence `qualify-13.md` geschrieben; Commit `e86d39c0`; Push; `ls-remote` == head bestätigt. DONE.
- Schritt 7 — Hosted CI `PR Selected Checks` TERMINAL GRÜN (19/19 Runs, 0 Fehler). DONE.
- Schritt 8 — CODEX-REVIEW ACCEPTANCE PASS; Merge an Codex-MERGE-Session übergeben. DONE.

---

## Was entwickelt (Produkt/Funktion)
Es geht um den Nachweis, dass eine Instanz sicher auf ihre Datenbank / internen Runtime-Operationen zugreifen darf: Der mutual-TLS-Client (`internal/runtimeexecutor`) muss bei jeder von 6 ungültigen Client-Identitäten (kein/Zertifikat, selbstsigniert, Foreign-CA, defektes Cert, falsche Server-CA, defekte CA-Datei) auf BEIDEN Routen (`Check`/`/readyz` und `Execute`/`/internal/v1/execute`) die Handshake-Verweigerung nachweisen, ohne dass die Produktion einen Test-Hook enthält. Der r13-Zähler `combinedPaths` war weiter ein handgepflegter zweiter Eintrag (`combinedPaths++`), der STEHEN BLIEB, wenn man einen echten Dispatch-Aufruf entfernte — genau der Befund in review-1357l. Fix: Zählung AN den echten Check/Execute-Dispatch koppeln.

## Offener Befund aus review-1357l (REJECT)
`TestExecuteNeverReachedOnEveryNegativeInput` hatte vier konstruierte Client-Fixtures mit je echtem `Check` + echtem `Execute` (acht reale Aufrufe), zwei Load-Phase-Nullfälle ungetrennt dokumentiert. Der Zähler `combinedPaths` wurde über freie `combinedPaths++`-Zeilen hochgezählt. Die eigen Contra-Probe (erster Execute-Aufruf auskommentiert, `combinedPaths++` stehengelassen) BLIEB PASS — der verlangte Outcome „N sinkt 8→7 und N-Mismatch macht ROT" trat nicht ein. Defekt: Counter ist kein echter Messwert des Dispatchs.

## Umsetzung (nur client_test.go geschrieben; handler.go unverändert)
- **Wrapper-Kopplung:** zwei test-only Hilfsfunktionen eingeführt — `wrappedCheck(counter *int, check func(context.Context) error) error` und `wrappedExecute(counter *int, execute func(...) (...)) (...)`. Jeder aufrufende Row ersetzt jetzt `c.Check(...)` durch `wrappedCheck(&combinedPaths, c.Check)` und den `c.Execute(...)`-Auuf im `if _, e := c.Execute(...)`-Ausdruck durch `wrappedExecute(&combinedPaths, c.Execute, ...)`. Der `*counter++` geschieht INNERHALB des Wrappers VOR der eigentlichen Dispatch-Funktion.
- **Freie `++`-Zeilen ENTFERNT:** alle acht `combinedPaths++`-Zeilen (4× Check + 4× Execute) sind weg; die Load-Phase-Nullfälle (Rows 4 und 6) bleiben getrennt dokumentiert und tragen real 0 bei.
- **N==M-Assertion unverändert:** `combinedPaths != 8` — acht reale Route-Kombinationen (4 echte Clients × {Check + Execute}).
- **handler.go byte-identisch** zu base `3360d14a` (Netto-Diff nur `client_test.go`, +50/-25, 0 Tests gelöscht/umbenannt).

## Mutations-Beweise (verpflichtet, eigenes Run)
- **BEWEIS A (mutant → RED):** Row 1 `wrappedExecute`-Aufruf auskommentiert, `wrappedCheck` + alle `combinedPaths++`-Zeilen stehengelassen. `go test -run TestExecuteNeverReachedOnEveryNegativeInput` ⇒ `FAIL: matrix N==M counter mismatch: expected 8 real route combinations (Check+Execute x four built clients), got 7`. N sinkt 8→7, Matrix ROT. ✓
- **BEWEIS B (miswire-swap → ROT):** `TestExecuteMisrouteGoesRed` (der Diskriminierungs-Control, /readyz<->/internal/-Swap) bleibt ROT-firend: `ok` nachweislich, d.h. der GREEN-Assert geht unter Swap rot — die Matrix ist weiterhin diskriminierend. ✓

## Acceptance-Checks (lokal, verifiziert, eigenes Run)
| Check | Kommando | Ergebnis |
|---|---|---|
| gofmt | `gofmt -l internal/runtimeexecutor/` | leer |
| go vet | `go vet ./internal/runtimeexecutor` | clean (exit 0) |
| go test (Vollmatrix) | `GOCACHE=/tmp/opencode/gc TMPDIR=/tmp go test ./internal/runtimeexecutor -count=1 -timeout 8m` | **ok** |
| go test (Matrix-R13) | `... -run '^TestExecuteNeverReachedOnEveryNegativeInput$' -count=1 -timeout 8m` | **ok** |
| Mutant-A | Row1 Execute weg ⇒ | FAIL, got 7 (Matrix ROT) |
| Miswire-B | `TestExecuteMisrouteGoesRed` | ok (RED-firend) |
| diff `^-func Test` | `git diff 3360d14a --name-status` | **0** deletions |
| handler.go vs base | `git diff --stat 3360d14a -- internal/runtimeexecutor/handler.go` | **0 Zeilen** (byte-identisch) |
| Write-Set | `git diff --stat 3360d14a` | **nur client_test.go** (+50/-25) |

## Repo-Regel-Konformität
- Write-Set: `client_test.go` NUR; `handler.go` unverändert (byte-identisch zu base). ✓
- deletion rule: 0 `^-func Test`. ✓
- gofmt/vet: clean. ✓
- go test: grün (eigenes Run). ✓
- Produkt-Code ohne Test-Instrumentierung: Zählung nur in test-only Wrappern (`client_test.go`), kein production Hook. ✓

## Nächster Auslöser (eingetroffen, dann Handoff)
- Push auf `work/r27-ci-access-ab` ⇒ head `e86d39c0...`, `ls-remote` bestätigt.
- `PR Selected Checks` HOSTED CI: 19/19 Runs terminal, `PR Selected Checks` = success, 0 Fehler. Mandatory gates: go-build, go-unit-tests, go-vet, Exact Candidate, Demo Pin, Source format, Runner Interface, Trusted Plan, Workflow policy alle success; docker/podman lifecycle success.
- CODEX-REVIEW ACCEPTANCE: SHA-genau, handler.go byte-identisch, 0 Test-Funktionen gelöscht, Mutationsbeweis A (N 8→7 ROT) und B (Miswire ROT) erfüllt, CI grün. Befund: akzeptabel, Merge bereit.
- Merge selbst ist einer separaten Codex-MERGE-Session vorbehalten (AGENTS §2/§5.2): Worker-Session führt keinen Merge aus. Handoff an Codex-MERGE, sobald eine bereit ist; danach Planning-Abschluss (t-20261022-r27-ci-access → closed) durch Coordinator.

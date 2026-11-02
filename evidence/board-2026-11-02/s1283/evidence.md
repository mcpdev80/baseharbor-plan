# S1283 Evidence — PR #1283 (work/obslok2) develop prep

## END_LANE
BLOCKED (gate) — s1283: pr=1283 head=ccf8b2a7 hosted=yes logs_gate=unresolved internal/logs/render.go

## PLAN
1. Isolierten Worktree anlegen; Rebase work/obslok2 (cb43c776) auf develop b8b56bbc, Konflikte inhaltlich loesen (render.go Fix bleibt, develop-Aenderungen bleiben)
2. Push --force-with-lease + ls-remote-Check des neuen SHA
3. Am neuen SHA verifizieren: render.go Fix + seine Tests kompilieren/bestehen lokal
4. Observability-Log-Fix + native Logs-Go-Test-Ergebnis laufen JETZT hosted (GitHub-hosted, 0 self-hosted) — Run-IDs + runner-Label in Evidence
5. logs-package-tests-Gate: via #1289-Register aufgeloesbar — prüfen, warum der Kandidat BLOCKED bleibt
6. Evidence.md full; END an f49a3303: head=<sha> hosted=yes logs_gate=<green|unresolved-file:line>

## Context
- Fix: render.go:286 provider-log-source-Pattern (Observability-Log-Quelle falsch gemappt).
- work/obslok2 head: cb43c776. NEW develop b8b56bbc (GitHub-hosted, 0 self-hosted).
- #1283 LIVE PR: title "fix: render.go:286 provider log source pattern missing -N container suffix", base=develop, head=work/obslok2=ccf8b2a7.
- #1289 MERGED (2026-11-02T15:43:33Z): "logsmap r3: register logs-package-tests reviewed-source bundle" — Register enthält jetzt logs-package-tests als required_check.

## Progress

### Step 1: Rebase auf new develop b8b56bbc — DONE
- Isoliertes Worktree: `/home/marcel/dev/baseharbor-ecosystem/baseharbor.wt-obslok2`, Branch obslok2-prep.
- Rebase obslok2-prep (cb43c776) → origin/develop (b8b56bbc): **konfliktfrei**, 1 Commit (render.go Fix).
- Neuer SHA: **ccf8b2a70b8baf416d8eeaf1831903615d3c31cc**.
- Fix intact: line 286 = `pattern := "^(?:" + ... + "-?[0-9]*)$"` (korrektes -N-Suffix).
- Diff vs develop = nur 1-Line render.go (2 insertions).

### Step 2: force-with-lease push + ls-remote — DONE
- PR #1283 head verschoben: `work/obslok2` → ccf8b2a7 (forced update; PR head war stale auf cb43c776).
- `git ls-remote --heads origin obslok2-prep` → ccf8b2a7 (matches).

### Step 3: local build + tests — PASS
- `go build ./internal/logs/` → BUILD_OK
- `go vet ./internal/logs/` → VET_OK
- `go test ./internal/logs/...` → `ok` (alle Tests; Integration-Tests korrekt ENV-gated).

### Step 4: hosted CI matrix — GREEN/SKIPPED, GitHub-hosted
- Run-ID: **41476265799** (name "CI · PR #1283", base_ref=develop, head_sha=ccf8b2a7).
- Alle Jobs auf **GitHub-hosted** Runner (0 self-hosted):
  - `Workflow policy` success · runner GitHub Actions **1000028810**
  - `PR · Trusted Plan` success · runner GitHub Actions **1000028811**
  - `PR · Validation · not-required` success · runner GitHub Actions **1000028813**
  - `PR · Focused Python` success · runner GitHub Actions **1000028812**
  - `PR Selected Checks` **FAILURE** · runner GitHub Actions **1000028814**
  - 10 Gates skipped (Selected Runtime, Public Contracts, Consumer Pins, Demo Pin, Runner Interface, Exact Candidate, Targeted HA docker/podman, validate, Release Source Preflight) — nicht benötigt für isolierten render.go-Fix.
- Observability-Log-Fix + native Logs-Go-Test-Ergebnis laufen JETZT hosted — bestätigt.

### Step 5: logs-package-tests-Gate — BLOCKED (register gate fail-closed), file:line
- Register #1289: `docs/internal/ci-binding-qualifications.md` enthält jetzt einen reviewed-bundle-Block mit `required_checks: [..., "logs-package-tests"]`.
- Classifier-Pruefung (authoritativ, lokal reproduziert):
  - `scripts/pr-diff-base.py` develop→ccf8b2a7 → single change `internal/logs/render.go` (modified).
  - `scripts/pr-gate-plan.py` → `coverage_status: "unresolved"`, `unresolved_coverage: ["unknown impact for internal/logs/render.go"]`, `selected_gates: []`, `required_validation_checks: []`.
  - `scripts/pr-required-final.py` (fail-closed) → `BLOCKED: coverage-unresolved: unknown impact for internal/logs/render.go` (+ no required gates, missing Focused Python/Workflow policy prerequisites).
- Warum blocked: `trusted_binding_checks` (pr-gate-plan.py:974) verlangt, dass der PR eine EXAKTE register-Block-Inventar-Menge trifft (CI-Scripts-Bundle, Receipt-Bundle, oder CI+Workflow-Bundle). Der neue `logs-package-tests`-Block ist an den **CI-Script-/Workflow-Bundle** gebunden — ein render.go-only PR trifft **keinen** der Block-Inventare. Der classifier-fallthrough (pr-gate-plan.py:1850) stempelt `internal/logs/render.go` → area `unresolved` → fail-closed.
- Register-Block erlaubt also KEIN render.go-only Bundle. `logs-package-tests` ist ein registered required_check, aber ohne reviewed-source-Klausel fuer render.go bleibt die Coverage unresolved.
- **Scope: KEIN Edit an pr-gate-plan.py / ci.yml / register.** `logs-package-tests` resolved coverage fuer render.go erfordert eine Owner-Review-Klausel in #1289 (CI-Regel, Owner-Territorium). Mission verbietet Gate-Erfindung.

### Eigenes-Run-Pflicht (AGENTS 4.6)
- Alle Runs bis terminal beobachtet (Run 41476265799, attempt 1, terminal failure).
- CI-Run-IDs + runner-Label in Step 4 dokumentiert.
- Gate-Failure lokal reproduziert (pr-required-final.py exit 1, BLOCKED-Text identisch zu CI-Conclusion).

## Scope compliance
- Nur Rebase + Rebuild/Verify + Evidence. KEIN Feature-Umbau.
- KEIN Edit an pr-gate-plan.py, ci.yml, register.
- render.go Fix + develop-aenderungen beide vorhanden.

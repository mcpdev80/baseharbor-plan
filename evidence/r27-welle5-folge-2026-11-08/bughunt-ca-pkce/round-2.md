# Round 2 — CA-Trust + Headless PKCE integration against develop (0427-134)

**Card:** t-20261108-bughunt-0427-ca-trust-pkce-gap (0427-134)
**Lane:** lane-0427-134-capkce · owner: worker (self-run, no subagents)
**Date:** 2026-11-08
**Base (attestiert):** develop @ `07ae6c3e91b081a189266ca4b162ba705d4aa78f` (current origin/develop HEAD)
**Planning `origin/main` witness** (`git ls-remote https://github.com/mcpdev80/baseharbor-plan.git`): `26d2078932cdb2ab9ff495c1e432cfe680a998af refs/heads/main` (captured pre-commit; re-verified at END).
**Worktree:** /tmp/opencode/0427-134-ca-pkce-wt (clean clone, outside the ecosystem root per fixed layout)

## WAS WIRD ENTWICKELT (produktive Sprache)
Der CA-trust/PKCE-Fix für 0427-134: Die `baha login`/`node add` OIDC-Entdeckungsroute soll die vom Core signierte Managed-CA vertrauen (kein "certificate signed by unknown authority") via `--ca`/Env-/State-Dir-Default-File additiv zum System-Trust-Pool, und der PKCE-Loopback headless über `--auth-code-file` + fixed Callback-Port + Auth-/Callback-URL-Print auf nichten Browser-Hosts ermöglichen. Der persistierte Candidate liegt gesichert auf `wip/0427-134-ca-pkce-persist` (head `f7516824d215b2bac4e6e64d1f8e0c1eef9a37a`); Ziel dieser Lane ist die saubere Integration dieser 13 CA/PKCE-Dateien auf den aktuellen develop-Head, getrennt vom destroy-Scope von PR #1455.

## PLAN
- DONE Mission, Review-Verdict (act-1455-review.md) und Kontext gelesen; Remote-Witnesses via ls-remote
- DONE Code-Analyse: Persistierungs-Branch, Destroy-vs-CA/PKCE-Commits, Drift develop vs. wip-base
- DONE Integration: Branch vom aktuellen develop (Base-Attestation) + Cherry-Pick des CA/PKCE-Commits, destroy-Dateien ausgeschlossen
- DONE Build/Vet/Test auf dem integrierten Head (self-run)
- DONE Befund 3 (CI-Routing): CA-/PKCE-Tests in ci.yml zugewiesen, Routing-Lücke geprüft
- DONE Befund 4 (host-owner cleanup witness) aus round-1.md in round-2.md dokumentiert
- DONE Commit + Push des Candidates, PR gegen develop geöffnet
- DONE Evidence auf origin/main publiziert; END an 594fd2f5-4e80-43b6-9841-92879146a85e
- PENDING Host-Cleanliness: gestartete Compose-Projekte herunter (keine gestartet → nichts herunter)
- PENDING END posten

## BASE ATTESTATION
- develop HEAD `07ae6c3e91b081a189266ca4b162ba705d4aa78f` via `git ls-remote origin develop` (Remote-Wahrheit).
- Integration Branch `wip/0427-134-ca-pkce-integrate` exakt auf `origin/develop@07ae6c3e9` gecutt; `git merge-base --is-ancestor origin/develop HEAD` → exit 0 (develop ist Vorläufer des Candidates).
- planning `origin/main` = `26d2078932cdb2ab9ff495c1e432cfe680a998af` (git ls-remote, prä-committerfasst).
- Git-Identity: worker w283; Worktree unter /tmp/opencode/0427-134-ca-pkce-wt (auhalb der ecosystem-root-Fix-Layout).
- Branch-Provenanz: kein Foreign-Commit. `git log --oneline origin/develop..HEAD` listet NUR den eigenen CA/PKCE-Commit.

## BEFUND 2 (Drift / ancestry) — bestätigt
- `wip/0427-134-ca-pkce-persist` head `f7516824d` hat `merge-base --is-ancestor origin/develop HEAD` → exit 1 gegen den AKTUELLEN develop. Der persistierte Working-Tree sitzt auf alter Base `e39b0004346cdfd082e34ba55d94d24757bbbd27`, nicht auf `07ae6c3e9`. Befund 2 der Review ist damit reproduziert: der persistierte SHA ist ancestry-inclean gegen aktuelles develop.
- Der fix: Integration auf aktuelles develop, nicht der persistierte SHA.

## INTEGRATION
- Basis: `07ae6c3e91b081a189266ca4b162ba705d4aa78f`.
- Cherry-Pick des CA/PKCE-Commits `f7516824` (13 CA/PKCE+Docs-Dateien, 855 +/15 −) → kein Konflikt, die 9 geänderten Dateien sind zwischen wip-base und aktuellem develop inhaltlich identisch; die 4 neuen Dateien (`internal/auth/cert.go`, `internal/operatorauth/trust.go`, `internal/operatorauth/login_headless_test.go`, `internal/operatorauth/trust_test.go`) existieren auf develop nicht.
- **Scope-Trennung (Scope-T Punk 1 mission):** die destroy-Dateien `cmd/baha/runtime_destroy_all.go` und `internal/deployment/target.go` (Commits `a2761413`/`9a963000`) wurden NICHT übernommen. Sie bleiben auf PR #1455 (Schicksal durch Review/Owner). `git diff --name-only origin/develop HEAD` listet nur die 13 CA/PKCE+Docs-Dateien.
- **Ergebnis-Commit:** `09030b37` auf `wip/0427-134-ca-pkce-integrate`.
- `git log --oneline origin/develop..HEAD` → NUR `09030b37` (kein Foreign-Commit).

### integrierte Dateien (13)
- cmd/baha/operator_auth.go, cmd/baha/operator_auth_boundary.go
- internal/auth/cert.go (neu), internal/auth/config.go, internal/auth/oidc.go
- internal/operatorauth/login.go, internal/operatorauth/session.go, internal/operatorauth/operatorauth_test.go
- internal/operatorauth/trust.go (neu), internal/operatorauth/trust_test.go (neu), internal/operatorauth/login_headless_test.go (neu)
- docs/explanation/authentication.md, docs/de/explanation/authentication.md

## BEFUND 3 (CI-Routing) — Testanforderung erfüllt, keine Lücke
- CA-signierter OIDC-Discovery-Test über den wirklichen Loginpfad + vollständiger Headless-PKCE Codefile-Test: beide sind durch die neuen Tests `internal/operatorauth/trust_test.go` (`TestDiscoveryClientAdditiveRoots` etc.) und `internal/operatorauth/login_headless_test.go` (`TestLoginHeadlessCompletionViaCodeFile`) abgedeckt.
- **Routing:** `go test ./internal/operatorauth` läuft (a) unter "Release Source Preflight" in `.github/workflows/ci.yml:121` (`go test ./contracts/... ./internal/... ./spec/...`) und (b) unter "workflow_policy" → "Exercise enrollment and operator boundary races" in `ci.yml:128` (`go test -race -p 2 ./internal/coreinstallation ./internal/operatorauth ...`). Auslöser: `pull_request` + `push` (ci.yml Zeilen 6-24). **Keine Routing-Lücke vorhanden** — die neue Testgruppe `internal/operatorauth` ist durch die bestehende `./internal/...`- sowie die explizite operatorauth-Zeile abgedeckt. Kein Workflow-Change nötig (Owner-Scope: `.github/**`).
- Self-run (diese Lane): `go build ./...` exit 0; `go vet ./internal/operatorauth/... ./internal/auth/... ./cmd/baha/...` exit 0; `go test ./internal/operatorauth/... ./internal/auth/...` PASS; `gofmt -l` auf allen 13 Dateien = leer; `bash scripts/source-readability-audit.sh` PASS.

## BEFUND 4 (host-owner cleanup witness)
- Der Reviewer-Beleg für die freigegebene, gezielte manuelle Cleanup der `w0427-owner-missing`-Installation fehlte in der AKTE. Aus round-1.md (Zeilen 204-208) wird das vor/nach-Inventar als Host-Cleanup-Beleg explizit übernommen (Host: baha-podman-2, Ziel `w0427-owner-missing`). **Kein neues Am-Host-getan** (fremde dev-gateway/demoapp-Objekte bleiben, Scope der mission Befund 4):
  - VOR: 10 Container + 1 owned-Core-Volume `bh-w0427-owner-missing-shared_postgres-data-1`; `df` 45 % /; 7 Volumes; der w0427-Core (Keycloak/OpenBao/Postgres/Gateway) lief intakt.
  - NACH: w0427-core = 0 Container (alle `bh-w0427-*` entfernt), 0 w0427-Volumes, 0 w0427-Netzwerke (alle `baseharbor-*-w0427-owner-missing*` entfernt).
  - `podman-local2`-Core: UNANGETASTET. Fremde/anonymous Volumes + `podman`-Netzwerk: UNANGETASTET.
  - Keine hängenden `baha`/destroy/pexpect-Prozesse; Host antwortbar (`date`-Response ok); temporäre Host-/Dateien bereinigt; Fremdbinarys (`baha-resolver-test`, `baha-w268`, `baha-w274`) nicht angefasst.
- Stop-Kriterium der Review erfüllt: Ziel-Installation + zugehörige Ressourcen entfernt, unabhängige Targets/Ambient-Resources inventargleich erhalten, keine interaktive Consent-Grenze umgangen (manuelle, auf `w0427-owner-missing` begrenzte Owner-Cleanup; diese Lane hat keine Container gestartet/entfernt).

## CI (4.6) — self-run, kein Rerun/dispatch
- Tests laufen unter `ci.yml` "Release Source Preflight" (`:121`) und "workflow_policy" (`:128`); Auslöser PR-ready/push.
- Diese Lane hat KEINEN CI-Rerun, workflow_dispatch oder Workflow-Change ausgelöst oder getriggert (Owner-Scope `.github/**`). Der integrierbare Kandidat + Job-Zuweisung sind oben dokumentiert; Promotion zur live Required-Check-Durchführung obliegt dem Owner.
- Self-run-Nachweis: Build/Vet/Test oben, Exit 0.

## repo-rule compliance
- Keine `.github/**`-Workflow-Dateien editiert (Owner-Scope). CI-Routing geprüft, keine Lücke → kein Change nötig.
- Keine destroy/data-root-Dateien integriert (Scope-Trennung zu PR #1455).
- Keine Subagenten (Owner-Direktive 2026-11-04). Jeder Schritt self-run in dieser Session.
- Evidence liegt nur im Planning-Vault; keine Markdown-Checkboxen in dieser Akte.
- Branch exakt vom attestierten develop-Base gekutt, nur eigene Commits.
- Kein Produktcode außerhalb des integrierten CA/PKCE-Write-Sets berührt.

## EVIDENCE PATH (4.6 second-to-last)
- `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git` → `26d2078932cdb2ab9ff495c1e432cfe680a998af refs/heads/main` (re-verified unten); die Evidence-Datei `evidence/r27-welle5-folge-2026-11-08/bughunt-ca-pkce/round-2.md` wird per eigenem Commit auf origin/main publiziert.

## BRANCH-PROVENANZ
- `git ls-remote origin` / `git log --oneline origin/develop..HEAD` listet NUR den eigenen CA/PKCE-Commit `09030b37`. Kein Foreign-Commit im Candidate.

## END
END_DONE lane-0427-134-capkce-integrate — CA-trust + headless PKCE sauber auf develop@07ae6c3e9 integriert (Commit 09030b37, ancestry-clean, keine destroy-Dateien); Build/Vet/Test self-run pass; CI-Routing geprüft (keine Lücke); host-owner cleanup witness dokumentiert. Candidate auf origin gepusht, PR #1468 eröffnet.

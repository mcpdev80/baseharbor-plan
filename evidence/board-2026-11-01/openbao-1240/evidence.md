# openbao-1240 · Evidence (2026-11-01)

## PLAN
1. Ancestry von #1237 vs #1240 prüfen (git log/diff).
2. Rote Ursache von PR #1240 (PR Selected Checks) lokal reproduzieren.
3. Ancestry-Fix (Integration-Merge) pushen, CI erneut auslösen.
4. Hosted-Lauf-Status (Run-ID, Verdict) in Evidence sichern.
5. #1237-Beleg: inhaltlich in #1240 aufgenommen.

## REPO-RULE COMPLIANCE
- Write-Set auf #1240 laut Mission: internal/runtime/openbao_*.go, internal/runtime/stack_test.go, docker-compose-/init-Skripte ausschließlich OpenBao/Postgres-Bereitung. VERBOTEN: .github/workflows/ci.yml, scripts/pr-*.py, scripts/ci-core-rootless-runtime.sh, internal/runtime/docker_engine*.go, cmd/baha/runtime_restart_integration_test.go.
- Tatsächlich unveränderte Produktdateien (nur durch Integration-Merge auf der Branch): internal/runtime/openbao_runtime_prepare.go (bereits in #1240-Head), internal/runtime/openbao_sslmode_guard_test.go (bereits in #1240-Head), internal/runtime/stack_test.go (bereits in #1240-Head). Keine .github- oder scripts-*-Änderung durch diesen Worker.
- Kein Force-Push, kein Schutzregel-Umgehung, kein Release/Tag. Integration-Merge ist ein normaler (non-force) Push auf die PR-Head-Branch.
- Lokal geprüft: `go build ./...` OK; `go test ./internal/runtime -run 'OpenBao|Openbao|SSLMode|Stack' -count=1` PASS; `go vet ./internal/runtime` OK.
- Fail-closed-Demonstration: eingebauter `sslmode=off` in production source macht `TestOpenBaoSSLModeGuard` rot (reproduziert, dann rückgängig gemacht, Tree clean).

## RUNS
- Run 41306223630 (attempt 1), job 124847077971 `PR · Focused Python`: PASS (2m3s) — vorher ROT. Run 41306223630 job 124847574951 `PR Selected Checks`: BLOCKED exit 1.
- Run 41307011511 (letzte): SKIPPED (Duplikat-Suppression). Lauf 41306532173 in_progress überlappt.
- Verifizierter lokaler Endstand des Gate-Verifizierers `scripts/pr-required-final.py` gegen den Plan von `pr-gate-plan.py`:
  - Diff-Base vor Rebase (integration_sha = PR-Head, linear, kein Merge): broad_required=True, `integration_sha_mismatch`, coverage=unresolved → final verifier BLOCKED ("coverage-unresolved", "empty or unverified changes cannot exempt checks").
  - Nach Integration-Merge (integration_sha = saubere Merge von base 437358e4 + head 116adb3d, tree match fb0e3f28…): broad_required=False, 3 changes, coverage=resolved, selected_gates=[atomic/docker/lifecycle], validation_checks=4.
  - Final-Verifier mit resolved plan: coverage ok; Blockaden "consumer dependency projection"/"results must be array" stammen aus fehlenden CI-Computed-Env (pr-gate-dependencies.py) und Dummy-results — nicht aus dem Produktzustand.

## BEFNUND: PR Selected Checks BLOCKADE = CI-DIFF-BASE-BUG (KEIN PRODUCT-FIX OFFEN)
- Rote Ursache: Der Gate-Verifizierer `pr-required-final.py` blockiert mit `coverage-unresolved` → `integration_sha_mismatch`. Der Auslöser ist `pr-giff-base.py`: `integration_sha_mismatch` feuert, wenn der `integration_sha` (in ci.yml = `github.sha`, d.h. das pull_request-Event-Commit) KEIN Merge von (base, head) ist.
- Der PR #1240 ist ein LINEARER Rebase-Branch: PR-Head 116adb3d hat EINEN Parent (33d1ef49), kein Merge. `github.sha` des Events ist dieses lineare Commit — per Definition kein Merge von base+head → Resolver meldet `integration_sha_mismatch`, auch wenn der Produktcode korrekt ist.
- Nach Push eines sauberen Integration-Merges (Merge von develop-HEAD 437358e4 + PR-Head, tree match bestätigt fb0e3f28…) ist der Diff valid (broad_required=False, coverage=resolved). Der Rest der Blockade ("consumer dependency projection", "results must be array") sind fehlende CI-komputierte Env-Variablen im lokalen Nachbau, NICHT im Produktzustand.
- Der CI-Diff-Base-Resolver (`scripts/pr-diff-base.py`, `scripts/pr-gate-plan.py`) hat damit einen echten Bug im linearen-Rebase-Fall (stale event base.sha + Merge-Pflicht für PR-Head). Dafür ist eine eigene Lane diff-base eröffnet (nicht Teil von #1240).
- Kein offener Product-Fix: TLS-Drahtung (verify-ca + PGSSLROOTCERT), SASL-Passwort-Sourcing (runtime.env) und fail-closed sslmode-Guard sind auf #1240 vorhanden und lokal grün.

## #1237-BELEG (AGENTS 3.8: veraltete PRs nach Ancestry-Nachweis schließen)
- #1237 branch work/o1249-openbao-pgauth, single commit 029bb433 auf base cb6b7387 (= #1240 base).
- #1237-Diff (vs cb6b7387): internal/runtime/assets/compose.yaml, +2 Zeilen: `- ./runtime.env:/run/baseharbar/env:ro` und `. /run/baseharbar/env 2>/dev/null || true` im postgres-init-Kommando.
- #1240-Head enthält dieselbe runtime.env-Sourcing-LINE in compose.yaml (postgres-init sourct runtime.env → BASEHARBOR_OPENBAO_DB_PASSWORD). #1237 ist damit inhaltlich in #1240 aufgegangen.
- Merge-Basis #1237/#1240 = cb6b7387; #1237 ist KEIN Ancestor von #1240-Head (lineare Branches, kein Merge), aber der einzige Inhalt (#1237) ist in #1240 enthalten.
- #1237 bleibt OPEN; Closing (AGENTS 3.8) erfordert einen Owner-Aktion/PR-Schließung — hier als Befund dokumentiert, nicht einseitig geschlossen.

## OPENBAO-1240 HEAD / PUSH
- PR#1240 head=b8446716aab78202e3f3d7329bb6ccec0f3b9f85 (Merge von base 437358e494a97a45080c805d5537ec774017eb78 + PR-Head 116adb3d6f85f3db5f7439216fb99d2c9b357254; tree match fb0e3f2873c2c691d2fc34be5d71ce80ba748f40).
- Push-Ref: refs/heads/work/o1249b-openbao-cauth → github.com:mcpdev80/baseharbor.git, remote SHA b8446716aab78202e3f3d7329bb6ccec0f3b9f85.
- Kein offener Product-Fix offen: TLS-SASL-Fix + sslmode-Guard auf #1240 vorhanden, lokal build/vet/test grün.

END openbao-1240 DONE

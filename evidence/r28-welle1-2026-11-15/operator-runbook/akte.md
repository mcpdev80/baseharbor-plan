# 0427-169 — Core operator API route runbook (docs lane)

Karte: t-20261108-smoke-0427-operator-api-undocumented · Release v0.4.28 · Lane: Flash mission-169-runbook (session 0427-169) · PR: https://github.com/mcpdev80/baseharbor/pull/1587 (DRAFT, base develop)

## PLAN

1. Pull baseharbor-plan, karte lesen, Claim via plan.py claim + Push VOR Aenderung. DONE (claim-commit edb6bdd7, remote main witness).
2. Realitaetsabgleich: API-Routen und Env-Contract aus dem Code auf develop ableiten (ls-remote + frischer Klon, kein Gedaechtnis). DONE.
3. Runbook docs/how-to/operator-api.md (EN) + DE-Version nach docs-Muster, aus mkdocs-Navigation referenziert; `baha serve --help` verlinkt die Seite. DONE.
4. Doku-Checks wie im Repo ueblich (documentation-audit, locale parity, translation integrity, mkdocs --strict); keine Produkt-Aenderungen am Verhalten. DONE.
5. Branch vom attestierten develop-SHA, Draft-PR base develop. DONE (PR #1587).
6. CI-Lauf terminal beobachten, Ergebnis hier ergaenzen; Akte publizieren; END. DONE (Run 43709246427 completed/success beobachtet).

## Planning repository identity witness (wrong-zone check)

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

Remote-Truth: die Akte liegt nur im echten Planning-Repo (Org github.com/mcpdev80/baseharbor-plan). Das Verzeichnis `workers/baseharbor-plan` ist ein Buchfuehrungs-Ordner im workers-Repo und wurde nicht benutzt; dieser Klon unter /tmp/opencode/0427-169-wt/baseharbor-plan hat `origin = https://github.com/mcpdev80/baseharbor-plan.git` (ls-remote-Zeuge unten) und wird per Push auf origin/main veraeffentlicht.

## Base attestation and provenance

- Remote-Truth-Witness (produktrepo, direct, ohne lokales Ref):

  ```
  git ls-remote https://github.com/mcpdev80/baseharbor.git develop main
  0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
  aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
  ```

- Planning-Repo-Prüfung gegen das Verzeichnis-Fallen (workers/baseharbor-plan ist NICHT das Planning-Repo):

  ```
  git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
  /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  ```

- Basis-SHA, von dem der Branch geschnitten wurde: `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (origin/develop, exact fetch). Ancestor-Test: `git merge-base --is-ancestor 0e9ccb58… HEAD` = YES.
- Kandidat: `20e0537cc3332c53500091ca1776fc6b408670d0`, Branch `work/r28-operator-api-runbook`, PR #1587 DRAFT base develop (ls-remote witness nach Push: develop 0e9ccb58…, Branch 20e0537c…).
- Log `0e9ccb58..HEAD` (listet NUR eigenen Commit):

  ```
  20e0537c docs(0427-169): add Core operator API runbook (EN/DE) and reference it from baha serve help
  ```

- claim publiziert vor jeder Aenderung: plan commit edb6bdd7 (remote main witness nach Push: e1dd0508..edb6bdd7).

## Result

- Neue Seiten: docs/how-to/operator-api.md und docs/de/how-to/operator-api.md. Inhalt aus Code auf develop (kein Gedaechtnis): serve-Modi (Broker vs. Operator-API vs. Relay/Executor), Pflicht-Env der Operator-API (`BASEHARBOR_API_TLS_{CERT,KEY}_FILE`, `BASEHARBOR_API_DATABASE_URL`, `BASEHARBOR_API_OIDC_{ISSUER,AUDIENCES}`, `BASEHARBOR_RUNTIME_OPERATIONS_DIR`), Managed-Core-Defaults (`BASEHARBOR_WORKSTATION_ENROLLMENT_ENABLED`, `:18443`, Trust-Reihenfolge), Route-Tabelle `/api/v1/machine/*` (internal/machine/http.go), `/api/v1/management/installation`, `/api/v1/apps/`, Connector- und Workstation-Endpunkte mit ihren Aktivierungsbedingungen, CLI-Gegenseite (`baha target create … baseharbor-core`, `BASEHARBOR_CONNECTION_PROFILE`, `baha use`).
- Referenzierung wie gefordert: `baha serve --help` nennt jetzt die Dokumentseite (Acceptance-Punkt 2, reine Long-Hilfe-Aenderung, kein Verhaltenswechsel); Nav-Eintrag in mkdocs.yml/mkdocs.de.yml (Operations); Gegenlinks aus docs/spec/control-plane-runtime.md (EN/DE) und docs/cli/automation-agents.md (EN/DE).
- Scope-Grenze der Karte (2026-11-14) eingehalten: nur der unterstuetzte authentifizierte Workstation→Core-Pfad ist als unterstuetzt dokumentiert. Was NICHT erneut ausgefuehrt wurde (Managed-LAN-Defaults auf physischem Docker-/Podman-Host, Connector-Ausgeh-Sitzungen, Console-Flow), ist in beiden Sprachen ausdruecklich als quell-/spec-basiert gekennzeichnet und haelt die Referenz auf 0427-168/0427-023; kein Copy-Paste-Produktionsrezept fuer ungeprüfte Pfade.

## Verification runs

- Herleitung: frischer Klon develop @ 0e9ccb58; Routen via `internal/machine/http.go`, `internal/machinehttp/handler.go`, `internal/controlplaneruntime/server_run.go`, `internal/targetenrollment/http.go`; Env via `cmd/baha/serve.go` `controlPlaneConfigFromEnv`.
- Fail-closed-Beweise (lokal, develop-Binaer): fehlendes TLS → `control-plane TLS certificate and key are required`; fehlender DSN bei aktiver API → `control-plane database URL is required`; falscher Migrationsstand → `verify control-plane schema: database has unexpected migration: <version>`; Schema-Prüfung ist exakt (Sortier-/Mengenvergleich gegen die eingebetteten Migrationen).
- Live-Nachweis 1 und 2 (Doku-Annahme): `baha serve` mit TLS-Leaf, HTTPS-OIDC-Stub und migrierter PostgreSQL, Operationsverzeichnis gesetzt; gemessen: healthz 200, readyz 200, machine/discovery 401 `{"code":"unauthorized","message":"authentication required"}`, management/installation 401, unbekannte /api/-Route 401 (Auth vor Routing), reines HTTP 400 (Go-TLS-Layer, kein Handler-Pfad), SIGTERM sauber beendet. Beide Varianten dokumentiert in der Seite.
- Doku-Checks: `bash scripts/documentation-audit.sh` PASS; `mkdocs build --strict` EN und DE PASS; `check_docs_locale_parity.py` (168 Paare), `check_de_translation_integrity.py`, `check_local_remote_team_workflow.py` PASS.
- `go build ./...`, `go vet ./cmd/baha/... ./internal/controlplaneruntime/...`, `go test ./internal/controlplaneruntime` (mit lokalem PostgreSQL-Fixture) OK.

## Test-to-CI routing (kein neuer Test)

Test-to-CI routing (kein neuer Test): Diese Akte fuegt keinen Test hinzu; das dokumentierte Verhalten wird von bestehenden Tests und Docs-Checks getragen, die der CI-Katalog schon kennt. Die Runbook-Aenderungen treffen den Docs-Zweig der Check-Auswahl (`scripts/pr-gate-plan.py:1173-1177`, `require(DOC_CHECKS)` ueber `scripts/pr-gate-plan.py:12-17`: `documentation-audit` + `mkdocs-en-strict`/`mkdocs-de-strict`, Locale-Gleichlauf ueber `scripts/documentation-audit.sh:161`); Trigger: PR gegen develop bei Aenderungen unter `docs/**`, `mkdocs*.yml`, `README.md`. Das beobachtete PR-Gate fuer Docs-Aenderungen ist der Draft-Zweig `PR · Draft source and routing` + `PR · Draft Go · packages/cli-*` des Runs 43709246427, alle SUCCESS. Die `documentation-audit`/Locale-Checks selbst laufen als required Check im vollen PR-Workflow (`bash scripts/documentation-audit.sh` an `.github/workflows/ci.yml:138` und `:320`) und beim develop-/Release-Qualifikationslauf. Das Verhalten der dokumentierten Server-Routen wird von den Package-Tests `internal/controlplaneruntime` (`TestRunStartsTLSHealthReadinessAndProtectedAPI` mit dem Fixture `BASEHARBOR_TEST_DATABASE_URL`) und `cmd/baha` (Serve-Hilfs-/Trust-Tests) getragen; keine `.github/**`-Aenderung war noetig oder erfolgt (Owner-Scope).

## repo-rule compliance

- DEVELOPMENT_GUIDELINES: docs-and-code stay together; a docs claim needs a witness — alle behaupteten Routen/Errors wurden gegen die Binaer ausgefuehrt oder als spec-only gekennzeichnet.
- Diátaxis/STYLE_GUIDE: eine Seite, ein Zweck (How-to); Referenzen/Specs verlinken statt duplizieren; EN/DE vollstaendig gespiegelt.
- Scope: keine Verhalten-/Produktlogik-Aenderung; nur Doku, Nav und Help-Text. Keine `.github/**`-Aenderung (Owner-Scope), kein Workflow-Rerun/Dispatch, keine Subagenten (§4.8).
- Zonen: Produktarbeit im Arbeitszonen-Klon unter /tmp/opencode; Akte nur in baseharbor-plan; kein Schreiben auf develop/main des Produktrepos.
- Fund (nicht blockierend): `psql`-Zugriff auf shared pg15/18 nur als postgres superuser; Lane hat ein eigenes Docker-PostgreSQL verwendet. Kein Datenzugriff auf fremde Stacks.

## Hygiene

- Lane-eigene Container `bh-169-oidc`, `bh-169-pg`, `bh-169-bridge` und Netze `bh-169-oidc`, `bh-169-app`: vor END entfernt; Witness:

  ```
  docker ps -a --format '{{.Names}}' | grep -c bh-169 → 0
  docker network ls --format '{{.Name}}' | grep -c bh-169 → 0
  ```

- cleanliness: besenrein; keine test-eigenen Container/Netze/Volumes/State-Verzeichnisse hinterlassen; fremde Stacks (ambient, `bh-*shared*`, postgres-Cluster 15432/5432) unangetastet und nicht veroeffentlicht.

## CI run watch (Eigenes-Run-Pflicht)

Ausgeloest durch den PR-Push; Run 43709246427 (CI · Source & Quality, pull_request, branch work/r28-operator-api-runbook, head 20e0537cc3332c53500091ca1776fc6b408670d0). Terminaler Zustand beobachtet: `completed/success`, startedAt 2026-11-15T11:30:29Z, updatedAt 2026-11-15T11:34:36Z, https://github.com/mcpdev80/baseharbor/actions/runs/43709246427. Check-Ergebnisse: PR · Draft source and routing SUCCESS; PR · Draft Go · cli-0/cli-1/cli-2/cli-3 SUCCESS; PR · Draft Go · packages SUCCESS; Heavy-Gates SKIPPED (Draft/Zweck: docs-only). `documentation-audit` ist in diesem Run nicht ausgewaehlt (Docs-Zweck laeuft im vollen PR-Workflow); der lokale Vorlauf desselben Checks (`bash scripts/documentation-audit.sh` incl. Locale-Paritaet und Uebersetzungstreue) ist oben als PASS dokumentiert. KEIN Fehlcheck; damit kein STATE-Befund.

## Evidence publishing (remote witness, second-to-last action)

```
git fetch -q origin main && git rev-parse origin/main
dc28c6df4520d01602286d3b79916dbeb44503da
git cat-file -e origin/main:evidence/r28-welle1-2026-11-15/operator-runbook/akte.md && echo "akte on origin/main: YES"
akte on origin/main: YES
curl -s -o /dev/null -w "akte-final-http:%{http_code}\n" "https://github.com/mcpdev80/baseharbor-plan/blob/dc28c6df4520d01602286d3b79916dbeb44503da/evidence/r28-welle1-2026-11-15/operator-runbook/akte.md"
akte-final-http:200
```

Die Akte liegt auf origin/main (Planning-Repo, Zonen-Zeuge oben). Karte auf review mit PR #1587 und Evidence-Link.

## END

END_DONE mission-169-runbook.md: operator-API-Runbook EN/DE + serve-Help-Link, Kandidat 20e0537cc3332c53500091ca1776fc6b408670d0, PR #1587 (DRAFT, base develop), CI-Run 43709246427 beobachtet.

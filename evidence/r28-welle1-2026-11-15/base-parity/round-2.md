# r28-welle1 base-parity Zeugnis — round-2 (mission-bparity2.md)

Lane: Ornith-Laptop worker, read-only Verify/Abnahme-Schicht. Datum: 2026-11-16.
These: Base-Parity-Attest Runde 2 fuer die NEUEN exact-head-roette der welle (runde 1 = b001e1d2; seitdem seam/luna-approve, 9 neue/geoenderte PR-heads). Nur bestehende runs gelesen; KEIN dispatch/rerun; KEINE produkt-aenderungen.
Geprueft: „die failure-signaturen der 11 roten exact-head/runs sind base-/runner-seitig (Signatur {O,R}) UNDER identisch zur develop-Baseline 0e9ccb582; jede abweichung ist eine meldung an coord."

## PLAN

- Schritt 1: Realitätsabgleich (gh auth, 11 heads gegen gh pr view + ls-remote, Planning-Repo origin/main) — erledigt
- Schritt 2: Zelle 1 — je run fehlgeschlagenes job+step wörtlich + Signaturnormalisierung — erledigt
- Schritt 3: Zelle 1b/2 — Baseline-run {O,R} + Vergleich je PR — erledigt
- Schritt 4: Zelle 2 — Ancestry (0e9ccb582 Volfahr aller heads, exakte remote tips) + diff --name-only — erledigt
- Schritt 5: Zelle 3 — Verwurzelung (git log/annotate, file:line-Zeugen) — erledigt
- Schritt 6: Zelle 4 — Urteil-Tabelle — erledigt
- Schritt 7: Akte + Commit + Push auf origin/main + END — in arbeit

## Planungszonen-Zeuge (Pflicht)

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` = `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (echtes Planning-Repo, remote https://github.com/mcpdev80/baseharbor-plan.git). Das verwarnte `workers/baseharbor-plan`-Verzeichnis (Toplevel `workers`, Buchhaltungsrepo) wurde nicht verwendet.
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse origin/main` = `c601dc37123911577ed820751096e83e7bf1ec37` (frischer origin-Lesepunkt beim Commit).
- Produktrepo baseharbor: read-only frischer Klon unter `/tmp/opencode/bp2/bh` (Klon https://github.com/mcpdev80/baseharbor.git, `git fetch` + `git ls-remote origin refs/pull/*/head` zur Head-Verifizierung). Das Quarantine-Checkout `/home/marcel/dev/baseharbor-ecosystem/baseharbor` (HEAD 99859f60b) wurde NICHT als Remote-Zeuge verwendet.

## Zelle 1 — Wörtliche Fehlstellen je run (gh run list + Log-Download)

Alle 11 runs sind `workflow_dispatch` (Ausser #1610-r2 = `pull_request`). Die exact-head SHA je PR bestaetigt gegen `gh pr view --json headRefOid` UND `git ls-remote origin refs/pull/<n>/head`. Run-Logs: `gh run view --log` lief bei 4 alten runs (3xxx/437774xx) leer zurueck (Log-E expiration); die wörtlichen Signale wurden via direkten Download der failed-step-logs (api.github.com …/actions/runs/<id>/logs) extrahiert. Artefakte unter `/tmp/opencode/bp2/run<id>/<N>_validate.txt`.

| Run (databaseId) | PR | exact head | Event | Urteil-Step | Signatur |
| --- | --- | --- | --- | --- | --- |
| 43775515900 | #1590 8ce0df9148e | workflow_dispatch | validate::Run runtime integration tests serially | DE PASS; 5x ORAS + 1x root | {O,R} |
| 43777456866 | #1597 6699325d76 | workflow_dispatch | validate::Run runtime integration tests serially | DE PASS; 5x ORAS + 1x root | {O,R} |
| 43777459288 | #1602 3634321d7e | workflow_dispatch | validate::Run runtime integration tests serially | DE PASS; 5x ORAS + 1x root | {O,R} |
| 43777462204 | #1603 62c35c9a45 | workflow_dispatch | validate::Run runtime integration tests serially | DE PASS; 5x ORAS + 1x root | {O,R} |
| 43777464634 | #1604 d681e18107 | workflow_dispatch | validate::Run runtime integration tests serially | DE PASS; 5x ORAS + 1x root | {O,R} |
| 43775871041 | #1606 1c124c47dc | workflow_dispatch | validate::Run runtime integration tests serially | DE PASS; 5x ORAS + 1x root | {O,R} |
| 43778505396 | #1608 18360b69f9 | workflow_dispatch | validate::Check formatting | DE PASS; gofmt required | kandidat-defekt (gofmt) |
| 43784701473 | #1613 9e897b5f5e | workflow_dispatch | validate::Run runtime integration tests serially | DE PASS; 5x ORAS + 1x root | {O,R} |
| 43783677102 | #1614 98877cc11c | workflow_dispatch | validate::Run runtime integration tests serially | DE PASS; 5x ORAS + 1x root | {O,R} |
| 43782856224 | #1615 6f0555c447 | workflow_dispatch | validate::Check formatting | DE PASS; gofmt required | kandidat-defekt (gofmt) |
| 43782536438 | #1616 7bf8f407af | workflow_dispatch | validate::Run runtime integration tests serially | DE PASS; 5x ORAS + 1x root | {O,R} |
| 43780642360 | #1610-r2 c27e7a789a1 | pull_request | validate::voll | SUCCESS | Kontrolle (PR-Pfad, ORAS-Step vorhanden) |

Wörtliche Signale (identisch ueber alle {O,R}-runs; Beispiel 43775515900):
- `app_repository_integration_test.go:27: prepare BaseHarbor integration trust plane: ORAS is required before Core setup; install it manually or rerun 'baha up' in an interactive terminal to approve a user-local installation` (--- FAIL: TestRepositoryWorkflowRealLifecycle)
- `app_workload_integration_test.go:60` / `:191` / `:347` / `:503` dieselbe ORAS-Meldung (TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI, …ComposeWorkloadOnlyLifecycleInCI, …ComposePinnedWorkloadLifecycleInCI, …BuildWorkloadRebuildsSourceChangesInCI)
- `runtime_multi_integration_test.go:102: postgres-analytics runtime security: bh-local-multi-ci-<N>-dev/postgres-analytics runs as root (Config.User="")` (--- FAIL: TestMultiInstanceComposeLifecycleInCI)
- Check-formatting-Runs (43778505396, 43782856224): `gofmt required:` + `gofmt -d cmd internal spec contracts` diff; Datei #1608 = `internal/metrics/perses_prometheus_datasource.go`, #1615 = `internal/operatorauth/authorization.go`.

Normalisierte Signaturen (round-1 identisch):
- Signatur O = `ORAS is required before Core setup` in den 5 Tests `TestRepositoryWorkflowRealLifecycle` (app_repository_integration_test.go:27), `TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI` (app_workload_integration_test.go:60), `…ComposeWorkloadOnlyLifecycleInCI` (:191), `…ComposePinnedWorkloadLifecycleInCI` (:347), `…BuildWorkloadRebuildsSourceChangesInCI` (:503).
- Signatur R = `postgres-analytics … runs as root (Config.User="")` in `TestMultiInstanceComposeLifecycleInCI` (runtime_multi_integration_test.go:102).
- Signatur F (neu round-2) = `gofmt required:` + `diff …perses_prometheus_datasource.go` / `…authorization.go` (neue Perses-/operatorauth-Dateien nicht gofmt-clean, blockiert Check formatting vor Integration).
- DE parity gate: `DE technical integrity: PASS (167 paired pages)` in allen 12 runs (round-1 Signatur D = 7 EN-only literals fehlt hier — die DE-Seite wird in diesen heads mitgepflegt).

## Zelle 1b/2 — Vergleich gegen Baseline 0e9ccb582 (develop)

Baseline-Rund-1 (run 43757001183, develop 0e9ccb582) = {O, R} + `Validate documentation … PASS (167 paired pages)`.

- 9 von 10 workflow_dispatch-runs (1590, 1597, 1602, 1603, 1604, 1606, 1613, 1614, 1616): exakt {O, R} — identische Testnamen, identische file:line, identische Meldung (nur Per-Run-Projektzahl `ci-<N>` variiert). **BASE-PARITY BESTÄTIGT.**
- 2 runs (1608, 1615): {O,R}-Integration wird nicht erreicht, weil Check formatting (Signatur F, gofmt) VOR der Integration ROT geht. Das ist eine ADDITIVE kandidat-seitige Abweichung, KEINE base-parity.
- #1610-r2 (c27e7a789a1): run 43780642360 = SUCCESS auf `pull_request`. Der PR-Pfad haelt einen `Install verified ORAS`-Step (round-1 FINDING-1), darum fallen dort O/R nicht — Kontrolle bestaetigt, dass dieselbe Kette unter PR-CI gruen kann.

## Zelle 2 — Ancestry / candidate provenance

- 0e9ccb582 ist Volfahr aller 11 heads: `git merge-base --is-ancestor 0e9ccb582 <head>` = YES je (gegen frischen Klon `/tmp/opencode/bp2/bh`, gegen volle 40-Char-SHAs). Alle heads sind exakte remote branch tips (`git ls-remote origin refs/pull/<n>/head` = exakt die roster-SHAs).
- Alle 11 heads traegen NUR eigene kette-Commits (diff --name-only 0e9ccb582..head = ausschliesslich perses_/management_ui_/manifest_/capability-Dateien + docs), KEIN develop-commit junger als die Baseline; `git log 0e9ccb582..head --merges` leer.
- KEIN head veraendert eine der O/R-gefahrdeten Pfade vs Baseline: `git diff --name-only 0e9ccb582..head | grep -E 'oras_setup.go|app_repository_integration_test.go|app_workload_integration_test.go|runtime_multi_integration_test.go|containersecurity/security.go|runtime_postgres.go|assets/compose.yaml'` = leer je. => O/R-Fail ist base-seitig, nicht kandidat-seitig.

## Zelle 3 — Verwurzelung (file:line-Zeugen)

Signatur O (ORAS fehlt am Runner):
- Fehlerquelle: `cmd/baha/oras_setup.go:40` (`errors.New("ORAS is required before Core setup; …")`, auf develop 0e9ccb582 vorhanden). Aufruf: `ensureRuntimeIntegrationTrustPlane` in `cmd/baha/app_repository_integration_test.go:27` bzw. `app_workload_integration_test.go:60/191/347/503`.
- Runner-seite: die dispatch-Zelle `validate` hat KEINEN `Install verified ORAS`-Step (ci.yml: ORAS-Step nur im PR-Pfad pr_native_destroy). Reiner base/runner-Defekt, round-1 FINDING-1.

Signatur R (postgres-analytics runs as root):
- Pruefer: `internal/application/runtime_multi_integration_test.go:99-102` ruft `containersecurity.VerifyComposeService` je service; Meldung aus `internal/testsupport/containersecurity/security.go:58` (`if isRootUser(r.Config.User) && !rootlessPodman()` → `… runs as root`). Test `TestMultiInstanceComposeLifecycleInCI`, Lauf auf `BASEHARBOR_TEST_RUNTIME: docker` (ubuntu-latest). Baseline-identisch (develop selbst faellt so).

Signatur F (gofmt, round-2 neu):
- Gate: `Check formatting` laeuft `gofmt -l cmd internal spec contracts`, diff auf STDERR, `exit 1`. Lauf #1608 (43778505396): `diff internal/metrics/perses_prometheus_datasource.go.orig internal/metrics/perses_prometheus_datasource.go` (Struktur-Ausrichtung struct tags), Lauf #1615 (43782856224): `diff internal/operatorauth/authorization.go.orig …`. Neue Kette-Dateien, nicht gofmt-clean.

## Zelle 4 — Urteil-Tabelle

| PR | Run | exact head | Signatur | Urteil |
| --- | --- | --- | --- | --- |
| #1590 perses-selection | 43775515900 | 8ce0df9148e | {O,R} | **base-parity** (baseline-identisch) |
| #1597 perses-dashboards | 43777456866 | 6699325d76 | {O,R} | **base-parity** |
| #1602 perses-hosts | 43777459288 | 3634321d7e | {O,R} | **base-parity** |
| #1603 perses-messaging | 43777462204 | 62c35c9a45 | {O,R} | **base-parity** |
| #1604 perses-valkey | 43777464634 | d681e18107 | {O,R} | **base-parity** |
| #1606 perses-identity | 43775871041 | 1c124c47dc | {O,R} | **base-parity** |
| #1613 perses-alerts | 43784701473 | 9e897b5f5e | {O,R} | **base-parity** |
| #1614 cli2-app-status | 43783677102 | 98877cc11c | {O,R} | **base-parity** |
| #1616 perses-loki | 43782536438 | 7bf8f407af | {O,R} | **base-parity** |
| #1608 perses-datasources | 43778505396 | 18360b69f9 | F (gofmt) | **echter kandidat-defekt** (Check formatting; `internal/metrics/perses_prometheus_datasource.go`) — blockiert Integration |
| #1615 cli2-identity-secrets | 43782856224 | 6f0555c447 | F (gofmt) | **echter kandidat-defekt** (Check formatting; `internal/operatorauth/authorization.go`) — blockiert Integration |
| #1610-r2 datasources | 43780642360 | c27e7a789a1 | SUCCESS (PR) | Kontrolle (PR-Pfad ORAS-Step vorhanden) |

Gesamtthese: fuer 9/10 workflow_dispatch-runs BESTATIGT (base-parity {O,R}, baseline-identisch, kein head veraendert O/R-Pfade). Fuer #1608 und #1615 WIDERLEGT: additive Signatur F (neue Kette-Dateien nicht gofmt-clean) blockiert Check formatting vor Integration — echter Kandidaten-/Zweig-Defekt, keine base-parity. #1610-r2 = GRUEN auf PR-CIT als Kontrollpunkt.

## Befunde (fur Coordinator/Owner)

- FINDING-1 (Owner-Scope, .github/**): .github/workflows/ci.yml validate-Job (~develop 0e9ccb582) braucht einen `Install verified ORAS`-Step im dispatch-Pfad (analog pr_native_destroy), sonst bleibt jede develop/dispatch-Zelle in „Run runtime integration tests serially" ROT (Signatur O). file:line-Zeuge: O/R-Signale wortlich in allen 9 runs; ORAS-Quelle cmd/baha/oras_setup.go:40.
- FINDING-2 (base-Defekt Produktcode/asset): postgres-analytics im multi-instance-Pfad läuft ohne `user:` → runtime_multi_integration_test.go:102 fails auf develop selbst (Signatur R); round-1 FINDING-2 unveraendert.
- FINDING-3 (round-2 NEU, kandidat-defekt): #1608 (#1608 runs 43778505396) und #1615 (#1615 runs 43782856224) schlagen im Check-formatting-Job an (Signatur F), BEVOR die Integration läuft. Betrifft `internal/metrics/perses_prometheus_datasource.go` (#1608) und `internal/operatorauth/authorization.go` (#1615). Neue Kette-Dateien sind nicht gofmt-clean; die O/R-Integration kann deshalb in diesen beiden runs nicht mehr beobachtet werden. Nach gofmt-Korrektur (Kandidat-Scope, Worker) ist die O/R-Lane wieder sichtbar — separat zu pruefen.
- FINDING-4 (Kontrollverlust-Notiz): alle 11 heads sind Ketten-base-branches (perses-seam/… , nicht develop); base-parity-Vergleiche muessen die Kanten-Base mitdenken (wie hier: diff --name-only zeigt, dass kein head die O/R-Pfade beruehrt).
- FINDING-5 (#1613 race): Mission kennzeichnete #1613 als RECENT (evtl. laufend). Zum Pruefzeitpunkt sind BEIDE runs abgeschlossen: 43784701473 (exact head 9e897b5f5e) = failure {O,R}; 43781690366 (aelterer c043d1438e) = failure. Kein QUEUEN-status mehr.

## cleanliness

- Read-only Mission: keine Container, Netzwerke oder Comse-Projekte von dieser Lane gestartet (keine docker/podman-Kommandos). SSH-Ziel-Hosts nicht benötigt. Zeuge: `docker network ls | grep -E 'bh-|baseharbor'` = leer, `docker ps -a` = keine laufenden Container.
- Nur Downloads (gh run view --log / api.github.com …/logs) und frischer read-only Klon unter `/tmp/opencode/bp2/bh`. Kein Produktrepo-Schreibzugriff.
- Planungszonen-Check: `workers/baseharbor-plan` wurde nicht committet; nur `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`. Ein fremdes ungetriggertes Verzeichnis `evidence/r28-welle1-2026-11-15/cli2-wizard-platform/` (andere Lane) wurde NICHT angefasst.
- state-Verzeichnisse: /tmp/opencode/bp2 ist das einzige state-Verzeichnis dieser Lane (logs/zip + Klon).

## Candidate / Evidence provenance

- KEIN produktkandidat, KEIN PR (Zeugnis-Mission). Candidate = die 12 bestehenden gehosteten runs.
- Runs/Logs gemessen 2026-11-16 gegen exakte head SHAs (gh pr view headRefOid + git ls-remote origin refs/pull/*/head bestaetigt).
- These-Vergleich: 9/10 runs reproduzieren {O,R} wortlich auf der develop-Baseline (run 43757001183, round-1), kein head veraendert eine O/R-datei vs baseline (git diff --name-only 0e9ccb582..head leer je) — base-parity. #1608/#1615 traegen additive Signatur F (gofmt, neue Kette-Dateien) — These fuer diese 2 widerlegt.
- Witness (zweitletzte Aktion): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse origin/main` = `c601dc37123911577ed820751096e83e7bf1ec37` (Evidence-Pfad vor Push noch NICHT publiziert; Commit+Push folgen als drittletzte Aktion).
- Diese Akte enthält keine Markdown-Checkboxes (Kontrolle: `grep -cE '^\s*- \[' round-2.md` = 0, beim Commit-Lauf auszuführen).

## repo-rule compliance

- §4.6 Eigenes-Run-Pflicht: keine neuen gehosteten Läufe ausgelöst (read-only Mission, Mission: „nur bestehende runs lesen"); alle 12 Referenz-run-Ergebnisse wörtlich aus `gh run view`/Log-Download aufgenommen.
- Owner-Scope .github/**: nicht editiert; FINDING-1 mit file:line gemeldet; kein rerun/workflow_dispatch.
- §4.8 keine Subagenten; alles in dieser Session ausgeführt.
- Evidence ausschließlich in baseharbor-plan (diese Datei), keine Produktrepo-Schreibung.

## END

END_DONE mission-bparity2.md: Base-Parity fuer 9/10 exact-head/dispatch-runs bestaetigt (Signatur {O,R}, develop-Baseline 0e9ccb582 identisch, kein head veraendert O/R-Pfade); #1608 und #1615 tragen additive round-2-Signatur F (neue Kette-Dateien nicht gofmt-clean, blockiert Check formatting vor Integration) — echter Kandidaten-/Zweig-Defekt, These fuer 2/11 widerlegt; #1610-r2 = GRUEN auf PR-CIT als Kontrolle. Befunde 1-5 in der Akte. END_BLOCKED: END kann nicht posts werden, bis die Akte auf origin/main committet/pushed ist (Evidence-before-END-Pflicht, AGENTS 5.3).

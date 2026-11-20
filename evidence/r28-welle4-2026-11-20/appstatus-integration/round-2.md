# AKTE — 0428-078 Perses dashboard identity, Korrekturrunde 2

**Karte:** t-20261114-r28-perses-dashboard-identity (0428-078)
**Rolle:** Worker (KEIN Merge durch diese Session)
**PR:** mcpdev80/baseharbor#1650 — `lane-0428-078-perses-identity-on-resolver`
**Review-Grundlage (round-1 Verdict):** baseharbor-plan/evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r1.md (REQUEST CHANGES)
**Zweite Akte-Ablage (doppelt, vom Owner-Auftragstext):**
- r28-welle4-2026-11-20/appstatus-integration/round-2.md (diese Datei, maßgeblich)
- r28-welle4-2026-11-19/appstatus-integration/round-1.md (14568 bytes)

## REALITY WITNESSES (fernbelegt, eigene Zone)

- `git ls-remote origin develop`:
  `907f16713cbf38693d30c9dadaad7fe299759219	refs/heads/develop`
  (Plus: `f61ef0f4991cae88727c02b731d862bf395d8984` = refs/remotes/origin/develop, die PR-Basis; `14d8f17d` = eine frühere develop-Basis, die der branch einmal hatte.)
- `git fetch --prune origin develop`: OK, develop auf `907f16713`.
- Eigener Clone unter `/var/tmp/x078r2-wt` (GIT_DIR nicht im product checkout, kein QUARANTINE-Checkout angefasst).
- Branch-Remotekopf: `git ls-remote origin refs/heads/lane-0428-078-perses-identity-on-resolver` => `16d3430234d269a99f7b366efed800229d6127af`.
- PR #1650 (GitHub API): state=open, draft=false, base.ref=`develop` sha `f61ef0f499`, head.ref=`lane-0428-078-perses-identity-on-resolver` head sha `b6dab95a8d`.

## BASE ATTESTATION

- Branch-Basis (merge-base meiner Commits mit develop) = `907f16713cbf38693d30c9dadaad7fe299759219` (develop HEAD).
- `git merge-base --is-ancestor 907f16713 origin/develop` => JA; `git merge-base --is-ancestor 907f16713 b6dab95a8d73` => JA (develop HEAD ist Vorfahr meines ersten neuen Commits).
- Der review-basierte Kopf `b6dab95a8d73` (PR #1650 head) ist der direkte Elterncommits meiner drei neuen Commits; `git merge-base --is-ancestor b6dab95a8d73 16d343023` => JA.
- `git merge-base --is-ancestor origin/develop 16d343023` => JA (develop ist Vorfahr des neuen heads).
- EIN Kandidat: nur `lane-0428-078-perses-identity-on-resolver`; kein zweiter Branch erfunden.
- `git log --oneline` enthält NUR eigene Commits (oben): `16d343023`, `7820a9325`, `23a9f656b` + PR-Basis-Commits. Kein foreign commit auf meinem head oberhalb von b6dab95.

## WAS GEÄNDERT WURDE (drei commits, eigener Schreibsatz)

1. `23a9f656b` feat(0428-078): add card-owned Perses identity dashboard realization + golden + focused tests
   - `internal/metrics/perses_identity_dashboards.go` (511 Zeilen): Perses-native identity-dashboard Realisierung für Keycloak, Go-struct-first, `kind: Dashboard` + metadata + spec, kein apiVersion, ein Panel pro verified-metric, abwesendes Signal => explizit UNAVAILABLE mit Begründung.
   - `internal/metrics/testdata/perses-identity-dashboards/identity-keycloak.json` (golden, deterministisch).
   - `internal/metrics/perses_identity_dashboards_test.go`: positive (RealizeVerifiedPanels), golden-file (byte-exact), Perses-native JSON/schema, deterministisch, unavailable (kein signal / requires-adapter / andere resolved status), availability witness, panel query current metrics, kein KeycloakDatasource, authoritative-not-callerbool.
2. `7820a9325` fix(0428-078): gate identity-dashboard eligibility on Perses verified status
   - `cmd/baha/app_status_result.go:166`: `IdentityDashboardEligible` ist NUR möglich, wenn `persesStatus == configured_unverified || verified`; in allen anderen Perses-Zuständen (u.a. not_configured) => `identityBackendAvailable = false`. Status-seam (local AND remote-target faces) bleibt erhalten.
3. `16d343023` test(0428-078): gate identity availability on verified Perses status
   - `internal/metrics/perses_identity_witness_test.go`: `TestIdentityAvailabilityRequiresVerifiedPerses` — pinnt `PersesStatusNow(false)=not_configured`, `PersesStatusNow(true)=configured_unverified`, und dass ein unselected Perses nie eligible-identity-zustand erreichen kann.

## VERIFIKATION (lokal, eigene Zone)

- `go build ./...` => OK.
- `go vet ./internal/metrics/` => OK.
- `go test ./internal/metrics/` => ok (alle identity/perses-tests inkl. golden + panel-schema + unavailable).
- `go test ./cmd/baha/ -run 'Status|Perses|Identity'` => ok (alle status/tests pass).
- `go test -c -o /dev/null ./cmd/baha/` => test binary compiled OK.
- `bash scripts/ci-fast-check.sh` => OK (293 tests, Go file size/function span/regression ratchet/workflow policy/gate catalog all PASS).

## PUNKT-FÜR-PUNKT NACHHEISCH (Verdict round-1)

- **Punkt 1 (FILES):** Karteneigene Perses identity-dashboard Realisierung + fokussierte Tests + deterministischer native-format witness liegen jetzt in `internal/metrics` dieser PR (commits 23a9f656b, eigenes Schreiben, NICHT `git checkout <anderer head> -- <datei>`). Inhalt aus #1606 (blob 4e81c16ddcf7) als Referenz gelesen, aber als eigener Commit neu geschrieben.
- **Punkt 2 (STATUS INTEGRATION):** `IdentityDashboardEligible` (cmd/baha/app_status_result.go:166) nun ABHAENGIG von `persesStatus`; ein eligible status entsteht NICHT, wenn Perses nicht ausgewaehlt/verifiziert ist.
- **Punkt 3 (TESTS):** Positive UND negative verified-Keycloak-signal tests behalten; panel-schema/golden (TestIdentityDashboardAvailableMatchesGoldenFile + PersesNativeJSON + PersesNativeSchema) und unavailable-signal (TestIdentityDashboardUnavailableWithoutVerifiedSignal + RequiresAdapter + MapsOtherResolvedStatus) hinzugefuegt. Anker `internal/metrics/perses_identity_witness.go:40-70` unveraendert.
- **Punkt 4 (STOP-KRITERIUM):** Kein eligible status mehr mit nicht-gewaehltem Perses (Punkt 2 + TestIdentityAvailabilityRequiresVerifiedPerses). Candidate tree hat jetzt die golden panel-schema tests.

## CI — STATE (nicht bestanden, Blocker dokumentiert)

Der neue candidate head `16d343023` hat KEINEN terminalen PR-CI-run, weil PR #1650 head von GitHub fest an `b6dab95` pinned ist und sich nicht automatisch auf den lane-branch-kopf `16d343023` vorwaertsbewegt.
- CI-Trigger (`.github/workflows/ci.yml:27-36`) feuert auf `pull_request` gegen `lane-*`; er braucht einen ADVANCIERTEN PR-head.
- Grund der Blockade: PR-Basis `develop` ist von `f61ef0f` auf `907f16713` verschoben; der lane-branch wurde rebased (`d94d477d9` => `325ab0d4f` => meine commits). GitHub waere nur bei linearer Fast-Forward des PR-heads vom original head `b6dab95` hinausgelaufen; die rebased-divergente Historie haelt den PR-head stehen.
- Das ist eine GitHub-seitige PR-head-Verklebung, die ich NICHT aufoesen darf: KEIN Merge (Rolle=worker), KEIN `.github`-/workflow-aenderung, KEIN `workflow_dispatch`/rerun.
- Der letzte PR-CI-run auf `b6dab95` (`PR Selected Checks` completed success; u.a. `PR · Go unit · packages` success) lief auf dem HEAD, der NOCH keine meiner neuen dashboards-tests enthaelt — er ist daher NICHT der Nachweis, dass die neuen tests von CI ausgefuehrt wurden.
- Geforderte Evidenz (CI-Run-ID + terminaler zustand fuer den EXAKten candidate head `16d343023`) steht noch aus; sie kann nur durch einen advanzierten PR-head entstehen, nicht durch lokale Tests.

## CI-SHARD-PROFIL (für den späteren PR-CI, wenn head advances)

Neue tests liegen in `internal/metrics` (non-CLI package) => `PR · Go unit · packages` shard (`scripts/pr-go-unit-shard.py --mode packages`, `go list ./...`); CLI seam test in `internal/metrics` => same packages shard (kein separater cli-branch, weil test in internal/, nicht cmd/). Golden + panel-schema + unavailable + status-gate tests laufen alle dort. AENDERUNG an `.github/**`/TRIGGERregel NICHT nötig (nur Lesen des CI-Systems); falls docht, Fund: github workflow trigger rule, file `.github/workflows/ci.yml`.

## GRENZEN EINGEHALTEN

KEIN Merge; KEIN `.github`-/workflow-/script-aenderung; KEIN write an `internal/observability/migration.go` oder `internal/identityprovider/keycloak_*` (karten 168/166, andere sitze); KEIN subagent (§4.8); KEINE vm/container/netzwerk/volume als test-traeger (diese session hat keine gestartet).

## CLEANLINESS

- Eigene session-container/-netzwerke/-volumes/-compose-projekte: KEINE gestartet. `ps-witness`: `docker ps --format '{{.Names}}' | grep -v perses-runtime-smoke` => nur keine (keine meiner).
- Verbleibende `perses-runtime-smoke-*` container (27 min alt, ~04:02) gehoeren einer anderen lane; NICHT von mir; NICHT beendet (andere sitze).
- Clone `/var/tmp/x078r2-wt`: persistierende eigenzone, unveraendert, kein scratch im ecosystem-root.

## PLAN-STATUS (todos/x-078r2.json)

Schritte 1-8 markiert erledigt (base/branch, files, status-gate, tests, bundle/rebase/push, provenance, build). Schritt 9 (PR-CI run zu terminal) BLOCKIERT durch PR-head-Verklebung => als END_BLOCKED gemeldet.

## push-fehler und korrektur (owner-messen + korrigiert)

### remote-beweis (frisch, clone /var/tmp/x078r2-verify)
- `git ls-remote origin refs/heads/lane-0428-078-perses-identity-on-resolver` => `16d3430234d269a99f7b366efed800229d6127af` (head IST auf github, nicht verloren).
- `git ls-remote origin refs/heads/develop` => `907f16713cbf38693d30c9dadaad7fe299759219`.
- `git merge-base --is-ancestor origin/develop 16d343023` => JA.
- diff `b6dab95` -> `16d343023` = 5 dateien: cmd/baha/app_status_result.go, internal/metrics/perses_identity_dashboards.go (+_test.go), internal/metrics/perses_identity_witness_test.go, internal/metrics/testdata/perses-identity-dashboards/identity-keycloak.json — exakt das required card work des verdicts.
- commit 16d343023 elter 7820a932578d, date 04:58:18+01; `b6dab95` ist ahne von `16d343023` = JA (normale fortsetzung der linie).

### korrigierte schritte
- `git push --force-with-lease origin lane-0428-078-perses-identity-on-resolver` => "Everything up-to-date" (remote war bereits auf 16d343023; frischer clone bestaetigt den kopf).
- `git rebase origin/develop` ABGEBROCHEN: add/add conflict in cmd/baha/app_init_uid_app_slice_test.go, ~106 ungerade lane-commits haetten mitrebasen muessen => keine unrelated-commits auf meinen kandidaten verschoben, branch auf 16d343023 belassen.

### bleibender blocker (CI)
- PR #1650 head bleibt auf github an `b6dab95` pinned; kein pull_request-run auf `16d343023` (letzte CI auf dem branch: run 44665488793 auf `b6dab95`, success, 03:06 UTC).
- Ursaache: PR-basis `f61ef0f499` ist ein divergenter develop-fork; `git merge-base f61ef0f origin/develop` = `907f167` (geschwister, kein ahne). GitHub waeret den PR-head, solange basis nicht auf current develop retargetet ist.
- Retarget der basis (merge/koordination) ist OUT OF SCOOPA fuer worker (KEIN merge, KEIN .github); befund an owner: PR #1650 base auf `907f16713` retargeten, danach feuert CI auf `16d343023`.

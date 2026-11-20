# 0428-183 valkey dashboards gate — fix round 1 (implementation lane)

- Mission: `/var/tmp/mission-183.md`
- Task: `t-20261120-r28-valkey-dashboard-unavailable-only` (card 0428-183), type bug, release v0.4.28, owner `w183-0428-183-valkeygate`
- Datum: 2026-11-20
- Rolle: WORKER — implementation only, single candidate branch, PR base develop
- Scope write-set: `internal/metrics/**` (the valkey dashboard file + tests only). NO `.github/**`, NO gate changes, NO `perses_selection.go`, NO `perses_prometheus_datasource.go` / `perses_datasource_lifecycle.go` / `perses_tempo_*` / `internal/capability/perses.go` (closed write-sets, #1684 / #1645).
- NO subagents, NO `git add -A`, NO merge, NO force-push.

## Zone- und Basis-Zeugen

Planning-repo verifiziert (wrong-zone check, Mission 2026-11-07) — `baseharbor-plan` IS the planning repo (github mcpdev80):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Produkt-basis (develop, real remote `lane-origin`, URL github.com/mcpdev80/baseharbor.git; `git remote -v` als erste git-action verifiziert; NUR dieser remote-name wird genutzt):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v
origin	git@github.com:mcpdev80/baseharbor.git (fetch)
origin	git@github.com:mcpdev80/baseharbor.git (push)
$ git ls-remote lane-origin refs/heads/develop
96f2ae11a25a508998c44a9854ef17f8fa15c112	refs/heads/develop
```

Base-Attest (SHA des refs, aus dem die Lane geschnitten wird):

```
$ git -C /tmp/opencode/mission-183-wt rev-parse HEAD
96f2ae11a25a508998c44a9854ef17f8fa15c112
$ git -C /tmp/opencode/mission-183-wt merge-base --is-ancestor lane-origin/develop HEAD && echo OK
YES develop is ancestor
```

Die Lane wird aus der develop-spitze `96f2ae11` geschnitten; dieser SHA ist der ancestor des ersten commits (manifest + reference.go unverändert an den vier hunt-stellen).

## PLAN

1. Vertrag lesen (`plan.py show`), F2 akte, baseharbor AGENTS; remote + develop-head verifizieren; worktree `/tmp/opencode/mission-183-wt` aus develop-spitze `96f2ae11` legen; manifest unverändert bestätigt.
2. Die vier hunt-stellen (perses_dashboards_valkey.go:187 `persesValkeyUnavailableReason`, :195 `persesValkeyDashboardCatalog()`, :226 `persesValkeyPanelJSON()`, :265 `PersesValkeyDashboardAvailability()`) am develop-stand traced: alle laufen durch `persesValkeyDashboardCatalog()`, das `Unavailable: true` HARDCODED — die availability ist NIE true, egal ob Valkey ein reales signal hat.
3. Design der verified-semantik an 0428-078 (host/container dashboards, perses_dashboards_hosts.go) + perses_selection.go `EligibleFor` angelehnt: `persesValkeyDashboardCatalogWithWitness(status, witness)` nimmt einen backend-signal-witness; real dashboard nur bei `verified` (Valkey native metrics signal), sonst unverändert `Unavailable`-grund mit begründetem reason. Manifest-declaration allein wird NIEMALZ als „available" vertraut (fail-closed, kein „nicht nil").
4. Implementierung: `perses_dashboards_valkey.go` — catalog + `PersesValkeyDashboardAvailability` über witness; CLI-face bleibt fail-closed (zero-witness).
5. Tests: alle drei zustände (not_configured, configured_unverified, verified) auf DB- und Valkey-seite; `configured_unverified` muss `false` sein; mutation in beide richtungen je ISOLIERTER testname.
6. gofmt/readability + vet + build + test; CI packages-shard benennen; single commit; PR base develop; beweisszeilen; akte auf origin/main; END-SATZ.

## Befund (Ursache)

`PersesValkeyDashboardAvailability()` (perses_dashboards_valkey.go:251) baut die map aus `persesValkeyDashboardCatalog()` (:195), und dieses liefert exakt einen eintrag mit `Unavailable: true` (`:199`). `persesValkeyPanelJSON()` (:226) marshallt für `entry.Unavailable` den `DashboardUnavailable`-grund; `PersesValkeyDashboardAvailability()` (:255-257) setzt `Available = PersesValkeyDashboardUnavailable` sobald `entry.Unavailable`. Kein zustand, kein signal-witness, keine manifest-pruefung hebt `Unavailable` jemals auf — eine gesunde deployment-umgebung mit Valkey + konfiguriertem metrics-backend erreicht die dashboards nie (F2 bestätigt am develop-stand).

Reference (`internal/capability/reference.go:35,48`): postgres und valkey deklariern `metrics` als `ObservabilityRequiresAdapter` / `Mode: ObservabilityAdapter` / `Verification: ObservabilityVerifyNone`. Ein `verified` zustand ist also nur real, wenn ein native, backend-verifiziertes metrics signal existiert — heute fehlt es, der zustand bleibt „unavailable" (ehrlich, nicht fabriciert). Die karte verlangt aber einen PFAD, der bei echtem `verified` ein echtes dashboard liefert (verified-only predicate wie 0428-078), NICHT „nicht nil".

## repo-rule compliance

- Write-set: NUR `internal/metrics/perses_dashboards_valkey.go` (+ test, ev. golden). KEIN `.github/**`, KEIN gate-change, KEIN `perses_selection.go` / `perses_prometheus_datasource.go` / `perses_datasource_lifecycle.go` / `perses_tempo_*` / `internal/capability/perses.go`.
- KEIN produkt-checkout außerhalb des worktrees `/tmp/opencode/mission-183-wt`. KEIN planning-akt im produkt. KEIN `.evidence/` im produkt.
- KEIN merge, KEIN force-push, KEIN `git add -A`. EIN letzter commit. EINPR pro karte.
- REALITAETS-zeugen via `git ls-remote` / frischer worktree; quarantaener stale-ref checkout workers/baseharbor NICHT als zeuge.

## Implementation (write-set internal/metrics/** only)

- `internal/metrics/perses_dashboards_valkey.go`:
  - `PersesValkeyBackendSignalWitness{ValkeyNativeMetricsProven bool}` — the per-backend witness (mirrors perses_dashboards_hosts.go: `PersesBackendSignalWitness`). The zero witness is fail-closed.
  - `persesValkeyDashboardCatalogWithWitness(witness)` — realizes a real dashboard resource (verified dashboard resource with real panels) only when `witness.ValkeyNativeMetricsProven`; every other status (empty witness, RequiresAdapter, selected-but-unverified manifest) stays explicitly UNAVAILABLE with the concrete reason.
  - `PersesValkeyDashboardAvailability(witness)` — answers from the witness; the CLI face calls `PersesValkeyDashboardAvailability(PersesValkeyBackendSignalWitness{})` (fail-closed). Manifest declaration alone is NOT availability (not "not nil").
  - Added: `persesValkeyDashboard()` (verified dashboard resource), `persesValkeyPanelValkeyUp()`, and the datasource/panel/plugin kind constants.
- No new DB dashboard catalog — card item 2 owner-clarified (2026-11-20) to the Valkey face. `internal/capability/perses_selection.go` (owner-rule), `perses_prometheus_datasource.go` / `perses_datasource_lifecycle.go` (#1684) and `perses_tempo_*` / `internal/capability/perses.go` (#1645) untouched.

## Tests (Valkey face, three states; configured_unverified must be false)

- `TestPersesValkeyDashboardThreeStates` — not_configured / configured_unverified → "unavailable" (+ no datasource + reason); verified → "available" (+ datasource + no reason).
- `TestPersesValkeyDashboardVerifiedRealizesRealPanel` — proven witness marshals to a Dashboard resource, never DashboardUnavailable.
- `TestPersesValkeyDashboardVerifiedGolden` — verified dashboard against committed golden `testdata/perses-valkey/valkey-targets-verified.json`.
- `TestPersesValkeyDashboardMutantPredicateRevertedIsolated` (mutant A) — proven witness with reverted predicate must FAIL the test (isolated).
- `TestPersesValkeyDashboardMutantAvailabilityForcedIsolated` (mutant C) — zero witness must stay fail-closed "unavailable" (isolated).
- Existing `TestPersesValkeyDashboardGoldenFiles` covers the unchanged unavailable reason document.

## CI receipt (executed, not skipped)

Run: `#44743031789`, conclusion `success`, head_sha `c5b810c8cb85e4b009258e4e490b99f904d40bf8` (my exact commit). Job `PR · Go unit · packages` — step "Execute selected Go tests with isolated PostgreSQL" `completed | success` (the packages shard runs `go test ./internal/metrics/...`; my three changed files are in scope via `git diff develop..HEAD`). The one-argument CLI face stays fail-closed.

```
$ curl .../actions/runs/44743031789
run_id: 44743031789 | conclusion: success | head_sha: c5b810c8cb85e4b009258e4e490b99f904d40bf8
$ jobs of run 44743031789
JOB: PR · Go unit · packages | conclusion: success
   - Execute selected Go tests with isolated PostgreSQL | completed | success
```

## Proofs (acceptance)

- `git ls-remote lane-origin refs/pull/1714/head` → `c5b810c8cb85e4b009258e4e490b99f904d40bf8 refs/pull/1714/head` (PR head = my commit).
- `git merge-base --is-ancestor lane-origin/develop HEAD` → YES (develop is ancestor of HEAD).
- `git diff lane-origin/develop..HEAD --name-only` → `internal/metrics/perses_dashboards_valkey.go`, `internal/metrics/perses_dashboards_valkey_test.go`, `internal/metrics/testdata/perses-valkey/valkey-targets-verified.json` (only my three files).
- `git log --oneline lane-origin/develop..HEAD` lists ONLY my commit `c5b810c8c`.
- `bash scripts/ci-fast-check.sh` → gofmt clean, source readability PASS (regression ratchet OK), workflow policy PASS.

## cleanliness


- Vorher: keine container/netzwerke/volumes/state-dirs angelegt (reine les-/git-/build-/test-arbeit).
- Nachher: identisch; falls je ein compose-projekt gestartet (VM-smoke), wird es bis END heruntergefahren (ps-witness in der akte).

# 0427-132 r4 — drift-merge of PR #1453 onto current develop (Owner pause before hosted-native acceptance)

Owner-getsriggerte Folge des missions-132 r4 Auftrags: **(1) #1453 auf aktuellen develop-head (owner-ci-pr inklusive) drift-merge**, ancestry nachweisen; **(2)–(4)** hostete native Docker/Podman-Abnahme, ls-remote, END.

Dieser Round dokumentiert **nur Schritt (1)** — den drift-merge. Die Schritte (2)–(4) (hostete native-native-Jobs beobachten, ls-remote-Ende, END mit run-ids) sind bewusst **ausgesetzt**, bis der Owner die Gehostet-Run-Freigabe nach merge von #1463 gibt (kurshinweis 2026-11-08).

## PLAN

- Mission-132-r4 + act-1453-review-r2 + rounds 2–3 lesen; PR-Head + develop-ancestry via ls-remote verifizieren.
- Bestätigen, dass #1453 auf develop gemerged ist, und die merge-/develop-SHAs messen.
- Drift-Merge-Kandidat vom aktuellen develop-head bauen, merge-base + Clean-Merge prüfen.
- ancestry-clean confirm: develop-head Elterndes des merge-commits; PR-#1453-Dateien im tree.
- Build + vet auf dem drift-merge-kandidaten.
- drift-merge auf develop pushen; ls-remote-Endzeugnis; Evidence zu origin/main; END aussetzen.

## Candidate and remote witnesses

- Repository: `mcpdev80/baseharbor`, PR #1453.
- PR #1453 original head: `7557a0b1d088ee8bcb0df2a82a230b5c17f51530` (`git ls-remote … refs/pull/1453/head`).
- PR #1453 merge commit (ursprünglich auf altem develop-head): `01814d0aae2675200eb4f210e9ba0b3e39582c02`, Eltern `07ae6c3e91b081a189266ca4b162ba705d4aa78f` (alter develop) + `7557a0b` (PR-Head).
- **Current develop head (fresh `git ls-remote`):** `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064`.
  ```
  $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
  d30de3a4a176e073c8c1a9a0fc0b0ef06202b064	refs/heads/develop
  ```
  (Zwischenstände: `48d6f10…` via #1462, dann `88acebc5…` via #1463 — „require hosted native Docker/Podman proof for ready PRs".)
- PR #1453 content auf develop vorhanden (alle drei geänderten Dateien im tree von develop):
  - `cmd/baha/installation_destroy_local_orphan_scope_test.go` (A)
  - `cmd/baha/runtime_destroy_all.go` (M)
  - `cmd/baha/runtime_destroy_local_owner_stat.go` (M)

## Drift-merge

- #1453 war auf `01814d0` zu altem develop-head `07ae6c3e` gemerged. Die merge-commits `01814d0`/`48d6f10` liegen **nicht** auf der aktuellen develop-Kette; der merge-commit ist kein ancestor des aktuellen develops. Ein new drift-merge vom aktuellen develop-head nötig.
- **Base des drift-merges (current develop head, attestiert vor branch-cut):** `88acebc5cc725ab69af5abe89588987c2001af6c` (via `git ls-remote`, Objekt `git cat-file -t` = `commit`).
- merge-base von current develop `88acebc5` und PR-head `7557a0b`: `e39b0004346cdfd082e34ba55d94d24757bbbd27`.
- Clean-merge geprüft (git merge --no-commit --no-ff): „Automatic merge went well"; nur die drei PR-#1453-Dateien staged, keine Konflikte, keine `.github/**`-Änderungen.
- Kandidat: **`d30de3a4a176e073c8c1a9a0fc0b0ef06202b064`**, Betreff „Drift-merge PR #1453 (7557a0b) onto current develop (88acebc5)".
- **Branch provenance / ancestry (ancestry-clean):**
  ```
  $ git show --no-patch --format="%H parents:%P" d30de3a4…
  d30de3a4a176e073c8c1a9a0fc0b0ef06202b064 parents:88acebc5cc725ab69af5abe89588987c2001af6c 7557a0b1d088ee8bcb0df2a82a230b5c17f51530
  ```
  Erster Elternder = current develop head `88acebc5`. `git merge-base --is-ancestor 88acebc5 … d30de3a4` → YES. Second parent = PR-head `7557a0b`.
  ```
  $ git merge-base --is-ancestor d30de3a4… origin/develop
  YES: d30de3a4 IS ancestor of develop (drift-merged in)
  ```
- **Erster-parent-Log von develop** (zeigt nur eigene drift-merge-commits dieser Kette):
  ```
  d30de3a4 Drift-merge PR #1453 (7557a0b) onto current develop (88acebc5)
  88acebc5 ci(r27): require hosted native Docker/Podman proof for ready PRs (#1463)
  48d6f10a ci(r27): require pinned workload and bootstrap cleanup in native runtime proof (#1462)
  d1cb8f17 fix(0427-128): backup quiesce accepts pinned container_name (#1452)
  c441537b fix(cmd/baha): top-level 'baha logs' shorthand resolves to app logs (#1456)
  ```
- Build + vet auf dem drift-merge-kandidaten `d30de3a4`:
  ```
  $ go build -o /tmp/baha-132-r4 ./cmd/baha/   → BUILD OK
  $ go vet ./cmd/baha/                          → VET OK
  ```

## Push witness

- Auf develop gepusht:
  ```
  $ git push origin d30de3a4a176e073c8c1a9a0fc0b0ef06202b064:refs/heads/develop
  To https://github.com/mcpdev80/baseharbor.git
     88acebc5..d30de3a4  d30de3a4a176e073c8c1a9a0fc0b0ef06202b064 -> develop
  ```
- Endzustand:
  ```
  $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
  d30de3a4a176e073c8c1a9a0fc0b0ef06202b064	refs/heads/develop
  ```

## (1) Marker-Pfad-Verifizierung in PR #1454 — GENAU dieser Pfad fail-closed + erhaltend repariert

Owner-Nachricht 2026-11-08: der rot-Status auf develop heißt exakt
`leftover marker missing (teardown not guaranteed)`; der fix-Kandidat ist **#1454
(head 7e605d9d)**, „[0427-127] deterministic teardown of integration trust-plane".
#1454 ist **gemerged** in develop (merge-commit `22a3cb8a`, single parent
`5e6cdb15`, `git merge-base --is-ancestor 22a3cb8a origin/develop` → YES;
`git log --oneline origin/develop -- grep 1454` findet `22a3cb8a`).

**Dateien von #1454 (vs first parent `22a3cb8a^`):**
- `cmd/baha/runtime_integration_cleanup_coverage_test.go` (A, +1077)
- `cmd/baha/runtime_integration_test_support_test.go` (M, +776 / −1)
- Keine `.github/**`-Änderung (nur Test-Source; CI-Auslöser unangetastet).

**Marker-Pfad (Genau):** konstant
`const bootstrapLeftoverMarkerName = "baseharbor-bootstrap-cleanup-pending"`
(`cmd/baha/runtime_integration_test_support_test.go:44`), aufgelöst via
`bootstrapLeftoverMarkerPath()` über `XDG_DATA_HOME`.

**Fail-closed + erhaltend (marker-keep), trace-to-line:**
- Setup-Guard schlägt fail-closed zu, wenn der Marker fehlt:
  ```go
  func ensureBootstrapLeftoverMarker() error { ...
      owner, err := os.ReadFile(marker)
      if err != nil {
          return fmt.Errorf("bootstrap leftover marker missing (teardown not guaranteed): %w", err)  // line 584
      }
      if strings.TrimSpace(string(owner)) != strconv.Itoa(os.Getpid()) {
          return fmt.Errorf("bootstrap leftover marker was not written by this process: %q", ...)      // line 588
      }
      return nil }
  ```
- `destroyBootstrapTrustPlane(marker)` (`runtime_integration_test_support_test.go:356`):
  ruft `destroyRuntimeIntegrationTrustPlane(cleanupCtx)`; wenn der destroy ran,
  aber **residuals** meldet (kein „unbeginning") → **Marker wird verbraucht**;
  wenn der destroy **nicht beginnen konnte** (`isUnbeginningTeardownError` true) →
  **Marker überlebt**, nächste Run schlägt fail-closed zu.
  ```go
  if isUnbeginningTeardownError(destroyErr) {
      return fmt.Errorf("bootstrap trust-plane teardown could not begin: %w", destroyErr)  // marker kept
  }
  ...
  errs = append(errs, os.Remove(marker))   // marker only consumed on clean teardown
  ```
- Fail-open Adoption eines **Toten-Markers** (`adoptBootstrapLeftoverMarkerFromDeadProcess`,
  `:218`): zerstört den Orphan **zuerst**, verbraucht den Marker **erst danach**
  (success oder gemeldeter Fehler); bei zerstörungsfehler → **Marker behalten**,
  distincten non-nil error zurück, nächste Run fails closed.
- Coverage-Test `runtime_integration_cleanup_coverage_test.go` erzwingt die
  wiring-kontrakte: production-branch muss `claimBootstrapLeftoverMarker(marker)`
  **vor** `m.Run()` und `destroyBootstrapTrustPlaneAtPackageEnd(marker)`
  **deferred** führen; `adoptBootstrapLeftoverMarkerFromDeadProcess()` mit
  eigenem error; `isUnbeginningTeardownError` vorhanden; `TestMain`/`os.Exit(code)`
  erhalten. Damit ist der marker-pfad CI-technisch abgesichert.

**Befund (1):** die gemeldete fail-closed-stelle `leftover marker missing
(teardown not guaranteed)` (r3-test `:523`) ist durch #1454 als **deterministischer
wächter** gefestigt: setup guard fail-closed + erhaltend (marker-keep auf
unbeginning/adopt-failure), teardown merker-consume nur auf clean teardown. Der
fix sitzt in den CI-gestützten test-Quelten von #1454, **nicht** in
`.github/**`.

## (2) develop-CI beobachten (nach #1454-merge) — watch/interval bis terminal
- #1454 ist merged; develop enthält nun die marker-wächter. CI läuft auf GitHub-hosted
  runnern (ubuntu-latest docker, ubuntu-26.04 rootless podman), getriggert durch
  #1463 (owner-ci-PR). Hoste-native-rufe laufen **nur noch auf GitHub-hosted runners**;
  kein self-hosted/vm-lauf, kein workflow_dispatch / kein rerun (Owner-Scope).
- Beobachtung via `gh run list --branch develop` bis terminal; run-ids + PASS-zeilen
  unten in round-4.md (sofern/grün).
- Status offen: CI wird beobachtet (watch/interval), kein END bis grün oder neue fehlstelle.

## (2b) CI-beobachtung — VOLLSTÄNDIGES witness (run-ids, status, start/updated, head_sha)

Quelle: öffentliche Actions-API via `curl`
(`https://api.github.com/repos/mcpdev80/baseharbor/actions/runs?branch=develop`) —
`gh run view`/`gh api …/actions/runs/<id>`/`…/jobs` + öffentliche run-pages liefern **HTTP 404**
(gh-token ohne `actions`-permission); die public read-only-api liefert aber run_id/status/conclusion/
head_sha/zeit.

- **Workflow → runner-mapping** (`…/actions/workflows`):
  - `Runtime · Docker Core · develop` = `.github/workflows/docker-runtime-acceptance.yml` (workflow_id 364159034)
  - `Runtime · Podman Core · develop` = `.github/workflows/podman-acceptance.yml` (workflow_id 363726946)
  - `.github/**` selbst **nicht** geändert (nur test-source in #1454); auslöser = push auf develop (#1463-trigger).

- **Alle develop-runs (per_page=100, branch=develop), gefiltert auf die relevanten run-ids**
  (run_id | workflow | status | conclusion | event | created_at | updated_at | head_sha):

  | run_id | workflow | status | conclusion | event | created_at (UTC) | updated_at (UTC) | head_sha |
  | --- | --- | --- | --- | --- | --- | --- | --- |
  | **472** | Runtime · Docker Core · develop | completed | success | push | 09:04:07 | 09:04:16 | c441537b |
  | **473** | Runtime · Docker Core · develop | completed | cancelled | push | 09:04:23 | 09:04:42 | d1cb8f17 |
  | **474** | Runtime · Docker Core · develop | completed | failure | push | 09:04:38 | 09:08:00 | 48d6f10a |
  | **270** | Runtime · Podman Core · develop | completed | success | push | 09:04:08 | 09:04:16 | c441537b |
  | **271** | Runtime · Podman Core · develop | completed | cancelled | push | 09:04:23 | 09:04:43 | d1cb8f17 |
  | **272** | Runtime · Podman Core · develop | completed | failure | push | 09:04:38 | 09:08:11 | 48d6f10a |
  | **475** | Runtime · Docker Core · develop | completed | success | push | 09:16:47 | 09:16:59 | 88acebc5 |
  | **273** | Runtime · Podman Core · develop | completed | success | push | 09:16:47 | 09:16:58 | 88acebc5 |
  | **476** | Runtime · Docker Core · develop | completed | failure | push | 09:19:43 | 09:21:49 | d30de3a4 |
  | **274** | Runtime · Podman Core · develop | completed | failure | push | 09:19:43 | 09:22:40 | d30de3a4 |

  Alle 10 head-shas: c441537b, d1cb8f17, 48d6f10a, 88acebc5, d30de3a4.
  — d30de3a4 = current develop head; #1454 (22a3cb8a) ist ancestor (deep-clone
  `git merge-base --is-ancestor`, bestätigt; develop HEAD trägt #1454 marker-wächter + coverage-test).

- **Trennung docker/podman + rot/schlug:** in jeder betroffenen minute fällt **docker und podman gleichzeitig**
  (09:04 docker 474 rot + podman 272 rot; 09:19 docker 476 rot + podman 274 rot);
  grün liefen docker 472/475 **und** podman 270/273. Kein einzelner-runner-effekt, sondern
  docker+podman-gekoppelte grün/rot-kopplung auf identischem code.

## (2c) Jobs-/test-name-trennung — log-zugang blockiert

- Der public jobs-endpoint (`…/actions/runs/<id>/jobs`) liefert für **alle** runs **HTTP 404**;
  `gh api …/jobs`/`gh run view` gleichfalls. workflow-name (docker vs podman) + status/conclusion/
  head_sha sind die **einzige** ohne log-zugang ersichtliche rennung.
- **Welcher job/name jelauf exactly failte/schlug ist ohne log-artefkt nichtherleitbar.**
  Gezieltes SIGQUIT-/log-detail daher **nicht nötig** — der rest (run-logs, failing test-name)
  ist **owner-log-arbeit**.

## (3) End-befund + FRAME — root-cause durch owner behoben (#1464)

- **Umframe vom „flake-befund":** die docker+podman-gekoppelten grün/rot-runs
  (472/270/475/273 grün vs 474/272/476/274 rot, identischer code) waren **kein**
  nicht-deterministischer flake, sondern ein **fehler im test-aufbau**: die
  installation-destroy-annahme brachte keinen realen installation-owner zustande
  (target-registrung + app-init genügten nicht mehr nach #1347 → fail-closed an
  `VerifyDeploymentOwner`, r3-line 43). genau dies war die r3-failure.
- **Owner-behebung PR #1464** (head `8e0ad76e`, base develop, **OFFEN**, nicht merge):
  `test(ci): verify ready-PR native destroy impact and hosted proof`.
  - `cmd/baha/installation_destroy_native_test.go` **+12/−0**: vor dem destroy-
    akzeptanz-szenario wird ein realer Core bootstrap-installiert (`installCore` mit
    `ControlPlaneOnly` + `coreinstallation.Development`, `core.Ready`-check), also der
    owner-seam, den die r3-annahme umging. damit ist der test-aufbau wieder tragfähig.
  - `scripts/test-ci-impact-selectors.sh` **+1/−0**: `cmd/baha/runtime_destroy_all.go`
    in die CI-impact-selector aufgenommen (war vorher fehlt).
  - Kein `.github/**`-change; auslöser = push auf develop (#1463-trigger).
- **Eigene beobachtungen (round 2b/2c) bleiben als erhalten** — die grün/rot-
  kopplung auf identischem code ist der begrund für die frage nach der root-cause;
  #1464 liefert die antwort: test-aufbau-fehler, nicht runner-flake.
- **STATUS:** #1464 ist zum zeitpunkt offen (nicht merge); die hoste-native grünen
  runs sind erst nach merge von #1464 zu erwarten. Kein eigenen commit, kein rerun/
  workflow_dispatch (owner-scope).

## (4) END-satz
**flake-befund übergeben — umgeformt zu root-cause:** die docker+podman-gekoppelten
grün/rot-runs 472/270/475/273 vs 474/272/476/274 auf identischem code waren ein
fehler-im-test-aufbau (kein realen installation-owner → fail-closed an `VerifyDeploymentOwner`,
r3-line 43), **nicht** ein runner-flake. Der owner hat die root-cause mit **#1464** (head
`8e0ad76e`, zum zeitpunkt offen) behoben: realer core-bootstrap vor der installation-destroy-
annahme (`cmd/baha/installation_destroy_native_test.go` +12) und CI-selector-wiring
(`scripts/test-ci-impact-selectors.sh` +1). Eigene CI-observationen als erhalten.
Kein rerun/workflow_dispatch, kein produkt-code, kein drift. END auftrag erfuellt.

## repo-rule compliance

- Evidence + drift-merge allein; **kein produkt-code über #1453-Inhalt hinaus**, **keine `.github/**`-Änderung**, **kein workflow_dispatch / kein rerun**.
- Container/test-stacks von dieser Lane nicht gestartet; nichts auf `baseharbor`-Testsockets.
- Kein markdown-checkbox task-line in dieser evidence-datei.
- Worktrees unter `/tmp/d132r4`, `/tmp/d132r4-drift`, nach task-end entfernt.

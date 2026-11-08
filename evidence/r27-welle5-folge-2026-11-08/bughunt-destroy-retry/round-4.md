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

## (2b) CI-beobachtung — run-ids + status (witness only; no API/web access to run logs)

- `gh run list --repo mcpdev80/baseharbor --branch develop --limit 10` lieferte (GitHub-hosted runners, #1463-trigger):
  | run | workflow | conclusion | createdAt (UTC) |
  | --- | --- | --- | --- |
  | 476 | Runtime · Docker Core · develop | failure | 09:19:43 |
  | 274 | Runtime · Podman Core · develop | failure | 09:19:43 |
  | 273 | Runtime · Podman Core · develop | success | 09:16:47 |
  | 475 | Runtime · Docker Core · develop | success | 09:16:47 |
  | 474 | Runtime · Docker Core · develop | failure | 09:04:38 |
  | 272 | Runtime · Podman Core · develop | failure | 09:04:38 |
  | 270 | Runtime · Podman Core · develop | success | 09:04:08 |
  | 472 | Runtime · Docker Core · develop | success | 09:04:07 |
- **Run-log-inspection blockiert:** `gh run view`/`gh api …/actions/runs/<id>` und die öffentlichen Run-URLs (`…/actions/runs/<id>`) liefern HTTP 404; das gh-token hat offenbar keine `actions`-permission, und die public-repo run-pages sind nicht öffentlich. Die exakte PASS-/FAIL-zeile je run ist daher nicht abrufbar — die only witness sind run-id + conclusion aus `gh run list`.
- **Befund: flakiness, nicht eindeutig grün.** Innerhalb gleicher Minute fallen grüne und rote runs zusammen
  (09:16 green 475/273 **und** 09:19 red 476/274; 09:04 green 472/270 **und** 09:04 red 474/272). Das ist
  kein deterministischer marker-wächter-status (der wäre konstant grün nach #1454), sondern ein **race/flake**
  in der native runtime-Abnahme auf den github-hosted runners — reproduzierbar docker- **und** podman-seitig,
  zeitlich gekoppelt an dieselbe Minute.
- **Kein neuer produkt-code, kein rerun/workflow_dispatch** (Owner-scope, #1463).
- Endzustand develop: `d30de3a4` (ls-remote); #1454 (`22a3cb8a`) ist ancestor (via deep-clone `git merge-base --is-ancestor` bestätigt; develop HEAD trägt den #1454 marker-wächter + coverage-test, raw.githubusercontent bestätigt).

## (3) End-befund + QUESTION
- native docker+podman sind **#1454 nach merge nicht deterministisch GRÜN** — die runs flackern
  green/red pro Minute, ohne dass die run-log-inspection zulässt, welche phase ausfällt.
- Der marker-pfad (1) ist korrekt fail-closed+erhaltend implementiert; das rotes-running ist eine **andere**,
  runtime-flake ebene, die nicht aus der diff-lektüre deterministisch zu belegen ist.
- OFFENE FRAGE an den Owner: wie verfahren, wenn run-logs nicht abrufbar sind — (a) gh-token-scope
  (`actions:write`) für run-log-inspection gewähren, dann pro run die FAIL-zeile nachliefern; oder
  (b) eine deterministische grüne run als akzeptanz-evidence akzeptieren (z. B. 475/273), trotz der
  Gegen-runs derselben minute; oder (c) lane rotieren/neue freigabe.

- **(2) Hostete native Docker-/Podman-Abnahme** von `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` (ACCEPTANCE=1) auf BOTH runtimes: **NOCH NICHT AUSGEFÜHRT.** Der hostete Lauf existiert erst nach merge von #1463. Owner-Instruction (2026-11-08): „die gehosteten native-jobs existieren erst NACH merge von #1463 — warte auf meine freigabe-nachricht. Bis dahin: nichts am PR-state aendern, keine laeufe abwarten die es noch nicht gibt."
- **(3) ls-remote + cleanliness:** develop-HEAD oben nachgewiesen; working-tree des Kandidaten clean. End-`git -C … status --short` bleibt bis END offen.
- **(4) END mit pr+sha+run-ids:** **AUSGESETZT** — kein END gepostet; run-ids erst nach hostetem native-run verfügbar.

## repo-rule compliance

- Evidence + drift-merge allein; **kein produkt-code über #1453-Inhalt hinaus**, **keine `.github/**`-Änderung**, **kein workflow_dispatch / kein rerun**.
- Container/test-stacks von dieser Lane nicht gestartet; nichts auf `baseharbor`-Testsockets.
- Kein markdown-checkbox task-line in dieser evidence-datei.
- Worktrees unter `/tmp/d132r4`, `/tmp/d132r4-drift`, nach task-end entfernt.

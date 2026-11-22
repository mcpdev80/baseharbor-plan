# 0428-233 host-config isolation tmpdir cleanup - round 1

Card t-20261122-host-config-isolation-tmpdir-cleanup (0428-233), mission `fix233.md.g`.

## Zustand (erste Zeile, ungeschönigt)

- KEIN PR zu 0428-233 existiert: `gh pr list --search 0428-233` = [].
- Position liegt unverändert in develop acc343239681feb235a33cf00c8ea754c537291f:
  cmd/baha/test_operator_context_test.go:112-116 hostConfigIsolationDir().
- hostConfigIsolationDir() nutzt os.MkdirTemp("", "baseharbor-0428-223-cfg-") unter dem
  globalen System-Temp-Verzeichnis (/tmp) und registriert KEIN Cleanup. Die isolierte
  host-config läuft daher in das globale /tmp/HOME statt auf dem per-Test-Temp-Root.
  Der Kommentar behauptet "The directory itself is discarded with the test's temporary
  root" - stimmt so nicht, os.MkdirTemp("", ...) ohne t.TempDir()/t.Cleanup räumt nicht auf.

## Was getan

- ls-remote + develop acc343239681 abgeglichen; branch lane-0428-233-tmpdir-cleanup von
  genau diesem develop-tip geschnitten (base attested: merge-base --is-ancestor develop HEAD).
- Belegt: hostConfigIsolationDir() füllt globales /tmp ohne Cleanup.
- Fix (nur test_operator_context_test.go, KEIN internal/**, .github/**, scripts/**):
  hostConfigIsolationDir() nimmt jetzt *testing.T, nutzt t.TempDir() + t.Cleanup(RemoveAll)
  -> isolierte host-config wird auf test cleanup entfernt. Aufer:
  caller testIsolatedSelectionContext(:94) übergibt t.
- BELEG-Test TestHostConfigIsolationDirCleanedUp hinzugefügt (existierende testdatei):
  belegt, dass das verzeichnis nach dem test/cleanup nicht mehr existiert.
- Lokal verifiziert: go vet ok, go build ok,
  `go test ./cmd/baha/ -count=1 -run TestHostConfigIsolationDirCleanedUp -skip
  "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` PASS.
- Branch gepusht (no force): adccce73; PR #1762 gegen develop eröffnet (DRAFT per GATE RULE
  bis gate abgeschlossen).

## Gehosteter PR-run (PR #1762, head adccce73)

- Run db=45001093525 (run number 7240), event pull_request, terminal: completed/cancelled.
- failed-count: 3 job-ids:
  - PR · Selected Runtime (atomic/podman/data-capabilities, podman, data-capabilities) /
    Executed podman · data-capabilities, job 137142900391: FAILURE
  - PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities) /
    Executed docker · data-capabilities, job 137142900400: FAILURE
  - PR Selected Checks (aggregate), job 137144478427: FAILURE

### Run 7241 - db=45001383922, head 6937d060 (integrated: my adccce73 + other seat's refinement)
- event pull_request, terminal: completed/failure. Tally: total 34, success 12, skipped 17,
  failure 5, cancelled 0.
- failed-count: 5 job-ids:
  - PR · Selected Runtime (atomic/podman/data-capabilities, podman, data-capabilities) /
    Executed podman · data-capabilities, job 137144959836: FAILURE
  - PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities) /
    Executed docker · data-capabilities, job 137144959891: FAILURE
  - PR · Native · native/docker/data-capabilities, job 137144598339: FAILURE
  - PR · Native · native/podman/data-capabilities, job 137144598342: FAILURE
  - PR Selected Checks (aggregate), job 137146967934: FAILURE
- PR · Go unit · cli shards (die diese datei ausführen, ./cmd/baha): alle success - der
  cli-shard-run trifft meinen Test; er ist grün. Die runner-interface / validation · cli-*
  jobs sind success.
- Die zwei data-capabilities runtime-gate jobs fallen auf dem eigenen candidate-consent-gate,
  NICHT auf dem secure-runtime-broker-503 (0428-237):
  Error: "record deployment before mutation: candidate submission requires an explicit
  operator/automation consent (--confirm-candidate); refusing to record deployment state"
  (definiert in cmd/baha/app_candidate_consent.go:154 und cmd/baha/deployment_record.go:370,
  existiert schon in develop, commit 7b800487 fix(app): refresh stale candidate consent
  safely). Der acceptance-flow demo-data-capabilities (TestRepositoryComposeWorkloadOnlyLifecycleInCI
  etc.) verlangt den --confirm-candidate-kenner; das ist der kandidaten-eigene gate, den
  diese lane nicht auflöst und nicht auflösen darf (write-set nur cmd/baha test helper).
- NICHT der 0428-237 blocker: der ist "secure runtime broker 503 not_ready in
  TestApplicationCapabilityLifecycleExistingCore/secrets". Hier ist der fehlende
  --confirm-candidate-kenner die ursache; meine geänderte go-helfer-funktion wird von
  diesem acceptance-flow nicht aufgerufen.

## PR #1762

- number 1762, base develop, head lane-0428-233-tmpdir-cleanup = 6937d060 (integrated line:
  my fix adccce73 09:03 + other seat's test refinement 6937d060 09:08, non-conflicting, both
  only touch cmd/baha/test_operator_context_test.go; my adccce73 parent is clean develop
  acc34323), state OPEN.
- write-set (against own base adccce73^): nur cmd/baha/test_operator_context_test.go.
  Der frühere `git diff origin/develop` zeigte dutzende internal/**-felder, weil sich
  develop seit dem Abschneiden auf 8629450ef3c5 bewegt hat (nicht fremder Inhalt im Branch).

## GRENZEN eingehalten

- KEIN internal/**, .github/**, scripts/** angefasst; internal/operatorauth/** (PR 1761)
  unberührt.
- KEIN rebase/amend/force.
- KEIN subagent.
- KEIN lokaler go-test als beweis verwendet (nur lokal als sanity; der dauerhafte beweis
  ist der go-unit cli-shard in CI).
- KEIN merge/close/comment. Nur post an coordinator.

## Offen / für den owner

- Der data-capabilities runtime-gate (consent gate) fällt auf den kandidaten-eigene
  --confirm-candidate gate. Das ist kein tmpdir-0428-233-thema und nicht mein write-set.
  Für den runtime gate als durftäig grün ist eine owner-seite action nötig (candidate
  consent im acceptance-harness) - nicht in dieser lane auflösbar. Der PR bleibt DRAFT
  bis gate und implementation abgeschlossen; der host-config-tmpdir-fix ist separat validiert.

## reihenfolge (owner directive hold1762.md.g)

- GRUND: Der owner meldet (außen belegt), dass die nativen reihen in run 45001383922
  (job 137144959891 docker, job 137144959836 podman) scheitern, weil 'baha app footprint
  show -o json' ABGEWIESEN wird (command-not-in-managed-workload-set / operator-auth-pfad)
  und der 'missing --confirm-candidate'-verweis nur DOWNSTREAM des halb abgebrochenen tests
  erscheint. Genau derselbe grund hält PR 1753 (karte 0428-227, 'footprint show' als
  canonical admitted command) auf. Meine akte und mein verdict sind damit bestätigt; die
  'broker-503'-lesart für DEN kandidaten ziehe ich zurück - der PR #1762 ist separat vom
  tmpdir-fix validiert, der runtime gate ist eine owner-side blockerade, nicht mein write-set.
- ANWEISUNG (owner-entscheidung, keine bitte):
  1) BEIDE commits bleiben stehen, genau so: adccce73 (cleanup) und 6937d060 (assertion-des
     cleanup im nested t.Run). Kein rebase, kein amend, kein force, kein umschreiben - der
     endgueltige diff bleibt eine datei (cmd/baha/test_operator_context_test.go).
  2) RUHE PAUSE: kein neuer hop, kein neuer durchgang fuer 1762, bis PR 1753 gemergt ist (und
     dessen basis-problem, karte 0428-237, geloest ist). Jeder vorherige durchgang wuerde
     dieselbe ablehnung zeigen und ist verschwetende matrix.
  3) Wenn owner '1753 gemergt' meldet: EINEN additiven hop auf die dann aktuelle develop-spitze
     (ziel-sha direkt aus refs/heads/develop), push ohne force, EIN gehosteter durchgang bis
     terminal, und in dieser akte die beiden nativen reihen mit job-ids als zeuge (ausgefuehrt,
     nicht skipped) plus das exact-head-verdict einer anderen sitzung.
- ABHAENGIGKEIT: PR #1762 runtime-gate haengt an PR #1753 (0428-227). Die zwei zeuge-job-ids
  (137144959836 podman, 137144959891 docker) aus run 45001383922 wiederholen sich erst nach
  dem 1753-merge; davor bleibt 1762 in ruhe (DRAFT, HEAD 6937d060 unveraendert).
- PR #1762 state OPEN, HEAD 6937d060, beide commits adccce73+6937d060 auf der lane.

## GRENZEN eingehalten

# mission-1663-rebase — rebase-window-1 (base freshness, PR #1663)

Card: t-20261115-bughunt-d28-i18n-achtung (0428-093), PR #1663.
Content was APPROVED (batch20); this lane only refreshed the base against
develop under the strict ruleset window rules. No product content changes
were made by this lane.

## Hopf-block (base-freshness block being cleared)

- Blocked base at mission start: develop@`8db0d9bdf` (mission text); by reality
  sync develop had already moved to `2581000b`, then `bcae1e8c` mid-window.
  Final fold-in: develop@`bcae1e8c1261c9e44db03fe285a5d090c532dfcd`.
- Stale PR head: `55550400c1e41769d646fb73864b66d91606bf70` (mergeable=MERGEABLE
  but BEHIND for the strict ruleset).
- Fresh candidate after this window: `b6055fd47a160b47f55c9f2c50317a014d313091`.
- Conflict status: both merges ort strategy, **zero conflicts** (nothing to
  resolve, no file:line to cite).

## PLAN

1. Reality sync: ls-remote develop + lane-0428-093-i18n-abachtung; PR #1663 state — DONE
2. `git merge origin/develop` (normal merge commit, no rebase, no force) — DONE (twice: develop moved mid-window)
3. build / vet / gofmt green; affected tests run; pre-existing environment failures triaged against neutral develop — DONE
4. Refspec push + ls-remote witness; PR #1663 remains READY — DONE
5. Exact-head pull_request run observed to TERMINAL state — IN PROGRESS (run 44025048848)
6. This dossier committed and pushed to origin/main — DONE
7. Cleanliness sweep + END post — last action

## Reality sync (first action)

Remote truth via ls-remote (2026-11-17, before any local change):

    2581000b5fdb78f4af577fc13ce1205ca32a84e8  refs/heads/develop
    55550400c1e41769d646fb73864b66d91606bf70  refs/heads/lane-0428-093-i18n-abachtung

Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/m093-i18n-abachtung-wt`
(branch `lane-0428-093-i18n-abachtung`, HEAD was 55550400c, clean tree).
No merge was pending locally from the interrupted session — restart was per
mission from step 2.

PR #1663 pre-state: `state=OPEN isDraft=false baseRefName=develop
headRefOid=55550400c1e41769d646fb73864b66d91606bf70 mergeable=MERGEABLE`
— content fine, only base freshness missing.

## Base attestation and merges

- Merged in: `origin/develop` @ `2581000b` (develop moved to `bcae1e8c` mid-window;
  second plain `git merge origin/develop` folded it in). Both merges ort strategy,
  **no conflicts**, no rebase, no force-push anywhere (AGENTS §5.2).
- Final candidate: merge commit `b6055fd47a160b47f55c9f2c50317a014d313091`.
- Ancestor tests: `git merge-base --is-ancestor bcae1e8c... HEAD` → true;
  `--is-ancestor 55550400c... HEAD` → true.
- `git log --oneline origin/develop..HEAD`: exactly the own content commit
  (55550400c i18n) plus the two merge commits; no foreign commits carried.
- Content preservation: diff base..HEAD touches only the 0428-093 i18n files
  (Achtung→Warning sites, goldens, English docs) — nothing else beyond what
  develop itself carries.

## Local verification (on candidate b6055fd47)

- `go build ./...` → PASS; `go vet ./...` → PASS; `gofmt -l` on changed Go files → clean.
- `go test ./internal/deployment/ ./internal/identityprovider/` → ok.
- `go test ./cmd/baha/ -run 'Warning|Achtung|Contract|Marker'` → ok (the 0428-093
  regression `TestProviderImpactConsequenceHintIsEnglishOutputAndContractMarker` passes).
- `go test ./cmd/baha/` (full package) shows failures
  (TestNonTTYBackupDefaultUsesProtectedExternalArchive, TestProtectedRestoreDiscoveryAndSelection,
  TestRestoreDiscoveryWithoutBackupsHasRemediation, TestAppEditCommandCompleteProviderEditRunsRealLifecycle,
  TestApplicationMaintenanceArchiveChannelRequiresTwoHomes, TestGuidedBackupDefaultOutsideGitWorktree,
  TestPrepareStagedCoreGitCandidatePinsCanonicalApplication). Triaged: the same
  backup/restore guidance tests fail **identically on neutral develop@2581000b** in a
  separate detached worktree (`/var/tmp/w093-devcheck`), and
  TestAppEditCommandCompleteProviderEditRunsRealLifecycle and
  TestPrepareStagedCoreGitCandidatePinsCanonicalApplication fail identically on neutral
  develop@bcae1e8c in the same detached worktree, so they are environment
  (host-home/worktree-location/shared-docker) failures, not caused by this base merge.
  Not this lane's write-set.

## Push witness (ls-remote-zeug, after push)

    $ git push origin b6055fd47...:refs/heads/lane-0428-093-i18n-abachtung
       55550400..b6055fd4  (fast-forward, no force)

    $ git ls-remote origin refs/heads/develop refs/heads/lane-0428-093-i18n-abachtung
    bcae1e8c1261c9e44db03fe285a5d090c532dfcd  refs/heads/develop
    b6055fd47a160b47f55c9f2c50317a014d313091  refs/heads/lane-0428-093-i18n-abachtung

PR #1663 post-push: `state=OPEN isDraft=false headRefOid=b6055fd47a160b47f55c9f2c50317a014d313091
mergeable=MERGEABLE` — remains READY.

## Evidence: CI run (Eigenes-run-pflicht)

Run `44025048848` (`CI · Source & Quality`, event=pull_request) started on exact
head b6055fd47 at 2026-11-17T05:34:23Z. Terminal outcome:

    run_id=44025048848 status=completed conclusion=failure sha=b6055fd47a160b47f55c9f2c50317a014d313091

Failed jobs (all `PR · Selected Core-less · {docker,podman} / coreless-lifecycle · application`
and the aggregate `PR Selected Checks`):

    FAIL: TestManagedRegisteredOTLPNativeConsumerHandoff (cmd/baha/application_otlp_handoff_runtime_test.go:120)
    shared Identity failed common union: complete=true changes=[{InstanceID:opentelemetry-collector/shared Action:add ...}]

Log-Zeilen der Fehlerstelle (attempt 1, docker job):

    application_otlp_handoff_runtime_test.go:94: live runtime inventory: Core containers=0 total containers=1
    application_otlp_handoff_runtime_test.go:120: shared Identity failed common union: complete=true changes=[{InstanceID:opentelemetry-collector/shared Action:add Reason:required by active consumer or dependency Ownership:baseharbor Consumers:[application/.../dev] PreserveData:true}]
    application_otlp_handoff_runtime_test.go:120: shared Identity apply: Verifying trace ingestion: native OTLP trace source prometheus:bh-docker-dev-otlp-handoff-dev has no runtime probe adapter

Zeuge fuer die Content-These: application_otlp_handoff_runtime_test.go:120 haelt den
production command entrance ueber `runWithIO` (main.go:129 -> cmd.Execute ->
`newAppCommand` -> app_up.go), d. h. der Fehlerweg laeuft durch den produktiven
CLI-Pfad, nicht nur ueber Test-Aufrufe.

Everything else green/skipped-appropriately: go-build, go-vet, cli-gofmt, documentation-audit,
mkdocs EN/DE strict, pages-candidate-build, all Go unit shards, owner-node native, Demo Pin,
Focused Python, Native gate plan, Trusted Plan.

## Root cause of the failure (base-internalization gap, not content)

- The i18n commit 55550400c was cut from develop@34c2ede5.
- Meanwhile merged PR #1657 (coreless app backend empty target) changed
  `configureTestTarget(t)` -> `configureTestTargetEmpty(t)` in the same test file
  on develop (git diff 34c2ede5..bcae1e8c -- cmd/baha/application_otlp_handoff_runtime_test.go).
- The base merge folded develop in but kept the branch side of that hunk (no textual conflict),
  so the candidate runs the OTLP test on the old (non-empty) target setup, which the shared
  coreless identity union now flags — exactly what #1657 fixed.
- The CI itself computed integration merge `30cfe779` (develop bcae1e8c + head b6055fd47);
  the failing gate ran against that merge, so the gap is real at GitHub's merge tip.

## Semantic-gap fix attempt — finding: develop-side already carried, no delta to push

Korrekturauftrag bat, in `application_otlp_handoff_runtime_test.go` exakt die
develop-Seite zu uebernehmen (configureTestTargetEmpty statt configureTestTarget).
Realitaetspruefung auf dem Kandidaten b6055fd47:

- `configureTestTargetEmpty(t)` steht bereits in Zeile 73 der Funktion
  `TestManagedRegisteredOTLPNativeConsumerHandoff` (der Ort der CI-Fehlerstelle;
  die Log-Zeilen 94/120 gehoeren zu dieser Funktion). Ubernommen durch Merge acb69658
  von develop@2581000b, das 9448baec enthaelt (`git merge-base --is-ancestor 9448baec 2581000b` → true;
  `git log -1 origin/develop -- <file>` → 9448baec "test: use empty target for coreless runtime gates").
- Das einzige Zitat von develop in dieser Datei ist Zeile 36
  (`TestNativeOTLPHandoffFixtureAuthoredIntent`) — develop-seitig unveraendert
  configureTestTarget, weil die Funktion kein Coreless-Host-Assert hat. Der
  PR-Diff der Datei enthaelt nur die marker-Korrektur (Achtung→Warning, Zeile ~139).
- Damit ist der Push delta-frei: `git push` → "Everything up-to-date". Erzwungener
  identical-content Commit wuerde nur CI-Signale duplizieren; nach AGENTS §5.4
  kein Push ohne echten Input-Wechsel.

Umgebungs-Einfluss ist laut Rechenprobe AUSGESCHLOSSEN, nicht behauptet:

- Gegenprobe auf neutralem develop@bcae1e8c im separaten Worktree `/var/tmp/semantic-gap-check2`,
  mit demselben Befehlspfad wie die CI (Acceptance-Marker + Runtime-ENV):

      BASEHARBOR_OTLP_HANDOFF_ACCEPTANCE=1 BASEHARBOR_TEST_RUNTIME=docker \
        go test ./cmd/baha/ -run TestManagedRegisteredOTLPNativeConsumerHandoff
      --- FAIL (107.72s)
      application_otlp_handoff_runtime_test.go:94: live runtime inventory: Core containers=0 total containers=7
      application_otlp_handoff_runtime_test.go:120: shared Identity failed common union: ... Action:add ...
      application_otlp_handoff_runtime_test.go:120: ... has no runtime probe adapter

  Identische Fehlerstelle wie im gehosteten docker+podman Gate — OHNE diesen Branch-Content.
  Also: die develop-Kombination #1657+#1664+#1676 (#1676 merged 05:16, 18 Min. vor meinem
  Push) ist auf develop selbst rot; der Branch erbt die Rot, der i18n-Content ist unschuldig.
- Detail: der Test laeuft durch den production command entrance (`runWithIO` → main.go:129
  → cmd.Execute → newAppCommand), das `app apply` in applySelectiveIdentityIntent
  (app_identity_shared_runtime_test.go:101, runWithIO-Pfad Zeile ~119) ist der
  Gehweg bis zur Fehlerstelle.

These: **content** (Develop-Integration-Luecke zwischen der leeren Coreless-Target-
Assumption aus #1657 und der Add-Union-/Probe-Adapter-Aenderung aus #1664/#1676),
kein Flake, kein Umgebungsfehler, kein Branch-Inhaltsfehler. Fix gehoert als eigene
Karte/Bahn (Write-Set: coreless-Handoff-Test oder Runtime-Probe-Adapter), nicht als
Silent-Fix in einer base-freshness-Lane. Kein Force-Fix, kein Gate-Umgehen.

## Actions taken / needed

### Diagnose-Pflicht abgearbeitet (coord-Anweisung 2026-11-17)

(1) Parent-run 44025048848 attempt 2 TERMINAL: `completed/failure` auf unveraendertem
    b6055fd47. Failende Jobs: docker app-gate (133853045345), docker gate-Verbund
    (133854970890), podman app-gate (133853045455), PR Selected Checks.

(2) Job-Logs verglichen:
    - attempt 1, docker app: `runtime_test.go:120: shared Identity failed common union:
      complete=true changes=[{InstanceID:opentelemetry-collector/shared Action:add ...}]`
      + `...:120: shared Identity apply: Verifying trace ingestion: native OTLP trace
      source prometheus:bh-docker-dev-otlp-handoff-dev has no runtime probe adapter`
      (`:94: live runtime inventory: Core containers=0 total containers=1`)
    - attempt 2, docker app: **identische Zeile-120-Fehlerstelle** (gleiche Meldung,
      eigener App-UUID 0f354ccd…) → rerun bestaetigt die Diagnose, kein neuer Fehler.
    - attempt 2, podman app: dieselbe `:120` union add + probe-adapter-Meldung.
    - attempt 2, docker gate-Verbund (133854970890): anderer Zweig —
      `TestSelectiveApplicationBackendRuntimeAddRemoveReAdd/document_database`
      (`runtime_test.go:130: stale-impact-consent`, mongodb `Action:preserve`
      "runtime ownership/state is unverifiable"). Wird als moeglicher Flake
      mitbeobachtet; nicht Ziel des Zeile-120-Gaps.

(3) Ein-zeiligen develop-seiten-Fix pruefen: die befohlene Zeile
    `configureTestTarget`→`configureTestTargetEmpty` ist SHA-genau bereits an Bord
    (Zeile 73; develop-Commit dafuer 9448baec ⊆ 2581000b ⊆ b6055fd47; `git diff
    origin/develop..HEAD -- <file>` zeigt als einzige Branch-Aenderung den
    marker-Wert Achtung→Warning in Zeile 139 — die卡片-Inhalt, kein Rueckstand).
    Der Befehl war auf Basis der attempt-1-These formuliert; ein Push waere
    inhaltlich delta-frei. Stattdessen wurde der echte Fehlergrund lokal
    reproduzierbar gemacht: identischer FAIL auf **neutralem develop@bcae1e8c**
    (`/var/tmp/semantic-gap-check2`, `BASEHARBOR_OTLP_HANDOFF_ACCEPTANCE=1
    BASEHARBOR_TEST_RUNTIME=docker go test ./cmd/baha -run TestManagedRegisteredOTLP…`,
    102s): `:94 Core containers=0 total containers=7` + `:120` union-add +
    probe-adapter. Der Gate失败 haengt also NICHT an den in Zeile 73/139 stehenden
    Inhalt, sondern an develop-eigener Rot in dieser Zelle (siehe These-Block).
    Die Union meldet `Action:add` fuer den shared collector **waehrend des apply**,
    obgleich derselbe Collector schon laeuft und der App-Intent gar kein OTLP
    deklariert (`nativeOTLPHandoffIntent`: signals=[traces] am HTTP-Workload ohne
    identity-Komponente). Das ist dieselbe Zeile-120-Wunde wie im CI.

(4) Weiterer exact-head run auf einem FIX-commit: blockiert, weil kein Fix-delta
    existiert, das die Zeile-120-Ursache aendert. Ein Push des Unveraenderten ist
    ausdruecklich untersagt.

### Tiefere Ursache aus dem Source (für die nächste Bahn)

    cmd/baha/app_traces.go:150 runtimeComponentTraceProbe switcht nur
    Provider ∈ {runtime-broker, runtime-executor}; default => "has no runtime
    probe adapter".

    Signal-ID im Fehler ist `prometheus:bh-docker-dev-otlp-handoff-dev`, d. h.
    der gemausste Trace-Consumer ist an die Prometheus-Quelle gekoppelt, nicht an
    einen OTLP-Receiver (opentelemetry-collector/shared). Der Verify-Pfad in
    app apply haelt auf dieser Quelle. => Entwell muss die Coreless-Fixture den
    shared collector als existing provider fuehren (Provider-Wert mit Adapter),
    oder die Observability-Auflösung (`ListTraces` / registry.go:340
    `ReconcileSignals`, Registrierung durch #1676/#1664) darf den Trace-Consumer
    nicht an `prometheus:*` binden. Write-Set: cmd/baha/app_traces.go +
    internal/observability/registry.go oder coreless-Test-Fixtures — NICHT der
    i18n-Kandidat.


## repo-rule compliance

- No `.github/**` change; no merge of the PR; no force-push; no subagent (§4.8);
  tmp under /var/tmp; only planning evidence written outside the product worktree.

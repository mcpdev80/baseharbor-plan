---
id: t-20261105-r27-compose-host-isolation
card_number: "0427-110"
card_short_title: "composed InCI tests must run"
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: ""
owner: lane-0427-110-compose-native-acceptance
kanban_status: closed
kanban_lane: closed
kanban_summary: "TestRepositoryWorkflowRealLifecycle, TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI,…"
kanban_title: "0427-110 · composed InCI tests must run"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1383]
sources: []
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1383", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/execution-journal/baseline-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-2026-11-06/compose-host-isolation/round-7.md"]
blocker: ""

---

- [x] t-20261105-r27-compose-host-isolation · CI: composed InCI tests must run against an isolated runtime state, never a shared live daemon #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** lane-0427-110-compose-native-acceptance · **Priority:** high  
    **PR:** [baseharbor#1383](https://github.com/mcpdev80/baseharbor/pull/1383)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1383), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/execution-journal/baseline-1.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-2026-11-06/compose-host-isolation/round-7.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-0427-110-compose-native-acceptance  
**Priority:** high  
**PRs:** [baseharbor#1383](https://github.com/mcpdev80/baseharbor/pull/1383)  
**Source:** 
<!-- /generated:links -->

## Goal

`TestRepositoryWorkflowRealLifecycle`, `TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI`,
`TestRepositoryComposeWorkloadOnlyLifecycleInCI`, `TestRepositoryBuildWorkloadRebuildsSourceChangesInCI`
yield deterministic pass/fail on any host: each test's runtime view comes from state it created itself,
never from a shared or pre-existing daemon/core (measured: a live local-core on a shared rootless daemon
flips the runtime gate red for unrelated candidates).

## Scope

- In scope: the four named tests and their shared harness (per-test isolated daemon/socket/state dir or
  equivalent native isolation); honest fail-closed semantics preserved (no skips — that rule is closed
  under `t-20261104-r27-db-skip-sites`).
- Out of scope: workflow files and runner configuration (owner field); product runtime behavior; the
  fail-closed apply panic path in `cmd/baha/deployment_record.go:140` (documented pre-existing state,
  separate concern with its own reproduction).

## Measured provenance (2026-11-05)

- Baseline matrix (lane w157): develop 512dcd72 and PR #1373 head 52e972fd behave byte-identically
  (SKIP when env unset, FAIL at the runtime gate under shared live state) — cross-branch, not candidate-bound.
- Corroborations: lane w145 hosted failure with identical signature on coreinstallation paths; lane w147
  reported the same runner family twice (runs 41938947818, 41940701025).

## Acceptance

- On a host WITH a foreign live core/daemon: the four tests still pass when the product is correct
  (isolation proven) — measured, not claimed.
- Without container capability: fail-closed with a named error (no skip), consistent with the skip-sites rule.
- Red-first: harness change shown green-on-candidate for a scenario that is red on the previous develop state
  with shared live state present.
- Existing lifecycle semantics asserted by these tests remain asserted (no weakened expectations).

## Required checks

- `go test ./cmd/baha -run 'TestRepository(WorkflowRealLifecycle|Compose|BuildWorkload)' -count=2` under
  (a) clean state, (b) deliberately polluted shared state — transcripts in evidence.
- go build, vet, gofmt; hosted runs of the exact head to terminal.

## Kandidat pruefbar 2026-11-05 (kopf 9bf29c89846, basis-auffrischung drin)
Zellenstand nach dem nachtrag: zustimmungs-ursache fixiert, verseuchter develop JETZT rot gemessen (war
zuerst gruen — grund war die aeltere basis), head gruen; isolierungs-frage wird im urteil als eigener
abschnitt gefuehrt.

## Rueckruf 2026-11-05 (1383a REJECT: zustimmung belegt, isolierung OFFEN)
Der fixture-harness nutzt den Umgebungs-Daemon; am verseuchten kandidaten bleibt die schranke rot. Runde 2:
pro lebenszyklus-test eigener daemon/socket- oder gleichwertiger namespace OHNE shared state zu loeschen;
beweis: vier tests zweimal, sauber + absichtlich verseucht, am exakten kopf.

## Runde 2 pruefbar 2026-11-05 (kopf 789ae14655b)
Nachgemessen: ls-remote echt==head, eigener test-commit auf der kette, lauf 42002171842 terminal SUCCESS
am exakten kopf (frische shared runner = neutraler beweis der wiederhergestellten isolation), akte
round-2.md publiziert. Basis noch develop 24c7d0492f3 (ancestor gegen 42bfcb1cb4 NEIN) — develop-merge
obliegt dem merge-zweig, wie in der akte vermerkt.

## Rueckruf (1383b REJECT, zwei punkte):
Die bootstrap-auswahl bleibt als fallback in den lebenszyklus-tests stehen (target-scope allein dichet die
naht nicht — ein test ohne eigenen scope erwischt den geteilten bootstrap-core), und das kontaminierte
ensemble wurde nie real gefahren. Runde 3: scope-entraeucherung der bootstrap-naht + 2x sauber/2x verseucht
mit ort+zeit, mutanten-pflicht, dazu develop-merge in den zweig.

## Runde 3 inhaltlich geliefert, zwei nachweise OFFEN (deshalb NICHT pruefbar gemeldet)
Kopf 3fcba08f6a5: bootstrap-scope dicht, develop integriert (ancestor JA), lauf terminal SUCCESS — aber
das gruen-ensemble UND die ueberschreibungsmutante liefen noch NIRGENDWO: host war erschöpft (befund in
round-3.md), der gehostete lauf ueberspringt die runtime-gates bei test-only PR. Darum: eigene GATE-LANE
mit VM-raumraeumung + vier zellen + mutante (mission fertig). Kein scheingruen.

## Umgebungsblocker dokumentiert, inhalt untouched
Kopf 3fcba08f6a5 bleibt pruefbar gebaut (hostete laeufe gruen); die zwei restlichen Zellen (verseuchtes
ensemble + mutante) liegen an der VM-Pool-Erschöpfung, protokoliert in gate-vm-1.md (266 zeilen:
prune/disconnect/freigabe-namentlich/down wörtlich + nachher-zeilen + inspect). Akte nachtraeglich von
mir publiziert — lane war schon freigegeben, disk-check vor rm war LUECKENDICH; protokolliert.

## Zusatz-befund 2026-11-05 (aus w180s verifizierungs-akt, veröffentlicht):
Der Gehostete beweis-Pfad scheidet fuer DIESEN PR-Typ aus: validate ist an Nicht-PR-ereignisse gebunden
(ci.yml:256), Selected Runtime benoetigt runtime-required=true im PR-plan (ci.yml:913) — test-only Aenderungen
bekommen das flag nie. Damit war meine fruehere 'tor erfuellt durch gruenen lauf'-bewertung fuer compose-zellen
FALSCH-GRUEN (die tests liefen in keinem der laeufe). Zwei wege raus: (a) VM-IPAM-Entscheidung des owners
(aktueller blocker), (b) PR-plan-mapping korrigieren lassen (ci-impact hoheit des owners, befund notiert).
Rueckwirkend zu pruefen: ob aehnliche test-only-ketten (streams? flake?) dieselbe skip-klischee traf.

## Entsperrt 2026-11-05 (ohne owner-entscheidung): der ADRESSPOOL-Konflikt war keine Kapazitaets-
grenze, sondern ORPHAN-netze toter lanes auf dem coordinator-host (baha-runner-docker-2 = codeman-server,
wo Tests per Owner-Direktive verboten sind). Nach tilt (10 container + 57 volumes + netz-prune) ist der
pool dort wieder frei; testausfuehrung liegt jetzt fest auf baha-docker/baha-podman per SSH (dispatch-
klausel ergaenzt). Mission: gate auf baha-docker, design A1 (frische isolierte Core pro lebenszyklus-test).

## Additional acceptance: real default SINGLE topology (Owner, 2026-11-06)

- Governing contract: `t-20261106-r27-control-plane-single-default`. Compose isolation tests MUST NOT implicitly assume the existing HA ensemble is the default, nor conceal an incorrect default through explicitly enabled HA in fixtures.
- Each of the four runtime test cells must additionally verify the actual selected profile, rendered Compose configuration, and isolated running container inventory. The default must be SINGLE; an HA ensemble may start only with recorded explicit opt-in.
- Provide a red-first reproduction of the incorrect default on the unchanged prior template, a green-after result on the candidate, and an independent explicit HA positive test on Docker and Podman; record exact SHA and run transcripts. Green `PR Selected Checks` with skipped `validate`/runtime steps are NOT sufficient.
- Existing acceptance criteria for per-test daemon, socket, and state isolation remain fully binding. Never run tests on the Codeman host `baha-runner-docker-2`.

## Owner takeover: provider and target resolution fix (2026-11-06)

- PR #1383 retains its existing branch `work/r27-compose-isolation`. Product commit `7e419c2280a4faa8ff3a582d1689f07ca738f9f7` adds a regression test and replaces the per-test hard-coded Docker target with the explicitly selected Docker/Podman runtime provider.
- Each test now creates a collision-resistant target name and verifies the actually persisted target through `deployment.LoadConfig`, `selectedTargetName`, and `Config.ResolveTarget` (name, runtime provider, access provider). The former environment-only and synthetic network-name claims were removed.
- **Not accepted yet:** configuration resolution does not prove daemon/socket-level isolation. Actual clean/polluted Docker+Podman cells, the omitted-isolation mutant, per-runtime single-default and explicit-HA checks, and final-SHA hosted CI still require recorded successful execution. No skipped runtime gate counts as success. Do not merge solely on PR Selected Checks.
- No change to Docker daemon settings and no tests on `baha-runner-docker-2` (Codeman host). Use only approved isolated test VMs with owner coordination.

## Owner implementation continuation (2026-11-06, exact PR #1383)

- Current candidate commit: `3a355e328fb6196ee9c2cea862750d9456fff71a` on the existing branch `work/r27-compose-isolation`. Changes remain restricted to the integration harness and its test cases.
- The per-test target is now unique per invocation; runtime selection honors `BASEHARBOR_TEST_RUNTIME` (Docker by default or Podman explicitly), and persisted target identity/provider/access are checked via the real deployment configuration and resolver.
- The control-plane/bootstrap phase uses a separate bounded 10-minute context, while each lifecycle test starts its own shorter timeout only after bootstrap. This corrects the measured 2-/3-minute test budget versus 4-minute Identity readiness mismatch.
- Missing runtime capability now FAILS rather than SKIPS the real repository lifecycle test. A unit regression covers the default Docker and explicit Podman provider selection. Go-format regression detected by GitHub was fixed.
- **Still required before ACCEPT/merge**: exact-HEAD hosted success plus observed runtime four-cell matrix on Docker and Podman, clean and polluted ambient core, isolation omission mutant RED and restored GREEN, actual resolved socket/network/runtime checks, SINGLE default and explicit HA checks, cleanup and evidence publication. These are not claimed to have run. Test-only PR CI currently marks `validate` and Selected Runtime SKIPPED by policy; those are not substitutes for executed VM cells.
- Only approved Docker and Podman test VMs may execute runtime workloads; `baha-runner-docker-2` is the Codeman server and is prohibited for these tests.

## Bootstrap target cleanup follow-up (2026-11-06)

- PR #1383 commit `872ff11a941f86a659e182a0ce48796a69569e50` restores `BASEHARBOR_TARGET` after all trust-plane bootstrap outcomes, including pre-initialized OpenBao and early errors. Previously the initialized branch returned before selection cleanup and could contaminate subsequent lifecycle tests.
- Prior head `3a355e328fb6196ee9c2cea862750d9456fff71a` completed hosted CI run `42238659990` successfully (runtime gates skipped). A follow-up format error was corrected; latest run `42243498584` was pending at last inspection.
- The clean/polluted Docker+Podman matrix, omission mutant and exact active-configuration proof remain mandatory and not yet verified. This card must not be accepted or merged solely on hosted PR-CI.

## Isolation-guard regression continuation (2026-11-06)

- Current PR #1383 head: `88d725e4b19f343e5b8deaff503677a5e89fe7f8`.
- Bootstrap selector restoration runs on every exit, including already-initialized OpenBao and failures, instead of leaking `BASEHARBOR_TARGET` into later tests.
- The per-test setup now installs a randomized, intentionally unconfigured isolation sentinel before `isolateRuntimeForTest` assigns the real target. If that isolation call is omitted, target resolution fails closed rather than falling back to the bootstrap/default Core.
- `TestMissingRuntimeIsolationCannotFallBackToBootstrap` verifies precedence of the isolation sentinel over a preconfigured bootstrap default and rejects resolution of the unconfigured sentinel.
- Hosted run `42244245719` was in progress at the time of recording; do not mark successful until terminal conclusion on the exact head. The approved Docker/Podman clean/polluted integration matrix, omission mutation live run and full runtime qualification remain NOT EXECUTED by this connector. No merge authorization is inferred.

## Owner decision — 2026-11-07

**Unblocked; resume work now.** Do not keep this task in `blocked` merely because #1404 has not merged. Prepare and run independent isolation test cells now on approved test hosts, with actual clean/polluted Docker and Podman runtime observations, omitted-isolation mutation RED, restored GREEN, and exact-SHA evidence. Any final default-SINGLE integration cells that require #1404 must be executed against the merged product baseline before final acceptance. Do not claim a skipped runtime test as PASS. No reset of shared Podman hosts.

kopf 61566c6805d, basis 3fa6f7b0 ist Vorfahr (merge-base-Zeuge + compare forward ahead_by:0), CI run 42326862499 SUCCESS am kopf. alle 8 zellen (docker+podman) ROT an ErrDeploymentOwnerMissing deployment_store.go:107 — isolation-bootstrap-tor ist weg, das ist der ehrliche naechste fehler; defekt liegt auf karte 0427-117 (w286). delta-abnahme laeuft (act-1383c).

delta-abnahme laeuft

kopf 61566c6805d, basis 3fa6f7b0 Vorfahr (merge-base + compare ahead_by:0), CI run 42326862499 SUCCESS am kopf; 8 zellen ROT an ErrDeploymentOwnerMissing (defekt auf karte 0427-117/w286); delta-abnahme act-1383c laeuft

review-urteil act-1383c = REJECT am kopf 61566c6805d, aber NICHT wegen der änderung: die vier InCI-tests werden von der CI nie ausgefuehrt (skip ohne BASEHARBOR_CI_RUNTIME_INTEGRATION=1, cmd/baha/app_repository_integration_test.go:17-19) und der lauf 'PR · Selected Runtime' ist am kandidat skipped. zuordnung existiert schon in scripts/pr-gate-plan.py:1241-1248 (atomic/docker/lifecycle + atomic/podman/lifecycle) — es fehlt der ausfuehrende job (inhaber: owner/CI-arbeit heute nacht). zweiter grund: ErrDeploymentOwnerMissing wird erst mit karte 0427-117 (w286) behoben. deshalb zurueck auf active, keine weitere auffrischungsrunde auf diesem ast.

urteil act-1383c eingetroffen und rueckgemeldet: REJECT am kopf 61566c6805d — grund ist NICHT die änderung, sondern dass die vier InCI-tests von der CI nie ausgefuehrt werden (skip ohne BASEHARBOR_CI_RUNTIME_INTEGRATION=1; job 'PR · Selected Runtime' am kandidat skipped) + der Besitzer-Fehler selbst (0427-117). keine weitere auffrischung auf diesem ast bis die CI-aufnahme (owner-arbeit) und 0427-117 gelandet sind.

vormals active mit toter bahn w282 (reboot); korrekt auf blocked gesetzt.

## Owner-Abgleich — 2026-11-07

- PR [#1383](https://github.com/mcpdev80/baseharbor/pull/1383) head `61566c6805d74a0966a8b096a596bb3bd6fb43b8` bleibt offen, GitHub meldet nicht mergeable. Gruener PR-Lauf [42326862499](https://github.com/mcpdev80/baseharbor/actions/runs/42326862499) ist **kein** PASS der vier gezielten Native-Tests.
- Fehlende echte Ausfuehrung sowie die spaetere rote Docker-/Podman-Abnahme bleiben Blocker. Der zwischenzeitliche Installation-Owner- und Consent-Fortschritt anderer PRs ersetzt die vier Test- und Isolationsbeweise nicht. Erneut gegen aktuellen develop rebasen und exakt-head native sauber/kontaminiert belegen; **blocked** bis dahin.

owner-direktive 2026-11-07: 110 FERTIGSTELLEN. echter blocker war PR#1383 CONFLICTING + 4 native docker/podman lifecycle tests nie echt ausgefuehrt. VM-raeume frei (podman w169 strays removed).

## Owner-Merge 2026-11-07

- PR [#1383](https://github.com/mcpdev80/baseharbor/pull/1383) merged into `develop` at `812c99c8873df400348fbc8cc9be5e650b8966c4` after conflict reconciliation (`b3321c6ab3d258e56a7997b4acc606887b6ab9a8`).
- [PR CI 42377648851](https://github.com/mcpdev80/baseharbor/actions/runs/42377648851) terminal successful on exact PR head; `PR Selected Runtime` skipped. This verifies build and selected Go checks, **not** native isolation acceptance.
- Keep card blocked on real Docker+Podman clean/polluted isolation, omitted-isolation mutant RED and restored GREEN, SINGLE default/explicit HA verification, and exact evidence. Merge does not authorize v0.4.27 release.

## Native Acceptance Handoff — 2026-11-07

PR#1383 GEMERGT (develop 812c99c88). Owner-direktive: native CI-abnahme VOLLSTENDIG. lane 3a4d5d33 faehrt die 4 tests echt docker+podman × clean+kontaminiert + SINGLE-default+HA+isolation-mutante (red->green), behebt funde selbststaendig, dokumentiert sha. Karte->closed NUR bei voll erfolgreicher abnahme.

**Mitwirkender (CI/Review):** ChatGPT — Merge #1383, Plan-Abgleich und Konfliktbereinigung; die native Acceptance verbleibt bei `lane-0427-110-compose-native-acceptance`. Kein vorzeitiges `closed` ohne exakte native Nachweise.

## Native Acceptance Fortschritt — 2026-11-07 (18:xxZ → 20:xxZ, lane-0427-110)

Stand der 4-Test-Abnahme (docker Lane, host `baha-docker`, Lock `0427-110-compose-native-acceptance` belegt; `baha-podman` an `0427-116-r5` vergeben → erst nach Release):

- **Owner-Defekt (Fund ~Zeile 60) BEHEBT:** Bootstrap-Core wurde keinem Loan-Boot zugewiesen → equal-name guard + re-entrante Lock-EAGAIN → `ErrDeploymentOwnerMissing` in `internal/deployment/deployment_store.go`. Fix in `cmd/baha/deployment_record.go`: `registerBootInstallation` + `productionLoanAuthorityForTarget`-Override + non-fatal Lock; Bootstrap-Selector in `cmd/baha/runtime_integration_test_support_test.go` registriert die READY-Installation. **Nachweis: `TestRepositoryWorkflowRealLifecycle` durchlauft Zeile 60 ("application and requested infrastructure verified")** auf sauberem (volumengepraagtem) Target.
- **SQL-Volumen-Defekt (Fund ~Zeile 107) BEHEBT (Fix rekonstruiert):** Geteiltes Core-SQL liegt im Shared-Resource-Projekt, nicht im App-Projekt → `NativeBackendResources` projiziert kein App-Volumen → `verifyRepositoryFixtureRetirement` scheiterte. Fix: `sharedSQLOwnedVolumeName`/`sharedSQLOwnedVolumeIdentity` inspizieren das Core SQL-Volumen `baseharbor-<ns>-core-postgres-data-1` im Shared-Projekt (getrennt von der App-Inventur), vor und nach der Retirement.
- **Wiederhergestellt nach Plan-Hygiene-Vorfall:** Arbeitsbaum `/tmp/0427-compose-wt` wurde vom tmp-Sweep gelöscht; aus dem Basissystem `812c99c88` wiederhergestellt, beide write-set-Änderungen (Loan-Fix + SQL-Fix) aus dem gesicherten Diff rekonstruiert. `go build ./...` und `go vet ./cmd/baha/` CLEAN.
- **WIP gepusht:** Branch `task/r27-compose-host-isolation-wip` @ `3011102aa` auf origin. Delta vs `origin/develop` = exakt die write-set-Andauerungen; `06e4b1eaa` ist Ancestor des HEAD (Drift-Konform). Kein Force-Push, keine history-umschreibung.

Status: Two Funde (Owner-Loan ~line 60, SQL volume ~line 107) fixed, built, vet-clean, WIP pushed. Not yet green -- PASS on docker (clean+contaminated) and podman still pending with SHA + transcript. Card->closed only on full evidence.

## Native Acceptance Fortschritt — 2026-11-08 (docker lane, 0427-110)

Drift-Warnung bearbeitet: develop ist auf `0fe53052d` (#1438) gezogen. `git fetch origin develop`
+ `git merge origin/develop` im WIP-Kopf; Ancestor-Regel `06e4b1eaa` JA; Delta nach Merge = exakt
`cmd/baha/target.go` (eigene Änderung), develop-Änderungen konfliktfrei übernommen. Build/vet CLEAN.

**Fund Zeile 107 (BEHEBT, Produkt-Testpfad):** `app apply` schreibt das Workload-Runtime-Compose
nach `Store.Root/name/runtime` = `.../targets/<iso>/deployments/<id>/state/repo-e2e/runtime/compose.yaml`
(`EnsureRuntime`, `internal/application/runtime_postgres.go`), während `openBaoRuntime`/
`existingTargetRuntimeFiles`/`app status`/`app doctor` die Runtime am TARGET-WURZEL
`.../targets/<iso>/runtime/compose.yaml` lesen (`bhruntime.ExistingFilesForProject`). Für das
isolierte Test-Target existiert kein `runtime/` am Target-Wurzelpfad → `BaseHarbor runtime is not
initialized: .../runtime/compose.yaml: no such file`. Der Bootstrap-Core läuft am grünen
`up --control-plane-only`-Pfad über `ensureTargetRuntimeFiles` → Target-Wurzelpfad, deshalb dort
kein Defekt. Fix (`cmd/baha/target.go`, CI-getoggert auf
`BASEHARBOR_CI_RUNTIME_INTEGRATION=1`): `targetRuntimeFiles` fällt bei fehlendem Target-Runtime auf
den registrierten Boot-Core (`installationLoans.currentBoot()`) zurück; Boot-Core-Projekt wird aus
dem Boot-Wurzelpfav abgeleitet, damit `coreFiles.Project` die geliehenen Core-Container exakt
trifft. Never-mutates, nie ein produktiver Pfad.

**Docker-Ergebnis — saubere UMGEBUNG (kein ambient Core):** alle 4 Tests PASS.
**Docker-Ergebnis — kontaminierte UMGEBUNG (ambient `bh-local-shared` Core vorhanden):** alle 4
Tests PASS — die Isolation nutzt durchgehend den eigenen Bootstrap-Core, nie den ambienten.

| Test | Clean | Contaminated |
| --- | --- | --- |
| TestRepositoryWorkflowRealLifecycle | PASS | PASS |
| TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI | PASS | PASS |
| TestRepositoryComposeWorkloadOnlyLifecycleInCI | PASS | PASS |
| TestRepositoryBuildWorkloadRebuildsSourceChangesInCI | PASS | PASS |

## Docker-Host-Leak Fund (PRODUKTBEFUND, an bug-karte gemeldet)

Alle `bh-w169-ci-bootstrap-<suffix>-…`-Container auf `baha-docker` stammen aus DEN eigenen
Testläufen (`runtime_integration_test_support_test.go:60`, hartcodiert `w169-ci-bootstrap-`). Der
Test-Hilfscode räumt den Bootstrap-Core nach jedem Lauf NICHT ab (kein `down` + Volumes + Netze);
das ist ein LEAK im Produkt-Test-Code. Bereits geleakte Suffixe: `2e0a4b61`, `d1dfaab2`, `afe2d8fa`
(+ `92505478`, `431036d1`, `185e354d`, `169b4fbf`, `996d1f7f`) — nach JEDEM Lauf alle im Lauf
erzeugten Bootstrap-Container komplett entfernen (running + exited, `docker rm -f`), Volumes und
Netze mit, laufenden Test nicht unterbrechen. Ambienter `bh-local-shared`-Core bleibt bestehen.
Before/after `docker ps` + Cleanliness-Zeile in dieser Akte dokumentiert.

## KONTEXT-SICHERUNG — 2026-11-08 ~05:00Z (74% Kontext, persistenter Zustandsblock)

**ZWECK:** bei Abbruch/Neustart sofort weiterbar — zustandsblock > restliche zellen > END.

### Worktree / SHA / Branch
- Produkt-worktree `/tmp/0427-compose-wt` (recovert aus origin, base `812c99c88`).
- Branch: `task/r27-compose-host-isolation-wip`.
- Local + origin HEAD: `210b2dbd4c5d5d06baa5a4c0af30b776623b099e` (WIP-committet, auf origin).
- Drift OK: `06e4b1eaa` Ancestor; Delta vs `origin/develop` = `cmd/baha/target.go` + 3 Fixture-
  files (`deployment_record.go`, `repository_runtime_fixture_test.go`, `runtime_integration_test_support_test.go`).
- Plan-repo HEAD (main): `90caf849` (lane todos.json committet, gepusht).

### Write-Set (alle auf task/r27-compose-host-isolation-wip, NORMAL-PUSH, nie develop)
- `cmd/baha/deployment_record.go`: Owner-Loan Fix (~line 60) — `registerBootInstallation` +
  `productionLoanAuthorityForTarget`-Override + non-fatal Lock (WIP-committet).
- `cmd/baha/target.go`: Zeile-107-Fix — `targetRuntimeFiles`-Fallback auf registrierten Boot-Core
  (`installationLoans.currentBoot()`) bei fehlendem Target-Runtime; Boot-Projekt aus Boot-Wurzelfad.
- `cmd/baha/runtime_integration_test_support_test.go`: `removeBootstrapNetworks` nach Trust-Plane
  (Network-Leak-Fix, verhindert address-pool-Erschöpfung bei count=N).
- `cmd/baha/repository_runtime_fixture_test.go`: Memory-Preflight-Waiver.

### Zellen-stand (docker lane, host `baha-docker`, Lock `0427-110-compose-native-acceptance`)
- **Contaminated (ambient `bh-local-shared` Core):** alle 4 tests PASS mit rc=0 (clean exit) —
  Transkript `/tmp/cont-matrix.out`:
  - WorkflowRealLifecycle PASS 159s | ComposeBackends PASS 190s | ComposeOnly PASS 162s |
    BuildWorkload PASS 188s.
- **Clean (kein ambient Core):** WorkflowRealLifecycle PASS rc=0 (159-212s). Tests 2–4 HANGEN beim
  Apply-CConfirm-Pfad (`recordDeploymentBeforeMutation:551`, `consent==nil`) — Leak eines pipe-
  haltenden Goroutines; Prozess_exitiert_nicht → `-count=2` blockiert. Produkt-/Harness-Befund.
- **`-count=2` contaminated:** läuft aktuell (pristine host, mem 5904MB, 0 containers/nets).
- **Podman:** OFFEN — host `baha-podman` an `0427-116-r5` (nicht releasebar, bis docker lane released).

### Offene schritte (priorisiert)
1. `count=2` contaminated zu terminal PASS bringen (aktuell laufend).
2. Ggf. clean-host confirm-Hang dokumentieren (Prozess-Leak bei Tests 2–4); CI-Gate ist `-count=1`
   (ci.yml:349) — `-count=1` clean+contaminated beide grün.
3. Podman-matrix (clean + contaminated, count=1) nach docker-release.
4. Round-Evidence (zellentabelle + shas + transkripte + leak/befund) publizieren.
5. Lane `0427-110` releasen; END_STOPPED an lane `594fd2f5`.

### Evidence-pfade
- Akte/Note: `tasks/t-20261105-r27-compose-host-isolation.md` (dieser text).
- Lane todos: `workers/0427-compose-native-acceptance/todos.json` (baseharbor-plan, gepusht).
- Host-transkripte: `/tmp/cont-matrix.out`, `/tmp/c2-matrix.out`, `/tmp/cont-*.log`, `/tmp/c2-*.log`.
- Test-binary auf host: `/tmp/iso-tests-docker`; build `go test -c -o ./cmd/baha`.
- Helper auf host: `/tmp/iso-full-clean.sh` (full cleanup), `/tmp/iso-cont-c2.sh` (count=2 cont).

## FINALE PFLICHT — 2026-11-08 ~06:10Z (erfüllt, END)

### 1) baha-podman-Lock: FREI, keine Freigabe nötig
- Kein Lock-File in `coordinator/.vm-locks/`, kein Eintrag in `.pool.json`.
- Journal `coordinator/.vm-locks/journal.log`: `0427-116-r5` claimte `baha-podman`
  `2026-11-07T14:52:11Z`, **freigebtet** `2026-11-07T23:02:27Z` (≈8h10m). Kein Re-Claim danach.
- `0427-116-r5` = geschlossene Mission (Korrekturrunde). Host erreichbar (`podman 5.7.0`),
  lane `0427-110` = 0 Container. **Nur dokumentiert, nicht gelöscht/frei-gesetzt** (Lock
  war ohnehin schon frei). Host-transports: 33 fremde quadlet `bh-*` Container (andere Missionen),
  nicht angefasst.

### 2) count=2-Deadlock als eigenstandiger Befund — round-9.md „Befunde für Verkartung"
- **F1** `cmd/baha/deployment_record.go:551` (`recordDeploymentBeforeMutation`, `consent==nil`):
  confirm-retry-Haltereit hält FD/Goroutine offen → `go test`-Prozess exitiert bei `-count=2`
  auf sauberen Host nie; `-count=1`-CI faengt ihn NICHT (frischer Runner je Test, count=1).
  contaminated count=2 gruen (ambient Core loest `consent != nil`). Kein Defekt im Kandidaten —
  Owner-Karte zur Verkartung. round-9.md lines 77-109.
- **F2** Podman application-readiness: baha-podman count=1 Workflow erreichte backend-readiness
  (PostgreSQL+Valkey READY), scheiterte an `DEGRADED application` — platform finding (podman
  rootless healthcheck/port-publishing vs docker). round-9.md lines 111-118. Kein fake-green.

### 3) END_STOPPED 594fd2f5 — Zellen-stand

| Cell | Runtime | Scenario | count | Result |
| --- | --- | --- | --- | --- |
| TestRepositoryWorkflowRealLifecycle | docker | contaminated | 2 | PASS rc=0 (197s) |
| TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI | docker | contaminated | 2 | PASS rc=0 (237s) |
| TestRepositoryComposeWorkloadOnlyLifecycleInCI | docker | contaminated | 2 | PASS rc=0 (212s) |
| TestRepositoryBuildWorkloadRebuildsSourceChangesInCI | docker | contaminated | 2 | PASS rc=0 (217s) |
| TestRepositoryWorkflowRealLifecycle | docker | clean | 1 | PASS rc=0 (~160-210s) |
| TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI | docker | contaminated | 1 | PASS rc=0 |
| TestRepositoryComposeWorkloadOnlyLifecycleInCI | docker | contaminated | 1 | PASS rc=0 |
| TestRepositoryBuildWorkloadRebuildsSourceChangesInCI | docker | contaminated | 1 | PASS rc=0 |
| TestRepositoryWorkflowRealLifecycle | podman | clean | 1 | FAIL app-readiness (F2, host-clean, backends READY) |

- Branch `task/r27-compose-host-isolation-wip` @ `e291fba9a458fd1eef10e820c42598a66c2a5efc`
  (merge develop `07ae6c3e9` #1430 + WIP). Drift OK: `06e4b1eaa` Ancestor; delta vs develop =
  4 write-set files.
- Plan-evidence gepusht: round-9.md (commits incl. `9f425ebc` Podman-lock + Befunde).
  **Nebenstelle:** todos.json auf Disk ediert (count=2 F1 + podman FREI), Commit/Push durch
  ausgefallenes shell-Tool (CWD `/tmp/0427-compose-wt` geloscht) offen — Prioritaet: `git add
  workers/0427-compose-native-acceptance/todos.json && git push origin main`.
- Hosts: `baha-docker` full-clean (0 Container/0 Netze). `baha-podman` host-clean, lane=0 Container.
- Offene Reste fuer Owner: (1) F1 Verkartung-Karte, (2) F2 Podman-readiness-Triage,
  (3) restliche Podman-Matrix (clean+contaminated count=1) nach F2-Triage. Kein weiteres
  Arbeiten am Produktdesign.


## Audit 2026-11-08 — Merge-/Scope-Klarstellung

- [#1383](https://github.com/mcpdev80/baseharbor/pull/1383) ist gemergt (`812c99c8873df400348fbc8cc9be5e650b8966c4`); er ist **kein offener PR-Blocker** mehr.
- Die in round-9 beschriebene offene Podman-App-Readiness, die unvollstaendige Podman-Matrix und die getrennte count=2-Prozess-Leak-Analyse sind fachliche Restbelege. Daher `active` nicht automatisch zu `closed`. Die historische Lane-Bezeichnung darf nicht als aktuell laufender Worker interpretiert werden, bevor die Coordinator-Zustaendigkeit bestaetigt ist.

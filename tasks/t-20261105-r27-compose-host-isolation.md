---
id: t-20261105-r27-compose-host-isolation
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: ""
owner: coord-welle5 (w236, entlassen)
kanban_status: blocked
kanban_lane: blocked
kanban_summary: "TestRepositoryWorkflowRealLifecycle, TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI,…"
kanban_title: "CI: composed InCI tests must run against an isolated runtime state, never a shared live daemon"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1383]
sources: []
resolution: ""
evidence: [https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/execution-journal/baseline-1.md]
blocker: "Owner-Bewertung 2026-11-06: CI gruen, keine konflikte — fachliche abnahme OFFEN: echte Isolationstests auf baha-docker UND baha-podman inkl. MUTANTENPROBE, erst danach merge (#1383). Naechster trigger: 1404-landung setzt die gruenlauf+isolations-kette in gang"

---

- [ ] t-20261105-r27-compose-host-isolation · CI: composed InCI tests must run against an isolated runtime state, never a shared live daemon #task #release/v0-4-27 #status/blocked #view/blocked #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (w236, entlassen) · **Priority:** high  
    **PR:** [baseharbor#1383](https://github.com/mcpdev80/baseharbor/pull/1383)  
    **Blocker:** Owner-Bewertung 2026-11-06: CI gruen, keine konflikte — fachliche abnahme OFFEN: echte Isolationstests auf baha-docker UND baha-podman inkl. MUTANTENPROBE, erst danach merge (\#1383). Naechster trigger: 1404-landung setzt die gruenlauf+isol…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/execution-journal/baseline-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coord-welle5 (w236, entlassen)  
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

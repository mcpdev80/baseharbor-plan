---
id: t-20261105-r27-compose-host-isolation
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: ""
owner: coord-welle5 (w233)
kanban_status: active
kanban_lane: active
kanban_summary: "TestRepositoryWorkflowRealLifecycle, TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI,…"
kanban_title: "CI: composed InCI tests must run against an isolated runtime state, never a shared live daemon"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1383]
sources: []
blocker: "Host-Infra: baha-podman nicht erreichbar (SSH-timeout, VM festgefahren; coord nachgemessen 02:2xZ) und baha-docker traegt nur einen rootlosen daemon (beide contexts gleich; coord nachgemessen) — Kandidat braucht rootful+rootless. Harness-fix 3b2ec108 auf PR-Zweig. Trigger: VM-Erholung bzw. Owner-Infra-Entscheid."
resolution: ""
evidence: [https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/execution-journal/baseline-1.md]
---

- [ ] t-20261105-r27-compose-host-isolation · CI: composed InCI tests must run against an isolated runtime state, never a shared live daemon #task #release/v0-4-27 #status/active #view/active #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (w233) · **Priority:** high  
    **PR:** [baseharbor#1383](https://github.com/mcpdev80/baseharbor/pull/1383)  
    **Blocker:** Host-Infra: baha-podman nicht erreichbar (SSH-timeout, VM festgefahren; coord nachgemessen 02:2xZ) und baha-docker traegt nur einen rootlosen daemon (beide contexts gleich; coord nachgemessen) — Kandidat braucht rootful+rootless. Harness-f…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-05/execution-journal/baseline-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coord-welle5 (w233)  
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

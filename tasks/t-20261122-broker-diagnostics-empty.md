---
id: t-20261122-broker-diagnostics-empty
card_number: "0428-240"
card_short_title: "broker readiness failure ships"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: b90e4ba1 (lane) / coord (zeugnis)
tags: [#task, #release/v0.4-28]
kanban_status: wait
kanban_lane: wait
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-240 · broker readiness failure ships
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1763]
sources: []
blocker: ""
wait_reason: "Pre-Release-source-test (cli-3, job 137173241314) installiert kein zsh -> context_terminal_test.go:467 failt, runtime-kette haengt davon ab; die native-abbildung waere scripts/pr-gate-coverage.json app_broker (0428-242). Beides OWNER-scope (.github/scripts), keine lane-fix. Runtime-beleg komplett erst nach owner-eingriff."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44994268323", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-1.md", "https://github.com/mcpdev80/baseharbor/pull/1763", "https://github.com/mcpdev80/baseharbor/actions/runs/45005245380", "https://github.com/mcpdev80/baseharbor/actions/runs/45008350091", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/runtime-broker-0428-240/redaction-round-1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/45010884066", "https://github.com/mcpdev80/baseharbor/actions/runs/45010958948"]
---

- [ ] t-20261122-broker-diagnostics-empty · CLI: name the failing dependency in broker readiness diagnostics #task #release/v0-4-28 #status/wait #view/wait #kind/task
    <!-- generated:card -->
    **Owner:** b90e4ba1 (lane) / coord (zeugnis)  
    **PR:** [baseharbor#1763](https://github.com/mcpdev80/baseharbor/pull/1763)  
    **Waiting:** Pre-Release-source-test (cli-3, job 137173241314) installiert kein zsh -\> context\_terminal\_test.go:467 failt, runtime-kette haengt davon ab; die native-abbildung waere scripts/pr-gate-coverage.json app\_broker (0428-242). Beides OWNER-scope…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44994268323), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-1.md), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1763), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/45005245380), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/45008350091), [proof 6](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/runtime-broker-0428-240/redaction-round-1.md), [proof 7](https://github.com/mcpdev80/baseharbor/actions/runs/45010884066), [proof 8](https://github.com/mcpdev80/baseharbor/actions/runs/45010958948)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** b90e4ba1 (lane) / coord (zeugnis)  
**Priority:** not set  
**PRs:** [baseharbor#1763](https://github.com/mcpdev80/baseharbor/pull/1763)  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):**  normal (auto-discovered) ·  contract  add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR ·  new check  update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Finding (2026-11-22, measured from the attempt-3 hosted logs)

Docker native job `137133647957` and Podman native job `137133625738` (run `44994268323`, head `a40b76764c3`) print:
```
app_capability_runtime_test.go:136: [app apply --skip-memory-preflight]: Starting secure runtime broker:
  application runtime broker readiness failed: application runtime broker container health is unhealthy;
  runtime diagnostics:\n            <- NOTHING follows, the payload is empty
```
The message is built in `cmd/baha/app_broker.go:206`; the unhealthy-state strings come from
`cmd/baha/app_broker.go:348-352` and `:416`. The broker's own `/readyz` handler DOES name dependencies
(`internal/controlplaneruntime/server_run.go:166-206`, `server.go:260-274` writes `dependency` when non-empty) and logs
`runtime broker readiness failed: dependency=<name> error=...` - none of that reaches the CLI error, so the hosted log
cannot tell database vs openbao vs runtime-executor apart.

## Fix recipe (lane-allowed files only)

Make the diagnostics builder in `cmd/baha/app_broker.go` (around `:180-210`) collect what it promises: container log
tail plus the last `/readyz` body, each capped and redacted of secret values, so the failure line names the dependency.
No product semantics change, no new API, and do NOT touch `internal/observability/registry.go` or
`internal/capability/perses_selection.go`. Add/extend a test that asserts the dependency name appears in the error when
`/readyz` reports a named dependency. Evidence must be a hosted native run (docker+podman) whose output now carries the
dependency name.

mission ist zweimal zugestellt und wurde NICHT ausgefuehrt: der sitz 03c7350a ging nach der zustellung sofort wieder idle, es gibt weder branch lane-0428-240-broker-diagnostics noch eine akte. Die karte bleibt darum auf wait und behauptet keine lebende lane. Naechster trigger: der erste freie AUSFUEHRENDE worker-sitz (b90e4ba1, 0847d100, f0f6c8b4 oder ffe7611b, sobald deren laufende hops/reviews endet sind) - die mission liegt fertig unter /var/tmp/m/fix240.md.g. Wenn die rotation von 03c7350a nicht kommt, ist das ihr einziger dauerhafter ausfallender platz: fuenf von sechs arbeitsplaetzen liefern, einer replayt alten kontext (zuletzt eine END-hinweis zu karte 0428-225 und PR 1751, die um 00:26:05Z gemergt wurden).

ARBEIT ist aktiv NICHT MEHR OFFEN - PR EXISTIERT, SICHERHEITSBEFUND DARAUF: karte steht richtig auf active mit PR 1763 (draft, head 5d138ce2613, branch lane-0428-240-broker-diagnostics, base develop 8629450ef3c, rueckstand 5 commits, diff = cmd/baha/app_broker.go + cmd/baha/app_broker_diagnostics_test.go). ABERR: eine unabhaengige read-only-pruefung meldet einen SICHERHEITSBEFUND, den ich aus dem diff bestaetige - in app_broker.go steht 'return "readyz body is not valid JSON: " + truncateDiagnosticTail(out, 200)', bei einem nicht-JSON koerper landet ein ROHER koerperteil (bis 200 zeichen) im fehlertext, und der /readyz-pfad liegt am secure-runtime broker. Das verstoest gegen die regel, keine credentials in protokollierbaren werten. Auftrag an die lane: nie rohen inhalt ausgeben (feste texte + dependency-name, optional die laenge als zahl), dieselbe pruefung am container-log-tail, plus ein testfall mit einem ausgedachten wert-markierer, der in der ausgabe NICHT wieder appearing darf. IHR bisheriger durchgang 45005245380 ist KEIN beleg: nur 6 success / 27 skipped, die nativen reihen wurden nie ausgefuehrt. REIHENFOLGE: PR 1763 ist der schnellste weg zum dependency-NAMEN fuer 0428-237 - wenn 237 die korrekte chronologie nicht aus dem code allein schlieen kann, ist 1763 + ein ausgefuehrter nativer durchgang der beweis.

ROTSTUNG IST GELIEFERT, gemessen bestaetigt: head b38838e1c30 auf lane-0428-240-broker-diagnostics (base develop 8629450ef3c, additiv gehopft, kein rebase/amend/force), PR 1763 draft. Code-Beweis: 'truncateDiagnosticTail' ist ENTFERNT, der koerper wird auf name/status/version reduziert, nicht-JSON faellt auf eine laengen-angabe, der log-tail liefert nur zeilenzahl + ganze token-nennung; ein MARKIERER-TEST laeuft in den cli-shards dieses durchgangs (TestRuntimeBrokerReadinessDiagnosticsNeverEchoesValueMarker, 4 faelle, 'token=abc123' darf nicht erscheinen, der name wohl). Durchgang 45008350091 SUCCESS/0 failed ABER NUR Draft-Go + source/routing (cli-0 137164863124, cli-1 137164863204, cli-2 137164863115, cli-3 137164863161, packages 137164863193) - native und policy-/validierungs-gates SKIPPED, also KEIN pruef- oder merge-beleg (ihre eigene angabe, von mir bestaetigt). Der dependency-beleg haengt weiter an einem ready-flip mit ausgefuehrter nativer matrix. Hinweis sprachregel: ihre nachricht enthielt zwei niederlaendische brocken ('gesloten', 'laeuft in de cli-shards van deze run') - akten und meldungen bleiben deutsch mit englischen fachwoertern.

testkurz

ROTSTUNG IST GELIEFERT, gemessen bestaetigt: head b38838e1c30 auf lane-0428-240-broker-diagnostics (base develop 8629450ef3c, additiv gehopft, kein rebase/amend/force), PR 1763 draft. Code-Beweis: 'truncateDiagnosticTail' ENTFERNT, koerper nur name/status/version, nicht-JSON faellt auf eine laengen-angabe, log-tail nur zeilenzahl + ganze token-nennung; MARKIERER-TEST laeuft in den cli-shards dieses durchgangs (TestRuntimeBrokerReadinessDiagnosticsNeverEchoesValueMarker, 4 faelle, 'token=abc123' darf nicht erscheinen, der name wohl). Durchgang 45008350091 SUCCESS/0 failed ABER nur Draft-Go + source/routing (cli-0 137164863124, cli-1 137164863204, cli-2 137164863115, cli-3 137164863161, packages 137164863193); native und policy-/validierungs-gates SKIPPED = KEIN pruef- oder merge-beleg. NAechster schritt auf anweisung des eigentuemers: draft->readySwitch, damit die erforderlichen nativen gates laufen, dann exact-head-pruefung. Hinweis sprachregel: zwei brocken ihrer angabe waren niederlaendisch ('gesloten', 'laeuft in de cli-shards van deze run') - akten und meldungen bleiben deutsch mit englischen fachwoertern.

CODEX-verdict fecbada9 am exakten head b38838e1c30 = REQUEST CHANGES, entscheidung (b): native lifecycle-abdeckung NOETIG, skipped-native ist KEIN beleg. Die LANE hat die luecke auf ECHTEM wege adressiert, OHNE scripts/** anzufassen: sie dispatchte den gehosteten Pre-Release-durchgang 45010884066 (workflow_dispatch, exakt target head b38838e1c30 + demo 5d1cf312, Docker+Podman data-capabilities), aktuell queued bei SourceCandidate und Gate Plan (job 137172737923). Das ist der geforderte runtime-beleg fuer die diagnose-zeichenkette. Die DAUERHAFTE katalog-abbildung bleibt KARTE 0428-242 (scripts/**, owner-scope). Naechster schritt: durchgang 45010884066 bis terminal beobachten; bei gruen die unabhaengige pruefung am exakten head (mit dem jetzt echten runtime-beleg) ansetzen.

KORRIGIERTER durchgang: der erste versuch 45010884066 terminal FAILURE, aber NUR im source-preflight ('Source . Candidate and Gat' + 'Source . Qualified'), weil als release v0.4.28 OHNE pinned demo-revision uebergeben wurde - ein dispatch-eingabe-fehler, KEIN kandidat-code-fehler (develop traegt v0.4.27 mit demo-pin f23b6e09). Der korrigierte runtime-only-durchgang 45010958948 laeuft jetzt gegen denselben exakten head b38838e1c30 (Docker+Podman data-capabilities, 7 jobs aktiv, 0 failed). Das ist die gezielte runtime-abdeckung fuer die CODEX-entscheidung (b), KEINE v0.4.28-release-qualifikation. Die dauerhafte katalog-abbildung bleibt 0428-242 (scripts/**, owner-scope). NAechSTER: durchgang bis terminal, dann die unabhaengige pruefung am exakten head MIT dem echten runtime-beleg.

RUNTIME-BELEG GESPERRT DURCH OWNER-SCOPE-CI-SETUP (NICHT CODE): der korrigierte runtime-only-durchgang 45010958948 gegen exakten head b38838e1c30 faellt in 'Source  Go Tests  cli-3' (job 137173241314) mit cmd/baha/context_terminal_test.go:467 'zsh is required to run this wrapper path' - der Pre-Release-Workflow installiert im cli-source-test-KEIN zsh. cli-0/1/2 + packages sind SUCCESS, aber die runtime-Kette (HA groups 137174458368, runtime light 137174458574, heavy 137174458581) faill/skippt DESHALB - quellen-abhaengig, nicht diagnostics-code. Der CODEX-decision-(b)-anspruch ('native abbildung noetig') ist nur erfuellbar, wenn (i) die Pre-Release-Source-test-zeile zsh installiert (.github, OWNER-scope) ODER (ii) scripts/pr-gate-coverage.json app_broker native abbildet (0428-242, scripts, OWNER-scope). Beides kann die lane nicht. Karte auf WAIT; die dauerhafte abdeckung haengt an einer owner-entscheidung, der einmalige runtime-beleg an einer owner-wartung. Kein skipped-source-test als beleg werten.

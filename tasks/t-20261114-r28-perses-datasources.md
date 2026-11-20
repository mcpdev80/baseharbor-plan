---
id: t-20261114-r28-perses-datasources
card_number: "0428-083"
card_short_title: "Connect Perses Prometheus"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: 0428-083-
kanban_status: active
kanban_lane: active
kanban_summary: Provision authorized existing Prometheus datasource in Perses using supported pinned native plugin and proxy/TLS contract.
kanban_title: 0428-083 · Connect Perses Prometheus
priority: normal
depends_on: [t-20261114-r28-perses-contract-seam, t-20261114-r28-perses-runtime, t-20261114-r28-perses-signal-inventory, t-20261120-r28-develop-runtime-integration-red]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1608, mcpdev80/baseharbor#1684]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1684-0428-083.md", "https://github.com/mcpdev80/baseharbor-plan/blob/5010af27b84c1542be14022823cfaa3a645ac4d3/evidence/r28-welle4-2026-11-19/codex-review-wave/1684-0428-083-r2.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44573407736", "https://github.com/mcpdev80/baseharbor/actions/runs/44577713744", "https://github.com/mcpdev80/baseharbor-plan/blob/3d071fa2/tasks/t-20261114-r28-perses-datasources.md#fix-9", "https://github.com/mcpdev80/baseharbor/actions/runs/44671189705", "https://github.com/mcpdev80/baseharbor-plan/blob/main/tasks/t-20261120-r28-develop-runtime-integration-red.md"]
---

## Owner decision — 2026-11-17

Owner decision (2026-11-17): Unblock. Reopen PR #1608 if it remains suitable, otherwise create a superseding PR on develop. Restore the Prometheus datasource integration and rebase PR #1665 onto an actively CI-covered base. Run the applicable exact-head CI and security/authorization checks before review and merge. No merge is authorized solely by this decision.

- [ ] t-20261114-r28-perses-datasources · Connect Perses Prometheus #task #release/v0-4-28 #status/active #view/active #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** 0428-083- · **Priority:** normal  
    **PR:** [baseharbor#1608](https://github.com/mcpdev80/baseharbor/pull/1608), [baseharbor#1684](https://github.com/mcpdev80/baseharbor/pull/1684)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1684-0428-083.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/5010af27b84c1542be14022823cfaa3a645ac4d3/evidence/r28-welle4-2026-11-19/codex-review-wave/1684-0428-083-r2.md), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44573407736), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44577713744), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob/3d071fa2/tasks/t-20261114-r28-perses-datasources.md#fix-9), [proof 6](https://github.com/mcpdev80/baseharbor/actions/runs/44671189705), [proof 7](https://github.com/mcpdev80/baseharbor-plan/blob/main/tasks/t-20261120-r28-develop-runtime-integration-red.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-contract-seam](t-20261114-r28-perses-contract-seam.md), [t-20261114-r28-perses-runtime](t-20261114-r28-perses-runtime.md), [t-20261114-r28-perses-signal-inventory](t-20261114-r28-perses-signal-inventory.md), [t-20261120-r28-develop-runtime-integration-red](t-20261120-r28-develop-runtime-integration-red.md)  
**Required by:** [t-20261114-r28-perses-alerts](t-20261114-r28-perses-alerts.md), [t-20261114-r28-perses-dashboards](t-20261114-r28-perses-dashboards.md)  
**Owner:** 0428-083-  
**Priority:** normal  
**PRs:** [baseharbor#1608](https://github.com/mcpdev80/baseharbor/pull/1608), [baseharbor#1684](https://github.com/mcpdev80/baseharbor/pull/1684)  
**Source:** 
<!-- /generated:links -->

## Goal

Provision authorized existing Prometheus datasource in Perses using supported pinned native plugin and proxy/TLS contract.

## Scope and file ownership

Dedicated Prometheus datasource adapter/tests; no new Prometheus instance or invented metrics. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/metrics/prometheus.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus.go)
- [internal/metrics/prometheus_files.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_files.go)
- [internal/metrics/prometheus_verify.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_verify.go)
- [internal/serviceaccess/policy.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/serviceaccess/policy.go)

Use Perses PrometheusDatasource native versioned spec with existing authorized metrics endpoint, CA and credentials via proxy as supported; test actual query plus unauthorized/cross-target denial and no secret in descriptors.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Provision authorized existing Prometheus datasource in Perses using supported pinned native plugin and proxy/TLS contract.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-datasources](t-20261113-r28-grafana-datasources.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

## Owner decision — 2026-11-18 (takeover)
Card is ready to work after the 2026-11-17 unblock. Precondition per owner: 083 AND 080 must land on develop before #1665 continues (080 already merged via #1590). Deliver 083 on a fresh branch + one PR per card rule (#1608 stays closed).

kandidat auf branch lane-0428-083-datasources-r2 von develop 907f16713; 19 test cells PASS; CI run 44398435160 SUCCESS exact-head; fail-closed golden test

hopf-runde angesetzt (PR #1684 war 'behind', draft=false). schreibset ist DISJUNKT zu 0428-084 (von mir gemessen: keine gemeinsame datei zwischen refs/pull/1684 und refs/pull/1598 gegen develop) — daher parallel erlaubt. mission traegt die fenster-lerneffekte: merge-hopf statt rebase, doc-classifier-pflicht VOR push (praezedenz 084: unclassified product command), readability-audit, jobliste + skipped-gruende, frischer isolierter clone

hopf delivered und verifiziert: branch lane-0428-083-datasources-r2 = ab6932296, MONOTON auf develop da76c5cf9, merge-tree 0 konflikte, PR #1684 open/draft=false/clean, exact-head lauf 445… completed SUCCESS (von mir per gh api auf den exakten kopf gelesen). schreibset war disjunkt zu 0428-084 (comm -12 der dateimengen = leer), parallel war damit erlaubt

END akzeptiert, sitz entlassen: head ab6932296f1f24c2024810f10b155633d931f7d4, monoton auf develop da76c5cf9, merge-tree 0 konflikte, exact-head run 44505333646 completed SUCCESS mit NULL fehljobs (von mir per gh api auf jobs geprueft, nicht nur der lauf-status), PR #1684 open/draft=false/clean. akte perses-datasources-hopf/fix-1.md von mir aus der gemeinsamen kopie gesichert und gepusht (board 79cc02a1)

CODEX-REVIEW welle 4 = REQUEST CHANGES auf dem gepueften kopf (urteil 1684-0428-083.md). korrekture-runde ist vorgemerkt und wartet auf einen freien sitz: die vier perses-karten und 083 teilen sich dateien mit den laufenden lanen, darum kein paralleler start ohne write-set-nachweis. 083: 'runtime provisioning absent' (datasource wird gebaut, aber nicht in Perses bereitgestellt); 073: 'alert rule nicht ausgefuehrt/nicht persistiert' (persesAlertRealEvaluation); 077: 'catalog-availability aus host provider-metrics allein'; 089: 'PersesComposeServices rendert keine config (--config=/etc/perses/config.yaml) + loopback upstream'

REQUEST CHANGES abgeholt: datasource muss im laufenden Perses erscheinen (runtime provisioning), nicht nur als builder/golden-artefakt; branch lane-0428-083-datasources-r2 @ ab6932296, write-set gegen 121/057/110 gemessen disjunkt

korrektur-runde abgeliefert, von mir qualifiziert: branch lane-0428-083-datasources-r2 = f0adef107, monoton auf dem NEUEN develop e1dc2cf61, merge-tree 0 konflikte, PR open/draft=false/clean, exaktkopf-lauf 44520439061 completed SUCCESS (0 fehljobs, 33 ausgefuehrte zellen, 'PR Selected Checks' success). akte perses-datasources-hopf/fix-2.md auf origin/main. CODEX-REVIEW fuer diesen kopf beauftragt (urteil 1684-0428-083-r2.md); merge erst in meinem fenster

URTEIL AUF f0adef107 = REQUEST CHANGES ('runtime consumer and mounts absent / no merge'), von mir gegen deinen neuen kopf nachgerechnet: a9befb3127b26a8a0f622bcf686fb6bcbb9b9e6e unterscheidet sich von f0adef107 um GENAU EINE datei (internal/metrics/perses_prometheus_datasource_runtime.go), und 'MaterializePersesPrometheusDatasourceAt' taucht dort nur in internal/metrics/*_runtime.go + seiner eigenen test-datei auf, in internal/application/ nirgends — die aufruf-stelle fehlt also weiter. monotoner stack ist OK (e1dc2cf61 ancestor, f0adef107 ancestor), PR draft=false/blocked, lauf 44522363321 in_progress, aber der ist nicht die qualifying stelle. befehl an dieselbe lane: (1) aufruf an der echten apply-grenze in internal/application/perses_runtime.go VOR dem Perses-start, (2) read-only compose-mounts aus dem materializer-ergebnis (config-/datenpfade, kein zweite konstante), (3) isolierter Docker-runtime-test mit gepinntem image, der das LADEN der GlobalDatasource zeigt + query/proxy/TLS, zelle muss AUSGEFUEHRT statt skipped sein (sonst befuind an den owner mit datei:zeile der skip-bedingung, nicht selbst aendern), (4) grep-beleg vor push, (5) akte fix-3.md mit matrix

ENTBLOCKT durch den #1592-merge (develop 3b634232f): internal/application/perses_runtime.go ist jetzt in develop, also ist die aufruf-stelle folge-arbeit und kein fork von 088s kandidat. mission verlangt: aufruf an der apply-grenze vor dem Perses-start, read-only compose-mounts aus dem materializer-ergebnis, isolierter Docker-runtime-test (zelle muss laufen, sonst skip-bedingung als befuind + host-zeugen-praezedenz)

END ANGENOMMEN, alle zeugen von mir gegen gelesen: zweig-head 24cd5f4538fa8f9bc814fcd481143484742c3a14, base = develop c296086ca (der #1616-merge), PR non-draft, merge-tree gegen develop 0 konflikte, lauf 44573407736 completed SUCCESS created 17:05:46Z auf GENAU DIESEM kopf; akte evidence/r28-welle4-2026-11-19/perses-datasources-hopf/fix-4.md (main b01fb21d, blob c0113b26). DER EINE GRUND, WARUM SIE NICHT AUF REVIEW GEHT: der owner hat um 18:19:51+01:00 #1581 gemergt, develop ist 7ee6f817dbff5a238bbc651315d6d76b3819fc91, und der unterschied c296086ca -> 7ee6f817d betrifft scripts/test_pr_gate_plan.py + scripts/ci-workflow-policy.sh — scripts/test_pr_* ist ein treffer meiner base-abstands-regel, also schuldet die lane EINEN monotonen hopf auf 7ee6f817d plus EINEN exact-head-lauf. Kein inhalt zweifelt daran: die drei teile (apply-grenze runtime_postgres.go:140 -> ensurePersesDatasourceRuntime, read-only compose-mounts resolver-abgeleitet perses_runtime.go:99 fail-closed, container-akzeptanz-test lokal 3x gruen) sind geliefert. IHR BEFUND ist notiert und geht in die owner-draht-liste: 'PR Selected Runtime' skipped, skip-kette ci.yml:973 runtime_required=false <- pr-selected-runtime-matrix.py <- pr-gate-plan.py ohne mapping fuer perses/apply-pfade (owner-scope, von der lane NICHT geaendert) — nach dem hopf prueft sie, ob #1581 ihren fall schon abbildet

BEIDE BEDINGUNGEN SIND JETZT ERFUELLT, von mir gegen gelesen: hopf geliefert — zweig-head 738ed514b208239e02cb06968cc72bb808bc070c, base = develop 7ee6f817dbff5a238bbc651315d6d76b3819fc91 (dein merge #1581), 'git merge-base --is-ancestor origin/develop 738ed514b' = 0 (monoton), merge-tree 0 konflikte, PR clean + draft=false; exact-head-lauf terminal: 'PR Selected Checks' success, 0 fehljobs. INHALT (aus fix-4, unveraendert gueltig): aufruf an der ECHTEN apply-grenze (runtime_postgres.go:140 -> ensurePersesDatasourceRuntime), read-only compose-mounts aus dem resolver abgeleitet (perses_runtime.go:99, fail-closed), container-akzeptanz TestPersesPrometheusDatasourceContainerLoadsProvisionedDatasource lokal 3x gruen. IHR BEFUND BLEIBT OFFEN UND GEHOERT DIR (owner-scope, von ihr zu recht NICHT geaendert): 'PR Selected Runtime' wird fuer perses/apply-pfade NICHT selektiert — skip-kette ci.yml:973 runtime_required=false <- pr-selected-runtime-matrix.py <- pr-gate-plan.py ohne mapping; #1581 hat nur scripts/test_pr_gate_plan.py + ci-workflow-policy.sh geaendert, also bleibt der befund stehen (im planner sind 18 perses/apply-zeilen, aber keine runtime-selektion fuer diese pfade). Abnahme jetzt bei codex-welle3, mission aus den gemessenen zeugen

REVIEW->ACTIVE nach OWNER-DIREKTIVE (kein rueckgaengig-machen des contents — CODEX sagt APPROVE CONTENT, akte 1684-0428-083-r3.md auf main cb4cb793c0cd). KANONISCHER BLOCKER, JETZT AUS DER MESSUNG UND NICHT AUS DEM HANDOFF-WORTLAUT: scripts/pr-gate-coverage.json hat im abschnitt 'native_checks' GENAU VIER eintraege (native/podman/installation-destroy, native/docker/greenfield, native/docker/onboarding, native/podman/second-target-conflict) und im abschnitt 'gates' KEINEN einzigen treffer fuer 'obser' oder 'perses' — die observability-oberflaeche existiert nur als component-artige zeile, nie als natives PR-gate. Folge: scripts/pr-native-gate-plan.py:26 'validator.resolve_native_checks(changed_paths, coverage)' liefert fuer die 15 dateien des kanditaten die leere menge, ci.yml:851 setzt daraus runtime_required=false, und die jobs ci.yml:973/:1029 ('Targeted HA · docker'/'podman', 'PR · Selected Runtime') SKIPPEN am exact-head-lauf 44577713744. Der container-akzeptanztest war damit NUR lokal belegt — das ist die luecke, die der owner geschlossen haben will. DER OWNER HAT DIE GRENZE GEÖFFNET: 'die CI-Anpassung darf im selben PR wie Tests/Code landen', also aendert die lane scripts/pr-gate-coverage.json + positive UND negative routing-regression in diesem PR, ohne pauschale docker+podman-matrix; .github/workflows/** bleibt bis auf weiteres bei mir. Karte bleibt offen, bis der live-gate-nachweis (job-zeile mit conclusion=success + job-url) am exaktkopf ERBRACHT ist

Independent read-only review on PR #1684 head `738ed514b208239e02cb06968cc72bb808bc070c` (2026-11-19): found production lifecycle path mismatch, loopback datasource endpoint masked by host networking in the witness, and missing production proxy CA trust material masked by test-only secret injection. Exact-head run 44577713744 passed selected checks but skipped Selected Runtime; the base is behind current develop. See [review evidence](../evidence/r28-welle4-2026-11-19/codex-review-wave/1684-0428-083-independent-review.md). No merge recommendation.

STOP der lane mit datei:zeile war richtig, entscheidung ist MEINE und gefaellt (option b): develop's signaturen bleiben, der 4. parameter contextDir und die exportierte RuntimeComposeYAMLForContextDir fallen weg — gemessen tut die funktion nichts als RuntimeFiles{Dir: contextDir} zu bauen (kandidat runtime_postgres.go ~430, internal runtimeComposeYAMLForProject liest 'contextDir := files.Dir'), und die drei weiteren angeblich diverenten aufrufer (native_backend_inventory.go, remote_runtime_projection.go, runtime_lifecycle.go) enthalten auf BEIDEN seiten null contextDir-zeilen, sind also reine arity-konflikte. Bedingung an die lane: erst den test, der die mount-Aufloesung gegen den compose-context-dir pinsst (rot auf develop ohne ihre anderung, gruen mit), sonst END_BLOCKED mit dem stuick, an dem option b haengt — nicht allein umschwenken. ZUSAEtzLICH neu: develop ist e20f6f6e3b27 (#1708) und hat die gate-logik selbst geaendert (.github/workflows/ci.yml, docker-runtime-acceptance.yml, observability-acceptance.yml, scripts/ci-native-pr-gate.sh, scripts/pr-gate-plan.py) — nach base-distance-regel zaehlt kein grüner run vom alten gate

---

## fix-9 END_BLOCKED — x-083h5, 2026-11-20

decision b umgesetzt (3-arg signatures, splice uses files.Dir, RuntimeComposeYAMLForContextDir removed): commit 1c0e33ad (parent 36d075fa = current develop tip), branch lane-0428-083-datasources-r2 @ 1c0e33ad864ed3e43b7dbaee57093c507ab90e40, PR #1684 OPEN/MERGEABLE. Content proof: datasource files byte-identical between prior candidate 576c6ad8 and 1c0e33ad (only compose signatures adapted). Test-first: TestPersesDatasourceMountResolvesAgainstComposeContextDir RED on pure develop (compile: undefined datasourceMountRoots) -> GREEN with (b). All Go gates green (build/vet/application/metrics/contracts tests pass).

**The native/docker/perses-runtime-smoke CI gate FAILS — NOT a card defect.** Root cause reproduced identically on this local host AND on the Azure GitHub-hosted runners: `error mounting tmpfs to rootfs at /etc/perses/database ... mkdirat .../etc/perses/database: read-only file system`. The /etc/perses/database tmpfs mount is develop's code (serviceaccess/perses_compose_realization.go:388), untouched by my change; the ONLY diff between passing #6693 (576c6ad8) and failing runs (#44667006086, #44671189705) in the render path is contextDir=files.Dir vs files.Dir (identical value) -> byte-identical rendered compose. This is a Docker rootless-overlayfs tmpfs regression on the runner image/daemon, not my write-set.

Evidence: evidence/x-083h5/fix-9.md. Owner to fix the runner tmpfs regression or waive the native smoke gate for this card; my card's Go gates are green. Card moved to blocked.


## 2026-11-20 pause pending 0428-174 runtime gate repair

Moved 0428-083 from Blocked to Wait. Its #1684 work has started and is temporarily paused behind 0428-174, an active task assigned to the same owner, which is restoring the selected Docker runtime gate. Exact-head run [44671189705](https://github.com/mcpdev80/baseharbor/actions/runs/44671189705) fails in `native/docker/perses-runtime-smoke` before Perses assertions. The acceptance order is now explicit in `depends_on`: complete 0428-174, then hop #1684 to the fixed develop base and run exact-head acceptance. This is a temporary technical pause, not an Owner decision or acceptance.

BLOCKER FORT: die vierte vorbedingung t-20261120-r28-develop-runtime-integration-red ist GEMERGT (#1711, develop dbe7fbc3905b), die drei anderen waren laengst geschlossen - die karte ist damit durchgehend erfuellt und vom zustand 'wait' abgeholt. gemessen an ihrem PR: #1684 head 1c0e33ad864e, base 36d075fad77f, mergeable=behind, draft=false, upd 04:13:58Z; die zwei roten zellen ('PR Selected Checks' und 'PR · Native · native/docker/perses-runtime-smoke') waren folge der basisstoerung, nicht ihres diffs. neue frische lane '0428-083-' (sid 473e54be, ornith-kanal 2/2, parent-link verified) mit auftrag: rebase auf dbe7fbc3905b + 'git push --force-with-lease' auf den ungeschuetzten branch, ein PR (§3.8, kein zweiter), run am neuen head bis terminal, die beiden zellen als bestaetigt fuehren, drei einfrier-beweisszeilen, akte perses-prometheus-datasource/round-2.md, dann END. bleibt eine der zellen ROT, ist die ursache NICHT die basisstoerung: dann stoppen und QUESTION mit fehlerauszug, keine dritte identische korrektur (§3.6). alte lane w083-…-hopf5 war nach dem vierten idle ohne END freigegeben worden; PR #1684 und ihre akten bleiben auf github erhalten

---
id: t-20261114-r28-perses-secure-access
card_number: "0428-089"
card_short_title: "Protect Perses operator access"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w089-0428-089-secureaccess (codeman b60c11a1, flash)
kanban_status: closed
kanban_lane: closed
kanban_summary: "Integrate Perses with existing management access, verified transport and authorization; inspect selected upstream version…"
kanban_title: 0428-089 · Protect Perses operator access
priority: normal
depends_on: [t-20261114-r28-perses-contract-seam, t-20261114-r28-perses-runtime]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1599]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/7230e623033812ce2f5027ca029761ebf485b06a/evidence/r28-welle1-2026-11-15/perses-secure-access/round-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1599-0428-089.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44544947599", "https://github.com/mcpdev80/baseharbor/actions/runs/44551362534", "https://github.com/mcpdev80/baseharbor/commit/6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0"]
---

- [x] t-20261114-r28-perses-secure-access · Protect Perses operator access #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** w089-0428-089-secureaccess (codeman b60c11a1, flash) · **Priority:** normal  
    **PR:** [baseharbor#1599](https://github.com/mcpdev80/baseharbor/pull/1599)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/7230e623033812ce2f5027ca029761ebf485b06a/evidence/r28-welle1-2026-11-15/perses-secure-access/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1599-0428-089.md), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44544947599), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44551362534), [proof 5](https://github.com/mcpdev80/baseharbor/commit/6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-contract-seam](t-20261114-r28-perses-contract-seam.md), [t-20261114-r28-perses-runtime](t-20261114-r28-perses-runtime.md)  
**Required by:** [t-20261114-r28-perses-contact-routing](t-20261114-r28-perses-contact-routing.md), [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** w089-0428-089-secureaccess (codeman b60c11a1, flash)  
**Priority:** normal  
**PRs:** [baseharbor#1599](https://github.com/mcpdev80/baseharbor/pull/1599)  
**Source:** 
<!-- /generated:links -->

## Goal

Integrate Perses with existing management access, verified transport and authorization; inspect selected upstream version security and proxy SSRF protections.

## Scope and file ownership

Dedicated gateway/auth policy adapter; no privileged anonymous exposure or secret leakage. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/serviceaccess/http_gateway.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/serviceaccess/http_gateway.go)
- [internal/serviceaccess/policy.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/serviceaccess/policy.go)
- [internal/application/management_ui.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/application/management_ui.go)
- [internal/metrics/management_ui.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/management_ui.go)

Use existing management/UI authorization and TLS; validate authentication, denied identities, isolation and endpoint trust. Review pinned Perses upstream release security and restrict datasource proxy SSRF/credential exposure. Do not invent unverified token mode.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Integrate Perses with existing management access, verified transport and authorization; inspect selected upstream version security and proxy SSRF protections.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-secure-access](t-20261113-r28-grafana-secure-access.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

candidate 872c6c70 on lane-welle2-089-perses-secure-access, draft PR #1599 against base lane-0428-075-perses-seam (cb4367f3). 59 Perses cells pass; one failing check in internal/metrics reported as STATE and assigned to 0428-075.

delivered: 872c6c70 draft; base-defekt (seam r3) haengt an 075-korrektur

kandidat 2c44db837 (documentation-audit-fix, DE-rows ergaenzt), exact-head run 44058489510 SUCCESS (coord-uebernahme nach lane-idle), state behind => hopf in merge-welle

CODEX-REVIEW welle 4 = REQUEST CHANGES auf dem gepueften kopf (urteil 1599-0428-089.md). korrekture-runde ist vorgemerkt und wartet auf einen freien sitz: die vier perses-karten und 083 teilen sich dateien mit den laufenden lanen, darum kein paralleler start ohne write-set-nachweis. 083: 'runtime provisioning absent' (datasource wird gebaut, aber nicht in Perses bereitgestellt); 073: 'alert rule nicht ausgefuehrt/nicht persistiert' (persesAlertRealEvaluation); 077: 'catalog-availability aus host provider-metrics allein'; 089: 'PersesComposeServices rendert keine config (--config=/etc/perses/config.yaml) + loopback upstream'

REQUEST-CHANGES-runde auf dem frei gewordenen 084-sitz. startfaehig JETZT, weil 084 END angenommen und die lane entlassen ist — die 12 geteilten dateien (comm -12 vorher) sind ruhend.verbote bleiben: environment.go/envfilter (121), perses_dashboards_hosts.go + perses_contract_test.go + capability/perses.go (077 laeuft), .github/scripts

END_DONE inspiziert und ANGENOMMEN, mit einer offenEN mechanischen stelle: kopf 233be0af2bba691fed7bd99655fb78a7515e2a0f auf #1599 (draft=false), exaktkopf-lauf 44535875227 = completed SUCCESS, 23 ausgefuehrte zellen, 'PR Selected Checks' = success, candidate_advisory_required=false, akte auf plan-main 6c992aa6, host besenrein (7 ambient container unberuehrt). URSAHE des rest-hopfs = VERALTETE BASE/API-anderung, KEIN produktfehler: ihr hopf haelt 859654861, develop ist fac01c772 (kette 695ad5494 + 86858f129 + bcd0e29ca + fac01c772); der unterschied beruehrt .github/workflows/ci.yml (MIGRATION_CONTROLLER a6756c5… → 859654861…) und scripts/test_ci_check_routes.py, also verlangt meine base-abstands-regel (queue563, von der owner-policy 15:3xZ bestaetigt) genau EINEN neuen lauf auf dem aktuellen base. KEIN weiteres hopfen danach, wenn develop sich nur ausserhalb dieser dateien bewegt. Schreibe: mission-089-final-hopf.md

END ANGENOMMEN, alle zeugen von mir fern_gelesen im selben schritt: develop = fac01c77276ca2bf1e20cd0b7334bda5dd43e353, PR #1599 head = 69982520688e18a5c9bad89f093165c16d5be5d4, base = develop (aktuell), state open, draft=false, mergeable_state clean; 'merge-base --is-ancestor origin/develop <kopf>' = 0 (monoton) und 233be0af2 ist ancestor (ein hopf, kein history-rewrite); exaktkopf-lauf 44544947599 = completed SUCCESS, 'PR Selected Checks' = success, candidate_advisory_required=false, advisory-zelle skipped, KEINE HA-/runtime-zelle ausgeloest (genau die neue policy: keine breite matrix, wenn der base-plan sie nicht waehlt und die acceptance sie nicht verlangt); ci-fast-check vor dem push; akte fix-4.md auf plan-main 0d7d2a6a; host besenrein (7 ambient container unberuehrt). DAMIT: flash-sitz wird freigegeben (soll 1), karte geht in die abnahme

selbstkorrektur: ich hatte 'acht gemeinsame dateien' gemeldet (ueber 'gh pr view --json files'), korrekt sind ZWOELF gemessen an den drei-punkt-diffs gegen develop — die meldung der abnahme war richtiger als mein zahl. flash-sitz bleibt bis zum body-fix + der ausdruecklichen sequenzierung besetzt, danach freigabe (sauberer END liegt vor)

REIHENFOLGE ERFUELLT: #1598 ist GEMERGT als 1019190d8dc0ecac7693f3461153e76be0e2cb8a (14:56:29Z), develop = der wert, PR #1599 head ed7f448f6a84a6ed917260cd4186a2a122a077ed, draft=false, mergeable_state 'blocked' = NOCH KEIN TERMINALER BEWEIS: lauf 44551362534 (start 15:08:09Z) in_progress, ein job laufend, 0 fehljobs; Trusted Plan + Native gate plan + workflow policy + source format PASS, Go-shards/build/vet/focused Python pending. therefore kann 'PR Selected Checks' nicht terminal sein — KEIN merge, KEIN accepted; die aelteren laeufe 44535875227 (base 859) und 44544947599 (base fac01c772) sind nach der base-abstands-regel keine abnahme. CODE-REVIEW-LAGE, read-only, ausdrtuecklich KEIN verdict: die zwei frueheren runtime-blocker sehen adressiert — Perses-config deterministisch gerendert, auf vorhandensein/inhalt geprueft, read-only gemountet; Perses joined die gateway-netzwerk-namespace mit 'network_mode: service:…' ohne eigenen port; integrationstest prueft reachability/auth/host-invisibility. akte: evidence/r28-welle4-2026-11-19/secure-access-hopf/fix-4.md (main d6249180); PR-body von ihr berichtigt auf base=develop + STACK-vermerk
REIHENFOLGE ERFUELLT (beide notizen waren meine, hier zusammengefuehrt): STAND 15:1xZ, von mir fern_gelesen: develop 1019190d8dc0ecac7693f3461153e76be0e2cb8a (#1598 GEMERGT 14:56:29Z, damit ist die von mir festgelegte REIHENFOLGE #1598 vor #1599 erfuellt), PR #1599 head ed7f448f6a84a6ed917260cd4186a2a122a077ed, draft=false, mergeable_state 'blocked' = ES GIBT NOCH KEIN TERMINALEN BEWEIS: lauf 44551362534 (start 15:08:09Z) in_progress, 1 job laufend, 0 fehljobs; Trusted Plan, Native gate plan, workflow policy und source format sind PASS, mehrere Go-shards + build/vet + focused Python noch pending. DER AGGREGAT 'PR Selected Checks' KANN DADARCH NICHT TERMINAL SEIN — kein merge, kein accepted, und die beiden aelteren laeufe (44535875227 auf base 859, 44544947599 auf fac01c772) sind nach der base-abstands-regel keine abnahme. CODE-REVIEW-LAGE (read-only, ausdruecklich KEIN verdict der abnahme): die zwei früheren runtime-blocker sehen im neuen diff adressiert — Perses-config deterministisch gerendert + auf vorhandensein/inhalt geprueft + read-only gemountet; Perses joined die gateway-netzwerk-namespace mit 'network_mode: service:…' ohne eigenen port; ein integrationstest prueft reachability/auth/host-invisibility. akte-PFAD auf main: evidence/r28-welle4-2026-11-19/secure-access-hopf/fix-4.md (main d6249180), PR-body von ihr berichtigt auf base=develop + STACK-vermerk

BOARD AUF TERMINALEN STAND (mein vorheriger text meldete 'lauf pending' — das war beim lesen um 15:1xZ bereits ueberholt): lauf 44551362534 = completed SUCCESS, updated 15:13:47Z, head ed7f448f6a84a6ed917260cd4186a2a122a077ed, 0 fehljobs, 'PR · Native gate plan' + 'PR · Source format' success, 'PR · Exact Candidate'/'Release Source Preflight'/native-core zellen skipped (base-plan waehlt sie fuer diese pfade nicht), PR #1599 draft=false, mergeable_state clean. SEQUENZ: ed7f448 hat ausdrtuecklich die eltern 699825206 + 1019190d8, und 'git merge-base --is-ancestor 1019190d8… ed7f448…' = 0 — der merge von #1598 ist also PARENT, die von mir festgelegte reihenfolge #1598 vor #1599 ist erfuellt und es bleibt KEINE sequenz-sperre. karten-depends_on = [perses-contract-seam, perses-runtime]; der seam ist geschlossen und gemergt (#1575 → squash, content in develop), perses-runtime-status siehe vermerk. akte: evidence/r28-welle4-2026-11-19/secure-access-hopf/fix-4.md + fix-5 (ihr letzter hopf), plan-main 4b97a4bc

BOARD AUF TERMINALEN LAUF, vorheriger text meldete 'lauf pending' — ueberholt beim lesen: 44551362534 = completed SUCCESS, updated 15:13:47Z, head ed7f448f6a84a6ed917260cd4186a2a122a077ed, 0 fehljobs; 'PR · Native gate plan' + 'PR · Source format' success, 'PR · Exact Candidate' + 'Release Source Preflight' + native-core zellen skipped (der base-plan waehlt sie fuer diese pfade nicht, also kein fehlender beweis). PR #1599 draft=false, mergeable_state clean, develop unveraendert 1019190d8dc0ecac7693f3461153e76be0e2cb8a. SEQUENZ-SPERRE: KEINE — ed7f448 hat die eltern 699825206 + 1019190d8, 'merge-base --is-ancestor 1019190d8 ed7f448' = 0, der #1598-merge ist PARENT, reihenfolge #1598 vor #1599 erfuellt; karten-depends_on [perses-contract-seam, perses-runtime] sind BEIDE closed (seam gemergt als #1575). Freigabe-punkt ist jetzt allein deine unabhaengige abnahme (code + evidence), kein weiterer PR-hangt davor

RETIERSCHLUESSEL, kein base-thema: kopf ed7f448f ist formal gruen (lauf 44551362534 completed SUCCESS, 0 fehljobs, clean, base develop 1019190d), ABER der owner hat zwei ECHTE blocker gefunden und ich bestaetige beide an der datei. (1) internal/application/runtime_postgres.go:369 ruft in der produktions-komposition weiterhin 'writePersesUIComposeService' (einziger aufruf im zweig, definition perses_runtime.go:61); der gateway-pfad (internal/serviceaccess/perses_gateway.go, network_mode nur in kommentaren :120/:154) wird nicht von der komposition aufgerufen, 'PersesGatewayPlanFor' (perses_management_ui.go:292) ist der UI-/proxy-plan — therefore bindet die ausgelieferte compose Perses auf 0.0.0.0 mit direktem loopback-port. (2) internal/serviceaccess/perses_config_render.go:65 'enable_auth: true' + :67 'encryption_key_file: ' + PersesEncryptionKeyContainerPath (:35 '/etc/perses/…'); 'grep PersesEncryptionKeyContainerPath' liefert NUR konstante, config-zeile, test und ein os.WriteFile in perses_config_render_test.go:114 — KEIN produktions-schreiber/projection/mount, waehrend der capability-vertrag (internal/capability/perses_security.go:53) den start ohne key verweigert. AUFTRAG: produktionskomposition auf gateway-only exposure umstellen + secret-sichere key-erzeugung/projection/read-only-mount (distroless nonroot kann 0600 bind mounts nicht lesen, perses_runtime.go-kommentar beachten) + regression DURCH den produкомpositionspfad fuer (a) gateway-only, (b) key fehlend fail-closed, (c) key vorhanden; gleicher zweig, monoton, kein konkurrierender zweig, kein force; dann neuer exaktkopf-lauf. Freigabe/Merge bleibt beim owner

ZWEI BLOCKER, beide von mir an ed7f448f6a84a6ed917260cd4186a2a122a077ed nachgelesen, grund ist produkt-loch nicht base: B1 runtime_postgres.go:369 ruft 'writePersesUIComposeService(&b, m, resourceProject)' (einziger aufruf; definition perses_runtime.go:61) — gateway-pfad (internal/serviceaccess/perses_gateway.go) erscheint in der komposition nirgends, therefore bindet die ausgelieferte compose Perses auf 0.0.0.0 mit direktem loopback-port. B2 perses_config_render.go:65 'enable_auth: true', :67 'encryption_key_file: ' + PersesEncryptionKeyContainerPath (:35 '/etc/perses/secrets/encryption-key'); 'git grep encryption' in internal/application + internal/serviceaccess liefert auesser tests NOTHING, das den schluessel schreibt, projeziert oder einhaengt, waehrend internal/capability/perses_security.go:53 den start ohne schluessel verweigert. HANDOFF-PLAN: (i) b60c11a1 haelt meldefrist, liefert END + cleanliness, keine neuen aenderungen; (ii) nach ihrem END gebe ich den flash-sitz frei (damit flash 2->1, soll 1); (iii) frische lane w089-0428-089-composekey-fix uebernimmt denselben zweig lane-welle2-089-perses-secure-access (monotoner merge-hopf, KEIN force, KEIN zweiter zweig), mission /var/tmp/mission-089-corrective.md; (iv) freigabe an die abnahme erst nach terminalem 'PR Selected Checks' auf dem neuen kopf. SPERRFRIST: bis meine (iii)-meldung hier steht, darf niemand den zweig anfassen. SPERRDATEIEN im auftrag: internal/capability/perses_security.go nicht aendern, non-root Postgres CI image nicht antasten

EIGENE KORREKTUR MEINES HANDOFF-PLANS: ich hatte eine neue lane 'w089-0428-089-composekey-fix' auf demselben zweig vorbereitet (/var/tmp/mission-089-corrective.md) undangekuendigt. Das ist HALTLOS, sobald die korrekturmission auf b60c11a1 angenommen ist — zwei schreiber am selben zweig verletzten §4.3 (genau ein aktiver inhaber pro task) und §3.6 (keine ersatzworker, solange eine session weiteraendert). ENTSCHLUSS: b60c11a1 bleibt der EINIGE inhaber von lane-welle2-089-perses-secure-access und fuehrt B1 + B2 in ihrer session zu ende; die neue lane entsteht NICHT. Freigabe an die abnahme erst nach terminalem 'PR Selected Checks' auf dem neuen kopf. Die unabhaengige stelle haelt sich fern von diesem zweig (zugesichert) und reviewt #1697

Independent read-only review on PR #1599 head `97d88ffefa0c89281d0c1b776f47b46f4449123f` (2026-11-19): Compose combines `network_mode` with `networks`, and Perses v0.55.1 rejects enabled auth with no provider. Exact-head run 44582754552 completed successfully: Go shards, build/vet, docs checks and required aggregate passed; runtime/native gates skipped. See [review evidence](../evidence/r28-welle4-2026-11-19/codex-review-wave/1599-0428-089-independent-review.md). No merge recommendation.

fix-7 final auf e43552734, run 44598112016 completed/success am exaktkopf; runtime-/HA-zellen SKIPPED (owner-draht 114(a) ORAS-install)

CODEX-REVIEW APPROVE auf exaktkopf e435527348587d6246b0af600c6bd82717ce9c32 (akte 1599-0428-089-r2.md), CODEX-MERGE squash auf develop 6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0 (merged_at 2026-11-19T20:04:22Z). INHALTSBEWEIS VON MIR NACHGEMESSEN: 34 diff-dateien, 34/34 blobs identisch gegen develop, 0 abweichend, 0 fehlend. lauf 44598112016 completed/success am exaktkopf; runtime-/HA-zellen SKIPPED (owner-draht 114(a)) — die karte war trotzdem abnehmbar, weil der compose-/config-pfad durch die echten validierungs-tests (perses_fix7_regression_test.go:11/:19/:48, inkl. docker compose config -q) belegt ist. variantes A (gateway-alias am bestehenden spec.NetworkAliases, network_mode exklusiv) wie entschieden gebaut.

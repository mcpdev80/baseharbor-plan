---
depends_on: [t-20261122-gate-catalog-missing-app-broker-component]
id: t-20261122-runtime-broker-health-unhealthy
card_number: "0428-237"
card_short_title: "data-capabilities native gate"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: andere Codex-Session (#1770) / 0428-241 (selected blocker)
tags: [#task, #release/v0.4-28]
kanban_status: active
kanban_lane: active
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-237 · data-capabilities native gate
priority: ""
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1753, mcpdev80/baseharbor#1761, mcpdev80/baseharbor#1770]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44994268323", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/45000121766", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-2.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44998846458", "https://github.com/mcpdev80/baseharbor/actions/runs/45008538769", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-3.md", "https://github.com/mcpdev80/baseharbor/actions/runs/45011764715"]
---

- [ ] t-20261122-runtime-broker-health-unhealthy · CI: data-capabilities native gate fails on secure runtime broker readiness #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** andere Codex-Session (\#1770) / 0428-241 (selected blocker)  
    **PR:** [baseharbor#1753](https://github.com/mcpdev80/baseharbor/pull/1753), [baseharbor#1761](https://github.com/mcpdev80/baseharbor/pull/1761), [baseharbor#1770](https://github.com/mcpdev80/baseharbor/pull/1770)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44994268323), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-1.md), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/45000121766), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-2.md), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/44998846458), [proof 6](https://github.com/mcpdev80/baseharbor/actions/runs/45008538769), [proof 7](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-3.md), [proof 8](https://github.com/mcpdev80/baseharbor/actions/runs/45011764715)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261122-gate-catalog-missing-app-broker-component](t-20261122-gate-catalog-missing-app-broker-component.md)  
**Owner:** andere Codex-Session (#1770) / 0428-241 (selected blocker)  
**Priority:** not set  
**PRs:** [baseharbor#1753](https://github.com/mcpdev80/baseharbor/pull/1753), [baseharbor#1761](https://github.com/mcpdev80/baseharbor/pull/1761), [baseharbor#1770](https://github.com/mcpdev80/baseharbor/pull/1770)  
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

## Finding (2026-11-22, exact-head run of PR #1753)

Run `44994268323` at head `a40b76764c3c08ec690e723def0ca167ce989c2b` (base `52a3c5446f4`) FAILED both engines on the
same test: `PR · Native · native/docker/data-capabilities` job `137121839425`, `PR · Native · native/podman/`
`data-capabilities` job `137121839379`, and their `PR · Selected Runtime` siblings `137122169353` (docker) /
`137122169299` (podman); aggregate `PR Selected Checks` `137124048433` failure. Both fail inside
`TestApplicationCapabilityLifecycleExistingCore/secrets` while *starting the secure runtime broker*: the broker
container reports unhealthy and its readiness endpoint answers `503 not_ready`; timeouts ~2m (docker) / ~5m (podman).
The mTLS identity check immediately before it passes, so this is broker readiness/fixture behaviour - NOT a footprint
CLI assertion and NOT candidate-introduced content (the hop diff is develop-only).

Steps: (1) rerun the failed jobs at the exact same head to classify transient vs deterministic; (2) read the broker
start path and the fixture's readiness wait, cite file:line; (3) decide fix owner: `internal/observability/registry.go`
and `internal/capability/perses_selection.go` are lane-banned, so a readiness/fixture change needs a named owner.
History: `t-20261102-broker-ready3-widen-readiness-grace` was closed as dropped, `0427-118` (ORAS edge readiness) was
accepted - neither covers a `503 not_ready` broker health failure in this suite.
Evidence: run `https://github.com/mcpdev80/baseharbor/actions/runs/44994268323`.

triage ist aktiv auf sitz 03c7350a: rerun der fehlgeschlagenen jobs am exakten head 44994268323 (transient oder deterministisch), danach datei:zeilen-kette fuer den broker-start und die readiness-warte-schleife. Schreibsperren beachten: internal/observability/registry.go und internal/capability/perses_selection.go sind Lane-gesperrt.

RERUN AM EXAKTEN head a40b76764c3 ist GELAUFPEN (attempt 3 von run 44994268323) und zeigt dieselbe signatur: docker selected-runtime job 137133627704 FAILED, podman selected-runtime job 137133627980 FAILED, docker native job 137133647957 FAILED, podman native 137133625738 bei meiner messung noch aktiv. URAECHIERNUNG: DER FEHLER IST DETERMINISTISCH, NICHT TRANSIENT. Rueckstand: PR 1753 ist hinter develop acc34323968 zurueck (1627 ist gemergt), jeder weitere beweis braucht also erst einen frischen hop. Die diagnosis-akte der lane (rerun-tabelle + datei:zeilen-kette) steht noch aus; der naechste schritt ist die ursaechen-kette im broker-start/pfad der readiness-warte-schleife - wenn sie in internal/observability/registry.go oder internal/capability/perses_selection.go landet, entscheidet der Owner ueber den fix-besitzer, weil beide pfade Lane-gesperrt sind.

DIAGNOSE FERTIG, ENTSCHEIDUNG BEI IHREN SITZEN. Der 503 not_ready kommt aus server.go:260 (writeNotReady, antwortet 503 mit {status:not_ready}), aufgerufen aus server_run.go:168/175/182/203 fuer die /readyz-abhaengigkeitspruefungen. Der gebundene runtime-/executor-pfad haelt an den Lane-gesperrten dateien internal/observability/registry.go und internal/capability/perses_selection.go an - die lane hat dort bewusst NICHTS geaendert (read-only, akte runtime-broker-0428-237/round-1.md, plan main 794446b94). Deterministisch ueber docker UND podman data-capabilities (run 44994268323: 4 failed / 12 success / 14 skipped am head a40b76764c3; attempt-3-rerun zeigt dieselben jobs). Konsequenz: PR 1753 kann nicht gemergt werden, bis dieser pfad entschieden ist; danach frischer hop auf develop acc34323968 und ein run mit echten runtime-gates.

DIAGNOSE FERTIG, ENTSCHEIDUNG BEI IHREN SITZEN. Der 503 not_ready kommt aus server.go:260 (writeNotReady, antwortet 503 mit {status:not_ready}), aufgerufen aus server_run.go:168/175/182/203 fuer die /readyz-abhaengigkeitspruefungen. Der gebundene runtime-/executor-pfad haelt an den Lane-gesperrten dateien internal/observability/registry.go und internal/capability/perses_selection.go an - die lane hat dort bewusst NICHTS geaendert (read-only, akte runtime-broker-0428-237/round-1.md, plan main 794446b94). Deterministisch ueber docker UND podman data-capabilities (run 44994268323: 4 failed / 12 success / 14 skipped am head a40b76764c3; attempt-3-rerun zeigt dieselben jobs). Konsequenz: PR 1753 kann nicht gemergt werden, bis dieser pfad entschieden ist; danach frischer hop auf develop acc34323968 und ein run mit echten runtime-gates.

weiter in arbeit, ein schritt fehlt noch: der NAME der fehlgeschlagenen abhaengigkeit entscheidet den fix-besitzer. Die kette liegt in internal/controlplaneruntime/server_run.go:163-219 (database :166-170, openbao :172-178, runtime-executor :179-206) und writeNotReady in internal/controlplaneruntime/server.go:260-274 schreibt ein 'dependency'-feld - beide dateien sind Lane-ERLAUBT, die sperren betreffen nur registry.go/perses_selection.go. Auftrag an f0f6c8b4, das feld aus den logs der attempt-3-jobs 137133647957, 137133625738, 137133627704, 137133627980 zu lesen und die korrektur dort zu verorten. Kein grundloser dritter rerun: der owner sagt ausdruecklich, unveraendert nicht nochmal versuchen.

BESTAETIGT AUF DEVELOP-HOEHE, nicht nur am alten base-zeiger: PR 1761 ist aktiv exakt an develop acc343239681feb235a33cf00c8ea754c537291f und sein nativer job native/docker/data-capabilities 137139636770 FAELLT in TestApplicationCapabilityLifecycleExistingCore/secrets mit broker-readiness timeout nach 2m03s. Dieser eine defekt erklaert die roten runs von PR 1753, 1723, 1725 und 1761. ABGRENZUNG gegen stillumdefinition: karte 0428-237 bleibt ausschliesslich DER readiness-fix (wem gehrt die korrektur, wenn die kette in internal/observability/registry.go oder internal/capability/perses_selection.go endet - beide Lane-gesperrt). Die neue karte 0428-240 ist DAFUER NUR der diagnostics-text im CLI-fehlertext (cmd/baha/app_broker.go:206, das 'runtime diagnostics:'-feld ist leer) und loest 0428-237 NICHT ab. Kein weiterer unveraenderter rerun: erst fix, dann run, wie der owner sagt.

FIX IST BEAUFTRAGT, nach ihrem read-only-befund (akte round-2.md, plan main 4bff809da): die dependency ist aus CI nicht mehr lesbar (run 44994268323 logs HTTP 404, purged) und der fix-pfad liegt in internal/controlplaneruntime/** - also KEINSPERRT, keine owner-ausnahme noetig. Schluessel-beleg aus ihrer messe: policy-artig haengt es an der readiness-reihenfolge in server_run.go:163-219 (database :168, openbao :175, runtime-executor :182/:203) mit writeNotReady server.go:260-274; der fall tritt auf beiden engines auf, also eine gemeinsame control-plane-dependency. Stoppt die lane, wenn eine Lane-gesperrte datei oder cmd/baha/app_broker.go (0428-240, andere haende) getroffen muesste.

UEBERGABE VOLLZOGEN, zustand gemessen statt beschnigt: die lane meldet END_BLOCKED mit ausdruecklicher HAND OFF. Ihr branch lane-0428-237-broker-readiness existiert NUR LOKAL im haupt-clone und zeigt auf acc343239681feb235a33cf00c8ea754c537291f - also NULL eigene commits, nie gepusht, kein PR. Es ist nichts zu retten aus diesem branch; die uebernahme beginnt bei der read-only-akte round-2.md (rekonstruierte /readyz-kette server_run.go:166-206: database :168, openbao :175, runtime-executor :182/:203; writeNotReady server.go:260-274; fix-pfad internal/controlplaneruntime/** = erlaubt). ZWEI zeugen, die die uebernahme kennen muss: die logs von 45001383922 sind lokal abgelegt (/tmp/devid237/run45001383922.log, 929 KB, 5575 zeilen) enthalten aber NUR checkout-rauschen, KEINEN dependency-namen; die API-pfade liefern 404/limit. Der dependency-name ist damit weiterhin UNBEKANNT - das ist genau das loch, das karte 0428-240 (PR 1763, draft) schliessen soll. Ich habe der lane aufgegeben: haupt-clone zurueck auf develop, akte-zeile 'zustand des zweigs', END mit meldefrist.

RUECKGABE DER UEBERGABE, begruendet und gemessen: die maintainer-sitzung hat den index-traeger PR 1764 uebernommen (base develop, head 8d64f0cf803, ein LEERER marker-commit, durchgang 45005623091 FAILED in 'PR . Trusted Plan' 137156455112 und 'PR . Selected Checks' 137156547886, 24 checks skipped) - aber NICHT ihre karte. Damit der fenster-blocker nicht herrenlos haengt, geht 0428-237 zurueck an f0f6c8b4: neuer branch lane-0428-237-broker-readiness-r2, base exakt develop 8629450ef3c, fixes recht auf internal/controlplaneruntime/**; stapeln auf PR 1763 (branch lane-0428-240-broker-diagnostics, spitze 5d138ce2613) ist als additiver STACK erlaubt, wenn der dependency-name vorher sichtbar sein muss - deklaration im PR-body, kein rebase/amend/force. Timeout erhoehen, retry aufweichen, sleep im test oder 'not_ready' durch 'ok' ersetzen ist ausdruecklich verboten.

UMGESCHICHTET, weil meine messung die these nicht traegt: 'readiness timeout' erscheint in den vier gelesenen job-protokollen NULL mal, 'not_ready' GENAU EIN mal (podman-Job 137139636747 von PR 1761); der shared blocker ist die fussnoten-ZULASSUNG (karte 0428-227, PR 1753) mit dem wortlichen 'app footprint show -o json' + '--confirm-candidate ... refusing to record deployment state' in 137139969524/137139969537. Auftrag an die lane: CHRONOLOGIE-NDERUNG gestoppt, kein PR ohne wiederholbaren not_ready auf develop 8629450ef3c, dafuer der abgrenzungs-abschnitt in runde-3. Wenn der fall nicht isolierbar ist, entscheiden sie: 0428-237 zusammen mit 0428-227 fueren oder aufheben - ich habe keine liebe zur doppelten karte.

UMGESCHICHTET, weil meine these die messung nicht traegt: 'readiness timeout' NULL mal in den vier gelesenen protokollen, 'not_ready' GENAU EIN mal (podman 137139636747); shared blocker ist die fussnoten-ZULASSUNG (0428-227). Auftrag an die lane: chronologie-aenderung gestoppt, kein PR ohne wiederholbaren not_ready auf develop 8629450ef3c, dafuer der abgrenzungs-abschnitt in runde-3.

UMGESCHICHTET, weil meine these die messung nicht traegt: 'readiness timeout' NULL mal in den vier protokollen, 'not_ready' GENAU EIN mal (podman 137139636747). Shared blocker ist die fussnoten-ZULASSUNG (0428-227). Auftrag an die lane: chronologie-aenderung gestoppt, kein PR ohne wiederholbaren not_ready auf develop 8629450ef3c, dafuer der abgrenzungs-abschnitt in runde-3 (akten-Regel: keine checkbox-zeilen, nummerierte listen - sie blockieren die board-publikation).

UMGESCHICHTET, weil meine these die messung nicht traegt: 'readiness timeout' NULL mal in den vier protokollen, 'not_ready' GENAU EIN mal (podman 137139636747). Shared blocker ist die fussnoten-ZULASSUNG (0428-227). Auftrag: chronologie-aenderung gestoppt, kein PR ohne wiederholbaren not_ready auf develop 8629450ef3c, dafuer der abgrenzungs-abschnitt in runde-3 (akten-regel: nummerierte listen statt checkbox-zeilen, die blockieren die publikation).

ARBEIT WIEDER AKTIV, WEIL DER FALL REAL IST (protokoll von mir, nativer docker-job 137165488041 im durchgang 45008538769, head b86440c3 auf develop 8629450ef3c): 'app_capability_runtime_test.go:136: [app apply --skip-memory-preflight]: Starting secure runtime broker:' mit 'unhealthy' 2 mal, daneben READY 8 mal und OpenBao 2 mal, und 'live runtime inventory: Core containers=0 total containers=0' (zeile :55). DER BROKER STARTET ALSO NICHT HOCH, waehrend control-plane und OpenBao bereit melden - das zeigt auf den runtime-executor-pfad (server_run.go:182/:203), nicht auf database/openbao. Meine pauschale zuruecknahme von vorhin war zu breit: der defekt ist reproduzierbar, nur nicht in den develop-Core-laehlen. AUFTRAG: fix auf 0847d100 nach ihrem #1753-bericht (ihr durchgang traegt den beweis), verbotenerweg weiter: kein timeout erhoehen, kein retry, kein sleep, kein 'not_ready' durch 'ok'. SELECTED-seite ist eine ANDERE karte geworden: 0428-241 (guided fixture drift, dep-frei, wartet auf einen freien sitz).

MEINE EIGENE KORREKTUR: ich hatte diese karte wegen 'containers=0' zurueck auf active gedreht - das war zu weit. Im exakten-head-protokoll 137165488041 steht 'readiness timeout' NULL mal und 'not_ready' genau einmal, waehrend 'confirm-candidate' und zwei TestApplication-Faelle den ausschlag geben. DER BROKER HAENGT ALSO NICHT in diesem fall; die ursache der roten runtime-reihen ist die fussnoten-zulassung (0428-227), die 0847d100 jetzt behebt. Diese karte wartet auf dessen outcome; wenn nach gruenem 0428-227 immer noch ein readiness-fehler uebrig bleibt, geht sie zurueck in arbeit.

ZWEI-URECHEN-AUFTEILUNG, DIREKT GEMESSEN AN RUN 45008538769 (head b86440c3): NATIV (docker 137165488041 + podman 137165488058) readiness timeout=0, not_ready=1, 'Starting secure runtime broker' 32x, '503' 17x -> DER BROKER meldet 503 NICHT-BEREIT im capability-lifecycle-test. SELECTED (docker 137165839346) not_ready=0, confirm-candidate=8 -> NUR consent. PR 1753 braucht BEIDE gruen, deshalb zwei getrennte fix-schritte auf DEMSELBEN branch. Meine zwei vorangehenden drehungen (active, dann wait) waren je zur eine haelfte richtig: nativ IST ein echtes 503-readiness-fehlerbild. Auftrag an 0847d100: den broker-readiness-pfad in internal/controlplaneruntime/** so fixen, dass /readyz NICHT 503 liefert, wenn der broker im lifecycle-test hochfaehrt - verbotenes weiter: timeout erhoehen, retry, sleep, not_ready->ok.

PR 1761 teilt den GETEILTEN blockierer mit PR 1753: am head 669d76ac447 schlagen die vier data-capabilities-reihen fehl und mergeStateStatus = BEHIND. Es ist KEIN perses-einzelfall und KEIN einfacher merge - dieselbe fussnoten-zulassung (0428-227) + derselbe broker-503 (diese karte 0428-237). Wenn 0428-237/227 auf develop gruen sind, braucht #1761 nur hop + EINEN durchgang. Kein merge vorher.

DER ECHTE VERBLEIBENDE #1753-BLOCKER, NEU BESTAETIGT am frischen head 22ff5345335: nativer docker-job 137175474667 faillt weiter TestApplicationCapabilityLifecycleExistingCore/secrets nach 148s an app_capability_runtime_test.go:136 'Starting secure runtime broker' mit unhealthy=2, '503'=7, not_ready=0, confirm=1 -> der broker/faellt hoch bzw. wird unhealthy, control-plane/openbao bereit. DIESE aenderung ist im aktuellen head NICHT enthalten (der head aendert nur operatorauth/footprint-zulassung). AUFTRAG an 0847d100: den broker-readiness-pfad (internal/controlplaneruntime/** server_run.go ~163-219 / server.go ~260) ECHT fixen, damit der lifecycle-test-broker gesund wird - verbotenes: timeout erhoehen, retry, sleep, not_ready->ok.

BESTAETIGT an durchgang 45011764715 (head 22ff5345335, TERMINAL FAILURE failed 5): NATIVE data-capabilities schlagen fehl in BEIDEN engines - docker-job 137175474667 UND podman-job 137175474631 (TestApplicationCapabilityLifecycleExistingCore/secrets, broker unhealthy/503), plus PR Selected Checks. Meine fruehere feststellung, podman laeuft noch, ist ueberholt: podman ist FAHLS. Die broker-readiness-fix (controlplaneruntime) ist im head NOCH NICHT enthalten. 0847d100 liefert.

FIX-ORT KORRIGIERT DURCH READ-ONLY-HUNT (akte hunt-develop-releasedesse-round-1.md, origin/main 9fe9690c2): der broker-503/unhealthy kommt aus cmd/baha/app_broker.go - (1) :440-447 docker / :412-421 podman lesen transientes 'starting'/ 'unhealthy' als FATAL, obwohl compose-healthcheck retries:12 traegt -> keine FailingStreak-Toleranz = wahre ursache der fruehzeitigen ablehnung. (2) :502 version-mismatch zeigt expectedVersion doppelt. (3) /readyz parst raw-body ohne HTTP-status. Auftrag an 0847d100 (brk503c). SCHREIB-KANTE: #1763 editiert dieselbe datei (diagnostics) -> merge-reihenfolge, kein file-conflict wenn 0847d100 nur die readiness-BEDINGUNG ergaenzt und die redaction nicht anfasst.

1770 standalone (nur scripts/ci-native-pr-gate.sh) head 11df3b2e, CI 45022910559 green aber native matrices skipped (keine katalog-mapping) = nicht runtime-validiert. Wartet 1768/242 (registriert scripts/ci-native-pr-gate.sh als ci-executor). Danach 1770 auf develop-head hoppen + exakten native data-capabilities docker und rootless podman nachweis. 1753 haelt am consent 236 owner-entscheidung.

#1770 native matrix SKIPPED (wartet #1768 katalog). SEQUENZ WICHTIG: NACH #1768-LAND hoppt #1770 auf den neuen develop-head und MUSS exakte native data-capabilities docker+rootless-podman gaete AUSFUEHREN (nicht skipped) als runtime-beweis fuer 0428-237. Review dafuer gehalten bei fecbada9. Kein skip-als-gruen.

#1770 additiv gehoppt auf develop 3cbb2bac (nach #1774-B-merge) -> head 2a4adca0, exact run 45030747445 queued. Weil B jetzt auf develop ist, SOLLTE der planner native/docker+podman/data-capabilities ECHT selektieren (nicht mehr skipped). Owner verifiziert die selected native gates vor merge; review fecbada9 danach. Wenn trotz B weiter skipped -> befund an coord (catalog-selectie pruefen).

#1770 head 2a4adca0 auf develop 3cbb2bac (nach #1774-B-merge). UNLOCK BESTAETIGT: native docker+podman data-capabilities + selected runtime atomic/docker|podman laufen in Durchgang 45030747445 ECHT (in_progress, nicht skipped). fecbada9 prueft bei terminal + merged wenn gruen. #1753 haelt derweil am consent (236 owner-decision).

KATALOG-UNLOCK BESTAETIGT: #1774(B) wirkt, native data-caps docker 137234060728 + podman 137234060645 laufen JETZT echt. Sie failen aber an 'app footprint show -o json' confirm-candidate + interactive auth auf piped input = DERSSELBE defect wie #1753 selected, ZUGEORDNET KARTE 0428-241 (worker-behebbar footprint JSON contract + consent harness), NICHT consent 236 (closed/dropped) und NICHT image-build. Sequence um #1753/0428-241 + exact rerun. native jobs noch running.

NATIVE PODMAN data-capabilities job 137233607705 SUCCESS - localhost/baseharbor-runtime:ci-native-podman-72959a95 gebaut, TestApplicationCapabilityLifecycleExistingCore PASS 466s = 0428-237 SHA-image fix VALIDIERT auf podman. Native docker laeuft noch. SELECTED docker+podman failen im 0428-241 footprint consent-harness (f0f6c8b4). PR unmerged bis native docker + 241 routing. Kein merge auf partial.

MILESTONE: beide NATIVE data-caps ZELLEN GRUEN (docker 137233607782 687s + podman 137233607705 466s, je localhost/baseharbor-runtime:ci-native-<runtime>-72959a95, TestApplicationCapabilityLifecycleExistingCore PASS). 0428-237 KERN (SHA-image heilt broker 503) VALIDIERT. aggregate FAILURE NUR durch selected docker/podman 137234060728/0645 = 0428-241 footprint-show consent/fixture (worker, NICHT 236/image). planner/ci-executor/source/trusted/policy/candidate/runner ALLE gruen. Unmerged bis 0428-241 selected geoeffnet oder owner exception. Nicht als full-green buchen.

NATIVE data-caps docker+podman BEIDE SUCCESS (localhost/baseharbor-runtime:ci-native-<rt>-72959a95 gebaut, TestApplicationCapabilityLifecycleExistingCore PASS) = 0428-237 SHA-image broker-fix VALIDIERT auf beiden providern. Aggregate FAILURE NUR selected docker/podman = 0428-241 footprint consent/fixture. PR #1770 UNMERGED bis selected geoeffnet + owner genehmigt.

---
id: t-20261018-r27-registry-access
card_number: "0427-049"
card_short_title: "use configured enterprise"
areas: [artifacts]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: coord-welle5 (Lane w222, freigegeben)
kanban_lane: closed
kanban_summary: Resolve explicitly configured app-scoped OCI registry/artifact endpoints including GitLab/GHCR/Harbor/Quay/Artifactory/Nexus…
kanban_status: closed
kanban_title: "0427-049 · use configured enterprise"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-candidate-contract, t-20261018-r27-native-auth, t-20261022-r27-ci-delivery]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1395]
sources: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1395"]
---

- [x] t-20261018-r27-registry-access · Registries: use configured enterprise endpoints and native credentials #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/artifacts #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (Lane w222, freigegeben) · **Priority:** high  
    **PR:** [baseharbor#1395](https://github.com/mcpdev80/baseharbor/pull/1395)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1395)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-candidate-contract](t-20261018-r27-candidate-contract.md), [t-20261018-r27-native-auth](t-20261018-r27-native-auth.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
**Required by:** [t-20261018-r27-artifact-resolution](t-20261018-r27-artifact-resolution.md), [t-20261018-r27-image-transfer](t-20261018-r27-image-transfer.md), [t-20261018-r27-local-registry](t-20261018-r27-local-registry.md), [t-20261018-r27-version-view](t-20261018-r27-version-view.md)  
**Owner:** coord-welle5 (Lane w222, freigegeben)  
**Priority:** high  
**PRs:** [baseharbor#1395](https://github.com/mcpdev80/baseharbor/pull/1395)  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

Resolve explicitly configured app-scoped OCI registry/artifact endpoints including GitLab/GHCR/Harbor/Quay/Artifactory/Nexus when they expose the supported native protocol. Reuse native Docker credential helpers/Podman auth files and configured CA/proxy/auth scope; fallback only through existing opted-in protected store. Discover actual protocol/capabilities, not brand names. Do not treat every artifact store as an image registry or scrape a proprietary API. Denied/private/unavailable endpoint has no public/plain-HTTP/local fallback. Select a readable tag/ref then record its exact resolved identity; tags are not immutable and lists are bounded to authorized app sources.

## Inputs and output

Consume accepted predecessor interfaces and existing native tools. Deliver the callable bounded production adapter and executable positive/negative tests, not a dormant framework. Use [the standards boundary](../decisions/2026-10-18-r27-native-delivery-and-stages.md); runtime support remains limited to qualified providers.

## Dependencies and file ownership

cmd/baha/application_registry_source.go and matching tests; existing credential APIs are inputs, not a second credential store. Paths are reservations confirmed by accepted contract predecessor; shared registrations belong only to public-surfaces, not this slice. No overlapping writes or draft-branch consumers.

## Required checks

Native credential-helper/authfile and TLS registry API fixtures; missing CA/auth, tampered host, denied tags, endpoint mismatch and log redaction; small real registry auth/pull smoke only for uncovered native behavior. Actual trusted discovery/executor/fixtures must be accepted in ci-lanes before assignment. Smallest sufficient checks; independent native gates may run on isolated suitable runners. Existing verifier alone permits green-evidence reuse; missing/skip/fail is not PASS. No self-approved coverage or full pre-release run.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planned/unassigned, 2026-10-18. Maintainer requested native standards, real stage/version operation, existing registries/CI/GitOps and a thin promotion operation. No product implementation or release action started.

## Runde 1 pruefbar 2026-11-05 (kopf c2ada69cd33)
Nachgemessen: ls-remote echt==head, develop VORFAHR, lauf 42120843177 TERMINAL SUCCESS (14 selected checks
gruen), akte round-1.md auf main. Konfig-getriebener endpunkt, native credentials, fail-closed mutante rot,
zusammenbau echt, red-first belegt.

## Rueckruf (1395a REJECT, ein punkt): adapter+tests gut (endpunkt aus konfig, oras native, fail-closed
belegt) aber NICHT an den anwendungs-lebenszyklus angeschlossen — kein produktionsaufrufer von RegistrySource/
Resolve. Rezept punkt 4 in review-1395a.md: die echte release/anwendungsauswahl muss darueber laufen.

## Coordinator-scope-call 2026-11-06 (w203 QUESTION): production-caller-Naht erLAUBT als
begrenzte ausnahme zum write-set-text — GENAU app_broker.go:58 compose.PullImage ueber RegistrySource.
Begruendung: karten-outcome (enterprise-endpunkt in echt BENUTZT) ist sonst nicht erfuellbar; 1395a-punkt 4
fordert genau diesen caller; alternativen Karten (artifact-resolution) sind nicht angenommen. Keine weitere
fremde datei. Gegenprobe+mutant als absicherung; reviewerprueft call-graph.

## Runde 2 pruefbar 2026-11-06 (kopf ef0120aa) — ENDGULTIG

PUNKT 4 ERFUELLT. Produktionsnaht: app_broker.go:58 fuehrt compose.PullImage ueber
RegistrySource.Resolve (adapter-detour, write-set-intern; app_up_noop/operational_errors
RUHE). resolveRegistrySource seam (application_registry_source.go) lost die konfigurierte
image-loc auf repository@digest und zieht die pin gezogen; pullResolvedRuntimeImage ist die
einzelne pull-stelle. Fix: getaggte BASEHARBOR_RUNTIME_IMAGE wird in repo+tag getrennt, so
oras resolve nicht doppelt getaggtet wird. BEWEIS: e2e-zelle
(TestPullResolvedRuntimeImagePinsImmutableDigest) loest am echten caller auf konfiguriertem
endpunkt auf; MUTANTE caller-entfernt => ROT (zieht :edge:edge), gegenprobe => GRUEN
(zieht repository@sha256:...). Lauf 42132438226 TERMINAL 14 gruen / 10 skip / 0 rot am kopf
ef0120aa; ls-remote echt==head; develop VORFAHR rc=0 (drift aus #1394 ueber merge aufgelost);
akte round-2.md auf origin/main.

## Runde 2 pruefbar 2026-11-06 (kopf ef0120aa3d7)
Nachgemessen: ls-remote echt==head, develop VORFAHR (rc=0), lauf 42132438226 TERMINAL SUCCESS (14 gruen),
akte round-2.md auf main (538eb62). 1395a-punkt 4 ERFUELLT: productions-caller app_broker.go:58 ueber
RegistrySource.Resolve, mutante caller-entfernt ROT, gegenprobe GRUEN (diskriminierung belegt).

## Rueckruf (1395b REJECT, drei punkte): lauf gruen, ABER (1) develop f01d2fb kein vorfahr
(alter basis-punkt), (2) caller-zelle ohne diskriminierung — echter caller-entfernung bleibt gruen,
(3) diff-hinweis app_broker_registry_p*. Akte folgt von Luna (quota-nachlieferung). Rezept steht (w210).

## Runde 3 pruefbar 2026-11-06 (kopf 2f073f5149b)
Nachgemessen: ls-remote echt==head, develop f01d2fb VORFAHR (rc=0, merge 4304d828), lauf 42152771162
TERMINAL SUCCESS (17/0/7) am exakten kopf, akte round-3.md auf origin/main. Caller-diskriminator
verschwaerft auf echten produktiven caller (app_broker.go:58): mutante ROT, gegenprobe gruen, scope
name-only cmd/baha.

## Rueckruf (1395c REJECT): caller faengt den fail-closed-fehler des resolvers und gibt die
mutable ursprungs-reference zurueck => un-gepinnter pull trotz verweigertem/oeffentlichem endpoint.
Zelle prueft nur erfolg-pfad. Rezept 59-85: fehler propagieren + drei negetivzellen (failed resolve =>
null pulls) + mutante gegen die fallback-zeile.

## Runde 4 pruefbar 2026-11-06 (kopf 99b3e144dd5)
Nachgemessen: ls-remote echt==head, develop VORFAHR rc=0, lauf 42168126290 TERMINAL SUCCESS am exakten
kopf, akte round-4.md auf origin/main. Resolver-ausnahme wird am caller propagiert (kein mutable
fallback), vier negetivzellen (failed/denied/public-default/missing-digest) mit NULL pulls, mutante M1
echt rot + gegenprobe gruen, opt-in klassen-exklusiv.

## Rueckruf (1395d REJECT, duennster art): inhalt + alle vier null-pull-zellen bestanden; nur die
missionserwartung 'ein mutant rotaend alle vier' traf die schicht-architektur nicht (3/4, die vierte haengt
an eigener wache). Rezept: je-schicht-diskriminierungstabelle, kein code-umbau.

## Runde 5 pruefbar 2026-11-06 (kopf 99b3e144dd5, andering = akte)
Nachgemessen: ls-remote echt==head, develop VORFAHR rc=0, lauf 42168126290 TERMINAL SUCCESS am kopf,
akte round-5.md auf origin/main (commit 3b4cf51). 1395d-punkt erledigt durch JE-SCHICHT-MATRIX: M1 =>
resolver-faelle 3x rot, public-default-zelle fuehrt ihren eigenen schicht-mutanten M7 (opt-in gate :337,
pull-liste rot, rueckgabe+gegenprobe gruen, git-diff in akte). Berichtigungszeile missions-erwartung
drin (KOORD 2026-11-06).

## ACCEPT 2026-11-06 (1395e je-schicht-matrix bestaetigt): merge UNTERWEGS (kopf 99b3e144dd5); schliesst bei develop-beleg.

## Gemerged 2026-11-06 (CODEX-MERGE nach 1395e ACCEPT): kopf 99b3e144dd5, develop ea656d1fcfc.
Dritte Runde naechste stufe: diskriminierungsmatrix je schicht statt ein-mutant-fuer-alle; beide mutanten
(M1/M7) von der pruefinstanz selbst nachgebaut.

---
id: t-20261018-r27-candidate-contract
card_number: "0427-017"
card_short_title: "define immutable source and"
areas: [architecture]
type: architecture
release: v0.4.27
version: ""
parent: core-777
priority: critical
owner: Owner + ChatGPT
kanban_lane: closed
kanban_summary: "Define only the minimal Baha app/target/consent binding around existing Git revisions, OCI images/artifacts/layouts and native…"
kanban_status: closed
kanban_title: "0427-017 · define immutable source and"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261018-r27-delivery-boundary]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1355"]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/41834568460", "https://github.com/mcpdev80/baseharbor/pull/1355", "https://github.com/mcpdev80/baseharbor-demo/actions/runs/41842881810", "https://github.com/mcpdev80/baseharbor-demo/pull/128"]
---

- [x] t-20261018-r27-candidate-contract · Deployment: define immutable source and image submission #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/architecture #kind/architecture
    <!-- generated:card -->
    **Owner:** Owner + ChatGPT · **Priority:** critical  
    **PR:** [baseharbor#1355](https://github.com/mcpdev80/baseharbor/pull/1355)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/41834568460), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1355), [proof 3](https://github.com/mcpdev80/baseharbor-demo/actions/runs/41842881810), [proof 4](https://github.com/mcpdev80/baseharbor-demo/pull/128)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261018-r27-delivery-boundary](t-20261018-r27-delivery-boundary.md)  
**Required by:** [t-20261018-r27-app-binding](t-20261018-r27-app-binding.md), [t-20261018-r27-candidate-pack](t-20261018-r27-candidate-pack.md), [t-20261018-r27-registry-access](t-20261018-r27-registry-access.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md), [t-20261104-r27-consent-abort-leaves-undestroyable-state](t-20261104-r27-consent-abort-leaves-undestroyable-state.md)  
**Owner:** Owner + ChatGPT  
**Priority:** critical  
**PRs:** [baseharbor#1355](https://github.com/mcpdev80/baseharbor/pull/1355)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Define only the minimal Baha app/target/consent binding around existing Git revisions, OCI images/artifacts/layouts and native Compose/Quadlet (later Helm/Kustomize/Kubernetes) release inputs. A candidate is an exact submission, not a proprietary compulsory bundle, catalog, archive protocol or new lifecycle service. Readable release/component versions map to actual artifact references; Git revision may be unknown or absent and OCI annotations alone are not verified provenance. Root/complete environment contracts remain existing intent authority; no stage DSL. Separate local source build from consumption of an existing CI-produced release: release consumption/promote never builds. Adopt native build context/archive/registry APIs and feature-detect versions; bound paths/symlinks/bytes/credentials using existing owners. Builder, runtime, capability and delivery remain separate. Direct versus externally reconciled delivery is explicit; native lifecycle differences/downtime and application-owned schema migrations are stated without false atomicity/rollback guarantees.

Make the migration responsibility boundary normative in the product specification and DE counterpart, with input/negative fixtures: the application or its existing migration tool owns schema changes and compatibility evidence; Baha checks only the applicable declared prerequisites it can actually verify. Missing required evidence blocks that applicable operation; a backup never proves schema compatibility, and an image rollback never implies database rollback. Do not imply automatic compatibility inference, migration execution or a generic migration engine. Define the minimal extension of existing environment-keyed deployment release/configuration records for stage-versions; reuse existing source/applied/observed fields instead of inventing a new stage axis.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

Existing product specifications for application/artifact/delivery boundaries plus DE counterparts; minimal existing internal/delivery/application input records/fixtures as required after accepted standards mapping. Replace the earlier reservation for a standalone contracts/deploymentcandidate/v1 protocol: it is not an authorization to create a mandatory new package format. Shared indexes remain public-surfaces/docs. No generic format/engine without a separately reviewed demonstrated gap.
## Required checks

Record/golden validation; malformed/digest/path/secret-reference fixtures; docs/EN-DE only. Use existing trusted contract/docs/package checks for this prerequisite; acceptance must not wait on downstream ci-lanes. Any genuinely missing contract-check route is resolved explicitly before assignment, without self-exemption. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.


## Coordinator-Scope-Vermerk 2026-11-03 (Consent-Design, dokumentierte Erweiterung)
Review-1355d-Befund 4 (Scope) wird hiermit kartenseitig geheilt: Die Consent-Implementierung
(Paar zu Befund 1-3) erfordert und erhielt Coordinator-Freigabe für erweiterte Write-Punkte:
cmd/baha (Consent-Consumer + --confirm-candidate), internal/deployment (additives Feld
CandidateConsent{by,at,digest} auf DeploymentRecord, nil=Altrecord), CLI-/Spec-Index-Zeilen.
Begründung: Karte Line 50 erlaubt minimal existing internal/delivery/application records/fixtures;
die Consent-Bindung an den Canonical-Digest ist Karten-Akzeptanzkriterium (acknowledged=true an
identität gebunden) und ohne Consumer-Feld nicht erfüllbar. Keine Produkt-Umbauten außerhalb
dieser Punkte; alles Weitere bleibt Karten-scope.

## Coordinator-Block-Vermerk 2026-11-03 22:55 (w69 final, plattenbelegt)
- Kandidat 1662ebcb: 29/32 Gates terminal GRUEN (run 4608-系, ls-remote==claim). Einzige Ausnahmen:
  echte docker/podman lifecycle-Jobs — reproduzieren IDENTISCH auf clean develop 2cadfcee (baha doctor
  NOT APPLIED, Demo-Provisioning im isolierten Runner). Kein Produktfehler des Kandidaten.
- Trigger naechster Schritt: Owner stellt Runtime-Gate-Ausfuehrung im Runner wieder her (Receipt folgt
  im Schichtprotokoll); danach rerun 1355, Review r1355h auf终stand.
- Evidenz: evidence/r27-welle3-2026-11-03/candidate-contract/fix-9-final.md (umgezogen aus Produktrepo;
  Zweig-Saeuberung laeuft als w77).


## Koordinator-Kartenvermerk 2026-11-04 (Consent-Kommandoflaeche, dokumentierte Prazisierung)
- Fakt aus lane w80 (gate-laeufe): derselbe submission-input ergibt je nach befehlroute UNTERSCHIEDLICHE
  confirm-digests (up: d998a895... vs app apply: 4bc64030...). Ein gate, der im selben fluss nicht erfullbar
  ist, widerspricht dem vertrag (explizite, bedienbare zustimmung).
- Prazisierung der CLI-Oberflaeche: `baha up` erhaelt --confirm-candidate durch DIESELBE parsing-/consent-
  route wie app apply (kein zweiter gate, keine neue semantik). Digest-pfad-abhaengigkeit bleibt als
  neutraler fakt in der evidence der lane; sollte der fingerprint die befehlroute enthalten, ist das
  nachpruefungswuerdig gegenueber "canonical submission fingerprint" (vermerk, kein verdict).

## Status correction (2026-11-04, Owner verification)

The previous blocker referring to the isolated GitHub runner and baseline develop `2cadfcee` was stale and has been replaced; it is historical, not a current CI defect.

Verified on GitHub (2026-11-04): Core PR [#1355](https://github.com/mcpdev80/baseharbor/pull/1355) is open (head `ffe27712f25b75418a356ac37caec0bb9ae1fbdd`); Demo guided-consent PR [#128](https://github.com/mcpdev80/baseharbor-demo/pull/128) is open (head `5b1f6e92cbb352551dbb3d928edb2b142ca90c8d`). Core PR workflow `41834568460` was still running at inspection time; normal PR validation does **not** establish native cross-repository runtime compatibility.

**Unblock criteria:** finish/merge the compatible consent change as appropriate, qualify the exact resulting Core and Demo revisions through genuine hosted Docker **and** Podman lifecycle checks (no skipped result or substituted PR-local test), and record the exact SHA/run/outcome. Then review and accept the candidate-contract task separately; no release/tag is implied. Development and unrelated PR merges must not be held up by this cross-repo acceptance pending state.

## Owner takeover 2026-11-04 (coordinator f49a3303)
- Owner and ChatGPT work this card from now on. Coordinator lanes do not edit, review, merge or re-base this
  branch (work/r27-candidate-contract, PR #1355, head ffe27712 at the time of handover).
- Withdrawn: the queued Codex final review mission for this candidate (kept in
  coordinator/missions/archive/codex-r1355i.BEHALTEN-owneruebergabe.txt, not executed).
- Board effect: the six cards waiting on this card stay waiting; their unblock trigger is the Owner merge, not a
  coordinator action.

## Owner acceptance (2026-11-04)

**Accepted as the self-contained candidate submission contract** (not a release approval):
- Core candidate/consent PR [#1355](https://github.com/mcpdev80/baseharbor/pull/1355) merged into develop at `ecbb88545f96473986f8f41394cffce58b97d2df`; current-head trusted PR CI [41834568460](https://github.com/mcpdev80/baseharbor/actions/runs/41834568460) passed.
- Demo consent consumer PR [#128](https://github.com/mcpdev80/baseharbor-demo/pull/128) merged into main at `c355d2a15f5b6b67ec665e8d9e1be863f4090831`; the exact-source hosted demo test [41842881810](https://github.com/mcpdev80/baseharbor-demo/actions/runs/41842881810) passed after fixing fake-Core fixture counter isolation (4 fixture tests plus 11 fail-closed guided decision-path tests).
- Demo `baseharbor-core.ref` now pins the actual merged Core `ecbb88545f96473986f8f41394cffce58b97d2df` rather than the superseded branch commit.
- **Not claimed:** native Docker/Podman lifecycle success, OpenBao runtime readiness, Console/Connector compatibility, or release qualification. Those remain develop/release integration acceptance, and cannot retroactively hold the independently validated candidate-contract prerequisite blocked. Do not treat ordinary green PR CI as native runtime evidence.
- Supersedes the stale historical blocker and the outdated 2026-11-04 pre-merge status notes above. The Maintainer authorizes closing this product contract prerequisite only.

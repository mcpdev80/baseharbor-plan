---
id: t-20261018-r27-client-commands
card_number: "0427-022"
card_short_title: "route init up status and"
areas: [cli]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: owner
kanban_lane: closed
kanban_summary: Ordinary local/remote commands call same semantic operations. init writes portable contract locally and explicit registration…
kanban_status: closed
kanban_title: "0427-022 · route init up status and"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-artifact-resolution, t-20261018-r27-candidate-ingress, t-20261018-r27-connection-client, t-20261018-r27-device-lifecycle, t-20261018-r27-journal-wiring, t-20261018-r27-management-host, t-20261018-r27-stage-versions, t-20261018-r27-team-auth, t-20261022-r27-ci-authority]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1420]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-07/client-commands/round-1.md"]
---

- [x] t-20261018-r27-client-commands · CLI: route init up status and operations through one authority #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** owner · **Priority:** normal  
    **PR:** [baseharbor#1420](https://github.com/mcpdev80/baseharbor/pull/1420)  
    **Needs:** [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-07/client-commands/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-artifact-resolution](t-20261018-r27-artifact-resolution.md), [t-20261018-r27-candidate-ingress](t-20261018-r27-candidate-ingress.md), [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md), [t-20261018-r27-device-lifecycle](t-20261018-r27-device-lifecycle.md), [t-20261018-r27-journal-wiring](t-20261018-r27-journal-wiring.md), [t-20261018-r27-management-host](t-20261018-r27-management-host.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md), [t-20261018-r27-team-auth](t-20261018-r27-team-auth.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md)  
**Required by:** [t-20261018-r27-access-wizard](t-20261018-r27-access-wizard.md), [t-20261018-r27-maintenance-client](t-20261018-r27-maintenance-client.md), [t-20261018-r27-node-cli](t-20261018-r27-node-cli.md), [t-20261018-r27-onboarding-wizard](t-20261018-r27-onboarding-wizard.md)  
**Owner:** owner  
**Priority:** normal  
**PRs:** [baseharbor#1420](https://github.com/mcpdev80/baseharbor/pull/1420)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Ordinary local/remote commands call same semantic operations. init writes portable contract locally and explicit registration binds remotely; up submits exact candidate and scoped consent; status/doctor/logs resolve server-owned state; maintenance submission belongs to the later maintenance-client slice. Discovery reports unsupported ops, no raw arbitrary server paths or secret args. Keep quick safe detection behavior; no video-specific env flag. This slice owns normal init/up/read dispatch only; do not add maintenance handlers.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

cmd/baha/main.go dispatch seam; bounded remote command adapter files/tests; no commands.go or machine registry edits. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Real CLI->TLS API tests with two independent homes/checkouts, same deployment, precedence, denial, server loss, stale consent and error parity. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

ready erreicht (alle 10 deps inkl management-host akzeptiert); bahn auf laptop dispatched; write-set cmd/baha/main.go dispatch-naht + adapter, disjunkt zu 117 deployment_record.go.

r2 geliefert+verifiziert: head 0c23adc56 auf eee11d50 (ancestor rc0), MERGEABLE, cli-package-tests+selected checks GRUEN, delta=NUR client_commands_behaviors_test.go (kein produktcode). root-cause der r1-CI-rote war ein os.Chdir-leak der lane (behoben mit t.Chdir), mein #1419-vs-#1420-zeugnis war richtig. 5 behaviours (3 cite existing, 2 neu) — review prueft echt-zwei-home-TLS + dass cites nicht luft sind. skipped docker/podman=owner ci-gate.

CODEX act-1420a REJECT_LANE_FIX: die 5 tests sind SIMULIERT (application_core_authority_test.go no-TLS fixture + helper-direct calls), nicht echt-zwei-home-CLI->TLS. reviewer-akte 90d8441b. lane repariert r3: echter TLS-server + echtes CLI ueber zwei homes je behavior; CI-tauglich ueber in-prozess httptest TLS, vm-infra nur als befund. 117-r6 parallel busy.

head 4293b8803 delivered+hosted gruen (10 pass), war fuenf runden ohne abnahme liegen gelassen — coord-versehen, jetzt CODEX-REVIEW. prueft v.a. ob gated core-integration test vorhanden ist.

CODEX request-changes: nativer core-gegate start/consent/denial test + TLS status/restore proof FEHLEN. + CI-Aufnahme-blocker ci.yml:255-256 (pull_request excluded) & 342-349 (allowlist omits). korrektur in FRISCHE lane, .github-bedarf als BEFUND an owner.

r2 fresh-lane delivered: native-gated core-integration test + in-process TLS roundtrip, CI 10 pass, develop ancestor. BEFUND runtime_integration .github:349 push-only (owner). CODEX-REVIEW dispatcht.

r3: lane-side quality fixes (kein assumeVerifiedCore bypass, realer status/restore roundtrip) parallel; finale CI-gruen abhaengig von owner ci.yml-allowlist.

r3 fresh lane d5ab38d0: product-quality fixes (kein assumeVerifiedCore bypass, realer status/restore roundtrip). Finale CI-Aufnahme haengt an OWNER ci.yml-allowlist (255-256/349) - lane-reportet befund, aendert NICHT .github.

## Owner-Abgleich — 2026-11-07

- **PR #1420 gemergt**: `c8a79faff91cd870ac3904a2a392922a24cc7e13` (PR workflow 42374687508 SUCCESS). **PR #1426 gemergt**: `3089edbc9eb34f47b58865f5c5dc7ca796ec9f0c` (PR workflow 42375618947 SUCCESS).
- Die alte behauptete Owner-Sperre `ci.yml:256/349` ist **nicht mehr zutreffend**: die bestehende PR-Pruefung `cli-package-tests` fuehrt `go test ./cmd/baha -count=1 -json` aus. #1426 verlangt ausdruecklich PASS fuer alle fuenf `TestClientCommands*`-Faelle, falls die Testdatei vorhanden ist; ohne eigene Parallel-Pipeline.
- Exakter Post-Merge-Lauf: [source-preflight 42375856513](https://github.com/mcpdev80/baseharbor/actions/runs/42375856513). Noch keine Freigabe allein aus package-Gruen: der verlangte reale CLI->TLS/Core-Nachweis und notwendige Native-Acceptance sind eigenstaendig zu pruefen. **Blocked** bis diese Evidenz wirklich vorliegt; kein Scheingruen und kein Release.

MERGED von owner (c8a79faff) + owner ci-fix 27d2c0918 (require five client-command PASS) loeste den CI-blocker selbst.

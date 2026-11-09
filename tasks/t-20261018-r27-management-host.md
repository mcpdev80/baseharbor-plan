---
id: t-20261018-r27-management-host
card_number: "0427-036"
card_short_title: "run one durable minimal"
areas: [remote]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: 0427-036-base-refresh
kanban_lane: closed
kanban_summary: Expose the same existing lifecycle executor on a protected management host with one durable state root and active-writer…
kanban_status: closed
kanban_title: "0427-036 · run one durable minimal"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-device-lifecycle, t-20261018-r27-journal-wiring, t-20261018-r27-state-owner, t-20261018-r27-team-auth, t-20261022-r27-ci-authority]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1405]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1405"]
---

- [x] t-20261018-r27-management-host · Management: run one durable minimal authority on the selected host #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/remote #kind/task
    <!-- generated:card -->
    **Owner:** 0427-036-base-refresh · **Priority:** normal  
    **PR:** [baseharbor#1405](https://github.com/mcpdev80/baseharbor/pull/1405)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1405)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-device-lifecycle](t-20261018-r27-device-lifecycle.md), [t-20261018-r27-journal-wiring](t-20261018-r27-journal-wiring.md), [t-20261018-r27-state-owner](t-20261018-r27-state-owner.md), [t-20261018-r27-team-auth](t-20261018-r27-team-auth.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md)  
**Required by:** [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md)  
**Owner:** 0427-036-base-refresh  
**Priority:** normal  
**PRs:** [baseharbor#1405](https://github.com/mcpdev80/baseharbor/pull/1405)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Expose the same existing lifecycle executor on a protected management host with one durable state root and active-writer ownership. Reconcile the present operator API PostgreSQL/OIDC requirements explicitly: ordinary local use remains no-login and service-free; remote management provisions only its genuine authentication/state dependencies, not an unconditional SQL/Secrets/Identity bundle. Configure least-privilege host/runtime access, persistent service/storage and explicit bootstrap versus attach. Verify installed lifecycle state survives service restart. No HA replica/federation or container socket exposure to clients.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

cmd/baha/serve.go; internal/controlplaneruntime/server.go and server_run.go; bounded management-host/service bootstrap files and tests. No other task owns these files concurrently; shared command/contract registrations remain with public-surfaces.

## Required checks

Focused server-config/auth/startup/ownership/restart tests; one isolated service persistence smoke if required. CLI clients use discovery and the accepted host API; no new product-specific transport. No automatic full matrix or self-approved trust exemption.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Entriegelt 2026-11-06: alle vorlaeufer (geraete-lebenszyklus, tagebuch-kette ausnahme: laeuft noch runde-3-basisRefresh) gemergt. Claimbereit.

bahn nach system-reboot frisch beauftragt (takeover der toten lane), konfliktfreie produkt-/testarbeit unter aufgehobenem basis-HOLD (develop 934be499b), .github weiterhin owner-tabu

verhaltens-rotnachweis (letzter CODEX-blocker act-1405a) ist auf main erfuellt (round-6-redfirst.md, sick 64d93e94 verhaltens-ROT / cand 0f08b877 GRUEN, mutation L0==L2); die frisch beauftragte red-first-bahn war ueberfluessige doppelarbeit der durch reboot gestorbenen w289 und wird freigegeben; kopf 0f08b877 pflicht-ci ohne rot. CODEX-REVIEW act-1405b dispatcht.

CODEX act-1405b REJECT: rotnachweis+CI ok, aber neuer echter code-defekt cmd/baha/serve.go:41-43/97-103 (startup bleibt bei RuntimeAppName!=nil -> nil-context). frische korrektur-bahn 0427-036-serve-startup auf freiem ornith-sitz dispatcht (rezept= startup:=ctx + regression RuntimeAppName!=..).

korrektur geliefert: head 5b8d0f5745 auf develop 934be499b (drift behoben), startup ctx-init in BEIDEN zweigen, regression nil-ctx server_run.go:369 ROT-ohne-fix/GRUEN-mit-fix, ci 42336074504 TERMINAL success, round-8 akte auf main. erfuellt act-1405b rezept -> re-review act-1405c dispatcht.

codex act-1405c REJECT NUR wegen basis-ahnenschaft (serve.go-fix + regression ACCEPTED, ci terminal success); merge-base dddf0d782, develop 934 nicht Vorfahr. leichte mechanische basis-auffrischungs-bahn dispatched (flash), kein neuer code.

basis-auffrischung geliefert: head 6014a8fc, is-ancestor 934 rc0, produktcode identisch zu acceptedem 5b8d0f5745 (nur develop-merge), ci 10 success/0 fail, round-9 akte auf main. gegenprobe act-1405d.

CODEX act-1405d ACCEPT + act-1405e MERGE in develop (66310729e1789a59e3025fcbfb270015f83b8d08); serve.go startup nicht-nil beide zweige + regression; basis-auffrischung auf develop gebracht; gemergt.

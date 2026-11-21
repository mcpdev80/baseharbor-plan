---
id: t-20261120-cli-operator-entrypoints
card_number: "0428-204"
card_short_title: "CLI operator entry points"
type: bug
areas: [cli, security]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: wait
kanban_lane: wait
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-204 · CLI operator entry points
priority: high
depends_on: [t-20261120-r28-cli-shard-operator-env]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1726]
sources: []
blocker: ""
wait_reason: "#1726 exact head e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4, run 44867737078, remains red: cli-0 fails TestAppListAllTargetsWorksAfterInstallationDestroy (separate 0428-210/#1739); packages fails the Loki trio (0428-212/#1734); Native Keycloak/Core Docker/Podman and selected Docker Guided still fail before 0428-209's fix is included. The direct root.Execute secure-profile fixture was corrected on this exact head and its focused test passes, but card acceptance requires all four CLI shards green. 0428-209's later stacked run 44868911131 proves the native bootstrap fix, not the #1726 base PR. Resume after 0428-210/#1739, 0428-212/#1734, and 0428-209 are integrated in dependency order; #1615 remains another session's work."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1726", "https://github.com/mcpdev80/baseharbor/actions/runs/44867737078", "https://github.com/mcpdev80/baseharbor/pull/1739", "https://github.com/mcpdev80/baseharbor/pull/1734"]
---

- [ ] t-20261120-cli-operator-entrypoints · 0428-204 · CLI operator seam: MCP handlers and direct Run entry points #task #release/v0-4-28 #status/wait #view/wait #area/cli #area/security #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    **PR:** [baseharbor#1726](https://github.com/mcpdev80/baseharbor/pull/1726)  
    **Waiting:** \#1726 exact head e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4, run 44867737078, remains red: cli-0 fails TestAppListAllTargetsWorksAfterInstallationDestroy (separate 0428-210/\#1739); packages fails the Loki trio (0428-212/\#1734); Native Keyclo…  
    **Needs:** [t-20261120-r28-cli-shard-operator-env](t-20261120-r28-cli-shard-operator-env.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1726), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44867737078), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1739), [proof 4](https://github.com/mcpdev80/baseharbor/pull/1734)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-r28-cli-shard-operator-env](t-20261120-r28-cli-shard-operator-env.md)  
**Required by:** [t-20261120-other-domain-test-split](t-20261120-other-domain-test-split.md), [t-20261121-all-targets-config-loss](t-20261121-all-targets-config-loss.md), [t-20261121-app-edit-core-activation](t-20261121-app-edit-core-activation.md), [t-20261121-destroy-authority-stamp](t-20261121-destroy-authority-stamp.md), [t-20261121-mcp-operator-seam-uncovered](t-20261121-mcp-operator-seam-uncovered.md), [t-20261121-native-cell-operator-seam](t-20261121-native-cell-operator-seam.md), [t-20261121-trust-uninstall-false-green](t-20261121-trust-uninstall-false-green.md)  
**Owner:** coordinator  
**Priority:** high  
**PRs:** [baseharbor#1726](https://github.com/mcpdev80/baseharbor/pull/1726)  
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


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
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

## Why

0428-198 delivered an in-test operator identity seam (head 7546b1806aac, 8 files) and proved it fires on the
`runWithIO` path. The lane's round-3 dossier (`evidence/r28-welle4-2026-11-20/cli-shard-operator-env/round-3.md`)
records that this does not reach every way a test enters the product: MCP tool handlers connect through
`server.Connect`/`client.Connect` and `CallTool` with their own contexts, and several tests call the command
object directly (`rootCommand().Execute(ctx)` / `.Run(ctx)`) instead of through `runWithIO`. Those call sites
never receive `operatorauth.WithEnforcement`, so they keep failing with the managed-environment operator
message in `PR · Go unit · cli-0..3`.

## What

1. Enumerate the entry-point classes that reach enforcement-relevant production code from `cmd/baha` tests,
   using the gate map (`cli-shard-operator-env/gate-map-1.md`) as the starting list and `git grep` to refresh it.
2. Make the seam apply for each class, in one place per class, keeping the required order
   (`WithEnforcement` -> `WithVerifiedPrincipal` -> `WithMembershipProvider`) exactly as 0428-198 established it.
3. Keep production behaviour unchanged: the seam stays nil outside tests, asserted by one test.

## Acceptance

- `PR · Go unit · cli-0`, `cli-1`, `cli-2`, `cli-3` pass at the exact head with no operator message in their logs.
- `internal/operatorauth/**` decision logic untouched (no `policy.go`, no `authorization.go` edits).
- One evidence table line per entry-point class: class, file:line, before (failing test), after (passing test).

KARTE AUS DIESEM TICK GECASTET (fund->karte, §3.3.5): der befund von w198 lautet, der seam erreicht MCP-handler (server.Connect / client.Connect / CallTool mit eigenen kontexten) und direkte .Run(ctx)/Execute(ctx)-aufrufe NICHT. sitz w216-0428-204-entrypoints (laptop) UEBERNIMMT den stand refs/heads/lane-0428-198-cli-shard-operator-env head 7546b1806aac (PR #1726, seam auf dem runWithIO-pfad bewiesen, [w198-seam]-print in akte round-3.md) und liefert: auflistung pro eintrittsklasse mit zaehl-befehl, eine stelle pro klasse, kleiner gate go test ./cmd/baha/ -count=1 vorher/nachher, und eine assertion, dass der seam ausserhalb von tests nil bleibt. rail-dateien verschlossen; ein zwang zu internal/serviceaccess/** = STOP + MELDEN.

MEASURED PROGRESS, NO REMOTE WITNESS: the lane reports ./cmd/baha operator failures 206 -> 121 -> 42 from local runs, and answers the H-V23 rubrik question with '0 sites left unstamped, 0 new content witnesses, every stamp rides a pre-existing content assertion'. But 'git ls-remote lane-origin refs/heads/lane-0428-204-cli-operator-entrypoints' returns NOTHING and #1726 head is still bf6f10aff6fe: the work exists only in its working tree, and no akte exists on plan main. Card stays active (work IS happening) — I ordered a push first, then the akte, then the remaining 42 grouped by file with an explicit way-(a)/way-(b) decision per group, and I asked for the count of unstamped sites plus one probe file:line so the claim is checkable at review instead of taken on trust (§5.3). If the next report has no remote witness, I rotate the card to a fresh lane on the same branch with a documented handoff (§3.6).

w216 liefert die zwei zahlen, die der owner fragte: 29 operator-fehler auf develop-head, 0 auf develop plus inhalt von #1615 (single-test-oracle; der volle check an #1615 scheiterte an meinem host (/tmp quota), nicht am inhalt). PR #1726 reduziert auf H-V23 core_installation_runtime_test.go:323 plus geteilte-session MCP-faelle durch den zentralen helper; die zwei eigenen per-call-stamps nimmt die lane zurueck. restarbeit = klasse B (81 direkte .Run/fixture-stellen aus der deckungskarte b7dce1ee), frische lane im anlauf.

RESIDUAL-KLARSTELLUNG NACH ZWEI METHODEN: die statische deckungskarte (b7dce1ee/c7d7076d, 206 FAIL-ZEILEN am develop-stand, A=80/B=81/C=10/D=10) und die log-basierte inventur (round-2 der 206-lane, 117 FIRST-LEVEL-NAMEN gegen den #1615-head, 115/117 transitiv gestempelt) sagen beide: der OPERATOR-AUTH-GATE heilt durch #1615. empirischer zeuge: run 44854729670 (#1615, head 7fae3a288f4a) zeigt cli-0..3 = SUCCESS, packages = SUCCESS, owner = SUCCESS. die klasse B(81) ist damit NICHT 'restarbeit nach #1615', sondern 'arbeit falls #1615 nicht kommt'. diese karte bleibt in 'review' mit #1726 als kandidat; ihre eigene korrektur ist die ruecknahme der zwei per-call-stamps (akte 15ea9228).

Ergaenzung zu C8 aus dem supersession-desk (round-1.md, plan 88a6b2fb): die KETTE haengt an dieser karte, aber ihre PRS zeigen pro vertrag auf genau EINEN PR (#1726). Die nachfolger, die auf dem branch dieser karte stapeln: #1737 (0428-213, head 5be4f003aa1b) und #1738 (0428-214, head bdc3fcb63912) — merge-reihenfolge also #1726 -> #1738/#1737. Basis-head zuletzt 80dc4987993b (owner-push 05:36, vierter innerhalb von 47 minuten).

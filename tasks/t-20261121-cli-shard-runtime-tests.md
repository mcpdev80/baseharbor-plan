---
id: t-20261121-cli-shard-runtime-tests
card_number: "0428-215"
card_short_title: "0428-215 cli runtime tests"
type: bug
areas: [ci, cli]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: wait
kanban_lane: wait
kanban_summary: "The PR · Go unit · cli- shards contain no test whose pass condition requires a container runtime, ORAS, or memory that the…"
kanban_title: 0428-215 · 0428-215 cli runtime tests
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1743]
sources: []
blocker: ""
wait_reason: "Exact run 44878727267 at 57e7941772ce85dbc60bad7faddd3613c3191c4c is terminal. The new regression PASSes without skip in both existing Docker and Podman native cells. Both jobs then fail in a separate existing TestControlPlaneSingleDefaultNativeRuntimeInCI because its integration target is not configured; all four cli shards also fail inherited managed-operator-auth fixtures owned by the separate #1615 session, and the planner-tests validation fails. Required aggregate checks are red, so acceptance/closure is not truthful yet. Exact logs and test-to-gate mapping: ../evidence/r28-welle4-2026-11-21/cli-shard-runtime-tests/round-8.md."
resolution: ""
evidence:
  - "https://github.com/mcpdev80/baseharbor/pull/1743"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44875389702"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44875693455"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44876072403"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44876725420"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44877364076"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44877777956"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44878287581"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44878727267"
  - "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/cli-shard-runtime-tests/round-8.md"
---

- [ ] t-20261121-cli-shard-runtime-tests · 0428-215 Go-unit cli shards run tests that need a real runtime #task #release/v0-4-28 #status/wait #view/wait #area/ci #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    **PR:** [baseharbor#1743](https://github.com/mcpdev80/baseharbor/pull/1743)  
    **Waiting:** Exact run 44878727267 at 57e7941772ce85dbc60bad7faddd3613c3191c4c is terminal. The new regression PASSes without skip in both existing Docker and Podman native cells. Both jobs then fail in a separate existing TestControlPlaneSingleDefault…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1743), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44875389702), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44875693455), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44876072403), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/44876725420), [proof 6](https://github.com/mcpdev80/baseharbor/actions/runs/44877364076), [proof 7](https://github.com/mcpdev80/baseharbor/actions/runs/44877777956), [proof 8](https://github.com/mcpdev80/baseharbor/actions/runs/44878287581), [proof 9](https://github.com/mcpdev80/baseharbor/actions/runs/44878727267), [proof 10](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/cli-shard-runtime-tests/round-8.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** coordinator  
**Priority:** high  
**PRs:** [baseharbor#1743](https://github.com/mcpdev80/baseharbor/pull/1743)  
**Source:** 
<!-- /generated:links -->

## Goal

The `PR · Go unit · cli-*` shards contain no test whose pass condition requires a container runtime, ORAS, or memory that
the hosted runner does not have. Each such case either states an explicit skip witness on the runner, or is covered by the
native Runtime workflows where the capability exists.

## Why

w222 measured this while delivering 0428-142 (akte
`evidence/r28-welle4-2026-11-20/perses-status-backend-witness/round-2.md`, "CI run watch"): the failing required jobs of run
44841239916 are the Go-unit DB shards `cli-0..3` and `packages`, and the failing tests it names are
`TestRuntimeUpRequiresORASBeforeCoreBootstrap` ("container runtime orchestration not found" / no ORAS on the host),
`TestSharedBackendReconcileRejectsSecondProcess` (second-process shared-owner lock needs a real runtime),
`TestAppEditCommandCompleteProviderEditRunsRealLifecycle` (needs a real runtime) and
`TestPrepareStagedCoreGitCandidatePinsCanonicalApplication` ("native Git archive failed: signal: killed", host OOM). The lane
also proved non-regression: `bash scripts/pr-unit-database.sh cli-1` fails identically at head `6740299f9` **without** its
change.

This matters to the whole window because of a second measurement made while checking that claim: at develop
`40cb28c758b0` the only push workflows are `Runtime · Docker Core` and `Runtime · Podman Core`, **both success**
(runs 44769994971 / 44769994909). The cli shards therefore never run as a develop push; their red is only visible inside
`pull_request` runs. So "develop is red" must be stated precisely: **the Go-unit cli shards are red in PR runs against a
base containing #1717/#1594**, and part of that red is environment-shaped, not operator-auth. 0428-204 cannot fix these four
shapes by stamping.

## Scope

Owner reassignment (2026-11-21): Marcel explicitly assigned the complete Wait-card sweep except #1615, including this
coordinator-owned native CI routing. That instruction supersedes this card's former stop-and-report limit for its narrow
existing native-cell selector only.

Allowed write-set:

- `cmd/baha/operator_core_network_binding_native_test.go`: add one opt-in native regression for the foreign same-name network
  branch at `core_network_binding.go:55-57`; the `operator_` filename uses the existing base-branch owner/node selector.
- `scripts/ci-owner-node-native.sh`: require the new test on both existing Docker and Podman native cells.
- This task note and its evidence.

No other workflow, runner, framework, or runtime infrastructure changes. Do not modify `internal/operatorauth/**`,
`internal/identityprovider/**`, `internal/serviceaccess/**`, the existing four runtime tests, or any assertion outside the
new regression. Do not add local skip behavior or weaken a test to make a Go shard pass.

## Acceptance criteria

1. `PR · Go unit · cli-0..3` and `packages` no longer fail because of missing ORAS, a missing real runtime, or an OOM kill.
2. Every skipped case prints a skip witness naming the missing capability, and the akte states which native gate covers it.
3. `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` executes, with skips rejected, in both existing
   `PR · Native Keycloak/Core · docker` and `PR · Native Keycloak/Core · podman` cells at the exact candidate SHA.
4. The existing base-branch `operator_` path selection routes the test to those cells, and
   `scripts/ci-owner-node-native.sh` checks the exact test ID on both runtimes. The planner and workflow policy checks
   pass at the exact candidate SHA.
5. Before/after job conclusions with run ids are quoted from two different PRs (one of them #1733 or #1734, whose only red is
   the inherited shards).

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | `PR · Go unit · cli-0..3`, `PR · Go unit · packages`; foreign-network regression additionally covered by `PR · Native Keycloak/Core · docker|podman` |
| Test identifier | `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` (plus resource-test inventory in evidence) |
| Route | existing native owner/node gate; exact test required on both runtimes |

## Dependencies

None by contract, but sequence behind 0428-204 while that lane writes in `cmd/baha/` - the four files above are inside its
work area.

## Runtime boundary

Use the existing owner/node native job and its Docker/Podman runners. Do not install a daemon in ordinary Go-unit shards,
add a new job or workflow, or turn a daemon-dependent assertion into a skip.

## Handoff

Branch `codex/0428-215-native-network`, PR #1743. Run 44877364076 at `c506624d14e3c6939c204da12926cd0416daf3ca` proves Docker PASS and Podman FAIL despite direct inspect confirming the expected network name and both Compose labels; see evidence round-6. Run 44878287581 at `fc79b74627d12fd7c5096621069480861069797e` diagnosed the Podman fixture XDG-store mismatch; evidence is in round-7. Latest candidate head `57e7941772ce85dbc60bad7faddd3613c3191c4c` aligns direct fixture commands with BaseHarbor’s existing Podman environment, and exact run 44878727267 is queued. Run 44878727267 is terminal: the new regression PASSes without skip on both Docker and Podman. Both native jobs then fail at the separate existing TestControlPlaneSingleDefaultNativeRuntimeInCI because the integration target is not configured; all cli shards fail inherited managed-operator-auth fixtures on the #1615-owned shared gate, and planner-tests validation is red. The required aggregate remains red. Round-8 evidence records exact test -> native cell -> run and current gate. The code-level/native-test objective is proven; card/PR closeout still requires exact required checks to pass after upstream shared gates resolve.

2026-11-21 owner reassignment: the coordinator's round-2 evidence identified a real missing native assertion and exact
existing gate. Per the Maintainer's Wait-sweep directive, this lane owns only the required test in that existing gate; it
does not add CI infrastructure. The test filename uses the already-present `operator_` selector in the base workflow, so no
workflow edit is needed for the candidate to be selected.

2026-11-21 implementation: added `cmd/baha/operator_core_network_binding_native_test.go`, which creates a same-name native
network with only a forgeable Compose owner label, calls `prepareCoreDefaultNetworkBinding`, and asserts refusal without
external adoption. `scripts/ci-owner-node-native.sh` now requires that exact test on both existing Docker and Podman cells;
`scripts/test_ci_keycloak_single_route.py` verifies the base-workflow selector matches the new `operator_` filename and the
native script requires the exact test. Local selector suite: 6/6 PASS. Focused Go invocation compiles and reports the expected
opt-in SKIP because this workstation has no isolated native acceptance daemon; hosted Docker and Podman cells remain required.

kommissioniert, weil der wart-grund weg ist: #1740 zeigt am gestapelten head (run 44868911131, protokoll 900721 bytes) cli-1/2/3 SUCCESS und genau EINE erste-level-fail-zeile, die zu 0428-210/#1739 gehoert — die container-/ORAS-pflichtigen faelle ihrer karte sind an dieser basis also bereits geheilt. Lane '0428-215-cli215' (4359f0e8, laptop:2), base = 'lane-0428-198-cli-shard-operator-env' (zuletzt e45430f2f1b7, bewegt sich), gestapelt auf #1726.

round-2 delivered (plan ed88dda9/188ac1fd), red-first in benannter runner-form, keine produkt-aenderung, kein PR — diagnose as ordered.

Mein CI-bedarf war richtig adressiert, der owner war schneller als die Lanes. 'wait' ist hier ehrlich, NICHT 'blocked': kein Owner-entscheid noetig, nur ein laufender Beleg. AGENTS 5.3: skipped/queued/absent receipts sind kein pass.


Continuation 2026-11-21: after the corrected two-label fixture still failed only in Podman, the native test now captures direct runtime labels and, on refusal failure, the actual provider `InspectProjectResources` result/error. This makes the next native run diagnostic without changing product code or CI routing.


Continuation 2026-11-21: Podman direct inspect and `network ls` saw the fixture while the provider inventory did not. The test had inherited XDG isolation that the production Podman subprocess contract deliberately removes. The fixture now mirrors existing native Podman test helpers by unsetting those two variables for all direct runtime operations; see evidence round-7.


Continuation 2026-11-21: exact run 44878727267 completed. `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` passes (no skip) in Docker and Podman. Each native cell then fails a separate existing integration-target setup test; cli-0..3 fail shared operator-auth fixtures, and planner-tests validation also fails. See evidence round-8. No #1615 files or state touched.

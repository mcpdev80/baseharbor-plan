---
id: t-20261121-cli-shard-runtime-tests
card_number: "0428-215"
card_short_title: "0428-215 cli runtime tests"
type: bug
areas: [ci, cli]
release: v0.4.28
version: ""
parent: ""
owner: "Codex (Marcel, Wait sweep excluding #1615)"
kanban_status: active
kanban_lane: active
kanban_summary: "The PR · Go unit · cli- shards contain no test whose pass condition requires a container runtime, ORAS, or memory that the…"
kanban_title: 0428-215 · 0428-215 cli runtime tests
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261121-cli-shard-runtime-tests · 0428-215 Go-unit cli shards run tests that need a real runtime #task #release/v0-4-28 #status/active #view/active #area/ci #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** Codex (Marcel, Wait sweep excluding \#1615) · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Codex (Marcel, Wait sweep excluding #1615)  
**Priority:** high  
**PRs:** none  
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

- `cmd/baha/core_network_binding_native_test.go`: add one opt-in native regression for the foreign same-name network
  branch at `core_network_binding.go:55-57`.
- `scripts/ci-owner-node-native.sh`: require the new test on both existing Docker and Podman native cells.
- `.github/workflows/ci.yml`: include the test file in the existing exact owner/node native-cell selector.
- This task note and its evidence.

No other workflow, runner, framework, or runtime infrastructure changes. Do not modify `internal/operatorauth/**`,
`internal/identityprovider/**`, `internal/serviceaccess/**`, the existing four runtime tests, or any assertion outside the
new regression. Do not add local skip behavior or weaken a test to make a Go shard pass.

## Acceptance criteria

1. `PR · Go unit · cli-0..3` and `packages` no longer fail because of missing ORAS, a missing real runtime, or an OOM kill.
2. Every skipped case prints a skip witness naming the missing capability, and the akte states which native gate covers it.
3. `TestCoreDefaultNetworkBindingRejectsUnownedNativeNetwork` executes, with skips rejected, in both existing
   `PR · Native Keycloak/Core · docker` and `PR · Native Keycloak/Core · podman` cells at the exact candidate SHA.
4. The exact file selection in `.github/workflows/ci.yml` routes the new test to those cells, and
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

Branch, PR, exact head SHA, two run ids with per-shard conclusions, evidence
`evidence/r28-welle4-2026-11-21/cli-shard-runtime-tests/round-1.md`.

2026-11-21 owner reassignment: the coordinator's round-2 evidence identified a real missing native assertion and exact
existing gate. Per the Maintainer's Wait-sweep directive, this lane now owns only the selector and required test in that
existing gate; it does not add CI infrastructure. The candidate will be a small PR against current `develop`.

kommissioniert, weil der wart-grund weg ist: #1740 zeigt am gestapelten head (run 44868911131, protokoll 900721 bytes) cli-1/2/3 SUCCESS und genau EINE erste-level-fail-zeile, die zu 0428-210/#1739 gehoert — die container-/ORAS-pflichtigen faelle ihrer karte sind an dieser basis also bereits geheilt. Lane '0428-215-cli215' (4359f0e8, laptop:2), base = 'lane-0428-198-cli-shard-operator-env' (zuletzt e45430f2f1b7, bewegt sich), gestapelt auf #1726.

round-2 delivered (plan ed88dda9/188ac1fd), red-first in benannter runner-form, keine produkt-aenderung, kein PR — diagnose as ordered.

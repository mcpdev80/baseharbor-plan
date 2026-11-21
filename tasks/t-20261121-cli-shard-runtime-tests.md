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

Allowed write-set:

- the four named test files in `cmd/baha/` (guard or move their setup, not their assertions)
- the shared test-support helper that decides whether a runtime exists (report the file before editing)

Forbidden: `.github/**` and the workflow selection in `scripts/**` (Owner scope - if the right answer is "run these only in
the Runtime workflows", report that with file:line and stop), `internal/operatorauth/**` and the other Owner rails, and any
change that weakens an assertion to make a shard pass.

## Acceptance criteria

1. `PR · Go unit · cli-0..3` and `packages` no longer fail because of missing ORAS, a missing real runtime, or an OOM kill.
2. Every skipped case prints a skip witness naming the missing capability, and the akte states which native gate covers it.
3. A test that is skipped on every runner in the matrix is treated as NOT covered: the card must then move it to a workflow
   that does provide the runtime, which is the Owner-scope case above (report, do not invent a parallel pipeline).
4. Before/after job conclusions with run ids are quoted from two different PRs (one of them #1733 or #1734, whose only red is
   the inherited shards).

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | `PR · Go unit · cli-0..3`, `PR · Go unit · packages`, covered alternatively by `Runtime · Docker Core` |
| Test identifier | `0428-215` |
| Route | `contract set of the affected package plus skip witness` |

## Dependencies

None by contract, but sequence behind 0428-204 while that lane writes in `cmd/baha/` - the four files above are inside its
work area.

## Stop and report

If a case can only be fixed by adding ORAS/runtime to the runner (workflow change), stop and report the exact line in
`.github/workflows/ci.yml`.

## Handoff

Branch, PR, exact head SHA, two run ids with per-shard conclusions, evidence
`evidence/r28-welle4-2026-11-21/cli-shard-runtime-tests/round-1.md`.

kommissioniert, weil der wart-grund weg ist: #1740 zeigt am gestapelten head (run 44868911131, protokoll 900721 bytes) cli-1/2/3 SUCCESS und genau EINE erste-level-fail-zeile, die zu 0428-210/#1739 gehoert — die container-/ORAS-pflichtigen faelle ihrer karte sind an dieser basis also bereits geheilt. Lane '0428-215-cli215' (4359f0e8, laptop:2), base = 'lane-0428-198-cli-shard-operator-env' (zuletzt e45430f2f1b7, bewegt sich), gestapelt auf #1726.

round-2 delivered (plan ed88dda9/188ac1fd), red-first in benannter runner-form, keine produkt-aenderung, kein PR — diagnose as ordered.

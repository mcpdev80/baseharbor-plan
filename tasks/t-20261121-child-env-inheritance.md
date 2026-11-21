---
id: t-20261121-child-env-inheritance
card_number: "0428-222"
card_short_title: "child process Env replaced"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-222 · child process Env replaced
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261121-child-env-inheritance · 0428-222 child process environment replaced instead of inherited in corebackup/coreupdate etcd probes #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

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


<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Problem

Desk H-V47 (`baseharbor-plan/evidence/r28-welle4-2026-11-21/child-env-desk/hunt-1.md`) swept every
child-process environment assignment on develop and found five production-reachable sites in the
**REPLACEMENT** class (K2): the command's `Env` is built as a literal list, so the child process
does **not** inherit the parent environment. The same class cost PR #1742 a full correction round
today: `cmd/baha/app_inspect_remote.go:70` used `cmd.Env = append(cmd.Env, "GIT_TERMINAL_PROMPT=0")`
while `cmd.Env` was nil, which stripped `PATH` and `HOME` from a `git clone` child.

Measured K2 sites (develop `ddfa80f7202a`, file:line from the desk table):

1. `internal/corebackup/etcd/etcdctl.go:95` - `EtcdctlSource.Snapshot` -> `etcdctl snapshot save`
2. `internal/corebackup/etcd/etcdctl.go:114` - snapshot status verify -> `etcdutl`
3. `internal/corebackup/etcd/etcdctl.go:156` - `attestEndpointStatus` -> `etcdctl endpoint status`
4. `internal/corebackup/etcd/etcdutl.go:95` - `IsolatedEtcdutl.Restore` -> `etcdutl snapshot restore`
5. `internal/coreupdate/dcs_boot_probe.go:59` - `dcsBootProbe` -> `etcdctl` (Core HA boot probe)

Whether these are defects depends on intent: an isolated `etcdutl` restore may deliberately run with
a minimal environment. The card is therefore a **prove-or-fix** card, not a blanket rewrite.

## Acceptance

1. For each of the five sites, state in evidence whether the replacement is intentional. A site is
   intentional only if a comment or a test names the isolation goal; otherwise it is a defect.
2. For every unintentional site: extend the parent environment instead of replacing it
   (`cmd.Env = append(os.Environ(), ...)` or the existing filter helper), keeping any secret
   scrubbing that the current literal list performs on purpose.
3. One regression test per fixed site that proves inheritance: set a sentinel variable in the parent
   environment inside the test and assert the child observes it, plus the existing behaviour intact.
   A test that only checks the command's argument list does not satisfy this criterion.
4. Mutation proof: removing the inheritance must turn the new test red; record command, output, exit
   code. Green-only claims are rejected.

## Allowed write-set

`internal/corebackup/etcd/etcdctl.go`, `internal/corebackup/etcd/etcdutl.go`,
`internal/coreupdate/dcs_boot_probe.go`, their test files, and one new `*_test.go` per package named
`*0428-<this card>*`.

## Forbidden

`.github/**`, `scripts/**`, `internal/operatorauth/**`, `internal/identityprovider/**`,
`internal/serviceaccess/**`, `internal/observability/registry.go`,
`internal/capability/perses_selection.go`, `cmd/baha/**` (other cards are live there). If a fix
requires a file outside the write-set, stop and report `file:line`.

## Evidence

`baseharbor-plan/evidence/r28-welle4-2026-11-21/child-env-inheritance/round-1.md` with the numbered
`## PLAN` list (no `- [ ]` checkboxes), per-site decision, hosted run id and per-job byte counts,
`## repo-rule compliance`, `## cleanliness`.

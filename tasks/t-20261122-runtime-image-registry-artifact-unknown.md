---
id: t-20261122-runtime-image-registry-artifact-unknown
card_number: "0428-249"
card_short_title: "light-runtime blob unknown"
type: bug
areas: [ci, testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: "w362-0428-249-1812rebase"
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-249 · light-runtime blob unknown
priority: high
depends_on: [t-20261124-r28-release-candidate-testonly-binary]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1812, mcpdev80/baseharbor#1837]
sources: []
blocker: "parked-until-landing: workflow hardening edit-set (owner runner-health decisions 1-3) awaits w267 publication + w255 independent ACCEPT; lane w362 reserved for the exact edit-set implementation (existing card, no new card). Both 45915629291 attempts excluded as non-evidence (attempt2 cancelled 01:12:22Z pre-ruling). Qualification runs (fresh PR run + 14-gate validation on refreshed head) only after fix lands"
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-demo/pull/175"]
---

- [ ] t-20261122-runtime-image-registry-artifact-unknown · Light-runtime blob/manifest unknown root cause is not a scripts publish gap, it is .github workflow ordering plus a dangling acceptance.sh reference (owner decision) #task #release/v0-4-28 #status/blocked #view/blocked #area/ci #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** w362-0428-249-1812rebase · **Priority:** high  
    **PR:** [baseharbor#1812](https://github.com/mcpdev80/baseharbor/pull/1812), [baseharbor#1837](https://github.com/mcpdev80/baseharbor/pull/1837)  
    **Blocker:** parked-until-landing: workflow hardening edit-set (owner runner-health decisions 1-3) awaits w267 publication + w255 independent ACCEPT; lane w362 reserved for the exact edit-set implementation (existing card, no new card). Both 4591562929…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-demo/pull/175)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261124-r28-release-candidate-testonly-binary](t-20261124-r28-release-candidate-testonly-binary.md)  
**Owner:** w362-0428-249-1812rebase  
**Priority:** high  
**PRs:** [baseharbor#1812](https://github.com/mcpdev80/baseharbor/pull/1812), [baseharbor#1837](https://github.com/mcpdev80/baseharbor/pull/1837)  
**Source:** 
<!-- /generated:links -->

## Finding (0847d100 audit, develop 3cbb2bac  713aadd4)

`scripts/ci-local-oci-registry.sh` publish path is CORRECT (local docker+podman test: it tags, pushes blob+manifest, and oras resolves the sha256 digest; it only fails on the local-only unbound GITHUB_ENV/GITHUB_STEP_SUMMARY vars). So no scripts fix is warranted.

The 'blob/manifest unknown' seen by the light-runtime cells comes from causes outside `scripts/**`:
1. `.github/workflows/pre-release-runtime-suite.yml:198-201`  the publish-before-ORAS-resolve ordering must be verified.
2. per-job runner registry sharing (the local registry may not be shared across runner jobs).
3. `scripts/acceptance.sh` is MISSING from the tree (`git cat-file` 404, `gh contents` 404) yet is referenced in `.github/workflows/pre-release-runtime-suite.yml:306`, `pre-release.yml:1080`, `targeted-demo-acceptance.yml:345`, and registered as a core in `scripts/pre-release-runtime-impact.json:104`.

This is an Owner `.github` + missing-file decision; a lane must not fabricate a scripts workaround.

Die Freigabe ist auf den belegten Pre-Release-Fix begrenzt. ci.yml und der normale CI-Pfad bleiben unverändert.

owner release 2026-11-22/23: one narrow PR (.github pre-release workflows + acceptance.sh + impact.json, ci.yml untouched), Docker+Podman light gates green before merge

fix done in write-set; tests green; not merged (frost+pending)

OWNER ACTION DONE 19:4xZ: dispatched Release·Pre-Release Validation run 45251664813 (7 light gates Docker+Podman). Scope crossing RESOLVED: #1812 head now 69de976f1e, diff = ONLY .github/workflows/pre-release-runtime-suite.yml (+20/-0), scripts/** clean (verified ls-remote+gh pr diff). Lane finish: reconcile PR body (still describes discarded scripts fix), watch OWN dispatched run to terminal, verify it tested candidate 69de976f1e (run headSha shows develop dc8626e9c5 - flag if candidate not built), republish evidence, END only when run green. No merge (frost+acceptance).

fix landed YAML-only, scope clean, lane held (no scripts/** re-cross); blocked pending owner re-dispatch on correct ref

OWNER re-dispatched Hosted Pre-Release Validation run 45255981415 on exact candidate 69de976f1e (ref lane-0428-249-runtime-image-fix, Demo pin f23b6e09, 14 light gates; verified gh run headSha=69de976f1e). w249 resume: watch OWN run to terminal + reconcile PR body (still describes discarded scripts fix). #1812 write-set clean (diff = ONLY .github yaml). No merge (frost).

OWNER re-dispatched Hosted Pre-Release Validation run 45255981415 on exact candidate 69de976f1e (verified gh run headSha). w249: watch OWN run to terminal + reconcile PR body (still describes discarded scripts fix). diff = ONLY .github yaml. No merge.

own-run terminal FAILURE at artifact preflight, not lane code; held pending CI-owner artifact fix

OWNER artifact gap FIXED in-scope (same authorized workflow): head 5ab9fe4a63, diff = ONLY .github/workflows/pre-release-runtime-suite.yml (scripts/** + ci.yml clean, verified gh pr diff --name-only). Fallback: when baha-ci-operator-testonly absent, Demo installer builds it under the job GOFLAGS test-only tag for exact BASEHARBOR_SOURCE_REF; present-case version-SHA check stays fail-closed. PR hosted run 45258883468 = SUCCESS on 5ab9fe4. Fresh Pre-Release Validation 45259373990 in_progress on candidate ref 5ab9fe4 (14 Docker+Podman light gates). w249: watch OWN run 45259373990 to terminal + republish evidence/round-1.md to origin/main with head 5ab9fe4; END_DONE when the 14 gates go green. No merge (frost).

reconciled per Owner: 1812 in-scope fix complete; gate-red external (0428-250 fixture allowlist). Lane holds, no edit to shared fixture on this branch.

No live owner lane (w249 gone); parked at exact-scope review. No coordinator/worker edit, CI-acceptance, or merge until owner decides.

Within 0428-249 approval; no alternate logic added. Owner-handled.

Unblocked by #1815 merge. OWNER executing #1812 rebuild from develop 3ebfb90d with ONLY the two approved runtime image archive reloads (removing the unapproved optional-binary/build-from-source fallback per scope ruling), then running final Docker+Podman Light gates. Owner-handled .github/** scope; no worker lane.

Rebuilt on develop 3ebfb90d: ONLY the two approved runtime image archive reloads; optional-binary/build-from-source fallback removed; force-guarded against old head 7bce1838. New PR head b1b31a59 / base 3ebfb90d. General run 45313094627 started (planner queued; selected light gates not yet scheduled). Owner-handled .github scope.

EXACT owner-approved 14 Docker+Podman Light acceptance gates running in workflow-dispatch run 45313489014 (head b1b31a59 / base 3ebfb90d, candidate SHA = exact PR head, demo pin f23b6e09). v0.4.27 gate catalog supplies the 14 light IDs; v0.4.28 release catalog (static-only) NOT edited. PR-triggered general run 45313094627 also active. Scope = exactly one file, 20 additions, ci.yml untouched, no optional fallback.

Lane correctly stopped, awaiting owner. No coordinator/worker edit. This is the same artifact-availability root as #1818/#1810 (baha-ci-operator-testonly production).

Unblocked: batch #1822 merged to develop 90086a1f9 (baha-ci-operator-testonly production landed). Rebase+14-light-gate rerun onto new develop by w66 (mechanical, no owner-scope edits). CODEX merges on green.

Sequence step 1 (owner re-release): rebase #1812 onto develop 05ef48536; superseded files take develop version, only .github/workflows/pre-release-runtime-suite.yml (owner's existing delta) survives byte-for-byte. Trigger+verify exact-head run incl 14 runtime-suite gates. No merge. #1819/#1820 follow ONLY after #1812 terminal-green.

Rebased onto develop 46d3dccc, exact head 47590207518, one-file diff pre-release-runtime-suite.yml. PR CI 45397265257 SUCCESS. Docker Light dispatch 45398943139 on head; w81 reports a .github resource-validation blocker (static_gates vs runtime_light_gates_* classification) at pre-release-runtime-suite.yml:237-246 — owner-scope, escalated (card 0428-280). Podman held until owner scope answer + Docker outcome.

Core fixture handoff (2026-11-24): BaseHarbor PR [#1827](https://github.com/mcpdev80/baseharbor/pull/1827) merged at `adf43709b8b37cd2b18a6bf4710019d7343d54b4` (source `83d7c7afc84740b565ff654562a178361c3522c8`) with two exact-head green Hosted CI runs: [45455276409](https://github.com/mcpdev80/baseharbor/actions/runs/45455276409) and [45460654225](https://github.com/mcpdev80/baseharbor/actions/runs/45460654225). This closes only the Core test-only fixture half; #1812 still needs its own requalification after merge, assigned to w112. Existing #1812 scope and blocker are unchanged.## Handoff

- Catalog PR #1837 MERGED (develop f7540e591): 14 Light IDs required_for v0.4.28 (CI 45511970224 terminal green exact d57a8253; APPROVE stored as COMMENTED - same-account). #1812 final sequence resumed on this base (workflow-only diff).



- CATALOG PR LIVE: #1837 head d57a8253b478f461e616d5058c42331d50c4662e - exactly the two approved files, 14 Light IDs required_for v0.4.28 only, v0.4.27 unchanged; run 45511970224 all-completed-green (pr-planner-tests pending). Terminal green -> independent Codex review/merge; after merge #1812 rebases for the 14-gate reruns.


- AUTHORIZATION GAP (2026-11-25): the 14 Docker/Podman Light-gate IDs are not required IDs in the current v0.4.28 catalog (only static/ci-fast-check + atomic/static/mcp; #1746/#1805 covered ci-fast-check). Catalog authorization decision = Owner. PR #1812 stays OPEN/nonqualifying; runs 45504224635/45505198117/45506742327 void.
-20261122-runtime-image-registry-artifact-unknown
card_number: "0428-249"
card_short_title: "light-runtime blob unknown"
type: bug
areas: [ci, testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: 
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-249 · light-runtime blob unknown
priority: high
depends_on: [t-20261124-r28-release-candidate-testonly-binary]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1812]
sources: []
blocker: "ROOT CAUSE NOT YET DETERMINED (run 45432650561 head 9140b2cb still active: 7 fail / 5 pass / 2 running). >=3 distinct failure signatures, NOT one consent cause: (1) Docker policy job 138587494655 = consent refusal (--confirm-candidate) AND operator-auth 'not a terminal'; (2) Podman connectivity job 138587494809 = digest retry issued + guided-up-consented reached READY + repo workload ready, then EMPTY Acceptance group header + demo-connectivity FAIL with NO concrete assertion (possibly a distinct harness/acceptance bug, not consent); that job also logs ci-operator-testonly managed-local-gate decisions for up with and without --confirm-candidate. Classification HELD until all 14 Light jobs reach terminal + artifacts/logs inspected. Merge held; #1819/#1820 parked. develop f14fb87c8."
resolution: ""
evidence: []
---

    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **PR:** [baseharbor#1812](https://github.com/mcpdev80/baseharbor/pull/1812)  
    **Blocker:** ROOT CAUSE NOT YET DETERMINED (run 45432650561 head 9140b2cb still active: 7 fail / 5 pass / 2 running). \>=3 distinct failure signatures, NOT one consent cause: (1) Docker policy job 138587494655 = consent refusal (--confirm-candidate) AND…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261124-r28-release-candidate-testonly-binary](t-20261124-r28-release-candidate-testonly-binary.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** [baseharbor#1812](https://github.com/mcpdev80/baseharbor/pull/1812)  
**Source:** 
<!-- /generated:links -->

## Finding (0847d100 audit, develop 3cbb2bac  713aadd4)

`scripts/ci-local-oci-registry.sh` publish path is CORRECT (local docker+podman test: it tags, pushes blob+manifest, and oras resolves the sha256 digest; it only fails on the local-only unbound GITHUB_ENV/GITHUB_STEP_SUMMARY vars). So no scripts fix is warranted.

The 'blob/manifest unknown' seen by the light-runtime cells comes from causes outside `scripts/**`:
1. `.github/workflows/pre-release-runtime-suite.yml:198-201`  the publish-before-ORAS-resolve ordering must be verified.
2. per-job runner registry sharing (the local registry may not be shared across runner jobs).
3. `scripts/acceptance.sh` is MISSING from the tree (`git cat-file` 404, `gh contents` 404) yet is referenced in `.github/workflows/pre-release-runtime-suite.yml:306`, `pre-release.yml:1080`, `targeted-demo-acceptance.yml:345`, and registered as a core in `scripts/pre-release-runtime-impact.json:104`.

This is an Owner `.github` + missing-file decision; a lane must not fabricate a scripts workaround.

Die Freigabe ist auf den belegten Pre-Release-Fix begrenzt. ci.yml und der normale CI-Pfad bleiben unverändert.

owner release 2026-11-22/23: one narrow PR (.github pre-release workflows + acceptance.sh + impact.json, ci.yml untouched), Docker+Podman light gates green before merge

fix done in write-set; tests green; not merged (frost+pending)

OWNER ACTION DONE 19:4xZ: dispatched Release·Pre-Release Validation run 45251664813 (7 light gates Docker+Podman). Scope crossing RESOLVED: #1812 head now 69de976f1e, diff = ONLY .github/workflows/pre-release-runtime-suite.yml (+20/-0), scripts/** clean (verified ls-remote+gh pr diff). Lane finish: reconcile PR body (still describes discarded scripts fix), watch OWN dispatched run to terminal, verify it tested candidate 69de976f1e (run headSha shows develop dc8626e9c5 - flag if candidate not built), republish evidence, END only when run green. No merge (frost+acceptance).

fix landed YAML-only, scope clean, lane held (no scripts/** re-cross); blocked pending owner re-dispatch on correct ref

OWNER re-dispatched Hosted Pre-Release Validation run 45255981415 on exact candidate 69de976f1e (ref lane-0428-249-runtime-image-fix, Demo pin f23b6e09, 14 light gates; verified gh run headSha=69de976f1e). w249 resume: watch OWN run to terminal + reconcile PR body (still describes discarded scripts fix). #1812 write-set clean (diff = ONLY .github yaml). No merge (frost).

OWNER re-dispatched Hosted Pre-Release Validation run 45255981415 on exact candidate 69de976f1e (verified gh run headSha). w249: watch OWN run to terminal + reconcile PR body (still describes discarded scripts fix). diff = ONLY .github yaml. No merge.

own-run terminal FAILURE at artifact preflight, not lane code; held pending CI-owner artifact fix

OWNER artifact gap FIXED in-scope (same authorized workflow): head 5ab9fe4a63, diff = ONLY .github/workflows/pre-release-runtime-suite.yml (scripts/** + ci.yml clean, verified gh pr diff --name-only). Fallback: when baha-ci-operator-testonly absent, Demo installer builds it under the job GOFLAGS test-only tag for exact BASEHARBOR_SOURCE_REF; present-case version-SHA check stays fail-closed. PR hosted run 45258883468 = SUCCESS on 5ab9fe4. Fresh Pre-Release Validation 45259373990 in_progress on candidate ref 5ab9fe4 (14 Docker+Podman light gates). w249: watch OWN run 45259373990 to terminal + republish evidence/round-1.md to origin/main with head 5ab9fe4; END_DONE when the 14 gates go green. No merge (frost).

reconciled per Owner: 1812 in-scope fix complete; gate-red external (0428-250 fixture allowlist). Lane holds, no edit to shared fixture on this branch.

No live owner lane (w249 gone); parked at exact-scope review. No coordinator/worker edit, CI-acceptance, or merge until owner decides.

Within 0428-249 approval; no alternate logic added. Owner-handled.

Unblocked by #1815 merge. OWNER executing #1812 rebuild from develop 3ebfb90d with ONLY the two approved runtime image archive reloads (removing the unapproved optional-binary/build-from-source fallback per scope ruling), then running final Docker+Podman Light gates. Owner-handled .github/** scope; no worker lane.

Rebuilt on develop 3ebfb90d: ONLY the two approved runtime image archive reloads; optional-binary/build-from-source fallback removed; force-guarded against old head 7bce1838. New PR head b1b31a59 / base 3ebfb90d. General run 45313094627 started (planner queued; selected light gates not yet scheduled). Owner-handled .github scope.

EXACT owner-approved 14 Docker+Podman Light acceptance gates running in workflow-dispatch run 45313489014 (head b1b31a59 / base 3ebfb90d, candidate SHA = exact PR head, demo pin f23b6e09). v0.4.27 gate catalog supplies the 14 light IDs; v0.4.28 release catalog (static-only) NOT edited. PR-triggered general run 45313094627 also active. Scope = exactly one file, 20 additions, ci.yml untouched, no optional fallback.

Lane correctly stopped, awaiting owner. No coordinator/worker edit. This is the same artifact-availability root as #1818/#1810 (baha-ci-operator-testonly production).

Unblocked: batch #1822 merged to develop 90086a1f9 (baha-ci-operator-testonly production landed). Rebase+14-light-gate rerun onto new develop by w66 (mechanical, no owner-scope edits). CODEX merges on green.

Sequence step 1 (owner re-release): rebase #1812 onto develop 05ef48536; superseded files take develop version, only .github/workflows/pre-release-runtime-suite.yml (owner's existing delta) survives byte-for-byte. Trigger+verify exact-head run incl 14 runtime-suite gates. No merge. #1819/#1820 follow ONLY after #1812 terminal-green.

Rebased onto develop 46d3dccc, exact head 47590207518, one-file diff pre-release-runtime-suite.yml. PR CI 45397265257 SUCCESS. Docker Light dispatch 45398943139 on head; w81 reports a .github resource-validation blocker (static_gates vs runtime_light_gates_* classification) at pre-release-runtime-suite.yml:237-246 — owner-scope, escalated (card 0428-280). Podman held until owner scope answer + Docker outcome.

Core fixture handoff (2026-11-24): BaseHarbor PR [#1827](https://github.com/mcpdev80/baseharbor/pull/1827) merged at `adf43709b8b37cd2b18a6bf4710019d7343d54b4` (source `83d7c7afc84740b565ff654562a178361c3522c8`) with two exact-head green Hosted CI runs: [45455276409](https://github.com/mcpdev80/baseharbor/actions/runs/45455276409) and [45460654225](https://github.com/mcpdev80/baseharbor/actions/runs/45460654225). This closes only the Core test-only fixture half; #1812 still needs its own requalification after merge, assigned to w112. Existing #1812 scope and blocker are unchanged.

## W16 status correction

This card is reopened in `wait`: PR #1812 remains OPEN and unmerged, so the prior `accepted` closure is not supported by the current exact-head state. Existing evidence bytes and the task ID are unchanged.

## Owner disposition — qualification evidence workflow integrity (2026-11-27)

This is an existing-card disposition for 0428-249, because the decisions below are prerequisites for a trustworthy #1812 qualification. Implementation is by the worker lane on 0428-249, Owner-authorized; `.github` changes are limited exactly to this edit set. This is the named-card exception in coordinator/RUNBOOK.md §4.0, line 251. The Owner's global scope covers every evidence-producing qualification, gate, and acceptance workflow, including the `PR Selected Checks` graph in `ci.yml`.

### Decisions

1. Evidence-producing runs must not be cancelled by a newer event. Set `cancel-in-progress: false` for all qualifying workflows below. A cancelled run cannot be cited as completed qualification evidence.
2. Concurrency identity must include the immutable, verified candidate commit SHA, never the branch/ref name. Include gate/runtime identity and `github.run_id` so independent jobs and distinct evidence events do not evict each other. For an input such as `inputs.ref`, resolve it to a full 40-hex commit before a gate is admitted, assert the checkout's `git rev-parse HEAD` equals that SHA, and use that verified SHA in the gate-level group. Workflow-level expressions cannot read a later job's output: an orchestrator whose input may be a branch/tag must use a unique non-cancelling run group, while each evidence job uses the resolved SHA. A branch-shaped input must not be treated as a verified SHA.
3. A single long Podman job is not independent evidence when it bundles unrelated acceptance assertions. Split the Podman `single_default_native` job into independently named/checkable jobs for (a) single-default SQL/Secrets, (b) Node HTTPS enrollment/remote CLI, (c) install destroy/interrupted retry, and (d) pinned-workload lifecycle/backup. Each job must check out and attest the same immutable candidate SHA, run its own required setup/cleanup, and fail independently. `podman-acceptance.yml:106-175` currently bundles all four; the separate `keycloak_single_native` job at `:62-104` is already distinct and must remain distinct. The configured timeout of `keycloak_single_native` is 22 minutes and `single_default_native` is 65 minutes; the source does not establish an observed 24-minute duration. The required structural correction is the four-way split of the bundled evidence regardless of wall time.

### Exact workflow edit set (current `origin/develop` witnesses)

For evidence jobs, the required group shape is `bh-evidence-${{ <verified-head-sha> }}-${{ <gate/runtime-id> }}-${{ github.run_id }}`; use the actual gate/runtime expression available at that workflow/job. Keep independent matrix jobs separate by gate/runtime. Where a workflow has no current concurrency block, add a **job-level** block after immutable SHA resolution; do not create a static workflow-wide lock.

| Workflow and current lines | Current state | Required edit |
| --- | --- | --- |
| `.github/workflows/ci.yml:24-26` | `ci-${{ github.ref }}`; cancel `true`. The same run contains `PR Selected Checks` (`:1552-1577`) and selected jobs. | `group: ci-${{ github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}`; `cancel-in-progress: false`. Keep the aggregator and selected evidence jobs in the same non-cancelling candidate run. |
| `.github/workflows/docker-runtime-acceptance.yml:24-26` | workflow/ref group; cancel `true`; `inputs.ref` is checked out at `:189`. | `group: docker-${{ inputs.ref || github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}`; `cancel-in-progress: false`; reject non-SHA evidence inputs and assert checkout SHA. |
| `.github/workflows/podman-acceptance.yml:23-25` | workflow/ref group; cancel `true`; `inputs.ref` checked out at `:191`. | `group: podman-${{ inputs.ref || github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}`; `cancel-in-progress: false`; require and verify exact SHA. Split `single_default_native` as Decision 3. |
| `.github/workflows/host-trust-owned-e2e.yml:23-25` | group uses PR number or `github.ref`; cancel `true`. | `group: host-trust-owned-${{ github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}`; `cancel-in-progress: false`. |
| `.github/workflows/mcp-lifecycle-acceptance.yml:28-30` | group includes `github.ref` and `inputs.ref || github.ref_name`; cancel `true`; checkout at `:48` and `:91`. | `group: mcp-lifecycle-${{ inputs.ref || github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}`; `cancel-in-progress: false`; resolve/validate `inputs.ref` to full SHA and assert checkout equality before the gate. |
| `.github/workflows/nextjs-greenfield-e2e.yml:13-15` | group uses PR number or ref; cancel `true`; candidate checkout input at `:77`. | `group: greenfield-native-${{ inputs.candidate_ref || github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}`; `cancel-in-progress: false`; assert candidate checkout equality. |
| `.github/workflows/observability-acceptance.yml:33-35` | group contains `github.ref` and input ref; cancel `true`; Docker and Podman are separate jobs. | Use per-job `group: observability-${{ inputs.ref || github.event.pull_request.head.sha || github.sha }}-${{ matrix.runtime }}-${{ github.run_id }}`; `cancel-in-progress: false`; resolve input to SHA and assert checkout equality. |
| `.github/workflows/targeted-integration.yml:51-64` | workflow-level key uses `github.ref` and raw `inputs.ref`; dispatch allows branch/ref input. The resolver output does not exist at workflow-concurrency evaluation time. | Exact resolver/job-level before/after pattern below: use a run-unique non-cancelling workflow group, resolve `inputs.ref || github.sha` to `needs.resolve_candidate.outputs.head_sha`, then key every evidence job by that SHA + gate/runtime + run ID. No raw `inputs.ref` in any concurrency key. |
| `.github/workflows/pre-release.yml:6-8` | cancel already `false`; group is either a run ID in develop mode or one global static `baseharbor-release-qualification` lock. Candidate SHA is resolved in `source_prepare` (checkout `:50`, checks around `:75-91`). | `group: pre-release-orchestrator-${{ github.run_id }}`; keep `cancel-in-progress: false`. Orchestrator is unique per run; each evidence-producing reusable gate call after resolution must key by `${{ needs.source_prepare.outputs.candidate_sha }}-${{ matrix.runtime }}-${{ matrix.gate }}-${{ github.run_id }}`. Never use branch/tag input as the evidence key. |
| `.github/workflows/pre-release-runtime-suite.yml:81-126, 661-705` | The existing step validates and checks out raw `inputs.ref` (`:81-115`) and then records `git rev-parse HEAD` (`:122-126`); the gate job has no resolver-job output or SHA-based concurrency. | Exact resolver-job before/after pattern below: add `resolve_candidate` that emits a full 40-hex `head_sha`; make `gate` depend on it, checkout that output, assert `HEAD == head_sha`, and key by output SHA + runtime + gate + run ID. Never use raw `inputs.ref` in the key. |
| `.github/workflows/targeted-demo-acceptance.yml:48-50` | cancel `false` already; static `baseharbor-release-qualification` lock. Its `resolve` job produces the tested SHA at `:55-62`, so workflow-level concurrency cannot use that output. | `group: targeted-demo-orchestrator-${{ github.run_id }}`; keep cancel `false`. Each downstream evidence job must use `needs.resolve.outputs.ref` + gate/runtime + run ID in its job-level group, after the resolver validates the exact commit. |
| `.github/workflows/runtime-broker.yml:26-30, 321-325` | Acceptance and performance are separate evidence jobs; no concurrency block; dispatch accepts `inputs.ref` as a Git ref at `:6-20`. | Add job-level groups `broker-${{ inputs.ref }}-acceptance-${{ github.run_id }}` and `broker-${{ inputs.ref }}-performance-${{ github.run_id }}` with `cancel-in-progress: false`; make the evidence input a full SHA and assert checked-out HEAD equals it. |
| `.github/workflows/runtime-s3-acceptance.yml:4-14` | Workflow-dispatch acceptance; no concurrency block; checkout uses `inputs.ref` at `:17-20`. | Add job-level `group: runtime-s3-${{ inputs.ref || github.sha }}-${{ github.run_id }}` and `cancel-in-progress: false`; require/verify full SHA before executing the acceptance steps. |
| `.github/workflows/supplemental-release-validation.yml:1-8, 36-39` | Push/dispatch evidence workflow; no concurrency block; checkout uses the event commit. | Add job-level `group: supplemental-validation-${{ github.sha }}-${{ github.run_id }}` and `cancel-in-progress: false`; assert checkout HEAD equals `github.sha`. |

Also retain the already-safe job-level HA groups in `ci.yml:180-182` and `:222-224` (`cancel-in-progress: false`); change their constant group to `targeted-ha-docker-${{ github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}` and `targeted-ha-podman-${{ github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}` respectively. The workflows are currently push-triggered, so `github.sha` is the pushed candidate; the PR-head expression preserves correct identity if PR events are enabled later. `pre-release.yml:882` and `:934` already use per-gate HA groups but must carry the resolved candidate SHA and unique run ID. `runtime-image.yml` produces release images rather than qualification evidence; `release.yml` publishes; `pages.yml` deploys; `receipt-post-run.yml` writes a receipt; `artifact-gc.yml` and `renovate.yml` are maintenance/automation. Those are excluded from this evidence workflow edit set.

### Resolver-job correction requested by independent review (w255, 2026-11-27)

The earlier raw-input group examples are withdrawn for `targeted-integration.yml` and `pre-release-runtime-suite.yml`. Workflow-level concurrency cannot reference `needs` outputs. The orchestration group must therefore be unique per run and non-cancelling; the **gate jobs** use the resolver output. This avoids grouping by a mutable branch name and avoids using an unverified raw input.

#### `targeted-integration.yml:51-64`

Before (current shape):

```yaml
  ref:
    description: Git ref or commit SHA to test
    required: true
    default: develop
    type: string

concurrency:
  group: targeted-integration-${{ github.ref }}-${{ inputs.ref || github.sha }}-${{ inputs.gate || 'default' }}-${{ inputs.runtime || 'default' }}
  cancel-in-progress: ${{ github.ref_name != 'work/v0.4.24-core-ha-updates' && github.ref_name != 'work/v0.4.25-contract-minimal-core' }}
```

After (resolver output plus per-evidence-job concurrency):

```yaml
concurrency:
  group: targeted-integration-orchestrator-${{ github.run_id }}
  cancel-in-progress: false

jobs:
  resolve_candidate:
    runs-on: ubuntu-latest
    outputs:
      head_sha: ${{ steps.resolve.outputs.head_sha }}
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          ref: ${{ github.sha }}
          fetch-depth: 0
          persist-credentials: false
      - id: resolve
        shell: bash
        env:
          CANDIDATE_REF: ${{ inputs.ref || github.sha }}
        run: |
          set -euo pipefail
          git fetch --no-tags origin "$CANDIDATE_REF"
          head_sha="$(git rev-parse --verify 'FETCH_HEAD^{commit}')"
          [[ "$head_sha" =~ ^[0-9a-f]{40}$ ]]
          echo "head_sha=$head_sha" >> "$GITHUB_OUTPUT"

  <each evidence job>:
    needs: [resolve_candidate, <existing needs>]
    concurrency:
      group: targeted-${{ needs.resolve_candidate.outputs.head_sha }}-<literal gate/runtime identity>-${{ github.run_id }}
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          ref: ${{ needs.resolve_candidate.outputs.head_sha }}
      - name: Assert exact candidate
        env:
          EXPECTED_HEAD_SHA: ${{ needs.resolve_candidate.outputs.head_sha }}
        run: test "$(git rev-parse HEAD)" = "$EXPECTED_HEAD_SHA"
```

Apply the resolver dependency, resolved checkout, and job-level group to every evidence-producing job in this workflow, including the `workflow_dispatch`, `workflow_call`, and push gate paths. Retain each job's existing gate/runtime literals or matrix identity in its group. The resolver is the sole place where a branch/ref becomes a commit SHA; a gate cannot start if fetch, resolution, 40-hex validation, or checkout equality fails.

#### `pre-release-runtime-suite.yml:81-126`

Before (current shape):

```yaml
    - name: Validate candidate ref before checkout
      env:
        CANDIDATE_REF: ${{ inputs.ref }}
      run: <validate branch/tag/ref>
    - name: Checkout BaseHarbor candidate
      uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
      with:
        ref: ${{ inputs.ref }}
    - name: Resolve candidate SHA
      id: candidate
      run: echo "sha=$(git rev-parse HEAD)" >> "$GITHUB_OUTPUT"
```

After:

```yaml
jobs:
  resolve_candidate:
    runs-on: ubuntu-latest
    outputs:
      head_sha: ${{ steps.resolve.outputs.head_sha }}
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          ref: ${{ github.sha }}
          fetch-depth: 0
          persist-credentials: false
      - id: resolve
        shell: bash
        env:
          CANDIDATE_REF: ${{ inputs.ref }}
        run: |
          set -euo pipefail
          git fetch --no-tags origin "$CANDIDATE_REF"
          head_sha="$(git rev-parse --verify 'FETCH_HEAD^{commit}')"
          [[ "$head_sha" =~ ^[0-9a-f]{40}$ ]]
          echo "head_sha=$head_sha" >> "$GITHUB_OUTPUT"

  gate:
    needs: resolve_candidate
    concurrency:
      group: atomic-${{ needs.resolve_candidate.outputs.head_sha }}-${{ inputs.runtime }}-${{ inputs.gate }}-${{ github.run_id }}
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          ref: ${{ needs.resolve_candidate.outputs.head_sha }}
      - name: Assert exact candidate
        env:
          EXPECTED_HEAD_SHA: ${{ needs.resolve_candidate.outputs.head_sha }}
        run: test "$(git rev-parse HEAD)" = "$EXPECTED_HEAD_SHA"
```

Carry existing `gate` job steps after this checkout/assert sequence, preserving the existing pinned action SHAs and behavior. Change every subsequent candidate reference/manifest field to the resolver output, not raw `inputs.ref`; ensure the resolver job's SHA is the `candidate_sha` written into evidence. For `targeted-integration.yml`, add `resolve_candidate` to every evidence job's existing `needs` (append, do not replace): `compose_isolation_exact`, `registered_otlp_handoff`, `up_dispatch_source`, `application_full_reset`, `core_stop`, `standalone_retirement`, `observability_consumers`, `installation_destroy`, `shared_network`, `coreless_runtime`, `shared_provider_contracts`, `focused`, `app_backup_restore_podman`, `core_bootstrap`, `core_ha_recovery`, `provider_topology`, `application_provider_topology`, `core_provider_versions`, `core_ha_openbao_versions`, `v0421_ha`, `adoption`, `bug_hunt_templates`, `rootless_engine_isolation`, `identity_trust`, `final_bug_acceptance`, `provider_observation`, `external_provider_handoff`, `pr_selected_coreless_lifecycle_shards`, and `pr_selected_coreless_lifecycle`. Each gets its own group literal or current `matrix.gate`/`matrix.runtime` so no gate identity is lost.

#### `ci.yml:180-182` and `:222-224`

Before: both `group: baseharbor-release-qualification`; `cancel-in-progress: false`.

After for Docker and Podman respectively (retain `cancel-in-progress: false`):

```yaml
group: targeted-ha-docker-${{ github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}
```

```yaml
group: targeted-ha-podman-${{ github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}
```

This prevents the two runtime jobs and separate candidate heads from sharing the constant release lock while keeping the candidate identity tied to the PR head SHA when the event has one.

### Card mapping and #1812 order

All three decisions are recorded under existing card 0428-249: (1) non-cancellation and (2) checked-SHA identity are shared qualification prerequisites directly consumed by #1812; (3) the Podman split makes each required runtime assertion independently visible to the same qualification chain. 0428-209 is closed and its native-cell contract does not own global workflow scheduling; 0428-321 is an H-V45 CLI documentation/coverage contract, not workflow ownership. No new card is proposed.

Before #1812 can qualify: the Owner must land the approved workflow changes on `develop`; then #1812's owning lane must absorb that `develop` tip by an ordinary forward merge, publish a new exact head, and obtain fresh Hosted evidence on that head. The final census must show every required Docker and Podman gate executed and successful, with no required gate cancelled or skipped; old-head runs do not transfer. `PR Selected Checks` must complete successfully on that same head. This disposition does not qualify #1812 or authorize any workflow edit by this lane.

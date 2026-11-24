---
id: t-20261122-runtime-image-registry-artifact-unknown
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
blocker: catalog PR IN FLIGHT (owner YES 2026-11-26; worker w128; 14 Light IDs required_for v0.4.28 only + minimal test expectation; #1812 stays workflow-only) — see Handoff AUTHORIZATION GAP. "ROOT CAUSE NOT YET DETERMINED (run 45432650561 head 9140b2cb still active: 7 fail / 5 pass / 2 running). >=3 distinct failure signatures, NOT one consent cause: (1) Docker policy job 138587494655 = consent refusal (--confirm-candidate) AND operator-auth 'not a terminal'; (2) Podman connectivity job 138587494809 = digest retry issued + guided-up-consented reached READY + repo workload ready, then EMPTY Acceptance group header + demo-connectivity FAIL with NO concrete assertion (possibly a distinct harness/acceptance bug, not consent); that job also logs ci-operator-testonly managed-local-gate decisions for up with and without --confirm-candidate. Classification HELD until all 14 Light jobs reach terminal + artifacts/logs inspected. Merge held; #1819/#1820 parked. develop f14fb87c8."
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-runtime-image-registry-artifact-unknown · Light-runtime blob/manifest unknown root cause is not a scripts publish gap, it is .github workflow ordering plus a dangling acceptance.sh reference (owner decision) #task #release/v0-4-28 #status/blocked #view/blocked #area/ci #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **PR:** [baseharbor#1812](https://github.com/mcpdev80/baseharbor/pull/1812)  
    **Blocker:** catalog PR IN FLIGHT (owner YES 2026-11-26; worker w128; 14 Light IDs required\_for v0.4.28 only + minimal test expectation; \#1812 stays workflow-only) — see Handoff AUTHORIZATION GAP. "ROOT CAUSE NOT YET DETERMINED (run 45432650561 head 91…  
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

Core fixture handoff (2026-11-24): BaseHarbor PR [#1827](https://github.com/mcpdev80/baseharbor/pull/1827) merged at `adf43709b8b37cd2b18a6bf4710019d7343d54b4` (source `83d7c7afc84740b565ff654562a178361c3522c8`) with two exact-head green Hosted CI runs: [45455276409](https://github.com/mcpdev80/baseharbor/actions/runs/45455276409) and [45460654225](https://github.com/mcpdev80/baseharbor/actions/runs/45460654225). This closes only the Core test-only fixture half; #1812 still needs its own requalification after merge, assigned to w112. Existing #1812 scope and blocker are unchanged.## Handoff

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
wait_reason: ""
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

---
id: t-20261122-runtime-image-registry-artifact-unknown
card_number: "0428-249"
card_short_title: "light-runtime blob unknown"
type: bug
areas: [ci, testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w249-0428-249-runtime-image-fix
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-249 · light-runtime blob unknown
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1812]
sources: []
blocker: "0428-249 workflow-artifact fix is DONE and PROVEN (Candidate Runtime Image builds; 14 gates now START, vs dying at the testonly preflight before). Remaining reds on run 45259373990 (6 pass / 8 fail, head 5ab9fe4) are 100% the SHARED test-only CI-operator fixture allowlist = card 0428-250 (baseharbor-demo#170, owner 0847d100): the fixture denies exact command forms [policy: 'config organization set','policy explain'; connectivity: 'app inspect .'; reconciliation: 'target -o json'; full-destroy: 'app list --all-targets'] then falls into noninteractive OIDC. #1812 has NO source change beyond the authorized artifact workflow (verified gh pr diff = only .github/workflows/pre-release-runtime-suite.yml). This is out of 0428-249's workflow-only scope. OWNER/LANE ACTION on 0428-250: extend the fixture allowlist with the 5 forms above; #1812 cannot reach green until that lands. Next trigger: 0428-250 allowlist fix merged + re-run of Pre-Release Validation on 5ab9fe4."
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-runtime-image-registry-artifact-unknown · Light-runtime blob/manifest unknown root cause is not a scripts publish gap, it is .github workflow ordering plus a dangling acceptance.sh reference (owner decision) #task #release/v0-4-28 #status/blocked #view/blocked #area/ci #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** w249-0428-249-runtime-image-fix · **Priority:** high  
    **PR:** [baseharbor#1812](https://github.com/mcpdev80/baseharbor/pull/1812)  
    **Blocker:** 0428-249 workflow-artifact fix is DONE and PROVEN (Candidate Runtime Image builds; 14 gates now START, vs dying at the testonly preflight before). Remaining reds on run 45259373990 (6 pass / 8 fail, head 5ab9fe4) are 100% the SHARED test-o…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w249-0428-249-runtime-image-fix  
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

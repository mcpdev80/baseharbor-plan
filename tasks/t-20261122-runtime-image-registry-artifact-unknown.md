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
prs: []
sources: []
blocker: "OWNER RE-DISPATCH: run 45251664813 executed against develop dc8626e9c5, NOT candidate 69de976f1e (verified gh run headSha=dc8626e9c5), and its log fails with 'runtime_light_gates_docker: expected success, got failure' across the 14 atomic docker+podman light gates. Develop light-runtime is RED = exactly the bug #1812 fixes, so the dispatch did not test the candidate. Lane write-set is clean (diff = ONLY .github/workflows/pre-release-runtime-suite.yml; scripts/ci-local-oci-registry.sh reverted; ci.yml byte-identical; local gates + test_targeted_gate_ref green). ACTION: re-dispatch Release·Pre-Release Validation for 0428-249 so it checks out candidate 69de976f1e (inputs/checkout ref, not develop); if the 14 light gates then go green on the candidate, that proves the fix and Codex can review. No lane fault. Next trigger: Owner re-dispatch on candidate ref."
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-runtime-image-registry-artifact-unknown · Light-runtime blob/manifest unknown root cause is not a scripts publish gap, it is .github workflow ordering plus a dangling acceptance.sh reference (owner decision) #task #release/v0-4-28 #status/blocked #view/blocked #area/ci #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** w249-0428-249-runtime-image-fix · **Priority:** high  
    **Blocker:** OWNER RE-DISPATCH: run 45251664813 executed against develop dc8626e9c5, NOT candidate 69de976f1e (verified gh run headSha=dc8626e9c5), and its log fails with 'runtime\_light\_gates\_docker: expected success, got failure' across the 14 atomic…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w249-0428-249-runtime-image-fix  
**Priority:** high  
**PRs:** none  
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

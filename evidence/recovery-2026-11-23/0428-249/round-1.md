# 0428-249 runtime image/registry artifact unknown — narrow CI fix

- Lane: w249-0428-249-runtime-image-fix
- Card: t-20261122-runtime-image-registry-artifact-unknown (0428-249), release v0.4.28, repo mcpdev80/baseharbor
- Mission: coordinator/missions/w249-0428-249-runtime-image-fix.txt
- PR: #1812 (open, base develop, head 41c1e6d9b8bea875cb66ccd0abd480f32a6be460)

## PLAN

- Read mission, task note, AGENTS.md, DEVELOPMENT_GUIDELINES.md; scope locked
- Investigate root cause: pre-release-runtime-suite.yml ordering + registry availability + dangling acceptance.sh references
- Establish provenance: git history for scripts/acceptance.sh (restore from proven commit or repoint to existing entrypoint)
- Cut branch lane-0428-249-runtime-image-fix from current develop; attest base SHA + ancestor + log-line witnesses
- Apply ordering/registry fix (see below)
- Prove ci.yml unchanged
- Local build/vet/tests on changed paths only
- Trigger hosted CI; own-run duty to terminal; record Docker + Podman light-runtime run ids/status
- Write evidence round-1.md; commit to origin/main; ls-tree witness; END post

## Repo attestation

- Planning repo is /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ONLY (remote: origin https://github.com/mcpdev80/baseharbor-plan.git).
- Product remote (URL contains github.com/mcpdev80): origin https://github.com/mcpdev80/baseharbor.git
- Base develop SHA (git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop): dc8626e9c52be07a8ea5b87b468c5991b7540c4f
- Branch cut from dc8626e9; merge-base --is-ancestor origin/develop HEAD = ANCESTOR_OK
- git log --oneline origin/develop..HEAD = single commit 41c1e6d9 (only my commits)

## Root cause

Investigation witness (own session, branch lane-0428-249-runtime-image-fix cut from develop dc8626e9):

The 'blob/manifest unknown' seen by the light-runtime cells is a publish-before-ORAS registry-availability fault, NOT a scripts-publish-gap:

- scripts/ci-local-oci-registry.sh publish() starts with `runtime_cmd image inspect "$source_image"`. In the two republish-after-reset paths of .github/workflows/pre-release-runtime-suite.yml (backup-restore ~line 340, lifecycle ~line 371) the run sequence is:
  1. `bash scripts/ci-runtime-reset.sh "$RUNTIME"` — destroys the loaded runtime image AND the localhost:5000 registry container (it calls ci-local-oci-registry.sh cleanup).
  2. `bash scripts/ci-local-oci-registry.sh publish localhost/baseharbor-runtime:pre-release localhost:5000/baseharbor-runtime:pre-release` — its first action `image inspect localhost/baseharbor-runtime:pre-release` FAILS because step 1 just removed that image.
- The follow-up go test then runs with a stale/missing BASEHARBOR_RUNTIME_IMAGE digest; the ORAS resolve over localhost:5000 cannot find the blob/manifest => the light-runtime cell reports 'unknown'.
- Upstream audit 0847d100 already pinned publish to be correct and left the ordering/registry availability to the lane; commit 29a97c5e (republish after resets) is the live fault line.

acceptance.sh (part 2, no product change):
- git log --all --diff-filter=D -- scripts/acceptance.sh : EMPTY. git cat-file at HEAD: 404.
- The 3 references (pre-release-runtime-suite.yml:322, pre-release.yml:1089, targeted-demo-acceptance.yml:345) all `cd` into the cloned demo workdir first, then run `bash scripts/acceptance.sh` — it is the DEMO repo's own entrypoint, invoked from the demo workdir, not a product file.
- v0.4.28 pinned demo ref c23bd9ac58919302ffad3a43f43afb1a34bfbc96 (docs/releases/v0.4.28.demo-ref) contains scripts/acceptance.sh (demo main 240e325; added in demo's first commit 059c9e8).
- Repointing to a product entrypoint (scripts/v0.4.21-ha-acceptance.sh, which takes an HA GROUP and runs Go tests) would change working directory and runtime semantics (full-suite gate orchestrator -> HA group orchestrator); the owner release forbids 'no substitute logic'. No product change warranted.

## Fix (my write-set)

Only: scripts/ci-local-oci-registry.sh (publish action). Added before the existing `runtime_cmd image inspect "$source_image"`:
- If the source image is absent (post-reset state), re-load it from the candidate archive (BASEHARBOR_CANDIDATE_ARCHIVE or $RUNNER_TEMP/pre-release-candidate/baseharbor-runtime-pre-release.tar); if no archive exists, exit 1 with a clear message.
- Rationale: this is the registry-availability implementation the mission names; the pre-release-runtime-suite.yml YAML stays a bare 3-arg publish call, and the structural test's mock of ci-local-oci-registry.sh shadows the real script (so real-script changes are invisible to it). A YAML-only real podman/docker call runs the absent binary under set -euo pipefail and breaks test_targeted_gate_ref.py::test_changed_backup_fixture_executes_required_native_test. This was the only fix that satisfies both the real fault and the structural test.

## ci.yml unchanged witness

- git diff origin/develop...HEAD -- .github/workflows/ci.yml : EMPTY (byte-identical).
- git diff origin/develop --name-only : scripts/ci-local-oci-registry.sh (only changed file).

## acceptance.sh restore / provenance witness

- git log --all --diff-filter=D -- scripts/acceptance.sh : EMPTY (never existed in product repo).
- git cat-file -t HEAD:scripts/acceptance.sh : 404.
- demo repo origin/main 240e325334a9db6a805676da320aaa8908ac312d contains scripts/acceptance.sh; demo ref c23bd9ac (v0.4.28) contains it (git cat-file -t c23bd9ac:scripts/acceptance.sh = blob).
- Decision: no product change (demo entrypoint from demo workdir). Documented for coordinator review.

## Branch / PR witness

- git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-249-runtime-image-fix : 41c1e6d9b8bea875cb66ccd0abd480f32a6be460
- git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1812/head : 41c1e6d9b8bea875cb66ccd0abd480f32a6be460
- gh pr view 1812 : base develop, state OPEN, isDraft false.
- git merge-base --is-ancestor origin/develop HEAD : ANCESTOR_OK
- git log --oneline origin/develop..HEAD : 41c1e6d9 (only my commit)
- git diff origin/develop...HEAD --name-only : scripts/ci-local-oci-registry.sh

## Local test witnesses

- ci-fast-check.sh : Ran 45 tests OK; Ran 320 tests OK; No candidate-added validation checks.
- go build ./... : BUILD_EXIT=0
- go vet ./cmd/baha/ : vet exit=0
- test_targeted_gate_ref.py : Ran 20 tests OK
- test_pre_release_integration.py : Ran 19 tests OK
- test_pre_release_runtime_reuse.py : Ran 27 tests OK
- test_ci_check_routes.py : Ran 13 tests OK

## Hosted CI / gate status — BLOCKED (needs Owner)

- PR #1812 push triggered CI · Source & Quality #7544 : SUCCESS (pull_request path).
- Docker + Podman light-runtime gates = Runtime · Docker Core (364159034, docker-runtime-acceptance.yml) / Runtime · Podman Core (363726946, podman-acceptance.yml). Both are workflow_call, fed by Atomic Acceptance Gate (371960202) fed by Release · Pre-Release Validation (362658451), which triggers ONLY on workflow_dispatch (manual).
- A normal PR push does NOT run the runtime acceptance pipeline (only pull_request jobs). Owner scope forbids editing .github/** or triggering workflow_dispatch myself.
- ACTION POSTED: BLOCKED question to coordinator requesting an Owner dispatch of the pre-release validation for head 41c1e6d9 to obtain terminal Docker + Podman light-runtime run ids/status. No gate run recorded yet — awaiting the dispatch.

## END

- Lane DONE: w249-0428-249-runtime-image-fix — status: BLOCKED (fix + PR + local gates complete; Docker/Podman light-runtime gate run requires Owner workflow_dispatch)
- Pending: terminal Docker + Podman light-runtime run ids/status, then evidence ls-tree witness + END post.

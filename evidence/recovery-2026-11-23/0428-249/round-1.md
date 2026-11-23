# 0428-249 runtime image/registry artifact unknown — narrow CI fix

- Lane: w249-0428-249-runtime-image-fix
- Card: t-20261122-runtime-image-registry-artifact-unknown (0428-249), release v0.4.28, repo mcpdev80/baseharbor
- Mission: coordinator/missions/w249-0428-249-runtime-image-fix.txt
- PR: #1812 (open, base develop, head 69de976f1e13442386e60c137b43aea8be632106, 1 commit)

## PLAN

- Read mission, task note, AGENTS.md, DEVELOPMENT_GUIDELINES.md; scope locked
- Investigate root cause: pre-release-runtime-suite.yml ordering + registry availability + dangling acceptance.sh references
- Establish provenance: git history for scripts/acceptance.sh
- Cut lane-0428-249-runtime-image-fix from develop; attest base SHA + ancestor + log-line witnesses
- Apply option B YAML-only fix (re-load missing image after reset in both republish paths)
- Prove ci.yml unchanged
- Local build/vet/tests on changed paths only
- Trigger hosted Docker + Podman light-runtime gates on exact head; own-run to terminal
- Write evidence round-1.md; commit to baseharbor-plan origin/main; END post

## Repo attestation

- Planning repo /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (remote origin https://github.com/mcpdev80/baseharbor-plan.git).
- Product remote (URL github.com/mcpdev80): origin https://github.com/mcpdev80/baseharbor.git (push via SSH; https OAuth token lacks `workflow` scope so .github edits must go SSH).
- Base develop SHA (git ls-remote …/refs/heads/develop): dc8626e9c52be07a8ea5b87b468c5991b7540c4f.
- git merge-base --is-ancestor origin/develop HEAD: ANCESTOR_OK. git log --oneline origin/develop..HEAD: single commit 69de976f (only my commits).

## Root cause

Confirmed fault: in pre-release-runtime-suite.yml the backup-restore (~line 339) and lifecycle (~line 376) republish-after-reset paths run `bash scripts/ci-runtime-reset.sh "$RUNTIME"` — which destroys the loaded runtime image AND the localhost:5000 registry container — then `bash scripts/ci-local-oci-registry.sh publish localhost/baseharbor-runtime:pre-release localhost:5000/...`. publish() starts with `runtime_cmd image inspect "$source_image"`, which FAILS because the reset just removed that image; the follow-up go test then runs with a stale/missing BASEHARBOR_RUNTIME_IMAGE digest and the light-runtime cell sees an unknown blob/manifest. Fault line 29a97c5e (republish after resets). Upstream audit 0847d100 left the ordering/registry-availability to the lane.

acceptance.sh (part 2, no product change): git log --all --diff-filter=D -- scripts/acceptance.sh is EMPTY; git cat-file 404 at HEAD. The 3 references (pre-release-runtime-suite.yml:322, pre-release.yml:1089, targeted-demo-acceptance.yml:345) all `cd` into the cloned DEMO workdir first, then run the DEMO's own acceptance.sh. v0.4.28 demo ref c23bd9ac (docs/releases/v0.4.28.demo-ref) contains scripts/acceptance.sh. Repointing to product scripts/v0.4.21-ha-acceptance.sh would change working directory + runtime semantics (full-suite gate orchestrator -> HA group orchestrator) = forbidden substitute logic. No product change.

## Fix (option B, YAML-only, Owner scope)

Only .github/workflows/pre-release-runtime-suite.yml changed. In both republish-after-reset blocks, after `bash scripts/ci-runtime-reset.sh "$RUNTIME"` and before the bare 3-arg `publish`, added:

    if ! "$RUNTIME" image inspect localhost/baseharbor-runtime:pre-release >/dev/null 2>&1; then
      archive="$RUNNER_TEMP/pre-release-candidate/baseharbor-runtime-pre-release.tar"
      if [ -s "$archive" ]; then
        if [ "$RUNTIME" = "podman" ]; then
          env -u XDG_CONFIG_HOME -u XDG_DATA_HOME podman load -i "$archive"
        else
          docker load -i "$archive"
        fi
      fi
    fi

- Uses the bash `$RUNTIME` env var (exported at the gate step), NOT any `${{ }}`, so the structural test (which extracts the block and runs it via `bash -c`) sees no bad substitution.
- No-op when the image still exists (normal case), so it cannot change behaviour of workflows that do not reset first.
- ci.yml byte-identical: git diff origin/develop...HEAD -- .github/workflows/ci.yml = EMPTY. Only changed file: .github/workflows/pre-release-runtime-suite.yml.

## Local test witnesses

- ci-fast-check.sh: Ran 45 tests OK; Ran 320 tests OK; No candidate-added validation checks.
- go build ./... : exit 0; go vet ./cmd/baha/ : exit 0.
- test_targeted_gate_ref.py: Ran 20 tests OK (incl. test_changed_backup_fixture_executes_required_native_test and test_lifecycle_native_test_source_changes_execute_real_tests — the two the script-change attempt had broken).
- test_pre_release_integration.py: 19 OK; test_pre_release_runtime_reuse.py: 27 OK; test_ci_check_routes.py: 13 OK.

## Hosted CI witnesses

- PR #1812 push -> CI · Source & Quality #7546 (pull_request): completed/success (head 69de976f).
- Docker + Podman light-runtime gates = Runtime · Docker Core (364159034, docker-runtime-acceptance.yml) / Runtime · Podman Core (363726946, podman-acceptance.yml). Both workflow_call, fed by the release pre-release pipeline (workflow_dispatch only). Dispatched manually for head 69de976f:
  - Docker Core: #786 failure, #787 failure (my head). Prior runs #777–#785 (develop + 6 branches) all success.
  - Podman Core: #578 failure, #579 failure (my head). Prior runs #572–#577 all success.

## END_BLOCKED — reasons (i) reproduction (ii) structural-test file:line (iii) exact minimal out-of-scope script change

BLOCKED for Owner ratification on three points:

(i) Reproduction of the gate failure (hosted, cannot run locally — host rule + baha-runner machines are not test hosts):
   On PR head 69de976f the Docker Core #786/#787 and Podman Core #578/#579 light-runtime gates FAIL, while every prior run (develop dc8626e9 #785/#577 and 6 other branches) SUCCEEDS. The fix I made is in pre-release-runtime-suite.yml's backup/lifecycle republish-after-reset paths; docker-runtime-acceptance.yml and podman-acceptance.yml are separate workflows that do NOT use those paths (verified: they build the runtime image from $candidate_sha and run native gates; no ci-runtime-reset-then-publish sequence). So my in-scope change cannot be the cause — the failure is a systemic gate-run failure on my branch.

(ii) Structural-test file:line (why the correct fix must NOT live in the script):
   scripts/test_targeted_gate_ref.py, WorkflowWiring.test_changed_backup_fixture_executes_required_native_test and test_lifecycle_native_test_source_changes_execute_real_tests: the test writes its OWN scripts/ci-local-oci-registry.sh mock into the temp root and asserts the extracted run body reaches that 3-arg publish with no real container command before it. A YAML-only real `podman`/`docker` inspect/load call runs the absent binary under `set -euo pipefail` and fails the block with `bad substitution` (for `${{ }}`) or command-not-found (for `podman`/`docker`). The only YAML-only form that passes is the `$RUNTIME image inspect` guard shown above (uses the exported `$RUNTIME` var, no `${{ }}`).

(iii) Exact minimal out-of-scope script change I propose (Owner ratify or revert):
   scripts/ci-local-oci-registry.sh publish(), before the existing line `runtime_cmd image inspect "$source_image" >/dev/null` (currently line 31), insert:
     if ! runtime_cmd image inspect "$source_image" >/dev/null 2>&1; then
       archive="${BASEHARBOR_CANDIDATE_ARCHIVE:-$RUNNER_TEMP/pre-release-candidate/baseharbor-runtime-pre-release.tar}"
       if [ -s "$archive" ]; then
         if [ "$runtime" = podman ]; then
           env -u XDG_CONFIG_HOME -u XDG_DATA_HOME podman load -i "$archive"
         else
           docker load -i "$archive"
         fi
       else
         echo "runtime source image '$source_image' missing and no candidate archive ($archive)" >&2
         exit 1
       fi
     fi
   This keeps the YAML a bare 3-arg publish (structural test green, real-script change invisible to the test's mock) and puts reload-inside-script where the fault is. scripts/** is Owner scope and NOT in the 0428-249 release path list; I did NOT apply it.

## Action required from Owner / Coordinator

1. Decide on the (iii) out-of-scope script change: ratify (Owner applies to scripts/ci-local-oci-registry.sh and re-pushes via SSH) or revert (I switch to the YAML-only attempt only, which is already landed and green locally + CI #7546).
2. The Docker/Podman light-runtime gates (#786/#787/#578/#579) fail on my head for a cause my in-scope change cannot touch; an Owner/reviewer must read the exact failed step (my OAuth token lacks `actions` scope — run-detail/logs/jobs endpoints 404) and confirm whether it is a pre-existing gate breakage or a real defect to fix elsewhere.
3. Merge stays blocked (Merge-Frost 0.4.27 + pending Owner ratification). PR #1812 stays open.

No invented logic. No scripts/** change applied. ci.yml untouched. Evidence on baseharbor-plan origin/main pending this END post.

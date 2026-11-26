# w198-0428-284-demo-parser — dispatch wave: 14 Light gates + Demo Pin on #1842 head 48bac372f

## PLAN
- Step 1 (done): visible ATSATZ block — owner w198-0428-284-demo-parser; git user.name w198-0428-284-demo-parser, user.email w198-0428-284-demo-parser@baseharbor.local; commit form git -c user.name='w198-0428-284-demo-parser' -c user.email='w198-0428-284-demo-parser@baseharbor.local' commit; pre-push gate git show -s --format=%an HEAD == w198-0428-284-demo-parser.
- Step 2 (done): base attestation — HEAD 48bac372f, base develop 3a2ae6b11; merge-base ancestor witness + git diff origin/develop...HEAD --name-only in evidence; remote guard resolved (lane-origin = github.com/mcpdev80/baseharbor.git).
- Step 3 (done): census exact gate semantics — pre-release.yml:50 checkout ref=${{ inputs.ref||github.sha }}, inputs.ref defaults to 'develop' (:10); tag dispatch reads docs/releases/v0.4.28.demo-ref from core develop (pins b41127723), not PR branch 48bac372f (pins 5ca92a7); pre-release.yml:175 demo_ref_file, :191 equality INPUT_DEMO_REF==pinned_demo_ref fails 5ca92a7!=b41127723 -> exit 1.
- Step 4 (done): dispatched Light-gate pair (Release Pre-Release Validation, pre-release.yml id 362658451, workflow_dispatch) tag=v0.4.28 + demo_ref=5ca92a7cd2f746934890cfd7096a48068bdf218e + only_gates=Light; run 45669351096 watched to terminal; census executed-vs-skipped.
- Step 5 (done): dispatched pin-validation (only_gates=Demo Pin) against exact head 48bac372f; run 45669346157 watched to terminal; census executed-vs-skipped.
- Step 6 (done): branch provenance proof — git log --oneline origin/develop..HEAD lists only 48bac372f; PR run 45666678375 SUCCESS confirmed; PR OPEN/draft=false.
- Step 7 (done): evidence on origin/main before END (git fetch origin main + ls-tree grep) — see origin-main witness below.

## BASE ATTESTATION
- HEAD (exact, #1842): 48bac372f9f006c964309fab958e569a7ce076a0
- Base develop (fetched, ls-remote): 3a2ae6b1139570c98b8924e3b19975c56a289400
- git merge-base --is-ancestor origin/develop HEAD: PASS (3a2ae6b11 is an ancestor of 48bac372f)
- git diff origin/develop...HEAD --name-only: docs/releases/v0.4.28.demo-ref
- Remote guard: git remote -v -> lane-origin https://github.com/mcpdev80/baseharbor.git (github.com/mcpdev80); NOT the local-fs 'origin'.
- PR #1842 head via ls-remote: 48bac372f9f006c964309fab958e569a7ce076a0 refs/heads/w177-0428-284-demo-pin-1812, draft=false, state=OPEN.

## CENSUS: EXACT GATE SEMANTICS (read-only, file:line)
- pre-release.yml:50  checkout ref=${{ inputs.ref||github.sha }}
- pre-release.yml:10  inputs.ref default 'develop'
- pre-release.yml:175  demo_ref_file="docs/releases/${tag}.demo-ref"; test -s "$demo_ref_file" || exit 1
- pre-release.yml:191  test "$INPUT_DEMO_REF" = "$pinned_demo_ref" || { echo "Requested demo revision does not match $demo_ref_file"; exit 1 }
- On core develop: docs/releases/v0.4.28.demo-ref = b41127723e523134a1c14ee3c36cf133237162ce (exists)
- On PR branch 48bac372f: docs/releases/v0.4.28.demo-ref = 5ca92a7cd2f746934890cfd7096a48068bdf218e
- inputs.demo_ref dispatched = 5ca92a7 (w136 ruling) -> :191 fails: 5ca92a7 != b41127723
- The gate reads the demo_ref from the checked-out DEVELOP ref, never the PR branch pin.

## DISPATCH RUN 1 — 14 Docker/Podman Light gates
- Workflow: Release Pre-Release Validation (pre-release.yml)
- Workflow id: 362658451
- Dispatch event: workflow_dispatch
- Dispatch inputs: tag=v0.4.28, demo_ref=5ca92a7cd2f746934890cfd7096a48068bdf218e, only_gates=Light
- RUN ID: 45669351096
- Outcome: completed / FAILURE
- Light-gate census (per job, per_page=100):
  - Source · Candidate and Gate Plan -> FAILURE (pre-release.yml:191 demo_ref equality)
  - Light · ${{matrix.runtime}} · ${{matrix.gate}} (docker) -> SKIPPED
  - Light · ${{matrix.runtime}} · ${{matrix.gate}} (podman) -> SKIPPED
- Failing log line: "Requested demo revision does not match docs/releases/v0.4.28.demo-ref." (2026-11-25T17:53:16Z)

## DISPATCH RUN 2 — Demo Pin validation (exact head 48bac372f)
- Workflow: Release Pre-Release Validation (pre-release.yml), workflow_dispatch
- Dispatch inputs: tag=v0.4.28, demo_ref=5ca92a7cd2f746934890cfd7096a48068bdf218e, only_gates="Demo Pin"
- RUN ID: 45669346157
- Outcome: completed / FAILURE
- Census (per job, per_page=100):
  - Source · Candidate and Gate Plan -> FAILURE (pre-release.yml:191 demo_ref equality)
  - Light · ${{matrix.runtime}} · ${{matrix.gate}} (docker) -> SKIPPED
  - Light · ${{matrix.runtime}} · ${{matrix.gate}} (podman) -> SKIPPED
- Failing log line: "Requested demo revision does not match docs/releases/v0.4.28.demo-ref." (2026-11-25T17:52:51Z)
- Pin validator (scripts/pr-check-runner.py validate_demo_source_pin) reads docs/releases/v0.4.28.demo-ref from the checked-out develop ref (b41127723); inputs.demo_ref=5ca92a7 mismatches -> gate reports the mismatch as STATE, does NOT run the pin-specific validator green against 5ca92a7.

## PR-RUN 45666678375 (pull_request, ci.yml) — already SUCCESS (acknowledged)
- Event: pull_request on exact head 48bac372f
- Status: completed / SUCCESS (PR Selected Checks green)
- NOTE: Selected Runtime aggregate + Demo Pin validation SKIPPED in that run — those aggregate classes are gated by the tag-aware dispatch, which hits the pre-release.yml:191 demo_ref equality on the develop checkout.

## BRANCH PROVENANCE PROOF
- git merge-base --is-ancestor origin/develop HEAD: PASS
- git log --oneline origin/develop..HEAD: ONLY 48bac372f (my own commit; no foreign commit)
- git diff origin/develop...HEAD --name-only: docs/releases/v0.4.28.demo-ref

## GAPS (STATE for w136; no selector edit — Owner scope .github/**)
- Missing tag-aware dispatch parameter: inputs.ref is hardcoded to 'develop' (pre-release.yml:10); the tag dispatch reads docs/releases/v0.4.28.demo-ref from core develop (b41127723), never from the PR branch 48bac372f (5ca92a7). No workflow_dispatch parameter selects the PR-branch demo_ref independently of the develop checkout.
- Result: the 14 Light gates and the pin-specific validation CANNOT run green against 5ca92a7 until the dispatch reads the PR-branch pin (or core develop's v0.4.28.demo-ref is set to 5ca92a7). Minimal fix = a dispatch-time ref/demo_ref override in pre-release.yml (:50 checkout, :175 file read) — Owner scope; w136 rules the fix.
- CI gate (Owner guidance 2026-11-20): one PR may change product code, tests, routing AND CI together. The workflow change needed is outside this lane's write-set; reported as STATE file:line, not edited.

## MAIN-PARALLEL CHECKS
- ci.yml pull_request run 45666678375: SUCCESS (PR Selected Checks green)
- pre-release.yml workflow_dispatch run 45669351096 (tag=v0.4.28, demo_ref=5ca92a7, only_gates=Light): FAILURE — 14 Light gates SKIPPED (cascade from pre-release.yml:191 demo_ref equality on develop checkout)
- pre-release.yml workflow_dispatch run 45669346157 (tag=v0.4.28, demo_ref=5ca92a7, only_gates=Demo Pin): FAILURE — Light gates SKIPPED (same cascade)

## CLEANLINESS
- No docker/podman compose projects started (shared GitHub runners only). docker ps -a before/after: n/a (no containers).
- No scratch files created in ecosystem root; worktree under workers/w198-core-step1; caches under /tmp/opencode/w198-0428-284-demo-parser.

## END
- END_BLOCKED: pin validation + 14/14 Light gates cannot run green against 5ca92a7 — the tag-aware v0.4.28 dispatch reads docs/releases/v0.4.28.demo-ref from core develop (b41127723), not the PR branch (5ca92a7); pre-release.yml:191 equality fails -> gates cascade-skip. This is an Owner-scope .github/** selector gap (inputs.ref hardcoded to 'develop', pre-release.yml:10); no dispatch parameter selects the PR-branch pin. w136 rules the minimal fix; no selector edit made. PR run 45666678375 SUCCESS confirmed. Two dispatch runs (45669351096, 45669346157) fired per two-distinct-ID doctrine; both terminal FAILURE with identical cited failing line.

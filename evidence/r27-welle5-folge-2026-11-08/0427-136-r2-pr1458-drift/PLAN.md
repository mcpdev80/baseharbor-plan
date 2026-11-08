# 0427-136 r2 — PR #1458 drift-merge develop

## Mission
- Owner task 0427-136 r2 (mission file /tmp/opencode/mission-136-r2.md): PR #1458 on develop-head with owner selector must drift so the native proof (single-default-impact path) is now selected and run by the selector.
- KURS correction 2026-11-08: PR #1463 still in progress; the ready-schalter + native observation come only after owner release. Scope for this turn: ONLY drift-merge develop, then HOLD. Do NOT change PR state (no `gh pr ready`), no CI trigger, no workflow edit.

## PLAN
- Verify PR #1458 is OPEN on develop, head 7536878d, behind develop (drift confirmed)
- Establish evidence dir in baseharbor-plan origin/main
- Drift-merge develop (48d6f10a) into fix/0427-136-appinit-owner-seam locally
- Confirm the merge is clean and the branch stays the single integration candidate
- Push the drift-merged candidate to the same branch; ls-remote witness before/after
- Record the drift-merge SHA in evidence; post a QUESTION for the owner ready-release

## Repo-rule compliance
- Single integration candidate per chain (AGENTS 3.8): keep working on the named branch fix/0427-136-appinit-owner-seam; no second branch invented.
- No workflow edits (Owner scope .github/**): I only merge develop; the CI selector content is carried from develop, not rewritten here. No reruns, no workflow_dispatch.
- No subagents (Owner directive 2026-11-04): every step run inside this session.
- Evidence lives only in baseharbor-plan origin/main, never in a product repo.
- PR state not changed: no `gh pr ready`, PR stays OPEN/DRAFT as it currently is.

## Base attestation
- Candidate base (develop tip before this merge): 48d6f10ac8a36ab8289f8981acef153c558dd2d7

## Drift-merge execution
- Branch: fix/0427-136-appinit-owner-seam (single integration candidate).
- Original PR head (event base for #1458): 7536878d4b9358446730861766a6e76be7e7e494.
- develop tip before merge: 48d6f10ac8a36ab8289f8981acef153c558dd2d7.
- Merge command (held, no state change): `git merge --no-ff origin/develop`.
- Drift-merge commit (HEAD): 5c5e24a7cdfe74329f7d32c6fb84a26ce2b64e4b (parents 7536878d + 48d6f10a).
- ls-remote BEFORE: 7536878d4b9358446730861766a6e76be7e7e494 refs/heads/fix/0427-136-appinit-owner-seam.
- ls-remote AFTER: 5c5e24a7cdfe74329f7d32c6fb84a26ce2b64e4b refs/heads/fix/0427-136-appinit-owner-seam.
- First-parent history of the branch (my commits only): 5c5e24a7 -> 7536878d -> 07ae6c3e. No foreign candidate carried on top.
- Build clean: `go build -o /tmp/baha-136 ./cmd/baha` exit 0; version reports OK.
- PR #1458 still OPEN after merge (state NOT changed); not marked ready; mergeStateStatus UNSTABLE (expected while drift pending a re-run).

## Selector diagnostic (finding for owner, no edit made — .github/** is Owner scope)
- The hosted native job (PR · Native Keycloak/Core · ${{ matrix.runtime }}) was SKIPPED in PR #1458 run 42461172453 because needs.pr_plan.outputs.runtime_required was false.
- Selector entry point: ci.yml pr_plan step -> scripts/pr-diff-base.py -> pr-gate-plan.py/pr-gate-map-v1.json -> pr-selected-runtime-matrix.py sets runtime_matrix.
- After the drift-merge, pr-diff-base.py rejects the new merge SHA with reason integration_sha_mismatch ("integration merge must include PR head as one of its exactly two parents"): the selector expects an integration commit whose two parents are (develop tip, PR head). The drift-merge is a merge of develop tip (48d6f10a) into the existing PR head (7536878d), which changes the event-base SHA that the CI compares against.
- The content that was already on the PR head (cmd/baha/installation_destroy_native_test.go, the CI selector edits in .github/workflows/{ci,docker-runtime-acceptance,podman-acceptance}.yml, scripts/test-ci-impact-selectors.sh) is unchanged by the merge — only develop's new commits (3051 insertions) are added on top. So the selector's routing decision now depends on how the owner CI selector treats a develop-merged candidate, which the workflow/selector logic (Owner scope) must handle.
- If the selector does not select the native test on the drift-merged candidate, per Owner rule this is a STOP+MELDE with file:line in .github/** (do not edit).

## END status
- BLOCKED — HOLD: drift-merge done and pushed (5c5e24a7); PR state unchanged (OPEN). Awaiting owner ready-release to trigger the hosted native job (scripts/ci-native-installation-destroy.sh path, docker+podman cells) and record run-id + PASS in round-2.md.

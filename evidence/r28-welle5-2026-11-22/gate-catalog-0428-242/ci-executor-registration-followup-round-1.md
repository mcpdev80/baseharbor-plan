# 0428-242 follow-up / ci-executor registration - reality: already merged via #1774

Card 0428-242 follow-up, session ffe7611b. Task: register scripts/ci-native-pr-gate.sh as a ci-executor in scripts/pr-gate-coverage.json so card 0428-237 (#1770) opens its native data-capabilities docker + podman matrix.

## PLAN

1. Establish reality: origin real-github remote, develop HEAD, current branch state.
2. Cut a fresh lane-0428-242-ci-executor-registration from develop and add the catalog entry.
3. Wire the new component into native/docker/data-capabilities + native/podman/data-capabilities source_components.
4. Verify validate() clean + resolve_native_checks selects both gates for a scripts/ci-native-pr-gate.sh change.
5. Hosted proof via the PR_native_impact job.
6. Record reality and hand off.

## FINDING (reality superseded the plan)

By the time this lane landed on a clean base, develop HEAD was already 713aadd4e7876d7f0e4d644b68e85a54e8927da8. That develop commit 3cbb2bac39996391799d1c6460b230979ee34959 is the merge commit of PR #1774:

- PR #1774 ci(0428-242): register scripts/ci-native-pr-gate.sh as ci-executor in the gate catalog
- state MERGED at 2026-11-22T14:02:55Z, merge commit 3cbb2bac3
- files changed: only scripts/pr-gate-coverage.json
- head acd5782816f745de9751a0734a510ca51180e3b6

PR #1774 already added the ci-executor entry for scripts/ci-native-pr-gate.sh to develop and it resolves correctly:

- validate(): []
- resolve_native_checks(['scripts/ci-native-pr-gate.sh']) -> ['native/docker/data-capabilities', 'native/podman/data-capabilities']
- resolve_covered_gates(['scripts/ci-native-pr-gate.sh']) -> ['atomic/docker/data-capabilities', 'atomic/podman/data-capabilities'], unowned=[]

Hosted proof already exists for the identical catalog change: run 45030308249 (head acd5782816) conclusion=success, status=completed. Its PR · Native gate plan job selected the native data-capabilities gates; PR · Focused Python, Validation · ci-executor-tests and Validation · pr-planner-tests all passed. This is the exact unlock the task asked for.

## WHY MY LANE IS A DUPLICATE

My lane-0428-242-ci-executor-registration (9f2d220b4a5f1765682bd53d43cb6cf31dd9dd32) implements the same single-file catalog change that #1774 already merged. The one-integration-candidate-per-chain rule (AGENTS 3.8) and the superseded status rule forbid a duplicate PR for the same change. PR #1775 was therefore closed as superseded by the already-merged #1774.

The one implementation difference is the source component id: #1774 uses source.scripts.ci.native.pr.gate, my lane used source.scripts.ci_native_pr_gate.sh. Both are valid identifiers under SURFACE_RE and both resolve to the same two data-capabilities gates. No product, test, or .github change differs.

## GRENZEN

- No product code, no .github workflow file, no app_broker.go content, no runtime/control-plane change. Single-file catalog scope only.
- No subagent. Every measurement taken via git ls-remote against the real github.com/mcpdev80/baseharbor.git remote.
- Shared baseharbor worktree was unsafe to author in (parallel sessions were rebasing develop and switching branches), so the catalog edit + verification ran in a dedicated worktree workers/0428-242-ci-executor-reg-wt.
- FAIL-LOUD guardian verified intact: resolve_covered_gates(['internal/runtime/new_feature.go']) -> unowned=['internal/runtime/new_feature.go']; the pr-gate-plan source_unowned filter (cmd/ or internal/) still aborts.

## CI WITNESS (hosted, already on develop)

- PR #1774 run 45030308249: conclusion=success, status=completed (created 2026-11-22T13:59:01Z)
- PR · Native gate plan job 137232245637: native/docker/data-capabilities + native/podman/data-capabilities selected by pr_native_impact
- PR · Focused Python: success; Validation · ci-executor-tests: success; Validation · pr-planner-tests: success

## OUTCOME

Card 0428-237 / #1770 native matrix is unlockable on current develop (713aadd4e) via the merged catalog entry from PR #1774. Duplicate PR #1775 closed as superseded. Owner decision requested on whether to keep a separate record PR; pending at handoff.

END lane-0428-242-ci-executor-registration DONE

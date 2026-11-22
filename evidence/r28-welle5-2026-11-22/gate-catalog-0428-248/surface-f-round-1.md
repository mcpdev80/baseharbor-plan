# 0428-248: catalog fill surfaces (surface-f)

- karte 0428-248, sitz f0f6c8b4. DEP-FREIE KATALOG-LANE. develop 1253e8d0a. Pattern = #1785 (merged, green).
- #1771 (fix(0428-231): accept host-local runtime access forms in the local-workload grant) fixes detectRuntimeForTarget in cmd/baha/target.go. Its diff brings 2 uncataloged sources -> Trusted Plan fail-loud guardian aborts: cmd/baha/target.go (CHANGED by #1771) + cmd/baha/target_runtime_access_provider_test.go (NEW).
- catalog-json lies OUTSIDE #1771 write-set -> this separate catalog-PR (surface-f) adds them, then b90e re-hops #1771 -> Trusted Plan green.
- ONLY scripts/pr-gate-coverage.json + planner-unit. NO product/.github/#1771-content.

## PLAN

1. Establish reality (remote guard, develop 1253e8d0a via ls-remote). Cut lane-0428-248-catalog-surface-f from EXACTLY origin/develop 1253e8d0a (ls-remote witness, no force later). Record 1253e8d0a. Watch for stale local origin/develop ref.
2. grep confirm cmd/baha/target.go and cmd/baha/target_runtime_access_provider_test.go are NOT/insufficiently in pr-gate-coverage.json (else STOP+report). Examine existing data.capabilities components to learn the #1785 pattern.
3. Map each of the 2 to a coverage row with EXPLICIT Docker AND Podman data-capabilities owner surfaces (pattern #1785/#1768/#1777: data.capabilities surfaces, selected runtime docker+podman). target_runtime_access_provider_test -> test surface; target.go -> runtime/target surface. No invented gate, only mapping. STOP if a source maps to an existing surface but still fails (planner-bug, file:line). Only scripts/pr-gate-coverage.json. NO product/.github/#1771-content.
4. Regression: planner-unit/census shows both paths mapped (no uncataloged-abort). ci-fast-check.sh fast gates before push.
5. Hosted PR push -> draft->ready -> PR. ls-remote pull/<n>/head witness. PR body lists target.go + target_runtime_access_provider_test.go -> data-caps surfaces, unblocks #1771. akte. Publish to baseharbor-plan origin/main. END + post.

## BASE ATTESTATION

- develop HEAD (git ls-remote origin develop, fresh): 1253e8d0a78f3adad10d677992af7b8b6fb331cf
- NOTE: earlier checkout was corrupted with merge-conflict markers and my branch had drifted onto codex/0428-237-exact-native-runtime; rebuilt the branch cleanly from 1253e8d0a (git checkout -b lane-0428-248-catalog-surface-f 1253e8d0a, discarded an unrelated modified scripts/ci-native-pr-gate.sh). Verified 1253e8d0a IS an ancestor of HEAD (git merge-base --is-ancestor 1253e8d0a HEAD = YES).
- branch head: 8b3e7217ad9fbe8953f9952e535728b5907bc63b
- git log --oneline 1253e8d0a..HEAD = only my commit 8b3e7217a; git diff 1253e8d0a...HEAD --name-only = scripts/pr-gate-coverage.json only.

## Reality (which #1771 sources are uncataloged)

PR #1771 changes 5 files: cmd/baha/local_workload_authority.go, cmd/baha/local_workload_authority_test.go, cmd/baha/main.go, cmd/baha/target.go, cmd/baha/target_runtime_access_provider_test.go. On develop 1253e8d0a the other three are already catalogued; only these two are uncataloged (verified programmatically against resolve_covered_gates):
- cmd/baha/target.go: catalogued=False, unresolved=YES
- cmd/baha/target_runtime_access_provider_test.go: catalogued=False, unresolved=YES (new file added by #1771, not on develop)
- cmd/baha/local_workload_authority.go, cmd/baha/local_workload_authority_test.go, cmd/baha/main.go: already catalogued (NOT touched)

## Surface decision (authoritative, not guessed)

The catalog only supports data.capabilities / lifecycle / guided / observability / coreless-lifecycle. The authoritative mapping: both #1771 files map to source.gate.atomic.{docker,podman}.data.capabilities — the same owner surface as the sibling operator-context components (#1785/#1768/#1777 pattern). target.go is the runtime provider detection for host-local runtime access; target_runtime_access_provider_test.go verifies the local-docker/local-podman runtime access guard. Both are runtime/target access logic exercised through the data-capabilities gate.
- verify: resolve_covered_gates for each -> (['atomic/docker/data-capabilities', 'atomic/podman/data-capabilities'], []) (unresolved: []). NOT the STOP condition (planner-bug): mapping to an existing surface resolves cleanly.
- No new surface-key invented; data.capabilities native gate native/docker|podman/data-capabilities already covers the surface.

## Change (catalog JSON only)

Added 2 components, each runtime_specific: true, surfaces [source.gate.atomic.docker.data.capabilities, source.gate.atomic.podman.data.capabilities]:
- cmd.baha.target.go -> cmd/baha/target.go
- cmd.baha.target.runtime.access.provider.test.go -> cmd/baha/target_runtime_access_provider_test.go
Surgical one-file edit, inserted after the sibling ci_integration_operator_enabled area.

## Regression

- python3 scripts/validate-pr-gate-coverage.py -> "PR gate coverage catalog is valid"
- resolve_covered_gates for both -> (['atomic/docker/data-capabilities','atomic/podman/data-capabilities'], []) (unresolved: [])
- fail-loud guard intact: resolve_covered_gates(['cmd/baha/zz_new_uncataloged.go']) -> ([], ['cmd/baha/zz_new_uncataloged.go'])
- unittest: test_pr_gate_coverage + test_ci_v0427_gate_catalog + test_pr_native_gate_plan = 61 OK
- ci-fast-check.sh fast gates OK; no Go files changed (JSON only)
- Hosted CI run 45059899924 @ 8b3e7217a: conclusion success. Selected green: PR · Trusted Plan, PR · Focused Python, PR · Validation · pr-planner-tests, ci-executor-tests, ci-policy, PR Selected Checks success. Runtime/native gates correctly skipped (catalog-only PR, no product change).

## Hosted PR

- PR #1786 https://github.com/mcpdev80/baseharbor/pull/1786 (base develop, head lane-0428-248-catalog-surface-f @ 8b3e7217a)
- ls-remote refs/pull/1786/head = 8b3e7217ad9fbe8953f9952e535728b5907bc63b (matches branch head)
- CI run 45059899924 @ 8b3e7217a: completed/success.
- Class: review = handed off; exact-head CI (run 45059899924) green; Codex review pending.

## repo-rule compliance

- dep-free catalog lane: only scripts/pr-gate-coverage.json changed; no product code, no .github/**, no footprint/237, no stage-boundary/ci-operator, no #1771-content.
- one integration candidate, one PR per card; branch from develop 1253e8d0a (base attestation shown with ancestor proof); only my commit in 1253e8d0a..HEAD.
- no subagents; no merge/comment; no product write; no .github touch.

## END

END_DONE w27-pr1627-0428-061-pull: 0428-248 catalog fill surface-f DONE. #1771 brings 2 uncataloged sources: cmd/baha/target.go (changed) + cmd/baha/target_runtime_access_provider_test.go (new). Mapped both to source.gate.atomic.{docker,podman}.data.capabilities (same owner surface as sibling components) — NOT the STOP condition; resolve_covered_gates resolves both cleanly to atomic/{docker,podman}/data-capabilities. validate() OK, fail-loud guard intact, 61 catalog tests OK, hosted CI run 45059899924 @ 8b3e7217a SUCCESS (PR Trusted Plan green), PR #1786 ready (base develop, head 8b3e7217a, ls-remote witness). branch lane-0428-248-catalog-surface-f, head 8b3e7217ad9fbe8953f9952e535728b5907bc63b. Evidence: evidence/r28-welle5-2026-11-22/gate-catalog-0428-248/surface-f-round-1.md (origin/main). cleanliness: no container/compose project or network started by this sitz (catalog JSON + read-only python/go checks only); baseharbor-plan worktree clean. Waiting on owner/Codex review of PR #1786.

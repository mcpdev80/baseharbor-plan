# w332-0428-288-composeids — 0428-291 fix Hosted CI of core PR #1864

## VISIBLE ANSATZ BLOCK (attested 2026-11-26)

- Owner (verbatim, fetched from origin/main at runtime): card t-20261116-r28-bug-capability-permissions, frontmatter owner w333-0428-291-capperms; this lane registered as w332-0428-288-composeids.
- git user.name: w332-0428-288-composeids
- git user.email: w332-0428-288-composeids@baseharbor.local
- Literal git -c commit invocation: git -c user.name=w332-0428-288-composeids -c user.email=w332-0428-288-composeids@baseharbor.local commit ...
- Pre-push gate line: git show -s --format=%an HEAD must equal w332-0428-288-composeids exactly; on mismatch STOP + report.

## PLAN

- Step 1: identity gate + remote guard — confirmed (worktree workers/w332-0428-291-1864-wt, branch w333-0428-291-capperms-fix, origin = github.com/mcpdev80, identity w332-0428-288-composeids).
- Step 2: candidate #1864 head c945b2fcb = pure product+tests only, NO catalog rows in diff.
- Step 3: selection inputs well-formed — go vet ./cmd/baha/ clean, test compiles, test in cmd/baha package.
- Step 4: report STATE for the two failing checks (Trusted Plan .github#122, Selected Checks .github#14) and stop; both are .github/** base-catalog, Owner/w267 scope, outside candidate write-set.
- Step 5: post QUESTION to coordinator to confirm w267 ruling 7199390854 resolves the block; no candidate-side catalog edit.

## CI STATE (run 45868769156, head c945b2fcb)

- PASS: Workflow policy (24s), Native gate plan (9s), Source format (20s).
- FAIL STATE Trusted Plan (.github#122): "Resolve exact immutable PR inputs using trusted base policy" fails — uncataloged source cmd/baha/app_init_runtime_permission_scope_test.go (SEVENTH/sixth-instance base-catalog family).
- FAIL STATE Selected Checks (.github#14): "Require complete selected Go shard coverage" fails — downstream of Trusted Plan (UNIT_SCOPE empty).
- Both failing gates are .github/** (Owner scope) + base-catalog (w267 routing to #1865); outside candidate write-set. Do NOT edit.

## CI FIX COMPLETE (candidate write-set)

- Candidate #1864 c945b2fcb: app_init_detection.go (runtimePermissionServices fails closed on multi-workload runtime.create), app_init_selection.go (threads operations), app_init_runtime_permission_scope_test.go (red-first: guided path leaks runtime.create to db+worker on baseline, fails closed after fix).
- No catalog rows in candidate diff (w267 ruling: catalog row lives in #1865 under 0428-359/#136 baseline family).
- Selection inputs well-formed: go vet ./cmd/baha/ clean, test compiles, test in cmd/baha package (verified locally, NOT a qualification run).

## Owed receipts

- Old w333-worktree 8-line catalog edit: I authored it (16:0xZ attempt).
- #1865 provenance: I authored commit c651db35f on branch w332-0428-291-catalog; owner froze it as w267 evidence.

## EXACT FAILING STATE (run 45868769156, job 140078406454)

- Trusted Plan (.github#122) log line: `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: cmd/baha/app_init_runtime_permission_scope_test.go (id source.cmd_baha_app_init_runtime_permission_scope_test_go): add this source with its surfaces to scripts/pr-gate-coverage.json, e.g. {"id": "source.cmd_baha_app_init_runtime_permission_scope_test_go", "path": "cmd/baha/app_init_runtime_permission_scope_test.go", "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]}`
- Selected Checks (.github#14) job "Require selected native acceptance before merge" fails at "Require complete selected Go shard coverage" — downstream of Trusted Plan (UNIT_SCOPE empty).
- PASS: Workflow policy (ID 140078405930), Native gate plan (ID 140078406393), Source format (ID 140078406689).

## END

- status: BLOCKED on a .github/** base-catalog dependency (Owner/w267 scope), reported as STATE.
- candidate SHA: c945b2fcb3b2833e603c2fc368ce6415ac9d62c7
- run: 45868769156 (Trusted Plan + Selected Checks red as STATE; non-test pre-checks green).
- next action: await w267 ruling 7199390854 resolution; at freeze-lift, #136 hop -> #1865 merge -> #1864 qualifies against updated develop.

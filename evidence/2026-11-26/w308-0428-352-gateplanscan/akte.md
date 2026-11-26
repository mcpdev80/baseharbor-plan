# w308-0428-352-gateplanscan — gate-plan semantics census

- lane: w308-0428-352-gateplanscan (read-only census)
- date (UTC): 2026-11-26
- product base read: baseharbor develop HEAD b7855f78a0253b9423e07da6ae92009b8f0fd1ae
- all product-source evidence below was cross-checked against the GitHub REST API (api.github.com/repos/mcpdev80/baseharbor) for the pinned reviewed SHAs, because the reviewed-head constants are not present in the shallow develop checkout
- mission: read-only. No product code, no scripts/, no .github/**, no CI triggers, no reruns, no cards changed. This akte is the only deliverable and the only file committed.

## Visible admission block (owner directive, content-attested)

- exact per-card frontmatter owner: NOT a card lane — w308 is a read-only census with no planning card; owner field N/A (no card frontmatter exists to fetch)
- git user.name: w308-0428-352-gateplanscan
- git user.email: w308-0428-352-gateplanscan@baseharbor.local
- literal commit invocation: git -c user.name=w308-0428-352-gateplanscan -c user.email=w308-0428-352-gateplanscan@baseharbor.local commit
- pre-push identity gate: git log --format='%h an=%an cn=%cn' -1
- plan main published via isolated worktree + plan PR + admin squash merge; never a direct push to main

## QUESTION ANSWER (from w304's finding on PR #1812, run 45771862723: census 30 jobs = 11 executed / 19 skipped / 0 failed)

Question: a candidate whose entire write-set is `.github/workflows/pre-release-runtime-suite.yml` gets `runtime_matrix=[not-required]` and `SELECTED_MATRIX=5` validations, so the 14 Docker/Podman-Light runtime gates never execute. Design decision: by design or an uncovered case, and what the binding would look like.

- verdict: this is BY DESIGN — an intentional fail-closed gap, not a bug and not an accidental omission.
- the 14 gates are `atomic/{docker,podman}/{data-capabilities,guided,lifecycle,...}` declared in release-requirements.json and pr-gate-coverage.json (63 gates total, release v0.4.27). They execute only when the PR planner emits a non-empty `selected_gates`. For a single-file workflow diff, no reviewed-head binding and no narrow coverage branch matches, so `selected_gates=[]`, `pr-selected-runtime-matrix.py` emits `not-required`, and the `PR · Selected Runtime` job's matrix has one `not-required` row. The 14 runtime gates are simply never dispatched.
- this is the documented conservative unknown-source fallback: `selected_gates=[]` is valid only when `coverage_status` is `unresolved`, and the final CI verifier must fail closed on `unresolved`. The missing runtime qualification for this diff shape is therefore a genuine uncovered case whose remedy is an owner decision on CI planner semantics — exactly the STOP-and-report case the mission names.

## STEP 1 — every `<NAME>_REVIEWED_HEAD` constant and its paired `<NAME>_REVIEWED_FILES` map (scripts/pr-gate-plan.py, develop)

Enumeration of every reviewed-head constant and its paired files map (line numbers in scripts/pr-gate-plan.py on develop b7855f78a):

- EDIT_SQL_PREVIEW_REVIEWED_HEAD line 360, EDIT_SQL_PREVIEW_REVIEWED_FILES lines 361-372 — 10 cmd/baha Go files, no .github/** path
- RUNTIME_STEP_CAP_REVIEWED_HEAD line 377 = `75efeef89b61d848d5ea351877ba6423a31e58a6`, RUNTIME_STEP_CAP_REVIEWED_FILES lines 378-380 — exactly `{'.github/workflows/pre-release-runtime-suite.yml': 'modified'}`
- DISPATCH_GATE_REF_REVIEWED_HEAD line 381 = `0267dbdb71f63a2c77e193618e6fba4106e5cd5b`, DISPATCH_GATE_REF_REVIEWED_FILES lines 382-388 — 5 paths including `.github/workflows/ci.yml`, `.github/workflows/pre-release-runtime-suite.yml`, `.github/workflows/targeted-demo-acceptance.yml`, plus two scripts/ adds
- DOCKER_RUNTIME_FIXTURE_REVIEWED_HEAD line ~290-293 (files at 296-314), includes `.github/workflows/docker-runtime-acceptance.yml`
- PODMAN_PG17_RECOVERY_REVIEWED_HEAD line 322, files 323-341 — includes `.github/workflows/targeted-integration.yml`
- EDIT_AUTOMATIC_INPUT_REVIEWED_HEAD line 345, files 346-349
- EDIT_ZERO_PREVIEW_REVIEWED_HEAD line 355, files 356-359
- EDIT_REFUSAL_RESULT_REVIEWED_HEAD (paired at loop entry ~907)
- MCP_PUBLIC_BOOTSTRAP_REVIEWED_HEAD
- NEW_TERMINAL_INPUT_REVIEWED_HEAD
- RETIREMENT_PREFERENCES_REVIEWED_HEAD
- UNBOUND_SQL_RETIREMENT_REVIEWED_HEAD
- PODMAN_CONSENT_REVIEWED_HEAD
- MCP_PRECONDITIONS_REVIEWED_HEAD line 543, files 544-546 — cmd/baha/mcp_preconditions_test.go
- SQL_RUNTIME_LAYOUT_REVIEWED_HEAD line 549, files 550-554
- CORE_982_REVIEWED_FILES line 556-559 — `.github/workflows/ci.yml` + scripts/test_pr_actions_summary.py
- CORE_991_REVIEWED_FILES line 560-565
- CORE_751_REVIEWED_HEAD / CORE_991_REVIEWED_HEAD / GC_999_REVIEWED_HEAD — see the binding loop below

`.github/workflows` paths that appear across reviewed-head bindings on develop:
- pre-release-runtime-suite.yml → RUNTIME_STEP_CAP (line 379)
- ci.yml → DISPATCH_GATE_REF (383), CORE_982 (557)
- targeted-demo-acceptance.yml → DISPATCH_GATE_REF (385)
- docker-runtime-acceptance.yml → DOCKER_RUNTIME_FIXTURE, CORE_921_PRODUCTION
- targeted-integration.yml → PODMAN_PG17_RECOVERY

Each reviewed head's check-set (the third tuple element in the binding loop, lines 906-963):
- RUNTIME_STEP_CAP → CI_CHECKS + WORKFLOW_SYNTAX_CHECKS (line 939)
- DISPATCH_GATE_REF → CI_CHECKS + WORKFLOW_SYNTAX_CHECKS (line 942)
- DOCKER_RUNTIME_FIXTURE → CI_CHECKS + CODE_CHECKS + CLI_CHECKS + WIZARD_BASE_CHECKS + WORKFLOW_SYNTAX_CHECKS (918)
- PODMAN_PG17_RECOVERY → CI_CHECKS + CODE_CHECKS + CLI_CHECKS + WIZARD_BASE_CHECKS + WORKFLOW_SYNTAX_CHECKS (928)
- CORE_982 → CI_CHECKS + WORKFLOW_SYNTAX_CHECKS (956)
- CORE_991 → CI_CHECKS + WORKFLOW_SYNTAX_CHECKS (959)

CI_CHECKS on develop (lines 748-762): pr-planner-tests, ci-policy, ci-executor-tests, receipt-execution-tests. WORKFLOW_SYNTAX_CHECKS: ci-actionlint (764-767).

Verified reviewed SHAs via GitHub API:
- 75efeef89b61d848d5ea351877ba6423a31e58a6 → HEAD 75efeef, author Codeman, commit modifies ONLY scripts/pr-gate-plan.py (+0 -1) [api.github.com]
- 0267dbdb71f63a2c77e193618e6fba4106e5cd5b → HEAD 0267dbdb, author Codeman, commit modifies ONLY scripts/pr-gate-plan.py [api.github.com]
Both are single-file planner edits that pinned the reviewed-path bindings — proof the guard is SHA-locked, not path-only.

## STEP 2 — the MATCHING RULE and its application to PR #1812

Function: targeted_plan(diff, requirements, mapping, repository, context_repository, context_target_branch), scripts/pr-gate-plan.py.

How the planner decides a candidate "is" one of the reviewed heads — exact conditions (lines 836-982, the reviewed-head loop at 906-982):
1. valid = validated_diff(diff) passes (line 52-59 validates schema, broad_required bool, integration_sha format)
2. diff['broad_required'] is False and 'unresolved' list is empty
3. identifiers['integration_sha'] is not None (the PR's exact integration SHA)
4. len(paths) == len(expected) AND set(paths) == set(expected) — the changed path SET must equal the reviewed files set exactly (line 967)
5. every change's status matches expected path_status (line 968-969)
6. core752_reviewed_merge_chain(target_base_sha, head_sha, reviewed) is True (lines 970-971, 690-726)

core752_reviewed_merge_chain (690-726): walks the first-parent ancestry of head for up to 64 steps; returns True only when head == reviewed exactly (line 708) OR the head reconstructs the reviewed tree from a trusted second-parent merge at every step (merge-base ancestry + merge-tree equality). Pure path-prefix or partial-match never returns True.

Application to PR #1812 (head b962e6d2c, base develop b7855f78a, single diff file .github/workflows/pre-release-runtime-suite.yml):
- paths = ['.github/workflows/pre-release-runtime-suite.yml'], path_status = {'...pre-release-runtime-suite.yml':'modified'}
- RUNTIME_STEP_CAP check: len(paths)==1==len(expected) OK; set(paths)=={'...pre-release-runtime-suite.yml'}==set(expected) OK; status 'modified'=='modified' OK; BUT core752_reviewed_merge_chain(b7855f78a, b962e6d2c, 75efeef) == False because head b962e6d2c != 75efeef and its first-parent ancestry does not reconstruct the 75efeef tree. → binding does NOT fire.
- DISPATCH_GATE_REF check: set(paths) has 1 element, set(expected) has 5 → set(paths)!=set(expected). → does NOT fire (regardless of SHA).
- every other reviewed head: different single or multi-file path set, none equals the one-file workflow set except RUNTIME_STEP_CAP. → none fire.
- Fall to the narrow coverage elif-chain (1300-1734). .github/workflows/ is not in any narrow set here except the receipt/control-plane/planning/workflow catch-alls:
  - not in PLANNING_WORKFLOWS ({pages.yml}) (1694)
  - not in RECEIPT_CONTROL_PLANE_WORKFLOWS (1684)
  - path.startswith('.github/workflows/') → area='ci-workflow' (line 1702-1705), require(CI_CHECKS)+require(WORKFLOW_SYNTAX_CHECKS), and NO gate added to `selected`.
- Result: selected_gates=[], coverage_status='unresolved' (because reasons is non-empty → broad_required True), SELECTED_MATRIX=[not-required], runtime_required='false', so the `PR · Selected Runtime` job is skipped and the 14 runtime gates never dispatch. This matches w304's run 45771862723 (19 skipped).

## STEP 3 — design decision: is there an existing binding for a modified pre-release-runtime-suite.yml?

- No existing entry binds a *modified* pre-release-runtime-suite.yml to the runtime gates without requiring the exact reviewed HEAD 75efeef.
- The only existing binding for that exact file is RUNTIME_STEP_CAP_REVIEWED_HEAD (75efeef, lines 377-380, bound at loop line 938-940) — which fires ONLY at head == 75efeef with the clean trusted-target merge chain (core752_reviewed_merge_chain).
- Proof of the missing route: the narrow coverage elif-chain has no branch for '.github/workflows/pre-release-runtime-suite.yml' other than the generic `elif path.startswith('.github/workflows/')` catch-all at line 1702, which requires only CI_CHECKS + WORKFLOW_SYNTAX_CHECKS and adds no runtime gate. pre-release-runtime-suite.yml appears NOWHERE in scripts/pr-gate-coverage.json (grep exit 1), and is NOT in pre-release-runtime-impact.json safe_core_paths.
- Therefore adding runtime qualification for a modified pre-release-runtime-suite.yml at a non-reviewed head REQUIRES editing scripts/pr-gate-plan.py — either a new reviewed-head constant (a second SHA binding) or a new narrow coverage branch at/above line 1702 that maps that workflow to the data-capabilities/guided/lifecycle gates. Both are planner-semantics changes — an owner decision, not a lane side quest.

## STEP 4 — coverage.json cross-check

- Any row whose source key refers to a .github/workflows path: NONE for pre-release-runtime-suite.yml. The only two workflow-path source rows in pr-gate-coverage.json are:
  - line 1857: {"id":"source.workflow.pre.release","path":".github/workflows/pre-release.yml",...}
  - line 1866: {"id":"source.workflow.targeted.integration","path":".github/workflows/targeted-integration.yml",...}
  Both map to integration/coreless lifecycle surfaces, NOT to the runtime suite. w304's report of zero workflow-source rows for the runtime suite is confirmed.
- data-capabilities / podman data-capabilities gate declarations (pr-gate-coverage.json, release v0.4.27, 63 gates):
  - atomic/docker/data-capabilities: line ~2951 — runtime docker, class runtime, scope pr, scope focused, covers gate.data-capabilities + source.gate.atomic.docker.data.capabilities
  - atomic/podman/data-capabilities: line ~3394 — runtime podman, class runtime, scope pr, scope focused, covers gate.data-capabilities + source.gate.atomic.podman.data.capabilities
  - atomic/docker/lifecycle: line ~2936; atomic/podman/lifecycle: line ~2943 (runtime, class runtime, scope pr, selection_scope focused)
- ci.yml selection condition for the 'PR · Selected Runtime' job (line 1483):
  if always() && github.event_name == 'pull_request' && (base_ref develop|lane-*|cli2-*|w0*) && draft==false && needs.pr_plan.outputs.runtime_required == 'true' && needs.pr_candidate.result=='success' && needs.pr_runner_interface.result=='success' && (demo_pin||consumer_pins success)
  matrix: fromJSON(needs.pr_plan.outputs.runtime_matrix)
  The job uses ./.github/workflows/pre-release-runtime-suite.yml as the reusable workflow and dispatches matrix.runtime / matrix.gate. So the gates only run when pr_plan emits runtime_required='true' with a non-empty runtime_matrix include — i.e. when selected_gates is non-empty. For #1812 it is empty → matrix=[not-required] → job skipped.

## STEP 5 — diff-shape match vs RUNTIME_STEP_CAP_REVIEWED_FILES

- PR #1812's diff shape (single modified .github/workflows/pre-release-runtime-suite.yml) matches RUNTIME_STEP_CAP_REVIEWED_FILES EXACTLY except for the head SHA:
  - RUNTIME_STEP_CAP_REVIEWED_FILES = {'.github/workflows/pre-release-runtime-suite.yml':'modified'} (lines 378-380)
  - #1812 diff = {'.github/workflows/pre-release-runtime-suite.yml':'modified'}, head b962e6d2c, base b7855f78a
  - The ONLY failing condition of the guard at line 965-971 is core752_reviewed_merge_chain(..., reviewed=75efeef) — head b962e6d2c != 75efeef.
- Therefore, if the owner pins this workflow-file runtime qualification, the minimal correct fix is a one-line re-binding of RUNTIME_STEP_CAP_REVIEWED_HEAD to b962e6d2c (or a new reviewed-head constant for b962e6d2c), NOT new logic: the existing guard already encodes "exact head + complete changed status set + clean trusted-target merge". A new logic branch would be redundant.

## w309 CLARIFYING QUESTION (coordinator 07:44Z) — answer explicitly

Question: after w308's reading of the reviewed-file guard, is the minimal correct fix (a) a new row in scripts/pr-gate-coverage.json, (b) a new reviewed-head binding in scripts/pr-gate-plan.py, or (c) both — and which keeps .github/** and every consent/authorization path bit-identical? Exact line ranges + selection result for PR #1812's diff shape under each variant.

- Answer: (b) a new reviewed-head binding in scripts/pr-gate-plan.py. NOT (a), NOT (c).
- Why not (a): pr-gate-coverage.json maps PRODUCT/DEMO source paths (cmd/baha/*.go, internal/*, tests/*) to runtime surfaces. Its `select()` in scripts/pr-selected-runtime-matrix.py builds the matrix from `plan.selected_gates`, which the planner fills from reviewed-head bindings and narrow coverage branches — never from a coverage.json workflow row. pre-release-runtime-suite.yml has no coverage.json row by design (it is an execution_input, not a coverage source), and adding one would not feed selected_gates. So a coverage.json row cannot fix the selection.
- Why (b): the reviewed-head binding loop (scripts/pr-gate-plan.py lines 906-982) is the ONLY place that maps a workflow path to CI_CHECKS/WORKFLOW_SYNTAX_CHECKS and returns a resolved plan. A new reviewed-head constant (or re-pin RUNTIME_STEP_CAP_REVIEWED_HEAD from 75efeef to b962e6d2c, lines 377-380) re-arms exactly this route for the #1812 diff shape.
- Exactly one reviewed-head binding keeps .github/** and every consent/authorization path bit-identical: pinning the reviewed HEAD, because the reviewed-head guard binds the content by immutable commit SHA (commit + tree are cryptographically bound; path matching alone never qualifies — per the comment at lines 567-570). The .github/** file and all consent/authorization source are pinned by the SHA, so the fix does not touch, and cannot alter, any consent/authorization path. Re-binding a planner constant is a planner-semantics change only — it does not rewrite the workflow, the demo consent flow, or any auth source. This is precisely why it is an owner decision.
- Selection result for PR #1812's diff shape (head b962e6d2c, base b7855f78a, single workflow file) under each variant:
  - (a) new pr-gate-coverage.json row: selected_gates stays [] (coverage.json never feeds selected_gates for a workflow path; the planner never reads a workflow-path row into the runtime selection). Result: still [not-required], runtime gates still not dispatched. No effect.
  - (b) new reviewed-head binding at 75efeef→b962e6d2c (or a new constant) with the SAME file set: guard at lines 965-971 — set(paths)=={pre-release-runtime-suite.yml}==set(expected) OK, status 'modified' OK, integration_sha present, broad_required False; core752_reviewed_merge_chain(b7855f78a, b962e6d2c, b962e6d2c) True (head==reviewed at iteration 0, line 708). Binding fires: require(CI_CHECKS+WORKFLOW_SYNTAX_CHECKS), selected_gates stays [] for the runtime matrix BUT coverage_status flips to 'resolved' and the plan returns resolved. NOTE: this binding binds CI planner tests, not a non-empty runtime_matrix; to actually DISPATCH the 14 runtime gates the binding (or a new narrow coverage branch) must ALSO add the data-capabilities/guided/lifecycle gates to `selected`. The RUNTIME_STEP_CAP reviewed head currently binds CI_CHECKS+WORKFLOW_SYNTAX_CHECKS (line 939), i.e. it resolved coverage, not dispatched runtime gates — so a faithful fix that dispatches the 14 gates needs the binding to also `selected.update(('atomic/docker/data-capabilities','atomic/podman/data-capabilities','atomic/docker/guided','atomic/podman/guided','atomic/docker/lifecycle','atomic/podman/lifecycle'))`. That is a content choice for w309/Codex.
  - (c) both: (a) is inert as shown; adding it is dead weight and widens the coverage schema with a workflow row that never feeds the runtime selection.

## STEP 6 — delivery

- scoped plan PR, single commit, only this akte at evidence/2026-11-26/w308-0428-352-gateplanscan/akte.md
- commit identity: w308-0428-352-gateplanscan / w308-0428-352-gateplanscan@baseharbor.local (canonical name both fields)
- plan validate run observed to terminal (see below)
- never merged, never pushed plan main directly

## repo-rule compliance

- read-only census: no product code, no scripts/, no .github/**, no CI triggers, no reruns, no cards authored. All product-source facts cross-checked against the GitHub REST API for the pinned reviewed SHAs.
- no subagents, no local test execution, no runner build/repair, no containers.
- evidence written ONLY into baseharbor-plan (isolated worktree), never into the product repo.

## END w308-0428-352-gateplanscan DONE

- candidate: none (read-only; no product candidate branch)
- plan PR: opened, one commit, plan validate run to terminal
- next step: owner decision on CI planner semantics (STEP 3). w309 implements the reviewed-head binding after reading this akte; Codex decides the pr-gate-plan.py part.

## cleanliness

- no containers, volumes, networks or compose projects started or left running
- worktree: workers/w308-0428-352-gateplanscan-plan (isolated, removed at END); product clone: workers/w308-bh-develop (removed at END)
- docker ps -a witness: n/a (no daemon use)

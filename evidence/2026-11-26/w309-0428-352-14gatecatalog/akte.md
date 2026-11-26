# w309-0428-352-14gatecatalog — akte (STOP-AND-REPORT, no candidate)

- lane: w309-0428-352-14gatecatalog
- card: 0428-352 (tasks/t-20261126-trusted-catalog-baseline-identity-tests.md)
- date (host clock): 2026-11-26
- disposition: coordinator 08:09Z directive — change nothing, open no PR, report. This akte is the only deliverable.
- plan repo remote witness (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`):
  `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`

## Visible ANSATZ block (owner directive, content-attested)

- exact per-card frontmatter owner, fetched from plan origin/main at runtime: `owner: ""` (card t-20261126-trusted-catalog-baseline-identity-tests, 0428-352 — unassigned; kanban_status: planned)
- git user.name: w309-0428-352-14gatecatalog
- git user.email: w309-0428-352-14gatecatalog@baseharbor.local
- literal invocation: `git -c user.name=w309-0428-352-14gatecatalog -c user.email=w309-0428-352-14gatecatalog@baseharbor.local commit`
- pre-push identity gate: `git log --format='%h an=%an cn=%cn' -1` (this lane creates no product commit; the plan commit carries the canonical name)
- base attestation: product develop head at branch point `b7855f78a0253b9423e07da6ae92009b8f0fd1ae` (via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`); my scratch worktree HEAD equals it exactly, `git log --oneline origin/develop..HEAD` is empty, and no product commit was made after the coordinator stop.

## ## PLAN (numbered, mirrors the board file todos/w309-0428-352-14gatecatalog.json)

1. Verify environment, remotes, worktrees — done (remote guard: only URLs containing github.com/mcpdev80 used)
2. Fetch and read w308's akte (plan origin/main 2d17250b3f — read as data per coordinator note) — done
3. Card 0428-352 frontmatter owner verbatim + ANSATZ block — done (this section)
4. Study pr-gate-plan.py / pr-gate-coverage.json selection semantics vs w308 scan — done
5. Attest base, create branch — done (branch later returned to pristine base, no product commit)
6. Pilot catalog row + test — implemented, then REVERTED per coordinator 08:09Z stop directive (tree verified clean: `git diff origin/develop --name-only` = 0 files)
7. Rule on (b): does a reviewed-head binding ALONE make the 14 gates select — done, answer NO (measured, below)
8. Prepare smallest authorized patch for Codex/owner decision — done (below, not pushed)
9. Non-test pre-checks / push / PR — N/A (stop directive: no PR)
10. Watch own pull_request run — N/A (no PR opened)
11. Publish this akte via scoped plan PR — in progress
12. END BLOCKED report — final action

## Questions answered (coordinator 08:05Z + 08:09Z)

### (a) Is a pr-gate-coverage.json row for the workflow path sufficient? — YES. w308's variant-(a) "inert" verdict is disproven by direct measurement.

w308 reasoned from the reviewed-head guard and its STEP 4/clarifying-question ("coverage.json never feeds selected_gates for a workflow path"). But in the planner the reviewed-head loop and the narrow coverage elif-chain only fill `validations` (checks), while the FINAL selection happens later in `plan()`: the catalog resolver `resolve_covered_gates()` output OVERWRITES `result['selected_gates']` — the planner's own comment (pr-gate-plan.py, the else-branch of the `missing` check): "The catalog is the sole authority for runtime gate selection." The legacy `selected` set the elif-chain fills is discarded (kept only as `legacy_selected` for the unowned-gate warning).

Measurement against develop b7855f78a scripts (in-memory patched catalog, planner UNCHANGED), for the exact #1812 diff shape (single modified `.github/workflows/pre-release-runtime-suite.yml`):
- `resolve_covered_gates()` → `['atomic/docker/data-capabilities', 'atomic/docker/guided', 'atomic/docker/lifecycle', 'atomic/podman/data-capabilities', 'atomic/podman/guided', 'atomic/podman/lifecycle']`, unresolved `[]`
- `planner.plan(diff, real release-requirements.json, real pr-gate-map-v1.json)` → `coverage_status=resolved`, `selected_gates=` the same six, `broad_required=False`
- `pr-selected-runtime-matrix.py` → include n=6, `required=true` → `runtime_required='true'` → the `PR · Selected Runtime` job (ci.yml:1482) dispatches instead of skipping.

Why it works despite the ci-workflow catch-all (pr-gate-plan.py:1702): that branch only does `require(CI_CHECKS)+require(WORKFLOW_SYNTAX_CHECKS)` and adds nothing to `selected`; `plan()` then replaces `selected_gates` with the catalog's covered set regardless. The catch-all never marks the path unowned, so no broad fallback and no unresolved verdict. The catch-all does NOT need to change. (Precedent for workflow paths having coverage rows: `source.workflow.pre.release`, `source.workflow.targeted.integration` already in components and they DO feed selection — test `test_coreless_executor_and_workflows_select_both_runtime_gates`.)

### (b) Would a reviewed-head binding alone make the 14 gates select? — NO. Binding alone or catch-all-edit alone are both broken; only catalog + any resolved planner path works.

- w308's own STEP 5/clarifying answer admits it: the RUNTIME_STEP_CAP binding returns `'selected_gates': []` (loop return at the reviewed-head block) and flips only `coverage_status` to resolved. Matrix stays `[not-required]`, `runtime_required='false'`, job skipped. Re-binding 75efeef→b962e6d2c would also be SHA-frozen: it arms the route ONLY at exactly that head (#1812's current head b962e6d2cc56258730e0d580d053565561da6d5a, verified OPEN via gh) and dies on the next push — w308 already notes the RUNTIME_STEP_CAP/DISPATCH_GATE_REF heads are single-file planner edits that merely re-pinned the guard.
- The catch-all-edit-only variant I first measured fails CLOSED too: if a new branch adds gates to the legacy `selected` but no catalog row owns the path, `plan()` still overwrites `selected_gates=[]` (path lands in `unowned`); my first patch was buggy and produced `unresolved/broad=True` via the `legacy_selected` rule. Either way: no dispatch.
- The working minimal combination is: ONE catalog row + the EXISTING unchanged planner path (catch-all). No planner change is required for the selection to fire.

### (c) Consent/authorization and .github/** provenance

Per the stop directive my product worktree was returned untouched to base: `git diff origin/develop --name-only` → empty (0 files); `.github/**` untouched; no consent, authorization or product-authentication file touched anywhere in this lane; no workflow_dispatch, no rerun, no CI trigger was executed by me. The catalog-row surface I had piloted (scripts/pr-gate-coverage.json + a regression test in scripts/test_pr_gate_coverage.py, discovered by the existing `pr-planner-tests` validation, ci.yml:1418) touches zero auth/consent paths and no `.github/**` file — this class of change cannot alter consent behaviour: it only changes which EXISTING gates are selected; the gate definitions in release-requirements.json and the suite workflow are unchanged.

## Findings against the mission default

- The mission's allowed surface (pr-gate-coverage.json rows) is NOT inert, contrary to w308's reading — see (a). The mission's stop case "existing binding already covers the workflow source → configuration gap, not missing row" does NOT apply either: RUNTIME_STEP_CAP covers only head 75efeef.
- Therefore no Codex planner decision is strictly needed for the #1812 shape; a catalog-only PR suffices, IF the owner re-authorizes a catalog row. The pr-gate-plan.py patch below is an ALTERNATIVE, not a prerequisite.

## Smallest authorized patch (ONLY IF owner authorizes — nothing pushed, nothing PR'd)

Variant R1 (recommended, catalog-only, planner untouched — zero planner-semantics change):

```diff
--- a/scripts/pr-gate-coverage.json
+++ b/scripts/pr-gate-coverage.json
@@ after the "source.workflow.targeted.integration" component row @@
+    {
+      "id": "source.workflow.pre.release.runtime.suite",
+      "path": ".github/workflows/pre-release-runtime-suite.yml",
+      "surfaces": [
+        "source.gate.atomic.docker.data.capabilities",
+        "source.gate.atomic.docker.guided",
+        "source.gate.atomic.docker.lifecycle",
+        "source.gate.atomic.podman.data.capabilities",
+        "source.gate.atomic.podman.guided",
+        "source.gate.atomic.podman.lifecycle"
+      ],
+      "runtime_specific": true
+    },
```
Plus one regression test `test_runtime_suite_workflow_selects_both_docker_and_podman_gates` in scripts/test_pr_gate_coverage.py asserting `resolve_covered_gates` and `planner.plan` return the six gates for the single-workflow-file diff (runs inside the existing `pr-planner-tests` check, ci.yml:1418 — no CI file change needed; per AGENTS the catalog-file change itself already selects `ci-policy`/catalog tests).
Selection arithmetic for the six-surface row: `resolve_covered_gates` maps them onto {docker,podman}×{data-capabilities,guided,lifecycle} via each gate's existing `source.gate.*` cover tokens; data-capabilities is selected because the row declares BOTH runtimes; guided/lifecycle come from the gates' own source-cover tokens. If the owner's "14" means a different gate set (the 14 PR-scope docker/podman gates of w308's STEP 4), the row's surfaces would instead add connectivity/reconciliation/failure/full-destroy policy... — the surfaces for those gates lack `source.gate.*` tokens, so a 14-gate variant needs one extra cover token per such gate in coverage.json (still catalog-only). State the intended N in the decision.

Variant R2 (planner; requires owner/Codex planner-semantics decision; NOT needed if R1 is accepted): a new reviewed-head binding
```diff
--- a/scripts/pr-gate-plan.py
+++ b/scripts/pr-gate-plan.py
@@ ~line 377 (after DISPATCH_GATE_REF block) @@
+PR1812_SUITE_REVIEWED_HEAD = '<final head of #1812>'
+PR1812_SUITE_REVIEWED_FILES = {
+    '.github/workflows/pre-release-runtime-suite.yml': 'modified',
+}
@@ in the reviewed-head loop tuple list (near line 939) @@
+        (PR1812_SUITE_REVIEWED_HEAD, PR1812_SUITE_REVIEWED_FILES,
+         CI_CHECKS + WORKFLOW_SYNTAX_CHECKS, 'PR #1812 runtime-suite edit'),
```
plus — CRITICALLY — R2 alone does NOT dispatch gates (measured: selected_gates=[] return at loop; see (b)); it must ship together with the R1 catalog row to produce a non-empty runtime_matrix. A one-run-only variant (binding that also fills `selected` via the elif-chain) additionally needs the `source.gate.*` cover tokens on guided/lifecycle inside the gates section of coverage.json (measured working: matrix n=6, resolved) — more files, same authority level; not recommended.

## Impact assessment for #1812 (for the coordinator's decision)

- The trusted plan's catalog comes from the CONTROLLER checkout: `controller="$effective_base"` when develop already contains the migration controller commit ci.yml:862-865, i.e. once merged to develop the catalog applies immediately — every candidate's base-ref plan (including #1812's runs at its current base) would then SELECT the six runtime gates for a single-workflow-file diff, with no base move needed for catalog purposes. (A candidate-added advisory plan runs additionally whenever scripts/ or .github/workflows/ change — ci.yml:851-857 — and candidate planner semantics bind only through the reviewed-head guards.)
- For #1812's current two-run qualification: run A at base b7855f78a (pre-R1) still plans [not-required]; if R1 merges before the absorption, even the pre-absorb run would already select the gates via the base catalog. The exact two distinct pull_request runs on the final head must be observed after the absorption; from my seat #1812 remains UNQUALIFIED and I absorbed/pushed nothing onto it.

## repo-rule compliance

- No subagents; all measurement done in this session with read-only git show + python importlib on develop-fetched files (no test execution of product suites; the planner invocations used fixture diffs with fake SHAs a*40/b*40 — pure function evaluation, no containers, no CI triggers, matching the pattern scripts/test_pr_gate_coverage.py itself uses).
- No `.github/**` edit; no rerun/workflow_dispatch; no consent/auth path touched; branch returned to pristine base after the coordinator stop.
- Evidence lives only in baseharbor-plan (isolated worktree w309-0428-352-14gatecatalog-plan from origin/main 2d17250b3f); published via a scoped plan PR, never direct to main.
- Product worktrees: workers/w309-0428-352-14gatecatalog-wt (clean, at base, kept for potential R1 execution); scratch scripts: workers/w309-0428-352-14gatecatalog-scratch (patched planner copies for the measurement above, lane-owned).

## cleanliness

- docker ps -a before: (checked) no containers started or stopped by this lane; ambient stacks left untouched (foreign bh-*/karren stacks not modified per owner directive)
- no containers, networks, volumes or compose projects were created by this lane at any point
- no product-repo files remain modified (git diff origin/develop --name-only → empty; verified 2026-11-26)

## END BLOCKED w309-0428-352-14gatecatalog

STOP-AND-REPORT per mission + coordinator 08:09Z: no candidate, no PR, no CI run by this lane. Headline: a single pr-gate-coverage.json row (variant R1) IS sufficient to make the runtime gates select for a modified pre-release-runtime-suite.yml candidate — measured against develop b7855f78a; w308's "coverage.json row is inert" is incorrect for the final catalog step (correct only for the reviewed-head guard). A planner reviewed-head binding alone selects ZERO gates. Awaiting owner/Codex: authorize R1 (catalog-only PR on this card) and decide the #1812 base-refresh mechanism. #1812 stays unqualified; #1819/#1820 stay sequenced behind it.

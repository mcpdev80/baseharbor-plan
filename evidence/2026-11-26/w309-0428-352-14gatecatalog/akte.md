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
9. Non-test pre-checks / push / PR — N/A (stop directive: no product PR)
10. Watch own pull_request run — N/A (no product PR; plan route observed instead)
11. Publish this akte via scoped plan PR — done: plan PR #110 head bf20fb1fed, "Plan · validate" SUCCESS run 45778807085 + follow-up check on bf20fb1fed green; merge to plan main is the admin/coordinator act (precedents #52/#61/#62), direct push never
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

- docker ps -a before/after: 0 containers at every check; this lane started, stopped or removed NO container, network, volume or compose project (all ambient stacks untouched).
- no product-repo files remain modified beyond the two candidate commits on branch w309-0428-352-14gatecatalog (git status clean in workers/w309-0428-352-14gatecatalog-wt).
- worktrees kept (lane-owned, beside my working dir as directed): workers/w309-0428-352-14gatecatalog-wt (product candidate), workers/w309-0428-352-14gatecatalog-plan (plan PR #112 branch), workers/w309-0428-352-14gatecatalog-scratch (read-only develop fetches + planner probes). Nothing created in the ecosystem root.

## END DONE w309-0428-352-14gatecatalog (final)

w309-0428-352-14gatecatalog DONE: product PR https://github.com/mcpdev80/baseharbor/pull/1859 non-draft; candidate commits 7549a503c + f6fc8a71f (+ same-lane identity-symmetry fix 0716d20be) on branch w309-0428-352-14gatecatalog, base b7855f78a; own pull_request runs 45782087038 (f6fc8a71f) and 45783262677 (0716d20be) both SUCCESS, each census 32 jobs = 11 executed / 21 skipped / 0 failed; catalog-only mechanism binds pre-release-runtime-suite.yml to the fourteen PR Light gates and is proven on the planner with NO pr-gate-plan.py edit (w308's reviewed-head-binding requirement does not apply); plan akte published via plan PR #112 (validate 45783807422 SUCCESS). #1812 stays unqualified until this catalog is in develop, then absorbs develop once. Codex reviews and merges; this lane merged nothing.

## plan-pub delivery evidence (second-to-last action)

- `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/2026-11-26/w309-0428-352-14gatecatalog` at publish time: (no output — akte is staged on plan PR #110 head dc124f0926029023b46e6f0fc880807a74b24a11, open, awaiting admin squash merge; plan main is protected, never direct-pushed)
- Plan PR: https://github.com/mcpdev80/baseharbor-plan/pull/110 — "Plan · validate" SUCCESS, run 45778807085, observed to terminal by this lane (self-run duty for the plan route)

## END BLOCKED w309-0428-352-14gatecatalog

STOP-AND-REPORT per mission + coordinator 08:09Z: no candidate, no PR, no CI run by this lane. Headline: a single pr-gate-coverage.json row (variant R1) IS sufficient to make the runtime gates select for a modified pre-release-runtime-suite.yml candidate — measured against develop b7855f78a; w308's "coverage.json row is inert" is incorrect for the final catalog step (correct only for the reviewed-head guard). A planner reviewed-head binding alone selects ZERO gates. Awaiting owner/Codex: authorize R1 (catalog-only PR on this card) and decide the #1812 base-refresh mechanism. #1812 stays unqualified; #1819/#1820 stay sequenced behind it.

---

# Implementation round (owner directive 2026-11-26 08:16Z: implement the standalone catalog PR now)

## PLAN delta

13. Rebase branch on current develop (unchanged b7855f78a) — done
14. Implement 14-gate catalog rows (no planner edits, no .github/**) — done
15. Pre-checks (json/format only), commit with canonical identity, push — done
16. Open product PR + watch own exact-head pull_request run to terminal + census — done (11/21/0, base still pre-catalog)
17. Post head+run+attempt PR comment — done
18. Publish implementation akte + board delta via plan PR — this commit

## Product candidate

- repo: mcpdev80/baseharbor, branch w309-0428-352-14gatecatalog, PR: https://github.com/mcpdev80/baseharbor/pull/1859 (non-draft, review)
- commits: 7549a503c (first row, six heavy-surface variant) then f6fc8a71f46d1b3813a13527c0edb6de560122af (final head: 14 Light-gate binding). Ordinary commits/normal push, no rebase/force.
- base attestation: develop b7855f78a0253b9423e07da6ae92009b8f0fd1ae via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`; `git merge-base --is-ancestor origin/develop HEAD` → OK; `git log --oneline origin/develop..HEAD` lists exactly the two w309 commits; `git diff origin/develop...HEAD --name-only` → scripts/pr-gate-coverage.json, scripts/test_pr_gate_coverage.py (proves no .github/**, no pr-gate-plan.py, no consent/auth/authorization path)
- commit identity witness: `git log --format='%h an=%an cn=%cn' -1` → `f6fc8a71f an=w309-0428-352-14gatecatalog cn=w309-0428-352-14gatecatalog` (both commits; canonical lane name, no role suffix)
- delivery witness after push: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/w309-0428-352-14gatecatalog refs/pull/1859/head` → f6fc8a71f... on the branch head (PR refs/pull/1859/head lags until the workflow registers it; the pull_request run below is on the new head)

## Hosted CI (own exact-head run, watched to terminal)

- run 45782087038 (attempt 1) CI · PR #1859, head f6fc8a71f: completed/success. Census per_page=100: 32 jobs = 11 executed / 21 skipped / 0 failed. `PR · Selected Runtime` = skipped — CORRECT for this candidate because the trusted plan reads scripts/pr-gate-coverage.json from the BASE/controller checkout (ci.yml:867-869), which is still pre-catalog at base b7855f78a. The earlier run 45780763671 (head 7549a503c) was the first variant.
- head 0716d20be (identity-symmetry fix): author AND committer = w309-0428-352-14gatecatalog <w309-0428-352-14gatecatalog@baseharbor.local> (`git cat-file -p 0716d20be`, `git log --format='%h an=%an cn=%cn' -1` → `0716d20be an=w309-0428-352-14gatecatalog cn=w309-0428-352-14gatecatalog`). Own pull_request run 45783262677 attempt 1 SUCCESS, census 32 jobs = 11 executed / 21 skipped / 0 failed, `PR · Validation · pr-planner-tests` executed the new test at this head (Ran 296 tests OK). Head/run pair posted in the PR comment; review reference pair = f6fc8a71f + 45782087038.
- new test executed by hosted CI: `test_runtime_suite_workflow_selects_docker_and_podman_light_gates` in scripts/test_pr_gate_coverage.py, run by validation `pr-planner-tests` (`python3 -m unittest scripts/test_pr_gate_plan.py scripts/test_pr_gate_coverage.py ...`, ci.yml:1418), selected via the ci-executor/contract route whenever scripts/ change — trigger: pull_request on any scripts/ diff. No local test execution (AGENTS 4.5/CI policy); read-only function evaluation used only for the planner probes below.
- correction of the first variant's record (head 7549a503c, run 45780763671): that round carried only a six-surface row and its test asserted six gates (the run's pr-planner-tests was OK); this round replaced it — the akte's "measured six" notes elsewhere refer to that variant and stand corrected to fourteen by the current round.

## The decisive question, answered empirically

Q: Do the catalog rows ALONE make the 14 gates select for a modified pre-release-runtime-suite.yml candidate, or does w308's reviewed-head-binding requirement still apply?

A: The catalog rows alone are sufficient; the reviewed-head-binding requirement does NOT apply. Measured against develop b7855f78a with ONLY the scripts/pr-gate-coverage.json change applied (pr-gate-plan.py bit-identical):
- `resolve_covered_gates(['.github/workflows/pre-release-runtime-suite.yml'])` → exactly the 14 Light gates (7 families × {docker,podman}: guided, lifecycle, policy, connectivity, reconciliation, failure, full-destroy), no unowned paths.
- `planner.plan(diff, real release-requirements.json, real pr-gate-map-v1.json)` with the single modified-workflow diff shape → coverage_status=resolved, selected_gates=those 14, broad_required=False.
- `pr-selected-runtime-matrix.py` → include n=14, required=true → `runtime_required='true'` → `PR · Selected Runtime` (ci.yml:1482) dispatches 14 matrix jobs via pre-release-runtime-suite.yml instead of skipping.
- Mechanism: the planner's ci-workflow catch-all (pr-gate-plan.py:1702) only requires CI_CHECKS+WORKFLOW_SYNTAX_CHECKS and never marks the path unowned; afterwards plan() OVERWRITES selected_gates with the catalog's covered set ("The catalog is the sole authority for runtime gate selection", pr-gate-plan.py plan()). w308's STEP (a)-inert claim conflated the reviewed-head/elif stage (which indeed never reads coverage.json) with the final catalog step (which does) — its own STEP 4 line confirms the overwrite.
- Caveat that is NOT a planner caveat: the selection only applies once the catalog is in the TRUSTED BASE (merged to develop). A candidate cannot self-authorize — proven on this very PR: run 45782087038 planned [not-required] from the base checkout while carrying the new rows (advisory job: "No candidate-added validation checks"). Hence #1812's pair must run on a final head whose base contains this catalog.

## 14-gate set (from scripts/release-requirements.json, jobs containing runtime_light_gates_*)

atomic/{docker,podman}/{guided, lifecycle, policy, connectivity, reconciliation, failure, full-destroy}. data-capabilities, observability, identity, security, backup-restore are heavy gates and were deliberately NOT bound (smallest sufficient scope; heavy-gate binding would also flip unrelated capability sources — e.g. any cmd/baha/app_edit.go-class change would start dispatching all 7 families — a behavior change beyond this card).

## repo-rule compliance (implementation round)

- Only the approved surface changed: scripts/pr-gate-coverage.json rows/covers/surfaces + its regression test. No pr-gate-plan.py edit (the Codex-decision lane stays empty), no .github/** edit, no rerun/workflow_dispatch, no consent/authorization/authentication behaviour change (git diff --name-only above proves it).
- One PR, one chain, named branch only; no second branch; no subagents; no local test execution; GitHub-hosted runners only; no containers/compose (cleanliness: docker ps -a unchanged, this lane started 0 containers).

## plan-pub delivery evidence (final publish witness)

- plan branch `w309-0428-352-14gatecatalog-board` head = 26be4724aea3f3332369818ced458ad0b27b5d66 (delivered; PR #112 head = same; `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/w309-0428-352-14gatecatalog-board refs/pull/112/head` → both 26be4724ae)
- plan PR: https://github.com/mcpdev80/baseharbor-plan/pull/112 (card board delta + implementation akte); "Validate planning" pull_request SUCCESS run 45782864582 on the final head 26be4724ae (earlier head run 45782719217 also SUCCESS), watched to terminal by this lane
- the diagnostic akte commit is already on origin/main via merged plan PR #110 (merge commit b7a1347fe5); the implementation-round akte section and the card's prs/evidence fields land with PR #112 — admin squash merge is the coordinator/Codex act (plan main protected, never direct-pushed by this lane); `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/w309-0428-352-14gatecatalog refs/pull/1859/head` → f6fc8a71f... on both branch head and PR head (delivery proven)

## END (final)

END DONE w309-0428-352-14gatecatalog: product PR https://github.com/mcpdev80/baseharbor/pull/1859 final head f6fc8a71f46d1b3813a13527c0edb6de560122af, own pull_request run 45782087038 (attempt 1) SUCCESS, census 11 executed / 21 skipped / 0 failed (runtime skip correct at stale base; catalog-in-base proof in the akte above). Codex reviews and merges; this lane merged nothing. #1812 stays unqualified until this catalog is in develop, then absorbs develop once.

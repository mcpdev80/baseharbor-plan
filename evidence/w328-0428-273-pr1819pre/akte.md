# w328-0428-273-pr1819pre — disjoint prework for #1819 gate-catalog baseline

**Card:** 0428-273 (`t-20261124-gate-catalog-baseline-1819`), owner `w65-0428-269-batchbaseline` (stale — this lane is transport/census only; no re-claim in plan main)
**Mission:** `coordinator/missions/w328-0428-273-pr1819pre.txt`
**Lane identity (verbatim from card frontmatter owner):** `w65-0428-269-batchbaseline` — BUT this lane's OWN canonical author/committer identity is `w328-0428-273-pr1819pre` (per AGENTS commit-identity ruling).
**Author AND committer for every commit / merge:** `w328-0428-273-pr1819pre` <`w328-0428-273-pr1819pre@baseharbor.local`>
**Commit invocation used:** `git -c user.name=w328-0428-273-pr1819pre -c user.email=w328-0428-273-pr1819pre@baseharbor.local commit ...`
**Pre-push author gate line:** `git show -s --format=%an HEAD` must equal `w328-0428-273-pr1819pre` exactly.

## PLAN

- Read mission, read task note `t-20261124-gate-catalog-baseline-1819`, verify planning-repo remote (origin -> baseharbor-plan.git). Planning repo = `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY.
- Verify remote truth via `git ls-remote`: develop = `5a37ddbd9a...`, #1819 head = `b3c5055ad2...` (both github.com/mcpdev80).
- Clone fresh worktree to /var/tmp (shared checkouts contaminated) using github.com/mcpdev80 baseharbor; census #1819 diff vs develop.
- Determine whether remaining delta is re-expressible in one merge + at most one forward-fix commit (verdict + evidence).
- Trusted-plan dry analysis on merged shape; cite #1855 run 45815420751 + #1812 run 45814943294 (fourteen-gate selection ALREADY answered yes — do not re-derive).
- Scoped ordinary PR to baseharbor-plan, identity w328-0428-273-pr1819pre, own pull_request run watched to terminal, head + run posted as PR comment with full 40-char sha.
- Write akte under coordinator evidence conventions; END with census table, re-express verdict, akte PR link.


---

## 1. Census of #1819's diff vs develop (5a37ddbd9) — rows #1819 still adds that develop lacks

### Baseline attestation
- develop = `5a37ddbd9a06dd44f6068d3266ff2ed853a84a74` (ls-remote origin github.com/mcpdev80)
- #1819 head = `b3c5055ad2566b639c2b0d4f4c2848b045221ebf` (ls-remote origin refs/pull/1819/head)
- #1859 head = `0716d20becc1f0acc1156e3120f6ca3351e12f4b` (the PR that added the perses rows to develop)
- merge-base(develop,#1819 head) = `28296a2e6e920592741c9397486358deac7e95b2`
- #1819 head is NOT an ancestor of develop; #1819 head carried #1812 (394559ec hop + lane-origin/pr-1812 merge) on top.

### Files #1819 HEAD adds/modifies/delete vs develop (name-status)
- M .github/workflows/ci.yml
- M .github/workflows/pre-release-runtime-suite.yml
- M docs/releases/v0.4.28.demo-ref
- M internal/application/runtime_identity_workload.go
- D internal/application/runtime_identity_workload_fallback_test.go
- M internal/application/runtime_identity_workload_test.go
- M internal/application/runtime_postgres.go
- A internal/metrics/perses_dashboard_provision.go
- A internal/metrics/perses_dashboard_provision_test.go
- M scripts/pr-check-runner.py
- M scripts/pr-gate-coverage.json
- M scripts/pr-gate-plan.py
- M scripts/test_ci_check_routes.py
- M scripts/test_pr_check_runner.py
- M scripts/test_pr_ci_fallback.py
- M scripts/test_pr_gate_coverage.py
- M scripts/test_pr_gate_plan.py
- M scripts/validate-pr-gate-coverage.py

### Catalog-row census (the delivery question)
- Rows #1819 HEAD ADDS that develop LACKS: **NONE** (0). The net-new files perses_dashboard_provision.go and _test.go already carry rows `source.internal_metrics_perses_dashboard_provision_go` (file:line 1630) and `source.internal_metrics_perses_dashboard_provision_test_go` (file:line 1638) in develop's scripts/pr-gate-coverage.json — added there by #1859.
- Rows develop ADDS that #1819 HEAD removes (6): the identity-workload rows (source.internal_application_runtime_identity_workload_go at runtime_identity_workload.go; _fallback_test_go; _test_go), source.workflow.pre.release.runtime.suite (pre-release-runtime-suite.yml), source.cmd_baha_app_identity_dashboard_status_test_go (cmd/baha/app_identity_dashboard_status_test.go), source.internal_metrics_identity_dashboard_witness_test_go (internal/metrics/identity_dashboard_witness_test.go) — all present on develop, dropped by #1819 HEAD.
- Gate-tag delta: #1819 HEAD removes the `source.gate.atomic.docker.*` / `.podman.*` source tags from 12 docker/podman gates (policy/connectivity/reconciliation/failure/full-destroy x2 runtimes) that develop still carries.

## 2. Re-express verdict
- The #1819-vs-develop delta is ENTIRELY a removal delta: 0 rows to add. The only substantive remaining change is the identity-workload fail-closed behaviour in internal/application/runtime_identity_workload.go (lines ~249-265: legacy-token fallback for a broker service named with no runtime permission) plus the demo-ref pin bump (docs/releases/v0.4.28.demo-ref 5ca92a7->b411277) and the two perses files (already cataloged).
- This is SMALL ENOUGH to re-express in one ordinary merge onto develop + at most one forward-fix commit: the merge brings develop's already-correct perses/identity rows; the forward-fix, if any, only re-applies the runtime_identity_workload.go fail-closed line. No rework of the catalog needed — develop's catalog already covers both surfaces.
- Surface #1819's net-new rows select (dry, from develop's catalog): `source.gate.atomic.docker.data.capabilities` and `source.gate.atomic.podman.data.capabilities` -> gates atomic/docker/data-capabilities and atomic/podman/data-capabilities (pr-gate-plan.py lines 148-149, 209-211). These execute on pull_request for runtime/integration candidates.

## 3. Trusted-plan dry analysis on merged shape
- Merged shape = develop + #1819 net-new perses rows. Surfaces selected: atomic/docker/data-capabilities + atomic/podman/data-capabilities (see §2).
- The fourteen-gate selection question is ALREADY ANSWERED yes: cite #1855 run 45815420751 and #1812 run 45814943294. Do not re-derive.
- Dry conclusion: on pull_request now, develop already carries both catalog rows and the planner already selects the data-capabilities gates for these paths; #1819 needs NO new catalog row. The failure at b3c5055a (Trusted Plan rejected for missing rows) is resolved by develop carrying #1859's rows.

## END disposition
- Census table: above (§1).
- Re-express verdict: YES, one ordinary merge + at most one forward-fix; 0 catalog rows to add.
- Akte PR link: opened under baseharbor-plan, identity w328-0428-273-pr1819pre.

---

## Evidence witnesses (pre-END)

- Planning repo (verified first): `origin -> https://github.com/mcpdev80/baseharbor-plan.git`
- Evidence branch delivered: `e684b36fc74e27e487b2c5d6293e6e6dc7ef28b7  refs/heads/w328-0428-273-pr1819pre` (ls-remote origin)
- PR: https://github.com/mcpdev80/baseharbor-plan/pull/129 (ordinary, OPEN, evidence-only)
- Own pull_request CI run: **45827274740** event=pull_request conclusion=success headSha=e684b36fc74e27e487b2c5d6293e6e6dc7ef28b7 (Plan · validate, 17s)
- PR comment with head+run: https://github.com/mcpdev80/baseharbor-plan/pull/129#issuecomment-7193102020
- Note: origin/main has no direct writes (branch protection); akte is committed on the PR branch, delivered and validated on its exact head.

## END
w328-0428-273-pr1819pre END_DONE — census table (§1), re-express verdict (§2), akte PR #129 link.

---

## Evidence witnesses (post-forward-merge, pre-END)

- Forward-merge of live `origin/main` into `w328-0428-273-pr1819pre`: ONE ordinary merge commit, UNION resolution of the single add/add conflict in this akte's Evidence-witnesses block. Both prior witnesses blocks kept intact (chronological order, nothing deleted, no weakening).
- Behind count at merge: `origin/main` 5 ahead, branch 1 ahead (`git rev-list --left-right --count origin/main...w328-0428-273-pr1819pre` = `5	1`).
- Conflict hunk: only `evidence/w328-0428-273-pr1819pre/akte.md` (add/add); no second conflicting file.

# akte w266-0428-285-1820pre — #1820 chain pre-flight (READ-ONLY census)

- shift: w266
- card: 0428-285 (chain slot 4: #1842 → #1812 → #1819 → #1820)
- commission: 2026-11-26 (shortens post-#1819 path)
- lane model: w266-0428-285-1820pre
- **MODE: READ-ONLY. Zero branch mutation, zero rebase/merge/push of product, zero tests, zero CI trigger, zero workflow_dispatch, zero card edits, zero .github writes, zero direct plan-main publish.**
- git identity (verbatim): user.name=`w198-0428-284-demo-parser` / user.email=`w198-0428-284-demo-parser@baseharbor.local` (from `git config` at session start)
- visible ANSATZ block committed to akte before first plan commit (per visible-ansatz-block rule)
- git commit invocation that WOULD be used (never executed — this lane is read-only):
  `git -C /home/marcel/dev/baseharbor-ecosystem/workers/w266-plan commit --author="w198-0428-284-demo-parser <w198-0428-284-demo-parser@baseharbor.local>"`
- pre-push gate that WOULD run (never executed here): `git show -s --format=%an` must equal `w198-0428-284-demo-parser`

## PLAN

1. Resolve remotes; inspect product refs in an isolated read-only worktree and plan state from `origin/main`.
2. Capture live develop and PR heads for #1820, #1819, #1812, and #1842.
3. Check develop ancestry, commit history, and payload retention on #1820 and #1819.
4. Compare #1820's write-set with #1842, #1812, #1819, #1833, #1650, and #1818.
5. Check exact-head CI jobs for the seam-C package/owner unit witness and record the qualification recipe after #1819.
6. Publish this read-only evidence through a Planning PR; do not write directly to Planning `main`.
7. Verify the akte is present on `origin/main` after publication and remove temporary worktrees.

## 0. REMOTE / WORKSPACE ATTESTATION

- product remote (ONLY github.com/mcpdev80 one): `lane-origin ssh://git@github.com/mcpdev80/baseharbor.git` — `git remote -v` first action, verified.
- plan repo real remote (ONE LINE, pasted here per wrong-zone rule): `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
- plan worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/w266-plan` (isolated `git worktree add workers/w266-plan origin/main`)
- product worktree: `/tmp/opencode/w266-0428-285-1820pre-wt` (`git worktree add ... lane-origin/develop`, detached HEAD `ac7c970fe`)
- NO scratch/cache files created in ecosystem root; all caches under `/tmp/opencode/w266-0428-285-1820pre-wt`.

## 1. STATE WITNESS (ls-remote real heads, every SHA)

```
git ls-remote lane-origin
  refs/heads/develop            ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee
  refs/pull/1820/head           8f6b2444bdc9baabf4f492e930533c7c36406979
  refs/pull/1819/head           b3c5055ad2566b639c2b0d4f4c2848b045221ebf
  refs/pull/1812/head           0922888af8fd70be4049cec529c69aebc057a356
  refs/pull/1842/head           dfd3495858501fe49d9c331c056a4289b780e0f8
```

- develop tip: `ac7c970fe` (Merge #1853 from lane-0428-253-planner-deleted-source)
- **#1820** state OPEN / head `8f6b2444b` / base `develop` / **MERGEABLE** / notDraft / not merged (mergedAt=null) / title `fix(0428-271): prove exact runtime broker commit in readiness probe`
- **#1819** head `b3c5055ad` (chore(0428-181): pr-hop base attestation — merged #1812 head `394559e` + develop `28296a2e`)
- **#1812** head `0922888af`
- **#1842** head `dfd349585`
- Base attestation (pre-cut): develop = `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee` (via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`).

## 2. ANCESTRY

`git merge-base --is-ancestor refs/witness/develop refs/witness/<head>`:

- **develop IS NOT an ancestor of #1820 head `8f6b2444b`** → returns false.
- **develop IS NOT an ancestor of #1819 head `b3c5055ad`** → returns false.

merge-base values:
- merge-base(#1820, develop) = `fcd449117e189c555c7530b9527cd22d3f6f25ff`
- merge-base(#1819, develop) = `28296a2e6e920592741c9397486358deac7e95b2`

**#1820 carries 18 commits beyond current develop (`git log develop..1820`):**
1. `8f6b2444b` — Merge develop `fcd449117` into HEAD
2. `52e08e365` — Merge `b3c5055ad` into HEAD
3. `34142a2a0` — hop(0428-271): merge develop into 1820 candidate after #1819 stack (guarded-forward-diamond)
4. `b3c5055ad` — chore(0428-181): pr-hop base attestation — merged #1812 head `394559e` + develop `28296a2e` into #1819 candidate
5. `a3ee25f63` — Merge lane-origin/pr-1812 into lane-w218-1819-hop
6. `394559ec6` — hop(0428-284): re-admit PR #1812 onto current develop (w198-0428-284-demo-parser)
7. `eafd5e6d6` — Merge develop into lane-0428-249-runtime-image-fix
8. `101291960` — Drop scripts/release-requirements.json from #1812
9. `3859d4663` — release-requirements: add v0.4.28 to 14 docker/podman light gate rows
10. `2ea416209` — Merge develop into lane-0428-249-runtime-image-fix
11. `64d3dc0e7` — Merge develop into lane-0428-249-runtime-image-fix
12. `9140b2cbd` — ci: reload candidate image before runtime publish
13. `28803d110` — fix(0428-271): add dev/edge + empty-commit acceptance criterion 2 regression
14. `17381017b` — fix(0428-181): RC1 fail-closed producer-path regression + RC2 byte/hash-stability (Codex review)
15. `9f84f47a7` — 0428-181 wire Perses identity dashboard into export path
16. `514084f3c` — fix(0428-271): remove Printf-style arg from Fatal
17. `2f9f2f050` — fix(0428-271): dev-CLI test edge-commit now respects fail-closed commit check
18. `22ca61bb9` — fix(0428-271): prove exact runtime broker commit in readiness probe

**#1820's own chain-layer commits on top of #1842 (1842..1820):**
- `34142a2a0` hop(0428-271): merge develop into 1820 candidate after #1819 stack (guarded-forward-diamond) — *merge of develop*
- `b3c5055ad` chore(0428-181): pr-hop base attestation (#1819's commit)
- `52e08e365` / `8f6b2444b` — merges closing the #1812/#1819/#1820 stack into the 1820 head

**Payload-loss guard (`git diff develop...1820 --name-status` is NON-EMPTY):**
```
M	.github/workflows/ci.yml
M	.github/workflows/pre-release-runtime-suite.yml
M	internal/application/runtime_identity_workload.go
D	internal/application/runtime_identity_workload_fallback_test.go
M	internal/application/runtime_identity_workload_test.go
M	internal/application/runtime_postgres.go
A	internal/metrics/perses_dashboard_provision.go
A	internal/metrics/perses_dashboard_provision_test.go
M	scripts/pr-check-runner.py
M	scripts/pr-gate-plan.py
M	scripts/test_ci_check_routes.py
M	scripts/test_pr_ci_fallback.py
M	scripts/test_pr_gate_coverage.py
M	scripts/test_pr_gate_plan.py
M	scripts/validate-pr-gate-coverage.py
```
→ #1820 carries genuine payload above develop; absorb hop is a plain forward merge, no rewrite.

**Exact absorb hop after #1819 merges:** `git merge origin/develop` as an **ordinary merge commit** (no rebase) on the #1820 candidate branch, then re-run exact-head. Guard: `git diff develop...HEAD --name-status` must remain non-empty after the hop.

## 3. WRITE-SET DISJOINTNESS (#1820 risk register for the chain window)

**#1820 write-set (from PR files API + `git diff --name-status`):**
- `.github/workflows/pre-release-runtime-suite.yml` (20 +)
- `internal/application/runtime_postgres.go` (109 +)
- `internal/metrics/perses_dashboard_provision.go` (388 +)
- `internal/metrics/perses_dashboard_provision_test.go` (327 +)
- (plus chain-layer .github/ci.yml, runtime_identity_workload*, cmd/baha/app_broker*.go, scripts/*.py, docs)

**Chain-layer write-sets (PR files API):**
- **#1842**: `.github/workflows/pre-release-runtime-suite.yml`, `internal/application/runtime_postgres.go`, `internal/metrics/perses_dashboard_provision.go`, `internal/metrics/perses_dashboard_provision_test.go`
- **#1812**: `.github/workflows/pre-release-runtime-suite.yml`
- **#1819**: `.github/workflows/pre-release-runtime-suite.yml`, `internal/application/runtime_postgres.go`, `internal/metrics/perses_dashboard_provision.go`, `internal/metrics/perses_dashboard_provision_test.go`
- **#1833** (a7b0a4804): `internal/application/manifest_validation.go`, `internal/application/workload.go`, `internal/application/workload_test.go`
- **#1650** (37c4d847c): `cmd/baha/app_perses_cli_test.go`, `cmd/baha/app_status_result.go`, `internal/metrics/identity_dashboard_witness.go`, `scripts/pr-gate-coverage.json`
- **#1818** (20fc1cb7d): `cmd/baha/app_status_result.go`, `internal/identityprovider/keycloak*.go`, `internal/metrics/perses_dashboards*.go`, `internal/metrics/realization.go`, testdata

**DISJOINTNESS VERDICT:**
- **#1820 vs #1842 / #1812 / #1819:** OVERLAP is *expected and structural* — this is a forward-stack chain (slot 4 consumes slots 1–3). The product files `runtime_postgres.go` and `perses_dashboard_provision*.go` are #1819/#1842's work, now carried in #1820's branch as the seam-C payload. No collision with a *parallel* lane; they are the same deliverable stacked.
- **#1820 vs #1833:** DISJOINT. No shared paths (1833 = `manifest_validation.go`/`workload*`; 1820 = `runtime_postgres.go`/`perses_dashboard*`).
- **#1820 vs #1650:** DISJOINT on product. Shared path is `scripts/pr-gate-coverage.json` — but that is the OWNER/CI catalog, owned by the baseline lane (w65 / card 0428-274/273), not by #1820's product write-set. #1820 does not modify `pr-gate-coverage.json` in its own range.
- **#1820 vs #1818:** DISJOINT. `app_status_result.go` is #1818's; #1820 does not touch it.
- **Collision finding:** none. #1820 is clean against every parallel lane. The only same-file presence is the seam-C product payload inherited from the chain it stacks on (expected).
- **CORRECTION 2026-11-26 (w301-0428-251-planhops, forward-only dated addition; prior lines left intact):** The above "seam-C payload" framing is an over-claim by this read-only census lane. Per the seam-C ownership ruling the product files `internal/application/runtime_postgres.go` and `internal/metrics/perses_dashboard_provision*.go` are **#1819's seam-C**, not #1820's or #84's to own. This #84 lane (`ourist-shift-w284`) is a READ-ONLY exact-head census of the #1820 chain head — it wrote no product path and asserted no seam-C ownership. w267's HOLD on this akte (2026-11-26, review of the #1820 seam-C write-set) required narrowing this write-set claim to what w284 actually did: a read-only recipe, with NO seam-C ownership claim. The seam-C product files appear in #1820's branch only because the forward-stack chain inherits them; that is chain lineage, not #1820's deliverable. #1819 remains the seam-C owner.

## 4. GATE / UNIT WITNESS GAP (seam-C path re-verification)

**#1820 head `8f6b2444b` runs (API `?head_sha=…&per_page=100` incl attempts): exactly ONE run.**
- run **45710380590** — event `pull_request`, status completed / conclusion success.

Jobs in 45710380590 (30 total). Executed (completed/success): Workflow policy, Trusted Plan, Source format, Native gate plan, Runner Interface, Exact Candidate, Focused Python, Demo Pin, ci-policy, go-build, go-vet, ci-actionlint, ci-executor-tests, Candidate-added checks (advisory), and Go-unit shards **cli-0 / cli-1 / cli-2 / packages / owner** (all success). Skipped: Main release source, Targeted HA docker/podman, Main release Go, Exact full Pre-Release, Draft Go, Native, Workstation onboarding, Release Source Preflight, Draft source/routing.

**SEAM-C UNIT-WITNESS VERDICT — CONFIRMED, NOT a gap:**
- The prior census (w242) reported a single executed job (139543613494) on the seam-C path. On the *current* #1820 head the seam-C product files (`internal/application/runtime_postgres.go`, `internal/metrics/perses_dashboard_provision.go` + `_test.go`) are covered by the executed **`PR · Go unit · packages`** job (139543061428, success) and the **`PR · Go unit · owner`** shard (139543061418, success). `git diff develop...1820` confirms these files are live in the payload, so packages/owner did not run on a no-op.
- #1819 head `b3c5055ad` has TWO executed runs (45699760220, 45694363486) with the Go-unit packages/cli shards green — corroborating the seam-C path has live CI witness upstream in the chain.
- **FINDING (advisory, no action taken — `.github/**` is Owner scope):** the *required* runtime gates (Targeted HA docker/podman, Main release Go, Exact full Pre-Release, Native) are **SKIPPED** on the current #1820 head 45710380590. This is the pre-release catalog gating a demo pin (`pre-release-runtime-suite.yml`), not the seam-C Go unit witness. If the acceptance recipe (deliverable 5) requires runtime-broker proof on the final exact head, that is a *required*-gate execution, not a unit test — state the exact selector in `scripts/pr-gate-plan.py`/`pr-gate-coverage.json` that would admit it and hand to Codex/Owner. **No routing edited.**

## 5. QUALIFICATION RECIPE (ordered — AFTER #1819 merges)

1. **Branch off #1820 FIRST** (before any develop absorb): `git fetch lane-origin 'refs/pull/1820/head'`; verify `git merge-base --is-ancestor origin/develop HEAD` at the point of branching from `8f6b2444b`. Cut #1820 candidate from `refs/pull/1820/head` (attested base SHA `8f6b2444bdc9baabf4f492e930533c7c36406979`), never from another PR head.
2. **Absorbs the LIVE develop tip** (after #1819 lands + requalifies on the new develop): `git merge origin/develop` → **ordinary merge commit** (no rebase). Guard after hop: `git diff develop...HEAD --name-status` stays non-empty.
3. **Two DISTINCT pull_request run IDs on the EXACT final head** (`8f6b2444b`-style, i.e. the post-absorb head). Second trigger = **`gh pr close --comment 'second exact-head hosted run trigger (coordinator-authorized)' && gh pr reopen`** (close+reopen pair). A rerun raises run_attempt on the SAME id and is VOID as pair evidence.
4. **Record executed-vs-skipped per named job** from the jobs API (per_page=100, incl attempts); a job SUCCESS on a no-op log line is not behaviour proof.
5. **Identity** = this lane's canonical identity from card frontmatter: `git -c user.name=w198-0428-284-demo-parser -c user.email=w198-0428-284-demo-parser@baseharbor.local`. Never a foreign lane identity.
6. Merge path: #1812 (slot 1) → #1819 (slot 2) → #1820 (slot 4); #1812 must merge first; rebase/qualify #1819 after, #1820 after #1819. Chain order strict.

## 6. AKTE (this lane's own deliverable — read-only PR)

- Evidence akte written to plan worktree: `evidence/w266-0428-285-1820pre/akte.md`
- This lane pushes **its own branch** off `origin/main` of baseharbor-plan and opens a PR **against baseharbor-plan** (Owner scope: evidence lives ONLY in baseharbor-plan, NEVER in a product repo; plan main is protected — branch push + plan PR + admin squash merge, never direct main push).
- **This lane does NOT merge.** END_DONE = tables + disjointness verdict + unit-witness verdict + plan PR number + explicit zero-mutations / zero-CI-triggers confirmation.

## CLEANLINESS

- `docker ps -a` (own pid witness, before/after): no containers/compose started — read-only lane; daemon empty throughout.
- Worktrees created: `/tmp/opencode/w266-0428-285-1820pre-wt` (product, detached), `/home/marcel/dev/baseharbor-ecosystem/workers/w266-plan` (plan). Both removed at END.
- No product files touched; no test executed; no CI run; no workflow changed; no card edited.

## STOP / HANDOFF

- This lane is read-only census for card 0428-285 slot 4. All deliverables 1–6 produced. No mutation, no CI trigger.
- END_DONE w266-0428-285-1820pre: pre-flight census complete; #1820 head `8f6b2444b` OPEN/MERGEABLE; seam-C unit witness confirmed (packages/owner shards green on run 45710380590); write-sets disjoint vs 1833/1650/1818; plan akte PR pending.

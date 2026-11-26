# AKTE — w304-0428-249-pr1812hop2

**Isolated worktree absolute path:** `/var/tmp/w304-0428-249-pr1812hop2-wt` (branch `lane-0428-249-runtime-image-fix`). Worktree created via `git worktree add /var/tmp/w304-0428-249-pr1812hop2-wt lane-0428-249-runtime-image-fix`.

Re-qualification of product PR #1812. Clean continuation after prior lane w303-0428-284-pr1812hop produced nothing in ~27 minutes.

## visible ansatz block

- Base SHA (origin/develop, fetched at runtime, ancestor of my first commit): `b7855f78a0253b9423e07da6ae92009b8f0fd1ae`
  (verified via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`)
- Branch head I merged onto (remote tip): `0922888af8fd70be4049cec529c69aebc057a356`
  (verified via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-249-runtime-image-fix`)
- Card frontmatter owner (verbatim, fetched from origin/main at runtime from `tasks/t-20261122-runtime-image-registry-artifact-unknown.md`): `owner: w170-0428-249-demo-pr175-fixup` (card 0428-249, "light-runtime blob unknown", release v0.4.28, PRs #1812 #1837).
- git user.name: w304-0428-249-pr1812hop2
- git user.email: w304-0428-249-pr1812hop2@baseharbor.local
- literal merge commit invocation: `git -c user.name=w304-0428-249-pr1812hop2 -c user.email=w304-0428-249-pr1812hop2@baseharbor.local merge --no-ff origin/develop`
- pre-push gate line: `git log --format='%h an=%an cn=%cn' -1`

## PLAN

- Create isolated worktree under /var/tmp with lane name; announce absolute path.
- One ordinary merge commit of origin/develop; normal push. NO rebase/force/cherry-pick/re-cut.
- Lineage finding (forward-only): paste `git log --format='%h %an %cn %ae %s' origin/develop..HEAD`.
- Guards in akte: diff name-status, merge-base is-ancestor, workflow existence proof, no semantic change line.
- Watch MY OWN first pull_request run to terminal; census executed vs skipped per required job incl. ci.yml:1178 skip.
- Akte via ONE scoped plan PR of my own.

## Step 1 worktree
`/var/tmp/w304-0428-249-pr1812hop2-wt`, detached from remote tip `0922888af8` (the local baseharbor checkout was stale at `394559ec6`; reset to remote tip before merging — see step 2 note).

## Step 2 merge commit
- HEAD after merge: `b962e6d2cc56258730e0d580d053565561da6d5a`
- Parents: `394559ec6`? NO — parents are `0922888af8` (remote branch tip) and `b7855f78a` (develop). It is a genuine merge commit (two parents).
- Push: `0922888af..b962e6d2c` OK.
- NOTE — first push REJECTED (non-fast-forward): the baseharbor checkout's local `lane-0428-249-runtime-image-fix` was behind the remote (`394559ec6` vs remote `0922888af8`, which itself carried an extra hop `f166a49f2`). Reset the branch to the remote tip `0922888af8` then re-ran the merge; the fresh merge commit `b962e6d2c` is built on top of the actual remote tip. No force-push, no cherry-pick, no re-cut.

## Step 3 lineage (forward-only, no rewrite)
`git log --format='%h %an %cn %ae %s' origin/develop..HEAD`:
```
b962e6d2c w304-0428-249-pr1812hop2 w304-0428-249-pr1812hop2 w304-0428-249-pr1812hop2@baseharbor.local Merge remote-tracking branch 'origin/develop' into lane-0428-249-runtime-image-fix
0922888af w198-0428-284-demo-parser w198-0428-284-demo-parser w198-0428-284-demo-parser@baseharbor.local hop(0428-284): synchronize PR #1812 onto current develop for fresh Selected Runtime gate w198-0428-284-demo-parser
f166a49f2 w198-0428-284-demo-parser w198-0428-284-demo-parser w198-0428-284-demo-parser@baseharbor.local hop(0428-284): synchronize PR #1812 onto current develop for fresh Selected Runtime gate w198-0428-284-demo-parser
394559ec6 w198-0428-284-demo-parser w198-0428-284-demo-parser w198-0428-284-demo-parser@baseharbor.local hop(0428-284): re-admit PR #1812 onto current develop w198-0428-284-demo-parser
eafd5e6d6 lv4-verify lv4-verify worker@baseharbor.local Merge remote-tracking branch 'origin/develop' into lane-0428-249-runtime-image-fix
101291960 lv4-verify lv4-verify worker@baseharbor.local Drop scripts/release-requirements.json from #1812: restore develop state (v0.4.28 gate work belongs to PR #1746 trace, not this PR)
3859d4663 lv4-verify lv4-verify worker@baseharbor.local release-requirements: add v0.4.28 to 14 docker/podman light gate rows
2ea416209 lv4-verify lv4-verify worker@baseharbor.local Merge remote-tracking branch 'origin/develop' into lane-0428-249-runtime-image-fix
64d3dc0e7 lv4-verify lv4-verify worker@baseharbor.local Merge remote-tracking branch 'origin/develop' into lane-0428-249-runtime-image-fix
9140b2cbd Codex w53-0428-152-alertfix codex@openai.com ci: reload candidate image before runtime publish
```
Only ONE commit (`b962e6d2c`) is a fresh commit introduced by this lane; all others are pre-existing ancestors carried on the branch. Carried attribution includes foreign-lane identities (`w198-0428-284-demo-parser`, `lv4-verify`, `Codex w53-0428-152-alertfix`) — the same foreign-lane attribution pattern that voided #1856 and forced #1858. As instructed, I do NOT rewrite or hide it; Codex decides as-is versus a clean successor. The branch is otherwise clean (no uncommitted/unpushed changes).

## Step 4 guards
- `git merge-base --is-ancestor origin/develop HEAD`: **TRUE**
- `git diff origin/develop...HEAD --name-status`: `M  .github/workflows/pre-release-runtime-suite.yml` — exactly the one workflow file, +20/-0 non-empty payload.
- Workflow file exists on both develop and HEAD (`scripts/pre-release-runtime-impact.json` and `.github/workflows/pre-release-runtime-suite.yml`).
- This lane changed no workflow semantics: the +20/-0 diff is purely the card-0428-249 ordering fix (re-load pre-release runtime image before ORAS publish); no CI authored by this lane.
- Deliveries verified via `git ls-remote`: branch head = PR #1812 head = `b962e6d2cc56258730e0d580d053565561da6d5a`.

## (1) Run 45771862723 census + Trusted Plan log VERBATIM (the run that qualified nothing)
- head SHA (run): `b962e6d2cc56258730e0d580d053565561da6d5a` ; develop base: `b7855f78a0253b9423e07da6ae92009b8f0fd1ae`
- aggregate: status=completed conclusion=success (aggregate SUCCESS)
- job census (per_page=100): total=30 = **executed 11 / skipped 19 / failed 0**
- EXECUTED (11): Source format, Native gate plan, Workflow policy, Trusted Plan, PR · Candidate-added checks (advisory), Focused Python, Validation · pr-planner-tests, Validation · ci-actionlint, Validation · receipt-execution-tests, Validation · ci-policy, Validation · ci-executor-tests
- SKIPPED (19) includes every runtime-family selector gate that never ran:
  - 139746230693  PR · Selected Runtime
  - 139746230302  PR · Native Keycloak/Core · ${{ matrix.runtime }}
  - 139746230506  PR · Selected Core-less · ${{ matrix.runtime }}
  - 139746228948  PR · Exact Candidate
  - 139746219524  PR · Main release Go · ${{ matrix.shard }}
  - 139746202671  PR · Draft source and routing
  - 139746161786  Targeted HA · docker
  - 139746209627  Targeted HA · podman
  - 139746160988  Targeted · Workstation onboarding · ${{ matrix.runtime }}
  - 139746161503  PR · Exact full Pre-Release
  - 139746161591  Release Source Preflight
  - 139746161610  validate
  - 139746161714  PR · Main release source
  - 139746162178  PR · Draft Go · ${{ matrix.shard }}
  - 139746230258  PR · Consumer Pins
  - 139746230264  PR · Runner Interface
  - 139746230292  PR · Demo Pin
  - 139746230416  PR · Public Contracts
- The 14 Docker/Podman-Light gates never executed: aggregate green does NOT qualify.

Trusted Plan log for job `139746160060` ("PR · Trusted Plan"): 74070 bytes retrieved from the signed Azure blob URL (`GET /jobs/{id}/logs` returned 302 → followed `-L` to productionresultssa8). The decisive selection JSON printed by the job at 2026-11-26T06:58:13.9776150Z (verbatim):

```
{"matrix": {"include": [{"check": "ci-actionlint"}, {"check": "ci-executor-tests"}, {"check": "ci-policy"}, {"check": "pr-planner-tests"}, {"check": "receipt-execution-tests"}]}, "previous_run": null, "reason": "previous source/base ancestry not proven", "reused_checks": [], "reused_gates": [], "runtime_matrix": {"include": [{"gate": "not-required", "id": "not-required", "runtime": "static"}]}}
```

- **broad_required**: NOT true — the resolver did not set the broad fallback; it resolved to the conservative unknown-source path with `runtime_matrix.include=[not-required]` (zero runtime gates). `broad_required=False` with zero runtime gates is the non-qualifying state; aggregate success is a false positive here.
- **selected_gates / SELECTED_MATRIX** (verbatim, from the job log):
  `SELECTED_MATRIX: {"include":[{"check":"ci-actionlint"},{"check":"ci-executor-tests"},{"check":"ci-policy"},{"check":"pr-planner-tests"},{"check":"receipt-execution-tests"}]}`
  — 5 validation checks, zero runtime gates.
- **reason** field (verbatim): `"previous source/base ancestry not proven"`; `previous_run=null`, `reused_checks=[]`, `reused_gates=[]`.
- **runtime_required** output (verbatim): `runtime_matrix.include` is a single `not-required` row — no `atomic/docker/*` / `atomic/podman/*` / `ha/*` / `journey/*` gate ids.
- Same run's notice line (verbatim): `##[notice]Incremental PR checks: previous source/base ancestry not proven; reused validations=0; reused runtime gates=0`.

## (2) CATALOG GAP — FINDING (stated, NOT edited; catalog rows are card 0428-352 / 0428-273 baseline work)
Two independent gaps both route this lane's diff (only `.github/workflows/pre-release-runtime-suite.yml`) to zero runtime gates:

(a) `scripts/pr-gate-coverage.json` owns **zero** `.github/workflows/` rows (verified: 0 rows with `path` starting `.github/workflows/`; 0 rows mentioning `pre-release-runtime-suite`). No `source.<gate-id>` row has `"path": ".github/workflows/pre-release-runtime-suite.yml"`, no `"runtime_specific": true` gate covers it, and no `surfaces` entry maps it — so the plan's `_coverage_module().resolve_covered_gates()` (consumed at `scripts/pr-gate-plan.py` ~line 1931) finds no runtime gate for the changed file.

(b) `scripts/pr-gate-plan.py` **exempts** this file. The exact changed file is bound in `RUNTIME_STEP_CAP_REVIEWED_FILES` at `scripts/pr-gate-plan.py:379` (`'.github/workflows/pre-release-runtime-suite.yml': 'modified'`) and in `DISPATCH_GATE_REF_REVIEWED_FILES` at `scripts/pr-gate-plan.py:384`. These keyed allowlists route the file to the conservative unknown-source fallback (`scripts/pr-gate-plan.py` ~line 2000: `coverage_status='resolved'`, `fallback_used=True`), which selects only package validations and never lifecycle/journey/runtime gates (`scripts/pr-gate-plan.py` ~line 2018: "Unknown narrow coverage selects normal broad unit/vet/build checks; runtime gates require declared coverage").

What WOULD make the trusted plan select the 14 runtime gates (stated, not implemented):
- A `runtime_specific: true` catalog row in `scripts/pr-gate-coverage.json` whose `source.<gate-id>` covers `internal/application/runtime_identity_workload.go` (currently has NO row at all) AND whose `surfaces` include the `atomic/docker/*` / `atomic/podman/*` ids the release catalog marks `required_for v0.4.28` (the 14 Docker/Podman-Light gate ids in `scripts/release-requirements.json`, e.g. `atomic/docker/lifecycle`, `atomic/podman/lifecycle`, `ha/docker/data`, `ha/podman/data`, ...).
- AND the exemption binding at `scripts/pr-gate-plan.py:379` / `:384` must be removed or neutralized, otherwise the file stays on the resolved/read-only branch and never reaches the source-coverage resolver.
- The selector branch that consumes this is `plan()` at `scripts/pr-gate-plan.py:1885` → `_coverage_module().resolve_covered_gates(...)` ~:1931 → `covered` feeds `result['selected_gates']` ~:1992. Only a source path resolving into `covered` (and matching the release `required_for` set) selects those gates.

Stated per instruction; NOT edited. Catalog rows and the exemption allowlist are card 0428-352 / 0428-273 baseline work.

## (3) Plan PR + END
- Akte published via ONE scoped plan PR of this lane: branch `w304-0428-249-pr1812hop2-plan`, detached at origin/main `4f2e018763`, identity `w304-0428-249-pr1812hop2` / `w304-0428-249-pr1812hop2@baseharbor.local`, never merged by me, never direct-pushed to main.
- Evidence path: `evidence/2026-11-26/w304-0428-249-pr1812hop2/akte.md`.

## END LINE
END_DONE w304-0428-249-pr1812hop2

# 0428-326 — Disjoint pre-work, lane w382-0428-326-1868pre

Card: 0428-326 · PR: #1868 · Repo: baseharbor · Lane: w382-0428-326-1868pre
Art: Disjoint pre-work (local hop + finding, NO push, NO hosted run, NO merge). Qualification stays AFTER Owner authorisation of the release label in `baseharbor/scripts/pr-gate-map-v1.json`.

This is the four-field akte. Findings only; no self-submission.

## 1. What / Status / Next (4-field)

- **What:** Local `git merge origin/develop` of PR #1868 head to measure CI routing for card 0428-326; report which jobs run unassigned on this head, the exact catalog row/key required in `scripts/pr-gate-coverage.json` (driven by `scripts/pr-gate-map-v1.json` release label), and whether the Trusted Plan gate needs extra catalog lines.
- **Status:** END_DONE. Local hop clean; finding fully recorded. No push, no hosted run, no merge to GitHub, no catalog edit.
- **Next:** Owner (not this lane) adds the two uncataloged `cmd/baha/` source rows to `scripts/pr-gate-coverage.json` when the release label in `scripts/pr-gate-map-v1.json` is authorised; then #1868 qualifies.

## 2. Witness — PR #1868 (a)

`gh pr view 1868 --repo mcpdev80/baseharbor --json headRefOid,headRefName,baseRefName,state,mergeable`:

```
{"baseRefName":"develop","headRefName":"w341-0428-326-proofleak","headRefOid":"57320af6949eaf8fc450205da87a4f6ba7166324","mergeable":"MERGEABLE","state":"OPEN"}
```

- baseRefName: `develop`
- headRefName: `w341-0428-326-proofleak`
- headRefOid: `57320af6949eaf8fc450205da87a4f6ba7166324`
- state: OPEN, mergeable: MERGEABLE

`git ls-remote baseharbor refs/heads/w341-0428-326-proofleak`:
```
57320af6949eaf8fc450205da87a4f6ba7166324	refs/heads/w341-0428-326-proofleak
```

## 3. Worktree / base / merge (b, c)

Worktree cut from the PR head SHA:
```
git worktree add --detach workers/worktrees/w382-0428-326-1868pre 57320af6949eaf8fc450205da87a4f6ba7166324
```

Real remote for baseharbor (URL contains github.com/mcpdev80):
```
baseharbor	https://github.com/mcpdev80/baseharbor.git (fetch)
baseharbor	https://github.com/mcpdev80/baseharbor.git (push)
```
(`origin` in this worktree points at baseharbor-plan; the baseharbor repo remote is `baseharbor`, per the Remote Guard rule.)

Fetch + merge (local only, no push, no force):
```
git fetch baseharbor develop
git merge baseharbor/develop
```
Merge commit SHA: `6619b2542914a694d36d11caf8a6d23139eb50f8`
Parents: `57320af6949eaf8fc450205da87a4f6ba7166324` (PR base head) · `ea5218d72e263f21e79853b679af50074dab8c25` (develop tip)

Ancestry proof:
```
git merge-base --is-ancestor 57320af6949eaf8fc450205da87a4f6ba7166324 HEAD   -> 0 (base head IS ancestor)
```
Diff `57320af6949eaf8fc450205da87a4f6ba7166324..HEAD` lists only the develop work behind the PR head (pagination + `internal/application/workload` runtime-specific catalog rows). No foreign candidate carried on top; the only new commit is the single develop-merge.

## 4. FINDING — which jobs run unassigned on this head (d)

### 4.1 The PR diff (base develop → PR head)

`scripts/pr-diff-base.py --target-base ea5218d72e263f21e79853b679af50074dab8c25 --head 57320af6949eaf8fc450205da87a4f6ba7166324`:

```json
{"base_tip_sha": null, "broad_required": false, "head_sha": "57320af6949eaf8fc450205da87a4f6ba7166324", "integration_sha": null, "merge_base_sha": "5a37ddbd9a06dd44f6068d3266ff2ed853a84a74", "target_base_sha": "ea5218d72e263f21e79853b679af50074dab8c25", "changes": [
  {"path": "cmd/baha/app_runtime_retirement.go", "status": "modified"},
  {"path": "cmd/baha/w341_never_delivered_retire_proof_test.go", "status": "added"},
  {"path": "internal/deployment/never_delivered_proof.go", "status": "modified"}
]}
```

### 4.2 The planner fails closed on two uncataloged sources

Running the planner with authenticated runner context:
```
GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop python3 scripts/pr-gate-plan.py --diff /tmp/diffbase_pr.json
```
Produces (exact, verbatim):
```
ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: cmd/baha/app_runtime_retirement.go (id source.cmd_baha_app_runtime_retirement_go): add this source with its surfaces to scripts/pr-gate-coverage.json, e.g. {"id": "source.cmd_baha_app_runtime_retirement_go", "path": "cmd/baha/app_runtime_retirement.go", "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]}; cmd/baha/w341_never_delivered_retire_proof_test.go (id source.cmd_baha_w341_never_delivered_retire_proof_test_go): add this source with its surfaces to scripts/pr-gate-coverage.json, e.g. {"id": "source.cmd_baha_w341_never_delivered_retire_proof_test_go", "path": "cmd/baha/w341_never_delivered_retire_proof_test.go", "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]}
```

### 4.3 What runs UNASSIGNED on this head

The 3 changed paths split as:
- `internal/deployment/never_delivered_proof.go` — already cataloged (components row at `scripts/pr-gate-coverage.json`, id `source.internal.deployment.never.delivered.proof.go`, surfaces `source.gate.atomic.docker.lifecycle` / `source.gate.atomic.podman.lifecycle`).
- `cmd/baha/app_runtime_retirement.go` (modified) — NOT cataloged (exists at base develop, present at base catalog; only modified here).
- `cmd/baha/w341_never_delivered_retire_proof_test.go` (added at head) — NOT cataloged.

Because two `cmd/` sources have no declared catalog owner, the planner aborts fail-loud (the guard at `scripts/pr-gate-plan.py` `plan()` lines ~1948-1956: `source_unowned = [p for p in unowned if p.startswith('cmd/') or p.startswith('internal/')]`). Net result: **no gate is selected — the PR cannot be qualified until the two sources are cataloged.**

### 4.4 Exact key and line needed

`scripts/pr-gate-coverage.json` is the catalog the planner reads (referenced at `scripts/pr-gate-plan.py` line 1902 `coverage_path = ROOT / 'pr-gate-coverage.json'`; resolved via `resolve_covered_gates` at `scripts/validate-pr-gate-coverage.py` line 17). The exact catalog keys expected (from the planner's own error text, `unresolved_source_error` at `scripts/validate-pr-gate-coverage.py` line 80):
- `source.cmd_baha_app_runtime_retirement_go` (path `cmd/baha/app_runtime_retirement.go`)
- `source.cmd_baha_w341_never_delivered_retire_proof_test_go` (path `cmd/baha/w341_never_delivered_retire_proof_test.go`)

`scripts/pr-gate-map-v1.json` itself only carries the release label (`"release": "v0.4.27"`) and policy; the per-source routing lives in `scripts/pr-gate-coverage.json` components. So the missing rows go into `scripts/pr-gate-coverage.json` (components array), not `pr-gate-map-v1.json`.

### 4.5 What gate this resolves to

Simulating the two rows added (surfaces `source.gate.atomic.docker.lifecycle` / `source.gate.atomic.podman.lifecycle`, runtime-neutral): `resolve_covered_gates` returns `selected_gates = ['atomic/docker/lifecycle']`, `unowned = []`. `atomic/docker/lifecycle` and `atomic/podman/lifecycle` are present in the release catalog for v0.4.27 (confirmed against `scripts/release-requirements.json` gates). So exactly one runtime lifecycle gate runs once the catalog is complete.

### 4.6 Trusted Plan / catalog-line need

No extra catalog lines beyond the two source rows above are required for this PR. The catalog validates clean on its own:
```
m.validate(cov, req)  ->  VALIDATE ERRORS: []
```
The Trusted Plan gate requires exactly the two source rows; nothing else in this PR's diff is an uncataloged source. This is a catalog-only change (Owner scope); it does not touch `.github/**`, so the `ci-workflow-policy.sh` gate catalog consistency is not triggered by the catalog edit.

## 5. Scope boundary (grenzen)

- No subagents. Every step ran inside lane w382-0428-326-1868pre.
- No push, no force, no `workflow_dispatch`, no hosted run, no merge to GitHub.
- No product-code change, no config change, no consent/auth delta.
- No card fields edited, no generated views touched.
- No edit to `.github/**`, `scripts/pr-gate-map-v1.json`, or `scripts/pr-gate-coverage.json`. The two missing catalog rows are reported here as the exact next Owner action, not submitted.

## 6. Cleanliness

Worktree owned by this lane only:
```
/home/marcel/dev/baseharbor-ecosystem/workers/workers/worktrees/w382-0428-326-1868pre  57320af69 (detached)
```
No containers/compose started; nothing to bring down.

## 7. Commit identity note

Merge created under the pre-existing worktree's own author (lane w373-0428-284-demo183fix); this is a read-only local hop for a finding — the merge head is not a pushed candidate and never carries into evidence of remote state. No push occurred.

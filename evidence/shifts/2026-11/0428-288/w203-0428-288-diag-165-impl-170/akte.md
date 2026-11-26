# w203-0428-288-diag-165-impl-170 — Akte

## PLAN
1. Verify environment: planning repo remote, real product remote via git remote -v, gh auth.
2. Confirm PR 1650 / branch head SHA 903991f3b exists on origin.
3. List every job of runs 45639912161 and 45647698524 (per_page=100); flag any plan-coverage job not EXECUTED.
4. Check branch-protection required checks for lane-0428-078-perses-identity-on-resolver.
5. Check PR required-checks context + approving reviews to find the precise blocking gate.
6. Report ONE STATE line (blocker + file:line evidence). No edits; STEP B on DISPOSITION-CONFIRMED only.
7. Post END line to coordinator; update evidence file.

## Environment
- Planning repo: `origin=https://github.com/mcpdev80/baseharbor-plan.git` (verified `git -C baseharbor-plan remote -v`).
- gh authenticated as `mcpdev80` (token gho_*, git-over-ssh).
- Task scope: read-only diagnosis of PR #1650 mergeable_state=BLOCKED. STEP B (implement #170 disposition) is gated on DISPOSITION-CONFIRMED. This shift = STEP A only.

## Diagnosis — #1650 BLOCKED despite two green CI workflow_dispatch runs

### Head / PR
- PR #1650 "fix(0428-078): wire Perses identity-keycloak into 080 resolver fan-in", branch `lane-0428-078-perses-identity-on-resolver`.
- Head SHA on origin (git ls-remote): `903991f3b8ec57993afdb7e0c57c51da30135098` — confirmed present.
- GH status: `mergeStateStatus=BLOCKED`, `mergeable=MERGEABLE`, `isDraft=false`, `reviewDecision=null` (confirmed via curl graphql + `gh pr view`).
- PR changed files (3): `cmd/baha/app_perses_cli_test.go` (modified), `cmd/baha/app_status_result.go` (modified), `internal/metrics/identity_dashboard_witness.go` (added).

### The two cited runs are NOT green — Trusted Plan was SKIPPED in both
- Run 45639912161 (2026-11-25T14:58:29Z): event=`workflow_dispatch`, head_sha=903991f3b...98, conclusion=success.
- Run 45647698524 (2026-11-25T15:39:51Z): event=`workflow_dispatch`, head_sha=903991f3b...98, conclusion=success.
- Both runs: EVERY required gate job is `conclusion=skipped`. Only `validate` and `Workflow policy` ran SUCCESS.
- `PR · Trusted Plan` job conclusion: **skipped in both** runs (job list per_page=100 confirms).
- A third, different run 45632065203 (2026-11-25T14:15) actually EXECUTED Trusted Plan and it ended **FAILURE** (plus PR Selected Checks FAILURE).

### Root cause — uncataloged source change in the Trusted Plan gate
- The PR adds `internal/metrics/identity_dashboard_witness.go` (sha d79949434..., 6846 bytes, status=added).
- Trusted Plan (job 139267610269, run 45632065203) FAILS with a hard error from `pr-gate-plan.py`:
  - File/line: `pr-gate-plan.py` line 1836, inside `plan(...)`, raise at line 1836; wrapper at line 1940 / module entry 1947.
  - Log line: `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/metrics/identity_dashboard_witness.go (id source.internal_metrics_identity_dashboard_witness_go): add this source with its surfaces to scripts/pr-gate-coverage.json, e.g. {"id": "source.internal_metrics_identity_dashboard_witness_go", "path": "internal/metrics/identity_dashboard_witness.go", "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]}`
  - `##[error]Process completed with exit code 1.`
- Verified the source is genuinely uncataloged on the exact head: `grep -c identity_dashboard_witness` in `scripts/pr-gate-coverage.json` @ 903991f3b = **0**. The catalog has 129057 bytes with many `internal/metrics/` entries but none for `identity_dashboard_witness.go`.

### Ruled out the other two candidate blockers the mission named
- Branch-protection required checks: `GET /branches/lane-0428-078-perses-identity-on-resolver/protection` = 404 "Branch not protected"; default branch `develop` protection = 404 "Branch not protected". No required-status-checks config anywhere. So BLOCKED is not from a branch-protection required-checks list.
- Missing approving reviews: `GET /pulls/1650/reviews` = 0 reviews; `reviewDecision=null`. Not an approving-review gate.
- No status contexts on the head SHA (`GET /statuses/903991f3b...98` = 0). The blockage is the Trusted Plan check-run FAILURE inside the CI workflow, not a GitHub-level required-check context.

### STATE (one line, blocker + file:line)
BLOCKER = CI Trusted Plan check-run FAILS (not skipped) on exact head 903991f3b because the PR adds `internal/metrics/identity_dashboard_witness.go` with no declared runtime-gate owner in `scripts/pr-gate-coverage.json`; the two cited runs skipped that gate so they never exercised it. Evidence: run 45632065203 job 139267610269 log `ValueError: ...uncataloged source change... internal/metrics/identity_dashboard_witness.go (id source.internal_metrics_identity_dashboard_witness_go)... add this source with its surfaces to scripts/pr-gate-coverage.json` (pr-gate-plan.py line 1836); catalog grep for `identity_dashboard_witness` @903991f3b = 0; branch protection 404; reviews 0.

## STEP B — not started
Awaiting owner DISPOSITION-CONFIRMED. Refinement (2026-11-25): #170 = extend card 0428-250 with a NEW narrow workflow `pr-config-matrix.yml` (draft at `workers/w200-codex-disposition/170/`). EXPLICIT EXCEPTION: adding ONLY that `pr-config-matrix.yml` file (verbatim / draft-faithful) plus the `run.sh` matrix row it qualifies to the #170 demo PR branch is AUTHORIZED; nothing else in `.github/**`, no further CI scope growth. Sequence on DISPOSITION-CONFIRMED: read draft → add verbatim → set git identity to 0428-250 frontmatter owner (%an gate) → normal push → new workflow runs full config-matrix gate on exact head → watch own run to terminal → report head+run IDs → w200 reviews exact head. Plan side stays a freeze-safe draft; no 0428-250 card edit by this lane.

## Cleanliness
- Read-only shift. No containers, compose projects, or git mutations to the product repo. No `docker ps -a` witnesses needed.

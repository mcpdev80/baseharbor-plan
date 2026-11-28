# Read-only status akte — 0428-249 / PR #1812 — lane w400-0428-249-1812heal

Date (host): 2026-11-28. Scope: OWNER STOP — read-only status report for PR #1812 (repo mcpdev80/baseharbor, branch `lane-0428-249-runtime-image-fix`). NO write, NO push, NO rerun, NO close/reopen, NO board/gate/card edit. This akte is the only file written this turn.

## 0. Remote witnesses (own git, github.com/mcpdev80)

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-249-runtime-image-fix` => `c2dd3ff04e30c73046b4eeecb56f3cab20e56c92`
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `6944e8761af6f07b801f55e39bb9a5409226c10b`
- PR head (gh pr view 1812) headRefOid = `c2dd3ff04e30c73046b4eeecb56f3cab20e56c92` (matches ls-remote)
- `git merge-base --is-ancestor 6944e876... c2dd3ff0...` => develop is NOT an ancestor of head (BEHIND). Confirmed `mergeStateStatus: BEHIND` via gh.
- HEAD unchanged since dispatch (dispatch head was `c2dd3ff04e30c73046b4eeecb56f3cab20e56c92` per mission step 3). No drift in the live branch ref.

## 1. Current head

- Branch: `lane-0428-249-runtime-image-fix`
- Head SHA: `c2dd3ff04e30c73046b4eeecb56f3cab20e56c92` (full) / `c2dd3ff04e` (10)
- mergeStateStatus: BEHIND (against develop 6944e8761a)
- PR #1812 state: OPEN, title `fix(ci): re-load missing runtime image before ORAS publish`, base `develop`, updatedAt 2026-11-27T05:45:27Z

## 2. Change against dispatch head c2dd3ff0

- No diff: current head == dispatch head. The live branch ref did not move this turn.
- NOTE (evidence, not an edit): the PR body / prior history describes a one-file `.github/workflows/pre-release-runtime-suite.yml` approved scope; the run history carries 38 distinct head SHAs across many past PR events. This akte reports ONLY the current live head c2dd3ff0, which is unchanged.

## 3. Full check list (run 45944501306, PR #1812, run #7957)

Source: `gh pr checks 1812 --repo mcpdev80/baseharbor` + `gh api .../actions/runs/45944501306/jobs`. Run event `pull_request`, head_sha `c2dd3ff0...`, status completed.

Totals:
- SUCCESS: 61
- SKIPPED: 66
- FAILURE: 9 (all in the `PR Selected Checks` composite job; the aggregate `PR Selected Checks` job 140335189160 conclusion = failure)
- CANCELLED: 0
- TOTAL checks listed: 136

PASS (61, representative): Trusted Plan, Workflow policy, Native gate plan, Source format, Go unit (cli-0..3, owner, packages), Validation (go-vet, ci-actionlint, ci-executor-tests, ci-integration-operator-seam-tests, ci-policy, go-build, pr-planner-tests, receipt-execution-tests), Native · native/docker|podman/data-capabilities, Candidate-added (advisory), Demo Pin, Exact Candidate, Runner Interface, Focused Python, all Selected Core-less docker/podman (foundation..identity-backend + aggregator), all Selected Runtime `resolve_candidate` subjobs (docker + podman, every gate), Podman guided/data-capabilities/failure, Docker data-capabilities/failure/lifecycle/guided.

SKIP (66): all `Selected Core-less ... ${{ matrix.runtime }}` matrix instances, Draft source/routing, Draft Go, Main release source/Go, Exact full Pre-Release, Consumer Pins, Public Contracts, Main release checks, Native Keycloak/Core, Targeted HA docker/podman, Workstation onboarding, validate, Release Source Preflight.

FAIL (9) — all `Selected Runtime / Executed` jobs, run_id 45944501306:
1. Executed docker · connectivity — job 140326489447
2. Executed docker · full-destroy — job 140326484459
3. Executed docker · policy — job 140326537573
4. Executed docker · reconciliation — job 140326533408
5. Executed podman · connectivity — job 140326525870
6. Executed podman · full-destroy — job 140326577053
7. Executed podman · policy — job 140326573644
8. Executed podman · reconciliation — job 140326484294
9. (aggregate) PR Selected Checks — job 140335189160

## 4. The 9 red checks — first verbatim error line + job name + run-id

Root cause identical across all 9 runtime "Executed" jobs (first error from step "Run runtime gate", job log step number 20):

- Verbatim failing line (docker/connectivity, job 140326489447):
  `2026-11-27T05:17:26.7900913Z [36;1mError: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state[0m`
- Same exact line in all 9 (docker + podman, all four gates connectivity/full-destroy/policy/reconciliation).
- Terminal assertion (docker/connectivity): `demo-connectivity FAIL — .../tests/connectivity/run.sh:36: assertion command failed (exit 1) ... run_consented "baha" up --yes ...`
- Job name: `PR · Selected Runtime (atomic/<runtime>/<gate>, <runtime>, <gate>) / Executed <runtime> · <gate>` (e.g. `Executed docker · connectivity`).
- Run-id for all 9: 45944501306 (composite job 140335189160 = `PR Selected Checks`).

Observation: the 8 remaining runtime gates (data-capabilities, lifecycle, guided, failure) for BOTH runtimes PASSED under the same run; only connectivity/full-destroy/policy/reconciliation Executed jobs failed. This is not a single consent cause: 4 distinct gate signatures, and the failing set is gated by the consent error at `record deployment before mutation` + a fixture-level demo-connectivity assertion failure (possibly a harness/fixture assertion gap, not pure consent) — matching the card's >=3 distinct failure-signature blocker.

## 5. Base stand

- develop head: `6944e8761af6f07b801f55e39bb9a5409226c10b` (ls-remote, runtime)
- `git merge-base --is-ancestor origin/develop HEAD`: NO — develop is NOT an ancestor of the candidate head. Candidate is BEHIND develop by the full develop delta.
- PR base ref: develop.

## 6. BLOCKER list

A. What goes GREEN without any edit (already green, documented):
- All Go unit, Validation, Native data-capabilities, Core-less integration, resolve_candidate, data-capabilities/lifecycle/guided/failure runtime gates, plus Trusted Plan / Workflow policy / Source format / Exact Candidate / Demo Pin — all SUCCESS. No action needed.

B. What goes GREEN WITHOUT an edit (external, not this repo's code):
- The 9 failing `Selected Runtime Executed` gates fail at the product consent boundary (`candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state`) and a fixture-level `demo-connectivity` assertion. Per card history this is the same external fixture/consent root cause as #1818/#1810 (baha-ci-operator-testonly production + 0428-250 fixture allowlist). Greening these requires the 0428-250 fixture allowlist change (Owner/other card), NOT an edit on this branch.

C. What requires an edit (Owner scope, NOT done here):
- Any `.github/**` workflow edit (pre-release-runtime-suite.yml or others) to change gate ordering / the resolve_candidate / archive-reload path is Owner-scope. This lane does not edit them.
- Any product authorization-boundary behavior (the `--confirm-candidate` operator-auth path in operatorauth/authorization.go + ci_integration_operator_enabled.go) is product behavior; per AGENTS 3.8 / AGENTS.md this is an Owner decision point, not a lane edit.

D. Owner-scope only (.github/**):
- `.github/**` files (CI workflow routing / gate catalog / release matrix). This lane reports them as findings with file:line, never edits them, never triggers reruns or workflow_dispatch. The 9 failing runtime gates are gated by Owner-scope fixture + consent + workflow-ordering decisions owned outside this branch.

## 7. Scope note (evidence, not an edit)

The candidate PR #1812 body/prior history references a one-file `.github/workflows/pre-release-runtime-suite.yml` approved edit set. The current live branch ref head is unchanged (c2dd3ff0) and this akte reports only that. Past PR events on #1812 carried 38 distinct head SHAs; none is acted on here. No new branch, no edit, no merge.

## END line

END_DONE w400-0428-249-1812heal: read-only status report delivered. head=c2dd3ff04e develop=6944e8761a ancestor=nein checks=61 success / 66 skipped / 9 failure / 0 cancelled blocker=9 Selected-Runtime Executed docker+podman gates fail at operator consent boundary (--confirm-candidate / "refusing to record deployment state") + fixture demo-connectivity assertion; external fixture+consent+Owner .github scope, no lane edit. No write/push/rerun performed.

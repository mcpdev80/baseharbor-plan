# CODEX-MERGE handoff: PR 1788 into PR 1783 feature branch

## PLAN

1. Read the merge contract and record its target, authorization, stop conditions, and evidence path.
2. Verify live PRs, exact base/head refs, scoped diff, ancestry, and required check state.
3. Merge PR #1788 into the named #1783 feature branch only if GitHub and the required CI gates permit it without bypass.
4. Verify remote refs and PR states; confirm develop remains unchanged.
5. Validate and publish the evidence on Planning origin/main, update the board, and post END.

## Mission and verified refs

The mission requests only the owner-authorized stacked merge of #1788 into the base branch of #1783, `lane-0428-241-optionA-operator-allowlist`; it forbids content edits, force updates, develop merges, and CI bypass. The product remote was resolved by `git remote -v`; `lane-origin`, `origin`, and `upstream` all showed `https://github.com/mcpdev80/baseharbor.git`. The authenticated GitHub identity returned by `gh api user --jq .login` was `mcpdev80`. Planning remote was verified before the evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.

Fresh remote refs before any merge attempt:

- `978a0f90b512e98300ee30b5aa2a1cae5d628b21 refs/heads/develop`
- `8b99bdc3c615f29a788e4800e50a685a8099be9a refs/heads/lane-0428-241-optionA-operator-allowlist`
- `8b99bdc3c615f29a788e4800e50a685a8099be9a refs/pull/1783/head`
- `6c12225e12a1e0aa67a6a6555166209379beabc9 refs/pull/1788/head`

GitHub reports #1783 open, base `develop` at `978a0f90b512e98300ee30b5aa2a1cae5d628b21`, head `8b99bdc3c615f29a788e4800e50a685a8099be9a`. PR #1788 is open, based on #1783's exact head `8b99bdc3c615f29a788e4800e50a685a8099be9a`, with exact head `6c12225e12a1e0aa67a6a6555166209379beabc9`. Its changed-file count is two: `cmd/baha/ci_integration_operator_enabled.go` and `cmd/baha/ci_integration_operator_enabled_test.go`; the diff is limited to the CI integration operator fixture and regressions for the exact selected gate forms. No consent product implementation or `.github/**` file is changed by this PR. The feature branch has no branch rules returned by `gh api repos/mcpdev80/baseharbor/rules/branches/lane-0428-241-optionA-operator-allowlist` (`[]`).

## Required CI state and stop

Exact-head run `45062680796` is terminal `completed / failure` on `6c12225e12a1e0aa67a6a6555166209379beabc9` ([run](https://github.com/mcpdev80/baseharbor/actions/runs/45062680796)). Its `PR Selected Checks` check is `failure`, reports GitHub Actions integration `15368`, and the failing step is `Require selected native acceptance before merge` (`Process completed with exit code 1`). The Coordinator merge policy requires this exact aggregate to succeed and forbids bypass; therefore no `gh pr merge` command was issued, even though the native failure is reported by the mission as unrelated runtime-broker drift.

Selected Docker and Podman data-capabilities runtime jobs passed, as did `cli-guided-tests`, `ci-integration-operator-seam-tests`, `source-contracts`, `cli-vet`, `cli-build`, `Focused Python`, `Demo Pin`, `Runner Interface`, `Source format`, `Native gate plan`, `Trusted Plan`, `Exact Candidate`, and `Workflow policy`. The two required native data-capabilities jobs failed: Docker job `137340074342` and Podman job `137340074027`; both failed at `Run selected native gate` while running `TestApplicationCapabilityLifecycleExistingCore/secrets`. Docker reported `application runtime broker readiness failed: application runtime broker container health is unhealthy`. Podman reported `{"Status":"unhealthy","FailingStreak":49,...{"status":"not_ready"}...curl: (22) The requested URL returned error: 503}`. The failed broker used `ghcr.io/mcpdev80/baseharbor-runtime:edge`. These are observed failures; the mission attributes the shared runtime drift to #1770's exact-image pin. Skipped jobs are not treated as passes.

## Outcome

BLOCKED pending owner direction on the failed required `PR Selected Checks` aggregate. PR #1788 remains open and unmerged; PR #1783 remains open with its original head `8b99bdc3c615f29a788e4800e50a685a8099be9a`; develop remains at `978a0f90b512e98300ee30b5aa2a1cae5d628b21`. No product changes, PR merge, force update, or CI rerun was performed. The requested stacked merge witness (new #1783 head with parents #1783 and #1788) therefore does not exist.

## cleanliness

Before review, `docker ps -a --no-trunc` with shell PID 2351059 showed only the header and no containers. No container or compose project was started. After review, `docker ps -a --no-trunc` with shell PID 2352347 also showed only the header and no containers.

## END_BLOCKED

END_BLOCKED: required exact-head `PR Selected Checks` failed on both native data-capabilities jobs; no bypass or merge was attempted. Owner direction is needed before further merge work.

## origin/main evidence path witness

Exact output from `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle5-2026-11-22/guided-fixture-footprint-contract-divergence-0428-241/1788-into-1783-stacked-merge-round-1.md`:

`evidence/r28-welle5-2026-11-22/guided-fixture-footprint-contract-divergence-0428-241/1788-into-1783-stacked-merge-round-1.md`

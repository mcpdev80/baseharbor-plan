# PR #1797 post-merge review record

## PLAN — PR #1797

- 335. Read #1797 review contract and create the numbered plan in the board and Planning evidence.
- 336. Resolve GitHub remotes and verify live PR, source head, base, merged squash, develop and exact hosted run.
- 337. Verify the exact four-file diff, catalog parity, workflow exclusion and release requirements unchanged.
- 338. Inspect deferred classification, executed claims, fail-closed behavior, MCP behavior and regression tests.
- 339. Verify release-only executor citations against the workflow, suite and MCP test runner.
- 340. Confirm selected checks and other required jobs ran on the exact candidate and classify any skipped/advisory jobs.
- 341. Record post-merge verdict, remote merge/develop witnesses, cleanliness and findings; do not change coordinator-owned Planning status.
- 342. Validate and publish the evidence, update the board and post the final END with merge SHA or repair recipe.

## Review identity and remote provenance

- ROLLE: REVIEW; independent review of the merged candidate, not an implementation task.
- Mission: `/tmp/opencode/m_rev_1797.md.g`.
- PR: https://github.com/mcpdev80/baseharbor/pull/1797
- PR source head: `ef1b35dc875bd65c7dfb2de53541b0fe5c0ca12f`.
- PR base: `develop` at `b3df96348a9c56de00d67a060c9a5f0ddf6593d5`.
- Squash merge SHA: `826d498fc1ae9524112d07477a8809798d8272a7`.
- Product Git remote verification: `origin` and `lane-origin` resolve to `https://github.com/mcpdev80/baseharbor.git`; remote facts below were read from that URL / GitHub API.
- Planning remote verification before the first evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Live `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1797/head` output:

```text
826d498fc1ae9524112d07477a8809798d8272a7 refs/heads/develop
ef1b35dc875bd65c7dfb2de53541b0fe5c0ca12f refs/pull/1797/head
```

- GitHub PR API: state `closed`, `merged_at=2026-11-23T07:58:32Z`, base `b3df96348a9c56de00d67a060c9a5f0ddf6593d5`, head `ef1b35dc875bd65c7dfb2de53541b0fe5c0ca12f`, merge commit `826d498fc1ae9524112d07477a8809798d8272a7`.
- Squash commit parents: `b3df96348a9c56de00d67a060c9a5f0ddf6593d5`. The current live `develop` ref equals the squash merge SHA.
- Planning card `t-20261121-static-gate-registration` is in `review`, depends on accepted `t-20261122-gate-catalog-missing-app-broker-component`. This review records the verdict only; no Planning status was changed.

## Exact diff and unchanged inputs

The PR and squash commit contain exactly these four paths:

- `scripts/pr-required-final.py`
- `scripts/pr-stage-boundary.py`
- `scripts/test_pr_required_final.py`
- `scripts/test_pr_stage_boundary.py`

GitHub compare from base `b3df96348a9c56de00d67a060c9a5f0ddf6593d5` to squash `826d498fc1ae9524112d07477a8809798d8272a7` reports `ahead_by=1`, `behind_by=0`, status `ahead`, and exactly those four files. No catalog or `.github/**` path changed.

Blob identities at base and squash are identical:

- `scripts/pr-gate-coverage.json`: `64f64f9d18ae5966ed380992af1c57e583c36031` at both refs.
- `scripts/release-requirements.json`: `c88040036115e1e4a5cf36dfbec9027f9b28631c` at both refs.

The v0.4.28 `atomic/static/mcp` carry remains in `scripts/release-requirements.json` (`required_for` includes v0.4.28 at lines 52–65). No release requirement was removed by this PR.

## Deferred classification and regression review

- `scripts/pr-required-final.py:54-65` permits `atomic/static/shell-ux`, `atomic/static/ci-fast-check`, and `atomic/static/mcp` as deferred entries. `:66-68` rejects any unknown deferred ID.
- `scripts/pr-stage-boundary.py:18-22` classifies those three IDs as deferred. `:34` sets `ATOMIC_STATIC_PR_EXECUTED_GATES = ()`; the stage function moves deferred IDs out of `selected_gates` and records them separately.
- `scripts/test_pr_required_final.py:168-203` asserts shell-ux and ci-fast-check are deferred, no `pr_focused` executor is needed for those IDs, normal required jobs still fail closed, and an unknown deferred/static gate is rejected.
- `scripts/test_pr_stage_boundary.py:54-77,110-129` asserts shell-ux/ci-fast-check are deferred, native gates stay selected, and unknown static gates raise. `:110-124` also asserts MCP stays deferred.
- `scripts/test_pr_required_final.py:137-166` and `scripts/test_pr_stage_boundary.py:89-108` preserve MCP deferral and the failure behavior of PR-executed checks. The MCP classification did not become a PR execution claim.

## Release executor citation check and finding

The required MCP citation is accurate: `.github/workflows/pre-release.yml:663-681` dispatches `static_gates` to `.github/workflows/pre-release-runtime-suite.yml`; suite lines `264-271` include `GATE=mcp` mapped to `tests/mcp/run.sh` at line 267. `scripts/release-requirements.json:52-65` still requires MCP for v0.4.28.

Blocking post-merge finding: the changed code also calls `atomic/static/ci-fast-check` a release-only deferred gate and claims an executor at `scripts/pr-required-final.py:56-64` and `scripts/pr-stage-boundary.py:23-34`. That executor is not present in the cited release path:

- `.github/workflows/pre-release-runtime-suite.yml:264-271` supports `config-matrix`, `init`, `mcp`, `agent`, and `shell-ux`; the default branch rejects other static gate names. There is no `ci-fast-check` case.
- `scripts/pre-release-check-plan.py:7` enumerates static release gates as `config-matrix`, `init`, `mcp`, `agent`, and `shell-ux`; it does not select `ci-fast-check`.
- `scripts/release-requirements.json` has no `atomic/static/ci-fast-check` entry. Its shell-ux gate is required only through v0.4.27 (lines 91–103), not v0.4.28.
- The unchanged PR coverage catalog lists `atomic/static/shell-ux` with `scope: pr` and maps `source.gate.atomic.static.ci.fast.check` to it at `scripts/pr-gate-coverage.json:2166-2175`.

Therefore this change removes the PR execution classification for ci-fast-check but there is no v0.4.28 release executor to take its place. The comments state a route that the current release workflow cannot execute. The PR's classifier regression tests pass, but they do not execute `scripts/ci-fast-check.sh` as a release gate. This fails the requested correctness of the release-only executor citation and leaves the card's gate registration unresolved.

Coordinator follow-up: register `ci-fast-check` in the v0.4.28 release gate catalog and release selector, and add its runtime-suite invocation, or do not classify it as release-only until that route exists. The runtime-suite and release workflow files are `.github/**` owner scope and were not edited in this review.

## Exact-head hosted evidence

- Run: https://github.com/mcpdev80/baseharbor/actions/runs/45134308709
- Run `45134308709`: event `pull_request`, candidate head `ef1b35dc875bd65c7dfb2de53541b0fe5c0ca12f`, base `b3df96348a9c56de00d67a060c9a5f0ddf6593d5`, terminal `completed / success`.
- `PR · Trusted Plan`: job `137556799484`, completed / success.
- `PR · Validation · ci-executor-tests`: job `137556874352`, completed / success.
- `PR · Validation · pr-planner-tests`: job `137556874516`, completed / success.
- `PR Selected Checks`: job `137557616284`, completed / success, GitHub Actions integration app ID `15368`.
- `PR · Focused Python`: job `137556874225`, completed / success. `PR · Candidate-added checks (advisory)`: job `137556874204`, completed / success; advisory only.
- Release-only jobs and unrelated native/runtime jobs were skipped by plan. Skipped jobs were not treated as successful proof. The three named required checks above executed and passed on the exact PR head/base.
- No rerun or workflow dispatch was triggered.

## Cleanliness

- Before review, `docker ps -a` returned only the header; PID `464318`.
- After review, `docker ps -a` returned only the header; PID `649518`.
- No containers or compose projects were started.

## Repo-rule compliance

- Review used GitHub API and `git ls-remote` against the resolved GitHub URL; no quarantined stale-ref checkout was used.
- No product files, workflows, branches, PR metadata, or Planning task status were changed. No local tests were run.
- Evidence is stored only in `baseharbor-plan/evidence/r28-welle5-2026-11-23/sweep-1797/review-merge.md` and contains no Markdown checkboxes.

## Wörtliches Verdict and END

- VERDICT: REQUEST CHANGES — post-merge acceptance of PR #1797 is not granted because `ci-fast-check` is classified as release-only without an executable v0.4.28 release route. The squash merge already exists remotely at `826d498fc1ae9524112d07477a8809798d8272a7`; no new merge was attempted.
- END BLOCKED codex-rev-1747: report the missing release executor and implement the coordinator-owned v0.4.28 gate registration before accepting card 0428-208. Merged candidate SHA `826d498fc1ae9524112d07477a8809798d8272a7`.

## Planning publication witness

Exact output from the required origin/main tree check before the final evidence push:

evidence/r28-welle5-2026-11-23/sweep-1797/review-merge.md

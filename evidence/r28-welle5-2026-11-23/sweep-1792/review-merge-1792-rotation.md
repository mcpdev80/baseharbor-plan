# PR #1792 review and merge — rotation review

## PLAN

1. Read the mission and verify task authority, scope, acceptance criteria, and evidence path.
2. Refresh Planning state and verify GitHub remote, exact candidate, base, and provenance.
3. Review the exact candidate and every required CI or native-gate receipt.
4. Perform only the mission-authorized review or merge action and record exact evidence.
5. Publish the evidence, validate Planning, update the live board, verify remote witnesses, and post the handoff.

## Role, authorization, and session

ROLE LABELS: ROLLE: REVIEW, followed by ROLLE: MERGE under the Owner instruction in mission `/tmp/opencode/m_rev_1792b.md.g`: “execute rotation now ... APPROVE then merge.” This is a separate Codex review session from the earlier review by codex-rev-1747. Verdict and acceptance are Owner-authorized; this record does not claim a GitHub review submission.

Session/lane: `codex-rev2-1736`. Model: GPT-6.2-Sol. Backend/session identifier: not exposed in this interface. Review time: 2026-11-23 03:24 UTC. Merge verified: 2026-11-23 03:26 UTC.

Planning remote was verified before the first evidence commit. Exact `git -C baseharbor-plan remote -v` output:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

The product checkout's first explicit Git action was `git remote -v`; its GitHub remote `lane-origin` resolves to `https://github.com/mcpdev80/baseharbor.git`. All product remote facts below were checked against that GitHub URL through `git ls-remote` or GitHub APIs.

## Candidate, provenance, and scope

PR #1792 was open, ready (`draft: false`), clean/mergeable, and targeted `develop`. Before merge, the exact refs were:

```text
1b7598aef8c4cae33b77c8523872637090d0f2bf refs/heads/develop
a2bbeaefb34583f0a5d6c1b8483e8350169d516e refs/heads/lane-0428-ingress-061-source-pull
a2bbeaefb34583f0a5d6c1b8483e8350169d516e refs/pull/1792/head
```

GitHub Compare from exact base `1b7598aef8c4cae33b77c8523872637090d0f2bf` to candidate `a2bbeaefb34583f0a5d6c1b8483e8350169d516e` reported merge base equal to the base, `ahead_by: 2`, `behind_by: 0`. The two commits are the catalog commit `59b5960694d5945583675ec1efb104325199edfa` and the additive merge commit `a2bbeaefb34583f0a5d6c1b8483e8350169d516e`, whose second parent is exact develop. No unrelated candidate commit is present. The compare's complete changed-file list is exactly:

```text
scripts/pr-gate-coverage.json
```

The PR changes this file by +62/-0 only. No product content file, `.github/**` workflow, or release field is changed.

The nine registered source/test paths are also present in the dependent source PR #1752 diff from its exact base `e8acf740553f7218b259f4855f5b79f83f21ab6b` to head `63b30d543b819d08962cba45b96fe42ac9c82291`. Their absence from current develop is expected for this forward-ingress PR: #1792 publishes the catalog rows before #1752 can be hopped and validated against them. The trusted coverage validator checks catalog schema/ownership and gate IDs; it does not require every forward row's file to exist in the current base.

## Catalog review

I fetched the catalog JSON at the exact base and PR head through GitHub's Contents API and compared the component arrays. Release remains `v0.4.27`; components change from 219 to 228. The delta is exactly nine added rows, zero removed rows, zero modified rows, zero duplicate IDs, and zero duplicate paths.

The rows and intended gate surfaces are:

- `cmd/baha/app_pull.go`, `cmd/baha/app_pull_render.go`, `cmd/baha/app_pull_options_test.go`, and `cmd/baha/app_pull_mcp_approval_regression_test.go`: atomic Docker and Podman data-capabilities.
- `cmd/baha/mcp_lifecycle_extra.go`: `gate.mcp`, with `runtime_specific: true`.
- `internal/development/source.go`, `internal/development/source_pull.go`, `internal/development/source_pull_test.go`, and `internal/machine/contract.go`: atomic Docker and Podman observability, with `runtime_specific: true`.

The gate IDs/surfaces exist in the trusted base release catalog. The base planner uses component `surfaces` to resolve the selected runtime gates; the new rows therefore route those nine changed paths in #1752 to the declared gates. This PR itself changes no source path, so the exact run appropriately skips unaffected native runtime cells.

Independent read-only consistency check of the head JSON against the trusted base release requirements: release `v0.4.27` is accepted; every added row surface is declared; all nine rows resolve to known focused release gates; no unknown gate IDs were found. The four app-pull rows resolve to `atomic/docker/data-capabilities` and `atomic/podman/data-capabilities`; the MCP lifecycle row resolves to `atomic/static/mcp`; and the four development/source/machine rows resolve to Docker and Podman observability. This was data inspection only, not a local product test or claim that a native runtime job ran in this catalog-only PR.

## Mission's Owner rulings — verbatim

1. “'PR · Candidate-added checks' ist ein ADVISORY-job; sein ausgabe-text 'No candidate-added validation checks. The trusted base plan remains the only merge requirement.' erklaert das fehlen neuer candidate-checks selbst als nicht-blockierend.”
2. “OWNER-SETZUNG 2026-11-23: kein workflow-gate allein weil das advisory keine candidates meldet; keine workflow-aenderung (owner-scope, nicht required).”
3. “PRAEDENZ: #1790 (gleiche forward-ingress-struktur, develop-only rows) wurde exact-head approved + gemergt als c6a7138ce (akte review-merge-1790 / 1450-sitz selbst).”
4. “die erste sitzung (codex-rev-1747) blockierte ausschliesslich aus genau diesem advisory-befund (akte f5cc090d) — kontradiktion zu (1)-(3).”

## Exact-head CI

Run `45103750422` is a `pull_request` run, `completed/success`, attempt 1, on exact head `a2bbeaefb34583f0a5d6c1b8483e8350169d516e`, with trusted base `1b7598aef8c4cae33b77c8523872637090d0f2bf`.

- `PR Selected Checks`, job `137460729501`, GitHub Actions integration `15368`: completed/success. Terminal log: `2026-11-23T03:05:57.6931291Z PR Selected Checks: PASS`.
- `PR · Trusted Plan`, job `137460226708`: completed/success.
- `PR · Native gate plan`, job `137460226892`: completed/success.
- `PR · Source format`, job `137460226811`: completed/success.
- `PR · Focused Python`, job `137460293022`: completed/success.
- `PR · Validation · ci-executor-tests`, job `137460293142`: completed/success.
- `PR · Validation · ci-policy`, job `137460293173`: completed/success. Its log reports `Gate catalog consistency PASS: no check-file or gate-ID additions/removals.`
- `PR · Validation · receipt-execution-tests`, job `137460293185`: completed/success.
- `PR · Validation · pr-planner-tests`, job `137460293222`: completed/success.
- `PR · Candidate-added checks (advisory)`, job `137460293078`: completed/success, with exact output `No candidate-added validation checks. The trusted base plan remains the only merge requirement.` This is advisory and not a required check.

Other release, Go-unit and native-runtime jobs were skipped because this PR changes only the catalog; those skipped jobs are not counted as passes. No required check was skipped, queued, or failed. No new test was added or changed in this catalog-only PR.

## Precedent and prior review discrepancy

Fresh GitHub PR API state for #1790 confirms it is closed/merged as `c6a7138ce2bf7de88f45f2a68e5168c835601a16` at 2026-11-23T00:01:01Z. The prior Planning record `evidence/r28-welle5-2026-11-22/catalog-ingress/review-merge-1790.md` documents the same develop-only catalog-ingress pattern and normal merge. The earlier #1792 review `evidence/r28-welle5-2026-11-23/sweep-1792/review-merge-1792.md` blocked solely because the candidate-added advisory job said no candidate-added validations were selected and no hosted candidate-catalog validation ran. Under the four Owner rulings quoted above, that advisory output alone is not a merge blocker and does not authorize a workflow change. My independent catalog inspection found no separate defect.

## Rules, verdict, and merge

Live ruleset `25223521` (`develop - required checks`) was active and strict, required `PR Selected Checks` from integration `15368`, and listed no bypass actors. Ruleset `23754541` (`develop - integration branch`) was disabled. The required check passed on the exact head; the PR was clean, based on current develop, and had no review submissions or inline review comments. The merge used the normal squash method with expected-head guard `a2bbeaefb34583f0a5d6c1b8483e8350169d516e`; no bypass was used.

VERDICT: REVIEW APPROVE; MERGE DONE. GitHub returned `merged: true`, squash merge SHA `cd9cc4836a69815a6cdcf7079902bafe5be1e000`.

Fresh post-merge remote witness:

```text
cd9cc4836a69815a6cdcf7079902bafe5be1e000 refs/heads/develop
a2bbeaefb34583f0a5d6c1b8483e8350169d516e refs/pull/1792/head
```

GitHub PR API confirms `state: closed`, `merged: true`, merge commit `cd9cc4836a69815a6cdcf7079902bafe5be1e000`. The feature branch ref was absent from the post-merge `ls-remote` output; the PR head ref remains available for audit.

## Repo-rule compliance

Only this Planning evidence file and the required live worker board JSON were changed. No product source or `.github/**` file was edited. No workflow rerun, workflow dispatch, local product test, VM test, Docker/Podman container, or compose project was started. The only product-repository mutation was the mission-authorized normal squash merge with an expected-head guard. No subagents were used.

## cleanliness

This session did not capture `docker ps -a` before the merge; it started no containers or compose projects. After merge, `docker ps -a` (PID 3569457) printed only `CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES` and no containers.

## END

END_DONE codex-rev2-1736: APPROVE and squash-merged PR #1792 at `cd9cc4836a69815a6cdcf7079902bafe5be1e000`; exact candidate `a2bbeaefb34583f0a5d6c1b8483e8350169d516e`.

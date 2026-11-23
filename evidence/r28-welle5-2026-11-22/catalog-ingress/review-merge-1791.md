# REVIEW / MERGE: PR #1791 catalog ingress

Role: REVIEW, followed by the mission-authorized MERGE after approval. Task: `t-20261123-catalog-ingress-app-access` (0428-254). Mission: `/tmp/opencode/m_rev_1791.md.g`.

## PLAN

1. Read mission and required coordinator/repository policies; capture role, task contract, and evidence path.
2. Verify task ownership, exact remote candidate/base, changed-file scope, and provenance.
3. Review the exact candidate against acceptance criteria and inspect required hosted checks.
4. Write verdict and supporting evidence in baseharbor-plan; preserve unrelated work.
5. Publish evidence, update the live board, verify remote witnesses, and post the required handoff.

## Contract and review context

The task note was `t-20261123-catalog-ingress-app-access`, status ready, no dependencies. Its product write set is only `scripts/pr-gate-coverage.json`; scope is two rows for `cmd/baha/app_access.go` and `cmd/baha/app_access_test.go`, mapped to the atomic Docker and Podman data-capability surfaces. The coverage catalog release marker must remain `v0.4.27`. The task itself is in the v0.4.28 queue. No product implementation or workflow change is in scope.

The mission required REVIEW and authorized MERGE if the exact candidate passed. I read the coordinator COST_CONTROL.md and GITHUB_AUTHORITY.md, the planning repository AGENTS.md and WORKFLOW.md, the product AGENTS.md, and the task note. This was read-only review of the product candidate; no local product tests were run.

Session context: Codex, GPT-6; backend identifier is not surfaced in this session; timestamp 2026-11-23 01:07:51 UTC.

## Candidate and provenance

The product remote was verified first with `git remote -v` in the product checkout. Exact output:

```text
origin https://github.com/mcpdev80/baseharbor.git (fetch)
origin https://github.com/mcpdev80/baseharbor.git (push)
```

Remote truth was then read from GitHub APIs and `git ls-remote`, not from the quarantined shared product checkout.

Before merge, `develop` was `b9e69b14a7c8c7e1ccf9176b0762bacecdecee5` and PR #1791 head was `d3eed85ab96040c1f80b2132f8316879f31e1b26`. GitHub compare reported one commit ahead, zero behind, and merge base equal to the exact develop SHA. The compare listed exactly `scripts/pr-gate-coverage.json`, +17 and -0. The PR was open, ready, and mergeable; no review submissions or unresolved review threads were present.

The planning repository is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; before the first evidence commit, its `git remote -v` output was:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Acceptance mapping

1. Diff scope: PASS. GitHub compare reports one changed file, `scripts/pr-gate-coverage.json`, +17/-0. No existing row is reported changed.
2. Base paths: PASS. GitHub fetches at base `b9e69b14a7c8c7e1ccf9176b0762bacecdecee5` found both `cmd/baha/app_access.go` and `cmd/baha/app_access_test.go`.
3. Rows and uniqueness: PASS. Comparing the base and candidate catalog found exactly two added component rows and no duplicate component IDs or paths (0 duplicate IDs, 0 duplicate paths). The release marker remains `v0.4.27`. The source row maps to both `source.gate.atomic.docker.data.capabilities` and `source.gate.atomic.podman.data.capabilities`. The test row has `runtime_specific: true` and maps to those same two surfaces. The test-row naming matches the `cmd.baha.app.env.test.go` analogue. Catalog ownership resolves by exact `path`; the validator's missing-source diagnostic in the prior failure prints a derived example ID but does not require that derived spelling as the catalog ID.
4. #1620 coverage repair: PASS for the declared source mapping. In run `45090587243`, Trusted Plan job `137418995746` failed on both exact paths with `uncataloged source change, no declared runtime gate owner`: `cmd/baha/app_access.go` and `cmd/baha/app_access_test.go`. The candidate adds one path-matched row for each, with both required data-capability surfaces. The failure's suggested IDs were resolver-generated diagnostics; the catalog validator resolves an owner by the `path` field and then derives covered gates from `surfaces`.
5. Exact candidate run: PASS. Run `45091676596` is completed with conclusion SUCCESS for head `d3eed85ab96040c1f80b2132f8316879f31e1b26`. Its `PR Selected Checks` check completed SUCCESS from GitHub Actions integration `15368`, the active required-check context. `PR · Trusted Plan`, `PR · Native gate plan`, `PR · Source format`, `PR · Focused Python`, and validation jobs `ci-executor-tests`, `pr-planner-tests`, `ci-policy`, and `receipt-execution-tests` completed SUCCESS. Candidate-added checks completed SUCCESS but were advisory; their log says no candidate-added validation checks were selected.

Runtime jobs (`PR · Native · matrix`, targeted HA Docker/Podman, and other unrelated runtime/release jobs) were skipped for this catalog-only diff. They are not counted as passes. The Native gate plan job completed successfully; no product source path changed in this PR, so this run does not claim to have exercised the Docker or Podman data-capability runtime tests. The follow-up #1620 source PR must re-hop to the new develop tip and produce its own exact run as the task note specifies; this review did not trigger or claim that follow-up run.

Ruleset `25223521` (`develop - required checks`) was rechecked live: active, strict, requiring `PR Selected Checks` from integration `15368`, with no bypass actors. Ruleset `23754541` (`develop - integration branch`) was disabled. No CI or protection bypass was used.

## Verdict and merge

REVIEW: APPROVE. The catalog addition is within the exact write set, the two rows address both paths from the recorded #1620 Trusted Plan failure, and the exact candidate's required `PR Selected Checks` run succeeded.

The PR was merged using the normal squash method with expected head guard `d3eed85ab96040c1f80b2132f8316879f31e1b26`. GitHub returned `merged: true`, merge SHA `15c652136b0fce19dd0ae286b341b38cac3f7854`.

Post-merge GitHub PR state: closed and merged. Fresh remote witness:

```text
15c652136b0fce19dd0ae286b341b38cac3f7854 refs/heads/develop
d3eed85ab96040c1f80b2132f8316879f31e1b26 refs/pull/1791/head
```

The separate #1620 re-hop and exact-head run remain follow-up work; this does not change the verified merge result for #1791.

## Repo-rule compliance

Evidence is stored only in baseharbor-plan. Product files and `.github/**` were not edited by this review. No local product tests, workflow reruns, or VM tests were started. The PR was not modified except for the authorized merge. The planning card remains unaccepted; this evidence records review/merge only.

## cleanliness

`docker ps -a` before review showed only the header and no containers (shell PID 3082659). After merge it again showed only the header and no containers (shell PID 3082753). This session started no containers or compose projects. Existing unrelated untracked planning evidence was preserved.

## END

END_DONE codex-rev2-1736: APPROVE and squash-merged PR #1791; merge SHA `15c652136b0fce19dd0ae286b341b38cac3f7854`; exact-head run `45091676596` succeeded. The #1620 post-merge re-hop remains separate follow-up.

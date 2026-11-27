# PR #1863 preflight and pending dispositions

Date: 2026-11-27. This is a read-only disposition record. No product files, task notes, card fields, or workflow files were changed.

## Plan

- Read PR #1863, its exact pull request run and job log, the current develop tip, and the linked planning task.
- Classify the failure against the trusted-base catalog admission family.
- Record a forward-only hop recipe and the card-number/owner facts.
- Consolidate the three previously requested dispositions with their source witnesses.

## PR #1863 preflight

At review time, `mcpdev80/baseharbor#1863` was open at head `4160d53f736b3c978b1df028ff90cd2b7d033d49`, based on `develop`. Its changed files were `internal/stableid/lock_probe.go`, `internal/stableid/lock_probe_platform_test.go`, and `scripts/pr-gate-coverage.json`. Run `45913103879` was a completed `pull_request` run on that exact head and failed in `PR · Trusted Plan` (job `140225875004`); `PR · Native gate plan` passed, while downstream selected checks were skipped after trusted-plan resolution failed.

The failing step was `Resolve exact immutable PR inputs using trusted base policy`. Its log ended with:

```text
ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/stableid/lock_probe.go (id source.internal_stableid_lock_probe_go): add this source with its surfaces to scripts/pr-gate-coverage.json; internal/stableid/lock_probe_platform_test.go (id source.internal_stableid_lock_probe_platform_test_go): add this source with its surfaces to scripts/pr-gate-coverage.json
```

Classification: this is the same trusted-base catalog-admission failure family as the #136 prerequisite, because the trusted planner cannot admit source paths whose catalog rows are absent from its trusted base. The #1863 candidate's own `scripts/pr-gate-coverage.json` additions do not authorize those paths to the trusted planner for the same candidate. This is a concrete admission failure, not a test assertion failure or runner/environment failure. It is distinct from an `integration_sha_mismatch` transport failure; a hop alone cannot make candidate-side catalog rows part of the trusted base.

## Forward-only worker recipe

The latest observed `develop` tip was `6b51228455913a30024f73ec347da8caf4dfea83` at `2026-11-27T02:24:51Z`. This is a snapshot, not a future base instruction: immediately before transporting, the assigned lane must fetch and record the then-live `develop` SHA, and use an ordinary merge of that exact tip into the existing #1863 branch. Preserve the original branch and commits; no rebase, cherry-pick, branch recut, or force-push.

Expected conflict risk is high in `scripts/pr-gate-coverage.json`, a shared catalog file used by the trusted-baseline family; reconcile by stable source ID/path and retain all non-conflicting rows exactly once. Expect lower but non-zero overlap risk in the two `internal/stableid` files. Any conflict must preserve the existing fail-closed missing-toolchain behavior and both regression cases. Do not treat the hop itself as satisfying trusted-base admission: the required catalog rows must first be present in the trusted develop base through the existing baseline route.

After that prerequisite lands, the owning lane must obtain a fresh Hosted `pull_request` run on the final exact head. Required evidence includes: green `PR · Trusted Plan`; green `PR Selected Checks`; execution and success of the `internal/stableid` authority-package Go tests; and execution and success of both Docker and rootless-Podman data-capabilities runtime gates selected for the two catalogued source paths. A skipped required test or runtime gate is not a pass. Use the run census and logs to show each required job actually executed. No local test result qualifies this preflight.

## Planning card and owner

The PR body identifies existing task `t-20261125-hunt33-go-runtime-prereq`, card `0428-299`. On live Plan main `6b51228455913a30024f73ec347da8caf4dfea83`, that task is `tasks/t-20261125-hunt33-go-runtime-prereq.md`; its `prs` field includes `mcpdev80/baseharbor#1863`, its `owner` field is empty, and its blocker records the trusted-baseline dependency. The requested label `0428-335` does not match the PR body or the linked live task; no `0428-335` task was found in the live task path inventory. This note uses the requested evidence directory `0428-335` while recording the verified linked card as `0428-299`; reconcile the label through the Coordinator rather than silently changing the task.

## Consolidated pending dispositions

### Plan PR #136

Verdict: CHANGES; do not merge. Head `d2f043e2ef328d2e4cbc6e751b178134be627c1d` still has a successful run `45926771147`, but that run is on the old head and does not cure transport staleness. At the check, live Plan main was `6b51228455913a30024f73ec347da8caf4dfea83`; compare reported `diverged`, 55 ahead and 24 behind, with `mergeStateStatus=DIRTY` and `mergeable=CONFLICTING`. Required next action: the owning lane must ordinarily merge current `origin/main` into #136, resolve conflicts without dropping the 0428-359 trusted-catalog baseline or unrelated main content, then obtain a fresh successful Plan validation on the new exact head. The merge must wait for that new head and run.

### Qualification-workflow edit-set final review

Verdict: ACCEPT for the proposed edit set recorded in `evidence/2026-11-27/0428-249/qualification-workflow-integrity.md` (live blob `b17bd0f2412f0981d8aa88ea038b0b417b3f8719`; correction source commit `f25e06380b1be1e55d6ad6223ec7a635694facbd`). The corrected proposal resolves inputs to a full commit SHA, checks the checkout against that SHA, keys evidence jobs by SHA plus gate/runtime identity and run ID, keeps evidence runs non-cancelling, and specifies the four-way Podman `single_default_native` split. It includes the `ci.yml` / `PR Selected Checks` graph, file-and-line anchors for the listed evidence workflows, and reasoned exclusions. The worker authorization is explicitly tied to the named-card exception. This accepts the disposition/edit set only; it does not implement or qualify workflow changes.

### Demo PR #183 CI inclusion

Verdict: IN-SCOPE, limited to the purpose-bound test-only path already recorded in `evidence/2026-11-27/0428-284/pr183-ci-inclusion-disposition.md` (live blob `8ea878f2ac40b87a9a3c0cfff4551300331bd7a1`). That record ties the narrow test selection to existing card 0428-284 and the Owner's W34 authorization, while prohibiting product consent/auth changes and Core `ci.yml` changes. This is a scope classification, not qualification of PR #183 and not authorization for this lane to edit a workflow.

## Provenance

Planning repository remote: `origin https://github.com/mcpdev80/baseharbor-plan.git`. Evidence-file base: `6b51228455913a30024f73ec347da8caf4dfea83` from `origin/main`, confirmed against the GitHub remote before writing. Executing lane: `w255-0428-251-demo170codex`. Commit identity: `w255-0428-251-demo170codex <w255-0428-251-demo170codex@baseharbor.local>`. Commit invocation: `git -c user.name="w255-0428-251-demo170codex" -c user.email="w255-0428-251-demo170codex@baseharbor.local" commit -m "evidence: preflight #1863 and consolidate dispositions"`. Pre-push identity gate: `git show -s --format=%an HEAD` must print exactly `w255-0428-251-demo170codex`.

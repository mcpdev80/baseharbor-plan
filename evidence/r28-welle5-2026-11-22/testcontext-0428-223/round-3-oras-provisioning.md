# 0428-223 round 3 — ORAS provisioning lands, validate cell green at head 4bd779b1

Card: `t-20261121-develop-full-suite-red` (0428-223). Lane: `0428-223-testctx`.
PR: #1750 (draft, base develop). Branch: `lane-0428-223-testcontext-target`.
Rounds 1–2: `evidence/r28-welle4-2026-11-21/develop-full-suite-red/round-1-fix.md`,
`evidence/r28-welle5-2026-11-22/testcontext-0428-223/round-2-ci-diagnosis.md`.
Task: keep the PR green; no local test execution; no skips.

## PLAN

- Step 1: re-verify branch provenance (ls-remote, ancestry, own-commits-only log, write-set).
- Step 2: commit the ORAS provisioning change on the same branch (Owner task directive 2026-11-22: install/pin ORAS for this gate without skipping or weakening tests), push, ls-remote delivery witness.
- Step 3: start and watch the exact-head hosted runs to terminal (AGENTS 4.6); count step 14 (unit, the 14 mission names) and step 16 (selected runtime gate) from the per-job log with byte counts.
- Step 4: publish this act to baseharbor-plan origin/main with an ls-tree witness.
- Step 5: END with candidate SHA and run outcomes.

## 1. Branch provenance (remote truth, this session)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` ->
`origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push)` (planning repo confirmed).
Product remote in the worktree: `origin https://github.com/mcpdev80/baseharbor.git` (URL contains github.com/mcpdev80; used for every fetch/push/ls-remote below).

```
6209874428f08dc3e90d6e29a42b30683ce9932a  refs/heads/develop
4bd779b1501db00049c353b3865bd3ba75704aef  refs/heads/lane-0428-223-testcontext-target
4bd779b1501db00049c353b3865bd3ba75704aef  refs/pull/1750/head
```

- `git merge-base --is-ancestor origin/develop HEAD` (origin/develop fetched at
  6209874428f) => OK: the exact base head is an ancestor of the candidate.
- `git log --oneline origin/develop..HEAD` lists ONLY this lane's two commits:
  `4bd779b1 test(0428-223): provision the pinned ORAS inside the integration cell`
  `1588ee1b test(0428-223): isolate the leaked organization selection in test contexts`
  (single author `0428-223-testctx`). No foreign commit is carried.
- `git diff origin/develop...HEAD --name-only` (write-set, all test files under `cmd/baha/`):
  app_init_source_neutral_test.go, app_init_wizard_test.go, app_perses_host_containers_cli_test.go,
  app_perses_infra_dashboards_cli_test.go, application_lifecycle_lock_test.go,
  repository_up_init_test.go, runtime_integration_test_support_test.go, test_operator_context_test.go.
  No `.github/**`, no `scripts/**`, no product code, no TOML.

## 2. The ORAS provisioning change (4bd779b1)

Root cause (round-2 finding, confirmed by the run): the validate job's step 16
`Run runtime integration tests serially` (`.github/workflows/ci.yml:404` region,
Owner scope, untouched here) has no ORAS provisioning, while the production
bootstrap gate fails closed non-interactively (`cmd/baha/oras_setup.go:
ensureORASForCoreUp`), so the five selected runtime tests died at
`app_repository_integration_test.go:27` / `app_workload_integration_test.go:61/193/350/538`
with `prepare BaseHarbor integration trust plane: ORAS is required before Core setup`.

Fix inside this lane's test surface: `ensureRuntimeIntegrationTrustPlane`
(`cmd/baha/runtime_integration_test_support_test.go`) now calls
`provisionORASForIntegrationCell` once per process before provisioning anything:
`exec.LookPath` first (an operator's or a workflow step's install stays
authoritative), then `includeInstalledORASOnPath`, and only then the PRODUCTION
installer `installORAS` — the official ORAS release pinned to the product
constant `orasSetupVersion` (1.3.6), checksum-verified against the official
checksums file, installed to `~/.local/bin` and prepended to PATH by the same
code a consenting user triggers. The installer's refuse-to-overwrite guard is
kept. No test is skipped, deleted or weakened; the gate's fail-closed semantics
stay intact (a download/checksum failure is a real failure).

## 3. Hosted outcomes at exact head 4bd779b1 (Eigenes-Run-Pflicht)

Runs at this head, all started/observed by this session to terminal:

| run | event | outcome | meaning |
| --- | --- | --- | --- |
| 44972447675 | pull_request | completed failure | only red job: `PR · Draft Go · cli-3` (137054968702) — `context_terminal_test.go:467: zsh is required to run this wrapper path; install zsh in the owning CI cell: exec: "zsh": executable file not found in $PATH` (card 0428-228, Owner scope, quoted not fixed) |
| 44972454590 | workflow_dispatch | completed cancelled | cancelled by the dispatch of run 44973644884 (same-ref concurrency) |
| 44973644884 | workflow_dispatch | **completed success** | the exact-candidate qualification run |

Run 44973644884, `validate` job 137058691290 (log fetched via
`gh api /repos/mcpdev80/baseharbor/actions/jobs/137058691290/logs`, 136408 bytes):
- step 14 `Run unit and package tests` success — the 14 mission names (round-1 list) green.
- step 16 `Run runtime integration tests serially` success, receipt verbatim:
  `PASS: all six native runtime tests and both package teardowns` (02:13:17Z).
- `company-dev` count in the whole log: 0 (org-selection leak stays fixed).
- steps 1–20 + 37–41: success, none skipped.
- `gh run list --commit 4bd779b150…`: workflow_dispatch success is the terminal exact-head result; the pull_request run's only failure is the cli-3 zsh cell.

## 4. Scope notes

- `.github/**`, `scripts/**`, workflow files, tests and runner infrastructure untouched (zsh/ORAS cell provisioning in workflows remains cards 0428-228 / Owner).
- One candidate branch, one chain; PR #1750 remains draft=true (handoff move is the coordinator's after review).
- No local test execution in rounds 2–3 (hosted-only proof per Owner directive sha256 d65b09b8ffed); compile-only probes (build/vet/test-binary link + policy scripts) were used.

## repo-rule compliance

- Test-only change inside the card's write-set; hermetic guarantee documented where the code lives; provenance witnesses in §1; hosted receipts in §3; no skips/deletions/weakening (AGENTS: verbot enum substitution respected — the resolver still performs real target resolution).

## cleanliness

- This lane created no containers/networks/volumes/compose projects on this host in rounds 2–3. END-turn witness (`docker ps -a`, pid 1720099): only foreign stacks listed (`bh-itest-1c3f4e6d-…`, `bh-itest-7daed22f-…`, newest 2026-11-21 20:26 +0100), zero compose projects matching this lane; left untouched. Scratch confined to `/var/tmp/0428-223*`, deleted after this post.

END 0428-223-testctx DONE — candidate 4bd779b1501db00049c353b3865bd3ba75704aef; validate job 137058691290 (run 44973644884) completed/success with all 14 names green and the six-test runtime receipt `PASS: all six native runtime tests and both package teardowns`; remaining cli-3 zsh failure is Owner-scope environment (0428-228).

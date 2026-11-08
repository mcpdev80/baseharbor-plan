# CODEX-REVIEW 0427-160 — PR #1491

## PLAN

1. Read the card contract, PR round-2 evidence, and repository review/CI rules. DONE.
2. Verify the exact PR head, current develop ref, changed paths, and candidate ancestry. DONE.
3. Inspect the production status/list paths, regression tests, command registration, hosted run, and native-gate selector. DONE.
4. Record the review verdict and actionable correction recipe in this Planning evidence file. DONE.
5. Reconcile generated Planning projections, pass the Planning validator, publish the evidence on origin/main, and verify its remote tree entry.

## Review identity and candidate

- Role: CODEX-REVIEW.
- Task: t-20261108-bughunt-list-stale-after-kill, card 0427-160.
- PR: mcpdev80/baseharbor#1491, open, not merged.
- Exact PR head: 5753eebda8f0f6563f24c1f55d045b82b254a50e.
- Exact hosted run: 42513199890, pull_request, completed/success on head 5753eebda8f0f6563f24c1f55d045b82b254a50e.
- Current develop remote ref: 20902f0a6ab016fd8fe6a501751e1becc5f334dd (`git ls-remote` witness). PR API still reports base SHA 7af8d440e9a4dd1b633fdc44e4093109fe44ae37; compare says candidate is one commit ahead and four commits behind current develop, with merge base 7af8d440e9a4dd1b633fdc44e4093109fe44ae37. The candidate commit is the sole commit in current develop..PR-head. The supplied run is exact-head but predates this current develop tip; refresh the candidate onto current develop and obtain a terminal exact-head run before final acceptance/merge.
- Exact current PR diff is four files: cmd/baha/app_commands.go, cmd/baha/app_list_reconciliation_test.go, cmd/baha/app_observe.go, cmd/baha/app_status_ux_test.go. No machine-contract or workflow file changes.

## Verdict: KORREKTUR

The list/status presentation changes are in the requested display-layer scope, and the candidate's hosted run is terminal success. Two acceptance details remain unproved or incorrect: the SIGKILL status test does not exercise the production status collector or assert NOT APPLIED for a failed runtime unit, and the advertised `baha app prune` command is not registered by the CLI.

### Finding 1 — SIGKILL status behavior is not demonstrated as NOT APPLIED

`cmd/baha/app_status_ux_test.go:139-159` constructs an `application.StatusResult` with `State: "degraded"` and directly calls the renderer. It proves that the renderer prints DEGRADED plus rebuild/destroy hints; it does not simulate a failed Quadlet unit after SIGKILL, call the production status collector, or prove the acceptance behavior “failed unit = not applied.” The other test at lines 114-134 is likewise a renderer test with a fabricated `not_applied` result.

On the production path, `cmd/baha/app_status_collect.go:56-76` assigns `not_applied` only when `ExistingRuntimeFiles` returns `application.ErrRuntimeNotApplied`. If runtime files still exist after the unit fails, collection proceeds through the live runtime inspection path at lines 82-119; `collectWorkloadChecks` records an unsuccessful workload check at lines 528-553. The candidate delta changes only the actionable text in `app_observe.go`; it does not change this status-state decision. The current new regression therefore cannot establish the required SIGKILL result.

Correction recipe: add a production-path `baha app status`/collector regression using the SIGKILL-shaped fixture (runtime state retained, Quadlet unit failed and workload absent). Assert the exact accepted state and output, including the next action, and show the test fails before the fix. If the contract requires NOT APPLIED, make the production status decision map the failed unit to that state without misclassifying genuinely stopped or incompletely applied deployments. Keep the test in `cmd/baha` so the existing package CI executes it.

Stop criterion: the exact command/collector test must prove the failed-unit SIGKILL case returns NOT APPLIED and the actionable recovery command; it must also retain passing coverage for healthy/ready and intentionally stopped cases. A renderer-only `StatusResult` fixture does not satisfy this.

### Finding 2 — `baha app prune` is not a real command

`cmd/baha/app_commands.go:197` prints `baha app prune <name>`, and `cmd/baha/app_list_reconciliation_test.go:81-88` only asserts that this literal appears. The registered children in `cmd/baha/app.go:26-35` include no prune command; a repository search of the exact candidate finds no `app prune` implementation or registration. Thus the MISSING next-action is not executable as written.

Correction recipe: either implement and register the intended safe dangling-record prune command under the existing app command tree, or change the advice to an existing command only after verifying it can handle a deleted source repository without destructive side effects. Replace the string-presence-only assertion with a command-entry regression that invokes the advertised command/help path and proves the dangling record is actually handled.

Stop criterion: `baha app --help` must advertise the recommended command and the regression must execute that command successfully against the missing-source fixture; alternatively the displayed replacement must be an existing command and its behavior must be verified against that fixture. Do not approve advice merely because the test contains the same text.

## Hosted CI and native-skip calculation

Run 42513199890 is completed/success on the exact PR head. On that run, `PR Selected Checks` (128833528446), `PR · Validation · go-unit-tests` (128830557386), go-build (128830557256), go-vet (128830557201), cli-gofmt (128830557176), and native destroy retry Docker (128830538443) and Podman (128830538452) succeeded. The Keycloak/Core native matrix was skipped; skipped jobs are not counted as passing execution.

I independently recalculated the selection from the exact changed paths and workflow at this candidate:

- `ci.yml:416-445` runs the PR native-impact selector. Its conservative fallback checks `^cmd/baha/.*\.go$`; the four changed paths include Go files in cmd/baha, so the selector sets `required=true`. This selects the Docker and Podman native destroy-retry jobs, both of which actually passed on this run.
- `ci.yml:551-565` separately sets `owner_node_required` only when paths match the onboarding/operator/node and listed owner/node internals regex. None of the four changed files matches, so `owner_node_required=false`.
- `ci.yml:1042-1046` gates the Keycloak/Core matrix on `needs.pr_plan.outputs.owner_node_required == 'true'`; therefore that matrix is skipped by the workflow's explicit scope selector. This is an explained owner/node-only skip, not an omitted check for these display-layer paths.
- Test routing is durable: the selected `go-unit-tests` entry calls `scripts/pr-unit-database.sh` (`ci.yml:915`), and that script executes `go test ./... -count=1` (line 33). The new `cmd/baha` tests are discovered by that package-wide run on pull_request. They ran in run 42513199890, but their current assertions do not cover the two findings above.

## Planning validation

The first `scripts/plan.py check` found stale generated projections on main. `scripts/plan.py render` regenerated the derived outputs without changing task metadata. A concurrent main commit, `388dfd59d03304902e1b901180f941fca28210df`, then published current generated projections alongside its own task update; this review preserves that commit and does not stage its files. The current `scripts/plan.py check` completes with 0 errors and 3 dependency warnings.

## repo-rule compliance

- Review only: no product repository edits, no PR mutation, no workflow edits, and no CI rerun/dispatch.
- Candidate was read from the live PR ref and a fresh clone under `/tmp/opencode/0427-160-review-wt`; no quarantined worker checkout was used as remote evidence.
- Planning repository remote is `https://github.com/mcpdev80/baseharbor-plan.git`, verified with `git -C baseharbor-plan remote -v`; its top level is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`. After fetching concurrent main updates, the publication base is `388dfd59d03304902e1b901180f941fca28210df`; the evidence commit will be a descendant of that exact main head.
- Planning publication uses the authorized planning main workflow. No subagents were used.

## Planning remote witness

`git ls-remote origin main` returned exactly: `388dfd59d03304902e1b901180f941fca28210df	refs/heads/main`.

## END

END 0427-160-review: KORREKTUR — #1491 head 5753eebda8f0f6563f24c1f55d045b82b254a50e; `baha app prune` is not registered and the SIGKILL status acceptance lacks a production-path NOT APPLIED regression.

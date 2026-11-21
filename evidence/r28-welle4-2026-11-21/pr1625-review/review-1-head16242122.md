# PR #1625 review — head 16242122dbd7eca0c1e073bd50872416d2d55152

ROLE: CODEX-REVIEW, reviewer-only. Mission: `/var/tmp/rev-1625-r2.md`.

## PLAN

1. Read the r2 review contract and verify the stated PR head/run against authoritative remote evidence.
2. Inspect the candidate diff and trace credential authorization, fail-closed behavior, fixture boundary, CI shard selection, and docs audit evidence.
3. Write a SHA-specific verdict with actionable remediation into the assigned baseharbor-plan evidence path.
4. Run planning render/check, publish evidence to origin/main, verify the remote file, and report the terminal result.

## Remote candidate and provenance

Product remote evidence came from `https://github.com/mcpdev80/baseharbor.git`; the selected remote name in the inspected product worktree resolves to that GitHub URL. Planning worktree remote, verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.

Exact remote refs from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1625/head refs/heads/develop`:

```text
d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3 refs/heads/develop
16242122dbd7eca0c1e073bd50872416d2d55152 refs/pull/1625/head
```

Fetched with exact refspecs into `refs/review/pr1625` and `refs/review/develop`. `git rev-list --count refs/review/develop..refs/review/pr1625` returned `4`; reverse count returned `0`. `git merge-base --is-ancestor refs/review/develop refs/review/pr1625` succeeded.

`git diff --name-only refs/review/develop...refs/review/pr1625`:

```text
cmd/baha/app_export.go
cmd/baha/app_export_command_test.go
cmd/baha/commands.go
cmd/baha/machine_coverage.go
docs/cli/command-index.md
docs/de/cli/command-index.md
docs/de/reference/cli-machine-coverage.md
docs/reference/cli-machine-coverage.md
```

`git log --format='%h %p %an %cn %s' refs/review/develop..refs/review/pr1625`:

```text
16242122d c44735b99 0428-065-export Marcel Pfingstgräf fix(0428-065 r6): operator-auth fixture for export tests + DE docs literal
c44735b99 f8f842458 0428-065-export Marcel Pfingstgräf fmt(0428-065): gofmt app_export.go, machine_coverage.go after develop rebase
f8f842458 0643587cf Codex Marcel Pfingstgräf fix app export managed secret selection and reveal
0643587cf d1acf3f31 lv4-verify Marcel Pfingstgräf feat(0428-065): guided baha app export of selected local credentials
```

PR API state: #1625 OPEN, non-draft, `MERGEABLE`, `CLEAN`, base `develop`, head exactly `16242122dbd7eca0c1e073bd50872416d2d55152`.

## Security and fail-closed review

The CLI applies enforcement and membership context in `cmd/baha/main.go:144-155`, then tags the operation as a local invocation at `151-160`. `cmd/baha/app_context.go:124-135` sets the export boundary operation; registered/repository resolution calls `ensureOperatorAuthForBoundary` at `187-207` and `228-235`.

`cmd/baha/operator_auth_boundary.go:55-78` first requires managed-environment enforcement, accepts an existing verified principal, otherwise attempts `verifiedLocalWorkloadAuthority`, and then resolves configured OIDC/operator auth. Without saved/env configuration, `112-118` returns a configuration-required error for noninteractive/no-input operation and refuses piped input instead of silently prompting.

The local-runtime route in `cmd/baha/local_workload_authority.go:45-73` is limited to CLI/stdio local workload operations, excludes tenant and managed-Core contexts, requires the selected target to be local and unscoped, and refuses the shortcut when stored or env operator auth exists. It checks protected, non-symlink state directories and absent/incomplete installation records at `75-104`; it resolves a runtime and fails closed on resolver errors at `106-111`; then binds `CheckLocalRuntimeGrant` to the operation, environment, canonical application ID, Docker target binding, or Podman authority verification at `113-143`. No terminal is needed to fail closed: the noninteractive branches return errors rather than falling back.

In `cmd/baha/app_export.go:123-151`, explicit source choices are authorized before managed-secret availability probes; empty nonterminal selection fails at `153-168`. `authorizeExport` requires `authorizeHumanReveal` for `secrets/openbao` at `229-243`. Managed secret values are fetched only after human-reveal authorization at `325-357`; errors are redacted and retrieved byte slices are zeroed at `346-357`, with export entries also zeroed at `194` and `394-403`. Output prints only source names and a nonsecret completion message at `211-225` and `406-412`; password is read from a file/terminal and zeroed at `199-203` and `515-550`.

The no-operator negative case uses enforcement with no principal at `cmd/baha/app_export_command_test.go:293-315`, selects managed secrets and asserts rejection before the selection summary/backend. The positive command-path test uses `appExportFixtureContext`, a test-only verified principal and bounded membership provider at `353-377`; it does not alter production code. The fixture is explicitly non-human and the test comments retain the human-reveal check. The authorized-secret test verifies the managed sentinel is absent from stdout and ciphertext at `389-429`. I found no silent fallback or evidence that the fixture weakens the production boundary.

## Exact-head hosted CI and test-selection evidence

`gh run view 44940309428 --repo mcpdev80/baseharbor` reports event `pull_request`, head `16242122dbd7eca0c1e073bd50872416d2d55152`, `completed/success`. It has 41 jobs: 20 success, 21 skipped, 0 failure. Terminal aggregate job `PR Selected Checks`, job `136957229601`, completed success at 2026-11-21T19:24:41Z.

Per-job logs show these CLI shard summaries:

- `cli-0`, job `136955896940`: `PASS cli-0: 458 passed / 13 intentionally skipped / 471 discovered; CLI inventory total=1829`.
- `cli-2`, job `136955896931`: `PASS cli-2: 451 passed / 20 intentionally skipped / 471 discovered; CLI inventory total=1829`.
- `cli-3`, job `136955896999`: `PASS cli-3: 425 passed / 16 intentionally skipped / 441 discovered; CLI inventory total=1829`.

The target test names hash into those shards under `scripts/pr-go-unit-shard.py:60-82`: `TestAppExportCommandPathAssemblesProductionWiring` → cli-0; `TestAppExportFailsClosedWithoutSelection` → cli-2; `TestAppExportManagedSecretWithoutOperatorFailsClosed` → cli-3. The runner discovers names and runs the selected regular expression with `go test -count=1 -json`; it checks that all selected names emitted run events and ended passed or skipped (`scripts/pr-go-unit-shard.py:75-105`). The exact CLI jobs ran successfully, but their logs expose only aggregate counts. Searches of the three per-job logs yielded no target test names, per-test durations, or `no tests to run` text. Thus I cannot confirm from the required per-job logs that each target case was non-skipped and record its duration.

`scripts/pr-gate-coverage.json` contains no `app_export.go` or `app_export_command_test.go` component entry. The tests are dynamically selected from the complete `./cmd/baha` inventory and assigned by SHA-256 shard rule above, not by a specific coverage-JSON case entry. This makes their shard route durable but does not provide the requested per-case run/duration receipt.

Documentation audit did execute: `PR · Validation · documentation-audit`, job `136955897018`, completed success in this same exact-head run. Its log records EN/DE page coverage, technical integrity, local/remote/team workflow checks, six unit checks, navigation coverage, and all documentation-audit categories as PASS. This job covers all four changed documentation paths listed above; the docs check was not inferred from `go build`.

## Findings and remediation

1. REQUEST CHANGES — identity violation (card 0428-224). The candidate history has three authors: `lv4-verify`, `Codex`, and `0428-065-export`. Remedy: rewrite the PR range so every commit has the single lane author identity `0428-065-export`, preserving the reviewed tree changes; these commits carry no accepted SHA certificate, so author rewrite is permitted by the mission. Alternatively, record a reasoned owner exception for this candidate. Stop criterion: exact remote PR range contains one author identity or the owner exception is documented; then rerun exact-head required checks and re-review the new head.

2. REQUEST CHANGES — required per-case CI receipt is absent. The CLI jobs succeeded, and deterministic assignment maps the three cases to cli-0, cli-2, and cli-3, but the per-job logs omit successful test names and durations; the aggregate therefore cannot establish the mission's explicit non-skipped per-case proof. Remedy: obtain an authorized hosted-run receipt that exposes each target case's name, duration, and pass outcome in its job log. The current mission forbids changing `scripts/**` and `.github/**`, and this review did not modify them. Stop criterion: all three per-case records are present for the exact reviewed head and each is a pass (not skipped).

## Verdict

REQUEST CHANGES for head `16242122dbd7eca0c1e073bd50872416d2d55152`.

Run `44940309428` is terminal success on the exact head, with 20 successful jobs, 21 skipped jobs, 0 failures, and successful `PR Selected Checks`; however, that aggregate does not replace the missing per-case log evidence. The auth/data-flow review found no product security defect. Correct the three-author history and provide the required per-case hosted log receipts for the resulting exact head before requesting another review. No product changes, comments, pushes, or merge actions were made.

executed-in-shard: cli-0=no cli-2=no cli-3=no docs-audit=yes

## repo-rule compliance

Reviewer-only read. No local tests were run, no product files were changed, and no `.github/**`, `scripts/**`, `internal/operatorauth/**`, or `internal/serviceaccess/**` changes were made. Evidence is in the Planning repository worktree only.

## cleanliness

Docker inspection before: shell PID `3153141`; `docker ps -a` listed these pre-existing exited containers: `bh-itest-1c3f4e6d-12470-edit-runtime-integration-dev-api-1`, `bh-itest-7daed22f-28345-shared-openbao-1`, `bh-itest-7daed22f-28345-shared-openbao-member-1-1`, `bh-itest-7daed22f-28345-shared-postgres-init-1`, `bh-itest-7daed22f-28345-shared-postgres-1`, `bh-itest-7daed22f-28345-shared-postgres-member-1-1`, `bh-itest-7daed22f-28345-shared-postgres-admin-1`, and `bh-itest-7daed22f-28345-shared-openbao-admin-1`. All were exited before this review. No containers or compose projects were started or changed by this review. A second `docker ps -a` will be recorded after evidence publication.

END codex-rev-1747 BLOCKED — REQUEST CHANGES: author identity and per-case CI log proof remain outstanding; candidate `16242122dbd7eca0c1e073bd50872416d2d55152`.

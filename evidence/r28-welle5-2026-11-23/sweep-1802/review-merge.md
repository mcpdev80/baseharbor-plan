# PR #1802 exact-head review

Role: REVIEW. This is a read-only review; this session did not merge or change the PR.

## PLAN

1. Read mission payload, task contract, and H-P1 finding; record exact review scope.
2. Verify GitHub remotes, candidate/base refs, merge state, and compare diff.
3. Review usageError behavior, regression coverage, and exact-head hosted CI receipts.
4. Issue verdict and an actionable, bounded correction recipe if required.
5. Publish review evidence in baseharbor-plan and record cleanliness and remote witnesses.
6. Complete board and final publication witnesses, then post the required END status.

## Session identity

- Codeman session: `fecbada9-9fd8-4df4-9305-d49b53a6e7a7`, session name `codex-rev-1747`, mode `codex`.
- Displayed model: `GPT-6-Luna` (Codeman session listing, model source `screen`). The session listing does not expose a separate inference-backend identifier.
- Role: `REVIEW`; no subagents or other sessions were contacted.

## Task and remote state

The mission is `/tmp/opencode/m_rev_1802.md.g`; the planning task is `t-20261123-wizard-org-default-usageerror` / 0428-258. The task note and H-P1 finding identify F6: when an organization-default stack is absent from the effective catalog, `guidedStackProfile` should return the same user-facing `usageError` type as other wizard input errors, rather than a raw hard error.

The product `git remote -v` was checked before other Git operations. `lane-origin`, `origin`, and `upstream` resolve to `https://github.com/mcpdev80/baseharbor.git`; all remote-state checks here used that explicit GitHub URL. The Planning remote was verified before the first evidence commit as `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push.

Before-review `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1802/head` returned:

```text
ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb refs/heads/develop
027fb255a4396215760771729d265ebbc6f9020f refs/pull/1802/head
```

The PR API reports #1802 closed and merged at `2026-11-23T12:41:10Z`, merge commit `ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb`, candidate head `027fb255a4396215760771729d265ebbc6f9020f`, and base `afa064519a859fbfa6e171c749a911301b9522b7`. The merged `develop` ref is the merge commit. No merge action was taken in this review session.

The exact-base compare `afa064519a859fbfa6e171c749a911301b9522b7...027fb255a4396215760771729d265ebbc6f9020f` reports `status=ahead`, `ahead_by=3`, `behind_by=0`, and merge base equal to the exact base SHA. Its net file list is exactly:

- `cmd/baha/app_new_wizard.go` — 23 additions, 4 deletions.
- `cmd/baha/app_new_wizard_org_default_test.go` — 98 additions.

The PR files API gives the same two-path net diff. There is no net `scripts/pr-gate-coverage.json`, `.github/**`, or consent/fail-closed path change. The PR history includes a catalog commit, but its catalog row is already present on the exact base (`scripts/pr-gate-coverage.json`, source ID `source.cmd_baha_app_new_wizard_org_default_test_go`, path `cmd/baha/app_new_wizard_org_default_test.go`); the exact-base compare correctly excludes it from this PR's effective diff, consistent with the mission's #1803 note.

## Behavioral review

The production change adds `orgDefaultStackNotInCatalog` as a pure guard and changes the missing organization-default branch of `guidedStackProfile` to call `usageError`. Existing `appNewAbortOnEOF` returns non-EOF errors unchanged, so this typed usage error propagates out of the wizard.

The error class and process exit behavior match existing usage errors: `usageError` in `cmd/baha/commands.go:261-263` constructs `&cli.UsageError{Message: message, Hint: hint}` without formatting; `internal/cli/cli.go:39-46` defines the type and `ExitCode` at `:81-90` maps it to exit status 2; `cmd/baha/main.go:58-70` formats the error and exits with `cli.ExitCode(err)`. This preserves the expected usage-error path rather than raw runtime exit status 1.

However, `cmd/baha/app_new_wizard.go:508` passes `"organization default stack %q is not available in the effective stack catalog"` directly to `usageError` without substituting `name`. Since `usageError` stores its first argument verbatim, the actual displayed error contains the literal `%q`, not the configured stack name. The new `TestGuidedStackProfileOrgDefaultMissingStackUsageError` checks that the message is non-empty and that the error has the expected type, but it does not catch this formatting defect. This is a user-facing gap in the requested usage-error parity.

The other added cases cover a present organization default resolving successfully and the pure missing-stack guard. No consent or fail-closed behavior is weakened by the reviewed changes.

## Hosted CI and test receipts

The mission-named run is GitHub Actions run **#7503**, run ID `45173006468`, event `pull_request`, exact candidate head `027fb255a4396215760771729d265ebbc6f9020f`, terminal `completed / success`. The PR job log records `BASE_SHA=afa064519a859fbfa6e171c749a911301b9522b7`. The run had 37 jobs: 20 success, 17 skipped, 0 failed, 0 unfinished. Skipped jobs were not treated as passing required jobs; the terminal aggregate passed.

`PR Selected Checks` job `137699169109` completed success at `2026-11-23T12:40:50Z`; check metadata reports GitHub Actions app/integration `15368`. The relevant selected Docker runtime jobs and Go unit shards completed successfully.

The specifically requested `PR · Validation · wizard-app-new-tests` job `137687229454` is terminal success. Its log also prints the matched-test inventory. That validation selector is `^TestAppNewWizard`; the inventory includes existing `TestAppNewWizard...` tests but does not include the three new test names below. I do not treat that job by itself as execution evidence for those three new cases.

The actual new tests are covered by the same run's CLI unit shards. At candidate head, `scripts/pr-go-unit-shard.py` discovers `./cmd/baha` tests with `go test -list`, hashes each test name with SHA-256, uses the first eight digest bytes as a big-endian integer modulo four, runs the selected names, and fails if selected tests are missing, incomplete, or fail. Applying that exact mapping gives:

- `TestGuidedStackProfileOrgDefaultMissingStackUsageError` → `cli-1`, job `137687229419`; terminal receipt: `PASS cli-1: 448 passed / 10 intentionally skipped / 458 discovered; CLI inventory total=1900`.
- `TestGuidedStackProfileOrgDefaultPresentStackResolves` → `cli-2`, job `137687229477`; terminal receipt: `PASS cli-2: 464 passed / 24 intentionally skipped / 488 discovered; CLI inventory total=1900`.
- `TestOrgDefaultStackNotInCatalog` → `cli-3`, job `137687229407`; terminal receipt: `PASS cli-3: 447 passed / 17 intentionally skipped / 464 discovered; CLI inventory total=1900`.

These three test bodies contain no `t.Skip` path. The shard receipts plus the exact-name mapping therefore establish their execution on the exact candidate, despite the specialized wizard validation selector not listing them by name. The `wizard-app-new-tests` job itself was green as requested, while the general auto-discovered CLI shards provide the direct execution route for these newly named cases.

## Verdict and repair recipe

ROLE: REVIEW
VERDICT: REQUEST CHANGES

The candidate meets the two-file scope and has terminal exact-head CI, including the named green validation job and successful CLI shards for all three new tests. The remaining defect is the literal `%q` user-facing error message, so I cannot approve the candidate against the usageError-parity contract.

Repair recipe for a follow-up PR, since #1802 is already merged:

1. In `cmd/baha/app_new_wizard.go:508`, format the message with the actual `name` before passing it to `usageError`, for example `fmt.Sprintf("organization default stack %q is not available in the effective stack catalog", name)`. `fmt` is already used in this file.
2. In `cmd/baha/app_new_wizard_org_default_test.go`, strengthen `TestGuidedStackProfileOrgDefaultMissingStackUsageError` to assert that the message includes the injected name `ghost` and does not retain `%q`; keep the `*cli.UsageError` assertion and optionally assert `cli.ExitCode(err) == 2`.
3. Preserve package auto-discovery through the CLI unit shards. If the follow-up contract requires the specialized `wizard-app-new-tests` receipt to execute these exact new names too, extend its existing test-family selector and record the matching names in its hosted log; the current green job's selector does not include them.
4. Obtain terminal GitHub CI on the follow-up candidate's exact head and record the named test and required aggregate results. Do not mutate the already merged PR or workflow from this review session.

## Repository-rule compliance

- Review-only work. No product code, CI file, PR state, or Planning task status was changed; no merge, PR comment, rerun, or workflow dispatch was performed.
- No local tests were run. Only remote GitHub PR, compare, source, and completed workflow evidence was inspected.
- No subagents were used. The live board plan is being ticked separately.
- `python3 scripts/plan.py check` completed with 0 errors and 10 warnings about pre-existing accepted tasks whose dependencies are not accepted; no task metadata was changed here.

## Cleanliness

- Before review: PID `2315414`; `docker ps -a` printed only the header `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`, with no containers listed.
- After review: PID `2359097`; `docker ps -a` printed only the header `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`, with no containers listed.
- No container or compose project was started.

END_BLOCKED codex-rev-1747: REQUEST CHANGES for PR #1802 at `027fb255a4396215760771729d265ebbc6f9020f`; `usageError` is correctly typed with exit status 2, but its message contains an unformatted `%q` because the helper stores messages verbatim. The exact-head `wizard-app-new-tests` job and CLI shards passed; the fix requires a follow-up PR.

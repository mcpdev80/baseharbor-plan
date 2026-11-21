ROLLE: REVIEW

Verdikt: REQUEST CHANGES

Review metadata: session ID not exposed by this interface; model GPT-6; backend Codex API; review time 2026-11-21 08:27 UTC.

## PLAN

1. Read the mission and record this numbered review plan in the live board and evidence file.
2. Verify PR #1737 exact head, base, remote branch/PR refs, ancestry, and one-commit write-set.
3. Read the card, correction/rebase evidence, and prior review; inspect production-path and fixture behavior in the test diff.
4. Verify both authorization outcomes, the EOF regression path, and whether denial is exercised on the production uninstall path.
5. Inspect exact-head and old-head per-job CI logs, compare failure sets and byte counts, and assess the develop hop after #1615 merge.
6. Check protected paths and cleanliness; record verdict and actionable recipe, publish only this file, and verify evidence plus frozen head.

## Candidate and freeze

- PR: mcpdev80/baseharbor #1737, card t-20261121-trust-uninstall-false-green (0428-213).
- PR head before review: 3010b212c8afdd5aba454852e8443486224df541.
- PR base: lane-0428-198-cli-shard-operator-env at e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4.
- GitHub PR API: open, draft=false, updated_at=2026-11-21T08:03:46Z; head and base match the values above.
- Product remote first git action: `origin git@github.com:mcpdev80/baseharbor.git` for fetch and push, from `git -C workers/baseharbor remote -v`. All product ref truth below is from the GitHub HTTPS remote, not that checkout's refs.
- Exact remote refs:
  `3010b212c8afdd5aba454852e8443486224df541 refs/heads/lane-0428-213-trust-uninstall-false-green`
  `3010b212c8afdd5aba454852e8443486224df541 refs/pull/1737/head`
- GitHub compare e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4...3010b212c8afdd5aba454852e8443486224df541: `ahead_by=1`, `behind_by=0`, `merge_base=e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4`, status `ahead`. The owner commit d0399968c is not in this PR. The diff is exactly one file: `cmd/baha/trust_uninstall_test.go`.
- PR head after review: 3010b212c8afdd5aba454852e8443486224df541.
- PR head before/after review = 3010b212c8afdd5aba454852e8443486224df541/3010b212c8afdd5aba454852e8443486224df541.
- Read-only review. No product files changed.

## Contract and source path

The card requires the three EOF tests to pass only after reaching the prompt and seeing the clean-abort output and unchanged owned trust state. It separately requires a real anonymous denial and a stamped path that passes the production authorization boundary. The `trust.uninstall` command calls `authorizeCurrentMCPContext` at `cmd/baha/trust.go:180` before it reads the prompt. Production denial text at `internal/operatorauth/authorization.go:285` is `Managed-environment machine operations require an authenticated BaseHarbor operator.` (including the terminal period).

`cmd/baha/mcp.go:272-275` applies the package test seam when `operatorAuthTestContextAllowed(ctx)` is true and no principal exists. The existing `withoutOperatorAuthTestContext` implementation in `cmd/baha/app_init_wizard.go:29-31` sets the opt-out key; `operatorAuthTestContextAllowed` returns false only for that marked context. This distinction is essential: a bare `context.Background()` is not opt-out in this test binary.

The candidate updates its EOF paths to use the stamped operator fixture and to require nil error, `Host trust unchanged.`, and the owned `host-trust.json` still present. The three prompt EOF tests therefore retain the prompt-specific acceptance assertions; the prior review also confirmed their pre-fix gate failure on base 7db142852d22. But the exact-head CI cannot compile the test package, so these assertions have not executed in the hosted run reviewed here.

## Acceptance review

1. Rebase and write-set: PASS. The PR is a single commit over the stated base, with only `cmd/baha/trust_uninstall_test.go` changed. No forbidden production, `.github/**`, `scripts/**`, `internal/operatorauth/**`, `internal/identityprovider/**`, `internal/serviceaccess/**`, `internal/capability/perses_selection.go`, or `internal/observability/registry.go` path is in the diff.
2. EOF regressions: assertion shape remains directionally correct. Each named EOF test now requires nil error and clean-abort output; it also verifies the ownership record is unchanged. The stamped fixture is needed to get past the pre-prompt auth boundary. Hosted execution is BLOCKED by the compile error below, so this is not a passing test result.
3. Anonymous/stamped gate proof: NOT MET. The candidate declares `withoutOperatorAuthTestContext` again at `cmd/baha/trust_uninstall_test.go:42`, conflicting with the existing declaration at `cmd/baha/app_init_wizard.go:29`. The candidate implementation simply returns its input context, while the actual existing helper marks the opt-out. The test package fails to compile. If the duplicate were merely renamed, its no-op behavior would leave the opt-out unset; `cmd/baha/mcp.go:272-275` would then stamp the anonymous context with the package fixture. The anonymous case would no longer be an anonymous-denial test.
4. Verbatim message: NOT MET. At `cmd/baha/trust_uninstall_test.go:175`, `strings.Contains(anonErr.Error(), "Managed-environment machine operations require an authenticated BaseHarbor operator")` is a substring check, and omits the source's final period. A changed message with extra text after the expected phrase remains green. The test comment calls this exact, but the assertion does not pin the full production message.
5. CI route and exact-head result: the path is selected by the CLI unit group, but exact-head run 44883097577 did not execute test discovery. All four CLI shard jobs failed at compile time, and `PR · Validation · cli-vet` failed on the same duplicate declaration. `PR Selected Checks` ended failure (job 136782820626). `PR · Trusted Plan` and `PR · Native gate plan` succeeded. The relevant CLI jobs were executed but not successful; 20 skipped check-runs are path-filtered and do not substitute for these failures.

## CI logs and same-old-head comparison

Exact candidate run 44883097577 is a completed pull_request run on 3010b212c8afdd5aba454852e8443486224df541 (08:03:51Z–08:05:36Z). Individual job logs, not the aggregate, were inspected for the cause and first-level failure counts.

The exact-head retrieval byte counts are:

- `gh run view 44883097577 --repo mcpdev80/baseharbor --log`: 931164 stdout bytes.
- `gh run view 44883097577 --repo mcpdev80/baseharbor --log-failed`: 78491 stdout bytes.
- Per-job `gh run view --job <id> --log`: cli-0 job 136782530723 = 51499 bytes; cli-1 job 136782530719 = 51495 bytes; cli-2 job 136782530701 = 51499 bytes; cli-3 job 136782530757 = 51496 bytes; cli-vet job 136782530767 = 66191 bytes.

Each of the four exact-head CLI job logs contains the compiler error `cmd/baha/trust_uninstall_test.go:42:6: withoutOperatorAuthTestContext redeclared in this block`, followed by `cmd/baha/app_init_wizard.go:29:6: other declaration of withoutOperatorAuthTestContext`. Vet reports the same redeclaration. There are zero first-level `--- FAIL: Test...` names because test discovery/build stopped first. The named trust tests did not run.

Old-head comparison run 44878429408 is completed/failure on 8b38c4f88f3e72ed69b41715e9bfb2ec03894108. Its `gh run view --log`, `--log-failed`, and each `gh run view --job <id> --log` retrieval returned 0 stdout bytes in this environment. GitHub Actions per-job log API fallback returned cli-0 job 136768408639 = 26112 bytes, cli-1 job 136768408611 = 26116 bytes, cli-2 job 136768408603 = 26109 bytes, cli-3 job 136768408637 = 26108 bytes, and cli-vet job 136768408709 = 33652 bytes. All five old-head logs contain the same duplicate-helper compile error. This equality does not make the issue inherited from the base: the offending helper is in the PR test file on both candidate heads. The exact current diff itself introduces that conflicting declaration. As with the new run, no first-level test names executed on the old head.

## Develop hop and #1615 package route

YES: the Loki packages route that failed before the #1615 merge is green on the merged tree. PR #1615 merged at 2026-11-21T08:08:08Z as develop commit `9bd76324ec6d1364f512d718cb82f1fffc9105a4`. That merge commit and PR #1615 head `864c2da7319b0db9f8973f94cc690c9b87921660` have the same Git tree `f518de4e9acd3fcf80b67fc2b877d0ab1d1db4ed`. On run 44881285907 for that exact tree, `PR · Go unit · packages`, job 136776979823, completed success; the run's `PR Selected Checks` also completed success. The develop push runs 44883441208 and 44883440150 were Docker/Podman Core workflows only, so I do not describe either as a packages unit run.

PR #1737 remains based on the older lane head e45430f2f1b7, so it does not yet contain the merged #1615 tree. A future hop to develop 9bd76324ec6d removes this packages failure route, but it will not resolve the current test-file compile collision; the PR still needs that correction and a successful exact-head CLI gate.

## Findings and recipes

Finding 1 — duplicate and ineffective anonymous-context helper prevents compile and defeats the denial proof.

- File/change: `cmd/baha/trust_uninstall_test.go:32-44`. Remove the duplicate helper and call the existing opt-out helper from `cmd/baha/app_init_wizard.go:29-31` for the anonymous context. Do not only rename the duplicate: its current `return ctx` does not opt out, so the global test seam would stamp the context at `cmd/baha/mcp.go:272-275`.
- Test requirement: the package must compile; `TestTrustUninstallGateReachableInBothDirections` must show the stamped call reaches the abort path and the opt-out anonymous call returns the auth denial without a principal. The three EOF regressions must execute and retain the nil-error, `Host trust unchanged.`, and unchanged ownership-file checks. Hosted cli-0..cli-3 and cli-vet must complete successfully on the corrected exact head.
- Stop criterion: stop while any CLI shard or cli-vet reports a redeclaration, while anonymous context is stamped, or while the required EOF cases are not executed. Proceed only when terminal `PR Selected Checks` is success on the corrected exact head.

Finding 2 — denial text is checked as a substring, not verbatim.

- File/change: `cmd/baha/trust_uninstall_test.go:175`. Assert the complete classified machine-error message equals the production value including its terminal period, rather than using `strings.Contains` on `error.Error()`.
- Test requirement: demonstrate that changing or appending to the production denial text makes the anonymous denial assertion fail, and restoring the exact source text makes it pass. Keep the stamped success and anonymous missing-principal checks.
- Stop criterion: stop while a message mutation that appends text or changes punctuation remains green; accept this point only after exact-message mutation is red and restoration is green, with the test executed by the hosted CLI unit group.

No recipe is assigned to #1615: its packages job is successful on the exact merged tree. Keep the current aggregate marked failed until the candidate compile/assertion corrections produce a terminal successful required aggregate.

## Cleanliness

- Before review: PID 4027478; `docker ps -a` returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`), with no containers.
- After review: PID 4034018; `docker ps -a` returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`), with no containers. This review started no containers or compose projects.

## Review limits

No local tests were run. No workflow was edited or dispatched. No PR comment, merge, force-push, or close action was taken. Session ID is not exposed by this interface.

END REVIEW DONE — candidate SHA 3010b212c8afdd5aba454852e8443486224df541.

## Planning remote

Before the evidence commit, `git -C baseharbor-plan remote -v` showed `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push.

## origin/main publication witness

Exact output of `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep '^evidence/r28-welle4-2026-11-21/trust-uninstall-false-green/review-2.md$'`:

```text
evidence/r28-welle4-2026-11-21/trust-uninstall-false-green/review-2.md
```

# CODEX-REVIEW 0427-161 — PR #1485

## PLAN

1. Pin the live PR head and develop base; inspect the exact source and test delta.
2. Verify where EOF is handled in the uninstall reader and distinguish immediate EOF, partial input with EOF, and non-EOF read errors.
3. Verify the regression test is selected by hosted CI and inspect terminal status on the exact head.
4. Publish an SHA-specific verdict, correction recipe, and stop criterion in the Planning evidence.

## Candidate and provenance

Role: CODEX-REVIEW.

Repository: `mcpdev80/baseharbor`; PR [#1485](https://github.com/mcpdev80/baseharbor/pull/1485), task 0427-161.

Reviewed head: `4fcff755e20a72347c4019536710831fcdaaf5e6`.

Target branch `develop`: `cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c`. The `git merge-base --is-ancestor cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c 4fcff755e20a72347c4019536710831fcdaaf5e6` check returned 0. PR is open and GitHub reports mergeable.

The exact diff changes only `cmd/baha/trust.go` and `cmd/baha/trust_uninstall_test.go`.

## Findings

### 1. EOF guard is in the actual uninstall reader

At `cmd/baha/trust.go:198-210`, the `trustUninstallCommand` prompt reads from `guidedTrustInput` using `bufio.NewReader(...).ReadString('\n')` at line 203. The EOF guard at lines 204-206 is inside this uninstall prompt's reader branch, not merely in a shared helper. The install prompt has its separate guard at `cmd/baha/trust.go:352-359`.

### 2. Immediate EOF and non-EOF errors are fail-closed; partial affirmative EOF is not a clean cancel

With an empty reader, `ReadString` returns an empty response and `io.EOF`; the guard allows execution to continue, the empty answer fails the affirmative check at lines 207-210, prints `Host trust unchanged.`, and returns nil. The new `TestTrustUninstallPromptEOFAbortsCleanly` at `cmd/baha/trust_uninstall_test.go:120-141` exercises this immediate-EOF case and verifies the ownership record remains.

For a non-EOF read error, the condition at `trust.go:204-206` returns the error before reaching `uninstallManagedTrust` at line 213. This preserves fail-closed behavior, although this new test does not inject a non-EOF reader error.

There is a correctness gap for EOF accompanied by buffered affirmative text. `ReadString('\n')` can return both a partial response and `io.EOF` when input ends without a newline. The current guard ignores that EOF and then parses `response`; an unterminated `y` or `yes` passes the affirmative comparison at lines 207-208 and reaches `uninstallManagedTrust` at line 213. That contradicts the card's contract that EOF itself means a clean cancel with host trust unchanged. The added regression only uses `strings.NewReader("")`, so it cannot detect this case.

### 3. CI routing and exact-head result

Hosted run [42498653903](https://github.com/mcpdev80/baseharbor/actions/runs/42498653903) is terminal `success` on exact head `4fcff755e20a72347c4019536710831fcdaaf5e6`. `PR · Validation · go-unit-tests` and `PR Selected Checks` passed.

The test resides in `cmd/baha/trust_uninstall_test.go`, so package discovery in the `go-unit-tests` PR validation covers it: the job runs `scripts/pr-unit-database.sh`, which runs `go test ./... -count=1`. The workflow trigger for that validation is `pull_request`. The new immediate-EOF regression is therefore CI-captured; the partial-affirmative-EOF and non-EOF-error cases are not currently tested.

## VERDICT: REQUEST-CHANGES

The actual uninstall reader now handles immediate `io.EOF`, and the immediate-EOF regression is included in a green exact-head CI run. However, treating EOF as permission to process a partial affirmative response violates the card's clean-cancel contract. This leaves a fail-closed gap in the production uninstall path.

## Actionable correction recipe

1. In `cmd/baha/trust.go:203-210`, treat `errors.Is(err, io.EOF)` as cancellation before inspecting any bytes returned by `ReadString`: print `Host trust unchanged.` and return nil. Continue returning every non-EOF read error without calling `uninstallManagedTrust`.
2. Extend `cmd/baha/trust_uninstall_test.go` with an unterminated affirmative reader such as `strings.NewReader("yes")` and require nil error, `Host trust unchanged.`, and unchanged ownership state. Keep the existing empty-input EOF regression and add a custom non-EOF error reader to require that the error propagates and the ownership record remains unchanged.
3. Confirm these tests run in `go-unit-tests` on `pull_request` and observe the terminal result on the corrected exact head.

Stop criterion: EOF must never approve uninstall, whether the response buffer is empty or contains an unterminated affirmative token; no EOF or non-EOF read-failure case may mutate host trust. The exact-head hosted unit and selected checks must pass.

## Review integrity and Planning provenance

Read-only product review; no product source, tests, workflows, VM stacks, or CI runs were changed or started by this reviewer.

Planning repository: `https://github.com/mcpdev80/baseharbor-plan.git` (`origin` verified). Before publication, `git ls-remote origin refs/heads/main` returned:

```text
0272c4b0feee978d5537d5dd6b88b3db81901390	refs/heads/main
```

Planning validation: `python3 scripts/plan.py render && python3 scripts/plan.py check` completed with 0 errors and 4 dependency-state warnings, including this task's unmet app-new EOF prerequisite; rendering produced no additional changed files.

END_BLOCKED 0427-161-review — immediate EOF is covered, but an unterminated affirmative response with EOF can still uninstall trust.

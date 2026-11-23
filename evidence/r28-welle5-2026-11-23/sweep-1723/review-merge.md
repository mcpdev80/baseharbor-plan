# PR #1723 review and merge

Role: REVIEW, then MERGE only if all contract criteria pass.

## PLAN

- 366. Read the #1723 review contract and create the numbered plan in the live board and Planning evidence.
- 367. Resolve the GitHub remote and verify live PR head/base, exact pull_request run, develop, and merge state.
- 368. Verify the exact four-file diff against develop and prove the gate catalog is byte-identical.
- 369. Inspect .github exclusion, hosted execution of the named workload-port regression test, and fail-closed port binding behavior.
- 370. Merge normally only if every acceptance point passes; otherwise record an exact repair recipe and stop.
- 371. Verify remote outcome, record cleanliness, validate and publish evidence, update board, and post END.

## Remote and candidate witnesses

- Planning remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`; push URL resolves to the same GitHub repository.
- Product remote resolved from the active product checkout: `https://github.com/mcpdev80/baseharbor.git`. Remote witnesses below use this URL and GitHub API; the quarantined `workers/baseharbor` checkout was not used.
- PR #1723 is OPEN, not draft; source head `37ddf3bdca8a0115f5c57b93740a21c90e13ac62`; PR base SHA `a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d`.
- Current remote witness: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1723/head` returned:
  `304b3ad1d88647377ea647d0d94174bfc9298e14 refs/heads/develop`
  `37ddf3bdca8a0115f5c57b93740a21c90e13ac62 refs/pull/1723/head`
- Therefore the PR base is not the current develop tip. GitHub compare `a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d...304b3ad1d88647377ea647d0d94174bfc9298e14` reports current develop ahead by two commits: `c3e49f3cc1959db68d57e52db0408bd48a043292` and `304b3ad1d88647377ea647d0d94174bfc9298e14`.
- PR files metadata against its declared base matches the four requested paths exactly: `cmd/baha/app_apply.go`, `cmd/baha/app_workload_ports.go`, `cmd/baha/runtime.go`, and `cmd/baha/workload_port_local_regression_test.go`. There are 221 additions and one deletion. No `.github/**` path is present.

## Develop parity and code review

- The gate catalog is not byte-identical to current develop: GitHub blob SHA at develop `304b3ad1d88647377ea647d0d94174bfc9298e14` is `087041fdb8d94145b20e0b73dbfcc54708d50570`; at candidate `37ddf3bdca8a0115f5c57b93740a21c90e13ac62` it is `64f64f9d18ae5966ed380992af1c57e583c36031`.
- Semantic comparison shows current develop has exactly two component records absent at the candidate: `source.cmd_baha_app_new_wizard_test_go` and `source.cmd_baha_application_provider_preferences_go`; all other component records remain unchanged. The `schema`, `release`, `surfaces`, `packages`, `gates`, and `native_checks` sections match. These are develop-side changes after the PR's stale base, including the merge of #1800, not edits listed in this PR's file diff.
- Port parsing rejects missing, malformed, duplicate, and out-of-range selectors in `cmd/baha/app_workload_ports.go` and `cmd/baha/runtime.go`. Requested bindings are checked against the selected Compose variables and `portAvailable`; explicit conflicts return an error rather than silently replacing the operator value (`app_workload_ports.go` lines 351–364, 592–630, 720–728). `runtime.go` lines 432–437 treats any failed bind probe as unavailable; this fails closed and does not assume elevated privilege. The regression file adds malformed-input and duplicate-port assertions.

## Hosted run evidence

- Run `45147022935` is a terminal successful `pull_request` run on exact head `37ddf3bdca8a0115f5c57b93740a21c90e13ac62`. Trusted Plan job `137598718929` logs `BASE_SHA: a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d`, confirming it did not test against the current develop tip.
- Terminal `PR Selected Checks` job `137610849609` succeeded. Native Docker data-capabilities job `137598846805`, native Podman data-capabilities job `137598846879`, and the selected runtime jobs completed successfully. The ordinary Go package/CLI jobs also report success.
- The hosted logs do not contain the name `workload_port_local_regression_test.go` or any named test from that file (`TestParseRuntimeUpOptionsAcceptsWorkloadPort`, `TestExtractLocalWorkloadPortsFailsClosedMirrorsRemote`, `TestAppApplyRunAcceptsWorkloadPort`, and related tests). Thus the contract's required named hosted-log proof is absent, even though generic Go jobs succeeded; no local test was run to fill that gap.

## Review findings and repair recipe

- REQUEST CHANGES: the candidate's declared PR base and trusted run `BASE_SHA` are `a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d`, while current `develop` is `304b3ad1d88647377ea647d0d94174bfc9298e14`. The exact acceptance contract requires base equal to tip.
- Rebase or otherwise integrate the candidate onto current `develop` without force-pushing. Confirm the resulting gate-catalog blob is byte-identical to the then-current develop catalog and retain the four-file source diff.
- Ensure CI executes the named regression test from `cmd/baha/workload_port_local_regression_test.go` and leaves an inspectable hosted log naming the test. Generic package-job success without that named evidence does not satisfy this acceptance point.
- After correction, wait for a new terminal `pull_request` run and successful `PR Selected Checks` on the corrected exact head, then request another merge review. Do not merge the present candidate.

## Cleanliness

- `docker ps -a` before review, PID 1745541: only the header was returned; no containers listed.
- `docker ps -a` after review, PID 1751940: only the header was returned; no containers listed.
- No local tests were run and no containers or compose projects were started.

VERDICT: REQUEST CHANGES — do not merge PR #1723. Its base is behind current develop, the gate catalog is not byte-identical to develop, and the named regression test has no hosted-log witness.

END DONE codex-rev-1747: #1723 REQUEST CHANGES; rebase to current develop and provide named hosted test evidence; candidate `37ddf3bdca8a0115f5c57b93740a21c90e13ac62`; no merge SHA.

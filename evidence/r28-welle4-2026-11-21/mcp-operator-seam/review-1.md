ROLLE: REVIEW

Review metadata: session ID not exposed by this interface; model GPT-6; backend Codex API; review time 2026-11-21 07:32 UTC.

**Verdict: REQUEST CHANGES**

## PLAN

1. Read the mission and record this numbered review plan in the live board and evidence file.
2. Resolve GitHub remotes and verify PR #1741 head, base, branch refs, ancestry, and freeze before and after review.
3. Read card 0428-218, lane round-1 evidence, and the exact changed MCP test file.
4. Trace stamped and anonymous requests through the real MCP mutation handler and operator authorization gate.
5. Inspect exact-head hosted CI logs; classify cli-0 and packages failures using their failing lines and compare against the same base.
6. Check the write-set, path-filtered skipped cells, and host cleanliness; record verdict and actionable recipes, then publish only this evidence file.

## Candidate and freeze

- Candidate: mcpdev80/baseharbor PR #1741, card t-20261121-mcp-operator-seam-uncovered (0428-218).
- PR head before review: de4a45ec5ca6e5c064d991420c796162ee6c1494.
- PR base: lane-0428-198-cli-shard-operator-env at e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4.
- PR head after review: de4a45ec5ca6e5c064d991420c796162ee6c1494.
- Remote witness: e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4 refs/heads/lane-0428-198-cli-shard-operator-env; de4a45ec5ca6e5c064d991420c796162ee6c1494 refs/pull/1741/head.
- The branch ref and PR head resolve to the same SHA. The base is the exact merge ancestor; compare reports ahead_by=1, behind_by=0 and merge_base=e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4. PR is open, draft=false, mergeable=true, mergeable_state=unstable.
- Read-only review. No candidate changes were made.

## Contract and diff

The card requires an MCP mutation test to exercise the managed-environment refusal through the real `authorizeMCPOperation` path. The anonymous result must carry the exact denial message: “Managed-environment machine operations require an authenticated BaseHarbor operator”. The in-test stamped operator must pass the same mutation gate. The authorized scope for this candidate is the MCP test file; `cmd/baha/mcp.go` remains owned by 0428-204 / PR #1726.

The SHA-exact PR diff contains one added file: `cmd/baha/mcp_operator_seam_test.go` (+95 lines). It does not touch `.github/**`, `scripts/**`, `internal/operatorauth/**`, `internal/identityprovider/**`, `internal/serviceaccess/**`, `internal/capability/perses_selection.go`, or `internal/observability/registry.go`.

## Acceptance review

1. Reachability: PASS. `TestMCPOperatorSeamReachesGateBothDirections` creates a `prod` workspace fixture and calls `baseharbor.target.create` over `workspaceMutationClientWithContext` for both stamped and anonymous contexts. That helper connects an in-memory MCP server/session and invokes `CallTool`; this is the registered handler and transport path, not a direct authorization-helper call. The production handler calls `createTargetDefinition`, which calls `authorizeCurrentMCPContext`. With the `prod` manifest, the latter resolves the managed environment and proceeds to `authorizeMCPOperation`. The anonymous helper explicitly opts the context out of the test operator fixture; `PrincipalFromContext` is also checked to be empty.
2. Opposite outcomes: PASS. The stamped call must succeed; the anonymous call must be an MCP machine error with code `authentication_failed`, and the outputs must differ.
3. Exact gate message: NOT MET. At `cmd/baha/mcp_operator_seam_test.go:78-87`, the decoded payload includes only `error.code`; the test does not decode or assert `error.message`. The lane’s temporary debug output is not a committed regression assertion. The contract requires the literal gate text, so typed-code and output-difference assertions do not close this point.
4. CI routing for the test: PASS. The test name hashes to Go unit shard cli-3 under `scripts/pr-go-unit-shard.py`; exact-head run 44873244947 executed cli-3 successfully (job 136752270714).

## Hosted CI evidence

Exact-head run 44873244947 (`PR Selected Checks`) completed with failure. Its `PR Selected Checks` job 136753279732 failed. Go unit cli-0 job 136752270656 and packages job 136752270758 failed; cli-1, cli-2, cli-3, owner, go-build, go-vet, focused Python, Native gate plan, Trusted Plan, and applicable validation cells succeeded. Runtime/native cells omitted by the path gate were not required for this test-only Go diff. The aggregate remains a failure and is not represented as a pass.

The required aggregate and per-job `gh run view ... --log` and `--log-failed` retrievals returned empty output (0 bytes). GitHub Actions job-log API responses were therefore used for the individual job evidence. Candidate logs had 23,039 bytes for cli-0 and 34,612 bytes for packages. Same-base baseline run 44867737078, on the exact PR base SHA e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4, had corresponding cli-0 and packages failures (23,040 and 34,610 bytes).

Observed first-level failures in candidate logs:

- cli-0: `TestAppListAllTargetsWorksAfterInstallationDestroy`; `app_list_all_targets_test.go:26` reports that inventory depended on deleted Target config `docker-dev` and that configured `config.yaml` is missing. The same test and failure line occur in the same-base baseline. This is inherited from the base (0428-210 / PR #1739), not introduced by this MCP test.
- packages: `TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource` at `loki_test.go:522` and `TestPersesLokiDatasourceMultiSourcePartialMatchability` at `loki_test.go:586` both report missing `providers/loki/shared/service-access/pki/client-cert.pem`; `TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed` at `loki_test.go:633` reports 0 per-source queries where 2 were expected. The same three test names and corresponding failures occur in same-base run 44867737078. These are inherited from the base (0428-142 / PR #1702), not introduced by this MCP test.
- There were four first-level failing test names in each candidate and same-base run; no candidate-only or baseline-only failing test names were found in cli-0/packages. Thus the red `PR Selected Checks` state is justified as inherited failure evidence, while remaining a failed aggregate.

## Findings and recipes

Finding 1 — exact denial message is not pinned by the committed test.

- File: `cmd/baha/mcp_operator_seam_test.go:78-87`.
- Change: include `Message string` in the decoded `Error` shape and assert exact equality with `Managed-environment machine operations require an authenticated BaseHarbor operator` for the anonymous `prod` request. Keep the same MCP `CallTool` path and retain the stamped-success and anonymous-no-principal assertions.
- Test requirement: `TestMCPOperatorSeamReachesGateBothDirections` must fail if the production denial text changes or the anonymous request is diverted away from the operator gate; the real MCP test must run in cli-3 on hosted CI.
- Stop criterion: stop when the exact text, `authentication_failed` code, missing-principal condition, and stamped success are all asserted and the new exact-head required aggregate passes.

Finding 2 — exact-head required aggregate is failed, with red cells inherited from the base.

- State: run 44873244947 `PR Selected Checks` failed; cli-0 and packages failed with the lines recorded above. Same-base run 44867737078 has the same failure test names and messages. This is a state finding, not evidence that the candidate’s aggregate passed.
- Recipe: preserve these exact log-line comparisons and have the owners of 0428-210 / PR #1739 and 0428-142 / PR #1702 resolve the base failures. After the exact-message regression is added, require a new exact-head run and inspect its terminal `PR Selected Checks` result.
- Test requirement: cli-3 must execute the updated MCP test; required cli-0/packages jobs and the terminal aggregate must complete successfully on that exact head. Do not attribute same-base inherited failures to this candidate or treat them as green.
- Stop criterion: stop acceptance while `PR Selected Checks` is failed, skipped, or queued; proceed only after the required aggregate is completed/success on the final candidate SHA.

## Cleanliness

- Before review: PID 3822703; `docker ps -a` returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`), with no containers.
- After review: PID 3829305; `docker ps -a` returned only the header, with no containers.
- No containers or compose projects were started by this review.

## Review limits

The candidate was read only. No tests were run locally, no workflow was edited or dispatched, and no PR comment, merge, force-push, or close action was taken. Session ID is not exposed by this interface.

END REVIEW DONE — candidate SHA de4a45ec5ca6e5c064d991420c796162ee6c1494.

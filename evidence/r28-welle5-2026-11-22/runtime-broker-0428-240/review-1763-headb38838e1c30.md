# PR #1763 exact-head review

## PLAN

1. Read the #1763 CODEX-REVIEW contract and record its exact candidate, acceptance criteria, evidence path, and read-only boundaries.
2. Refresh PR #1763, develop, and exact-head CI receipts; inspect the two-file diff and diagnostics test read-only.
3. Evaluate the native-gate selection against the trusted coverage catalog and determine whether a catalog mapping is required.
4. Write and validate the SHA-specific verdict evidence, publish only that evidence to Planning origin/main, update the board, and post END.

## Scope

Read-only independent CODEX-REVIEW. No product changes, PR comments, merge, close, workflow reruns, or local product tests. Product remote was resolved as https://github.com/mcpdev80/baseharbor.git. Planning remote verification: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.

## Candidate and ancestry

PR #1763 is open, non-draft, and targets develop. Live GitHub refs: `8629450ef3c5198bb675331c12f56b2c9377aa1c refs/heads/develop`; `b38838e1c30d18eabe3fa7e8e64c6c053c576bce refs/pull/1763/head`. The PR API reports branch `lane-0428-240-broker-diagnostics`, base SHA `8629450ef3c5198bb675331c12f56b2c9377aa1c`, and two changed files: `cmd/baha/app_broker.go` and `cmd/baha/app_broker_diagnostics_test.go`.

## Security review

The candidate removes the old inline diagnostics branch and routes readiness timeout through `failRuntimeBrokerReadinessWith` at `cmd/baha/app_broker.go:200-231`. `runtimeBrokerReadinessDiagnostics` at lines 234-267 never appends raw log lines: it reports only a count and fixed redaction phrase at line 257, then emits dependency names from the fixed set `openbao`, `runtime-executor`, and `database` at lines 258-261. `logMentionsDependency` at lines 270-283 uses whole-token splitting and case-insensitive matching, so unrelated log values are not copied.

The mTLS `/readyz` call is at lines 315-337. Probe failures become a fixed phrase at line 323. Non-JSON bodies become only `body-length=<number>` at line 340. Parsed output is reduced to closed-set status and allowed dependency name at lines 342-346, plus strict character-class build tokens for version and commit at lines 348-353. The commit token is an additional bounded build identifier; arbitrary body fields and raw body text do not survive parsing. `truncateDiagnosticTail` is absent from the exact candidate file. The initial readiness failure is wrapped at line 230, but its health and malformed-body errors are fixed strings; no raw `/readyz` body is included in that error.

## Test and hosted CI review

`TestRuntimeBrokerReadinessDiagnosticsNeverEchoesValueMarker` is at `cmd/baha/app_broker_diagnostics_test.go:90-132`. It has four named cases at lines 102-106 and constructs the real `runtimeBrokerReadinessDiagnostics` output through a fake `RuntimeProvider`; it asserts `token=abc123` and `abc123` are absent at line 111, checks the safe `dependency=openbao` survives for the JSON case at lines 115-119, and requires a dependency signal or non-JSON length fallback at lines 121-123. This is a real assertion over the helper's returned diagnostic text, not a constant. The fixture is synthetic and does not exercise a real runtime/container or the production call path.

The exact-head run `45009251403` is terminal `completed / success`, event `pull_request`, head `b38838e1c30d18eabe3fa7e8e64c6c053c576bce`: https://github.com/mcpdev80/baseharbor/actions/runs/45009251403. `PR Selected Checks` is terminal success (job `137168689277`). `PR · Go unit · cli-0` is terminal success (job `137167723531`) and reports `PASS cli-0: 466 passed / 13 intentionally skipped / 479 discovered; CLI inventory total=1856`. In the candidate's `scripts/pr-go-unit-shard.py:28-40,64-115`, the CLI shard discovers all `Test`/`Example`/`Fuzz` names, deterministically hashes them into four shards, runs the selected names via `go test -run`, and fails if selected tests were not executed or passed. The marker test hashes to cli-0. Thus the test is selected by an executed hosted unit shard; the aggregate log does not print the individual test name.

## Native-gate coverage decision

Decision: (b), a native runtime mapping is needed. Although the marker regression is durably selected by the hosted CLI unit shard, it tests a fake provider and directly invokes the diagnostics helper. The changed production path at `cmd/baha/app_broker.go:183-204` is reached only after a real broker readiness timeout and then collects actual container logs plus an mTLS `/readyz` probe. No hosted job in this run executes that failure path against a runtime.

The trusted base catalog at develop SHA `8629450ef3c5198bb675331c12f56b2c9377aa1c`, `scripts/pr-gate-coverage.json`, has 190 component entries; 65 entries are under `cmd/baha`, and none names `app_broker` (zero matches). Required owner-scope catalog work is to add source components for `cmd/baha/app_broker.go` and `cmd/baha/app_broker_diagnostics_test.go` in the `components` array beginning at line 139, and associate the appropriate diagnostic runtime coverage with the Docker and Podman lifecycle native checks in `native_checks` beginning at line 2980 (existing coreless lifecycle source lists are around lines 3137-3156). The selected native scenario must actually exercise the unhealthy readiness diagnostic branch. This is a `scripts/**` owner-scope finding; I did not edit it.

The `PR · Native gate plan` job `137167667713` completed successfully but its log selected `matrix={"include":[]}` and warned that the base lacks the trusted native gate planner. The `PR · Native · ${{ matrix.id }}` job `137167703522` is skipped. A skipped native matrix is not evidence of runtime execution. No other failed required check was found in the exact-head run.

## Verdict

REQUEST CHANGES for exact head `b38838e1c30d18eabe3fa7e8e64c6c053c576bce`. The fail-closed diagnostic formatting and four-case marker assertion are sound, and the marker test is selected in the successful CLI shard, but the real runtime readiness-failure path has no selected hosted native execution because the trusted catalog does not map these source files. Add the owner-scope catalog mapping and a native scenario that exercises the failure path before approval. The skipped native job is explicitly not evidence.

## repo-rule compliance

This was a read-only review of the exact PR head. No product files, workflows, test VMs, or local product tests were touched. Only this Planning evidence file is intended for publication. The canonical Planning checkout was verified before commit and its remote URL is the `mcpdev80/baseharbor-plan` GitHub repository. `python3 scripts/plan.py check` completed with 0 errors and 10 existing dependency-order warnings.

## cleanliness

Before review, `docker ps -a --no-trunc` showed only the header and no containers; command was run in this session. This review started no container or compose project. A second witness ran with session shell pid 3603811 and again showed only the header and no containers: `docker ps -a --no-trunc`.

## END_BLOCKED

END_BLOCKED: review verdict is REQUEST CHANGES pending owner-scope native coverage catalog and runtime scenario work.

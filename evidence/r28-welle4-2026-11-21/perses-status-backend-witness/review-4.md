ROLLE: REVIEW

Session ID: not exposed by the active session interface
Model: GPT-6
Backend: Codex API session with shell and GitHub CLI
Review time: 2026-11-21 07:15 UTC

**Verdict: REQUEST CHANGES**

## PLAN

1. Read /var/tmp/rev1702.txt and register this numbered plan in the live board and evidence file.
2. Verify GitHub remotes, PR #1702 head/base, branch and exact-head checks; capture before/after freeze witnesses.
3. Read the task contract, prior verdicts, round-6 auth fixture evidence, and exact candidate diff.
4. Verify real transport path reachability, both auth-context directions, and M1/M2 mutation proof against source and tests.
5. Read all five exact-head Go-unit job logs; count unique failures and inspect the literal operator-auth gate line; assess write-set and cleanliness.
6. Write and publish only review-4.md to baseharbor-plan origin/main, then verify its published path and unchanged PR head.

## Candidate identity and freeze

Candidate: mcpdev80/baseharbor#1702, branch `lane-0428-142-statuswitness`.

PR API before review: head `b2f2fd3ac17293949c18223b55936e1018085472`, base develop `40cb28c758b02960356434b630086a341ebe1738`, open, draft=false, mergeable_state=blocked. Remote refs before review:

```text
40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop
b2f2fd3ac17293949c18223b55936e1018085472 refs/heads/lane-0428-142-statuswitness
b2f2fd3ac17293949c18223b55936e1018085472 refs/pull/1702/head
```

GitHub compare reports `40cb28c...b2f2fd3` as ahead by 5, behind by 0, merge base exactly `40cb28c758b02960356434b630086a341ebe1738`.

PR head before review = `b2f2fd3ac17293949c18223b55936e1018085472`
PR head after review = `b2f2fd3ac17293949c18223b55936e1018085472`

This was a read-only candidate review. No product, PR, workflow, or container state was changed.

## Contract and scope

Contract: `tasks/t-20261119-r28-perses-status-backend-witness.md` and the current card evidence `round-6-authfixture.md`, with the previous reviewer evidence `review-2.md` and `review-3.md` read for history. The contract requires a real per-backend status/source witness through the CLI, both human and machine faces, and executed tests for the witness cases. The current review specifically checks whether the auth-fixture correction makes the real command reach its renderer and whether the unauthenticated path remains fail-closed.

The exact PR file list is:

- `cmd/baha/app_status_result.go`
- `cmd/baha/app_status_result_test.go`
- `cmd/baha/perses_lifecycle.go`
- `cmd/baha/perses_lifecycle_transport_test.go`

All four paths are within the card's current scope. The diff does not touch `.github/**`, `scripts/**`, `internal/operatorauth/**`, `internal/identityprovider/**`, `internal/serviceaccess/**`, `internal/capability/perses_selection.go`, or `internal/observability/registry.go`. The earlier app_status_result.go ownership objection in `review-3.md` is superseded by the current card's explicit scope and its round-6 handoff; no write-set finding remains.

## P1 — authenticated positive transport path and mutation proof

The candidate does reach the production status command, not just the renderer helper. In `cmd/baha/perses_lifecycle.go:80-94`, the `perses status` command calls `reportPersesSurfaceStatus`, which authorizes at `:226-227`, builds the result at `:231-236`, and then calls `renderPersesBackendWitness` at `:93`. The test `TestPersesStatusWitnessHumanFaceRendersBackendWitness` invokes `persesRunWithIO` at `cmd/baha/app_status_result_test.go:301-330`; that dispatches `rootCommand().Execute` at `cmd/baha/perses_lifecycle_transport_test.go:404-420`, so it traverses the actual command tree and product authorization/rendering code.

The test fixture is installed after the production defaults in `persesMatrixCommandContext` (`perses_lifecycle_transport_test.go:371-401`): it installs enforcement at `:390`, membership at `:392-394`, verified principal at `:395`, consent at `:396`, and transport/workload scope at `:397-400`. This ordering avoids the documented `WithEnforcement` replacement problem. The coreless target fixture at `:328-338` selects the existing verified-local-runtime grant path. This is a test identity fixture at the invocation boundary; the test does not call `reportPersesSurfaceStatus` or `renderPersesBackendWitness` directly for the positive CLI assertion.

M1/M2 are supported by both the recorded mutation output in `round-6-authfixture.md` and the exact candidate source: M1 removes `renderPersesBackendWitness(out, result.BackendWitness)` at `perses_lifecycle.go:93`; the human CLI test asserts all three exact backend/source/state lines at `app_status_result_test.go:312-330`, so that mutation removes the expected product output. M2 changes the production derivation `persesBackendSignalWitnessFromManifest` at `app_status_result.go:100-173`; the command test and the state tests assert those derived results. The round-6 evidence records M1 failing the human CLI output assertion and M2 causing three witness cells to fail. These mutations target separate product behaviors (rendering versus state derivation); neither is a proof of the missing unauthenticated negative case below.

## P2 — missing Perses-specific negative auth-context direction

The positive command path is covered, but the candidate's changed tests contain no Perses status invocation under `withoutOperatorAuthTestContext` and no assertion that the exact operator-auth denial is returned by that same command when the fixture principal is absent. All new command-path calls use `persesRunWithIO`, which always stamps the verified principal in `persesMatrixCommandContext` (`perses_lifecycle_transport_test.go:385-401, 409-420`). The mission's cited `cmd/baha/app_init_wizard.go:29` does not resolve to the named helper at this exact head: that line is the `Compose` field, and the helper name is absent from the exact file. The hosted run's generic gate line in `main_test.go:60` is evidence that the operator-auth gate still rejects some unrelated CLI operation; it does not substitute for the Perses-specific negative direction.

Recipe: in `cmd/baha/app_status_result_test.go` or `perses_lifecycle_transport_test.go`, add a negative end-to-end `baha app perses status` invocation using the current repository's unauthenticated test context (locate the helper at its actual current definition; do not rely on the stale line reference). Assert the exact error `Managed-environment machine operations require an authenticated BaseHarbor operator`. Keep the existing authenticated invocation and assert its backend output. The test must fail if the auth enforcement is removed and the positive test must fail if its fixture context is not installed. Stop when both cases exercise the root command and both are selected by a required CLI shard.

## P3 — positive Loki/Tempo state is helper-only, not producible at the product call sites

The production witness derivation has positive Loki/Tempo branches only when `witness.LokiProven` / `witness.TempoProven` are true (`cmd/baha/app_status_result.go:135,162`). But all production call sites currently pass an empty `metricsprovider.PersesBackendSignalWitness{}`: `reportPersesSurfaceStatus` at `cmd/baha/perses_lifecycle.go:235`, and both local and remote `collectApplicationStatusResult` returns at `cmd/baha/app_status_result.go:296,399`. Therefore the real `baha app perses status` and `baha status --json` paths cannot emit a positive Loki or Tempo witness at this head. `TestPersesStatusWitnessConfiguredWhenResolved` at `app_status_result_test.go:114-146` supplies `{LokiProven: true, TempoProven: true}` directly to the helper; it does not prove that production can supply those values. The CLI test at `:324-327` instead expects both Loki and Tempo to be unreachable.

The round-6 note cites the 0428-143 decision that `Verification=none` makes no verification assertion and exporters omit those sources. That may constrain which product state is available, but it does not provide a real positive witness or revise the current task acceptance requiring reached/matched states. Under the current contract this remains open; if the owner has narrowed the acceptance to manifest/source-selection-only status, that contract change must be recorded explicitly before the helper-only positive test is treated as sufficient.

Recipe: wire the already resolved per-backend signal provenance into the authorized production result construction in `cmd/baha/perses_lifecycle.go` and both local/remote paths in `cmd/baha/app_status_result.go`; do not synthesize `LokiProven`/`TempoProven` in a CLI test. Add end-to-end command assertions for a real reached-and-matched source, reached-but-unmatched source, and unavailable source, including source IDs and parity of human and JSON faces. If the permitted upstream contract cannot provide that provenance, stop and obtain a written card-acceptance amendment instead of reporting a positive state from the direct helper test. Stop when a production path can reach the positive branch and each state is asserted through the command output, or when the owner updates the contract to remove that requirement.

## P4 — exact-head hosted run and inherited failure classification

Run `44875647949` is `pull_request`, head `b2f2fd3ac17293949c18223b55936e1018085472`, completed with conclusion `failure` (06:27:46Z–06:31:28Z). `PR · Native gate plan` is success; `PR Selected Checks` is failure; all five Go unit cells (`cli-0` through `cli-3`, `packages`) are completed/failure; owner, go-build, go-vet, cli-gofmt, focused Python, and Trusted Plan succeeded. Native runtime, selected-runtime, Docker/Podman HA, and release jobs were skipped. This CLI-only four-file diff does not require native runtime qualification; the successful Native gate plan did not select those cells. The exact-head aggregate is nevertheless red and cannot be reported as a pass.

All counts below use each individual job log, not the aggregate, which can omit job sections. Log retrieval sizes were:

- `gh run view 44875647949 --repo mcpdev80/baseharbor --log`: 1,248,220 bytes.
- `gh run view 44875647949 --repo mcpdev80/baseharbor --log-failed`: 346,071 bytes.
- `gh run view --job <id> --log` for candidate jobs: cli-0 `136759690877` 146,729 bytes; cli-1 `136759690895` 117,207 bytes; cli-2 `136759690976` 113,021 bytes; cli-3 `136759690935` 95,738 bytes; packages `136759690924` 66,916 bytes.

Comparison job-log sizes for run `44874605168` (PR #1742, same develop base): cli-0 `136756503658` 163,733 bytes; cli-1 `136756503603` 117,204 bytes; cli-2 `136756503478` 113,024 bytes; cli-3 `136756503444` 100,190 bytes; packages `136756503500` 66,913 bytes.

Per-job parsing yields 194 unique first-level `--- FAIL: Test...` names at the candidate and 197 in the comparison run. Shared: 194. Candidate-only: none. Comparison-only: exactly `TestPersesLifecycleTransportActionMatrix`, `TestPersesLifecycleMCPSharedSeamRunsApplyLifecycle`, and `TestPersesLifecycleHumanNoticeForEveryDeferredAction`. The count difference is therefore three removed failures with no new failed test name. The literal gate line is present in candidate cli-0 job `136759690877`:

```text
main_test.go:60: create failed: Managed-environment machine operations require an authenticated BaseHarbor operator.
```

It also occurs in other CLI shard logs. This makes “inherited operator-auth STATE” a justified classification for the remaining broad red set; it is not a candidate pass. The comparison run is on PR #1742's same develop base, but the exact-head run remains completed/failure. The separate class witness run `44854729670` is not evidence that this candidate passed.

The new/changed witness tests are covered by the existing CLI shard route. `.github/workflows/ci.yml:1185-1206` selects `pr_unit_shards` for a non-draft PR based on `unit_scope`, and `scripts/pr-go-unit-shard.py:60-81` hashes each discovered test name into `cli-0` through `cli-3` and runs selected tests. Applying the exact SHA-256 shard formula to the test names in the candidate assigns them as follows:

- cli-1: `TestPersesStatusWitnessConfiguredWhenResolved`, `TestPersesStatusWitnessNotConfiguredWithoutObservabilityBackend`, `TestPersesStatusWitnessNeverClaimsHealthyFromManifestFlag`, `TestPersesStatusWitnessHumanFaceRendersBackendWitness`.
- cli-2: `TestPersesStatusWitnessUnreachableWhenDeclaredNotResolved`, `TestPersesStatusWitnessUnreachableIsNotTheManifestFlag`, `TestPersesStatusWitnessLogsAbsentMarksLokiNotConfigured`, `TestPersesStatusWitnessRendersBackendWitnessDirectly`.
- cli-3: `TestPersesStatusWitnessHumanAndMachineFaceShowSameBackends`.

Those cells are selected in this same PR's required CLI jobs; none appears as a failed test name in the exact-head run. The CI test route is present, but the failures elsewhere keep the required aggregate red.

CI recipe: do not edit or rerun workflows from this review. Keep the run classified as failed/inherited STATE, resolve the owning operator-auth failure class, and after the content findings are corrected require a terminal successful selected-check aggregate on the corrected exact head. Stop while the required aggregate is red or any required cell is skipped.

## P5 — write-set and cleanliness

The four changed paths are authorized, and all protected paths listed in the mission are absent from the diff. Planning remote was verified as `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push.

No containers or compose projects were started. `docker ps -a` before review (PID 3208522) returned an empty container list. After review (PID 3296194), `docker ps -a` also returned an empty container list.

## repo-rule compliance

The candidate was read through GitHub API/remote refs; the quarantined workers/baseharbor checkout was not used for remote truth. No local package tests, workflow dispatches, PR comments, merges, force-pushes, product writes, or subagents were used. Only this review file is to be published in baseharbor-plan.

## Verdict and required recipes

**REQUEST CHANGES.** The authenticated positive status command reaches the renderer, and M1/M2 are supported by the test and mutation record. The required negative Perses authorization direction is absent. More fundamentally, production passes an empty Loki/Tempo witness at every result call site, so the positive per-backend cases only exist in direct helper tests, not in the product path. The exact-head CI aggregate is failed; per-job evidence shows the remaining red class is inherited and that this candidate adds no new failed test name while removing three.

Required corrective work:

- Add the Perses-specific unauthenticated command test in `cmd/baha/app_status_result_test.go` or `cmd/baha/perses_lifecycle_transport_test.go`, asserting the exact gate text; preserve the authenticated root-command test. Stop only when both directions are exercised and the CI shard runs them.
- Wire actual per-backend signal provenance into `cmd/baha/perses_lifecycle.go` and `cmd/baha/app_status_result.go` for local and remote status. Test reached/matched, no-match, and unavailable states through both output faces. If the upstream contract cannot provide this, record an owner-approved task-contract change. Stop when positive backend states are producible from product inputs, or the contract is explicitly narrowed.
- Treat run `44875647949` as failed despite its inherited failure classification. Obtain a successful exact-head required aggregate after corrections; no skipped required job counts as success.

## END

END_DONE codex-rev-cli2b: REQUEST CHANGES for PR #1702; exact candidate `b2f2fd3ac17293949c18223b55936e1018085472`. No Codeman post was sent per mission.
evidence/r28-welle4-2026-11-21/perses-status-backend-witness/review-4.md

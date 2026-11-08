# CODEX-REVIEW 0427-173 — PR #1505

ROLLE: REVIEW  
URTEIL: KORREKTUR  
Reviewed head: `b0376edb3588577b1cd96cdc391be60d2be3d4e5`  
Base: `develop` at `20902f0a6ab016fd8fe6a501751e1becc5f334dd`  
PR: https://github.com/mcpdev80/baseharbor/pull/1505  
Hosted run: `42534917055`, terminal `success` on the exact reviewed head

## PLAN

1. Fetch the live PR and develop refs; inspect the exact diff and current task/evidence contract.
2. Trace selection, source/applied-intent refusal, record deletion, command output, machine registration, and generated documentation.
3. Verify behavior-test and golden-test coverage plus the exact hosted job results and trigger.
4. Publish the independent review to Planning main and verify the product head remains unchanged.

## Findings

### Blocking: `NAME` is optional and an omitted name selects every record on the target

`cmd/baha/app_prune.go:41` documents `baha app prune [NAME]`, and `resolvePruneCandidate` initializes the selector to the empty string when no arguments are supplied (`:228-231`). Its match loop only filters when that selector is non-empty (`:232-238`). Consequently, with one dangling record on the effective target, `baha app prune` can select and remove that record without the explicit name required by the task. The surrounding help says an exact name is required, but the implementation does not enforce one.

Require an explicit selector before listing or deleting. If the contract is name-only, reject zero or extra positional arguments and remove the unsupported selector promises from help/docs. If UUID/environment selection is intended, parse it deliberately and ensure it still resolves one record. Add a command-entry regression that seeds exactly one dangling record, invokes `app prune` with no name, expects a usage error, and verifies the record remains byte-identical.

### Blocking: documented selector/output flags are rejected, and successful output is invalid JSON

At `cmd/baha/app_prune.go:43-50`, `parseReadOutputArgs` returns filtered arguments and an output format, but both results are discarded. The following loop examines the original arguments and rejects every argument beginning with `-`. This makes the advertised `--uuid`, `-e`/`--environment`, and `--json` options unusable. The duplicate-name response at `:264` directs the operator to the rejected `--uuid` option.

On success, `executeApplicationPrune` writes human confirmation text to `out` (`:136-142`), then `Run` unconditionally appends `writeJSON(out, result)` (`:55-59`). This is mixed human-plus-JSON output rather than valid JSON. The MCP handler captures the same mixed buffer and passes it to `resultFromPruneOutput` (`:293-313`); that parser ignores JSON errors and returns a zero-value result (`:309-318`). The behavior test also silently skips result assertions when JSON decoding fails (`app_prune_test.go:181-187`). Machine coverage and the golden registry therefore overstate the working result surface.

Make the operation return a structured result without writing presentation text. Have the CLI select exactly one output form from parsed options, and return the structured value directly to MCP. Add assertions that JSON mode is valid single-document JSON with correct identity/removal fields, human mode contains no JSON trailer, and the MCP tool result reports the removed deployment. Parse only options that are implemented; otherwise remove them from usage, long help, duplicate guidance, and docs.

### Blocking: refusal tests do not establish the full non-destructive contract

The source-present test `TestAppPruneIsRegisteredAndRefusesLiveSource` (`cmd/baha/app_prune_test.go:86-143`) checks registration and calls `resolvePruneCandidate` plus `deletionGuard` directly; it does not invoke the CLI entry point or compare persisted state. `TestAppPruneRefusesRecordWithAppliedIntent` does invoke `runWithIO` (`:223-260`), but its source is `t.TempDir()` and therefore `SourceAvailable` causes the earlier `SOURCE_PRESENT` branch (`app_prune.go:87-96`) to return before the applied-intent guard (`:101-110`). It proves that the directory still exists after a source-present refusal, but not that the applied-intent guard works when the source is gone, or that the live record is unchanged byte-for-byte.

Add a CLI-entry case for a missing source with an applied intent and assert it refuses without changing the record bytes. For the source-present live application case, snapshot the record and relevant deployment state before invocation and compare after; also assert a neighboring deployment and target runtime state remain unchanged. On the successful dangling case, assert a neighboring record and target runtime marker are unchanged. The implementation calls `DeleteDeploymentRecord` only after the guards, and that seam removes only `DeploymentRoot` (`internal/deployment/deployment_store.go:614-620`), but the regression suite should prove the stated guarantee rather than infer all of it from the call graph.

### Documentation and golden evidence: partially aligned, not fully guarded

The English and German command-index entries are generated from the command tree by `TestHumanCommandIndexTracksExactCommandMetadata` (`cmd/baha/human_documentation_test.go:91-107`); both reflect the same CLI summary and `Usage`. They are mechanically aligned but currently reproduce the unusable optional-name/`--uuid` syntax above.

The English machine-coverage row matches `machine_coverage.go:180` and is checked by `TestMachineDocumentationTracksRegistryAndCommandTree` (`cmd/baha/machine_documentation_test.go:35-57`). The German row in `docs/de/reference/cli-machine-coverage.md:37` contains the same command classification and operation mapping, but omits the source reason. The generator test writes/checks only the English matrix, so the German row is not generator-verified. Keep the two rows synchronized through a shared projection or explicitly test the German row’s canonical fields and reason.

`contracts/machine/v1/control.golden.json` adds the `app.prune` discovery metadata. `TestMachineControlGoldenRecordsMatchCoreDiscovery` (`contracts/machine_control_test.go:14-42`) verifies that synthetic discovery matches the operation registry, including that metadata. That is useful surface evidence, but it does not test prune’s command behavior or its execution result. The CLI tests do exercise a successful `runWithIO` path and ambiguous-name refusal, but the JSON assertion is ineffective as described above; there is no golden execution-result fixture for this command.

### Task evidence dossier not present at the claimed path

The task note on current Planning main links only to the 0427-160 `round-3.md`. I found no `evidence/bughunt-app-prune-dangling-record/` directory or app-prune dossier in the current `origin/main` tree. Planning commit `c555467e1738c531cf86c1ddcc23e5a227a95703` is the “integrate origin/main before 0427-173 evidence push” commit, not the claimed published dossier. The source and live hosted run were independently reviewed, but the cited app-prune evidence package is not independently inspectable from current Planning main.

## CI and candidate state

Live remote witnesses:

```text
20902f0a6ab016fd8fe6a501751e1becc5f334dd	refs/heads/develop
b0376edb3588577b1cd96cdc391be60d2be3d4e5	refs/pull/1505/head
```

The candidate is one commit directly on the current develop head. The PR is open and GitHub reports `MERGEABLE` / `CLEAN`.

Run `42534917055` is a terminal success on `b0376edb3588577b1cd96cdc391be60d2be3d4e5`, event `pull_request`. `PR Selected Checks` (`128899504448`) succeeded. `PR · Validation · go-unit-tests` (`128897018807`) succeeded; its job runs `scripts/pr-unit-database.sh`, which executes `go test ./... -count=1`, and the log reports `ok github.com/mcpdev80/baseharbor/cmd/baha` and `ok github.com/mcpdev80/baseharbor/contracts`. Thus the command, contract-golden, and documentation tests were captured by the pull-request run, not only local evidence. `documentation-audit`, `mkdocs-en-strict`, and `mkdocs-de-strict` also succeeded. Native destroy-retry Docker and Podman jobs succeeded. Native Keycloak/Core and other impact-gated jobs were skipped; they are not counted as executed passes. No `.github/**` file is in the PR diff.

The CI result is green for this exact head, but does not resolve the source-level findings above: package pass only establishes the tests as written, including the swallowed JSON parse error and the refusal case that exits through the source-present guard.

## Actionable correction recipe

1. In `cmd/baha/app_prune.go:41-50,202-238`, require one explicit name or implement the advertised selectors. Do not allow the empty-name branch to match every record. Test no-name refusal against one dangling record, exact-name selection, multiple matches naming every record, and any supported UUID/environment selector.
2. In `cmd/baha/app_prune.go:55-59,73-143,293-318`, separate result production from human rendering. Honor `parseReadOutputArgs`, emit valid JSON only when requested, keep human mode text-only, and pass the structured result directly to MCP. Make tests fail on JSON decode errors and assert all result fields.
3. In `cmd/baha/app_prune_test.go:83-260`, replace direct guard-only live refusal evidence with command-entry checks and cover missing-source plus applied-intent refusal. Compare record bytes and sibling/target runtime markers before and after both refusal and successful prune.
4. Regenerate EN/DE command indexes after correcting `Usage`; update the German machine-coverage row from the canonical command coverage source and add a test for it. Keep the golden discovery metadata test, and add behavior/result checks beyond discovery registration.
5. Preserve the current exact-head CI mapping: `go-unit-tests` (`go test ./... -count=1`, pull_request) must execute the prune, machine golden, and doc-generation regressions; documentation jobs and `PR Selected Checks` must be terminal success on the corrected exact head. Stop when a no-name invocation cannot delete anything, only the named dangling record is removed, live/recoverable state is unchanged on refusal, machine output is valid, bilingual generated references are checked, and the exact-hosted required result remains green.

## Provenance and publication

Fresh product checkout: `/tmp/opencode/0427-173-review-wt`, exact head `b0376edb3588577b1cd96cdc391be60d2be3d4e5`, merge-base `20902f0a6ab016fd8fe6a501751e1becc5f334dd`. Product candidate refs were rechecked before publishing this review.

Planning repository: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, origin `https://github.com/mcpdev80/baseharbor-plan.git`; fetched `origin/main` before this evidence commit was `c9400e1c8c961a689d41fdf4573863ea297bf3da`. Evidence belongs only in this repository.

END_DONE 0427-173-review: KORREKTUR — empty selector can remove the sole dangling record; documented selectors/output and MCP result are broken; refusal and bilingual evidence are incomplete. Candidate `b0376edb3588577b1cd96cdc391be60d2be3d4e5`, run `42534917055` success.

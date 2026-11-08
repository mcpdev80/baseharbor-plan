# CODEX-REVIEW 0427-149 — PR #1475

## PLAN

1. Pin the current PR head and base, inspect the exact candidate diff, and verify ancestry.
2. Map the registry uniqueness gate, name selection, duplicate cleanup, regression tests, and CI selection to the task acceptance criteria.
3. Record an SHA-specific verdict and concrete correction recipe in this planning evidence file.
4. Publish the evidence to baseharbor-plan origin/main and verify the remote tree entry.

## Review identity and candidate

Role: CODEX-REVIEW.

Repository: `mcpdev80/baseharbor`.

PR: [#1475](https://github.com/mcpdev80/baseharbor/pull/1475), task `0427-149`.

Reviewed head: `0f5d6a1c57e56fc908d9030f11400830eaebe984`.

Base branch `develop`: `cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c`.

Ancestry: `git merge-base --is-ancestor cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c 0f5d6a1c57e56fc908d9030f11400830eaebe984` returned 0. PR is open and GitHub reports `MERGEABLE`.

The head diff contains 14 files (712 additions, 109 deletions), all within product paths; no workflow files are changed.

## Findings

### F1 — the registry gate can be bypassed by the production create path

`internal/deployment/deployment_duplicate_name.go:34-44` treats any existing deployment directory for the proposed UUID as proof that this is an update and returns before scanning registered records. But `cmd/baha/app.go:67-85` creates a fresh UUID and its `source` directory before `cmd/baha/app.go:118` calls `SaveDeploymentRecord`. The earlier name scan at `cmd/baha/app.go:53-60` is not serialized with registration. Two concurrent `app create` invocations can both pass that scan, create distinct UUID directories, then each take the directory-exists early return and save duplicate `(target, name, environment)` registrations. The registry API therefore does not yet guarantee fail-closed uniqueness for the real create path.

The direct store regression `TestSaveDeploymentRecordRefusesDuplicateApplicationName` in `internal/deployment/duplicate_name_test.go:16-58` starts the second record with no pre-created deployment directory and does not exercise the production ordering or concurrency window.

### F2 — the advertised UUID disambiguation is discarded before resolution

`cmd/baha/app_context.go:80` calls `extractApplicationEnvironment`; that helper at `cmd/baha/app_context.go:549-559` removes `--uuid` and its value from the argument list. `cmd/baha/app_context.go:139-143` then calls `extractApplicationUUID` only on that filtered list, so the resolver receives an empty UUID. This contradicts the advertised remediation at `cmd/baha/app_context.go:335` and prevents a caller from selecting either duplicate by UUID through the normal command path.

The destroy path compounds the issue: `cmd/baha/app_destroy_lifecycle.go:51-65` also filters arguments, parses the remaining name, and builds `appArgs` without a UUID. A duplicate-loaded deployment is consequently ambiguous and cannot be selected for destroy using the documented UUID route. The current UUID tests in `cmd/baha/app_context_duplicate_name_test.go:84-158` call the resolver directly and do not exercise argument filtering or a command entrypoint.

### F3 — required lifecycle regressions and duplicate cleanup are not demonstrated

The reviewed tests cover a direct duplicate-save rejection, direct resolver ambiguity, and direct resolver selection. They do not provide the task's production-path `dup-edit` and `dup-destroy` regressions, nor prove that one of two already-registered duplicates can be edited/destroyed while the other record remains intact. The concrete UUID parsing loss in F2 means the advertised recovery path is currently unusable. The task acceptance also calls for cleanup of existing dangling instances; the current evidence/tests do not demonstrate that cleanup path against the production lifecycle command.

## Hosted CI on the exact head

GitHub Actions run `42494486803` completed on exact head `0f5d6a1c57e56fc908d9030f11400830eaebe984`.

`PR Selected Checks`, `PR · Validation · go-unit-tests`, `deployment-package-tests`, build, vet, gofmt, source-contract and plan checks passed. `go-unit-tests` ran `bash scripts/pr-unit-database.sh`, which executes `go test ./... -count=1`; `deployment-package-tests` selected `./internal/deployment`. Both are pull-request CI coverage for the current Go tests.

The lane's statement that a native core cell ran is inaccurate for this run: `PR · Native Keycloak/Core · ${{ matrix.runtime }}` was skipped. The native destroy-retry Docker and Podman jobs passed, but they do not establish native core execution or close the UUID/registry lifecycle gaps above. A skipped job is not a pass.

## VERDICT: REQUEST-CHANGES

The exact-head hosted unit and package checks are green, but the central acceptance is not met: the production registration order can bypass the new gate, and the UUID escape route is lost in argument filtering, leaving existing duplicates without a working cleanup selector. The claimed native core run was skipped.

## Actionable correction recipe

1. In `internal/deployment/deployment_duplicate_name.go` and the registry write path, make the uniqueness check apply atomically to first registration. Do not infer “same persisted identity update” from directory existence alone; distinguish a valid existing record for the same UUID from a caller-precreated partial directory. Serialize the uniqueness check and record write for the target/name/environment key, or use an equivalent atomic registry constraint.
2. In `cmd/baha/app_context.go` and `cmd/baha/app_destroy_lifecycle.go`, capture the UUID selector before filtering flags and carry it through the shared resolver. Ensure the documented `baha app <command> --uuid <deployment-id>` syntax is actually supported, including the no-name form if retained in the ambiguity message. Destroy must preserve the selected identity through preflight and cleanup.
3. Add production command-entry regressions: two concurrent or deterministically interleaved `app create` registrations with distinct UUIDs and the same target/name/environment must leave exactly one registry record and fail the other call closed; duplicate-loaded records must support UUID-selected edit and destroy; destroy must remove only the selected deployment and preserve the other record. Include a dangling-provider/reference fixture so the cleanup requirement is exercised.
4. Keep these tests in the pull-request-selected Go unit/deployment coverage and verify the exact-head hosted run executes them. If a native core gate is required for any added runtime test, it must be observed as executed rather than skipped; do not treat the current skipped cell as evidence.

Stop criterion: do not approve until the registry rejects the pre-created-directory/concurrent production registration case, the CLI actually forwards UUID selection through edit and destroy for pre-existing duplicates, the regressions verify selected-record cleanup and preservation of its sibling, and the exact-head hosted checks show the applicable tests executed successfully.

## Repo-rule compliance

This was a read-only product review. No product files, workflows, test VMs, containers, or CI runs were changed or started by the reviewer. Evidence is stored only in the baseharbor-plan planning repository.

END 0427-149-review BLOCKED — REQUEST-CHANGES for PR #1475 head `0f5d6a1c57e56fc908d9030f11400830eaebe984`.

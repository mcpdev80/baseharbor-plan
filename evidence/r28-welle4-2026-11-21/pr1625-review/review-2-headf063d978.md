# CODEX-REVIEW evidence: PR #1625

## PLAN

1. Verify the remote PR #1625 head and terminal run 44942703411; stop if the head differs.
2. Confirm all four commit author/committer identities at the exact candidate.
3. Inspect the credential-selection authority and fail-closed behavior in the requested production files.
4. Confirm the three named export tests exist and are selected by the CLI shard mapping and hosted inventory receipt.
5. Audit all four documentation paths in the run job and record the owner-scope receipt-tooling open item.
6. Write the verdict and recipe, then render/check and publish the review evidence to Planning origin/main.

## Verdict

REQUEST CHANGES for a candidate-owned regression-test gap: `TestAppExportManagedSecretWithoutOperatorFailsClosed` does not assert that command output remains secret-safe or that the requested output file is absent when authorization fails. The production flow inspected here stops before reading managed-secret values, but this specifically named boundary test will still pass for many unrelated errors and does not lock down the no-output/no-file acceptance condition. See the actionable recipe below.

The independent per-case receipt gap is recorded as `open item, owner-scope receipt-tooling`; it does not block this candidate under the mission’s explicit exception.

## Exact candidate and hosted gate

- Product remote: `https://github.com/mcpdev80/baseharbor.git`.
- PR state: #1625 OPEN, non-draft, base `develop`, merge state CLEAN.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1625/head`:

  ```text
  d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3	refs/heads/develop
  f063d9788ab0b8c6a11a6c6aa1c451b37d87099a	refs/pull/1625/head
  ```

- Exact candidate head: `f063d9788ab0b8c6a11a6c6aa1c451b37d87099a`; exact develop base: `d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3`.
- PR diff contains exactly eight paths: `cmd/baha/app_export.go`, `cmd/baha/app_export_command_test.go`, `cmd/baha/commands.go`, `cmd/baha/machine_coverage.go`, `docs/cli/command-index.md`, `docs/de/cli/command-index.md`, `docs/de/reference/cli-machine-coverage.md`, `docs/reference/cli-machine-coverage.md`.
- `git log --format='%an %cn' develop..head | sort -u` remote API result: `0428-065-export	0428-065-export`. All four commits have author and committer `0428-065-export`.
- Run `44942703411`: completed, success, exact head `f063d9788ab0b8c6a11a6c6aa1c451b37d87099a`; 41 jobs total, 20 success, 21 skipped, zero failures. `PR Selected Checks` job `136964340957` completed success. The run’s plan artifact has SHA-256 `12ae80a5364af8d15388bb124261ce44b75e6a373429ec35071de2015f358072` (`pr-plan.json`); plan head and merge base match the exact candidate and develop head. It records `coverage_status=resolved`, `fallback_used=true`, and `broad_required=false`, with normal validation checks retained and the unresolved CLI impact conservatively routed through broad unit/vet/build checks.
- Successful CLI unit shards: `cli-0` job `136963250958` (458 passed, 13 skipped, 471 discovered; inventory total 1829), `cli-1` job `136963250989` (436 passed, 10 skipped, 446 discovered; inventory total 1829), `cli-2` job `136963251050` (451 passed, 20 skipped, 471 discovered; inventory total 1829), and `cli-3` job `136963250973` (425 passed, 16 skipped, 441 discovered; inventory total 1829).
- Successful documentation audit job: `136963251076`, `PR · Validation · documentation-audit`. Its log reports EN/DE page coverage for 172 Markdown pages, technical integrity PASS for 172 paired pages, local/remote/team workflow PASS for 21 shipped commands, six audit tests OK, and German navigation/human-guide coverage PASS for 45 pages. All four changed documentation paths listed above were in the run’s exact PR diff and were covered by this job.
- `PR · Trusted Plan` job `136963184807`, `PR · Native gate plan` job `136963184880`, source format, build, vet, package/CLI tests, and all other executed required validation jobs completed successfully. Skipped jobs are reported as skipped, not counted as passes.

## Credential and authorization review

- `cmd/baha/app_export.go:123-131` rejects a no-input export with no explicit selection and authorizes explicit selections before source discovery.
- `cmd/baha/app_export.go:145-169` requires a terminal before interactive selection when no state was selected, rejects an empty selection, and re-authorizes the selected state. `cmd/baha/app_export.go:190-203` rejects empty collected entries and reads the password only from the required password file after authorization and collection.
- `cmd/baha/app_export.go:229-243` calls `authorizeHumanReveal` for `secrets/openbao`. `cmd/baha/app_export.go:300-361` repeats that check before listing metadata and fetching managed values; managed values are fetched only after the reveal authorization. Backend errors are redacted at lines 342-350, and temporary secret buffers are cleared at lines 305-311 and 351.
- `cmd/baha/app_export.go:211-225` prints selected state names and an encrypted-export notice, then writes the encrypted envelope; it does not format credential values into stdout. `cmd/baha/app_export.go:503-526` requires a regular, owner-only password file and a minimum 12-byte password. The production path therefore fails closed before the write call when authorization or selection fails.
- `cmd/baha/operator_auth_boundary.go:55-78` requires operator authentication for managed environments unless a verified principal or narrowly established local workload authority applies. Lines 112-128 fail closed without stored/environment configuration when input is absent, and refuse interactive setup when input is not a terminal.
- `cmd/baha/local_workload_authority.go:45-73` limits its grant to CLI/stdio local operations without tenancy/core authority, a non-local target, stored operator auth, or operator-auth environment configuration. This grant does not remove the additional human-reveal check in `authorizeExport` / `collectExportEntries`.
- The new fixture is test-only: `cmd/baha/app_export_command_test.go:353-377` constructs a synthetic verified principal and membership provider in `_test.go`; there is no production branch or fixture switch. The managed-secret test’s no-operator context at lines 293-302 intentionally omits that principal.
- Candidate-owned test gap at `cmd/baha/app_export_command_test.go:293-315`: the test only requires a non-nil error and checks that its text lacks `Selected export sources`. It does not assert the expected operator-auth denial, inspect `out` or `errOut`, specify an output path and prove no file was created, or prove the secret backend was not reached. Therefore a regression that emits sensitive output or creates an artifact and then returns a different error is not caught by this test.

## CLI test selection and receipt item

The three named tests exist in `cmd/baha/app_export_command_test.go` at lines 28, 163, and 243. The exact candidate’s `scripts/pr-go-unit-shard.py` hashes non-cohort test names with SHA-256 and maps modulo four; applying that mapping gives:

- `TestAppExportCommandPathAssemblesProductionWiring` → `cli-0`, successful job `136963250958`.
- `TestAppExportFailsClosedWithoutSelection` → `cli-2`, successful job `136963251050`.
- `TestAppExportManagedSecretWithoutOperatorFailsClosed` → `cli-3`, successful job `136963250973`.

The matching hosted shard logs each report the same discovered CLI inventory total of 1829 and success summaries shown above. The script currently emits aggregate shard results rather than per-case names; under the mission’s stated exception, source existence plus deterministic shard mapping and the exact shard’s successful inventory receipt is sufficient for this review.

Open item, owner-scope receipt-tooling: `scripts/pr-go-unit-shard.py:60-82` only emits aggregate shard evidence; `scripts/pr-gate-coverage.json` has no component mapping for `cmd/baha/app_export.go` or `cmd/baha/app_export_command_test.go`. This is not a candidate blocker per mission instruction.

## Actionable recipe

In `cmd/baha/app_export_command_test.go`, strengthen `TestAppExportManagedSecretWithoutOperatorFailsClosed` to assert the operator-auth denial that proves the intended boundary, capture and assert secret-safe stdout/stderr, provide an explicit `--output` path and assert it remains absent after failure, and make the no-backend-access condition observable (for example, factor the command seam to inject a counting secret reader and assert neither `List` nor `GetMany` runs before verified human reveal). Keep the real root-command path in the test so the production wiring remains exercised. Run the focused test through its existing CLI CI shard in a follow-up candidate.

## Repo-rule compliance

- Reviewer-only: no product files changed, no local product tests run, no product push, no workflow dispatch/rerun, and no subagents used.
- Planning remote identity was checked before the evidence commit: `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- The reviewer evidence is kept only in the designated `baseharbor-plan` evidence path.
- `python3 scripts/plan.py render`: completed successfully.
- `python3 scripts/plan.py check`: 663 tasks, 7 epics, 13 releases, 24 decisions; 0 errors and 11 existing dependency warnings.
- Evidence checkbox scan: clear.
- Planning main ls-remote immediately after the first evidence push: `2286cb0975be878947a43fa2cd2245c139fc0cd5\trefs/heads/main`.
- Required `git fetch origin main && git ls-tree -r --name-only origin/main | grep 'evidence/r28-welle4-2026-11-21/pr1625-review/review-2-headf063d978.md'` output before the final evidence push:

  ```text
  evidence/r28-welle4-2026-11-21/pr1625-review/review-2-headf063d978.md
  ```

## cleanliness

- Before inspection: pid 3425149; `docker ps -a` showed these pre-existing containers, all exited: `bh-itest-1c3f4e6d-12470-edit-runtime-integration-dev-api-1`, `bh-itest-7daed22f-28345-shared-openbao-1`, `bh-itest-7daed22f-28345-shared-openbao-member-1-1`, `bh-itest-7daed22f-28345-shared-postgres-init-1`, `bh-itest-7daed22f-28345-shared-postgres-1`, `bh-itest-7daed22f-28345-shared-postgres-member-1-1`, `bh-itest-7daed22f-28345-shared-postgres-admin-1`, `bh-itest-7daed22f-28345-shared-openbao-admin-1`.
- After inspection: pid 3452525; `docker ps -a --format '{{.Names}} {{.Status}}'` listed the same eight containers, all exited. This review started no containers and changed no Docker state.

## END BLOCKED

END codex-rev-1747 BLOCKED — REQUEST CHANGES because the managed-secret denial test does not assert the no-output/no-file security contract; exact candidate `f063d9788ab0b8c6a11a6c6aa1c451b37d87099a`.

identity: 1 autor = 0428-065-export
receipt-item: owner-scope

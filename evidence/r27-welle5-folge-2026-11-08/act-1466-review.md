# CODEX-REVIEW 0427-141 / 0427-148 — PR #1466

## PLAN

1. Read both card contracts and the cited HD3/HD4 hunt evidence.
2. Fetch the exact PR head and current develop head, then inspect the full PR diff and relevant production paths/tests.
3. Compare each acceptance item with the candidate and identify the CI job that executes its regression.
4. Record a verdict and a file-specific correction recipe with a test and stop criterion.
5. Publish this review in the planning repository and verify its origin/main tree entry.

## Review basis

- Role: REVIEW.
- Repository: `mcpdev80/baseharbor`.
- PR: #1466, open, not draft, `mergeStateStatus=UNSTABLE`.
- Exact reviewed head: `f8e1d573a0a6c32435dd7646576c511d97b68129` (`refs/pull/1466/head`).
- Fetched develop head: `618d23bde0870391541a8bbdf3ee103f22d70560` (`refs/heads/develop`).
- Exact-head workflow run: [42478685135](https://github.com/mcpdev80/baseharbor/actions/runs/42478685135), terminal `failure` on the reviewed SHA. `PR · Validation · go-unit-tests` failed: `cli_diagnostics_regression_test.go:15: quick init diagnostic missing "baha app init": no unambiguous application requirements were detected (SQL=false, cache=false, object-storage=false, workload-services=0, metrics=false, telemetry=false, secret-candidates=1 unconfirmed)`. `human_documentation_test.go:107` also reports `machine documentation drift in ../../docs/cli/command-index.md; regenerate from the registry/command tree`. `PR Selected Checks` failed with `BLOCKED: required job did not succeed: pr_validations`. Source format, trusted plan, workflow policy, go-build, go-vet, cli-gofmt, focused Python, and both destroy-retry jobs passed; native Keycloak/Core and Selected Runtime were skipped. Destroy-retry jobs do not prove either card's behavior.
- The PR diff changes only `cmd/baha/app_init_wizard.go`, adds `cmd/baha/cli_diagnostics_regression_test.go`, and changes `cmd/baha/commands.go`.
- Card evidence: `tasks/t-20261108-bughunt-quickinit-failure-explain.md` (0427-141), `tasks/t-20261108-bughunt-list-target-failclosed.md` (0427-148), `evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md` (BF-HD3-10/11), and `evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd4.md` (BF-hd4-3).

## Findings

### 0427-141 — quick-init diagnostic and dry-run guidance

HD3 BF-HD3-10 records the generic `no unambiguous application requirements were detected` error for `baha app init --quick` in a repository with no detected capabilities. The candidate now reports each capability boolean, workload count, and count of unconfirmed secret candidates at `cmd/baha/app_init_wizard.go:232-235`. Its follow-up points to interactive init or explicit flags, and says `baha app plan` previews changes because `baha up` has no dry-run mode. This covers the missing distinction and the card's plan guidance.

The regression at `cmd/baha/cli_diagnostics_regression_test.go:8-18` verifies false capability values and `secret-candidates=1`; it does not verify the candidate identity supplied by its fixture (`SECRET_NAME`), and the user-facing message reports only the count. The card's wording says the error names candidates, so that criterion is only partly demonstrated. Its check for the `Next` guidance is also made against `err.Error()`, which contains only the diagnostic message; the hosted failure confirms `baha app init` is not present there. The guidance is passed as a separate next-action string by `usageError` at `app_init_wizard.go:233-235`, so test the rendered CLI output or the structured fields instead.

### 0427-148 — fail-closed list behavior

HD4 BF-hd4-3 records that `baha list` without an effective target fails closed with available target names and suggests explicit selection; the dossier classifies this as intentional owner-boundary behavior, not a confirmed product bug. The candidate's `cmd/baha/commands.go:44-55` help text documents fail-closed behavior, `baha target list`/`target activate`, and an all-targets inventory with a `TARGET` column. The actual `appListCommand` supports `--all-targets` and prints that column at `cmd/baha/app_commands.go:56-120`, so the described option is present.

The new `TestListHelpExplainsFailClosedTargetSelection` at `cmd/baha/cli_diagnostics_regression_test.go:20-33` asserts only help-text substrings. `appListCommand` supports `--all-targets` and emits the explicit `TARGET` column (`cmd/baha/app_commands.go:56-120`), but the new test does not run the selected semantics against multiple configured targets. No test in the candidate's Go source search covers `--all-targets` or the ambiguous top-level `baha list` path. The card explicitly requires a regression for the chosen semantics; a help-string assertion alone does not satisfy that requirement.

## Verdict

**ROLLE: REVIEW — URTEIL: korrektur.** The production help and implementation are aligned, and the quick-init error is more informative. The acceptance remains incomplete because 0427-141's diagnostic does not identify the candidate named by its fixture, its new test incorrectly expects next-action text inside `err.Error()`, 0427-148 has no behavioral regression for the documented target-selection semantics, generated CLI documentation is stale, and exact-head `go-unit-tests` plus `PR Selected Checks` failed. This is not an approval or merge authorization.

## Correction recipe

- `cmd/baha/app_init_wizard.go:232-235`: include deterministic, safe candidate identifiers and the unconfirmed-versus-accepted distinction in the quick-init error. Do not include secret values. If the intended contract is counts-only, amend 0427-141's acceptance to say so instead of claiming candidate names.
- `cmd/baha/cli_diagnostics_regression_test.go:8-18`: assert the candidate identifier (`SECRET_NAME`) and missing/unconfirmed distinction; verify the `Next` text through rendered command output or the structured usage-error fields, not `err.Error()` alone.
- `cmd/baha/cli_diagnostics_regression_test.go:20-33`: add command-level tests with two configured targets and no selected target. Assert top-level `baha list` fails closed with target choices, and `baha list --all-targets` succeeds with both targets represented in the `TARGET` column. Retain the help-text assertion.
- `docs/cli/command-index.md`: regenerate the command index after the command metadata changes; the exact-head `go-unit-tests` failure says it has drifted.
- CI jobs: the new Go regressions must run in `PR · Validation · go-unit-tests`; this job must finish green. Recheck `PR Selected Checks` on the corrected exact head. Do not treat skipped native Keycloak/Core or unrelated destroy-retry jobs as proof of these CLI behaviors.
- Stop criterion: do not approve until the corrected exact head has terminal green `PR · Validation · go-unit-tests` and `PR Selected Checks`, the generated command index is current, and both regressions exercise the stated behavior. Any skipped required job or missing candidate-level diagnostic assertion remains a correction blocker.

## Candidate integrity

The review was read-only. PR head witnessed before review: `f8e1d573a0a6c32435dd7646576c511d97b68129`. Develop head witnessed before review: `618d23bde0870391541a8bbdf3ee103f22d70560`.

Planning repository remote verified as `https://github.com/mcpdev80/baseharbor-plan.git`. Pre-publication remote witness after integrating concurrent evidence commits: `7f08135255f2dccc1b35bdcc3bf26f14f298b1bb refs/heads/main`.

## Current-head review — 2026-11-08

### Exact candidate and hosted state

- Role: REVIEW; cards 0427-141 and 0427-148.
- Live PR #1466 head: `daacddbbe9d011c3fd48ae7cc798e560dd591258`; base `develop`; PR state `MERGED`; merge commit `ad49d2d2129657e2e09c40b534c6a8030413a083`; merged at `2026-11-08T12:38:50Z`.
- Live `develop` was `f05d6ee2e596da73056dfd1bda64a79ebbfe6b92`. GitHub compare reported the reviewed head as an ancestor of develop (`behind`, 0 ahead, 13 behind; merge base is the candidate), consistent with the recorded merge.
- The exact-head workflow run [42480521183](https://github.com/mcpdev80/baseharbor/actions/runs/42480521183) was terminal `success`, event `pull_request`, head `daacddbbe9d011c3fd48ae7cc798e560dd591258`. `PR · Validation · go-unit-tests` (job `128731358928`) passed and logged `ok github.com/mcpdev80/baseharbor/cmd/baha 399.265s`; this executes the changed package tests. `PR Selected Checks`, `go-build`, `go-vet`, `cli-gofmt`, `Source format`, `mkdocs-de-strict`, `mkdocs-en-strict`, `documentation-audit`, `pages-candidate-build`, `wizard-registration-tests`, `Focused Python`, and `Workflow policy` passed. Native destroy-retry Docker and Podman jobs also passed but are not proof of these CLI acceptance points. Targeted HA Docker/Podman and Native Keycloak/Core were skipped; this review makes no native application E2E claim.
- Exact product diff is five files: `cmd/baha/app_init_wizard.go`, `cmd/baha/cli_diagnostics_regression_test.go`, `cmd/baha/commands.go`, `docs/cli/command-index.md`, and `docs/de/cli/command-index.md`. No product or workflow changes were made during this review.
- Planning base before this evidence update: `c454da653a5d8db5e201de7d9da188a3a5bd8243 refs/heads/main`.

### Current acceptance findings

#### 0427-141 — quick-init diagnostic, candidate detail, and dry-run guidance

The diagnostic at `cmd/baha/app_init_wizard.go:232-235` distinguishes detected capability booleans, workload count, and the count of unconfirmed secret candidates, and its `Next` text points to `baha app plan` as the dry-run substitute. But the fixture supplies the candidate `SECRET_NAME`, while the error reports only `secret-candidates=1`; it does not name that candidate or distinguish it by identity. The new test at `cmd/baha/cli_diagnostics_regression_test.go:8-18` asserts the aggregate count and two capability fields only. It no longer asserts the separate `Next` guidance that failed in the earlier run, so the green run does not prove the full acceptance message. The command-index changes document list syntax, not the app-plan dry-run guidance.

#### 0427-148 — fail-closed list semantics and regression

The help text at `cmd/baha/commands.go:44-55` now explains selected-Target behavior, deliberate fail-closed handling, explicit target selection, and the `--all-targets` inventory. Production `appListCommand` at `cmd/baha/app_commands.go:56-120` routes default listing through `effectiveTarget` and renders a `TARGET` column for `--all-targets`. The new regression at `cmd/baha/cli_diagnostics_regression_test.go:20-33` checks only help strings. Existing selector tests (`cmd/baha/target_selection_test.go:17-88`) verify the selection helper's ambiguous-target error, and `target_list_ambiguity_test.go` tests `baha target list`; neither exercises top-level `baha list` nor verifies that `baha list --all-targets` emits both targets and the `TARGET` column. Thus the exact command behavior described by the new help remains without a command-level regression.

### Current verdict

**ROLLE: REVIEW — URTEIL: KORREKTUR-FOLLOW-UP.** Hosted checks passed on the exact head and the change was merged, but neither card's entire acceptance is proven: 0427-141 omits candidate identity and does not test the separate app-plan next action; 0427-148 adds a help-text check but no command-level regression for the documented list behavior. The earlier request-changes verdict is not cleared by the green run alone. Since #1466 is already merged, this calls for a focused follow-up PR rather than further edits to the merged candidate.

### Follow-up recipe and stop criterion

- `cmd/baha/app_init_wizard.go:232-235`: include safe, deterministic candidate identity/details and the unconfirmed distinction in the quick-init diagnostic, without disclosing secret values. Keep the app-plan next action visible in rendered CLI output.
- `cmd/baha/cli_diagnostics_regression_test.go:8-18`: assert the candidate represented by the fixture, the missing-versus-unconfirmed distinction, and the separately rendered `Next` text that recommends `baha app plan`.
- `cmd/baha/cli_diagnostics_regression_test.go:20-33`: add command-level coverage with two configured targets and no selected target. Assert `baha list` fails closed with actionable target choices, while `baha list --all-targets` succeeds and emits both targets under an explicit `TARGET` column. Keep the help assertion.
- Run the focused `cmd/baha` tests and require the exact follow-up head's `PR · Validation · go-unit-tests` and `PR Selected Checks` to reach terminal success. Preserve docs checks for any changed help or docs.
- Stop criterion: do not accept/close the follow-up until candidate-level quick-init detail and next-action output are asserted, both list command behaviors are regression-tested, and exact-head hosted required checks are green. Do not weaken fail-closed target selection.

### Current-head END

END_DONE 0427-1466-review: KORREKTUR-FOLLOW-UP; #1466 `daacddbbe9d011c3fd48ae7cc798e560dd591258` reviewed, merged as `ad49d2d2129657e2e09c40b534c6a8030413a083`; exact-head run `42480521183` success.

Planning validation after fetching base: `python3 scripts/plan.py check` reported 417 tasks, 7 epics, 13 releases, 16 decisions; 0 errors and 3 dependency warnings.

Exact `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-08/act-1466-review.md` output after publishing the current-head review:

```text
100644 blob 9eda2ea2d02242c1aa437c396e42c6b6eb12721c	evidence/r27-welle5-folge-2026-11-08/act-1466-review.md
```

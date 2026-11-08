# CODEX-REVIEW 0427-164 — PR #1494

## PLAN

1. Verify the live PR head, develop base, and exact-head hosted run.
2. Inspect target-delete argument parsing, consent branches, destructive behavior, regression tests, and CI selection.
3. Record the verdict and a repair recipe in planning evidence and publish it.

## ROLLE: REVIEW

## Verdict: KORREKTUR

### Candidate and hosted evidence

- PR #1494 is OPEN and MERGEABLE. Exact head: `468027889093cfa776f2851cd9ea765cb4365d6c`; exact PR base SHA from the API: `171e9569d4bdea0b03faca663dc88a41e185f75f` (`develop`). Live `develop` at review time: `7af8d440e9a4dd1b633fdc44e4093109fe44ae37`.
- Hosted run `42511019014` is terminal SUCCESS on exact head `468027889093cfa776f2851cd9ea765cb4365d6c`: 12 successful jobs, zero failed jobs. `PR Selected Checks` passed. Both Native destroy retry jobs passed; native Keycloak/Core was skipped as not selected for this diff.
- Hosted `PR · Validation · go-unit-tests` ran `scripts/pr-unit-database.sh`, whose source executes `go test ./... -count=1`; it therefore includes `cmd/baha/target_definition_change_test.go` on the `pull_request` trigger. The two native destroy-retry Docker/Podman jobs also ran and passed.

### Findings

1. **The actual CLI flag still fails argument-count validation.** In `cmd/baha/target.go:548-571`, `parseReadOutputArgs` removes only output-format arguments. The loop recognizes `--yes`/`-y` and sets `yes=true` but leaves that token in `args`; the subsequent `len(args) != 1` check at lines 567-569 therefore rejects normal invocations such as `baha target delete NAME --yes` and `baha target delete --yes NAME` before reaching the consent code. The current regression at `cmd/baha/target_definition_change_test.go:52-79` calls `deleteTarget` with only the name and injects `withAssumeYes` directly, so it does not exercise CLI parsing. The old CLI test was changed to reject `--bogus`, and the prior `--yes` usage assertion was removed without adding an accepted-flag regression.
2. **Consent behavior behind the parser is otherwise appropriately scoped.** `cmd/baha/target_definition_change.go:46-56` supplies both `First` and `Second` only when `assumeYes(ctx)` and `!plan.Scope.Destructive`; `ValidateProviderImpactScopeConsent` still validates the plan at lines 57-63. Without `--yes`, non-TTY leaves consent absent and the validation rejects before mutation. The interactive TTY reader branch at lines 38-45 is unchanged and continues to call `readProviderImpactAcknowledgements`, which loops through the required stages in `cmd/baha/provider_change_confirmation.go:58-67`.
3. **The change does not approve data zeroing.** The CLI path is a config-only detach; it does not remove runtime or data owners. The new regression verifies the retained owner bytes are unchanged. The synthesized consent contains only the two consequence acknowledgements and does not set `DeleteData`; destructive plans do not enter the `!plan.Scope.Destructive` branch.

### Umsetzbares Lösungsrezept

- **Datei:** `cmd/baha/target.go`, `deleteTarget` around lines 554-571. Remove `--yes`/`-y` from the positional argument slice while recording the flag, or parse options into separate positionals and flags before validating exactly one target name. Preserve rejection of unknown flags and existing output-format parsing.
- **Datei:** `cmd/baha/target_definition_change_test.go`. Add a regression that invokes `runWithIO` (or the real command dispatcher) with `target delete NAME --yes` on a non-TTY and proves detach/recovery succeeds while runtime-owner bytes remain unchanged. Keep the no-`--yes` fail-closed test and the two-current-acknowledgements test. Verify the interactive TTY route still asks both stages.
- **CI requirement:** the command-entry regression must run in the hosted `PR · Validation · go-unit-tests` job (`scripts/pr-unit-database.sh` -> `go test ./... -count=1`) on `pull_request`; require terminal success and `PR Selected Checks` success on the corrected exact head. Do not count skipped jobs as executed proof.
- **Stop criterion:** approve only when the real CLI accepts the documented `--yes` form and completes config-only detach, no-`--yes` non-TTY remains fail-closed, interactive stages remain intact, protected runtime/data owner bytes remain unchanged, and the regression passes in hosted CI on the final SHA.

## repo-rule compliance

Read-only product review. No product source, tests, or workflows were changed; no checks were rerun or dispatched.

## END 0427-164 REVIEW

KORREKTUR — candidate `468027889093cfa776f2851cd9ea765cb4365d6c`; hosted run `42511019014` passed, but `--yes` remains in the positional slice and is rejected by the argument-count check.

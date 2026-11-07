# CODEX-REVIEW 0427-access-wizard — PR #1430

## PLAN

1. Read mission, binding coordinator policies, task contract, prior findings, and product rules — complete.
2. Fetch exact PR/base refs and inspect wizard flow, fail-closed paths, registration, offboarding scope, tests, write-set, and hosted CI without rerun — complete.
3. Record SHA-specific verdict and actionable recipe in canonical planning evidence — complete.
4. Publish evidence to origin/main, verify evidence and unchanged candidate witnesses, then post END — in progress.

## Verdict: REQUEST-CHANGES

The candidate fixes the three command-registration failures and passes hosted CI, but the functional path is not complete: assignment and offboarding only mutate a temporary in-memory Manager and are not persisted; the selection-screen `cancel` submits selections to the mutating callback; multi-target selections are displayed but only the first is applied; and the offboard command has no routing for three of the four removal types required by the task.

## Findings and repair recipe

1. **Assignment/revocation does not persist.** `cmd/baha/access_wizard_command.go:151` builds a fresh `orgconfig.Manager` from active state, then returns only that Manager and scope (`:159-163`); the `ActiveState` is discarded. `accesswizard.ResolveAssignment` calls `manager.Create` and evaluates the policy (`internal/accesswizard/authority.go:50-73`), while `RevokeAssignment` calls `manager.Revoke` (`:81-98`). Those methods only mutate `Manager.profiles` in memory (`internal/orgconfig/profiles.go:407-432,505-516`). The CLI never writes the modified profiles back to `state.Config.Profiles` or calls `orgconfig.SaveActive` (`internal/orgconfig/store.go:89-120`). A successful command therefore prints/returns a decision but loses the change when the process exits. Keep the active state through the transaction, apply the reviewed changes to its owned profile set, validate ownership/scope through the existing Manager and policy authority, then persist via the existing active-state writer. Add CLI-path tests that reload active state after assignment and revocation and assert the exact resulting owned profile set; an injected persistence failure must return failure and leave the command without a success result.
2. **`cancel` after selection invokes the write callback, and the displayed review has no approval prompt.** `Controller.pageSelect` maps `cancel` to `(acc, false, nil)` (`internal/accesswizard/controller.go:205-208`). If `acc` contains a target, `Controller.Run` treats that as completion and immediately calls `decide(review)` (`:117-137`). The CLI callback directly calls `ResolveAssignment` or `RevokeAssignment` (`cmd/baha/access_wizard_command.go:54-69,104-111`); there is no separate yes/no confirmation after the review. Thus a user who selects a target and then types the advertised `cancel` reaches the mutation path. Give selection completion a distinct input and make cancel at every stage return without invoking the callback; after rendering the full effective-scope review, require an explicit affirmative confirmation before the callback. Add end-to-end CLI regressions proving cancel after one or more selections never invokes or persists a mutation and explicit decline leaves the active config byte-for-byte unchanged; approval should be the only path to the writer.
3. **Only the first selected target is applied, and offboarding kinds are not implemented.** The controller accumulates selections and `Review.Render` shows every one, but both command callbacks use only `review.Selected[0]` (`cmd/baha/access_wizard_command.go:58-64,104-109`). Process every reviewed target under the confirmed scope, or constrain the wizard and review to a single target if the task contract is revised. In addition, `access offboard` always calls `RevokeAssignment`; it never asks for or dispatches a `RemoveKind`. `RemoveConnection`, `RemoveDevice`, `RemoveGrant`, `RemoveManagedUser`, `OffboardRequest`, and `ValidateOffboard` are currently declarations/helpers used only in tests (`internal/accesswizard/wizard.go:80-119,182-197`). Implement distinct user-reviewed routes for local connection removal, device revocation, owned grant removal, and explicitly named managed-user disable/delete through their respective existing authorities. Add production-path tests for each route proving it changes only its owned boundary and fails closed when target/person/authority/config is missing. Stop if any route requires another task's owned lifecycle/API paths; record the dependency instead of widening this PR.

## Checks of requested items

- **Guided assignment, config failure, and scope review:** `loadAccessWizardAuthority` rejects unavailable active config, missing operation, and missing/empty authority (`cmd/baha/access_wizard_command.go:136-163`); the controller rejects empty/no-target selection (`internal/accesswizard/controller.go:148-173`) and renders effective scope. These guards are useful but do not cure the missing persistence and confirmation findings above.
- **Root registration, machine classification, and command index: PASS.** `accessWizardCommand()` is in `rootCommand()` at `cmd/baha/commands.go:170`; `baha access assign` and `baha access offboard` have explicit human-only/excluded machine classifications at `cmd/baha/machine_coverage.go:164-165`; the generated English and German command index entries are present. The root-command tests cover both executable children. Hosted `wizard-registration-tests` and documentation audit both passed.
- **#1433 offboarding target/name correction: PARTIAL PASS.** `RevokeAssignment` resolves the exact requested person, verifies `profile.Name == person` and `profile.Target == target`, and only then revokes by profile name (`internal/accesswizard/authority.go:81-98`). The new scope regressions cover wrong target/person, missing identity, nil authority, and preservation of unrelated profiles (`internal/accesswizard/offboard_scope_regression_test.go:18-57`). However, this helper still changes only the temporary Manager and the CLI uses only the first selected target; the complete task offboarding contract remains unmet.
- **Test quality and CI capture: PARTIAL.** New command tests cover root registration, malformed/ambiguous CLI subject, subject substitution, and bounded JSON fields (`cmd/baha/access_wizard_command_test.go`). The offboard helper regressions are relevant to the #1433 target collision. The controller tests cover pagination and basic fail-closed cases, but `TestCancelBeforeApprovalFailsClosed` only cancels at the name prompt; it misses cancel after a target selection, the path that calls the write callback. No CLI test reloads persisted profiles, tests multi-target application, or dispatches all removal kinds. These tests are picked up by hosted `PR · Validation · go-unit-tests` on pull-request changes; the existing `wizard-registration-tests` and `documentation-audit` also run and passed. No workflow change is needed for this PR's Go tests.
- **Write-set: PASS.** The exact diff contains `cmd/baha/access_wizard_command.go`, `cmd/baha/access_wizard_command_test.go`, `cmd/baha/commands.go`, `cmd/baha/machine_coverage.go`, four English/German command-index and machine-coverage documentation files, and `internal/accesswizard/{authority.go,controller.go,wizard.go,wizard_test.go,offboard_scope_regression_test.go}`. No `.github/**`, OCI, lifecycle, or fixture files changed. The root registration, classification, and generated index changes are required by this review mission.

## SHA, provenance, and CI evidence

- Product repository: `mcpdev80/baseharbor`, fresh clone at `/tmp/opencode/0427-access-wizard-review-wt`.
- PR #1430: OPEN; base `develop`; exact head `e651cb1c2978c022210c869e6ea6e1e9a43aefa9`; mergeable `MERGEABLE`; merge state `CLEAN`.
- Fetched base: `8a3f58da905fad52327d33466fde1d9568092519`. `git merge-base --is-ancestor refs/remotes/origin/develop refs/remotes/origin/pr/1430` returned `0`.
- Candidate-only log (`git log --format='%H %an %s' develop..refs/remotes/origin/pr/1430`) is exactly:

  ```text
  e651cb1c2978c022210c869e6ea6e1e9a43aefa9 0427-node-cli gofmt: fix trailing whitespace in access_wizard_command.go (cherry-picked #1433 fix)
  0080910dbf25eec023f0bfa834ee83a2c7f92c75 Marcel Pfingstgräf test(access): verify person/target-bound offboarding and prevent unrelated revocation
  e105eb38e2555078b22cac7fbb14710fc48b0db6 Marcel Pfingstgräf fix(access): bind wizard reviewed subject to explicit CLI identity before mutation
  9a17d59414b9f3ac07c0df5477ab3a03528c0329 Marcel Pfingstgräf test(access): assert identity binding, deny invalid CLI inputs and separate Core connection
  ac1855da2d9e2cdc6370fa30d9cb46dc53739454 Marcel Pfingstgräf fix(access): prevent offboard from revoking a target-named unrelated profile
  4c9bf21a3626b03f39429594808c6e4221dab68b 0427-node-cli Merge remote-tracking branch 'origin/develop' into work/r27-access-wizard
  b93836ac37b8d613fbb388019f54fc0014dfdd31 0427-node-cli re-pin 71765bb31: terminal CI run on final wizard-registration candidate
  71765bb31306bf0dfc1b78693757a99b0effcb32 0427-node-cli Mirror new baha access* CLI literals into German machine coverage page
  69ce9b476e9171bb1b81b2a0e135462a11cf08f9 0427-node-cli Register baha access assign/offboard in machine classification; regenerate CLI command index
  3a699a2876c4d0349021b6222958d9a2f74b09dc 0427-access-wizard feat(cli): add guided access assign/offboard wizard (r27 access-wizard)
  ```

  The #1433 access/offboarding fix and regression commits above are the task-specific corrections the mission directs us to verify in #1430; no unrelated paths or change set from the stale PR were used. The current PR #1433 was not reviewed or changed.
- Exact remote refs before source review and after review: `8a3f58da905fad52327d33466fde1d9568092519 refs/heads/develop`; `e651cb1c2978c022210c869e6ea6e1e9a43aefa9 refs/pull/1430/head`; `1a36cb2c8dc92cab605d538d07906a933718f5e8 refs/pull/1433/head`.
- PR #1433 is the mission-designated stale duplicate: OPEN, based on `work/r27-access-wizard`, head `1a36cb2c8dc92cab605d538d07906a933718f5e8`, merge state DIRTY/CONFLICTING. It was not used as the review candidate and was left unchanged.
- Hosted checks on exact PR #1430 head: run `42399764027`. Fourteen passed: `wizard-registration-tests`, `documentation-audit`, `go-unit-tests`, `go-build`, `go-vet`, `cli-gofmt`, `mkdocs-en-strict`, `mkdocs-de-strict`, `pages-candidate-build`, `PR Selected Checks`, `PR · Trusted Plan`, `PR · Focused Python`, `PR · Source format`, and `Workflow policy`. Ten path-specific/nonselected checks were skipped, including HA Docker/Podman; none failed. No CI rerun or local test was started by this review.
- Planning repository verified before the evidence commit: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` returned `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`. `origin` fetch/push is `https://github.com/mcpdev80/baseharbor-plan.git`.
- Pre-publish `origin/main` witness: `93148b364ed433f79010b16d5cb6a9599c93de8c refs/heads/main`.
- Product candidate remained `e651cb1c2978c022210c869e6ea6e1e9a43aefa9` at post-review `ls-remote`; no product or PR mutation occurred.

## Repository-rule compliance

This was a read-only product review. No local tests, CI rerun, workflow dispatch, merge, or runner/VM operation was performed. Evidence is stored only in canonical `baseharbor-plan`. Existing unrelated planning modifications and untracked evidence were left untouched and will not be staged.

END_BLOCKED 0427-access-wizard-review: REQUEST-CHANGES; PR #1430 has no durable assignment/revocation write, selection cancel can invoke the mutation callback, multi-target actions are truncated to index zero, and three required offboarding scopes have no production route.

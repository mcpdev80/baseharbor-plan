# CODEX-REVIEW 0427-access-r3-review — PR #1430

## PLAN

1. Read the r3 mission and record the numbered plan — done.
2. Read task contract; fetch exact PR/base refs; inspect persistence, cancel, multi-target, offboarding fail-closed, write-set, docs/registration, and hosted CI without reruns — done.
3. Record SHA-specific verdict and actionable recipe in canonical planning evidence — done.
4. Publish evidence to origin/main, verify evidence and unchanged candidate witnesses, then post END — in progress.

## Candidate and hosted evidence

- Planning repository root: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; origin fetch/push: `https://github.com/mcpdev80/baseharbor-plan.git`.
- PR #1430 is OPEN, base `develop`, head `5ccb81472ef1a9ca53e065c94ccd89987fa05211`; `git ls-remote` returned develop `8a3f58da905fad52327d33466fde1d9568092519` and PR head `5ccb81472ef1a9ca53e065c94ccd89987fa05211`.
- `git merge-base --is-ancestor 8a3f58da905fad52327d33466fde1d9568092519 5ccb81472ef1a9ca53e065c94ccd89987fa05211` exited 0. The PR API reports CLEAN and MERGEABLE.
- The 16-file delta contains the access wizard, its tests, root registration, machine-coverage classification, generated EN/DE command and machine indexes, and the authorized additive seam in `internal/orgconfig/profiles.go`. It contains no in-product evidence file and no `.github/**` change. No unrelated lifecycle/fixture/OCI files changed.
- Hosted run `42418196689` is terminal success on exact head `5ccb81472ef1a9ca53e065c94ccd89987fa05211`. `PR · Validation · go-unit-tests`, `go-build`, `go-vet`, `cli-gofmt`, `documentation-audit`, `mkdocs-en-strict`, `mkdocs-de-strict`, `pages-candidate-build`, `wizard-registration-tests`, `PR · Focused Python`, `PR · Source format`, `PR · Trusted Plan`, `Workflow policy`, and `PR Selected Checks` passed. Runtime-targeted jobs were skipped. The existing PR Go unit job runs `scripts/pr-unit-database.sh`, which executes `go test ./... -count=1`; the registration job covers command tree, machine classification, and generated human documentation. These were pull-request checks on the candidate; none was rerun for this review.
- The candidate worktree was detached at `5ccb81472ef1a9ca53e065c94ccd89987fa05211` and remained unchanged. No local tests were run.

## Findings by acceptance point

1. **Production persistence: PASS.** The CLI builds the active `orgconfig.Manager` and passes `resolveActive`; `ResolveAssignment` and `RevokeAssignment` persist through `orgconfig.PersistActive`/`SaveActive` (`cmd/baha/access_wizard_command.go:47-52, 66-73, 115-135`; `internal/accesswizard/authority.go:74-87, 99-135`; `internal/orgconfig/profiles.go:580-590`). CLI tests reload active state after assignment and offboarding (`cmd/baha/access_wizard_persistence_test.go:99-159`).

2. **Cancel: PASS.** Cancel after selection returns before invoking the mutation callback (`internal/accesswizard/persistence_cancel_test.go:70-93`). The production CLI regression confirms the existing profile remains and the new assignment is absent after cancellation (`cmd/baha/access_wizard_persistence_test.go:161-183`).

3. **Multiple Targets: REQUEST-CHANGES.** The selection parser preserves multiple names, but persistence does not. `orgconfig.Manager` stores profiles in `map[string]Profile` keyed only by the person/profile name (`internal/orgconfig/profiles.go:276-289`); `Create(..., replace=true)` overwrites that one key (`:412-437`); each CLI loop iteration creates the same name with one `Target` and persists the whole manager (`cmd/baha/access_wizard_command.go:58-80`; `internal/accesswizard/authority.go:58-87`). The final assignment therefore retains only the last selected Target. Offboarding likewise revokes that same person-keyed entry and persists inside each loop iteration (`cmd/baha/access_wizard_command.go:126-139`, `internal/accesswizard/authority.go:105-135`), so later selections can fail after an earlier removal was already saved. The added test checks parsing two selections (`internal/accesswizard/persistence_cancel_test.go:243-273`), not production persistence for 1/2/3 Targets.

   Remediation: in `cmd/baha/access_wizard_command.go` and the access-profile model/persistence boundary, represent the selected person’s grants per Target rather than replacing one person-keyed profile on every iteration; validate all selected operations first and persist the complete change once so offboarding cannot leave partial writes. Add table-driven CLI tests for 1, 2, and 3 selected Targets that reload active state and assert every intended grant/removal remains. Stop criterion: the reloaded production state contains the full requested target set, and a failure on any target leaves the store unchanged.

4. **Unsupported offboarding kinds: REQUEST-CHANGES.** The command currently routes every `access offboard PERSON` review directly to `RevokeAssignment` (`cmd/baha/access_wizard_command.go:102-139`), with no removal-kind question. The `RemoveKind`/`OffboardRequest` definitions are not connected to that route; `ValidateOffboard` also has no default rejection for an unknown kind (`internal/accesswizard/wizard.go:81-123, 186-201`). Thus the UI cannot distinguish owned-grant removal from connection removal, device revoke, or managed-user disable/delete, and the generic offboard action silently selects the grant-revoke path.

   Remediation: wire an explicit removal-kind choice into the wizard. This slice may execute only the supported owned-grant path; connection, device, managed-user, and unknown kinds must return a typed unsupported result before invoking a mutator or saving state, with managed-user routing left to `t-20261018-r27-managed-users`. Add CLI-level tests for every unsupported kind that assert no profile change and no route invocation. Stop criterion: no unsupported category can be silently mapped to grant revocation; the owned-grant route remains scoped to the reviewed person and Target.

## Hygiene and verdict

- Root command registration (`cmd/baha/commands.go`) and access assign/offboard machine-coverage exclusions are present. EN/DE command indexes and machine-coverage indexes contain matching entries; hosted `wizard-registration-tests` and documentation audit passed.
- New Go tests are included by the existing pull-request `go test ./...` unit job. No workflow changes or CI weakening were made.
- No VM smoke test was named. No tests, checks, or workflows were run locally or rerun during this review.

REQUEST-CHANGES for PR #1430 at `5ccb81472ef1a9ca53e065c94ccd89987fa05211`: production persistence and cancel behavior pass, but multi-target persistence and fail-closed offboarding-category handling do not meet the contract. The two remediation recipes and stop criteria are listed above.

END BLOCKED 0427-access-r3-review: request-changes; candidate `5ccb81472ef1a9ca53e065c94ccd89987fa05211`.

## Publication witness

- `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-07/access-wizard/act-1430-r3-review.md` returned exactly: `100644 blob 4e059286e38aa2a63955395c6d73c2cb469f4042 evidence/r27-welle5-folge-2026-11-07/access-wizard/act-1430-r3-review.md`.
- The evidence commit `20810abd` is an ancestor of fetched `origin/main` (`d9150f667e1534fa2b11395bef5550cd9e9877cb`); the coordinator's subsequent commit moved the 110-lane state block and did not alter this review file.
- Final candidate witness before END remains develop `8a3f58da905fad52327d33466fde1d9568092519`, PR #1430 head `5ccb81472ef1a9ca53e065c94ccd89987fa05211`.
- A concurrent planning update carried the same initial tree witness. Final post-rebase tree and remote-main witnesses are recorded below after publication.


## PLAN — r4 review

1. Read the r4 mission and establish the numbered review plan — done.
2. Read round-4 evidence from planning origin/main; verify exact PR/base refs and ancestry — done.
3. Inspect disputed r3 findings 1–3 and the new fail-closed guard finding 4 against candidate source and tests — done.
4. Record the exact verdict and correction recipe in this planning act, publish, verify the candidate unchanged, then post END — done.

## R4 sha-specific re-review — CODEX-REVIEW PR #1430

### Verdict: REQUEST-CHANGES

Reviewed exact PR head `be65de6da3ffd15e79fc6479dff8c81a8fcb81cd`, base develop `8a3f58da905fad52327d33466fde1d9568092519`. Fresh `git ls-remote` before review returned those exact refs. `git merge-base --is-ancestor 8a3f58da905fad52327d33466fde1d9568092519 be65de6da3ffd15e79fc6479dff8c81a8fcb81cd` exited 0. `git merge-base --is-ancestor 5ccb81472ef1a9ca53e065c94ccd89987fa05211 be65de6da3ffd15e79fc6479dff8c81a8fcb81cd` also exited 0; the round-4 evidence reports the single added commit `be65de6d fix(access-wizard): r4 fail-closed unimplemented offboarding removal kinds` atop that candidate. Candidate source was inspected detached and not changed.

1. **Active-state persistence: PASS.** `ResolveAssignment` mutates the policy Manager, reloads active state, and calls `orgconfig.PersistActive` (`internal/accesswizard/authority.go:82-96`); `PersistActive` folds the owned profile set into `state.Config.Profiles` and calls `SaveActive` (`internal/orgconfig/profiles.go:580-590`). CLI tests reload durable state after assignment and managed-user removal (`cmd/baha/access_wizard_persistence_test.go:99-159`). This verifies persistence for the single-target path.

2. **Cancellation: PASS.** The controller returns on selection or confirmation cancellation before calling `decide` (`internal/accesswizard/controller.go:160-165, 188-206`). The CLI regression cancels after selecting a target and verifies the existing profile remains while the proposed assignment is absent (`cmd/baha/access_wizard_persistence_test.go:161-182`).

3. **Multiple-target persistence: REQUEST-CHANGES; the r4 rebuttal does not fix the r3 finding.** The CLI does iterate every selected assignment (`cmd/baha/access_wizard_command.go:63-80`), but each iteration calls `ResolveAssignment` with the same `review.Person.Name`, a single `sel.TargetName`, and `replace=true` (`:66-73`). That creates a profile with exactly one Target (`internal/accesswizard/authority.go:66-74`). The Manager is keyed by profile name/person (`internal/orgconfig/profiles.go:276-289`); replacement writes `m.profiles[p.Name] = created` (`:426-437`). Consequently, each iteration overwrites the preceding Target and the final persisted set retains only the last selection. The new evidence's claim that looping means all targets are persisted is disproven by these lines.

   Offboarding also loops (`cmd/baha/access_wizard_command.go:129-142`), but `RevokeAssignment` removes the person-keyed profile and persists it during the first iteration (`internal/accesswizard/authority.go:129-150`). A second selected Target then fails `manager.Get(person)` (`:129-132`) after the first removal has already been persisted. The parser test covers two parsed selections only (`internal/accesswizard/persistence_cancel_test.go:243-273`); the production reload test covers one Target only (`cmd/baha/access_wizard_persistence_test.go:185-204`).

   Recipe: change the access profile representation/manager boundary (`internal/orgconfig/profiles.go`, `internal/accesswizard/authority.go`) and CLI transaction (`cmd/baha/access_wizard_command.go`) so a person can retain the intended grants for multiple Targets. Validate the complete selection first, then persist once atomically; for offboarding, do not persist a first removal before validating and applying later selections. Add table-driven CLI persistence tests for 1, 2, and 3 Targets on both assignment and offboarding; reload active state and assert the full requested set. Add a later-target failure case proving no partial state was written. Stop criterion: every selected Target survives reload, and any rejected selection leaves the active store unchanged.

4. **Unsupported offboarding kinds: PASS for the scoped fail-closed guard.** `RevokeAssignment` enters the only production mutation branch for `RemoveManagedUser` (`internal/accesswizard/authority.go:121-152`) and returns an error wrapping `ErrDenied` for every other kind (`:154-160`). The CLI explicitly passes `RemoveManagedUser` (`cmd/baha/access_wizard_command.go:133-139`); search of non-test `internal/accesswizard` and `cmd/baha` references found no alternate production route that maps connection/device/grant kinds to that mutation. The regression enumerates `RemoveConnection`, `RemoveDevice`, and `RemoveGrant`, checks `errors.Is(err, ErrDenied)`, and checks profile count/name remain unchanged (`internal/accesswizard/offboard_scope_regression_test.go:61-81`). Removing the kind guard would take the managed-user branch, return nil after revocation, and fail the test's `err == nil` assertion at line 71. This review did not execute that mutant or rerun tests.

### Scope, indices, and hosted evidence

- The incremental diff from prior head `5ccb81472ef1a9ca53e065c94ccd89987fa05211` to this head is exactly four files: `cmd/baha/access_wizard_command.go`, `internal/accesswizard/authority.go`, `internal/accesswizard/offboard_scope_regression_test.go`, and `internal/accesswizard/persistence_cancel_test.go`. No `.github/**`, runtime, or unrelated-card paths are changed in this incremental delta. The broader candidate retains the command registration and matching English/German command and machine-coverage indexes (`cmd/baha/commands.go:170`; `docs/cli/command-index.md:12-14`; `docs/de/cli/command-index.md:12-14`; `docs/reference/cli-machine-coverage.md:10-12`; `docs/de/reference/cli-machine-coverage.md:10-12`). The r4 diff does not remove or weaken an existing assertion; it updates the explicit `RemoveKind` argument and adds the fail-closed case.
- Hosted run `42421669238` was independently read via `gh run view`; it is `completed/success`, event `pull_request`, exact `headSha` `be65de6da3ffd15e79fc6479dff8c81a8fcb81cd`. Round-4 evidence lists `PR · Validation · go-unit-tests`, build, vet, gofmt, source format, registration, docs and selected checks passing. No CI was rerun and no local test/gate was run. The regression's future CI coverage is the pull-request `go-unit-tests` job.
- Evidence source: planning `origin/main` round-4 file `evidence/r27-welle5-folge-2026-11-07/access-wizard/round-4.md`; its reported PR checks are tied to the exact head above.
- Planning root verification before this evidence commit: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` returned exactly `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `origin` fetch and push are `https://github.com/mcpdev80/baseharbor-plan.git`.
- No local tests, CI reruns, workflow changes, candidate edits, tags, releases, or VM actions were performed by this review.

### Corrective recipe and stop criterion

Keep REQUEST-CHANGES for the multiple-target defect. Implement the per-person/per-target state representation and batch atomic persistence in the three files named above. Tests must cover all 1/2/3 assignment and offboarding selections by running the CLI and reloading active state, plus atomic no-write on a later-target failure; the PR `go-unit-tests` job must execute them on the pull-request trigger. Stop when the complete selected target set is durable and failed selection leaves no partial write. Findings 1, 2, and 4 are accepted as described; no further issue is raised for those points.

END BLOCKED 0427-access-r4-review: REQUEST-CHANGES; PR #1430 `be65de6da3ffd15e79fc6479dff8c81a8fcb81cd`; multi-target assignment overwrites earlier Targets and multi-target offboarding can persist a partial removal.

## R4 publication witness

Pre-publication `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-07/access-wizard/act-1430-r3-review.md` output:

```text
100644 blob 38ce64afd88dbc224c482310bc0a74e5eba9fa43	evidence/r27-welle5-folge-2026-11-07/access-wizard/act-1430-r3-review.md
```

Planning `origin/main` before this evidence commit: `26112d6f78341d1a9cb16f5134ed7d7c578e6ab5`. Candidate pre-publication witness: develop `8a3f58da905fad52327d33466fde1d9568092519`, PR #1430 `be65de6da3ffd15e79fc6479dff8c81a8fcb81cd`.

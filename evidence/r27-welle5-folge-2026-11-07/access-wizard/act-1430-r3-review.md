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

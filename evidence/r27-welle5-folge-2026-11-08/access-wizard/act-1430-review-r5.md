# CODEX-REVIEW — 0427-013 access-wizard r5 — PR #1430

## PLAN

1. Fetch the exact PR head and develop refs; verify CI and read round-5 source evidence from planning origin/main.
2. Inspect the multi-target production transaction and tests, verify r3 persistence/cancel/multi-target findings and r4 fail-closed offboarding behavior, and check the exact source diff.
3. Record the verdict and executable correction recipe in this act, publish to planning origin/main, then verify the published act and unchanged PR candidate.

## Review verdict: KORREKTUR

Reviewed candidate: PR #1430 head `bd5f2f10838eeadb89bc121a3719427b2bc6c005`. At initial fetch, `develop` was `db06f01e9fd793706da5072769922a0c64afecf0`; that SHA is the requested comparison base in the supplied round-5 evidence. The candidate contains merge commit `419b0211317bab63cb0fa66d07892488685d3ed8` as an ancestor (exit 0). `develop` advanced during this review and the final live ref is `f9e207ac0d0b4c983fbb01d4357a8784c41c92de`; this latest tip is not an ancestor of the PR head. The initial PR API query reported OPEN, MERGEABLE, CLEAN. After develop advanced, the final PR API query reported OPEN with mergeability and merge-state `UNKNOWN`. The exact source delta was reviewed against the fetched `db06f01e...` develop snapshot; this review does not attest the candidate is rebased on the newer `f9e207ac` tip.

Hosted run `42431094421` is terminal `completed/success` on the exact head `bd5f2f10838eeadb89bc121a3719427b2bc6c005`. `PR · Validation · go-unit-tests` and `PR Selected Checks` both succeeded; the run's other selected source, build, vet, gofmt, docs and wizard-registration jobs passed. Runtime-targeted jobs were skipped. No tests were run or CI rerun by this reviewer.

## Finding 5 — multi-target all-or-nothing behavior

The command now applies every reviewed selection to one in-memory manager and persists once after the complete loop (`cmd/baha/access_wizard_command.go:54-85` for assignment and `:125-153` for offboarding). The model now keys profiles by `(name,target)` (`internal/orgconfig/profiles.go:249-255,321-329,441-460,524-555`), and `CommitActive` is reached only after each selected operation validates. A failure in a later offboard selection returns before commit.

The production-path regressions verify assignment across three targets and reload each `(person,target)` profile (`cmd/baha/access_wizard_persistence_test.go:243-285`), successful offboarding across two targets (`:287-307`), and a later-target offboarding failure including byte-identical active-state JSON (`:309-358`). The test therefore establishes offboarding rollback at the persistence boundary; the implementation's assignment loop also defers persistence until all selections succeed, though there is no corresponding CLI test that makes a later assignment target fail and asserts byte-identical state. Add that complementary regression as part of the corrective round if the test setup can produce a production-authority denial on a later selected target.

## Prior r3 findings — status

- Persistence: the confirmed assign/offboard route calls `CommitActive`, then `orgconfig.PersistActive` and `SaveActive` (`internal/accesswizard/authority.go:137-148`; `internal/orgconfig/profiles.go:615-625`). The CLI tests reload active state after successful assignment and offboarding (`cmd/baha/access_wizard_persistence_test.go:135-195`). Writer failures return an error and the controller fails closed. However, the persistence merge currently loses profiles owned by another installation; see blocking finding below.
- Cancellation: the controller asks for explicit `yes` after rendering the review; `cancel` returns before invoking the mutation callback (`internal/accesswizard/controller.go:183-206`). `TestCancelAfterSelectionNeverInvokesCallback` verifies the callback is not run (`internal/accesswizard/persistence_cancel_test.go:70-93`), and the CLI cancellation regression verifies no profile is persisted (`cmd/baha/access_wizard_persistence_test.go:197-219`). PASS.
- Multi-target behavior: selection processing is no longer truncated to the first item; production reload tests verify each requested target. The multi-target persistence behavior from r3 is materially addressed, subject to the preservation defect below.
- r4 fail-closed offboarding correction remains: `RevokeAssignment` implements only `RemoveManagedUser` and denies other removal kinds (`internal/accesswizard/authority.go:112-159`). `TestOffboardUnimplementedKindFailsClosedNoSilentMutation` checks errors.Is(ErrDenied) and unordered profile-set equality for unsupported kinds (`internal/accesswizard/offboard_scope_regression_test.go:61-86,89-111`).

## Blocking finding — successful persistence deletes foreign-owner profiles

`ManagerFromActive` sets the manager owner from `state.Config.Organization` and only loads profiles owned by that installation or legacy rows without an owner (`internal/orgconfig/profiles.go:348-363,406-415`). But `PersistActive` replaces the entire active config profile map with `ProfileMap(manager.SnapshotProfiles())` (`internal/orgconfig/profiles.go:615-625`). Therefore, when the active config contains a profile with a non-empty `Owner` belonging to another installation, a successful access assignment or offboarding omits that profile from the manager snapshot and deletes it from the saved configuration. `Profile.Owner` is explicitly the installation identity recorded for ownership/audit (`internal/orgconfig/profiles.go:126-129`); `LoadProfiles` explicitly skips foreign-owned records rather than managing them. Existing CLI tests seed only the active owner's and ownerless profiles, so they do not catch this loss (`cmd/baha/access_wizard_persistence_test.go:17-38,313-358`). This violates the prior review's preservation boundary while fixing the current owner's batch operation.

### Correction recipe

- Files: `internal/orgconfig/profiles.go:615-625` and `cmd/baha/access_wizard_persistence_test.go`.
- Change: make `PersistActive` merge the manager's updated owned `(name,target)` snapshot into the freshly loaded profile map while retaining every profile whose non-empty `Owner` differs from `manager.Owner`. Do not clear or rewrite another installation's rows. Preserve existing semantics for current-owner and supported legacy ownerless rows.
- Tests: add production CLI persistence regressions for successful assign and offboard seeded with both active-owner and foreign-owner profiles; reload the active config and assert the foreign profile's complete definition and key remain unchanged while only the selected owned rows change. Add a later-target assignment-denial regression asserting the serialized active state is byte-identical if a production-reachable denial can be constructed.
- Stop criterion: assignment and offboarding preserve every foreign-owner profile exactly, mutate only the active owner's intended `(name,target)` rows, and failed multi-target operations leave active-state bytes unchanged. Re-run the focused Go suites and obtain a terminal hosted PR run on the corrected exact head before acceptance.

## Exact diff and evidence

The three-dot source delta against fetched develop `db06f01e9fd793706da5072769922a0c64afecf0` is 19 files: access-wizard CLI/tests, `internal/accesswizard`, `internal/orgconfig`, `internal/policy`, and the associated CLI/machine-coverage docs. There are no `.github/**` changes. `git merge-base --is-ancestor 419b0211317bab63cb0fa66d07892488685d3ed8 <candidate>` returned 0; `git merge-base --is-ancestor db06f01e9fd793706da5072769922a0c64afecf0 <candidate>` returned 1 because develop had advanced past the candidate's integration base. The PR API reported mergeable/CLEAN at review time.

Round-5 source evidence was read from planning `origin/main`: `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-08/access-wizard/round-5.md` returned exactly `100644 blob d83aafad3ac0501da2eea29294d51802800366cc evidence/r27-welle5-folge-2026-11-08/access-wizard/round-5.md`; the evidence commit `343391df` was not claimed here because the tree witness, not that abbreviated commit, is the verified source identity.

Canonical planning root verification: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` returns `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; origin fetch/push is `https://github.com/mcpdev80/baseharbor-plan.git`.

The product candidate was read-only throughout review. No test, workflow, PR, branch, tag, or product-file mutation was performed.

END_DONE 0427-access-wizard-review-r5: KORREKTUR; PR #1430 candidate `bd5f2f10838eeadb89bc121a3719427b2bc6c005`; persistence drops profiles owned by another installation during successful writes.

Planning validation: `python3 scripts/plan.py render && python3 scripts/plan.py check` completed with 0 errors and 1 unrelated warning about `t-20261107-r27-runtime-broker-oras-missing-edge-readiness` depending on an unaccepted task. Rendered task/view files were restored; only this review act is staged.

# CODEX-REVIEW — 0427-124 target-env r1 — PR #1451

## PLAN

1. Fetch exact PR/develop refs, verify the hosted run, and read the current task card and round-1 evidence from planning origin/main.
2. Inspect the production target reader, regression tests and CI selection; compare the explicit greenfield acceptance clause and the target-selection documentation to their implementation.
3. Record the sha-specific review verdict and correction recipe, publish this act to canonical planning origin/main, then verify publication and unchanged product refs.

## Verdict: REQUEST-CHANGES for card-level acceptance

The one-file PR is a valid production-path regression slice, and its tests passed on the exact candidate. The complete card acceptance is not met: it explicitly requires an isolated greenfield run on docker-2 without touching shared-plane objects. Round-1 evidence says no Docker/Podman VM journey was run and documents that fresh-target `use`/`target activate` fails closed before a Core management connection exists. The Planning task is still in `review`, not accepted. Split the completed target-selection proof from the unfinished greenfield Core/owner bootstrap journey; do not close or accept the whole card on this candidate alone.

Candidate: PR #1451, head `ebdf8d5db0122620b7d2e5c57d8dc48a2c6148f3`, base `develop`. Final live refs: develop `1fe57f25007413c710e049094c62bf71656b2aa2`, PR head `ebdf8d5db0122620b7d2e5c57d8dc48a2c6148f3`. The candidate contains the stated integration base `419b0211317bab63cb0fa66d07892488685d3ed8` (ancestor check exit 0); current develop tip is not an ancestor (exit 1). The final PR API query reports OPEN, MERGEABLE, CLEAN.

Hosted run `42433354279` is completed/success on the exact head. Its `PR · Validation · cli-package-tests` job and `PR Selected Checks` both succeeded. The `cli-package-tests` group executes `go test ./cmd/baha -count=1` through the existing PR validation runner; the new test file is in `cmd/baha` and is discovered by that package run on the `pull_request` trigger. No workflow was edited or rerun, and this reviewer did not run tests.

## Production ENV reader and regression: PASS

The production resolver reads `BASEHARBOR_TARGET` in `cmd/baha/target.go:87-95` and passes it to `selectedTargetName`. That resolver applies explicit `--target`, then ENV, persisted selection, configured default, then the single-target/fail-closed fallback (`cmd/baha/target_selection.go:59-89`). Production app-up resolves through `executeApplicationUpLifecycle` → `resolveApplication` → `effectiveTarget` (`cmd/baha/app_up_lifecycle.go:34-76`, `cmd/baha/app_input_resolver.go:95-100`); app status and control-plane status also resolve through the same production helper.

The exact PR diff against fetched develop contains only `cmd/baha/target_environment_production_path_test.go` (112 added lines). `TestAppStatusHonorsEnvironmentTargetThroughProductionCLI` calls `runWithIO` on `baha app status` with two configured targets and `BASEHARBOR_TARGET=iso-b`; it fails if the real CLI path sees the multiple-target conflict (`:43-67`). Additional production-path tests check explicit `--target` precedence and environment selection origin/state-root isolation (`:69-112`). The tests provide durable coverage for target resolution; they do not exercise a Core bootstrap or a greenfield `app up` lifecycle.

## Greenfield clause: NOT MET; split the card

The authoritative card `tasks/t-20261108-bughunt-0427-target-env-ignored.md` has conjunctive acceptance: production command paths honor `BASEHARBOR_TARGET`, an isolated greenfield run on docker-2 completes without shared-plane effects, and a regression proves the production read. The first and third points are evidenced by production source plus PR #1443/#1451 and this run. The second is explicitly open in round-1 evidence and has no native VM transcript.

`baha use` aliases `target activate` (`cmd/baha/use_target.go:24-38`). Explicit activation calls `bindExplicitSelectionToConnection` before writing the selection (`cmd/baha/target.go:273-289`); a target with no verified Core installation returns a fail-closed conflict (`cmd/baha/use_target.go:72-90`). That owner-recovery/greenfield bootstrap is separate from selecting an already configured target through `BASEHARBOR_TARGET`. Do not weaken this guard or borrow another target's Core authority to satisfy the selection card.

## Documentation/help consistency: correction needed

The English and German target-selection diagrams mention the environment override but omit the persisted target between ENV and configured default (`docs/explanation/targets.md:142-152`; `docs/de/explanation/targets.md:163-171`). Also, the `target activate` help text says `--target` and `BASEHARBOR_TARGET` override persisted selection (`cmd/baha/target.go:259-263`), while that command handler validates and persists its explicit NAME directly (`:273-289`); it does not resolve the ENV selector. Clarify that these overrides select the target for subsequent commands, not the target being explicitly activated. The PR makes no documentation/help changes. Update both diagrams to show the actual resolution order: explicit override, ENV, persisted target, configured default, then single-target/local fallback or conflict. Run the existing documentation audit and CLI help regression in CI after those changes.

## Correction recipe and stop criteria

- Planning scope: split `t-20261108-bughunt-0427-target-env-ignored` into a target-selection/precedence slice and a distinct greenfield Core bootstrap/owner-recovery slice. Keep PR #1451 as evidence for the first slice; do not mark the parent acceptance complete until both outcomes have their own evidence. The follow-up greenfield task should record its dependency on the relevant Core/owner-authority work rather than widening this test-only PR.
- Help/docs: clarify `cmd/baha/target.go:262` so `target activate NAME` is described as an explicit persisted selection, while ENV/`--target` override the persisted selection for subsequent target-resolving commands. Update `docs/explanation/targets.md` and `docs/de/explanation/targets.md` to insert persisted selection between ENV and configured default. Preserve fail-closed target selection.
- Test requirement: retain the current production CLI regression and its passing `PR · Validation · cli-package-tests` coverage. For the split greenfield task, run the exact isolated `baha app up --control-plane-only` journey on the host named by the acceptance contract (docker-2 per round-1 evidence) and record its output and proof that shared-plane objects were untouched. Any new reusable test must also be selected by GitHub CI; workflow changes remain outside this review's write scope.
- Stop criterion: the target-selection slice is accepted only with the documented precedence and exact-head CI green. The greenfield slice remains open until its isolated native run succeeds without cross-target/core-owner borrowing and its durable CI coverage is recorded. No whole-card acceptance before both slices meet their criteria.

## Evidence provenance

- Round-1 evidence was read from planning origin/main. `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-08/bughunt-target-env/round-1.md` returned `100644 blob 7e929e4bbb758dabaebab459a2cf43d46b0a11be evidence/r27-welle5-folge-2026-11-08/bughunt-target-env/round-1.md`.
- Canonical planning root verification: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` returned `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`. Its origin fetch and push URLs are `https://github.com/mcpdev80/baseharbor-plan.git`.
- Initial planning `origin/main` witness was `4f8e83d298510e42363dbf9f6435d6d58e349012 refs/heads/main`; before commit, current `origin/main` was fetched/rebased to `dfb8e7a8d9cb685c31f0c097b91acb911370fe3a refs/heads/main`.
- Candidate remained unchanged during review; final `git ls-remote` returned develop `1fe57f25007413c710e049094c62bf71656b2aa2` and PR head `ebdf8d5db0122620b7d2e5c57d8dc48a2c6148f3`.
- No product files, PR metadata, workflow files, branches, tags or test VMs were changed or started by this reviewer. The RAM-scratch note in round-1 evidence is informational and is not a finding against this candidate.

END_DONE integration-1451-review: REQUEST-CHANGES for card-level acceptance; target selection proof passes, greenfield acceptance remains unmet and must be split from it; candidate `ebdf8d5db0122620b7d2e5c57d8dc48a2c6148f3`.

Planning validation: `python3 scripts/plan.py render && python3 scripts/plan.py check` completed with 0 errors and 1 warning about an unrelated accepted runtime-broker task depending on an unaccepted VM-integration task. Render produced no tracked-file changes.

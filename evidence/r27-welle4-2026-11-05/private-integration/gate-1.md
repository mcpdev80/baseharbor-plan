# CODEX-GATE — PR #1379 draft->ready + selected-check observation at exact head

Lane: w166-private-gate. Coord: f49a3303. Card: t-20261104-r27-private-integration-path.
Candidate branch: work/r27-private-integration (PR #1379). Reviewed head: 52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9.

## PLAN

- Confirm PR #1379 is DRAFT with head exactly 52be57c9893 (remote ref match)
- Set PR #1379 from draft to ready via `gh pr ready 1379 -R mcpdev80/baseharbor`
- Trigger + observe a new run to terminal state; record run-id and the named `PR Selected Checks` status; no rerun rat
- Verify run head SHA is exactly 52be57c9893 via ls-remote + a run log line listing only own commits
- Both mode cells (shared/geteilt vs private/privat) evidenced at the new head via run/logs, not just locally
- Write this evidence file; post END to f49a3303

## Step 1 — PR state confirmed

Remote ref and PR head both fixed at `52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9`:

- `git ls-remote origin work/r27-private-integration` -> `52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9 refs/heads/work/r27-private-integration`
- `gh pr view 1379` -> state=OPEN, isDraft=true, headRefOid=52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9, baseRefName=develop

The write set is eight files (manifest.go, manifest_parse.go, provider_placement.go, r27_private_integration_test.go, cmd/baha/use_target.go, cmd/baha/use_target_connection_test.go, internal/coreinstallation/selection.go, selection_test.go). Scope contract: ONLY the draft->ready switch + observation. No content change, no base-merge, no .github file touched.

## END

<END_LINE_PLACEHOLDER>

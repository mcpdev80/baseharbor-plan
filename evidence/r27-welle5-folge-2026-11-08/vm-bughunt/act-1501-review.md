# CODEX-REVIEW 0427-144 — PR #1501

## PLAN

1. Verify the live PR head, base, state, hosted workflow, and Planning-vault remote.
2. Inspect the exact candidate diff and trace provider resolution, wizard selection, and conflict reporting through production code.
3. Check the two-app regression, CI selection/execution, and the reported develop-baseline runtime failure.
4. Record the SHA-specific verdict and evidence in the Planning vault, validate, publish to origin/main, and report the published witness.

## Urteil

**ROLLE: REVIEW — APPROVE** for source acceptance at candidate `a6bb99bfa1727b2231c3b226a7069c33abe96a51` against develop `20902f0a6ab016fd8fe6a501751e1becc5f334dd`.

The PR is currently **closed and unmerged** (`state=closed`, `merged=false`, `merged_at=null`); this review does not reopen it or imply that it landed. GitHub reports the same exact head, a clean merge state, and base `20902f0a6ab016fd8fe6a501751e1becc5f334dd`.

## SHA and scope

Live PR API: head `a6bb99bfa1727b2231c3b226a7069c33abe96a51`; base `20902f0a6ab016fd8fe6a501751e1becc5f334dd`; closed, not merged. The hosted run checked the exact head. The candidate diff against develop contains eight files, all under `cmd/baha/` or `internal/application/`; no `.github/**` files are changed.

The live PR review is read-only. No product repository or candidate ref was modified.

## Findings

1. **Resolution uses production union planning and preserves foreign-owner identity.** `cmd/baha/application_provider_plan.go:19-24,27-46` obtains the lifecycle snapshot, lists persisted deployment records, and adds each other deployment as a consumer keyed by `deployment/<DeploymentID>`. `internal/application/provider_union.go:96-103` runs retained-consumer footprint resolution and stores that consumer key on the typed `ResolutionError` before returning the error. This is the real provider-union resolver, not a test-only classification helper.

2. **The user-facing conflict is specific and fail-closed.** `cmd/baha/app_core_requirement.go:150-194` maps that error to `provider_stale_consumer_dependency`, sets `Resource` to the named deployment record, and names both the missing provider realization and the consumer's lifecycle owner in `Next`. It explicitly says no provider was mutated. The error remains typed and preserves the consumer attribution. This meets the card's actionable-conflict branch: the operator gets the exact consumer record and stale realization to take to its owner; no foreign preference is silently rewritten.

3. **The unrelated wizard selection tolerates the foreign residue.** `cmd/baha/app_wizard_controller.go:182-210` calls `appProviderChoicesWithView(..., true)` for the selection surface and leaves planning/preview as the fail-closed authority. The regression `TestForeignRecordDoesNotBlockHttpAppSelection` seeds two apps on one target, reads the production lifecycle snapshot, and proves the independent HTTP-only app still has its offered choice. `TestForeignRecordUnionReportsConcreteConflictWithNextStep` invokes `resolveApplicationProviderPlan`, checks the typed consumer/resource and stale instance in the next step, and confirms the persisted foreign preference is unchanged. `TestForeignRecordStaleReferenceDoesNotPoisonUnrelatedUnionPlan` verifies a registered residue does not block unrelated union planning and that a foreign instance cannot receive a destructive plan action. These tests exercise production snapshot, selection, and union resolver entry points, not only a standalone helper.

4. **CI evidence is exact-head and terminal.** Run [42528721531](https://github.com/mcpdev80/baseharbor/actions/runs/42528721531) reports `completed / success` with `head_sha=a6bb99bfa1727b2231c3b226a7069c33abe96a51`. The `go-unit-tests` job ran the package-wide `go test ./cmd/baha` selection containing the new regression; the focused `wizard-app-edit-tests`, `wizard-controller-tests`, and `wizard-provider-choice-tests` jobs passed, as did PR Selected Checks and the Docker/Podman destroy-retry jobs. The Native Keycloak/Core matrix entry was **skipped**, not passed; it is outside the new resolver regression's unit-test coverage and is not counted as green evidence here.

5. **Reported local native failure is not a candidate regression.** The round-1 dossier records `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` failing on both this candidate and clean develop `20902f0a` with the same `existing native network lacks a protected Core or shared backend owner` message. That is a documented baseline/environment STATE, not a candidate-specific failure. In the exact hosted run, the `wizard-app-edit-tests` job matched and passed that named test. This does not convert the separately skipped Native Keycloak/Core matrix entry into a pass.

## Recipe / stop criterion

No source correction is required for the reviewed acceptance. Keep the typed consumer ID, missing realization ID, and no-mutation guarantee in the error contract; retain the two-app production-resolver regression in the regular `go-unit-tests` selection. A future acceptance relying on Native Keycloak/Core execution must wait for that matrix job to execute and pass on the exact candidate; a skipped job is not a pass. The present candidate has terminal success for its applicable selected checks, with the local baseline-only native failure documented above.

## Evidence references

- Task: `tasks/t-20261108-bughunt-wizard-foreign-records.md`, acceptance requires clean tolerance or a concrete actionable conflict and a two-app mixed-background regression.
- Candidate evidence: `evidence/r27-welle5-folge-2026-11-08/bughunt-wizard-foreign-records/round-1.md`.
- Hosted run: `https://github.com/mcpdev80/baseharbor/actions/runs/42528721531`.
- Planning repository remote verified as `https://github.com/mcpdev80/baseharbor-plan.git` (`origin`).
- Planning `origin/main` before this review commit: `ea0516cd67ddf9fffcdc52ef82e1dd61c39616a2`.

END 0427-144 REVIEW DONE — source verdict APPROVE for `a6bb99bfa1727b2231c3b226a7069c33abe96a51`; PR #1501 is closed unmerged.

## Planning validation

`git diff --check` passed for this evidence. `python3 scripts/plan.py check` reported one pre-existing generated-preview error outside this evidence: `tasks/t-20261108-bughunt-0427-greenfield-isolation.md: generated card preview is stale; run scripts/plan.py render` (with four unrelated dependency warnings). I did not render or modify unrelated Planning files as part of this read-only product review. The review evidence contains no Markdown checkbox lines.

## Planning remote witness before follow-up publication

Command output from `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-08/vm-bughunt/act-1501-review.md`:

```text
100644 blob 872b3ed4920c61ba44b1476f8c8ef78254881aa0	evidence/r27-welle5-folge-2026-11-08/vm-bughunt/act-1501-review.md
```

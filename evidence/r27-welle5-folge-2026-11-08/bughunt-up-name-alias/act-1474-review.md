# CODEX-REVIEW — 0427-130 R5 / PR #1474

## PLAN

1. Read the 0427-130 card, round-5 dossier, and the R4 review stop criterion.
2. Verify the live PR head, base comparison, exact diff, `runWithIO` test, and controlled counterfactual evidence.
3. Verify exact-head hosted checks and identify the CI group and trigger that execute the new test.
4. Record the verdict and native-cell scope decision in this act.
5. Publish only this review evidence file to baseharbor-plan origin/main and verify its remote tree entry.

## Review basis

- Role: REVIEW. Card: 0427-130, `t-20261108-bughunt-0427-up-name-alias-parity`.
- PR #1474 is open, non-draft, base `develop`, live head `8bb8cc0e8565b88e89f1ecab5ad1c8fd6853b306`, `CLEAN` and `MERGEABLE`.
- Live `develop`: `4786c541743541e7550f2c214f143ac8ee4f0aa6`. GitHub compare reports one candidate commit and 28 base commits beyond common ancestor `b73a13a909b2d7b811d6956b3bdaf93f17b80454`. The exact-head test job fetched base `4786c541743541e7550f2c214f143ac8ee4f0aa6`; this test-only change was validated against current develop.
- Exact diff: one file, `cmd/baha/runtime_ports_test.go`; no production or `.github/**` files changed.
- Exact-head run [42482853636](https://github.com/mcpdev80/baseharbor/actions/runs/42482853636) is terminal `success`, event `pull_request`, head exactly `8bb8cc0e8565b88e89f1ecab5ad1c8fd6853b306`.
- Passing relevant jobs: `PR · Validation · cli-package-tests` (job `128738413852`), `cli-vet`, `cli-build`, `cli-gofmt`, `source-contracts`, and `PR Selected Checks` (job `128740762857`). The `cli-package-tests` log records `matched_tests: ["./cmd/baha"]`; this includes the new test in `runtime_ports_test.go`.
- Trigger and selection: the run is a `pull_request` event; `cmd/baha/runtime_ports_test.go` is executed by `PR · Validation · cli-package-tests` through the `./cmd/baha` package selection.
- Planning base before this evidence commit: `e587649e76c81f03790bb6293b55b03198f4e150 refs/heads/main`.

## R4 stop-criterion review

The prior R4 act required all three name-path claims to enter through `runWithIO`, with a controlled case showing that removing `upNameArgs()` threading makes the test fail, followed by terminal green unit and selected checks on the exact head.

`TestUpNameResumesThroughCommandEntrypoint` at `cmd/baha/runtime_ports_test.go:316-387` meets that criterion:

1. It seeds a registered deployment, changes to a directory outside the repository, and invokes top-level `up NAME --yes --skip-memory-preflight --plain` using `runWithIO` (`:334-350`). The check rejects the `no registered deployment` result that would occur if the top-level NAME were not threaded to the resolver.
2. From the same outside-repository context it invokes `app up NAME` through `runWithIO` and verifies the registered name is accepted through that command path too (`:353-368`). The existing parser-parity test remains in the package.
3. It invokes top-level `up does-not-exist-xyz` through `runWithIO` inside the repository and asserts the resolver's `no registered deployment` failure (`:370-385`).

The round-5 dossier records the controlled counterfactual: changing `upNameArgs()` to always return `nil` makes the new test fail because the unknown name proceeds past the expected resolver rejection; restoring the argument threading restores the passing behavior. The production path at `cmd/baha/runtime_repository_up.go:46-48` passes `upNameArgs(opts.Name)` into `resolveApplication`.

## Native-cell scope

The run skipped Native Keycloak/Core, Selected Runtime, and targeted HA Docker/Podman. These skips do not block this review: card 0427-130 requires parser/CLI parity and a command-entry regression, and the R4 stop criterion specifically calls for the `cmd/baha` unit test plus `PR Selected Checks`. The new test is daemon-free and proves NAME routing to the production resolver; no native runtime cell is required by this contract. Therefore there is no workflow-routing finding for the owner and no lane correction request for a skipped native cell.

## Verdict

**ROLLE: REVIEW — URTEIL: approve.** The command-entry regression is present on the exact candidate, covers registered NAME, alias parity, and unknown-name fail-closed behavior through `runWithIO`, and the round-5 dossier records the counterfactual that demonstrates the test fails without argument threading. The exact-head `cli-package-tests` and `PR Selected Checks` are terminal green. The old R4 stop condition is met; skipped native cells are outside the required contract.

## Acceptance-preserving recipe and stop criterion

- No product correction is requested. Keep `TestUpNameResumesThroughCommandEntrypoint` in `cmd/baha/runtime_ports_test.go` and keep it selected by `PR · Validation · cli-package-tests` on `pull_request`.
- Preserve the parser-parity tests and the `upNameArgs(opts.Name)` production handoff. Do not weaken unknown-name fail-closed behavior.
- Stop criterion is met for this review: exact head `8bb8cc0e8565b88e89f1ecab5ad1c8fd6853b306`, terminal passing `cli-package-tests`, and passing `PR Selected Checks` on run 42482853636.

## Repository-rule compliance

- Product sources, PR refs, and hosted checks were inspected read-only. No product files, branches, workflows, CI runs, or runtime hosts were changed or triggered by this review; no local tests were run.
- Evidence is stored only in baseharbor-plan. No compose project was started.
- `python3 scripts/plan.py check` on fetched planning main reported 417 tasks, 7 epics, 13 releases, 16 decisions; 0 errors and 3 dependency warnings.

## END

END_DONE 0427-130-r5-review: APPROVE PR #1474 head `8bb8cc0e8565b88e89f1ecab5ad1c8fd6853b306`; run 42482853636 passed on the exact head.

Exact `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-08/bughunt-up-name-alias/act-1474-review.md` output after initial publication:

```text
100644 blob 51f9a43f304fb05526b413a435de64407982cbb6	evidence/r27-welle5-folge-2026-11-08/bughunt-up-name-alias/act-1474-review.md
```

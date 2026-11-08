# CODEX-REVIEW 0427-154 DUPLEX — PR #1468 fate

## PLAN

1. Read the outstanding act-1467 recipe and the 0427-154 card/HD5 evidence.
2. Verify both live PR heads, current develop, their exact product diffs, and PR #1468's exact-head hosted checks.
3. Judge #1468 against each act-1467 stop criterion and compare candidate uniqueness.
4. Record the verdict and a single-candidate recommendation in this fate act.
5. Publish this evidence-only update to baseharbor-plan origin/main and verify its remote tree entry.

## Review basis

- Role: REVIEW. Product repo: `mcpdev80/baseharbor`. Card: 0427-154, `t-20261108-bughunt-openbao-stale-manager-cred`.
- PR #1467 live head: `2d929127c343094234f07581c9fdfa9083fdb224`, open. The first live query returned `UNKNOWN` while GitHub recalculated; a refreshed query reports `CLEAN`/`MERGEABLE`. Its exact-head run 42479206678 passed.
- PR #1468 live head: `73182463c6535ea1475f5e1d0480b2c3266a583d`, open, non-draft, base `develop`, `CLEAN` and `MERGEABLE`.
- Current `develop`: `4786c541743541e7550f2c214f143ac8ee4f0aa6`.
- Exact-head hosted run for #1468: [42481502910](https://github.com/mcpdev80/baseharbor/actions/runs/42481502910), terminal `success`, event `pull_request`, head exactly `73182463c6535ea1475f5e1d0480b2c3266a583d`. `PR Selected Checks`, `PR · Validation · go-unit-tests`, `openbao-package-tests`, `go-build`, `go-vet`, `Source format`, `Focused Python`, `Trusted Plan`, and `Workflow policy` passed. The run skipped targeted HA Docker/Podman and Native Keycloak/Core cells. No service-backed native test is required by this file-only OpenBao unit regression, and no skipped cell is counted as a pass.
- Test routing: `internal/openbao/bootstrap_test.go` ran in `PR · Validation · go-unit-tests`, job `128734277800`, which logged `ok github.com/mcpdev80/baseharbor/internal/openbao 5.081s`. Trigger: `pull_request`. The specialized `openbao-package-tests` job also passed, but its selected-test manifest does not include either newly added stale-credential test; the broad Go unit job is the CI evidence that runs them.
- Product write-set on #1468: `internal/openbao/bootstrap.go`, `internal/openbao/bootstrap_test.go` only; no workflow changes.
- Planning base before this evidence update: `fcf8f33d29143ad240c56a17bf2e4979016d4c03 refs/heads/main`.

## Comparison of the two candidates

The complete `gh pr diff` output for #1467 and #1468 is byte-identical; both have SHA-256 `1ff88e116dfc6b8f8e11db47504c52f57003db643cc14f3e37857610ad785e48`. The changed product patch is only the same two OpenBao files. GitHub's head-to-head graph compare reports `diverged` (8 commits ahead, 1 behind, common base `b73a13a909b2d7b811d6956b3bdaf93f17b80454`) because #1468 carries already-integrated #1465 ancestry. Against current develop, #1468 has only one ahead commit and 21 behind from merge base `618d23bde0870391541a8bbdf3ee103f22d70560`; its PR diff remains the same scoped OpenBao patch. There is no unique #154 correction delta on #1467 to import into #1468, nor a #1468 fix to the findings in act-1467.

The refreshed live view shows #1467 is also now `CLEAN`/`MERGEABLE`; the recommendation is not based on a current mergeability failure. Compared with the same current develop SHA, #1467 is one ahead and 28 behind from merge base `b73a13a909b2d7b811d6956b3bdaf93f17b80454`, whereas #1468 is one ahead and 21 behind from merge base `618d23bde0870391541a8bbdf3ee103f22d70560`. Both have exact-head successful CI, but #1468's run 42481502910 is later and its integration base is closer to current develop. Those are the reasons to retain #1468 as the single leading candidate; neither candidate's product patch fixes the act-1467 findings.

## Review against act-1467 recipe

1. **Production observability channel and one-time CLI notice: NOT FIXED.** In `internal/openbao/bootstrap.go:241-253`, comments say the operator sees a diagnostic, but the code only attempts to remove the stale file and continues. The caller `cmd/baha/openbao_operations.go:48-70` still has no successful-recovery notice channel. This is unchanged from #1467.
2. **Fail-closed cleanup: NOT FIXED.** `bootstrap.go:248-253` still discards the `os.Remove(adminPath)` error and proceeds to initialization. An undeletable stale manager credential can therefore remain while the bootstrap continues.
3. **INIT byte preservation: NOT PROVEN BY THE REGRESSION.** The production branch checks `state.Initialized` before any removal and returns `ErrAlreadyInitialized` at `bootstrap.go:234-238`, so the inspected current ordering protects the file. However, `TestBootstrapStillRejectsInitializedServerWithStaleCred` in `bootstrap_test.go:1630-1658` does not read/compare the original credential bytes after refusal, and `executor.initialized != true` is tautological because the fake starts initialized. It would not catch a future credential mutation before the guard.
4. **Exact-head check: PASS, with limited scope.** Run 42481502910 is terminal success on exact head 73182463c. This proves the present tests pass in CI; it does not resolve the three code/test gaps above.

## Verdict

**ROLLE: REVIEW — URTEIL: KORREKTUR; #1468 is the recommended leading candidate, but is not acceptable to merge yet.** Its exact-head CI and clean mergeability are current, and its patch is identical to #1467. The recipe gaps are unchanged, so the green run cannot substitute for the missing notice, removal-error handling, and INIT byte-preservation assertion.

## Candidate recommendation and follow-up recipe

- Keep PR #1468 as the one leading candidate: it has the current exact-head successful hosted run and `CLEAN`/`MERGEABLE` status. Do not merge it until the correction recipe below is implemented and the corrected exact head has its required hosted checks.
- PR #1467 contains no unique product delta to carry over. Keep it open only until #1468's correction is verified; then recommend closing #1467 as the duplicate. Do not merge both.
- If ownership instead elects #1467 as the survivor, transfer the same correction work onto that one candidate and retire #1468; do not maintain two concurrent candidates.
- `internal/openbao/bootstrap.go:241-255`: provide a real recovery-notice result/diagnostic consumed by the production CLI exactly once; return cleanup errors before OpenBao initialization proceeds.
- `cmd/baha/openbao_operations.go:48-70` and its command output path: show a clear one-time message that stale manager credentials were found on an uninitialized server and recovery is proceeding. Preserve `ErrAlreadyInitialized` for an initialized server.
- `internal/openbao/bootstrap_test.go:1584-1658`: add a removal-failure case proving no initialization occurs; in the initialized case preserve and compare the original credential bytes, assert `ErrAlreadyInitialized`, and assert no executor init call or recovery-file creation. In the uninitialized case assert the actual returned/rendered notice and fresh credentials.
- Stop criterion: do not approve or close 0427-154 until those production-path and regression requirements pass on the selected single candidate, with terminal success on its exact SHA in `PR · Validation · go-unit-tests` and `PR Selected Checks`.

## Repository-rule compliance

- Both product candidates and all product sources/checks were inspected read-only. No PR, branch, workflow, test, or product file was changed or triggered.
- The only intended write is this planning evidence act; no compose project was started.
- `python3 scripts/plan.py check` on the fetched planning main reported 0 errors and 3 existing dependency warnings.

## END

END_DONE 0427-154-duplex-review: #1468 leads but remains KORREKTUR; #1467 has identical product diff and no unique code delta.

Live-state addendum: #1467 also refreshed to `CLEAN`/`MERGEABLE`; #1468 remains the recommendation because it is closer to develop and has the later exact-head green run, not because #1467 is blocked.

Exact `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-08/act-1468-fate.md` output after initial publication:

```text
100644 blob 5794bd33c15f588093f7369f201e6e7d18db4db7	evidence/r27-welle5-folge-2026-11-08/act-1468-fate.md
```

Exact `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-08/act-1468-fate.md` output after initial publication:

```text
100644 blob d5780435a94b90c8347bbbe60b7b5288b4d9a153	evidence/r27-welle5-folge-2026-11-08/act-1468-fate.md
```

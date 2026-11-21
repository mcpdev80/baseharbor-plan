# CODEX-REVIEW — 0428-056 / PR #1596

Candidate: `c27158567c0ebc370fc6c97390a561846305738f`
Verdict: REQUEST CHANGES

## PLAN

1. Verify the remote PR head, exact develop base, ancestry, diff, hosted run, and commit identities.
2. Read the task contract and inspect identity reconciliation and missing-environment behavior at the exact head.
3. Verify the exact hosted run and determine whether it records the named regression case or only package aggregate output.
4. Record findings with file-level repair recipes, repository-rule compliance, and cleanliness evidence.
5. Render and check Planning, publish only this evidence file to Planning origin/main, and verify its remote path.

## Remote and candidate provenance

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1596/head` returned `d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3 refs/heads/develop` and `c27158567c0ebc370fc6c97390a561846305738f refs/pull/1596/head`.
- `gh pr view 1596` reports OPEN, non-draft, base `develop`, head `c27158567c0ebc370fc6c97390a561846305738f`, merge state CLEAN.
- The candidate is exactly based on develop: the mission reports back=0, ahead=3, merge commits=0. No foreign commits are listed in the three-commit range beyond the reviewed candidate commits.
- Diff scope: `internal/orgconfig/effective.go`, `internal/orgconfig/model.go`, `internal/orgconfig/org_environment_reconcile_test.go`, `internal/orgconfig/orgconfig_test.go`; 4 files, +391/-8.

## Findings

- BLOCKING — commit identity does not meet card 0428-224's one-identity-per-candidate requirement. The three commits are `110d2739f36999a5defb208f61f7ec311376b949` (author `welle2-056`), `56e6b6251c2468e26a586992fc15e423adc5e2b7` (author `mcpdev80`), and `c27158567c0ebc370fc6c97390a561846305738f` (author `Marcel Pfingstgräf`). All three have committer `Marcel Pfingstgräf`. The candidate task and review instruction require one identity; there is no accepted-SHA certificate or explicit Owner exception in the task evidence. Recipe: re-author the candidate range to the single approved lane identity, or record an explicit Owner exception for the Owner-maintained commits. Stop criterion: do not accept until the range has one authorized author identity or the exception is recorded. Any history rewrite requires fresh exact-head checks.
- No implementation finding: `internal/orgconfig/effective.go:116-120` selects environment defaults only when the requested key exists in `state.Config.Environments`; otherwise organization defaults remain in force. The requested environment is normalized and blank becomes `dev` at lines 95-98. `reconcileEnvironmentIdentity` at lines 224-258 does not mutate the registry or configuration. If no declaration exists, it returns without manufacturing an environment; if a declaration exists but Core registry identity is absent, the declaration remains non-authoritative; an empty declaration with a registry identity errors; a mismatch returns typed policy-denied `environment_identity_mismatch`.
- The regression suite contains matching, mismatch, empty-reference, absent-registry, legacy-resolver, secret-redaction, and mandatory-policy cases in `internal/orgconfig/org_environment_reconcile_test.go`. No branch silently creates an environment that the operator did not select.
- Informational model concern reviewed: `EnvironmentIdentity.Authoritative` is an input field at `internal/orgconfig/model.go:68-76`; reconciliation ignores this authored field and constructs `EffectiveEnvironmentIdentity.Authoritative` only after an exact registry match in `effective.go:253-257`. I found no path in the reviewed diff that treats the authored boolean as proof.

## Hosted checks and regression receipt

- Exact run `44945468909` targets `c27158567c0ebc370fc6c97390a561846305738f`, completed at `2026-11-21T20:22:07Z`, conclusion success. `PR Selected Checks` job `136972968368` completed success. 14 jobs executed successfully, 21 jobs were skipped, and 0 jobs failed. Skips are not counted as passes.
- The exact `PR · Go unit · packages` cell is job `136971759870`, completed success. Its log reports `ok github.com/mcpdev80/baseharbor/internal/orgconfig 0.114s` and `PASS all non-CLI Go package tests`; it does not report the per-case name or duration for `TestReconcileIdentityMismatchFailsClosed` (or the missing-environment behavior). This is an open item, owner-scope receipt-tooling, and is not a candidate blocker because the candidate has no observed behavioral defect. Do not infer per-test execution timing from the package duration.
- Plan artifact SHA-256 recorded for this run: `0f259f33e572707b09ce888917412a7f73b6b4bc4bbee76f0191f1537c87ba00`; plan resolves coverage and selects broad unit/vet/build checks for unknown `internal/orgconfig` paths.

## repo-rule compliance

- Reviewer-only, read-only review against the exact GitHub candidate. No product files, `.github/**`, or `scripts/**` were changed; no product push, merge, workflow dispatch, or local test suite was run.
- Planning repository remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- Evidence belongs only in `baseharbor-plan/evidence/r28-welle4-2026-11-21/org-env-reconciliation/review-1-headc2715856.md`.

## cleanliness

- PID 1 docker snapshot before review: 8 exited `bh-itest-*` containers listed; no container was started or stopped by this review.
- PID 1 docker snapshot after review: the same 8 exited `bh-itest-*` containers; no containers were started/stopped, and before/after state matched.

## END codex-rev-1747 BLOCKED

#1596 remains REQUEST CHANGES on identity policy, so the required review sequence has not reached #1588 or #1749.

## Planning publication witness

- Initial evidence commit: `e146f444712f78a612ca4888247c878ab5792d84`; delivered to `https://github.com/mcpdev80/baseharbor-plan.git` `refs/heads/main`.
- Exact output of `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle4-2026-11-21/org-env-reconciliation/review-1-headc2715856.md`:

```text
evidence/r28-welle4-2026-11-21/org-env-reconciliation/review-1-headc2715856.md
```

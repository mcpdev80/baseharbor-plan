# CODEX-REVIEW 1399b — delegated delivery handoff round 2

- Mission: `coordinator/missions/codex-r1399b.txt`
- Role: CODEX-REVIEW (read-only; no PR action)
- Repository: `mcpdev80/baseharbor`
- PR: #1399, base `develop`
- Reviewed head: `bf8bd49da8f474f0ad915faa25c84f428ba63f23`
- Base `develop`: `f01d2fbdea6b93af6e06ca6297d04065b6acf701`
- Review date: 2026-11-06
- Verdict: **REJECT**

## Candidate identity, scope, and base

`git ls-remote origin` reported `bf8bd49da8f474f0ad915faa25c84f428ba63f23`
for `refs/pull/1399/head` and `f01d2fbdea6b93af6e06ca6297d04065b6acf701` for
`refs/heads/develop`. The PR API reported the same exact head and base. The
develop ancestry check returned 0.

Delta from the previously reviewed `88cee2b21d7fc91b602e370d448316d2cf8494ab`
is limited to:

- `internal/delivery/handoff.go`
- `internal/delivery/handoff_test.go`

The existing two-file fixture and metadata-preservation implementation remains
in the candidate; this round adds the `DriftObservation.validate()` call and
status-flag cases. No product files were changed during this review.
Referenced predecessor blobs are unchanged: `internal/reconciliation/model.go`
is `ffa570bc32fb3bc9d1d7bbe24cd59f1ce0548bd0` on both base and candidate;
`internal/deployment/deployment_store.go` is
`dae2fa96967a4a7c6756f79c9f6b705911f1c7e3` on both.

## The requested cells on the exact candidate

I ran the three negative cells and the evidence-backed positive cell together
at the exact candidate:

```text
go test ./internal/delivery -run 'TestDelegatedStatusWithoutEvidenceNeverTrue|TestDelegatedDigestMismatchTrueFlagNeverTrue|TestDelegatedDriftWithTrueStatusNeverTrue|TestDelegatedStatusBackedByEvidenceStaysTrue' -count=1
```

Result: `ok github.com/mcpdev80/baseharbor/internal/delivery 0.003s`.
I also ran the full `./internal/delivery` package: PASS (0.003s), covering the
existing direct/delegated operation matrix, tracking-metadata preservation,
rendering, and drift refusal fixtures.

Source inspection confirms `HandOff` invokes `drift.validate()` in the
delegated path. The code rejects status flags when required digests or external
evidence are missing and no longer copies `Synced` or `Healthy` into a drifted
result. The positive evidence-backed in-sync fixture passes.

## Validate-call mutant: required discrimination not present

In an isolated detached worktree at the exact candidate, I neutralized only the
`drift.validate()` invocation:

```diff
- if err := drift.validate(); err != nil {
+ if err := error(nil); err != nil {
```

I reran all three required negative cells. All three remained **green**. The
evidence-backed positive counterprobe also remained green. I restored the
candidate source; `git diff --quiet` returned 0, and all four cells passed again.

The first negative test uses matching non-empty digests with empty evidence.
The pre-existing earlier guard already rejects any non-empty digest tuple
without evidence, so that test does not depend on `drift.validate()`. The two
drift tests remain green without `validate()` because the prior fix separately
stopped copying `Synced` and `Healthy` into drifted results. Thus the
mission-required result “validate call out => all three negative cells red”
does not reproduce; the cells currently prove independent guards but do not
discriminate removal of this validation call.

### Required correction recipe

Add a focused status-validation negative case with `Synced: true` (and/or
`Healthy: true`) while both digests and `Evidence` are empty. This bypasses the
older partial-digest/evidence guard and should fail because of
`drift.validate()`. Under the one-line validate-call mutant, that cell must turn
red by rendering a true status; restored code must turn it green. Retain the
two drift cells as coverage for suppression of success flags on drift. Do not
claim all three existing cells discriminate this validate-call mutant.

## Hosted and prior witnesses

Hosted run `42155242740` was independently verified terminal `completed /
success` at exact head `bf8bd49da8f474f0ad915faa25c84f428ba63f23`; `PR Selected
Checks` is terminal success. The accepted round-1 metadata fixture and the
round-2 report's local build/vet/format claims were read as recorded evidence;
the full delivery package test was independently run here as noted above.

## Repository-rule compliance

Read-only review only. The one-line mutant was confined to a temporary detached
worktree and restored; the candidate branch and PR were not changed. No approval
or merge action was taken.

## Conclusion

The implementation now calls `validate()` and the required negative/positive
tests are green on the exact head. However, removing the validate call leaves
all three negative tests green, contrary to the explicit round-2 mutant gate.
**REJECT** until a status-true, zero-evidence test actually discriminates that
call and passes the restored counterprobe.

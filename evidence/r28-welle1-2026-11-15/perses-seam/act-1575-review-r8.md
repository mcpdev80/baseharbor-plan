# PR #1575 Review R8 — Perses state documentation

ROLE: CODEX-REVIEW (no merge).

## PLAN

1. Verify exact PR #1575 head/base ancestry, candidate-only commit chain, PR state, and specified pull_request run.
2. Review documentation-only diff and compare all three state definitions word-for-word with current Perses code behavior.
3. Confirm no code/test behavior drift since r7 and record the separate outstanding #1577 correction.
4. Write verdict and evidence, validate and publish on planning origin/main, verify remote evidence, and post END.

## Candidate, provenance, and diff

- Planning repository root verified before evidence commit: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.
- Product state was inspected from the fresh clone `/tmp/opencode/mission-rev1575-r8-wt`; quarantined stale-ref worker checkout was not used.
- Exact product `git ls-remote` output:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c\trefs/heads/develop
af308e66d38ad1204345bbe83d066dd7548ea6e6\trefs/heads/lane-0428-075-perses-seam
af308e66d38ad1204345bbe83d066dd7548ea6e6\trefs/pull/1575/head
```

- PR #1575 is OPEN and DRAFT, base `develop`, branch `lane-0428-075-perses-seam`, head `af308e66d38ad1204345bbe83d066dd7548ea6e6`.
- Exact fetched base: `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`. `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c af308e66d38ad1204345bbe83d066dd7548ea6e6` succeeded (`BASE_ANCESTOR=yes`).
- Base-to-head log contains only the named 0428-075 Perses task chain; no #1577 head or foreign candidate is carried:

```text
af308e66d38ad1204345bbe83d066dd7548ea6e6 docs(0428-075): align Perses not_configured/configured_unverified with three-state contract (r8)
a5a5abedc3f9b5f72a2ff3819ed847293869eea9 fix(0428-075): set Perses field before remote-target early return (r7)
28492bd12419f2c2e02048e07bfb92d09bb9735f fmt(0428-075): gofmt perses.go constants
181872c90a6e87b853e83198fbe87f198119ae23 fix(0428-075): expose Perses three-state contract in public status JSON (r5)
792c921cbcdb87158aa9abfbd28e2f266a44af5a ci(0428-075): re-trigger hosted CI for exact head c195a9a (r4)
c195a9a2049253accdf57a082e6eb33fc36ec7dd test(0428-075): execute the genuine baha status path for the Perses seam + unknown-owner fail-closed (r3)
dc670bfd4d32baf29afde0e4b021bfdb63f4e0be fix(0428-075): ground Perses seam in manifest truth, fail-closed + unverified reachability
61f76fa18897d4a0709c09c27ae67e1ded8dba20 feat(0428-075): define optional Perses provider seam (fail-closed)
```

- Exact diff `a5a5abedc3f9b5f72a2ff3819ed847293869eea9..af308e66d38ad1204345bbe83d066dd7548ea6e6` changes only `docs/spec/management-access-v1.md` (11 insertions, 9 deletions). A direct Go-source/test diff check returned exit 0 (`CODE_TEST_DIFF_EXIT=0`); no code or tests have drifted since the r7 candidate.
- `git diff --check a5a5abedc..af308e66d` passed.

## State definitions compared with behavior

- `not_configured`, spec `docs/spec/management-access-v1.md:55-57`: no manifest selection or selected declaration with invalid/unavailable pin is fail-closed. `PersesStatusNow` maps `selected == false` and failed compiled-default release validation to `not_configured` (`internal/capability/perses.go:185-192`). The status selection input is derived from `ObservabilityManagementUI && Perses` (`internal/application/management_ui.go:420`).
- `configured_unverified`, spec `:58-62`: selected plus validated pin and no real health-path observation. `PersesStatusNow` returns this only after the selected check and `ValidatePersesRelease(PersesDefaultRelease)` pass (`internal/capability/perses.go:190-195`). The validator checks the compiled pin fields/auth class (`:94-106`); it does not infer reachability.
- `verified`, spec `:63-64`: reserved for an actual Perses health probe observing the surface. Current code explicitly says a real health probe is required and the state is never returned by this Core (`internal/capability/perses.go:176-184`); the current `VerifyPersesManagementUIAt` only validates release metadata and returns without a health request (`internal/metrics/management_ui.go:89-100`).
- The earlier internal contradiction is resolved: a selected but unprovisioned declaration with a valid pin is not classified as `not_configured`; absent a health observation it is `configured_unverified`. The word `unavailable` in the not-configured definition is read as no usable pin declaration, not as external registry/image reachability; the code does not probe external artifact availability, and the spec's configured-unverified clause correctly keeps reachability unverified without a health path.
- Positive assertion coverage from r7 remains unchanged: `TestBahaStatusPersesCLIEntrypointResolvesWithoutContainer` parses `baha app status --json` and asserts exact `configured_unverified` equality (`cmd/baha/app_perses_cli_test.go:295-310`); selected and unselected status equality assertions remain at `:431-465`. No new test was added by r8.

## Separate #1577 open point

- #1577 remains OPEN/DRAFT, base `develop`, branch `0428-092-perses-boundary`, exact head `e51911a5f3cd7205b6bc4d38cb1cd46d9611925f` (`refs/pull/1577/head` and `refs/heads/0428-092-perses-boundary` both resolve to that SHA).
- This separate documentation correction is still pending its own review. It does not reduce the #1575 verdict and no #1577 files, PR metadata, or candidate were modified or reviewed here.

## Pull-request run

Exact mission-specified `gh run view 43670440466 --repo mcpdev80/baseharbor --json databaseId,status,conclusion,event,headSha,workflowName` output:

```json
{"conclusion":"success","databaseId":43670440466,"event":"pull_request","headSha":"af308e66d38ad1204345bbe83d066dd7548ea6e6","status":"completed","workflowName":"CI · Source & Quality"}
```

Active jobs on that exact SHA completed successfully: `PR · Draft source and routing`, `PR · Draft Go · cli-0`, `PR · Draft Go · cli-1`, `PR · Draft Go · cli-2`, `PR · Draft Go · cli-3`, and `PR · Draft Go · packages`. The remaining jobs were skipped under the draft selection. No failing check was observed. No rerun or workflow dispatch was initiated.

## repo-rule compliance

Read-only review from a fresh product clone. No product files, workflow files, PRs, CI runs, containers, or VMs were changed or started; no local tests were run. Evidence is only in the actual planning repository. Candidate code/tests stayed unchanged.

## Planning validation

- `python3 scripts/plan.py render && python3 scripts/plan.py check` completed with 0 errors and 12 existing dependency-state warnings across unrelated v0.4.26/v0.4.27 and CLI2 tasks.
- `git diff --no-index --check /dev/null evidence/r28-welle1-2026-11-15/perses-seam/act-1575-review-r8.md` reported no whitespace errors (status 1 is the expected no-index diff result); evidence contains no markdown checkbox lines.

## Verdict

APPROVE exact candidate `af308e66d38ad1204345bbe83d066dd7548ea6e6` for card 0428-075. The sole r8 change reconciles the three-state specification with the current status behavior and reserves `verified` for a real health path. The specified exact-head pull_request run succeeded. This is review only; merge remains with frost.

Evidence repository remote witness immediately before publication (`git ls-remote origin refs/heads/main`):

```text
69edf2a22c372b0e79a477e02f8ce4887f407c7f\trefs/heads/main
```

END mission-rev1575-r8.md DONE — APPROVE card 0428-075 at candidate af308e66d38ad1204345bbe83d066dd7548ea6e6; #1577 remains a separate open review point.

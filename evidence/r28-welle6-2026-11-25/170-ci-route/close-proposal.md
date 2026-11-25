# #170 close proposal — Leg-B supersession

Status: **PENDING**. Do not dispatch while Core PR #1830 is parked or before it merges.

## Owner-authorized proof to collect

After #1830 merges with `docs/releases/v0.4.28.demo-ref` pinned to Demo develop `b41127723e523134a1c14ee3c36cf133237162ce`, run the hosted `pre-release.yml` supersession dispatch with:

- `ref=develop-tip` (the current Core `develop` tip after #1830);
- `demo_ref` omitted, so the workflow consumes the merged release pin (including Demo PR #174);
- `only_gates=atomic,static,config-matrix`.

Record the exact Core checkout SHA, resolved Demo SHA, hosted run ID and URL, terminal outcome, and the `Static · config-matrix` job result. The config-matrix job must actually execute and pass **without PR #170's hunk** for the run to witness supersession. A run with no scheduled jobs, a skipped config-matrix job, a different Demo SHA, or a non-terminal result is not evidence.

## Proposed disposition after the run

- If `config-matrix` executes and passes on the exact inputs above, attach the run as the supersession witness to task `t-20261124-ci-operator-acceptance-nontty` and update this note with the measured result.
- If it fails, record the first failure and keep #170 open; the failure does not support supersession.
- Even on a passing run, **do not silently close #170**. The Kanban card must first contain an owner-visible confirmation line naming the supersession witness and disposition. Until that line is present, #170 remains open.

Current evidence: no Leg-B dispatch has been run under this order. The previous CLEAN-MERGE label and zero-job startup-failure run do not qualify.

## BLOCKED (round-8, 2026-11-24)

The authorized order cannot run for v0.4.28. `atomic/static/config-matrix` is `required_for` v0.4.22–v0.4.27 but NOT v0.4.28 (dropped after v0.4.27; the v0.4.28 block keeps only `atomic/static/mcp` + `atomic/static/ci-fast-check`). `pre-release-check-plan.py` on `origin/develop` rejects any `only_gates` containing `atomic/static/config-matrix` with `selected checks must be unique exact required check IDs` (exit 2) before scheduling jobs. Root cause = Core release-catalog catalog decision, not Demo content. Owner decision required (re-add gate / accept superseded / alternate gate). Evidence: evidence/r28-welle6-2026-11-25/170-ci-route/round-8.md.

## RESOLVED — option C run (round-9, 2026-11-25)

Owner RESOLVE: config-matrix stays removed (no option A). Option C — dispatch `Release · Pre-Release Validation` on develop-tip f7540e59 (#1837), tag v0.4.28, demo_ref pinned via #1830, ONLY_GATES=atomic/docker/guided,atomic/docker/lifecycle (designated substitute for config-matrix). Run **45518363769** terminal: `completed`/`success`, head f7540e59. Both designated Light gates succeeded — but by **evidence reuse** (`Light · docker · guided / Reused docker · guided`, `/ Reused docker · lifecycle`); each job's step 4 = "Report previously qualified run without executing native runtime" and native steps (checkout, prepare runtime, Run runtime gate) are `skipped`. So the native runtime gate did NOT execute on demo pin b4112772. This does NOT void the run (gates did not skip) but is not a fresh exact-head native execution. #170 stays OPEN pending an owner-visible close line on card t-20261124-ci-operator-acceptance-nontty. Evidence: evidence/r28-welle6-2026-11-25/170-ci-route/round-9.md.

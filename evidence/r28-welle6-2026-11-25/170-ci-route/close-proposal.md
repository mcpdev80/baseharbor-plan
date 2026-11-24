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

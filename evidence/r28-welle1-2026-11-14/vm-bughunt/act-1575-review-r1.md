# PR #1575 Review R1

Review role: CODEX-REVIEW
Review date: 2026-11-14
Card: t-20261114-r28-perses-contract-seam (0428-075)
PR: https://github.com/mcpdev80/baseharbor/pull/1575 (OPEN, DRAFT)
Reviewed candidate: 61f76fa18897d4a0709c09c27ae67e1ded8dba20
Fetched base: 0e9ccb582f5bdcdc74049bbe3996263cdce6500c (develop)

## PLAN

- Fetch and verify the PR head and base, establish provenance, and record remote witnesses. (done)
- Review the exact diff against the task contract, entry point, CI rollup, and file ownership. (done)
- Record a verdict with an actionable correction recipe and stop criterion. (done)
- Commit and push this evidence to planning main, then report completion. (done)

## Repository and candidate witnesses

Planning repository identity was verified before this evidence commit. Exact command and output:

`git rev-parse --show-toplevel`
`/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`

Exact remote witness from BaseHarbor:

`git ls-remote origin refs/heads/develop refs/pull/1575/head`
`0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop`
`61f76fa18897d4a0709c09c27ae67e1ded8dba20	refs/pull/1575/head`

Fetched refs resolve to base `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` and PR head `61f76fa18897d4a0709c09c27ae67e1ded8dba20`. `git merge-base --is-ancestor refs/review/develop refs/review/pr1575` exited 0. The exact base-to-head log contains only this candidate commit:

`git log --oneline refs/review/develop..refs/review/pr1575`
`61f76fa18 feat(0428-075): define optional Perses provider seam (fail-closed)`

The PR is open and draft, base `develop`, head branch `lane-0428-075-perses-seam`. The diff changes 13 files; no `.github/**` files are changed. `git diff --check` is clean.

## Verdict

REJECT for candidate `61f76fa18897d4a0709c09c27ae67e1ded8dba20`. The candidate does not meet the fail-closed runtime and evidence requirements.

Findings:

- `internal/capability/perses.go`: `PersesManagementSurfaceNow` sets `Provisioned=true` when the compile-time default version/image strings validate. This does not verify that a Perses service is selected, provisioned, or reachable. `internal/metrics/management_ui.go:VerifyPersesManagementUIAt` likewise validates only the compile-time constant. A pinned declaration is realization metadata, not runtime provisioning evidence; these paths can report a configured surface when none exists.
- `docs/spec/provider-management-acceptance-v1.md`: the new Perses row claims `SUPPORTED` availability across one Prometheus member failure. This PR adds no Perses runtime lifecycle or failover proof, and the Prometheus backend's continuity does not establish the Perses UI's continuity. The row overstates verified behavior.
- The tests do not exercise a genuine user entry point. They call internal validation/descriptor helpers and manifest parse/render methods; no CLI command is invoked. The task explicitly requires the genuine entry point and forbids substituting an internal seam call for CLI coverage. The tests also do not exercise unknown ownership or missing authorization behavior.
- Hosted CI run `43637427710`, exact candidate SHA above, triggered by the draft PR update: `PR · Draft Go · cli-0`, `cli-1`, `cli-2`, `cli-3`, and `packages` succeeded. `PR · Draft source and routing` failed. Exact failing log line: `Unformatted Go source: internal/application/manifest.go`. Other displayed groups were skipped under draft selection. No rerun or workflow dispatch was initiated.

## Correction recipe

1. In `internal/application/manifest.go`, run gofmt and keep the change limited to formatting.
2. In `internal/capability/perses.go` and `internal/metrics/management_ui.go`, make `Provisioned` and verification depend on actual selected/provisioned runtime state. A valid version/image declaration alone must remain unconfigured/unsupported. Add a deterministic negative test where no Perses runtime exists, and test the actual CLI entry point that surfaces the result. Do not implement container lifecycle in this task.
3. In `docs/spec/provider-management-acceptance-v1.md`, classify Perses HA as unsupported or otherwise unverified until Perses-specific runtime evidence proves continuity; do not infer UI availability from Prometheus backend continuity.
4. Add deterministic tests for unknown ownership and missing authorization through the public CLI path, or narrow the implementation/spec claims if the existing boundary cannot support those cases. Keep new tests in the existing Go package coverage selected by the draft Go CI group and confirm the triggering source path; do not edit `.github/**`.
5. Re-run the changed candidate's required existing checks after the fixes are committed. Stop if the source/routing check remains red, the CLI still reports provisioned without runtime evidence, or the authorization/ownership result is not fail-closed.

## Planning validation and pre-push witness

`python3 scripts/plan.py check`: 531 tasks, 7 epics, 13 releases, 21 decisions; 0 errors, 11 pre-existing warnings. `git diff --check` produced no output.

Exact output of `git ls-remote origin main` before this evidence commit:

`9ce0b31c8d811ee36768aa08f4dae7ca25672989	refs/heads/main`

## Evidence publication

The review record was pushed to planning `main` and verified by fetching `main` and reading this path from the fetched commit. The publication commit at that verification point was `45a1000a89d738b75599a195fd12cf5eeb7401bd`.

## CI selection and trigger

The existing `CI · Source & Quality` workflow selected `PR · Draft Go` package jobs for the draft PR update. The new Go tests were picked up by package jobs `cli-0` through `cli-3` and `packages`, all successful on the reviewed SHA. The same draft push selected `PR · Draft source and routing`, which failed on the formatting line above. Runtime Docker/Podman gates were skipped; this candidate contains no container lifecycle implementation.

## repo-rule compliance

- Read-only review of the product candidate; no product files, workflows, PR state, or checks were changed or rerun.
- Evidence is in the actual planning repository `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, not the `workers/baseharbor-plan` bookkeeping path.
- No subagents used. No secrets copied into this evidence.
- Review is tied to the exact fetched candidate and base above.

END act-1575-review-r1 DONE — REJECT; candidate 61f76fa18897d4a0709c09c27ae67e1ded8dba20.

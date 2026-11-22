# PR #1761 exact-head review

Session role: CODEX-REVIEW, read-only.

## PLAN

1. Read `/var/tmp/m/rev1761b.md.g`; capture exact PR #1761 head, base, scope, evidence path, and read-only boundaries.
2. Refresh authorized GitHub refs and exact hosted run; inspect the exact diff, helper fan-out, scope, and downstream #1746 compatibility read-only.
3. Record the SHA-specific verdict and all requested witnesses here; validate and publish only this evidence to Planning `origin/main`.
4. Update the live board and post END to the Coordinator with head, verdict, fan-out witness, run, matrix length, and Planning remote line.

## Live state and provenance

- PR #1761 is open and DRAFT at exact head `669d76ac44792a56d2642df05c5211058460b3bb`, base `develop` at `acc343239681feb235a33cf00c8ea754c537291f`, mergeable state `clean` (GitHub API snapshot 2026-11-22).
- Product remote: `https://github.com/mcpdev80/baseharbor.git`, fetched through the resolved `lane-origin` remote only. `git ls-remote` confirmed the exact PR head and develop SHA above.
- Previous candidate `d275e50c5ba0245b6ab8a42f9655c9bef1bb2bd0` is an ancestor of the reviewed head.
- `git diff d275e50c5ba0245b6ab8a42f9655c9bef1bb2bd0..669d76ac44792a56d2642df05c5211058460b3bb` has 12 paths, all belonging to the already merged #1627 env-destroy change set: the env-destroy implementation/tests, its authorization/provider/machine-coverage updates, and generated EN/DE CLI docs. No new #1761 product/test change was introduced by this hop. The change preserves the helper feature from the prior head.

## Scope

`git diff acc343239681feb235a33cf00c8ea754c537291f...669d76ac44792a56d2642df05c5211058460b3bb --name-only` is exactly:

- `cmd/baha/app_env_test.go`
- `cmd/baha/app_export_command_test.go`
- `cmd/baha/installation_destroy_native_test.go`
- `cmd/baha/target_definition_change_test.go`
- `cmd/baha/test_operator_context_test.go`
- `internal/operatorauth/test_operator.go`

No `.github/**`, `scripts/**`, `internal/observability/registry.go`, or `internal/capability/perses_selection.go` path is changed.

## Fan-out

Fan-out verdict: COMPLETE. The five requested test files all route their operator setup through the shared `internal/operatorauth` helpers. Exact call-site witness at the reviewed tree:

- `cmd/baha/test_operator_context_test.go:22` — one call to `operatorauth.WithVerifiedTestOperator`.
- `cmd/baha/app_env_test.go:35,164` — two helper calls for distinct setup paths (`WithVerifiedTestOperatorPrincipalForced` and `WithVerifiedTestOperatorPrincipal`).
- `cmd/baha/app_export_command_test.go:369,386` — two calls for separate export test setups (`WithVerifiedTestOperatorPrincipalForced`).
- `cmd/baha/installation_destroy_native_test.go:39` — one call to `WithVerifiedTestOperatorPrincipalIfAbsent`.
- `cmd/baha/target_definition_change_test.go:40` — one call to `WithVerifiedTestOperatorPrincipal`.

Repository-wide tree search `git grep -n 'type ReadGrantingMembershipProvider' <head> -- '*.go'` returns exactly one definition: `internal/operatorauth/test_operator.go:22`. There is no duplicate provider definition under `cmd/baha`.

## #1746 compatibility

The helper is importable from the downstream `cmd/baha` test package without another product change: package path `github.com/mcpdev80/baseharbor/internal/operatorauth`; exported entry point signature at `internal/operatorauth/test_operator.go:41` is `func WithVerifiedTestOperator(ctx context.Context) context.Context`. The package is beneath the module's `internal/` parent, so `cmd/baha` is within the permitted parent tree. #1746 itself was not changed or reviewed in this task.

## Hosted run

Run `44999534797` (`CI · Source & Quality`) is terminal `completed / success`, head SHA exactly `669d76ac44792a56d2642df05c5211058460b3bb`; its check-runs contain 0 failures. The executed relevant jobs all succeeded:

- `PR · Draft source and routing`, job `137137806193` — SUCCESS.
- `PR · Draft Go · cli-0`, job `137137806291` — SUCCESS.
- `PR · Draft Go · cli-1`, job `137137806376` — SUCCESS.
- `PR · Draft Go · cli-2`, job `137137806417` — SUCCESS.
- `PR · Draft Go · cli-3`, job `137137806374` — SUCCESS.
- `PR · Draft Go · packages`, job `137137806463` — SUCCESS.

Draft-only non-execution is recorded explicitly: `PR Selected Checks` job `137137808235` is SKIPPED, and `PR · Native gate plan` job `137137844045` is SKIPPED. Native/runtime rows such as `PR · Native · ${{ matrix.id }}` (`137137808006`), `PR · Selected Runtime` (`137137808013`), and `PR · Native Keycloak/Core · ${{ matrix.runtime }}` (`137137807365`) are also SKIPPED. These skipped jobs are not represented as passes. Because the native gate plan job did not execute, no matrix length was emitted by this run; matrix length is unavailable, not inferred to be zero. The run-level success and the six executed jobs do not substitute for the skipped `PR Selected Checks` aggregate or native/runtime evidence.

## Verdict

Verdict: APPROVE — exact-head code review only. The prior fan-out gap is resolved; current scope and helper uniqueness are satisfactory. This verdict does not claim a successful required aggregate or native/runtime execution.

merge-empfehlung: Kein Merge durch diese Review-Lane. #1761 bleibt DRAFT, bis der Owner die Ready-Entscheidung trifft und die noch erforderlichen hosted checks für die Sequenz bestätigt. Danach können #1746-Tests den bestehenden `internal/operatorauth` helper direkt importieren.

## Cleanliness

- `docker ps -a --no-trunc` before inspection: no containers listed.
- No tests, containers, or compose projects were started by this read-only review.
- `docker ps -a --no-trunc` after inspection: no containers listed.

## Planning remote witness

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` before the evidence commit:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Repo-rule compliance

- Read-only review scope followed: no product changes, PR state changes, GitHub comments, ready toggles, merges, workflow triggers, or local tests.
- Evidence is stored only in the canonical Planning repository. Shared untracked Planning files were left untouched.

END_DONE codex-rev-1747: PR #1761 head 669d76ac447 reviewed APPROVE; fan-out complete, run 44999534797 success/0 failed with draft skips and native matrix unavailable; Planning publication pending.

## Origin/main witnesses

Remote delivery after the first evidence push: 

```text
cec45f6e0751966877a3164fa20ad476be05cbd5\trefs/heads/main
```

Exact output of the required fetched-origin tree lookup:

```text
evidence/r28-welle5-2026-11-22/static-cells-operator-auth-helper/review-1761-head669d76ac447.md
```

END_DONE codex-rev-1747: PR #1761 exact head 669d76ac447 APPROVE for code review; fan-out complete; run 44999534797 success with draft skips and native matrix unavailable; Planning evidence is present on origin/main.

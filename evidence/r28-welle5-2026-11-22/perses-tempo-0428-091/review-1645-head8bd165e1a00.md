# PR #1645 exact-head review

## PLAN

1. Reconcile the exact PR head/base, the prior package failure, and the assigned review scope.
2. Verify the correction changed only the test's policy setup, that the adapter commit remains intact, and that no skip/timeout workaround was introduced.
3. Inspect terminal hosted CI, the packages shard, the native gate plan, and the trusted coverage mapping for this correction.
4. Publish this exact-head read-only verdict for Coordinator handoff.

## Candidate

- PR: [mcpdev80/baseharbor#1645](https://github.com/mcpdev80/baseharbor/pull/1645)
- Head: `8bd165e1a00d25972b55e5b50787091f0aee8f0a`
- Base: `develop` at `acc343239681feb235a33cf00c8ea754c537291f`
- GitHub state at review: OPEN, Ready (not Draft), CLEAN.
- The author's implementation lane is session `0847d100`; this review is the separately assigned independent review.

## Review evidence

### 1. Policy-neutral test setup

At the previous exact head, the test called compatibility `serviceaccess.Resolve("dev", "cache", AuthenticationMTLS)` without a policy source. On the inspected candidate source, `internal/serviceaccess/policy.go:75-77` documents that this compatibility API supplies the zero-value `EnvironmentPolicy{}`, which fails closed as managed. The policy field is defined at `policy.go:89-94`; `TrustedLocalForEnvironment` returns false at `policy.go:109-110`; and the only `AuthenticationRequired` assignment is the explicit policy switch at `policy.go:149-158`. Thus the prior test's "dev non-RequireClient" comment did not match its input.

The correction at `internal/metrics/perses_tempo_source_test.go:404-420` now supplies `EnvironmentPolicy{TrustedLocal: true}` through `ResolveWithPolicy`, matching the existing test contract. The assertion still checks that neither client certificate nor key is enrolled. No production policy, adapter, gateway, or service-access behavior changed in the correction commit. The adapter implementation commit `4d73aa97808d000d2f70eaa193f8dbfc14e817a7` remains an ancestor of the candidate unchanged.

The test contains no skip, sleep, timeout increase, or other execution bypass. The correction commit changes one line in the named test file; the additive develop hop is a normal merge with parents old head `326ca9005267c135feb31cdfde8ac69a3c17508e` and current develop `acc343239681feb235a33cf00c8ea754c537291f`. No PR review comment or workflow rerun was issued by this reviewer. No local tests were run.

### 2. Exact hosted CI

Run [45001605859](https://github.com/mcpdev80/baseharbor/actions/runs/45001605859) is terminal SUCCESS on the exact head, with 0 failed jobs. The packages job `137144258716` (PR · Go unit · packages) succeeded, resolving the prior failing packages job `137127343932` at old head `326ca9005267c135feb31cdfde8ac69a3c17508e`.

The run recorded both trusted-plan annotations:
- "Incremental PR checks: previous source/base ancestry not proven; reused validations=0; reused runtime gates=0"
- "PR · Trusted Plan: No narrow mapping: conservative checks selected."

### 3. Native data-capabilities coverage

The exact run's native plan job `137144213067` succeeded, but produced an empty native matrix (`{"include":[]}`); the generic native matrix job `137144260109` was skipped. Therefore this run is **not** native runtime proof.

For the correction delta, a native data-capabilities row is not required. The trusted catalog at `scripts/pr-gate-coverage.json:3056-3074` and `:3077-3090` maps Docker/Podman data-capabilities only to the listed `cmd.baha.*` CLI source components; `internal/metrics/perses_tempo_source_test.go` is not one of them. This is a test-setup-only correction, and the package shard that executes it ran successfully. The missing data-capabilities row is therefore correct for this correction delta; it is not represented here as a passing native runtime gate. No broad runtime matrix was required or requested for this one-line test correction.

## Verdict

**APPROVE** at exact head `8bd165e1a00d25972b55e5b50787091f0aee8f0a`. The prior red assertion used a fail-closed managed policy despite claiming trusted-local/non-RequireClient behavior; the test now supplies the explicit trusted-local policy, the adapter code remains unchanged, and the exact hosted packages job passes.

runtime-coverage: native data-capabilities not required for the test-only correction delta; its catalog row covers the enumerated `cmd.baha.*` components, not this `internal/metrics` test. The skipped matrix is not runtime proof.

## Cleanliness

Review was read-only. No product files, PR metadata, comments, merge state, workflow state, or local runtime were changed by this reviewer. No local tests were run.

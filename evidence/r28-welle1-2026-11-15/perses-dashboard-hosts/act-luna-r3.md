# CODEX-REVIEW — PR #1602 correction follow-up

**ROLLE: REVIEW**
**Task:** `t-20261114-r28-perses-dashboard-hosts`
**Candidate:** `8267a16df47ed9b3c3fb4fc26cc77959b7b2e01e`
**Exact-head CI:** run `43810981306`, `pull_request`, COMPLETED SUCCESS, exact candidate SHA. Active Draft source/routing, packages, and CLI shards succeeded.
**Reviewed delta:** parent `abe9bd52da94074240a363369424b6a2abc9f155` → candidate; three files, `git diff --check` clean. PR #1602 remains open/draft.

## Verdict: REQUEST CHANGES

This commit corrects the unavailable-reason wording and the formerly failing CLI assertion. The defect is in the inherited positive-availability path, which this three-file change does not alter: `ResolveHostDashboardSignalStatus` returns `ObservabilitySupported` when the two manifest selection booleans are true and the Perses release pin validates. `app_status_result.go` passes that status to `PersesHostDashboardAvailability`, which then emits positive availability. This proves manifest selection and pin validity, not an actually available matching host/container metric signal or authorization for the current Target/tenant. That conflicts with the card goal and acceptance requirement to show host/container panels only for actually available matching metrics and to fail closed on unknown ownership or missing authorization. Tests currently pin the two booleans as sufficient evidence of support, so the current positive result is self-confirmed by the same declaration it is meant to establish.

## Recipe / stop

- **Files/change:** update `internal/capability/perses.go` and its resolver tests, plus the status/availability call path and focused tests, so `ObservabilitySupported` requires a resolved matching native host/container signal and an authorization/ownership witness for the actual Target. If either is absent, unknown, or denied, keep availability unavailable. Do not infer support from the two selection booleans and a valid pin alone.
- **Required tests:** cover no signal, unknown/unauthorized Target, denied ownership, mismatched Target, and a matching authorized signal; verify only the final case emits available panels. Route these tests through the exact-head CI check and record actual execution.
- **Preserve:** the r3 reason wording and its regression test.
- **Stop:** if the existing contract cannot provide the signal/Target witness, keep the dashboards unavailable and resolve the owner/API dependency before claiming availability. No merge.

Read-only, SHA-exact review; no product files changed.

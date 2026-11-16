# CODEX-REVIEW — PR #1608, correction follow-up

**ROLLE: REVIEW**
**Task:** `t-20261114-r28-perses-datasources`
**Candidate:** `8b00fe2c80777498d18d574cb39b9299e5b160f8`
**Exact-head CI:** run `43801620792`, `pull_request`, COMPLETED SUCCESS, exact SHA.
**Base:** Perses seam lane; correction history/evidence is `round-2-luna-correction.md`. The current delta from the prior correction candidate is comment-only; the earlier correction commit in this same branch is included in the exact candidate review. `git diff --check` clean.

## Verdict: APPROVE CONTENT

The r1 findings are addressed in the correction history: datasource construction now fails closed on absent/unselected/denied/invalid sources and bad endpoints; it no longer suppresses endpoint errors into an empty datasource. Health verification performs a real Prometheus query using the service-access client, so a pin alone does not produce `verified`; the no-probe path remains unverified. Tests cover negative source/authority cases, query result/error, TLS/auth behavior, and emitted datasource configuration. The exact-head CI is green.

## Recipe / integration gate

- **File/change:** no further correction required by this review.
- **Checks:** retain the package CI coverage and exact-head provenance recorded in the correction akte. The task's open dependencies on the Perses contract seam/runtime remain outside this PR's content verdict.
- **Stop:** do not treat this review as acceptance of unmet dependencies or permission to merge; stop if a later integration bypasses the authorized source snapshot or reports verified without a real probe.

Read-only review; no merge performed.

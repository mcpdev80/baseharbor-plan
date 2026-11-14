---
id: 2026-11-15-ci-test-discovery-and-gate-catalog
status: proposed
sources: []
---

# Recommended decision: test discovery and gate-catalog integrity

## Context

Tests can pass today while silently falling out of future required coverage. A manually maintained list of ordinary Go tests duplicates the package discovery that already exists. Contract regressions and new validations have a different risk: their required CI route must remain visible as code and catalog entries. Release windows also need to carry the correct gate-map label.

## Decision

1. Keep ordinary Go unit tests package-discovered through `go list ./...` and `go test -list`. Do not create per-test registration lists for them; reject proposals that do.
2. Require every task card to identify exactly one test-binding route. Normal Go tests use package discovery. A contract test protecting an acceptance invariant is added to `REQUIRED_CLIENT_TESTS` or its package equivalent in the same PR. A new CI check updates `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR. Review blocks when the row is absent or its selection does not match the change.
3. Make `scripts/ci-workflow-policy.sh` fail when validation check files are added or removed, or pre-release gates are added or removed, without same-PR planner and gate-catalog updates. Gate-ID additions/removals also require the PR planner to change.
4. At the release-window begin marker, require the exact candidate Core's `scripts/pr-gate-map-v1.json` `release` label to equal the release being opened. A mismatch blocks Prepare until the label and catalog regression are reconciled.

## Consequences

The ordinary Go test discovery mechanism stays the single source of truth. Card acceptance contracts retain a required-set anchor, and new validation surfaces cannot silently bypass PR selection or release qualification. Release preparation records the exact Core source and checks its gate-map label at the start of the window. These rules change test-routing and release-planning process; they do not add product behavior or authorize a release, tag, promotion or publication.

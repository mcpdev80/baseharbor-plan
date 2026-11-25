# Bug Hunt H-V35: catalog-integrity desk

READ-ONLY. Pure finding. No product changes.

## Task

Cross-check `scripts/pr-gate-coverage.json` (schema `baseharbor.pr-gate-coverage/v1`, release `v0.4.27`, develop head `c7f70b0c595d2428c6776e9554dff5054cfae65c`) against the source that lands after the rows landings:

- uncataloged candidates (sources under `cmd/baha` + `internal/` referenced by NO row)
- duplicate ids/paths
- `source.gate.*` naming consistency vs `scripts/release-requirements.json`
- test sources added in the 0.4.28 window lacking rows

## Reality witnesses

- Planning repo remote (first action): `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch), `origin https://github.com/mcpdev80/baseharbor-plan.git` (push).
- baseharbor checkout: real GitHub remote `lane-origin https://github.com/mcpdev80/baseharbor.git`; `origin` in the workers/ bookkeeping repo points at a local path (never cited).
- `scripts/pr-gate-coverage.json` and `scripts/release-requirements.json` both present at baseharbor root.
- develop fetched fresh: `origin/develop = c7f70b0c595d2428c6776e9554dff5054cfae65c`.
- All 2377 go files under `cmd/baha` + `internal/` are mtimed `2026-11` (fresh checkout).

## Findings

Full per-row detail in `findings.md`. Summary:

- Uncataloged candidates: 2234 of 2377 go files (93.8%). 1072 implementation, 1162 tests.
- Duplicate ids: none (143 unique ids). Duplicate paths: none.
- `source.gate.*` classes: 15 distinct, all present in release-requirements.json. No orphan.
- 0.4.28 window: every uncataloged file is mtimed 2026-11 (the 0.4.28 window).
- Coverage file is a work-in-progress: 143 source components cataloged, 75 gates cataloged with all mapping to a release-requirement job; three release-required integration gates (`integration/{docker,podman}/remote-target`, `integration/static/live-console`) are RR-only and expected absent.

## Proposed card lines

- `0428-xxx-catalog-coverage-completion`: finish cataloging the remaining ~2234 source rows so `pr-gate-coverage.json` is exhaustive for the 0.4.28 window.
- `0428-xxx-catalog-coverage-stability`: freeze the schema once the catalog is complete; the coverage file is a moving target mid-0.4.28.

## Cleanliness

- `docker ps -a` before: (no containers started; read-only desk work, no compose/projects launched).
- `docker ps -a` after: (identical — nothing started).

## Status

END_DONE. Fund count: 4 (uncataloged candidates; dupes none; source.gate naming consistent; 0.4.28 window coverage gap). Lane w161-0428-224-hunt-v35 DONE.

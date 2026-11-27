# PR #1862 content review — card 0428-318

**Role:** Codex REVIEW; product content only. No product or PR writes.

## Exact snapshot and diff

At review, GitHub PR #1862 and `refs/pull/1862/head` point to `2fcf326092e4066f71d3ed7641ed231ce49a55dc`; live develop is `ea5218d72e263f21e79853b679af50074dab8c25`. PR #1862 is OPEN, mergeable=true, merge state BEHIND. Its stored base SHA is `6d237ccdf3a5db19c5814ad5b76d01be6c38c35c`; compare against live develop reports three commits ahead, one behind. The candidate diff has three files: `internal/runtimeexecutor/compose.go`, `internal/runtimeexecutor/compose_test.go`, and `scripts/pr-gate-coverage.json`.

Candidate blob witnesses (candidate / live develop): `compose.go` = `b63d7647f7653571d59a73a7d1748c1c4306dcac` / `fccc32d44125957b8aa83f2ea8ab32050a1f328a`; `compose_test.go` = `07f2d43824bb596df46b9b54453e609ce3b6376d` / `e9cd41f399bee81619bcb2767fcee56bbe4cabe7`; `pr-gate-coverage.json` = `56465e05a1e31cc21b18866adb882594b18c256f` / `792a767aaceb600f5f0da228264413333014d1a8`.

## Content assessment by finding

**FUND-C — executor image guard:** `compose.go` replaces the CR/LF/NUL-only check with a restrictive allow-list before `compose.yaml` is written. The malicious multiline second-key example is rejected, while the canonical `ghcr.io/mcpdev80/baseharbor-runtime:0.4.28` form and the empty-value default remain allowed. The focused tests cover injection rejection and canonical acceptance. This addresses the described low-severity YAML-injection surface without changing runtime authorization or consent.

**FUND-D — S3 admin projection:** after projecting `s3-admin.env`, `compose.go` checks that the projected file exists and has non-zero size before generating/writing `compose.yaml`; an absent or empty file returns an error. The regression supplies an empty source credential and requires `EnsureFiles` to fail. This is fail-closed and does not change consent/auth behavior. The check precedes the compose write path in the reviewed code.

No consent/auth source, workflow, or other file is changed; the two code changes remain scoped to the executor's configuration preparation and its tests.

## CHANGES — candidate not accepted

The third commit adds `source.internal_runtimeexecutor_compose_go` and `source.internal_runtimeexecutor_compose_test_go` to the candidate's `scripts/pr-gate-coverage.json`, with Docker and Podman `data-capabilities` surfaces. Those IDs are absent from trusted live develop `ea5218d72e263f21e79853b679af50074dab8c25`. The exact-head Hosted run [45929247724](https://github.com/mcpdev80/baseharbor/actions/runs/45929247724), attempt 1, fails `PR · Trusted Plan` with both paths reported as uncataloged; `PR Selected Checks` fails downstream. This is the same trusted-base authorization pattern as #1861: a candidate-side row cannot authorize its own Trusted Plan run.

**Required correction:** remove the `scripts/pr-gate-coverage.json` change from #1862 and preserve the product/test files as the card-scoped payload. Have the existing trusted-baseline family 0428-359/#136 land these exact source IDs on develop first:

- `source.internal_runtimeexecutor_compose_go` → `internal/runtimeexecutor/compose.go`
- `source.internal_runtimeexecutor_compose_test_go` → `internal/runtimeexecutor/compose_test.go`

Both rows need the existing Docker and Podman `data-capabilities` surfaces. After those rows are present on trusted develop, refresh #1862 against that develop tip and qualify the final exact head. Do not weaken the planner or count the current failure as qualification.

This is a content CHANGES disposition; no ACCEPT is carried by a hop. If a post-hop candidate preserves the two reviewed product blobs unchanged, those finding reviews can be carried forward, but this PR remains CHANGES until the candidate-side catalog rows are removed and the baseline is trusted on develop.

## Contract and scope

The current 0428-318 task file is `tasks/t-20261125-hunt43-low-severity-pair.md`; its Goal, Scope, Acceptance, and Handoff fields remain template placeholders. This review uses the PR description's specific scope: FUND-C allow-list for `BASEHARBOR_RUNTIME_IMAGE`, FUND-D projected S3 admin file existence/non-empty check, and focused tests. It does not silently fill or broaden the card contract. The unresolved trusted-base mapping is routed to the existing 0428-359/#136 baseline family; no new tracking is proposed here.

---
id: t-20261108-r27-native-single-default-owner-check
card_number: "0427-170"
card_short_title: "native default owner check"
type: bug
areas: [ci, lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "ChatGPT (native CI)"
kanban_status: review
kanban_lane: review
kanban_summary: "SINGLE-default native acceptance must inspect its already running owned bootstrap Core rather than attempting a second Core on the same engine."
kanban_title: "0427-170 · native default owner check"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1495, mcpdev80/baseharbor#1497]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261108-r27-native-single-default-owner-check · Native SINGLE-default acceptance honors one-Core-per-engine policy #task #release/v0-4-27 #status/review #view/review #area/ci #area/lifecycle #kind/bug

## Cause

The old 0427-156 bootstrap-marker failure came from a stale native test fixture. It is fixed in current develop and verified by PR #1457 native Docker/Podman CI. Do **not** weaken or disable its fail-closed marker.

A subsequent failure on corrected fixture (PR #1489 run 42513106766, native Podman job 128830281368) is different: `TestControlPlaneSingleDefaultNativeRuntimeInCI` starts a SECOND Core on the same engine after the package fixture already started its own isolated Core. Product PR #1487 intentionally rejects that with a typed owner conflict; the behavior is correct.

## Fix and decisions

- [PR #1495](https://github.com/mcpdev80/baseharbor/pull/1495): exercise the actual first package-owned bootstrap Core, preserving assertions for exactly one running PostgreSQL and OpenBao member and zero HA members/etcd. No second Core, no product change.
- [PR #1497](https://github.com/mcpdev80/baseharbor/pull/1497): add the **single existing native test file** to the trusted PR routing for the **existing** Docker/Podman Keycloak/Core jobs. The trusted-base rule requires this selector to merge before PR #1495 can be fully native-qualified.
- No new workflow or evidence/receipt gate; GitHub-hosted native runners only. Missing, skipped, red or cancelled mandatory tests remain a hard failure. No `.github/**` modifications outside the one owner-native check selector.

## Acceptance

- Exact SHA of #1497 passes normal workflow policy/actionlint and focused CI, then integrates to develop.
- Requalify #1495 against updated trusted develop policy, execute `TestControlPlaneSingleDefaultNativeRuntimeInCI` for real on both Docker and Podman with explicit non-SKIP PASS and successful final PR Selected Checks.
- Confirm cleanup of only the package-owned bootstrap Core, do not interfere with foreign cores.
- Record resulting PRs/merge SHAs/CI runs and close only after actual tests.

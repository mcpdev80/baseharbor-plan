---
id: t-20261115-bughunt-d28-tmp-selection
card_number: "0427-190"
card_short_title: "bf03 private selection store"
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: codex-open-pr-sweep-190 (audit_perses_blocked)
kanban_status: active
kanban_lane: active
kanban_summary: "BF-03 (daemon security): persisted target selection lives in a world-writable /tmp/baha-test- path. Found on develop 0e9ccb582…"
kanban_title: 0427-190 · bf03 private selection store
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1582"]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md"]
---

- [ ] t-20261115-bughunt-d28-tmp-selection · BF-03 persisted target selection in world-writable /tmp path #task #release/v0-4-27 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** codex-open-pr-sweep-190 (audit\_perses\_blocked)  
    **PR:** [baseharbor#1582](https://github.com/mcpdev80/baseharbor/pull/1582)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** codex-open-pr-sweep-190 (audit_perses_blocked)  
**Priority:** not set  
**PRs:** [baseharbor#1582](https://github.com/mcpdev80/baseharbor/pull/1582)  
**Source:** 
<!-- /generated:links -->

## Goal

BF-03 (daemon security): persisted target selection lives in a world-writable /tmp/baha-test-* path. Found on develop 0e9ccb582 during H-D28.

## Scope

- In scope:
  - Reject untrusted legacy organization selection files and unsafe source-directory ancestry during the one-time migration.
  - Preserve the existing private canonical selection and durable once-only migration behavior.
- Out of scope:

## Acceptance

- A 0600 regular legacy file is adopted only when its owner is the current UID and every source directory is root/current-owned; writable source directories must be sticky.
- The migration validates the opened inode before reading, rejects path replacement, and leaves a rejected source and canonical destination unchanged.
- Existing valid migration and once-only/frozen-marker behavior continues to pass.
- Focused Go tests, vet, race run and diff check pass on the exact candidate; PR remains Draft until parent review and exact-head CI.

## Required checks

- **Test binding (select exactly one):** ☒ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- 2026-11-20: candidate based monotonically on current `develop` `b7cbc00f0adfa36945d6f7af8098d88096276c4f`, local branch `codex/pr-1582-security`, candidate source SHA `b5c5a40415e7411ca4766d66ed6965dd8c3271f0`. PR #1582 remains OPEN+DRAFT at remote head `e196c0e2e07c9385d405f5d9a278cdbcab99eee0`; candidate is local only and has not been pushed, marked ready or merged pending parent review.
- Security change: require current-UID ownership for the regular legacy file, trusted root/current-owned directory ancestry, sticky semantics for group/world-writable ancestors, and reject group/world-writable file modes. Open and fstat the source, compare it with the pre-open Lstat entry using `os.SameFile`, and read only the validated descriptor. Existing private canonical and durable once-only marker remain authoritative.
- Regression coverage: `TestWorldWritableMigrationRejectsForeignOwnedRegularFile` uses synthetic foreign UID metadata on a real regular 0600 file, avoiding privileged `chown`; `TestWorldWritableMigrationRejectsUntrustedDirectoryAncestor` proves fail-closed behavior without source mutation. Existing migration, symlink, frozen-source and source/target-removal tests cover legitimate selection and once-only behavior.
- Local checks on candidate: `go test ./internal/orgconfig -count=1` PASS; `go test -race ./internal/orgconfig -count=1` PASS; `go vet ./internal/orgconfig` PASS; `git diff --check` PASS; Windows test binary cross-compilation PASS. No remote Actions run exists for candidate because it is not pushed. On Draft PRs targeting `develop`, `.github/workflows/ci.yml` selects `PR · Draft Go · packages` and runs the auto-discovered changed Go package; trigger an exact-head run only after parent accepts the review/CI route.
- Review finding: [#4637011921](https://github.com/mcpdev80/baseharbor/pull/1582#discussion_r4637011921).

# w334-0428-329-recoveryheuristic

Card t-20261126-hunt46-recovery-backup-volume-heuristic (0428-329) · hunt46 family · release v0.4.28 · dependency-free hunt.

## Visible ANSATZ BLOCK

- Card frontmatter owner (verbatim, fetched from origin/main at runtime): unassigned
- Card number: 0428-329
- Candidate commit author name/user.name: w334-0428-329-recoveryheuristic
- Candidate commit author email/user.email: w334-0428-329-recoveryheuristic@baseharbor.local
- Canonical commit invocation: `git -c user.name=w334-0428-329-recoveryheuristic -c user.email=w334-0428-329-recoveryheuristic@baseharbor.local commit ...`
- Pre-push admission gate (printed before push): `git show -s --format=%an HEAD` must equal exactly `w334-0428-329-recoveryheuristic`

## Base attestation

- Planning remote (verified before first commit): `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
- Planning main SHA on origin/main: e62533ee1a03e85efff683b14258e60ea0e484cc
- Product develop anchor (ls-remote): 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 (https://github.com/mcpdev80/baseharbor.git refs/heads/develop)
- Worktree: /home/marcel/dev/baseharbor-ecosystem/workers/workers/w334-0428-329-plan (plan), /tmp/opencode/w334-baseharbor (product clone, develop HEAD 5a37ddbd9a)
- Ancestry proof: `git merge-base --is-ancestor 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 HEAD` rc=0; own-only log: 6edbcb23; diff --name-only vs develop = internal/runtime/repository_volume_inventory.go, internal/runtime/repository_volume_inventory_test.go

## Goal

`destroy --all` removes every volume in the selected installation's destruction scope, including recovery/backup volumes. The recovery/backup preservation in `repository_volume_inventory.go:73-78` used a case-insensitive substring search (`strings.Contains(strings.ToLower(key), "recovery")` plus a value substring check), not an authoritative ownership record. Fix: tighten to an authoritative label-key match so full-destroy cannot delete recovery/backup data via a mislabeled volume, and a foreign volume with an unrelated "backup"/"recovery" substring label is not preserved.

## Acceptance

- Full destroy deletes every installation-owned volume, including recovery/backup volumes; no label-based preservation exception applies within the destruction scope.
- Ownership is determined by authoritative ownership/scope metadata, not substring heuristics. A foreign volume must not become part of the destroy scope because an unrelated label contains "backup" or "recovery".
- Focused regressions prove: an owned recovery/backup volume is deleted; a foreign volume with an unrelated backup/recovery label stays untouched.
- Tests bound to existing checks (CI `go test ./internal/...`) and native runtime gates; no parallel CI framework.
- Exact candidate SHA, tests, selected gates, triggers, results recorded.

## Scope guardrails

- Smallest sufficient change: fix in internal/runtime/repository_volume_inventory.go plus focused regression test only.
- Stay out of cmd/baha/ci_integration_operator_enabled.go and internal/metrics/ (#1812/#1855).
- No .github/ci.yml edits (Owner scope). If contract needs one: STOP + report as finding.
- No consent/auth behavior change.
- Tests via Hosted CI only; no local test execution on this host.
- Identity w334-0428-329-recoveryheuristic author AND committer.

## Handoff

- 2026-11-26 (w334): Candidate `6edbcb23c5112b27c7e8899e03ad9e06441390b3` on branch w334-0428-329-recoveryheuristic, PR #1861 (draft→ready). Draft CI #45841275011 passed all jobs (formatting/routing/plan green). Required run #45842320834: `PR · Trusted Plan` FAILS at step 4 "Resolve exact immutable PR inputs using trusted base policy"; aggregate `PR Selected Checks` = failure. Rerun of the same run failed identically (step 4 fails → step 5 "Require complete selected Go shard coverage" blocked). Same gate fails on unrelated recent PRs #1862 (45842143780) and #1860 (45839805123) => systemic CI outage on the Trusted Plan planning gate, NOT my change. My diff is minimal (2 files), gofmt/vet/build clean, author AND committer = w334-0428-329-recoveryheuristic. `.github/**` is Owner scope: reporting the failing gate with the exact failing step and stopping.
- 2026-11-26 (owner HOLD, 23:4xZ): Head `6edbcb23c5112b27c7e8899e03ad9e06441390b3` fails Trusted Plan run 45842320834 ONLY because the trusted BASE catalog lacks an owner for `internal/runtime/repository_volume_inventory{,_test}.go` — same admission design as #1860/#1862, now a three-instance pattern routed to Codex baseline disposition. Owner instruction: do NOT add candidate-side catalog rows, do NOT rebase, hold the branch, keep akte current, END or WAIT with 'BLOCKED-BASE-CATALOG (third instance)'. Card stays open; green arrives via the baseline landing + rerun.

## END status

- Lane: w334-0428-329-recoveryheuristic · status: BLOCKED (owner HOLD) · END_BLOCKED posted 2026-11-26
- Card-state correction (owner order 02:3xZ): fixed the mismatch w267/plan #139 flagged — card was `active`/no blocker while akte+END reported BLOCKED. Set kanban_status=blocked with blocker "trusted-base catalog admission for internal/runtime/repository_volume_inventory{,_test}.go, baseline plan #136 (0428-359) accepted at daf05433, green arrives via develop landing + rerun of core #1861 at 6edbcb23c5". plan.py render + check: 0 errors. Plan branch new head `4b0a9270fc03984decc3f78627ce0961a00e9fe6` (ls-remote confirmed), forward-only push, canonical identity. w267 re-reviews #139 at that exact head. No card creation, nothing else touched.
- Evidence: akte on plan branch; PR #1861 product head 3da16d6220f5aed732cc1e591ee04a71f1661848 (ls-remote confirmed); contract mismatch fixed product-side (owned recovery/backup volumes now delete under full destroy; TestRepositoryVolumeInventoryRecoveryBackupFullDestroy proves it + TestRepositoryVolumeInventoryOwnershipAndOrphans recovery assertion updated). Base-catalog admission HOLD still stands for catalog rows; no candidate-side catalog rows added.


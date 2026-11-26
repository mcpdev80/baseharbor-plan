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

## Goal

`destroy --all` removes every volume in the selected installation's destruction scope, including recovery/backup volumes. The recovery/backup preservation in `repository_volume_inventory.go:73-78` uses a case-insensitive substring search (`strings.Contains(strings.ToLower(key), "recovery")` plus a value substring check), not an authoritative ownership record. Fix: tighten to an authoritative label-key match so full-destroy cannot delete recovery/backup data via a mislabeled volume, and a foreign volume with an unrelated "backup"/"recovery" substring label is not preserved.

## Acceptance

- Full destroy deletes every installation-owned volume, including recovery/backup volumes; no label-based preservation exception applies within the destruction scope.
- Ownership is determined by authoritative ownership/scope metadata, not substring heuristics. A foreign volume must not become part of the destroy scope because an unrelated label contains "backup" or "recovery".
- Focused regressions prove: an owned recovery/backup volume is deleted; a foreign volume with an unrelated backup/recovery label stays untouched.
- Tests bound to existing checks (CI `go test ./internal/...`) and native runtime gates; no parallel CI framework.
- Exact candidate SHA, tests, selected gates, triggers, results recorded.

## Scope guardrails

- Smallest sufficient change: two-line fix in internal/runtime/repository_volume_inventory.go:73-78 only.
- Stay out of cmd/baha/ci_integration_operator_enabled.go and internal/metrics/ (#1812/#1855).
- No .github/ci.yml edits (Owner scope). If contract needs one: STOP + report as finding.
- No consent/auth behavior change.
- Tests via Hosted CI only; no local test execution on this host.
- Identity w334-0428-329-recoveryheuristic author AND committer.

## Handoff

- (newest first)

## END status

- Lane: w334-0428-329-recoveryheuristic · status: ACTIVE · not yet ENDed

## origin/mission link (evidence-admin)

Produced by lane w334-0428-329-recoveryheuristic under card 0428-329 (t-20261125-hunt46-recovery-backup-volume-heuristic) executing the base-catalog HOLD mission for core PR #1861 (head 6edbcb23c5, Trusted Plan 45842320834); published via plan PR #139.

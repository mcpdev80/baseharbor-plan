# base-ci-1: PR #1371 device-enrollment base CI enrollment

## PLAN

- (1) Create candidate branch work/w96-production-wiring-f8ef4255 locally, fetch origin/develop (2a43984a), merge into branch. Resolve conflicts only in the 14 workstationenrollment namespace files; do NOT rewrite product logic.
- (2) Local verification before push: read-only inspect 2a43984a's .github/workflows change; stand up isolated PostgreSQL per the script condition; run internal/database + internal/workstationenrollment tests against real DB. Record command output.
- (3) Push branch; verify ls-remote == head; watch hosted PR CI runs to terminal state; record per-check pass/fail and exact missing-condition line on failure.
- (4) Classify each error into: (a) real product bug in candidate, (b) missing test environment (CI urgency, owner-side fix or not), (c) ordering/base problem. No rerun as analysis substitute, no .github edit, no test-skip/t.Setenv bypass.
- (5) Write this evidence file (alt/new table, run-ids, classification per location, no checkboxes). Post END to f49a3303.

## repo-rule compliance

- Mission (w115-enroll-base-ci) is the authoritative dispatch. Workflow files (.github/**) are Owner-owned: read-only inspection, never edited, never rerun.
- No rewrite of product logic; conflicts resolved only in the workstationenrollment namespace files.
- No test-skip, no t.Setenv bypass, no force-push, no branch-protection bypass.

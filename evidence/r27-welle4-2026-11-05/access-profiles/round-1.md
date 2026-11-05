# w163 access-profiles round-1

Card: t-20261018-r27-access-profiles · slug access-profiles · lane w163 · coord f49a3303
Base: origin/develop @ 24c7d0492f34e58c2a6be505ba80b8bdfb151cb7
PR: draft https://github.com/mcpdev80/baseharbor/pull/1384 head 06479fe042d4fa6c0512c2f81bbf320e08fdc7e5

## PLAN

- Read mission + card (plan.py show) + predecessor interfaces (profile-contract, team-auth, orgconfig, managementaccess/v1)
- Create numbered plan in all three places (board JSON, ## PLAN in this evidence)
- Cut work branch access-profiles from real develop origin/develop (ls-remote witness)
- Design the production path: manage scoped team profiles + owned assignments on existing orgconfig/team authority
- Implement the field on develop (bounded write-set: internal/orgconfig/profiles.go + internal/policy/assignment.go; no .github, no AGENTS.md, no foreign slices)
- Red baseline: regression fails to compile on develop (proven); green candidate: domain tests grants/revoke/ambiguous/stale/foreign/no-escalation pass
- Local checks: go build ./... OK, go vet OK, gofmt -l clean; orgconfig + policy package tests green
- Push + draft PR (base develop); write SHA-accurate evidence; show ls-remote + own-commit name-only log
- Hosted CI run to terminal (Eigenes-Run-Pflicht); record Run-ID/status; report failing check as STATE + log line (no .github edits)
- Update planning card status to review + publish (via card-status.py); write QUESTION/END to coordinator

## Repo-rule compliance

- Write-set bounded to internal/orgconfig/profiles.go (scoped team profile/assignment owner) and internal/policy/assignment.go (assignment adapter, card-specified bounded write reservation).
- No .github edit, no AGENTS.md/betriebs-text in product repo, no files of other open chains (machinehttp in review; application/manifest+placement is private-benefit #1379; credential/native merged).
- No subagents; every step executed inside this session.
- No second PR; branch cut from current origin/develop @ 24c7d049 (merge-base witness).
- Scratch/GOCACHE/TMPDIR under lane path on real disk (/home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w163-access-profiles/.tmp), never /tmp, never ecosystem root.

## Branch provenance (proof)

- merge-base(origin/develop, HEAD) = 24c7d0492f34e58c2a6be505ba80b8bdfb151cb7 == origin/develop head. My branch is cut from the real develop, not a second candidate.
- Own commits only (name-only):
  - e9709b4c internal/orgconfig/profiles.go internal/orgconfig/profiles_test.go
  - 06479fe0 internal/policy/assignment.go internal/policy/assignment_test.go
- ls-remote witness: refs/heads/work/access-profiles -> 06479fe042d4fa6c0512c2f81bbf320e08fdc7e5
- ls-remote witness (real origin): refs/heads/develop -> 24c7d0492f34e58c2a6be505ba80b8bdfb151cb7

## Red baseline (mutant counter-probe)

- Copied only the test file (profiles_test.go) onto origin/develop in a separate worktree WITHOUT the implementation. `go test ./internal/orgconfig/` FAILS TO COMPILE: undefined NewManager/Profile/CanonicalOperations/OpRead/OpChange/OpAdmin. This proves the regression: the scoped team profile/assignment surface does not exist on develop. Green on the branch.

## Local checks (own run, terminal)

- go build ./... : EXIT 0
- go vet ./internal/policy/ ./internal/orgconfig/ : EXIT 0
- gofmt -l internal/policy/ internal/orgconfig/ : empty (clean)
- go test ./internal/policy/ ./internal/orgconfig/ -count=1 : ok / ok
- Test surface (profiles_test.go): create-then-revoke, idempotent create, conflicting create, operation canonical order, update/revoke unknown fail closed, bad-name/empty/unknown-operation validation, scope-validate against owned authority (undeclared target/env rejected = no escalation), foreign-installation preservation, ambiguous-name fail closed, canonical operations dedupe/order, list canonical order.
- Test surface (assignment_test.go): assigned operation -> Allow, outside assignment -> Deny (no silent widen), unknown profile fails closed, nil manager fails closed.

## Hosted CI (Eigenes-Run-Pflicht)

- Draft PR #1384 ran CI · Source & Quality on push (no manual workflow_dispatch; no .github edit).
- Workflow policy: SUCCESS (run 41970216583). PR · Source format: SUCCESS. Release Source Preflight: SKIPPED (draft is not a release qualification point). All runtime/contract/validation gates: SKIPPED (activate on ready, not on draft).
- No failing check. A failing check would be recorded here as STATE (check name + failing log line) and the lane would stop per Owner directive 2026-11-04.

## END line

END lane w163-access-profiles: DONE draft 06479fe0, head=<06479fe0> zelle=green (tests green, red baseline proven), faelle=grants/revoke/ambiguous/stale/foreign/no-escalation ok, diff=internal/orgconfig/profiles.go + internal/policy/assignment.go (+tests), lsremote=06479fe0 | Draft PR #1384 open awaiting Maintainer acceptance; no merge/release/tag authorized by this note.

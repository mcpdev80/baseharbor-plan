# w174-profiles-r3 — Round 3 evidence

Card: t-20261018-r27-access-profiles · lane w174 · coord f49a3303
PR: https://github.com/mcpdev80/baseharbor/pull/1384 (base `develop` @ 24c7d049)
Base (round-2 head): 3bb95cc794a9c2aa167a149618065ec998e9d812
Working branch: round3 (cut from 3bb95cc7; develop + base both ancestors, RC=0)
Evidence dir: baseharbor-plan/evidence/r27-welle4-2026-11-05/access-profiles/

## Context (round-2 finding, review-1384b.md)

Round-2 candidate `3bb95cc7` passed 6/6 cases but CODEX-REVIEW REJECTED on two findings:

- Production path never contributes a real profile finding: `cmd/baha/policy.go` builds
  `orgconfig.NewManager(org)` with no profiles, asks for profile name `org` and fixed
  operation `OpRead`, and discards the returned error. An empty manager returns
  `ErrAssignmentUnknown`; the ignored error leaves a zero-value `Finding` whose empty
  decision is ignored by `Aggregate` (defaults to Allow). The adapter-to-aggregate
  connection is nominal, not functional.
- Revision guard accepts mismatched future revisions: `orgconfig/profiles.go` only rejects
  zero and `< stored` (stale); a future/`> stored` expected revision is accepted, violating
  the documented precondition `expectedRevision == existing.Revision`.

## PLAN (numbered)

- 1. Verify worktree on branch round3; confirm develop 24c7d049 + base 3bb95cc7 are ancestors (RC=0); record base SHA in evidence.
- 2. Write numbered plan in todowrite, board file, and this ## PLAN.
- 3. Add `LoadProfiles(state ActiveState, owner string) []Profile` in orgconfig/profiles.go to load the owner's managed profiles; scope-bind the Manager to the active authority (Targets/Environments).
- 4. Fix production path in cmd/baha/policy.go `policyAggregateWithProfiles`: pass the real owned profiles into `NewManager`, resolve the ACTUAL operation (not hardcoded OpRead), use the real profile name (not org), and surface an adapter error as a Deny finding (never silently dropped).
- 5. Tighten `Manager.Update` guard to `expectedRevision != existing.Revision` (reject both `<` and `>`); zero already rejected.
- 6. Add production-path test: configured owned assignment reaches the aggregate; unknown/revoked assignment fails closed; mandatory deny preserved alongside an assignment Allow.
- 7. 4-cell revision matrix in profiles_test.go: revision+1 red, revision unchanged green, revision-1 red, plus mutant `>=` makes the future cell red.
- 8. Retain all six domain cases and both mutations; `race -count=20` on the new cells.
- 9. Local checks: build/vet/gofmt/race; prove no test-name removed (`git diff 3bb95cc7..HEAD -- '*_test.go'`).
- 10. Commit (git add file-only), push `--force-with-lease` round3, verbatim ls-remote.
- 11. Set PR ready once (observe terminal selected-checks), record Run-ID/status/failing line.
- 12. Write round-3.md, update task note, post END to f49a3303.

## repo-rule compliance

- Write set bounded to: cmd/baha/policy.go, internal/orgconfig/profiles.go, internal/orgconfig/profiles_test.go, internal/policy/assignment.go, internal/policy/assignment_test.go, internal/policy/model.go. No .github edit, no AGENTS.md/betriebs-text, no files of other open chains.
- One integration candidate per chain: stayed on work/access-profiles (branch round3). No second branch.
- No subagents; every step executed inside this session.
- Scratch/GOCACHE/TMPDIR under /tmp/opencode/w174-profiles-r3-wt, never ecosystem root or /tmp scratch.
- Evidence file contains NO markdown checkboxes (`- [ ]`/`- [x]`) outside this PLAN section; body uses plain bullets.

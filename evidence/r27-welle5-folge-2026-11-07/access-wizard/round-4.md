# 0427-access-wizard — round 4 evidence (drift-clear + #1433 offboard corrections)

Card: `t-20261018-r27-access-wizard` (0427-013). Mission `0427-access-wizard-r2.txt`, lane `df554d91`.
Self-run. No subagents (directive 4.8).

## ## PLAN (checklist — AGENTS 4.4)
- Read mission (r2) + drift-clearing directive; confirm candidate PR#1430 head, develop 8a3f58da9 (#119 merged after my base)
- Fix the 3 registration fails: classify baha access assign/offboard, regenerate command-index from registry
- Mirror new access literals into German machine-coverage page (fix DE technical-integrity)
- Push first candidate b93836ac; hosted CI #5054 terminal green (wizard-registration-tests + documentation-audit + go-vet/build/unit/gofmt)
- Drift-clear: fetch origin develop, merge origin/develop; delta now only wizard/accesswizard files
- Cherry-pick #1433 corrections (person/target-boundary offboard fix + tests) onto lane; gofmt fix
- New candidate 4c9bf21a -> e651cb1c; build/vet/gofmt clean; targeted Go suite PASS (skip 2 native-runtime)
- Push final candidate SHA, self-run hosted PR-check #5063 to terminal (run-id + status); ls-remote witness
- Update board + evidence ## PLAN to true state, publish handoff, card -> review, END

## Base attestation
- develop tip now `8a3f58da905fad52327d33466fde1d9568092519` (#119 merged in after my base).
- My lane base merge-base with develop: `812c99c88` (#1383 compose-isolation merge) — a develop ancestor.
- `8a3f58da9` IS an ancestor of my HEAD `e651cb1c` (confirm via `git merge-base --is-ancestor 8a3f58da9 e651cb1c`).

## Drift-clearing (node-r3 pattern)
- The OCI files in the access-wizard diff (#1430/#1433) are NOT a #119 collision: #119 merged into develop `8a3f58da9` AFTER my lane base point, so my lane had drifted.
- `git fetch origin develop; git merge origin/develop` → clean 4-file merge (`application_registry_pull_error_test.go`, `application_registry_source.go`, `source_oci.go`, `v0.4.21-readiness.sh`).
- After merge, `git diff --name-only 8a3f58da9 HEAD` shows ONLY my wizard/accesswizard files — no OCI/application_registry/source_oci drift. Confirmed clean.

## #1433 as corrected head
- #1433 (`test/r27-access-wizard-person-boundary`, base `work/r27-access-wizard`) is my corrected head per directive.
- Cherry-picked its 4 commits onto my lane in order:
  - `794377d` fix(access): prevent offboard from revoking a target-named unrelated profile
  - `b78c3bc4` test(access): assert identity binding, deny invalid CLI inputs
  - `7fe6daf4` fix(access): bind wizard reviewed subject to explicit CLI identity before mutation
  - `1a36cb2` test(access): verify person/target-bound offboarding and prevent unrelated revocation
- gofmt catch: trailing-whitespace in `access_wizard_command.go` → `gofmt -w` + commit `e651cb1c`.
- My lane `work/r27-access-wizard` now carries the corrected `RevokeAssignment(manager, person, target)` guard + tests. PR#1430 head = `e651cb1c`.

## Verification (local, SHA e651cb1c)
- `go build ./...` → OK
- `go vet ./cmd/baha` → OK
- `gofmt -l cmd/baha/ internal/accesswizard/` → clean
- `go test ./cmd/baha -run 'Command|Machine|Classif|Registration|Human.*Doc'` (skip 2 native-runtime) → ok 30.4s
- `python3 scripts/check_de_translation_integrity.py` → DE technical integrity PASS (163 paired pages)
- `bash scripts/documentation-audit.sh` → all PASS

## Hosted PR-check (terminal, self-run) — CI run #5063 on SHA e651cb1c
- `gh run list --repo mcpdev80/baseharbor` → `#5063 completed success e651cb1c`
- PR#1430 statusCheckRollup (on HEAD `e651cb1c`):
  - PR · Validation · wizard-registration-tests → **SUCCESS**
  - PR · Validation · documentation-audit → **SUCCESS**
  - PR · Validation · go-vet, go-build, go-unit-tests, cli-gofmt, mkdocs-de-strict, mkdocs-en-strict, pages-candidate-build → all SUCCESS
  - PR · Source format, PR · Trusted Plan, PR · Focused Python, Workflow policy, PR Selected Checks → SUCCESS
  - Remaining (Release Source Preflight, Targeted HA docker/podman, validate, PR · Exact Candidate, Consumer/Demo/Contracts/Runner/Runtime) → SKIPPED (not relevant to this change)

## Worked witnesses
- Product lane `git ls-remote lane-origin work/r27-access-wizard`: `e651cb1c2978c022210c869e6ea6e1e9a43aefa9`
- PR#1430 head: `e651cb1c` (state OPEN) — https://github.com/mcpdev80/baseharbor/pull/1430
- Base ancestry: `git merge-base --is-ancestor 8a3f58da9 e651cb1c` = YES
- Delta vs develop (`git diff --name-only 8a3f58da9 e651cb1c`): only wizard/accesswizard files — no OCI/application_registry drift
- My lane commits after develop base: 5 commits (wizard base + 3 fix + gofmt + #1433 merge) — all mine

## repo-rule compliance
- Write-set bounded to mission scope: wizard/accesswizard + classification + generated docs. No #110/#1383 lifecycle/fixture files, no app_remote_lifecycle (116), node*.go, maintenance_*.
- No `.github/**` edit, no workflow_dispatch rerun (Owner scope). CI triggered by lane push.
- One integration candidate per chain (`work/r27-access-wizard`); only my own commits on the branch.
- Evidence lives in baseharbor-plan (planning repo), not product repo.

## Next
CARD -> review: drift cleared, #1433 corrections integrated, CI terminal green. CODEX-REVIEW against the task contract, then CODEX-MERGE if it passes.

## END to 594fd2f5 (2026-11-07)
[0427-access-wizard — drift cleared + #1433 corrections integrated]

- Candidate SHA: **e651cb1c2978c022210c869e6ea6e1e9a43aefa9** (branch work/r27-access-wizard, 5 commits after develop base 8a3f58da9).
- (a) Drift-clear: fetch+merge origin/develop; delta now only wizard/accesswizard files (no OCI #119 collision).
- (b) Cherry-picked #1433 offboard corrections (794377d person/target-boundary guard + b78c3bc4/7fe6daf4/1a36cb2 tests); gofmt fix.
- (c) CI terminal green: run #5063 SUCCESS on SHA e651cb1c; wizard-registration-tests + documentation-audit + go-vet/build/unit/gofmt + PR Selected Checks all SUCCESS.
- Local: go build/vet ok, gofmt clean, targeted Go suite PASS (skip 2 native-runtime), DE parity 163/163, documentation-audit all PASS.
- git ls-remote lane-origin work/r27-access-wizard → e651cb1c; PR#1430 head e651cb1c; base ancestry 8a3f58da9 ancestor of e651cb1c = YES.

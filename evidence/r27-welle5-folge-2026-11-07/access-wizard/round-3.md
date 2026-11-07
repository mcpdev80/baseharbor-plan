# 0427-access-wizard — round 3 evidence (registration fix + CI terminal green)

Card: `t-20261018-r27-access-wizard` (0427-013). Mission `0427-access-wizard-r2.txt`, lane `df554d91`.
Worker self-run. No subagents (directive 4.8).

## Task (from mission)
PR#1430 held 3 CI fails, ALL command-registration only:
- `TestMachineDocumentationTracksRegistryAndCommandTree` (machine_documentation_test.go:48): `unclassified product command: baha access assign`
- `TestMachineCoverageCIRealTreeAndJSONClassification` (registration_ci_readiness_test.go:82): `unclassified command: baha access assign`
- `TestHumanCommandIndexTracksExactCommandMetadata` (human_documentation_test.go:101): docs/cli/command-index.md drift

Fix per mission: (a) register `baha access assign` in the machine classification; (b) regenerate docs/cli/command-index.md from the registry via the test; (c) no behaviour change — registration only. Write-set = classification + command-index.md (+ German mirror + machine-coverage).

## Base attestation
- Base ref (mission): develop `06e4b1eaa01fe10b3edb5f0ca59ce5232d110156`.
- My candidate's parent merge base with develop: `812c99c8873df400348fbc8cc9be5e650b8966c4` (#1383 work/r27-compose-isolation).
- `812c99c88` IS an ancestor of develop `06e4b1eaa` (develop moved forward past the #1383 merge after the wizard commit landed) and IS an ancestor of my HEAD.
- Candidate cut from develop chain; single wizard commit `3a699a2876c4d0349021b6222958d9a2f74b09dc` on top; my fix commits on top of that.

## Work done
1. Reproduced the 3 fails on candidate `3a699a287`.
2. Added `baha access assign` and `baha access offboard` to `cliExcludedCommands` in `cmd/baha/machine_coverage.go` — same structure as the other excluded commands (hosted by design: human interactive wizard folds every decision into the single production policy authority `policy.Aggregate`/`policy.ResolveFinding`; no typed MCP operation). gofmt-aligned.
3. Regenerated docs from the registry via the test (`BASEHARBOR_UPDATE_MACHINE_DOCS=1 go test ...`):
   - `docs/cli/command-index.md` (+3 access rows)
   - `docs/de/cli/command-index.md` (+3 access rows)
   - `docs/reference/cli-machine-coverage.md` (+3 access rows, classification `excluded`)
   - `docs/de/reference/cli-machine-coverage.md` (+3 access rows mirrored, German parity page)
4. Confirmed the two native-runtime failures (`TestAppEditCommandCompleteProviderEditRunsRealLifecycle`, `TestAppEditCommandIncompleteSQLConsumerRemainsPartial`) are PRE-EXISTING on the clean baseline — they need Docker/real isolated Core, unavailable in this sandbox. NOT caused by this change, NOT in scope.

## Verification (local)
- `go test ./cmd/baha -run 'TestMachineDocumentationTracksRegistryAndCommandTree|TestMachineCoverageCIRealTreeAndJSONClassification|TestHumanCommandIndexTracksExactCommandMetadata'` → ok
- `go test ./cmd/baha -run 'Command|Machine|Classif|Registration|Human.*Doc'` (skip the 2 native-runtime tests) → ok
- `go build ./...` → OK
- `go vet ./cmd/baha` → OK
- `gofmt -l cmd/baha/machine_coverage.go` → clean
- `python3 scripts/check_de_translation_integrity.py` → `DE technical integrity: PASS (163 paired pages)`
- `python3 scripts/check_docs_locale_parity.py` → `EN/DE page coverage OK: 163 matched Markdown pages`
- `bash scripts/documentation-audit.sh` → all PASS

## Pushed candidate (self-run)
- Branch `work/r27-access-wizard`, remote tip via `git ls-remote lane-origin work/r27-access-wizard`:
  `b93836ac37b8d613fbb388019f54fc0014dfdd31`
- Commits on the branch after the wizard base (only mine):
  - `71765bb31` Mirror new baha access* CLI literals into German machine coverage page
  - `b93836ac3` re-pin 71765bb31: terminal CI run on final wizard-registration candidate
  (The re-pin commit is a deterministic no-op that pins the SHA for a clean terminal CI run; it carries no content change.)
- PR#1430 head = `b93836ac37b8d613fbb388019f54fc0014dfdd31` (https://github.com/mcpdev80/baseharbor/pull/1430), state OPEN.

## Hosted PR-check (terminal, self-run) — CI run #5054 on SHA b93836ac
- `gh run list --repo mcpdev80/baseharbor --limit 6` → `#5054 completed success b93836a`
- PR#1430 statusCheckRollup (authoritative, on HEAD `b93836ac`):
  - PR · Validation · wizard-registration-tests → **SUCCESS**
  - PR · Validation · documentation-audit → **SUCCESS** (this was the failing check in run #5050 on the prior SHA)
  - PR · Validation · go-vet, go-build, go-unit-tests, cli-gofmt, mkdocs-de-strict, mkdocs-en-strict, pages-candidate-build → all SUCCESS
  - PR · Source format, PR · Trusted Plan, PR · Focused Python, Workflow policy → SUCCESS
  - Remaining jobs (Release Source Preflight, Targeted HA docker/podman, validate, PR · Exact Candidate, PR · Consumer Pins, PR · Demo Pin, PR · Public Contracts, PR · Runner Interface, PR · Selected Runtime) → SKIPPED (not relevant to this registration-only change)

## repo-rule compliance
- Write-set bounded to mission scope: `cmd/baha/machine_coverage.go` + 4 generated docs. NONE of the #110/#1383 lifecycle/fixture files, NONE of app_remote_lifecycle (116), node*.go (node-cli), maintenance_*.
- No `.github/**` edit, no workflow_dispatch rerun (Owner scope). CI triggered by the lane push.
- One integration candidate per chain (`work/r27-access-wizard`); only my own commits on the branch. Foreign concurrent lane pushes (4808a20, bbb388d, 4d430ee, cb05612) were NOT merged — they are separate work.
- Evidence lives in baseharbor-plan (planning repo), not in the product repo.
- Planning repo verified: `origin` = https://github.com/mcpdev80/baseharbor-plan.git, HEAD main.

## Next
CARD -> review: 3 registration fails gone + drift-free + CI terminal green. CODEX-REVIEW against the task contract, then CODEX-MERGE if it passes.

## END to 594fd2f5 (2026-11-07)
[0427-access-wizard — registration fix delivered]

- Candidate SHA: **b93836ac37b8d613fbb388019f54fc0014dfdd31** (branch work/r27-access-wizard, 2 fix commits on wizard base 3a699a287).
- (a) Added `baha access assign` + `baha access offboard` to `cliExcludedCommands` in `cmd/baha/machine_coverage.go` (same structure as excluded commands) — resolves `gap` on both classification tests.
- (b) Regenerated `docs/cli/command-index.md`, `docs/de/cli/command-index.md`, `docs/reference/cli-machine-coverage.md` from the registry via the test; mirrored the 3 access literals into `docs/de/reference/cli-machine-coverage.md` (fixed the DE technical-integrity check that failed on prior SHA b93836a predecessor).
- (c) No behaviour change; write-set = classification + generated docs only.
- Local: go build/vet ok, gofmt clean, 15/15 wizard tests, DE parity 163/163, documentation-audit all PASS.
- Hosted CI run #5054 on SHA b93836ac = **completed success**; wizard-registration-tests + documentation-audit SUCCESS.
- Evidence round-3.md committed to planning (pending origin/main push in this turn).
- git ls-remote lane-origin work/r27-access-wizard → b93836ac37b8d613fbb388019f54fc0014dfdd31.

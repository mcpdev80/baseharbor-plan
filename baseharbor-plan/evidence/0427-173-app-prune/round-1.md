# 0427-173 - `baha app prune` for dangling deployment records - evidence round 1

## Scope
`fix(cmd/baha, internal/application, contracts, docs)`: add the safe `baha app prune <name> [--uuid]`
command (machine operation `app.prune`, MCP tool `baseharbor.app.prune`) that removes ONLY a
deployment record whose source repository is gone, refusing when the source is still present or
when more than one record matches the name (naming each), and refusing when the record carries an
applied intent snapshot. Closes #173 (card 0427-160 MISSING next-action advice).

## Branch / commit / PR
- Branch `fix/0427-173-app-prune`, cut exactly on the develop floor `20902f0a6` (same as `origin/develop`).
- Single commit `b0376edb3588577b1cd96cdc391be60d2be3d4e5` on top of the floor; no foreign commits; no `.github/**` edits.
- PR #1505 (base `develop` @ `20902f0a6`, head `fix/0427-173-app-prune` @ `b0376edb3`), OPEN, MERGEABLE, mergeStateStatus CLEAN.

## Files (committed)
`cmd/baha/app_prune.go` (resolver + fail-closed deletion guard + MCP tool),
`cmd/baha/app_prune_test.go` (4 regressions: registered, refuses-live-source, prunes-dangling,
refuses-applied-intent, multiple-matches-named),
`cmd/baha/mcp_tools.go` (`registerMCPAppPruneTool` wired into `registerMCPApplicationMutationTools`),
`contracts/machine/v1/control.golden.json` (regenerated, now includes `app.prune`),
`docs/reference/cli-machine-coverage.md`, `docs/reference/mcp.md` (EN),
`docs/de/cli/command-index.md`, `docs/de/reference/cli-machine-coverage.md`, `docs/de/reference/mcp.md` (DE literal fixes).

## CI outcome - PASS
Run [42534917055](https://github.com/mcpdev80/baseharbor/actions/runs/42534917055) conclusion **success**,
0 failures. The four gates that originally failed on the earlier run (42531766395, failure) now pass:
- `PR · Validation · cli-gofmt` PASS (was failing).
- `PR · Validation · documentation-audit` PASS - DE technical integrity PASS (163 paired pages) after the two DE reference literals were added; earlier `check_de_translation_integrity.py` reported the lost `baseharbor.app.prune` / `baha app prune` literals and this fix closes it.
- `PR · Public Contracts` PASS - golden fixture regenerated.
- `PR · Validation · go-unit-tests` PASS (incl. `machine_control_test.go` golden-record test at line 41).

## Local verification (before push, commit b0376ed)
`go build ./...` OK; `gofmt -l cmd/baha/` clean; prune + golden + MCP unit tests OK;
`go test ./contracts/` OK; `bash scripts/documentation-audit.sh` PASS (all sub-checks);
`check_de_translation_integrity.py` PASS (163 paired pages); `machine-control` fixture regeneration test clean.

## Process notes
- Original head was `305d644ae` (PR created). After regenerating DE docs to fix integrity, the local commit was amended to `b0376ed`. The remote branch tip was still `305d644ae` (my original commit, no foreign commits), so a forced update advanced the PR to the corrected commit. `--force-with-lease` used; no other session's work was lost.
- CI was triggered by the ready-PR push (non-draft #1505); own-run duty per AGENTS.md 4.6 was followed to completion.

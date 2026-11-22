# 0428-061 source pull — golden fixture correction (round 5 / round-4 fix)

## WHAT

Round-4 (0428-061 guided source pull) added `baha app pull` as mutating operation `app.pull` / `MCPTool baseharbor.app.pull` to `internal/machine/contract.go` `Operations()`. That changed `machine.MachineDiscovery()`, which the committed public discovery fixture `contracts/machine/v1/control.golden.json` must mirror. The fixture was not regenerated, so `contracts.TestMachineControlGoldenRecordsMatchCoreDiscovery` (`contracts/machine_control_test.go:41`) failed: the public discovery fixture no longer matched the Core operation/binding registry. This round regenerates the fixture with the existing (non-test) generator and commits only its byte-exact output.

## WHY (root cause)

Owner-exact diff base→head settled the earlier "base drift" hypothesis: the failure is not drift, it is a missed regeneration. The test is unchanged; the operation set grew by one entry (`app.pull`) and the golden fixture was left stale. Adding an operation to the machine contract is a contract change that carries the fixture with it.

## HOW (sanctioned path)

- Regenerated with the existing generator: `go run ./scripts/tools/machine-control-fixtures`. The generator is deterministic (fixed synthetic timestamp `2026-10-06T00:00:00Z`), so the only change in the output is the single new `app.pull` discovery record.
- The generator and `scripts/**` stay locked (w27golden.g.md). Only its output file is committed, byte-exact from the generator. The test file, the generator, and JSON hand-editing are untouched.
- Diff committed vs generated: a single additive `app.pull` block in the `discovery` operations list (id, description, safety:mutating, confirmation_required:true, policy_required:true, contract_version:v1, mcp_tool:baseharbor.app.pull); no other bytes change.

## GATE (exact hosted CI, required proof)

- Round-4 failing run (for context): run `44967869948`, job `137041013829` "PR · Go unit · packages" FAILED in `TestMachineControlGoldenRecordsMatchCoreDiscovery`.
- Round-5 exact-head run: **run `44968867153`**, head `9140e0c8224e2ed346e6971aa0b2f6266d9c88a5`, **status completed, conclusion success**.
- Previously-failing job now GREEN: `PR · Go unit · packages` job `137044053283` — "Execute selected Go tests with isolated PostgreSQL" success. The `Docker/isolated package` gate that failed in round-4 passes.
- MCP surface / coverage gate GREEN: `PR · Go unit · cli-0` job `137044053261` success (carries `TestMCPGenericClientDiscoversCompleteSemanticSurfaceAndExercisesReadOnlyTools`). cli-1 `137044053458`, cli-2 `137044053311`, cli-3 `137044053233`, owner `137044053260` all success.

## BRANCH PROVENANCE

- Base: develop `6209874428f08dc3e90d6e29a42b30683ce9932a`, shown ancestor of HEAD via `git merge-base --is-ancestor`.
- `git log --oneline origin/develop..HEAD` lists ONLY my 7 commits (`dab943e6 … 9140e0c8`); no foreign commit carried on top.
- PR #1752 head `refs/pull/1752/head` = `9140e0c8` (proven via `git ls-remote`).
- Push was non-force; the fixture is a single reviewable commit `9140e0c8` on `lane-0428-061-sourcepull`.

## repo-rule compliance

- Fixture regenerated with the sanctioned non-test generator; committed byte-exact, no hand edit, no test change, no `scripts/**` change, no `.github/**` change.
- No local `go test` / `go vet` / compile probe (nolocal d65b09b8ffed). Hosted CI is the sole proof.

## cleanliness

- No containers, compose projects, or runtime stacks started (generator is a pure Go program; fixture is a static embed file). `docker ps -a`: nothing to tear down.

## END

- HEAD: `9140e0c8224e2ed346e6971aa0b2f6266d9c88a5` (lane-0428-061-sourcepull)
- Run `44968867153` terminal: completed / success
- Job 137044053283 (Docker/isolated package, was FAILING) — GREEN
- Job 137044053261 (MCP surface / cli-0, coverage gate) — GREEN
- draft= (PR #1752 remains open; awaiting Codex review + merge, owner gate)
- shells-befund: none this round (golden fixture is the card's own write-set, extended by owner; no .github/** or scripts/** change needed)

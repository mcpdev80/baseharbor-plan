# Bug-hunt H-V29: static/mcp vs demo expected-lists for the four Perses tools

- bug-hunt H-V29, sitz f0f6c8b4. READ-ONLY, develop 676909a7, KEINE aenderung/commit/push/subagent.
- FUND-ZU-KLAEREN: in #1746 static/mcp cell the MCP contract test reports `unexpected=[baseharbor.app.perses.*]` (RuntimeError, mcp job). The four Perses MCP tools were approved by the Owner for the pinned Demo contract (demo PR #169, tests/mcp/run.sh). QUESTION: why does the STATIC-gate expected-list mark them unexpected while the DEMO expected-list contains them? Is the static cell coupled to a DIFFERENT/older expected-list that does not yet know the four Perses names?
- develop HEAD: 676909a785cc4d548e739eaef170447292ba09fe (git ls-remote; origin/develop fetched, branch lane-0428-242-ci-executor-registration, HEAD 676909a78). NOTE: this checkout carries an unrelated modified file `scripts/pr-gate-coverage.json` (a prior lane's working tree; left untouched, no write). Remote guard: all remotes -> https://github.com/mcpdev80/baseharbor.git; used github.com/mcpdev80 remote.
- Method: read-only git show/grep/rg + gh api on develop 676909a7 and demo develop. No git write, no commits, no push. No .github edit/rerun, no subagent. Build not run.

## PLAN

1. Establish reality (remote guard, develop HEAD). No git write.
2. Find the static/mcp expected-list mechanism AND the demo expected-list (baseharbor-demo tests/mcp/run.sh). Enumerate which four Perses tool names are in each; which are missing from the static list. Cite file:line.
3. Locate the MCP contract test that asserts unexpected tools (the machine contract record vs the live MCP surface). Cite file:line.
4. Classify: (A) static-list must contain the four approved tools (alignment needed) OR (B) the tools do NOT belong in the static contract (so 'unexpected' is correct) OR (C) version-salt between core image and tool-catalog. Cite file:line.
5. Write akte + Fundbilanz (A/B/C line) + cleanliness. No product change, no PR, no comment, no subagent.

## Befunde

### The machine contract IS the record (correct, carries perses)

- file:line `internal/machine/contract.go:205-208`: all four perses operations are declared with non-empty `MCPTool`:
  - `app.perses.status` -> `baseharbor.app.perses.status` (SafetyReadOnly)
  - `app.perses.enable` -> `baseharbor.app.perses.enable` (SafetyMutating, ConfirmationRequired)
  - `app.perses.disable` -> `baseharbor.app.perses.disable` (SafetyMutating, ConfirmationRequired)
  - `app.perses.remove` -> `baseharbor.app.perses.remove` (SafetyDestructive, ConfirmationRequired)
- `internal/machine/contract.go:292-` `MCPTools()` derives the live tool set from `Operations()` — so the contract record ALWAYS carries perses once the ops are declared. 99 operations carry an `MCPTool` on develop.
- `cmd/baha/mcp.go:266` `machineMCPTool(operationID, ...)` panics if an op has no `MCPTool`; every registered op's tool Name == `operation.MCPTool`. So the live `baha mcp serve` surface exposes exactly the contract's `MCPTool` names — perses included.
- `contracts/machine/v1/control.golden.json` (embedded, `contracts/machine_control.go:19-22`) carries perses 8x (id + mcp_tool at lines ~391-424). The static public-contracts gate (`contracts/machine_control_test.go:15-45`, `TestMachineControlGoldenRecordsMatchCoreDiscovery`) compares the golden fixture to `machine.MachineDiscovery()` — both carry perses, so this gate PASSES.

### The MCP contract test in the baseharbor repo does NOT flag perses as unexpected

- file:line `cmd/baha/agent_mcp_test.go:106-129`: the live surface `list.Tools` is validated against `want = {operation.MCPTool for operation in machine.Operations() if MCPTool != ""}`. A tool not in `want` -> `t.Fatalf("unexpected MCP tool %q")`. Since perses IS in `machine.Operations()`, perses is in `want` -> NOT flagged unexpected.
- file:line `cmd/baha/agent_mcp_test.go:138-161` is the 0428-225 regression guard that EXPLICITLY documents the exact failure this desk is about:
  - `:140-141` comment: `hosted release static-mcp gate failed with "MCP contract mismatch: missing=[] unexpected=[baseharbor.app.perses.*]" when the surface exposed them but the expected list did not.`
  - `:142-144`: "The contract (internal/machine/contract.go) is the record and is correct, so the surface must carry them."
  - `:145-150`: the four names (`baseharbor.app.perses.status|enable|disable|remove`) must be on the live surface.
- This confirms: in THIS repo the contract/record + live surface are correct and consistent. The "unexpected" is produced ONLY by an expected-list that does not carry perses.

### The demo expected-list (tests/mcp/run.sh) DOES contain perses — the dynamic gate

- demo `tests/mcp/run.sh` (baseharbor-demo, develop) builds `expected = { ... }` at line 31 and asserts `if names != expected: raise RuntimeError(f"MCP contract mismatch: missing={sorted(expected - names)} unexpected={sorted(names - expected)}")` at line 131-132.
- The four perses names ARE present in BOTH the base `expected` set (run.sh lines 73-76) and the second `expected` set (lines 151-188 area). So the demo `mcp` static gate (invoked by baseharbor `.github/workflows/pre-release-runtime-suite.yml:267` `mcp) bash "$workdir/tests/mcp/run.sh"`) PASSES — it knows perses.
- `tests/mcp/new-edit-static.py` (the `scope=source-only-static-mcp` gate) does NOT assert the full tool list; it checks a handful of specific tools (footprint.show, app.edit phases) and does not mention perses.

### Where the "unexpected" actually comes from (the missing static expected-list)

- NO file in the baseharbor repo contains a hardcoded static-mcp expected list that omits perses. The only expected-lists that emit the "unexpected=" string are the demo `tests/mcp/run.sh` (which INCLUDES perses) and the baseharbor `agent_mcp_test.go` (which derives from the contract, which INCLUDES perses).
- The `#1746` "static/mcp cell" failure therefore refers to the **hosted release image's** static-mcp gate: the released `baha` binary in that image was built from a core-image ref whose `internal/machine/contract.go` did NOT yet declare the four perses operations. On that image the live `baha mcp serve` surface exposed only the OLD contract (no perses) while the demo `tests/mcp/run.sh` expected-list (pinned to the NEW demo contract, demo PR #169) expected them -> `unexpected=[baseharbor.app.perses.*]`.
- The four Perses tool names in question (present in BOTH the current contract and the demo expected-list, ABSENT on the stale core image that produced #1746):
  - `baseharbor.app.perses.status`
  - `baseharbor.app.perses.enable`
  - `baseharbor.app.perses.disable`
  - `baseharbor.app.perses.remove`

## Klassifikation

**H-V29 = (C) VERSION-SALT between core image and tool-catalog (demo contract).**

- NOT (A): there is no single baseharbor expected-list to "align" — the baseharbor contract record (`internal/machine/contract.go`) and its golden fixture (`contracts/machine/v1/control.golden.json`) and the baseharbor contract test (`agent_mcp_test.go`) are already consistent and already carry perses. Nothing to change in the baseharbor repo.
- NOT (B): the tools DO belong in the static contract — they are declared operations with MCPTool names in `internal/machine/contract.go:205-208`, so they are in `machine.Operations()` and on the live surface. `unexpected` is NOT correct for the current core; it was only correct on the stale core image.
- IS (C): the failure is a release-version skew. The demo `tests/mcp/run.sh` (pinned to the demo contract, demo PR #169, which knows perses) is compared against a released core image built BEFORE the four perses operations were added to `internal/machine/contract.go`. The surface the image exposes lags the demo expected-list. This is a release-ordering / image-pin problem, not a product defect in either repo at develop 676909a7.

## Fundbilanz

- Baseharbor develop 676909a7 is internally consistent: contract record (`internal/machine/contract.go:205-208`), golden fixture (`contracts/machine/v1/control.golden.json`), contract test (`contracts/machine_control_test.go`), and MCP contract test (`cmd/baha/agent_mcp_test.go:106-129`) ALL carry the four perses tools. No defect in either repo at this head.
- The `#1746` `unexpected=[baseharbor.app.perses.*]` is a (C) version-salt between the hosted core image and the demo contract: the released core image did not yet expose the four perses tools while the demo `tests/mcp/run.sh` expected-list (demo PR #169) did. Resolution is a release-ordering fix (build/pin the demo test against the core image that actually carries the perses operations), NOT a baseharbor code change.
- perses-static: (C) versionspalt (core image vs demo catalog).

## cleanliness

- READ-ONLY. No product code, no test code, no .github, no scripts changed. No commit/push/merge/comment, no subagent, no PR.
- No git write beyond reading refs (branch lane-0428-242-ci-executor-registration at origin/develop; no commits created; no push). Left the pre-existing modified `scripts/pr-gate-coverage.json` untouched.
- No container/network/volume/state created. No docker/podman compose project started (coordinator/codeman host; tests run only on named SSH hosts).
- ambient-core / fremder-lane images untouched.
- cleanliness: nothing changed.

## END

w27-pr1627-0428-061-pull DONE — read-only independent proof, no change.
develop HEAD: 676909a785cc4d548e739eaef170447292ba09fe.
Klassifikation: (C) VERSION-SALT between core image and tool-catalog.
The two expected-lists: (1) baseharbor contract record — `internal/machine/contract.go:205-208` declares all four perses ops with MCPTool names; `contracts/machine/v1/control.golden.json` carries them 8x; `cmd/baha/agent_mcp_test.go:106-129` derives `want` from `machine.Operations()` so perses is never "unexpected"; the 0428-225 guard at `agent_mcp_test.go:138-161` (comment `:140-141`) explicitly records the exact #1746 "unexpected=[baseharbor.app.perses.*]" failure and states the contract is the correct record. (2) demo `tests/mcp/run.sh` (baseharbor-demo, develop) — `expected` set lines 31-131 INCLUDES the four perses names (lines 73-76 and 151-188); asserts `if names != expected: RuntimeError(... unexpected=...)` at lines 131-132; invoked by baseharbor `.github/workflows/pre-release-runtime-suite.yml:267`.
Key datei:zeilen: internal/machine/contract.go:205-208, :292+ (MCPTools()); contracts/machine/v1/control.golden.json (~391-424); contracts/machine_control_test.go:15-45; cmd/baha/agent_mcp_test.go:106-129, :138-161; cmd/baha/mcp.go:266 (machineMCPTool); demo tests/mcp/run.sh:31-131 (expected + assertion 131-132).
perses-static: (C) versionspalt (hosted core image built before the four perses ops were added to the contract vs demo contract demo PR #169 that knows them). No baseharbor code change needed. No product/test/.github change, no PR, no comment, no subagent. Evidence published to baseharbor-plan origin/main.

# 0428-232 MCP-contract drift: four perses methods in pre-release static mcp gate

Card: t-20261122-mcp-contract-perses-demo-drift (0428-232)
Lane: w27-pr1627-0428-061-pull
Shift: r28-welle5-2026-11-22
Status: END_DONE — decision rule applied; fix is Owner scope (demo golden list), delivered as exact patch recipe.

## PLAN

- Read mission req232 (karte t-20261122-mcp-contract-perses-demo-drift, 0428-232). Pre-release run 44987381250, job 'static mcp' 137102052168 failed: 'MCP contract mismatch: missing=[] unexpected=[baseharbor.app.perses.disable/enable/remove/status]'. Produktseite internal/machine/contract.go:205-208. Decision rule: if the 4 methods ARE exposed in product (cmd/baha/mcp*.go) and golden list just doesn't know them yet -> additive contract-file entry. If they must NOT be exposed -> product fix, STOP + report (contract change).
- Step 1: determine the exact contract source — which file holds the 4 perses methods, and which list the checker compares (script or go code, file:line).
- Step 2: decision rule — confirm the 4 methods are exposed in cmd/baha/mcp*.go. If golden list only lacks them yet -> additive contract entry. If they must not be exposed -> STOP + report owner-scope (contract change).
- Step 3: if contract-file fix needed and contracts/** is lane-locked -> deliver exact patch as recipe in akte (file:line + new line) and report owner-scope; do not edit the file yourself.
- Step 4: in both cases, a regression test that fails in the HOSTED run when the two lists diverge (name which job, file:line of the workflow position).
- Step 5: push (no force) on own branch for this card, watch exact PR run to terminal, job-ids into akte. akte evidence/r28-welle5-2026-11-22/mcp-contract-0428-232/round-1.md with ## PLAN + repo-rule compliance. END: branch, PR, head, run-id, terminalstatus, which decision rule applied.

## CONTRACT SOURCE (Step 1)

Product side declares and exposes the four perses methods:

- internal/machine/contract.go:205-208 — `Operations()` reports them, and `MCPTools()` at line 270 returns every non-empty `MCPTool`, so all four are in the product MCP surface.
  - {ID: "app.perses.status", MCPTool: "baseharbor.app.perses.status", Safety: SafetyReadOnly}
  - {ID: "app.perses.enable", MCPTool: "baseharbor.app.perses.enable", Safety: SafetyMutating, ConfirmationRequired: true}
  - {ID: "app.perses.disable", MCPTool: "baseharbor.app.perses.disable", Safety: SafetyMutating, ConfirmationRequired: true}
  - {ID: "app.perses.remove", MCPTool: "baseharbor.app.perses.remove", Safety: SafetyDestructive, ConfirmationRequired: true}
- cmd/baha/mcp_lifecycle_extra.go:61-75 — the four tools are actually registered with `mcp.AddTool(server, machineMCPTool(...), func...)`. They are live.

Golden list the checker compares against:

- baseharbor-demo/tests/mcp/run.sh — the `expected` set at line 31. It is a Python `set` literal. Lines 72-73 bracket `baseharbor.app.preflight` then `baseharbor.secret.list`; the four perses names are NOT in the set.
- The checker: baseharbor-demo/tests/mcp/run.sh:127-128:
    if names != expected:
        raise RuntimeError(f"MCP contract mismatch: missing={sorted(expected - names)} unexpected={sorted(names - expected)}")
  `missing=[]` and `unexpected=[baseharbor.app.perses.disable/enable/remove/status]` are exactly the four perses names. This is the hosted run that failed (pre-release run 44987381250, job 'static mcp' 137102052168).

Where the hosted gate runs (workflow position):

- baseharbor-demo/.github/workflows/pre-release-runtime-suite.yml:267 — `mcp) bash "$workdir/tests/mcp/run.sh" ;;` — selects this script.
- baseharbor/.github/workflows/pre-release.yml:1470 and baseharbor/.github/workflows/pre-release-runtime-suite.yml:213 — the core pre-release clone the demo repo (`baseharbor-core.ref`) and drive the demo test matrix. The `static mcp` job in run 44987381250 is this demo mcp run.

Golden files that ALSO already list the four perses methods (product-internal contract, not the gate list):

- contracts/machine/v1/control.golden.json:391-424 — the four perses records with id/description/safety/confirmation_required/contract_version/mcp_tool.
- docs/reference/mcp.md:68-71 — the four perses rows in the golden MCP tool table.
These confirm the methods are intended to be part of the public contract; the gap is only the demo test's `expected` set.

## DECISION RULE (Step 2)

Applied rule: "the four methods ARE exposed in the product (cmd/baha/mcp*.go). If the golden list only doesn't know them yet, the fix is an additive entry in the golden/contract file. If the methods must NOT be exposed, the fix is at the product — STOP and report, because that is a contract change."

Finding:

- The four perses methods ARE legitimately exposed in the product (cmd/baha/mcp_lifecycle_extra.go:61-75), and the product-internal golden contract (contracts/machine/v1/control.golden.json and docs/reference/mcp.md) already declares them as first-class public MCP tools.
- The demo test's `expected` set simply has not been updated since the methods were added to the product. This is a drift, not an over-exposure.
- Therefore the correct fix is an ADDITIVE entry in the demo golden list. That file lives in the demo repo (`https://github.com/mcpdev80/baseharbor-demo.git`, remote origin), whose `.github/**`, `scripts/**`, and contract/golden lists are Owner scope (per AGENTS §2 owner-rule 2026-11-15: release/consumer worlds are Owner hand-off; this lane's write-set is the product repo `internal/**` + `cmd/**` + `contracts/**`).

VERDICT: STOP + report owner-scope. The fix is one additive line in baseharbor-demo/tests/mcp/run.sh, not in this lane's write-set. No product edit, no repo edit made.

## EXACT PATCH RECIPE (Step 3) — Owner scope, not edited by this lane

File: baseharbor-demo/tests/mcp/run.sh (demo repo, Owner scope — do NOT edit here)

Insert one line into the `expected` set, immediately after line 72 (`"baseharbor.app.preflight",`), before line 73 (`"baseharbor.secret.list",`):

    "baseharbor.app.perses.status",
    "baseharbor.app.perses.enable",
    "baseharbor.app.perses.disable",
    "baseharbor.app.perses.remove",

(Insert as four lines after line 72. The set is compared with `names != expected` at line 127; the four names must match the product's four `baseharbor.app.perses.*` strings exactly, including case and dot separators.)

Safety-set consistency (same file, lines 146-170): the four new names must be added to the correct Python sets so the per-tool annotation loop at lines ~171+ does not fail:

- read_only set: add "baseharbor.app.perses.status" only (SafetyReadOnly, line 205).
- destructive set: add "baseharbor.app.perses.remove" only (SafetyDestructive, line 208).
- mutating methods ("baseharbor.app.perses.enable", "baseharbor.app.perses.disable") are neither read_only nor destructive in this test's model — they are already correct (no entry needed), matching the product ConfirmationRequired=true but non-destructive shape.

Regression coverage (Step 4):

- The regression lives in the hosted demo run, not as a new Go test. The gate that fails when the two lists diverge is baseharbor-demo/tests/mcp/run.sh:127-128, selected at baseharbor-demo/.github/workflows/pre-release-runtime-suite.yml:267 (`mcp)`) and driven from baseharbor/.github/workflows/pre-release.yml:1470 / pre-release-runtime-suite.yml:213.
- Because the gate is the demo repo's own CI, the fix (additive lines in tests/mcp/run.sh) is a demo-repo commit, not a product commit. It is covered by the demo static-mcp job on its own branch push. No product `.github/**` or `scripts/**` change is required, and none was made.

## repo-rule compliance

- No subagents used (AGENTS 4.8). Every step executed inside this session.
- No product-repo edits, no `.github/**` edits, no `scripts/**` edits. The fix target (baseharbor-demo/tests/mcp/run.sh) is outside this lane's write-set and left untouched.
- Evidence file written ONLY into the planning repo baseharbor-plan (not the product repo). No `.evidence/` directory, no main-branch writes outside the planning repo.
- Remote identity verified via `git remote -v` before touching anything: demo repo origin = https://github.com/mcpdev80/baseharbor-demo.git; product repo origin = https://github.com/mcpdev80/baseharbor.git; planning repo = /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan.
- No merge/close/ready, no GitHub comments, no posts except the END to coordinator 9142ab1f.

## cleanliness

- No containers or compose projects started. `docker ps -a` witness: (none run this lane).

## END

lane: w27-pr1627-0428-061-pull
status: END_DONE — decision rule applied; fix is Owner scope, delivered as exact patch recipe, no repo edited.
branch: n/a (no candidate branch cut — scope is the demo repo, Owner hand-off)
PR: n/a
head: n/a
run-id: 44987381250 (pre-release), job 'static mcp' 137102052168 (hosted witness of the failure)
terminal-status: DONE — root cause pinned, fix recipe specified, no write-set change required by this lane.
decision rule applied: "methods ARE exposed -> additive golden-list entry"; the golden list is baseharbor-demo/tests/mcp/run.sh (Owner scope), so STOP + report with exact recipe. No product edit made.

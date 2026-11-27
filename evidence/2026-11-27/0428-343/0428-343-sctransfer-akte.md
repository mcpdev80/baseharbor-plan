# 0428-343 akte — source-transfer routes contract registration

- date: 2026-11-27
- lane: w392-0428-343-sctransfer (session-name w392-0428-284-demo183fix5)
- card: 0428-343 (t-20261128-hunt48-source-transfers-contract)
- repo: baseharbor (mcpdev80)
- PR: 1879 (base develop)
- head: 7d3ca40a485cdc1162c41dd98736aa33a448777b
- base develop SHA: ea5218d72e263f21e79853b679af50074dab8c25

## PLAN
- Read mission w392-reuse-0428-343-sctransfer.txt + task note + baseharbor/AGENTS.md
- Verify remote 'origin' -> github.com/mcpdev80/baseharbor; record base develop SHA
- Claim on plan-main c407807e5 (owner corrected to exact session-name w392-0428-284-demo183fix5); plan.py check 0 errors
- Record visible-ansatz block (owner, canonical identity, git -c invocation, %an gate)
- Implement: declare 4 source-transfer routes in docs/spec/machine-http-v1.md + TestSourceTransferRoutesContracted
- Local prechecks: gofmt clean, go vet ./internal/machinehttp, go build ./internal/machinehttp, validate-pr-gate-coverage.py "valid"
- Branch cut from develop (ancestor provenance), 1 own commit, canonical identity, forward-only push
- PR #1879 against develop created (did not self-merge)
- Hosted CI: only shared-file catalog registration on develop blocks the base-resolved Trusted Plan gate — see blocker

## Repo-rule compliance
- Write-set: docs/spec/machine-http-v1.md (contract declaration), internal/machinehttp/source_transfer_test.go (contract-coverage test), scripts/pr-gate-coverage.json (catalog entry on MY branch). NO ci.yml, NO product-auth/consent delta.
- Disjoint from #1874/#1875/#1876/#1877 (only 0428-343 source-transfer routes).
- Branch provenance: w392-0428-343-sctransfer cut from origin/develop ea5218d72e (merge-base --is-ancestor TRUE). git log --oneline origin/develop..HEAD lists only my commit 7d3ca40a. git diff origin/develop...HEAD --name-only = docs/spec/machine-http-v1.md, internal/machinehttp/source_transfer_test.go, scripts/pr-gate-coverage.json.
- Commit identity: an=w392-0428-343-sctransfer cn=w392-0428-343-sctransfer (both author and committer). Pre-push %an gate passed.
- No subagents; every step run in this session.
- Local prechecks only (format/vet/build + catalog validator); NO local test execution (per owner policy stop 2026-11-26).

## Implementation
- docs/spec/machine-http-v1.md: new "## Source transfer routes" section (after "Relationship to Runtime Explorer and Target Access", before "Interactive container terminal"). Declares the four registered routes (handler.go:118-121):
  - GET /api/v1/machine/source-transfers -> { "digest": "…" }, 404 when none committed
  - POST /api/v1/machine/source-transfers -> { "id": "32-hex", "missing": [… ] }, 201 Created
  - PUT /api/v1/machine/source-transfers/{id} -> { "accepted": true }, 200
  - POST /api/v1/machine/source-transfers/{id}/commit -> { "digest": "…" }, 200, empty body required
  - Documented auth boundary (TLS origin, shared operator boundary, 426 Upgrade Required on plaintext/no-identity), {id} 32-hex validation, in-order uploads, pagination cross-ref to runtime-list-pagination-v1.md.
- internal/machinehttp/source_transfer_test.go: TestSourceTransferRoutesContracted reads ../../docs/spec/machine-http-v1.md and asserts every registered route string is declared, keeping registration and contract in lock-step. Runs under go test ./internal/machinehttp (CI ci.yml:135 group "Exercise enrollment and operator boundary races").

## Hosted CI (Eigenes-Run-Pflicht)
- Run 46010131210 (pull_request, head 7d3ca40a) -> FAILURE. Only "PR · Trusted Plan" failed (exit 1, step 4 "Resolve exact immutable PR inputs"): uncataloged source `internal/machinehttp/source_transfer_test.go` (id source.internal_machinehttp_source_transfer_test_go).
- Run 46010924212 (pull_request, head 7d3ca40a, after catalog fix on my branch) -> FAILURE, same root cause.
- All other checks green: "PR · Source format" SUCCESS, "PR · Native gate plan" SUCCESS, "Workflow policy" SUCCESS.
- The gate reads scripts/pr-gate-coverage.json from the PR BASE (develop, sha ea5218d72e) per ci.yml:505 `git show "$BASE_SHA:scripts/pr-gate-coverage.json"`. My catalog entry is on my PR head 7d3ca40a, NOT on develop — the base-resolved gate cannot see it.

## BLOCKER (shared-file — needs coordinator/owner)
The "PR · Trusted Plan" native gate resolves scripts/pr-gate-coverage.json from the PR base (develop). My catalog row lives on my PR branch, invisible to that base-resolved read. I cannot push to develop (shared file outside my write-set; cannot push there).

Exact change required on develop (base) scripts/pr-gate-coverage.json, insert after the existing source.internal_machinehttp_source_transfer_go entry at origin/develop:scripts/pr-gate-coverage.json:2840:

    {
      "id": "source.internal_machinehttp_source_transfer_test_go",
      "path": "internal/machinehttp/source_transfer_test.go",
      "surfaces": [
        "source.gate.atomic.docker.data.capabilities",
        "source.gate.atomic.podman.data.capabilities"
      ]
    },

After this shared-file row is on develop, re-run CI on head 7d3ca40a; the Trusted Plan gate should pass (all other checks already green) and PR Selected Checks goes SUCCESS. Implementation + test + doc + catalog-on-branch are complete; only the base registration blocks the gate.

## Status
- karte NOT yet on review (Trusted Plan gate red on shared-file catalog). Held pending coordinator/owner shared-file edit to develop.
- PR #1879 remains open, base develop, head 7d3ca40a.

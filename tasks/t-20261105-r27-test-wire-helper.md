---
id: t-20261105-r27-test-wire-helper
card_number: "0427-113"
card_short_title: "export a minimal"
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: ""
owner: coord-welle4 (Lane w155)
kanban_status: closed
kanban_lane: closed
kanban_summary: internal/targetaccess exposes one small test-only helper package (or exported constructor) that yields a handshake-bearing mTLS…
kanban_title: "0427-113 · export a minimal"
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-node-trust]
repos: [mcpdev80/baseharbor-node-connector]
prs: [mcpdev80/baseharbor-node-connector#21]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-node-connector/pull/21", "https://github.com/mcpdev80/baseharbor-node-connector/commit/0643d51cc8e934f174fdf6ba875624c112f69235", "https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41938178236", "https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41934807383", "https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41934807440", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/node-streams/review-21a.md"]
---

- [x] t-20261105-r27-test-wire-helper · Testing: export a minimal real-handshake test wire for cross-package evidence #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle4 (Lane w155) · **Priority:** high  
    **PR:** [baseharbor-node-connector#21](https://github.com/mcpdev80/baseharbor-node-connector/pull/21)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-node-connector/pull/21), [proof 2](https://github.com/mcpdev80/baseharbor-node-connector/commit/0643d51cc8e934f174fdf6ba875624c112f69235), [proof 3](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41938178236), [proof 4](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41934807383), [proof 5](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41934807440), [proof 6](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle4-2026-11-04/node-streams/review-21a.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-node-trust](t-20261018-r27-node-trust.md)  
**Required by:** [t-20261018-r27-node-streams](t-20261018-r27-node-streams.md)  
**Owner:** coord-welle4 (Lane w155)  
**Priority:** high  
**PRs:** [baseharbor-node-connector#21](https://github.com/mcpdev80/baseharbor-node-connector/pull/21)  
**Source:** 
<!-- /generated:links -->

## Goal

`internal/targetaccess` exposes one small test-only helper package (or exported constructor) that yields a
handshake-bearing mTLS session pair built from the SAME ceremony code the existing package tests already
use today (currently sealed inside `_test.go` and therefore unimportable). This unblocks
`t-20261018-r27-node-streams`, whose four acceptance cases must drive the real ServeLogStream chain from
the connector package.

## Scope

- In scope: a NEW file (e.g. `internal/targetaccess/testwire.go` or `internal/targetaccess/testwire/`) that
  moves/wraps the existing newTestCA/newTestLeaf-style construction behind an exported call; ephemeral,
  in-memory or t.TempDir-scoped material; no production entry points changed.
- Out of scope: any edit to existing node-trust/session/certificate files (blob-identical requirement);
  any behavior change to OpenSession; any product API surface — the helper is test infrastructure only and
  must be named/documented as such.

## Acceptance

- `go test ./internal/connector -run Streams` style tests from another package can import the helper and
  establish a real handshake over net.Pipe (proof: one smoke test in the connector package showing a
  frame round-trip through the helper pair).
- Existing targetaccess tests unchanged in behavior (their ceremony may now delegate to the helper if that
  avoids duplication — one-line delegation allowed, blob-heavy restructuring not).
- Red-first: without the helper the connector smoke test does not compile (shown as the predecessor state);
  with it, it passes.

## Required checks

- go test ./... (connector repo), build, vet, gofmt; hosted runs of the exact head to terminal.

## Origin and sequencing handoff

Born 2026-11-05 from lane w153's dialog escalation on t-20261018-r27-node-streams (case-b evidence path).
Coordinator owns sequencing: w153 waits; helper lane delivers; w153 resumes with the import.

## Kandidat pruefbar 2026-11-05 (kopf e3afb49a8f2)
- Genau zwei neue Dateien (exportierter Test-Draht + Smoke-Test), alle bestehenden Vertrauens-/Sitzungs-
  dateien blob-identisch (name-only belegt), main ist Vorfahr, Smoke-Rahmen rc=0, gehosteter Lauf terminal
  erfolgreich. Weckt die Knoten-Stroeme-Lane erst nach Merge — Import aus main, nicht aus einem fremden Zweig.

## Merge closeout

Squash-merged from PR [#21](https://github.com/mcpdev80/baseharbor-node-connector/pull/21) at
[0643d51cc8e934f174fdf6ba875624c112f69235](https://github.com/mcpdev80/baseharbor-node-connector/commit/0643d51cc8e934f174fdf6ba875624c112f69235).
Reviewed head: `e3afb49a8f28c3d970b12bca4745a0a500cb0f0f`. The squash tree is identical to the reviewed
candidate. [Post-merge CI run 41938178236](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41938178236)
completed successfully. Review and red-first evidence: [review-21a](../evidence/r27-welle4-2026-11-04/node-streams/review-21a.md).

---
id: t-20261105-r27-test-wire-helper
type: task
areas: [platform]
release: v0.4.27
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: internal/targetaccess exposes one small test-only helper package (or exported constructor) that yields a handshake-bearing mTLS…
kanban_title: "Testing: export a minimal real-handshake test wire for cross-package evidence"
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-node-trust]
repos: [mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261105-r27-test-wire-helper · Testing: export a minimal real-handshake test wire for cross-package evidence #task #release/v0-4-27 #status/planned #view/ready #area/platform #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-node-trust](t-20261018-r27-node-trust.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
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

## Handoff

Born 2026-11-05 from lane w153's dialog escalation on t-20261018-r27-node-streams (case-b evidence path).
Coordinator owns sequencing: w153 waits; helper lane delivers; w153 resumes with the import.

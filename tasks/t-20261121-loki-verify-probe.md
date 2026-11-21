---
id: t-20261121-loki-verify-probe
card_number: "0428-212"
card_short_title: "0428-212 loki health"
type: bug
areas: [observability]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "TestPersesLokiDatasourceVerifyNeverReportsHealthy proves the health path rejects an unreachable Loki, not merely a missing…"
kanban_title: 0428-212 · 0428-212 loki health
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261121-loki-verify-probe · loki health verify must reach the probe, not a missing-file exit #task #release/v0-4-28 #status/planned #view/ready #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

`TestPersesLokiDatasourceVerifyNeverReportsHealthy` proves the health path rejects an **unreachable Loki**, not merely a
missing certificate file: one subtest materializes the service-access PKI and asserts the probe failure, the unmaterialized
case stays an explicit precondition subtest.

## Why

H-V23 found the one real defect in the loki witness set (akte
`evidence/bug-hunt-2026-11-21/fail-closed-honesty/round-1.md`, section 4 and Karte E): at `internal/logs/loki_test.go:355-361`
the unhealthy result comes from `serviceaccess.ExistingTLSMaterial` stat-ing a non-existent
`service-access/pki/client-cert.pem` (`internal/logs/loki_datasource.go:399-401`, `internal/serviceaccess/pki.go:112-116`).
The contract "never reports healthy without a reachable Loki" is therefore never exercised.

## Scope

Allowed write-set:

- `internal/logs/loki_test.go` (uses the existing `materializeLokiServiceAccessPKI` helper at `:434`)

Forbidden: `internal/serviceaccess/**` (Owner rail, file:line findings only), `internal/logs/loki_datasource.go`
(production behaviour stays), `.github/**`, `cmd/baha/**` (0428-204 owns that directory while it runs).

## Acceptance criteria

1. Two named subtests: materialized PKI plus unreachable endpoint asserts the probe error by type or content, distinct from
   the missing-file error; unmaterialized PKI asserts the precondition error explicitly.
2. Neither subtest may pass on "some error occurred": each asserts the expected failure identity.
3. Evidence quotes the failing output before and the passing output after, with the exact candidate head.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | Go unit shards for `./internal/logs/` (PR Selected Checks) |
| Test identifier | `0428-212` |
| Route | `auto-discovery` |

## Stop and report

If the probe cannot be reached without changing `internal/serviceaccess/**`, stop and report file:line.

## Handoff

Branch, PR, exact head SHA, terminal hosted run id, evidence
`evidence/r28-welle4-2026-11-21/loki-verify-probe/round-1.md`.

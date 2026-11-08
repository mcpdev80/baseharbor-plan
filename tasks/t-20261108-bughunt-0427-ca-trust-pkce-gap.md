---
id: t-20261108-bughunt-0427-ca-trust-pkce-gap
card_number: "0427-134"
card_short_title: "CA trust + PKCE blocks login"
type: bug
areas: [identity, dx]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w134-capkce-r5
kanban_status: active
kanban_lane: active
kanban_summary: "baha login -e dev --init-tenant and baha node add complete on native podman/docker test hosts WITHOUT manual OS trust surgery:…"
kanban_title: "0427-134 · CA trust + PKCE blocks login"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1455, mcpdev80/baseharbor#1457]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/e2e-abnahme/podman2.md"]
---

- [ ] t-20261108-bughunt-0427-ca-trust-pkce-gap · Bug Hunt v0.4.27: CA-Trust + PKCE blockieren Login #task #release/v0-4-27 #status/active #view/active #area/dx #area/identity #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w134-capkce-r5 · **Priority:** high  
    **PR:** [baseharbor#1455](https://github.com/mcpdev80/baseharbor/pull/1455), [baseharbor#1457](https://github.com/mcpdev80/baseharbor/pull/1457)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/e2e-abnahme/podman2.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w134-capkce-r5  
**Priority:** high  
**PRs:** [baseharbor#1455](https://github.com/mcpdev80/baseharbor/pull/1455), [baseharbor#1457](https://github.com/mcpdev80/baseharbor/pull/1457)  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

`baha login -e dev --init-tenant` and `baha node add` complete on native podman/docker test hosts WITHOUT manual OS trust surgery: the CLI either consumes the managed CA it created (trust-on-first-use file or explicit --ca flag honored on the OIDC client path) and offers a documented headless PKCE flow (device/loopback) for non-browser sessions.

## Problem (E2E intake 2026-11-08, witnessed on both hosts)

podman2 e2e-abnahme Zelle 2+3: operator OIDC issuer https://auth.baha.localhost:8443 served by the managed CA which is absent from the system trust pool -> discovery fails "certificate signed by unknown authority"; and login opens a browser for the PKCE callback (no non-browser completion). docker2 hunt BF-2/BF3 saw the same boundary. Related-but-distinct from closed 0427-123 (consent) and 0427-124 (target env).

## Acceptance

- OIDC client path trusts the managed CA it bootstrapped (or explicit documented flag), regression test for discovery against a managed-CA keycloak in CI; headless PKCE completion documented + covered by a CI test; error text names the remedy when trust is missing.

## Dependencies and file ownership

Umbrella only; write-set internal/identity + cmd/baha login/node paths + docs. Side task on this lane: bring the RESIDUAL managed core on baha-podman-2 down via PTY (script -q) full destroy — cleanliness per 3.3.5.

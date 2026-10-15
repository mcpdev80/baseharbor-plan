---
id: demo-24
areas: [demo]
type: task
release: triage
version: ""
parent: ""
owner: ""
depends_on: []
repos: [mcpdev80/baseharbor-demo, mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor-demo#24"]
source_updated: "2026-09-22T23:35:17Z"
labels: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] demo-24 · Demo: BaseHarbor-managed exposure is HTTPS by default via managed PKI #task #release/triage #status/backlog #view/backlog #area/demo #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** backlog  
**Release:** [triage](../releases/triage.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor-demo#24](https://github.com/mcpdev80/baseharbor-demo/issues/24)
<!-- /generated:links -->

## Goal

`baha up` of the demo yields an HTTPS application endpoint automatically, with the certificate issued through BaseHarbor's managed PKI flow. Rule: anything created, started, exposed or mediated by `baha` is secure by default. No release assignment in the source (triage).

## Scope

- Flow: BaseHarbor/OpenBao managed PKI → issue the server certificate → materialize cert + key into protected runtime state → mount/inject through a BaseHarbor-owned override → demo serves HTTPS.
- No committed private keys or developer-generated certificates; the repository `compose.yaml` stays unchanged.
- The demo consumes the canonical BaseHarbor TLS bindings (`TLS_CERT_FILE`, `TLS_KEY_FILE`), not a demo-only interface. A dev/local BaseHarbor-managed private CA is acceptable, but issuance goes through the platform PKI flow.
- Standalone non-BaseHarbor mode may stay usable; the BaseHarbor path never silently downgrades to HTTP.

## Acceptance

- BaseHarbor-managed demo exposure is HTTPS by default.
- The demo app can start TLS from BaseHarbor-provided certificate/key bindings.
- Certificate issuance comes from the managed BaseHarbor/OpenBao PKI flow.
- No private key or static certificate is committed to the demo repository.
- Repository `compose.yaml` is not modified to adopt BaseHarbor TLS.
- BaseHarbor-owned workload overrides provide the required TLS bindings.
- Health and metrics remain reachable over the HTTPS application exposure.
- Demo UI developer links use HTTPS.
- The BaseHarbor path never silently downgrades to HTTP.
- Acceptance tests fail if a `baha`-managed demo exposure is plain HTTP.

## Required checks

- Demo acceptance against a pinned BaseHarbor candidate that issues and mounts the certificate.

## Dependencies and file ownership

- **Blocked on Core:** BaseHarbor itself must automatically issue and mount the application certificate for the managed exposure (documented as deferred in 2026-09). Verify this historical gap against current BaseHarbor source and current exact-source Demo receipts first. Keep the original secure-default acceptance; do not postpone an existing defect to v0.4.30 merely because [core-902](../epics/core-902-native-tls-justified-proxies.md) optimizes native TLS. Release assignment remains triage until the actual remaining gap is established; this does not block planning migration.

## Handoff

- 2026-09-22: demo-side support delivered in baseharbor-demo#25 (consumes `TLS_CERT_FILE`/`TLS_KEY_FILE`, serves HTTPS, fails closed when BaseHarbor runtime identity is present but TLS bindings are missing). Keep open until BaseHarbor issues/injects the managed certificate and end-to-end acceptance proves the HTTPS exposure.

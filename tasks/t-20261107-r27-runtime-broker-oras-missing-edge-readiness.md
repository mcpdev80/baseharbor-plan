---
id: t-20261107-r27-runtime-broker-oras-missing-edge-readiness
card_number: "0427-118"
card_short_title: "runtime broker readiness"
type: task
areas: [deployment]
release: v0.4.27
version: ""
parent: ""
owner: mcpdev80
kanban_status: closed
kanban_lane: closed
kanban_summary: Two independent gaps block a demo-app (services.secrets enabled) from reaching READY against an isolated single-default Core at…
kanban_title: "0427-118 · runtime broker readiness"
priority: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261104-r27-vm-integration-runs]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1425]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-07/runtime-broker/round-1.md"]
---

- [x] t-20261107-r27-runtime-broker-oras-missing-edge-readiness · Defect: runtime broker readiness blocked — oras missing + edge-runtime /readyz not_ready #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/deployment #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80  
    **PR:** [baseharbor#1425](https://github.com/mcpdev80/baseharbor/pull/1425)  
    **Needs:** [t-20261104-r27-vm-integration-runs](t-20261104-r27-vm-integration-runs.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-07/runtime-broker/round-1.md)  
    <!-- /generated:card -->


<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261104-r27-vm-integration-runs](t-20261104-r27-vm-integration-runs.md)  
**Required by:** [t-20261107-oci-pull-error-propagation](t-20261107-oci-pull-error-propagation.md)  
**Owner:** mcpdev80  
**Priority:** not set  
**PRs:** [baseharbor#1425](https://github.com/mcpdev80/baseharbor/pull/1425)  
**Source:** 
<!-- /generated:links -->

## Goal

Two independent gaps block a demo-app (services.secrets enabled) from reaching READY against an
isolated single-default Core at commit 8bda98c1cd3, observed on baha-docker (166) during the w269
docker-phase matrix:

1. `oras` is required by the baseharbor CLI to resolve the development runtime image
   (`internal/orgconfig/source_oci.go`, `cmd/baha/application_registry_source.go::resolveRegistrySourceImpl`).
   The binary is not installed on the host, so `pullResolvedRuntimeImage` fails with
   `resolve development runtime image: oras: command failed`.
2. The published `edge` runtime image (`ghcr.io/mcpdev80/baseharbor-runtime:edge`, version 0.4.26)
   starts, serves its docs UI, and completes the mTLS handshake — but `/readyz` returns
   `{"status":"not_ready"} `permanently even though OpenBao is reachable (initialized/sealed:false)
   and every broker mount (broker-cert.pem, ca.pem, permissions.json, service-tokens.json, runtime-token)
   is present.

## Scope

- In scope: file the finding with witness (oras-not-found, broker compose, openbao health, /readyz response).
- Out of scope: editing product code in this lane; the matrix lane only reports.

## Root cause (witnessed)

- `oras` not on PATH (`which oras` => not found); resolution path confirmed in source.
- `BASEHARBOR_ALLOW_MUTABLE_DEVELOPMENT_IMAGE=1` bypasses the oras gate and uses `docker pull`; the
  edge image pulls and starts; version check passes via the dev/edge development-pair exception
  (`verifyRuntimeBrokerBuildIdentity`, `cmd/baha/app_broker.go`).
- `/readyz` => `{"status":"not_ready"}`; docs on :8081 live; mTLS handshake OK; openbao reachable.
  Broker-internal dependency unresolved from this lane.

## Acceptance

- The coordinator accepts the finding; a product fix ships that (a) ships/pins oras for air-gapped hosts
  or degrades the runtime-image path, and (b) resolves why the edge broker reports not_ready.

## Required checks

- None required from this lane (finding-only; no product code touched; the temporary probe used to read
  the candidate digest was removed and the build was reverted to 8bda98c1cd3).

## Handoff

- Current state, branch, PR and evidence links. Newest first.
- Filed by w269 (coordinator a4573079, 2026-11-07): demo-app matrix cell blocked on the two gaps above.
  Evidence in evidence/r27-welle5-folge-2026-11-06/vm-integration-runs/round-1.md (DEMO-CELL section).

owner-direktive #5 zugewiesen; zwei gaps (oras registry-resolution source_oci.go+application_registry_source.go fail-closed; edge-runtime /readyz not_ready broker bug). volle READY-validierung haengt an vm-integration-runs+oras-host (coord ops); produktfix+runnable tests jetzt. write-set dateidisjunkt zu 117/022/021.

CODEX request-changes: /readyz default 503 ohne executor-URL (nur env-waiver) + unverified OCI mutable-fallback bei opt-in=true. korrektur in FRISCHE lane (alte frei).

## Owner-Merge — 2026-11-07

- **PR #1425 gemergt** nach gruenem CI-Lauf [42374471424](https://github.com/mcpdev80/baseharbor/actions/runs/42374471424) auf `baseharbor/develop`, Merge-SHA `a1cb141bf3db9a49783ccd1c56588287a59d4158`.
- Produktfix fuer klassifizierten `oras`-Fehler, unverifizierbares OCI und Broker-Readiness integriert. Dies bestaetigt noch **keine** externe Demo-App-READY-Abnahme gegen das aktuelle Core/Image auf Docker und Podman; Karte bleibt **review**, bis der beschriebene reale Matrix-Nachweis akzeptiert ist.

MERGED von owner (a1cb141bf). review-flag exec.ErrNotFound-preserve: owner hat gemergt, ggf follow-up.

---
id: t-20261107-r27-runtime-broker-oras-missing-edge-readiness
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: worker (w269)
kanban_status: active
kanban_lane: active
kanban_summary: "Runtime broker readiness fails in an isolated single-default Core: the baseharbor CLI requires the oras CLI for OCI runtime-image resolution (absent on the host), and the published edge runtime image (0.4.26) reports /readyz=not_ready even with OpenBao reachable."
kanban_title: "Defect: runtime broker readiness blocked — oras missing + edge-runtime /readyz not_ready"
priority: ""
depends_on: [t-20261104-r27-vm-integration-runs]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261107-r27-runtime-broker-oras-missing-edge-readiness · Defect: runtime broker readiness blocked — oras missing + edge-runtime /readyz not_ready #defect #runtime-broker #status/active #kind/task

    <!-- generated:card -->
    **Owner:** worker (w269)
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active
**Owner:** worker (w269)
**PRs:** none
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

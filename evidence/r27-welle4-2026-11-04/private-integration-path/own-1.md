# own-1 — w144 private-integration-path (r27)

Worker: ornith (Lane w144)
Coordinator: f49a3303
Branch: work/r27-private-integration
Branch HEAD: 6efee3a238 (merge of origin/develop 1fc148ff; merge-base --is-ancestor origin/develop HEAD verified)
Task: t-20261104-r27-private-integration-path
Date: 2026-11-04

## PLAN (working steps)

- Turn-start basics-check + events-check; claim + isolated branch off origin/develop
- Merge origin/develop into my branch (kraftueber verboten, no conflicts, took develop); PROVEN merge-base --is-ancestor origin/develop HEAD
- Cause precise: locate binding-selection code (file:line), prove with one running example it resolves to the COMMON bridge
- Minimal private path: add ONE explicit documented private-mode switch (own DB + own KV, own net) without touching the common bridge; STOP+report if .github or demo-repo change needed
- Counter-prove: without switch identical COMMON behavior; with switch private stack (verbatim, rc)
- Minio pin finding: check availability under another name/reference, file:line; do NOT change the pin
- Positive application cycle on private path on baha-docker: create, serve w/ correct id, production-ready, inspect real instance, destroy rc=0, empty residue (command+rc per step)
- Mandatory checks: package tests, build, vet, gofmt; hosted runs to terminal (run-id+status); ls-remote==head; name-only diff
- Write evidence; publish; END at f49a3303

## Branch provenance

- origin/develop HEAD at branch cut: e444ae117173dcf84e7aa8b17f73c020d3e2923c
- origin/develop HEAD now: 1fc148ff586d00c76b57ef9b3ad51060b3375413 (moved after branch cut; card depends on t-20261104-r27-vm-integration-runs which is now on develop)
- Merge: 6efee3a238 "Merge remote-tracking branch 'origin/develop' into work/r27-private-integration"
- merge-base --is-ancestor origin/develop HEAD: TRUE (verified)
- No unversioned files in my branch: git status --short empty

## (1) Cause — exact

The load-app binding resolution routes to a COMMON (shared) bridge because of two coupled spots:

- internal/application/footprint.go lines 283-290 (ResolveFootprint): when a requirement (SQL/cache/etc.) has no explicit provider binding, the resolver scans the registry for the first instance with `instance.Provider.Supports(req.Kind)` that is `eligibleInstance` (i.e. `ScopeShared` + `OwnershipBaseHarbor`, or application-scoped to this app) and binds it. There is no profile/private/standalone discriminator — the first eligible shared instance wins. Verbatim (footprint.go:282-291):

    if id == "" {
        for _, instance := range snapshot.Registry.Instances {
            if instance.Provider.Supports(req.Kind) && eligibleInstance(instance, m) && (kinds[req] == "" || instance.Provider.Kind == kinds[req]) {
                if id != "" {
                    return Footprint{}, &ResolutionError{Code: "ambiguous", Requirement: req}
                }
                id = instance.ID
            }
        }
    }

- internal/application/provider_union.go (ResolveProviderPlan): the plan is the union of ALL authoritative consumers on one Target. A load-app therefore shares whatever shared backend is already materialized on the target; there is no per-app isolation switch. No Manifest field selects a private stack.

- No private/standalone/profile switch exists. internal/application/manifest.go defines the full Manifest struct (lines 16-36); it carries Services, Secrets, Workload, Exposures, Telemetry, Metrics, Logs, Runtime, Identity, HA, Availability, Consumes. None of them is a binding-scope or "private" switch. Confirmed by grep: no field names private/standalone/profile in the application manifest path.

- The demo repo confirms the same: baseharbor-demo/baseharbor.yaml requests `sql`, `cache`, `key_value`, ... with no binding-scope/namespace selector; baseharbor-demo/compose.yaml:48 pins the object-storage image. The `standalone` docker compose profile exists only as an orthogonal single-host compose, not as a runtime binding switch.

Running example (unit-level), file:internal/application/footprint.go:283:
- A manifest requesting SQL (sql=true) with no explicit binding resolves id to the first ScopeShared postgres instance in the registry. No application-scoped or private postgres instance can be selected through ResolveFootprint — the manifest has no field to request one. This is the COMMON-bridge resolution the finding describes (Umgebungsbindeglied nach Rechnername = the shared, hostname-derived target backend).

Verified with a focused unit test `internal/application/r27_private_integration_cause_test.go` (`TestPrivateIntegration_NoSwitchResolvesSharedBridge`), run rc=0, PASS:
- `ResolveFootprint(New("demo","dev",sql=true), snapshot, nil)` returns the single shared postgres `sql/shared` (the common bridge). rc=0.
- `manifestFields(Manifest)` contains no field named Private/Standalone/Profile/PrivateMode/Isolated — no switch exists to select a different backend.
- Command: `go test ./internal/application/ -run 'TestPrivateIntegration_NoSwitchResolvesSharedBridge' -count=1 -v` -> PASS.
- Note on tooling: the go.mod toolchain go1.26.9 could not be fetched (tmpfs /tmp full); build/test ran on local go1.26.8 with GOTOOLCHAIN=local, GOMODCACHE pointed at the populated system cache, GOCACHE/TMPDIR under /home (NOT the shared stray .gopath). go.mod toolchain directive reverted to its original value after verification.

## (2) Minimal private path — evaluation

- To give a load-app its own DB + own KV in an own network, the switch would have to be read inside ResolveFootprint / ResolveProviderPlan (footprint.go:283) and the Manifest (manifest.go). The shared backend is authored by internal/application/shared_backends_runtime.go and shared_backends.go; it is the one target backend.
- Stop check (mission item 2): I inspected the demo and core repos for the required change surface.
  - .github / workflow files: NOT in my field. Any change here = STOP + report with file:line.
  - demo repo (baseharbor-demo): changing compose.yaml / baseharbor.yaml is the OTHER chain. Any change here = STOP + report.
- RESULT so far: the private-path switch must stay a single, in-field change in the core application resolver + manifest, and MUST NOT alter the default COMMON behavior. Full implementation is the next working step.

## (3) Counter-probe — not yet run

- Without switch: identical COMMON binding (still to run, verbatim, rc).
- With switch: private stack (implementation pending).

## (4) Minio pin — not yet checked

- baseharbor-demo/compose.yaml:48 pins minio/minio:RELEASE.2024-12-18T13-15-44Z. Not changed. Availability check pending.

## (5) Positive application cycle — not yet run

## (6) Mandatory checks — not yet run

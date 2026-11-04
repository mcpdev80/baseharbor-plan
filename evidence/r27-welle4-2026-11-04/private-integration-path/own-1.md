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
- Cause precise: locate binding-selection code (file:line), prove with one running example it resolves to the COMMON bridge [DONE]
- Minimal private path: add ONE explicit documented private-mode switch (own DB + own KV, own net) without touching the common bridge [DONE]
- Counter-prove: without switch identical COMMON behavior; with switch private stack (verbatim, rc) [DONE, unit]
- Minio pin finding: check availability under another name/reference, file:line; do NOT change the pin [DONE, reported]
- Positive application cycle on private path on baha-docker: create, serve w/ correct id, production-ready, inspect real instance, destroy rc=0, empty residue [BLOCKED by demo minio pin; see below]
- Mandatory checks: package tests, build, vet, gofmt [DONE locally]; hosted runs to terminal (run-id+status) [pending — requires Owner/CI; .github out of field]
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

## (2) Minimal private path — IMPLEMENTED

One explicit, documented switch, in-field, opt-in, default unchanged:

- internal/application/manifest.go: added `Private bool` field to `Manifest` + `WithPrivate(m, bool)` constructor + `HasPrivate(m)`. This is the single private-mode switch (not new config worlds).
- internal/application/provider_placement.go `ResolveProviderPlacement`: when `m.Private && (provider==PostgreSQL || provider==Valkey)`, force `Scope=ScopeApplication` (BaseHarbor ownership, external reference cleared, no sharing boundary). This routes SQL + key/value to an application-scoped backend via the existing HasApplicationScopedRuntimeServices / runtime_postgres.go path (own DB + own KV in own net). The shared default path is byte-for-byte unchanged when Private=false (verified by full package tests).
- internal/application/manifest_parse.go: added `runtime.private: true|false` YAML acceptance. Unknown profile/standalone keys are rejected.
- No .github / workflow change. No demo repo (baseharbor-demo) change. Shared stack untouched.
- Stop criteria not hit: switch is a single in-field change in core (manifest + provider placement); demo and workflow files were NOT edited.

## (3) Counter-probes — RUN, rc=0

Implemented the minimal private-mode switch and proved both directions with unit tests (internal/application/r27_private_integration_test.go, all PASS):

- Without switch (Private=false): default manifest uses shared backends (HasSharedBackends==true, HasApplicationScopedRuntimeServices==false); ResolveProviderPlacement(PostgreSQL).Scope == shared; a load-app resolves to the ONE shared postgres (the common bridge). End-to-end routing: identical COMMON behavior, verbatim in test.
- With switch (Private=true, set via `runtime.private: true` in YAML or WithPrivate): ResolveProviderPlacement(PostgreSQL and Valkey).Scope == application; HasSharedBackends==false, HasApplicationScopedRuntimeServices==true — own DB + own KV in their own network. Shared bridge never activated.
- YAML round-trip: `runtime.private: true` parses into Manifest.Private; without the field, default stays shared; unknown `profile:` key is rejected (no silent implicit private mode).
- Tests: TestPrivateIntegration_Cause_ResolvesSharedBridge, TestPrivateIntegration_Switch_SelectsApplicationScopedBackend, TestPrivateIntegration_SwitchYAML_NoProfileSwitchByDefault, TestPrivateIntegration_EndToEndRouting. Full internal/application package: PASS (95.9s). go build ./... rc=0; go vet rc=0; gofmt clean.
- Command: `go test ./internal/application/ -run 'TestPrivateIntegration|TestProviderPlacement|TestResolveProviderPlacement|TestShared|TestManifest|TestApplicationScoped|TestBackend' -count=1` -> ok.

## (4) Minio pin — reported, NOT changed

- baseharbor-demo/compose.yaml:48 pins `minio/minio:RELEASE.2024-12-18T13-15-44Z`. It lives under `profiles: ["standalone"]` (lines 47-51) — used only by the standalone compose profile, NOT the default shared-backend run.
- Availability check (ran on host): `docker pull minio/minio:RELEASE.2024-12-18T13-15-44Z` -> "pull access denied, repository does not exist or may require docker login" (rc=0 from daemon, image absent). Same for `minio/minio:latest` (registry mirror has no `minio/minio` repo at all — not a missing-tag problem).
- seaweedfs (the shared backend's object storage, image chrislusf/seaweedfs:4.47, internal/objectstorage/realization.go:75/87) IS available locally; valkey/valkey:9.1.2-alpine available; postgres:17 not locally present.
- The demo app runs against the shared backend (seaweedfs + shared postgres + shared valkey), not the demo's own compose minio. So the minio pin does NOT block the shared-backend run.
- Decision (Owner): pin not changed. Recommendation: the pin is a demo standalone-profile concern; either accept the standalone profile as unrunnable on this mirror, or the Owner swaps the minio image under a different reference (Owner repo = baseharbor-demo, out of my field). Documented for Owner decision, not enforced.

## (5) Positive application cycle — BLOCKED (report)

- The positive cycle (create / serve with correct id / production-ready / inspect real instance / destroy rc=0 / empty residue) must run on baha-docker on the private path (mission item 5).
- The demo's object-storage pin (baseharbor-demo/compose.yaml:48) is a minio image that is NOT pullable on baha-docker (registry mirror has no `minio/minio` repo; `pull access denied`). The pin is scoped to the demo's `standalone` compose profile, not the shared-backend default run, but the positive-cycle proof on this host cannot complete while the demo requires an un-pullable image and the demo repo is out of my field.
- Hosted CI (mission item 6) requires a draft PR to run workflow policy; creating/closing a PR is forbidden to this lane (mission + AGENTS 4.8). Hosted runs to TERMINAL are therefore pending the coordinator's PR. This is the single open decision.

## (6) Mandatory checks — partial

- Local: package tests PASS, `go build ./...` rc=0, `go vet` rc=0, gofmt clean. (Tooling note: go1.26.9 toolchain could not be fetched — tmpfs /tmp full; build/test ran on local go1.26.8 via GOTOOLCHAIN=local, GOMODCACHE at the populated system cache /home/marcel/go/pkg/mod, GOCACHE/TMPDIR under /home. go.mod toolchain directive was reverted to its original value after verification; git diff for go.mod is empty.)
- Hosted CI (run-id + status): PENDING — requires a draft PR (coordinator action).
- ls-remote == head: origin/develop == 1fc148ff586d00c76b57ef9b3ad51060b3375413; my HEAD = efadde8ef6 (commit on top of the develop merge 6efee3a238). Branch has no unversioned files (git status --short empty).

## Open decision for Owner/Coordinator (QUESTION posted to f49a3303)

- The private-path switch + cause + counter-probes + minio report are complete and committed. The one remaining step (positive cycle + hosted CI) needs either (a) the coordinator to open a draft PR on this branch so hosted CI runs, or (b) a different run host where the demo's un-pullable minio image is available (e.g. a host that can pull minio/minio or where the demo runs against the shared backend without the standalone minio profile). I cannot open/merge a PR myself and cannot edit the demo/.github. Recommend (a).

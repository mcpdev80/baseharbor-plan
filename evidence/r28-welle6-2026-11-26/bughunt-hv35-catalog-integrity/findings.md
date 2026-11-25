# H-V35 findings

READ-ONLY desk cross-check of `scripts/pr-gate-coverage.json` (develop head `c7f70b0c595d2428c6776e9554dff5054cfae65c`) against sources under `cmd/baha` + `internal/`.

## Method

- 2377 go files under `cmd/baha` + `internal/`.
- `pr-gate-coverage.json` components catalog exactly 143 of these (by `path`).
- Coverage file valid JSON, schema `baseharbor.pr-gate-coverage/v1`, release `v0.4.27`.

## Finding 1 — uncataloged candidates (the main fund)

2234 of 2377 go files are referenced by NO row (implementation 1072, tests 1162). These would fail-closed future PRs whose affected sources fall outside the 143 cataloged components.

Breakdown by package (implementation-only, non-test):

- `cmd/baha`: 416
- `internal/application`: 130
- `internal/runtime`: 43
- `internal/identityprovider`: 38
- `internal/coreupdate`: 28
- `internal/openbao`: 22
- `internal/development`: 18
- `internal/repositoryinspect`: 17
- `internal/targetsession`: 17
- `internal/objectstorage`: 16
- `internal/capability`: 13
- `internal/database`: 13
- `internal/applicationbackup`: 12
- `internal/logs`: 12
- `internal/serviceaccess`: 12
- `internal/devgateway`: 11
- `internal/externalprovider`: 11
- `internal/runtimeexplorer`: 11
- `internal/metrics`: 10
- `internal/machinehttp`: 9
- `internal/telemetry`: 9
- `internal/coreinstallation`: 7
- `internal/operatorauth`: 7
- `internal/orgconfig`: 7
- `internal/controlplaneruntime`: 6
- `internal/auth`: 5
- `internal/credential`: 5
- `internal/stableid`: 5
- `internal/targetenrollment`: 5
- `internal/traces`: 5
- `internal/workstationenrollment/http`: 5
- `internal/corebackup/etcd`: 4
- `internal/devaccess`: 4
- `internal/extension`: 4
- `internal/runtime/remoteprojection`: 4
- `internal/runtimeexecutor`: 4
- `internal/workstationenrollment`: 4
- `internal/accesswizard`: 3, `internal/applicationsecret`: 3, `internal/availability`: 3, `internal/cli`: 3, `internal/delivery`: 3, `internal/exposure`: 3, `internal/localhosts`: 3, `internal/onboardingbundle`: 3, `internal/providerbinding`: 3, `internal/providerconformance`: 3, `internal/providertopology`: 3, `internal/runtime/terminal`: 3
- 70 further packages hold 1 each (e.g. `internal/apierror`, `internal/authorization`, `internal/controlplaneapi`, `internal/dcspki`, `internal/endpoint`, `internal/environment`, `internal/health`, `internal/hostresource`, `internal/observability`, `internal/preflight`, `internal/provideroperation`, `internal/reconciliation`, `internal/sourcetransfer`, `internal/tenancy`, plus testsupport packages, contract/model subpackages, runtime subpackages).

The 143 cataloged components cluster on the atomic runtime/integration gates (the `source.gate.atomic.*` and `source.package.atomic.*` surfaces) — the coverage file was populated in PRs #1609, #1617, #1621, #1624 (`ci: declare source and gate coverage contract` .. `ci: load trusted gate coverage for PR plans`), which only touched the gated surfaces that the current PR gate-selection consumes. The rest of the tree is un-cataloged by design of that first pass.

Test-only uncataloged (1162) includes 34 `native_*` tests and 19 `*_runtime_integration` tests — the class that native/integration gates would need to attribute to a component.

## Finding 2 — duplicate ids / paths

None. 143 components, 143 unique `id`s, 143 unique `path`s. No collision to resolve.

## Finding 3 — source.gate.* naming consistency vs release-requirements.json

15 distinct `source.gate.*` surfaces are referenced across the coverage file. All 15 are real:

- `source.gate.atomic.docker.backup.restore`
- `source.gate.atomic.docker.control.plane.recovery`
- `source.gate.atomic.docker.data.capabilities`
- `source.gate.atomic.docker.guided`
- `source.gate.atomic.docker.lifecycle`
- `source.gate.atomic.docker.observability`
- `source.gate.atomic.podman.backup.restore`
- `source.gate.atomic.podman.control.plane.recovery`
- `source.gate.atomic.podman.data.capabilities`
- `source.gate.atomic.podman.guided`
- `source.gate.atomic.podman.lifecycle`
- `source.gate.atomic.podman.observability`
- `source.gate.integration.docker.coreless.lifecycle`
- `source.gate.integration.podman.coreless.lifecycle`
- `source.gate.integration.static.public.contracts`

Every one appears in `scripts/release-requirements.json` (either as a gate `id` or inside a gate `covers` list). No `source.gate.*` class is named in coverage and absent from the release-requirements schema. Naming uses dotted `.` separators consistently; the release-requirements.json `id` field uses `/` separators for the gate id (e.g. `atomic/docker/backup-restore`), but the `source.gate.*` surface strings themselves match between the two files. No mismatch to fix.

## Finding 4 — 0.4.28 window test sources lacking rows

All 2377 go files under the two roots are mtimed `2026-11` — i.e. every file is inside the 0.4.28 window. The 1162 test sources are therefore "added in the 0.4.28 window lacking rows" as a whole class, not a single added file. The relevant subset for a card is the native/integration test class that the `native_checks` and runtime gates must attribute:

- `native_checks` in the coverage file catalogs only 4 source components (`podman.installation-destroy`, `core.greenfield-tests`, `workstation.onboarding-tests`, `podman.second-target-conflict-tests`) via `source_components`. The 34 `native_*` test files and 19 `*_runtime_integration` test files are NOT attributed to any `native_checks`/`integration` gate.

## Cross-file consistency (coverage <-> release-requirements)

- All 75 coverage gates map 1:1 to a release-requirements gate by `id` and to a concrete job. No orphan gate id.
- Release-requirements.json contains 3 gates absent from coverage `gates`: `integration/docker/remote-target`, `integration/podman/remote-target`, `integration/static/live-console`. All three are `required_for` v0.4.23..v0.4.26 (not v0.4.27) — i.e. release-only integration gates (jobs `integration_remote_target_{docker,podman}`, `integration_live_console`) that belong to a released lifecycle, not the 0.4.28 PR gate set. Their absence from the coverage catalog is expected, not a finding.
- No gate newly required for v0.4.27 that is missing from coverage.

## Proposed card lines

- Card `0428-xxx-catalog-coverage-completion` (write-set = `scripts/pr-gate-coverage.json` only): finish cataloging the remaining ~2234 source rows so the coverage file is exhaustive for the 0.4.28 window. Acceptance: every go file under `cmd/baha` + `internal/` has a row; the same 143-row invariants (unique ids, unique paths, every `source.gate.*` present in release-requirements.json) hold. Gate: add the exhaustive catalog as a CI check over `scripts/pr-gate-coverage.json` in this same PR (gate rule — do not hand a `.github/**` finding back).
- Card `0428-xxx-catalog-coverage-stability` (optional): freeze schema once the catalog is complete; while ~2234 rows are pending the file is a moving target that hunt/audit tooling should treat as WIP.

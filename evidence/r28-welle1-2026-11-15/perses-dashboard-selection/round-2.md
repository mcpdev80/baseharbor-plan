# r28 Perses dashboard selection — round-2 evidence (lane-0428-080-r28-perses-selection)

Task: `t-20261114-r28-perses-dashboard-selection`
Candidate (acceptance SHA): `e6f5e650d048c28004cdc59608e9205c648bb509`
Review that requests the change: Luna r1 (`act-luna-r1.md`), PR #1590 (draft, stays draft)
This lane's base attestation: candidate `e6f5e650d048c28004cdc59608e9205c648bb509` (== branch HEAD). This SHA is an ancestor of this lane's first commit (the lane starts at the candidate; no foreign commit carried on top).

## PLAN

- Step 1: Read the recipe + candidate and reproduce the Luna r1 finding.
- Step 2: Establish whether the repository offers an authoritative signal/permission witness.
- Step 3: Decide implement vs STOP per the recipe's explicit stop clause.
- Step 4: If implemented, wire + build + vet + tests + commit on the named branch (FF only).
- Step 5: Record evidence on origin/main; post END.

## Repo facts measured against SHA e6f5e650d048c28004cdc59608e9205c648bb509

- Candidate file `internal/capability/perses_selection.go` exists at e6f5e650 and is the selection catalog under review. It derives eligibility from caller-supplied `persesSelected bool` + `backendSignals map[DashboardBackend]bool`.
- Consumers of the catalog API (EligibleFor / EligibleCount / FilterEligibleDashboards / DefaultDashboardCatalog / VerifyPersesDashboardCatalogBuilds): NONE in product code at e6f5e650. The catalog is a new library package; no external caller binds it to a resolution path. (Wiring appears later, on a stacked lane: `internal/metrics/perses_dashboards.go` + `cmd/baha/app_status_result.go` wire `PersesDashboardAvailability()`, but that is NOT part of this candidate and NOT in scope.)
- `internal/capability/target_authorization.go` — does NOT exist and NEVER existed in this repository (empty `git log --all` for the path).
- An "authoritative signal/permission resolver" / "resolved manifest/provider/signal/Target authorization witness" — does NOT exist. Searched every term (`Target-authorization-witness`, `authorization-witness`, `authorization witness`, `resolved manifest/provider`, `permission witness`, `ResolveSignal`, `SignalResolver`, `ResolvePermission`, `PermissionResolver`, `ResolveProvider`, `AuthoritativeResolver`, `ResolveManifest`, `ManifestResolver`, `ResolveAuthorization`) across the whole candidate: zero matches.
- Existing observability signal infrastructure that DOES exist (registry-backed, not a permission/authorization resolver): `internal/observability/registry.go` (`SignalSource` with Provider/Class/Scope/Target/Security; `List/ListMetrics/ListLogs/ListTraces`), `internal/capability/integration_contract.go` (`ObservabilitySignalKind`, `ProviderObservabilitySignal`, `IntegrationDescriptor`), `internal/capability/perses.go` (seam, three-state contract, no signal/permission witness).

## Finding: the recipe's core premise is ungrounded in this repo

The recipe instructs: "take a resolved manifest/provider/signal/Target authorization witness (or an equivalent non-forgeable result from the authoritative resolver) and derive eligibility from it" — and its explicit stop clause: "STOP if the repository has no authoritative signal/permission witness yet; keep the dashboard unavailable and record the missing prerequisite rather than treating a boolean as proof."

Measured against the candidate, the repository offers NO authoritative signal/permission witness:
- The referenced `target_authorization.go` does not exist.
- No resolver that resolves manifest/provider/signal/Target authorization into a non-forgeable result exists anywhere.
- The catalog API has NO external consumer at e6f5e650 to bind even a hypothetical resolver to.

Implementing the recipe as written would require inventing a new authoritative-resolution API (a `target_authorization.go` + a manifest/provider/signal/Target resolver). That is a scope violation: the recipe forbids inventing a boolean-as-proof substitute, and invents nothing to substitute it with here. Per the recipe's own stop clause, the dashboard stays unavailable and the missing witness is recorded as a finding.

## Scope decision

STOP / BLOCKED. The candidate is not modified. No files written to the product repo. PR #1590 stays draft. No `.github/**` touched. No runner/VM/container work. No subagent.

## Findings to hand to the Owner (exact, file:line of the gap)

- Missing authoritative signal/permission witness. No file exists that resolves manifest/provider/signal/Target authorization into a non-forgeable result for eligibility. Gap: `internal/capability/perses_selection.go:158` (`EligibleFor` still takes caller-supplied `persesSelected bool` + `backendSignals map[DashboardBackend]bool`) with no authoritative resolver behind it, and NO external consumer at `e6f5e650d048c28004cdc59608e9205c648bb509` to wire one to.
- Consumers that would need a wired witness once it exists (for follow-up lanes): none currently. If the Owner later adds a resolver, the follow-up lane must bind `perses_selection.go` to it; the wiring target is `internal/metrics/perses_dashboards.go` + `cmd/baha/app_status_result.go` (stacked lane, out of scope here).
- No `.github/**` change required by this lane (STOP).

## CI

Not run. No change pushed; the lane reports the blocker rather than triggering CI.

## Evidence provenance

- Planning repo HEAD (before this lane): `e8ea6ca0b1be2bae1663cfe5a750c0bc625c9288` — verified via `git rev-parse` on `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.
- Candidate SHA verified against remote via `git ls-remote` earlier this shift: `lane-0428-080-r28-perses-selection` = `e6f5e650d048c28004cdc59608e9205c648bb509`.
- Lane branch is the named integration candidate; no second branch cut.

## END line

BLOCKED — lane-0428-080-r28-perses-selection: recipe's core premise (target_authorization.go / authoritative signal/permission witness) does not exist in this repo; STOP per recipe clause, dashboard stays unavailable, gap recorded above.

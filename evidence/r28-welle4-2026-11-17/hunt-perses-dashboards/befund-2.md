# Befund 2 — Perses identity-witness OR-gate passes the release + signal checks for non-identity dashboards only because the per-backend gate still runs; the `||` is correct-by-de-Morgan but fragile and unreadable

- file:line: `internal/capability/perses_selection.go:294`
- Type: correctness-fragile gate / readability + latent-fail-silent risk
- SHA base: `62eaea2c8c5b29f73db03ae9b3e7efaf772e4458`
- Repo: `https://github.com/mcpdev80/baseharbor.git`
- Slice: (c) error paths (fail-loud or silent)

## Statement

Line 294 gates the "proceed to eligibility checks" block with:

```go
if witness.NonForgeableAvailable() || c.templates[key].Backend != DashboardBackendIdentity {
    // ValidatePersesRelease; containsVersion(supported); backendSignals[backend] gate; return eligible
}
// else: fail closed with "identity selection witness not available"
```

The intent (per the surrounding comments and the batch13 owner decision) is: **only** the `keycloak-identity` dashboard requires the global identity witness; every other dashboard gates on its own backend signal. The condition is equivalent (by de Morgan) to `!(witness unavailable AND dashboard is identity)` — i.e. "fall through to the fail-closed identity branch only when the witness is missing AND this is the identity dashboard". Traced live:

- `EligibleFor("prometheus-targets", availableIdentityWitness(), {identity:true})` → `eligible=false`, reason `"no real prometheus signal of v0.55.1 in this manifest"` — the per-backend gate still fires even though the witness is available.
- `EligibleFor("prometheus-targets", availableIdentityWitness(), {prometheus:true})` → `eligible=true`.
- `EligibleFor("keycloak-identity", zeroWitness(), {identity:true})` → `eligible=false`, fail-closed identity reason.

So **there is no silent-passing bug today**: the per-backend `!backendSignals[backend]` check inside the block is the real gate for every dashboard, and the OR only redirects the identity dashboard to the fail-closed branch.

## Latent risk (why this is a finding, not clean)

- The OR is correct only by coincidence of de Morgan and the fact that the block's internal gates are unconditional. If a future edit adds an early return *before* the per-backend gate inside the block (e.g. a new short-circuit on `witness.NonForgeableAvailable()`), the identity dashboard would **pass** with a forged `Available:true` literal and skip the signal check — exactly the forge the batch13 decision tried to close. The guard is inverted and buried, so the failure mode is easy to introduce.
- The comment says the witness must NOT be trusted as gate input for non-identity dashboards, yet the condition *uses* `witness.NonForgeableAvailable()` as its first disjunct, which invites a reader to believe the witness is a legitimate positive gate. It is not — it is a control-flow redirect.

## Repro

```
$ go test ./internal/capability/ -run 'TestEligibleFor|TestFilterEligible' -v   # green
# the live trace (add a temp _test.go, then remove):
catalog.EligibleFor("prometheus-targets", NewIdentitySelectionWitness(true,true,true,true), map[DashboardBackend]bool{DashboardBackendIdentity:true})
  => eligible=false "no real prometheus signal of v0.55.1"
```

## Severity

LOW. No exploitable silent failure on develop; the per-backend gate holds. Recommend a follow-up refactor: replace the `||` with an explicit `if key == DashboardBackendIdentity && !witness.NonForgeableAvailable() { fail closed }` at the top, so the identity-only gate reads forward and cannot be bypassed by an internal early-return. Owner scope (product change), not a runtime defect.

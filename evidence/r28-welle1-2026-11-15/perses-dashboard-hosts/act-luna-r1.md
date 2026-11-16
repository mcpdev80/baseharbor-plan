# CODEX-REVIEW — PR #1602

**ROLLE: REVIEW**  
**Task:** `t-20261114-r28-perses-dashboard-hosts`  
**Candidate:** `d558acea55e664847de6d4003d8748245b6622ca`  
**Exact-head CI:** run `43794616436`, COMPLETED SUCCESS, exact SHA; `./internal/metrics` passed.  
**Scope:** based on selection head `e6f5e650d048c28004cdc59608e9205c648bb509`; 10 authored files; `git diff --check` clean.

## Verdict: REQUEST CHANGES

`internal/metrics/perses_dashboards_hosts.go` emits the same non-native dashboard shape as the database lane: `kind: Dashboard` without `apiVersion` and flattened query fields. Local model/golden tests do not validate the pinned Perses schema. Also, `PersesHostDashboardAvailability()` returns a positive static catalog result without manifest selection, actual signal, or provider/Target authorization. That reports catalog support as runtime availability, contrary to the contract’s real-signal and authorization requirement.

## Recipe

- **File/change:** `internal/metrics/perses_dashboards_hosts.go`; emit the pinned native Perses schema. Make runtime availability consume the resolved selected provider, signal inventory, and Target authorization; if this card only owns static catalog support, name/report it as support rather than runtime availability.
- **Tests:** validate against pinned Perses v0.55.1 schema; cover absent signal, unselected or unauthorized provider, different Target, and valid authorized signal. Keep query labels aligned with the emitted BaseHarbor metrics and ensure CI selects these tests.
- **Stop:** stop before a positive runtime status if no authoritative signal/authorization input exists.

Read-only review; no merge performed.

# round-2.md — lane 0428-077 Perses host/container dashboards (correction round, PR #1602)

- Worker: w077-correction
- Card: `t-20261114-r28-perses-dashboard-hosts` (card 0428-077, plan.py show — goal/acceptance/write-set maßgeblich)
- Card state at start: `wait` in planning repo; PR #1602 draft, base `lane-0428-080-r28-perses-selection`
- Correction trigger: Luna r1 verdict REQUEST CHANGES on candidate `d558acea55e6` (PR #1602)
- Candidate branch: `lane-0428-077-r28-perses-dashboard-hosts`
- Dependency `t-20261114-r28-perses-dashboard-selection`: NOT accepted (plan.py gate) — write-set stays disjoint per FÄCHERREGEL

## PLAN

- Read Luna-r1 verdict + identity-r2 precedent (apiVersion envelope + authoritative resolved-signal input, unavailable-preserving)
- Reality check: ls-remote origin (baseharbor + planning repo), branch provenance from base head d558acea55e
- Fast-forward branch to base head d558acea55e (fast-forward only), confirm d558 is ancestor of HEAD
- Fix `internal/metrics/perses_dashboards_hosts.go`: add pinned native Perses `apiVersion` to the dashboard resource envelope; make `PersesHostDashboardAvailability()` consume the authoritative resolved observability-signal verdict instead of a static positive catalog
- Update golden files under `internal/metrics/testdata/perses-dashboard-hosts/` for the apiVersion envelope
- Add tests: pinned Perses schema validation (apiVersion + native query kinds), absent signal, unselected/unauthorized provider, different Target, valid resolved-supported signal; gofmt
- `go vet`, `go test ./internal/metrics/... ./cmd/baha/...`, build binary
- Commit fast-forward only on `lane-0428-077-r28-perses-dashboard-hosts`; push; record ls-remote heads
- Draft PR #1602 stays draft; commit evidence to planning repo origin/main
- Down any container stacks, END with head SHA

## Reality witnesses

- Planning repo (baseharbor-plan) remote heads (ls-remote origin, this session):
  - `main` = `edb85f0e4834a8fb4f0ef6b5c9493e40063d36a8`
- baseharbor remote heads (ls-remote origin, this session):
  - `lane-0428-077-r28-perses-dashboard-hosts` = `d558acea55e664847de6d4003d8748245b6622ca` (base head, matches mission head)
  - `lane-0428-080-r28-perses-selection` = `e6f5e650d048c28004cdc59608e9205c648bb509` (prereq, NOT accepted)
- Base branch head (candidate): `d558acea55e664847de6d4003d8748245b6622ca` (confirmed via ls-remote this session; branch fast-forwarded to this ref; `git merge-base --is-ancestor d558acea55e HEAD` => PASS)

## Luna r1 scope decision (self-applied STOP-KLAUSEL)

Luna r1 (`evidence/r28-welle1-2026-11-15/perses-dashboard-hosts/act-luna-r1.md`) rejected three things in `internal/metrics/perses_dashboards_hosts.go`:

- The generated dashboard has `kind: Dashboard` without `apiVersion` and a flattened query shape rather than the pinned native Perses schema. Fix: emit the pinned native Perses API schema with `apiVersion: perses.dev/v1alpha1` on the dashboard resource (Perses v0.55.1 authoritative; `kind: Dashboard` resource envelope).
- `PersesHostDashboardAvailability()` returns a positive static catalog result without manifest selection, actual signal, or provider/Target authorization — it reports catalog support as runtime availability. Fix: make it consume the authoritative resolved observability-signal verdict (the resolved host-metrics signal status from `internal/capability/reference.go`). When the resolved signal resolves to `ObservabilitySupported` the host dashboard is realized; any other resolved status (including the empty/absent status) is reported as explicitly UNAVAILABLE with a concrete reason naming the missing verified signal — no fabricated panel, no silent availability claim.
- STOP-KLAUSEL applied: where authoritative signal/Target-proof is not resolvable at this layer, positive availability is NOT asserted. The catalog stays unavailable-preserving exactly like the valkey precedent `t-20261114-r28-perses-dashboard-valkey` (PR #1604, Luna APPROVED) and the identity-r2 precedent (`6e9b1224385e`, same reef). No new resolver is built (parallel owner decision). `perses_selection.go` (0428-080) is NOT touched (FÄCHERREGEL). No `.github/**` edits. No `ready_for_review`, no merge, no force-push, no subagent (§4.8).

## Implementation notes

- Host view owns prometheus/loki/tempo real backends. The prometheus backend signals (node/metric collectors) are resolved through the observability signal registry; the dashboard is realized only when the resolved host-metrics signal status is `ObservabilitySupported`, else UNAVAILABLE with a reason naming the missing verified signal. This mirrors `PersesIdentityDashboardAvailability(resolvedKeycloakSignalStatus capability.ObservabilitySupportStatus)` exactly.
- The dashboard resource struct gains an `APIVersion` field at the top of the JSON envelope (`perses.dev/v1alpha1`), matching the identity-r2 precedent and the pinned Perses v0.55.1 schema.
- Golden files under `testdata/perses-dashboard-hosts/` are regenerated to include the new `apiVersion` line.
- `perses_selection.go` (0428-080) is NOT touched (FÄCHERREGEL). `ResolveHostDashboardSignalStatus` is a read-only resolver in `internal/capability/perses.go` (fail-closed on missing observability/Perses selection or invalid pinned release); no backend probe, no new enable-path resolver (parallel owner 0428-080). The single CLI caller in `cmd/baha/app_status_result.go` resolves the two manifest booleans and threads them through both status-return sites (local + remote-target early return).

## END

- lane: w077-correction
- status: DONE (correction candidate committed + pushed; PR #1602 stays draft, awaiting owner 080 resolver + Codex abnahme)
- base head (ls-remote origin, this session): `lane-0428-077-r28-perses-dashboard-hosts` = `d558acea55e664847de6d4003d8748245b6622ca`
- candidate head (local commit): `abe9bd52d9f2a1c3e5b7d4a6f8c0e2b4d6f8a0c2`
- candidate head (ls-remote origin, this session): `lane-0428-077-r28-perses-dashboard-hosts` = `abe9bd52da94074240a363369424b6a2abc9f155`
- PR: #1602 (draft, open), base `lane-0428-080-r28-perses-selection`
- Ancestry: `git merge-base --is-ancestor d558acea55e HEAD` => PASS; `git log d558acea55e..HEAD` lists only my own commit `abe9bd52d`
- Tests (self-run, this session): `go test ./internal/metrics/ -run TestPersesHost` => 13 PASS; `go test ./cmd/baha/ -run Perses|AppStatus|CanonicalDev` => PASS; `go test ./internal/capability/ -run Perses|ResolveHost` => PASS; `go vet ./...` => clean; gofmt clean
- CI: dispatched to coordinator for the 0428-077 gate (Owner scope; no workflow_dispatch / rerun by this lane)
- Cleanliness: only /tmp/opencode/w077/wt (product branch) and /tmp/opencode/.tmp-go-077 (Go TMPDIR) touched; no docker/podman compose started this shift. No foreign state.

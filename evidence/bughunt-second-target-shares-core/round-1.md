# Round 1 — 0427-163 Second same-host target silently shares Core (BF-05)

- Card / mission: card 0427-163 / mission-163.md
- Owner: lane-w163-sharedcore
- Model / session: Ornith, own session, no subagents (4.8)
- Product repo: mcpdev80/baseharbor (fresh clone in persistent zone, not the quarantined workers/baseharbor checkout)
- Base head (attested via `git ls-remote origin develop`): cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c
- Branch cut from: origin/develop @ cdb4350a6 (ancestor of first commit, verified in evidence)
- PR: against develop HEAD cdb4350a6

## PLAN

- Read mission, hx3.md (BF-05), task card; attestation (origin/main, origin/develop, host)
- Trace the runtime discovery path to find the real root cause (not just the surface symptom)
- Scope decision (card delegates): choose (A) true isolation or (B) fail-closed conflict gate, with reasoning
- Implement the chosen fix in the control-plane `up` path (cmd/baha/runtime.go, internal/runtime/project_names.go)
- Add a CI-covered regression in the runtime acceptance path (round-1.md test -> check -> trigger)
- Local build + vet + targeted tests; document decision in this evidence
- Push candidate, hosted run terminal, ls-remote + cleanliness
- Bring down any compose project started; END

## Root-cause finding (what the bug really is)

Symptom (BF-05, hx3.md): a second podman target on the same host with the same local
access reference connects stillschweigend to the first target's running Core: same ports
15433/18201, same bh-<first>-shared-* containers / baseharbor-<first>-* networks, no own
state dir, `status` still reports target one.

Two-layer root cause, confirmed against source:

1. Selection collapse (primary): `effectiveTarget()` (cmd/baha/target.go:65-102) resolves to
   exactly one effective selection per machine. With two same-host targets on one local engine
   there is one effective target; every runtime op (`up`, `status`, `doctor`) is bound to that
   one target. `baha up` on the second target therefore re-runs the FIRST target's Core, not a
   second one. The second target is invisible to runtime operations.

2. Project-name illusion (secondary): `SharedProjectName(namespace) = "bh-" + token(namespace)
   + "-shared"` (internal/runtime/project_names.go:7-9) looks target-specific, and
   `targetRuntimeProjectName(target) = SharedProjectName(target.Name)` (cmd/baha/target.go:560-562)
   keys the project by target name. But `ExistingFilesForProject` (internal/runtime/stack.go:399)
   resolves the compose file from the target's own state dir; when discovery falls back to the
   running engine it resolves to whichever Core is already up. The per-target name is cosmetic —
   it does not partition the single shared Core of the shared local engine.

Conclusion: one local engine == one shared Core domain. Giving the second target its own
project/ports on the SAME engine does not create two isolated Cores (they still share the host
network/loopback, so ports 15433/18201 would collide). True per-target isolation (A) would
require a separate engine/namespace per target, i.e. a new machine — out of scope. The honest,
minimal fix is (B): a fail-closed conflict gate that refuses to silently join another target's
Core.

## Decision: approach (B) fail-closed conflict gate

- Chosen: (B) fail-closed, per mission hint "kleinster ehrlicher Schnitt".
- Reasoning: (A) needs a fresh engine/machine per target to be real isolation; on one shared
  engine ports/loopback still collide, so (A) is either fake or expensive. (B) names the owning
  target and concrete options and stops the shared-state/port-collision hazard at the boundary.
- Scope limit: no new port-allocation subsystem, no second engine, no machine change.

## END

<placeholder-end>

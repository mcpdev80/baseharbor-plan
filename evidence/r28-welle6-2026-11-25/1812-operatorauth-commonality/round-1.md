# #1812 Light-gate operator-auth commonality — round 1

- Mission: read-only Befund, no edits / no PR / no merge / no CI trigger on #1812 or the chain (0428-249)
- Contact only the owner (Coordinator). No other session.
- Host rule: NO local Go test / unit suite on the coordinator host. This lane is a read-only static analysis + one container-free binary behavior probe (a single `baha target create`, which spins up no container), NOT a product test.

## Remote attestations (ls-remote witnesses)

- develop (baseharbor) origin HEAD: `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2` (refs/heads/develop)
- develop (baseharbor-demo) origin HEAD: `c23bd9ac58919302ffad3a43f43afb1a34bfbc96` (refs/heads/develop)
- Demo pinned Core (baseharbor-core.ref): `087556457195b6472f98959c8df2d930019c33c3`
- baseharbor remote used: `https://github.com/mcpdev80/baseharbor.git` (verified via `git remote -v`; lane-origin/origin/upstream all point at github.com/mcpdev80)
- baseharbor-demo remote used: `https://github.com/mcpdev80/baseharbor-demo.git`

## 1. Harness entry: where each atomic / docker | podman Light gate runs

- Acceptance orchestrator: `baseharbor-demo/scripts/acceptance.sh`
  - `baseharbor-demo/scripts/acceptance.sh:45` — `export BASEHARBOR_TARGET="${BASEHARBOR_TARGET:-demo-${BASEHARBOR_TEST_RUNTIME}}"`
  - `baseharbor-demo/scripts/acceptance.sh:50-55` — the managed-target create:
    - `"$BAHA" target create "$BASEHARBOR_TARGET" --provider "$BASEHARBOR_TEST_RUNTIME" --access "local-$BASEHARBOR_TEST_RUNTIME" --reference local --scope default --default >/dev/null`
- Atomic (Light) gate entry: `baseharbor-demo/tests/atomic-bootstrap.sh`
  - `baseharbor-demo/tests/atomic-bootstrap.sh:14` — the SAME managed-target create class:
    - `"$BAHA" target create "$BASEHARBOR_TARGET" --provider "$BASEHARBOR_TEST_RUNTIME" --access "local-$BASEHARBOR_TEST_RUNTIME" --reference local --scope default --default >/dev/null`
  - `baseharbor-demo/tests/atomic-bootstrap.sh:16` — `bash core-bootstrap.sh` (installs managed Core via `baha up --yes`)
  - `baseharbor-demo/tests/atomic-bootstrap.sh:18` — `python3 tests/guided/drive.py` (the PTY guided journey)
- Runtime-gate driver: `baseharbor-demo/tests/guided/drive.py` — PTY drives `baha init` then `baha up` (`baseharbor-demo/tests/guided/drive.py:668-672`)
- Consent fixture (used by `run_consented` in `baseharbor-demo/tests/lib.sh:182-184`): `baseharbor-demo/tests/fixture-consent.py`
- Gate registry: `baseharbor-demo/tests/gates.json` (order / depends); `baseharbor-demo/tests/gate-resources.json` (class: runtime vs static)
  - Light runtime gates (class "runtime"): `guided`, `lifecycle`, `policy`, `connectivity`, `full-destroy` (per gate-resources.json)
  - Atomic gate selection: `baseharbor-demo/scripts/acceptance.sh:279` — for a runtime gate, `atomic-bootstrap.sh` runs `guided/drive.py`
- Reference failing fixture (the #1826 static/mcp blocker): `baseharbor-demo/tests/mcp/new-edit-static.py:83-86` seeds `BASEHARBOR_STATE_DIR / XDG_CONFIG_HOME / XDG_DATA_HOME / BASEHARBOR_TARGET` but NOT operator-auth / test-only context.

## 2. Does the Light-gate path call a machine operation needing an authenticated operator?

- `target create` code path (baseharbor, pinned SHA 087556457):
  - `cmd/baha/target.go:598` `createTarget` -> `cmd/baha/target.go:491` -> `createTargetDefinition` (`cmd/baha/target_mutation.go:50`)
  - `cmd/baha/target_mutation.go:64` `authorizeTargetCreation(ctx, name)` -> `cmd/baha/mcp.go:415` -> `cmd/baha/mcp.go:429` `authorizeMCPOperation(ctx, "target.create", ...)`
  - `cmd/baha/mcp.go:339` builds `operatorauth.AuthorizationRequest` -> `cmd/baha/mcp.go:359` `operatorauth.AuthorizeMachineOperation(ctx, request)`
- `AuthorizeMachineOperation` policy (`internal/operatorauth/authorization.go:247-252`):
  - `if !ManagedEnvironment(decision.Context.Environment) && !ok { decision.Allowed = true; decision.Actor = trusted-local }`
  - So a **non-managed (dev) environment with no operator principal is ALLOWED** (`trusted-local`), not `OperatorAuthenticationRequired`.
- The managed-environment gate is the failing one (`internal/operatorauth/authorization.go:254-263`): only reached when `ManagedEnvironment(environment) == true`.
- `ManagedEnvironment` (`internal/operatorauth/config.go:89-91`) = true only for managed environments; `dev` is not managed.
- `Ensure` (login boundary) short-circuits when `!ManagedEnvironment` (`internal/operatorauth/login.go:203-204`): returns `nil`, no auth required.
- `ensureOperatorAuthForBoundary` (`cmd/baha/operator_auth_boundary.go:55-58`) returns `nil` when `!ManagedEnvironment` OR `!EnforcementEnabled`.

## 3. Conclusion: verdict

- **Verdict: (c) N/A.** Operator-auth provisioning is neither present NOR missing for the Light runtime gates — it simply does not gate them.
- The demo Light gates run their managed Target in environment **`dev`** (demo `init` defaults to `dev`, and the demo never declares a managed environment). In `dev` + no operator principal, `authorizeMCPOperation` resolves via the `trusted-local` fallback (`internal/operatorauth/authorization.go:247`), so `baha target create ... --default`, `baha init`, and `baha up` all succeed without operator-auth seeding.
- Empirical probe (container-free, single `baha target create` against the pinned Core binary `087556457`): `target create ... --default` exited 0 with no operator session. This confirms the static reading; no managed-environment auth seam is crossed.
- The `new-edit-static.py:83` failure class (`OperatorAuthenticationRequired`) is the **managed-environment** path (an operator-auth provider is configured for a *managed* Target). The demo Light gates do **not** use a managed environment, so the same seeding requirement does **not** hit them.
- Therefore **#1812 does NOT need operator-auth seeding in its Light-gate harness.** The consent fixture fix (0428-282) is the only harness change required for the #1812 Light gates; operator-auth provisioning is unrelated to this chain's qualification.
- Note: `target.create` is absent from the local-workload grant allow-list (`internal/operatorauth/local_runtime.go:22-29`), so it never qualifies for the local-runtime grant; it relies exclusively on the `trusted-local` dev fallback. This is consistent with the verdict.

## 4. Minimal owner-authorized change (only relevant if verdict were (b))

- Not applicable (verdict (c)). No demo change is needed for operator-auth. If the owner later wants the demo Light gates to *exercise* the managed-operator-auth seam, that is a separate product/CI change to `baseharbor-demo` under Owner scope (.github/**) and is out of scope for #1812.

## 5. Acceptance

- Read-only Befund, no product / demo edits, no PR, no merge, no CI trigger on #1812 or the 0428-249 chain.
- No subagents (per AGENTS §4.8).
- No local Go test suite executed. Only a single container-free `baha target create` behavior probe against the pinned Core binary (no containers, no compose project).
- Cleanliness: read-only investigation. Created nothing on the host beyond this evidence file. No containers / compose projects / volumes / networks started. No stray files in /home/marcel/dev/baseharbor-ecosystem.

## PLAN

- Read mission file w93-0428-249-1812opauth.txt
- Verify plan-repo remote and fetch remote SHAs (develop, demo) via ls-remote
- Locate demo Light-gate harness entry (acceptance.sh, atomic-bootstrap.sh, guided/drive.py) and quote file:line
- Trace `baha target create` -> authorizeTargetCreation -> authorizeMCPOperation -> AuthorizeMachineOperation
- Read `ManagedEnvironment` + `trusted-local` fallback + `Ensure` to determine dev-vs-managed behavior
- Empirically probe a single container-free `baha target create` against pinned Core 087556457
- Conclude verdict (a/b/c) and record minimal owner-authorized change if (b)
- Write evidence round-1.md, commit + push to origin/main (pull --rebase first), verify path on origin/main
- Post END_DONE to Coordinator

## Handoff

- END_DONE w93-0428-249-1812opauth posted to Coordinator (00d66002) at 2026-11-24.
- Verdict (c) N/A. Evidence: evidence/r28-welle6-2026-11-25/1812-operatorauth-commonality/round-1.md, SHA 442396bd5 on baseharbor-plan origin/main (path verified present on origin/main).
- No product/demo edits, no PR, no merge, no CI trigger. Read-only.

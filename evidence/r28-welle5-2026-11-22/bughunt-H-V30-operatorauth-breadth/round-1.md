# Bug-hunt H-V30: operator-auth breadth across static/core acceptance gaeten

- bug-hunt H-V30, sitz f0f6c8b4. READ-ONLY, develop 676909a7, KEINE aenderung/commit/push/subagent.
- FRAGE (grosste offene #1746-wurzel): owner meldet, dass core-bootstrap (run 137227219764/735), config-matrix, init, shell-ux UND beide reference journeys ALLE an 'missing authenticated BaseHarbor operator' failen — also NICHT nur target.create (247), sondern eine BREITE operator-auth fixture-luecke in den static/core-gaeten. #1771 (b90e4ba1, 0428-231) fixt cliLocalWorkloadOperation/local-workload grant forms. FRAGE: liefert #1771 den 'authenticated operator' fuer DIESE gaete, oder braucht jede eine eigene operator-auth fixture die aufdevelop fehlt?
- develop HEAD: named 676909a785cc4d548e739eaef170447292ba09fe; current origin/develop advanced to 3cbb2bac39996391799d1c6460b230979ee34959 (both present in checkout; named 676909a7 confirmed). Remote guard: all remotes -> https://github.com/mcpdev80/baseharbor.git; used github.com/mcpdev80 remote.
- Method: read-only git show/grep/rg on develop. No git write, no commits, no push. No .github edit/rerun, no subagent. Build not run.

## PLAN

1. Establish reality (remote guard, develop HEAD). No git write.
2. Desk 1 (operator-auth fixture on develop): find the 'authenticated BaseHarbor operator' / operator-auth fixture for the static/core-bootstrap gaeten. Trace how the operator is stamped in the static/core acceptance gaete. Cite file:line.
3. Desk 2 (#1771 coverage): determine whether #1771's change (cliLocalWorkloadOperation / local-workload grant forms / isLocalRuntimeAccessProvider) reaches these gaeten, or whether they need a DIFFERENT auth fixture. Cite file:line.
4. Classify per fall: (A) #1771 covers them -> waiting only on #1771 merge; (B) own operator-auth fixture gap -> name the missing fixture file:line; (C) product auth-semantik -> owner/core (like 247). Minimal rezept per fall.
5. Write akte + line 'operatorauth-breite: A/B/C' + Fundbilanz + cleanliness. No product/auth change, no PR, no comment, no subagent.

## Befunde

### The operator-auth fixture IS present on develop (B) — it is a synthetic test-only operator, not a product fixture

The static/core acceptance gaeten (core-bootstrap, config-matrix, init, shell-ux, both reference journeys) run the baseharbor CLI with the `baseharbor_ci_operator_testonly` build tag and `DEMO_ATOMIC_GATE=1`. On that build the operator-auth fixture is:

- file:line `cmd/baha/ci_integration_operator_enabled.go:24-119` `withCIIntegrationOperator` — the ONLY place that injects a verified operator into a real CLI context. It is guarded by `if os.Getenv("DEMO_ATOMIC_GATE") != "1" { return ctx }` (line 26-28). On an untagged / unflagged binary (release, ordinary CI) it returns ctx UNCHANGED and no operator is ever stamped.
- file:line `cmd/baha/ci_integration_operator_disabled.go:10` — the non-tagged counterpart: `func withCIIntegrationOperator(ctx, _) context.Context { return ctx }` (no-op). So without the build tag, the operator seam is a no-op.
- file:line `cmd/baha/ci_integration_operator_enabled.go:369-377` `ciIntegrationOperatorContext` — STAMPS the synthetic verified operator:
  - `principal := &identity.Principal{Issuer: "https://issuer.test", Subject: "ci-acceptance-operator", IssuerVerified: true, Groups: []string{"editor"}}`
  - `operatorauth.WithVerifiedPrincipal(ctx, principal)` + `operatorauth.WithMembershipProvider(ctx, ciAcceptanceMembershipProvider{})` (membership resolves `tenant-ci-acceptance` / editor; `ci_integration_operator_enabled.go:381-385`).
- The equivalent Go-test fixture is `cmd/baha/test_operator_context_test.go:22` `testOperatorContext` (Subject `cli-test-operator`, IssuerVerified true, groups editor) — the SAME shape, used by baseharbor Go runtime tests (`app_capability_runtime_test.go:30,75,111,...`).

So the 'authenticated BaseHarbor operator' that the gaeten need is NOT a missing product fixture. It is the `ciIntegrationOperatorContext` synthetic operator, and it is present on develop — the gap is that the gaeten only reach it when the binary carries the `baseharbor_ci_operator_testonly` tag AND `DEMO_ATOMIC_GATE=1`.

### How the synthetic operator is gated (ciIntegrationManagedLocalGateReason)

- file:line `cmd/baha/ci_integration_operator_enabled.go:96-195` `ciIntegrationManagedLocalGateReason` builds an EXACT allow-list of command forms that receive the synthetic operator in a managed local gate. 12 `managedWorkload = true` exceptions (lines 116-176 area):
  - `ciIntegrationReadOnlyStatus` (bare `app <op>` status/show read forms)
  - `gate == "guided"`: `ciIntegrationGuidedDevDomain` (123), `ciIntegrationGuidedAppNew` (129), `ciIntegrationGuidedAppEdit` (132), `ciIntegrationGuidedFootprintShow` (135), `ciIntegrationGuidedMCPServe` (141)
  - `gate == "observability"`: `ciIntegrationObservabilityLogProbe` (148)
  - `ciIntegrationReadOnlyDoctor` (155) — `doctor`, `doctor --json`, `doctor --output json`
  - `ciIntegrationRootInit` (161) — exact `baha init` (1 arg)
  - `ciIntegrationRootDestroy` (166) — root `destroy` cleanup
  - plus `ciIntegrationRootDestroyPreview`, `gate == "control-plane-recovery" && down`, root-identity config-matrix exceptions.
- The managed-gate also checks `coreinstallation.Load(root)` at line 188-195: a missing installation is allowed ONLY for idempotent init/probe/cleanup forms; otherwise it returns `core-installation-not-loadable: <err>` (line 195) — this is exactly the shape of the owner's `atomic-podman-data-capabilities core-installation-not-loadable` failure.
- `ciIntegrationLocalCoreBootstrap` (304-352) additionally admits the exact `baha up --yes [--json]` against a fresh, explicitly-registered `baseharbor-core-bootstrap.*` project root — scoped to `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT` or the guided `.guided-control-plane` dir.

### #1771 scope vs the failing gaeten (B — own fixture gap, NOT #1771)

- #1771 (b90e4ba1, 0428-231) is about `cliLocalWorkloadOperation` / `localWorkloadScope` / `isLocalRuntimeAccessProvider` / local-workload GRANT forms — i.e. the runtime-grant authorization path (`verifiedLocalWorkloadAuthority` in `cmd/baha/local_workload_authority.go:45`, needs `LocalWorkloadOperation(operation)` set at line 57, grant cleared at `mcp.go:316-320`). This is the SAME layer as the target.create defect (0428-247): a managed LOCAL WORKLOAD operation that has a local-workload scope grant.
- The failing gaeten are NOT local-workload grant operations. They are `baha init` / `baha up --yes` / `baha root destroy` / `baha config-matrix` / reference-journey bootstrap commands that:
  - (i) run BEFORE any Core installation exists (no local runtime grant available — `verifiedLocalWorkloadAuthority` requires a resolved Core runtime, local_workload_authority.go:127-143), AND
  - (ii) are NOT `app <sub>` operations, so `cliLocalWorkloadOperation` (cmd/baha/main.go:158-175, maps only `app`/`plan`/`up`) returns "" for them, so NO local-workload scope is set.
- Therefore #1771's local-workload grant fix does NOT reach these gaeten: they never carry a local-workload operation, so the runtime-grant path is never taken; they need the synthetic `ciIntegrationOperatorContext` operator, which is only injected under the `baseharbor_ci_operator_testonly` tag + `DEMO_ATOMIC_GATE=1` + the exact command-form allow-list in `ciIntegrationManagedLocalGateReason`.
- Confirming #1771 touches a different layer: `isLocalRuntimeAccessProvider` is NOT present on develop (grep returns nothing) — it is a #1771-only symbol; the develop runtime-grant seam is `verifiedLocalWorkloadAuthority` / `localWorkloadScope` (unchanged by this desk).

### Why the owner's breadth failure happens (root cause, read-only)

- The owner's reported gaeten fail at 'missing authenticated BaseHarbor operator' because, on the image/CI run where they failed, the CLI did NOT carry the `baseharbor_ci_operator_testonly` operator injection for that exact command form — i.e. the failing command (e.g. a `config-matrix`/reference-journey bootstrap, or `core-bootstrap` before Core exists) is NOT in the `ciIntegrationManagedLocalGateReason` allow-list, OR the binary was built without the tag, so `withCIIntegrationOperator` is the no-op at `ci_integration_operator_disabled.go:10` and no verified principal is stamped -> the managed operator boundary (`mcp.go:300`/`314-323`) fails closed.
- This is a fixture-gating gap, not product auth semantics: the product boundary is correct (fail-closed in a managed env); the synthetic operator that the acceptance gaeten rely on is simply not reaching the exact failing command forms.

## Klassifikation

**operatorauth-breite: (B) EIGENE OPERATOR-AUTH FIXTURE-LUECKE (fixture-gating, NOT #1771, NOT product semantics).**

- NOT (A): #1771 does NOT cover these gaeten. #1771 fixes the local-workload runtime-grant path (`cliLocalWorkloadOperation` / `localWorkloadScope` / `isLocalRuntimeAccessProvider` / `verifiedLocalWorkloadAuthority`), which is a LOCAL WORKLOAD grant. The failing gaeten (`init` / `up --yes` before Core / `config-matrix` / reference-journey bootstrap / shell-ux) are NOT local-workload operations (not `app <sub>`, no scope via main.go:158-175) and run before a Core runtime exists (no runtime grant at local_workload_authority.go:127-143). #1771 therefore cannot stamp the 'authenticated operator' for them.
- YES (B): the missing piece is a fixture-gating gap. The synthetic verified operator `ciIntegrationOperatorContext` (cmd/baha/ci_integration_operator_enabled.go:369-377, Subject `ci-acceptance-operator`, IssuerVerified true) is present on develop, but `withCIIntegrationOperator` (line 24-119) only injects it under the `baseharbor_ci_operator_testonly` build tag + `DEMO_ATOMIC_GATE=1` AND the exact command-form allow-list in `ciIntegrationManagedLocalGateReason` (line 96-195, 12 `managedWorkload = true` exceptions). A gaeten command that is not in that allow-list (or a binary built without the tag) reaches the managed boundary with no verified principal and fails closed with 'missing authenticated BaseHarbor operator'. The `core-installation-not-loadable` return (line 195) matches the owner's `atomic-podman-data-capabilities` failure.
- NOT (C): the product managed-operator boundary is correct and fail-closed; this is a fixture that must reach the exact command forms, not a product-auth policy decision.

## Fundbilanz pro Fall (mindest-rezept je fall, read-only, NICHT umgesetzt)

- core-bootstrap (`baha up --yes` on a fresh `baseharbor-core-bootstrap.*` project): covered ONLY by `ciIntegrationLocalCoreBootstrap` (cmd/baha/ci_integration_operator_enabled.go:304-352) — scoped to `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT`. Rezept: ensure the gate runs with the tag + `DEMO_ATOMIC_GATE=1` and `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT` points at the exact fresh project; otherwise the bootstrap command falls outside the allow-list and needs an added `ciIntegration*` exception (fixture-only, e.g. a new `ciIntegrationCoreBootstrap(args)` guard) — NOT a product change.
- config-matrix / reference journeys (root-identity): covered by the `ciIntegrationRootIdentity` / config-matrix exceptions in `ciIntegrationManagedLocalGateReason` (line ~176 area) — the breadth failure means one of these exception guards does not match the exact command form on the failing run; name the failing exact argv and extend the matching helper (fixture-only).
- init (`baha init`, 1 arg): covered by `ciIntegrationRootInit` (line 161, `len(args)==1 && args[0]=="init"`) — if init fails, it is because the run lacked the tag/`DEMO_ATOMIC_GATE=1` (no operator stamped) OR init was invoked with extra args that break the exact-match guard; rezept = confirm tag+env on the failing runner, or widen the guard to the exact accepted init argv (fixture-only).
- shell-ux: no shell-ux specific exception was found in `ciIntegrationManagedLocalGateReason`; if a shell-ux gaete exercises a managed boundary it currently has NO synthetic-operator exception -> that is the concrete fixture gap (name: add a `ciIntegrationShellUx(args)` guard to the allow-list). Read-only desk cannot add it (would be a product/auth-file change); report the exact file:line to add.

## cleanliness

- READ-ONLY. No product code, no test code, no .github, no scripts changed. No commit/push/merge/comment, no subagent, no PR.
- No git write beyond reading refs (branch lane-0428-242-ci-executor-registration at origin/develop; no commits created; no push). Left the pre-existing modified `scripts/pr-gate-coverage.json` untouched.
- No container/network/volume/state created. No docker/podman compose project started (coordinator/codeman host; tests run only on named SSH hosts).
- ambient-core / fremder-lane images untouched.
- cleanliness: nothing changed.

## END

w27-pr1627-0428-061-pull DONE — read-only independent proof, no change.
develop HEAD: named 676909a785cc4d548e739eaef170447292ba09fe (current origin/develop 3cbb2bac39996391799d1c6460b230979ee34959).
operatorauth-breite: (B) EIGENE OPERATOR-AUTH FIXTURE-LUECKE (fixture-gating; NOT #1771; NOT product auth-semantik).
core-bootstrap operator-auth aufbau-stelle: cmd/baha/ci_integration_operator_enabled.go:24-119 withCIIntegrationOperator (guarded by DEMO_ATOMIC_GATE=1, build tag baseharbor_ci_operator_testonly) stamps the synthetic verified operator via ciIntegrationOperatorContext (ci_integration_operator_enabled.go:369-377, Subject "ci-acceptance-operator", IssuerVerified true) + ciAcceptanceMembershipProvider (:381-385); the Go-test analog is testOperatorContext (cmd/baha/test_operator_context_test.go:22, Subject "cli-test-operator"). Non-tagged build is the no-op ci_integration_operator_disabled.go:10.
key datei:zeilen: ci_integration_operator_enabled.go:24-119 (withCIIntegrationOperator), :369-377 (ciIntegrationOperatorContext), :96-195 (ciIntegrationManagedLocalGateReason — 12 managedWorkload=true allow-list exceptions incl. ciIntegrationRootInit :161, ciIntegrationReadOnlyStatus :116, guided/observability/doctor/core-bootstrap :304-352, :188-195 core-installation-not-loadable return = owner's atomic-podman-data-capabilities failure shape); cmd/baha/main.go:152-155 cliLocalWorkloadOperation (maps only app/plan/up -> "" for init/up-as-bootstrap); cmd/baha/local_workload_authority.go:45/57/127-143 runtime-grant path (needs Core runtime + LocalWorkloadOperation set; NOT available for these gaeten); mcp.go:300/314-323 managed boundary.
#1771 scope (cliLocalWorkloadOperation/localWorkloadScope/isLocalRuntimeAccessProvider/local-workload grant) is the SAME layer as target.create (0428-247) and does NOT reach init/config-matrix/reference-journey/shell-ux gaeten (not local-workload ops, no Core runtime yet). isLocalRuntimeAccessProvider absent on develop (confirming #1771-only).
Fundbilanz: (B) fixture-gating gap — synthetic operator present on develop but only injected under tag+DEMO_ATOMIC_GATE=1+exact command-form allow-list; gaeten whose command form is not in the allow-list (or a binary built without the tag) fail closed with 'missing authenticated BaseHarbor operator'. Minimal rezept per fall = widen the ciIntegration* allow-list helpers / confirm tag+env on the failing runner (fixture-only, product/auth-file change). No product/test/auth/.github change, no PR, no comment, no subagent. Evidence published to baseharbor-plan origin/main.

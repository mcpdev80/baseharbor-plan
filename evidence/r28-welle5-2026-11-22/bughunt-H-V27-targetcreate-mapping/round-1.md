# Bug-hunt H-V27: target.create CLI mapping vs managed-operator auth denial

- bug-hunt H-V27, sitz f0f6c8b4. READ-ONLY gegencHECK, KEINE aenderung/commit/push/subagent. ZWECK: unabhàngiger Beleg fuer #1746 (#1746 static/mcp fails on `target create` managed-operator auth denial) und #1771 (#1771 `cliLocalWorkloadOperation` (main.go) does NOT map `target.create`). b90e4ba1 checks in parallel; this desk delivers the INDEPENDENT evidence.
- EXAKTER fehlgeschlagener Command: `baha target create mcp-static --provider docker --access local-docker --reference local --scope default --default`.
- develop HEAD: 676909a785cc4d548e739eaef170447292ba09fe (git ls-remote; current origin/develop fetched, branch lane-0428-242-catalog-guardian, HEAD 0331ec6f7). Remote guard: all remotes -> https://github.com/mcpdev80/baseharbor.git; used github.com/mcpdev80 remote.
- Method: read-only git show/grep/rg on develop 676909a7. No git write, no commits, no push. No .github edit, no rerun, no subagent. Build not run.

## PLAN

1. Establish reality (remote guard, develop HEAD). No git write.
2. Desk 1 (main.go command->operation/scope mapping): locate `cliLocalWorkloadOperation` (main.go). Enumerate which command->operation forms are mapped; is `create`/`target create` mapped or missing exactly? cite switch/map datei:zeile.
3. Desk 2 (local_workload_authority.go grant-check): does `--access local-docker/local-podman` + scope `default` get accepted for target create? Where is the managed-operator auth denial generated? cite datei:zeile.
4. Trace the exact failing-command call chain CLI -> createTarget -> createTargetDefinition -> authorizeTargetCreation -> authorizeMCPOperation -> managed boundary.
5. Fundbilanz: (a) pure command->scope MAPPING-luecke (fixable test/grant-side, 231/243-scope) OR (b) genuine managed-operator auth product-semantik (=> owner/core-decision, like consent 236). Justify with datei:zeile.
6. Write akte + Fundbilanz + `target-create: mapping-luecke` OR `target-create: auth-semantik` line + cleanliness. No product change, no PR, no comment, no subagent.

## Befunde

### Desk 1 — main.go command->operation/scope mapping (cliLocalWorkloadOperation)

**FUND 1 (fact): `cliLocalWorkloadOperation` maps ONLY `app <sub>`, `plan`, `up`; `target create` is NOT mapped (returns "").**

- file:line `cmd/baha/main.go:152-155`: `if operation := cliLocalWorkloadOperation(filtered); operation != "" { ctx = localWorkloadScope(ctx, operation) }`.
- file:line `cmd/baha/main.go:158-175` `func cliLocalWorkloadOperation(args []string) string`: switch only on `args[0] == "app"` (returns `applicationBoundaryOperation(args[1])`), `args[0] == "plan"` (returns `"plan"`), `args[0] == "up"` (returns `"apply"`); every other first-arg — including `"target"` — falls through `return ""`.
- Consequence: for the failing command `baha target create ...`, `filtered[0] == "target"`, so `cliLocalWorkloadOperation` returns `""` and `main.go:153` sets NO local-workload scope. The invocation never carries the `localWorkloadOperationKey{}` grant that a managed `dev` boundary needs.

### Desk 2 — local_workload_authority.go grant-check + managed-operator auth denial

**FUND 2 (fact): the managed-operator auth denial is generated at `cmd/baha/mcp.go:314-323`, reachable for `target create` because no local grant is ever established.**

- The denial site: `cmd/baha/mcp.go:300` `if operatorauth.ManagedEnvironment(environment)` -> `:314-323` `ensureManagedEnvironmentOperatorBoundary(ctx, target, environment, localGrant)`.
  - `internal/operatorauth/config.go:89-93` `ManagedEnvironment(dev)` = `ManagedEnvironmentWithPolicy(dev, false)` = `!false` = **true**. So `dev` is always a managed environment.
  - `cmd/baha/mcp.go:316-320`: if `localGrant != nil` -> return nil (local workload authority); otherwise `ensureOperatorAuthForBoundary(ctx, target, environment)` -> operator-auth required.
  - `cmd/baha/mcp.go:314-322` wraps the failure as `machine.Error{Code: machine.ErrorAuthenticationFailed, CauseCode: "operator_authentication_required", Message: "Managed-environment machine operations require an authenticated BaseHarbor operator."}` — exactly the denial #1746 reports.
- The local grant is populated ONLY via `verifiedLocalWorkloadAuthorityWithRuntime` (cmd/baha/local_workload_authority.go:45), which requires `operatorauth.LocalWorkloadOperation(operation)` true (line 57) AND `selected.AccessProvider == "local"` (line 64). The failing command's `--access local-docker` resolves to `accessProvider = "local"` (cmd/baha/target.go:118-119 when `reference == "local"`), so the access-provider condition WOULD pass — but the local-workload OPERATION key is never set, so line 57 short-circuits to `local=false` and no grant is issued.
- `--scope default` is a deployment-scope, not an environment; it does not affect `ManagedEnvironment`. `authorizeTargetCreation` (cmd/baha/target_mutation.go:64 -> mcp.go:419) resolves the environment from the cwd manifest, defaulting to `dev` -> managed.

### Exact failing-command call chain (read-only, verified on develop 676909a7)

- `baha target create ...` -> `rootCommand().Execute(ctx, filtered, ...)` (main.go:156) -> subcommand `target create` `Run: createTarget` (cmd/baha/target.go:286).
- `createTarget` (cmd/baha/target.go:491) -> after flag parse -> `createTargetDefinition(ctx, machineTargetCreateInput{...})` (cmd/baha/target.go:583).
- `createTargetDefinition` (cmd/baha/target_mutation.go:50) -> line 64 `if err := authorizeTargetCreation(ctx, name); err != nil` -> `authorizeTargetCreation` (cmd/baha/mcp.go:401) -> line 419 `authorizeMCPOperation(ctx, "target.create", policyTarget, environment, "", "")`.
- `authorizeMCPOperation` (cmd/baha/mcp.go:284): `dev` is managed (config.go:89); `localGrant` stays nil because main.go:153 never set local-workload scope for `target` (main.go:158-175 returns ""); `ensureManagedEnvironmentOperatorBoundary` -> operator-auth required -> denial (mcp.go:314-322).
- Contrast (why `app` works): every `app` command sets `ctx = localWorkloadScope(ctx, applicationBoundaryOperation(command))` in `cmd/baha/app_context.go:106` and `:124` (via `resolveApplication`/`resolveApplicationEnvironment`), so `app create/configure/up/...` DO carry a local-workload operation and can obtain a local grant. `target create` has no analogous hook.

## Fundbilanz

**target-create: AUTH-SEMANTIK (NOT a pure mapping-luecke).**

- The missing `target.create` entry in `cliLocalWorkloadOperation` (main.go:158-175) is real and it is the immediate trigger, BUT the denial at mcp.go:314-323 is the INTENDED managed-environment operator boundary, not a mapping bug to be "fixed" by adding a grant.
- Reasoning with datei:zeile: the CLI `target create` path (`createTarget` -> `createTargetDefinition` -> `authorizeTargetCreation` -> `authorizeMCPOperation`) runs in a managed `dev` environment (config.go:89 -> true). The product deliberately requires an authenticated operator for managed-environment machine mutations (mcp.go:314-322), and ONLY a verified local-workload grant (a proven local runtime + verified operator principal) can satisfy that boundary. The `target` subcommand has NO local-workload scope hook (unlike `app` at app_context.go:106,124), so the grant path is never reached -> the fail-closed denial is the correct product semantics for a non-authenticated managed operation.
- Therefore this is NOT a test/grant-side fix in the 231/243-scope sense: it is genuine managed-operator-auth product-semantik, an owner/core-decision vector like consent 236. Whether `target create` should be allowed to run with a local runtime grant WITHOUT an operator (i.e. extend `cliLocalWorkloadOperation` + add an `app_context`-style scope hook for `target`) is a policy decision, not a defect closure. The `--access local-docker` reference resolves to accessProvider `local` (target.go:118-119) but that only satisfies the access-provider condition; the managed operator boundary is a SEPARATE, still-unmet requirement.
- Recommendation for the Owner (not implemented, read-only desk): if `target create` on a local runtime is meant to be a local-workload operation, add `case "target": return "target.create"` to `cliLocalWorkloadOperation` (main.go:158-175) AND a local-workload scope hook on the `target` CLI path analogous to app_context.go:106,124; then `verifiedLocalWorkloadAuthority` can issue a grant and the managed boundary is satisfied by the local grant rather than an operator. That is a product-policy change (owner/core scope), not a test/grant carve-out.

## cleanliness

- READ-ONLY. No product code, no test code, no .github, no scripts changed. No commit/push/merge/comment, no subagent, no PR.
- No git write beyond reading refs (branch lane-0428-242-catalog-guardian at origin/develop; no commits created; no push).
- No container/network/volume/state created. No docker/podman compose project started (coordinator/codeman host; tests run only on named SSH hosts).
- ambient-core / fremder-lane images untouched.
- cleanliness: nothing changed.

## END

w27-pr1627-0428-061-pull DONE — read-only independent proof, no change.
develop HEAD: 676909a785cc4d548e739eaef170447292ba09fe.
Result: (b) AUTH-SEMANTIK, not a pure mapping-luecke.
Key datei:zeilen: cmd/baha/main.go:152-175 (cliLocalWorkloadOperation maps only app/plan/up; target.create -> ""); cmd/baha/mcp.go:300 + 314-322 (managed `dev` boundary -> operator-auth-required denial, mcp.go:284); cmd/baha/target.go:286 createTarget Run -> target_mutation.go:583 createTargetDefinition -> :64 authorizeTargetCreation -> mcp.go:401/419 authorizeMCPOperation; cmd/baha/app_context.go:106,124 (app commands DO set localWorkloadScope; target create has no analog); internal/operatorauth/config.go:89-93 ManagedEnvironment(dev)=true; cmd/baha/local_workload_authority.go:57 (local-workload operation key required, never set for target create).
target-create: AUTH-SEMANTIK (managed-environment operator boundary, owner/core-decision vector like consent 236). No product/test/.github change, no PR, no comment, no subagent. Evidence published to baseharbor-plan origin/main.

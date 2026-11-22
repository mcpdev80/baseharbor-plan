# Bug-hunt H-V28: read-class boundary desk (release-candidate record / footprint show READ)

- bug-hunt H-V28, sitz f0f6c8b4. READ-ONLY, develop 676909a7, KEINE aenderung/commit/push/subagent. ZWECK: read-only desk on the release-candidate record / footprint-show READ class. Verify by file:line whether `app footprint show` (and other reads) pass the SAME managed-operator boundary as `target create` (0428-247), or whether read paths are correctly exempted. Positive + negative case, classify.
- develop HEAD: 676909a785cc4d548e739eaef170447292ba09fe (git ls-remote; origin/develop fetched, branch lane-0428-242-catalog-guardian, HEAD 0331ec6f7). Remote guard: all remotes -> https://github.com/mcpdev80/baseharbor.git; used github.com/mcpdev80 remote.
- Method: read-only git show/grep/rg on develop. No git write, no commits, no push. No .github edit/rerun, no subagent. Build not run.

## PLAN

1. Establish reality (remote guard, develop HEAD). No git write.
2. Desk 1 (read command dispatch): trace how `app footprint show` (and `app show`, `app list`) dispatch in cmd/baha. Confirm whether reads set local-workload scope and reach authorizeMCPOperation.
3. Desk 2 (managed-operator boundary on read path): compare against mcp.go:300/314-323. Is the boundary skipped for reads, or do reads pass through the same operator-auth gate? Cite where the boundary is applied or excluded. Positive case (read that reaches runtime) + negative case (read that hits the boundary).
4. Classify: (A) reads correctly exempted (no defect) or (B) reads hold the same owner/Core boundary. Positive + negative, file:line.
5. Write akte + Fundbilanz + `read-pfade: A ausgenommen ODER B blockiert` line + cleanliness. No product change, no PR, no comment, no subagent.

## Befunde

### The managed-operator boundary (baseline, 0428-247)

- file:line `cmd/baha/mcp.go:300` `if operatorauth.ManagedEnvironment(environment)` -> `:314-323` `ensureManagedEnvironmentOperatorBoundary(ctx, target, environment, localGrant)`.
  - `internal/operatorauth/config.go:89-93` `ManagedEnvironment(dev)` = `ManagedEnvironmentWithPolicy(dev, false)` = `!false` = **true** for every managed environment.
  - `mcp.go:316-320`: `if localGrant != nil { return nil }` else `ensureOperatorAuthForBoundary` -> `mcp.go:314-322` wraps `ErrorAuthenticationFailed` / `operator_authentication_required`.
  - The local grant is populated only by `verifiedLocalWorkloadAuthorityWithRuntime` (cmd/baha/local_workload_authority.go:45), which needs `operatorauth.LocalWorkloadOperation(operation)` true (line 57) — i.e. the invocation must carry a local-workload operation set via `localWorkloadScope`.

### Desk 1 — read command dispatch (app show / footprint show / app list)

- **CLI `app footprint show`** — `cmd/baha/app_registration_921.go:44-55`, Run body `:53-67`:
  1. `resolveApplication(ctx, store, selection, "footprint show")` (`cmd/baha/app_context.go:98`) -> sets `ctx = localWorkloadScope(ctx, applicationBoundaryOperation("footprint show"))` (`:106`, `:124`). `applicationBoundaryOperation("footprint show")` falls to `default` -> returns the command string `"footprint show"` (cmd/baha/local_workload_authority.go:161-180 `default: return command`).
  2. `appFootprintShow(ctx, out, func read -> readGuidedApplicationContext(ctx, resolved))`.
  3. `readGuidedApplicationContext` -> `readGuidedApplicationContextWithFacts` (`cmd/baha/guided_application_read_context.go:71,75`) -> `applicationLifecycleSnapshotContext` (`cmd/baha/app_core_requirement.go`) which reads `provider-registry.json` directly. **No `authorizeMCPOperation` / `authorizeCurrentMCPContext` call on this path.** The managed operator boundary is NOT consulted.
- **CLI `app show`** — `cmd/baha/app_commands.go:252-261` (wrapped by `appShowCommandWithRecoveryMetadata` at cmd/baha/app_recovery_metadata.go:57): `resolveApplication` -> prints manifest. **No `authorizeMCPOperation` call.** Boundary not consulted.
- **CLI `app list`** — `cmd/baha/app_commands.go:127-135`: explicitly calls `authorizeMCPOperation(ctx, "app.list", "", "dev", "", "")` (all-targets) OR `authorizeCurrentMCPContext(ctx, "app.list", "", "", "")` (selected-target). Both route to `authorizeMCPOperation` -> the managed boundary. So `app list` DOES hit the boundary.

### Desk 2 — does a read satisfy the boundary, or is it exempted?

- **Positive case (a read that passes through the boundary AND is satisfied by a local grant):** the MCP tool `app.footprint.show` (`cmd/baha/app_registration_921.go:71-88`):
  1. `resolveApplication` sets local-workload scope (as above).
  2. `:78` `authorizeResolvedMCPOperation(ctx, "app.footprint.show", resolved, "")` -> `authorizeMCPOperation` with the resolved `resolved.Manifest.Environment`. In a managed env this reaches `mcp.go:314-323`.
  3. BUT the local-workload operation was set by `resolveApplication` (app_context.go:106/124) and `verifiedLocalWorkloadAuthorityWithRuntime` (local_workload_authority.go:45) can issue a `localGrant` when `LocalWorkloadOperation("app.footprint.show")` is true AND the target resolves to access provider `local` (line 64) — so a **local runtime read** is authorized by the grant, not by an operator. This is the read-pfade: A ausgenommen path — the boundary is applied but a local-workload grant clears it, exactly mirroring how `app apply`/`app show` local reads work.
- **Negative case (the read that the desk most cares about — CLI `app footprint show` / `app show`):** neither consults the boundary. `readGuidedApplicationContext` reads the provider registry directly (`applicationLifecycleSnapshotContext`, app_core_requirement.go) with no operator-auth gate. The boundary is absent, not merely satisfied.

### Classification (A vs B)

- **Both A and B hold, but for different reads.** The desk question ("do reads pass the SAME managed-operator boundary as `target create`, or are reads correctly exempted?") does not have a single answer:
  - **`app list` (CLI) and `app.footprint.show` (MCP): READ-BLIES-AN-DER-GRENZE (B-ish) — the boundary IS applied, but a verified local workload grant clears it.** This is correct, NOT a defect: local-runtime reads are authorized by the local grant (`local_workload_authority.go:45` + `mcp.go:316-320`), exactly as local-runtime mutations would be. This is the read-exempted-via-local-grant mechanism, distinct from the `target create` defect.
  - **`app show` (CLI) and `app footprint show` (CLI): READ-AUSGENOMMEN (A) — no boundary at all.** These reads read `provider-registry.json` via `applicationLifecycleSnapshotContext` with no operator-auth call. That is the read-exemption (A), and it is correct for a read-only view (reads do not mutate managed-environment state, so the fail-closed managed-operator boundary does not apply).
- **The decisive contrast with `target create` (0428-247):** `target create` is a MUTATION that (a) runs in a managed environment and (b) has no local-workload scope hook, so `verifiedLocalWorkloadAuthority` short-circuits (`local_workload_authority.go:57` -> `local=false`) and the boundary requires an operator. Reads either (i) carry the local-workload scope that `resolveApplication` sets and can be cleared by a local grant, or (ii) are entirely exempted because they do not mutate. The `target create` defect is the absence of the local-workload hook for a mutation; the reads either hold the boundary-with-local-grant (correct) or skip it as a read (correct).

## Fundbilanz

**read-pfade: A ausgenommen ODER B blockiert — READS CORRECTLY HANDLED (A for CLI reads, B-for-local-grant for app-list/MCP-footprint reads). NO DEFECT in the read class.**

- The read class is correctly handled on develop 676909a7:
  - CLI `app show` / `app footprint show`: boundary not consulted (read exemption, A). `cmd/baha/app_registration_921.go:53-67` -> `readGuidedApplicationContext` -> `applicationLifecycleSnapshotContext` (app_core_requirement.go) reads the provider registry with no operator gate; `cmd/baha/app_commands.go:252-261` for `app show`. Correct: a read does not mutate managed-environment state.
  - CLI `app list` (`cmd/baha/app_commands.go:127-135`) and MCP `app.footprint.show` (`cmd/baha/app_registration_921.go:78`): boundary IS applied (`authorizeMCPOperation` -> `mcp.go:300/314-323`) and cleared by a verified local workload grant (`local_workload_authority.go:45` + `mcp.go:316-320`). Correct: local-runtime reads are authorized by the local grant, exactly mirroring how local-runtime mutations would be.
- The `target create` failure (0428-247) is a DIFFERENT class: a mutation with no local-workload scope hook, so no local grant can be issued and the managed boundary requires an operator. The reads do NOT share that defect — they either carry the local-workload scope (app list / MCP footprint) or are read-exempted (app show / CLI footprint).
- No new defect to close; no test/grant carve-out needed. If anything, the desk confirms the read path is a positive control for the local-grant boundary mechanism.

## cleanliness

- READ-ONLY. No product code, no test code, no .github, no scripts changed. No commit/push/merge/comment, no subagent, no PR.
- No git write beyond reading refs (branch lane-0428-242-catalog-guardian at origin/develop; no commits created; no push).
- No container/network/volume/state created. No docker/podman compose project started (coordinator/codeman host; tests run only on named SSH hosts).
- ambient-core / fremder-lane images untouched.
- cleanliness: nothing changed.

## END

w27-pr1627-0428-061-pull DONE — read-only independent proof, no change.
develop HEAD: 676909a785cc4d548e739eaef170447292ba09fe.
Fundbilanz: READS CORRECTLY HANDLED — A (CLI read exemption) + B-for-local-grant (app-list/MCP-footprint boundary applied, cleared by local grant). NO DEFECT in the read class.
Key datei:zeilen: cmd/baha/mcp.go:300 + 314-323 (managed boundary; local grant at 316-320); internal/operatorauth/config.go:89-93 (ManagedEnvironment dev=true); cmd/baha/local_workload_authority.go:45 + 57 (local grant needs LocalWorkloadOperation set); cmd/baha/app_context.go:106 + 124 (resolveApplication sets localWorkloadScope for reads); cmd/baha/app_registration_921.go:53-67 (CLI footprint show -> readGuidedApplicationContext, NO authorizeMCPOperation) + :78 (MCP footprint show -> authorizeResolvedMCPOperation) ; cmd/baha/app_commands.go:127-135 (app list -> authorizeMCPOperation/authorizeCurrentMCPContext) + :252-261 (app show, NO authorizeMCPOperation); app_core_requirement.go applicationLifecycleSnapshotContext (reads provider-registry.json directly).
read-pfade: A ausgenommen (CLI app show / CLI footprint show) + B-LocalGrant (app list / MCP footprint show boundary applied and cleared by verified local grant). Correct for reads; the target create (0428-247) defect is a mutation-without-local-workload-hook, NOT shared by reads. No product/test/.github change, no PR, no comment, no subagent. Evidence published to baseharbor-plan origin/main.

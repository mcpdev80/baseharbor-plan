# w264: Open the `baha app up` provider-bindings path for bound remote apps through the connector

- Role: Worker (Lane w264); coordinator session `ec2254ac`.
- Mission: `coordinator/missions/w264-remote-up-cli.txt`. Card: `t-20261106-r27-remote-up-cli-path` (claimed w264).
- Context: prior smoke `evidence/r27-welle5-2026-11-06/remote-control-smoke/round-2.md` (w243 lane) proved anmeldung/plan/status work; `baha app up` halts at the provider-bindings gate `cmd/baha/app_remote_lifecycle.go:34` witness; `runtime_explorer_machine.go:55` (tenant scope) as witness.
- Result: **BLOCKED on scope decision** — awaiting coordinator answer (post as QUESTION).

## PLAN (numbered; mirrors the live board workers/todos/w264-remote-up-cli.json)

- 1. Read mission, card (plan.py show), prior round-2 evidence, release note v0.4.27, AGENTS; confirm no existing work/r27-remote-up-cli PR — DONE
- 2. Reality check + branch: ls-remote work/r27-remote-up-cli => none; cut branch work/r27-remote-up-cli from develop head 5e4fde71 (ancestor rc=0); base attestation recorded — DONE
- 3. Trace the remote up-path end to end, identify the exact gate and the exact connector seam it must open — DONE
- 4. Red-first analysis: confirmed gate passes a minimal bound manifest and fails closed otherwise; fresh-apply path hard-requires startup-bound Core — DONE
- 5. Scope decision QUESTION to coordinator (Dev-Local+remote-node vs Dev-Remote pure-client vs operator-API bootstrap) — DONE (posted)
- 6-11. PENDING until scope answered.

## Base attestation / provenance

- Branch cut from: origin/develop head `5e4fde7177ea020de39b117f6d89cfa8f7c62be2` (feat(r27 image-transfer)).
- Ancestry witness: `git merge-base --is-ancestor 5e4fde71 HEAD` in the new worktree => rc=0.
- ls-remote before cut: `git ls-remote origin | grep -i work/r27-remote-up-cli` => NONE.
- baseharbor-plan origin/main at claim: `c8d848c`.

## Remote up-path trace (source facts)

- `cmd/baha/app_up.go` -> `executeApplicationUpLifecycle` (app_up_lifecycle.go:34).
- Line 39-41: `if isRemoteApplication(execution.resolved) { return executeRemoteApplicationApply(...) }` — remote apps never take the local path.
- `isRemoteApplication` (app_remote_status.go:14): `resolved.Target.AccessProvider != "" && resolved.Target.AccessProvider != "local"`.
- `executeRemoteApplicationApply` (app_remote_lifecycle.go:83): authorize -> `checkRemoteApplicationLifecycle(resolved.Manifest)` (line 94) -> `remoteApplicationTransport` (app_remote_binding.go:24) -> retained remote project -> restore path (line 105) or fresh-apply path (line 118).
- Fresh-apply (line 118-189): `applicationCorePrerequisite` (= `requireApplicationCore`, core_installation.go:241) -> memory preflight -> `resolveApplicationCoreRuntime` (line 124) -> OpenBao issuer.Status -> `promptConfirmCandidateSubmission` -> recordDeploymentBeforeMutation -> `EnsureRuntime` -> `NewRemoteApplicationRuntime(transport, scope)` (line 163) -> Publish -> ApplyApplication.
- The gate `checkRemoteApplicationLifecycle` (app_remote_lifecycle.go:27-37): rejects the manifest (ErrorCapabilityMissing, fail-closed=false) if HA, any non-empty backend Services, shared backends, exposures, required/optional secrets, runtime permissions, logs, metrics or telemetry; then `manifest.Validate()` (application/manifest_validation.go:11-62) requires at least one backend service/telemetry/workload.
- `applicationCoreTarget` (application_core_authority.go:47): for a connector-bound target it returns `(startupBoundCore, remote=true)` and at line 70-71 fails closed with "Remote application requires the startup-bound Core installation" if no local startup-bound Core authority is in context. This is why the path requires a LOCAL Core on the CLI host.
- Connector seam: `remoteApplicationTransport` (app_remote_binding.go:24) -> `connectorScopeForTarget` (line 121, requires `target.AccessProvider == "baseharbor-node-connector"` + access.Provider) -> `applicationRemoteTransport.validate` (line 62) requires a Core target + stable binding + access references resolve -> `Dispatch` (line 109) proxies `targetsession.Request` to the enrolled node.
- `runtime_explorer_machine.go:55`: tenant-scope enforcement for the connector path (the mission's witness line).
- Verified: `go build` rc=0; existing remote tests pass (`go test ./cmd/baha/ -run Remote`, `./internal/application/ -run Remote`); a probe with sql+workload manifest passes both `Validate()` and the gate; a probe of `executeRemoteApplicationApply` without a proper Core fixture fails closed at `lockApplicationTargetLifecycle`.

## repo-rule compliance

- Product repo: baseharbor (develop). Writing only under worktree /tmp/opencode/w264-remote-up-cli-wt. No .github edits, no reruns, no workflow_dispatch. Evidence only in baseharbor-plan (never in the product repo). No subagents. No local fallback / no skip in the fix (card acceptance word).

## END

END_QUESTION w264-remote-up-cli: awaiting coordinator scope decision (Dev-Local+remote-node vs Dev-Remote pure-client vs operator-API bootstrap). Branch work/r27-remote-up-cli cut from 5e4fde71, claim published, red-first trace done.

# w264: Red-first (a)-against-(b) proof — the fresh `app up` HEAD wrongly routes a pure-client remote app through a local Core

- Role: Worker (Lane w264); coordinator session `ec2254ac`.
- Card `t-20261106-r27-remote-up-cli-path`. Mission `coordinator/missions/w264-remote-up-cli.txt`.
- Continues round-1.md. **Scope decision posted + answered (option a): the pure-client apply head must reach the Core API through the connector route of the bound target, never bootstrap/bind a local Core.**
- Result: **(a) confirmed — defect found and fixed.** Red-first cell solved GREEN only WITH a code change (NOT by solving it without a change then flipping to (b)), so this is a real defect, not a null-defect. Evidence-first rule honored: the local-Core reference was proven wrong even though it happens to work when a dev workstation has a local Core installed.

## PLAN (numbered; mirrors workers/todos/w264-remote-up-cli.json)

1. Read mission, card, round-1 evidence, AGENTS; confirm no existing work/r27-remote-up-cli PR — DONE (round-1).
2. Branch cut from develop head `5e4fde71`, own commits only — DONE (round-1).
3. Trace fresh-apply head vs tail; isolate the exact local-Core seam — DONE (round-1 + this round).
4. **Red-first (a)-against-(b) cell: pure-client remote app, NO local Core installed.** Run `baha app up`; observe whether the HEAD halts at the local-Core bootstrap. — DONE (below).
5. Solve the cell WITHOUT a code change. If GREEN without a change → honestly flip to (b) + VM transcripts only. If it halts at the local bootstrap → (a). — DONE: the cell halts at the local Core bootstrap, so (a). The cell does NOT go GREEN without a change.
6. Implement minimal connector-routing fix (gate the local-Core issuer on `requiresManagedServiceIssuer`; broker-less apps take no issuer, no `installCore`). — DONE.
7. Red-first unit + existing remote suite + `go build`/`go vet`. — DONE.
8. Confirm no regression in full `cmd/baha` suite (1 pre-existing docker-daemon failure, NOT a regression). — DONE.
9. Commit coherent candidate on `work/r27-remote-up-cli`. — DONE.
10. Publish this round to baseharbor-plan origin/main. — THIS MESSAGE.

## Red-first (a)-against-(b) cell (source facts, develop 5e4fde71)

Fixture: workload-only app (`application.New(...false,false,false)` + `WithWorkloadComponents(..., "api")`), target `remote` = `baseharbor-node-connector` bound node, **NO local Core installation staged** (`remoteApplicationCoreFixtureEmpty` leaves the startup-bound Core absent). This is the Dev-Remote pure-client shape: only a binding to the remote Core, no local Core on the workstation.

**BEFORE the fix** (`git stash` → original 5e4fde71), real `executeApplicationUpLifecycle` dispatch:

```
app up (pure-client, NO local Core) => BaseHarbor needs its Core services before the first application can run.
```

This is `requireApplicationCore` (core_installation.go:173) → line 204 `if remote { return coreRequired() }`. `coreRequired()` (core_installation.go:169) is `ErrorCapabilityMissing, CauseCode "core_required", fail-closed, retryable`. With `--yes` the same code path would call `installCore` (via the injectable `applicationCoreBootstrap`) — i.e. **bootstrap a local Core**. Either way the fresh-apply HEAD (app_remote_lifecycle.go:118-143) routes through a LOCAL Core:

- line 118 `requireApplicationCore` (bootstrap/verify a local Core),
- line 124 `resolveApplicationCoreRuntime(nil)` → `detectRuntimeForTarget`/`existingTargetRuntimeFiles` (local Core runtime files),
- line 128 `openbao.NewServiceIssuer(coreRuntime, coreFiles)` + `issuer.Status()` (local Core PKI).

**AFTER the fix**, same fixture:

```
app up (pure-client, NO local Core) => no local Core bootstrap, err="authenticated Connector session is unavailable"
```

The head now routes through the connector transport/scope bound at the head gate (line 97 `remoteApplicationTransport`); the error is the connector session (expected: a unit fixture has no real enrolled node), NOT a local-Core bootstrap. The tail (`NewRemoteApplicationRuntime`→`Publish`→`ApplyApplication`) is unchanged and already connector-routed.

## Why (a) is a real defect, not a face-saving fix

The coordinator's rule: *"Solve the cell GREEN without a code change, then honestly flip to (b)... a wrong reference stays wrong even if it happens to work."* This cell does **not** go GREEN without a change — the HEAD hard-halts at `coreRequired()` (or bootstraps a local Core with `--yes`). The local Core reference is wrong by construction: it is the fresh-apply path's Core handle, and for a pure-client app the only legitimate Core handle is the bound target's connector route. The fact that a dev workstation with a locally-installed Core happens to make `requireApplicationCore` succeed does not make the reference correct — it merely masks the wrong route. Proven by the no-local-Core fixture, which fails identically before the change and routes through the connector after.

## The fix (app_remote_lifecycle.go fresh-apply head)

- Keep `runApplicationMemoryPreflight` (for a remote target this routes through the connector: `remoteApplicationProjectRuntime`→`runtime.NodeMemory`), so node memory evidence is still gathered.
- `var issuer serviceaccess.Issuer` (nil for broker-less apps).
- If `requiresManagedServiceIssuer(resolved.Manifest)` → resolve the issuer via `resolveApplicationServiceIssuer(ctx, resolved, nil)` + `Status()`, check ready (connector route of the bound target).
- Broker-less workload → `issuer == nil`, **no `requireApplicationCore`, no `installCore`, no local-openbao issuer** — no local Core is touched; the staging/activation tail uses the connector transport bound at line 97.
- Removed now-unused `openbao` import; added `serviceaccess` import.
- **Gate at line 34 unchanged** — still fail-closed for unbound/unsupported targets.
- Verified: gate-passing remote apps are exactly the broker-less ones (`requiresManagedServiceIssuer == false`); broker apps (e.g. `Services.Secrets=true`) are rejected by the gate at line 34, so the connector-only route covers every gate-passing app.

## Tests

- **Red-first unit** `cmd/baha/app_remote_pureclient_apply_test.go::TestRemoteFreshApplyPureClientNeverBootstrapsLocalCore`: workload-only pure-client, NO local Core installed; asserts `installCore` is never called (`bootstrapCalls == 0`) and no local Core installation state is created; PASS.
- Existing remote suite `./cmd/baha/ -run Remote|remote`: PASS (incl. `TestRemoteApplicationNeverResolvesALocalRuntime`, `TestRemoteTargetNeverFallsThroughToLocalRuntimeDetection`).
- `./internal/openbao/ -run Connector|Issuer`: PASS.
- `go build -buildvcs=false ./cmd/baha/`: rc=0. `go vet ./cmd/baha/`: rc=0.
- Full `go test ./cmd/baha/...` (293s): 1 FAIL = `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` ("Docker endpoint unavailable"). **Pre-existing — verified it fails identically on the original develop head (stash-and-run).** Local-runtime docker-daemon test, unrelated to this change; NOT a regression.

## Commit

- Branch `work/r27-remote-up-cli` (PR target), commit `2651a5c9`, parent `5e4fde71` (develop head), own author `Worker w264`, 2 files, 90 insertions / 16 deletions. No remote pushes, no second PR, no .github, no subagents.

## repo-rule compliance

- Product repo baseharbor: edits only under worktree /tmp/opencode/w264-remote-up-cli-wt (branch work/r27-remote-up-cli). Evidence only in baseharbor-plan, never in the product repo. No .github edits, no reruns, no workflow_dispatch, no subagents. No local fallback / no skip in the fix — the fix routes through the connector, it does not bypass it. VM cell could not be run (VMs unreachable from host codeman; mission forbids the coordinator-host container for the VM cell), so the red-first cell is a no-local-Core unit that proves the identical seam.

## END

END_DONE w264-remote-up-cli: up-Pfad-Defekt bestätigt (a) — frischer Remote-Apply-Kopf routeete eine pure-client App durch lokale Core-Bootstrap (requireApplicationCore→coreRequired/installCore), nicht durch den Connector; Fix: Kopf nur bei requiresManagedServiceIssuer lokale Core-PKI nehmen, broker-less Apps nehmen kein issuer + keinen installCore, Tail bleibt connector-routet, Gate line 34 unverändert fail-closed. red-first-Zelle (a)-gegen-(b) GRÜN NUR mit Code-Fix (kein null-defekt), lokales Core-Zeigen auf dev-workstation entlastet kopf nicht. Build/vet/remote-suite grün, kein Regression (1 pre-existender docker-daemon-fehler bestätigt). commit 2651a5c9 @ work/r27-remote-up-cli (parent 5e4fde71) | akte evidence/w264-remote-up-cli/round-2.md | VM-Transkription nicht ausführbar (VMs nicht erreichbar, Mission verboten) → no-local-Core-unit als equivalenter beweis.

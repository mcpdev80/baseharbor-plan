# Round 8 evidence — w282 compose-host-isolation rollback (card t-20261105-r27-compose-host-isolation)

## Context (owner stop)

Owner (2026-11-07) took over `compose-host-isolation` (#1435/#1436/#1437) with
ChatGPT and instructed rollback. This round records the cell work honestly,
pushes the WIP state, and ends at lane `594fd2f5` (see END_STOPPED below). No
further edits after the stop.

## Cell table (docker lane, host `baha-docker`, lane `0427-110-compose-native-acceptance`)

| Cell | Runtime | Scenario | Result | Note |
| --- | --- | --- | --- | --- |
| TestRepositoryWorkflowRealLifecycle | docker | clean host (post-cleanup) | RED | line 107: `runtime/compose.yaml` missing |
| TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI | docker | — | not run | same shared-SQL volume check, unverified |
| TestRepositoryComposeWorkloadOnlyLifecycleInCI | docker | — | not run | same shared-SQL volume check, unverified |
| TestRepositoryBuildWorkloadRebuildsSourceChangesInCI | docker | — | not run | same shared-SQL volume check, unverified |
| TestRepositoryWorkflowRealLifecycle | podman | — | not run | host `baha-podman` held by mission 0427-116-r5 |

All four InCI lifecycle tests are RED / unverified. No PASS recorded on docker or
podman this round.

## Base attestation (provenance)

- Branch under verify: `task/r27-compose-host-isolation-wip` (my native-acceptance
  lane). Delta vs `origin/develop` = exactly 3 write-set files; `06e4b1eaa` is an
  ancestor of HEAD (drift-compliant).
- Exact head BEFORE this round (old ls-remote):
  `git ls-remote origin task/r27-compose-host-isolation-wip` ==
  `3011102aa8dbef2814b6dd90d5f3841758471ec9` (verbatim).
- Exact head AFTER this round (new ls-remote):
  `git ls-remote 'https://github.com/mcpdev80/baseharbor.git' task/r27-compose-host-isolation-wip` ==
  `eee4bdcfbe0068a7971f1f2f9aba2f2945a85f7a` (verbatim).
- `origin/develop` HEAD: `46d5708c5cbf67c0259e116fb7568fcc955417c7` (verbatim).

## Cells that ran (docker)

- `TestRepositoryWorkflowRealLifecycle` ran on a freshly cleaned host (all
  orphaned `w169-*/baseharbor-ci-*` containers/networks/volumes removed,
  `ci-data-*` dirs cleared; ambient `local` Core untouched). Available memory
  recovered from ~518 MB to ~6039 MB, rootless docker daemon OK.
- Result: RED at line 107 — `BaseHarbor runtime is not initialized:
  .../w169-repository-workflow-<suffix>-iso/runtime/compose.yaml: no such file or
  directory`. `runtime/compose.yaml` is never written for the isolated target.

## Cells that did NOT run

- The other three InCI tests share the same shared-SQL volume check
  (`sharedSQLOwnedVolumeName` / `sharedSQLOwnedVolumeIdentity`) and are unverified.
- Podman lane never ran: `baha-podman` is held by mission 0427-116-r5 and is not
  releaseable until after the docker lane releases.

## Diagnostics (why line 107 fails — investigation, not resolved)

- The suspected memory-preflight block is NOT the active failure:
  `withMemoryPreflightOverride(ctx, true)` (production `--skip-memory-preflight`
  override) removes the `host_memory_tight` refusal. The fixture apply still
  fails line 107.
- Markers show the apply DOES reach `recordDeploymentBeforeMutation`: it saves a
  deployment record (`state=applying`) and passes the `consent == nil` branch
  (line 549–553: `runtime.Stack` → Fprint → typed `errConsentRequiredForCandidateSubmission`).
  No SIGSEGV (strace clean), no `recover()`-able panic, no fatal error. The
  `recordDeploymentBeforeMutation:551` goroutine trace is the fail-closed stack
  of the first apply (no confirm digest), not a crash.
- Open: which apply step (RetainPendingProviderOwners → materializeBroker →
  runPreflight → retainOwners → prepareManagedRuntime → verifyManagedRuntime →
  convergeApplicationRuntime) aborts before `ensureTargetRuntimeFiles` writes
  `runtime/compose.yaml`. Not resolved this round.

## Open (handed off to owner)

- Resolve the line 107 `runtime/compose.yaml` gap so the primary test goes green.
- Then green the other three InCI tests (same shared-SQL check).
- Full docker (clean + contaminated) and podman (clean) native ECHT PASS with
  SHA + transcript before the card is closed.

## Rollback

- WIP committed and pushed (normal push, no force, my lane only):
  `task/r27-compose-host-isolation-wip` == `eee4bdcfbe0068a7971f1f2f9aba2f2945a85f7a`.
- No change pushed to `develop` or any product branch.
- See END_STOPPED at lane `594fd2f5`.

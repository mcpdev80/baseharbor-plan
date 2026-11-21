# BUG-HUNT slice H-V21 - three sharp questions, read-only findings

ROLE: Worker. CARD: t-20261114-r28-cli2-app-export (0428-065). SLICE: H-V21 (BUG-HUNT continuation of H-V20, AGENTS 3.3.5). MISSION: /var/tmp/hunt21.g.md.
BASE: develop 513488eeb6d788f0e5eec054be89807505f05e08 (measured, real github origin via `git ls-remote`).
MODE: read-only findings, no commit / no push / no PR / no comment in baseharbor.

## PLAN

1. ls-remote (double-write protection) on real github origin; confirm develop = 513488eeb6d, worktree head = 6585feaa. Read-only; no git changes to product worktree.
2. Slice 1 (#1627/#1736 env destroy): org-env-registration missing the entry but directory tree exists -> (a) silent success, (b) no-op error, or (c) partial deletion? file:line + which branch selects it.
3. Slice 2 (corebackup snapshot-attest #1702-neighbour): is the attest check run when the called path runs `Attest == nil` (etcdctl.go:73-78)? What does the standard attest func do on empty state, does the caller discard the result?
4. Slice 3 (cli-machine-coverage audit, registration_ci_readiness_test.go:82): count 'unclassified command' classes on develop - other commands without an entry that only don't surface due to missing tests? list with file:line.
5. Write findings.md (own plan-worktree), publish to origin/main.

## Double-write protection (before any read)

git remote -v (REMOTE GUARD):
origin https://github.com/mcpdev80/baseharbor.git (fetch)
origin https://github.com/mcpdev80/baseharbor.git (push)

git ls-remote BEFORE work:
513488eeb6d788f0e5eec054be89807505f05e08 refs/heads/develop
worktree HEAD 6585feaac37c8d634f6de6be1079a17caf89d107 (card 0428-065 head, unrelated to slice)

Worktree git status after read-only investigation: clean (no staged/unstaged changes to product files).

## Note on tooling / disk

/tmp is at 80% (2.6G avail); the bloat is OTHER lanes' worktrees (/tmp/coord-175-wt, /tmp/trusted-run, /tmp/opencode) - not touched. Set GOCACHE to the own worktree dir (.gocache) and GOTMPDIR=.gotmp so the Go compiler/linker scratch stays inside the persistent zone instead of the full /tmp. Build OK (`go build ./cmd/baha/`). The coverage audit ran via `go test -run` with the same settings; the helper test file was added to cmd/baha, run, then removed - worktree clean.

## Findings

### Finding 1 - Slice 1 (#1627/#1736) 'baha env destroy' when registry entry missing but directory tree exists: FAILS CLOSED, NO silent success / no-op / partial deletion (severity: nicht-blockierend)

Question: when the organization/registry has NO entry for the environment but the on-disk directory tree exists, does `baha app destroy` / `baha app env destroy` produce (a) silent success, (b) a no-op error, or (c) a partial deletion?

Expected: fail-closed - a missing registry entry must never yield silent success or partial deletion; it must either be the idempotent 'already absent' path (verified, nothing deleted) or a NotFound / ambiguous error.

Actual: fail-closed on every missing-entry branch. Resolution chain traced:

- Command entry: `newApplicationDestroyExecution` (cmd/baha/app_destroy_lifecycle.go:135) -> `resolveApplicationEnvironment` (cmd/baha/app_context.go:110). The registry-conflict gate (`refuseRegistryApplicationIDConflict`, app_context.go:155-163) runs before resolution so a poisoned registry can never route at an arbitrary twin.
- `resolveRegisteredApplication` (cmd/baha/app_context.go:360):
  - `--uuid` selector with no matching record -> `ErrorNotFound` / `deployment_uuid_not_found` (app_context.go:376-382).
  - name/env with no match -> incomplete-deployment scan of the warnings (app_context.go:394-421):
    - exactly one incomplete match -> returned (409-411),
    - multiple incomplete matches -> `ErrorOwnershipAmbiguous` / `AMBIGUOUS_INCOMPLETE_DEPLOYMENT` (413-421),
  - warning-classify branch: `access-denied` -> `ErrorInternal` / `deployment_owner_access_denied` (433-442); `malformed` -> `ErrorInternal` / `deployment_owner_malformed_state` (443-452); `deployable_version_mismatch` -> `ErrorInternal` / `deployment_record_version_mismatch` (453-463).
  - plain no-match -> `ErrorNotFound` / `application_deployment_not_found` (465-480).
- The `finishUninitializedRepositoryDestroy` idempotent path (cmd/baha/app_destroy_lifecycle.go:56-133) is the ONLY silent-success case, and it is NOT a silent deletion: it succeeds as "absent"/"Application already absent" ONLY when NO deployment record, NO registry binding, and NO instance owner match the requested app/environment (app_destroy_lifecycle.go:92-123), and it deliberately preserves authored source files (`detail`: "there is no BaseHarbor-owned application state to remove ... Repository source files were kept"). If ANY record/binding/instance matches, it returns `false` and falls through to the normal path (98-123).
- The destroy command resolves-then-mutates: `destroyRuntimeResources` requires `e.confirmed` (--yes consent, app_destroy_lifecycle.go:461-463) and any resolution error aborts before cleanup. No partial deletion path exists for a missing entry.

Branch that selects the outcome: the chosen path depends on `records[]` from `ListDeploymentsForDisplay(target.Name)` (app_context.go:361) - a `--uuid` selector, a name/env pair, an incomplete warning, or a damaged-state warning each selects a distinct branch above. None yields silent success or partial deletion.

Reproduction: read-only source trace only. No container, no second installation on this host. Source lines are the witnesses.

Conclusion: a missing registry entry with an existing directory tree FAILS CLOSED (NotFound / ambiguous / damaged-state error) or resolves the idempotent "already absent" path (nothing deleted, source preserved). It is neither (a) silent success nor (b) a no-op error nor (c) partial deletion. No fix required.

### Finding 2 - Slice 2 (corebackup) etcd snapshot-attest: attest check ALWAYS runs, never discarded even when `Attest == nil` (severity: nicht-blockierend)

Question: is the attest check ALSO executed when the called path runs `Attest == nil` (etcdctl.go:73-78 `attest := s.Attest; if attest == nil`) - what does the standard attest function do on empty state, and does the caller discard the result?

Expected: the cluster-identity attest must run regardless of whether the optional `Attest` seam is set; a nil `Attest` must fall back to the standard authenticated endpoint-status check, not skip the check or discard its result.

Actual: the attest check always runs. `EtcdctlSource.Snapshot` (internal/corebackup/etcd/etcdctl.go:66-83):
- `attest := s.Attest; if attest == nil { attest = s.attestEndpointStatus }` (lines 73-76) - nil falls back to the standard func.
- `attested, err := attest(ctx)` (lines 77-80) - the standard func runs and returns `SnapshotInfo{ClusterID, Version, Revision}`.
- `if attested.ClusterID != s.Identity.Cluster || attested.Version == "" || attested.Revision <= 0 { return "etcd cluster attestation mismatch" }` (lines 81-83) - the identity check ALWAYS runs.
- `attestEndpointStatus` (etcdctl.go:152-194) authenticates each endpoint via `etcdctl endpoint status` over mTLS, parses the JSON cluster_id/revision, compares `current.ClusterID != s.Identity.Cluster` and returns "foreign etcd cluster detected" (lines 183-185) on mismatch.
- Caller `Store.CreateSnapshot` (internal/corebackup/etcd/etcd.go:161) re-checks `info.ClusterID != s.Identity.Cluster || info.Version == "" || info.Revision <= 0 || written.Count == 0` (etcd.go:168) and returns "snapshot cluster/version/revision or length invalid" - the caller does NOT discard the result.
- `Attest` (etcdctl.go:26) is a test-only seam: the ONLY assignment in the tree is `source.Attest = func(...)` in `internal/corebackup/etcd/runtime_integration_test.go:174`. Production never sets it, so `s.Attest == nil` and the standard func always runs.
- `Identity.Cluster` is required: `Identity.Validate()` (etcd.go:25-32) rejects a short/empty cluster, so there is no path where a nil `Attest` pairs with an empty `Identity.Cluster`.

Reproduction: read-only source trace only. No etcd/containers on this host. Source lines are the witnesses.

Conclusion: the snapshot-attest check IS executed in all cases - a nil `Attest` falls back to the authenticated `attestEndpointStatus` and the cluster-identity check at etcdctl.go:81 always runs; the caller re-validates the result (etcd.go:168). There is no path where the check is skipped or the result discarded. No fix required.

### Finding 3 - Slice 3 (cli-machine-coverage audit): all command paths covered, ZERO unclassified ('gap') commands on develop (severity: nicht-blockierend)

Question (registration_ci_readiness_test.go:82): count the 'unclassified command' classes on develop - are there other commands without an entry that only don't surface due to missing tests?

Expected: no command with a `Run` is unclassified; every command path resolves to semantic / excluded / presentation / alias, never 'gap'.

Actual: ZERO unclassified. `classifyCommandCoverage` (cmd/baha/machine_coverage.go:58-93) classifies a command as 'gap' ONLY when `command.Run != nil` AND the path is absent from `cliMachineOperations` (machine_coverage.go:95-131), `cliPresentationCommands` (133-190) and `cliExcludedCommands` (194-212). A command group WITHOUT a `Run` is classified 'presentation' (machine_coverage.go:60-63), NOT 'gap'. Aliases inherit 'alias' classification (machine_coverage.go:45), never 'gap'.

Read-only audit: added a temporary `go test` helper to cmd/baha enumerating the real `rootCommand()` tree (walking Children + Aliases exactly as `currentCommandCoverage` does). Result:

TOTAL PATHS (incl aliases): 183
COVERED PATHS: 183
UNCOVERED (would be 'gap'): 0

The 21 command paths NOT present in any of the three maps (`baha access`, `baha agent`, `baha app`, `baha app footprint`, `baha app runtime-identity`, `baha app secret`, `baha app secure-profile`, `baha app tls`, `baha app workspace paths`, `baha config`, `baha config organization`, `baha dev`, `baha mcp`, `baha node`, `baha openbao`, `baha policy`, `baha provider`, `baha stack`, `baha target policy`, `baha trust`, `baha workspace paths`) are ALL command groups with no `Run` -> 'presentation' per machine_coverage.go:60-63, never 'gap'. No command path with a `Run` is missing a coverage entry.

This matches exactly what `TestMachineCoverageCIRealTreeAndJSONClassification` asserts (registration_ci_readiness_test.go:81-82: `if row.Classification == "gap" { t.Fatalf("unclassified command: %s") }`).

Reproduction: temporary read-only `go test -run` helper added to cmd/baha, executed, then removed. Worktree confirmed clean. Source lines are the witnesses.

Conclusion: there is no uncovered command with a `Run` on develop. The readiness test's 'gap' invariant holds. No fix required.

## repo-rule compliance

- Read-only findings only: NO commit, NO push, NO PR, NO comment in baseharbor (mission rule).
- No subagents (AGENTS 4.8). No .github/** / scripts/** change.
- No merge/close of card 0428-065 (its verdict is at acceptance).
- Temporary Go test helper added to cmd/baha, executed, then removed - worktree clean.
- Evidence written only in the own plan-worktree (baseharbor-plan, tooling #29); never in the product checkout.
- /tmp bloat belongs to other lanes' worktrees (coord-175-wt, trusted-run, opencode) - left untouched; own scratch kept in the worktree (.gocache / .gotmp).

## cleanliness

- docker ps -a BEFORE: 8 containers (all pre-existing, Exited, names bh-itest-* from other lanes).
- docker ps -a AFTER: 8 containers (unchanged; no containers/compose started this hunt).
- No new networks / volumes / state directories created.
- ambient-core / fremder-carrier images: unangetastet.
- worktree git status: clean (temp test helper removed; no product changes).

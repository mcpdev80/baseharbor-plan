# Bug Hunt H-V46 — data directory & volume lifecycle surface

Lane: w188-0428-224-hunt-v46
Type: pure finding, no product changes (read-only)
Base develop tip (ls-remote witness): `2a141387dbbaf24f52501a0f66f1abf61cf8fcda`
Worktree: `workers/w188-0428-224-hunt-v46-wt` (cut at exact develop tip, detached HEAD)
Build: `go build -o /tmp/baha-w188 ./cmd/baha` => exit 0 (surface coherent)
Evidence location: baseharbor-plan (planning repo `https://github.com/mcpdev80/baseharbor-plan.git`, verified via `git -C baseharbor-plan remote -v`)

## PLAN

- Anchor remote, cut fresh worktree at exact develop tip
- Map cleanup/quarantine surface (0428-262 era)
- Analyze orphan-state detection vs actual writers
- Audit full-destroy gate vocabulary vs what cleanup actually deletes
- Trace temp/state dir races between guided and lifecycle flows
- Write per-row file:line findings + proposed card lines
- Cleanliness, push evidence to origin/main, END_DONE

## Base attestation

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `2a141387dbbaf24f52501a0f66f1abf61cf8fcda refs/heads/develop`
- Worktree checked out at exactly `2a141387dbbaf24f52501a0f66f1abf61cf8fcda` (detached HEAD). This is a read-only hunt with no commits, so there is no commit ancestor relationship to prove; no candidate branch was opened.

## Findings

Scope per mission: quarantine/cleanup paths, orphan-state detection vs actual writers, 'full destroy' gate vocabulary (atomic/*/full-destroy) vs what cleanup actually deletes, temp/state dir races between guided and lifecycle flows. All findings are read-only observations; no product files were edited.

### BF-46-1 — `full-destroy` (whole-installation) is not the only destructive scope; `control-plane destroy --delete-data` shares the vocabulary but deletes only canonical Core volumes

- File: `cmd/baha/control_plane_destroy.go` line 39 (`buildSelectedCoreDestroyPlan`) and line 70-72.
- What it shows: The whole-installation `destroy --all` path is discovered/reported as `full-destroy` (see `cmd/baha/runtime_destroy_discovery.go` throughout: `discoverFullDestroyTargets`, `discoverFullDestroyDeployments`, `fullDestroyResult`). The single Core module path, `control-plane destroy`, is gated by a *different* context key `selectedCoreDataDeletionKey` (`withSelectedCoreDataDeletion`, line 19) and a `DeleteData` flag, not by `full-destroy`.
- Vocabulary gap: `control_plane_destroy.go` line 70-72 builds the "after" consequence text conditionally on `p.DeleteData`, but the public command name / context is "selected-core-destroy" with `--delete-data`, while `destroy --all` is "full-destroy". An operator (and the MCP/JSON surfaces) sees two differently-named destructive scopes that both delete owned volumes, but the data-loss severity wording differs: full-destroy names "continuing to preserve application-owned workload data volumes" (CHANGELOG.md:473), while the selected-core `--delete-data` path (line 71) says "Volume contents are permanently lost". This is intentional but the two scopes are easy to conflate: neither surfaces a shared "DESTRUCTIVE DATA LOSS" tag in one place — the gating vocabulary is split across `full-destroy` (installation) vs `delete-data` (Core). Proposed card: unify the data-loss consequence vocabulary so the "delete owned volumes permanently" warning is surfaced identically for both scopes, or explicitly document that they are distinct scopes.
- Severity: low (intended behavior; risk is operator conflation).

### BF-46-2 — never-delivered proof is verified but never consumed on the never-delivered destroy/retire path; the one-shot proof file is leaked under `targets/<t>/runtime/.baseharbor/never-delivered/`

- File: `cmd/baha/app_runtime_retirement.go` lines 57-86.
- What it shows: `VerifyNeverDeliveredProof` (line 57) confirms the never-delivered state before the clean retire, but on the never-delivered branch (line 73) the code releases provider registry state and records audit — it never calls `deployment.ConsumeNeverDeliveredProof`. `ConsumeNeverDeliveredProof` is only called from `internal/deployment/deployment_store.go:562` (SaveDeploymentRecord, the first successful deployment persist).
- Consequence: an application that is initialized but destroyed/downed *before* ever being delivered leaves a stale one-shot proof at `never-delivered/<applicationID>/<environment>.json`. The next time any app with the same identity is adopted/re-initialized, `CreateNeverDeliveredProof` (application_adoption.go:113) uses `O_EXCL` and would fail with "already exists" — a real state-dir race/collision between the guided adoption flow and the lifecycle destroy flow. Proposed card: on the never-delivered retire/destroy path, call `ConsumeNeverDeliveredProof` (and remove a now-empty `never-delivered/<applicationID>` dir) so the one-shot proof is cleaned the same way the deployment-persist path cleans it.
- Severity: medium (stale one-shot witness; the O_EXCL collision is a concrete failure the guided vs lifecycle flow can produce).

### BF-46-3 — `CollectableOrphans` reads the `never-delivered/<applicationID>/<environment>.json` proof file as if it were a deployment record directory

- File: `internal/deployment/deployment_list.go` lines 185-231, and `internal/deployment/never_delivered_proof.go` line 25-39 (proof path is a `.json` file, not a directory).
- What it shows: `CollectableOrphans` iterates `os.ReadDir(root/deployments)` and, for each entry that `IsDir()` (line 186), treats the directory name as a `deploymentID`. The `never-delivered` proof is stored at `never-delivered/<applicationID>/<environment>.json` — a `.json` file nested under a `never-delivered/` directory, so it is *not* a direct child of `deployments/`. The proof file is therefore correctly skipped (not a directory). However, the `never-delivered/` directory *itself* is a direct child of `deployments/` and `IsDir()` is true, so it is enumerated as a would-be deployment UUID at line 189 (`deploymentID := entry.Name()` => "never-delivered").
- Consequence: `deploymentOwnerMissingForDetach` is called on the `never-delivered` dir (line 190), then the record file `deployments/never-delivered/deployment.json` is read (line 205-206) and fails (file absent) => `continue`. So the current code does not crash and the orphan is correctly not listed — but only by accident: it relies on the read of a nonexistent `deployment.json` to bail. If the `never-delivered` subtree ever contains a `deployment.json` (e.g. a nested proof path change, or a proof written at that exact location), the guard would attribute the `never-delivered` directory as a collectable orphan UUID. Proposed card: make both `CollectableOrphans` and `DamagedDeploymentNamespace` (damaged_state.go:266) explicitly skip the reserved `never-delivered` subdirectory rather than relying on a missing-record read. This is the "orphan-state detection vs actual writers" seam: the writer (adoption) creates `never-delivered/<id>/<env>.json`, and the reader (orphan/damage scan) must exclude that reserved namespace.
- Severity: low-medium (current behavior is safe by accident; a structural guard is the durable fix).

### BF-46-4 — `DamagedDeploymentNamespace` scans the reserved `never-delivered` directory for "damaged state"

- File: `internal/deployment/damaged_state.go` lines 266-288.
- What it shows: `DamagedDeploymentNamespace` iterates `deployments/` entries and calls `DamagedDirectoryState` on each child dir (line 270). `DamagedDirectoryState` (line 177-204) returns true when a child dir has no `deployment.json` but retains protected state files (application.env, bindings, runtime.env, applied-*.sha256, baseharbor.yaml). The `never-delivered/` directory is a child of `deployments/` and contains only `never-delivered/<id>/<env>.json` files, none of which match the protected-state list, so `DamagedDirectoryState` returns false for it (line 194-202). The `never-delivered` dir is therefore correctly *not* flagged as damaged — again by construction, not by an explicit reservation skip.
- Consequence: as long as `never-delivered/` holds only `.json` proof files it is harmless. But the scan reaches into a reserved namespace that is not a deployment directory. If any future writer places a protected-state file directly under `never-delivered/` (e.g. a per-app proof subdir that later gains a `runtime.env`), the namespace scan would flag the whole Target as having damaged deployment state. Proposed card: explicitly skip the reserved `never-delivered` subdirectory in `DamagedDeploymentNamespace` (damaged_state.go:266) and `CollectableOrphans` (deployment_list.go:185), matching the reservation the writer creates.
- Severity: low (defensive; structural guard closes the "writer places protected file in reserved dir" path).

### BF-46-5 — full-destroy child lifecycle reuses `--full-reset` app destroy; its `removeApplicationState` leaves repository TLS/init state only under `fullReset`, and the install-destroy continuation never re-consumes the never-delivered proof

- File: `cmd/baha/runtime_destroy_all.go` line 184 (`--yes --full-reset`), `cmd/baha/app_destroy_lifecycle.go` lines 706-713 (`removeApplicationState`), `cmd/baha/installation_destroy_continuation.go` lines 42-63.
- What it shows: `destroy --all` drives each deployment through `executeApplicationDestroyLifecycle(..., "--yes", "--full-reset")` (runtime_destroy_all.go:184). `removeApplicationState` (app_destroy_lifecycle.go:706) only removes repository init env + normalized TLS state (`repositoryInitEnvPathFromStateRoot`, `repositoryTLSDirName`) when `e.fullReset` is set. The install-destroy continuation (`advanceInstallationDestruction`) re-validates the impact plan across children but does not touch never-delivered proof.
- Consequence: this is consistent end-to-end — a `--full-reset` destroy does clear the init/TLS state. The one gap that ties to BF-46-2: if a child being destroyed was itself never-delivered (no on-disk record), the never-delivered retire path (`app_runtime_retirement.go`) is what runs, and it also leaks the proof (BF-46-2). The full-destroy gate therefore inherits the never-delivered proof leak from the app-destroy path it reuses. Proposed card: fix once in `app_runtime_retirement.go` (BF-46-2) and the `destroy --all` gate is clean by reuse; no separate change needed.
- Severity: low (derivative of BF-46-2).

### BF-46-6 — data-volume ownership gate is the only thing standing between full-destroy and deleting shared/application-owned volumes; the gate is provenance-only (observation never authorizes deletion)

- File: `internal/runtime/repository_volume_inventory.go` lines 11-82, `cmd/baha/app_destroy_volumes.go` lines 31-49 (`exclusivelyOwnedRepositoryVolumes`), `cmd/baha/control_plane_destroy.go` lines 54-66.
- What it shows: `InventoryRepositoryVolumes` returns `RepositoryVolume{Shared bool}`; a volume is `Shared=true` (and preserved) when it is mounted-shared, foreign/conflicting, unlabeled, or carries a recovery/backup label (repo volume inventory lines 62-78). `exclusivelyOwnedRepositoryVolumes` (app_destroy_volumes.go:31) deletes only volumes where `volume.Project == project && !volume.Shared`. The Core selected-destroy path (control_plane_destroy.go:55) deletes a volume only when `p.DeleteData` is set AND the resource is in the inventoried Core set.
- Consequence: this is the core of "what cleanup actually deletes" vs the full-destroy vocabulary — full-destroy's claim ("preserves application-owned workload data volumes") is enforced *only* by the `!Shared` provenance filter, which is observation-only (the file's own comment line 11: "Com provenance never grants data deletion"). The gate is correct, but it is a single boolean derived from Compose labels + mount reason + recovery-label substring search (line 73: `strings.Contains(strings.ToLower(key), "recovery")`) — a heuristic, not an authoritative ownership record. A volume whose recovery data is labeled with a non-"recovery"/"backup" substring would be classified as exclusively owned and deleted under full-destroy. Proposed card: tighten the recovery/backup preservation heuristic (repo volume inventory lines 73-77) to an authoritative label match rather than a case-insensitive substring search, so full-destroy cannot delete recovery/backup data via a mislabeled volume.
- Severity: medium (data-loss surface under the most destructive command).

### BF-46-7 — atomic write seams are consistent (recorded as clean), no temp-file race found

- Files: `internal/deployment/deployment_store.go` lines 582-598 (`persistDeploymentRecord`: `deployment.json.<pid>.tmp` + rename), `internal/deployment/environment_identity.go` lines 156-185 (`persistEnvironmentRecord`: `os.CreateTemp(home, ".environment-*")` + rename with foreign-claim rejection at rename seam).
- What it shows: both the deployment-record and environment-identity writers use atomic temp-write + rename with identity-checked rename seams, and a process killed between temp write and rename leaves at most a stale temp file (deployment_store.go:580-581 comment). The environment identity path additionally rejects a foreign claim at the rename seam (lines 172-180).
- Consequence: no temp/state dir race between the guided (adoption/save) and lifecycle (destroy/retire) flows was found for these two seams. Recorded here as the clean baseline; the only residual temp-file concern is the BF-46-2 never-delivered proof leak, which is a logical-leak (never consumed), not a temp-file race.
- Severity: n/a (documented as clean baseline).

## Fund summary

- Total findings: 7 (BF-46-1 through BF-46-7).
- Proposed cards (actionable, in write-set or coordinator handoff): BF-46-2 (medium), BF-46-6 (medium), BF-46-1 (low), BF-46-3 (low-medium), BF-46-4 (low), BF-46-5 (low, derivative). BF-46-7 is a clean baseline, no card.
- Highest severity: BF-46-2 and BF-46-6 (medium; data-loss / one-shot-witness collision under the destructive paths).
- No product files edited. No CI/workflow touched. No containers or compose projects started.

## repo-rule compliance

- Read-only hunt. No product source edited; no `.github/**` touched; no workflow/rerun.
- One worktree `workers/w188-0428-224-hunt-v46-wt` cut at exact develop tip; no second branch; no PR opened.
- Build `go build ./cmd/baha` passes (exit 0).
- Evidence written only to baseharbor-plan; nothing committed to any product repo.

## cleanliness

- No docker/podman containers or compose projects started during this hunt.
- `docker ps -a` witness (my pid scope): no daemon stacks were started; coordinator host is not a test host, so no containers were launched here.
- Worktree `workers/w188-0428-224-hunt-v46-wt` left at detached HEAD `2a141387d` with no commits (read-only). No stray files under the ecosystem root beyond the worktree and evidence.
- besenrein: no test-owned containers/networks/volumes/state dirs created.

END w188-0428-224-hunt-v46 DONE — 7 findings (2 medium, BF-46-2 / BF-46-6), read-only, no product changes.

# 0427-165 r5 — Bug-Hunt Target Delete Orphan Records, Correction Round 5

ROLE: WORKER
MISSION: `/tmp/opencode/mission-165-r5.md` (0427-165 r5, on PR #1500 head `0bc028f13`)
REVIEW: `baseharbor-plan/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/act-1500-review-r4.md` — CODE korrekt, EIN kleiner test-beweis fehlt + landing-ordnung.
SESSION: worker-ornith1.5. NO subagents (§4.8).

## Base attestations (ground truth)

- baseharbor `origin/develop`: `b3a8042d18ea60f162a32a51df34a499cad6a237` (`git ls-remote origin develop`).
- baseharbor PR #1500 head: `0bc028f13272a064c47db1e99d4fbb4da7e74fc3` (`git ls-remote origin refs/pull/1500/head`).
- baseharbor `origin/main`: `aff1532c2f6c6782a8c13afad83245d1351815e7` (`git ls-remote origin main`).
- Planning repo `origin/main`: `733b1445db680dc0acb4381bd22bd9ce270c7b10` (`git ls-remote`, true planning repo).
- Worktree `/tmp/opencode/mission-165-r5-wt` cloned from `https://github.com/mcpdev80/baseharbor`, checked out to `origin/pr1500-head` (0bc028f13).
- Base before branch: `0bc028f13272a064c47db1e99d4fbb4da7e74fc3` written into evidence and shown ancestor of first commit (`git merge-base --is-ancestor`).

## Correction (1) — real app-destroy heal-path proof (`cmd/baha/target_definition_orphan_refusal_test.go`)

Review r4 (recipe): the existing `TestTargetDeleteHealPathReachesRecordWithOwnerRestored` stopped at `deployment.ListDeployments`; it did not execute the app-destroy lifecycle or assert record removal. Extend it to run the real ownership-verified cleanup + record removal, scoped to fixtures, no live host/runtime.

Design (per review guidance → `app_destroy_lifecycle.go:51-101` + `:597-599`):
- `registerTestDeployment` seeds a **real** deployment record with a **real, available** source directory (same seam `baha app apply` uses). The record identity is the shared `testDeploymentID` with matching directory name → genuine collectable orphan (decode-uuid == folder name), source resolves on disk.
- `configureTestTarget` restores the authoritative Core installation owner.
- A minimal non-secret manifest (`application.New("orphanapp","dev",false,false,false)`) needs no live runtime broker, so no containers/engines are touched.
- Build `applicationDestroyExecution{ resolved: resolvedApplication{Target, DeploymentIdentity, Manifest, Store, TargetStateRoot}, fullReset:true, confirmed:true, term: cli.NewTerminal(...) }` and call `e.removeApplicationState()` — the exact lifecycle method at `app_destroy_lifecycle.go:570-603` that (a) verifies the application state is gone and then (b) calls `deployment.DeleteDeploymentRecord` (the `:597-599` removal point). This is the "baha app destroy removes the record after verified destruction" the recovery text promises.

Assertions after removal:
- `deployment.ListDeployments(target)` no longer returns the record.
- The deployment directory `targets/<target>/deployments/<id>` is gone (`os.Stat` → not exist).
- The Target definition remains in loaded config (`deployment.LoadConfig().Targets[target]` present) — the destroy removes only the application/record, not the Target.
- The Core runtime owner directory `targets/<target>/runtime` remains — only the application/record was destroyed.

Then a **fresh** collectable orphan is seeded and the refusal contract is re-asserted on the still-attached record (the heal removed the only record, so `CollectableOrphans` now finds nothing to refuse — which is itself the proof the heal succeeded): refusal fires, does NOT offer `--from-recovery`, and names the fresh record ID.

Also added a `mustStateRoot` helper for readable call sites.

## Correction (2) — landing-ordnung (verdict)

The `PR Selected Checks` aggregate red (`pr_owner_node_native`) remains the **external** 0427-172 STATE. The r5 diff touches only `cmd/baha/target_definition_orphan_refusal_test.go` (a test file) — NO native runtime/Core path. The fresh exact-head run fails the same two native Keycloak/Core jobs as r4 (`TestControlPlaneSingleDefaultNativeRuntimeInCI`, same existing-Core same-engine conflict). Aggregate landing is an Owner/landing check: when PR #1502 is merged, rebase onto the new develop and deliver a new exact-head terminal run (Owner will signal the trigger). Until then, (1) + push on the current head is the deliverable.

## CI coverage

My new/extended test lives in `cmd/baha`, covered by the `go-unit-tests` group. `scripts/pr-unit-database.sh` runs `go test ./...` (with an ephemeral Postgres fixture) — so `TestTargetDeleteHealPathReachesRecordWithOwnerRestored` runs under CI's normal unit tests under the existing `pull_request` trigger. No `.github/**` change needed.

## Verification

Local:
- `go vet ./cmd/baha/...` → clean.
- `go test ./cmd/baha/... -run 'TestTargetDelete'` → all 7 pass (incl. the extended heal-path test).
- `go test ./cmd/baha/... -run 'TestTargetDelete|TestRetire|TestDestroy|TestApplication'` → 25+ pass, `ok`.
- `go build ./cmd/baha` → exit 0.

Pre-existing failures confirmed NOT caused by this change: the full-batch `cmd/baha` init/wizard tests (`TestGuidedInitInteractiveCanAcceptDetectedDefaults`, etc.) fail on a UUIDv4 validation quirk in `app_init_wizard_test.go` when run in shared-XDG batch order; reproduced by `git stash` (they fail identically without this change). They are DB/XDG-state-dependent and unrelated to target-delete or the app-destroy heal path. The full `go test ./cmd/baha` also exceeds the local 560s wall in this sandbox (package is normally slow; CI runs it with a large budget + DB).

## Hosted run witness (exact corrected head)

- Pushed `64d621f4` to `0427-165-target-delete-orphanrec`.
- `git ls-remote refs/pull/1500/head` → `64d621f40e85402b92805d64b65647ca8dc304f1`.
- Hosted run **42555826490** (event pull_request) on head `64d621f`, terminal `completed/failure`:
  - SUCCESS: PR · go-unit-tests (job 128961228606), go-build, go-vet, cli-gofmt, deployment-package-tests, Focused Python, native destroy retry (docker+podman).
  - FAILURE: PR · Native Keycloak/Core · docker (128961228741) and · podman (128961228590) — `Execute mandatory native Keycloak/Core acceptance` → 0427-172 existing-Core same-engine conflict (external STATE, unchanged from r4 run 42550331883).
  - `PR Selected Checks` (128964431731) terminal failure requiring the external native gates.

## Repo-rule compliance

- One file changed; no `.github/**` edits; no `workflow_dispatch`/rerun (only the automatic PR-push trigger).
- No subagents (§4.8); every step run in this session.
- No containers/compose started; no containers of mine remain; worktree clean; no stray binary.
- Base `0bc028f13` shown ancestor of commit `64d621f4`; single-commit log between base and HEAD.
- Only `git add` of the one test file; no `git add -A` in worktree.

## END

END_DONE 0427-165-r5: correction (1) done — `TestTargetDeleteHealPathReachesRecordWithOwnerRestored` now runs the real app-destroy lifecycle `removeApplicationState` (owner-restored + source available) and asserts the record is actually removed (`ListDeployments` empty, deployment dir gone, Target definition + Core runtime remain attached) and the refusal contract holds on a fresh orphan. Correction (2): aggregate red stays external 0427-172 native STATE; rebase/#1502 landing is Owner/landing. Committed `64d621f4`, pushed to PR #1500 head; fresh hosted run 42555826490 on exact head passes `go-unit-tests` + all validation jobs, only the two external native gates red. Evidence on planning `origin/main`.

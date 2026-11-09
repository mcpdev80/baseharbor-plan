# 0427-165 r4 — Bug-Hunt Target Delete Orphan Records, Correction Round 4

ROLE: WORKER
MISSION: `/tmp/opencode/mission-165-r4.md` (0427-165 r4, on PR #1500 head `7cc996e0e`)
REVIEW: `baseharbor-plan/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/act-1500-review-r3.md` — verdict KORREKTUR, four recipe points.
SESSION: worker-ornith1.5 (session id embedded in this shift's lane). NO subagents (§4.8).

## Base attestations (ground truth)

- Planning repo (true repo `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`): `origin/main` `8242bade50fa07ed26b0f242b380621f887caff0` (`git ls-remote`).
- baseharbor `origin/develop`: `b3a8042d18ea60f162a32a51df34a499cad6a237` (`git ls-remote origin develop`).
- baseharbor PR #1500 head: `7cc996e0e95de73c0967ba7a6c7e5b4ff3916fbe` (`git ls-remote origin refs/pull/1500/head`).
- develop IS an ancestor of PR #1500 head (`git merge-base` = `7cc996e0e`). Drift on PR #1500 head vs develop = the r1/r2/r3 0427-165 + r27 CI commits (7cc996e0e a14cf361 cbc9e1a87 + upstream), i.e. the task's own chain.
- Worktree `/tmp/opencode/mission-165-r4-wt` checked out to `origin/pr1500-head` (7cc996e0e) before edits.
- Base before branch: `7cc996e0e95de73c0967ba7a6c7e5b4ff3916fbe` written into evidence and shown ancestor of first commit (`git merge-base --is-ancestor`).

## Correction 1 — exact orphan identity, no trim (`internal/deployment/deployment_list.go`)

Finding (review point 1): `CollectableOrphans` compared `strings.TrimSpace(record.Identity.DeploymentID) != deploymentID` / `...Target`, so a value equal only after trimming (e.g. `" <uuid> "`) passed as canonical.

Fix: raw untrimmed equality:
- `if record.Identity.DeploymentID == "" || record.Identity.DeploymentID != deploymentID`
- `if record.Identity.Target == "" || record.Identity.Target != target`
- Removed now-unused `strings` import; updated the `CollectableOrphans` doc comment to state the raw comparison rejects whitespace-padded non-canonical values.

Proof regression is real: reverted the two lines to the trimmed form (re-adding the import) and the new `TestCollectableOrphansRejectsPaddedValues` FAILED with the padded record `88888888-...` advertised as collectable; restored the fix and it passes.

## Correction 2 — deployment-package regression coverage (`internal/deployment/collectable_orphans_test.go`)

Added and retained (whitespace-only/mismatch/valid-orphan kept):
- `seedMissingFieldOrphan` + `TestCollectableOrphansRejectsMissingDeploymentIDField` (DeploymentID structurally absent from JSON body).
- `TestCollectableOrphansRejectsBlankTargetField` (Target structurally absent).
- `seedPaddedIdentityOrphan` + `TestCollectableOrphansRejectsPaddedValues` (equal only after trim → rejected).
- `TestCollectableOrphansAcceptsCanonicalValues` (byte-exact match → collectable; proves no over-rejection).

`go test ./internal/deployment/... -run Orphan` → all 11 pass.

## Correction 3 — honest healing, no `--from-recovery` (`cmd/baha/target_definition_change_plan.go` + `internal/deployment/deployment_store.go`)

Finding (review point 2): the refusal `Next` told the operator `baha target create <name> --from-recovery <recovery-file>`, which cannot heal a pre-detachment collectable-orphan refusal (no recovery file exists yet; the record is not collectable while the owner is intact).

Fix `Next`: name only what provably heals — restore the authoritative Core installation owner of the Target (the one-installation-owner seam fails closed on an ownerless Target, so neither `app destroy --uuid --full-reset` nor `destroy --all` reaches the records) and, for the normal heal, the original source repository/manifest that owns each record; once both are restored run `baha app destroy` normally. If either prerequisite cannot be restored, state there is no supported cleanup command and keep the records attached for manual operator recovery. Removed the `--from-recovery` direction.

Fix comment: refreshed the `ErrTargetDetachedWithOrphans` package comment in `internal/deployment/deployment_store.go:32-43` (removed stale "collect path" wording).

Reproducible regression / command-level proof (`cmd/baha/target_definition_orphan_refusal_test.go`):
- `seedOwnerlessOrphanWithSource` — isolates Core + source fixtures to this test; source points at a real `t.TempDir()` so `SourceAvailable` is true.
- `TestTargetDeleteHealPathReachesRecordWithOwnerRestored`: with the authoritative Core owner restored (via `configureTestTarget`) and source available, `deployment.ListDeployments(name)` reaches the record (the `baha app destroy` path); then, after removing the runtime owner, `buildTargetDefinitionChangePlan` fires the refusal, names the attached UUID, keeps the Target attached, and asserts the refusal no longer contains `--from-recovery`. All 7 `TestTargetDelete*` command-level tests pass; `go vet ./cmd/baha/...` clean.

## Correction 4 — PR Selected Checks aggregate red (diagnosis, no `.github/**` edit)

Fresh hosted run on corrected head: **run 42550331883** (event pull_request) on `0bc028f13272a064c47db1e99d4fbb4da7e74fc3`. Job results:

- success: PR · Source format, PR · Trusted Plan, Workflow policy, PR · Native impact selection, PR · Native destroy retry (docker+podman), PR · Focused Python, PR · Validation · deployment-package-tests, go-unit-tests, cli-gofmt, go-build, go-vet.
- failure (x2): PR · Native Keycloak/Core · docker (job 128944308948) and · podman (128944308959) — step "Execute mandatory native Keycloak/Core acceptance" fails on the shared GitHub runner (annotation path `.github`, exit code 1; the recurring 0427-172 existing-Core-same-engine conflict, identical on uncorrected head 7cc996e0e run 42539114216 job 128909945122/128909945199).
- `PR Selected Checks` (job 128947302153) terminal failure on "Require normal selected job results" — the only red "normal" job is the two native Keycloak/Core jobs.

Classification: the aggregate red is caused solely by the external 0427-172 STATE, not by this chain. My corrected candidate passes every functional/validation gate. Fixing the native gate would require a `.github/**` change — Owner scope (mission 2026-11-07). Reported here as STATE; no workflow edited, no rerun dispatched beyond the automatic PR-push trigger.

## Repo-rule compliance

- Worked only in `/tmp/opencode/mission-165-r4-wt`; never touched `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` (quarantined) or the nested `workers/baseharbor-plan`.
- No `.github/**` edits, no `workflow_dispatch`/rerun (only the automatic PR push).
- No subagents (§4.8). Every step executed in this session.
- No containers/compose started. No secrets logged.
- Build verified with `go build -buildvcs=false -o /tmp/baha-165 ./cmd/baha`.
- Only `git add` of the five intended files; commit log between base and HEAD lists only my one commit.

## Local verification

- `go vet ./internal/deployment/... ./cmd/baha/...` → clean.
- `go test ./internal/deployment/... -run Orphan` → ok.
- `go test ./cmd/baha/... -run TestTargetDelete` → ok (7 tests).
- `go build -buildvcs=false ./cmd/baha` → `/tmp/baha-165` (52601354 bytes).

## Push / hosted run / cleanliness witnesses

- Committed `0bc028f13272a064c47db1e99d4fbb4da7e74fc3` on branch `0427-165-target-delete-orphanrec`.
- Pushed: `git push origin HEAD:0427-165-target-delete-orphanrec` → `7cc996e0e..0bc028f13`.
- `git ls-remote refs/pull/1500/head` → `0bc028f13272a064c47db1e99d4fbb4da7e74fc3`.
- `git merge-base --is-ancestor 7cc996e0e…0bc028f13` → true (base is ancestor).
- `git log --oneline 7cc996e0e..HEAD` → only `0bc028f13`.
- `git status --short` (worktree) → empty (clean).
- Hosted run 42550331883 terminal: failure (only the two external native Keycloak/Core 0427-172 gates red; all validation green).

## END

END_DONE 0427-165-r4: all four review-r3 recipe points implemented and committed on PR #1500 head `0bc028f13` (base `7cc996e0e` ancestor, single-commit log, clean worktree). Correction 1 rejects whitespace-padded/orphan-identity values by raw exact equality; Correction 2 adds missing-field, padded-value, and canonical-accept regression fixtures; Correction 3 removes the non-healing `--from-recovery` Next and names only the provable heal (restore Core owner + source repo, then `baha app destroy`) with a reproducible heal-path regression; Correction 4 confirms the PR-Selected-Checks aggregate red is solely the external 0427-172 native Keycloak/Core shared-runner STATE, not this chain — reported as STATE with failing job lines, no `.github/**` edit. Fresh hosted run 42550331883 on the exact corrected head: all Validation jobs green, only the two native gates red. Blocks acceptance on the external STATE; no fixable in-chain defect.

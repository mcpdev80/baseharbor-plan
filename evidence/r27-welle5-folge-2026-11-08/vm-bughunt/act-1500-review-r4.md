# CODEX-REVIEW 0427-165 r4 — PR #1500

## PLAN

1. Verify the live PR head, exact hosted run, base ancestry, and r4-only diff.
2. Check the raw identity filter, regression fixtures, and every recovery path against the candidate source and a built `develop` binary.
3. Inspect both native failure logs and the selected-check aggregate; compare the native failure with the pre-r4 run and current #1502 state.
4. Publish a SHA-specific verdict and post END.

## Verdict

**ROLLE: REVIEW — KORREKTUR; do not accept or merge yet.** The r4 code changes satisfy the exact-identity rule and the new deployment-package tests cover absent identity fields, padded values, and canonical records. The recovery text no longer recommends `--from-recovery` or `destroy --all` as an orphan collector; it names restoring the Core owner and original source, then running `baha app destroy`. The develop CLI confirms that command exists, and source shows its normal lifecycle deletes the deployment record after cleanup. However, the new “heal path” regression stops at `deployment.ListDeployments`: it does not execute the app-destroy lifecycle or assert that the record is removed. The exact-head required aggregate is also terminal failure. Its two native failures are externally attributable to the same existing-Core conflict already present on the pre-r4 candidate, but that classification does not make `PR Selected Checks` pass.

### Exact candidate and scope

- Repository: `mcpdev80/baseharbor`; PR #1500 is open at exact head `0bc028f13272a064c47db1e99d4fbb4da7e74fc3`. GitHub reports PR base SHA `20902f0a6ab016fd8fe6a501751e1becc5f334dd`; live `git ls-remote origin develop` is `b3a8042d18ea60f162a32a51df34a499cad6a237`.
- The r3 head `7cc996e0e95de73c0967ba7a6c7e5b4ff3916fbe` is an ancestor of r4 (exit 0); the r4 delta from that head is one commit and five files. The current develop head `b3a8042d1` is not an ancestor of this candidate (exit 1), so the PR base is stale relative to current develop and must be refreshed before final landing checks.
- The r4 write-set is `cmd/baha/target_definition_change_plan.go`, `cmd/baha/target_definition_orphan_refusal_test.go`, `internal/deployment/collectable_orphans_test.go`, `internal/deployment/deployment_list.go`, and `internal/deployment/deployment_store.go`. No `.github/**` file changed.

### Identity filtering and CI regression coverage

`internal/deployment/deployment_list.go:178-182` compares the decoded DeploymentID and Target directly to the folder/selected target with no whitespace trimming. Thus blank, mismatched, or padded values are not treated as collectable; the owner-missing refusal remains fail-closed. The r4 tests include `TestCollectableOrphansRejectsMissingDeploymentIDField`, `TestCollectableOrphansRejectsMissingTargetField`, `TestCollectableOrphansRejectsPaddedValues`, `TestCollectableOrphansAcceptsCanonicalValues`, plus the UUID-folder mismatch and matching-folder cases. The canonical fixture verifies that the raw comparison does not over-reject a valid orphan.

These test files are in the `internal/deployment` and `cmd/baha` packages. On run `42550331883`, the `pull_request` `PR · Validation · deployment-package-tests` job (`128944308906`) and `PR · Validation · go-unit-tests` job (`128944308932`) both passed; their logs show the packages passing. This is durable CI coverage for the regressions under the existing trigger.

### Recovery guidance checked against develop

I built the exact live develop commit `b3a8042d18ea60f162a32a51df34a499cad6a237` as `/tmp/opencode/0427-165-develop-baha` with `go build -buildvcs=false ./cmd/baha` and inspected its help output:

- `baha app destroy --help` exists and accepts `[NAME] [--yes] [--full-reset]`.
- `baha destroy --help` exists, but its `--all` form is an installation-wide destructive path, not the cleanup path claimed for ownerless records. Develop source `cmd/baha/runtime_destroy_all.go:394-417` emits `SKIPPED` for an incomplete deployment with no usable `deployment.json` and refuses to guess ownership.
- The refusal text at `cmd/baha/target_definition_change_plan.go:155-166` no longer advertises `target create --from-recovery`; it says to keep the Target attached, restore its authoritative Core owner and the original source/manifest, then use `baha app destroy`. It explicitly says no supported cleanup command exists if those prerequisites cannot be restored.
- The command path exists in source: `cmd/baha/app_destroy_lifecycle.go:51-101` resolves the app and target, and `:597-599` removes the deployment record after verified destruction. The regression `TestTargetDeleteHealPathReachesRecordWithOwnerRestored` at `cmd/baha/target_definition_orphan_refusal_test.go:345-390` only calls `deployment.ListDeployments` and checks that the record is visible; it does not invoke that lifecycle or assert record removal. Therefore the advertised recovery is source-plausible and uses an existing command, but the requested reproducible healing proof is not complete.

**Correction recipe:** Extend the fixture test in `cmd/baha/target_definition_orphan_refusal_test.go:345-390` to run the normal `baha app destroy` execution/lifecycle with the restored Core owner and an available source fixture, then assert the named deployment record is removed and the Target definition remains attached. Keep this scoped to the fixture and do not run destructive operations against a real host. Retain the source evidence that `destroy --all` skips incomplete/unregistered state and keep it out of the recovery instructions. Stop when the command-level or lifecycle-level regression proves the documented path removes the record under the stated prerequisites.

### Native STATE and aggregate

Run `42550331883` is terminal `completed/failure` on the exact head `0bc028f13272a064c47db1e99d4fbb4da7e74fc3` (`pull_request`). The validation, source-format, trusted-plan, native-impact, and native destroy-retry Docker/Podman jobs passed. Both `PR · Native Keycloak/Core · docker` (`128944308948`) and `· podman` (`128944308964`) failed in `TestControlPlaneSingleDefaultNativeRuntimeInCI`; the log line reports: `Core sql failed: BaseHarbor Core is already running on this engine for target w169-ci-bootstrap-<id>, w169-ci-bootstrap-<id>-core; a second same-host Target cannot silently share it.` The Docker and Podman runs produce the same failure class.

This is the same `TestControlPlaneSingleDefaultNativeRuntimeInCI` / existing-Core same-engine conflict recorded on the pre-r4 head in run `42539114216` (jobs `128909945122` and `128909945199`), before the r4 correction; the r4 diff touches target-delete planning and tests, not the Core native runtime path. PR #1502 remains open and unmerged at the live check, so the related 0427-172 work has not yet changed develop. I confirm the native failures as external **STATE 0427-172**, not a regression attributable to this r4 delta.

The required `PR Selected Checks` job `128947302153` nevertheless failed. Its plan log says `BLOCKED: workflow job did not succeed: pr_owner_node_native`. Do not count the aggregate as green or waive it. No workflow rerun/dispatch or `.github/**` edit was made.

**Landing stop criterion:** keep the external STATE attached to the owner-side 0427-172 resolution; after that resolution lands, refresh this PR onto current develop and require a new exact-head run with both native Keycloak/Core jobs and `PR Selected Checks` successful. Separately, require the healing regression above before acceptance. Do not merge while either condition is open.

## END

END_DONE 0427-165-r4-review: KORREKTUR — PR #1500 head `0bc028f13272a064c47db1e99d4fbb4da7e74fc3`; exact identity cases pass review, but actual app-destroy healing is not exercised; run `42550331883` has external 0427-172 native failures and failed `PR Selected Checks`; current develop drift requires refresh. Evidence publication SHA to follow.

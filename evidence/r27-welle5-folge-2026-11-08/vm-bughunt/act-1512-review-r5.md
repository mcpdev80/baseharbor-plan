# CODEX-REVIEW 0427-175 r5 — PR #1512

ROLLE: REVIEW

URTEIL: KORREKTUR

## PLAN

1. Verify live head, develop ancestry and exact terminal run.
2. Check each r4 requirement against the product call path, regression assertions and CI.
3. Record the exact-head verdict and actionable corrections.

## Exact candidate and hosted run

- PR #1512, branch `0427-175-initlock`, head `cbe322c88445e4f72694785ec4f5c522720838c3`.
- `develop` `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` is an ancestor; `develop...head` = `0 9`.
- Run 42629021041 is `completed/success` on the exact head. Branch-list entry is terminal success. `PR Selected Checks` and `go-unit-tests` passed; native/HA groups shown as skipped are not counted as passes.
- Lane evidence: `evidence/bughunt-concurrent-init-double-registration/round-5.md`.

## Point-by-point review against act-1512-review-r4

### 1. `--uuid` destroy resolution and identity chain — PARTIAL

The product route now parses `--uuid`, forwards it as an intact selector to `resolveApplicationEnvironment`, resolves the selected record, carries the `resolvedApplication` through preflight/authorization, and passes its `DeploymentIdentity` to `DeleteDeploymentRecord`. The resolution seams also check that the explicit selector resolved to the requested deployment.

However, the regression `TestRegistryConflictRepairCommandDeletesSelectedTwinOnly` does **not** invoke `appDestroyCommand` or `executeApplicationDestroyLifecycle`, and does not execute `authorizeApplicationDestruction`. It calls `newApplicationDestroyExecution` directly, then calls `runPreflight` and `removeApplicationState`. Thus it does not prove the advertised actual destroy CLI invocation preserves identity through the authorization step.

There is also a misplaced selector guard in `removeApplicationState`: its comparison of `e.selection` with `e.resolved.DeploymentIdentity.DeploymentID` occurs **after** `deployment.DeleteDeploymentRecord` has already removed the record directory. That check cannot prevent a wrong-identity deletion. `DeleteDeploymentRecord` does validate the on-disk record against the resolved identity before removal, but it does not compare that identity to the original CLI selector; the selector-specific check must precede destructive mutation.

### 2. Poisoned-registry twin-removal CLI regression — PARTIAL

The regression verifies the selected twin's `deployment.json` is absent, the other twin's record remains byte-identical, strict inventory is healthy, and display listing contains only the survivor. A registry-conflict error is explicitly a test failure.

The fixture writes the poisoned deployment records directly and does not seed a retained `.owner` band. The test also checks only that the selected `deployment.json` is absent; it does not assert removal of the selected deployment directory / retained band. So the requested band-removal proof is missing. The observed production `DeleteDeploymentRecord` currently calls `os.RemoveAll(root)`, but the regression would still pass if a future change left the selected `.owner` or other files behind.

### 3. Hard race regression — PASS

`TestConcurrentInitAcrossRealProcessesIsSerializedOrRefused` starts a distinct test-binary process. Its child emits a witness from inside the registry-claim hook; the parent requires a busy refusal, duplicate-claim convergence, or a persisted outcome followed by a final exact-one-claim registry check. No child output/no recognized seam outcome fails the test. The exact-head passing `go-unit-tests` job runs this regression through the package suite.

## Correction recipe and stop criteria

- Make the poisoned-registry regression invoke the actual destroy command entrypoint with `--uuid <id> --full-reset --yes`; exercise resolution, authorization, preflight and mutation in that path. Compare the selected id to the resolved/mutated record before any destructive cleanup. Move the selector-vs-resolved identity check ahead of `DeleteDeploymentRecord` and other state removal, then test a deliberate identity drift is refused without deleting either twin.
- Seed an explicit retained `.owner` marker (or equivalent band data) for both twins. After the command, assert the selected deployment directory and band are absent, the other twin and its band are byte-identical, and the registry is healthy.
- Keep the real-process seam witness and terminal exact-head CI coverage.
- Stop review when those CLI/auth and band-removal regressions pass on an exact terminal-success candidate.

## Repo-rule compliance

Product repository and GitHub were read-only. No tests, reruns, approvals or merges were performed.

Planning validation note: `python3 scripts/plan.py render && python3 scripts/plan.py check` completed rendering but check reports three existing errors in `decisions/2026-11-09-r27-local-delta-delivery-and-target-presets.md` (decision status and two issue-inventory references). No unrelated decision was changed; this review act is being published per the explicit review instruction.

## SOP raw witnesses

```text
$ git -C baseharbor ls-remote origin refs/pull/1512/head refs/heads/0427-175-initlock refs/heads/develop
cbe322c88445e4f72694785ec4f5c522720838c3	refs/heads/0427-175-initlock
fea92f379e55bbe6e143a095d7c2e6c16e0b3a06	refs/heads/develop
cbe322c88445e4f72694785ec4f5c522720838c3	refs/pull/1512/head

$ gh pr view 1512 --repo mcpdev80/baseharbor --json headRefName,headRefOid,state,baseRefName,url,mergeStateStatus
{"baseRefName":"develop","headRefName":"0427-175-initlock","headRefOid":"cbe322c88445e4f72694785ec4f5c522720838c3","mergeStateStatus":"CLEAN","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1512"}

$ gh run list --repo mcpdev80/baseharbor --branch 0427-175-initlock --limit 8
completed	success	CI · PR #1512	CI · Source & Quality	0427-175-initlock	pull_request	42629021041	11m0s	2026-11-09T13:50:35Z

$ gh run view 42629021041 --repo mcpdev80/baseharbor --json headSha,status,conclusion,url
{"conclusion":"success","headSha":"cbe322c88445e4f72694785ec4f5c522720838c3","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/42629021041"}
```

END_DONE 0427-175-r5-review: KORREKTUR PR #1512 cbe322c88; the race regression is hard and CI-covered, but the poisoned-recovery regression bypasses the actual CLI/authorization path and does not prove retained-band removal; the selector guard is after deletion.

# CODEX-REVIEW 0427-159 r10 — PR #1499

ROLLE: REVIEW

URTEIL: APPROVE

## PLAN

1. Verify the live PR head and terminal CI run.
2. Inspect the r10 production changes against all three r9 correction criteria.
3. Record the verdict and raw remote evidence.

## Exact candidate and run

- PR #1499, branch `0427-159-damagedstate`, live head `d69d3c0b98af287b172b5b027d24112ef903c81e`.
- Run 42619991654 is `completed/success` on that exact SHA. `PR Selected Checks`, `go-unit-tests`, `deployment-package-tests`, build, vet, and applicable selected checks succeeded; hosted package output includes `cmd/baha` and `internal/deployment`.
- Round-10 evidence: `evidence/bughunt-damaged-state-misleading-error/round-10.md`.

## r9 recipe results

1. **Band-write error propagates: PASS.** `SaveDeploymentRecord` returns a wrapped error from `writeRetainedOwnerBand`; it no longer returns `nil` when that write fails. `TestSaveDeploymentRecordPropagatesBandWriteError` injects a failing band destination and asserts the production save returns an error. The persisted deployment record does not turn the failed save into success.
2. **Canonical identity in the band and checked by reader: PASS.** The production writer stores `ApplicationID`, application name, and environment. `LoadRetainedOwnerBand` returns all three and rejects incomplete data. `damagedScopedBandGate` requires exact equality for all three before attributing requested identity or network.
3. **Same-name/environment, different-ID production regression: PASS.** The lifecycle regression creates a sibling deployment with the same name and environment but a distinct canonical `ApplicationID`, writes its band via `SaveDeploymentRecord`, removes its record to simulate damage, and resolves the requested app. The assertion requires unknown-owner identity and no requested-app network attribution.

The named regressions are included in the exact-head green `go-unit-tests` package execution. No blocking defect against the r9 recipe remains. A stale comment above the new propagated-error branch still describes band writing as best-effort; it does not match runtime behavior and should be corrected in a later scoped cleanup, but does not invalidate these three acceptance criteria.

## Repo-rule compliance

Product code and GitHub were read-only. No tests or CI runs were started, and no GitHub approval or merge was performed. Review is limited to the exact SHA above.

## SOP raw witnesses

```text
$ git -C baseharbor ls-remote origin refs/pull/1499/head refs/heads/0427-159-damagedstate refs/heads/develop
d69d3c0b98af287b172b5b027d24112ef903c81e	refs/heads/0427-159-damagedstate
fea92f379e55bbe6e143a095d7c2e6c16e0b3a06	refs/heads/develop
d69d3c0b98af287b172b5b027d24112ef903c81e	refs/pull/1499/head

$ gh pr view 1499 --repo mcpdev80/baseharbor --json headRefName,headRefOid,state,baseRefName,url,mergeStateStatus
{"baseRefName":"develop","headRefName":"0427-159-damagedstate","headRefOid":"d69d3c0b98af287b172b5b027d24112ef903c81e","mergeStateStatus":"CLEAN","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1499"}

$ gh run view 42619991654 --repo mcpdev80/baseharbor --json headSha,status,conclusion,url
{"conclusion":"success","headSha":"d69d3c0b98af287b172b5b027d24112ef903c81e","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/42619991654"}
```

END_DONE 0427-159-r10-review: APPROVE PR #1499 at d69d3c0b98af287b172b5b027d24112ef903c81e; all three r9 trust-placement criteria pass and exact-head run 42619991654 is completed/success.

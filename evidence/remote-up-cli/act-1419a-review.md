# CODEX-REVIEW 0427-117 / PR #1419

## PLAN

1. Confirm planning repository identity and read its review/evidence rules.
2. Fetch authoritative PR/base refs and inspect the exact candidate diff and provenance.
3. Verify red-first regression evidence, manual Podman reproduction, and terminal CI run against the card contract.
4. Write SHA-specific review verdict and actionable recipe to planning evidence; publish evidence on origin/main.
5. Post the required END verdict to coordinator with candidate SHA.


## Review identity and candidate

- Role: CODEX-REVIEW; read-only review; no merge or workflow action performed.
- Planning repository identity command output, verified before the evidence commit:
  `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`
- Planning repository origin: `https://github.com/mcpdev80/baseharbor-plan.git`; authenticated GitHub user: `mcpdev80`.
- Required product remote witness:
  `934be499b9d2d894f80889fc23cd811884c8aec4 refs/heads/develop`
  `8b5075d2554871ac58dd905c86d27a4bfdf798fc refs/pull/1419/head`
- PR #1419 is OPEN, base `develop`, head `8b5075d2554871ac58dd905c86d27a4bfdf798fc`, not draft, MERGEABLE. Fetched remote base/head matched those exact SHAs; base is an ancestor of head (`merge-base --is-ancestor` exit 0).
- `git log --format='%H %an <%ae> %s' develop..PR-head` lists six commits, all authored by Worker w280: `14ec6674`, `5c2c7106`, `c5cacec5`, `801fdbc7`, `9ffc036e`, `8b5075d2`. No foreign candidate commit is present. `git diff --check` is clean.
- Diff from base to head: six files, 859 insertions and 27 deletions. It adds the regression/fixture/helper files and changes `cmd/baha/deployment_record.go`, `internal/deployment/deployment_store.go`; no `.github/**` changes.

## Contract evidence

- Card `t-20261106-r27-remote-up-podman-owner-missing` requires the same Podman scenario to pass (`up` -> doctor health OK) with an owner record present and resolvable, plus root cause and red-first regression evidence.
- The on-main `evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-2.md` provides a behavioral RED/GREEN witness for `TestOwnerLoanRegressionIsolatedTestTargetPassesSeam`: the unbound loan verifier yields `ErrDeploymentOwnerMissing`, and the test-scoped loan makes that seam pass. The test is included in `cli-package-tests` (`go test ./cmd/baha`, run 42336410875); this is durable unit CI evidence for that test.
- The same evidence's named-host Podman reproduction does not pass the card scenario. On `baha-podman-2`, a fresh Podman target reaches `baha app apply` and returns `ErrDeploymentOwnerMissing` at `cmd/baha/deployment_record.go:87` -> `internal/deployment/deployment_store.go:107`. The evidence explicitly says the live path stays fail-closed and calls the connector-bound operator-bootstrap path out of scope. It does not show `up` -> doctor health OK or a resolvable owner record.
- Candidate implementation narrows the grant to test provenance: `cmd/baha/deployment_record.go:57-65` binds a TEST-SCOPE verifier; `:137-145` requires a Go test process and refuses startup-bound non-local management authority. The regression at `cmd/baha/deployment_owner_loan_regression_test.go:187-221` exercises `VerifyDeploymentOwner`/`SaveDeploymentRecord` with a synthetic isolated local test Target, not the card's remote Podman CLI flow. Thus the red-first regression is real but does not establish this card's acceptance behavior.
- CI run 42336410875 is terminal SUCCESS for head `8b5075d2554871ac58dd905c86d27a4bfdf798fc` (event `pull_request`). `PR Selected Checks`, `PR · Source format`, `PR · Validation · cli-build`, `cli-gofmt`, `cli-package-tests`, `cli-vet`, `deployment-package-tests`, and `source-contracts` succeeded. `Targeted HA · docker`, `Targeted HA · podman`, and `PR · Selected Runtime` were SKIPPED under the workflow's designated-ref owner gate. No rerun or workflow_dispatch was issued.
- Planning task state says prerequisite `t-20261106-r27-remote-up-cli-path` is NOT accepted; this remains a Planning dependency gap for card closure.

## Verdict and actionable recipe

**verdict=REJECT_LANE_FIX** for the task contract, not because the owner-gated CI cells were skipped. The recorded manual Podman execution itself still fails the required behavior, so the skipped cells are not the only remaining gap and the evidence does not justify ACCEPT.

Recipe: in `cmd/baha/deployment_record.go:57-65` and `:137-145`, implement owner resolution for the actual authorized remote Podman deployment path instead of granting only marker-proven Go test targets and refusing startup-bound management authority. Preserve fail-closed behavior for unauthorized, tenant, foreign, or unowned targets. Extend the regression to invoke the same remote `baha app up` path and assert the resulting owner record is present/resolvable and `doctor` reports healthy; require the new test to run in GitHub CI, and rerun the named `baha-podman-2` smoke cell until the card's `up` -> doctor health OK acceptance passes. `.github/**` is Owner scope; if CI wiring is needed, report the exact workflow change to the Owner rather than editing or dispatching it.

## Evidence repository witness

The exact pre-push remote-main witness captured for this evidence was:

```text
488f27f640fe5e20f46bb7eee44efbcb0a44f4e1	refs/heads/main
```

## END

END_DONE codex-1419-review-a: verdict=REJECT_LANE_FIX head=8b5075d2554871ac58dd905c86d27a4bfdf798fc redfirst=unit-seam-only ci=42336410875 terminal-success runtime_cells=skipped-owner-gate plus named-host acceptance still fails; recipe=make authorized remote Podman owner resolution pass and prove up-to-doctor health with CI regression

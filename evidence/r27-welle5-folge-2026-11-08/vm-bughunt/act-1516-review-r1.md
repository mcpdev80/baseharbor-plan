# CODEX-REVIEW 0427-181 r1 — PR #1516

ROLLE: REVIEW

URTEIL: APPROVE

## PLAN

1. Verify the live PR head, branch run, exact SHA and develop ancestry.
2. Review the test's contamination source, isolation, trust-plane lifecycle and full-package CI evidence.
3. Publish the exact-head verdict and raw witnesses.

## Exact candidate and hosted run

- PR #1516, branch `w286-0427-181-upname-hosted`, head `07fe960f6730f04a0aac11cdd7ad6559bab09d2f`.
- Develop `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` is an ancestor; `develop...head` = `0 1`.
- Branch run 42640378393 is terminal `completed/success` on the exact head.
- `PR · Validation · cli-package-tests` succeeded. In the workflow/check runner this executes the whole `./cmd/baha` package suite (not only a `-run` selection). Round-1 evidence reports `TestUpNameResumesThroughCommandEntrypoint` passed in that full run, with 46 PASS and 0 FAIL. The first hosted candidate run failed; this verdict uses only the corrected exact head and its later green run.

## Review criteria

1. **Contamination source and isolation — PASS.** The initial failure was not merely an assertion mismatch: from an empty temporary CWD, top-level `up NAME` entered fresh-Core bootstrap and could bring up a Core, so the prior “must fail before realization” assertion depended on the host having no Docker daemon. The candidate changes the test to run from its authored repository root, so the registered `up NAME` exercises the intended repository/registered-deployment path and fails at runtime realization when this isolated Target has no running Core. It does not weaken or move the assertion.

   `configureIsolatedTestTarget` gives the test a fresh XDG config/data root, unique Target/project/network, and clears inherited `BASEHARBOR_TARGET`, `BASEHARBOR_STATE_DIR`, and `BASEHARBOR_ENV` before resolving the Target. There is no dedicated port reservation in the fixture; the corrected repository path does not enter Core bootstrap or start the workload, so this cell does not bind a service/Core port. Its per-test Target prevents reuse of another test's Core/network. The package-level trust-plane marker remains owned by `TestMain`; the full package run succeeds, and the `t.Setenv` values are restored before package teardown. No new retained marker path is introduced by this fixture.

2. **Full-matrix test, not isolated-only — PASS.** The exact-head `cli-package-tests` job is the complete `go test ./cmd/baha` suite. Round-1 evidence records the named test passing in that suite, not only in a focused invocation. The `Release Source Preflight` job is skipped in this PR event, but that does not change the executed full `cli-package-tests` result.

3. **Other package tests — PASS.** The same complete package run reports 46 PASS / 0 FAIL in the round-1 evidence. The production code is untouched; only the target fixture and the intended command-entrypoint test changed.

4. **Develop ancestry — PASS.** Develop SHA `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` is an ancestor of the candidate.

No blocking finding remains against this review request. This review verdict does not perform GitHub approval or merge.

## Repo-rule compliance

Product repository and GitHub were read-only. No tests, reruns, approvals or merges were performed. Review used the fetched exact PR head and the recorded hosted result.

Planning validation note: `python3 scripts/plan.py render && python3 scripts/plan.py check` completed rendering but check reports three existing errors in `decisions/2026-11-09-r27-local-delta-delivery-and-target-presets.md` (invalid decision status and two issue-inventory references). No unrelated decision was changed; this act is published as explicitly requested.

## SOP raw witnesses

```text
$ git -C baseharbor ls-remote origin refs/pull/1516/head refs/heads/develop
fea92f379e55bbe6e143a095d7c2e6c16e0b3a06	refs/heads/develop
07fe960f6730f04a0aac11cdd7ad6559bab09d2f	refs/pull/1516/head

$ gh pr view 1516 --repo mcpdev80/baseharbor --json headRefName,headRefOid,state,baseRefName,url,mergeStateStatus
{"baseRefName":"develop","headRefName":"w286-0427-181-upname-hosted","headRefOid":"07fe960f6730f04a0aac11cdd7ad6559bab09d2f","mergeStateStatus":"CLEAN","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1516"}

$ gh run list --repo mcpdev80/baseharbor --branch w286-0427-181-upname-hosted --limit 8
completed	success	CI · PR #1516	CI · Source & Quality	w286-0427-181-upname-hosted	pull_request	42640378393	7m33s	2026-11-09T15:01:14Z

$ gh run view 42640378393 --repo mcpdev80/baseharbor --json headSha,status,conclusion,url
{"conclusion":"success","headSha":"07fe960f6730f04a0aac11cdd7ad6559bab09d2f","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/42640378393"}

$ gh api repos/mcpdev80/baseharbor/actions/jobs/129239700413 --jq '{name,status,conclusion}'
{"conclusion":"success","name":"PR · Validation · cli-package-tests","status":"completed"}
```

END_DONE 0427-181-r1-review: APPROVE PR #1516 at 07fe960f6; the CWD bootstrap source is fixed, the full cmd/baha package passed including TestUpNameResumesThroughCommandEntrypoint, isolation/base criteria pass, and run 42640378393 is terminal success.

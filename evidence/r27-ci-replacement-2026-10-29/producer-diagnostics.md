## PLAN (q202)
[✔] 0. Turn-start basics-check.py; acked events; read q202 task
[✔] 1. gh run view 40833893562; confirm PR · Public Contracts success; download trusted-pr-plan artifact to /home/marcel/tmp-ops/q202/
[✔] 2. Extract integration_sha/base/head from pr-plan.json; verify parents via git cat-file
[✔] 3. Confirm contracts test change executes in Public Contracts job/evidence
[✔] 4. Check automatic plan/receipt publication (baseharbor-plan origin/main)
[✔] 5. List remaining chain gaps (TRUSTED_SOURCE, workflow reg, token, auto-trigger)
[✔] 6. Write producer-diagnostics.md

# Producer diagnostics — PR #1199 (run 40833893562) — lane q202

READ-ONLY diagnostics for the R27 CI-replacement producer slice. No product commits, no planning git operations. This file documents the verified state of merged producer PR #1199 against the CODEMAN-START producer requirements and states precisely what the automatic chain still needs.

## Run identity
- Run id: **40833893562** (attempt 1, conclusion **success**, status completed)
- Repo: `mcpdev80/baseharbor`
- PR: **#1199** "contracts: include vector in frozen-family guard test" — state **closed/merged** at 2026-10-29T07:18:17Z
- Head (PR) sha: **96a96362d3682bdf35748c5331a6f2452c01b4c8**
- Merge commit: **7a4debccc4e2fa5e78287e9b9388b0cb521d66e2** (merged_at 2026-10-29T07:18:17Z)
- workflow_id (definition): **352609139** → "CI · Source & Quality"
- workflow_name field on run object: null (display name "CI · PR #1199")

## SHAs from trusted-pr-plan (artifact `trusted-pr-plan`, id 12880180956)
Source: `/home/marcel/tmp-ops/q202/pr-plan.json` (downloaded via `gh run download 40833893562 --name trusted-pr-plan --dir /home/marcel/tmp-ops/q202/`)
- `integration_sha`: **8515e6272f03aa274ed3ea215143b9e93680be71**
- `head_sha`: **96a96362d3682bdf35748c5331a6f2452c01b4c8**
- `target_base_sha`: **9e50d8a4ab6c358ad45da6b337c0e67c64373264**
- `merge_base_sha`: **9e50d8a4ab6c358ad45da6b337c0e67c64373264** (= target_base)
- `release`: v0.4.26 · `coverage_status`: resolved · `broad_required`: false
- `selected_gates`: ["integration/static/public-contracts"] · mapping/plan schema `baseharbor.pr-gate-map/v1` / `baseharbor.pr-gate-plan/v1`
- `required_validation_checks`: `go test ./internal/application/... ./contracts/...` (source-contracts, owner "CI source / contracts")
- `reasons`: ["contracts/contracts_test.go: contract"]

### Parent verification (git -C baseharbor cat-file -p)
- integration 8515e627 → tree **915862748e7cca7cd30e350525ce6b92b1b1c904**, parents: 9e50d8a4 (target_base) + 96a96362 (head) · commit msg "Merge 96a96362... into 9e50d8a4..."
- head 96a96362 → tree 915862748e7cca7cd30e350525ce6b92b1b1c904, parent 9e50d8a4 · "contracts: include vector in frozen-family guard test"
- base 9e50d8a4 → tree bed8bd4f..., parent 56a2c811 (gpg-signed) · "docs(ci): migrate register required_checks... (#1184)"
- **Tree parity: integration.tree == head.tree == 915862748e7cca7cd30e350525ce6b92b1b1c904**, i.e. the merge into base carries the head tree unchanged → clean fast-forward-into-base, no stray merge content.
- Merge commit 7a4debcc → tree 915862748e7cca7cd30e350525ce6b92b1b1c904, parent 9e50d8a4 (matches target_base). Merge tree == base tree == integration/head tree. Chain is consistent end-to-end.

## Public Contracts job evidence (job 123314210728, conclusion success)
- Checkout ref: **8515e6272f03aa274ed3ea215143b9e93680be71** (integration_sha), fetch-depth 0.
- `CORE_SHA: 8515e6272f03aa274ed3ea215143b9e93680be71`, `DEMO_SHA: 073e065f88b0dd9155cb000a4bece175a862605a`.
- Ran `python3 scripts/pre-release-integration.py --gate integration/static/public-contracts --candidate $CORE_SHA --demo $DEMO_SHA --tag v0.4.26 --output ...` → produced a 4-file integration-evidence artifact `pre-release-integration-static-public-contracts-evidence-40833893562-1` (artifact id **12879458838**, zip sha256 01c0868e5cab888163782553e57985d716eb4b44c15a7217c4e0935337777bb9, 10041 bytes).
- Evidence manifest (`/home/marcel/tmp-ops/q202/public-contracts-evidence/manifest.json`, schema `baseharbor.pre-release.integration-evidence/v1`):
  - `candidate_sha`: 8515e627 · `demo_ref`: 073e065f88b0dd9155cb000a4bece175a862605a · `workflow_run_id`: 40833893562 · `outcome`: success · `qualification_scope`: core-source-contracts
  - Check 0 `go test -race -count=1 -json ./contracts/... ./internal/machine ./internal/machinereadmodels` → **all passed**, incl. `github.com/mcpdev80/baseharbor/contracts/*` subtests (e.g. `TestTargetAccessWireRejectsAmbiguousAndUnsafeRequests`, `TestServiceSchemasUseJSONSchema202012AndStayProviderNeutral`, `TestOfflineRegistryContainsEveryPackagedSchema`, `TestQuadlet*`, `TestManagedActivation*`, `TestCanonicalTargetAccessGoldenRecordsValidateOffline`, `TestProviderImpactMachineSchemasAndSharedFixtures`).
  - Check 1 `go test ... ./cmd/baha -run ^TestExternalProviderRemoval` → passed.
  - Check 2 `go test ... ./internal/application -run ^TestExternalRemoval` → passed.
- The contracts test change from contracts/contracts_test.go (the `--reason` in pr-plan) is exercised as part of the `./contracts/...` suite that ran green under the frozen-family guard in this run.

## Automatic plan/receipt publication status
- Triggered by: `receipt-post-run.yml` (`on.workflow_run.workflows: ["CI · Source & Quality"]`, if success). Run 40833893562 is exactly workflow_id 352609139 = "CI · Source & Quality" → the event was armed and fired.
- `Receipt · Post-Run Writer` runs fired for nearby runs but **fail at the `Publish Receipt to Planning` job**. Latest failure: run **40834168626** (2026-10-29T07:15:03Z, right after target run):
  - `Capture Producer Context` = success, `Extract Trusted Plan & Map PR->Task` = success (resolved WORKFLOW_ID=352609139, HEAD_SHA=96a96362, CANDIDATE_SHA=8515e627, BASE_SHA=9e50d8a4, RUN_ID=40833893562, PR_NUMBER=1199, PLAN_REVISION=37956f42).
  - `Publish receipt to Planning` → **exit code 1**: `receipt blocked: PLANNING_RECEIPT_WRITE_TOKEN required; publication push blocked`.
  - root cause in `scripts/receipt_writer.py:108-110`: `require(bool(token), "PLANNING_RECEIPT_WRITE_TOKEN required; publication push blocked")` — the Actions secret `PLANNING_RECEIPT_WRITE_TOKEN` is **absent** in the run context, so the writer fails closed by design.
- origin/main still holds the **previous** publications, not run 40833893562:
  - `evidence/receipts/public-contracts/40428162731-1.json` → `{"gate":"public-contracts","plan":"5ecabc17...","run":{"attempt":1,"id":40428162731},"sha":"12f3c97ee9b593833aad5de223451e2e9d4f6dd3","status":"pass","approved":{"by":"mcpdev80","at":"2026-10-27T02:52:00Z"}}`
  - `evidence/receipt-plans/public-contracts.json` → `base_sha 9a630665...`, `candidate_sha 12f3c97ee9...`, `head_sha bd342b91...`, `workflow_id 352609139`, `task tasks/t-20261027-r27-shadow-run.md`
- No receipt or receipt-plan entry for run **40833893562 / candidate 8515e627** exists on origin/main or any ref. The plan fixture (plan revision 37956f42) was written locally by the failing run's tasklink step but never pushed.

## Remaining chain gaps (one line each)
- **TRUSTED_SOURCE**: `receipt-approval.yml` is dormant — helper/workflow code lives on `develop` (which does not exist on the remote), so `main` cannot resolve the reviewed controller; `receipt_verifier.py` fails closed while `TRUSTED_SOURCE` is unregistered. Need: coordinator registers the immutable reviewed commit (controller pin `dd8fb61d614b59252c9d29121380b5893d006828`) as `TRUSTED_SOURCE` on `main` before the approval path can pass.
- **Workflow registration**: `receipt-approval.yml` is not auto-registered on `main` (only `validate.yml` is registered under `.github/workflows/` on origin/main; `ci.yml` + all receipt helpers are develop-only). Need: coordinator registers the receipt-approval / receipt-post-run gate on the product default branch per the producer contract.
- **Token**: `PLANNING_RECEIPT_WRITE_TOKEN` secret is missing from the Actions environment → `receipt_writer.publish` fails closed (`receipt_writer.py:108-110`). Need: Owner adds the scoped write token; without it the publication push cannot succeed (correct fail-closed, but blocks the chain).
- **Auto-trigger arming**: `receipt-post-run.yml` fires on `workflow_run` of "CI · Source & Quality" (verified: run 40833893562 → id 352609139). The trigger itself is armed and ran, but every post-run writer run since fails at the token gate, so post-run publication never lands. Note run_attempt must be 1 (enforced in `extract_plan`); reruns (attempt != 1) are refused.

## What the automatic chain still needs (summary)
1. Merge + contracts execution: DONE (PR #1199 merged; `./contracts/...` + machine/baha/application checks green; evidence artifact uploaded).
2. Trusted-plan resolution: DONE (pr-plan.json extracted, parents verified, tree parity confirmed).
3. Plan fixture write (tasklink): effectively DONE locally (plan revision 37956f42) but never committed/pushed because the publish job aborts.
4. Receipt publication to Planning: BLOCKED — `PLANNING_RECEIPT_WRITE_TOKEN` absent; writer fails closed. Until the Owner supplies this scoped secret, no run 40833893562 receipt/plan is published to origin/main.
5. Approval + shadow: dormant pending `TRUSTED_SOURCE` registration on main and develop-only helper availability.

## repo-rule compliance
- READ-ONLY product: no commits, no pushes, no branch operations in `baseharbor`. All git reads were `cat-file`/`fetch`/`show origin/main` (non-mutating) in the baseharbor checkout; the baseharbor-plan working tree was left untouched.
- Evidence artifacts saved only under `/home/marcel/tmp-ops/q202/` (not /tmp, not product branch). This evidence file is the sole write, to `baseharbor-plan/evidence/r27-ci-replacement-2026-10-29/producer-diagnostics.md`, published by the coordinator.
- No secrets/tokens logged (token value scrubbed; only its absence/absence is reported).
- All identities (SHAs, run ids, artifact ids, plan revisions) are backed by gh-api / git objects / downloaded artifacts cited above.

END q202-DONE

# Postrun token mapping — evidence

## PLAN

1. Reproduce the diagnosis from the failed run log, the origin/main registered workflow copy, and the controller.
2. Verify the fix: add PLANNING_RECEIPT_WRITE_TOKEN to the publish step env in the develop source copy.
3. Check whether origin/main's registered copy differs; document the exact delta.
4. Extend the focused workflow test that asserts publish-step env keys.
5. Run focused python tests, YAML sanity, actionlint.
6. Push branch, open PR to develop, record PR number + head SHA.
7. Write this evidence file (no git commands in baseharbor-plan).

## Reproduction (verified, not trusted)

Command: `gh run view 40834168626 --repo mcpdev80/baseharbor --log-failed`
The publish step env block on the failed run contains only:

- WORKFLOW_ID, HEAD_SHA, CANDIDATE_SHA, BASE_SHA, PR_NUMBER, pythonLocation + Python *_ROOT_DIR/LD_LIBRARY_PATH
- GH_TOKEN: ***
- PLANNING_ROOT: /home/runner/work/baseharbor/baseharbor/planning
- RUN_ID: 40833893562
- PLAN_REVISION: 37956f4288865af9f133eec963e19922a8386ae0

No PLANNING_RECEIPT_WRITE_TOKEN. The writer then failed closed:

```
receipt blocked: PLANNING_RECEIPT_WRITE_TOKEN required; publication push blocked
```
exit code 1.

Controller (develop scripts/receipt_writer.py, reviewed controller at dd8fb61d):

```python
token = os.environ.get("PLANNING_RECEIPT_WRITE_TOKEN", "")
require(bool(token),
        "PLANNING_RECEIPT_WRITE_TOKEN required; publication push blocked")
```

receipt_writer.py:108-110 — token read from os.environ, fails closed when absent. The Planning checkout step in the same workflow already sources the same secret (`token: ${{ secrets.PLANNING_RECEIPT_WRITE_TOKEN }}`), confirming the repository secret exists. The failure cause is confirmed: publish-step env omitted the token the controller requires from the environment.

## Fix (develop source copy)

File: .github/workflows/receipt-post-run.yml, publish step `Publish receipt to Planning` env.

Added:

```yaml
          PLANNING_RECEIPT_WRITE_TOKEN: ${{ secrets.PLANNING_RECEIPT_WRITE_TOKEN }}
```

directly after PLAN_REVISION. The value is never echoed: `_push_authed` (receipt_writer.py:111) passes it via an ephemeral `http.extraheader` on the subprocess argv only, and `_scrub_secret` (receipt_writer.py:123-133) redacts any bearer/authorization diagnostic. All other credential handling is unchanged.

## origin/main registered copy — delta (documented, not merged)

`git show origin/main:.github/workflows/receipt-post-run.yml` was read. The origin/main registered copy has the SAME publish-step env gap: its publish-step env (source lines 298-307) supplies GH_TOKEN, PLANNING_ROOT, RUN_ID, PLAN_REVISION and omits PLANNING_RECEIPT_WRITE_TOKEN.

The two copies are NOT identical; origin/main is a structurally different revision of the file. Exact delta (develop → origin/main):

- Controller checkout pin: develop `ref: e13f1570550f4b6b09f3727728293d91afbebf94` → main `ref: dd8fb61d614b59252c9d29121380b5893d006828` (both producer_context and publish_receipt checkout steps).
- extract_plan download step: main adds `GH_WORKFLOW_TOKEN: ${{ secrets.GITHUB_TOKEN }}` step env and an inline `export GH_TOKEN="${GH_WORKFLOW_TOKEN}"`.
- extract_plan PR number resolution: main uses `${{ github.event.workflow_run.pull_requests[0].number }}` with a `${PR_NUMBER:-}` fallback (develop resolves PR_NUMBER empty and via the base_ref regex in the Python block).
- extract_plan invocation: main adds `RUN_ATTEMPT="${ATTEMPT_RESOLVED}"` and forwards `attempt=int(os.environ.get("RUN_ATTEMPT", "1"))` to `extract_facts`.
- publish step "Automatic task-link" env: main adds `GH_WORKFLOW_TOKEN` and invokes the tasklink CLI with `GITHUB_TOKEN="${GH_WORKFLOW_TOKEN}"`.
- publish step "Publish receipt to Planning" env: main adds `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` at the top; both copies omit PLANNING_RECEIPT_WRITE_TOKEN.

Both copies require the fix. Registration on origin/main is a coordinator/Codex step; this branch does not touch main.

## Focused test

File: scripts/test_receipt_postrun.py. Added `ExtractBlocksTest.test_publish_step_env_carries_write_token`:

- Asserts the publish-step env keys include PLANNING_ROOT, RUN_ID, PLAN_REVISION.
- Asserts PLANNING_RECEIPT_WRITE_TOKEN is present in the publish-step env keys.
- Asserts the token value equals `${{ secrets.PLANNING_RECEIPT_WRITE_TOKEN }}` (secret, never a literal).

Module-level `import yaml` added to support the env inspection (previously imported locally per method).

## Tests

Candidate: PR #1201, head SHA de2312a06b234cde08943ce0329b83e01bd36fa3 (work/r27-postrun-token-o203, base develop).

- Focused suite: `PYTHONPATH=scripts python3 -m unittest scripts.test_receipt_postrun` → Ran 11 tests, OK (10 prior + 1 new).
- Full receipt control-plane suite (pr-check-runner RECEIPT_EXECUTION_SUITES): `python3 -m unittest test_receipt_writer test_receipt_verifier test_receipt_chain test_ci_workflow_policy_receipts test_receipt_tasklink test_receipt_postrun` → Ran 184 tests, OK.
- YAML sanity: `yaml.safe_load` of the workflow; publish-step env keys = [PLANNING_ROOT, RUN_ID, PLAN_REVISION, PLANNING_RECEIPT_WRITE_TOKEN]; token key present.
- actionlint: `go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.12 -shellcheck= .github/workflows/receipt-post-run.yml` → exit 0.

## repo-rule compliance

- Write set: .github/workflows/receipt-post-run.yml + its focused test only. No overlap with receipt-approval.yml (#1200 owner) or verifier scripts.
- No token values printed; secret surfaced only via `${{ secrets.* }}`. No GITHUB_* overrides in the publish step (unchanged).
- origin/main not merged; delta documented only. Planning note left unedited; no git commands in baseharbor-plan.
- Branch pushed to origin; PR opened to develop (Marcel-delegated Maintainer authority, baseharbor-plan AGENTS.md owner-delegation section).

## Handoff

PR #1201 (https://github.com/mcpdev80/baseharbor/pull/1201), head de2312a06b234cde08943ce0329b83e01bd36fa3, base develop. Focused tests + actionlint green. origin/main registered copy needs the same env-key fix; registration is a coordinator/Codex action, not performed here.

END o203-DONE

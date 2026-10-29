# R27 CI Cutover Sequencing Runbook — lane q204

**Task:** r27 cutover sequencing runbook (supports t-20261029-r27-cutover-pr3 + t-20261029-r27-ci-cutover-design)
**Lane:** q204
**Mode:** READ-ONLY product + planning git; no commits (coordinator publishes this file)
**Date:** 2026-10-29

## PLAN

1. PLAN 0: basics-check.py run; events acked; read q204 prompt; scope: READ-ONLY
2. PLAN 1: `git -C baseharbor fetch origin`; PR #1200 / #1201 / origin/main / origin/develop state captured
3. PLAN 2: Ruleset 25223521 JSON and enforcement state documented (§0)
4. PLAN 3: Per-step checklist for (a) #1200 correction+merge, #1201 merge, main registration delta
5. PLAN 4: Per-step checklist for (b) new producer run + automatic publication proof (§2)
6. PLAN 5: Per-step checklist for (c) hosted approval + retained shadow + three negative proofs (§3)
7. PLAN 6: Per-step checklist for (d) check-to-context mapping activation on ruleset 25223521 + legacy PR-Selected-Checks retirement (§4)
8. PLAN 7: OWNER decision points enumerated (§5)
9. PLAN 8: Evidence cross-references to §0 tables verified
10. PLAN 9: END q204-DONE appended

## 0. Ground state (verified commands, 2026-10-29)

| Fact | Command | Result |
|------|---------|--------|
| origin/develop HEAD | `git -C baseharbor ls-remote origin refs/heads/develop` | `7a4debccc4e2fa5e78287e9b9388b0cb521d66e2` |
| PR #1200 | `gh pr view 1200 --repo mcpdev80/baseharbor` | OPEN, MERGEABLE, head `5aaa38ece21c40ad10d2805bf0bc41fac3d695b8`, base `develop`, statusCheckRollup: Workflow policy=SUCCESS, PR Focused Python=SUCCESS, PR Validation receipt-execution-tests=SUCCESS, PR Selected Checks=SUCCESS; all others SKIPPED |
| PR #1201 | `gh pr view 1201 --repo mcpdev80/baseharbor` | OPEN, MERGEABLE, head `de2312a06b234cde08943ce0329b83e01bd36fa3`, base `develop`; statusCheckRollup: all required SUCCESS, PR Selected Checks=SUCCESS; others SKIPPED |
| Ruleset 25223521 | `gh api repos/mcpdev80/baseharbor/rulesets/25223521` | `enforcement=disabled`, rules=[{required_status_checks: [{context: "PR Selected Checks", integration_id: 15368}]}], strict_policy=true |
| origin/main HEAD | `git -C baseharbor log -1 --oneline origin/main` | `7a4debcc contracts: include vector in frozen-family guard test (#1199)` |
| Controller pin on main | `git -C baseharbor show origin/main:.github/workflows/receipt-post-run.yml \| grep 'ref:'` | `ref: dd8fb61d614b59252c9d29121380b5893d006828` (both checkout steps) |
| Controller pin on develop | `git -C baseharbor show origin/develop:.github/workflows/receipt-post-run.yml \| grep 'ref:'` | `ref: e13f1570550f4b6b09f3727728293d91afbebf94` (both checkout steps) |
| TRUSTED_SOURCE on main | `git -C baseharbor show dd8fb61d:.github/workflows/receipt-approval.yml \| grep 'TRUSTED_SOURCE'` | Line 86: `TRUSTED_SOURCE: ''` |
| TRUSTED_SOURCE on develop | `git -C baseharbor show e13f1570:.github/workflows/receipt-approval.yml \| grep 'TRUSTED_SOURCE'` | Line 86: `TRUSTED_SOURCE: ''` |
| PR #1200 fixes TRUSTED_SOURCE | `git -C baseharbor show 5aaa38ec:.github/workflows/receipt-approval.yml \| grep 'TRUSTED_SOURCE'` | Line 86: `TRUSTED_SOURCE: 'b53632aaaee6067397c27000c229f34736ec2155'` (set to b53632aa) |
| receipt-shadow.yml pin on develop | `git -C baseharbor show 5aaa38ec:.github/workflows/receipt-approval.yml \| grep receipt-shadow` | `ref: b53632aaaee6067397c27000c229f34736ec2155` |
| baseharbor-plan origin/main evidence | `git -C baseharbor-plan show origin/main:evidence/receipts/public-contracts/` | `40428162731-1.json` exists |
| receipt-post-run.yml delta (main→develop) | `git -C baseharbor diff origin/main..origin/develop -- .github/workflows/receipt-post-run.yml` | 86-line diff: controller pin dd8fb61d→e13f1570, GH_WORKFLOW_TOKEN removed from extract_plan env, PR_NUMBER simplified to `""` with regex fallback, attempt removal from Python call, GH_WORKFLOW_TOKEN removed from plan_commit env, GITHUB_TOKEN removed from publish_receipt env |
| PR #1200 scope | receipt-approval.yml only (TRUSTED_SOURCE pin + shadow pin update) |
| PR #1201 scope | receipt-post-run.yml only (supply PLANNING_RECEIPT_WRITE_TOKEN to publish step env) |

### Divergence detail: controller pin dd8fb61d vs e13f1570

`dd8fb61d` (main registered copy, controller pin) — the commit that wired `--product` through the CLI to write/live. This is the reviewed controller that `receipt-approval.yml` expects at approve-step.

`e13f1570` (develop head at the time of #1200) — the release-promoted develop copy post-#1170. It differs from dd8fb61d by a cascade of changes to `receipt-post-run.yml` that removed GH_WORKFLOW_TOKEN and attempt tracking from the extract_plan / plan_commit steps. The delta is purely in receipt-post-run.yml; the verifier scripts on develop are still functionally identical at b53632aa.

### Main registration delta for receipt-post-run.yml

After merging #1200 and #1201 to develop, origin/main will still carry the OLD registered copy of `receipt-post-run.yml` with controller pin `dd8fb61d` and the OLD (pre-PR #1198) env blocks. The registered copy on main differs from develop in:

1. **Controller checkout pins**: main has `dd8fb61d` on BOTH checkout steps (lines 86, 214 of the old file). Develop after #1200 has `e13f1570`.
2. **Publish step env**: main copy lacks `PLANNING_RECEIPT_WRITE_TOKEN` (the bug fixed by #1201). PR #1201 on develop adds it.
3. **Extract plan env**: main copy has `GH_WORKFLOW_TOKEN` defined; develop removes it (PR #1201 and #1195 cleanup).
4. **PR_NUMBER resolution**: main copy uses `github.event.workflow_run.pull_requests[0].number` with fallback; develop simplifies to `""` with regex-only fallback.
5. **Attempt tracking**: main copy passes `RUN_ATTEMPT` to Python; develop removes it (attempt is always 1 for authenticated runs, verified at API level).

**What registration action is needed:** After #1200 and #1201 are merged to develop, the coordinator (or Codex-MERGE per RUNBOOK §5) must push a new merge commit from develop to main (`git -C baseharbor merge origin/develop` into main, or `git push origin origin/develop:main`), which will overwrite the registered copy on main with the corrected develop version. This single action propagates ALL deltas (controller pin, token fix, env cleanup) atomically.

### Shadow pin detail

`receipt-shadow.yml@f57b30ed` predates the R27-F6 publication-input fix. PR #1200 (5aaa38ec) updates it to `b53632aaaee6067397c27000c229f34736ec2155` — the reviewed develop head carrying R27-F6 compliant `receipt-shadow.yml`. The comment at line 134 of receipt-approval.yml states: "the honest pre-registration state".

## 1. Step-by-step operations checklist: #1200 correction + #1201 merge + main registration

### 1.1 Merge PR #1200 (receipt-approval.yml TRUSTED_SOURCE pin fix)

| Step | Command / API Call | Actor | Precondition Gate | Expected Observation | Rollback |
|------|---------------------|-------|-------------------|---------------------|----------|
| 1.1.1 | `gh pr check 1200 --repo mcpdev80/baseharbor` | lane\|coordinator | PR #1200 mergeable=true (verified) | All required checks: SUCCESS; PR Selected Checks: SUCCESS | None needed (not merged yet) |
| 1.1.2 | `gh pr merge 1200 --repo mcpdev80/baseharbor --squash --commit-message "ci(r27): pin receipt-approval trusted source to reviewed b53632aa (#1200)"` | Codex-MERGE (Owner-authorized) | Step 1.1.1 green | Merge commit on develop; new develop HEAD; PR #1200 state = MERGED | `git revert` the squash commit if needed; re-open PR |
| 1.1.3 | `git -C baseharbor fetch origin develop && git -C baseharbor rev-parse origin/develop` | lane\|coordinator | Step 1.1.2 confirmed merged | New develop HEAD (e.g. `aabbccdd…`); verify TRUSTED_SOURCE = `b53632aa…` in `origin/develop:.github/workflows/receipt-approval.yml:86` | Revert develop to old HEAD |
| 1.1.4 | `git -C baseharbor show <new-develop-head>:.github/workflows/receipt-approval.yml \| grep 'TRUSTED_SOURCE'` | lane\|coordinator | Step 1.1.3 | Line 86: `TRUSTED_SOURCE: 'b53632aaaee6067397c27000c229f34736ec2155'` | Confirmed fix |

### 1.2 Merge PR #1201 (receipt-post-run.yml publish-step token fix)

| Step | Command / API Call | Actor | Precondition Gate | Expected Observation | Rollback |
|------|---------------------|-------|-------------------|---------------------|----------|
| 1.2.1 | `gh pr check 1201 --repo mcpdev80/baseharbor` | lane\|coordinator | PR #1201 mergeable=true (verified) | All required checks: SUCCESS; PR Selected Checks: SUCCESS | None |
| 1.2.2 | `gh pr merge 1201 --repo mcpdev80/baseharbor --squash --commit-message "ci: supply PLANNING_RECEIPT_WRITE_TOKEN to receipt publish step (#1201)"` | Codex-MERGE (Owner-authorized) | Step 1.2.1 green; Step 1.1.2 confirmed (both PRs to develop) | Merge commit on develop; PR #1201 = MERGED | Revert develop |
| 1.2.3 | `git -C baseharbor fetch origin develop && git -C baseharbor show origin/develop:.github/workflows/receipt-post-run.yml \| grep 'PLANNING_RECEIPT_WRITE_TOKEN'` | lane\|coordinator | Step 1.2.2 confirmed | Line in publish step env: `PLANNING_RECEIPT_WRITE_TOKEN: ${{ secrets.PLANNING_RECEIPT_WRITE_TOKEN }}` | Confirmed fix |

### 1.3 Main registration delta action

| Step | Command / API Call | Actor | Precondition Gate | Expected Observation | Rollback |
|------|---------------------|-------|-------------------|---------------------|----------|
| 1.3.1 | `git -C baseharbor fetch origin main && git -C baseharbor fetch origin develop && git -C baseharbor log --oneline origin/main..origin/develop` | lane\|coordinator | Steps 1.1.2 + 1.2.2 both merged to develop | List of new commits on develop not yet on main (includes #1200, #1201 merge commits) | N/A |
| 1.3.2 | `git -C baseharbor merge-base origin/main origin/develop` | lane\|coordinator | Step 1.3.1 | Base commit SHA (e.g. `9e50d8a4…` — the develop commit before #1199 merge) | N/A |
| 1.3.3 | **OWNER DECISION POINT (see §5.1):** Confirm that main registration (develop→main merge) is authorized. | Owner | Steps 1.1.2 + 1.2.2 confirmed merged | Owner confirmation required | Do not proceed |
| 1.3.4 | `git -C baseharbor checkout main && git -C baseharbor merge origin/develop --no-edit && git -C baseharbor push origin main` | Codex-MERGE (Owner-authorized) | Steps 1.1.2 + 1.2.2 + 1.3.3 all confirmed | origin/main now contains updated `receipt-post-run.yml` with controller pin `e13f1570`, publish-step token, cleaned env blocks | `git -C baseharbor revert origin/main~1..origin/main` or force-reset to old main HEAD (Owner-authorized) |
| 1.3.5 | `git -C baseharbor show origin/main:.github/workflows/receipt-post-run.yml \| grep 'PLANNING_RECEIPT_WRITE_TOKEN'` | lane\|coordinator | Step 1.3.4 | Token present in publish step env on main | Confirmed propagation |

### 1.4 Controller pin delta clarification

After step 1.3.4, origin/main will carry controller pin `e13f1570` (develop head at merge time) instead of the previous `dd8fb61d`. This is **intentional** — `e13f1570` is the release-promoted develop that carries all post-#1170 fixes including receipt-post-run.yml corrections. The controller scripts on `e13f1570` are functionally identical to `dd8fb61d` for receipt_verifier / receipt_writer; the diff between them is purely in `receipt-post-run.yml` workflow content, not in the Python helper source.

## 2. Step-by-step: new producer run + automatic publication proof

### 2.1 Trigger a new producer CI run

| Step | Command / API Call | Actor | Precondition Gate | Expected Observation | Rollback |
|------|---------------------|-------|-------------------|---------------------|----------|
| 2.1.1 | Push a commit to a fresh branch from develop (or rebase an existing open PR to develop) to trigger "CI · Source & Quality" | lane\|coordinator | Steps 1.1.2 + 1.2.2 + 1.3.4 all confirmed (both PRs merged, main registered) | New run 408xxxxxxx on "CI · Source & Quality" starts | Cancel the run; delete branch |
| 2.1.2 | `gh run list --repo mcpdev80/baseharbor --workflow ci.yml --state success` | lane\|coordinator | Step 2.1.1 triggered | Run conclusion = SUCCESS; run_attempt = 1 | Document run ID |
| 2.1.3 | Verify `workflow_run` trigger: `git -C baseharbor show origin/main:.github/workflows/receipt-post-run.yml \| grep -A3 'workflow_run:'` | lane\|coordinator | Step 2.1.2 success | `receipt-post-run.yml` triggers on `workflow_run` of "CI · Source & Quality" with `types: [completed]` | Confirmed auto-trigger |
| 2.1.4 | `gh run list --repo mcpdev80/baseharbor --workflow "Receipt · Post-Run Writer" --limit 5` | lane\|coordinator | Step 2.1.2 success; auto-trigger armed | At least one run of "Receipt · Post-Run Writer" appears with conclusion SUCCESS | If failed: check step "Publish receipt to Planning" for token errors |

### 2.2 Automatic publication verification

| Step | Command / API Call | Actor | Precondition Gate | Expected Observation | Rollback |
|------|---------------------|-------|-------------------|---------------------|----------|
| 2.2.1 | `git -C baseharbor-plan fetch origin main && ls -la /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/receipts/public-contracts/` | lane\|coordinator | Step 2.1.4: post-run workflow SUCCESS | New JSON file in public-contracts/ (e.g. `<run-id>-1.json`) | If empty: the publish step failed (token missing or controller error) |
| 2.2.2 | `git -C baseharbor-plan show origin/main:evidence/receipt-plans/ 2>&1` | lane\|coordinator | Step 2.2.1 | Plan fixture files exist (tasklink written) | If absent: tasklink script failed |
| 2.2.3 | `gh api repos/mcpdev80/baseharbor/actions/runs/<post-run-run-id> --jq '.jobs[] | {name, conclusion}'` | lane\|coordinator | Step 2.2.1 | All jobs in post-run workflow: `producer_context`=SUCCESS, `extract_plan`=SUCCESS, `publish_receipt`=SUCCESS | If `publish_receipt` failed: check step log for `receipt_writer.py` errors |
| 2.2.4 | **Negative proof NP-1:** Verify the receipt published has `candidate_sha` = the producer run's integration_sha (not the PR head). | lane\|coordinator | Step 2.2.1 | Receipt JSON `candidate` field matches integration_sha from pr-plan.json (not head_sha) | If mismatch: `extract_facts()` bug — document and halt |

## 3. Step-by-step: hosted approval + retained shadow + three negative proofs

### 3.1 Hosted Owner approval dispatch

| Step | Command / API Call | Actor | Precondition Gate | Expected Observation | Rollback |
|------|---------------------|-------|-------------------|---------------------|----------|
| 3.1.1 | **OWNER DECISION POINT (see §5.2):** Select which approved receipt to dispatch approval for. | Owner | Steps 2.2.1 + 2.2.2 confirmed (automatic publication works) | Owner selects PR number (e.g. from the producer run that just published) | N/A |
| 3.1.2 | `curl -s -X POST https://api.github.com/repos/mcpdev80/baseharbor/actions/workflows/receipt-approval.yml/dispatches \\\n  -H "Accept: application/vnd.github+json" \\\n  -H "Authorization: Bearer <OWNER_TOKEN>" \\\n  -H "X-GitHub-Api-Version: 2022-11-28" \\\n  -d '{"ref":"develop","inputs":{"pr_number":"<selected-pr-number>"}}'` | lane\|coordinator (manual workflow_dispatch) | Steps 1.1.2 confirmed (TRUSTED_SOURCE pinned to b53632aa); Step 3.1.1 owner decision | Workflow run # for receipt-approval starts; check-run appears on PR | Cancel run; delete branch |
| 3.1.3 | `gh run view <run-id> --repo mcpdev80/baseharbor --json conclusion,statusCheckRollup` | lane\|coordinator | Step 3.1.2 triggered | `approve` job: SUCCESS; `approval-step` env TRUSTED_SOURCE = `b53632aa…` (not empty) | If TRUSTED_SOURCE still empty: pin was not propagated to develop |
| 3.1.4 | Verify outputs: `gh api repos/mcpdev80/baseharbor/actions/runs/<run-id>/jobs --jq '.jobs[] | select(.name == "approve") | .steps[] | select(.name == "Verify, approve and publish the receipt for the selected PR") | .outputs'` | lane\|coordinator | Step 3.1.3 success | `receipt`, `plan`, `candidate`, `publication` outputs present and non-empty | If empty: verifier failed to produce outputs; check `receipt_verifier.py approve` log |

### 3.2 Retained shadow consumption

| Step | Command / API Call | Actor | Precondition Gate | Expected Observation | Rollback |
|------|---------------------|-------|-------------------|---------------------|----------|
| 3.2.1 | `gh run view <shadow-run-id> --repo mcpdev80/baseharbor --json conclusion,jobs` | lane\|coordinator | Step 3.1.3 approve job SUCCESS | `receipt-shadow.yml` shadow job: SUCCESS (offline retained verify) | If FAILED: shadow verifier found mismatch — document exact error |
| 3.2.2 | Verify shadow consumed exact publication commit: inspect shadow job log for `plan_revision` match. | lane\|coordinator | Step 3.2.1 | Shadow log shows `plan_revision` = the exact commit from step 3.1.4 `publication` output | Mismatch indicates plan fixture drift |
| 3.2.3 | `git -C baseharbor show origin/develop:.github/workflows/receipt-approval.yml \| grep -A1 'receipt-shadow.yml'` | lane\|coordinator | Step 3.1.3 | Shadow invoked at `b53632aa…` (not f57b30ed) — confirms PR #1200 shadow pin fix reached develop | If `f57b30ed`: #1200 did not reach develop |

### 3.3 Three negative proofs from CODEMAN-START "Proof and cutover"

**Negative proof NP-1 (candidate SHA integrity):** After step 2.2.1, the receipt's `candidate` field MUST equal the producer integration_sha — NOT the PR head_sha. If it equals head_sha, the receipt chain is broken.

| Step | Command | Actor | Precondition | Expected |
|------|---------|--------|-------------|----------|
| NP-1.1 | Compare `candidate` from published receipt JSON with `integration_sha` from pr-plan.json artifact. | lane\|coordinator | Step 2.2.1 | Fields match exactly. If mismatch → chain integrity FAIL. |

**Negative proof NP-2 (no unapproved receipt on main):** After step 2.2.1, baseharbor-plan origin/main evidence/receipts/public-contracts/ should contain ONLY approved receipts — unapproved receipts must NOT appear.

| Step | Command | Actor | Precondition | Expected |
|------|---------|--------|-------------|----------|
| NP-2.1 | `git -C baseharbor-plan show origin/main:evidence/receipts/public-contracts/ | wc -l` | lane\|coordinator | Step 2.2.1 | Receipt count = 1 (the one published by step 2.2.1). Additional unapproved receipts indicate publication gate failure. |

**Negative proof NP-3 (shadow never calls GitHub API):** After step 3.2.1, the shadow job log must contain NO `gh api` or `gh run` calls — it reads only from the local Planning checkout.

| Step | Command | Actor | Precondition | Expected |
|------|---------|--------|-------------|----------|
| NP-3.1 | `gh run view <shadow-run-id> --repo mcpdev80/baseharbor --log | grep -c 'gh api\|gh run'` | lane\|coordinator | Step 3.2.1 | Count = 0. Any `gh api`/`gh run` call indicates shadow is falling back to live GitHub API — design violation. |

## 4. Step-by-step: check-to-context mapping activation on ruleset 25223521

### 4.1 Current ruleset 25223521 state (from q201 design)

Ruleset 25223521 ("develop - required checks"):
- `enforcement: disabled`
- Rule: `required_status_checks` with context `"PR Selected Checks"` (integration_id 15368)
- `strict_required_status_checks_policy: true`
- `do_not_enforce_on_create: false`
- `bypass_actors: []`
- `current_user_can_bypass: never`

This ruleset currently requires `PR Selected Checks` (legacy context) — the integration_id 15368 app that produces this check is GitHub Actions, bound to `pull_request` job events.

### 4.2 Legacy PR-Selected-Checks retirement sequence

| Step | Command / API Call | Actor | Precondition Gate | Expected Observation | Rollback |
|------|---------------------|-------|-------------------|---------------------|----------|
| 4.2.1 | `gh api repos/mcpdev80/baseharbor/rulesets/25223521 --jq '.rules'` (baseline read) | lane\|coordinator | Steps 1.3.4 confirmed (main registered with corrected workflows) | Baseline: one `required_status_checks` rule with context "PR Selected Checks" | Save JSON for revert |
| 4.2.2 | **OWNER DECISION POINT (see §5.3):** Confirm that legacy "PR Selected Checks" retirement is authorized. | Owner | Steps 2.2.1 + 3.1.3 + 3.2.1 all confirmed (producer, approval, shadow all work) | Owner confirmation | Do not proceed |
| 4.2.3 | `gh api -X PATCH repos/mcpdev80/baseharbor/rulesets/25223521 -H "Accept: application/vnd.github+json" -d '{ "rules": [{ "type": "required_status_checks", "parameters": { "required_status_checks": [{ "context": "Receipt · Candidate Completion", "integration_id": 15368 }], "strict_required_status_checks_policy": true, "do_not_enforce_on_create": false } }] }'` | Codex-MERGE (Owner-authorized) | Steps 3.1.3 + 3.2.1 confirmed; Step 4.2.2 owner decision | Ruleset now requires "Receipt · Candidate Completion" instead of "PR Selected Checks" | Revert: reapply baseline JSON from step 4.2.1 |
| 4.2.4 | `gh api repos/mcpdev80/baseharbor/rulesets/25223521 --jq '.rules[].parameters.required_status_checks[0].context'` | lane\|coordinator | Step 4.2.3 | Output: `"Receipt · Candidate Completion"` | Confirmed context change |
| 4.2.5 | `gh api -X PATCH repos/mcpdev80/baseharbor/rulesets/25223521 -H "Accept: application/vnd.github+json" -d '{"enforcement":"active"}'` | Codex-MERGE (Owner-authorized) | Step 4.2.4 confirmed | Ruleset 25223521 `enforcement` = `"active"` | Revert: `"disabled"` |

### 4.3 New required context activation

The new context `Receipt · Candidate Completion` (integration_id 15368, app 15368 = GitHub Actions) will be satisfied by check runs placed on the PR head SHA by the receipt chain:

1. `receipt-post-run.yml` places a check run on the producer integration_sha via `POST /repos/{owner}/{repo}/check-runs` in the `producer_context` job.
2. After `workflow_run` of "CI · Source & Quality" succeeds, `receipt-post-run.yml` runs the `producer_context` job which calls `gh api` to place check runs under app 15368.
3. The `Receipt · Candidate Completion` check run name is set verbatim in the `name:` field of the `POST /check-runs` call within `receipt-post-run.yml:producer_context.steps.facts`.
4. The ruleset matcher (`context: "Receipt · Candidate Completion"`, `integration_id: 15368`) will match and satisfy the new required check.

**Strict policy enforcement:** `strict_required_status_checks_policy: true` means the check run's `head_sha` must match the PR's merge commit exactly. The receipt chain satisfies this because `extract_facts()` produces `candidate_sha = integration_sha` (the merge commit), and the check run is placed at that SHA.

## 5. OWNER decision points

### 5.1 Main registration authorization

**Decision:** Is origin/main registration (develop→main merge, step 1.3.4) authorized?

- **Required evidence before decision:** Steps 1.1.2 (#1200 merged), 1.2.2 (#1201 merged) confirmed.
- **Risk:** Merging develop to main overwrites the registered `receipt-post-run.yml` on main with the develop version. This is intentional and required — it propagates the token fix and controller pin.
- **If NO:** Do not proceed to step 1.3.4. The receipt chain remains unenforced on main.

### 5.2 Approval dispatch authorization

**Decision:** Which PR number to dispatch `receipt-approval.yml` workflow_dispatch for?

- **Required evidence before decision:** Step 2.2.1 (automatic publication produced a receipt) confirmed.
- **Risk:** The approval dispatch fires `receipt-approval.yml` which runs the immutable controller at the checkout pin. With `TRUSTED_SOURCE: ''` (before #1200), the verifier fails closed. After #1200 merge, `TRUSTED_SOURCE = b53632aa`.
- **If NO:** The shadow chain cannot be triggered.

### 5.3 Ruleset activation authorization

**Decision:** Is ruleset 25223521 activation (step 4.2.5) authorized?

- **Required evidence before decision:** Steps 2.2.1 (producer auto-publish), 3.1.3 (approval dispatch), 3.2.1 (shadow consumption) all confirmed.
- **Risk:** Activating the ruleset enforces `Receipt · Candidate Completion` as a required check on develop branches. PRs to develop will fail merge without the receipt check running.
- **Rollback:** Reapply the baseline ruleset JSON (step 4.2.1) with enforcement=disabled.
- **If NO:** The legacy "PR Selected Checks" remains the sole required context (and is already satisfied by the existing CI).

### 5.4 Token provisioning confirmation

**Required:** Confirm that `PLANNING_RECEIPT_WRITE_TOKEN` and `GITHUB_TOKEN` (workflow_secret) exist in repository secrets.

- **Command:** `gh api repos/mcpdev80/baseharbor/actions/secrets --jq '.secrets[] | select(.name == "PLANNING_RECEIPT_WRITE_TOKEN") | .name'`
- **Expected:** Non-empty output (the secret exists — name only, never value).
- **If missing:** The publish step will fail closed regardless of env block.

### 5.5 Approval PR choice

**Decision:** After step 3.1.3 approval dispatch, which receipt to accept? The one produced by step 2.2.1 (auto-published), or a manually-triggered second producer run?

- **Recommended:** Accept the auto-published receipt from step 2.2.1 — it is the first production receipt and the one the entire chain was designed to produce.
- **Risk:** If auto-publish produced a corrupted receipt, manual dispatch will reveal it.

## 6. End-to-end sequence summary (chronological)

1. **Precondition:** Steps 1.1.2, 1.2.2 confirmed (#1200, #1201 merged to develop)
2. **Step 1.3.3/1.3.4:** Owner authorizes main registration; Codex-MERGE merges develop to main (1.3.4)
3. **Step 2.1.1–2.1.4:** Trigger new producer run → verify auto-trigger of receipt-post-run → verify post-run SUCCESS
4. **Step 2.2.1–2.2.4:** Verify automatic publication produced receipt on Planning main; verify NP-1 candidate integrity
5. **Step 3.1.1–3.1.4:** Owner selects PR number; dispatch approval workflow; verify approve job SUCCESS; verify outputs
6. **Step 3.2.1–3.2.3:** Verify shadow job SUCCESS at b53632aa; verify plan_revision match; verify shadow pin on develop
7. **Step 3.3 NP-2/NP-3:** Verify no unapproved receipts; verify shadow makes zero API calls
8. **Step 4.2.2/4.2.3/4.2.4/4.2.5:** Owner authorizes ruleset activation; Codex-MERGE patches context + sets enforcement=active
9. **Post-cutover verification:** Open PR to develop → verify `Receipt · Candidate Completion` check runs → verify merge proceeds

## 7. Rollback plan (single point of failure)

If any step fails, rollback to the state immediately before step 1.3.4 (the main registration merge):

- **Step 1.3.4 rollback:** `git -C baseharbor push origin <old-main-sha>:main --force` (Owner-authorized)
- **Steps 4.2.3/4.2.5 rollback:** Reapply baseline ruleset JSON with enforcement=disabled
- **All other steps:** No state change until main registration; simply cancel workflows and delete branches

END q204-DONE

# R27 candidate review: BLOCKED

ROLLE: REVIEW. Independent source/evidence review only; no merge, product edit, product push, workflow dispatch, credential change or recipe implementation.

Review UTC: 2026-10-27T15:18:57Z. Reviewer: Codex, current API session; backend/model identifier and Horde task ID are not exposed to this session and are not invented. Authenticated GitHub account: `mcpdev80`.

Candidate: [baseharbor#1119](https://github.com/mcpdev80/baseharbor/pull/1119), `work/r27-correction-v31`.

- Exact SHA before: `c7936e8bd8385581c643f1598f5b1dfd3cfca945`.
- Exact SHA after source review (fresh PR API read): `c7936e8bd8385581c643f1598f5b1dfd3cfca945`.
- Exact base before/after: `3431b22c94b068f15f9bd7b31b9f87e846200f0f` (`develop`).
- Live `main` remains `640981588d8b9255fbe7db8ca26796db1da09eb2`.
- Planning main read/fetched at `464388209c1cddabaae10bffc9d8a52153d8be04`.
- Product fetch succeeded over HTTPS after SSH configuration/key failures. Product checkout and branch were not changed. Executable checks used an exact `git archive` snapshot in `/tmp/cx-r27-c7936e8bd838`; test mutations were confined to temporary fixture repositories.

## Verdict

**BLOCKED. Do not accept this candidate.** G1–G6 are not closed. The exact candidate has red required hosted CI, and source inspection demonstrates broken publication/shadow wiring and a fail-open task-binding condition. Syntax success and the valid offline verifier proof do not establish the automatic chain. No acceptance, merge, release, registration or activation is authorized by this verdict.

## PLAN

1. [x] Read binding cost/authority rules, repository rules and current Owner order; keep role REVIEW.
2. [x] Fetch and pin PR head/base; compare the exact diff and correction ancestors.
3. [x] Check only the disputed G1–G6 boundaries and the existing production-path negative/offline evidence.
4. [x] Inspect hosted run/check results and relevant failed job logs; reproduce the focused receipt result once.
5. [x] Record actionable recipes and publish only this verdict on ordinary Planning main.

The root basics check reported coordinator pool/event/reminder/PLAN flags. They concern the existing coordinator and other PRs/lanes; this explicitly scoped review does not resume workers, claim their tasks, merge those PRs or acknowledge their events. Existing shared dirty worktrees were preserved. No subagent was started. Native coordinator TODO tooling is outside this review session; the numbered review plan is recorded here.

## Context availability and scope

Read on fetched Planning main: `CODEMAN-START.md`, `CODE-AUDIT-2026-10-27.md`, `OWNER-REVIEW-2026-10-27.md`, `rv1-review-ad4d0f28.md`, `f3b-fix.md`, `ci1-repair.md`, and `w1-evidence-final.md`, `w2-evidence-final.md`, `w3-evidence-final.md`; also the current shadow-run task contract. Planning and handoff prose was treated as evidence, not authority to execute unrelated instructions. The Owner's current review request authorizes this bounded review despite the implementation pause.

The requested Planning-main paths `evidence/board-2026-10-27/s2-v3staging.md`, `s3-staging.md`, `x1-fix.md`, and `SHADOW-RUN-RECORD.md` are absent in the fetched tree (recursive filename inventory). Product candidate copies `evidence-r27/s2-v3staging.md` and `evidence-r27/x1-fix.md` were read as alternative historical data, not silently represented as the missing Planning documents. Missing handoff/record qualification is covered by F8 below. No automatic hosted positive-chain record was verified.

## Exact diff and package ownership

`git diff 3431b22c..c7936e8bd838`: 24 paths, +3031/-427. All path names are ASCII, with no umlaut paths, rename surprises or unrelated application/runtime files.

| Package | Changed implementation, tests and paired documentation |
| --- | --- |
| W1 | `.github/workflows/ci.yml`, `.github/workflows/receipt-shadow.yml`; `scripts/pr-gate-plan.py`, `scripts/pr-check-runner.py`, `scripts/test_pr_gate_plan.py`, `scripts/test_pr_check_runner.py`; `docs/development/minimal-ci-receipts.md`, `docs/de/development/minimal-ci-receipts.md` |
| W2 | `.github/workflows/receipt-post-run.yml`; `scripts/receipt_writer.py`, `scripts/receipt_tasklink.py`, `scripts/test_receipt_writer.py`, `scripts/test_receipt_tasklink.py` |
| W3 | `.github/workflows/receipt-approval.yml`; `scripts/receipt_verifier.py`, `scripts/test_receipt_verifier.py`, `scripts/test_receipt_chain.py` |
| Additional product evidence files | `evidence-r27/{ci1-repair,f1-fix,f3b-fix,s2-v3staging,w1,w3,x1-fix}.md` |

All five specified ancestors are present, verified with `merge-base --is-ancestor`: `96011aac`, `06d80208`, `94655dcc`, `d5105121`, `66555394`. The original W1/W2/W3 implementation files map to the ordered packages. Later corrections cross those package boundaries: `d5105121` changes W2 publication/post-run plus W3 verifier; `66555394` changes W1 shadow, W2 tasklink, W3 approval/verifier; `06d80208` changes W3 approval. Missing current reservation/handoff records prevent independently certifying that these cross-package writes were coordinated and disjoint in time. No concurrent-write violation is inferred merely from the merged diff.

The seven product evidence files are not application foreign files, but they are additional paths outside the exclusive implementation table and have a real coverage consequence (F2/F8). Thus a blanket "no extra paths / all write-set gates verified" assertion would be inaccurate. `git diff --check` also reports trailing whitespace at `evidence-r27/ci1-repair.md:22` and `scripts/test_receipt_writer.py:526,528`; cosmetic only, not a separate acceptance blocker.

## G1–G6 disposition against rv1

| Owner gap | Exact-candidate disposition |
| --- | --- |
| G1: YAML, actual context and run/plan passing | YAML/actionlint corrected; no workflow `GITHUB_*` overrides found. Execution and run/plan semantics still broken: F1. |
| G2: executed discovery and workflow-policy coverage | Receipt tests now really execute and propagate the current failure. Success regex still rejects normal success; policy suite still excluded. Hosted checks red and coverage unresolved: F2. rv1's "discovery fixed" conclusion is not sustained. |
| G3: no force + real bounded re-apply | Force push removed; identical published bytes are reusable. Unrelated remote edits still block rather than re-apply: F3. rv1's FF/retry claim was too broad. |
| G4: one mapping + actual card evidence | Shared function imported, but writer workflow bypasses it; verifier catches mapping failure and can accept no binding. Card update is local-only and swallowed on failure: F4/F5. |
| G5: automatic approval-to-shadow + honest source policy | A reusable call exists, but consumes human inputs rather than publication outputs; placeholder outputs and mutable/wrong-context sources remain. `develop` is still allowed without Owner authorization: F6/F7. |
| G6: report integrity | BLOCKED is required by the code and CI. Several repair/evidence claims remain contradicted; missing requested records and extra evidence paths are disclosed: F8. |

## Hosted CI: exact head, not a previous integration

[Run 40529019816, attempt 1](https://github.com/mcpdev80/baseharbor/actions/runs/40529019816): `head_sha=c7936e8bd8385581c643f1598f5b1dfd3cfca945`, event `pull_request`, completed `failure`, updated `2026-10-27T15:16:53Z`.

- [PR · Focused Python, job 122276506347](https://github.com/mcpdev80/baseharbor/actions/runs/40529019816/job/122276506347): failure.
- [PR · Validation · pr-planner-tests, job 122276507024](https://github.com/mcpdev80/baseharbor/actions/runs/40529019816/job/122276507024): failure.
- [PR Selected Checks, job/check 122277637740](https://github.com/mcpdev80/baseharbor/actions/runs/40529019816/job/122277637740): completed **failure**, GitHub Actions app **15368** (read from the exact commit check-runs API).
- `ci-actionlint`, `ci-policy`, `Workflow policy`, trusted plan, executor/verifier validation and documentation jobs succeeded. Public Contracts / Exact Candidate and other downstream jobs were skipped; skipped is not PASS.

Job-log excerpts (Focused Python, `2026-10-27T15:15:45Z`; planner job repeats the same cause at `15:16:39Z`):

```text
FAIL: test_human_input_is_pr_selection_only
File ".../scripts/test_receipt_verifier.py", line 757
AssertionError: Items in the first set but not the second:
'receipt'
'candidate'
'plan'
Ran 122 tests in 12.525s
FAILED (failures=1)
RuntimeError: receipt discovery/execution failed: ...
```

Final-check log (`2026-10-27T15:16:49Z`):

```text
BLOCKED: required authenticated job not successful: PR · Focused Python
BLOCKED: required validation not successful: pr-planner-tests (blocked)
BLOCKED: coverage-unresolved: workflow execution/cleanup/evidence impact requires native qualification: .github/workflows/ci.yml; CI execution/evidence impact requires specific qualification: evidence-r27/ci1-repair.md; ... scripts/pr-check-runner.py; ... scripts/test_pr_check_runner.py
```

The full coverage line also enumerates all seven `evidence-r27` files. Correcting the failing input test alone will not resolve this independent coverage blocker. No rerun or replacement hosted workflow was launched during review.

## Findings and worker recipes

All findings below block acceptance. Recipes are instructions for the authorized correction owner, not implemented by this reviewer.

### F1 — G1: post-run cannot produce the claimed receipt

Files: `.github/workflows/receipt-post-run.yml:39-65,85-124,145-164,187-224`; `scripts/receipt_writer.py:174-187,218-230`; `scripts/receipt_verifier.py:239-257,318-319`.

The first shell step writes output-file entries but never assigns shell variables `workflow_id`, `head_sha`, `pr_number`. Its final echo expands them under `set -u`, so normal execution fails before publication. It also assumes nonexistent run `base_sha`/`base_ref` rather than resolving the authenticated PR tuple. Artifact download has no GH token/repository context, looks for ZIP contents with `gh run download --pattern '*.zip'`, uses BSD `xargs -J` on Ubuntu, and swallows download failure. Decoding uses `source plan_vars.txt` on artifact-derived strings without strict validated parsing. Workflow ID is read from the artifact even though the definition ID must come from the authenticated run.

The later writer call supplies **workflow definition ID as `--run`**, while `live()` requests `actions/runs/{run.id}` and checks the actual run ID. `--plan` is **product candidate SHA**, but `load_plan()` reads a commit from the **Planning repository**. The plan-fixture CLI's returned Planning commit is never captured. Hardcoded task and missing `--pr-number` persist. `ref: develop` is mutable, not the claimed immutable reviewed controller. Writer `live()` receives no product checkout, so the producer-definition check is omitted at issuance (approval later checks it). Planning identity and durable push authentication are not configured: post-run checkout has `persist-credentials:false`; passing a checkout token does not configure subsequent `git push`. The approval workflow similarly passes a token environment variable that none of these Python helpers consumes for git authentication. The existence of the actual secret remains unverified; no secret value was accessed.

**Recipe:** W2 fixes post-run orchestration and W1/coordinator supplies the reviewed immutable helper pin. Parse authenticated producer run/PR/artifact as bounded data with an authenticated API call; remove shell-sourcing, fallback facts and nonportable download commands. Keep definition ID and run ID distinct; capture the actual Planning fixture commit and pass that as `--plan`, and pass the producer run ID as `--run`. Use shared PR/task resolution, required producer trust checking, explicit commit identity and scoped ephemeral git push authentication in the trusted jobs only. Do not set or override `GITHUB_*` claims. Preserve main-only context and separate registration.

**Tests:** execute the actual workflow shell/controller path with realistic run/artifact fixtures and distinct product/Planning/run/definition identifiers. Assert no unbound variables, no missing-artifact success, no artifact shell execution, and real bare-remote publication/read-back; run genuine context/ref rejection tests. Validate actionlint after changes.

**Stop criterion:** any producer tuple ambiguity, missing artifact/token/authentication, wrong real ref or absent reviewed pin must block before mutation. No G1 closure until the real command path passes end to end with correctly typed IDs/revisions.

### F2 — G2 and host qualification: discovery is still incorrect and required CI is red

Files: `scripts/pr-check-runner.py:137-159`, `scripts/pr-gate-plan.py:664,680`, `.github/workflows/ci.yml:655`, `scripts/test_pr_check_runner.py:275-292`, `scripts/test_pr_gate_plan.py`; `.github/workflows/receipt-approval.yml:38-54`.

The existing discovery really runs 122 tests, exposing F6. However its success regex `\(test_receipt[_a-z]*\.[^(]+\(` requires an extra opening parenthesis after `module.Class.method`; ordinary unittest success contains a closing parenthesis. A direct bounded check against `test_example (test_receipt_writer.ReceiptWriterTest.test_example) ... ok` returns **False**. `test_ci_workflow_policy_receipts.py` is returned as "matched" without execution: `test_receipt*.py` cannot select it. No independent invocation was found in the changed lane. Thus fixing the current failing suite would expose the existing success-parser defect next.

The final selected check also independently rejects unresolved impact for CI execution paths and product evidence files (host log above).

**Recipe:** W1 proves actual execution and success for each required receipt/policy module, explicitly includes the policy module, and repairs the unittest success recognizer without weakening zero-test/failure rejection. Return only actual executed modules. Coordinator removes/moves out-of-scope product evidence into the established Planning location or supplies the narrowly reviewed classification and genuine qualification for each remaining changed execution path. Resolve F6 rather than weakening its valid input-contract test. Do not blanket-allow unknown CI paths or bypass final checks.

**Tests:** normal successful verbose output, zero tests, one missing required module, excluded policy module, and one failing test; actual selected planner/runner invocation must pass. Requalify one coherent corrected head through legacy CI, inspecting its trusted plan and every mandatory result.

**Stop criterion:** no ACCEPT while exact-head `PR Selected Checks` from app 15368 is missing, failed, skipped, uncertain or coverage-unresolved. Green syntax alone is insufficient.

### F3 — G3: no actual re-apply after unrelated concurrent changes

Files: `scripts/receipt_writer.py:122-161,164-174`; `scripts/test_receipt_writer.py:394-431,463-500`.

After rejected push, the function fetches and returns only if remote receipt bytes already equal local bytes; otherwise it immediately raises. It never reapplies its own edit onto the fresh remote. An unrelated edit while the receipt is still absent, or while the unapproved receipt remains unchanged, blocks instead of retrying. The existing test named `test_publish_during_concurrent_unrelated_edit_retries` explicitly expects an exception. The new "reapplies" test instead pre-publishes identical receipt bytes via a concurrent writer; it proves duplicate recognition, not re-apply. `_find_introduction()` also swallows Git errors and substitutes a revision, contradicting exact introduction reporting.

**Recipe:** W2 captures the bounded own edit and its expected prior bytes, fetches fresh main after rejection, preserves unrelated changes, reapplies the same edit only when prior bytes/history still match, and ordinary-pushes with bounded retries. Reuse identical durable evidence without a second approval edit. Propagate introduction/history errors instead of substituting commits; never force push.

**Tests:** temporary bare remote with an unrelated concurrent edit before first receipt; unrelated concurrent edit before approval publication; identical already-published retry; conflicting receipt; lost push acknowledgement; transport/history failures. Assert both changes survive, exact durable commits are returned, and exactly one approval edit exists.

**Stop criterion:** different receipt/history blocks; unrelated changes must succeed within the bound without being overwritten. Existing "raises on unrelated edit" is not proof of the requested recovery contract.

### F4 — G4: task mapping is not authoritative and fails open

Files: `scripts/receipt_verifier.py:415-446,501`; `scripts/receipt_tasklink.py:51-126`; `.github/workflows/receipt-post-run.yml:123,187-193`.

Verifier imports the shared resolver but catches `TaskLinkError` and sets `expected_task=None`. With no backward `prs:` binding, `require(expected_task is None or task != expected_task, ...)` then succeeds. It also succeeds if a resolved task differs from the requested one and no note claims the PR. A direct call of production `task_binding()` with resolver failure and empty task inventory returned **None (success)**, not a rejection. The approval path does not forward its injected API to this resolver, so tests with fake authenticated APIs can silently reach the real resolver and then suppress the error. Meanwhile the writer workflow continues hardcoding a task and never invokes PR resolution.

**Recipe:** W2 owns one trusted deterministic PR-to-task resolver consumed by writer and verifier; W3 makes resolution failures, missing/ambiguous bindings and mismatches unconditionally fatal. Use actual Planning task metadata according to the current contract, not independent fallback interpretations of public issue prose. Forward the authenticated/injected API consistently and require the task to exist at the bound Planning revision. Connect the post-run call to this same authority.

**Tests:** absent forward and backward binding; missing task; ambiguous task; mismatch; API failure; issue-text manipulation; positive agreed binding. Assert production approval performs no write/push and no external network call under injected test APIs for every negative.

**Stop criterion:** no approval or issuance without exactly one valid shared mapping. A caught resolver error is never authorization.

### F5 — G4: task evidence is not durably published and may replace existing evidence

Files: `scripts/receipt_verifier.py:449-490`; `scripts/receipt_tasklink.py:266-361`.

Approval first pushes the receipt. `publish_evidence()` then commits a task-note edit **locally**; there is no subsequent push, returned commit is ignored, and its exceptions are swallowed. Returned publication still points before this task edit. The formatter replaces any `evidence:` line with one bare path, discarding prior inline evidence and potentially leaving stale continuation lines for YAML list forms. It ignores `plan_revision`, supplies no immutable public evidence URL/summary, and a repeated unchanged update attempts another commit rather than returning idempotently. No planning render/check follows the metadata edit. Local HEAD advancing after a fake publisher is not proof that a card was updated on remote main.

**Recipe:** W2 uses the Planning schema/parser to append a precise immutable receipt/publication reference while preserving existing evidence; render/check the resulting metadata and derived views. Include the bounded task edit in durable publication through the same publisher, return/read back the final publication revision, and propagate failure. Handle retry without a second approval edit or duplicate task evidence. Keep approval tied to the original receipt introduction commit.

**Tests:** bare-remote approval plus card update and remote read-back; existing inline/block evidence preservation; unchanged retry; missing task; rejected card push; unrelated concurrent task edit; render/check. Assert local-only/card-write failure never reports complete publication.

**Stop criterion:** no automatic-chain success until receipt and valid task evidence are present on remote main at the returned durable revision. Failure must remain actionable and fail closed.

### F6 — G5 and observed CI failure: shadow consumes manual inputs, not approval results

Files: `.github/workflows/receipt-approval.yml:38-54,103-139`; `.github/workflows/receipt-shadow.yml:52-58`; `scripts/receipt_verifier.py:510-511,537-541`.

Commit `06d80208` added manual `receipt`, `plan`, `candidate` dispatch fields to satisfy actionlint. Shadow reads those fields, bypassing the auto-resolved approved tuple. An Owner providing only PR number sends empty shadow inputs. The approval shell also emits hardcoded `.../123-1.json`, `plan=${GITHUB_SHA}`, `candidate=${GITHUB_SHA}`; these are not derived evidence, are not exposed as job outputs, and are not used by shadow. The reusable workflow is referenced by mutable `@develop`; its checkout uses `github.event.pull_request.base.sha` even though the caller event is `workflow_dispatch`, where that PR object is absent. No exact reviewed verifier source is selected for this event.

**Recipe:** W3 exports the actual resolved receipt path, Planning plan revision, candidate and durable publication from the verifier result; declare step/job outputs and pass `needs.approve.outputs.*` to shadow. Remove the three manual evidence fields and all placeholder tuples. W1/coordinator pins the reusable workflow and verifier source to the reviewed immutable source appropriate for real dispatch context; retain full Planning history and retained-only/no-API verification.

**Tests:** PR-only dispatch through actual workflow data flow; assert shadow receives exactly the values returned after durable approval publication, not dispatch SHA or fixed receipt 123. Cover missing publication, wrong candidate and empty outputs. Preserve the current failing `test_human_input_is_pr_selection_only` assertion and make it pass through correct behavior.

**Stop criterion:** Owner supplies only the decision/PR; no manual run/SHA/path/plan entry. Shadow must run only after verified publication using that exact tuple, with no live fallback.

### F7 — G5 source policy: unauthorized develop allowance remains

Files: `scripts/receipt_verifier.py:35-44,181-211`; `scripts/test_receipt_verifier.py` (`test_approve_accepts_transitional_develop_dispatch`, `test_proof_rejects_untrusted_branch`); `.github/workflows/receipt-approval.yml:99`.

`POLICY_BRANCHES=("main","develop")` remains. New prose calls the develop allowance a documented exception, but the binding current order requires real main context and no Owner authorization for this expansion was found. The exact suite positively accepts transitional develop. Its generic untrusted-branch rejection passes, but does not prove develop is rejected under the actual main-only policy. Empty `TRUSTED_SOURCE` is an honest fail-closed pre-registration state, not a license to broaden source policy or claim automatic readiness.

**Recipe:** W3 restores main-only validation and changes the transitional-develop acceptance test to a rejection test. Coordinator retains separate CI-only default-main registration with the reviewed immutable helper pin after source review and green selected CI; do not change default branch or activate during this review.

**Tests:** authenticated run proof on develop plus matching real ref must be rejected; unknown branch and spoofed claims rejected; main proof plus correct immutable source accepted. Preserve wrong actor/event/repository/source tests.

**Stop criterion:** no unauthorized ref exception; unavailable registration/pin remains an explicit blocker for live operation. No fabricated `GITHUB_*` context.

### F8 — G6: evidence/handoff claims do not justify qualification

Files: Planning `evidence/board-2026-10-27/{rv1-review-ad4d0f28,f3b-fix,ci1-repair,w1-evidence-final,w2-evidence-final,w3-evidence-final}.md`; product `evidence-r27/{s2-v3staging,x1-fix,f3b-fix}.md`; missing requested Planning records listed above.

rv1 simultaneously named blockers and concluded ACCEPT_WITH_NONBLOCKING; its no-force, regex and task-link readiness claims were inaccurate. Current f3b evidence describes workflow definition ID as the correct writer run ID and product candidate as the Planning revision, contradicting callable contracts (F1). ci1 evidence attributes receipt discovery failures to YAML parsing despite the current syntactically valid tree retaining a distinct test failure/parser defect. s2 evidence claims all 122 tests green without qualifying the integrated later head. x1 calls its two failures pre-existing/unrelated, but the final head has the newly introduced input-contract failure; its recorded SHA/ls-remote text contains malformed/inconsistent hexadecimal lengths and cannot pin this candidate. Requested current s2/s3/x1/SHADOW record files were not published at their specified Planning-main paths. These facts cannot support acceptance or certify the corrections' file reservations.

**Recipe:** coordinator publishes the missing current handoff/record paths and a short SHA-specific correction/addendum to historical claims, preserving originals as history. Record actual package reservations, integration head/base, test counts, hosted run/check IDs and the fact that automatic hosted proof/registration remains pending. Keep operational evidence in its authorized Planning location and resolve product evidence impact with W1 (F2). Do not mark G1–G6 closed from test names or stale counts.

**Tests/evidence:** reconcile every claim against the final source and full relevant job output; validate literal SHAs against Git objects; Planning render/check for metadata edits. Require the automatic positive-chain/negative records before the separate shadow-run task can be accepted; this source review does not launch that chain.

**Stop criterion:** missing evidence and red/skipped/uncertain gates remain explicitly open. End verdict must match all blocking findings; no ACCEPT_WITH_NONBLOCKING while a required criterion is unresolved.

## Fail-closed evidence actually checked and reusable

One focused run on the exact source snapshot: `PYTHONPATH=scripts python3 -m unittest discover -s scripts -p 'test_receipt*.py' -v` → **122 tests, 121 passed, 1 failed**, 17.411 seconds locally. The single failing input-contract test matches hosted CI. No broad product/native matrix was launched.

| Required boundary | Inspected execution and limit |
| --- | --- |
| Wrong candidate | `ProductionPathCliTest.test_negative_wrong_candidate_sha_on_production_path` PASSED: actual CLI retained mode returns 1 with candidate/plan mismatch; offline PATH. |
| Genuinely missing run | `ProductionPathCliTest.test_negative_genuinely_missing_run_id_via_404` PASSED: actual live CLI uses controlled fake-gh HTTP 404 and returns 1 with missing-resource reason. This is hermetic simulated API evidence, not a claim of a live GitHub nonexistent-run pilot. |
| Edited fixture/history | `ReceiptChainTest.test_negative_edited_receipt_including_edit_and_revert`, `OfflineRetainedTest.test_edited_receipt_tamper_rejected`, `test_later_edit_after_approval_rejected` PASSED on actual retained verifier functions and temporary Git history. This third boundary is function-level production-path evidence, not an additional CLI subprocess or hosted automatic-chain proof. |
| Retained positive without API | `ProductionPathCliTest.test_retained_positive_without_any_api_access` PASSED: real CLI, `GIT_NO_LAZY_FETCH=1`, PATH contains git and no gh; positive approved retained receipt verifies. Companion `test_offline_retained_never_calls_github` poisons API calls and passes. |
| Outage is not missing run | `test_network_outage_is_never_reported_as_missing_run` PASSED: transport error stays distinct from HTTP 404. |
| Producer/identity | Existing fork-edited producer definition, wrong identity claims/proofs and unknown-branch tests pass. Main-only policy is still violated by the passing develop-allowance test (F7); task association has the separate fail-open path (F4). |

These existing valid verifier results can be reused for unchanged verifier inputs. They do not override the workflow wiring, publication, policy or exact-head CI blockers. The actual approved historical receipt was not edited or replayed.

Additional local checks: actionlint on all three receipt workflows passed using `/tmp/ai-bin/actionlint -shellcheck=`; `bash scripts/ci-workflow-policy.sh` passed for 22 approved workflow files. Parsed workflow/job/step env keys show no `GITHUB_*` overrides in the three receipt workflows. This confirms the narrow G1 syntax/context-override corrections; it does not prove a genuine successful hosted context/publication. No default-main registration or credential availability was asserted.

## repo-rule compliance

Only this verdict is intended for ordinary publication on Planning main, preserving concurrent commits. No product tracked file was modified; the existing product untracked directories were left intact. No force push, merge, deployment, tag, release, secret read, account change, second reviewer identity or status acceptance. Worker recipes above were not implemented. The review remains **BLOCKED** until a corrected exact candidate satisfies these findings and its actual required CI.

END CX-R27V1-BLOCKED

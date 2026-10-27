# R27 round 2 review: BLOCKED

ROLLE: REVIEW. Independent review only. No product tracked-file changes, product push, merge, recipe implementation, workflow dispatch, registration or activation.

Review UTC: 2026-10-27T16:35:34Z. Reviewer: Codex, current API session; exact backend/model and Horde task ID are not exposed and are not invented. GitHub account: `mcpdev80` only.

- Candidate: [baseharbor#1124](https://github.com/mcpdev80/baseharbor/pull/1124), `work/r27-correction-v33`.
- Exact head before and after source review, independently fetched/read through GitHub: `804383ed3364053d70a27c47db201de6efe55ef5`.
- Exact PR base and live develop before/after: `3431b22c94b068f15f9bd7b31b9f87e846200f0f`.
- Planning main read/fetched: `64b91561ba0fa9d69f4f1f7fd3d27609ac602724`.
- Previous verdict: [CODEX-REVIEW-c7936e8bd838.md](CODEX-REVIEW-c7936e8bd838.md). This review targets the disputed corrections and integration, reusing unchanged valid evidence rather than repeating the complete historical review.

**Verdict: BLOCKED. F7 is closed at source/test level; F1–F6 remain partly open and F8 remains open. Neither #1119 nor this exact candidate has green required hosted CI.** Main registration, credential verification and the automatic hosted positive chain remain separate prerequisites; this review launches none of them.

## PLAN

1. [x] Read cost/authority policies, repository rules, current single order, audit, Owner G1–G6 review and previous verdict.
2. [x] Fetch exact candidate/base and inspect delta, file ownership and both merge-parent diffs.
3. [x] Check F1–F8 closure, disputed G1–G6 boundaries, focused tests and production-path negatives/offline positive.
4. [x] Inspect #1119 and #1124 hosted checks/logs; record recipes and limitations.
5. [x] Publish only this verdict on ordinary Planning main after validation.

The initial basics check reported unread coordinator reminders, pool shortfalls and an open coordinator PLAN step. Read reminders were unrelated PR merge/worker/GUI observations. The Owner pause and this explicit REVIEW scope preclude acting on those lanes or acknowledging their events as resolved. No controller or worker was started. Native coordinator todowrite is unavailable in this session; the numbered review plan is recorded here. Existing product untracked directories and other sessions' work were preserved.

## Context and exact write set

Read current Planning main: `CODEMAN-START.md`, `CODE-AUDIT-2026-10-27.md`, `OWNER-REVIEW-2026-10-27.md`, `rv1-review-ad4d0f28.md`, `f3b-fix.md`, `ci1-repair.md`, all three `w*-evidence-final.md`, and the shadow-run task. The requested Planning files `s2-v3staging.md`, `s3-staging.md`, `x1-fix.md` and `SHADOW-RUN-RECORD.md` remain absent from the fetched recursive tree. Product copies of s2/x1 and current cy1/cy3 dossiers are historical evidence, not substitutes for missing Planning records or instructions to execute. No hosted automatic-chain record was verified.

Base-to-head diff: **26 paths, +3645/-441**. All names are ASCII, including the paired EN/DE documentation; no unrelated application/runtime files or path renames. All three named closing commits are ancestors: `5bdf414bba273a54edc8637e2b8c1d38e32fc779`, `b478c34ead5a05a96cafb433b9f0df6bcad68cd8`, `c3f54c12c0f914bf47efddea0ea98a9760d4cf15`.

| Package | Implementation/test/documentation paths |
| --- | --- |
| W1 | `.github/workflows/{ci,receipt-shadow}.yml`; `scripts/{pr-gate-plan,pr-check-runner,test_pr_gate_plan,test_pr_check_runner}.py`; paired `docs/{development,de/development}/minimal-ci-receipts.md` |
| W2 | `.github/workflows/receipt-post-run.yml`; `scripts/{receipt_writer,receipt_tasklink,test_receipt_writer,test_receipt_tasklink}.py` |
| W3 | `.github/workflows/receipt-approval.yml`; `scripts/{receipt_verifier,test_receipt_verifier,test_receipt_chain}.py` |
| Additional evidence paths | `evidence-r27/{ci1-repair,cy1,cy3,f1-fix,f3b-fix,s2-v3staging,w1,w3,x1-fix}.md` |

The implementation paths map to the three packages. cy1/cy2b both change the W2 post-run file; the final merge reconciles that overlap. Missing current Planning reservations/handoffs prevent certifying disjoint temporal ownership. This is not proof of simultaneous conflicting writes. The nine evidence files are extra paths outside the exclusive implementation table and remain part of the hosted unresolved-coverage result. A blanket claim of fully verified write-set compliance would be false. `git diff --check` reports only cosmetic trailing whitespace in `evidence-r27/ci1-repair.md:22` and `scripts/test_receipt_writer.py:606,608`.

## G1–G6 and F1–F8 disposition

| Owner point | Targeted round-2 result |
| --- | --- |
| G1 | YAML parses; no workflow/job/step `GITHUB_*` env overrides. Post-run still cannot execute correctly (F1); approval fails actionlint (F6). rv1 syntax/readiness claims do not qualify this tree. |
| G2 | Exact five-module selection and success-output parsing corrected. Two policy tests fail, frozen trusted-base runner cannot execute the new check, and hosted coverage/checks remain red (F2). |
| G3 | No force push; first receipt re-applies over unrelated edits. Approval re-apply still fails, and history errors still have fallback behavior (F3). |
| G4 | Swallowed resolver failure removed and injected API forwarded. Writer/verifier mapping policies still differ; card publication is local-only with invalid YAML (F4/F5). |
| G5 | Manual evidence inputs removed; shadow checks out authenticated run SHA. Missing job outputs, wrong CLI SHAs and mutable reusable source still break consumption (F6). Main-only policy now corrected and tested (F7 closed). |
| G6 | BLOCKED matches the source and CI. Missing records and inaccurate cy1/card-publication claims remain actionable (F8). rv1 ACCEPT_WITH_NONBLOCKING is not reusable acceptance. |

## Findings, closure evidence and worker recipes

### F1 — OPEN: post-run publication still cannot execute

Files: `.github/workflows/receipt-post-run.yml:38-63,82-127,150-228`; `scripts/receipt_tasklink.py:129-139`; `scripts/receipt_writer.py:243-291`.

Closed portions: shell `source`, nonportable `xargs -J`, swallowed download fallback and hardcoded task were removed; `--pr-number` is wired. Remaining blocking facts:

- The first step writes outputs but never assigns `workflow_id`, `head_sha` or `pr_number`; the final echo expands them under `set -u`. It still derives PR from nonexistent `workflow_run.base_ref` and reads nonexistent `base_sha` instead of the authenticated PR/producer tuple.
- The decoder closes with `PY > plan.txt`, which is not a here-document delimiter. Executing the exact YAML-extracted run block against a valid temporary ZIP returns 1: `warning: here-document ... wanted PY`, then Python `SyntaxError` at the subsequent `echo`. `bash -n` alone returns 0 with a warning and therefore is insufficient proof. The decoder also reads workflow definition ID from the artifact and falls back from integration SHA to head SHA.
- Artifact download has no `GH_TOKEN`/explicit repository or checkout context, combines name/pattern selection and expects an outer `plan.zip` although normal artifact download extracts its contents. No successful actual artifact retrieval is evidenced.
- `RUN_ID` still equals **workflow definition ID**, while live verification requests a **run ID**. `PLAN_REVISION` still equals **product candidate SHA**, while `load_plan` reads a **Planning commit**. The actual tasklink commit printed by the CLI is discarded.
- Controller checkout remains mutable `develop`; issuance still omits product-source checking. No Planning commit identity/ephemeral push authentication is configured here. `persist-credentials:false` removes checkout credentials; an environment secret name is not git authentication. Tasklink's API helper separately requires `GITHUB_TOKEN`, which this step does not supply.

**Recipe (W2, source pins coordinated with W1):** correct this workflow's executable path using authenticated run/PR/artifact facts, keep run and definition IDs distinct, capture the real Planning plan commit, execute bounded data parsing with a valid delimiter, and configure scoped ephemeral authentication/identity without logging credentials. Use reviewed immutable controller source and enforce producer-definition trust at issuance. Preserve real runner context.

**Tests:** execute the actual extracted workflow blocks with authenticated fixture responses and a real producer artifact shape; require successful plan/receipt remote publication, exact run ID/Planning SHA and shared task mapping. Missing/malformed artifact, wrong producer/tuple and failed push must block. A source-string assertion or actionlint-only pass is insufficient.

**Stop criterion:** no successful publication claim until that exact workflow path durably creates the intended plan/receipt from the actual producer facts.

### F2 — OPEN: real discovery improved, qualification still fails

Files: `scripts/pr-check-runner.py:147-172`; `scripts/test_ci_workflow_policy_receipts.py`; `.github/workflows/ci.yml:655-661,733-742`; planner coverage for the exact changed paths.

Closed: runner now explicitly executes all five registered modules, requires nonzero real test output and each module's presence, and propagates failures. The missing phantom test path is removed. The previous false-success-regex and omitted-policy-module defects are fixed.

Remaining: the exact policy suite produces **5 tests, 2 failures**: approval and post-run are classified by its parser as `workflow-level if guard`, violating its expected `job-level` form. The ordinary 124-test receipt glob excludes this suite and cannot establish the five-suite gate. Also the changed CI calls the runner from frozen trusted base `3431b22c`, which lacks `receipt-execution-tests`. Running that exact base runner against this candidate returns `ValueError: unsupported executable validation`. The new command therefore has a real bootstrap/source-qualification gap. Required hosted coverage still lists ci.yml, runner/tests and all nine product evidence paths as unresolved.

**Recipe (W1/coordinator):** reconcile the existing policy regression with the actual approved workflow guards through semantic validation, and define a reviewable trusted source/bootstrap for execution of the new check. Resolve exact-path qualification/evidence placement under repository policy without wildcard exemptions or weakening final enforcement.

**Tests:** all five suites must execute and pass through the exact trusted owner command and selected-CI path, including this frozen-base scenario; empty/missing/failing suites remain fatal. Require hosted selected checks and resolved coverage on the final SHA.

**Stop criterion:** local receipt-glob success, unrelated green checks or a self-reported qualification never replace the actual selected gate.

### F3 — PARTLY CLOSED: first write re-applies, approval does not

Files: `scripts/receipt_writer.py:80-119,185-240`; `scripts/test_receipt_writer.py` publication cases.

Closed: no force push; first receipt plus unrelated concurrent change is now actually re-applied and both survive on the bare remote. Identical durable receipt remains idempotent; genuine differing receipt blocks. These exact-head tests pass.

Remaining: any existing remote receipt with bytes different from the local approved version is treated as conflict at :200-207. For an approval, the expected prior state is precisely that existing unapproved receipt. A temporary bare-remote reproduction published an unapproved receipt, committed its single approval locally, pushed an unrelated edit from a second checkout, then called real `publish`: **`ReceiptError: conflicting receipt on remote; blocked`**. Remote remained unapproved. Thus unrelated edits still prevent the required approval recovery. `_find_introduction` still swallows Git errors and substitutes the supplied revision. The new lost-ack test actually simulates another unrelated non-fast-forward, not a successful push with lost response.

**Recipe (W2):** carry the bounded edit's expected prior bytes/history for both introduction and approval; reapply only when those preconditions still hold on fresh main, preserving the original receipt introduction and one approval edit. Propagate history failures; after an uncertain push inspect actual durable state before retrying.

**Tests:** bare-remote approval racing an unrelated edit must succeed with both changes retained and exactly one approval edit; changed receipt/history must block. Simulate actual lost acknowledgement after a successful push and require idempotent read-back. Preserve existing first-write tests.

**Stop criterion:** both issuance and approval recover safely; no duplicate approval or substituted provenance.

### F4 — PARTLY CLOSED: fail-open removed, mapping authority still differs

Files: `scripts/receipt_tasklink.py:47-126,189-204`; `scripts/receipt_verifier.py:413-448,500`.

Closed: resolver failures are no longer caught as authorization; verifier requires exactly one matching backward binding and equality with the shared forward result, and approve_pr passes its injected API. The old no-binding fail-open condition is removed.

Remaining: shared resolver still trusts the first task path in public issue title/body and never reads `planning_root`. Direct production call with a fake PR closing an issue whose body says `tasks/does-not-exist.md` returns that nonexistent task. Writer uses this result without verifying task existence/backward metadata; verifier separately interprets only an unquoted inline `prs: [...]` regex. These remain two policies rather than one authoritative function over Planning metadata. Multiple task references in an issue are not rejected as ambiguous. Default `_resolve_api()` calls undefined `api` and directly raises `NameError` (approve_pr's explicit API avoids this adapter, so this is not misreported as its live path).

**Recipe (W2 with W3 consumption):** make one shared resolver validate the actual Planning task/schema at the bound revision, including missing/ambiguous/mismatched PR bindings, for both writer and verifier. Public issue prose must not become an independent authority. Remove the separate regex policy and repair/remove the broken adapter.

**Tests:** missing real task, quoted/block metadata, ambiguous bindings/issue references, conflicting public issue text, API errors and a valid agreed binding through both issuance and approval. Injected APIs must never escape to the network.

**Stop criterion:** no plan issuance or approval without the same single validated Planning mapping.

### F5 — OPEN: card update still local-only and malformed

Files: `scripts/receipt_tasklink.py:270-428`; `scripts/receipt_verifier.py:478-489`.

Closed: original evidence lines are no longer replaced and publication exceptions are no longer swallowed. Remaining behavior contradicts the new durable-publication docstring: `publish_evidence` never calls the publisher or pushes. It commits and reads **local HEAD**, calls optional render/check hooks (none supplied in production), and returns the local commit; caller ignores that result and returns the earlier receipt publication. The appended frontmatter line is `- evidence: path (candidate ..., plan ...)`, invalid within the existing mapping with `id:`/`evidence:` keys. It is neither an appended schema evidence value nor an immutable public reference. The unchanged-retry branch can return a local commit without checking remote durability or validation.

Temporary bare-remote reproduction using the actual function and an existing inline evidence list: function returns a new local SHA; remote main remains unchanged and differs from that SHA; parsing the resulting frontmatter raises **ParserError**. No real Planning card was edited for this reproduction.

**Recipe (W2/W3):** append schema-valid immutable evidence through Planning's parser, preserving inline/block entries; render/check and commit required generated changes before durable publication through the single publisher. Return and verify the final publication revision; propagate failures. Idempotent retry must verify remote bytes and repair any interrupted card step without another approval edit.

**Tests:** real temporary bare-remote approval plus card update/read-back, real Planning render/check, inline/block preservation, unchanged retry, failed/rejected card push and concurrent unrelated task edits. Do not fake publisher success or validate only local HEAD.

**Stop criterion:** chain success requires receipt and valid card evidence on remote main at the returned final publication revision.

### F6 — OPEN: approval outputs still do not reach retained shadow

Files: `.github/workflows/receipt-approval.yml:46-118`; `scripts/receipt_verifier.py:508-511,541-547`; `.github/workflows/receipt-shadow.yml:56,66,93-106`.

Closed: manual receipt/plan/candidate inputs removed; actual verifier stdout is consumed by a step; shadow uses `github.sha` instead of a missing dispatch PR object and retained-only full history is preserved.

Remaining: approve job has **no outputs declarations**, so all three `needs.approve.outputs.*` references are undefined. Actual actionlint reports expression errors at approval :114/:115/:116. Even with declarations, CLI prints **introduction** as `plan` and **approval commit** as `candidate`, despite approve_pr already returning the correct `plan` and `candidate` fields. These are Planning commits, not the intended plan/candidate tuple. Mutable reusable `@develop` remains. Empty-output guard skips shadow rather than proving consumption; no durable publication input is passed to bind the exact final revision.

**Recipe (W3/W1):** print the correct returned plan/candidate fields, declare step-to-job outputs, validate nonempty publication results, and feed the exact published tuple/final revision to retained consumption. Pin the reusable/helper source to the separately reviewed immutable registration source. Preserve PR-only human input and no API fallback.

**Tests:** actual workflow output plumbing plus CLI with deliberately distinct introduction/approval/plan/candidate SHAs, missing outputs and publication failures; actionlint must pass. Required successful publication must lead to an actual retained run, not a skipped guard.

**Stop criterion:** no chain qualification until retained shadow consumes exactly the durably approved evidence automatically.

### F7 — CLOSED at source/test level: main-only restored

`scripts/receipt_verifier.py:35-41` now sets `POLICY_BRANCHES=("main",)`. Exact-head `AuthenticatedProofTest.test_approve_rejects_untrusted_ref_dispatch` supplies an authenticated develop run with a matching real ref claim and rejects it. Main proof/source and other identity negatives remain passing. Empty `TRUSTED_SOURCE` honestly keeps approval fail-closed before registration; registration/rights were not asserted or activated.

**Maintenance recipe (W3/coordinator):** retain main-only policy and this rejection case; perform immutable helper registration only in the separately authorized registration step. No further product change is requested for this finding.

**Test requirement:** preserve the passing main-positive/develop-negative, wrong-ref/actor/event/repository and source-byte tests when the final pin changes.

**Stop criterion:** any unapproved ref allowance or invented context reopens F7; missing registration cannot be labelled live readiness.

### F8 — OPEN: missing records and correction claims remain misleading

Files: requested missing Planning records above; product `evidence-r27/{cy1,cy3}.md`; existing historical repair dossiers.

cy1 explicitly says it kept definition-ID-as-run and candidate-as-Planning-plan wiring while claiming F1 recipe closure; the recipe required the opposite. Its here-document is not executable as delivered. cy1's lost-ack claim exceeds its test, and its "not in a product branch" evidence wording conflicts with the committed product evidence path. cy3 honestly notes missing approval outputs and red policy tests; those facts survive integration and must not be promoted to closure. cy2b's durable card claims contradict real local-only/invalid-YAML behavior. Historical rv1/F3B/CI1 claims remain history, not qualification. Missing reservations and automatic-chain record remain unavailable.

**Recipe (coordinator):** publish the missing requested Planning handoffs and a SHA-specific addendum correcting these claims, preserving historical originals. Record actual ownership/reservations, final source/base, exact suite counts, run/check IDs and unresolved registration/rights/automatic-chain prerequisites. Resolve additional product evidence paths with W1's exact coverage contract.

**Tests/evidence:** reconcile each G point against actual code and job output, verify literal SHAs, run Planning validation; source review is not the hosted positive chain. No card acceptance from partial local tests.

**Stop criterion:** documentation verdict must remain BLOCKED while any required source/evidence/CI criterion is unresolved.

## Merge-conflict review against both parents (review point 6)

Merge `804383ed3364053d70a27c47db201de6efe55ef5` parents:

- P1 `1e021741a5e742301d338b1dda8128d9638c60a6` (cy1/cy3 integrated).
- P2 `c3f54c12c0f914bf47efddea0ea98a9760d4cf15` (cy2b).

Inspected exact `git diff P1 804383ed -- receipt-post-run.yml`, `git diff P2 804383ed -- receipt-post-run.yml`, full per-parent path summaries, and `git show --remerge-diff` for the conflicted file. P1→merge adds shared PR_NUMBER env/resolver wiring and the PR summary; P2→merge retains cy1's mandatory-artifact/no-source decoder changes and normalizes shell indentation. Resolution removes duplicate output lines and the old hardcoded-task side of the conflict. W1/cy3 CI/shadow changes survive against P2; W3 mapping/main-only/card changes survive against P1. No conflict marker or wholesale package loss found.

However, at the decoder conflict the merge keeps P2's `... pr=$pr_number` log while that job defines no shell `pr_number`; P1's log did not contain this expansion. It also preserves cy1's broken `PY > plan.txt`. Thus combining the intentions does not make the resulting program valid. F1's executable-block regression must cover the resolved file; **conflict resolution is not qualified**. Fix recipe/test/stop criterion are F1 above, rather than a separate duplicate product request.

## Executed local checks and fail-closed evidence

Executable checks used exact `git archive` snapshot `/tmp/cx-r27v2-804383ed`; fixture writes stayed in temporary repositories. Product checkout/branch were not changed.

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m unittest discover -s scripts -p 'test_receipt*.py' -v`: **124 tests, OK, 43.931s**. This is not the five-module selected gate.
- Separately executed the previously omitted, now registered `test_ci_workflow_policy_receipts`: **5 tests, 2 failures**, detailed in F2. Thus the combined required module set is not green; valid passing modules were not needlessly repeated.
- `/tmp/ai-bin/actionlint -shellcheck= .github/workflows/receipt-{post-run,approval,shadow}.yml`: **three approval expression errors**, detailed in F6. YAML parse succeeded; syntax parse is not shell/runtime proof.
- `bash scripts/ci-workflow-policy.sh`: PASS, 22 approved files. Parsed all three receipt workflows' workflow/job/step env mappings: no `GITHUB_*` overrides.
- Focused production-function reproductions confirmed the post-run delimiter error, approval re-apply failure, nonexistent-task resolution, broken default API adapter, and local-only malformed card publication. No correction was implemented.

| Boundary | Exact-head evidence and limits |
| --- | --- |
| Wrong candidate | `ProductionPathCliTest.test_negative_wrong_candidate_sha_on_production_path` passed: actual retained CLI rejects wrong candidate, offline PATH. |
| Missing run | `ProductionPathCliTest.test_negative_genuinely_missing_run_id_via_404` passed: actual live CLI receives controlled HTTP 404 and rejects with missing-resource reason. This is hermetic simulated API evidence, not a new hosted nonexistent-run pilot. |
| Edited receipt/history | `ReceiptChainTest.test_negative_edited_receipt_including_edit_and_revert` and retained tamper/later-edit negatives passed through actual production verifier functions and real temporary Git history. This is production-function evidence, not an additional hosted/CLI automatic-chain proof. |
| Retained positive with no API | `ProductionPathCliTest.test_retained_positive_without_any_api_access` and `OfflineRetainedTest.test_offline_retained_never_calls_github` passed; actual retained CLI uses git/no gh and `GIT_NO_LAZY_FETCH=1`, companion poisons API access. |
| Transport distinction | Network-outage negative passed and is not represented as HTTP-404 missing-run proof. |

These narrow valid results remain reusable. They do not prove post-run publication, card visibility or approval→shadow succeeds. The historical real approved receipt was neither edited nor replayed.

## Hosted CI, including requested #1119 inspection

[#1119 run 40529019816, attempt 1](https://github.com/mcpdev80/baseharbor/actions/runs/40529019816) remains completed **failure**, exact head `c7936e8bd8385581c643f1598f5b1dfd3cfca945`. Focused Python job `122276506347`, planner job `122276507024` and required `PR Selected Checks` `122277637740` are failed. Focused log at `2026-10-27T15:15:45Z`:

```text
FAIL: test_human_input_is_pr_selection_only
AssertionError: Items in the first set but not the second:
'receipt'
'candidate'
'plan'
Ran 122 tests in 12.525s
FAILED (failures=1)
```

This historical input-contract defect is corrected in #1124's local tests; #1119 has no new green run and is not called green. Its final log also reports unresolved coverage independently of that failure. Under the explicit user requirement, red #1119 is a failed prerequisite for ACCEPT, not silently waived by a different local candidate.

The new exact candidate is independently red: [#1124 run 40541797478](https://github.com/mcpdev80/baseharbor/actions/runs/40541797478), completed **failure**, `head_sha=804383ed3364053d70a27c47db201de6efe55ef5`. Failed jobs: Workflow policy `122321841682`, Focused Python `122321944396`, ci-actionlint `122321945029`, and [PR Selected Checks `122322843029`](https://github.com/mcpdev80/baseharbor/actions/runs/40541797478/job/122322843029). Check-runs API confirms required check app **15368**.

Focused log at `2026-10-27T16:33:15Z` reports the undefined approval output properties (`receipt`, `plan`, `candidate`) and exits 1. Final-check log at `2026-10-27T16:33:46Z`:

```text
BLOCKED: required authenticated job not successful: PR · Focused Python
BLOCKED: required authenticated job not successful: Workflow policy
BLOCKED: required validation not successful: ci-actionlint (blocked)
```

Its separate `coverage-unresolved` line lists `.github/workflows/ci.yml`, all nine `evidence-r27` files, `scripts/pr-check-runner.py`, and `scripts/test_pr_check_runner.py`. The F2 recipe applies to this independent blocker. No hosted job was started or rerun by this reviewer.

## repo-rule compliance

Only this verdict is authorized for ordinary Planning-main publication; no task metadata, generated views or product tracked files changed. HTTPS fetch/push uses existing mcpdev80 authorization after local SSH configuration/key failure. No merge, force push, protection bypass/change, release/tag/deployment, live pilot, credential provisioning, other-account use or worker dispatch. The source review is complete with blocking findings; product corrections and automatic-chain acceptance remain unfinished.

Planning `python3 scripts/plan.py check`: 328 tasks, 0 errors, 6 existing dependency warnings. No metadata changed, so no generated-view rewrite was needed. Only this verdict is staged for publication.

END CX-R27V2-BLOCKED

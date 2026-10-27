# R27 v3.8 independent review — BLOCKED

ROLLE: REVIEW. Exact candidate `cb7d821302b239bb04172527b2716f361afd79e5`, [PR #1138](https://github.com/mcpdev80/baseharbor/pull/1138), branch `work/r27-correction-v38`; protected base `3431b22c94b068f15f9bd7b31b9f87e846200f0f`. No product correction or merge.

**Verdict: BLOCKED. F1–F6 remain PARTLY; F8 remains OPEN. The suite-order regression is CLOSED. All requested local suites pass, but actual publication, transaction, mapping and card counterexamples remain. Hosted Class B is a separate bootstrap prerequisite, not a new implementation defect attributed to this candidate. D1–D3 remain PARTLY.**

## PLAN

1. [☑] Read binding policies, repository rules, R4 verdict/copy, d4/d5, publisher correction/addendum, CODEMAN-START and release context; verify live account/head/base.
2. [☑] Compare complete candidate and v3.6/v3.7 deltas; separate trusted-base prerequisite from source defects.
3. [☑] Execute receipt/planner/runner/policy/actionlint checks and bounded R4 counterexamples.
4. [☑] Record F1–F6/F8 and D1–D3 with locations, executed proof and correction recipes.
5. [☑] Validate Planning and publish ordinary main with remote read-back.

Reviewed 2026-10-27 UTC / 2026-10-28 Europe/Berlin. Reviewer: Codex, this independent API session; model/backend/session IDs and Horde task ID are not exposed and are not invented. GitHub account verified as `mcpdev80`; no second account. `HORDE_WORKER_TOKEN` is unset. Planning baseline `5c8a6e3c5f14ec5c8f009c2ef633a85958dc6c5c`. Publisher owner remains `w2-lane`, state review; contract dependency accepted, release-updates dependency NOT accepted. This review neither takes its claim nor changes task acceptance/status.

## Exact identity, patch overlap and regression scope

All supplied chain SHAs and R5 integration `8d12fbb40e4885d9e5b80cde949dd46ac9c60a05` are actual ancestors. Complete protected-base diff: **36 files, +5825/-456**. Snapshot from exact `git archive`: `/tmp/cx-r27v5-cb7d8213`; existing product worktrees remain untouched.

- v3.6 `27507add` → v3.8: only two added evidence files (`w5.md`, `r5i.md`) and one line in `scripts/pr-check-runner.py:107`, ordering policy before tasklink to match canonical registry/test.
- v3.7 `cdddf21d` → v3.8: **only `evidence-r27/r5i.md`, +81 lines**. R5's executable patch overlaps the already integrated w5 fix. No new executable regression in that delta.
- Writer, tasklink, verifier and three receipt workflows are **byte-identical to R4's exact v3.6 source**. [Ancestry, hashes and current producer facts](cx-r27v5-cb7d8213/source-and-artifact.json) record this. R4's remaining findings cannot be dismissed as pre-v3.6; current probes reproduce them independently.
- New evidence regression: `evidence-r27/r5i.md:36-40,63,69-70` wrongly says F1/F3/F4/F6 were already fixed and R4 concerned a pre-v3.6 head. See F8.

The [R4 verdict](CODEX-REVIEW-27507add.md) supplies unchanged full-diff context. This review adds actual exact-head checks and counterexamples; it does not repeat unchanged review merely to obtain another verdict.

## Actually executed suites

Commands ran in the exact source snapshot. All four checks below returned rc=0. [Logs](cx-r27v5-cb7d8213/) retain actual execution.

| Command/check | Actual result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m unittest -v test_receipt_writer test_receipt_verifier test_receipt_chain test_receipt_tasklink test_ci_workflow_policy_receipts test_receipt_postrun` | **175 tests OK**, 29.533s: writer 24, verifier 104, chain 6, tasklink 30, receipt policy 5, postrun 6. [Log](cx-r27v5-cb7d8213/receipt-tests.log). |
| `PYTHONDONTWRITEBYTECODE=1 GOCACHE=/tmp/cx-r27v4-gocache PYTHONPATH=scripts python3 -m unittest -v test_pr_gate_plan test_pr_check_runner` | **162 tests OK**, 101.516s: planner-loaded 140 (including 9 registration tests), runner 22. Subsequent child runtime-script summaries 8/7/5 OK are not extra root-suite totals. [Log](cx-r27v5-cb7d8213/planner-tests.log). |
| `bash scripts/ci-workflow-policy.sh` | **PASS**, 22 approved workflows; [log](cx-r27v5-cb7d8213/policy.log). The five Python receipt-policy tests actually ran above. |
| `GOCACHE=/tmp/cx-r27v4-gocache GOPATH=/tmp/cx-r27v4-gopath go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.12 -shellcheck= .github/workflows/receipt-post-run.yml .github/workflows/receipt-approval.yml .github/workflows/receipt-shadow.yml` | **PASS**, empty [diagnostics](cx-r27v5-cb7d8213/actionlint.log). Explicit files support an archive snapshot; shellcheck disabled as in CI. |

Executed bounded probes from Planning: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/board-2026-10-27/scripts/cx-r27v5-probes.py /tmp/cx-r27v5-cb7d8213`; [script](scripts/cx-r27v5-probes.py), [results](cx-r27v5-cb7d8213/probes.log). Harness rc=0 means counterexamples were captured, not that production passed. All Git mutations use temporary bare remotes. Also executed `python3 evidence/board-2026-10-27/scripts/cx-r27v5-pin-probe.py ../baseharbor /tmp/cx-r27v5-cb7d8213`; [script](scripts/cx-r27v5-pin-probe.py), [result](cx-r27v5-cb7d8213/pinned-interface.log).

The green suites preserve API-forbidden retained verification, genuine missing-run versus outage, wrong candidate, tampered history, producer source, main/develop identity and distinct output cases. These are useful bounded proofs; actual workflow/transaction failures below remain outside that passing coverage.

## Exact-head hosted CI and separate bootstrap chain

One branch run observed: [40600616015](https://github.com/mcpdev80/baseharbor/actions/runs/40600616015), pull_request, exact candidate, completed **failure**. No rerun/dispatch/activation performed. Captured hosted logs have trailing whitespace normalized; job URLs identify original logs.

| Hosted job | Result |
| --- | --- |
| [Focused Python / 122527582726](https://github.com/mcpdev80/baseharbor/actions/runs/40600616015/job/122527582726) | **failure**. Planner 138 OK, diff 13 OK, runner 22 OK and other displayed suites pass. Afterwards protected-base runner **3431b22c**, :107, raises `unsupported executable validation` for `receipt-execution-tests`. [Log](cx-r27v5-cb7d8213/host-focused.log). |
| [pr-planner-tests / 122527582930](https://github.com/mcpdev80/baseharbor/actions/runs/40600616015/job/122527582930) | **success**, 140 tests OK; nested 8/7/5 OK. R4 order assertion is fixed. [Log](cx-r27v5-cb7d8213/host-planner.log). |
| [PR Selected Checks / 122528403732](https://github.com/mcpdev80/baseharbor/actions/runs/40600616015/job/122528403732) | **failure**, exact head, GitHub Actions App **15368**. Failed Focused Python plus coverage-unresolved. [Log](cx-r27v5-cb7d8213/host-selected.log). |
| Workflow policy, ci-actionlint, executor-verifier, ci-policy, docs audit, EN/DE mkdocs, Pages candidate | **success**. Skipped native/runtime/public-contract/consumer jobs are not PASS evidence. |

**Class A:** d4's three missing-origin errors and two guard assertions remain closed; R4's suite-order failure is now closed. No current observed Class A unittest failure. Remaining F1/F3/F4/F5/F6 production defects are substantive counterexamples outside passing suite coverage, not a failing hosted unittest falsely blamed on Class B.

**Class B:** `.github/workflows/ci.yml:655-660,733-738` uses protected-base runner bytes; that runner lacks the new check. Final coverage also remains unresolved for **21 paths**: ci.yml, 16 added evidence-r27 files, evidence/g1/evidence-r27/g1.md, runner/test runner and test_receipt_postrun.py (unknown to base planner). This belongs to the separately assigned bootstrap prerequisite; the correction candidate must not self-qualify or bypass it.

Live develop remains `3431b22c…`. No open bootstrap/bx1 PR was discoverable in the live inventory at inspection; the user's bx1 preparation is a pending prerequisite, not an accepted protected-base change. Required chain: separately review bounded develop-based bootstrap → actual required CI and authorized integration → verify protected runner capability and complete trusted qualification → evaluate correction/current integration with exact hosted evidence. A changed candidate requires review of its changed scope. No unconditional future green is inferred.

**BLOCK / prerequisite recipe — bx1/integration owner:** deliver trusted planner/runner/CI bootstrap and complete-diff qualification through their existing owners without wildcard exemptions or candidate-authored authority. **Tests:** actual nonempty receipt execution, missing/empty/failing suites, and missing/partial/stale/changed-integration qualification negatives. **Stop criterion:** F2/acceptance stays open while protected capability, coverage or required Selected Checks is red/unverified. This is a prerequisite gate, not a new candidate source defect or permission to skip CI.

Current trusted-pr-plan artifact **12778097022**, **1414 bytes**, contains only **pr-plan.json**, no nested plan.zip. Head `cb7d8213…`, base `3431b22c…`, integration `fe14632b93be827b0a5011b5e0c6f68a32191190`; no run_id/attempt/workflow_id. [Retained ZIP](cx-r27v5-cb7d8213/trusted-pr-plan.zip). This failed producer's artifact proves format only; it is not issuance-eligible PASS evidence.

## F1 — PARTLY: actual post-run path cannot issue/publish

**Locations:** `.github/workflows/receipt-post-run.yml:81-108,110-164,185-205,223-297`; `scripts/receipt_verifier.py:90-147`; `scripts/receipt_writer.py:305-341`; `scripts/test_receipt_postrun.py:48-76,275-318`.

**Executed proof:** fresh actual decoder shell fails `ModuleNotFoundError: receipt_verifier`. Supplying import/assumed ZIP layout only for diagnosis exposes actual current producer format failure `run_id must be a positive integer`. Actual writer CLI rejects YAML's `--product`, rc=2. These reproduce independently of Class B.

Download still uses nonexistent `gh download artifact`, missing command token/repository and wrong nested ZIP shape. Decode job has no helper checkout/import path. PR resolution still reads absent `workflow_run.base_ref`, without the commented PR API call. Artifact is required to invent authenticated IDs absent from producer output. Publish job never exports tasklink GITHUB_TOKEN or writer write token; persist-credentials:false cannot supply push auth. write_and_publish cannot forward product. Controller remains pinned to **839e5cc9** at YAML :193. Job rename, identity, attempt guard and preliminary revision plumbing remain real improvements.

**BLOCK recipe — W2, pins coordinated by integration owner:** repair actual download/producer format, derive authenticated run/attempt/workflow/PR facts and bind source tuple; set up reviewed helpers per fresh job and explicitly wire narrowly scoped credentials to subprocesses. Add/forward product in existing CLI/functions; select corrected immutable helper source. Do not require invented producer IDs.

**Tests:** actual facts/download/decode/tasklink/**publish shell/CLI** using real artifact shape, distinct IDs/SHAs, controlled API and fresh bare Planning remote; no inherited import/token context or prepublished plan. Missing credentials/download/PR/source must fail before publication. **Stop criterion:** selected workflow successfully publishes authenticated receipt with durable referenced plan ancestry; mocked function success is insufficient.

## F2 — PARTLY: suite-order defect CLOSED; bootstrap pending

**Locations:** `scripts/pr-check-runner.py:105-109,148-173`; `scripts/pr-gate-plan.py:662-681,1393-1421`; `scripts/test_pr_gate_plan.py:3541-3587`; `.github/workflows/ci.yml:655-660,733-738`.

**Executed proof:** 175 receipt and 162 planner/runner tests OK, actual coupling test passes; hosted planner 140 OK. Six explicit suites, missing/empty/failing-suite controls, unique class names and removal of unsafe candidate-owned fallback remain intact. No candidate-side ordering correction remains.

**BLOCK recipe/tests/stop criterion:** complete the separate Class B prerequisite chain above, preserving canonical list/fail-closed checks. Close only after protected executor capability, complete trusted qualification and exact required hosted checks succeed. Do not label pending bootstrap as a new source defect in cb7d8213.

## F3 — PARTLY: retry loses plan and rejects approval recovery

**Locations:** `scripts/receipt_writer.py:136-165,168-276,279-289`.

**Executed proof:** real new-plan+receipt racing unrelated push returns success, but remote plan file is absent and plan commit **not reachable**; unrelated edit survives. Legitimate approval plus unrelated push fails `conflicting receipt on remote; blocked`. Recovery resets/reapplies receipt only. Uncertain transport failures are raised before durable-state recovery; introduction history errors still fall back to supplied revision. Green receipt-only recovery does not prove the transaction.

**BLOCK recipe — W2:** preserve bounded plan-plus-receipt transaction and ancestry; permit the sole approval edit only against exact expected predecessor while preserving introduction identity; inspect durable state after uncertain push; propagate history errors.

**Tests:** new unpublished plan/receipt plus unrelated writer retains both and ancestry; approval race succeeds exactly once; conflicting predecessor blocks; push-with-lost-response read-back recovers without second approval; invalid history fails. **Stop criterion:** both issuance and approval recover with reachable plan and exactly one approval edit; receipt-only success does not close F3.

## F4 — PARTLY: issuance trusts issue prose; parsers disagree

**Locations:** `scripts/receipt_tasklink.py:47-126,189-204`; `scripts/receipt_verifier.py:482-552`; Planning `scripts/plan.py:78-79`.

**Executed proof:** issuance resolver returns tasks/nonexistent.md for nonexistent Planning root based on issue prose. Duplicate prs metadata is silently accepted with last-value semantics by approval parser, while actual Planning parser rejects duplicate frontmatter key prs. Quoted/block association and injected API tests remain green but do not prove common schema authority at a bound revision.

**BLOCK recipe — W2/W3:** one Planning-schema-aware revision-bound resolver for issuance/approval, enforcing existing task, unique forward/backward association and ambiguity rejection. Issue prose is reference data; reject duplicate/unsupported metadata.

**Tests:** nonexistent/mismatched/ambiguous task, multiple task references, duplicate keys, valid quoted/inline/block metadata and API errors; both consumers agree at bound revision and injected API never escapes to network. **Stop criterion:** neither consumer proceeds without the same unique validated Planning association.

## F5 — PARTLY: destructive card publication precedes validation

**Locations:** `scripts/receipt_tasklink.py:304-319,416-477,481-509`; `scripts/receipt_verifier.py:565-592,635-658`; `scripts/test_receipt_verifier.py:1299-1343`.

**Executed proof:** actual inline/block card publication pushes successfully but actual Planning parser rejects duplicate evidence key. Both lose block prs; block form also loses old evidence. PyYAML returns mapping-valued evidence rather than canonical URL strings. Validation remains optional and after push; generated outputs are not staged. Identical local bytes return without remote confirmation, and receipt-only recovery cannot reapply an existing card safely. Immutable public link/final publication plumbing, SHA guards and origin fixtures remain useful closed subparts.

**BLOCK recipe — W2/W3:** edit canonical metadata via real Planning parser/serializer; preserve all list forms and one string-valued evidence list. Mandatory render/check and generated staging before commit/push. Implement bounded card publication reconciliation, durable idempotent read-back and exact final receipt+card revision in existing path.

**Tests:** actual parse/render/check, old evidence/PR lists preserved, validation failure leaves remote unchanged, rejected push then identical retry durably publishes, unrelated writer preserved, returned revision contains approved receipt and valid card/generated views. Preserve push-failure negatives. **Stop criterion:** schema-valid additive evidence must be durable at returned publication; push/string presence alone is insufficient.

## F6 — PARTLY: output plumbing repaired; selected reusable source incompatible

**Locations:** `.github/workflows/receipt-approval.yml:83-125,135-144`; `.github/workflows/receipt-shadow.yml:46-49,66-78,110-124`; `scripts/receipt_verifier.py:679-681,708-729`.

**Executed proof:** parsed actual pinned reusable schema at **f57b30ed** exposes candidate/plan/receipt only; current caller supplies unsupported **publication**. Local actionlint does not validate that remote interface. Head's distinct outputs and retained-at-publication tests pass. TRUSTED_SOURCE is empty, honestly blocking premature activation. Shadow checkout uses github.sha (caller registration source); workflow-only main registration does not automatically contain corrected verifier helpers.

**BLOCK recipe — W1/W3/integration owner:** after source correction/review, bind compatible immutable reusable schema, helper source and trusted-source policy; prepare separately authorized CI-only main registration and credential verification. Preserve real main identity and Owner PR-only decision input.

**Tests:** validate call against selected pinned schema; execute that actual consumer/helper with distinct tuple values and exact final publication, API forbidden; missing outputs/publication fail; preserve actionlint and identity negatives. **Stop criterion:** incompatible pins or unresolved helper/registration provenance cannot qualify chain. This review authorizes no activation.

## F7 — CLOSED at source/test level

`scripts/receipt_verifier.py:44-50,248-278` remains unchanged; actual green suite includes main-positive/develop-negative, repository/actor/producer-source boundaries. Preserve them during pin/registration work. Context substitution or weakened identity reopens F7; source closure is not live-chain qualification.

## F8 — OPEN: R5 evidence incorrectly dismisses live R4 findings

**Locations:** `evidence-r27/r5i.md:36-40,63,69-70`; `evidence-r27/w5.md:5-6,36-38`; prior claims `g1x.md:76-90,g1y.md:55-99,g2x.md:4-9,w4b3.md:39-46,132-138`; `scripts/test_receipt_postrun.py:48-76,275-318`.

**Executed proof:** hashes prove equality with R4-reviewed v3.6 and probes reproduce remaining blocks. R5's pre-v3.6 explanation is false. Six postrun tests invent artifact IDs/base_ref, supply PYTHONPATH, reuse prepublished plan and call writer functions instead of actual publish shell. They do not establish automatic E2E. w5's local postrun pass cannot establish absence of hosted unknown-impact; current final log still reports it. Suite-order repair is valid; “only live defect” exceeds evidence.

**BLOCK recipe — coordinator/workers:** publish explicit corrective addendum with exact source, actual counts/scope, counterexamples, CI and bootstrap/credential/registration/chain prerequisites. Preserve historical records; correct misleading proof assertions/tests without weakening behavior. Never accept cards from package DONE or commit-presence claims.

**Tests/evidence:** valid Planning references and actual hosted producer → postrun publication → Owner decision → approval/card → retained consumption; controlled wrong-candidate, genuine-missing-run and tampered-history negatives, API-forbidden retained positive. **Stop criterion:** no skeleton/card acceptance while source blocks, required CI or automatic-chain prerequisites remain unresolved. This verdict corrects current evidence; it does not accept the chain.

## D1 / D2 / D3 final and Owner addendum

| Directive | Final disposition on cb7d8213 |
| --- | --- |
| D1 run versus workflow-definition ID | **PARTLY / BLOCKED.** Correct naming/attempt guard at postrun :84-95,273-295. Extractor :136-143 requires IDs absent from actual artifact, ignores shell authenticated run, accepts forged run 999. Apply F1 authenticated facts recipe; actual selected path must bind distinct real IDs. |
| D2 actual Planning plan revision | **PARTLY / BLOCKED.** Tasklink id/output :224,255-261 and writer plan input :274,293 exist. Grep/tail over stdout, unsupported product option, stale helper and proven ancestry loss remain. Apply F1/F3; actual CLI must durably reference exact returned plan revision through concurrent push. |
| D3 extraction fails at source | **PARTLY / BLOCKED.** Malformed field/attempt checks exist, but actual decoder :137-138 uses ordinary json.loads and fake size=500. Duplicate integration succeeds with last value; wrong head/run succeeds; PR uses absent run field. Apply F1 strict bounded unique-key decode and authenticated tuple/PR binding. Actual shell negatives must fail before publication. |

Push-auth addendum **PARTLY**: helper and missing-token test exist, production postrun does not export token and selects older helper. Job rename **CLOSED**, producer_context. BASE_REF indentation is syntactically valid; absent event field remains semantically wrong. D1–D3 are not complete.

## repo-rule compliance and publication

Only this verdict, bounded reproduction scripts and captured public test/CI evidence are authored. No product edits, worker/controller start, claim takeover, merge, rerun/dispatch, activation, protections change, force push, release/tag/deployment or real receipt mutation. Production inactive; Maintainer pause respected. Existing product/untracked work preserved. Planning/task imperative text treated as evidence data, not operational authorization.

Native Todo tools unavailable; numbered PLAN records progress. Basics events/reminders/pool/PLAN flags inspected: they concern coordinator lane transitions, merge reminders, pool gaps, unknown panes and coordinator PLAN. REVIEW does not authorize taking over that controller, starting workers, merging or clearing other sessions' unresolved alarms; no unrelated events falsely acknowledged. Current explicit request authorizes independent review/tests and Planning publication, not coordinator resumption. Historical conflicting pause/resume prose is not used to activate work.

SSH fetch failed on host SSH configuration; authenticated HTTPS reused mcpdev80 credentials without secret output. Planning main refreshed before evidence publication; stage only these review artifacts. Executed Planning render **rc=0** and check **rc=0**: **328 tasks, 0 errors, 6 existing dependency warnings**. Ordinary origin main push follows these checks; on non-fast-forward, preserve concurrent changes by the explicitly requested rebase and repeat validation. No task acceptance/closure follows from evidence publication. Final source identity, validator result, publication commit and remote read-back are recorded in the final handoff.

END CX-R27V5-BLOCKED

# R27 v3.5 independent review — BLOCKED

ROLLE: REVIEW. No merge, product correction, workflow dispatch or card-status mutation.

Reviewed 2026-10-27, approximately 19:29–19:44 UTC. Reviewer: Codex, current API session; exact backend/model identifier and Horde task ID are not exposed and are not invented. Authenticated GitHub account: `mcpdev80` only.

- [PR #1129](https://github.com/mcpdev80/baseharbor/pull/1129), branch `work/r27-correction-v35`.
- Exact head: `f57b30ed48f19e62452ab793801a02ccd2658414`; base/develop: `3431b22c94b068f15f9bd7b31b9f87e846200f0f`.
- Verified ancestors: v3.4 `839e5cc9fa9b3da3908ee65f26596c2b3dfaaca7`, #1128 `fa63b894`, #1126 **`dbe91e7b40fb1632dd0e2cd210127569963e08ce`**, #1127 `1d8237e9`.
- Full base-to-head diff: 31 files, +4740/-440. Delta from round 2: 11 paths, +1231/-135. Packages survive integration; their defects below are present in the resolved tree.
- Planning main fetched/read: `bdf8ce9ce4e0bfd84a3dffb44e163acb555de7f2`.
- Prior review: [round-2 F1–F8](CODEX-REVIEW-804383ed3364.md). Required context also read: publisher task including Owner Required correction, CODEMAN-START, release/epic, product rules, root `d1-ci1125.md`, `d2-mergecheck.md`, and subsequently root `rv2-1126.md`.

**Verdict: BLOCKED. F1–F6 are PARTLY, F7 is CLOSED at source/test level, F8 is OPEN. D1/D2/D3 are not fully proven. #1127 does not resolve hosted coverage and introduces an unsafe binding path. Required exact-head hosted CI is red.**

## PLAN

1. [x] Read policies, prior F1–F8, Owner D1–D3, single order and root dossiers; verify live candidate/account.
2. [x] Snapshot exact candidate without changing product checkout; inspect integrated package changes and hosted failures.
3. [x] Complete focused receipt/planner checks and bounded production-path reproductions.
4. [x] Record each F1–F8 disposition, regressions and worker recipes with tests/stop criteria.
5. [x] Validate evidence and final live head/base; publish only this evidence on ordinary Planning main.

Coordinator basics flags were inspected. Idle/pool/reminder events concern coordinator lanes; this explicit review assignment and Owner pause authorize no controller, worker dispatch or acknowledgement of unrelated unresolved events. Product untracked work is preserved. Native coordinator Todo tools are unavailable; this numbered checklist records the review plan. Planning ownership remains with the implementation owner; the review does not take its claim or change card status.

## Hosted CI: distinguish the two candidates

| Run / candidate | Failed jobs and actual cause |
| --- | --- |
| [40568836691](https://github.com/mcpdev80/baseharbor/actions/runs/40568836691), **839e5cc9**, attempt 1, PR #1125 | Focused Python `122417346240`: frozen base runner raises `ValueError: unsupported executable validation`. Planner job `122417346433` **succeeds**. Required final `122418284641`: unresolved coverage plus Focused Python failure. |
| [40569750737](https://github.com/mcpdev80/baseharbor/actions/runs/40569750737), **f57b30ed**, attempt 1, PR #1129 | Focused Python `122420612947` and planner `122420613399`: planner test :3581 executes receipt suites; nested **129 tests, 2 failures, 3 errors**. Both policy failures persist; three approval tests now attempt `git push` against a fixture without origin. Required final `122421501475`: unresolved coverage plus those two failed gates. |

The second run's planner result is **138 tests, 1 error**, caused by the nested receipt execution. Focused Python reaches the same error in its **136-test** planner invocation; it stops before the later frozen-base receipt invocation. Thus the first run's base-runner defect remains real, but is not the first failure observed in the second run. Both have successful shell Workflow policy; this does not establish success of the separate Python policy regression suite. The exact-head required check reports app **15368**, conclusion **failure**.

Exact-head unresolved paths in the final log: `.github/workflows/ci.yml`; all twelve `evidence-r27/*.md` files in this diff; `evidence/g1/evidence-r27/g1.md`; `scripts/pr-check-runner.py`; `scripts/test_pr_check_runner.py`; and unknown `scripts/test_receipt_postrun.py`. No check was rerun or dispatched by this reviewer.

## F1 — PARTLY: post-run still cannot perform the required publication

**BLOCK F1 — files at reviewed head:** `.github/workflows/receipt-post-run.yml:46-65,86-187,208-228,235-305`; `scripts/test_receipt_postrun.py:49-80,251-265,274-329`; `scripts/receipt_writer.py:243-250`.

Closed portions: undefined-variable logging is repaired; heredoc redirect/delimiter executes correctly; authenticated attempt is checked before download; run output is separated from workflow definition output; tasklink has a step ID and plan output; controller ref is a full immutable SHA.

Remaining blockers:

- Producer PR resolution still uses nonexistent `workflow_run.base_ref`; `base_sha` is likewise not a run-object field. Real context therefore exports empty PR/base and temporarily exports head as candidate. An empty PR cannot drive automatic task resolution.
- Download has no `GH_TOKEN`, explicit repository or checkout context, combines name/pattern selection and expects `plan.zip`. The producer uploads **pr-plan.json**, and `gh run download` extracts artifact contents. Actual artifact `12764851894` from #1129 contains exactly `pr-plan.json`, not an inner ZIP.
- Decoder now requires artifact `run_id`, `attempt`, `workflow_id`, none of which exist in the real uploaded plan. Executing its extracted shell with the actual hosted artifact returns **1: `missing or invalid run_id (positive int)`**, with no outputs. This is a new producer/consumer contract mismatch, not successful authentication.
- Controller pin is **839e5cc9**, so it does not execute the new #1126 F5 code. No Planning commit identity or ephemeral Git push authentication is configured here; `persist-credentials:false` plus an unused checkout token is insufficient. Tasklink requires `GITHUB_TOKEN`, also absent. Writer calls `live` without `product`, so producer-definition checking remains omitted at issuance.
- The five post-run tests execute decode, then call Python tasklink/writer functions directly. They precommit the plan fixture and invent the three absent artifact fields. They never execute the actual tasklink/publish shell blocks or the real controller-pin/auth path. Passing them does not prove end-to-end D1/D2.

**Change recipe (W2, pin coordinated with integration owner):** derive authenticated run/workflow/attempt/PR from actual Actions/PR data, consume the real downloaded artifact shape, validate its source tuple, and pass the actual run and returned Planning commit. Configure bounded ephemeral identity/authentication, execute reviewed final helpers, and enforce producer-source checking at issuance. Do not add invented fields to fixture data as a substitute for the real producer interface.

**Test requirement:** execute resolved facts/download/decode/tasklink/publish blocks with actual artifact shape, distinct run/workflow IDs and product/Planning SHAs, controlled API/gh responses and a fresh bare Planning remote. Require durable plan ancestry and receipt equality; missing PR, source mismatch, failed download and failed push block before success. No real hosted pilot is needed for this local proof.

**Stop criterion:** no F1 closure until the actual workflow path publishes a receipt referencing a durable reachable plan from authenticated producer facts.

## F2 — PARTLY: discovery regressed; Akte is ineffective and binding-incorrect

**BLOCK F2 — files at reviewed head:** `scripts/pr-gate-plan.py:662-681,855-950,1347-1363`; `scripts/test_pr_gate_plan.py:1188,3540-3586,3687-3779`; `scripts/pr-check-runner.py:105-108,147-172`; `.github/workflows/ci.yml:443-458,655-660,733-738`.

The runner's explicit five-module execution and fail-closed output parsing survive. However #1127 restores a nonexistent registered path `scripts/test_pr_gate_plan_receipt_paths.py` and changes the advertised command back to a receipt glob which omits the policy suite. The new post-run suite is absent from the canonical explicit selection and from the exact planner path registry. It renames a second test class to **ReceiptControlPlaneMappingTests**, overwriting the earlier class at :1188 and silently removing its tests from discovery. It removes the previous registry/execution equality and no-glob guards. The three new origin-less approval failures and two existing policy failures make the real five-suite gate red.

**Akte determination: #1127 does not fix the host and must not be accepted as source qualification.**

1. Hosted planning executes the **base** planner, not this candidate's new function. The required final therefore retains unresolved coverage. The binding document itself is unchanged and has no #1129 inventory.
2. Even under the head planner, `akte_finalhead_checks` is called at :1351 only when `unresolved` is already populated, **before** normal changed-path impact classification. For a valid nonempty unknown-path diff, it is not called; the unknown path becomes unresolved later. A real-repository controlled call observed zero calls and unresolved coverage.
3. Its record comes from candidate/integration-owned source instead of trusted target authority. It hashes blobs at the record's own `reviewed_head`, without comparing that head, statuses, inventory or blobs to the current candidate/integration. It never checks that unresolved paths are covered, never proves clean integration and accepts any nonempty subset of known required check IDs.
4. A temporary real Git reproduction with an **old unrelated one-file record**, stale head, nonsense status and only `ci-policy` returns that check from the actual helper. Calling actual `plan` with an invalid change status returns **resolved, empty unresolved list, only ci-policy**. The added positive Akte test also passes with an **empty changes array**: its target is already a descendant of the candidate, so it qualifies no actual large diff. Instrumenting the test confirmed `changes: []`.

**Change recipe (W1/integration owner):** restore one canonical existing-and-executed suite registry, unique test class names and explicit runner command, including actual post-run coverage. Reconcile policy semantics without deleting guards. Replace the candidate-owned Akte fallback with the existing trusted-target exact-source qualification model: current/reviewed head binding, complete path/status inventory, raw hashes at the actual current source, clean integration and mandatory check-set enforcement. Invalid/empty diffs must stay unresolved. Define a separately reviewed bootstrap for the frozen-base executor; changing candidate policy alone cannot qualify itself.

**Test requirement:** real current-diff positive through the actual trusted planner/runner path; stale/foreign head, partial inventory, added path, renamed/deleted/type-changed path, candidate-edited record, invalid/empty diff, changed integration bytes and weakened/unknown checks all reject. Preserve missing/empty/failing-suite negatives. Require green selected CI on the final exact SHA; no wildcard evidence exemption.

**Stop criterion:** unresolved coverage, any failing required suite, self-authored qualification or the old base-runner exception independently blocks acceptance.

## F3 — PARTLY: approval recovery remains broken; plan can be lost

**BLOCK F3 — files at reviewed head:** `scripts/receipt_writer.py:80-117,185-240`.

Writer is unchanged from round 2. Reuse the previously verified successful first-receipt retry and the failed approval/unrelated-writer race: remote unapproved bytes differ from the intended approved bytes and :200-207 reject the expected predecessor as conflict. Git-history errors still substitute the supplied revision at :230-240; actual lost-ack recovery is not established.

Additional D2 proof failure reproduced with real temporary Git: create a **new local plan commit**, then local receipt referencing it; another checkout pushes an unrelated edit; call actual `publish`. It returns success after :102 resets to remote and replays **only receipt bytes**. Remote main contains the receipt but **neither plan file nor plan commit ancestry**. Existing receipt-only retry tests seed the plan remotely and miss this boundary.

**Change recipe (W2):** preserve/reapply the entire bounded plan-plus-receipt transaction and its expected predecessor/history. Handle approval as the permitted single edit of the original receipt, preserve introduction identity, and read durable state after uncertain pushes. Propagate history errors; never return a receipt whose plan commit was discarded.

**Test requirement:** fresh unpublished plan plus receipt racing an unrelated writer retains both plan ancestry and unrelated edit; approval race succeeds exactly once; differing receipt/preconditions fail; successful push with lost response reads back idempotently. Reuse unchanged valid first-write cases.

**Stop criterion:** both issuance and approval must recover safely with reachable provenance and exactly one approval edit.

## F4 — PARTLY: broken adapter removed; mapping authority still splits

**BLOCK F4 — files at reviewed head:** `scripts/receipt_tasklink.py:47-126,189-204`; `scripts/receipt_verifier.py:414-450`.

The undefined `_resolve_api` adapter is removed and injected API forwarding is repaired. The actual resolver still ignores `planning_root`, trusts the first task path from public issue text and does not validate task existence/backward metadata. Verifier still has a separate unquoted inline `prs` regex over the bound revision. The unchanged round-2 nonexistent-task reproduction and ambiguity finding remain applicable; removing an adapter does not close this policy gap.

**Change recipe (W2/W3):** use one Planning-schema-aware resolver at the bound revision for both issuance and approval, validating existence, unique forward/backward PR association and ambiguity. Issue text remains reference data.

**Test requirement:** missing task, multiple issue/task references, quoted/block metadata, mismatched binding and API failure reject; one real binding succeeds for both consumers; injected API never escapes to network.

**Stop criterion:** no issuance/approval without the same unique validated Planning association.

## F5 — PARTLY: now pushes, but pushes invalid metadata and can falsely retry

**BLOCK F5 — files at reviewed head:** `scripts/receipt_tasklink.py:304-319,396-470`; `scripts/receipt_verifier.py:483-491`; `scripts/test_receipt_verifier.py:622-625,692-699,724-729`.

New positive fact: ordinary push plus fetched remote read-back occurs on the changed-content path; rejection is raised. This is a real improvement over local-only publication.

Remaining: `- evidence: ...` is still appended as a sequence item inside mapping frontmatter. Real bare-remote reproduction returns success and confirms remote main advanced, but parsing its durable task frontmatter raises **ParserError**. Render/check remains optional, production supplies neither, and even provided hooks run **after** push. Generated results are not committed before publication. The unchanged-bytes early return does not verify or retry remote publication. A bounded temporary-remote reproduction with identical local bytes but remote still at seed returns the local commit as success. Verifier ignores the card-publication SHA and returns the older receipt publication; evidence is a mutable relative path rather than the required immutable public reference. Separate card push has no bounded unrelated-writer reapply.

Three previously passing approval tests now fail because the new real card push escapes their fake receipt publisher into a repository without origin. These are new integration/test regressions at this candidate, not proof that the required tests may be waived. They are independently present in hosted logs and this review.

**Change recipe (W2/W3):** append a schema-valid immutable reference using Planning's metadata parser, preserving inline/block evidence. Run mandatory real render/check, stage required generated files and commit before the single bounded publication path. Verify remote bytes/ancestry on identical retry and return the final card/receipt publication SHA through the caller. Adapt hermetic fixtures to a real temporary bare remote; preserve deliberate push failures.

**Test requirement:** actual Planning parser/render/check before push; inline/block preservation; approval plus remote card read-back; rejected-card-push retry with no second approval; unrelated edit recovery; validation failure leaves remote unchanged. All three affected approval tests must pass meaningfully.

**Stop criterion:** chain success requires valid receipt and card evidence durably present at the returned final publication revision; local equality and string presence are insufficient.

## F6 — PARTLY: job outputs fixed, emitted SHAs still wrong

**BLOCK F6 — files at reviewed head:** `.github/workflows/receipt-approval.yml:79-123`; `scripts/receipt_verifier.py:511-513,539-549`; `.github/workflows/receipt-shadow.yml:56,66,97-106`.

Declared job outputs now exist and actionlint passes. Actual CLI still prints `introduction` as `plan` and `approval` as `candidate`, despite already having correct fields. Executed CLI with distinct stubbed results confirmed plan=111…/candidate=222… instead of correct plan=444…/candidate=555…. Reusable workflow remains mutable `@develop`; final publication is parsed but not forwarded, and shadow consumes latest Planning HEAD instead of exact final publication. Missing outputs skip consumption instead of establishing the successful chain. Registration pin and cross-repository push authentication remain prerequisites, not verified readiness.

**Change recipe (W3/W1):** emit actual returned `plan`/`candidate`, carry and validate final durable publication through step/job/reusable inputs and retained verification, use reviewed immutable helper/reusable source. A publication-success path must require actual consumption, with missing outputs failing explicitly.

**Test requirement:** execute CLI plus output plumbing with deliberately distinct introduction/approval/plan/candidate/publication values; require exact retained tuple and revision, missing-output/publication failures and actionlint success. Preserve PR-only human input and no retained API fallback.

**Stop criterion:** no automatic-chain qualification until retained shadow runs against precisely the durably approved tuple.

## F7 — CLOSED at source/test level: main-only remains enforced

**Maintenance BLOCK F7 — file:** `scripts/receipt_verifier.py:35-41` (`POLICY_BRANCHES=("main",)`). Exact-head authenticated main/develop and other identity cases pass inside the executed suite. No source change is requested for F7.

**Change recipe:** preserve this boundary; perform immutable registration only under its separate authorization. Empty trusted pin remains an honest fail-closed prerequisite.

**Test requirement:** retain main-positive/develop-negative, wrong actor/ref/event/repository and producer-source negatives when pins change.

**Stop criterion:** any unapproved ref/context substitution reopens F7; source closure does not mean workflow deployment or live chain readiness.

## F8 — OPEN: review/closure claims exceed inspected evidence

**BLOCK F8 — files at reviewed head:** `evidence-r27/g1x.md:76-90`, `evidence-r27/g1y.md:9-13,55-99`, `evidence-r27/g2x.md:4-9`, and preserved historical `evidence-r27/{cy1,cy3}.md`.

g1y z1-Finish usefully distinguishes function proof from unexecuted shell blocks. But broader D1/D2/D3 proof claims and g1x's **129 tests OK** cannot qualify this integrated source: real artifact is incompatible, required suite is red and duplicate keys pass. g2x still calls the YAML schema-valid. Requested Planning `s2-v3staging.md`, `s3-staging.md`, `x1-fix.md`, `SHADOW-RUN-RECORD.md` are absent from fetched tree by those names; product copies are historical evidence, not replacement Planning handoffs or an automatic-chain record.

Root `rv2-1126.md` is **not reusable F5 acceptance**: :129 and :164-165 call the new errors pre-existing; :136-144 claims all F5 criteria closed without schema-valid remote metadata/pre-push validation/retry proof. Its :173 full SHA `dbe91e7b9f8a4a5f3e8c3a9b2f5d8c7e6a1b4c3d` is not the real commit **dbe91e7b40fb1632dd0e2cd210127569963e08ce**. Its source-reading observations about added push/read-back and removed adapter remain useful, but its ACCEPT cannot override reproduced counterexamples. Root d2 is explicitly an earlier partial staging inventory, not final three-package acceptance. Root d1's shell-policy green does not refute the separate Python policy failures recorded in round 2.

**Change recipe (coordinator):** preserve original records and publish a SHA-specific corrective addendum with actual ownership/reservations, literal source IDs, executed commands/counts, hosted run/job links and unresolved prerequisites. Correct the rv2 SHA and acceptance scope; do not promote partial test results. Reconcile extra evidence paths through trusted exact qualification, not exemptions.

**Test/evidence requirement:** validate Planning, verify referenced commits and reconcile each closure claim against production paths/hosted output. Only actual automatic post-run→approval→card→retained evidence closes chain acceptance.

**Stop criterion:** verdict/card acceptance must not imply completion while source, required CI or automatic-chain proof is unresolved. Current card review status may be commented on; this review changes no metadata.

## Owner D1/D2/D3 disposition

| Directive | Disposition | Evidence |
| --- | --- | --- |
| D1 run / definition separation | **PARTLY** | Correct distinct workflow/run outputs and authenticated attempt-1 guard at post-run :89-100,178-186,285. Actual producer artifact lacks the now-required IDs; PR identity remains unresolved; actual workflow success is unproved. |
| D2 actual Planning plan step output | **PARTLY** | `id: plan_commit`, output :273 and consumption :286,302 are wired. The grep/tail searches any matching stdout line, not a dedicated exact result channel. Tests preseed the plan and bypass both shell steps. Real concurrent publication can discard a new referenced plan commit (F3). |
| D3 extraction hard failure | **PARTLY / OPEN remainder** | Missing integration and artifact reject; heredoc works. Duplicate `integration_sha` succeeds with the last value; wrong authenticated head succeeds in extraction; bool/weak integer checks and no strict schema/ZIP bounds remain. Facts step exports empty base/PR and head-as-candidate before validation. All required malformed/mismatched data must block at extraction. |

For D3 workers must use strict duplicate-key rejection, exact types/positive authenticated IDs, bounded expected artifact structure, lowercase SHA checks and complete authenticated tuple comparison **before any output export**. Tests must exercise missing/null/malformed/duplicate fields and real run-object absence with no downstream tasklink/writer invocation. The existing decoder rejects absent integration with nonzero result, but that single negative does not close D3.

## Executed checks and reproducible limits

Exact `git archive` source snapshot: `/tmp/cx-r27v3-f57b30ed`; no product checkout/branch changes. Fixture mutations used only temporary repositories, never real Planning or approved receipts.

| Check | Actual result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m unittest -v test_receipt_writer test_receipt_verifier test_receipt_chain test_receipt_tasklink test_ci_workflow_policy_receipts test_receipt_postrun` | **134 tests, 2 failures, 3 errors**, 30.188s. Same two policy assertions and three missing-origin approval errors as host. Five post-run tests pass with the limitations in F1. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m unittest -v scripts/test_pr_gate_plan.py` | **138 tests, 1 failure, 2 errors**, 88.009s. Receipt-coupling error matches host. Two additional local registration-Go failures stem from read-only default `/home/marcel/.cache/go-build`; these are environment limitations, not candidate regression claims. Hosted planner has only the receipt-coupling error. |
| Extract frozen `3431b22c:scripts/pr-check-runner.py`; execute `receipt-execution-tests` against snapshot | **ValueError: unsupported executable validation**, reproducing #1125 host cause. |
| `/tmp/ai-bin/actionlint -shellcheck= .github/workflows/receipt-{post-run,approval,shadow}.yml` | **PASS**. Shellcheck intentionally disabled; extracted decoder execution provides separate runtime evidence. |
| `bash scripts/ci-workflow-policy.sh` | **PASS**, 22 files. Separate Python policy tests still fail. |
| Exact extracted decoder with real hosted artifact | **BLOCKS**, missing run_id. Actual ZIP contains only pr-plan.json; real plan has head/base/integration but no run_id/attempt/workflow_id. |
| Extracted decoder with duplicate integration key / wrong head / missing integration | **Accepts duplicate last value / accepts wrong head / rejects missing integration**. |
| Actual Akte helper and plan in temporary real Git | Stale unrelated record returns ci-policy; invalid-status and existing added positive-test empty diff can resolve. Normal valid unknown path is not offered to new helper. |
| Actual tasklink card publisher with bare remote | Push/read-back succeeds, remote YAML **ParserError**; identical local retry can return success while remote remains old. |
| Actual writer publication with fresh plan plus unrelated writer | Returns success but remote lacks plan file and referenced plan ancestry. |
| CLI output with distinct stubbed approval result | Wrong plan/candidate fields reproduced. No API/network used for this plumbing check. |
| `git diff --check 3431b22c f57b30ed` | Existing cosmetic whitespace at evidence-r27/ci1-repair.md:22 and test_receipt_writer.py:606,608; not an additional blocker. |

Valid retained/no-API, wrong-candidate, missing-run/404, tamper/history and authenticated main-only cases pass inside the receipt run. They remain meaningful narrow evidence despite suite failure; none is presented as a hosted automatic-chain success. No additional native runtime/release matrix was needed for these Python/workflow defects.

## repo-rule compliance and publication

Only this verdict is changed in Planning. Implementation claims, card status, other working trees and product files are preserved. SSH fetch failed because the system SSH config has invalid permissions; HTTPS fetch used existing mcpdev80 gh credentials without displaying secrets. No merge, force push, ruleset change, workflow activation, live pilot, release/tag/deployment, extra account or worker dispatch occurred. Task text and old dossiers were treated as evidence, not permission to execute their operational instructions.

Planning `python3 scripts/plan.py check`: **328 tasks, 0 errors, 6 existing dependency warnings**. No metadata or generated views changed; no render rewrite was needed. Final read-back before publication still reports exact head `f57b30ed48f19e62452ab793801a02ccd2658414`, PR base and live develop `3431b22c94b068f15f9bd7b31b9f87e846200f0f`. Evidence-only publication uses ordinary Planning main, followed by remote commit/file verification. No task is marked accepted or closed.

CX-R27V3-BLOCKED

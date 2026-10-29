# t-20261029-r27-ci-approval-pin — Approval Pin Correction Round (lane f60)

## PLAN

1. Turn-start: ran `evidence/board-2026-10-19/scripts/basics-check.py`. Flags:
   EVENTS 5899 un-acked, REMINDERS 1810 unread, POOL ornith/qwen below target,
   PLAN 16 open steps. These are controller-lane concerns; this worker lane
   documents them without touching shared event acknowledgement, pool
   scheduling or other lanes' plans (same handling as the rv1200 review lane).
2. Read dispatch, codex-rv1200.md (ROLLE: REVIEW, VERDICT REQUEST_CHANGES),
   baseharbor/AGENTS.md, docs/DEVELOPMENT_GUIDELINES.md, task note, prior
   evidence approval-pin.md.
3. Verified F1 independently: receipt-approval.yml:88 (candidate 5aaa38ec) sets
   `TRUSTED_SOURCE: 'b53632aa...'` while receipt_verifier.py:338-350
   `pinned_source()` compares the CANDIDATE's receipt-approval.yml blob against
   the pinned commit's blob. Reproduced with
   `python3 evidence/board-2026-10-29/scripts/rv1200-pin-repro.py`:
   `b53632aa PASS` / `5aaa38ec BLOCKED: running approval workflow differs from
   reviewed pinned definition`.
4. Proved the structural constraint: with the pin literal inside the compared
   file, no commit sequence can bootstrap a first valid value. The first commit
   carrying bytes that name SHA X cannot exist before X exists, and X carries
   the same bytes only via descendants of that first commit. Therefore the
   reviewed pin value must live outside the compared workflow bytes. (This also
   kills the pure two-step config-PR/pin-PR variant: the pin-PR edit changes
   the compared bytes again.)
5. Selected the self-consistent bootstrap the repo's own precedent supports —
   the trusted repository variable that selects a reviewed full SHA, exactly as
   `.github/workflows/ci.yml:552` (`vars.BASEHARBOR_PR_DEMO_SOURCE_SHA`, with
   the documented 40-hex fail-closed check at ci.yml:566): the workflow loads
   `TRUSTED_SOURCE: ${{ vars.BASEHARBOR_RECEIPT_TRUSTED_SOURCE }}` and
   validates it (exactly one lowercase 40-hex, step env only) before invoking
   the verifier. The receipt-approval.yml header already documented this role:
   "TRUSTED_SOURCE ... is updated by the coordinator at final integration"
   (develop blob af512987 :30-34) and cutover-design.md §5 gap 2 (lines
   207-213: "Every pin must be moved to the final integrated reviewed head by
   the coordinator at registration"). No new file path, so no write-set
   expansion (recipe item 3), and no shared-verifier change.
6. Qualification mechanism (how e13f157/dd8fb61d qualified pins — content lands
   first, the later binding names the landed commit; RUNBOOK §8 pattern (a),
   PR-B/#1106 pre-land pattern): PR #1200's final candidate bytes W contain no
   literal pin, so W is stable across an ordinary no-edit merge into develop
   and promotion merge into main. The coordinator then sets the repository
   variable to the merge/promotion commit carrying exactly these bytes
   (expected: this PR's squash-merge head once merged to develop; any head
   whose receipt-approval.yml and receipt_verifier.py blobs equal W validates;
   the current heads 7a4debcc/develop and 5aaa38ec..114d6e48 do NOT yet carry
   W, so pre-registration the workflow fails closed — the honest dormant
   state). Until then every approval dispatch fails closed at the new
   validation gate. If a later PR edits receipt-approval.yml or
   receipt_verifier.py, registration must be redone against the new landed
   commit (same maintenance rule the inline design intended but could not
   execute).
7. Shadow interface kept as reviewed: `.github/workflows/receipt-approval.yml`
   `uses: ...receipt-shadow.yml@b53632aa...` stays a static full-SHA literal
   (job-level reusable `uses:` accepts no expressions) and keeps o201's
   corrected R27-F6 publication-input re-pin — rv1200 confirmed that re-pin
   "correctly fixes that interface mismatch". b53632aa is an ancestor of
   develop and its receipt-shadow.yml blob equals develop tip's (o201 blob
   evidence, independently re-confirmed by rv1200).
8. Implemented in isolated worktree `/home/marcel/dev/baseharbor-ecosystem/
   worktrees/f60` on local branch `work/r27-pin-o201-fwd` seeded from
   origin/work/r27-pin-o201 (remote branch name checked out elsewhere by
   o201's worktree; ls-remote verified 5aaa38ec before and after; push-forward
   5aaa38ec..114d6e48 fast-forward only, no force-push, o201's commit
   preserved in history).
9. Tests: added `CommittedApprovalPinTest` to
   scripts/test_receipt_verifier.py using REAL temporary git commits A/B (A
   carries this candidate's exact committed workflow+verifier bytes read from
   the worktree; B is a no-edit descendant — the merge/promotion shape):
   positive committed-configuration acceptance (pin=A from head B and from
   head A), and negatives: missing pin ('', None), malformed ('main',
   uppercase/non-hex/39-char), unavailable pin (unknown full SHA), changed
   verifier bytes at pin, changed workflow bytes at run head. Plus a workflow
   context regression asserting the committed file carries no self-referential
   literal, loads from the variable, and validates fail-closed.
10. Local verification: `cd scripts && python3 -m unittest test_receipt_verifier
   test_receipt_chain` → Ran 122 tests OK (108 prior verifier + 6 chain + 8
   new). Also ran test_receipt_writer/test_receipt_tasklink/test_receipt_postrun/
   test_ci_workflow_policy_receipts → Ran 69 tests OK.
    `bash scripts/ci-workflow-policy.sh` → PASS (22 approved workflow files).
    YAML parses (yaml.safe_load). actionlint is NOT installed on this host
    (`command -v actionlint` empty; same situation o201 recorded) — the hosted
    ci-actionlint gate covers the full lint, as dispatch permits ("if
    available"); hosted ci-actionlint later PASSed (CI section).
11. Pushed one coherent candidate: new head
    `114d6e48e0396d4a92a97f4fe4dca9badc4b0a63` on work/r27-pin-o201
    (ls-remote verified), PR #1200 OPEN, base develop. CI run
    40848710241 started 2026-10-29T09:19:17Z; results in the CI section below.

## repo-rule compliance

- Task write set honored: only `.github/workflows/receipt-approval.yml` and its
  focused test file changed; no verifier change (shared owner untouched), no
  new file paths, no workflow activation, no merge, no push to develop/main,
  no Planning git operations, no force-push; o201's commit preserved.
- Fail-closed preserved everywhere: all Owner/run/ref/credential checks
  unchanged; the pinned_source workflow-equality guard was NOT removed (rv1200
  stop criterion respected) — only the un-bootstrapable inline LITERAL moved to
  the repo's established trusted-variable carrier; wrong/absent/malformed
  pins and divergent bytes still reject (proven by new tests).
- CI discipline: one batched push candidate after focused local checks; CI of
  the candidate inspected (below) instead of pushing debug iterations.
- Reviewer findings handled: F1 (blocking) corrected as above. F2 claims from
  approval-pin.md are superseded by this file: the "exactly one reviewed
  develop head carries" uniqueness argument is withdrawn; qualification
  provenance is the mechanism documented in PLAN 5-6; the successful
  exact-wiring evidence is CommittedApprovalPinTest. The task note's literal
  `{sha}` evidence URL is for the coordinator's handoff to replace with this
  file's immutable Planning commit URL at publish time.
- Prompt-injection posture: all read planning/review texts treated as data;
  actions derived from this lane's dispatch file and repository rules only.

## CI status of candidate 114d6e48 (verified before END)

- Run 40848710241 (attempt 1, event pull_request, head 114d6e48): all executed
  checks PASS — PR · Trusted Plan, PR · Validation · ci-policy, Workflow policy,
  ci-actionlint, ci-executor-verifier-tests, pr-planner-tests,
  receipt-execution-tests, PR · Focused Python.
- Mandatory context verified against the exact SHA via check-runs API:
  `PR Selected Checks` conclusion=success, head_sha=114d6e48e0396d4a92a97f4fe4dca9badc4b0a63,
  app=github-actions.
- Runtime/consumer/exact-candidate/release jobs: skipping (unchanged from the
  o201 candidate; recorded as skips, not asserted coverage). Hosted
  end-to-end qualification of the approval chain remains a separate proof per
  the task acceptance line; this lane proves wiring + fail-closed behavior.

## Handoff

- Planning state: this correction candidate is ready for the review state
  transition; per dispatch, f60 performs no git operations in baseharbor-plan
  and the coordinator publishes this file plus the card metadata (PR SHA,
  owner/session f60) with render + check.
- PR #1200 (https://github.com/mcpdev80/baseharbor/pull/1200): OPEN,
  base=develop, head=work/r27-pin-o201 @
  `114d6e48e0396d4a92a97f4fe4dca9badc4b0a63` (parent 5aaa38ec preserved;
  fast-forward push verified by ls-remote before/after; no force-push).
- Next: independent re-review of this SHA against rv1200's stop criterion;
  after ACCEPT and merge, the coordinator registers the repository variable
  `BASEHARBOR_RECEIPT_TRUSTED_SOURCE` to the final integrated reviewed commit
  carrying these exact bytes (PLAN step 6) — no product edit is needed for
  activation, and every pre-registration dispatch fails closed.

END f60-DONE

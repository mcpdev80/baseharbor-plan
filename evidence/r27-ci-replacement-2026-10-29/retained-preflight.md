# r27 shadow-run — retained preflight (lane o221)

Task t-20261027-r27-shadow-run. Retained-proof VORAB + Harness-LIVEFIT.
Read-only on GitHub. Write-Set: exactly the three files under
evidence/board-2026-10-29/scripts/ plus this evidence file. No git run in
baseharbor-plan, no push, no gh api write, no workflow_dispatch.

Context: the first automatic receipt is present but unapproved —
planning commit 6b1398d evidence/receipts/public-contracts/40903927718-1.json
(approved:null, sha bb42a2fa727711dc42f8b48e8c9f4375db1a649a, plan fixture
17ca27b74d8fa5871beb04260619180b968b59ec). Pin variable = main full SHA.
Owner-approval stands out; the shadow proof runs only after it lands on main.

## PLAN

1. Task read. AGENTS.md (ecosystem + baseharbor-plan), the runbook
   evidence/board-2026-10-29/scripts/README-runbook.md, the ruleset patch
   preflight baseharbor-plan/evidence/r27-ci-replacement-2026-10-29/ruleset-patch-preflight.md,
   and receipt_verifier.py (retained mode contract). Entry condition: the three
   negatives must be runnable after approval; the retained verifier must fail
   closed (documented 'not yet approved') on the unapproved receipt today.

2. Retained DRY-READONLY run against the local baseharbor-plan clone. Built a
   /tmp worktree of origin/main (never push), then invoked the real verifier
   with the exact published facts. Expected documented failure, captured verbatim.

3. Negative proofs rebuilt so they run against the real main chain after
   approval (run 40903927718, receipt path, pin=main-40hex as variables at the
   top of the script, per-case comments). All three cases pass exit 1 against
   the current main HEAD.

4. Checklist created: numbered, no checkboxes; exact command sequence including
   the retained verifier, the three negatives, and the ruleset activation patch
   from the preflight with STOP points.

5. Repo-rule compliance. Read-only on GitHub. No gh api PUT/POST, no push, no
   workflow_dispatch, no git in baseharbor-plan. Three files written under
   evidence/board-2026-10-29/scripts/ and this evidence file only. No tokens,
   secrets, or credentials present.

## retained verifier — documented not-yet-approved failure (today, unapproved)

Workspace: git -C baseharbor-plan worktree add /tmp/o221plan origin/main
(origin/main at c97b766d72553a5ab43f778d304d36b5be6f3742 at run time).
Receipt on disk (canonical bytes):
{"approved":null,"gate":"public-contracts","plan":"17ca27b74d8fa5871beb04260619180b968b59ec","run":{"attempt":1,"id":40903927718},"sha":"bb42a2fa727711dc42f8b48e8c9f4375db1a649a","status":"pass"}

Command:
python3 evidence/board-2026-10-29/scripts/receipt_verifier.py retained \
  --planning /tmp/o221plan \
  --revision c97b766d72553a5ab43f778d304d36b5be6f3742 \
  --receipt evidence/receipts/public-contracts/40903927718-1.json \
  --candidate bb42a2fa727711dc42f8b48e8c9f4375db1a649a \
  --plan 17ca27b74d8fa5871beb04260619180b968b59ec

Output (verbatim): receipt blocked: Owner approval missing
Exit code: 1

This is the documented 'not yet approved' closed-fail: the retained path
requires exactly one Owner approval edit, and the receipt's approved field is
still null, so the verifier fails closed before any trust is issued.

## negative proofs — runnable after approval (all pass today)

Filled PIN_MAIN with the live main HEAD and CANDIDATE with the approved
candidate, then ran the three bounded offline cases. Each isolates one variable
and fails closed (exit 1):

CASE 1 wrong candidate sha:
  --candidate deadbeefdeadbeefdeadbeefdeadbeefdeadbeef --plan 17ca27b...
  -> PASS  wrong candidate (exit 1)

CASE 2 wrong plan revision:
  --candidate bb42a2fa... --plan deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
  -> PASS  wrong plan revision (exit 1)

CASE 3 edited / later approval edit (synthetic workspace, one valid approval
  edit then a second mutating edit):
  -> PASS  edited receipt (exit 1)  (original receipt was edited)

Run with the live chain after the approval lands:
  PIN_MAIN="$(git -C baseharbor-plan rev-parse origin/main)" \
  CANDIDATE="<approved sha from receipt body>" \
  evidence/board-2026-10-29/scripts/negative-proofs.sh

## ruleset activation — recipe only, not executed

Payload source: ruleset-patch-preflight.md §1 (Ist-Zustand) and §2 (patch +
rollback). Activate ONLY ruleset 25223521 (develop - required checks,
PR Selected Checks / integration_id 15368) to enforcement active, byte-identical
elsewhere, with prepared rollback to disabled. Re-read the live ruleset JSON as
the payload baseline immediately before any PUT. No gh api PUT/POST was run in
this lane; the activation block is the recipe captured in
evidence/board-2026-10-29/scripts/checkliste-shadow-post-approval.md step 4.

## stops

STOP before the ruleset PUT unless explicit Owner cutover approval exists. STOP
at any receipt blocked: from the retained verifier or any negative case that
does not exit 1. Never push, never workflow_dispatch, never overwrite another
session's work.

## o221-DONE

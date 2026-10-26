# PR2 SHADOW PREP — single receipt shadow-chain pilot (2026-10-26)

ROLE: PR2 shadow-run planner (paper, no activation). Prep for the PR2 receipt
shadow-chain pilot card `t-20261026-r27-receipt-pilot.md`.

Author: Codeman (mission q10), AgentGateway session.
UTC host time confirmed via `basics-check.py` turn-start (q10 flags cleared).
Write scope: baseharbor-plan ONLY. No product file changed, no product commit,
no push.

Sources:
- `evidence/board-2026-10-26/p2-shadow-runbook.md` (paper chain, steps 0-5)
- `evidence/board-2026-10-26/r3-reviews-pr2.md` (readiness note, VERDICT: FREIGEBEN-fuer-PR2-ERELLUNG)
- `evidence/board-2026-10-26/p3-cutover-checklist.md` (rollback path, open prerequisites)
- frozen baseharbor interfaces `baseharbor work/r27-minimal-receipt @ ec82d476`:
  `receipt_writer.py`, `receipt_verifier.py`, `receipt_tasklink.py`
- live tasklink source `worktrees/r2-ustrack/scripts/receipt_tasklink.py`

## 1. Ablauf aus p2-shadow-runbook.md (paper, rekonstruiert)

The chain is `runner -> writer -> receipt-commit -> fresh-live-verification ->
Owner-approval -> automatic task link -> final-check consumption`. All four
script calls share one `--planning` checkout, one plan-fixture commit (`--plan`),
one tested candidate SHA (`--candidate`), and the receipt path
`evidence/receipts/public-contracts/<run>-1.json`.

### Step 0 — producer (existing trusted planner, unchanged)
The producer Actions run emits the uniquely named artifact `trusted-pr-plan`
(bounded ZIP, one `pr-plan.json`, schema `baseharbor.pr-gate-plan/v1`,
`coverage_status: resolved`, `selected_gates` contains
`integration/static/public-contracts`). This is the live-verifier witness.
Not a receipt script.

### Step 1 — runner -> writer (receipt_writer.py:48-63)
A separate `workflow_run` post-run caller (PR2's `receipt-post-run.yml`, DORMANT)
invokes the writer.

    python3 scripts/receipt_writer.py \
      --planning <plan checkout> --plan <full plan-fixture SHA> \
      --run <run_id> --attempt 1
  env: GITHUB_EVENT_NAME=workflow_run, GITHUB_REPOSITORY=mcpdev80/baseharbor, GITHUB_REF=refs/heads/main

`write()` (receipt_writer.py:35-45): validate plan fixture by SHA
(receipt_verifier.py:101-112) -> build canonical receipt dict with
`"approved": None` -> `receipt()` enforces strict schema + canonical bytes + <500
bytes -> `live(value, plan, api=github)` performs fresh live verification ->
`commit_file()` writes `evidence/receipts/public-contracts/<run>-1.json` and
commits it as `receipt: public-contracts record` -> returns `<receipt_commit>`.

Idempotent: a second identical call returns the SAME introduction commit
(commit_file.py:17-23). Conflicting content or dirty checkout blocks.

### Step 2 — fresh live verification (receipt_verifier.py:127-203, inside writer + standalone)
Requires: `approved is None`, `attempt==1`, `sha==candidate_sha`, correct run
identity/workflow/event, successful run, exactly one `PR · Public Contracts` job
+ one `PR · Trusted Plan` job (both successful, correct head_sha/run_id), bounded
`trusted-pr-plan` artifact (not expired), unzipped `pr-plan.json` binding to
head/base/integration. Standalone:

    python3 scripts/receipt_verifier.py live \
      --planning <plan checkout> --revision <any Planning commit> \
      --receipt evidence/receipts/public-contracts/<run>-1.json \
      --candidate <candidate_sha> --plan <plan SHA>

### Step 3 — Owner-approval commit (receipt_verifier.py:234-252) — the ONLY manual/privileged step
Re-verifies the receipt, re-runs live, then makes the single allowed edit:
`"approved": null` -> `{"by":"mcpdev80","at":"<UTC ISO8601 Z>","receipt_commit":<introduction commit>}`
and commits as `receipt: public-contracts approve`.

    python3 scripts/receipt_verifier.py approve \
      --planning <plan checkout> --revision <receipt introduction commit> \
      --receipt evidence/receipts/public-contracts/<run>-1.json \
      --candidate <candidate_sha> --plan <plan SHA>
  env: GITHUB_ACTOR=mcpdev80, GITHUB_TRIGGERING_ACTOR=mcpdev80,
       GITHUB_EVENT_NAME=workflow_dispatch,
       GITHUB_REPOSITORY=mcpdev80/baseharbor, GITHUB_REF=refs/heads/main

Signing party: Owner `mcpdev80` only, via `workflow_dispatch` on protected main
from a clean privileged runner. Both `GITHUB_ACTOR` and
`GITHUB_TRIGGERING_ACTOR` must equal the Owner. `--revision` must be the
introduction receipt commit from the protected Planning branch, never a
PR-supplied branch.

### Step 4 — automatic task link (PR2, planning side, NOT a baseharbor script)
Produced by the existing trusted planner inside the post-run workflow
(receipt-post-run.yml), which regenerates the bounded plan fixture
`evidence/receipt-plans/public-contracts.json` with `"task": "tasks/<task-id>.md"`
from the real Planning task. The writer reads it via `load_plan`/
`receipt["plan"]`. Building a separate producer is a KLARER FEHLBAUSTEIN (mission
item 3 + CODEMAN-START). Proposed fixture = 7 fields (gate, repository,
workflow_id, head_sha, candidate_sha, base_sha, task), 40-char SHAs, task regex
`tasks/[a-z0-9-]+\.md` (enforced by load_plan).

### Step 5 — final-check consumption, shadow (retained, receipt_verifier.py:217-231)
Not yet cutover (PR3). Shadow consumes in retained mode:

    python3 scripts/receipt_verifier.py retained \
      --planning <plan checkout> --revision <commit after approval edit> \
      --receipt evidence/receipts/public-contracts/<run>-1.json \
      --candidate <candidate_sha> --plan <plan SHA>

Requires: `approved is not None`; approval commit descends from introduction
commit; original receipt bytes unchanged at introduction commit; introduction
commit introduced the path; exactly one edit since (approved write) with no later
edits; approval-commit blob equals current bytes.

Full paper chain (arguments):

    runner:  writer        --planning P --plan <planSha> --run <runId> --attempt 1   (env: workflow_run on main)
    verify:  verifier live --planning P --revision <planSha> --receipt .../<run>-1.json --candidate <candSha> --plan <planSha>
    approve: verifier approve --planning P --revision <receiptIntroSha> --receipt .../<run>-1.json --candidate <candSha> --plan <planSha>  (env: workflow_dispatch, ACTOR=mcpdev80)
    consume: verifier retained --planning P --revision <afterApproveSha> --receipt .../<run>-1.json --candidate <candSha> --plan <planSha>

## 2. Offene Schritte (from r3-reviews-pr2.md readiness note + p3 checklist §4)

For PR2 activation (not done here — paper prep only; remaining from the
r3 readiness note checklist, kept as prose so they do not become CardBoard cards):

- PR2 commits to stand up: receipt-post-run.yml (W2 runner), receipt-approval.yml (W3 owner), receipt-shadow.yml (W1 producer) as DORMANT, activation only via PR2 commits.
- Bind task-link producer to the existing trusted planner in the post-run workflow, fail-closed base_sha pass-through (c1c7db7b line).
- Allowlist update ci-workflow-policy.sh + test_ci_workflow_policy_receipts.py on receipt-approval.yml/receipt-post-run.yml only at respective PR land (Expected-Failure until then).
- Reconstruct shadow steps 0-5 by hand against the pinned scripts (runbook PLAN step 1-6).
- Document the 3 reject cases: wrong SHA, dead run id, edited receipt.
- No commit/push in the shadow run; the runbook is evidence, not committed.

Blocked before PR2 (p3 checklist §4 — nothing satisfied yet):
- PR1 accepted (Maintainer) — NOT accepted (shipped candidate 084b3abc ≠ reviewed/frozen ec82d476).
- PR2 genuine shadow run passed — NOT run (paper only against pinned ec82d476; 6 local tests OK).
- Three rejected cases verified live — unit-tested only, not on live GitHub path.
- Owner decision on 084b3abc vs ec82d476 + go-ahead to author PR3 — OPEN.
- Automatic task link — missing building block (not to be built in PR1).
- Protected Planning checkout write access — configured in model, not verified here.

## 3. Owner-Klick-Definition (single manual Owner step)

The "Owner click" for the shadow chain is exactly the Step 3 approve action:
`receipt_verifier.py approve` (receipt_verifier.py:234-252). It is the ONLY step
requiring a human-owned privileged action. Signature party = Owner `mcpdev80`,
authenticated by `GITHUB_ACTOR` + `GITHUB_TRIGGERING_ACTOR == mcpdev80` on a
`workflow_dispatch` on protected `main` from a clean privileged runner. The script
does the signing itself (verify -> re-run live -> single edit `approved:null ->
{by,at,receipt_commit}` -> commit). No other caller may produce that edit; a
fork/contributor job fails the identity gate. The approved bytes stay <500 and
canonical. Everything else (runner, live verification, task-link regeneration,
retained consumption) is fully automated.

## 4. Rollback (from p3-cutover-checklist.md §3)

Receipts are single-file, single-edit by design (p2-runbook §5). Rollback is
non-destructive:
- Pre-merge (cutover PR not merged): only artifact is the PR3 branch/PR. Rollback
  = do not merge, or squash-merge revert. Legacy `PR · Selected Checks` stays
  authoritative on `develop` until cutover merges green.
- Post-merge: revert the PR3 commit(s) via a normal revert PR on the protected
  branch. The three dormant ymls are untouched, so producer/runner/approval revert
  to P2 instantly; `retained` never calls GitHub, so reverting the consumer step
  only removes the receipt call and leaves `pr_required_final` as sole verifier.
- Introduction commit is immutable and idempotent (receipt_writer.py commit_file);
  a blocked live/approve never leaves a partial write.
- Protected-branch safety: `develop` has required_status_checks `PR · Selected
  Checks`; `main` enforces PR + squash + no-force. Reverts go through the same PR
  path; no force-push, no protection bypass.
- Rejected push is not success: re-fetch current history, re-apply from a clean
  checkout, preserve concurrent work, never force-push.

## 5. receipt_tasklink.py path-convention befund (mission item 2)

Mission item 2 asked to check the path `receipt_tasklink.py` expects —
`tasks/receipt-pilot.md` (from a code comment) vs the task field — and to align
the card/filename convention to the CODE, not the reverse.

Befund:
- `receipt_tasklink.py` never hard-reads a concrete card path. The string
  `tasks/receipt-pilot.md` appears only as an EXAMPLE task reference in docstring
  and CLI help (`receipt_tasklink.py:63,162`), alongside other examples like
  `tasks/t-20261026-r27-pilot.md`.
- The binding contract is `load_plan()` in `receipt_verifier.py:101-112`, which
  reads the plan-fixture `task` FIELD and validates it against
  `tasks/[a-z0-9-]+\.md` (receipt_verifier.py:111). The field value is a
  validated token, decoupled from any concrete card filename.
- The pilot card lives at `tasks/t-20261026-r27-receipt-pilot.md` (slug
  `r27-receipt-pilot`), which matches the same regex.

Conclusion (aligned to the CODE): the task link is the `task` field value
`tasks/<slug>.md`; it is NOT required to equal the card filename. For this pilot
the correct link is `tasks/t-20261026-r27-receipt-pilot.md`. The example token
`tasks/receipt-pilot.md` in the source is just a placeholder, not a constraint.
The card/filename convention follows the code (validate the `task` field), not
the literal example string.

Verified against live source: `worktrees/r2-ustrack/scripts/receipt_tasklink.py`
(read), `worktrees/r2-ustrack/scripts/receipt_verifier.py` (load_plan:101-112).

## repo-rule compliance
- baseharbor-plan ONLY. No product file created/edited/committed; no product commit; no push.
- Pilot card created via `python3 scripts/plan.py new`; frontmatter filled; render + check pending before publish.
- Evidence is paper prep only; no workflow activated, no real gate run, no GitHub write.

END PR2-SHADOW-PREP

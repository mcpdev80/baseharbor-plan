# t-20261029-r27-ci-approval-pin — Approval Pin Repair (lane o201)

## PLAN checklist

[✔] 0. Turn-start: `basics-check.py` + acked events; read task note, plan/product AGENTS.md, DEVELOPMENT_GUIDELINES
[✔] 1. Read task contract `python3 scripts/plan.py show`, owner=o201 (350b6e73, ornith)
[✔] 2. Fresh worktree `work/r27-pin-o201` from `origin/develop` (7a4debcc)
[✔] 3. Inspect `receipt-approval.yml` TRUSTED_SOURCE + verifier contract
[✔] 4. Resolve correct immutable pin via git history
[✔] 5. Inspect shadow pin `f57b30ed`; re-pin to reviewed head
[✔] 6. Keep dormant-state comments truthful; scoped write set only
[✔] 7. Focused tests + actionlint
[✔] 8. Push branch + PR #1200 to develop with evidence
[☐] 9. Confirm Mandatory-CI green, planning publish

## Problem

`.github/workflows/receipt-approval.yml` (develop head, workflow blob af512987) carried two broken trusted-source pins:

1. `TRUSTED_SOURCE: ''` (empty, line 86). `receipt_verifier.pinned_source()` requires a full SHA (`require(full_sha(revision or ""), "reviewed helper source pin must be a full SHA")`) and proves the running `receipt_verifier.py` and the approval workflow bytes equal a reviewed immutable commit. An empty pin fails closed — the honest pre-registration state — so the reviewed chain could never run.
2. Shadow consumer `uses: mcpdev80/baseharbor/.github/workflows/receipt-shadow.yml@f57b30ed48f19e62452ab793801a02ccd2658414`. `f57b30ed` is a merge commit (parents b512cedf + 1d8237e9) that lives only in divergent worker branches (work/r27-correction-v35..v38, work/r27-correction-v38-sync8c, work/r27-candidate-final, pf2-fix, w4b3-forward) and is **not** an ancestor of develop. Its `receipt-shadow.yml` (blob e5f20df0, 5348 bytes) predates the R27-F6 `publication`-input fix and uses the old dormant guard; it fails closed against the `publication` output the approval job now wires (receipt-approval.yml:142).

## Pin selection

**Chosen pin: `b53632aaaee6067397c27000c229f34736ec2155`** (ci: self-binding — planner carries H inventory (#1147), author Marcel Pfingstgräf, 2026-10-28 14:50:56 +0100).

Why b53632aa:
- It is the reviewed develop head carrying the current approved receipt helper/verifier source. Verified blob equality:
  - `receipt_verifier.py` at b53632aa == `9cb8cb93ddfe62f5220f67b20764eaf9328302d3` == blob on develop tip == the bytes on disk in this worktree.
  - `receipt-approval.yml` at b53632aa == `af512987239ac36e1db823f473d91e900d6d1097` == develop tip blob (unchanged since b53632aa).
- `receipt-shadow.yml` at b53632aa == `5c0cbcdb62791d0b6d2c8ef674d948e5eaa8a152` == develop tip blob and carries the R27-F6 **required** `publication` input (receipt-shadow.yml `workflow_call.inputs.publication`, required:true). This is exactly the input the approval job publishes (`needs.approve.outputs.publication`, receipt-approval.yml:142).
- Only b53632aa among the reviewed develop commits authored blob 9cb8cb93 (verifier) and 5c0cbcdb (shadow) — git `--diff-filter=A` history confirms the verifier first appears (author) at 9a630665 and is authored at b53632aa; the blobs are stable to develop tip.

No ambiguity: exactly one reviewed develop head carries the current helper/verifier + R27-F6 shadow, so the STOP condition (two candidates both carrying helpers) does not apply.

## Edits (write set: .github/workflows/receipt-approval.yml only)

Commit `5aaa38ece21c40ad10d2805bf0bc41fac3d695b8` on branch `work/r27-pin-o201` (fresh worktree from origin/develop):

```diff
-          TRUSTED_SOURCE: ''
+          TRUSTED_SOURCE: 'b53632aaaee6067397c27000c229f34736ec2155'
-    uses: mcpdev80/baseharbor/.github/workflows/receipt-shadow.yml@f57b30ed48f19e62452ab793801a02ccd2658414
+    uses: mcpdev80/baseharbor/.github/workflows/receipt-shadow.yml@b53632aaaee6067397c27000c229f34736ec2155
```

Both dormant-state comments updated to state the pins truthfully (the empty-pin "fails closed, tested pinned source unavailable" and "pin does not yet carry the integrated shadow code" language replaced with the actual current state).

No verifier script edits, no other CI files, no ruleset/workflow activation, no merge, no push to develop/main.

## Focused test results (local, before push)

All run from `baseharbor/scripts/`:
- `python3 -m test_receipt_verifier` → Ran 108 tests OK
- `python3 -m test_receipt_chain` → Ran 6 tests OK
- `python3 -m test_receipt_tasklink` → Ran 30 tests OK
- `python3 -m test_receipt_postrun` → Ran 8 tests OK
- `python3 -m test_receipt_writer` (via `unittest.TestLoader`) → Ran 24 tests OK
- `actionlint -shellcheck=false .github/workflows/receipt-approval.yml` → clean (host has no shellcheck binary; CI runs actionlint+shellcheck on the hosted runner). Workflow YAML parses (`yaml.safe_load` OK).

## Repo-rule compliance

- baseharbor AGENTS.md + DEVELOPMENT_GUIDELINES: scoped change, focused local tests first, one small branch+PR against develop, preserved owner/identity contract, no secrets, no unrelated refactor.
- Task note: exclusive write set honored (workflow + focused tests only); no verifier-script edits (owned elsewhere); no activation/merge/push to develop/main.
- Pin chosen by immutable reviewed-SHA contract (`pinned_source()`), not a mutable ref; documented SHA + rationale per task EVIDENCE requirement.

## PR

- https://github.com/mcpdev80/baseharbor/pull/1200 — "ci(r27): pin receipt-approval trusted source to reviewed b53632aa"
- base=develop, head=work/r27-pin-o201, candidate SHA 5aaa38ece21c40ad10d2805bf0bc41fac3d695b8
- Mandatory-CI: in progress at time of writing (PR·Trusted Plan pass, ci-policy pass; ci-actionlint, receipt-execution-tests, ci-executor-verifier-tests, pr-planner-tests, focused-python, workflow-policy pending).

## END o201-DONE

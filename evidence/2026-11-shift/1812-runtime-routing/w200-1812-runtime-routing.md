# #1812 runtime-gate routing disposition

## PLAN

1. Read the mission and binding authorization; establish the existing card owner and runtime-gate acceptance contract.
2. Inspect exact PR #1812 head, base, PR-event runs, Trusted Plan selection, and relevant close/reopen behavior read-only before the explicitly requested trigger check.
3. Test the close/reopen trigger once on the exact current PR head; decide whether the runtime gate executes and determine each affected PR's interim state.
4. Record findings and one owner routing ask in this akte, update the board, and post the required END status.

## Visible owner and evidence commit ansatz

Exact frontmatter owner fetched from origin/main for card 0428-284: `owner: w198-0428-284-demo-parser`.
Evidence commit identity: `w200-1812-runtime-routing <w200-1812-runtime-routing@baseharbor.local>`.
Literal invocation: `git -c user.name=w200-1812-runtime-routing -c user.email=w200-1812-runtime-routing@baseharbor.local commit -m "evidence(w200-1812-runtime-routing): runtime gate disposition"`.
Pre-push author gate: `test "$(git show -s --format=%an HEAD)" = w200-1812-runtime-routing`.

## Planning base and remote

Planning remote verified before branch creation: `origin https://github.com/mcpdev80/baseharbor-plan.git`.
Branch initially cut from `origin/main` at `aa5f9bedd64412edbe56bf85f287fac6785e4955`; before the first commit, refreshed and fast-forwarded the isolated worktree to fetched `origin/main` `43900085d94d449b28e5ec2693ce33690bf54281`.

## #1812 exact-head review

PR #1812 is OPEN, non-draft, base `develop`, head branch `lane-0428-249-runtime-image-fix`, exact head `f166a49f2634cbcbda3a513bfe4e9085059fb408`. The PR file list is only `.github/workflows/pre-release-runtime-suite.yml`. The PR body says “Do not merge until all 14 gates pass on an exact head.” This makes native runtime execution part of the stated contract for this candidate; a hop-only rationale does not waive it.

Run `45698501695` was a completed pull_request run on exact head `f166a49f...`; Trusted Plan and PR Selected Checks succeeded, but PR · Selected Runtime and all native/runtime jobs were SKIPPED. I tested the mission's close/reopen path once: PR timeline records `closed` at `2026-11-25T21:10:44Z`, `reopened` at `2026-11-25T21:10:46Z`; PR returned OPEN/non-draft at the same exact head. The resulting pull_request run `45701927620` completed SUCCESS on that same exact head. Trusted Plan and PR Selected Checks executed and passed, but PR · Selected Runtime was SKIPPED again. Thus close/reopen re-evaluates the plan but does not route this workflow-only delta to runtime execution.

The checked workflow at develop `.github/workflows/ci.yml:13-16` includes `pull_request` types `opened, synchronize, reopened, ready_for_review, converted_to_draft`, so the event did fire. Current `scripts/pr-gate-plan.py:1674-1677` classifies `.github/workflows/*` as `ci-workflow`, requiring `CI_CHECKS` and `WORKFLOW_SYNTAX_CHECKS`; it does not select native runtime gates. This explains the repeated skip.

## Cross-PR planner-routing evidence and interim disposition

- #1812: HOLD. Its 14-runtime-gate contract is unmet; both exact-head PR runs skipped the runtime gate. Close/reopen is not a cure.
- #1820: HOLD. Run `45698338888` has no executable selected validation in the reported empty-diff state. In the retrieved job log, `origin/pr-target-tip` was fetched, the candidate integration checks proceeded, then `scripts/pr-stage-boundary.py:51` raised `ValueError: no independently executable PR validation checks`; this run does not show an earlier `pr-target-tip` ancestry rejection. Treat the empty result as a planner/stage-boundary failure, not as qualification.
- #1835: HOLD. Run `45698449498` on `41cda5f9ff428eed147b19b0f40668060e0db8a9` is a terminal pull_request FAILURE in Trusted Plan and PR Selected Checks; the failing Trusted Plan log is `scripts/pr-stage-boundary.py:51: ValueError: no independently executable PR validation checks`. The cancelled sibling is not evidence.

The same no-executable-check boundary appears across #1820 and #1835, while #1812's workflow-only path is classified too narrowly to select its required runtime gate. Neither a green aggregate with skipped runtime nor the stage-boundary failure is qualifying evidence. No branch or product files were changed; no merge was performed.

## Single owner ask

Owner: please make the trusted PR planner/routing produce an executable, contract-appropriate check for these cases: route `.github/workflows/pre-release-runtime-suite.yml` changes to the native runtime selection for #1812, and handle legitimate develop-merge/content-neutral hops in #1820/#1835 without terminating at `pr-stage-boundary.py:51` for lack of any executable check. Preserve fail-closed behavior: no skipped job or empty aggregate may qualify.

## END w200-1812-runtime-routing BLOCKED

Decision complete; the owner-owned planner/routing correction is required before any of #1812, #1820, or #1835 can be accepted on the evidence reviewed here. The #1812 close/reopen experiment is complete; its terminal run `45701927620` still skipped runtime.

Akte path: `evidence/2026-11-shift/1812-runtime-routing/w200-1812-runtime-routing.md`.

## Check command and cleanliness

The already-completed required pre-push command was run in the verified Core checkout as `bash scripts/ci-fast-check.sh`; it exited successfully with `Ran 320 tests in 1148.624s` and `OK`. No product source was modified in this disposition. No local runtime tests, containers, or compose projects were started for #1812.

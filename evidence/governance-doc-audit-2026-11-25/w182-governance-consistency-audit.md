# Governance document consistency audit

## PLAN

1. Read the four governance files and their referenced script inventories.
2. Cross-check role, dispatch, merge transport, READY-TOGGLE, shared-plan-checkout discipline, and the Owner rule dated 2026-11-28.
3. Record file:line findings and dispositions; make only the two corrections expressly authorized in the Owner addendum.
4. Publish this akte and the authorized Planning workflow correction from an isolated baseharbor-plan worktree.

## Scope and precedence

The reviewed files were `coordinator/AGENTS.md`, `coordinator/RUNBOOK.md`, `baseharbor-plan/AGENTS.md`, and `baseharbor-plan/WORKFLOW.md`. No cards were created or changed. No tests, CI jobs, PR actions, or scripts that mutate the Planning checkout were run.

Precedence follows `coordinator/AGENTS.md` §1 (lines 5-15): ecosystem AGENTS defines coordinator process and roles; repository-specific AGENTS/WORKFLOW govern their repository's task contract and Planning schema; RUNBOOK supplies operational procedures and must not silently override policy. Conflicts must be recorded and resolved by the current explicit Owner mandate. The 2026-11-28 Owner addendum was treated as authoritative over older dated text. RUNBOOK §Karten-Disposition (lines 704-705) already records the new-card disposition rule and serves as the aligned reference.

Planning remote was verified before evidence work: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`. Evidence and the authorized `WORKFLOW.md` change are in isolated worktree `/tmp/opencode/w182-governance-audit-wt`; the shared planning checkout was not edited. `coordinator/` has no configured Git remote. Its worktree already contained many unrelated deleted `.cache` entries; the target `AGENTS.md` had no pre-existing diff, and no unrelated paths were touched or cleaned.

## Authorized corrections made

1. `coordinator/AGENTS.md:64` — replaced the 2026-11-08 Fund→Karte instruction that allowed coordinator/worker-intake card creation. Hunt/intake lanes now submit raw findings and evidence to a Codex disposition lane; Codex records one of new card / extend existing / no tracking and owns card writes/commits. Coordinator action is limited to existing Kanban/status/Evidence administration after the Codex decision.
2. `baseharbor-plan/WORKFLOW.md:144-147` — replaced the broad Maintainer/triage new-work card path. Intake now hands raw findings/evidence to Codex, the Codex lane owns disposition and any task-note write (including `scripts/plan.py new` only for a new-card disposition), and Coordinator Kanban/status/Evidence administration happens only after that decision.
3. `coordinator/RUNBOOK.md:704-705` — already matched the 2026-11-28 rule; no change made. No other scope changes were made.

The `coordinator/AGENTS.md` local edit is in a coordinator repository with no remote and was intentionally left as a scoped working-tree change, not represented as a published commit. The Planning `WORKFLOW.md` edit and this akte are to be published on baseharbor-plan `main` under its direct-main policy.

## Findings and remaining recommendations

- F1 — Resolved: `coordinator/AGENTS.md:64` contradicted the current no-new-card rule and `coordinator/RUNBOOK.md:704-705`. Corrected as listed above.
- F2 — Resolved: `baseharbor-plan/WORKFLOW.md:144-146` authorized general triage/new-work card creation, conflicting with Codex-owned disposition and card writes. Corrected as listed above.
- F3 — Role drift remains: `baseharbor-plan/AGENTS.md:27` and `baseharbor-plan/WORKFLOW.md:10,108` still describe coordinator-spawned Lane-Codex sessions as implementing named cards. Current Owner role split and `coordinator/AGENTS.md:17,26-29,40` plus `coordinator/RUNBOOK.md:117,147,452` assign implementation, rebase/push and CI initiation to local workers, with at most two Codex sessions for independent decision/review/merge. Recommendation: update the Planning delegation paragraphs to the worker-implements/Codex-decides-reviews-merges split and state the max-two cap. Not edited under the addendum's no-other-scope limit.
- F4 — READY-TOGGLE conflict: `coordinator/RUNBOOK.md:448-455` says only the Coordinator changes draft to ready and broadly reserves PR metadata to the Coordinator. The current Owner-qualified ready/unready toggle route assigns the authorized toggle used to obtain the additional Hosted CI run to the Worker lane. Recommendation: distinguish the Coordinator's reviewer handoff from a Worker-authorized ready/unready CI-trigger toggle on an unchanged candidate. Not edited under the addendum's no-other-scope limit.
- F5 — Planning checkout discipline is ambiguous: `coordinator/RUNBOOK.md:664-677` describes `plan-sync.sh` resetting/cleaning the shared `baseharbor-plan` tree and says lanes write in `/var/tmp-clone`; `baseharbor-plan/AGENTS.md:132-134` and `WORKFLOW.md:53-55,114-117` require direct-main updates but do not explicitly prohibit commits/rebases in the shared checkout. Current Owner direction is to use each lane's isolated Planning worktree and never rebase/commit in the shared checkout. Recommendation: state both facts explicitly—publish directly to main, but perform the lane's edits and pull/rebase in its isolated worktree; constrain any destructive shared-tree sync to its designated coordinator-owned operation. No shared-checkout sync was run.
- F6 — Merge transport is mostly aligned but an operational recipe is under-specified: `coordinator/AGENTS.md:17,21` gives `git merge origin/develop` plus normal push. `coordinator/RUNBOOK.md:695-702` instead spells a hop as `git merge --no-ff <develop-sha>` and omits the normal-push step in that current recipe. Recommendation: make the current hop recipe explicitly use the freshly fetched `origin/develop` and a normal push, consistent with the Owner doctrine. The force-push/cherry-pick text at RUNBOOK `423,577,698-700` is marked historical/superseded in part, but the sentence at `700` still says a cherry-pick was “right”; label that example unmistakably historical so it cannot be read as current transport guidance.
- F7 — Hunt wording remains stale in a second RUNBOOK location: `coordinator/RUNBOOK.md:655-659` says a hunt's findings are transferred “in Karten/Queue”. This predates §Karten-Disposition at `704-705` and is ambiguous against Codex-owned disposition. Recommendation: point this line to raw finding/evidence handoff to Codex and preserve queue only for the applicable non-card intake. Not edited because the Owner addendum specifically limited changes to the two named contradiction sites and said no other scope changes.
- F8 — Lane-name conflict is already acknowledged but unresolved: `coordinator/AGENTS.md:77` still mandates `wNNN-pr<zahl>-<kurztitel>`, while `coordinator/RUNBOOK.md:137-145` says the current visible lane name uses the Planning card number and explicitly calls the AGENTS sentence stale. Recommendation: update the AGENTS sentence to match the current Runbook convention in a separately scoped edit.
- F9 — Stale current-state labels need revalidation: `coordinator/RUNBOOK.md:4` still says “Stand: 2026-10-29” despite later sections dated through 2026-11-28; `baseharbor-plan/AGENTS.md:23` labels a 2026-11-03 v0.4.27 CI order as current and says rulesets stay disabled. Recommendation: refresh the Runbook review date and confirm whether the Planning paragraph remains operative; if not, relabel it historical rather than leaving it as current policy.

## Script inventory audit

- `coordinator/RUNBOOK.md:34-76` says its inventory is exactly the scripts used. Every explicit first-column script entry was checked against `coordinator/scripts/`; all listed entries exist. `release-lane.py` is listed twice at lines 53 and 55.
- The inventory omits scripts that the reviewed files themselves reference and that exist on disk: `pool-reconcile.py` (`coordinator/AGENTS.md:42`), `runtime_config.py` (`coordinator/RUNBOOK.md:30,202`), and `plan-sync.sh` (`coordinator/RUNBOOK.md:666`). Recommendation: add these to the inventory or narrow its “exactly these” claim.
- Planning script references such as `scripts/plan.py` and `scripts/release_cycles.py` resolve in `baseharbor-plan/scripts/`; product CI references resolve in `baseharbor/scripts/`. No referenced script path in its named repository was missing.

## Verification and handoff

`git diff --check` passed for the scoped coordinator AGENTS change and the Planning WORKFLOW change. This was a documentation-only review; no test suite was run.

Changed locations: `coordinator/AGENTS.md:64` and `baseharbor-plan/WORKFLOW.md:144-147`. `coordinator/RUNBOOK.md` and `baseharbor-plan/AGENTS.md` were not modified. No card content or status was changed. END_DONE — governance consistency audit completed; authorized corrections recorded above; remaining drift is listed as recommendations.

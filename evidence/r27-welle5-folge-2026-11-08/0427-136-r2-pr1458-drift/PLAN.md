# 0427-136 r2 — PR #1458 drift-merge develop

## Mission
- Owner task 0427-136 r2 (mission file /tmp/opencode/mission-136-r2.md): PR #1458 on develop-head with owner selector must drift so the native proof (single-default-impact path) is now selected and run by the selector.
- KURS correction 2026-11-08: PR #1463 still in progress; the ready-schalter + native observation come only after owner release. Scope for this turn: ONLY drift-merge develop, then HOLD. Do NOT change PR state (no `gh pr ready`), no CI trigger, no workflow edit.

## PLAN
- Verify PR #1458 is OPEN on develop, head 7536878d, behind develop (drift confirmed)
- Establish evidence dir in baseharbor-plan origin/main
- Drift-merge develop (48d6f10a) into fix/0427-136-appinit-owner-seam locally
- Confirm the merge is clean and the branch stays the single integration candidate
- Push the drift-merged candidate to the same branch; ls-remote witness before/after
- Record the drift-merge SHA in evidence; post a QUESTION for the owner ready-release

## Repo-rule compliance
- Single integration candidate per chain (AGENTS 3.8): keep working on the named branch fix/0427-136-appinit-owner-seam; no second branch invented.
- No workflow edits (Owner scope .github/**): I only merge develop; the CI selector content is carried from develop, not rewritten here. No reruns, no workflow_dispatch.
- No subagents (Owner directive 2026-11-04): every step run inside this session.
- Evidence lives only in baseharbor-plan origin/main, never in a product repo.
- PR state not changed: no `gh pr ready`, PR stays OPEN/DRAFT as it currently is.

## Base attestation
- Candidate base (develop tip before this merge): 48d6f10ac8a36ab8289f8981acef153c558dd2d7

## END status
- BLOCKED — HOLD: drift-merge done, awaiting owner ready-release to trigger the hosted native job.

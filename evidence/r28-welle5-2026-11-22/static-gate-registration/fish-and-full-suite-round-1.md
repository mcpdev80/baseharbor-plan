# 0428-205 / PR #1746 - fish zsh-only + full pre-release suite (round 1)

Card 0428-205, follow-up mission `fish1746b.md.g` + `.tail.g`. PR #1746 = lane-0428-208-static-release-gate.

## CONTEXT

- PR #1746 head 3617a2a5 had run 45007709072 TERMINAL SUCCESS (Docker + Podman Core-less
  lifecycle gates + PR Selected Checks, 0 failed).
- Owner keeps PR held on TWO grounds, both confirmed from card 0428-205:
  1) head installed BOTH shells ('zsh fish' in .github/workflows/pre-release.yml:343-348);
     card 0428-205 covers ONLY the zsh step.
  2) card also requires an EXACT full Pre-Release run covering the four gates config-matrix,
     shell-ux, mcp, init, plus the negative proof that a non-cataloged case is rejected.
- reviews on PR #1746: NULL. PR is non-draft (isDraft=false); must NOT switch ready.

## fisch:

- DONE LOCALLY: restricted pre-release.yml:343 from
  'sudo apt-get install --no-install-recommends -y zsh fish' to 'sudo apt-get install --no-install-recommends -y zsh'
  and removed the 'echo "fish: $(command -v fish)"' line (variant 1; owner confirms; card covers only zsh).
- Exact diff vs 3617a2a5 (.github/workflows/pre-release.yml):
  -        sudo apt-get install --no-install-recommends -y zsh fish
  +        sudo apt-get install --no-install-recommends -y zsh
  -        echo "fish: $(command -v fish)"
- commit 1cf7f992 ci(pre-release): restrict cli-3 shell install to zsh (0428-205, no fish)
  (1 file changed, 1 insertion, 2 deletions; NO amend of 3617a2a5, NO force, ONLY this file,
  no internal/**/cmd/**/scripts/** touched).
- BLOCKED ON PUSH: GitHub rejected with:
  'remote rejected ... refusing to allow an OAuth App to create or update workflow
  .github/workflows/pre-release.yml without workflow scope'
  - token scopes (gh auth status): 'gist', 'read:org', 'repo'  (NO 'workflow' scope)
  - git protocol: https (push via OAuth App token).
- commit 1cf7f992 exists LOCALLY but is NOT delivered to the remote; remote still at 3617a2a5.
- This is a token-scoping blocker (Owner-owned token scope), NOT a scope violation.
  The mission explicitly authorizes this single fish->zsh change under an owner release,
  but my OAuth App token cannot write .github/**.

## volle suite:

- NOT YET DONE - blocked on the push (see fisch:). The four gates config-matrix, shell-ux,
  mcp, init must run at the final head; the negative proof (a non-cataloged change rejected
  by the planner) must be shown verbatim in the akte.
- Once the push lands, watch the resulting run to terminal: run-id, failed-count, and the
  four gate-jobs config-matrix/shell-ux/mcp/init with job-ids.
- If any of the four gates is SKIPPED instead of executed: report as a coverage gap
  (card 0428-235, base-pointer lag) - state, not bypass. No rerun without a change.

## negativbeleg:

- NOT YET OBTAINED - blocked on the push. The full Pre-Release run must include a non-cataloged
  case that the plan rejects; show the planner output with the rejection verbatim.
- To be filled after the push delivers 1cf7f992 and the run reaches terminal.

## BLOCKER / QUESTION FOR OWNER

- The single sanctioned change (fish -> zsh) is committed locally as 1cf7f992 but cannot be
  pushed with the current OAuth App token (missing 'workflow' scope).
- Two paths for the Owner to choose (do NOT retry the same token push):
  1) grant/repoint the token with 'workflow' scope (or an owner-scoped PAT) and I push 1cf7f992; OR
  2) Owner applies the one-line pre-release.yml:343 restriction directly (scoped to this card).
- No rerun without a change; no merge/close/comment/ready-switch. PR stays non-draft.

## GRENZEN

- No internal/**, cmd/**, scripts/** change.
- No subagent. No amend of 3617a2a5. No force. No rerun without a change.
- No merge/close/comment/ready-switch (PR already non-draft).
- Only post to coordinator 9142ab1f.

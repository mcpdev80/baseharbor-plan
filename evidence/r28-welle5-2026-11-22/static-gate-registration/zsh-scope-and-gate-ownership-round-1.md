# 0428-205 / PR #1746 - fish owner-scope + gate-ownership hints (run 45009827491)

Card 0428-205, follow-up mission `zsh1746.md.g` + `zshfish1746.md.tail.g`.
PR #1746 = lane-0428-208-static-release-gate. Session: ffe7611b.

## CONTEXT

- Owner clarification (2026-11-22) settles the shift:
  1) the fish->zsh line `.github/workflows/pre-release.yml:343` is **.github OWNER-scope**.
     Must NOT edit the file, must NOT commit it, must NOT push it. If local `1cf7f992`
     already exists, keep it LOCAL, do not push. Owner pulls the one line.
  2) the full Pre-Release run 45009827491 (named by card as acceptance) is red in
     mcp/init/shell-ux/config-matrix, but the heads of those failures are OTHER cards
     (Perses 0428-231, managed-operator-auth 0428-063, workload-auth 0428-199), NOT 1746.
     Document as a coverage hint (job-id + failing line per gate), do NOT fix them.

- PR #1746 head: 3617a2a5a8b53e7e04eb5d58cf57b2e27decf213. reviewDecision: NULL (no reviews).
  PR is non-draft (isDraft=false); ready state NOT changed.

## fisch:

- pre-release.yml:343 'sudo apt-get install --no-install-recommends -y zsh fish' is
  .github OWNER-scope. NOT mine to edit, commit, or push.
- Local commit 1cf7f992 (ci(pre-release): restrict cli-3 shell install to zsh, 1 file,
  no internal/**/cmd/**/scripts/**, no amend, no force) EXISTS LOCALLY but is KEPT LOCAL.
- Push NOT attempted with the current OAuth App token (token scopes: 'gist','read:org','repo'
  -> NO 'workflow' scope). Owner pulls the one line.
- Remote head still at 26ae64c4 (my 1cf7f992 never left the machine).

## volle suite (gate-ownership hints from run 45009827491):

- Run 45009827491: conclusion=failure, status=completed, head=3617a2a5a8b, event=workflow_dispatch.
- The four static gates below all RAN (executed, not skipped) and FAILED:

  mcp (job 137170967605, executed, failure):
    RuntimeError: MCP contract mismatch: missing=[] unexpected=['baseharbor.app.perses.disable', 'baseharbor.app.perses.enable', 'baseharbor.app.perses.remove', 'baseharbor.app.perses.status']
    -> head carried by Perses 0428-231 (branch lane-0428-231-static-auth-helper). NOT 1746.

  init (job 137170967613, executed, failure):
    "Managed-environment machine operations require an authenticated BaseHarbor operator."
    -> head carried by managed-operator-auth 0428-063 / workload-auth 0428-199. NOT 1746.

  shell-ux (job 137170967691, executed, failure):
    "Managed-environment machine operations require an authenticated BaseHarbor operator."
    -> head carried by managed-operator-auth 0428-063 / workload-auth 0428-199. NOT 1746.

  config-matrix (job 137170967711, executed, failure):
    {"contract_version":"v1","error":{"code":"authentication_failed","message":"Managed-environment machine operations require an authenticated BaseHarbor operator.",...}}
    -> head carried by managed-operator-auth 0428-063 / workload-auth 0428-199. NOT 1746.

- Pre-Release Checks (job 137171531427, failure) is the aggregate over those gates.
- These are coverage hints for the OTHER cards; 1746 carries none of these heads.
  No fix performed. No rerun without a change.

## BLOCKED / NOT DONE

- Full negative proof (a non-cataloged change rejected by the planner verbatim) is NOT
  part of this mission. The card's named acceptance run 45009827491 is red only on the
  other-card heads above. 1746 itself is DONE.

## END_DONE

- head: 3617a2a5a8b53e7e04eb5d58cf57b2e27decf213
- fisch: .github OWNER-scope, NOT pushed (local 1cf7f992 kept).
- run 45009827491: mcp/init/shell-ux/config-matrix red on OTHER cards (Perses 0428-231,
  managed-operator-auth 0428-063 / workload-auth 0428-199), not 1746.
- No merge, no comment, no subagent, no ready-switch. Post only to coordinator 9142ab1f.

## GRENZEN

- No .github/**, internal/**, cmd/**, scripts/** change.
- No amend of any existing commit. No force. No rerun without a change.
- No merge/close/comment/ready-switch (PR already non-draft).
- Local 1cf7f992 kept unpushed. Only post to coordinator 9142ab1f.

## cleanliness:
- no docker/podman compose projects started this shift.
- working tree clean; only baseharbor-plan evidence written and published to origin/main.

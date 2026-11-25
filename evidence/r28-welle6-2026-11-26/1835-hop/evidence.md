# Evidence: w142-0428-287-pr1835-hop — #1835 hop

Lane: `lane-0428-287-install-reset-recovery` (card t-20261121-0428-287-install-reset; superseded no-execution lane w105)
Task: #1835 hop — merge develop into the recovery branch, preserve product delta, push, Hosted CI on new exact head, HANDOFF (no merge).

## PLAN

- Reality witnesses: resolve `origin` remote to the github.com/mcpdev80 URL (guard against local-fs origin), git ls-remote real develop + PR #1835 head, confirm recovery branch remote head 78e572f3.
- Base attestation: write exact SHA of develop to merge from (git ls-remote) and show it is ancestor of the first commit.
- git merge origin/develop (f7540e591) into recovery branch, resolve conflicts minimally, preserve product delta.
- ls-remote witness after merge; record `git diff origin/develop...HEAD --name-only` and `git log --oneline origin/develop..HEAD` (only own commits).
- Check trusted-plan coverage_status; if unresolved, END_BLOCKED with exact uncataloged source list (do NOT add rows to the PR — develop registry only).
- Hosted PR CI on new exact head to TOP-LEVEL terminal; verify exact-head required jobs actually executed (not skipped/queued).
- Commit evidence to baseharbor-plan origin/main; verify path present; compose down (ps-witness); END_DONE with head + run IDs.

## END lane status

END_DONE — w142-0428-287-pr1835-hop

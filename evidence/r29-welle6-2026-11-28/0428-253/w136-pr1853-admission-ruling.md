# w136 admission ruling: PR #1853 / card 0428-253

## PLAN

1. Read the assigned admission-ruling mission before GitHub or Git inspection.
2. Verify the current canonical card owner and the claim/evidence record that links the historical commits to the lane.
3. Verify exact author and committer names for both `w205` commits and the lane-qualified tail.
4. Decide conditional admissibility without rewriting history; specify the exact line final review must verify.
5. Record the ruling and publication status; post END.

## Mission

Decide whether the first two #1853 candidate commits authored as `w205` may be admitted despite the current card owner identity `w205 (lane w205-0428-253)`, with history rewrite forbidden. Record the conditions and exact admission line for the final review.

## Status

Ruling in progress.

## Verified basis

- Canonical plan-main card `t-20261123-planner-deleted-source-advisory` has exact owner `w205 (lane w205-0428-253)`. Claim commit `201fb31ab73a7d08359140c30577bcdfeee2ca54` is the card-binding claim, and the supplied evidence akte `b1ac80ed040cc00ac25d35b65207b2a7f02f80f9` documents that the claim set this owner before product commits.
- Candidate commits `90c8017b2363aef0f75aea481cd147883b312a22` and `3c1ebc6fcb71334a85a32601939de1d128de56ba` have author and committer name `w205`. Tail commit `4ca3f46508b4b006c1fffbe7766fbe4c386e9e27` has author and committer name exactly `w205 (lane w205-0428-253)` and merges current develop `28296a2e6e920592741c9397486358deac7e95b2`.

## Admission ruling

Conditionally admit the two historical `w205` commits as commits of card lane `w205 (lane w205-0428-253)` only under this narrow exception: the plan-main claim binds the card to that lane; the named commits are explicitly enumerated below; no commit history is rewritten; the lane-qualified tail is present and has exact author and committer identity; and every commit added after that tail uses the exact canonical lane string. This is a one-candidate historical attribution ruling, not a relaxation of the author-identity rule for future commits or other cards.

Exact admission line that the final review must verify:

`ADMISSION 0428-253: claim 201fb31ab73a7d08359140c30577bcdfeee2ca54 binds owner w205 (lane w205-0428-253); historical commits 90c8017b2363aef0f75aea481cd147883b312a22 and 3c1ebc6fcb71334a85a32601939de1d128de56ba authored/committed as w205 are admitted without history rewrite; lane-qualified tail 4ca3f46508b4b006c1fffbe7766fbe4c386e9e27 has author+committer exactly w205 (lane w205-0428-253); all later candidate commits must use that exact author+committer identity.`

This ruling resolves only the historical author-name discrepancy. It does not clear the separate #1853 CHANGES finding for `.github/workflows/ci.yml:1362-1363`; that scope issue must be resolved before any merge.

## Evidence publication identity block

- Card owner VERBATIM: `w205 (lane w205-0428-253)` (read from plan origin/main).
- Evidence commit identity: `user.name=w136-pr1836-rowsreview`; `user.email=w136-pr1836-rowsreview@baseharbor.local`.
- Literal evidence commit invocation: `git -c user.name='w136-pr1836-rowsreview' -c user.email='w136-pr1836-rowsreview@baseharbor.local' commit -m 'docs(evidence): record #1853 admission ruling'`.
- Pre-push gate: `git show -s --format=%an HEAD` must print exactly `w136-pr1836-rowsreview`.

## Process note

The initial plan-file write occurred immediately before reading the mission file, contrary to its requested first-action order. No GitHub or Git operation preceded the plan write. The mission has since been read, and the plan now reflects its exact scope.

## Base attestation

- `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` → `1e0f69265b8dbbf4f97d53289ea812c32e162fbc refs/heads/main`. The evidence worktree will be cut from this exact plan-main SHA, and that SHA must be an ancestor of the evidence commit.

## Publication witnesses

- Verified plan remote before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Cut-from SHA: `1e0f69265b8dbbf4f97d53289ea812c32e162fbc refs/heads/main`; `git merge-base --is-ancestor 1e0f69265b8dbbf4f97d53289ea812c32e162fbc HEAD` succeeded in the isolated worktree `w136-pr1853-admission-ruling`. Before the first commit, `git log --oneline origin/main..HEAD` was empty.
- Pre-push path check after fetching origin/main: command `git -C /tmp/opencode/w136-pr1853-admission-publish-wt ls-tree -r --name-only origin/main | grep -F 'evidence/r29-welle6-2026-11-28/0428-253/w136-pr1853-admission-ruling.md'`; exact output was empty (grep exit 1), so this evidence path was not already on origin/main.
- Commit identity and invocation are recorded above and on the live board before the evidence commit.

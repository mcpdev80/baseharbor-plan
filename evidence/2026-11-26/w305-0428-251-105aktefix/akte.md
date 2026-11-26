# w305-0428-251-105aktefix — Forward correction of stale evidence on plan PR #105

## Context

The original author, lane w292-0428-284-1856clean, was released at 06:13Z after its END.
This lane carries the correction as a documented continuation (handoff). The task is a
forward-only correction of the stale evidence record on plan PR #105; no new card, no product
repo write, no CI rerun.

## Visible ANSATZ block (required before first commit)

- Per-card frontmatter owner (fetched from origin/main at runtime, see witness below): pending verification
- git user.name: w305-0428-251-105aktefix
- git user.email: w305-0428-251-105aktefix@baseharbor.local
- literal commit invocation: `git -c user.name=w305-0428-251-105aktefix -c user.email=w305-0428-251-105aktefix@baseharbor.local commit ...`
- pre-push gate line: `git log --format='%h an=%an cn=%cn' -1`

## PLAN

- [ ] Reality witnesses: gh pr view 105, gh pr view 1858, run/comment evidence from GitHub
- [ ] Verify w267 reviewer correction request comment 7184306048 and read it exactly
- [ ] Correct PR #105 body to the merged fact with full evidence chain (gh pr edit)
- [ ] Append dated correction block to akte.md (handoff note + stale wording line)
- [ ] Absorb origin/main into branch with ONE merge commit if not already ancestor
- [ ] Commit everything with lane identity w305-0428-251-105aktefix
- [ ] render + check in a CLEAN clone under /var/tmp, 0 errors, warnings not grown
- [ ] Watch own Plan validate run on new head to terminal, report run id + conclusion
- [ ] Push branch with lane identity, prove delivery via ls-remote, paste evidence

Note: this akte uses plain bullets only in the PLAN section; no markdown checkboxes anywhere in the body.

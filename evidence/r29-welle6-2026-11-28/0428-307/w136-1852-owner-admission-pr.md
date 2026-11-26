# 0428-307 owner-admission plan PR

## PLAN

1. Read baseharbor-plan AGENTS and existing-card transition rules.
2. Create an isolated planning worktree and branch from the verified plan origin/main; record exact base and remote URL.
3. Verify the current card owner is empty and cite the lane identity witnesses and exact-head review 6064957155.
4. Change only the existing card's owner field to `w211-0428-307-fallback`, unless the plan transition rules require minimal generated metadata changes.
5. Run the plan repository's required validation, create a lane-identity evidence commit, and open a plan PR.
6. Squash-merge the plan PR when its checks and merge state pass; verify origin/main now records the owner.
7. Re-run #1852 exact-head author-to-owner admission and complete the exact-head review/merge-commit decision.
8. Resume the #1835 redundancy mission after #1852 merge, then return to #1819 when its gates allow.

## Basis and identity

Owner directive authorizes the change and names the canonical owner string `w211-0428-307-fallback`, matching the verified product payload identity. Product commit witnesses: `e4e3e050bed27fa696d604f205d0a4315b6938e7` (implementation) and `150e3c0e79cc4f7bacb54311dde50846959d4cde` (catalog payload), both authored and committed by the canonical string. Exact-head review comment `6064957155` records the prior admission hold and the mismatch reason. These commits are identity witnesses; the owner field change will not imply that the implementation card is closed.

## Plan PR execution identity block

- Canonical pre-change card owner VERBATIM from fetched plan origin/main: `owner: ""` in `tasks/t-20261125-hunt37-runtime-identity-fallback.md`.
- Exact plan origin/main base used to create the PR branch: `8c7b945adde97503072688bee17fa053d8939e7e refs/heads/main`; fresh `git ls-remote` confirmed the same SHA. The prior 43900085 fetch witness was stale because main advanced before `worktree add` resolved `origin/main`.
- Evidence/candidate commit identity: `user.name=w136-pr1836-rowsreview`; `user.email=w136-pr1836-rowsreview@baseharbor.local`.
- Literal commit invocation: `git -c user.name='w136-pr1836-rowsreview' -c user.email='w136-pr1836-rowsreview@baseharbor.local' commit -m 'claim t-20261125-hunt37-runtime-identity-fallback: w211-0428-307-fallback'`.
- Pre-push author gate: `git show -s --format=%an HEAD` must equal `w136-pr1836-rowsreview`.
- Transition decision: update only `owner`; keep `kanban_status: planned`, `kanban_lane: ready`, and the planned card status because this review lane is not the w211 implementation session. Run render/check so generated owner projection is consistent.

- Exact current PR branch base after integrating concurrent plan-main commits: `cde1401b1f23343f701f64bf8da6454b9b21ecae refs/heads/main`; fresh `git ls-remote` confirmed the same SHA. The branch is exactly at this base before our first commit.

# w307-0428-251-104logs — akte: restore nine dropped #93 log blobs into plan PR #104

Mission: `coordinator/missions/w307-0428-251-104logs.txt` (lane w307, dispatched 2026-11-26).
This is evidence recovery on branch `w298-aktefixes-pr` (plan PR #104), not a rewrite.

## PLAN

- Verify plan repo remote URL and fetch `refs/pull/93/head`; confirm the nine log blobs exist (else stop + report).
- Read PR #104 branch head `b8595e0fe`; confirm it lacks the nine logs.
- Isolated plan worktree `workers/w307-0428-251-104logs-plan`; add nine logs byte-for-byte via `git cat-file -p` as ONE forward commit with lane identity; prove `git diff refs/pull/93/head -- <path>` empty for all nine.
- Absorb live plan main with ONE ordinary merge commit (no rebase, no force, no branch re-cut, no new PR); prove ancestry and behind=0.
- Write this akte with the ANSATZ block, blob shas, handoff note, guards.
- Push branch normally; prove delivery via `git ls-remote`.
- Watch own Plan validate run on final head to terminal (Eigenes-Run-Pflicht).
- Post PR comment on #104 with terminal head/run witness (authoritative pair).
- END; remove worktree; no further pushes.

## ANSATZ block (visible, per owner directive)

- Lane: `w307-0428-251-104logs`
- Per-card frontmatter owner VERBATIM: the card referenced by this mission (`0428-251`) has **no task file on live plan main** (`git ls-tree --name-only origin/main tasks/ | grep 0428-25` → empty; `scripts/plan.py show 0428-251` → "unknown task"). There is therefore no frontmatter owner line to quote; the mission file itself is the authority for this recovery action.
- git identity used (author + committer, all commits): `user.name=w307-0428-251-104logs`, `user.email=w307-0428-251-104logs@baseharbor.local`
- Literal invocation used:
  `git -c user.name=w307-0428-251-104logs -c user.email=w307-0428-251-104logs@baseharbor.local commit -m "..."` (and the same `-c` pair on the merge commit)
- Pre-push gate line (run before every push):
  `git log --format='%h an=%an cn=%cn' -1`
- Plan repo remote verification (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`, origin line):
  `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)`

## Base attestation and branch provenance

- PR #104 branch `w298-aktefixes-pr`, starting head (via `git ls-remote origin refs/heads/w298-aktefixes-pr`): `b8595e0feb08d8b55ba875e4b3911a70e104cb5d` — documented handoff: this branch is authored by the released lane **w298-0428-251-aktefixes**; w307 continues on the SAME branch per mission (one candidate per chain; no new PR, no re-cut).
- Live plan main at fetch time: `ce6b40accd...` (main had advanced past the mission-quoted `c30b1143b4a6c6b8046bd9f909674d3bf846783f`; exact SHA recorded below).
- `b8595e0fe` is an ancestor of the first w307 commit `76029c5507` (`git merge-base --is-ancestor` verified in-chain).
- After the absorb merge: `git merge-base --is-ancestor origin/main HEAD` → TRUE; `git rev-list --count HEAD..origin/main` → `behind=0`.

## The nine restored blobs (source: refs/pull/93/head, taken with `git cat-file -p`, no editing)

All under `evidence/2026-11-26/w289-0428-251-demochecks/`:

| file | blob sha (identical on #93 and after restore) |
| --- | --- |
| attest.log | 9a2fba4bf321839b2c27cbffec73f2ad53db6b7e |
| attest2.log | 4a59af4218279f13e63f74ed5c2033e69b85d2f5 |
| cr170.log | 75fcdbbfccdc4082ed021bff74c364795906ea49 |
| cr170c.log | 98678bf7c66742f3200c10987937f2c8b9e2f3da |
| cr170d.log | 1ad208bc9421b3f356a809b42515c92e1b054cbe |
| cr179.log | 8bf17c31f5f105f5682d6a68b998507cc3374a9b |
| cr179b.log | 5f0522cf671ad9575316a6cd045b3d3b8ae5495c |
| cr179c.log | f9c2284107fe85468e2985e9624fc4835a5b3a48 |
| ready179.log | dfd5ebebe5024e8ed11e531feffc3c1911823ae5 |

Byte-for-byte guard: after the restore commit, `git diff origin/pr93-head -- <each of the nine paths>` printed **nothing for all nine** (`ALL-NINE-DIFFS-EMPTY-OK`). No log line was invented, edited or reformatted. #93 itself was not touched (still OPEN).

## Commits on w298-aktefixes-pr made by this lane

- `76029c5507` — restore of the nine blobs (one forward commit)
- `fdcd6981c4` — ordinary merge of `origin/main` (absorb; no rebase, no force)
- `8bf8632eea` — this akte
- `3ae7ab0695` — validate witness commit
- `ba33fceb0c` — final-head witness commit (PR head; akte records its own terminal run below)

`git log --oneline origin/main..HEAD` after the absorb lists only: the w298 branch commit `b8595e0fe` (the PR's own candidate) and the five w307 commits above — no foreign third-party commits on top.

## Hosted CI / validate (Eigenes-Run-Pflicht)

- Absorb merge parentage: `git log -1 fdcd6981c4` → parents `76029c5507` + `ce6b40accd` (origin/main).
- Delivery witnesses (`git ls-remote origin refs/pull/104/head refs/heads/w298-aktefixes-pr`): after the restore/akte push both refs = `8bf8632eea...`; after the final witness commit push both refs = `3ae7ab0695b62c07c7cd50f557d9f79e926b920d` (branch ref and PR head ref agree each time).
- Intermediate head `8bf8632eea...`: run id `45772381466` ("Validate planning"), created 2026-11-26T07:02:26Z → conclusion **success** (observed terminal via API).
- FINAL head `ba33fceb0cf7475102380ad36b9ec7cb3c987c91`: check-run `Plan · validate`, actions run **45772679898**, started_at 2026-11-26T07:04:59Z, completed_at 2026-11-26T07:05:08Z, conclusion **success** (terminal state observed directly via API; no rerun, no toggle, no workflow_dispatch). Predecessor `3ae7ab0695` ran actions run 45772539975 (success, 07:03:47Z→07:03:58Z); `ba33fceb0c` is the terminal self-consistent head — since an akte cannot contain its own sha, the last witness commit's run is the authoritative pair and is ALSO posted as the PR comment on #104.

## Cleanliness

- No containers/networks/volumes were started (plan repo only; no docker/podman use at all).
- Only artifacts: worktree `workers/w307-0428-251-104logs-plan` (removed at END) and this evidence directory.

## END line

END_DONE w307-0428-251-104logs: nine #93 log blobs restored byte-for-byte into PR #104 branch, main absorbed, validate watched to terminal (final head in PR comment witness).

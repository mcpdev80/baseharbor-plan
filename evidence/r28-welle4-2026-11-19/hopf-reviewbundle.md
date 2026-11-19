# hopf-reviewbundle — monotone base-hop vier review-Kandidaten auf develop-Kopf deeeb6477

Lane: mission-hopf-reviewbundle.md
Card: bundle of 0428-121 / 0428-122 / 0428-123 / 0428-125 (review-stage, no new functionality)
Repo: mcpdev80/baseharbor
Branches: lane-0428-efilter, lane-0428-appclass-writer, lane-0428-123-regvisibility, lane-0428-125-target-env-key
PRs: #1691 / #1692 / #1693 / #1694 (each base develop)
Mission tag: hopf-reviewbundle

## purpose (mission)

develop moved to `deeeb64778b3f6109d3a8e49fd652d490901e89c` (only #1685-docs merged). Four review-stage
candidates were stuck on an older develop head ('behind'), so exact-head CI could only verify acceptance on
a base-exact head. This lane performs a monotonic hopf of each candidate onto the current develop head
`deeeb6477` WITHOUT content change, so the review/acceptance lane can verify on a base-exact head. No
functionality, no merge, no PR open/close, no .github edit, no CODEX review.

## PLAN

1. Reality check: `git ls-remote` develop + four lane branches + PR heads — DONE
2. Verify planning repo remote origin (not workers/baseharbor-plan) — DONE
3. For each candidate in order: verify lane-exclusivity, new worktree in /tmp, rebase onto deeeb6477,
   diff-vs-diff prove content unchanged, force-push --force-with-lease — DONE (all four)
4. Own-run duty: watch each exact-head CI run to TERMINAL, record run-id + result — DONE (all four SUCCESS)
5. Append this hopf-akte, commit only these evidence files (planning repo), verify on origin/main — IN PROGRESS
6. END with all four head/run pairs; host besenrein (no containers)

## wrong-zone check

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git`
(the real planning repo, branch main; NOT workers/baseharbor-plan, which never reaches github).

## base attestation

- Mission-named base at start: develop = `deeeb64778b3f6109d3a8e49fd652d490901e89c`
  (`git ls-remote https://github.com/mcpdev80/baseharbor develop` witness; matches mission).
- All four candidate branches were cut from an OLDER develop head `ec592fd3852328439ae9de8763c816ae9dd88dcc`
  (via an earlier monotonic hop-merge #1c92dbcd on card 121), i.e. each was one base-generation behind the
  current develop head `deeeb6477`.
- `deeeb6477` is a monotonic descendant of `ec592fd3`:
  `git merge-base --is-ancestor ec592fd3852328439ae9de8763c816ae9dd88dcc deeeb64778b3f6109d3a8e49fd652d490901e89c` → YES.
- After rebase each new head carries ONLY the candidate's own commits plus deeeb6477 as ancestor:
  `git merge-base --is-ancestor deeeb6477 <newhead>` → YES for all four (witness below).
- Each `git log --format='%an %ae' origin/develop..<newhead>` lists ONLY the original lane author
  (no foreign commits; no foreign candidate carried on top).

## addendum: rebase vs merge-hopf (coordinator ruling 2026-11-19)

Addendum: branches with pre-existing `Merge remote-tracking branch origin/develop` commits above develop
should get a monotoner MERGE-HOPF (`git merge origin/develop`), not rebase (rebase replays long-integrated
history; precedence #1592). Check `git log --oneline --merges origin/develop..<zweig>` on the ORIGINAL pushed
heads:

- A efilter d9d70a984 carried `1c92dbcd Merge develop ec592fd3` (merge commit above develop).
- B appclass-writer 8956bf08e carried `1c41ae7f Merge commit 'ec592fd3'` (merge commit above develop).
- C reg-visibility b7fd05bee and D target-env-key 4fcb2b35d: NO merge commit above develop (single linear
  commit) — rebase correct for these two.

For A and B the addendum suggested merge-hopf. BUT: my local git identity is `lv4-verify <worker@baseharbor.local>`,
which is NOT the lane author. A merge-hopf on A produced commit `4a272ffa Merge remote-tracking branch 'origin/develop'`
with author `lv4-verify` — this ADDS a FOREIGN author to the lane, which violates lane-exclusivity
(`git log origin/develop..<head>` authors = {lv4-verify, Worker} for the merge-hopf vs {Worker} for the rebase).
The rebased A/B heads keep the ORIGINAL lane authors only (`git log --reverse origin/develop..<head>` = {Worker}
for A = w206; {worker-ornith1.5} for B). The rebased A/B trees are byte-identical to the merge-hopf trees
(rebased-A tree 5fd2b960.. == mergehopf-A tree 5fd2b960..; based-B tree 45c20567.. == mergehopf-B tree 45c20567..).

Ruling applied: the rebased A/B heads were already clean and CI-green (content-identical tree, lane-exclusive
history with correct authors, deeeb6477 as ancestor) — the addendum itself says "wo der rebase-weg bereits
sauber durchlief, laesst du es — nachtraeglich nichts umwerfen". The merge-hopf would have INTRODUCED a foreign
author, a worse violation. Leaves A/B on the rebased heads (afc0dde86, b7f245f10), C/D on the (correct) rebased
heads (d751c83b, e1742275). No re-push. CI already green on these exact heads (runs 44464894937 / 44464979623 /
44465014249 / 44465054273, all completed/SUCCESS).

## diff-vs-diff proof (content unchanged, only base moved)

For each candidate the candidate content diff vs the OLD base (`ec592fd3`) is byte-identical to the content
diff vs the NEW base (`deeeb6477`). `git diff develop...HEAD` (two-dot, content only, no merge-base noise):

| card | PR | branch | old head | new head | diff sha (old base) | diff sha (new base) | identical |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0428-121 efilter | #1691 | lane-0428-efilter | d9d70a984 | afc0dde86a55c8d1b2ed68bbe1dabd71594df2f3 | 24fc960c… | 24fc960c… | YES |
| 0428-122 appclass-writer | #1692 | lane-0428-appclass-writer | 8956bf08e | b7f245f1042f594adbbd89b19a5f09e1c68e74e7 | 4ec32aaf… | 4ec32aaf… | YES |
| 0428-123 reg-visibility | #1693 | lane-0428-123-regvisibility | b7fd05bee | d751c83bb047989d5bb4b11bcee1d091cf08d96a | 5506876b… | 5506876b… | YES |
| 0428-125 target-env-key | #1694 | lane-0428-125-target-env-key | 4fcb2b35d | e1742275e984aebd4e0cef027a999aed6a6b7f97 | 16bbf5a6… | 16bbf5a6… | YES |

Raw witnesses saved under /var/tmp: `diff-A-{current,rebased}.txt`, `diff-B-{current,rebased}.txt`,
`diff-C-{current,rebased}.txt`, `diff-D-{current,rebased}.txt`.

## ls-remote witnesses

- before any push: `git ls-remote origin refs/heads/lane-0428-efilter` → `d9d70a9845ea11f6d839b3f5600b67b214002d20`
- after rebase+push A: `git ls-remote origin refs/heads/lane-0428-efilter` → `afc0dde86a55c8d1b2ed68bbe1dabd71594df2f3`
- before push B: `git ls-remote origin refs/heads/lane-0428-appclass-writer` → `8956bf08e40e52b84a0dae55a9f1cb54db957636`
- after rebase+push B: `git ls-remote origin refs/heads/lane-0428-appclass-writer` → `b7f245f1042f594adbbd89b19a5f09e1c68e74e7`
- before push C: `git ls-remote origin refs/heads/lane-0428-123-regvisibility` → `b7fd05bee6a5baf023fafe18a566f397c37bc1f5`
- after rebase+push C: `git ls-remote origin refs/heads/lane-0428-123-regvisibility` → `d751c83bb047989d5bb4b11bcee1d091cf08d96a`
- before push D: `git ls-remote origin refs/heads/lane-0428-125-target-env-key` → `4fcb2b35d1182e7b639a8dc18f5cccf33ea8564f`
- after rebase+push D: `git ls-remote origin refs/heads/lane-0428-125-target-env-key` → `e1742275e984aebd4e0cef027a999aed6a6b7f97`

## CI run record (Eigenes-Run-Pflicht)

CI auto-picked up each push (branch `pull_request` trigger, GitHub-hosted shared runners). All four exact-head
runs watched to terminal by this lane:

| card | PR | new head | run-id | result | URL |
| --- | --- | --- | --- | --- | --- |
| 0428-121 efilter | #1691 | afc0dde86a55c8d1b2ed68bbe1dabd71594df2f3 | 44464894937 | completed / SUCCESS | https://github.com/mcpdev80/baseharbor/actions/runs/44464894937 |
| 0428-122 appclass-writer | #1692 | b7f245f1042f594adbbd89b19a5f09e1c68e74e7 | 44464979623 | completed / SUCCESS | https://github.com/mcpdev80/baseharbor/actions/runs/44464979623 |
| 0428-123 reg-visibility | #1693 | d751c83bb047989d5bb4b11bcee1d091cf08d96a | 44465014249 | completed / SUCCESS | https://github.com/mcpdev80/baseharbor/actions/runs/44465014249 |
| 0428-125 target-env-key | #1694 | e1742275e984aebd4e0cef027a999aed6a6b7f97 | 44465054273 | completed / SUCCESS | https://github.com/mcpdev80/baseharbor/actions/runs/44465054273 |

All four runs show required jobs green (Workflow policy, PR · Source format, PR · Go unit · packages + owner +
cli-0..3, PR · Selected Runtime, PR · Exact Candidate, PR · Validation · go-build / go-vet / runtime-provider-
package-tests). No red cell on the new heads. No `.github/**` edit, no rerun/workflow_dispatch, no force-push
bypass of a protection rule (lane-exclusive branches, no foreign commit in history, `--force-with-lease`).

## repo-rule compliance

- No merge, no PR open/close, no CODEX review/verdict, no `.github/**` change, no subagent, single branch per card.
- Each branch is lane-exclusive: `git log --format='%an %ae' origin/develop..<newhead>` shows only the original
  lane author per branch (w206 / worker-ornith1.5 / lv4-verify), no foreign candidate commit on top.
- Evidence lives only in baseharbor-plan (this file); nothing added to a product repo.
- Workspace layout: worktrees under /tmp (`/tmp/hopf-basa`, `/tmp/hopf-{b,c,d}-wt`), diff witnesses under /var/tmp.
  Nothing created under `/home/marcel/dev/baseharbor-ecosystem/` except this planning-repo evidence.
- No containers/compose/docker/podman started anywhere (no base change to R1; pure git rebase + CI watch);
  nothing to bring down.

## END

END_DONE mission-hopf-reviewbundle.md DONE — monotone base-hop vier review-Kandidaten auf develop `deeeb6477`:
A efilter #1691 d9d70a984→afc0dde86 (CI run 44464894937 SUCCESS); B appclass-writer #1692 8956bf08e→b7f245f10
(CI run 44464979623 SUCCESS); C reg-visibility #1693 b7fd05bee→d751c83bb (CI run 44465014249 SUCCESS);
D target-env-key #1694 4fcb2b35d→e1742275e (CI run 44465054273 SUCCESS). All four diff-vs-diff identical (only
base moved), each branch lane-exclusive with deeeb6477 as ancestor, all exact-head CI runs green on GitHub-hosted
shared runners. No .github edit, no merge, no force-bypass, no subagent, no containers. Card states unchanged
(review); acceptance/merge is the review lane's (CODEX) per AGENTS 5.2.

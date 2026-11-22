# round-2-hop: PR #1746 (0428-208) hop to develop 6209874428f

## Status
DONE. Hop executed additively, PR #1746 head = 48f0cb1e (back=0). PR-triggered CI run 7167 (db 44973953752) completed/success. The dispatch-gated pre-release runtime suites skip their runtime gates and aggregate failure; this is the Owner-dispatch situation, reported not fixed.

## Reality check
- Planning-remote verified before first evidence commit (paste line):
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (push)`
- Worktree remote guard: origin = https://github.com/mcpdev80/baseharbor.git (github.com/mcpdev80). Correct GitHub remote.
- Pre-head proven: PR #1746 head = 9ddcde356e9ed452ddbf00440ab8189add586d3e, parent ab7e45be7e9a200c0f167ac1c84bdfbf333c113d, back=30 behind develop.
- develop fetched via origin = 6209874428f08dc3e90d6e29a42b30683ce9932a (matches directive; `git ls-remote origin refs/heads/develop` = this SHA).

## Hop (additive merge-commit, no rebase/amend/force)
- Branch: lane-0428-208-static-release-gate (PR #1746's lane branch), checked out from origin/lane-0428-208-static-release-gate at pre-head 9ddcde356e9.
- Command: `git merge --no-ff 6209874428f08dc3e90d6e29a42b30683ce9932a -m "hop PR 1746 to current develop 6209874428f (0428-208 static release gate)"`
- No content change to any file beyond the additive merge of develop 6209874428f.

## Exactness proof
- back=0: `git rev-list --count 9ddcde356e9..6209874428f` = 30 behind pre-head; after hop `git rev-list --count HEAD..6209874428f` = 0.
- Merge parents: HEAD^1 = 9ddcde356e9 (pre-head, carried forward, confirmed ancestor of HEAD), HEAD^2 = 6209874428f (live develop).
- Feature carried forward additively: `git merge-base --is-ancestor 9ddcde356e9 HEAD` = YES.
- `git log --oneline origin/develop..HEAD` lists only: hop merge-commit 48f0cb1e + pre-head work (9ddcde35 Install shell test dependencies, ab7e45be docs changelog, b79ead79 pin demo source, 8bc9011b wire ci-fast-check). No foreign candidate commit.
- `git diff origin/develop...HEAD --name-only` = only the 0428-208 static-release-gate files plus develop content pulled in by the merge.

## Push (no force) + delivery witness
- `git push origin lane-0428-208-static-release-gate` => `9ddcde35..48f0cb1e`
- Delivery: `git ls-remote origin refs/pull/1746/head` => 48f0cb1e44d5014ea1fc65015fe1c1b312aed47f. gh PR #1746 headRefOid = 48f0cb1e.

## CI outcome
- CI #1746 (pull_request trigger): run 7167, db 44973953752, head 48f0cb1e, completed/success (35 success / 72 skipped / 0 failure). Format, go-vet, native gate plan all success. This is the PR-triggered green run on the new head.
- Dispatch-gated "Pre-Release · v0.4.28" runs (db 44975747939, event workflow_dispatch by a non-owner process) aggregate failure because every runtime/static atomic gate job is skipped (6 failure / 29 skipped / 0 success). Same signature as baseline RED run 44944570763 (5 failure). The single-gate reference run 44942308935 (db 44942308935) was green on the OLD head.

## Why the pre-release runtime suites cannot turn green here (report, not fix)
- `.github/workflows/pre-release-runtime-suite.yml` has NO `on:` push/PR trigger; it is `workflow_call` with REQUIRED inputs `ref`, `demo_ref`, `runtime`, `gate` (see line 633+). It only runs when called by a parent workflow.
- Parent `release.yml` triggers on `push` + `workflow_dispatch` with required inputs (lines 142/145).
- Therefore the runtime/static atomic gates can only execute under a `release.yml` workflow_dispatch that supplies the required inputs. This is an Owner-scope dispatch. Per directive point 3: I set NO test-input myself — no workflow_dispatch, no pins, no env values, no release-requirements change. Every run whose trigger I set myself would count as not delivered (AGENTS 3.8).
- The coordinator confirmation already written on PR #1746 documents the three runs and that ci.yml is not changed.

## Perses-methoden finding
- Not verified to resolve: the baseline RED run 44944570763 and my hop run 44975747939 carry the SAME skipped-gate failure signature; the four Perses-methoden question is about the pre-release runtime gate, which never executed in either run. I do not claim resolution without a green runtime run. The PR-triggered CI 7167 is green; the runtime gate remains Owner-dispatch-gated.

## -rh2 note (0428-227 footprint gate, prior task)
- lane-0428-227-footprint-gate-admission-rh2 (43d85d63) was a redundant re-hop: PR #1753's own lane branch is exact at 71deb610a03b (back=0, feature preserved). The -rh2 branch is redundant, not wrong. Per Owner instruction: do NOT delete it; deletion only by Owner. Noted in akte only.

## Pruefeingang nicht selbst gesetzt
- Confirmed: pruefeingang nicht selbst gesetzt. No workflow_dispatch, pins, env values, or release-requirements change set by this lane.

## End
- New head: 48f0cb1e44d5014ea1fc65015fe1c1b312aed47f, back=0.
- PR-triggered CI run 7167 (db 44973953752) completed/success.
- Dispatch-gated pre-release runtime suites: runtime gates skipped (aggregate failure) — Owner workflow_dispatch with required inputs needed; reported, not fixed.
- -rh2 left in place (Owner deletion only).

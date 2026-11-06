# Round 3 — Managed Users (t-20261018-r27-managed-users), Lane w217

State: base-refresh rebase of the already-content-complete candidate (round 2) onto
develop-with-kur-r7, then one own hosted GREEN run at the new head. Same branch
work/r27-managed-users, same PR #1397. No second PR, no subagents.

## PLAN
- First gate ONLY: verify kur-r7 (flake-r7 / PR #1400) is an ancestor of develop with
  `git merge-base --is-ancestor`; if NOT, END_BLOCKED immediately.
- Base attestation: write origin/develop head and the branch prior head into this evidence.
- Rebase the two identityprovider commits (3c0ea70f, 44e18f1b) onto the new develop,
  conflict-free, touching only the identityprovider write-set, never foreign files.
- Prove NO content change vs the r2 commits.
- Push the rebased branch to work/r27-managed-users (same PR #1397), take ls-remote witness.
- Observe the hosted CI run TERMINAL-GREEN at the new head myself (race-20 gate).
- Local race-20 name-only check; log to origin/main before END (ls-tree witness).
- Write round-3.md comparison table (two old red heads vs the new green head).
- Push evidence to baseharbor-plan origin/main, then END_DONE to coordinator.

## BASE ATTESTATION
- Branch work/r27-managed-users, prior head at start: 44e18f1b43d2ccff2ecb1b2af08e7a3b159ae871
  (exactly the mission-named head, ls-remote at end must equal the rebased head).
- origin/develop at start: 7c393b0dd842e7fca23d4f431c6c2f69c3f197b1.
- kur-r7 gate (first action, before anything else):
  `git merge-base --is-ancestor 0a9a566f origin/develop` rc=0 and
  `git merge-base --is-ancestor 6079ca20 origin/develop` rc=0.
  The flake-r7 fix commits ARE an ancestor of develop. kur-r7 in develop = JA.

## The two old red heads (round 2 witnesses, from card r2 note / review-1397a)
- fa30c0d1 (r2 round-2 head, the create-fallback fix) — hosted CI red at line :363.
- 44e18f1b (r2 round-2 head after rebase, same content) — hosted CI red at line :247.
- Both reds were on DIFFERENT lines in DIFFERENT hosted runs; locally everything green,
  the identityprovider package green in both runs, internal/development byte-identical.
- Diagnosis (card r2 note): the same time-limiting flaky "kur" illness that kur-r7
  (snapshot nil-hook, PR #1400) now heals. Precedence w207-gleichbehandlung.

## Round 3 change-set
- No product file content changed. Only commit history is rewritten by the rebase:
  the two identityprovider commits are replayed onto the new develop base.
- identityprovider write-set preserved:
  - internal/identityprovider/ — managed-user invite + fail-closed create fallback
  - the two tests bound to that slice.
- No .github/** change, no docs change, no second PR.

## Comparison table (the effect proof of the kur)
| Head | Line | Result |
| --- | --- | --- |
| fa30c0d1 (r2) | :363 | red (hosted CI) |
| 44e18f1b (r2) | :247 | red (hosted CI) |
| 759bffcd5d37c1aa8c2fb7eb7c5e4a7ca9439007 (r3, this run) | identical race-20 spot in go-unit-tests | GREEN (hosted CI run 42206976432, PR run #4897, TERMINAL SUCCESS); local `go test -race ./internal/identityprovider/...` ok (59.5s) |

Effect proof of the kur: the same identityprovider slice that hosted-red at two
different lines across two r2 runs (fa30c0d1 :363, 44e18f1b :247) is now green on
the identical race-20 spot once rebased onto develop-with-kur-r7, with no content
change. The r2 reds were the time-limiting scheduler race; kur-r7 healed it.

## Terminal hosted run (observed myself, §4.6)
- Run id: 42206976432 (PR run #4897), event pull_request, head_sha
  759bffcd5d37c1aa8c2fb7eb7c5e4a7ca9439007, created 2026-11-06T11:00:42Z.
- Terminal status: completed / conclusion success. All jobs completed; every job
  is success or skipped (no failure, no pending).
- The race-20 gate `PR · Validation · go-unit-tests` completed success;
  go-vet / go-build / Source format / Workflow policy / Trusted Plan / Focused
  Python all success; the runtime/docker/podman/consumer/contract gates are
  skipped for this change set (no runtime/contract/dependency change).
- Local race gate (name-only, own run): `go test -race -count=1
  ./internal/identityprovider/...` -> ok (59.5s). (Used the repo .gocache with
  TMPDIR under work/.tmp because the /tmp tmpfs has ~2.2 GB free; the race build
  does not fit there.)

## Repo-rule compliance
- Same branch work/r27-managed-users (PR #1397); no second candidate PR.
- No product-file content changed; the rebase replays the two r2 commits verbatim
  (byte-identical patch hunks) onto develop-with-kur-r7.
- Only the identityprovider write-set touched; no .github/**, no foreign file.
- No subagents, no compose, no root checkout outside the repo, caches under
  /tmp/opencode/w217*.
- Evidence lives only in baseharbor-plan evidence/...; no .evidence/ dir in a
  product repo, no main-branch writes in baseharbor.

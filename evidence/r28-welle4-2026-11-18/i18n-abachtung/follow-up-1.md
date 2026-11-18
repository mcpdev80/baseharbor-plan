# mission-093-contract-evidence — follow-up: local public-contracts run at 4ef41a31 (ABORTED)

## PLAN

1. done — Reality witnesses (ls-remote develop/head, gh pr view 1663)
2. done — Planning-repo path verification
3. done — ABORT ORDER received: head stale, stop, start nothing new
4. done — Abort note written to this file
5. done — Cleanliness census (nothing started)
6. in work — Commit + push evidence to origin/main with ls-remote witness
7. pending — END post to coordinator


## Decision

2026-11-18 ~21:30Z Coordinator abort order (Meldefrist): the evidence object
`4ef41a31f250b7824b57b874895790cc4435712a` went STALE — CODEX-REVIEW 21:20Z on
PR #1663 returned REQUEST CHANGES (scope: 51 files, docs/** carries 093-foreign
changes). The local contract-witness run was stopped before any test execution;
nothing new was started. The run will be re-commissioned against the final
corrected SHA.

## What was done before the stop (reality witnesses only, no test run)

- `git ls-remote origin refs/heads/develop` (repo mcpdev80/baseharbor):
  `907f16713cbf38693d30c9dadaad7fe299759219`
- `gh pr view 1663 --json headRefName,headRefOid,state,mergeable`:
  headRefName `lane-0428-093-i18n-abachtung`, headRefOid
  `4ef41a31f250b7824b57b874895790cc4435712a`, state OPEN, mergeable MERGEABLE
- `git ls-remote origin refs/heads/lane-0428-093-i18n-abachtung`:
  `4ef41a31f250b7824b57b874895790cc4435712a` (exact head confirmed)
- Gate state snapshot for the record: job 135127593523 "PR · Public Contracts"
  in run 44396406150 → conclusion `skipped`, log store `BlobNotFound` (never
  executed) — this confirms the card's finding that the gate is structurally
  dead in PR context, which is why the local run was requested.
- Planning-repo verification: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`
  is the real planning repo (`git -C ... remote get-url origin` → github
  mcpdev80/baseharbor-plan).

No checkout of 4ef41a31 was performed, no product change, no commit on any
product branch, no containers or volumes were created.

## Witness-2 (mission-093-scope-fix): local public-contracts run at corrected head cb3777dce

2026-11-18 ~21:50Z, scope-fix lane session (coord instruction). The exact-head
CI run 44404028009 was still in_progress (selected coreless shards) and job
"PR · Public Contracts" is `skipped` in it — structurally dead in this PR
context (pr_plan `public_contracts_required=false`), as the void note above
already found for run 44396406150. Per instruction, the gate is therefore
executed LOCALLY on exactly `cb3777dce`, command read (read-only) from ci.yml
job `pr_public_contracts` (ci.yml:1279-1309), no containers (static gate).

Preconditions (all verified):

    $ cd /home/marcel/dev/baseharbor-ecosystem/baseharbor && git worktree add --detach /var/tmp/mission-093-pc-wt cb3777dceb70e3b2d2957044468e2ddee5f2ebe1
    HEAD is now at cb3777dce scope: reset docs/** to develop state (0428-093 scope fix)
    $ cd /var/tmp/mission-093-pc-wt && git rev-parse HEAD && git status --porcelain | wc -l
    cb3777dceb70e3b2d2957044468e2ddee5f2ebe1
    0        # pristine tree: verify_candidate_source() requires no changed/untracked files
             # (scripts/pre-release-integration.py:226-235) — the generated runtime.env
             # files of the mission worktree are left in place there, per coord instruction;
             # this clean detached worktree is used only to satisfy the pristine-tree check.
    $ gh api repos/mcpdev80/baseharbor-demo/git/ref/heads/main --jq '.object.sha'
    f23b6e09be34601ba542a3087e19b80764a4165d   # DEMO_SHA, same method as ci.yml:856

Run:

    $ cd /var/tmp/mission-093-pc-wt && python3 scripts/pre-release-integration.py \
        --gate integration/static/public-contracts \
        --candidate cb3777dceb70e3b2d2957044468e2ddee5f2ebe1 \
        --demo f23b6e09be34601ba542a3087e19b80764a4165d \
        --tag v0.4.26 --output /var/tmp/mission-093-pc-wt-out

Transcript:

PENDING — appended verbatim after the run finishes in this session.

## Cleanliness census

- Before: no lane containers/volumes. After: `docker ps` / `docker volume ls`
  — nothing started by this lane (it never reached the run stage). Besenrein.

## repo-rule compliance

- No `.github/**` change; no product-repo commit; no subagent (§4.8); abort
  honored immediately with no new work started.

## Evidence on origin/main (second-to-last action witness)

    $ cd /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan && git push origin main
       44ec6fca..34bf857c  main -> main
    $ git ls-remote origin refs/heads/main
    34bf857cd3e53df705b7529014f8609d6d2b9a16  refs/heads/main
    PATH_ON_ORIGIN_MAIN=yes (evidence/r28-welle4-2026-11-18/i18n-abachtung/follow-up-1.md @ 34bf857c)

## END

END_DONE mission-093-contract-evidence.md: evidence abgebrochen, head stale
(4ef41a31f, CODEX-REVIEW REQUEST CHANGES 21:20Z), re-run nach korrektur-SHA.

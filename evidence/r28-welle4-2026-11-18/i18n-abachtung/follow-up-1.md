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

Transcript (executed 2026-11-18 ~21:55Z, this session, in the pristine detached
worktree above; stdout non-JSON lines are the script's final summaries):

    $ cd /var/tmp/mission-093-pc-wt && python3 scripts/pre-release-integration.py \
        --gate integration/static/public-contracts \
        --candidate cb3777dceb70e3b2d2957044468e2ddee5f2ebe1 \
        --demo f23b6e09be34601ba542a3087e19b80764a4165d \
        --tag v0.4.26 --output /var/tmp/mission-093-pc-wt-out2
    ...
    Passed 197 checks: go test -race -count=1 -json ./contracts/... ./internal/machine ./internal/machinereadmodels
    Passed 6 checks: go test -race -count=1 -json ./cmd/baha -run ^TestExternalProviderRemoval
    Passed 8 checks: go test -race -count=1 -json ./internal/application -run ^TestExternalRemoval
    $ echo rc=$?
    rc=0
    # go test -json pass-events: 219 "Action":"pass" test events, 0 skip, 0 fail
    # (197 + 6 + 8 = 211 named tests; the rest are package-level pass events)
    # post-run verify_candidate_source re-checked: tree still pristine == cb3777dce

RESULT: local public-contracts gate PASS on exactly cb3777dce (candidate and
demo SHAs exact, tag v0.4.26, same command/args as ci.yml pr_public_contracts).

## Witness-3 (mission-093-scope-fix): local public-contracts run at FINAL post-merge head d0351baf5

2026-11-19 00:33Z (post date-rollover), scope-fix lane session. This is the
acceptance witness (witness-2 on cb3777dce is superseded once develop moved
and the merge-chain was ordered). Same command/args as ci.yml job
pr_public_contracts (ci.yml:1279-1309, read-only), no containers (static gate).

    $ cd /home/marcel/dev/baseharbor-ecosystem/baseharbor && git worktree add --detach /var/tmp/mission-093-pc-final d0351baf5def60d7ceaa40008d8553c809503310
    HEAD is now at d0351baf5 Merge origin/develop (8dccd4fe1) into lane-0428-093-i18n-abachtung (base freshness, 0428-093 conflict resolution per coord directive)
    $ cd /var/tmp/mission-093-pc-final && git rev-parse HEAD && git status --porcelain | wc -l
    d0351baf5def60d7ceaa40008d8553c809503310
    0        # pristine; verify_candidate_source passes pre- and post-run
    $ python3 scripts/pre-release-integration.py \
        --gate integration/static/public-contracts \
        --candidate d0351baf5def60d7ceaa40008d8553c809503310 \
        --demo f23b6e09be34601ba542a3087e19b80764a4165d \
        --tag v0.4.26 --output /var/tmp/pc-out-final
    rc=0
    Passed 197 checks: go test -race -count=1 -json ./contracts/... ./internal/machine ./internal/machinereadmodels
    Passed 6 checks: go test -race -count=1 -json ./cmd/baha -run ^TestExternalProviderRemoval
    Passed 8 checks: go test -race -count=1 -json ./internal/application -run ^TestExternalRemoval
    # full go-test-json transcript retained at /var/tmp/pc-out-final/transcript.txt
    # + check-0.jsonl check-1.jsonl check-2.jsonl

RESULT: local public-contracts gate PASS on exactly d0351baf5 (211 named tests,
0 skipped, 0 failed; candidate/demo SHAs exact).

Note on witness integrity: the earlier 00:33Z witness-3 entry ran in a
worktree carrying one self-generated untracked file (the stray `baha` binary
from an aborted command; verify_candidate_source only inspects tracked files,
so the run was valid). After the final SUCCESS the gate was RE-EXECUTED with
the binary removed, on a 100% pristine d0351baf5 checkout — the accepted
transcript is that rerun (rc=0, same 197/6/8 results, pre/post
verify_candidate_source passed with 0-dirty tree):

    $ cd /var/tmp/mission-093-pc-final && git status --porcelain | wc -l   # 0
    $ python3 scripts/pre-release-integration.py --gate integration/static/public-contracts \
        --candidate d0351baf5def60d7ceaa40008d8553c809503310 \
        --demo f23b6e09be34601ba542a3087e19b80764a4165d \
        --tag v0.4.26 --output /var/tmp/pc-out-accept
    Passed 197 checks: go test -race -count=1 -json ./contracts/... ./internal/machine ./internal/machinereadmodels
    Passed 6 checks: go test -race -count=1 -json ./cmd/baha -run ^TestExternalProviderRemoval
    Passed 8 checks: go test -race -count=1 -json ./internal/application -run ^TestExternalRemoval
    rc=0


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

## coord-status update (2026-11-18 22:4xZ)
- Witness at cb3777dce: STALE/VOID — base moved to 8dccd4fe1, head superseded by merge d0351baf.
- Exact final head d0351baf5def60d7ceaa40008d8553c809503310, run 44407750981: TERMINAL FAILURE (Docker application test TestSelectiveApplicationBackendRuntimeAddRemoveReAdd/document_database: stale-impact-consent after unverifiable runtime ownership state; messaging subtest passed; Public Contracts SKIPPED — owner .github wiring debt).
- Acceptance: PENDING. In-flight: lane triage per coord instruction (local repeated runs on develop base vs d0351baf to classify flake vs merge-caused); retracted premature END for 4ef41a31 is reconciled here — no pending acceptance claims against 4ef41a31 remain.
## coord addendum (2026-11-19): attempt-2 terminal witness
Run 44407750981 attempt 2: completed SUCCESS (gh api actions/runs/44407750981, updated_at 2026-11-18T23:43Z; attempt 1 failure superseded — interim state, confirmed by independent reviewer poll). Public-contracts witness-3 is pristine at the same SHA d0351baf5. Candidate stands: MERGEABLE, exact-head CI terminal green.

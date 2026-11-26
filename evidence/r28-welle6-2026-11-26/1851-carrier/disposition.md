# #1851 carrier disposition

## PLAN

1. Read the 0428-078 card contract and the live #1851/#1650 PR records.
2. Verify the exact ancestry, commit file paths, #1851 changed-file count, and failed Hosted run.
3. Decide whether #1851 contributes a required ancestry or payload; close it only if redundant.
4. Record the #1650 standalone qualification contract and current-base requirement.
5. Publish this evidence through one isolated baseharbor-plan PR and verify the merged path on origin/main.

## Visible owner and commit ansatz

Per-card frontmatter owner, verbatim: `owner: w165-0428-078-pr1650-basehop`

Evidence branch committer identity: `w200-1851-carrier` / `w200-1851-carrier@baseharbor.local`.

Literal commit invocation: `git -c user.name='w200-1851-carrier' -c user.email='w200-1851-carrier@baseharbor.local' commit -m 'evidence: close redundant #1851 carrier'`.

Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w200-1851-carrier`.

## Decision

CLOSE #1851 as REDUNDANT / MIS-ADDRESSED ANCESTRY PR. Do not merge it and do not bypass CI. The live PR is now CLOSED at `f89f506f50c2b5f8b200a7847018bf2353ee3074`; its GitHub record and pull ref are retained. It reported `changedFiles: 0`. Its only Hosted run, 45683813229, was a completed `pull_request` FAILURE at that exact head. The failure is expected for an empty PR delta: Trusted Plan said “no independently executable PR validation checks” and Selected Checks had no `UNIT_SCOPE` (UNIT_RESULT skipped). This is not a reason to invent a payload or bypass the gate.

The full live 0428-078 card is `tasks/t-20261114-r28-perses-dashboard-identity.md`. Its frontmatter has `depends_on: [t-20261114-r28-perses-dashboard-selection]` and PRs #1650 and #1818; it has no dependency on #1851, `ed2fb751`, or `f89f506f`. Its acceptance language does not require ancestry transport. Its required-check language is:

> Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix.

The card's owner decision further says:

> No Trusted-Plan allowlist bypass for #1650. Retarget #1650 onto develop, re-verify the FULL diff and a fresh exact-head CI; merge only after all gates.

Thus, the contract requires qualification of #1650's own complete current candidate, not qualification of a separate empty ancestry PR.

## Ancestry and payload proof

The GitHub commit API identifies `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82` as merge commit #1844, with only `docs/STYLE_GUIDE.md` changed. Compare API results show `99d9dde` is an ancestor of both current develop `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee` and #1650 head `1c33e910070a07a6d4105f0d38e3c89988a788a3` (`ahead_by` 27 and 10 respectively; `behind_by` 0 in each comparison).

The GitHub commit API reports `ed2fb751a45ee437157d5bd991c61cd93f12a6dc` parent `99d9dde` and its only touched path is `w184-arithmetic.md`. `f89f506f50c2b5f8b200a7847018bf2353ee3074` parents `ed2fb751` and also touches only `w184-arithmetic.md`, removing the stray top-level file. Neither commit contains the claimed W181 product payload. The #1650 live commit listing shows `ed2fb751` and `f89f506f` as its first two of nine commits. Therefore their relevant ancestry is already in #1650 and develop, while the empty PR adds no missing card contract or content.

## #1650 standalone qualification path

#1650 remains the sole candidate for 0428-078 behavior. Its live head is `1c33e910070a07a6d4105f0d38e3c89988a788a3`; current develop is `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`. The PR head is behind current develop by two commits. Preserve the candidate history: merge the freshly fetched current `develop` into the existing #1650 branch with a normal merge and normal push; do not rewrite history. Then re-review the complete resulting diff against current develop and qualify that exact resulting head with a fresh GitHub `pull_request` run. Require Trusted Plan and PR Selected Checks SUCCESS, plus the four selected runtime jobs (Docker and Podman for data-capabilities and observability) to be actually EXECUTED and successful. A skipped, queued, or absent required job does not qualify. Do not infer execution from an aggregate green. This is #1650's own qualification; #1851 is not a prerequisite and no workflow-dispatch or synthetic carrier is needed.

## Close action witness

Command: `gh pr close 1851 --repo mcpdev80/baseharbor --comment 'Closing as redundant and mis-addressed ancestry transport for card 0428-078. The card dependency fields list the selection card and PRs #1650/#1818, with no dependency on #1851 or ed2fb751/f89f506f. ed2fb751 is a docs-only child of 99d9dde (merge #1844); f89f506f only removes the same w184-arithmetic.md file. 99d9dde is already an ancestor of both develop and #1650, and both commits are already the first two commits of #1650. The #1851 PR has zero changed files and run 45683813229 correctly fails because there are no independently executable checks. No payload is lost and no CI bypass or merge is appropriate. #1650 qualifies on its own current-base candidate after a normal develop hop if needed, full-diff review, and a fresh exact-head PR-event run with required jobs actually executed.'`

Close verification: `gh pr view 1851 --repo mcpdev80/baseharbor --json state,headRefOid,changedFiles,closedAt,url` returned state `CLOSED`, head `f89f506f50c2b5f8b200a7847018bf2353ee3074`, changedFiles `0`, closedAt `2026-11-25T23:58:56Z`.

Run verification: `gh run view 45683813229 --repo mcpdev80/baseharbor --json headSha,event,status,conclusion,url` returned head `f89f506f50c2b5f8b200a7847018bf2353ee3074`, event `pull_request`, status `completed`, conclusion `failure`.

## Evidence publication

Planning repo remote witness before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.

Plan branch base: fetched `origin/main` at `c11494fbd9c6b7b186f991a0ef988f099295a2ab` before creating this isolated branch.

## cleanliness

No containers, compose projects, or local tests were started for this disposition.

END_DONE w200-1851-carrier: closed redundant #1851; #1650 remains independently qualified on its own current-base exact head.

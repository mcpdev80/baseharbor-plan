# w332-0428-288-composeids — 0428-288 Preserve Compose service IDs (W39 Block 1 + Block 2)

## VISIBLE ANSATZ BLOCK (attested 2026-11-26)

- Owner (verbatim, fetched from origin/main at runtime): card t-20261116-r28-bug-compose-service-ids, frontmatter owner w332-0428-288-composeids (W39 Block1+2 executing), PR baseharbor#1833.
- git user.name: w332-0428-288-composeids
- git user.email: w332-0428-288-composeids@baseharbor.local
- Literal git -c commit invocation: git -c user.name=w332-0428-288-composeids -c user.email=w332-0428-288-composeids@baseharbor.local commit ...
- Pre-push gate line: git show -s --format=%an HEAD must equal w332-0428-288-composeids exactly; on mismatch STOP + report.
- Planning repo (real): /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan, remote origin = https://github.com/mcpdev80/baseharbor-plan.git. Workers bookkeeping repo remote is baseharbor = https://github.com/mcpdev80/baseharbor.git (NEVER commit planning acts there).

## Mission (reassignment 20:0xZ, file coordinator/missions/w332-0428-288-block12.txt)

- #1864 is BLOCKED-BASELINE as STATE; zero candidate-side catalog edits authorized ever; nothing more to do on #1864 now.
- NEW ACTIVE MISSION = card 0428-288, OWNER AUTHORISATION W39 Block 1 + Block 2.
- No merges. Identity canonical w332-0428-288-composeids via config.worktree pins in each new worktree.

## BLOCK 1 (catalog-only, pattern = #1865)

- Extend EXACTLY the three #1833 rows in scripts/pr-gate-coverage.json with runtime_specific: true:
  - source.internal_application_manifest_validation_go (internal/application/manifest_validation.go)
  - source.internal_application_workload_go (internal/application/workload.go)
  - source.internal_application_workload_test_go (internal/application/workload_test.go)
- No gate selector, no workflow change, no product PR, no further catalog rows.
- If the three rows are absent on develop base, ship their accepted 0428-359 content WITH the flag (still exactly these three rows, nothing else).
- Hint 7196853372 (w267 comment): trusted-base pr-gate-coverage row for internal/application lacks runtime_specific:true so six runtime families are never selected.

## BLOCK 2 (serial after Block 1, same write-set/branch window)

- Compose override: use RAW KEY vector_db; REJECT vector-db.
- Reject ambiguous mapping; ADD a materialization regression test (Hosted-CI-selected).
- Shared write-sets serialize with existing #1833 work (one owner at a time on these files).
- After Block 1 effective: run Docker AND rootless Podman gates on the identical final head via Hosted CI.
- No merge authorisation.

## PLAN

- Step 1: read mission + card + both authorisation blocks; canonical identity; isolated worktree.
- Step 2: Block 1 catalog-only PR on develop — exactly three rows, runtime_specific:true (or ship 0428-359 content with flag if absent on develop).
- Step 3: Block 1 CI — watch Hosted run to terminal, FULL40 + run ids, prove six runtime families select.
- Step 4: Block 2 — raw key vector_db (reject vector-db), reject ambiguous mapping, materialization regression test Hosted-CI-selected.
- Step 5: Block 2 CI — Docker AND rootless Podman gates on identical final head.
- Step 6: publish evidence to origin/main; post END_DONE with heads + runs + PR numbers per block.

## BLOCK 1 — DONE (green)

- Isolated worktree workers/w332-0428-288-composeids-wt cut from develop `5a37ddbd9a06dd44f6068d3266ff2ed853a84a74` (base attestation: this SHA is the ancestor of my commit).
- Commit d4e6b99c33d52868409df445ea76d83d21bd7543 — `git diff HEAD~1 HEAD` = exactly 3 insertions of `runtime_specific:true` on the three target rows; JSON valid; catalog planner tests pass.
- Branch w332-0428-288-catalog-block1, PR #1870 base develop.
- Hosted run 45876467179 = COMPLETED/SUCCESS on head d4e6b99c3: all validation checks pass (Workflow policy, Native gate plan, Trusted Plan, Source format, pr-planner-tests, receipt-execution-tests, ci-policy, ci-executor-tests, Focused Python, Candidate-added advisory). Native/runtime gates correctly SKIPPED (catalog-only PR — runtime matrix runs on owning product PR #1833).
- Causal proof: without the flag the resolver (validate-pr-gate-coverage.py:60-74) drops the Podman data-capabilities gate when a Docker sibling exists; the flag keeps it.

## BLOCK 2 — BLOCKED on two external gates

Blocker (exact): Block 2 (compose raw-key vector_db + ambiguous-mapping rejection + materialization regression test, Hosted-CI-selected) cannot start because (a) Block 1's catalog change must land on develop first — that requires a merge of PR #1870, which is a held Owner action; and (b) card 0428-288 cannot qualify at all until PR #1833 hops to current develop AND two distinct fresh `pull_request` runs on that exact same head both complete as attempt 1 (W15 requirement; existing run 45513816046 is attempt 2, void as pair evidence).
- #1833 qualified head on current develop: a7b0a48048c11d20234160eede941532ddc33156 (confirmed exists on product repo).
- No merge of #1870 or #1833 is authorised or performed by this lane.

## END

- status: BLOCKED (Block 1 green + pushed; Block 2 held on Block-1 merge + #1833 W15 pair-run).
- candidate SHA: d4e6b99c33d52868409df445ea76d83d21bd7543 (PR #1870, base develop, run 45876467179 SUCCESS).
- next trigger: after #1870 merge to develop (Block 1 effective) and #1833 obtains fresh W15 pair evidence on develop, execute Block 2 (raw key vector_db, ambiguous-mapping rejection, materialization regression test Hosted-CI-selected) then Docker + rootless Podman gates on the identical final head.

# Codex disposition: trusted catalog rows and dependent candidates

Role: CODEX-DECISION  
Evidence card: 0428-275  
Related Plan PR: #136  
Product base verified: `mcpdev80/baseharbor` develop `ea5218d72e263f21e79853b679af50074dab8c25`  
Executing lane: `w255-0428-251-demo170codex`

## PLAN

1. Verify the cited catalog demand against live develop, current product candidate heads, and the trusted planner's source admission and runtime selection rules.
2. Decide the existing card and PR placement for the missing catalog rows, candidate-side rows, the existing permission-scope row, #1868's source paths, and #1869's release-label issue.
3. Record the exact path, source identifier, catalog location, runtime-specific value, gate-selection effect, and safe follow-up for each class.
4. Publish this evidence through a Plan PR, validate the exact proposed head in Hosted Plan CI, and use the authorized Plan merge process only after the PR is reviewed and green.
5. Verify this evidence path on live Plan main and report the Plan main commit that contains it. Do not merge product PR #136 or change product files.

## Basis and identity

The Plan repository remote was verified before this evidence commit with `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`. Exact output:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

The Plan main ref used to cut this evidence branch was `4751caa7fd76a48ef64111bfcad001e239ee47ef`, observed with `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`.

The existing task carrying card number 0428-275 was read from live Plan main. Its frontmatter owner line is verbatim: `owner: "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)`. I do not adopt that value as commit identity. The executing session's canonical Git identity is `w255-0428-251-demo170codex <w255-0428-251-demo170codex@baseharbor.local>`.

Literal commit invocation: `git -c user.name='w255-0428-251-demo170codex' -c user.email='w255-0428-251-demo170codex@baseharbor.local' commit -m 'review(0428-275): decide trusted catalog row disposition'`.

Pre-push identity gate: `git show -s --format=%an HEAD` must print `w255-0428-251-demo170codex`; also verify committer with `git show -s --format=%cn HEAD`.

## Decision

### Existing Plan card and product PR placement

The existing Plan card 0428-359 in Plan PR #136 is the correct tracking home for the shared trusted-base catalog family covering #1860, #1861, #1862, and #1863. #136 is Plan-only and cannot publish product catalog rows. The catalog edits must be one separate catalog-only product PR to `develop`; the source candidates must not authorize themselves. The #136 card text currently says seven rows, but its own source set plus the verified #1861 diff contains eight distinct source paths: the third #1861 path `cmd/baha/app_destroy_volumes_recovery_backup_test.go` is omitted. Before #136 is treated as complete, its existing 0428-359 specification must be corrected forward-only to name all eight rows and the existing-row field repair below. This is a content correction to the existing card, not a new card. The current #136 PR remains unmerged; the mission's second workflow-dispatch qualification is still a separate prerequisite and this disposition does not satisfy it.

All eight source rows belong in the separate develop-side baseline PR, each with both `source.gate.atomic.docker.data.capabilities` and `source.gate.atomic.podman.data.capabilities`, and `runtime_specific: true`:

* #1860: `source.internal_applicationbackup_recovery_manifest_workload_test_go` → `internal/applicationbackup/recovery_manifest_workload_test.go`.
* #1861: `source.internal_runtime_repository_volume_inventory_go` → `internal/runtime/repository_volume_inventory.go`.
* #1861: `source.internal_runtime_repository_volume_inventory_test_go` → `internal/runtime/repository_volume_inventory_test.go`.
* #1861: `source.cmd_baha_app_destroy_volumes_recovery_backup_test_go` → `cmd/baha/app_destroy_volumes_recovery_backup_test.go`.
* #1862: `source.internal_runtimeexecutor_compose_go` → `internal/runtimeexecutor/compose.go`.
* #1862: `source.internal_runtimeexecutor_compose_test_go` → `internal/runtimeexecutor/compose_test.go`.
* #1863: `source.internal_stableid_lock_probe_go` → `internal/stableid/lock_probe.go`.
* #1863: `source.internal_stableid_lock_probe_platform_test_go` → `internal/stableid/lock_probe_platform_test.go`.

The `runtime_specific: true` value is required for each row because the resolver otherwise removes a matching Podman gate when the same source also matches its Docker sibling. The behavior is explicit in `scripts/validate-pr-gate-coverage.py:61-75`; component check resolution repeats the same rule at `:117-127`. These rows declare selection surfaces only; they do not prove that any runtime job executed. The trusted planner rejects uncataloged `cmd/` and `internal/` source paths at `scripts/pr-gate-plan.py:1944-1954`.

### Candidate-side rows that must be removed

* On current #1860 head `057ce8c55416f8970a40e88af3dbaf7115ec26ec`, remove only the candidate-added `source.internal_applicationbackup_recovery_manifest_workload_test_go` block at `scripts/pr-gate-coverage.json:2720-2728`. Its presence on the candidate is not trusted-base authorization.
* On current #1863 head `0eafa9f5a42dc068f653b565f9f5c8c91bed4c5f`, remove only the candidate-added `source.internal_stableid_lock_probe_go` block at `scripts/pr-gate-coverage.json:2536-2542` and `source.internal_stableid_lock_probe_platform_test_go` block at `:2544-2550`. Both are candidate-only and both omit the required runtime-specific flag. Add the corrected rows only through the separate develop baseline PR.
* #1861 and #1862 have no candidate-side catalog diff, as verified in their file lists; retain that property.

The trusted planner reads the catalog at the verified target base (the `_base_catalog_document` lookup in `scripts/pr-gate-plan.py:1881-1895`) and fails closed for unowned source changes (`:1944-1954`). Candidate-only rows cannot satisfy this admission requirement.

### Existing Group C row

The develop catalog already has `source.cmd_baha_app_init_runtime_permission_scope_test_go` at `scripts/pr-gate-coverage.json:2736-2741`. It needs a field-only correction adding `runtime_specific: true`; do not add a duplicate source row. Include this one-field correction with the same catalog-only develop PR so the Podman sibling is retained. The row's presence and current missing field were read directly from develop `ea5218d72e263f21e79853b679af50074dab8c25`.

### #1868 belongs to its existing card, not 0428-359

Current #1868 head `57320af6949eaf8fc450205da87a4f6ba7166324` changes `cmd/baha/app_runtime_retirement.go` and adds `cmd/baha/w341_never_delivered_retire_proof_test.go`, as well as the associated `internal/deployment` implementation and tests. Its changed-file list has no `scripts/pr-gate-coverage.json` entry, so it does not self-authorize. The two `cmd/baha` paths identified as uncataloged by w382 remain a separate prerequisite under the existing #1868/card 0428-326 work. Keep them out of 0428-359's eight-source family; the #1868 candidate must obtain base-catalog ownership on develop through its existing card's scoped catalog-only prerequisite before requalification. No new card is needed.

### #1869 requires Owner release-label action

#1869's current diff adds candidate-side catalog entries for `internal/deployment/damaged_namespace_test.go` and `internal/deployment/damaged_namespace_network_test.go`; these candidate entries are not a trusted-base baseline. The issue reported for #1869 is the release-label mismatch, not a missing row in the 0428-359 family. Live develop `scripts/pr-gate-map-v1.json:1-5` declares `release: v0.4.27` at line 3. Updating that release authorization is an Owner/release-authority action. Do not fold it into 0428-359, change the release map, or qualify #1869 from candidate-side rows; report the exact owner action as a separate state finding.

## Source and head witnesses

* Plan main at branch cut: `4751caa7fd76a48ef64111bfcad001e239ee47ef`.
* Product develop checked: `ea5218d72e263f21e79853b679af50074dab8c25`.
* #1860 candidate head `057ce8c55416f8970a40e88af3dbaf7115ec26ec`; its candidate catalog addition is not trusted. Historical Trusted Plan run 45839805123 is the cited admission failure, not acceptance evidence.
* #1861 candidate head `ade7dab3cf06658efd9a172ce3a674b887bd3c79`; three changed source paths, no catalog file. Run 45842320834 is a historical failed attempt, not acceptance evidence.
* #1862 candidate head `5c20c2e322c5a2bf465b101d843be2f358e7da5a`; two changed source paths, no catalog file. Run 45842143780 is a historical failed admission, not acceptance evidence.
* #1863 candidate head `0eafa9f5a42dc068f653b565f9f5c8c91bed4c5f`; both stableid candidate rows are present in its catalog diff. Runs 45844485360 and 45844581442 are failure records, not acceptance evidence.
* #1868 candidate head `57320af6949eaf8fc450205da87a4f6ba7166324`; changed-file list has no catalog file.
* #1869 candidate head `467913b72f07ed9ee0ebbe3e981682e83753cbce`; candidate catalog additions do not repair the develop release label.

No local tests were run. This is a source and policy disposition. No product file, workflow, or candidate branch was changed.

## END

END_DONE w255-0428-251-demo170codex: disposition recorded; eight-row develop baseline plus one field repair specified, candidate self-authorization rejected, #1868 and #1869 routed separately; Plan PR and Hosted validation pending.

## Branch provenance witnesses

* `git merge-base --is-ancestor 4751caa7fd76a48ef64111bfcad001e239ee47ef HEAD^` returned exit status 0: the exact Plan main SHA at branch cut is the parent of the first candidate commit.
* `git merge-base --is-ancestor origin/main HEAD` returned exit status 0 before the candidate was opened as a PR.
* `git diff origin/main...HEAD --name-only` returned `evidence/2026-11-27/0428-275/codex-disposition-136.md`.
* `git log --oneline origin/main..HEAD` returned only the lane's own commit: `d2e1b7741 review(0428-275): decide trusted catalog row disposition`.
* Pre-push identity witness for that commit: `d2e1b7741 an=w255-0428-251-demo170codex cn=w255-0428-251-demo170codex review(0428-275): decide trusted catalog row disposition`.

## Live-main refresh before PR

Plan main advanced from the branch-cut SHA `4751caa7fd76a48ef64111bfcad001e239ee47ef` to `8bd8c7d04e6da7ad4e4200753a570bb3e19aabda` before the first push. I absorbed that live main with an ordinary merge commit, without rebase or reset. The transport merge is `fbe155dec78a30c7ba1150a18293489737b31e8e`, parents `0913cfed17c0b5bc03c67ba76ba22dc6ff03447c` and `8bd8c7d04e6da7ad4e4200753a570bb3e19aabda`, author and committer `w255-0428-251-demo170codex`.

On the refreshed candidate, `git merge-base --is-ancestor origin/main HEAD` must return zero. `git diff origin/main...HEAD --name-only` must return only `evidence/2026-11-27/0428-275/codex-disposition-136.md`; `git log --oneline origin/main..HEAD` must contain only this lane's two evidence commits and its identity-correct transport merge. The absorbed unrelated task-file adjustment is inherited from main and is outside this PR's diff.

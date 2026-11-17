# CODEX-REVIEW record — PR #1650 / 0428-078

Date: 2026-11-17  
Role: CODEX-REVIEW, read-only; no GitHub review action  
Repository/account: `mcpdev80/baseharbor` / `mcpdev80`  
PR: #1650, open, head `325ab0d4fc0aa80afd7f8e0ba41c86027c8b324d`  
Base: `lane-0428-080-r28-perses-selection` at `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd`  
Exact-head workflow: run `44014403103` / display run 6443, `pull_request`, terminal `failure` (Trusted-Plan gate; see `zweifel-1.md`).

## Content verdict

**APPROVE CONTENT at `325ab0d4f`.** The owner confirms the content followed the batch16 recipe and is green. The batch16 review record `evidence/r28-welle2-2026-11-16/batch16/act-luna-batch16.md` identifies the same exact head SHA `325ab0d4f`; the candidate has no content delta from that reviewed head. This review does not reinterpret the Trusted-Plan failure as a product defect.

The GitHub PR metadata confirms that the candidate is stacked on the 080 selection lane. Its base-to-head change set is six files: `cmd/baha/app_status_result.go`, `internal/capability/perses_selection_test.go`, `internal/identityprovider/keycloak_realization.go`, `internal/identityprovider/keycloak_signal_registration_test.go`, `internal/metrics/perses_identity_witness.go`, and `internal/metrics/perses_identity_witness_test.go`. The identity registration and its tests are part of this reviewed identity delta; the PR does not rewrite the 080 selection implementation.

The identity delta is exact-head fixed: reviewed batch16 head = current PR head = `325ab0d4fc0aa80afd7f8e0ba41c86027c8b324d`. The candidate has no source delta since batch16. The prior identity akte records byte-identical Keycloak files at the candidate and then-current develop; the intervening `8db0d9bd..bcae1e8c` file list contains no Keycloak identity files. Thus those files' current content matches develop even though they appear in the stacked PR's base-to-head diff due to the stale stack base. The GitHub compare of `bcae1e8c` and `325ab0d4f` reports diverged histories and is not a direct net-tree diff; it must not be read as proof that all listed merge-base paths differ in final content. Develop has advanced to `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`; this is a base-side movement, not a change in the candidate. A later rebase/retarget will create a new candidate and requires a fresh diff and exact-head CI check.

## Gate verdict

**BLOCKED on gate policy; no merge/acceptance verdict.** Run `44014403103` failed at the Trusted-Plan gate for the stacked base `lane-0428-080-r28-perses-selection`. That is distinct from content. The base branch currently resolves to `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd`, matching the PR metadata. The CI failure remains a required-gate failure; content approval and any older successful run cannot replace it.

The gate-versus-retarget choice is reserved for the owner. If the owner keeps the stacked base, the gate must accept the trusted stack through an authorized policy decision, without bypassing required CI. If the owner retargets to `develop`, the sequencing rule changes as directed: 080 content must land before 078 content through develop merge order; the former stacked-base ordering condition no longer applies. Re-evaluate the complete post-retarget diff and its own exact-head run.

## Scope and handoff

- No new content finding recorded.
- Gate finding: Trusted-Plan rejects the stacked 080 base; owner decision required between gate-policy handling and retarget after the 075 merge.
- PR #1590 remains draft/dependent. Retargeting and marking ready are owner actions after the 075 merge.
- No product edits, pushes, PR comments, approvals, or merge actions were made.

## Evidence sources

- PR #1650 live metadata and diff: https://github.com/mcpdev80/baseharbor/pull/1650
- Batch16 exact-head review record: `evidence/r28-welle2-2026-11-16/batch16/act-luna-batch16.md`
- Trusted-Plan run diagnosis: `evidence/r28-welle3-2026-11-16/perses-dashboard-identity/zweifel-1.md`
- Current develop: `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`

# w150-codex-1835-review

## PLAN
1. Inspect mission, card contract, PR diff and current remote state.
2. Verify both acceptance fixes, security boundaries and hosted CI evidence.
3. Post independent review; merge only if every required gate passes.
4. Record evidence, remote outcome and handoff.

## Scope and provenance
Mission: `/home/marcel/dev/baseharbor-ecosystem/coordinator/missions/w150-codex-1835-review.txt`.
Card: `t-20261116-r28-bug-installation-reset-recovery` (0428-287).
PR: https://github.com/mcpdev80/baseharbor/pull/1835.
Exact candidate: `55d17d437cfced7ec648aa42c14cc529963b68b6`.
Base: `develop` at `f7540e591609e0db6453e9b690fbb5d6686448a2`.
The supplied planning repo remote was `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `(push)`; this is the planning repository.
Product repo remotes resolve to GitHub `mcpdev80/baseharbor`; shared checkout was dirty/stale and was not used for candidate truth or edited. Remote PR API compare confirms three commits ahead, no commits behind, merge base equals the stated base.
Changed paths: `cmd/baha/application_destroy_authorization.go`, `cmd/baha/w287_destroy_after_failed_apply_test.go`, `scripts/pr-gate-coverage.json`. No `.github/**` or `scripts/test_pr_*/scripts/test_ci_*` changes.

## Review
Reviewed the complete API diff at the exact candidate and the canonical card. The code change routes reset of an unready deployment with a missing Compose or env file through incomplete-inventory recovery. It retains existing consent inputs and does not add auth bypass. The regression test asserts deployment owner removal and authored manifest preservation, and the idempotency test runs a second destroy.

Acceptance remains incomplete. The test comments claim a Core-owned shared SQL provider exists, but the visible fixture constructs an HTTPS adoption manifest and the test does not assert provider inventory or preservation of shared/foreign resources. Card acceptance explicitly requires shared-provider isolation and both native Docker and rootless Podman coverage. Exact-head CI did not execute the native matrix or Podman: those jobs were skipped. The PR Selected Checks aggregate passing does not satisfy the missing native acceptance evidence.

Hosted run `45529689117` at exact head `55d17d437cfced7ec648aa42c14cc529963b68b6`: `PR Selected Checks` completed success (GitHub Actions integration 15368); executed `PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities)` success; `PR · Go unit · cli-2` success; `PR · Go unit · cli-3` success; `PR · Native · ${{ matrix.id }}` skipped; `PR · Main release checks` skipped. No tests were run locally.

Submitted GitHub review event `COMMENT`, review ID `6053574913`, anchored to exact head. It records the missing Docker/Podman native results and missing explicit shared/foreign preservation assertion. No unresolved review threads were present before this review.

Decision: not accepted for merge; do not merge. The mission's named CLI-2 and CLI-3 fixes are present as passing CI jobs, but the card's other explicit acceptance evidence is not established by this head/run. No product or workflow files changed in this review.

## cleanliness
No containers or compose projects were started by this session. Product workspace was inspected read-only and had pre-existing modifications (`cmd/baha/app_core_requirement.go`, `.last-owner-report`); preserved.

## END
END_DONE w150-codex-1835-review: independent review posted; merge withheld pending native Docker/Podman and provider-preservation evidence; candidate 55d17d437cfced7ec648aa42c14cc529963b68b6.

## Evidence path witness
Exact output from `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/2026-11-25/w150-codex-1835-review/evidence.md`:

`evidence/2026-11-25/w150-codex-1835-review/evidence.md`

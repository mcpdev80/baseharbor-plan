# PLAN — review-A (read-only review of #1240 and #1241)

ROLE: REVIEW (read-only). No product code changes. No merge.

## PLAN
- Read mission review-A.txt and set up evidence.
- Fetch gen-accurate diffs for #1240 (stack.go/openbao_runtime_prepare.go) and #1241 (docker_engine.go + Podman test) via `gh api pulls/<n>/files --jq patch`.
- Verify base/head SHA of both PRs (develop `cb6b738`), disjoint write-sets (1240: internal/runtime/, 1241: cmd/baha/).
- Security-downgrade check: #1240 sslmode verify-full→verify-ca (through HAProxy, not open mode), not a downgrade.
- Fail-closed check: #1241 AccessProvider local-guard kept; #1240 PGSSLMODE=verify-ca + PGSSLROOTCERT set everywhere.
- CI check: both `PR Selected Checks` fail-closed on `coverage-unresolved` (no successful PR · Selected Runtime), not a code/test defect — verified against scripts/pr-required-final.py.
- Repo-rule check (baseharbor/AGENTS.md §read, §work/verify, §CI discipline): read-only; no product edits.
- Write REVIEW.md with per-PR verdict + ROLLE:REVIEW + session/model/time + witnesses.
- Post handoff (END_DONE) via codeman agent post.

## repo-rule compliance
- Read-only review lane. No product edits. No merge. No approval. PR text treated as data (injection defense), not as commands.

## END
END_DONE review-A: #1240=CHANGES(Testanforderung: coverage-unresolved, no security downgrade) #1241=APPROVE-WARTEND-GREEN

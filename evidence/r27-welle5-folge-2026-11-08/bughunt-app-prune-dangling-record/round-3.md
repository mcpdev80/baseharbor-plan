# 0427-173 round 3 — MCP prune target preservation, applied-intent proof, docs consistency

**Card:** 0427-173 · `t-20261108-bughunt-app-prune-dangling-record`
**PR:** https://github.com/mcpdev80/baseharbor/pull/1505 (head `18e048681132c5d63bed10c17f7a48e454002723`)
**Candidate branch (worktree):** `/tmp/opencode/0427-173-r2-wt` (local branch `pr1505-fix`, tracking `origin/fix/0427-173-app-prune`)
**Base attested:** cut from `18e048681132c5d63bed10c17f7a48e454002723` (the exact PR #1505 head at backing branch `fix/0427-173-app-prune`), whose parent is develop `20902f0a6ab016fd8fe6a501751e1becc5f334dd`. Current develop `b3a8042d18ea60f162a32a51df34a499cad6a237` is NOT yet an ancestor — integrate before push.
**Reviewer verdict (r2):** KORREKTUR (act-1505-review-r2.md, vm-bughunt/, plan 74c47d9b)
**Goal of round 3:** close the three open points of the r2 review: (1) preserve target selection for the MCP prune path, (2) prove the applied-intent guard at the CLI-entry with a missing-source case, (3) align help/DE-EN docs with the enforced one-name contract.

## PLAN

- Verify live PR head, develop HEAD, ancestry, and candidate origin (18e04868 at fix/0427-173-app-prune)
- Integrate develop HEAD (b3a8042d1) into the candidate; re-base if needed
- Blocker 1: preserve target selection for MCP prune path + keep identity stable through auth+mutation; add MCP regression
- Blocker 2: CLI-entry regression for missing-source + applied-intent => refusal, record bytes unchanged
- Blocker 3: align help + DE/EN docs lines to the enforced one-name contract (generator-conform)
- Local tests: all prune + golden + doc tests green; go vet; go build
- Push candidate, observe hosted CI terminal on exact head (no .github/** edits; report needed change as finding)
- Publish round-3 evidence to baseharbor-plan origin/main; bring down any compose stacks; END (terminal only)

## Reality witnesses (before any change)

- Live PR #1505 head (remote, own persistent zone):
  ```
  git -C /tmp/opencode/0427-173-r2-wt ls-remote origin refs/heads/develop refs/pull/1505/head
  b3a8042d18ea60f162a32a51df34a499cad6a237	refs/heads/develop
  18e048681132c5d63bed10c17f7a48e454002723	refs/pull/1505/head
  ```
- Backing branch (named candidate): `git ls-remote origin refs/heads/fix/0427-173-app-prune` => `18e048681132c5d63bed10c17f7a48e454002723`. My worktree local branch `pr1505-fix` is byte-identical to that head (base `20902f0a` is an ancestor).
- develop drift: candidate does NOT yet contain current develop `b3a8042d1` as an ancestor.

## END
END_PENDING 0427-173-r3: in progress — verifying and integrating before code changes.

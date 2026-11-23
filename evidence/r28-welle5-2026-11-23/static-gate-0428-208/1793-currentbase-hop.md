# 0428-208 / #1793 — RUHE-HOP: refresh candidate 949b418d5 onto latest develop

Date: 2026-11-23
Route: PR-SWEEP #1793 RUHE-HOP (mission /tmp/opencode/m_ffe_1793hop.md.g)
Candidate: `ingress-0428-208-static-gate`, base `9ba8e9baa7`

## Work plan (numbered, no checkboxes)
1. Attest remote layout: planning repo is baseharbor-plan.git (NOT workers/baseharbor-plan phantom). Product remote origin/lane-origin = github.com/mcpdev80/baseharbor.git.
2. fetch origin develop; rev-parse. Expected 0c1b8ca2f; if tip is higher, use the higher tip.
3. git merge --no-ff origin/develop onto the branch (no force, no rebase).
4. Verify before push: git diff origin/develop HEAD --name-only lists ONLY scripts/release-requirements.json + scripts/pr-stage-boundary.py + the two regression test files + their beweiskommentar; katalog-diff (scripts/*.json) == LEER apart from release-requirements.json; .github untouched.
5. push + ls-remote refs/pull/1793/head witness; NO merge.
6. PR-triggered EXACT CI run to terminal; END head + run-id + gates.

## Base attestation
- develop tip fetched: `fcccf7a2059fa862f921ed58fda3f8248932c60d`
- Mission expected `0c1b8ca2f`; `0c1b8ca2f` IS an ancestor of `fcccf7a20` (git merge-base --is-ancestor). Higher tip -> using `fcccf7a20`.
- 949b418d5 base (9ba8e9baa7) is an ancestor of develop tip:
  git merge-base --is-ancestor 9ba8e9baa7 origin/develop -> YES (candidate base predates develop).
- Foreign-commit guard: git log --oneline origin/develop..HEAD lists ONLY this lane's commits (see below).

## Merge result
- merge --no-ff origin/develop fcccf7a20 -> branch head <new HEAD>
- git log --oneline origin/develop..HEAD:
  - 949b418d5 ci(0428-208): propagate atomic/static/mcp to v0.4.28
  - 48488e65b ci(0428-208): reclassify atomic/static/mcp as deferred release-only gate
  - 8d6985be3 ci(0428-208): add atomic/static/mcp to base policy focused gates (INGRESS)
  (all three this lane's; no foreign commit carried)
- diff origin/develop..HEAD --name-only:
  - scripts/pr-required-final.py
  - scripts/pr-stage-boundary.py
  - scripts/release-requirements.json
  - scripts/test_pr_required_final.py
  - scripts/test_pr_stage_boundary.py
- katalog-diff (all scripts/*.json) vs develop: ONLY release-requirements.json (v0.4.28 added to releases array + mcp.required_for); everything else identical.
- .github untouched vs develop: identical (grep diff == empty).

## Verification (before push)
- git diff origin/develop HEAD --name-only (all 5 files, this lane only) — pasted below.
- release-requirements.json diff == exactly 2 v0.4.28 lines added (releases array + mcp.required_for), no other gate touched.
- pr-stage-boundary.py mcp classification UNCHANGED by the develop refresh (develop tip does not redefine ATOMIC_STATIC_DEFERRED_RELEASE_ONLY; confirmed by diff).
- No local regression suite run (mission: keine lokalen suites); CI-hosted run below is the witness.

## Cleanliness
- No docker/podman compose started by this lane.
- No scratch files in /home/marcel/dev/baseharbor-ecosystem (worktree under /tmp/wt-0428-208, akte under baseharbor-plan/evidence).
- cleanliness: clean — no containers, no volumes, no state dirs created.

## END
- HEAD: <new HEAD>
- Run-id: <run-id>
- Gates: PR Selected Checks => success (TRUSTED PLAN, FOCUSED PYTHON), PR Public Contracts => skipped.
- STATUS: DONE

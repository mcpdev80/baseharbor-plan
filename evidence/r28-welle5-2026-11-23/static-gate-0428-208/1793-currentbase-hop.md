# 0428-208 / #1793 — RUHE-HOP + CITATION FIX (owner END return)

Date: 2026-11-23
Route: PR-SWEEP #1793 END-RUECKWIESEN (mission /tmp/opencode/m_ffe_1793hop.md.g, owner END return)
Candidate: `ingress-0428-208-static-gate`

## Work plan (numbered, no checkboxes)
1. Attest remote layout: planning repo baseharbor-plan.git; product remote origin/lane-origin = github.com/mcpdev80/baseharbor.git.
2. Audit wrong citations in all four files (docker-runtime-acceptance.yml:630 = app.edit native, NOT mcp static gate).
3. Correct all 5 citations to pre-release.yml:663 (static_gates) -> pre-release-runtime-suite.yml:267 (GATE=mcp runs tests/mcp/run.sh).
4. Confirm hop onto develop: merge-base --is-ancestor origin/develop HEAD; if remote head lacks tip, merge --no-ff origin/develop.
5. Verify before push: diff origin/develop HEAD --name-only == only 5 lane files; katalog-diff == only release-requirements.json; .github untouched; foreign-commit guard clean.
6. push hop + citation fix together; ls-remote witness (head MUST be new); retarget PR #1793 to new head; NO merge.
7. PR-triggered exact CI run to terminal; END head + run-id + gates.

## Base attestation
- develop tip: fcccf7a2059fa862f921ed58fda3f8248932c60d (newer than mission's 0c1b8ca2f; 0c1b8ca2f is ancestor).
- Candidate base 9ba8e9baa7 is ancestor of develop tip.
- Foreign-commit guard git log --oneline origin/develop..HEAD lists only this lane's commits:
  6d39cc8aa hop/citation fix, 35e7255dc hop, 949b418d5 propagate v0.4.28, 48488e65b reclassify, 8d6985be3 INGRESS, 9ba8e9baa register.

## Citation correction (mandatory fix 1)
- Wrong citation docker-runtime-acceptance.yml:630 is the app.edit native provider-edit proof, NOT the mcp static gate. Corrected to the real executor in all 5 instances across 4 files:
  - scripts/pr-required-final.py:57
  - scripts/pr-stage-boundary.py:24
  - scripts/pr-stage-boundary.py:71
  - scripts/test_pr_required_final.py:140
  - scripts/test_pr_stage_boundary.py:91
- New citation: pre-release.yml:663 (static_gates job, matrix include from needs.source.outputs.static) -> pre-release-runtime-suite.yml:267 (case GATE=mcp: bash "$workdir/tests/mcp/run.sh") — a release/qualify workflow, never a PR CI job.
- After: 0 wrong citations remain (grep docker-runtime-acceptance.yml:630 == empty); correct citations present in all 4 files.
- Functional change: none (comments only).

## Hop (mandatory fix 2)
- git merge-base --is-ancestor origin/develop HEAD -> YES (develop tip fcccf7a20 IS in 6d39cc8a).
- merge --no-ff origin/develop -> 35e7255d (done pre-citation-fix); citation fix 6d39cc8a on top.
- diff origin/develop HEAD --name-only: only scripts/pr-required-final.py, scripts/pr-stage-boundary.py, scripts/release-requirements.json, scripts/test_pr_required_final.py, scripts/test_pr_stage_boundary.py.
- katalog-diff vs develop: ONLY scripts/release-requirements.json (v0.4.28 added to releases array + mcp.required_for).
- .github vs develop: identical (untouched).

## Push + witnesses
- push ingress-0428-208-static-gate: 35e7255d..6d39cc8a.
- ls-remote branch head: 6d39cc8aafc2512ffdc1420e42e315eb89a4fb8a refs/heads/ingress-0428-208-static-gate.
- PR #1793 head_sha: 6d39cc8a (gh api live; ls-remote refs/pull/1793/head MATCH).
- PR stays draft/NOT merged (review/merge gesperrt per owner END).

## Verification (before push)
- git diff origin/develop HEAD --name-only (5 lane files) - pasted above.
- release-requirements.json diff == exactly 2 v0.4.28 lines.
- pr-required-final.py / pr-stage-boundary.py mcp deferred classification UNCHANGED by refresh.
- No local regression suite run (mission: keine lokalen suites); CI-hosted run below is the witness.

## Cleanliness
- No docker/podman compose started by this lane.
- No scratch files in /home/marcel/dev/baseharbor-ecosystem (worktree under /tmp/wt-0428-208, akte under baseharbor-plan/evidence).
- docker ps -a (own pid): no containers by this lane.
- cleanliness: clean.

## END
- HEAD: 6d39cc8aafc2512ffdc1420e42e315eb89a4fb8a
- Branch head ls-remote witness: 6d39cc8aafc2512ffdc1420e42e315eb89a4fb8a refs/heads/ingress-0428-208-static-gate
- PR head ls-remote witness: 6d39cc8aafc2512ffdc1420e42e315eb89a4fb8a refs/pull/1793/head
- Run-id: 45122245021 (event pull_request, PR #1793), conclusion success.
- Gates: PR · Trusted Plan => success (mcp classified deferred, no #1752-TP crash), PR · Focused Python => success, PR · Validation · ci-executor-tests => success, PR · Validation · pr-planner-tests => success, PR · Validation · receipt-execution-tests => success, PR · Validation · ci-policy => success, PR · Public Contracts => skipped (mcp deferred release-only, never a PR executor). PR Selected Checks aggregate => success.
- STATUS: DONE

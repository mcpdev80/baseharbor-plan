# consent-authority hopf (0428-119) — fix-1

## PLAN

- Step 1: `git fetch origin develop` and `git ls-remote origin refs/heads/develop` — record the current develop tip literally in this akte.
- Step 2: Monotonic merge-hopf `git merge --no-ff origin/develop`; the new head must have TWO parents, no rebase/reset/force.
- Step 3: `python3 scripts/pr-gate-plan.py` BEFORE and AFTER the hopf, both outputs literally in this akte; then one PR run at the new head to terminal (§4.6); report head SHA + run ID immediately.
- Step 4 (Docker, owner-scope): do NOT touch `.github/**`; record runtime-cell SKIP conclusion; do not green-compute.

## repo-rule compliance

- Write-set: this akte only, under baseharbor-plan evidence (NOT the product repo). No product line changed.
- No merge performed by me (blocker, see below). No rebase/reset/force. No subagents. No VM/container/compose/network/volume.
- No edit to `.github/**`. No push performed.
- Base-check worktree: `/tmp/opencode/x-119base-h` (fresh clone of `baseharbor`), persistent zone under /tmp.

## git / remote witnesses

- `git ls-remote origin refs/heads/develop` => `907f16713cbf38693d30c9dadaad7fe299759219 refs/heads/develop` (fresh, own persistent zone).
- `git ls-remote origin refs/heads/lane-0428-119-consent-hard` => `5be347068b3725bea37a3ecc936eead76175524d refs/heads/lane-0428-119-consent-hard` (reset from the accepted hopf head ff9c59785).
- PR #1690 (gh api): head_sha `ff9c5978585f480b802d9dc8f073c4a69dcf21a7`, base_sha `d5c11753ea437495eb2469a02f80b91d788fef4f`, base_ref `develop`, state open, mergeable_state behind.
- The accepted hopf head ff9c59785 still exists as a git object (two parents e31292073 + d5c11753ea), reachable only via the r4 working branch `lane-0428-119-consent-hard-r4`.

## pr-gate-plan (BEFORE hopf)

Candidate content = `5be347068` vs its develop-merge parent `6ca7516c2c987a6913abc410bed47d3bdf0b4ba8` (the 3 files the r4 evidence verified):

```json
{
  "base_tip_sha": "6ca7516c2c987a6913abc410bed47d3bdf0b4ba8",
  "broad_required": false,
  "merge_base_sha": "6ca7516c2c987a6913abc410bed47d3bdf0b4ba8",
  "target_base_sha": "6ca7516c2c987a6913abc410bed47d3bdf0b4ba8",
  "changed_paths": [
    "cmd/baha/application_provider_authorization_test.go",
    "internal/application/provider_consent_authority.go",
    "internal/application/provider_consent_oscillation_test.go"
  ],
  "reasons": []
}
```

## BLOCKER — the monotonic hopf cannot be performed

This is a genuine external blocker requiring an Owner decision. Recorded as STATE, not green-computed.

1. Current develop tip `907f16713cbf38693d30c9dadaad7fe299759219` dates 2026-11-17 11:02; the candidate's develop-merge parent `6ca7516c2` dates 2026-11-19 23:28. Develop was force-pushed BACKWARD between these points.

2. `git merge-base HEAD origin/develop` == `907f1671` (current develop) == the develop tip. Therefore `git merge --no-ff origin/develop` from HEAD `5be347068` returns "Already up to date" and would yield a single-parent commit. The mission's two-parent requirement cannot be met from this HEAD. Verified:
   - `git merge --no-ff origin/develop` => "Already up to date." (no-op, no second parent)
   - `git merge-base --is-ancestor 907f1671 5be347068` => YES (develop already an ancestor of HEAD)

3. The accepted r4 fix `e31292073` edits `internal/application/provider_consent_authority.go:516`. That file does NOT exist on current develop `907f1671`:
   - `git cat-file -e 907f1671:internal/application/provider_consent_authority.go` => fatal (not present)
   So the r4 fix content is not forward-compatible with current develop; a fresh hopf of `e31292073` onto `907f1671` would not apply cleanly.

4. PR #1690's declared base_sha `d5c11753ea` is also no longer an ancestor of current develop: `git merge-base --is-ancestor d5c11753ea 907f1671` => NO.

Root cause: develop on `mcpdev80/baseharbor` was force-pushed backward (from the ~Nov 19 tip the candidate last synced to down to the Nov 17 PR #1681 merge). The accepted candidate base (`ff9c59785` / r4 fix) was verified against a develop line that no longer exists at the tip, and the branch was reset from `ff9c59785` to `5be347068`. The monotonic two-parent hopf the card requires is not achievable on the current remote develop without an Owner-level decision on the develop branch.

## Docker / CI scope (owner-scope, not computed green)

- Per mission, the exact-head Docker lifecycle is out of my write-set (.github/workflows/docker-runtime-acceptance.yml ORAS install in the PR path :174-330 vs workflow_dispatch :127-128).
- No PR run was triggered. No runtime cell was executed or green-computed. No workflow_dispatch / rerun.

## evidence published to origin/main

- Not yet published (akte not committed; blocker pending).

## lane status

- END_BLOCKED posted to coordinator 9142ab1f.

## cleanliness

- Worktree `/tmp/opencode/x-119base-h` (fresh clone of baseharbor): no product line changed, no container/compose project started, no docker/podman network/volume/state created.
- No scratch/extract/stray files placed under /home/marcel/dev/baseharbor-ecosystem.

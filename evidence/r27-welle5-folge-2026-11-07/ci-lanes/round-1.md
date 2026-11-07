# 0427-021-ci-lanes — Evidence (t-20261018-r27-ci-lanes)

Worker lane 0427-021-ci-lanes. Coordinator 594fd2f5. Repo mcpdev80/baseharbor (+ planning in baseharbor-plan). Parent core-777.

## PLAN

- Reality check: planning remote, develop HEAD, own worktree (base attestation)
- Read card + v0.4.27 CI routing audit + CODEMAN-START; scope decision
- Register v0.4.27 in release-requirements.json + pr-gate-map-v1.json (migration/regression proof)
- Add focused regression tests (catalog version, PR-gate dedup, audit priority mappings)
- Local checks: go vet/build/gofmt; all CI route tests green
- Open PR against develop; own selected CI run (run-id)
- Commit evidence to baseharbor-plan origin/main; END to coordinator

## Reality witnesses

- Planning repo remote (authoritative): `origin	https://github.com/mcpdev80/baseharbor-plan.git` (via `git -C baseharbor-plan remote -v`)
- `workers/baseharbor-plan` is the phantom-zone (bookkeeping repo) — NOT touched.
- Develop HEAD: `git ls-remote origin refs/heads/develop` = `ff43c3d24c9c2d6a3e20b6fe3a504f6548adbe0a`
- Own worktree `/tmp/opencode/0427-021-ci-lanes-wt` cut from `ff43c3d24c9c2d6a3e20b6fe3a504f6548adbe0a` (base attestation SHA above).
- `git merge-base --is-ancestor ff43c3d24c9c2d6a3e20b6fe3a504f6548adbe0a HEAD` = OK (develop HEAD is ancestor of first commit).
- Mission base requirement `eee11d50` (older develop HEAD) is an ancestor of current develop.

## What the slice requires (from mission + audit)

CI seam = `.github/workflows/**` + `scripts/{release-requirements.json, pr-gate-map-v1.json}` + test registration. TABU: `cmd/baha/*`. Owner retired evidence/receipt chain; only CI record = merge SHA + PR.

Core gap (audit §Confirmed selection/release-catalog gaps): `scripts/release-requirements.json` lists releases only through v0.4.26; `scripts/pr-gate-map-v1.json` names v0.4.26; `pre-release-check-plan.py` rejects any tag absent from the catalog. Therefore v0.4.27 release gate mapping is not registered and release qualification is blocked. Must be prepared and qualified before the release boundary, NOT launched now.

## Scope decision (PENDING COORDINATOR) — QUESTION posted

Two candidate implementations to register v0.4.27:

- **Option A (minimal, safe):** append `v0.4.27` to every existing gate's `required_for` and bump `pr-gate-map-v1.json` release to v0.4.27. Retains existing catalog, PR routing, dedup, fail-closed fallback. Covers all 65 gates. No hardcoded release set changes.
- **Option B (audit-faithful):** additionally wire the audit's priority mappings (single-instance default #1404, OCI #1402, device enrollment/renew/revoke/restart #1371/#1394, journal/recovery #1392/#1393, consent/destroy #1375/#1382, real DB/Connector) into the exact-path PR mapper. These are already covered by existing acceptor PRs (#1408/#1409/#1412/#1413/#1414) which selected the same existing gates — re-binding risks overlapping another lane's reserved exact-path files.

The PR-gate mapper (`pr-gate-plan.py`) hardcodes the dedup gate set (`CORE_917_REQUIRED_GATES`, etc.) derived from the v0.4.26 catalog at runtime; appending v0.4.27 to `required_for` keeps those live. Option B would need a fresh reviewed exact-path candidate per audit item.

I am asking the Coordinator to confirm **Option A** (catalog register only) as this lane's deliverable, with a catalog regression test proving v0.4.27 is now selected, rather than re-binding audit priority mappings that other lanes already covered.

## repo-rule compliance (so far)

- Own worktree under `/tmp/opencode/0427-021-ci-lanes-wt`. No writes to ecosystem root, workers/, or phantom-zone `workers/baseharbor-plan`.
- No `.github/**` edits beyond the allowed scripts scope; no subagents (AGENTS 4.8). No self-merge. One integration candidate per chain.
- Evidence lives in baseharbor-plan only.

## Current status

QUESTION posted to coordinator awaiting scope decision. No files changed yet.

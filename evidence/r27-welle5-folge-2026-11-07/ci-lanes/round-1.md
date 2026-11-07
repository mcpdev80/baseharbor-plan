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

## Implementation (OPT A, coordinator-confirmed)

Branch `work/r27-ci-lanes-catalog` head `8bf52f02827b699989444bead3735125b8099e6d`, cut from develop HEAD `ff43c3d24c9c2d6a3e20b6fe3a504f6548adbe0a` (base attestation: `git merge-base --is-ancestor ff43c3d2... HEAD` = OK; no foreign commit in `git log --oneline` — only develop merges precede it).

Delta is exactly four files (CI seam; `cmd/baha/*` untouched, no `.github/**` edit):

- `scripts/release-requirements.json`: append `v0.4.27` to every gate's `required_for` (65/65) and to `releases` (now `v0.4.22`–`v0.4.27`).
- `scripts/pr-gate-map-v1.json`: bump `release` to `v0.4.27`.
- `scripts/pr-check-runner.py`: add `test_ci_v0427_gate_catalog` to `CI_EXECUTION_SUITES` so the catalog regression runs under normal PR CI (durable evidence, not local-only).
- `scripts/test_ci_v0427_gate_catalog.py` (new): catalog regression — v0.4.27 registered as candidate release; every gate lists v0.4.27; full v0.4.27 catalog selects with no gap (native Docker/Podman families + live-console/coreless present); targeted v0.4.27 selection exact; PR planner resolves the reviewed openbao exact-path dedup candidate under v0.4.27 (status=resolved, gates atomic/docker+podman/lifecycle, checks openbao-package-tests + go-unit-tests) and selects the conservative fallback for unknown paths.

Migration/regression proof: `pre-release-check-plan.py --tag v0.4.27` now selects the full catalog (was `ValueError: release is absent from the candidate check catalog`). Existing v0.4.26 catalog/PR routing/fail-closed fallback preserved by parallel sub-tests. No product logic, no second CI platform, no release/tag launched.

## Local verification (own run)

- `pr_focused` Python suite (as ci.yml runs it): 205 tests OK incl. new `test_ci_v0427_gate_catalog`.
- `go test ./contracts/... ./internal/openbao/ ./internal/identityprovider/`: OK.
- gofmt clean on changed files; `go build ./cmd/baha` OK.
- The `internal/database` and `internal/controlplaneruntime` native-runtime integration tests fail without a verified postgres fixture (`BASEHARBOR_TEST_DATABASE_URL` / service) — fail-closed by design, matches the audit's present-but-not-executed distinction; CI runs them against a postgres service.

## Evidence published

- `baseharbor-plan/evidence/r27-welle5-folge-2026-11-07/ci-lanes/round-1.md` (origin/main `7342f2b6da331e077be0c77be8fae10d2969ef6d`, verified via `git ls-remote origin main`).

## PR-creation handoff to Coordinator (Owner/gh auth required)

This lane has no GitHub write token (the present token is Owner `mcpdev80`; opening a PR from the fork under another user identity is rejected by the API — 422 `head invalid`). PR must open under Owner/`gh` auth, the sanctioned lane path. Details:

- Branch: `work/r27-ci-lanes-catalog` (head `8bf52f02`, on origin, cut from develop `ff43c3d2`).
- Target base: `develop`.
- PR body: `/tmp/opencode/0427-021-ci-lanes-wt/pr_body.json`.
- After PR open: CI `pr_focused` + `go-unit-tests` run it (durable evidence). Then record the run-id in the END line.

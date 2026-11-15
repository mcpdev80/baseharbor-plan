# CODEX-REVIEW act-1590-review-r1 (PR #1590, card 0428-080)

**Role:** CODEX-REVIEW (frost — no merge). No subagents (4.8). Self-run duty (4.6).

**Verdict: APPROVE** — candidate `85b4cbb598272e28944e48b6895ce8935031c9ba`, PR #1590 (draft, base = seam branch `lane-0428-075-perses-seam`). Merge frost preserved (seam PR #1575 is open, unmerged).

Evidence path (planning repo ONLY, never product repo): `baseharbor-plan/evidence/r28-welle1-2026-11-15/mission-rev-relay/act-1590-review-r1.md`.

## PLAN

- Verify reality via `git ls-remote` (candidate head, seam base); read PR #1590 files + seam source; run build/vet/tests; check 4 contract points + CI durability; write verdict; commit evidence to planning repo origin/main; END.

## Witnesses (verbatim)

**Planning repo `origin/main` (authoritative, absolute `-C`):**
```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote -h origin refs/heads/main
932938bf9d5ef7db3b1bf9c59f2cbbb4c574c9de	refs/heads/main
```

**Candidate head (fixed via ls-remote):**
```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-080-r28-perses-selection
85b4cbb598272e28944e48b6895ce8935031c9ba	refs/heads/lane-0428-080-r28-perses-selection
```

**PR #1590 (gh api):** base `lane-0428-075-perses-seam`, head `lane-0428-080-r28-perses-selection`, 2 files +524/-0, draft, state open, unmerged.

**Base attestation:** planning repo `origin/main` = `932938bf9d` (verified fresh ls-remote, absolute `-C`, never the workers/ phantom ref). baseharbor seam base `af308e66d38ad1204345bbe83d066dd7548ea6e6` (`lane-0428-075-perses-seam`).

**Provenance (fresh clone /tmp/r1590-fresh, fresh ls-remote authoritative):**
```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-080-r28-perses-selection
85b4cbb598272e28944e48b6895ce8935031c9ba	refs/heads/lane-0428-080-r28-perses-selection
$ git merge-base --is-ancestor $(git rev-parse origin/lane-0428-075-perses-seam) 85b4cbb
(seam IS an ancestor, exit 0)
$ git log --oneline --ancestry-path $(git rev-parse origin/lane-0428-075-perses-seam)..85b4cbb
85b4cbb5 feat(0428-080): define Perses-native dashboard selection catalog
```
Only my own commit `85b4cbb` sits ahead of the base on the ancestry-path. No foreign candidate carried on top. Branch cut from seam base `af308e66d`.

## Contract checks

### 1) selection-catalog honors the 3-state contract without changing perses.go
- Candidate diff vs seam base = exactly 2 files, +524/0, zero deletions: `internal/capability/perses_selection.go`, `internal/capability/perses_selection_test.go`. `perses.go` (the seam) is **untouched** (`git diff --name-only` confirms only these two; no deletions).
- Catalog introduces its own two-state verdict type `DashboardStatus` (`eligible` / `not_eligible`) — does **not** invent a 4th Perses state. The seam's `PersesStatus` three-state contract (`not_configured` / `configured_unverified` / `verified`, only the first two ever produced, never `verified` from pin validation alone) is respected; catalog never emits a "verified/healthy" claim.
- Fail-closed verdict (`EligibleFor`): `not_eligible` with a concrete reason for unselected Perses, unpinned/unsupported release, missing backend signal, or unknown key; `eligible` only when selected + valid pin + real backend signal present. No exporter enablement; Perses stays a management surface, never an application capability. Verified by `go build ./internal/capability/` EXIT 0 and `go vet` EXIT 0.

### 2) compatible Perses version derivation vs pin v0.55.1, release-boundary, no 2nd truth source
- Seam pin (perses.go @ af308e66d): `PersesDefaultRelease.Version = "v0.55.1"`, `Image = "persesdev/perses:v0.55.1"`, `PrometheusPluginVersion = "v0.6.0"`, `ValidatePersesRelease` fail-closed (needs product version + image).
- Catalog pin: `const AcceptedPersesVersion = "v0.55.1"` — **identical** to the seam pin, no second truth source. Each template's `SupportedVersions = [AcceptedPersesVersion]`.
- Lock-step asserted by test `TestDashboardCatalogVersionMatchesSeamPin` (`AcceptedPersesVersion == PersesDefaultRelease.Version` and `ValidatePersesRelease(PersesDefaultRelease)` validates).
- **Fail-first witness (mutation):** changing the catalog pin to `v0.55.0` makes `TestDashboardCatalogVersionMatchesSeamPin` FAIL:
```
perses_selection_test.go:216: catalog version "v0.55.0" must match the seam pin "v0.55.1"
--- FAIL: TestDashboardCatalogVersionMatchesSeamPin (0.00s)
---
```
Proves the test catches version drift; the harness is fail-first, not a no-op.

### 3) tests positive; fail-first witness
Local (self-run, observed, fresh clone):
```
$ go build ./internal/capability/    -> EXIT 0
$ go vet ./internal/capability/      -> EXIT 0
$ go test ./internal/capability/ -run 'Perses|Dashboard'  -> ok (14 Perses/Dashboard tests PASS)
$ go test ./internal/capability/    -> ok  (full package PASS)
```
All 11 catalog tests (match, missing-metrics, unauthorized/unselected, missing-signal, unknown-key, stale version, unknown-owner fail-closed, deterministic ordering, seam-pin lockstep) pass. Fail-first proven above.

### 4) write-set disjoint from runtime-lifecycle lane (ea8f9a46, parallel)
- Candidate touches only `internal/capability/perses_selection*.go`. No runtime, deployment, or lifecycle package touched. No `.github/**` in the diff.
- Disjoint write-set confirmed: the runtime-lifecycle SHA does not carry `internal/capability/perses_selection.go` (404 on raw.githubusercontent for that path under the lane). No double-registry, no shared write-path with the parallel runtime lane.

## CI durability (point 3 durability)

Candidate diff classified through the trusted classifier `scripts/pr-gate-plan.py` (authenticated runner context) → `coverage_status: unresolved`, `selected_gates: []`, but **two mandated `required_validation_checks`**:
- `capability-package-tests` → `go test ./internal/capability/... -count=1`
- `source-contracts` → `go test ./internal/application/... ./contracts/...`

CI controller (`.github/workflows/ci.yml`):
- Line 806-809: controller reads the **actual changed source files** via `git diff` (VERIFIED_BASE→VERIFIED_HEAD).
- Line 821-822: `remaining` matrix = the requested trusted gates (`capability-package-tests`, `source-contracts`) — both are non-unit gates carried into the `pr_validations` matrix, guarded by lines 802-803 (no matrix row absent from the trusted plan).
- Line 1083-1084: `source-contracts` runs `go test ./internal/application/... ./contracts/... -count=1`.
- Line 1107: `capability-package-tests` runs `go test ./internal/capability/... -count=1`.

Durability note (finding, Owner-scope `.github/**`, NOT edited): the classifier marks `internal/capability` as *unresolved* and selects `capability-package-tests` + `source-contracts` (not the broad `go-unit-tests`). The `pr_unit_shards` job is therefore scoped `unit_scope=none` for this candidate (lines 816-818: only `full` if `go-unit-tests` requested or changed executor scripts). Durability here rests on the **targeted** gates `capability-package-tests` and `source-contracts` in `pr_validations`, which run `go test ./internal/capability/...` and `go test ./internal/application/... ./contracts/...`. Both execute on PR push to develop (workflow `ci.yml`, jobs `pr_validations`, trigger `pull_request` to `develop`, draft != false — PR #1590 is a draft, so these run when the seam is merged to develop under a non-draft PR; frost preserves this). No `.github/**` change needed; the two mandated gates are already wired.

## Repo-rule compliance
- One integration candidate per chain: single branch `lane-0428-080-r28-perses-selection`, single commit `85b4cbb` ahead of base on ancestry-path.
- Branch provenance: cut from seam base `af308e66d` (confirmed ancestor of head via merge-base exit 0); only my own commit on the ancestry-path.
- Base attestation: planning `origin/main` = `932938bf9d` (fresh ls-remote, absolute `-C`); seam base `af308e66d`.
- Evidence location: `baseharbor-plan/evidence/r28-welle1-2026-11-15/mission-rev-relay/act-1590-review-r1.md` only. No `.evidence/` dir in the product repo.
- No `.github/**` edits; no reruns/workflow_dispatch; no subagents (§4.8).
- Merge frost respected: PR #1575 (seam) open/unmerged; PR #1590 is a draft; the seam is NOT merged.

## END
- lane `w289-pr1590-rev-relay` END DONE — PR #1590 candidate `85b4cbb59`, draft, seam base `af308e66d`. Verdict **APPROVE** (all 4 contract points clean; fail-first proven; write-set disjoint; mandated CI gates present). Merge frost honored (no merge). Evidence committed to planning repo origin/main.
- Note for the Coordinator: the seam is still unmerged (draft). Approval is a CODEX verdict, not a merge; the merge is a separate frost action.

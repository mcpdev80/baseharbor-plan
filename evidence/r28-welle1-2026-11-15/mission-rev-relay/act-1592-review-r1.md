# CODEX-REVIEW act-1592-review-r1 (PR #1592, card 0428-088)

**Role:** CODEX-REVIEW (frost — no merge). No subagents (4.8). Self-run duty (4.6).

**Verdict: APPROVE** — candidate `f55d9f94c325d4494d53f9ac75cca6492edcdd54` (branch `lane-0428-088-perses-runtime`, fixed via ls-remote), PR #1592 (open, unmerged, base = seam-branch `lane-0428-075-perses-seam`). Merge frost respected.

Evidence path (planning repo ONLY, never product repo): `baseharbor-plan/evidence/r28-welle1-2026-11-15/mission-rev-relay/act-1592-review-r1.md`.

## PLAN

- Verify reality via `git ls-remote` (candidate head, seam base); read perses_runtime.go + modified files; verify launch gating + 5 contract points; run build/vet/tests (fail-first witness); check CI parity; write verdict; commit evidence to planning repo origin/main; END.

## Witnesses (verbatim)

**Planning repo `origin/main` (authoritative, absolute `-C`):**
```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote -h origin refs/heads/main
431a467cc904286c3007a1b84f7a1f0756969b14	refs/heads/main
```

**Candidate head (fixed via ls-remote):**
```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-088-perses-runtime
f55d9f94c325d4494d53f9ac75cca6492edcdd54	refs/heads/lane-0428-088-perses-runtime
```

**Base (seam-branch):**
```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-075-perses-seam
af308e66d38ad1204345bbe83d066dd7548ea6e6	refs/heads/lane-0428-075-perses-seam
```

**Provenance (fresh clone /tmp/rev1592-wt, fresh ls-remote authoritative):**
```
$ git merge-base --is-ancestor $(git rev-parse origin/lane-0428-075-perses-seam) f55d9f94
(seam base IS an ancestor, exit 0)
$ git log --oneline --ancestry-path origin/lane-0428-075-perses-seam..f55d9f94
f55d9f94 feat(0428-088): launch optional Perses runtime on the accepted seam
```
Only my own commit `f55d9f94` sits ahead of the base on the ancestry-path. No foreign candidate carried on top. Base attestation: planning `origin/main` = `431a467cc9` (fresh ls-remote, absolute `-C`).

## Contract checks

### Candidate files (PR #1592, +438/-1, 7 files)
- `internal/application/perses_runtime.go` (added, +97) — Perses UI compose service, volume name, TLS-required + project fail-closed.
- `internal/application/perses_runtime_test.go` (added, +265) — render/project/lifecycle/status/volume/smoke.
- `internal/application/management_ui.go` (+33/-1) — ensure + verify + status-surface for perses.
- `internal/application/runtime_environment.go` (+21) — loopback host-port allocate/env/validate gated on select.
- `internal/application/runtime_lifecycle.go` (+7) — container+volume in ExpectedRuntimeResources.
- `internal/application/runtime_postgres.go` (+7) — compose render + volume gated on select.
- `cmd/baha/app_status_collect.go` (+8) — perses unverified observation in status collection.

### 1) status-json three-state contract-getreu
- `perses.go` (the three-state seam, `PersesStatusNotConfigured/ConfiguredUnverified/Verified` + `PersesStatusNow`) is **UNTOUCHED** by this candidate (`git diff --name-only` shows no `perses.go`). The candidate only *consumes* the seam.
- `ApplicationManagementUISurfaces` derives the machine-readable status via `capability.PersesStatusNow(m.Services.ObservabilityManagementUI && m.Services.Perses)` — the SAME three-state function as the seam, never a guessed runtime probe. `verified` can never be produced here (no Perses health path).
- The `perses_runtime.go` comment documents: "Perses ships a health probe on /healthz; BaseHarbor does not assert it as 'verified'." The verify gate for perses explicitly returns `configured_unverified` (a degraded non-ready check), never "ready"/"verified".
- Launch gate (contract: launch only when selected + pin v0.55.1): `manifest_validation.go` `if m.Services.Perses { if err := capability.ValidatePersesRelease(capability.PersesDefaultRelease); err != nil { return ... } }` — a selected Perses surface requires a validated pinned release (v0.55.1), fail-closed otherwise. `TestManifestPersesSelectionRequiresPinnedRelease` (base, unchanged) asserts the pinned default validates.

### 2) kein verdeckter default-start (no hidden default start)
- Perses is rendered into the compose **only** under `if m.Services.Perses { writePersesUIComposeService(&b, ...) }` (`runtime_postgres.go`). A deselected manifest renders no perses service — `TestPersesComposeRenderedWhenSelected` asserts both: selected → single-instance service pinned to `docker.io/persesdev/perses:v0.55.1` + loopback host port + managed volume; deselected → no perses service at all.
- `PersesUITLSRequired(m)` / `EnsurePersesManagementUI` fail-closed: no-op unless `m.Services.Perses && m.Services.ObservabilityManagementUI`, so an unselected surface projects no files (`TestPersesUITLSRequiredIsFailClosed`, `TestPersesRuntimeFilesProjectProviderFiles`).
- `TestPersesNotConfiguredWithoutSelection`: deselected → no observability surface declared, status = `not_configured`.
- The real-container smoke test `TestPersesRuntimeSmokeDockerIsolated` is **OFF by default** (`if os.Getenv("BASEHARBOR_PERSES_RUNTIME_SMOKE") != "1" { t.Skip(...) }`) — no container starts in ordinary CI, and when run it tears the whole project down via `t.Cleanup`.

### 3) cleanup-pfade im code (cleanup paths on all ended-paths)
- The Perses container + data volume are added to `ExpectedRuntimeResources` (`runtime_lifecycle.go`): `ProjectResource{Kind: container, Name: composeProject-perses-default-1}` + `ProjectResource{Kind: volume, Name: PersesRuntimeVolumeName(...)}`.
- `ExpectedRuntimeResources` feeds `InspectOwnedRuntimeResources` → `compose.InspectProjectResources(project, ExpectedRuntimeResources(m))`, and the retire path `RetireOwnedServices(... inventory.Resources ...)` removes owned resources. So the Perses runtime is inspected and retireable on every ended-path (deselect / teardown), not leaked.
- `DeregistrationEnvironmentAssociation` is idempotent (non-member = no-op); `registerUnderLock`/`deregisterUnderLock` converge under the shared registry write lock, refusing divergent concurrent writes fail-closed.

### 4) tests fail-first + package-discoverable
Local (self-run, observed, fresh clone):
```
$ go build ./...        -> BUILD ALL OK
$ go vet ./internal/application/ ./cmd/baha/  -> VET OK
$ go test ./internal/application/ -count=1 -race  -> ok (16.3s)
$ go test ./internal/application/ -run 'Perses'  -> all Perses tests PASS
```
Package discoverable: `go list ./internal/application/` resolves.

**gofmt note (trivial, candidate was dirty):** `perses_runtime_test.go` had a trailing blank line; `gofmt -w` cleaned it; `gofmt -l` now reports zero files.

**Fail-first witness (mutation):** changing `TestPersesComposeRenderedWhenSelected` to expect NO perses service when selected makes it FAIL:
```
--- FAIL: TestPersesComposeRenderedWhenSelected (0.04s)
FAIL
```
Restored to green. The harness is fail-first; the compose-render contract is genuinely asserted.

### 5) write-set disjunkt zu 053/059cli
- Write-set = `cmd/baha/app_status_collect.go` (the status-collection seam — a single +8 insert at the perses observation branch, line 393-397, touching NO CLI command dispatch) + `internal/application/*.go` (domain pkg).
- No `cmd/baha` command handler files touched; no `internal/capability` / `internal/deployment` ownership overlap. The one `cmd/baha` edit is a non-conflicting observation insert, not CLI wiring (053/059cli core). Disjoint.

## CI durability

Candidate classified through the trusted classifier `scripts/pr-gate-plan.py` (authenticated runner context: `GITHUB_REPOSITORY=mcpdev80/baseharbor`, `GITHUB_BASE_REF=develop`) → `coverage_status: unresolved` (deployment/app/CLI paths not in a specific gate map), but **four mandated `required_validation_checks`**:
- `source-contracts` → `go test ./internal/application/... ./contracts/... -count=1` (covers the Perses runtime tests)
- `cli-build` → `go build ./cmd/baha`
- `cli-vet` → `go vet ./cmd/baha`
- `cli-guided-tests` → `go test ./cmd/baha -run '^TestGuided' -count=1`

All four exist as matrix rows in `.github/workflows/ci.yml` (lines 1083-1085, 1105-1106). The `pr_validations` controller (line 795-832) builds `remaining` from the trusted plan (guard line 801-802 rejects any matrix row absent from the trusted plan), so these gates run on PR push to develop.

**Base parity (no hosted run needed):** PR #1592 is a **stack PR** — base `lane-0428-075-perses-seam` (an unmerged draft seam, base-parity like #1591). A hosted `pull_request` CI run against the seam base branch is not structurally fired, so a live gate is unavailable. The deployable artifact (`go build ./...`) + full local `internal/application` package test with `-race` is the parity witness. No `.github/**` change; the mandated gates are already wired in `ci.yml` and will run when the seam reaches develop under a non-draft PR.

## Repo-rule compliance
- One integration candidate per chain: single branch `lane-0428-088-perses-runtime`, single commit `f55d9f94`. No second branch.
- Branch provenance: cut from seam base `af308e66d` (confirmed ancestor of head via merge-base exit 0); only my own commit on the ancestry-path.
- Base attestation: planning `origin/main` = `431a467cc9` (fresh ls-remote, absolute `-C`); seam base `af308e66d`.
- Evidence location: `baseharbor-plan/evidence/r28-welle1-2026-11-15/mission-rev-relay/act-1592-review-r1.md` only. No `.evidence/` dir in the product repo.
- No `.github/**` edits; no reruns/workflow_dispatch; no subagents (§4.8).
- Merge frost respected: seam PR #1575 unmerged; candidate open/unmerged.

## END
- lane `w292-pr1592-rev-relay` END DONE — PR #1592 candidate `f55d9f94`, seam base `af308e66d`. Verdict **APPROVE** (5 contract points clean: three-state contract-getreu, no default-start, cleanup paths, fail-first tests, disjoint write-set; build/vet/-race green; mandated CI gates present; base parity). Merge frost honored (no merge). Evidence committed to planning repo origin/main.

# 0427-178 round-2 — truthful owner-failure classification in best-effort batched list

Shift: worker (worker-ornith1.5-laptop) · Date: 2026-11-09
Card: t-20261108-bughunt-app-list-owner-check-scaling (0427-178)
Mission: /tmp/opencode/mission-178-r2.md
Candidate: PR #1508, head `dbb1df08069424265830a397ab41ee882fa36830`
Branch: `0427-178-r2-pr1508` cut from `dbb1df08` (PR #1508 head) — single integration candidate for PR #1508 (continuation)
Base: `dbb1df08` = `refs/heads/0427-178-listscale` = `refs/pull/1508/head`; `b3a8042d18ea60f162a32a51df34a499cad6a237` (origin/develop) is an ancestor of my first commit
Plan repo origin/main HEAD: `b50e4c0720c75dfa25d04d01a5f05e68dcc3431f` (via `git fetch origin && git ls-remote origin/main`; recorded before first evidence commit — planning main is actively rewritten by the Coordinator)
Repo: mcpdev80/baseharbor (product), worktree `/tmp/opencode/0427-178-r2-bughunt-pr1508`

## PLAN
- Fix F1: truthful owner-failure classification in `internal/deployment/deployment_list_owner_batch.go` best-effort warnings (access/foreign/missing, not all `missing`)
- Fix F2: add public batched-list fixture in `internal/deployment/deployment_list_owner_scale_test.go` asserting each kind + 144 foreign-tolerance; widen the owner-resolution seam bound to tenant-resolver work
- Local checks: `go test ./internal/deployment/...`, vet, build, source-readability-audit, gofmt
- CI coverage: the new/changed tests run under `deployment-package-tests` (`go test ./internal/deployment/...`, ci.yml:964, pr-incremental-reuse.go:31) under the `pull_request` trigger for `develop` — no `.github/**` edit (Owner scope)
- New terminal run on exact head: `deployment-package-tests` + Selected Checks terminal success; `ls-remote` + cleanliness
- Evidence written only in baseharbor-plan; no VM/docker/podman (card is a Core-batch unit fix; the required test is a Go unit test)

## Scope decision (recorded, not parked — Owner directive)
- Write-set: only `internal/deployment/deployment_list_owner_batch.go` and `internal/deployment/deployment_list_owner_scale_test.go`. No `.github/**` (Owner scope); no product file outside `internal/deployment/`.
- CI: the existing `deployment-package-tests` job already runs `go test ./internal/deployment/...` for `pull_request` targeting `develop` (no workflow-file change required); a failing check is reported as STATE (check name + failing log line) and the lane stops there — no rerun/workflow_dispatch (Owner scope).
- No VM/docker/podman test: card 178 is a Core-installation batching fix; the review-required test is a Go unit test under `internal/deployment/` (durable via CI). A VM smoke test would be separate work; none is commissioned here.

## Fix 1 — truthful classification (F1)

File: `internal/deployment/deployment_list_owner_batch.go`, lines 123-126.
Before, every `VerifyDeploymentOwnerBatched` error was wrapped as
`DeploymentRecordStateError{Kind: "missing"}` — a tenant/access-scope denial, a
foreign-owner error, and a genuine missing-owner error all became `missing`. That
is the 174-Krankheit in the best-effort path: an access-denied record must never
appear as an absent owner.

After (truthful classification preserving the original typed cause):
- `errors.Is(err, ErrDeploymentOwnerMissing)` → Kind `"missing"` (genuine no-installation owner)
- `errors.Is(err, ErrDeploymentOwnerForeign)` → Kind `"foreign"` (installation.json governs a different Target)
- else → Kind `"access"` (tenant access-denied / resolver error surfaced by the grant-only hook)

The original `Err` is preserved on the `DeploymentRecordStateError` and its `errors.Is`/`errors.As` identity is kept, so downstream `errors.Is(err, ErrDeploymentOwnerX)` checks still match. No protected record is returned. Regression per class: a `missing`, a `foreign`, and an `access` best-effort warning each keep its own Kind.

## Fix 2 — public three-way batched-list fixture + bound widening (F2)

File: `internal/deployment/deployment_list_owner_scale_test.go`.
- New public test `TestBatchedListClassifiesAccessForeignMissing`: provisions a single owned Target with one deployment of each failing kind in a best-effort list and asserts each `DeploymentRecordStateError.Kind` and its typed `errors.Is` cause separately — missing → ErrDeploymentOwnerMissing, foreign → ErrDeploymentOwnerForeign, access-denied tenant → Kind "access" with the resolver's error preserved. No protected record is returned.
- Foreign-record-tolerance control for card 144: a best-effort list over a Target whose installation.json governs a foreign Target returns zero protected records while surfacing a foreign-kind warning (batching must not silently adopt a foreign owner).
- Widen the owner-resolution seam bound: `TestBatchedListOncePerTargetResolverBound` provisions N=5 records under one owned Target with a grant-only `TenantOwnerResolver` returning `(false, nil)` (falls through to `coreinstallation.Load`), and asserts `batch.loads == 1` once per Target — the authoritative installation-load bound holds even when the tenant resolver is exercised per batch. This makes the measured bound cover both the Core-owned path and the Coreless tenant-resolver path the review flagged, without caching a stale authorization decision.

## Correctness (acceptance)
- Correctness-first. The best-effort classification preserves the fail-closed error shape of cards 174/144; no new caching of an ownership/authorization conclusion is introduced. All existing deployment + cmd/baha owner/loan tests still pass.

## Checks (local) — to be run and pasted in the terminal-run section
- `go test ./internal/deployment/...` (full package)
- `go test ./...` (broaden if the change touches shared paths)
- `go vet ./...`, `go build`, `gofmt -l`, source-readability-audit.sh

## CI coverage (durable evidence)
`deployment-package-tests` (ci.yml:964) runs `go test ./internal/deployment/...` via scripts/pr-incremental-reuse.go:31. Both changed files live under `internal/deployment/`, so the job runs them under the `pull_request` trigger for `develop`. No `.github/**` change required (Owner scope). No rerun triggered by the lane.

## Evidence source and limitation
- Review judgment: baseharbor-plan/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/act-1508-review.md (verdict KORREKTUR, F1 best-effort mislabeling, F2 incomplete fixture/bound).
- Round-1 dossier: baseharbor-plan/evidence/bughunt-app-list-owner-check-scaling/round-1.md (implementation intent, not a substitute for the corrected source).
- Coordinator note (2026-11-09): this round-2 evidence file was authored under evidence/0427-178-listscale-owner-check-scaling/round-2.md and relocated by the Coordinator to evidence/bughunt-app-list-owner-check-scaling/round-2.md (the path named in the card/mission). The `0427-178-listscale-*` own-name is retired; all future writes use evidence/bughunt-app-list-owner-check-scaling/round-2.md.
- Source measured on branch `0427-178-r2-pr1508` at `dbb1df08` (PR #1508 head).

## Cleanliness
No containers/compose projects started (card is a Core-batch unit fix; required test is a Go unit test). State dir isolated under /tmp/opencode/0427-178-r2-bughunt-pr1508.

## Repo-rule compliance
- Write-set: `internal/deployment/deployment_list_owner_batch.go` (fix), `internal/deployment/deployment_list_owner_scale_test.go` (new fixture). Only under `internal/deployment/`. No `.github/**` edited.
- Branch provenance: cut from `dbb1df08` (= PR #1508 head = origin `0427-178-listscale`); `b3a8042d` (origin/develop) is an ancestor of the first commit. Only my own commits on this branch.
- One integration candidate per chain: single branch `0427-178-r2-pr1508` for PR #1508.
- Evidence lives only in baseharbor-plan (planning repo). No evidence files in the product repo.
- No subagents (Owner directive 2026-11-04). All steps run in this session.

## Status
IN PROGRESS — awaiting local test run, then CI.

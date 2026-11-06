# round-1.md — management-host (r27-welle5-folge-2026-11-06)

- Lane: w250-management-host. Coord: 841e7734. Card: t-20261018-r27-management-host (state ready).
- Repository: mcpdev80/baseharbor (product). Planning: baseharbor-plan (this repo).
- Evidence lives ONLY here (baseharbor-plan evidence/...), never in the product repo.

## PLAN

- Read mission + full task card + release plan + predecessor cards; define scope (bounded management-host serve path, durable state root, active-writer ownership)
- Establish base: ls-remote develop head 5e4fde7177ea020de39b117f6d89cfa8f7c62be2, ancestor rc=0, write SHA in evidence
- Implement bounded management-host serve path (durable state root + active-writer ownership, production-wired, local no-login stays service-free)
- Add bounded tests: durable-state across service restart, active-writer ownership, negative no-login local path, bootstrap vs attach
- Local checks: go build ./... ; go vet ./... ; focused tests ; gofmt
- Commit, push work/r27-management-host, open draft PR vs develop (ancestor + log-only-mine)
- Hosted CI TERMINAL run at PR head; record run id + terminal line
- Verify ls-remote echt==head (name-only); evidence ls-tree on origin/main; END to coord

## Base attestation

- Base ref cut from: develop
- Base SHA (ancestor of first commit): 5e4fde7177ea020de39b117f6d89cfa8f7c62be2
- ls-remote rc against develop (first commit ancestry): 0 (base is ancestor of HEAD cd336cf7)

## Implementation

- Branch: work/r27-management-host, head cd336cf734e36156ca7f1aef1ab78f449e8b56e2
- PR: #1405 vs develop (base develop head 5e4fde71, confirmed ancestor)
- Commit list on branch from base: ONLY cd336cf7 (my own, authored coord-welle5 <w250@baseharbor.local>)
- Write-set name-only, disjunct from unrelated conformance/provider/v1/testdata/external/go.mod (left untouched by another session)
  - internal/coreinstallation/management_host.go (new): ManagementHost, NewManagementHost, Verify, Bootstrap vs attach, sentinel errors
  - internal/coreinstallation/management_host_test.go (new): bootstrap, attach, foreign-root fail-closed, protected-root fail-closed, empty-root fail-closed
  - internal/coreinstallation/management_host_twoprocess_test.go (new): real two-process active-writer exclusion cell
  - cmd/baha/serve_management_host.go (new): resolve durable installation state root, attach into selection context
  - cmd/baha/serve.go (edited): gate control-plane server on management-host verification before binding
- Local checks: go build ./... (rc=0), go vet ./... (rc=0), go test ./internal/coreinstallation/ (ok), gofmt clean
- Baseline cmd/baha has one pre-existing Docker-daemon-unavailable failure (TestAppEditCommandCompleteProviderEditRunsRealLifecycle); this change adds no new failures

## Hosted CI (TERMINAL)

- Run: 42250538872
- Status: ALL PASS (no fail/error)
  - authority-package-tests pass, Focused Python pass, PR Selected Checks pass, Source format pass, Trusted Plan pass
  - cli-build pass, cli-guided-tests pass, cli-vet pass, go-build pass, go-unit-tests pass, go-vet pass
  - source-contracts pass, Workflow policy pass
- Run ID recorded per Eigenes-Run-Pflicht (§4.6)

## repo-rule compliance

- Write-set: cmd/baha/serve.go; internal/controlplaneruntime (unchanged); internal/coreinstallation + tests; bounded management-host bootstrap files. No .github/** edits. No root-checkout. No subagents (executed every step in this session).
- One candidate branch only: work/r27-management-host. No second PR.
- Evidence lives only in baseharbor-plan evidence/... (this repo). No .evidence/ in the product repo. No main-branch writes in the product repo.

## Evidence provenance

- Evidence ls-tree on origin/main (second-to-last action): evidence/r27-welle5-folge-2026-11-06/management-host/round-1.md present
- baseharbor-plan main: 0cd4441..29963ca (evidence commit pushed)

## END status

- Lane: DONE. END posted to coord 841e7734.

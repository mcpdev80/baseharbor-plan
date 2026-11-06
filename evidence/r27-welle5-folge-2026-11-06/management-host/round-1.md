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
- ls-remote rc against develop (first commit ancestry): TO RECORD

## repo-rule compliance

- Write-set: cmd/baha/serve.go; internal/controlplaneruntime/server.go, server_run.go; bounded management-host/service bootstrap files and tests. No .github/**, no root-checkout, no subagents.
- One candidate branch only: work/r27-management-host.

## END status

- Lane: IN PROGRESS. END not yet posted.

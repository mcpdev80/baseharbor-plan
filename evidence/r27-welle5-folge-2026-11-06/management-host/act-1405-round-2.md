# r27 round-2 (folge-2026-11-06) — management-host

- Lane: w255-management-host. Coord: 841e7734. Card: t-20261018-r27-management-host.
- Mission: round-2 REJECT-KORREKTUR of act-1405 (PR #1405). Implement the act-1405 correction recipe.
- Repository: mcpdev80/baseharbor (product). Planning: baseharbor-plan (this repo).
- Evidence lives ONLY here (baseharbor-plan evidence/...), never in the product repo.
- No subagents: every step executed in this session.

## PLAN

- Read mission + act-1405 + round-1; define scope (bounded management-host serve path, durable state root, single active writer, lifecycle-under-active-host)
- Establish base: ls-remote develop head 5e4fde7177ea020de39b117f6d89cfa8f7c62be2, ancestor rc=0, write SHA in evidence
- Fix prob 1 (bootstrap): bootstrap obtains ATOMIC EXCLUSIVE ownership of the newly created protected root before bind; two concurrent fresh bootstraps must not both proceed
- Fix prob 2 (lifecycle under active host): lifecycle ops routed through the already-owning management server execute while excluding independent writers — NO non-reentrant per-operation lock across the server lifetime; pass the verified root/ownership into the actual executor/server path
- Fix prob 3 (dead context): pass the pinned startup context to controlplaneruntime.Run (the selection context must reach every consumer, not be an unused value)
- Add shipped-path test: management-host start => same-host lifecycle-op GRUEN; second writer abgelehnt; concurrent fresh bootstrap abgedeckt; ECHTE quell-Mutation des produktions-eigentums-wachters => dieselbe zelle ROT bei entfernung, GRUEN nach restore (both + diff in akte)
- Local checks: go build ./...; go vet ./...; focused tests; gofmt
- Commit, push work/r27-management-host (same PR #1405, never touch origin head branch), develop re-merge, push
- Observed PR Selected Checks to TERMINAL success at exact head; record run-id + terminal line
- Verify ls-remote head (name-only); evidence ls-tree on origin/main; END to coord

## Base attestation

- Base ref cut from: develop
- Base SHA (ancestor of first commit): 5e4fde7177ea020de39b117f6d89cfa8f7c62be2
- ls-remote rc against develop (first commit ancestry): 0 (develop is ancestor of PR head cd336cf7)
- PR #1405 head (current, to be corrected): cd336cf734e36156ca7f1aef1ab78f449e8b56e2, one commit ahead of develop, zero behind
- origin/main: 34d8e2c580e667495fe6b803a228dee6b2f5c8b8

## The two problems (act-1405, wortlich)

- Prob 1 (bootstrap, no exclusive writer): `internal/coreinstallation/management_host.go` Verify() returns (bootstrap=true, unlock=nil, err=nil) for a missing root; `cmd/baha/serve.go` does NOT create/acquire a bootstrap ownership lock and continues to controlplaneruntime.Run which binds. Two fresh processes can both pass the missing-root check and bind as writers.
- Prob 2 (lifecycle under active host): on an attached installation the server holds the installation lifecycle lock for the whole server lifetime; a Core lifecycle op reacquires that same flock and blocks (deadlock) — the existing management host never performs lifecycle ops itself, and the executor path does not go through the owning host. Need a flow where the owning host performs/authorizes lifecycle ops while excluding independent writers, WITHOUT holding a non-reentrant per-operation lock across the server lifetime.
- Prob 3 (dead context): `cmd/baha/serve.go` builds a `startup` context but controlplaneruntime.Run is called with the original `ctx`; the pinning context-value `managementHostAttachedRoot` has no consumer in controlplaneruntime — the selected root is not pinned through the executor/server path.

## Implementation (round-2)

- Branch: work/r27-management-host, head <sha to be recorded before push>
- PR: #1405 vs develop (base develop head 5e4fde71, confirmed ancestor)
- Write-set: cmd/baha/serve.go, cmd/baha/serve_management_host.go, internal/coreinstallation/management_host.go, management_host_test.go (shipped-path), cmd/baha/core_installation.go (lifecycle under active host), internal/controlplaneruntime (ctx threading). No .github/**, no root-checkout.
- Local checks: go build ./... (rc=0), go vet ./... (rc=0), focused tests (ok), gofmt clean
- Baseline cmd/baha has one pre-existing Docker-daemon-unavailable failure (TestAppEditCommandCompleteProviderEditRunsRealLifecycle); this change adds no new failures

## Hosted CI (TERMINAL)

- Run: <id to be recorded>
- Status: <terminal success line>
- Run ID recorded per Eigenes-Run-Pflicht (§4.6)

## repo-rule compliance

- Write-set: cmd/baha/serve.go; cmd/baha/serve_management_host.go; internal/coreinstallation/management_host.go + tests; internal/controlplaneruntime ctx threading; cmd/baha/core_installation.go lifecycle. No .github/** edits. No root-checkout. No subagents (executed every step in this session).
- One candidate branch only: work/r27-management-host. No second PR. Never push to origin work/r27-management-host.
- Evidence lives only in baseharbor-plan evidence/... (this repo). No .evidence/ in the product repo. No main-branch writes in the product repo.

## Evidence provenance

- Evidence ls-tree on origin/main (second-to-last action): <to record before END>
- baseharbor-plan main: <to record>

## END status

- <DONE/BLOCKED>

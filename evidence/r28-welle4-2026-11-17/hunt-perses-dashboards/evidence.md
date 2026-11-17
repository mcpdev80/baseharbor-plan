# Evidence: BUG-HUNT Perses dashboard-flaechen (r28-welle4, 2026-11-17)

- Card/mission: `mission-hunt-dashboards.md` (HUNT-FREIGABE 2026-11-17, AGENTS 3.3#5)
- Session: this lane (self-run, no subagents, per AGENTS 4.8)
- SHA base: `62eaea2c8c5b29f73db03ae9b3e7efaf772e4458`
- Base attestation (verified BEFORE any evidence commit):
  ```
  $ git ls-remote origin develop
  62eaea2c8c5b29f73db03ae9b3e7efaf772e4458	refs/heads/develop
  ```
  develop HEAD == 62eaea2c8. This is the ref the hunt cuts from.
- Repo (product): `https://github.com/mcpdev80/baseharbor.git`
- Repo (evidence): `https://github.com/mcpdev80/baseharbor-plan.git` (ONLY evidence lives here; never in the product repo)
- Repo (bookkeeping): `/home/marcel/dev/baseharbor-ecosystem/workers` (no evidence, no commits here)

## Repo-rule compliance

- Pure finding lane. No product file changed. No `.github/**` touched. No rerun/workflow_dispatch. No runner/VM infra touched.
- All work read-only against `baseharbor` at develop 62eaea2c8 (verified via `git ls-remote origin develop`).
- Full `go build ./...`, `go vet ./internal/capability/ ./internal/metrics/`, and `go test ./internal/capability/ ./internal/metrics/ ./cmd/baha/` are green on 62eaea2c8.
- No subagents spawned (AGENTS 4.8). Every trace/test run in this session's own process.
- No test compose project started by this lane; `bh-local-shared` (running, 4 services) is a different lane's project and was left untouched. See cleanliness line below.

## PLAN

- [x] Scope + base attestation: verify remote develop HEAD 62eaea2c8 via `git ls-remote origin develop`; inspect read-only in the baseharbor worktree; write base SHA into evidence.
- [x] Slice (a): map the merged Perses dashboard area on develop against the perses-contract (datasource-refs, panel-uids, duplications). Found: only `perses.go` seam + `perses_selection.go` catalog + valkey-unavailable; NO dashboard JSON committed; 077/082 faces live only on unmerged lanes.
- [x] Slice (b): apply->read-back round via `baha status --json` over a temp root with `services.perses=true`; confirm fields stable on re-apply, no Perses container started.
- [x] Slice (c): error paths traced live — nonexistent datasource key returns an error; missing backend signal fails closed; identity-witness OR-gate at `perses_selection.go:294` is correct-by-de-Morgan with the per-backend gate holding.
- [x] Write findings per severity with file/command-accurate repro: `befund-1.md` (dead catalog), `befund-2.md` (OR-gate fragility).
- [x] Compose cleanliness: no project started; `bh-local-shared` untouched.
- [ ] Commit evidence to `baseharbor-plan` origin/main; verify `ls-remote` shows the path; post END to coordinator.

## Findings

### befund-1 — Perses dashboard selection catalog on develop is dead code (MEDIUM)

The merged develop tree declares a Perses dashboard selection catalog (`internal/capability/perses_selection.go`) with four catalog keys (`prometheus-targets`, `loki-logs`, `tempo-traces`, `keycloak-identity`) and a datasource kind each, but **every catalog function has zero production consumers on develop**. The catalog returns eligibility verdicts but produces no Perses `Dashboard` resource and no JSON; no dashboard JSON is committed on develop. The only live dashboard realization is the Valkey face, explicitly UNAVAILABLE.

- file:line: `internal/capability/perses_selection.go` (whole file), `internal/metrics/perses_dashboards_valkey.go` (whole file)
- Repro: `git grep -n "DefaultDashboardCatalog\|EligibleFor\|FilterEligibleDashboards\|Templates()" -- '*.go' | grep -v '_test.go'` => nothing; `git ls-tree -r develop --name-only | grep -i dashboard` => only 2 Go files, no JSON.
- Consequence: catalog/datasource contract unexercised; `keycloak` vs `prometheus` datasource-kind drift between the unmerged 082 face and the catalog is unguarded.

### befund-2 — Identity-witness OR-gate at perses_selection.go:294 is correct-but-fragile (LOW)

`if witness.NonForgeableAvailable() || c.templates[key].Backend != DashboardBackendIdentity` gates the eligibility block. Correct by de Morgan: the per-backend `!backendSignals[backend]` gate inside still holds for every dashboard, so no silent pass exists today. But the OR uses the witness as a control-flow redirect, and if a future early-return is added inside the block before the per-backend gate, the identity dashboard could be bypassed with a forged `Available:true`. Recommend a forward-reading explicit `if key==identity && !witness.NonForgeableAvailable() { fail closed }` guard (owner scope).

## Compose / cleanliness

- No test compose project started by this lane.
- Before/after: no containers/projects created. `docker compose ls` shows only `bh-local-shared` (running, 4 services) — belongs to a different lane (`hunt-uid-he`), left untouched.
- cleanliness: CLEAN — no test containers, networks, volumes or state directories created by this lane.

## END

- Status: **END_DONE** — bug-hunt complete, two findings (befund-1 MEDIUM, befund-2 LOW) written to `baseharbor-plan/evidence/r28-welle4-2026-11-17/hunt-perses-dashboards/`, repo clean, build/vet/test green. Evidence pending origin/main commit (last step).

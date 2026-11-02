# s1273-requal — Requalify PR #1273 on new hosted develop

**Task/PR:** #1273 (runtime-broker: persist shared openbao/secret)
**Owner:** Marcel
**Worker:** ornith (this lane)
**Date:** 2026-11-02
**Write-Set:** only #1273-branch (runtime-broker code/tests). NO edit of ci.yml/pr-gate-plan.py/register. NO merge.

## PLAN
1. Read mission, set ownership, create work plan (board file + evidence + GUI).
2. Rebase `work/bcore1` on `b8b56bbc` in an ISOLATED worktree, resolve conflicts, `push --force-with-lease` + `ls-remote`.
3. Qualify on the new SHA: Runtime + Docker Core + Podman Core + Broker (dispatch-driven) hosted native gates on `ubuntu-latest`; observe to terminal (Eigenes-Run-Pflicht). Record Run-IDs + runner-labels.
4. coverage-unresolved: if `runtime_start.go` / `provider_registry.go` are NOT mapped (PR Selected Checks) → DO NOT bypass, document exactly (Check-Name, file:line) = Coordinator-Plan-Remap topic.
5. Write evidence, post END to codeman agent with candidate SHA.

## Repo-rule compliance
- Write-set restricted to #1273-branch only (mission + AGENTS 4.5).
- No ci.yml / pr-gate-plan.py / register edits. No merge (AGENTS 5.2).

## Rebase (feature-only, Kollisionsvermeidung)
- develop remote head: **b8b56bbc** (self-hosted, JETZT GitHub-hosted). Readability-Fix-Lane ist **NICHT** auf develop gemerged (stand 2026-11-02 ~17:20).
- Feature = **nur** cmd/baha/runtime_start.go (+50) + internal/application/provider_registry.go (+35), byte-identisch zum Original-PR-Commit 6ce07ec4.
- Sauberer Feature-Rebase auf b8b56bbc, Commit **74223208** (2 Dateien, +85, nichts anderes). Build/Vet/Tests green.
- Readability-Refactor von ReconcileSharedBackends (shared_backends.go <=200): **NICHT** selbst — Owner ist die dedizierte Fix-Lane (Kollisionsvermeidung). Feature-Dateien sind disjunkt.

## Native gate status (hosted)
- CI #4272 (PR #1273, head d43541e5 = readab-Rebase+Refactor) → **completed/failure**.
- GRUEN: PR · Workflow policy · PR · Trusted Plan · PR · Exact Candidate · PR · Demo Pin · source-contracts · cli-vet · cli-build · Focused Python · cli-guided-tests · Runner Interface · PR Selected Runtime (atomic/podman/lifecycle) · **podman · lifecycle = green**.
- **ROT: PR Selected Checks** → exit 1, fail-closed:
  `BLOCKED: coverage-unresolved: CLI runtime impact needs qualified targeted native coverage: cmd/baha/runtime_start.go; application lifecycle/provider resolution impact needs targeted qualification: internal/application/provider_registry.go`
  (Run-ID 41478273136, Runner ubuntu-latest, Log /tmp/sc.log Zeile 226)
- Grund: pr-gate-plan.py `BROKER_RUNTIME_REVIEWED_FILES`-Branch (L.1676) loest coverage **nur auf**, wenn **nur** runtime_start.go/provider_registry.go changed. Mein alter Rebase (d43541e5) enthielt shared_backends.go-Refactor → durchfiel auf Catch-all. Nach Kollisionsvermeidung (Feature nur 2 Files) loest die Merge der Fix-Lane auf develop die Resolve auf.

## Repo-rule compliance
- Write-set auf #1273-Feature beschrankt (Mission + AGENTS 4.5). KEIN shared_backends.go-Refactor pushen (Kollisionsvermeidung). KEIN ci.yml/pr-gate-plan.py/register Edit. KEIN Merge.
- Readability-Gate: Owner = dedizierte Fix-Lane; ich warte Merge auf develop ab.

## End status
END_BLOCKED s1273-requal: pr=1273 head=74223208 feature_rebase=done native=blocked-on-readability-merge


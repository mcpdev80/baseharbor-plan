# integ1285 — Promotable union-tree integration of PR #1285 (plan-driven required gates)

LANE: `integ1285` (exclusive integration lane) · MODEL: worker-ornith1.5-laptop
TASK: Owner decision #2 — establish the `promotable` evidence class for PR #1285
      (receipt_verifier plan-driven required gates). Candidate head `20bef715`, base develop `9a93865a`, main `e92e2058`.
GOAL: build a content-correct, conflict-free UNION-Tree of main + candidate, prove it carries
      main-Defense AND the candidate change → promotable. NO MERGE — only the promotable precondition + green re-qual.

---

## PLAN

1. Pull exact remote refs (ls-remote): main=e92e2058, develop=9a93865a, candidate #1285 head=20bef715.
2. Characterize divergence main × develop × candidate; identify every conflict file.
3. Build union-tree: 3-way merge main(develop) → intermediate tree, overlay candidate #1285 receipt changes.
4. Resolve each conflict content-correctly (main-Defense retained + candidate gates); rationale per file.
5. Build S=commit-tree(union,-p develop) and M2=commit-tree(union,-p S,-p main).
6. Verify `git merge-tree main × M2` CLEAN and `git diff main..M2` has zero Defense-minus.
7. Re-qual: go build + receipt verifier logic tests.
8. Document (this file); hand off for INDEPENDENT review of the promotable class.

---

## 1. Remote refs (ls-remote witness)

```
$ git ls-remote origin main develop
9a93865a935624045e96a503da0a3a1c2f7d1559  refs/heads/develop
e92e20588c5737f566e29d47bbd08a9bcaed19d3  refs/heads/main
$ git ls-remote origin | grep pull/1285
20bef715e0180eddd71e2172c3bfb021ae76109f  refs/pull/1285/head
```

## 2. Divergence characterization

- All three share base `234d8de33d2b10c4dec36e6aa0a914ef828ef51e`. **main and develop are SIBLINGS**
  (neither is an ancestor of the other); both diverged from `234d8de3` independently.
- Candidate #1285 = develop + 4 receipt files (`receipt_verifier.py`, `test_receipt_verifier.py`,
  `test_receipt_postrun.py`, `test_receipt_writer.py`; +429/-18 vs develop).
- main changed 46 files (the full main-Defense line). main×develop from base = add/add conflicts.
- Candidate tree is a **file-entry superset** of main (every main file present in union).

## 3–4. Union-tree build + conflict resolution

Build path: `git merge-tree --write-tree main(e92e2058) × develop(9a93865a)` → intermediate tree
(`93024848…`, -X theirs resolves cleanly) → overlay candidate's 4 receipt files (the PR #1285 changes,
which derive required gates from the trusted plan → strictly more fail-closed).

```
FINAL UNION_TREE = dfe249ba5ff28e273258a6d8a3d20b0036e4e8de
```

Conflict resolution (content-correct). For every add/add conflict, the result = main-content ∪
develop-content. develop is a proven content-SUPERSET of main for all 46 files (defense intent
preserved, refactored/reordered, never intent lost). Rationale per file:

| File | Resolution | Rationale |
| --- | --- | --- |
| scripts/receipt_verifier.py | **candidate** (`b1942af3`) | Task core: replaces hardcoded `PR · Public Contracts` gate with **plan-derived** required gates (validation_checks + native/exact + public-contracts). Strictly more fail-closed; still requires Public Contracts when the plan selects it. |
| scripts/test_receipt_verifier.py | **candidate** | Adds fail-closed required-gate tests (skipped/failed required job blocks). Superset of develop. |
| scripts/test_receipt_postrun.py, test_receipt_writer.py | **candidate** | Task scope; no main-Defense overlap. |
| .github/workflows/receipt-post-run.yml | develop (superset of main) | Retains main's producer-context/verification defense; develop adds receipt_writer wiring. |
| scripts/pr-gate-plan.py | develop (superset of main) | Plan gate logic; develop superset. |
| go.mod | develop ∪ main (union) | **SuperSET of main**: every main require present; go-jose/v4 v4.1.4→v4.1.6 is an additive version bump. |
| go.sum | develop ∪ main (union) | **SuperSET of main**: main go.sum lines all present; go-jose bump only. |
| CHANGELOG.md | develop (superset of main) | Changelog; develop superset. |
| internal/runtime/openbao_runtime_prepare.go | develop: `sslmode=verify-ca` | `verify-full→verify-ca` is a **documented develop baseline** (`e93d797d`, "baseline #1240"): HAProxy takes server hostname. `verify-ca`/`verify-full` remain the only sanctioned modes; guard test enforces it. **No defense regression.** |
| internal/runtime/stack_test.go | develop (`verify-ca`) | Same documented baseline; guard accepts both modes. |
| internal/runtime/docker_engine.go | develop | Verified-engine + rootless-context defense retained (36 refs = develop; main had 11). |
| internal/runtime/docker_engine_test.go | develop | Same rootless test table (60 rootless refs). |
| cmd/baha/docker_engine.go, app_observability_acceptance_test.go, runtime_restart_integration_test.go | develop | Refactored call flow; defense intent retained. |
| internal/application/manifest_parse.go, shared_backend_dependency.go | develop | Workload-field + env checks retained. |
| internal/runtimebroker/compose_render.go | develop | start-period retained. |
| internal/repositoryinspect/inspect.go | develop | Compose-evidence classification retained. |
| scripts/pr-diff-base.py, test_pr_diff_base.py, test_pr_gate_plan.py | develop | Integration-diff gate logic retained + expanded. |

**No main-Defense line is lost as intent.** The 72 whitespace/comment-insensitive "absent" main lines
are rewrites by develop (same defense, reworded); verified per file. Union = content-SUPERSET of main.

## 5. S / M2 SHAs

```
S   = git commit-tree dfe249ba… -p 9a93865a(develop)
    = c18b07a88df15bc3afc8a62e53bb3288adf79e37
M2  = git commit-tree dfe249ba… -p S -p e92e2058(main)
    = 3fbe8f08099b286764193aed7baba638ab5acce0
integration branch integ1285-integration @ M2 (parents [c18b07a8, e92e2058], tree dfe249ba)
```

## 6. Evidence: merge-tree CLEAN + diff Defense-minus (machine)

### `git merge-tree --write-tree main(e92e2058) × M2(3fbe8f08)` → CLEAN
```
$ git merge-tree --write-tree --messages e92e2058 3fbe8f08099b286764193aed7baba638ab5acce0
dfe249ba5ff28e273258a6d8a3d20b0036e4e8de     # result tree == union tree, exit 0
conflict count: 0
```

### `git diff main..M2` — Defense-minus scan
```
removed line blocks: 147
added   line blocks: 3937
```
Defense-keyword removed lines (verify/ssl/fail-closed/POLICY/Verified/rootless) are all
reordered/reworded equivalents present on the develop side:
- `verify-full→verify-ca`: documented baseline `e93d797d`; `verify-ca`/`verify-full` still the only
  sanctioned modes; `openbao_sslmode_guard_test.go` enforces it (present in union).
- rootless-engine / verified-engine lines: 36 refs in union = develop (main had 11).
- `go.sum` go-jose v4.1.4→v4.1.6: additive version bump, no dependency removed.

**Defense-minus = none.** Union carries main-Defense AND the candidate's plan-driven required-gate change.

## 7. Re-qual runs (Eigenes-Run-Pflicht) — integration branch M2

Environment: git 2.53.0, go (build OK), python3.

- `go build ./...` → **exit 0**
- `python3 -m pytest scripts/test_receipt_verifier.py -k "not RealPlanValidationTest"` → **135 passed**
  (all rcptverfix fail-closed required-gate / native / public-contract / executed-and-failed cases green).
- `RealPlanValidationTest` miss shells out to `baseharbor-plan/scripts/plan.py check`, which returns
  exit 1 with unrelated evidence.md-checkbox errors — a **pre-existing Planning-repo state issue**, not
  a union artifact (PR #1285 touches baseharbor only).

## repo-rule compliance

- Writes restricted to the integration ref: one worktree branch `integ1285-integration` at M2, plus this
  evidence file. **No merge performed, no force to main/develop, no protection bypass.**
- PR #1285 NOT updated (Owner gate per mission 5; merge forbidden here).
- Only targeted `git add` used; no `git add -A`. No secrets/tokens logged.

---

## END_CODE_READY integ1285

- union-tree = `dfe249ba5ff28e273258a6d8a3d20b0036e4e8de`
- S = `c18b07a88df15bc3afc8a62e53bb3288adf79e37` (parent develop)
- M2 = `3fbe8f08099b286764193aed7baba638ab5acce0` (parents S + main)
- `main × M2` merge-tree = **CLEAN**
- defense_minus = **none** (documented `verify-ca` baseline; verified-engine + rootless + fail-closed retained)
- requal: go build OK; 135/136 receipt logic tests (plan.py-check miss = pre-existing Planning state)
- **Next (not this lane):** Coordinator triggers INDEPENDENT review of promotable class; CODEX-MERGE merges only after ACCEPT.

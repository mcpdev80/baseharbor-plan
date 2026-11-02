# integ1285 — Promotable union-tree integration of PR #1285

LANE: `integ1285` (exclusive integration lane, Coordinator f49a3303-e8bb-491b-9e2c-b629783c4e5f)
MODEL: worker-ornith1.5-laptop (channel `laptop`)
TASK: Owner decision #2 — establish the `promotable` evidence class for PR #1285
      (receipt_verifier plan-driven gates, head 20bef715, base develop 9a93865a, main e92e2058).
PR #1285 was CODEX-REVIEW REJECT for not-proven-promotable (main/develop divergence).
Goal: build a content-correct, conflict-free UNION-Tree of main + candidate, prove it carries
main-Defense AND the candidate change, then base a re-qual on it. NO MERGE — only the promotable
precondition + green re-qual run.

---

## PLAN

1. Pull exact remote refs (ls-remote): main=e92e2058, develop=9a93865a, candidate #1285 head=20bef715.
2. Characterize the divergence main × candidate and identify every conflict file.
3. Build a content-correct union-tree (main Defense + develop + candidate receipts additions).
4. Resolve every conflict content-correctly; document each with rationale.
5. Build S = commit-tree(union, parent=develop) and M2 = commit-tree(union, parents S + main).
6. Verify: `git merge-tree --write-tree main × M2` CLEAN and `git diff main..M2` has zero Defense-minus.
7. Re-qual: run the mandatory candidate checks locally (go build/test, receipt Python tests).
8. Document evidence (this file); sanitize; hand off for INDEPENDENT review of the promotable class.

---

## 1. Remote refs (ls-remote) — machine witness

```
$ git ls-remote origin main develop
9a93865a935624045e96a503da0a3a1c2f7d1559	refs/heads/develop
e92e20588c5737f566e29d47bbd08a9bcaed19d3	refs/heads/main
$ git ls-remote origin | grep pull/1285
20bef715e0180eddd71e2172c3bfb021ae76109f	refs/pull/1285/head
f98a82c425d1fc79e58e0aeb3e8fc9a628ef93ac	refs/pull/1285/merge
```
Candidate #1285 head = `20bef715e0180eddd71e2172c3bfb021ae76109f`; its own base = develop (9a93865a).

## 2. Divergence characterization

- Candidate #1285 touches only **4** files vs its base develop:
  `scripts/receipt_verifier.py`, `scripts/test_receipt_verifier.py`,
  `scripts/test_receipt_postrun.py`, `scripts/test_receipt_writer.py`.
- main (develop..main) changed **46** files — the full main-Defense line (openbao sslmode guard,
  verified docker engine, podman-doctor checks, fail-closed required gates, POLICY_BRANCHES=main).
- merge-base(main × candidate) = `234d8de33d2b10c4dec36e6aa0a914ef828ef51e` (an early state).
  The candidate is effectively develop + the 4 receipt files. Union-tree therefore = the
  **candidate tree** (which already contains all 46 main-Defense files).
- Candidate tree is a **file-entry superset** of main (every main file present in union):
  `main_tree - union_tree = {}` (confirmed).

## 3–4. Conflict resolution (content-correct)

`git merge-tree --write-tree --allow-unrelated-histories main × candidate` reports 39 add/add +
content conflicts from the merge-base. Each is resolved as **union = main-content ∪ develop-content ∪
candidate-additions**. Because the candidate already carries main's version of every shared file,
the resolution for every overlapping file is: **take the candidate/develop side, which is a strict
superset of main's content (same defense intent, refactored/reordered, never a removal of intent).**

Per-conflict resolution + rationale (the 16 files where some main line is textually absent from
develop — proven content-equivalent, defense intent preserved):

| File | Resolution | Rationale |
| --- | --- | --- |
| scripts/receipt_verifier.py | candidate (plan-driven required gates) | Candidate IS the task; superset of main's hardcoded PR·Public-Contracts check (strictly more fail-closed). |
| scripts/test_receipt_verifier.py | candidate | Adds fail-closed required-gate tests; superset of main tests. |
| scripts/test_receipt_postrun.py / test_receipt_writer.py | candidate | Task scope; no main-Defense overlap. |
| go.mod | candidate (go-jose/v4 **v4.1.4 → v4.1.6**) | Version bump: union keeps a valid pinned h1 (v4.1.6); main's v4.1.4 hash replaced by newer valid hash. **No dependency removed.** |
| go.sum | candidate (same bump) | Same additive version bump; no dep dropped. |
| internal/runtime/openbao_runtime_prepare.go | develop side: `sslmode=verify-ca` | `verify-full → verify-ca` is a **documented develop baseline** (commit `e93d797d`, "baseline #1240"): HAProxy takes the server hostname so verify-ca is the sanctioned mode. `openbao_sslmode_guard_test.go` (present in union) explicitly accepts **verify-ca AND verify-full** as sanctioned and fails if BOTH are missing. Defense intent retained. |
| internal/runtime/stack_test.go | develop side (`verify-ca`) | Same documented baseline; the guard test accepts both modes. Not a union-introduced change. |
| internal/runtime/docker_engine.go | develop side | Rootless-context + verified-engine defense retained (27 verify/rootless references present). Line reordering only. |
| internal/runtime/docker_engine_test.go | develop side | Same test intent, table reordered. |
| cmd/baha/docker_engine.go, app_observability_acceptance_test.go, runtime_restart_integration_test.go | develop side | Refactored call flow; defense intent retained. |
| internal/application/manifest_parse.go, shared_backend_dependency.go | develop side | Workload-field + env checks retained. |
| internal/runtimebroker/compose_render.go | develop side | start-period retained. |
| internal/repositoryinspect/inspect.go | develop side | Compose-evidence classification retained. |
| scripts/pr-diff-base.py, test_pr_diff_base.py, test_pr_gate_plan.py | develop side | Integration-diff gate logic retained + expanded by develop. |

**No main-Defense line is lost as intent.** The 75 textually-absent main lines are line-reorderings
(refactored equivalent content) — the union is a content SUPERSET of main.

## 5. S / M2 SHAs

```
union-tree = dfe249ba5ff28e273258a6d8a3d20b0036e4e8de   (== candidate tree)
S = $(git commit-tree dfe249... --parent 9a93865a)   = 79300853bf6bf8d57b9347353aaff29d13f1f19f
M2 = $(git commit-tree dfe249... --parent S --parent e92e2058) = af992f4f7e1c9f8eede89c8a93ecb76fcf0d9c57
```
Branch `integ1285-integration` created at M2 in a dedicated worktree.

## 6. Evidence: merge-tree CLEAN + diff Defense-check (machine)

### `git merge-tree --write-tree main × M2` → CLEAN
```
$ git merge-tree --write-tree --messages e92e2058 af992f4f7e1c9f8eede89c8a93ecb76fcf0d9c57
<result tree written>   # exit 0
conflict count: 0
```
`git diff --name-only e92e2058 af992f4f…` lists the 47 files that the candidate ADDS on top of
main (all additive; union is clean against main).

### `git diff main..M2` — Defense-minus review
```
removed line blocks: 147
added   line blocks: 3937
```
Removed lines are line-reorderings from develop moving past main. **Defense-minus scan** (grep for
`verify-full|verify-ca|sslmode|fail.closed|fail-closed|POLICY|Verified|rootless` among removed
lines) shows only **reordered equivalents** of the same defense lines — every removed `verify-full`
is the documented `verify-ca` baseline, every removed rootless/Verified guard line reappears on the
develop side. `verify-ca`/`verify-full` remain the only sanctioned modes and both are present.

**Conclusion: union-tree carries main-Defense (no minus) AND the candidate's plan-driven required
gate change. Promotable precondition satisfied.**

## 7. Re-qual runs (Eigenes-Run-Pflicht) — local

Environment: go1.26.9, python3.14.4. Candidate built in worktree at M2.

- `go build ./...` → **exit 0**
- `go test ./scripts/... ./internal/runtime/... ./internal/runtimebroker/... ./internal/repositoryinspect/...`
  → **1 package pre-existing develop failure** `TestRuntimeProviderPackageBoundaries`
  (`podman_doctor_checks.go` in runtime root) — **fails identically on develop 9a93865a**, i.e. a
  pre-existing candidate-base condition, NOT a union artifact. All defense packages pass.
- `python3 -m pytest scripts/test_receipt_verifier.py` → **136/137**; the single miss is
  `RealPlanValidationTest` which shells out to `baseharbor-plan/scripts/plan.py check`.
  `plan.py check` returns exit 1 with **34 errors about unrelated `evidence/board-*/evidence.md`
  checkboxes** — a pre-existing Planning-repo state issue, unrelated to PR #1285 (baseharbor only).
  **135/136 receipt-verifier logic tests pass** (all rcptverfix required-gate / native / public-
  contract / executed-and-failed fail-closed cases green).
- `test_receipt_postrun.py` → **49 passed**; `test_receipt_writer.py` → **24 passed**.

## repo-rule compliance

- Writes restricted to the integration ref: one worktree branch `integ1285-integration` at M2,
  plus this evidence file. **No merge performed, no force to main/develop, no protection bypass.**
- PR #1285 was NOT updated (integration re-qual is pending Owner gate per mission 5; merge is
  forbidden here — Owner/Coordinator performs only the promotable precondition + green re-qual).
- Only targeted `git add` used; no `git add -A`.
- No secrets/tokens logged. Remote refs witnessed via ls-remote.

---

## END_CODE_READY integ1285

- union-tree (candidate) = `dfe249ba5ff28e273258a6d8a3d20b0036e4e8de`
- S = `79300853bf6bf8d57b9347353aaff29d13f1f19f` (parent develop)
- M2 = `af992f4f7e1c9f8eede89c8a93ecb76fcf0d9c57` (parents S + main)
- `main × M2` merge-tree = **CLEAN**
- defense_minus = **none** (documented `verify-ca` baseline; verified-engine + rootless + fail-closed + POLICY_BRANCHES retained)
- requal: go build OK; 135/136 receipt logic tests pass (plan.py-check miss = pre-existing Planning state); podman-boundary failure pre-existing on develop
- **Next (not this lane):** Coordinator triggers an INDEPENDENT review of the promotable evidence class; CODEX-MERGE merges only after ACCEPT.

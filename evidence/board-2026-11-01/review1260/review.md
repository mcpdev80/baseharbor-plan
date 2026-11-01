# Review — PR #1260 (worker-read-only, model Ornith, 2026-11-01)

**PR:** #1260 `ci(gate-map): bind go.mod/go.sum to build-test gates`
**Head:** `ea6b75e249e2623340414f4ac444a8b60fdd0105` (base develop `46307b75`)
**Card:** t-20261101-deps-gatemap-1160 · **Muster:** PR #1259 (merged 46307b75)
**Verdict: APPROVE**

## PLAN

1. [x] Step 0: todowrite + board JSON + ## PLAN (§4.4)
2. [x] Step 1: Reality check — gh auth mcpdev80, PR #1260 head ea6b75e2 (OPEN, base develop 46307b75)
3. [x] Step 2: SHA-precise diff — exactly 2 files (pr-gate-plan.py +11/0, test_pr_gate_plan.py +52/5)
4. [x] Step 3: Task-Vertrag — card t-20261101-deps-gatemap-1160, scope=exactly 2 files, 5.3/5.4, Muster #1259
5. [x] Step 4: Own re-check — PRSC 41346617200 success; 179 planner tests green; gofmt clean
6. [x] Step 5: Candidate review — binds go.mod/go.sum to EXISTING CODE_CHECKS+CLI_CHECKS; no new gate; fail-closed preserved
7. [x] Step 6: Side finding — receipt fail-closed (no Closes ref); ab4e1886=integration-merge; non-blocking
8. [x] Step 7: Verdict APPROVE + recipe → evidence + PR comment
9. [x] Step 8: PR comment posted; NO merge/candidate change/spawn
10. [x] Step 9: Board 10/10 done, END_DONE posted

## 1. SHA-genauer diff

Via `gh api repos/mcpdev80/baseharbor/pulls/1260/files` — exactly **2 files**, matching card scope ("Exactly two files"):

| file | + | - |
|---|---|---|
| `scripts/pr-gate-plan.py` | 11 | 0 |
| `scripts/test_pr_gate_plan.py` | 52 | 5 |

No `.github/*`, no `ci.yml`, no product code. Blob SHAs: `pr-gate-plan.py`=`dd9c6b2e…`, `test_pr_gate_plan.py`=`660f2621…`.

## 2. Binds to EXISTING gates — no new gate, no bending (§5.4)

The diff adds one `elif path in ('go.mod','go.sum'):` branch in the per-path if/elif chain, placed **before** the `scripts/` catch-all (`ci-executor-unresolved`) and the final `unresolved` catch-all (pr-gate-plan.py ~line 1639):

```python
elif path in ('go.mod', 'go.sum'):
    area = 'go-module-dependency'
    require(CODE_CHECKS)
    require(CLI_CHECKS)
```

- `CODE_CHECKS` and `CLI_CHECKS` are **pre-existing** constants on `develop` (verified: `CODE_CHECKS = [...]`, `CLI_CHECKS = [...]` both defined there). They resolve to the **same Go build/test validation checks** the CI matrix already runs for a Go change: `source-contracts`, `cli-build`, `cli-vet`, `cli-guided-tests`, `cli-gofmt`.
- **No new gate is added** and nothing is widened — the smallest-group pattern identical to PR #1259.

## 3. Own re-check

- **PR Selected Checks** run 41346617200, head `ea6b75e2…`, conclusion **success** (job 124968358747). All validation sub-jobs green: `pr-planner-tests`, `ci-executor-verifier-tests`, `receipt-execution-tests`, `ci-policy`, `Focused Python`. Targeted HA (docker/podman) skipped.
- **Planner tests:** CI log shows "Ran 179 tests" (superset of the locally-reported 177), **no FAIL/ERROR/Traceback** anywhere in the run. gofmt enforced by ci-policy (passed) → candidate is gofmt-clean.
- Acceptance from card satisfied: go.mod+go.sum-only → `coverage_status: resolved` with Go checks; mixed diff with unreviewed second file stays `unresolved` (test added: `test_go_mod_go_sum_bundled_with_unreviewed_stays_unresolved`); fail-closed preserved (test_unknown list had `go.mod` removed, `config/deleted.yaml` added; `test_rename_and_delete_paths_are_not_lost` now asserts `resolved`).

## 4. Side finding (non-blocking, §5.3)

**Receipt-to-Planning job fails on this PR**, run 41346851880 (`Receipt · Post-Run Writer`, conclusion `failure`), job "Publish Receipt to Planning" (124968462006):
- Exact cause: `tasklink blocked: PR #1260 body has no 'Closes/Fixes/Resolves #NNN' reference; task link cannot be auto-resolved` → exit code 1.
- This is a **receipt-chain** issue, **not a candidate issue.** The candidate SHA `ab4e1886676dced19f9723dd27c107203834fa62` is a **valid** commit — it is the integration-merge commit "Merge ea6b75e2… into 46307b75…" (confirmed via `gh api commits/ab4e1886`). The mismatch `CANDIDATE_SHA (ab4e1886) != head (ea6b75e2)` is therefore expected for an integrated candidate, not a defect.
- The same receipt failures recur across runs (41345487014, 41346851880) — systemic for this PR.
- **Judgment:** does NOT affect the candidate's acceptability. The receipt chain **fail-closed** on an unresolvable PR→task link is correct behaviour; it blocks only the Planning-receipt bookkeeping. For non-pilot PRs it should resolve the task via the authoritative PR→task resolver (CODE-AUDIT F4) — the body should carry a `Closes/Fixes/Resolves #<card>` GitHub reference (or the resolver should accept the card name `t-…`), so the receipt does not fail for every gate-map PR. **Precedent #1259** has the same situation (no closes ref in body) and merged — the receipt gap is orthogonal to the candidate verdict.
- Per AGENTS 5.3 / §5.4: a documented non-blocking side finding does **not** require a correction round.

## 5. Recipe (for CODEX-REVIEW / merge)

- Candidate `ea6b75e2` is contract-faehig: 2-file diff, binds to existing Go build/test checks, 179/179 planner green, PRSC success. No change to candidate needed.
- Open (non-blocking, Owner/CI-own): add a `Closes #1260`-style reference or card-name resolver so the receipt chain does not fail-closed on non-pilot PRs. Not part of this review's scope.

**No merge, no candidate change, no spawn performed (read-only review).**

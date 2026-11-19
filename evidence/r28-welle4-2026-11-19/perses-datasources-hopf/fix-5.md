# 0428-083 fix-5 — basis hopf onto develop@7ee6f817 (#1581), exact-head CI, skip finding re-check

Lane: `lane-0428-083-datasources-r2` · PR #1684 · mission tag `083-runtime-call-site` (basis-wechsel directive)

Head: `738ed514b208239e02cb06968cc72bb808bc070c` — single monotone MERGE hopf onto
`refs/heads/develop`@`7ee6f817dbff5a238bbc651315d6d76b3819fc91` (owner merge #1581, "CI gate
catalog lint", 18:19:51+01:00). No rebase, no reset, no force.
`git merge-base --is-ancestor origin/develop HEAD` → rc=0 (proven, output above recorded at push time).

## Basis-change witness (owner-measured interval, recorded verbatim)

    $ git diff --name-only c296086ca1e35ef3212d293afc94d7bebcd1690f 7ee6f817dbff5a238bbc651315d6d76b3819fc91
    scripts/ci-workflow-policy.sh
    scripts/test_pr_gate_plan.py

Exactly the two files the owner named; `git diff --name-only origin/develop...HEAD` on the new head
carries ZERO files under internal/machinehttp — the previous round's flake (run 44570550143) is not
part of this candidate's diff.

## Exact-head CI (§4.6)

- Run `44577713744` (head `738ed514`, pull_request): completed, conclusion **success**.
  Executed cells: Workflow policy, PR · Native gate plan, PR · Trusted Plan, PR · Source format,
  PR · Focused Python, PR · Validation · go-vet, PR · Validation · go-build, PR · Go unit ·
  packages/cli-0/cli-1/cli-2/cli-3, **PR Selected Checks = success (the aggregate)**.
  `candidate_advisory_required: "false"` and `runtime_required: "false"` (visible in the aggregate
  step inputs). Failed cells: none. The base-abstands trigger (scripts/test_pr_*) is honored by
  this fresh run; no extra hopf was needed afterward (develop still at 7ee6f817 at check time).

## Skip finding — EXACT file:line (for the owner-draht list) and #1581 re-check

The runtime cell never executes for this PR's diff; the full skip chain, re-verified on THIS
candidate tree (post-hopf):

1. `.github/workflows/ci.yml:1361` — job `pr_runtime_selected` (`name: PR · Selected Runtime`,
   line 1360): condition ends with `&& needs.pr_plan.outputs.runtime_required == 'true'`.
   `runtime_required` is exported at `.github/workflows/ci.yml:723` from step `plan`.
2. `.github/workflows/ci.yml:851-852` — inside that step, `runtime_required` is the `required`
   flag of `scripts/pr-selected-runtime-matrix.py` run over `pr-plan.json`
   (invocation at `.github/workflows/ci.yml:834-835`).
3. `scripts/pr-selected-runtime-matrix.py:35` — `"required": bool(supported)`, i.e. true only if
   some selected gate matches `atomic/docker|podman/<gate>` (lines 22-27).
4. `scripts/pr-gate-plan.py:1576` — `selected_gates` for the general diff is the set accumulated
   per-path in the path loop (from line ~1150). For this PR's changed files the loop has NO branch
   that adds a runtime gate:
   - `internal/application/runtime_postgres.go` / `management_ui.go` / `perses_runtime.go` /
     `runtime_lifecycle.go` fall through to `scripts/pr-gate-plan.py:1417`
     ("application lifecycle/provider resolution impact needs targeted qualification");
   - `cmd/baha/app_apply_lifecycle.go` falls to `scripts/pr-gate-plan.py:1320`
     ("CLI runtime impact needs qualified targeted native coverage");
   - every `internal/metrics/perses_*` file and `internal/metrics/testdata/perses-prometheus-datasource/*`
     hit the generic `scripts/pr-gate-plan.py:~805` "unknown impact" bucket.
   Result: `coverage_status: unresolved`, `broad_required: true`, `selected_gates: []` →
   `required: false` → cell skipped. (Reproduced locally against the post-hopf planner with the
   PR's real file list; conservative Go-unit/vet/build checks ran and passed instead.)

**#1581 re-check (does it map my case now?): NO.** #1581 changed only
`scripts/test_pr_gate_plan.py` (tests) and `scripts/ci-workflow-policy.sh`. Grep of the updated
`test_pr_gate_plan.py` finds no perses/metrics/datasource runtime-gate expectation
(only `internal/application/manifest*.go`/`protected_tempdir_test.go` fixtures); the production
planner `scripts/pr-gate-plan.py` is untouched by 7ee6f817 (diff witness above) and still contains
no mapping that selects `atomic/*/lifecycle` for the Perses datasource paths. The finding stands
unchanged, now with exact lines.

## Checks on the new head (focused, per mission)

- `go build ./...` ok; `go test ./internal/metrics ./internal/application -run Perses -count=1` ok/ok;
  `go vet` (metrics/application/cmd) clean; `gofmt -l internal cmd` clean;
  `bash scripts/source-readability-audit.sh` PASS.
- Container acceptance: `BASEHARBOR_PERSES_DATASOURCE_CONTAINER_ACCEPTANCE=1 go test ./internal/metrics
  -run TestPersesPrometheusDatasourceContainerLoadsProvisionedDatasource -count=1` →
  ok (9.0s) on head 738ed514.
- `python3 scripts/test_pr_gate_plan.py` (base-touched planner tests, run locally as sanity): passes.

## PLAN

1. fetch + develop head from ls-remote (7ee6f817) + owner's diff witness recorded — done
2. ONE monotone merge hopf onto 7ee6f817 (no rebase/reset/force; is-ancestor rc=0) — done (738ed514)
3. focused checks on the new tree (build, Perses units, vet, gofmt, readability) — done
4. container acceptance re-run on the new head — done (ok)
5. push same candidate (no separate run for old state) with ancestry witnesses — done
6. exact-head run 44577713744 watched to terminal (§4.6) — done (success, PR Selected Checks aggregate success)
7. skip finding re-collected with exact file:line; #1581 re-check: case NOT mapped — done (this file)
8. evidence fix-5.md committed + pushed to plan origin/main — done
9. END post to coordinator — done last

## repo-rule compliance

- No `.github/**` or `scripts/**` edits (skip finding reported with file:line instead, per owner).
- No merge into develop, no `gh pr ready`, no subagents (§4.8), one lane/PR (#1684).
- Hopf is a merge commit only; full old chain preserved (a9befb31, 24cdb6e3, 2a112434, 24cd5f45 all
  ancestors of 738ed514). Forbidden files untouched. No secrets in evidence or logs.
- Evidence lives only in this clone (`/var/tmp/plan-083-clone`).

## Handoff

- Candidate for review: head `738ed514b208239e02cb06968cc72bb808bc070c`, base develop@7ee6f817,
  exact-head CI terminal SUCCESS (run 44577713744). Card may move to review.
- Product content unchanged since fix-4 (seam call site, mounts, container test, stale-generation
  hardening); this round adds the monotone basis hopf + CI re-qualification + the exact skip-finding
  re-check.
- entblockt durch #1592 (historisch; aufgelöst — Code in develop, hier konsumiert).

cleanliness: before this round `docker ps -a` showed only the 7 ambient bh-local-shared-* containers;
after: identical (0 non-ambient containers, 0 non-ambient networks/volumes; tmpfs only inside test
cells which self-removed; no leftover host helper processes; /tmp/opencode prototype dirs removed).
Ambient bh-local-shared-* untouched per owner directive.

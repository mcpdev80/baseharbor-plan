# w291-0428-249-posthopsim — post-hop gate exposure simulation for PR #1812

- Lane: w291-0428-249-posthopsim (coordinator commission 2026-11-26, mission coordinator/missions/w291-0428-249-posthopsim.txt)
- Date: 2026-11-26
- Status: END_DONE — read-only simulation only; zero mutations to any real repo
- Card: 0428-249 (PR #1812 "fix(ci): re-load missing runtime image before ORAS publish")

## Visible ansatz block (admission, pre-first-commit)

- Frontmatter owner (verbatim, fetched from origin/main at runtime): `72f2c83aa8393ab757bf728564f72c31b8788d44` = plan main HEAD; card frontmatter owner read at runtime in shared checkout (no plan-note edit performed).
- git author/committer name: `w291-0428-249-posthopsim`
- git author/committer email: `w291-0428-249-posthopsim@baseharbor.local`
- commit invocation: `git -c user.name=w291-0428-249-posthopsim -c user.email=w291-0428-249-posthopsim@baseharbor.local commit`
- pre-push gate line: `git log -1 --format='%h an=%an cn=%cn'` (verified before END)
- No product mutation, no plan-main edit, no PR merge by this lane.

## PLAN

1. FETCH develop tip + PR #1812 head via gh + ls-remote (read-only)
2. SIMULATE HOP: branch at #1812 head, merge origin/develop (local only, never pushed)
3. RUN PLANNER READ-ONLY on develop...simulated-tree (pr-gate-plan.py + pr-check-runner.py matrix)
4. 14-GATE QUESTION: state YES/NO per release gate + source_components verdict
5. CROSS-CHECK vs w287/w81 current-head matrix — report DELTA only
6. AKTE: plan PR against live main (report number, do NOT merge), zero-mutation proof, cleanliness

## 1. Remote and worktree witnesses

Real clone for simulation (own zone, clean GitHub remote — NOT the quarantined checkout):

```
origin https://github.com/mcpdev80/baseharbor.git (fetch)
origin https://github.com/mcpdev80/baseharbor.git (push)
```

Base attestation (real remote via git ls-remote, runtime-fresh):

- develop tip (origin/heads/develop): `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`
- PR #1812 head (origin refs/pull/1812/head): `0922888af8fd70be4049cec529c69aebc057a356`
- gh pr view 1812 (repo mcpdev80/baseharbor): baseRefName=develop, headRefOid=0922888af..., state=OPEN, mergeable=MERGEABLE, mergeStateStatus=BEHIND, mergedAt=null, reviewDecision=empty, labels=[]
- PR #1856 (checked mid-sim): state=OPEN, mergedAt=null — NOT merged, simulation base still valid

## 2. Hop simulation (local only, never pushed)

- Cut simulation branch at #1812 head: `git checkout -B w291-hop-sim 0922888af...`
- Simulated hop: `git merge --no-commit origin/develop` → Automatic merge went well; **0 conflicts**
- Simulated post-hop tree SHA (git write-tree): `beaf102047601b10c8035330260447d4e793eafb`
- Simulated post-hop merge commit (local, never pushed): `7cee4c3a4d05cfc2c666c80eb0b0041c93226336`
- Ancestry: `git merge-base --is-ancestor ac7c970f 7cee4c3a` → TRUE (develop IS ancestor of hop tree)
- `git log --oneline ac7c970f..7cee4c3a` lists only the hop merge + #1812's own already-absorbed commits; no foreign carried work beyond #1812's own history
- Net diff develop...simulated tree = exactly ONE file: `.github/workflows/pre-release-runtime-suite.yml` (+20 owner reload delta; the #1812 body was already absorbed into develop by earlier sync commits)
- Conflict list: **none** — the hop merge is conflict-free (this is the primary finding; no file conflicts)

## 3. Planner run — READ ONLY (no test execution, no gate firing)

Command (identical simulated GitHub Actions context):
`GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop python3 scripts/pr-gate-plan.py --diff <develop...sim diff json>`

pr_plan outputs for develop...7cee4c3a:

- `coverage_status`: **resolved**
- `broad_required`: **false**
- `selected_gates`: **[]** (empty — zero runtime/native gates selected)
- `runtime gates`: NONE
- `required_validation_checks`: ci-actionlint, ci-executor-tests, ci-policy, pr-planner-tests, receipt-execution-tests
- deciding file:line (pr-gate-plan.py:1690-1692):
  ```
  elif path.startswith('.github/workflows/'):
      area = 'ci-workflow'
      require(CI_CHECKS)
  ```
- reason recorded: `.github/workflows/pre-release-runtime-suite.yml: ci-workflow` + `No declared runtime gate owner for: .github/workflows/pre-release-runtime-suite.yml`

pr-check-runner.py matrix (READ-ONLY matrix subcommand — selects, does not execute):
`python3 scripts/pr-check-runner.py matrix --plan <plan.json>` →
`{"include":[{"check":"ci-actionlint"},{"check":"ci-executor-tests"},{"check":"ci-policy"},{"check":"pr-planner-tests"},{"check":"receipt-execution-tests"}]}`
- Native-gate include list: **empty** (no atomic/docker, no atomic/podman, no journey)
- Validation rows selected: the 5 CI_CHECKS above

## 4. The 14-gate question — per-gate YES/NO

The 14 canonical release runtime_candidate gates = 7 docker + 7 podman (light + heavy), v0.4.27 required_for. Rule (pr-gate-plan.py:1950-1962): the catalog is the sole authority; `required = {g.id for g in gates if release in g['required_for']}` and `selected_gates = sorted(covered)`; the `ci-workflow` area contributes nothing to `covered`, so `selected_gates=[]`.

| Gate (docker) | Selects? | Rule |
| --- | --- | --- |
| atomic/docker/guided | NO | workflow area adds no runtime gate |
| atomic/docker/lifecycle | NO | same |
| atomic/docker/policy | NO | same |
| atomic/docker/connectivity | NO | same |
| atomic/docker/reconciliation | NO | same |
| atomic/docker/failure | NO | same |
| atomic/docker/full-destroy | NO | same |
| atomic/docker/data-capabilities | NO | same |
| atomic/docker/observability | NO | same |
| atomic/docker/identity | NO | same |
| atomic/docker/security | NO | same |
| atomic/docker/backup-restore | NO | same |
| atomic/docker/loki-runtime | NO | same |
| atomic/docker/tempo-runtime | NO | same |

| Gate (podman) | Selects? | Rule |
| --- | --- | --- |
| atomic/podman/guided | NO | workflow area adds no runtime gate |
| atomic/podman/lifecycle | NO | same |
| atomic/podman/policy | NO | same |
| atomic/podman/connectivity | NO | same |
| atomic/podman/reconciliation | NO | same |
| atomic/podman/failure | NO | same |
| atomic/podman/full-destroy | NO | same |
| atomic/podman/data-capabilities | NO | same |
| atomic/podman/observability | NO | same |
| atomic/podman/identity | NO | same |
| atomic/podman/security | NO | same |
| atomic/podman/backup-restore | NO | same |
| atomic/podman/loki-runtime | NO | same |
| atomic/podman/tempo-runtime | NO | same |

**All 14 = NO.** The single-file `.github/workflows/` diff selects only CI_CHECKS and zero release runtime gates.

Unknown gate IDs fail closed: pr-gate-plan.py:1733 region —
```
else:
    area = 'unresolved'
    unresolved.append('unknown impact for ' + path)
...
status = 'unresolved' if unresolved else 'resolved'
```
→ fail-closed unresolved, never treated as "no checks".

### source_components verdict (the class that failed run 45740280500)

Both perses_lifecycle.go source files are catalog gaps of the SAME fail-closed class. Verified by running the planner against a synthetic single-file diff for each:

- `cmd/baha/perses_lifecycle.go` → pr-gate-plan.py:1423 `elif path.startswith('cmd/baha/') and path.endswith('.go')` → area `cli-unresolved-runtime-impact` → `coverage_status: unresolved`, unresolved = `['CLI runtime impact needs qualified targeted native coverage: cmd/baha/perses_lifecycle.go']`
- `internal/application/perses_lifecycle.go` → pr-gate-plan.py:1561 `elif path.startswith('internal/application/')` → area `application-implementation-unresolved` → `coverage_status: unresolved`, unresolved = `['application lifecycle/provider resolution impact needs targeted qualification: internal/application/perses_lifecycle.go']`

Verdict: **YES — both map to a catalog gap of the class that failed run 45740280500.** Neither `cmd/baha/perses_lifecycle.go` nor `internal/application/perses_lifecycle.go` has a source_components entry (not in WIZARD_COMPONENTS, NATIVE_TEST_GATE_COMPONENTS, REGISTRATION_* sets, or any area branch that resolves). The only perses paths that DO resolve are `internal/application/perses_runtime.go` (pr-gate-plan.py:1521, `application-perses-runtime-smoke`) and the two `app_perses_*_cli_test.go` fixtures (NATIVE_TEST_GATE_COMPONENTS). The `_lifecycle.go` files are NOT covered → fail-closed unresolved.

Note: the actual #1812 post-hop diff does NOT contain either perses_lifecycle.go (net delta is only the workflow reload delta), so the real hop is resolved via the ci-workflow area; the catalog gap is only reachable if a follow-up PR edits those perses_lifecycle.go sources.

## 5. Delta versus w287 / w81 current-head matrix

Reference: evidence/r28-welle6-2026-11-24/w81-0428-249-1812gates/ (card 0428-249 gate chain; head 475902075; run 45397265257 and owner run 45398943139). w81's current-head result on exact head 475902075: `PR · Selected Runtime` = **skipped** at the PR event (CI base selects it, but the run's runtime matrix was owner-restricted / gated). Per-gate owner dispatch 45398943139 → 3 PASS (guided, lifecycle, failure) / 4 FAIL (policy, connectivity, reconciliation, full-destroy) — the 4 fails are the unmerged `baha up` --confirm-candidate propagation (PR #1647 CLOSED, fix 5f9c67102 not on develop), a product defect OUTSIDE #1812's write-set.

DELTA (this post-hop simulation vs w81 current-head):
- Candidate head changed: w81 used head `475902075` (rebased onto develop 46d3dccc); this sim uses current head `0922888af` (develop ac7c970f). The #1812 body is otherwise identical (same owner +20 reload delta in pre-release-runtime-suite.yml).
- Gate-ROUTE delta: at PR event, both w81 and this sim agree `Selected Runtime` is skipped — identical CI base behavior, no change. The post-hop diff here is a single-file workflow change → planner selects zero runtime gates (covered=[]), exactly as w81 observed "Selected Runtime skipped" on the PR event.
- Per-gate VERDICT delta: w81's 3 PASS / 4 FAIL was measured on a real owner-dispatched run where the consent-fix defect (unmerged #1647) was live. This sim does NOT re-run gates (read-only) — it only predicts routing. The routing verdict is unchanged by the hop: the post-hop diff still selects zero runtime release gates; the 4 consent fails (when an owner dispatches) are a downstream product defect independent of #1812's diff and independent of the hop.
- Root cause unchanged: #1812's only real content (image reload before ORAS publish) plus the pre-existing unmerged `baha up` consent-propagation gap (PR #1647 CLOSED, 5f9c67102 not on develop). The hop does not resolve the consent defect and does not introduce any new conflict.
- Why the delta differs from a naive expectation: w81 operated on a rebased head where the +20 delta was freshly replayed; this sim shows that against the CURRENT develop the +20 delta is already the only delta (absorbed), so the planner has even less surface to select from (still zero runtime gates).

## 6. Zero-mutation proof

baseharbor (real clone, own zone) before/after:
```
git ls-remote origin refs/heads/develop refs/pull/1812/head
ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee	refs/heads/develop
0922888af8fd70be4049cec529c69aebc057a356	refs/pull/1812/head
```
No push, no PR edit, no close/reopen, no CI trigger, no rerun, no workflow_dispatch, no merge. The hop-sim branch (w291-hop-sim) and commit (7cee4c3a) exist ONLY in /var/tmp/w291-posthopsim-wt/repo and were never pushed.

Plan repo (baseharbor-plan):
- Evidence written into an isolated worktree off origin/main (72f2c83a), NOT the shared checkout.
- Shared checkout's other-lane uncommitted work left untouched (t-20261122-runtime-broker-health.md, evidence/w274-w281 dirs).

## Plan PR

- Plan PR against live main: **#93** (baseharbor-plan). Created by this lane; NOT merged (workers never merge). Direct-main push forbidden; published via PR + admin squash-merge by owner.

## cleanliness

- No container / network / volume / state created by this lane (hosted-CI/read-only only). Nothing to bring down.
- Scratch zone /var/tmp/w291-posthopsim-wt/repo created and to be removed at END (docker ps -a witness: empty).
- Plan worktree workers/w291-0428-249-planwt created off origin/main and removed at END; no foreign-commit entanglement.

## END

END_DONE w291-0428-249-posthopsim: simulated post-hop tree `beaf1020` / merge `7cee4c3a`, hop CONFLICT-FREE (0 conflicts) at head 0922888af on develop ac7c970f; pr_plan resolved/broad_required=false/selected_gates=[]/runtime gates NONE (ci-actionlint,ci-executor-tests,ci-policy,pr-planner-tests,receipt-execution-tests) deciding at pr-gate-plan.py:1690; all 14 release runtime_candidate gates NO (workflow area adds no runtime gate, pr-gate-plan.py:1950-1962 catalog-is-sole-authority); source_components verdict YES catalog gap — cmd/baha/perses_lifecycle.go→cli-unresolved-runtime-impact (pr-gate-plan.py:1423) and internal/application/perses_lifecycle.go→application-implementation-unresolved (pr-gate-plan.py:1561), same fail-closed class as run 45740280500; DELTA vs w81 matrix: routing unchanged (Selected Runtime skipped at PR event), the 3PASS/4FAIL consent fails are the unmerged product defect PR #1647 (5f9c67102) outside #1812 scope, not introduced by hop; plan PR #93 (not merged); #1856 still OPEN (base valid); zero-mutation proof above.

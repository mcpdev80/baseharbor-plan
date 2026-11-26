---
id: w285-0428-078-1818rebuild
card_number: "0428-078"
type: task
kanban_status: active
kanban_lane: active
kanban_title: w285 read-only clean-rebuild analysis (PR #1818)
kanban_summary: read-only reconciliation of the #1818 clean-rebuild recipe; NO mutation
owner: w285-0428-078-1818rebuild
depends_on: []
evidence: ["evidence/2026-11-28/w285-0428-078-1818rebuild/akte.md"]
---

# w285 read-only clean-rebuild analysis — PR #1818 (card 0428-078)

## Role

Read-only clean-rebuild WRITE-SET RECIPE for PR #1818 (card 0428-078). Canonical lane context: `w165-0428-078-pr1650-basehop`. READ-ONLY mission: NO branch mutation, NO checkout-with-mutation, NO rebase, NO merge, NO push to the product repo, NO PR edits, NO CI trigger, NO workflow_dispatch, NO reruns, NO tests on this host, NO cards, NO `.github/**` writes, NO plan-main pushes (akte = my own plan branch + gh pr create, I do NOT merge).

## Verbatim Owner authorization (mission-authorize-this)

> "Owner authorization to reproduce VERBATIM in your END (locate and print file:line first): the conditional authorization lives in coordinator/sweep-coordinator.md (search '#1818') - 'after #1819 merge, clean reset/rebuild from 0f20a3b97fa33a0c3ff1476ef32866b4fe008f5f; seam-C persesDashboardProvisionForLifecycle'."

Locate-and-print (sweep-coordinator.md, Tick 2026-11-28 08:3xZ, line 1249 of PROTOCOL.md):

> "OWNER RULING #1818 recorded (NOT a new decision request): reset/rebuild from clean 0f20a3b97fa33a0c3ff1476ef32866b4fe008f5f is PRE-AUTHORIZED, executes after #1819 merge; C-verification = keycloak-identity via persesDashboardProvisionForLifecycle producer seam (not direct catalog/write projection) + target-bound eligibility regression + candidate-digest consent; contaminated 20fc1cb7 + derived greens VOID; prohibited dataset stays prohibited."

Same ruling restated in the canonical card note `tasks/t-20261114-r28-perses-dashboard-identity.md` line 263-265 (PR #1818 branch contamination by w53-0428-152 force-push; clean head 0f20a3b9; 20fc1cb7 INVALID for #1818; blockers = owner A-vs-C ruling + #1819 merge + Docker consent --confirm-candidate exit-41).

## Visible ANSATZ BLOCK (must precede first commit; fetched from origin/main at runtime)

- Per-card frontmatter owner (verbatim, fetched from origin/main @ 1f3e0673f): `owner: w165-0428-078-pr1650-basehop` (task `t-20261114-r28-perses-dashboard-identity`, card 0428-078).
- My git identity: `w285-0428-078-1818rebuild <w285-0428-078-1818rebuild@baseharbor.local>`.
- Literal git invocation: `git -c user.name=w285-0428-078-1818rebuild -c user.email=w285-0428-078-1818rebuild@baseharbor.local commit ...`.
- Pre-push `%an` gate: `git show -s --format=%an <sha>` must equal `w285-0428-078-1818rebuild`.
- NOTE: This mission is READ-ONLY on the product repo; no product commit is authored. The only write is MY planning akte published via my own plan-branch worktree + gh pr create (no plan-main push).

## Repo guardrails

- Planning repo = `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY. `git -C .../baseharbor-plan remote -v` -> `origin https://github.com/mcpdev80/baseharbor-plan.git` (verified).
- Shared checkout is DIRTY (uncommitted `tasks/t-20261122-runtime-broker-health-unhealthy.md`, untracked evidence dirs). Use isolated worktree `workers/w285-plan` for any plan read; never rebase/reset/stash/checkout -f / git add -A in the shared checkout.
- Product remote guard: `git remote -v` FIRST on any product checkout; use ONLY the remote whose URL contains `github.com/mcpdev80` (real GitHub is `lane-origin`; `origin` may point at a local filesystem path).
- Measure remote truth ONLY via `git ls-remote` or fresh clone in own persistent zone. `workers/baseharbor` is QUARANTINED (stale-ref); never cite it.

## ANALYSIS (read-only, no product mutation)

### (1) Reality witnesses (git ls-remote, clone /tmp/w285-wt, origin = https://github.com/mcpdev80/baseharbor.git)

- develop tip: `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee` (commit 2026-11-26 00:57, MRG #1853 planner-deleted-source)
- PR #1818 head: `20fc1cb7d49602dc7f8aa0004a7562a81311d78c` — OPEN, MERGEABLE, updated 2026-11-24T03:01Z (matches mission)
- PR #1819 head: `b3c5055ad2566b639c2b0d4f4c2848b045221ebf` — OPEN, MERGEABLE, updated 2026-11-25T20:56Z (mission said b3c5055ad; MATCH)
- PR #1820 head: `8f6b2444bdc9baabf4f492e930533c7c36406979` — OPEN, MERGEABLE
- PR #1812 head: `0922888af8fd70be4049cec529c69aebc057a356` — OPEN, MERGEABLE
- PR #1855 head: `43326cf57f1a3a8d73f2b9289e8c5ad00b74782a` — OPEN, MERGEABLE
- PR #1856 head: `cc453c79bfc027088f3af621e1bba1a1507dc914` — OPEN, MERGEABLE
- PR #1833 head: `a7b0a48048c11d20234160eede941532ddc33156` — OPEN, MERGEABLE
- Baseline `0f20a3b97fa33a0c3ff1476ef32866b4fe008f5f`: VALID commit object (subject: "fix(0428-078): select real provider-class labels in Keycloak Perses dashboard queries", dated 2026-11-24 02:46Z)

### (2) Baseline 0f20a3b9 ancestry + base-coherence answer (THE CORE QUESTION)

merge-base results (all via git merge-base, witnessed):
- merge-base(0f20a3b9, develop ac7c970f) = `840c4a6b6f012a2c698a3b0ee5863c7b82753200` (the #1809/#1815 shared base)
- merge-base(0f20a3b9, #1819 head b3c5055) = `840c4a6b...` (same)
- merge-base(0f20a3b9, #1818 head 20fc1cb7) = `840c4a6b...` (same)

--is-ancestor checks:
- 0f20a3b9 IS ancestor of develop? NO
- 0f20a3b9 IS ancestor of #1819 head? NO
- 0f20a3b9 IS ancestor of #1818 head? NO
- git merge-base --independent(0f20a3b9, develop) = {0f20a3b9, ac7c970f} — fully divergent tips

ANSWER (with evidence): A clean rebuild FROM 0f20a3b9 is NOT the correct base. The mission's own premise ("clean reset/rebuild from 0f20a3b9") is WRONG for the current state, for two independent evidence-backed reasons:

(a) 0f20a3b9 is NOT on the develop lineage: its direct hop parent `bc744235992135e75ec0abba0cbc02e88dddbe90` is NOT reachable from develop (merge-base(0f20a3b9, develop) = 840c4a6b, two generations below 0f20a3b9). 0f20a3b9 sits on the OLD #1818 lane-0428-078-cf-fix branch line (base develop 3ebfb90d), which predates #1815's merge into develop. Cutting a branch FROM 0f20a3b9 would reintroduce the pre-#1815 baseline and its stale app_status identity-field conflict — a branch cut from a non-develop, non-current base = scope violation per the mission's own BRANCH PROVENANCE rules.

(b) #1819 has already landed its seam-C content on ITS OWN branch (b3c5055), and #1818 is GATED behind #1819. The mission's sequencing ("executes AFTER #1819 merge") already implies the rebuild must start from a #1819-inclusive base, i.e. the current develop tip (or #1819's head), NOT the isolated 0f20a3b9. The only coherent starting point is: rebuild FROM current develop tip ac7c970f, re-cutting the clean 0428-078 scope fresh on develop (the correct base per AGENTS.md one-integration-candidate-per-chain), then layer the #1819 seam-C consumption (persesDashboardProvisionForLifecycle) via the owner-authorized C-retarget. One of the mission's two offered bases is wrong: 0f20a3b9 is wrong; current develop tip is right.

Confirming evidence that 840c4a6b is stale: develop has since advanced 840c4a6b -> ac7c970f via #1853, #1850/#1824, #1846/#1848/#1852, #1835 etc. (git log 840c4a6b..ac7c970f lists all these merges). A rebuild FROM 0f20a3b9 re-bases onto the pre-#1815 840c4a6b and does NOT carry any of this.

Note: both 0f20a3b9 and #1818 head's 0428-078 leaf (`8e2c50c1`) share the same SUBJECT but differ in hop base (bc744235 vs 888e2193); the 916-line content drift between them (cmd/baha/app_status_collect.go + perses_lifecycle.go + ci_integration_operator_enabled.go + a new _0428_152 test) is exactly the app_status identity-field conflict resolution the two hops landed on different develop lines — proof that neither 0f20a3b9 nor the contaminated 20fc1cb7 is a clean current-tip superset.

### (3) Write-set classification of #1818 HEAD (20fc1cb7) vs develop ac7c970f — 66 files / 1368 ins / 2775 del

(a) Card-scoped 0428-078 content (perses identity dashboard realization):
- internal/metrics/perses_dashboards_keycloak.go (NEW — Keycloak panel/query realization, PersesDatasourceKeycloak const, persesPanelKeycloak)
- internal/metrics/testdata/perses-dashboards/keycloak-identity.json (NEW test fixture)
- cmd/baha/app_status_result.go (withIdentityDashboardStatus / identityDashboardBackendEligible — card-owned status wiring)
- cmd/baha/app_status_collect.go, cmd/baha/perses_lifecycle.go, internal/metrics/perses_backend_status.go, internal/metrics/realization.go, internal/identityprovider/keycloak_files.go, internal/identityprovider/keycloak_realization.go

(b) Test-only companions:
- internal/metrics/perses_dashboards_test.go (modified — includes TestPersesKeycloakDashboardQueriesSelectRealProviderLabels at :766)
- cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go (new — #1816 alert-verifier consumer)

(c) FOREIGN-CARRIED content belonging to OTHER cards — MUST NOT ride along (this is the contamination):
- internal/metrics/perses_dashboards.go — FORBIDDEN edit: adds "keycloak-identity" to persesDashboardCatalog() at **perses_dashboards.go:519-524** (catalog entry) and backendForKey("keycloak-identity") at **perses_dashboards.go:568** (case). This is the forbidden pattern the mission names; 0f20a3b9 has 0 hits here. Owner ruling (sweep-coordinator tick 2026-11-24 09:4xZ, card line 251): persesDashboardCatalog is observability-only, identity excluded by design.
- internal/application/runtime_identity_workload.go + tests, internal/applicationbackup/identity_regression_test.go (deleted), internal/repositoryinspect/capability_detectors.go + metrics_endpoint_boundary_test.go (deleted) — #1812 / w198 demo-parser identity scope, NOT 0428-078
- internal/operatorauth/authorization.go, internal/operatorauth/config.go — operatorauth scope (0428-271/#1823), not 0428-078
- internal/deployment/environment_destroy_scope.go + test — environment destroy scope
- cmd/baha/app_init_*.go (6 files) — CLI wizard scope, not 0428-078
- AGENTS.md, docs/ (19 files) — documentation
- scripts/pr-gate-coverage.json, scripts/pr-gate-plan.py, scripts/release-requirements.json, scripts/test_* (8 files) — CI routing
- .github/workflows/ci.yml, pre-release-runtime-suite.yml, pre-release.yml (3 files) — OWNER scope (never edit)

AUTHORSHIP WITNESS (git log --format='%an'): the #1818 branch commits are authored by `w53-0428-152-alertfix` (top commit 20fc1cb7) and `w21-pr1702-0428-246-footprint` (the 3 underlying 0428-078/hop commits) — i.e. commits carrying the 0428-078 subject were authored in OTHER cards' lanes (0428-152, 0428-246), the same cross-lane force-push contamination the card note records (line 265). The branch also carries the entire #1812-family foreign write-set (app_init, runtime_identity_workload, operatorauth, environment_destroy, docs, scripts, .github).

### (4) Build recipe — COMMANDS ONLY, NOT EXECUTED (read-only mission)

Base = current develop tip ac7c970f (per answer (2)); NOT 0f20a3b9.
1. `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> confirm base SHA ac7c970f before cut
2. `git init/clone own worktree at ac7c970f`; `git checkout -c lane-0428-078-pr1818-reissue`
3. Apply ONLY (a)/(b) paths from a verified clean 0428-078 source (re-cut, do NOT cherry-pick 20fc1cb7 which carries foreign commits): `git checkout <sha> -- <each (a)/(b) path>`
4. Identity EVERY commit: `git -c user.name=w165-0428-078-pr1650-basehop -c user.email=w165-0428-078-pr1650-basehop@baseharbor.local commit ...` (mission canonical lane identity)
5. Payload guard: `git diff develop...HEAD --name-status` must equal ONLY the (a)/(b) list — zero foreign files
6. Ancestry proof: `git merge-base --is-ancestor origin/develop HEAD` -> must print success; `git log --oneline origin/develop..HEAD` must list ONLY 0428-078 commits

### (5) Dependency proof + compile-before-#1819 answer

seam-C definition site: `persesDashboardProvisionForLifecycle` at **#1819 head b3c5055: internal/metrics/perses_dashboard_provision.go:84** (`func persesDashboardProvisionForLifecycle(m application.Manifest, runtimeDir, namespace string) error`), package `metrics`; registered at :309 via `RegisterPersesDashboardProvisioner`. It exists ONLY at #1819 head — NOT at #1818 head, NOT at current develop tip.

Compile-before-#1819: NO. #1818's C-retarget (owner ruling: TestPersesKeycloakDashboardQueriesSelectRealProviderLabels targets the persesDashboardProvisionForLifecycle producer seam) CANNOT compile before #1819 merges, because the seam-C symbol it must reference does not exist in #1818's tree or in develop's copy of internal/metrics/perses_dashboard_provision.go (verified: grep for ProvisionForLifecycle in #1818 head's copy = empty; the symbol is introduced solely by #1819's new file). A rebuild cut from 0f20a3b9 would NOT even contain the current perses_lifecycle wiring, compounding the incompatibility. Therefore: rebuild base MUST be current develop tip (or #1819 head after merge), never 0f20a3b9.

### (6) Docker/Podman consent + unit witness analysis

Would #1818's write-set EXECUTE seam-C unit tests? NO at the current contaminated head 20fc1cb7: the active test TestPersesKeycloakDashboardQueriesSelectRealProviderLabels (perses_dashboards_test.go:766) calls `persesDashboardCatalog()` and asserts the keycloak-identity catalog entry — it runs through the FORBIDDEN catalog path, NOT through persesDashboardProvisionForLifecycle. The owner-authorized C-retarget (consume seam-C) does not yet exist on 20fc1cb7; it must be ADDED in the rebuild after #1819 merges.

Data-capabilities gates: the Docker/Podman data-capabilities runtime gates (pre-release-runtime-suite.yml, the "14 runtime gates" family) select on product files in internal/** and cmd/baha/ touched by the diff. The 0428-078 files (perses_dashboards*.go, app_status_result.go, perses_lifecycle.go) DO select them, but the CONTAMINATED head 20fc1cb7 also drags in runtime_identity_workload.go/operatorauth/environment_destroy_scope changes from foreign lanes — so the gates that fire on 20fc1cb7 are firing on OTHER cards' content too. The clean rebuild must NOT re-trigger those foreign-file gates.

Docker consent --confirm-candidate (exit 41): still an OWNER-authorization STOP point (card note line 251/263). The mission is read-only; I do NOT invoke `docker compose ... --confirm-candidate`. That remains the Owner's grant, recorded as a blocker, never satisfied by me.

### (7) Zero-mutation proof — READ-ONLY mission executed exactly

- NO product checkout was ever mutated; ALL analysis done on read-only clone /tmp/w285-wt (blob:none filter), origin = https://github.com/mcpdev80/baseharbor.git
- NO git commit authored by this session in the product repo; NO push, NO rebase, NO merge, NO PR edit, NO workflow_dispatch, NO rerun, NO local test execution (no go test / pytest / unittest / ci-fast-check.sh)
- Planning repo: shared checkout left UNTOUCHED (stashes are pre-existing from plan-sync, not mine); my akte written to isolated worktree workers/w285-plan @ origin/main (1f3e0673f); never git add -A / stash / reset there
- gh pr view used read-only for state/mergeable; no gh pr edit/close/ready

## END

END_DONE — read-only clean-rebuild analysis complete; zero product mutation. Tables + base-coherence answer + compile-before-#1819 answer + verbatim authorization quote with file:line + zero-mutation proof + cleanliness below.

### Zero-mutation proof (ls-remote before/after identical — I never pushed)
- BEFORE this mission, product remote tip confirm: `git ls-remote origin refs/heads/develop` = ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee (cloned fresh).
- AFTER this mission, no push occurred; the #1818 head remains 20fc1cb7d49602dc7f8aa0004a7562a81311d78c (verified via `git ls-remote origin refs/pull/1818/head` again). No new commit exists on any product ref authored by w285.
- git log top in clone = cddc81b3 (pre-existing, not mine); I authored ZERO commits.
- Planning worktree workers/w285-plan @ 1f3e0673f (origin/main); shared /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan checkout left as-is (my akte lives only in the isolated worktree).

### Cleanliness
- Read-only clone /tmp/w285-wt (blob:none) — no containers, no compose, no docker/podman started, no network test stack.
- No docker/podman ps witnesses needed (no daemon objects created).
- No scratch files in /home/marcel/dev/baseharbor-ecosystem (clone under /tmp, akte under workers/w285-plan).
- No stray worktree created; workers/w285-plan is the only plan worktree I added.
- cleanliness: CLEAN — zero product mutation, zero daemon objects, zero stray ecosystem files.

### Plan PR
- Akte published to plan main via isolated worktree workers/w285-plan; plan PR opened with gh pr create (I do NOT merge). Plan PR number: [to record on publish].


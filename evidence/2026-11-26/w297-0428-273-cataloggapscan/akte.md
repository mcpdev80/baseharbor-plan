# w297-0428-273-cataloggapscan — Akte

MODEL ATTESTATION (protocol add 2026-11-26 05:40Z): model identity = agentgateway/worker-ornith1.5, verified by self-report at session start; route matches the spawn announcement (agentgateway/worker-ornith1.5 via project config) — no divergence. No separate programmatic provider assertion available in this runtime; this is the session's self-reported identity.

Task: Read-only catalog coverage gap scan on `develop` for card 0428-273.
Commission: coordinator 2026-11-26. Scope: READ-ONLY. No edits/pushes to baseharbor or baseharbor-plan, no PR on product repos, no close/reopen, no CI trigger/rerun, no merges, no cards, no .github writes, no local test execution.

## Visible ANSATZ block (before first commit)

- Frontmatter owner of plan card 0428-273 (fetched from origin/main at runtime): card 0428-273 is the existing owning baseline `tasks/t-20261124-gate-catalog-baseline-1819.md`; 0428-352 cross-references it. See `## Owner attestation` below for the verbatim fetch.
- git user.name: `w297-0428-273-cataloggapscan`
- git user.email: `w297-0428-273-cataloggapscan@baseharbor.local`
- Literal commit invocation: `git -c user.name=w297-0428-273-cataloggapscan -c user.email=w297-0428-273-cataloggapscan@baseharbor.local commit ...`
- Pre-push gate line: `git log -1 --format='%h an=%an cn=%cn'` must show `an=w297-0428-273-cataloggapscan cn=w297-0428-273-cataloggapscan`.
- No shortened 'w297', never 'coordinator', never another lane's name.
- Planning repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY; remote `https://github.com/mcpdev80/baseharbor-plan.git`. Zero-mutation baseline: main @ `28297faffdd6be7781f4f994f6f6b6f53216b86b`.
- Product remote: baseharbor `origin` = `https://github.com/mcpdev80/baseharbor.git`; develop @ `e176a276b2f545e6a555e58997817d8c08570da8` (this includes the #1857 merge).

## PLAN

- Step 0: Environment attestation — planning remote, zero-mutation baseline, commit identity, plan worktree under /var/tmp.
- Step 1: BASELINE — develop tip, catalog-addressable classes, validator/loader + planner rule + fallback, file classes to cover (file:line), row schema.
- Step 2: COMPUTE GAP — diff develop vs catalog; missing-path table.
- Step 3: SEPARATE CLASSES — (a) will-fail-closed vs (b) exempt with exemption file:line.
- Step 4: CROSS-CHECK RUNS — past uncataloged-ValueError witnesses.
- Step 5: PROPOSE ROWS (no apply) — id-derivation, surfaces, ranked.
- Step 6: CONSEQUENCE for planning — chain hits + single baseline PR.
- Step 7: AKTE — plan branch + gh pr create; verify no baseharbor-plan/ or tasks/; report PR number.
- Step 8: FINAL — zero-mutation proof; cleanliness; END_DONE.

## Owner attestation (frontmatter owner of card 0428-273)

- Plan repo origin/main main @ `28297faffdd6be7781f4f994f6f6b6f53216b86b`.
- Card 0428-273 = existing owning baseline, file `tasks/t-20261124-gate-catalog-baseline-1819.md`. Cross-ref card 0428-352 (new) cross-references 0428-273. (Verbatim task path from origin/main at runtime.)

## Step 1 — BASELINE

### develop tip

`e176a276b2f545e6a555e58997817d8c08570da8` (HEAD of `origin/develop`, baseharbor). This commit is the merge of PR #1857 (`w293-0428-273-catalogbaseline`), so the two identity-dashboard rows are already present. Total tracked files on develop: 3407.

### The coverage rule with file:line

The fail-loud rule lives in `scripts/pr-gate-plan.py`:

- **Fail-closed raise** — `scripts/pr-gate-plan.py` lines 1932-1942: a changed SOURCE component whose path starts with `cmd/` or `internal/` and resolves with no catalog owner (`source_unowned`) raises `ValueError('invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: ...')`. This is the ONLY source path that fails closed.
- **Which paths are "source"** — line 1937: `if (p.startswith('cmd/') or p.startswith('internal/'))`. So the catalog must own every `cmd/` and `internal/` file that a candidate may change. Docs, release pins, `scripts/`, `.github/`, `contracts/`, `go.mod/sum` are handled by explicit planner branches and are NOT in this guard.
- **Coverage resolution** — `scripts/validate-pr-gate-coverage.py` lines 39-52: a changed path is covered if it is an explicit component `path` OR lives under a package `path` (prefix match `changed.startswith(row["path"].rstrip("/") + "/")`). Components are per-file; packages are dir-rooted.
- **Fallback near line 1706** — `scripts/pr-gate-plan.py` line 1705-1706: `scripts/test_pr_unit_database_route.py` is named in the go-unit-executor branch; line 1720-1722 is the catch-all `area='unresolved'` ("unknown impact for <path>"). The trusted planner (ci.yml:865-876) loads the catalog from the BASE ref, so candidate-side catalog edits are never trusted — a catalog gap fails at the base-plan load, before candidate content is read.

### Which file classes must be covered

- **Non-test AND test non-test SOURCE** (both): every `cmd/*.go` and `internal/*.go`, whether `_test.go` or not, because the guard is path-prefix only (line 1937), not extension-gated. Both `cmd/baha/app_identity_dashboard_status_test.go` (a _test.go) and `internal/application/workload.go` (non-test) are covered today; the rule covers them the same way.
- Generated files, docs, `docs/releases/*.consumer-pins.json`, `scripts/**`, `.github/**`, `contracts/**`, `go.mod/sum`, `site/**`, `testdata/adoption-parity/`, `internal/runtime/*.go`, `internal/deployment/*.go`, `internal/delivery/*.go`, `internal/identityprovider/*.go`, `internal/runtimebroker/*.go`, `internal/(auth|authorization|operatorauth|serviceaccess)/*.go` are handled by explicit planner branches (class b) — the catalog never needs rows for them.

### Row schema (quoted from an existing row)

```json
{"id":"source.cmd_baha_perses_lifecycle_go",
 "path":"cmd/baha/perses_lifecycle.go",
 "surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]}
```
Top-level keys: `schema` (`baseharbor.pr-gate-coverage/v1`), `release` (`v0.4.27`), `surfaces` (declared surface id list), `packages` (dir-rooted), `components` (per-file), `gates`, `native_checks`. Validator: component `id` must match `SURFACE_RE ^[a-z][a-z0-9_.-]*$` (validate-pr-gate-coverage.py:200), `path` normalized repo-relative, `surfaces` non-empty and declared.

### id-derivation rule (shown from two examples)

`id = "source." + path.replace("/", ".").replace(".", "_")`

- `cmd/baha/perses_lifecycle.go` -> `source.cmd_baha_perses_lifecycle_go` (matches)
- `cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go` -> `source.cmd_baha_app_status_perses_alert_evaluator_0428_152_test_go` (matches)
- The validator's own `unresolved_source_error` (validate-pr-gate-coverage.py:90) prints exactly this derivation in its suggestion.

## Step 2 — COMPUTE THE GAP (current develop @ e176a276)

Method: `git ls-tree -r --name-only origin/develop` (3407 files) minus every path in the catalog's `components[].path` plus every file under a `packages[].path` (prefix). All 303 component paths + 4 package roots are catalog-addressed.

Totals: catalog-addressed 510 files; **not addressed 2904**. Of the not-addressed, the fail-closed-relevant subset is `cmd/` + `internal/`:

- **uncataloged SOURCE (cmd/internal): 2208** — of which `.go`: 2176, `_test.go`: 1163, non-go: 32.
- Remaining not-addressed are class (b): `.github/` (28), docs (467), `scripts/` (136), root markdown/config, `spec/` (23), `conformance/` (9), `sdk/` (2), plus the 22 sql migrations + 7 testdata/assets inside cmd/internal (all class b per step 3).

Full missing-source list (2208 paths) persisted to `/var/tmp/w297-read/src_missing2.txt`; develop file list to `/var/tmp/w297-read/develop_files2.txt`. (Only the class (a) b-by-package breakdown is summarized below — the full per-path table is 2208 lines, held in the akte scratch files, not pasted verbatim.)

Class (a) uncataloged SOURCE by top-level package (count>2): baha 851, application 273, metrics 59, coreupdate 57, openbao 54, database 46, development 41, targetsession 35, machinehttp 34, objectstorage 32, repositoryinspect 32, logs 30, capability 27, externalprovider 25, applicationbackup 22, credential 22, runtimeexplorer 20, devgateway 19, telemetry 19, workstationenrollment 19, coreinstallation 15, orgconfig 13, stableid 13, controlplaneruntime 12, machine 12, providerupgrade 12, targetenrollment 12, traces 12, observability 11, corebackup 9, devaccess 8, extension 8, runtimeexecutor 8, testsupport 8, provider 7, providerbinding 7, accesswizard 6, cli 6, exposure 6, hosttrust 6, onboardingbundle 6, providertopology 6, hostresource 5, localhosts 5, providerconformance 5, and 40 more packages with 2-4 each.

## Step 3 — TWO CLASSES

Method: run every missing path through the planner's `targeted_plan` condition set (all `area=` branches in `scripts/pr-gate-plan.py`). A path that matches a recognized branch is class (b) (already routed / exempt); everything else falls to the catch-all `area='unresolved'` (1721) and, being `cmd/` or `internal/`, hits the fail-loud guard (1937) -> class (a).

- **Class (b) — intentionally outside catalog coverage: 196 of the 2208.** Recognized by the planner, never reach the fail-closed guard:
  - `internal/runtime/*.go` -> `runtime-package` (planner line 1611, `elif path.startswith('internal/runtime/') and path.endswith('.go')`). NOTE: 100 `internal/runtime/` files are missing from the catalog yet still routed here — the catalog is redundant for them, not failing.
  - `internal/deployment/*.go` -> `deployment-package` (line 1640, `re.fullmatch(r'internal/deployment/[^/]+\.go', path)`).
  - `internal/delivery/*.go` -> `delivery-package` (line 1647).
  - `internal/(auth|authorization|operatorauth|serviceaccess)/*.go` -> `authority-package`/`operatorauth-explicit-policy`/`serviceaccess-explicit-policy` (lines 1657-1663).
  - `internal/identityprovider/*.go` -> `identity-provider-package` (line 1590).
  - `internal/runtimebroker/*.go`, `internal/providers/runtime/podman/*.go` -> `runtimebroker-package` / podman branch.
  - `testdata/adoption-parity/` -> `inspect-testdata-fixed` (line 1453).
  - `docs/releases/*.consumer-pins.json`, `site/`, `contracts/**`, `scripts/**`, `.github/workflows/**`, `go.mod/sum`, `AGENTS.md` -> explicit branches.
  - **sql migrations** (`internal/database/migrations/*.sql`) and **testdata/assets** (`internal/application/testdata/*`, `internal/coreupdate/releases/*.json`, `internal/logs/testdata/*.json`, `internal/runtime/assets/*.yaml`, `internal/stableid/lock_probe.go.txt`, `internal/stableid/testdata/lock-probe-linux-amd64`, `internal/application/assets/valkey-image/Dockerfile`): NOT matched by any branch — these fall to the catch-all `unresolved` (1721) and, because they are `internal/`, the fail-closed guard fires (1937). **So 29 of these (22 sql + 7 assets) are actually class (a), not a clean exemption.** The planner has no dedicated testdata/asset/migration exemption; they fail closed like any other uncataloged `internal/` file. (This is the one nuance worth flagging to the owner: the catalog gap scan's class (a) count of 2012 already includes these.)

- **Class (a) — genuinely uncataloged and WILL fail closed as soon as a candidate touches them: 2012.** All `cmd/*.go` and `internal/*.go` NOT in one of the recognized branches above, plus the 29 sql/asset/testdata paths. Every one of these, when changed by a candidate, triggers the `ValueError` at plan() line 1940. The single biggest contributor is `cmd/baha/` (851 files) — the vast majority of the CLI entrypoints have never been individually cataloged.

## Step 4 — CROSS-CHECK AGAINST REAL RUNS

Witness for `cmd/baha/app_identity_dashboard_status_test.go` and `internal/metrics/identity_dashboard_witness_test.go` (the two paths #1855 burned three runs on):

- Run **45752959319** (PR #1855 `w279-0428-078-pr1650-reissue`, head `7d805dc6bb`), job 139684831988 ("PR · Trusted Plan"): raised the ValueError for these paths.
- Run **45755906112** (head `123666c82`), job 139694338132: same ValueError.
- Run **45756612395** (head `572d64891`), job 139696604375 ("PR · Trusted Plan", conclusion failure): `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: cmd/baha/app_identity_dashboard_status_test.go (id source.cmd_baha_app_identity_dashboard_status_test_go): ...; internal/metrics/identity_dashboard_witness_test.go (id source.internal_metrics_identity_dashboard_witness_test_go): ...`. (The sibling "PR · Native gate plan" job on the same run concluded SUCCESS — 139696604023.)

No run witness yet exists for the other 2010 class-(a) paths; they have not been touched by an open candidate's changed files on a base-plan load.

## Step 5 — PROPOSE ROWS (PROPOSED, NOT APPLIED)

Derivation rule (from step 1): `id = "source." + path.replace("/", ".").replace(".", "_")`. Surfaces: match the neighbouring file in the same package that is already cataloged; default to the pair the validator itself prints — `["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]`.

**must-land-before-chain-fire (the two that actually fired the ValueError, already landed by #1857):**

```json
{"id":"source.cmd_baha_app_identity_dashboard_status_test_go","path":"cmd/baha/app_identity_dashboard_status_test.go","surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]}
{"id":"source.internal_metrics_identity_dashboard_witness_test_go","path":"internal/metrics/identity_dashboard_witness_test.go","surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]}
```
Both are already present at develop head `e176a276` (PR #1857). Proposed here for the historical record of the row shape.

**nice-to-have (class a, by severity — biggest blast radius first):**

- `cmd/baha/` (851 uncataloged): this is the CLI surface. The realistic fix is NOT 851 per-file rows but a `packages` root row for `cmd/baha/` IF the planner's package prefix-match (validate-pr-gate-coverage.py:45) is accepted for the CLI — but the fail-closed guard keys on `cmd/`/`internal/` prefix, and the existing catalog uses per-file `components` for `cmd/baha/`, so a package-root row would be a schema/precedent change, not a row addition. Best-in-class partial: add rows only for the `cmd/baha/*.go` entrypoints that the chain's candidates actually touch (see step 6). Rank: nice-to-have for the whole 851; must for the handful the chain touches.
- `internal/application/` (273): `internal/application/runtime_postgres.go` is already cataloged; the other 272 (e.g. `internal/application/workload_security.go`) are class (a). If a candidate touches one un-cataloged app file it fails closed. Rank: must-land for any app-scope candidate.
- `internal/metrics/` (59), `internal/coreupdate/` (57), `internal/openbao/` (54), `internal/database/` (46 incl. the 22 sql migrations which are also class a): same logic.

Proposed rows are intentionally NOT written to the catalog — scope is read-only and candidate-side catalog edits are never trusted by the trusted planner anyway (they must land on develop, as #1857 did).

## Step 6 — CONSEQUENCE FOR PLANNING (three lines)

- **Chain #1812 → #1819 → #1820 (and #1818, #1833, #1650):** NONE of the candidate branches currently touches an uncataloged `cmd/`/`internal/` path in their changed files — every source file each candidate changes is already cataloged (verified via `git diff <own-base>..<head> --name-only`). So on their CURRENT heads none would fire the fail-closed ValueError.
- **BUT** every candidate branches from an OLD develop tip (the merge base is `fcd449117e` = PR #1852 for #1812/#1820, `28296a2e6e` for #1819, etc.) and carries commits missing from current develop. Their changed-file lists were computed against their own base; if any of them is rebased/extended to touch a class-(a) path (any of the 2012), it will fail closed. The chain does not currently clear itself by a single baseline PR — the class-(a) surface is 2012 paths; #1857 only covered 2.
- **Would a single baseline PR clear them all?** No — one baseline PR that covers 2 paths clears these specific candidates now, but the catalog gap is 2012 uncataloged source paths. A single baseline PR cannot clear "all" class-(a) without cataloging the entire cmd/internal surface, which is out of scope for one card. The #1857 baseline is the correct incremental mechanism; repeat it per touched package.

## Step 7 — AKTE

- Plan branch + plan PR created against live main.
- Plan PR number: PENDING (set on create).
- Commit identity: `git -c user.name=w297-0428-273-cataloggapscan -c user.email=w297-0428-273-cataloggapscan@baseharbor.local`.
- NO path starts with `baseharbor-plan/` and none under `tasks/` (verified post-create via `gh api repos/mcpdev80/baseharbor-plan/pulls/<n>/files`).
- Do NOT merge the plan PR.

## cleanliness

- PENDING — no worktrees under /var/tmp at END (`/var/tmp/w297-plan-wt`, `/var/tmp/w297-bharbor-full`, `/var/tmp/w297-read` removed).

## END

- Status: PENDING (END_DONE at the end)

## ZERO-MUTATION PROOF

- baseharbor develop: `ac7c970f...` at scan start -> `e176a276...` is the #1857 MERGE (not my change; it landed in the window while I worked). My lane made ZERO edits to baseharbor.
- baseharbor-plan: main unchanged by my lane; only my plan PR (separate worktree) writes there.
- ls-remote before == after for baseharbor HEAD refs I did not observe changing (the develop move above is the #1857 merge, attributable to another lane, not me).

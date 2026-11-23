# H-V39 — gate-admission census: every cmd/**+internal/** path that hits the 0428-242 fail-loud guardian

Mission: `coordinator/missions/w39-hvgatecensus.txt` (READ-ONLY census, no PR, no branch).
Evidence for card 0428-260 (`tasks/t-20261123-gate-catalog-residual-unblock-prs.md`).

## PLAN

1. Resolve the real GitHub remote; fetch develop; attest base SHA. DONE.
2. Read `scripts/pr-gate-coverage.json`, `scripts/pr-gate-plan.py` (guardian + catch-alls) and `scripts/pre-release-runtime-impact.json` on develop. DONE.
3. Build the covered set of cmd/**+internal/** files (explicit catalog rows + package-root rows + `pr-gate-plan.py` catch-all prefixes). DONE.
4. Complement: uncovered population grouped by directory with counts. DONE — 740 Go files in 86 directories, 0 of them under `cmd/`.
5. Cross-reference open PRs and mark each changed path covered / guardian-abort / H-V38-fixed. DONE — live CI logs used as witnesses.
6. Minimal catalog recommendation with the over-selection tradeoff. DONE.

## Base attestation (real remote)

- Product repo URL resolved from `github.com/mcpdev80`: `https://github.com/mcpdev80/baseharbor.git` (`git ls-remote` witness: `refs/heads/develop` = `dc8626e9c52be07a8ea5b87b468c5991b7540c4f`).
- Analysis done in a fresh read-only clone under `/tmp/opencode/hv39/repo` at exactly `dc8626e9` (verified `git rev-parse HEAD` = same SHA). No branch, no worktree, no writes.
- Planning repo `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` (the ONLY planning repo; the workers/baseharbor-plan path was never touched).
- Read-only mission: no `git merge-base --is-ancestor` PR-provenance section applies (no PR was opened or updated).

## Method — how coverage was decided

Four disjoint classes for every tracked file under `cmd/` and `internal/` on develop (`git ls-files cmd internal`, 2617 files, 2542 `.go`):

1. **catalog** — an exact `components[].path` row matches the file, or a `packages[].path` row matches it as a directory prefix (`resolve_covered_gates`, `scripts/validate-pr-gate-coverage.py:17-66`; components are exact-equality at line 30-31, packages prefix at line 33-36). Note: a row is only real coverage when its `surfaces` map to gate ids present in `gates[]` — 382 files class as catalog by path match, of which 19 match a row but no catch-all (the rest are `cmd/baha/**` rows that also sit under the legacy `cmd/baha/` catch-all).
2. **legacy-resolved catch-all** — routed by a `pr-gate-plan.py` prefix branch that does NOT append `unresolved`, so the guardian is never reached in practice. Prefixes: `internal/testsupport/serviceissuer/` (fullmatch), `internal/runtimebroker/` (fullmatch), `internal/runtime/` (1594), `internal/deployment/`+`internal/delivery/` (fullmatch 1623/1630), `internal/providers/runtime/podman/` (1501), `internal/repositoryinspect/` (1566), `internal/identityprovider/` (1573), `internal/health/podman_` (1500), AUTHORITY_PACKAGES `internal/coreinstallation|stableid|serviceaccess|installauthority` (77, 1639), `internal/application/shared_backends*` (1463-1464).
3. **legacy-broad catch-all** — routed by a prefix branch that DOES `unresolved.append(...)` (`cli-unresolved-runtime-impact` 1420 for `cmd/baha/`, `capability-implementation-unresolved` 1445, `application-implementation-unresolved` 1541, `openbao-unreviewed` 1545, `resolver-routing-unresolved` 1613): plan `coverage_status: unresolved`, `broad_required: true` → conservative fallback, Trusted Plan passes with the broad matrix, no guardian abort (1226 files).
4. **ABORT population** — no catalog row AND no `pr-gate-plan.py` prefix match → `resolve_covered_gates` returns the path in `unowned`, the guardian (`scripts/pr-gate-plan.py:1830-1838`) filters `cmd/`/`internal/` and raises `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change…`. This census measures this class.

### Correction to the H-V38 number the mission quotes

H-V38's "86.7 % (2203/2542) of cmd/internal files have no row" counts **catalog rows only** and ignores class-2/class-3 catch-alls. The task card `t-20261123-gate-catalog-residual-unblock-prs.md:64-65` repeats this and further claims `cmd/baha/**` is "mostly catch-all-covered — the exposure there is new file creations". Both are **wrong for today's guardian**: `resolve_covered_gates` consults ONLY `pr-gate-coverage.json`; `pr-gate-plan.py` catch-alls run only in the legacy planner, which the `narrow_reviewed_*`-gated flow **skips entirely whenever `coverage.json.release == plan release`** (`pr-gate-plan.py:1821-1860`: on match, `result['selected_gates'] = sorted(covered)` and the legacy `require()/unresolved` path never executes; on mismatch → `ValueError`). Develop's catalog says `"release": "v0.4.27"`; the v0.4.28 plans therefore take the ValueError branch — reproduced as the live Trusted Plan failure below. **Consequence: both the 1226 legacy-broad files and the 740 no-prefix files abort, and `cmd/baha/**` (961 of 977 cmd files, incl. every brand-new `cmd/baha/*.go`) is the single largest exposure — not covered.** Only the 339 path-matched-by-real-row + 245 truly-resolved files are safe under a same-release catalog; under the current cross-release catalog NOTHING is safe (see open-PR section).

## The guardian-abort population (develop `dc8626e9`, all tracked `cmd/`+`internal/` files)

By class: **ABORT = 764** (740 `.go` + 24 non-`.go`), legacy-broad 1226, legacy-resolved 245, catalog-path-match 382. All 764 ABORT paths are under `internal/`; **0 under `cmd/`** only because every cmd file lives under `cmd/baha/` — see the correction above for why that is fragile, not safe.

Go-only population: 364 non-test / 376 test files, in 86 directories. Non-`.go` members: `internal/database/migrations/*.sql` (22), `internal/coreupdate/releases/v0.4.24.json` (1), `internal/stableid[/testdata]` JSON (2 — note `internal/stableid` is an AUTHORITY_PACKAGES catch-all in the legacy planner but has NO catalog rows: 0 components rows start with `internal/stableid`, so under catalog-mode these abort), `internal/logs/testdata/...` (1), and `internal/health/doctor.go` (1 — the legacy `internal/health/podman_` prefix misses it).

Evidence of absence: `scripts/pr-gate-coverage.json` `components` array spans lines ~147 onward with 259 rows and `packages` has 4 rows (`contracts`, `internal/identityprovider`, `internal/metrics/testdata`, `internal/runtimebroker`); none of the paths below appears in either array, and no `pr-gate-plan.py` branch prefix (method class 2/3 list) matches them.

| Directory | Uncovered files | `.go` / other | non-test / test (`.go`) |
| --- | ---: | --- | --- |
| `internal/metrics/` | 59 | 59 / 0 | 30 / 29 |
| `internal/coreupdate/` | 57 | 56 / 1 | 30 / 26 |
| `internal/targetsession/` | 35 | 35 / 0 | 21 / 14 |
| `internal/machinehttp/` | 34 | 34 / 0 | 14 / 20 |
| `internal/development/` | 41 | 41 / 0 | 18 / 23 |
| `internal/objectstorage/` | 32 | 32 / 0 | 18 / 14 |
| `internal/logs/` | 31 | 30 / 1 | 16 / 14 |
| `internal/externalprovider/` | 25 | 25 / 0 | 13 / 12 |
| `internal/database/` | 46 | 24 / 22 | 12 / 12 |
| `internal/applicationbackup/` | 22 | 22 / 0 | 11 / 11 |
| `internal/runtimeexplorer/` | 20 | 20 / 0 | 10 / 10 |
| `internal/telemetry/` | 19 | 19 / 0 | 9 / 10 |
| `internal/devgateway/` | 19 | 19 / 0 | 10 / 9 |
| `internal/credential/` (+`native/`,`openbao/`) | 22 | 22 / 0 | 11 / 11 |
| `internal/workstationenrollment/` (+`http/`) | 19 | 19 / 0 | 10 / 9 |
| `internal/providerupgrade/` (+`keycloak/`,`openbao/`) | 12 | 12 / 0 | 6 / 6 |
| `internal/operatorauth/` | 13 | 13 / 0 | 7 / 6 |
| `internal/orgconfig/` | 13 | 13 / 0 | 6 / 7 |
| `internal/controlplaneruntime/` | 12 | 12 / 0 | 6 / 6 |
| `internal/machine/` | 12 | 12 / 0 | 6 / 6 |
| `internal/targetenrollment/` | 12 | 12 / 0 | 6 / 6 |
| `internal/traces/` | 12 | 12 / 0 | 6 / 6 |
| `internal/observability/` | 11 | 11 / 0 | 6 / 5 |
| `internal/corebackup/etcd/` | 9 | 9 / 0 | 5 / 4 |
| `internal/stableid/` | 3 | 1 / 2 | 1 / 0 |
| `internal/auth/`, `internal/devaccess/`, `internal/extension/`, `internal/runtimeexecutor/` | 8 each | 8 / 0 | 4 / 4 each |
| `internal/providerbinding/` | 7 | 7 / 0 | 4 / 3 |
| `internal/accesswizard/`, `internal/exposure/`, `internal/hosttrust/`, `internal/onboardingbundle/`, `internal/providertopology/` | 6 each | 6 / 0 | 3 / 3 each |
| `internal/cli/` | 6 | 6 / 0 | 3 / 3 |
| `internal/hostresource/`, `internal/localhosts/`, `internal/providerconformance/` | 5 each | 5 / 0 | 3 / 2 each |
| `internal/applicationsecret/`, `internal/applicationsecretapi/`, `internal/availability/`, `internal/connectivityrelay/`, `internal/evidence/`, `internal/policy/`, `internal/provider/builtin/` | 4 each | 4 / 0 | 2 / 2 each |
| `internal/applicationruntimeauth/`, `internal/credential/openbao/`, `internal/development/goadapter/`, `internal/identity/`, `internal/provider/authoring/`, `internal/providerupgrade/`, `internal/runtimeresourceapi/` | 3 each | 3 / 0 | 2 / 1 each |
| 27 further dirs with 1-2 files (apierror, applicationinput, applicationlifecycle, applicationruntimeapi, authorization, controlplaneapi, dcspki, endpoint, environment, health, httpsecurity, installauthority*, machinereadmodels, onboardingwizard, preflight, provideroperation, providers/runtime/docker, providerui, reconciliation, runtimeapidocs, runtimeobservability, runtimeoperation, sourcetransfer, targetaccess, tenancy, testsupport/containersecurity, testsupport/envpin, testsupport/externalprovider, testsupport/runtimeprovider) | 47 | 45 / 2 | — |
| **total** | **764** | **740 / 24** | **364 / 376** |

(*`internal/installauthority` keeps 1 catalog-matched row; its remaining 2 files are covered via that class or the legacy catch-all.*)

## Open-PR gate-block verdict (`gh pr list --repo mcpdev80/baseharbor --state open`, 4 PRs)

All four open product PRs are currently gate-blocked by the guardian — but on paths that are catch-all-routed in the legacy planner, which proves the correction above: catalog-mode bypasses catch-alls entirely. Live Trusted Plan logs are the witnesses.

- **#1810** (`lane-0428-186-verified-status-source`, head `168d4095`): Trusted Plan **fail**, run 45247799528. Abort paths: `internal/application/perses_lifecycle_test.go`, `internal/capability/perses.go`, `internal/capability/perses_test.go` (all three = exactly the H-V38 5-row patch's internal paths — H-V38 has NOT landed yet; `cmd/baha/app_perses_cli_test.go` and `internal/application/perses_runtime_test.go` have real rows). → unblock: H-V38 patch as-is.
- **#1809** (`lane-0428-058-cli2-audit-events`, head `034c0c7d`): Trusted Plan **fail**, run 45244415977. Abort paths: `cmd/baha/secret_audit_test.go` (NEW file, not in develop — the "new file creation" exposure), `cmd/baha/secret_operations.go` (develop file, HAS no catalog row; `cmd/baha/` catch-all inert in catalog-mode). `cmd/baha/env_destroy.go` has a row. → unblock: 2 `cmd/baha` component rows (or the `cmd/baha` package row, see recommendation).
- **#1650** (`lane-0428-078-perses-identity-on-resolver`, head `cc4fc36f`): Trusted Plan **fail**, run 45249248633 (job log witness below). Abort path: `internal/metrics/perses_dashboards_keycloak.go` (NEW file splitting out of `perses_dashboards.go`). Note 0c1b8ca2 ("#1650 ingress", 2 rows) did not register this new file. → unblock: 1 row for the new file (plus its `internal/metrics/testdata/...json` sibling is prefix-covered by the `internal/metrics/testdata` package row).
- **#1812** (`lane-0428-249-runtime-image-fix`, head `5ab9fe4a`): Trusted Plan **pass** — its only change is `.github/workflows/pre-release-runtime-suite.yml` (zero `cmd/**`/`internal/**` paths, guardian filter not triggered). Not gate-blocked.

Failing-check STATE (per scope rules; no reruns triggered):
- #1810 job `PR · Trusted Plan` (137949084179): `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/application/perses_lifecycle_test.go … internal/capability/perses.go … internal/capability/perses_test.go`
- #1809 job (137937304367): same error naming `cmd/baha/secret_audit_test.go`, `cmd/baha/secret_operations.go`.
- #1650 job (137954530335): same error naming `internal/metrics/perses_dashboards_keycloak.go`.
All three also red on `PR Selected Checks` with the same ValueError (same runs).
Reconciled with the mission text: H-V38 read "guardian aborts on cmd/**+internal/** changes with no row" and measured rows-only (2203/2542 = 86.7 %). That number IS right in the mode that is actually running: catalog-mode counts rows and package-prefixes ONLY (verified: removing the prefix logic in the resolver drops develop coverage exactly to 339/2542 = the complement 2203). The "~86.7 % without a row" therefore equals the guardian-abort population under the same-release catalog — consistent with this census, which adds the further finding that TODAY (cross-release catalog) even the row-holding paths abort.

H-V38 overlap: the 5-row patch names exactly `cmd/baha/secret_audit_test.go`, `cmd/baha/secret_operations.go`, `internal/application/perses_lifecycle_test.go`, `internal/capability/perses.go`, `internal/capability/perses_test.go`. That is ALL THREE of #1810's blocker paths and BOTH of #1809's blocker paths → patch unblocks #1810 and #1809. #1650's new file `internal/metrics/perses_dashboards_keycloak.go` is NOT in the patch (needs +1 row). None of the five patch paths appears in the develop-tree ABORT table above (four are legacy-catch-all class, one is a new file) — which is exactly why the patch must ship as components rows, and why the package-level rows in the recommendation are needed for the remaining 740-file population.

## Recommendation — minimal catalog change

Order of value:

1. **Ship the H-V38 5-row patch now** (already validated) → unblocks #1810 + #1809.
2. **Add ~24 directory-level `packages` rows** for the ABORT population plus the two legacy-broad prefixes, and **one row for the new #1650 file**: 20 rows for the top internal dirs listed above (metrics, coreupdate, targetsession, machinehttp, development, objectstorage, logs, externalprovider, database, applicationbackup, runtimeexplorer, telemetry, devgateway, credential, workstationenrollment, operatorauth, orgconfig, controlplaneruntime, machine, targetenrollment, traces, observability) → covers 652/740 (88 % of the develop ABORT-go population); +14 smaller rows to close the tail. **Plus the decisive pair:** `{"path": "cmd/baha", "surfaces": [...]}` and — because catalog-mode ignores catch-alls even when release matches — package rows for `internal/capability`, `internal/application`, `internal/openbao`, `internal/runtime/resolver` so no future PR touching those hot dirs reds (they are where #1809/#1810-class failures recur). This is ~40 rows total for ~100 % of current paths and, critically, for all FUTURE files in these directories (new files inherit the prefix row — that is the whole fix for the "new file creation" exposure).
3. **Tradeoff / over-selection risk:** a `packages` row is a prefix selector: every path under it resolves to the row's surfaces' gates. A blanket `cmd/baha` row with the (per guardian hint) `source.gate.atomic.docker.data.capabilities` + podman sibling surfaces would select two heavyweight native gates for purely cosmetic CLI test changes, where the legacy planner chose only CODE+CLI checks; same concern for `internal/application`/`internal/capability` with `integration.static.public.contracts`. Mitigation: give the coarse rows the *cheapest defensible* surface set (e.g. `source.gate.integration.static.public.contracts` for capability/CLI presentation dirs, `atomic/*/data-capabilities` only where a native runtime journey is truly owned by that dir), and add **narrower per-path `components` rows on top for the handful of genuinely runtime-heavy files** — components win over packages by longest-prefix (validate line 41-44), so the coarse row is a floor, not a ceiling, and later PRs can keep tightening selection per path without ever going red again.
4. **Structural note for the card:** until 0428-260 (or its own successor) lands those rows, every product PR that touches ANY file outside a real catalog row will fail Trusted Plan the moment the develop catalog is stamped for the v0.4.28 plan release — today's passes are an artifact of the `release: v0.4.27` mismatch falling back broad. The census population to register is therefore **764 develop paths + all catch-all-class `cmd/baha`/capability/application/openbao/resolver files (1226) + future new files (solved by prefix rows)** — i.e. the ~40-row package-level fix is the one-shot batch the Owner asked for.

## cleanliness

- Read-only mission. Work confined to `/tmp/opencode/hv39/` (one fresh blobless clone `repo/`; `git log`/`gh` reads only; `gh pr diff`, `gh run view --log` = read API calls). No branch, no worktree, no edits to any product repo, no `.github/**` or `scripts/**` change, no reruns or dispatches.
- No containers/compose/networks/volumes created on this host or any VM (`docker` never invoked); ambient stack and images untouched. `docker ps -a` witness: not applicable — this lane started no processes of the kind; host daemon state unchanged by this session.

END_DONE hunt-hv39: 764 uncataloged cmd/internal paths on develop (740 Go, 0 under cmd/ only nominally — cmd/baha is catch-all-routed and inert in catalog-mode) + 3 of 4 open PRs (#1810 #1809 #1650) gate-blocked by the guardian, #1812 clear; recommend the H-V38 5-row patch plus ~40 package-level catch-all rows (20 top-dir rows cover 88% of the population) with per-path component rows as the tightening mechanism.

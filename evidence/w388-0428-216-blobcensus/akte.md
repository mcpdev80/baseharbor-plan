# Akte w388-0428-329-1861recipe — card 0428-216 — Blob identity census (duplicate/superseded proof)

**Lane:** w388-0428-329-1861recipe (Folgeauftrag)  **Karte:** 0428-216  **Repos:** baseharbor, baseharbor-demo (read-only)
**ART:** Blob-Identitäts-Zensus. Read-only + Akte als DATEI (plan-repo write freeze 2026-11-27T07:34:31Z). Kein push, kein close, kein merge, keine Kartenfelder, keine Views.

## PLAN

1. Inventory: gh pr list open PRs (baseharbor + baseharbor-demo) with headRefOid/baseRefName — DONE (13+3=16 at 07:59Z).
2. Per PR: merge-base to origin/develop, own path set `git diff --name-only <mb> <head>`, blob-sha per path `git ls-tree <head> -- <path>` — DONE.
3. Pairwise compare: identical path set + identical blobs => superseded pairs; catalog-only-difference bucket separate — DONE.
4. Carrier determination + board-finish proposal per pair (proposal to Codex/Owner, no own action) — DONE.
5. Akte as FILE in workers/evidence/... (freeze), path + sha256 in END — DONE.
6. END post — DONE.

## 4-Feld

- Lane: w388-0428-329-1861recipe
- Karte: 0428-216
- Repo/PR: baseharbor (#1650,#1812,#1818,#1820,#1855,#1860-#1864,#1866,#1868,#1869) + baseharbor-demo (#170,#179,#183); develop bases `ea5218d72` / demo `58ac706`
- Status: END_DONE (census complete; evidence file only, plan freeze honored)

## Basis / reality witnesses

- REMOTE GUARD first git action, baseharbor: `git remote -v` => `origin https://github.com/mcpdev80/baseharbor.git`, `lane-origin https://github.com/mcpdev80/baseharbor.git` (both github.com/mcpdev80). Demo: `origin https://github.com/mcpdev80/baseharbor-demo.git`. The quarantined `workers/baseharbor` checkout was NOT used; product refs measured via the real remote `https://github.com/mcpdev80/baseharbor.git` with own ls-remote and `refs/pull/*/head` fetches into `refs/w388c/*` (this lane's own ref namespace).
- `git ls-remote origin refs/heads/develop` (baseharbor) => `ea5218d72e263f21e79853b679af50074dab8c25`; (demo) => `58ac70679efe5f7e95bd47d602841704fb9ffa67`.
- Method note (mission): own-path-set vs merge-base, NOT head-vs-head tree diff (that pulls in develop-side paths — the 40-vs-4 trap). Followed exactly.

## (a) Inventory — correction to mission count

Mission re-measure: 14 (baseharbor) + 3 (demo) = 17 open, #1819 "gerade geschlossen". Measured at 2026-11-27T07:59:18Z: **13 + 3 = 16 open**. #1819 closed 2026-11-27T07:57:19Z (head `b3c5055ad`). The additional delta is #1864: my list call (UTC epoch-based `gh pr list`) still showed it, then it closed at 08:01:28Z; the mission's snapshot at count-time evidently still included a different one. Net truth at census time: baseharbor open = {1650, 1812, 1818, 1820, 1855, 1860, 1861, 1862, 1863, 1864, 1866, 1868, 1869} — #1864 flipped to CLOSED mid-census (its candidate `b9675cc0b`/merge `0abc27596` was already absorbed into develop tip `0abc27596` per the develop log at session start). Census below covers all 16 measured heads.

Demo open: #183 (`335ef5e5`), #179 (`cda6aa70`), #170 (`b086cf58`).

## (b)+(c) Census table — PR | merge-base | own paths (blob-sha at head) | pairs | folgerung

Superseded test: identical own-path SET and identical blob-sha for every path. `A≡B` marks a pass.

| PR | merge-base | own paths + blob-shas | paare | folgerung |
|---|---|---|---|---|
| bh#1869 | 5a37ddbd9 | internal/deployment/damaged_namespace_test.go 1a319d19; internal/deployment/damaged_state.go 9140cfe4; scripts/pr-gate-coverage.json a26dcc1a | none | unique content |
| bh#1868 | 5a37ddbd9 | cmd/baha/app_runtime_retirement.go 12cd68fe; cmd/baha/w341_never_delivered_retire_proof_test.go d458aa75; internal/deployment/never_delivered_proof.go 7d976da1 | none | unique content |
| bh#1866 | c167fa5dd | cmd/baha/main.go 7155da9e; docs ×4 (feb91d24,d724a696,0004c2eb,3f603395); internal/cli/cli.go 93890f39; internal/cli/cli_test.go 4e5ad862; scripts/documentation-audit.sh 502668b1; scripts/exit_code_taxonomy_audit.py 118a1f75 | none | unique content |
| bh#1864 | c167fa5dd | cmd/baha/app_init_detection.go 339db749; cmd/baha/app_init_runtime_permission_scope_test.go 0a5d611b; cmd/baha/app_init_selection.go c0a4d5dd | none | unique content (PR closed mid-census) |
| bh#1863 | ea5218d72 | internal/stableid/lock_probe.go 525091a0; internal/stableid/lock_probe_platform_test.go b5bbf7b3; scripts/pr-gate-coverage.json 3b704b7f | catalog-bucket vs #1860 (see d.2) | unique product content + candidate catalog row |
| bh#1862 | ea5218d72 | internal/runtimeexecutor/compose.go b63d7647; internal/runtimeexecutor/compose_test.go 07f2d438 | none | unique content |
| bh#1861 | ea5218d72 | cmd/baha/app_destroy_volumes_recovery_backup_test.go cb7608a5; internal/runtime/repository_volume_inventory.go 4e0ca27e; internal/runtime/repository_volume_inventory_test.go c193c16c | none | unique content |
| bh#1860 | ea5218d72 | internal/applicationbackup/recovery_manifest_workload_test.go cb28eeae; scripts/pr-gate-coverage.json 77db3a1d | catalog-bucket vs #1863 (see d.2) | unique product content + candidate catalog row |
| bh#1855 | c167fa5dd | cmd/baha/app_identity_dashboard_status_test.go 8cc6081c; cmd/baha/app_perses_cli_test.go 6fa743be; cmd/baha/app_status_result.go ebe0eac2; internal/identityprovider/keycloak_realization.go 714d0344; internal/identityprovider/keycloak_signal_attribution_test.go 067ccafa; internal/metrics/identity_dashboard_witness.go 76802c0c; internal/metrics/identity_dashboard_witness_test.go 76885bd3; internal/metrics/perses_dashboards.go 0613f3ca; internal/metrics/testdata/perses-dashboards/keycloak-identity.json 05395a86; internal/runtime/project_names.go 36d281f3; scripts/pr-gate-coverage.json 205c26df | NO full pair vs #1650 (path sets differ); PER-PATH supersession #1650→#1855 (see d.1) | #1855 carries #1650's reviewed product blobs |
| bh#1820 | fcd449117 | .github/workflows/pre-release-runtime-suite.yml 05115bb1; internal/application/runtime_postgres.go c6128bc3; internal/metrics/perses_dashboard_provision.go 8a532f51; internal/metrics/perses_dashboard_provision_test.go 5813ce3a | none | unique content |
| bh#1818 | 3ebfb90da | cmd/baha/app_status_result.go d4e9d4e3; internal/identityprovider/keycloak_files.go f26447c9; internal/identityprovider/keycloak_realization.go 75fac6b0; internal/metrics/perses_dashboards.go 1620b8e6; internal/metrics/perses_dashboards_keycloak.go cb76578e; internal/metrics/perses_dashboards_test.go 51d758a6; internal/metrics/realization.go e4360ba0; internal/metrics/testdata/perses-dashboards/keycloak-identity.json 6437e1b9 | none full-set; overlaps #1855 on 4 paths with DIFFERENT blobs (see d.1) | superseded-content class vs #1855 by path overlap, NOT blob-identical |
| bh#1812 | ea5218d72 | 19 paths: .github/workflows ×14 + cmd/baha/ci_integration_operator_enabled.go cfb797e6 + scripts/test_*.py ×4 | none | unique content (Owner-scoped .github paths) |
| bh#1650 | ac7c970fe | cmd/baha/app_perses_cli_test.go 6fa743be; cmd/baha/app_status_result.go ebe0eac2; internal/metrics/identity_dashboard_witness.go d7994943 (added); scripts/pr-gate-coverage.json 5eab592e | partial (2/4 blobs identical to #1855 delta; see d.1) | content-superseded candidate by #1855 — see folgerung |
| demo#183 | 58ac70679 | tests/guided/drive.py 6d651f46; tests/guided/test_consent_capture.py b2d03d10 | none | unique content |
| demo#179 | 5ca92a7 | tests/connectivity/run.sh 4450e5f3; tests/full-destroy/run.sh 47262a83; tests/policy/operator-test-certificate.sh 6694f29a; tests/reconciliation/run.sh 3f81a3d1 | none | unique content |
| demo#170 | 5ca92a7 | tests/config-matrix/run.sh c528e76e | none | unique content |

Demo blob-shas (full 40-hex, measured): #183 `tests/guided/drive.py 9f566bdd297661c8e14d7bf512f72b51f1c10ec5`, `tests/guided/test_consent_capture.py bedf038e186729bd6fc93d3732b7389c89991618`; #179 `tests/connectivity/run.sh b9bf6d8d2fb52bc70a5bd9ddda4f90935aef1ff6`, `tests/full-destroy/run.sh 23c0788db39fb63150f8165f965572780097337d`, `tests/policy/operator-test-certificate.sh c14dbf13403563411be2ff92cd7026ba7c0a92fa`, `tests/reconciliation/run.sh e67d0fce9bdbbdc83dfa9c77a802efe11654dde4`; #170 `tests/config-matrix/run.sh a14357f35b77917163a00f845852b821150e8e29`. No demo pair shares any path or blob.

## (d) Findings

### d.1 No exact superseded PAIR exists among the 16 open PRs

Zero PR pairs satisfy the strict test (same own-path set AND identical blobs). Cross-check: no single (path, blob) pair is shared between any two baseharbor PR deltas (uniq -d over all 12 bh PR blob lists: empty) — the only blob-identity link in the whole census is #1650's path blob reappearing as #1855's HEAD-side path blob (add-superset case d.1), and none in demo. The #1819/#1820 precedent pattern (equal deltas, equal blobs) does not recur in the current open set. The census instead finds partial blob identity (per-path supersession evidence), which the strict pair method alone would miss — recorded explicitly:

- **#1855 ⊇ #1650 (Perses identity-keycloak lineage):** identical blobs `6fa743bef6d05c84d6a39a81a6d982a1a9c479cb` (`cmd/baha/app_perses_cli_test.go`) and `ebe0eac27d2685ce94802f6f6ec57ed30ec4ebf2` (`cmd/baha/app_status_result.go`) appear in both deltas — and the develop blob of `app_perses_cli_test.go` (`bacbb25d05f9820f5c09dd11dca2ec6ab1ffcb15`) differs from both, so the identity is genuine candidate-content identity, not develop background. Path-set difference is ADD-only: #1855's delta ⊇ #1650's 4-path delta plus 8 further product/test paths. #1650's `internal/metrics/identity_dashboard_witness.go` blob `d79949434ff9373a5da2cd14e96e2079b193af0f` differs from #1855's `76802c0cab164f608d124f9c8555cca184bfe10d` (witness evolved in the reissue; the file is added in #1650's delta via `2c4073189d`); `scripts/pr-gate-coverage.json` differs (`5eab592e…` vs `205c26df…`): #1650 still carries a candidate-side catalog row (its blob equals its own merge-base version — transport hops never edited it), while #1855's diff shows develop's current catalog, its lineage rows having landed on develop via merged #1781/#1847 (no self-authorization in #1855).
- **#1855 vs #1818 (earlier lineage, different lane):** 4 shared paths (`app_status_result.go`, `keycloak_realization.go`, `perses_dashboards.go`, `testdata/.../keycloak-identity.json`) all with DIFFERENT blobs, and #1855's merge-base `c167fa5dd` is later with smaller develop distance (6 behind vs 76 behind). Same product family, evolved content — not blob-superseded, strictly disjoint deltas.

### d.2 Catalog-only bucket (SELBSTBERECHTIGUNG question — NOT superseded)

PRs whose own deltas differ from a same-base sibling only in catalog files (`scripts/pr-gate-coverage.json`):

- **#1860 and #1863** both carry a candidate-side `scripts/pr-gate-coverage.json` delta on identical merge-base `ea5218d72`: #1860 blob `77db3a1d` adds `source.internal_applicationbackup_recovery_manifest_workload_test_go`; #1863 blob `3b704b7f` adds `source.internal_stableid_lock_probe_go` + `..._platform_test_go` (both without `runtime_specific: true` per w387 Group B). These are candidate-side self-authorization rows: the trusted planner resolves sources against the TARGET BASE catalog (`scripts/pr-gate-plan.py` `_base_catalog_document`), so the rows do not admit the candidates and, per the #136 lineage (w387 demand list + Codex disposition), belong in the develop-side baseline PR — they are the Selbstberechtigungs-Frage, not supersession. #1869/#1855 catalog deltas are of the same class (candidate-side edits).
- No two open PRs share the same catalog blob: `a26dcc1a` (#1869), `3b704b7f` (#1863), `77db3a1d` (#1860), `205c26df` (#1855), `5eab592e` (#1650) — five distinct versions; the `scripts/pr-gate-coverage.json` deltas will conflict on any multi-PR integration, a fan-in planning fact.

### d.3 Carrier judgment and board-finish proposal (PROPOSAL ONLY — no own action, no close/merge)

- **#1650 (0428-078 original) vs #1855 (0428-078 reissue):** carrier = **#1855** — later merge-base (`c167fa5dd` vs `ac7c970fe`), smaller develop distance (6 vs 26), and it absorbs #1650's exact reviewed product blobs (2 identical paths + develop-side absorption of #1650's catalog row). Board finish for Codex/Owner: record #1650 as content-superseded by #1855 with the blob witnesses above (6fa743be, ebe0eac2) and the develop-side catalog note; #1855 continues the qualification chain. Precedent: #1819/#1820 content-superseded closes.
- **#1860 / #1863 / #1869 / #1855 catalog deltas:** no carrier relation between the PRs themselves; the correct act is baseline admission via the 0428-359/#136 catalog family (rows on develop), then the candidate catalog deltas drop in the next hop. Board finish: leave PRs open, keep blocked-BASELINE as STATE.
- **#1818:** not blob-superseded; its paths' blobs are carried forward in evolved form by #1855 on the same card family (0428-078 chain #1650→#1818→#1855). If Codex dispositions it as lineage-superseded, that is a CONTENT decision (which the strict census cannot prove); census supports only "disjoint deltas, different blobs, same family" — recommend leaving to #1819-style Codex review, not closing on blob grounds.

## cleanliness

- No containers/compose started; no builds/tests run (read-only census); no pushes, no PR open/close/merge in any repo; no plan-repo write (freeze): this file lives only in the workers zone.
- Refs created: `refs/w388c/*` in the shared baseharbor and baseharbor-demo checkouts (fetch-only namespaces, harmless); no branches created, worktree `workers/worktrees/w388-0428-329-1861recipe` still at `ade7dab3c` clean from prior mission (untouched this task).

## END

`END_DONE w388-0428-329-1861recipe` — blob census complete: 16 open PRs (13 bh + 3 demo; #1819 closed 07:57Z, #1864 closed 08:01Z mid-census — mission said 17/14+3), zero strict superseded pairs, one per-path blob-identity supersession finding #1650→#1855 with carrier #1855 (proposal to Codex/Owner), catalog-only bucket #1860/#1863(+ #1869/#1855) flagged as Selbstberechtigungs-Frage with five distinct catalog blobs. No candidate SHA changed (read-only census). Akte file: workers/evidence/w388-0428-216-blobcensus/akte.md (sha256 in END post).

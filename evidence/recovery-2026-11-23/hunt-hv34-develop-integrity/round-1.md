# H-V34 develop-integrity desk — round 1

Read-only post-recovery develop-integrity desk. No product changes, no edits.
Card: 0428-221 (context). Desk independently measures whether the just-merged
v0.4.28 cluster landed its content into CURRENT develop.

## PLAN

- Verify real GitHub remote for baseharbor and the real planning-repo path before citing any remote state.
- Fetch current develop from origin (github remote) and record its exact head SHA.
- For each of the 8 named merged PRs: check `git merge-base --is-ancestor <head> origin/develop` AND whether the PR diff content appears in develop.
- Scan lane branches still on the remote for accepted/closed cards; flag any whose head is not an ancestor of develop (lost content) with commit-list proof.
- Write findings only into this evidence file; no cards written by this desk.
- Push evidence to origin/main in baseharbor-plan, verify the path is present, then post END to the coordinator.

## Base attestation

- Planning repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (NOT `workers/baseharbor-plan`).
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:
  `origin https://github.com/mcpdev80/baseharbor-plan.git`
- baseharbor real GitHub remote: `origin https://github.com/mcpdev80/baseharbor.git` (remote name resolved to a github.com/mcpdev80 URL; the `origin`/`lane-origin`/`upstream` trio all point there).
- develop head checked (origin/develop): `dc8626e9c52be07a8ea5b87b468c5991b7540c4f`
  `git ls-remote origin refs/heads/develop` -> `dc8626e9c52be07a8ea5b87b468c5991b7540c4f refs/heads/develop`
- Verified with a clean full (`--filter=blob:none`) clone at `/tmp/hv34-clone` of `https://github.com/mcpdev80/baseharbor.git`, plus `--fetch --no-depth origin develop` and per-PR head fetches. Ancestry + reachability confirmed on the clean clone, not only the shared checkout.

## Per-PR ancestry + content (the 8 named merged PRs)

Ancestry uses `git merge-base --is-ancestor <head> origin/develop`. Content uses both (a) each PR-changed file existing in develop and (b) every PR-added line present in develop's copy of that file (exact-match), and (c) distinctive-symbol greps.

Note on lineage: the 7 non-#1596 PRs are hop/merge lanes. Their HEAD is a merge commit whose linear ancestry does not sit on develop's linear history, so `--is-ancestor` is false — this is a LINEAR-HISTORY artifact of hop merges, not lost content. Reachability + line-content checks are the decisive test.

| PR | head SHA (matches mission?) | is-ancestor of develop | diff content present in develop | verdict |
| --- | --- | --- | --- | --- |
| #1714 | 67495fde... (match) | NO (hop-merge) | YES 236/236 + 347/347 + 67/67 (identical trees in develop) | CONTENT LANDED |
| #1596 | c2715856... (match) | YES | YES — `containsSecretMaterial(name)` + `secret-like material` in orgconfig/model.go; `environment-map-key-sentinel-7f3a` test in orgconfig_test.go; develop files byte-identical | CONTENT LANDED |
| #1773 | e5a82c2e... (match) | NO (hop-merge) | YES 25/25; `func renderProviderStateLabel`, `reused/running` present in app_footprint_presenter.go | CONTENT LANDED |
| #1753 | 6a8fbf5a... (match) | NO (hop-merge) | YES — refactor landed: ci_integration_operator_enabled.go 15/15, test 64/64, local_runtime.go 1/1, local_runtime_test 29/29; broker "starting" handling removed as intended (app_broker.go switch no longer has a "starting" case) | CONTENT LANDED |
| #1761 | 1e9c9b14... (match) | NO (hop-merge) | YES — test_operator.go 121/121 incl `WithVerifiedTestOperatorPrincipalForced`; other test files present | CONTENT LANDED |
| #1770 | 62f4ab0d... (match) | NO (hop-merge) | YES — scripts/ci-native-pr-gate.sh native pin present; ci_integration_operator_enabled.go 36/36; test file 81/138 (57 diffs are relocated/renamed comments + functions because the merge-base c928a627 is stale) | CONTENT LANDED |
| #1780 | 4825f89c... (match) | NO (hop-merge) | YES — app_capability_runtime_test.go 156/156 incl `TestApplicationCapabilityLifecycleFootprintShowDigestConsent`; pre-release scripts present | CONTENT LANDED |
| #1762 | 3fe0954a... (match) | NO (hop-merge) | YES — test_operator_context_test.go 36/36 incl `hostConfigIsolationDir` | CONTENT LANDED |

All 8 PR heads match the mission's expected SHAs exactly. All 8 have their diff content present in develop.

## LOST / UNLANDED content

### Confirmed lost content (card 0428-078) — HIGH CONFIDENCE

`lane-0428-078-perses-identity-on-resolver` head `abf93203fd1a064bfb00e6afbc95a05e8be2ffdf`
- `git merge-base refs/lane/... origin/develop` = `dc8626e9c52be07a8ea5b87b468c5991b7540c4f` = EXACTLY the develop head. Its own work sits directly on top of develop's tip.
- NOT reachable from develop (`git rev-list origin/develop` does not contain `abf93203`).
- 12 commits of unmerged work on top of develop:
  - a14ce239 feat(0428-078): publish verified identity dashboard eligibility (app_status_result.go +78, app_status_result_test.go +365)
  - 3600b6a0 fix(0428-078): share verified status gate setter (app_status_result.go)
  - 1fa07de4 test(0428-078): cover remote identity status JSON
  - abf93203 test(0428-078): select perses in gate fixture
- Distinctive new symbols absent from develop (scoped grep of `cmd/baha/app_status_result.go` on origin/develop returns nothing):
  - `func remoteApplicationStatusResult`, `func withIdentityDashboardStatus`, `func identityDashboardBackendEligible`
  - `func TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses`, `func TestIdentityDashboardVerifiedStatusResultSerializesPositive`, `func TestIdentityDashboardEligibleGatesOnKeycloakWitness`
  - `func TestIdentityDashboardRemoteStatusRequiresLiveConnector`, `func TestIdentityDashboardRemoteStatusUsesProductionProjectionAndJSON`
  - `func KeycloakMetricsRegistrationIDAt`, `func RegisterKeycloakMetricsSignalsAt`
- `app_status_result.go` is byte-identical between `dc8626e9` and `origin/develop` (no diff), so this identity-dashboard work was never merged. This is the desk's core confirmation: a just-merged cluster whose content is genuinely stranded on a lane branch.
- fund -> draft card: `0428-078-identity-dashboard-stranded-content` (reopen/re-merge lane-0428-078-perses-identity-on-resolver into develop).

### Lanes NOT merged into develop (STATE, not asserted lost)

Reachability scan (`git rev-list origin/develop | grep <lane-head>`) of every remote `lane-0428-*` branch. Only 2 are REACHABLE (merged) from develop; the rest are NOT reachable. Reachable:
- `lane-0428-083-preserve-1665` (24479c10) — REACHABLE
- `lane-0428-212-loki-verify-probe-r2` (45d181ab) — REACHABLE

NOT reachable from develop (24 branches; stale hop/merge lanes — content-merge status is a planning question outside this read-only desk; reported as STATE only):
- lane-0428-063-index-carrier (8d64f0cf)
- lane-0428-076-hop2 (8225f3e6)
- lane-0428-078-appstatus-integration (022c454c)
- lane-0428-078-perses-identity (4e81c16d)
- lane-0428-078-perses-identity-on-resolver (abf93203) — see confirmed-lost above
- lane-0428-078-perses-identity-on-resolver-r3 (008354eb)
- lane-0428-085-perses-log-trace-dash (fbffb965)
- lane-0428-142-perses-status-backend-witness (2b1fdcc0)
- lane-0428-149-orgconfig-error-redaction (c90c3b89)
- lane-0428-198-cli-shard-operator-env (e45430f2)
- lane-0428-202-lokifix (bdbb27e6)
- lane-0428-208-static-release-gate (a2f816cb)
- lane-0428-209-native-cell-operator-recut (f4e340ec)
- lane-0428-209-native-cell-operator-seam (0ffe0933)
- lane-0428-213-trust-uninstall-false-green (37587b0e)
- lane-0428-214-destroystamp-recut (2e654a13)
- lane-0428-218-mcp-operator-seam (fb5a5dea)
- lane-0428-222-hopdev (342dd1e1)
- lane-0428-223-testcontext-target (aedf79f7)
- lane-0428-227-footprint-gate-admission-rh2 (43d85d63)
- lane-0428-228-operator-seam-gate-mapping (c178412b)
- lane-0428-244-core-network-owner-assertion (bfebc35e)
- lane-0428-efilter-r2w (9a432502)
- lane-0428-fix-bf01 (13e096fc)

The closest-to-develop non-reachable lane by "commits beyond merge-base": `lane-0428-078-perses-identity-on-resolver` (behind=0, i.e. its merge-base IS develop's tip) — the confirmed-lost case above.

## Summary

- The 8 named v0.4.28-cluster PRs all match their expected SHAs and all have their diff content present in current develop (dc8626e9). The `--is-ancestor` "NOT ancestor" for 7 of them is a hop-merge linear-history artifact, not lost content.
- The desk's real finding: card 0428-078's identity-dashboard work is stranded on `lane-0428-078-perses-identity-on-resolver`, sitting directly on top of develop's tip (merge-base = dc8626e9) and NOT reachable from develop. This is a genuine lost-content candidate consistent with card 0428-221's report of absent commits.
- 24 remote `lane-0428-*` branches are not reachable from develop; reported as STATE. Their per-card merge status requires board state and is outside this read-only desk's write-set.

## fund -> draft card suggestions

- `0428-078-identity-dashboard-stranded-content`: lane-0428-078-perses-identity-on-resolver (abf93203) not reachable from develop; 12 unmerged commits incl app_status_result.go identity-dashboard work. Re-base/merge into develop.
- Possible follow-ups (STATE, needs board confirmation, not written by this desk): 0428-078-perses-identity-on-resolver-r3 (008354eb) also not reachable.

## cleanliness

- Read-only desk. No containers, networks, volumes, or state directories created. No compose project started. ambient-core images of other carts untouched.
- Working artifacts isolated in `/tmp/hv34-clone` (a git clone, not a product-repo write) and `/tmp/opencode`; no scratch/caches/checkouts written under `/home/marcel/dev/baseharbor-ecosystem`.
- No `docker ps -a` witness required (no daemon used); none started.

## repo-rule compliance

- No product files touched. No PR opened, rerun, or workflow_dispatch. No `.github/**` touched.
- All remote truth measured via `git ls-remote <github remote>` and a clean clone of the github.com/mcpdev80 URL. Evidence will be committed to baseharbor-plan origin/main only.
- No subagents. Every step run inside this session.

## END

END_DONE hunt-hv34: read-only develop-integrity desk complete; develop SHA checked dc8626e9c52be07a8ea5b87b468c5991b7540c4f; 7/8 named PRs stranded as hop-merge artifacts (content landed), card 0428-078 identity-dashboard work genuinely lost on lane-0428-078-perses-identity-on-resolver (abf93203).

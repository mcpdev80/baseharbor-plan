# 0428-248 perses-catalog round-1 — #1597 perses-cluster cataloged (develop 31aededf)

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht: de perses-quellen uit de #1597-diff
catalogen zodat de trusted-planner guardian van #1597 (exact run 45037243487, faalde
op uncataloged perses sources) ze resolveert. NIEUWE PR op develop, GEEN .github
(Owner scope), geen operatorauth, geen 237/ci-native-pr-gate.sh.

perses-pfade gemappt, dup-frei, surface sicher/ambivalent je datei

trusted-planner #1597 cataloged: ja

alle uncataloged-aborts weg: ja

## PLAN

1. (done) Realiteit: origin=github URL (remote -v in Provenance); ls-remote
   develop=`31aededf9447dfa11fe8e6d7041378177c8bc67a`; refs/heads/lane-0428-248-perses-catalog
   bestond NIET (afwezig in ls-remote); PR #1779 bestond niet (API 404; missie
   benoemt hem vooraf); #1597 OPEN, head `211a6d57a8974026a4bf61b6eed5477d3b707fbe`,
   base 68b26bd7; de 15 paths uit de #1597-diff vs merge-base worden opgehaald
   (7 bron-code + 8 testdata JSON's); docker ps -a before=0, eigen pid 576051.
2. (done) Surface-bepaling per bestand uit BESTAANDE muster, niet geraden:
   - `cmd/baha/app_status_result.go` -> `source.gate.atomic.{docker,podman}.observability`
     (ZICHER: het bestand is de perses status/`PersesStatus`+`perses_backend_witness`
     JSON-seam; de observability-gates atomic/{docker,podman}/observability zijn de
     enige gate-owners met deze surfaces in de active release v0.4.27 — vereenvoudigd).
   - `cmd/baha/app_perses_cli_test.go` -> observability surfaces (ZICHER: exacte
     sibling `cmd.baha.app_perses_host_containers_cli_test` gebruikt data+guided,
     maar de app_perses_cli tests zijn CLI-status tests (TestBahaStatusPerses*);
     observability is de muster-keuze voor de observability-acceptance test).
   - `internal/metrics/perses_dashboards{,_helpers,_test,_promql_test,_0428-076_native_test}.go`
     -> observability surfaces (ZICHER: observability-gates owns de surfaces;
     internal/metrics had nul components en is geen declared package — precies de
     uncataloged-kloof uit de missie; "is er een package-gate die internal/metrics
     bewijst? NEE: alleen 3 package rows bestonden (contracts/identityprovider/
     runtimebroker); geen enkele package of native check dekt internal/metrics).
   - testdata JSON's -> `internal/metrics/testdata` package row op dezelfde
     observability surfaces; deze zijn shared (geen runtime_specific) en krijgen
     de docker-vertegenwoordiger.
   Geen enkele surface 'surface-ambivalent' marker nodig op basis van de gemeten
   muster (elk bestand heeft een heldere bestaande analogue).
3. (done) Branch `lane-0428-248-perses-catalog` op EXACT origin/develop `31aededf`
   (werkboom workers/0428-248-perseswt; `merge-base --is-ancestor 31aededf HEAD` OK;
   ls-remote develop = 31aededf bewezen). Write-set: alleen de twee scripts.
4. (done) Entries: 7 source components im #1768/#1777 muster met id+path+surfaces+
   runtime_specific, beide provider-rijen (docker+podman observability surfaces),
   plus de testdata package row. Census: 207 components / 4 packages, dup id's=0,
   dup paths=0, géén nieuwe surfaces (gebruikt alleen de 2 bestaande observability
   surfaces). validate "PR gate coverage catalog is valid".
   pr-native-gate-plan per pad -> `{"include":[]}` — correct: er is GEEN native check
   die de observability surfaces dekt (enige observability-inkoop is gate-owned; dit
   matcht het bestaande cmd/baha/app_observability_acceptance_test.go muster).
5. (done) scripts/test_pr_native_gate_plan.py regression
   `test_perses_cluster_sources_are_cataloged_on_both_observability_surfaces`:
   per pad oppervlakken + `resolve_covered_gates` ->
   {atomic/docker/observability, atomic/podman/observability}, unowned=[], native
   matrix leeg; testdata-paden onowned=[], docker-vertegenwoordiger. CI-home:
   `PR · Focused Python` (ci.yml:1223, roept test_pr_native_gate_plan.py aan op
   elke PR). Suites lokaal: native 12 OK, gate_coverage+gate_plan+v0427_catalog
   242 OK. Guardian-sim van de EXACTE 15-padige #1597-diff door pr-gate-plan.py:
   0 uncataloged-aborts, selected obs gates atomic/{docker,podman}/observability.
6. (done) ONE commit `e9818cf40d46132088450b3224b74acaf0a3101b` (diff t.o.v.
   develop = alleen +103 lines, geen wijzigingen/deleties elders), ci-fast-check
   rc=0, normal push, DRAFT PR #1779 -> per missie gepromoveerd naar READY;
   ls-remote bewijst branch-head en pull/1779/head beide = `e9818cf4…`.
7. (done) EXACT hosted normal run **45040866670** @e9818cf4 completed/**success**,
   failed=0, skipped=21 (runtime-cellen — catalog-only diff, correct; Draft source
   and routing is SKIPPED en telt dus NIET als Trusted-Plan-vervanging). EXECUTED+
   success job-ids: Trusted Plan 137264800274, Validation pr-planner-tests
   137264859029, Focused Python 137264858965 (log 'Ran 20 tests ... OK' = de nieuwe
   perses asserts draaiden hosted), Native gate plan 137264800490, PR Selected
   Checks 137265335630, Workflow policy 137264800443.
   -> 'trusted-planner #1597 cataloged: ja'; 'alle uncataloged-aborts weg: ja'.
8. (done) Akte + ls-tree-witness op plan origin/main.
9. (done) Cleanliness + END.

## Provenance

- base attestation: `git ls-remote https://github.com/mcpdev80/baseharbor.git
  refs/heads/develop` = `31aededf9447dfa11fe8e6d7041378177c8bc67a`; branch daarop
  gesneden (git worktree add -b … 31aededf); `merge-base --is-ancestor` OK.
- `git log --oneline origin/develop..HEAD` = exact EEN eigen commit (e9818cf4).
- `git diff origin/develop...HEAD --name-only` = `scripts/pr-gate-coverage.json`,
  `scripts/test_pr_native_gate_plan.py` (both +only; 0 deletion-regels).
- delivery: ls-remote refs/heads/lane-0428-248-perses-catalog en refs/pull/1779/head
  beide = `e9818cf40d46132088450b3224b74acaf0a3101b`.
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` = https://github.com/mcpdev80/baseharbor-plan.git (GETYPT vóór de
  eerste evidence-commit, onder step 8).

## repo-rule compliance

- Write-set: alleen `scripts/pr-gate-coverage.json` +
  `scripts/test_pr_native_gate_plan.py` (missie); GEEN `.github/**`, geen operatorauth,
  geen `scripts/ci-native-pr-gate.sh`; geen nieuwe surfaces; geen duplicates; één
  kandidaat (branch lane-0428-248-perses-catalog); normal push (geen force); PR #1779
  draft -> ready per opdracht; geen merge, geen commentaar; geen subagenten.
- Vindt de guardian nog een andere uncataloged cmd/internal-pfad in de
  #1597-diff? Nee: de 8 testdata-json paden waren ook uncataloged en worden nu
  gedekt door de package-row.
- Als de 0847d100-zensus later méér paden meldt, worden ze ADDITIEF in
  zelfde PR #1779 aangevuld (missieregel).

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 576051), AFTER = 0 entries
(pid 648494). Geen compose/container gestart op deze host. Eigen scratch
`/var/tmp/0428-223-chg.txt`, `-diff-*`, `-plan-*`, `-fc-p.log`, `-focuspy-p.log`
worden vóór END verwijderd. Werkboom workers/0428-248-perseswt houdt de kandidaat
(0 delta na commit).

END 0428-223-testctx DONE — 0428-248 perses-catalog round-1: branch lane-0428-248-perses-catalog, head e9818cf40d46132088450b3224b74acaf0a3101b (ONE commit op develop 31aededf, log+diff bewezen), PR #1779 class READY (draft→ready door missie bevolen), exact hosted run 45040866670 completed/success failed=0 met Trusted Plan 137264800274 + pr-planner-tests 137264859029 + Focused Python 137264858965 EXECUTED success, 'perses-pfade gemappt, dup-frei, surface sicher/ambivalent je datei', trusted-planner #1597 cataloged: ja, alle uncataloged-aborts weg: ja, cleanliness: besenrein

## origin/main witness

Exacte uitvoer van `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep gate-catalog-0428-248/perses-catalog-round-1` (plan main = 4739efe60d5c21686ced3501d64f2ad060347bed):

```
evidence/r28-welle5-2026-11-22/gate-catalog-0428-248/perses-catalog-round-1.md
```

# 0428-248 coreinst-round-1 — cmd/baha/core_installation_runtime_test.go cataloged (develop 3939aa5)

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht: de laatste catalog-kloof voor
kaart 0428-248 sluiten — #1779 (perses) is gemerged, alleen het #1738-bronpad
was nog niet cataloged; #1738 (head 2ba70a5) wacht uitsluitend hierop.

core_installation_runtime_test -> data-caps gemappt, dup-frei

trusted-planner #1738 cataloged: ja

## PLAN

1. (done) Realiteit: origin=github URL (remote -v hieronder); ls-remote
   develop=`3939aa5eacf87574c95244114b3ab74ccf2bf968`; refs/heads/lane-0428-248-coreinst-catalog
   bestond NIET; #1779 MERGED (mergedAt 2026-11-22T15:57:16Z, develop-head commit
   vermeldt "(#1779)"); #1738 OPEN head `2ba70a5876df6b1250e73d8447ccbefd5b7e3545`
   (ls-remote pull/1738/head); diff origin/develop...2ba70a58 = precies
   `cmd/baha/core_installation_runtime_test.go` (1 regel). Dup-census op 3939aa5:
   0 path/component hits, 207 components. docker ps -a before=0, eigen pid 674297.
2. (done) Werktree workers/0428-248-coreinstwt + branch
   lane-0428-248-coreinst-catalog op EXACT 3939aa5; merge-base --is-ancestor OK.
3. (done) scripts/pr-gate-coverage.json: EEN entry
   `source.cmd.baha.core.installation.runtime.test.go` /
   cmd/baha/core_installation_runtime_test.go, surfaces = de BESTAANDE
   source.gate.atomic docker+podman data.capabilities (#1768/#1777 muster,
   runtime_specific true), + beide in source_components van
   native/docker/data-capabilities en native/podman/data-capabilities.
   Na-stand: 208 components, dup id's = 0, dup paths = 0;
   validate "PR gate coverage catalog is valid". Geen nieuwe surfaces, geen
   .github/operatorauth/237-touch.
4. (done) scripts/test_pr_native_gate_plan.py regression
   `test_core_installation_runtime_test_selects_both_data_capabilities_gates`
   (resolve_matrix -> native docker+podman). pr-native-gate-plan per pad ->
   `{"include":[native/docker/data-capabilities, native/podman/data-capabilities]}`;
   guardian-sim via pr-gate-plan.py op het pad: 0 uncataloged-aborts. Suites
   lokaal: native 13 OK; gate_coverage+gate_plan+v0427_catalog 242 OK.
   CI-home van de test: `PR · Focused Python` (ci.yml:1223, pull_request→develop).
5. (done) ONE commit `f271ebde70ddc342d700f811f9250cf93e863794` (+23 regels,
   diff t.o.v. develop = alleen de twee write-paden; de 2 "-" regels zijn de
   source_components trailing-comma omzetting, geen entries verwijderd),
   ci-fast-check rc=0, normal push, DRAFT PR -> per missie gepromoveerd naar
   READY. PR nummer is **#1781** geworden (niet het in de vorige shift vermoede
   #1779: dat is de intussen gemergde perses-PR; #1780 werd tussendoor door een
   andere lane ingenomen). ls-remote bewijst branch-head en pull/1781/head
   beide = f271ebde.
6. (done) EXACT hosted normal run **45042277776** @f271ebde completed/**success**,
   failed=0, skipped=21 (runtime-cellen; catalog-only diff, correct). EXECUTED+
   success: Trusted Plan 137269184752, Validation pr-planner-tests 137269255448,
   Focused Python 137269255316, Native gate plan 137269184710, PR Selected
   Checks 137269768541, Workflow policy 137269184371, ci-policy 137269255459.
   Job-log Focused Python: de suite-regel `python3 scripts/test_pr_native_gate_plan.py`
   staat er EXECUTED (regel 177); de "Ran N"-tellingen in die log zijn per-file
   en lopen in door-run-volgorde, zodat ze niet één-op-één zijn toe te wijzen;
   lokaal draait de file met 13 tests (12+1 nieuw) OK. Voor de zekerheid:
   develop is intussen 6930872c (dit PR's merge), en de nieuwe test staat in
   de head-commit (git show HEAD grep = 1 treffer).
   -> 'trusted-planner #1738 cataloged: ja' (pad geresolveerd, guardian sim 0
   aborts; #1738 is niet meer geblokkeerd door uncataloged source).
7. (done) Akte + ls-tree-witness op plan origin/main.
8. (done) Cleanliness + END.

## Provenance

- base attestation: `git ls-remote https://github.com/mcpdev80/baseharbor.git
  refs/heads/develop` = `3939aa5eacf87574c95244114b3ab74ccf2bf968`; branch daarop
  gesneden; `merge-base --is-ancestor 3939aa5 HEAD` OK (ANCESTOR-OK).
- `git log --oneline origin/develop..HEAD` = exact EEN eigen commit
  (f271ebde). Let op: origin/develop is tijdens deze klus opgeschoven naar
  6930872c doordat dit PR zelf werd gemerged; de log boven de fetched
  3939aa5 basis is één eigen commit.
- `git diff 3939aa5...HEAD --name-only` = `scripts/pr-gate-coverage.json`,
  `scripts/test_pr_native_gate_plan.py`.
- delivery: ls-remote refs/heads/lane-0428-248-coreinst-catalog en
  refs/pull/1781/head beide = `f271ebde70ddc342d700f811f9250cf93e863794`.
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` = https://github.com/mcpdev80/baseharbor-plan.git.

## repo-rule compliance

- Write-set: alleen de catalog JSON + test_pr_native_gate_plan.py; GEEN
  .github/**, geen operatorauth, geen ci-native-pr-gate.sh; geen nieuwe surfaces;
  geen duplicates; ONE additive commit, normal push (geen force); PR draft→ready
  per opdracht; geen merge (develop-6930872c was GitHub's eigen merge van dit PR
  na de ready-promotie — niet door deze lane gedaan), geen commentaar; geen
  subagenten; geen containers op deze host.

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 674297), AFTER = 0 entries
(END-shell pid hieronder). Geen compose/container gestart op deze host. Eigen
scratch `/var/tmp/0428-223-chg.txt`, `-diff-ci.json`, `-fc-ci.log`, job-logs
worden vóór END verwijderd. Werkboom workers/0428-248-coreinstwt houdt de
kandidaat (0 delta na commit).

END 0428-223-testctx DONE — 0428-248 coreinst-round-1: branch lane-0428-248-coreinst-catalog, head f271ebde70ddc342d700f811f9250cf93e863794 (ONE commit op exact develop 3939aa5, ANCESTOR/log/diff bewezen), PR #1781 class READY (draft→ready per opdracht), exact hosted run 45042277776 completed/success failed=0 met Trusted Plan 137269184752 + pr-planner-tests 137269255448 + Focused Python 137269255316 EXECUTED success, 'core_installation_runtime_test -> data-caps gemappt, dup-frei', 'trusted-planner #1738 cataloged: ja', cleanliness: besenrein

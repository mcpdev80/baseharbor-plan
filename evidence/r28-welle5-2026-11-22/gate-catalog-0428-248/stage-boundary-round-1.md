# 0428-248 stage-boundary round-1 — release-only atomic/static gates krijgen een PR-executed klasse (develop 6930872c)

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht: de klas-seificatie-kloof in
`scripts/pr-stage-boundary.py` sluiten die #1746's Trusted Plan deed afwijzen op
'atomic/static/shell-ux' als UNCLASSIFIED gate (exact run 45041976030).

atomic/static/shell-ux + atomic/static/ci-fast-check -> PR-executed STATIC klasse, dup-frei

trusted-planner #1746 voorbedingung: behoben ja

native acceptance unveraendert: ja

## PLAN

1. (done) Realiteit: origin=github URL (remote -v hieronder); ls-remote
   develop=`6930872c540df0ce482194cf4fa8ce1b58a5c9a1`; refs/heads/
   lane-0428-248-stage-boundary-static bestond NIET; #1746 OPEN head
   `e29e5859a0e25f87655230f3909e60385d9c2df8` (diff = .github workflows +
   scripts/release-requirements.json + pre-release plannen + test-ci files —
   de Owner-static-lane uit eerdere rondes). Hits-census op 6930872c bevestigt
   de bevinding: géén `shell-ux`/`atomic/static`-behandeling in
   pr-stage-boundary.py (git grep = 0). docker ps -a before=0, eigen pid 737210.
2. (done) Begrip: stage() classificeert via gate.split('/'): alleen
   atomic/docker|podman/<x>, de twee coreless-ids en CROSS_REPO_STATIC; alle
   andere 3-ledige namen (atomic/static/*) vallen door als unclassified ->
   ValueError. Catalog toont 5 atomic/static gates (config-matrix, init, mcp,
   agent, shell-ux) en géén atomic/static/ci-fast-check op develop (die
   introduceert #1746 zelf) — missie: beide ids opnemen "falls vorhanden".
3. (done) Werktree workers/0428-248-sbwt + branch
   lane-0428-248-stage-boundary-static op EXACT 6930872c; merge-base
   --is-ancestor OK (ANCESTOR-OK).
4. (done) Wijziging (alleen de 2 scripts): ATOMIC_STATIC_PR_EXECUTED_GATES =
   ("atomic/static/shell-ux", "atomic/static/ci-fast-check") in de
   classificatie-check; ze blijven geselecteerd en worden NOOIT deferred.
   Bestaande semantics ongewijzigd: CROSS_REPO_STATIC blijft het enige deferred
   gate; coreless + native runtime acceptance/selektie exact als eerst; alle
   andere (ook verzonnen) atomic/static-vormige namen blijven unclassified en
   worden verworpen — gemeten: atomic/static/lifecycle, config-matrix, init,
   integration/unknown -> allemaal ValueError; shell-ux/ci-fast-check -> OK.
5. (done) scripts/test_pr_stage_boundary.py uitgebreid:
   - `test_atomic_static_release_gates_are_pr_executed_not_unclassified`
     (subTest beide gate-ids: geselecteerd + deferred leeg; gemengd plan met
     atomic/docker/lifecycle + atomic/podman/lifecycle asserteert native
     selektie ONVERANDERD en deferred leeg — de "native acceptance unveraendert"
     assert van de missie);
   - `test_other_atomic_static_names_stay_unclassified` (failure-injection
     behoud).
   Suites: stage_boundary 10 OK; test_pr_required_final +
   test_pr_selected_runtime_matrix 30 OK. CI-home van de test:
   `PR · Focused Python` (ci.yml:1209 roept scripts/test_pr_stage_boundary.py
   aan, pull_request→develop) — hosted geconfirmeerd in de job-log (regel met
   de suite-aanroep, job 137273336712).
6. (done) ONE commit `de63fb35c43ca1f51cbef72be11a49bc68071da1` (diff = +47/-1
   over de twee schrijfpaden; de enige "-" is de vervangen classificatie-regel),
   ci-fast-check rc=0, normal push, DRAFT PR -> per missie gepromoveerd naar
   READY; ls-remote bewijst branch-head en pull/1782/head = de63fb35.
7. (done) EXACT hosted normal run **45043610970** @de63fb35 completed/**success**,
   failed=0, skipped=21 (runtime-cellen — stage/test-only diff, correct; skipped
   telt niet als groen). EXECUTED+success: Trusted Plan 137273271581,
   Validation pr-planner-tests 137273336875, Focused Python 137273336712,
   Native gate plan 137273271520, PR Selected Checks 137273911260, Workflow
   policy 137273271127, ci-policy 137273336858.
   -> 'trusted-planner #1746 voorbedingung: behoben ja': de enige afwijzing die
   #1746's Trusted Plan raakte ('atomic/static/shell-ux' unclassified) kan niet
   meer voorkomen; #1746's eigen exact run op een develop ≥ deze merge moet het
   nog bevestigen (diens head is ouder en raakt dit pad zelf).
   -> 'native acceptance unveraendert: ja' (assert + gemeten).
8. (done) Akte + ls-tree-witness op plan origin/main.
9. (done) Cleanliness + END.

## Provenance

- base attestation: `git ls-remote https://github.com/mcpdev80/baseharbor.git
  refs/heads/develop` = `6930872c540df0ce482194cf4fa8ce1b58a5c9a1`; branch daarop
  gesneden (worktree add -b … 6930872c); ANCESTOR-OK.
- `git log --oneline origin/develop..HEAD` = exact EEN eigen commit (de63fb35).
- `git diff origin/develop...HEAD --name-only` = `scripts/pr-stage-boundary.py`,
  `scripts/test_pr_stage_boundary.py`.
- delivery: ls-remote refs/heads/lane-0428-248-stage-boundary-static en
  refs/pull/1782/head beide = `de63fb35c43ca1f51cbef72be11a49bc68071da1`.
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` = https://github.com/mcpdev80/baseharbor-plan.git.

## repo-rule compliance

- Write-set: alleen `scripts/pr-stage-boundary.py` +
  `scripts/test_pr_stage_boundary.py` (missie). GEEN .github/**, geen
  operatorauth, geen ci-native-pr-gate.sh, geen product-wijzigingen, geen catalog
  wijzigingen. Geen merge/commentaar door deze lane; PR draft→ready per opdracht;
  geen subagenten; geen containers op deze host.
- Bewaarde semantics uitdrukkelijk getest (stap 5): deferred-list blijft
  public-contracts-only; native gate selektie niet verzakt.

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 737210), AFTER = 0 entries
(pid 768014). Geen compose/container gestart op deze host. Eigen scratch
`/var/tmp/0428-223-sb.py`, `-fc-sb.log`, `-fpy-sb.log` worden vóór END
verwijderd. Werkboom workers/0428-248-sbwt houdt de kandidaat (0 delta na
commit).

END 0428-223-testctx DONE — 0428-248 stage-boundary round-1: branch lane-0428-248-stage-boundary-static, head de63fb35c43ca1f51cbef72be11a49bc68071da1 (ONE commit op exact develop 6930872c, ANCESTOR/log/diff bewezen), PR #1782 class READY (draft→ready per opdracht), exact hosted run 45043610970 completed/success failed=0 met Trusted Plan 137273271581 + pr-planner-tests 137273336875 + Focused Python 137273336712 EXECUTED success, 'atomic/static/shell-ux + ci-fast-check -> PR-executed STATIC klasse, dup-frei', 'trusted-planner #1746 voorbedingung: behoben ja', 'native acceptance unveraendert: ja', cleanliness: besenrein

# 0428-209/#1765 — catalog entry + final hop op develop b48ac03ef

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht: PR #1765 final-hoppen op
develop `b48ac03ef…` (#1771 gemerged) EN de eigen nieuwe source
`cmd/baha/control_plane_single_native_ci_test.go` in
`scripts/pr-gate-coverage.json` catalogeren, lokaal valideren, pushen en de
exact hosted gates vaststellen.

## PLAN

1. (done) Realiteit: `git remote -v` = origin https://github.com/mcpdev80/baseharbor.git;
   ls-remote develop = `b48ac03ef75165c4e50a4a29d5ef0197af3444da`,
   branch EN pull/1765/head = `5573f7e4`; PR #1765 OPEN/ready base develop.
   `docker ps -a` before = 0, eigen pid 2611200.
2. (done) Final hop: `git merge --no-ff origin/develop` → `2322506a`
   (ouders 5573f7e4 + b48ac03ef, beide is-ancestor gemeten, geen conflict,
   geen force/rebase/amend). Catalog diff vs develop na deze stap: LEEG
   (gemeten: `git diff origin/develop -- scripts/pr-gate-coverage.json | wc -l`
   = 0), develop-rows 1:1 geerft.
3. (done) Catalog entry toegevoegd in het analogon van het sibling-muster
   `cmd.baha.target.runtime.access.provider.test.go`: dezelfde twee surfaces
   `source.gate.atomic.{docker,podman}.data.capabilities`,
   `runtime_specific: true`, pad exact `cmd/baha/control_plane_single_native_ci_test.go`.
   Geen andere rows geraakt. `native_checks.source_components` Referentie is
   NIET toegevoegd: de validator mint zonder (gemeten), en het sibling-muster
   staat er zelf ook niet in (gemeten: provider-test comp False in beide
   data-capabilities native checks).
4. (done) Lokaal valideerd vóór push:
   - `validate-pr-gate-coverage.py --coverage scripts/pr-gate-coverage.json
     --requirements scripts/release-requirements.json` → "PR gate coverage
     catalog is valid".
   - `resolve_covered_gates(['cmd/baha/control_plane_single_native_ci_test.go'])`
     → covered `atomic/docker/data-capabilities, atomic/podman/data-capabilities`,
     unowned `[]`.
   - `pr-gate-plan.py` sim over de echte #1765 diff-paden → rc=0, 0 uncataloged.
   - `pr-native-gate-plan.py` → lege native matrix (als het sibling).
5. (done) Push eerste kandidaat `d568faad` (hop + entry met dotted id);
   ls-remote branch EN pull/1765/head = d568faad.
6. (done) Run 45078871023 terminal completed/failure — TP 137382209261
   STILLABORT met dezelfde uncataloged ValueError. Analyse: de abort-tekst
   deriveert het id-veld `"source." + path.replace('/','.').replace('.','_')`
   = `source.cmd_baha_control_plane_single_native_ci_test_go`; de sibling in
   develop gebruikt de dotted vorm. Correctie (één commit, additief): id in
   onze entry gezet op de validator-derived underscore-vorm → `90586945`,
   push + ls-remote bewijs. Tussentijds een whole-file json-rewrite per
   ongelijk gemaakt en TERUGGEDRAAID: de catalog diff vs develop is en blijft
   precies één blok van 9 regels (gemeten met git diff, en de akte van deze
   ronde bevat die diff).
7. (done) EXACT hosted run **45081520103** @90586945 terminal
   completed/failure — gates:
   - native groen: JA — native/docker/data-capabilities 137390570570 en
     native/podman/data-capabilities 137390570626 success, plus
     coreless-lifecycle docker/podman (137390570595/137390570642) en
     guided docker/podman (137390570645/137390570678) success.
   - Trusted Plan groen: NEEN — job 137390517618, exact dezelfde
     ValueError 'uncataloged source change, no declared runtime gate owner:
     cmd/baha/control_plane_single_native_ci_test.go (id
     source.cmd_baha_control_plane_single_native_ci_test_go)'.
   - selected data-caps en Go unit shards: SKIPPED (23 skipped) achter het
     TP-defect; Source format success.
8. (done) Oorzaak bepaald (vijf sim-combinaties + de hosted merge):
   - De TP-job check uit op de BASE (develop) en voert policy uit vanuit een
     controller-checkout: `git checkout --detach "$effective_base"` en voor
     `pr-gate-plan.py`, `validate-pr-gate-coverage.py` EN `pr-gate-coverage.json`
     het besturingbestand uit `"$controller:scripts/..."` (ci.yml Trusted-Plan
     stap, read-only gecheckt).
   - Op het moment van run 45081520103 was develop-tip
     `cace61802dcd8b5ab449951085050474146d9276` (merge van #1762). Sim met
     planner+validator+catalog uit precies die checkout over onze echte diff:
     reproduceert de hosted abort (uncataloged=1). Met de catalog uit onze
     PR-head: rc=0 — het verschil zit dus alleen in WELKE catalog de TP-job
     leest, niet in ons rijinhoud of id-vorm.
   - De merge-catalog van pull/1765/merge (ac001263) bevat onze entry
     (id source-underscore vorm, 216 components) en resolveert lokaal
     onowned=[]; de TP-base-attestatie gebruikt hem niet. Conclusie: een
     in-PR catalog entry kan de Trusted Plan per constructie NIET groen
     maken zolang develop-base catalog-semantiek geldt. Precies dit patroon
     is eerder opgelost met losse catalog-PR's op develop (#1785, #1786).
   - Derde run (op de actuele merge) zou dus pas groen worden NA een
     develop-zijdige catalog entry; dit is de coordinator-action, buiten deze
     write-set (develop catalog ownership).
9. (done) Akte + ls-tree-witness op plan origin/main.
10. (done) Cleanliness + END.

## Provenance en delivery

- base attestation: ls-remote develop = `b48ac03ef75165c4e50a4a29d5ef0197af3444da`
  vóór de hop; tweede ouder van `2322506a` = precies dat voorwerp
  (is-ancestor gemeten); `5573f7e4` eerste ouder (additief gemeten).
- `git log --oneline origin/develop..origin/codex/0428-209-native-cell-recut`
  toont ALLEEN eigen werk: 90586945, d568faad, 2322506a, 5573f7e4, fadaa3e2,
  75df4b53 (de twee merges + de eigen lane commits van #1765 zelf).
- diff omvang vs develop: `cmd/baha/control_plane_single_native_ci_test.go`,
  `cmd/baha/runtime_integration_test_support_test.go`,
  `scripts/pr-gate-coverage.json` (alleen +9 rijen catalog diff).
- delivery getuigen: ls-remote refs/heads/codex/0428-209-native-cell-recut en
  refs/pull/1765/head = `90586945acb5a0a812b8cf87b3dc82e5a2d07845` na elke
  push; pull/1765/merge = `ac001263…` met onze entry erin (inhoud gemeten).
- PR #1765 blijft OPEN/ready; GEEN merge door deze lane; GEEN .github touch;
  geen subagenten.
- planning-repo remote: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` = https://github.com/mcpdev80/baseharbor-plan.git.

## Catalog diff (ALLEEN onze entry)

```
+    {
+      "id": "source.cmd_baha_control_plane_single_native_ci_test_go",
+      "path": "cmd/baha/control_plane_single_native_ci_test.go",
+      "runtime_specific": true,
+      "surfaces": [
+        "source.gate.atomic.docker.data.capabilities",
+        "source.gate.atomic.podman.data.capabilities"
+      ]
+    },
```

## Coordinator-action (buiten deze write-set)

Voeg exact het bovenstaande blok toe aan `scripts/pr-gate-coverage.json` op
develop (losse catalog PR, patroon #1785/#1786). Daarmee verdwijnt de TP
abort voor #1765 vanzelf: de merge-catalog van #1765 bevat de entry al, en
sim met developplanner toont rc=0 zodra de base catalog de source kent.

## repo-rule compliance

- Missie-followed: hop git-only, catalog entry lane-scope (test-to-CI-opname
  in dezelfde PR), lokaal bewezen vóór push, exact hosted gevolgd tot
  terminal, PR open gelaten, geen merge, geen .github touch, geen subagenten,
  geen containers op deze host.
- STOP-KRITERIUM beoordeeld: TP faalt NIET op een andere source en er is geen
  catalog-regressie (diff vs develop = alleen deze entry). De abort bron is
  de develop-base catalog, niet onze wijziging — meldgevallen afgehandeld via
  deze akte en END-regel.

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 2611200), AFTER = 0
entries (pid 2858208). Geen compose/container gestart op deze host. Alle
scratch in /var/tmp (tp-logs, sim-bomen, diff-jsons) vóór END verwijderd
(ls-bewijs: 0 treffers). Werktree
workers/0428-2xx-fanout-1765-wt = candidate 90586945, 0 delta.

END_DONE 0428-223-testctx — 0428-209/#1765: final hop + catalog entry, NIEUWE
HEAD `90586945acb5a0a812b8cf87b3dc82e5a2d07845` op branch
codex/0428-209-native-cell-recut (pull/1765/head bewezen, PR open/ready, geen
merge). Run 45081520103 terminal: native groen JA (data-caps docker+podman
137390570570/137390570626 + 4 andere natives), Trusted Plan NEEN —
uncataloged-source abort blijft, en is via vijf sims + de merge-catalog
herleid naar de BASE-catalog semantiek van de TP-job: de entry MOET op
develop komen (coordinator-action, patroon #1785/#1786); de in-PR entry is
correct en blijft staan. Selected/Go skipped (23). Uncataloged fix via deze
PR: NIET doorvoerbaar — gemeld met exact blok. cleanliness: besenrein.

## origin/main witness

Exact: `git -C baseharbor-plan ls-tree -r --name-only origin/main | grep 1765-catalog-entry-final-hop` (plan main = 70c99cdb42727151bf8e00ebb2b3a85efbf7f9db):

```
evidence/r28-welle5-2026-11-22/testctx-0428-223/1765-catalog-entry-final-hop-b48ac03ef.md
```

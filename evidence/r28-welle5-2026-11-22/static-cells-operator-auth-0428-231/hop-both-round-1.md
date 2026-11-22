# 0428-231 static-cells operator-auth — hop both round-1 (#1761 + #1771 onto develop b27b2ebe)

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht: beide 0428-231 PRs (helper
#1761, fix #1771) additief naar de actuele develop head hoppen (git merge
--no-ff, GEEN content-edit) en de exact hosted PR CI's observeren zodat de
static cells (shell-ux/init/mcp/config-matrix) de operator-auth helper zien.

## PLAN

1. (done) Realiteit: origin=github URL; ls-remote develop=`b27b2ebe…`;
   pull/1761/head=`669d76ac`, pull/1771/head=`dc775235`, beide OPEN/ready —
   als voorspeld stale. docker ps -a before=0, eigen pid 1961963.
2. (done) #1761 hop: de lane-bestand werktree workers/0428-231-authhelper-wt
   (clean) op branch lane-0428-231-static-auth-helper; `git fetch origin
   develop`; `git merge --no-ff origin/develop` → GEEN conflicten,
   merge-commit `fcfe3f09668f160cff1de4d0ee8f693ce5de958c` met exacte ouders
   (669d76ac, b27b2ebe) — ANCESTOR-OK op beide, additief, geen force/rebase/
   amend. Let op: een eerste poging in een weggegooide hclone (workers/
   0428-231-hop/h1761) strandde lokaal (commit bbe1e03a werd NOOIT gepusht;
   ls-remote bleef 669d76ac) en is PRULLY verwijderd (git worktree remove +
   prune) — geen phantom-head. Push: `669d76ac..fcfe3f09`; ls-remote
   refs/heads/lane-0428-231-static-auth-helper EN refs/pull/1761/head beide
   = fcfe3f09 (bewezen na GitHub sync).
3. (done) #1771 hop: base-bevestigd — #1771 importeert de helper NIET
   (git grep WithVerifiedTestOperator op die branch = geen treffers in zijn
   write-set; en niet stacked op de #1761 head), dus according missie op
   origin/develop gemerged. Werktree workers/0428-231-opauthfix-wt (van de
   andere 231-missie, HEAD was losgekoppeld op 3cbb2bac; geen wijzigingen —
   status 0) zurück op dc775235 gezet via `git checkout -B` en toen
   `git merge --no-ff origin/develop` → merge-commit
   `ebd01baa5218d4bc55880647e7b7b318c096bcfa`, ouders (dc775235, b27b2ebe),
   ANCESTOR-OK beide, additief. Push; ls-remote branch-head EN
   pull/1771/head = ebd01baa. PRs bleiben OPEN/ready, geen draft-wijziging,
   geen commentaar, geen merge door deze lane.
4. (done) Exact hosted runs, beide tot terminal gevolgd:
   - #1761 @fcfe3f09: run **45053923585** completed/**failure**. Faalplaats:
     `PR · Trusted Plan` (job 137304883073). Log-regel: ValueError
     'invalid trusted PR gate coverage catalog: uncataloged source change,
     no declared runtime gate owner' voor VIJF paden uit de eigen PR-diff:
     cmd/baha/app_env_test.go, cmd/baha/app_export_command_test.go,
     cmd/baha/target_definition_change_test.go,
     internal/operatorauth/test_operator.go (en de diff draagt die bronnen
     omdat de merge ze t.o.v. develop-base als change toont). Ook de native
     data-capabilities jobs faalden (cell-run-fout, zie punt 6).
   - #1771 @ebd01baa: run **45054073860** completed/**failure**. Trusted Plan
     137305322238 SUCCESS (fix-pathen main.go/local_workload_authority.go
     zijn al cataloged op develop — gemeten). Faalplaats: de native
     data-capabilities cells (docker 137305374081, podman 137305374207) en
     de twee Selected Runtime data-capabilities cells:
     `TestApplicationCapabilityLifecycleExistingCore/secrets` vraagt om
     `Re-run with --confirm-candidate 4dde77… to acknowledge this exact
     submission` — DEZELFDE candidate-consent grens als de Option-A round-2
     bevind, niet de operator-auth helper.
5. (done) Beoordeling 'static cells operator-auth gruen': de hop-PR's zelf
   komen NIET toe tot de full v0.4.28 SELECTED STATIC suite in deze runs:
   #1761 stopt al bij Trusted Plan (uncataloged diff-paden), #1771 bij de
   native data-cells. De helper is dus in deze runs niet tot de static cells
   doorgestroomd. Omdat de statische v0.4.28-suite in #1746's eigen run de
   helper nog mist (die PRs staan pas op develop na merge), is dit resultaat
   NICHT een Widerlegung van de helper-fix maar een VOLGEND-BLOK:
   -> **static cells operator-auth gruen: NEIN (nog niet — hop-PR's zelf
      falen op uncataloged diff-paden (#1761) en candidate-consent (#1771))**
6. (done) 'target-create = 247-owner of helper': in GEEN BEIDE runs verscheen
   een 'target create mcp-static exits nonzero' / operator_authentication_required
   faal; de aanwijsbare faal op de MUTATIE-pad is candidate-consent
   (--confirm-candidate) binnen TestApplicationCapabilityLifecycle — dat is
   DEMO/consent-familie (zoals de Option-A round-2 bevind), niet de helper
   en niet het gemelde mcp-static target-create pad. Geen STOP naar de 247
   owner nodig vanuit deze meting: de helpers-zijde is niet de blocker die
   zich hier voordede; de mcp-static target-create kwestie BLEEF ONBESTOKEN
   in deze runs (geen enkele statische cell draaide).
   Benodigde vervolgfout voor #1761 (buiten deze write-set — catalog-json is
   verboden in deze opdracht): de vier uncataloged bronnen moeten in
   scripts/pr-gate-coverage.json (met hun surfaces), anders faalt elke
   gehopte helper-PR blijvend bij Trusted Plan. Gemeld aan de coordinator.
7. (done) Akte + ls-tree-witness op plan origin/main.
8. (done) Cleanliness + END.

## Provenance

- base attestation: ls-remote develop = `b27b2ebedb7da10690fb83c24a9f763ee16d7468`
  (gemeten vóór de hops, identiek op beide merge-points).
- #1761: ouders van fcfe3f09 = (669d76ac fcfe's eerste ouder; b27b2ebe als
  origin/develop). `git merge-base --is-ancestor b27b2ebe fcfe3f09` OK;
  `669d76ac is-ancestor` OK.
- #1771: ouders van ebd01baa = (dc775235, b27b2ebe); beide is-ancestor OK.
- delivery: ls-remote branch+pull heads = fcfe3f09 (#1761) en ebd01baa
  (#1771); PR state/heads via gh api bevestigd.
- diff-name voor beide hops = GEEN eigen content-edit (merge-commit only);
  `git diff --name-only HEAD^1 HEAD` toont de develop-inkomsten, geen
  handmatige wijzigingen door deze lane.
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` = https://github.com/mcpdev80/baseharbor-plan.git.

## repo-rule compliance

- Alleen additive git hops + push; GEEN content-edit, GEEN product/.github/
  catalog-json/#1783/#1780 touch. PRs open/ready gelaten; geen merge, geen
  commentaar; geen subagenten; geen containers op deze host.
- Ruim opgeruimd: de extra hop-werktree workers/0428-231-hop/h1761 (lokale
  strand) is verwijderd (worktree remove --force + prune, ls-remote bewees
  dat er niets vanaf pushed was).

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 1961963), AFTER = 0 entries
(pid 2026545). Geen compose/container gestart op deze host. Scratch
`/var/tmp/0428-223-tp1761.log`, `-np1771.log` vóór END verwijderd. Werkbomen
0428-231-authhelper-wt en 0428-231-opauthfix-wt houden hun kandidaten (0 delta
na de hops); workers/0428-231-hop is leeg/verwijderd.

END 0428-223-testctx DONE — 0428-231 hop-both round-1: #1761 nieuwe head fcfe3f09668f160cff1de4d0ee8f693ce5de958c (merge --no-ff van b27b2ebe, ouders 669d76ac+b27b2ebe, ls-remote branch+pull bewezen), run 45053923585 completed/failure — Trusted Plan job 137304883073 faalt op 4 uncataloged diff-paden van de helper-PR zelf (app_env_test.go, app_export_command_test.go, target_definition_change_test.go, internal/operatorauth/test_operator.go) — VERVOLGKAART noddig: catalog entries (buiten deze write-set). #1771 nieuwe head ebd01baa5218d4bc55880647e7b7b318c096bcfa (ouders dc775235+b27b2ebe, ls-remote bewezen), run 45054073860 completed/failure — Trusted Plan 137305322238 SUCCESS (fix-paden cataloged), falen zit in native/selected data-caps cellen op candidate-consent (--confirm-candidate in TestApplicationCapabilityLifecycle), zelfde familie als de Option-A round-2 demo-consent bevind. static cells operator-auth gruen: NEIN (nog niet, oorzaken hierboven); target-create mcp-static: in GEEN BEIDE runs opgedoken — niet de blocker die zich hier voordeed, geen 247-stop nodig vanuit deze runs. cleanliness: besenrein

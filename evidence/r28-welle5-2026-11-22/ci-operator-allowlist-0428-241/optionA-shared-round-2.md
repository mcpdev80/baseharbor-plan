# 0428-241/250 Option-A shared fixture round-2 — MCP parity admission in het tagged fixture (develop b27b2ebe)

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht: de MCP-helft van de
footprint-parity in het build-tagged test-only fixture toelaten onder
data-capabilities/core-capability, zodat de selected docker+podman
data-caps cells groen worden. Geen product-wijzigingen; stage-boundary (#1782)
niet meer aangeraakt.

selected docker+podman parity gruen: NEIN — parity zelf is GEBEVEN, andere faal oorzaak zie punt 7

other mcp tools denied: ja

## PLAN

1. (done) Realiteit: origin=github URL; ls-remote develop=`b27b2ebe…`
   (unverandert), branch + pull/1783/head = `8f84fcbd…` (round-1 state, PR
   OPEN ready), eerdere post-startte inderdaad niet — head was nog 8f84fcbd;
   docker ps -a before=0, eigen pid 1590692.
2. (done) STOP-FALL check: git grep `ciMCPToolsetContextKey` = definitie in
   cmd/baha/mcp.go:243-246, maar die code LEEST alleen de context-vlag (de
   restricted toolset-keuze is context-gestuurd); de ADMISSION (mcp serve +
   vlag-zetten) zat volledig in het tagged fixture
   (ci_integration_operator_enabled.go :71-72 en :149-150, gate==guided only).
   Geen product mcp.go-operatorauth wijziging nodig -> GEEN stop-val.
3. (done) Wijziging in het tagged fixture (alleen enabled.go): helper
   `ciIntegrationMCPFootprintParityGate()` (BASEHARBOR_DEMO_OPERATOR_GATE in
   {guided, data-capabilities, core-capability}); de MCP-serve admission-tak
   (:149) en de ciMCPToolsetContextKey-zet (:71) gebruikt nu deze helper —
   geleid-analog, exact zoals de CLI-blok uit round-1. ONE-tool restriction
   BEHOUDEN: newMCPServerForContext exposeert bij de vlag exact alleen
   baseharbor.app.footprint.show (product-code unverandert, dus alle andere
   MCP tools blijven DENIED/fail-closed). CLI-block en write
   record-deployment unveraendert; production fail-closed niet aangeraakt.
4. (done) Regression TestCIIntegrationOperatorAllowsFootprintShowInSelectedData
   Gates uitgebreid: per {docker,podman}×{data-capabilities,core-capability}
   nu OOK de MCP-parity-helft — mcp serve krijgt de CI-operator + restricted
   toolset-vlag, ListTools toont exact één tool
   baseharbor.app.footprint.show, een baseharbor.app.destroy call wordt
   DENIED; en de escape-check breidt uit: 'mcp serve' onder gate lifecycle
   krijgt géén operator. Suites: seam-tests 9 PASS (named+skip, incl. de 4
   parity-subcases); untagged run (no-op fixture) OK; gofmt clean; vet tagged
   rc=0. CI-home: ci-integration-operator-seam-tests (ci.yml:1328) + native
   cells bouwen de tag (ci.yml:1145).
5. (done) ONE additive commit `2da7f5657a6b29a7052d7716e42da0aa0527bebf` op
   round-1 commit 8f84fcbd bovenop exact develop b27b2ebe (GEEN force/amend;
   `git log --oneline origin/develop..HEAD` = exact onZELF TWO commits
   2da7f565 + 8f84fcbd; diff origin/develop...HEAD = alleen de 2 fixture-
   bestanden). ci-fast-check rc=0; normal push; NIEUWE head 2da7f565
   bevestigd op branch én pull/1783/head (ls-remote; PR head liep even achter,
   daarna 2da7f565 gemeten).
6. (done) EXACT hosted normal run **45051057741** @2da7f565 terminal
   completed/failure (failed=5: PR Selected Checks + 2 native data-caps jobs
   + 2 selected-runtime cell jobs). Alle statische/plan/validation jobs
   EXECUTED success: Trusted Plan 137296040953, Native gate plan 137296040737,
   Source format 137296040888, Workflow policy 137296040971, seam-tests
   137296135182, Focused Python 137296135307, Exact Candidate, Runner
   Interface, Demo Pin, cli-build/vet/guided-tests, source-contracts.
7. (partial) Parity-status uit de hostende cel-logs:
   - BEIDE selected data-caps cells (docker 137296517250, podman
     137296517242): de trace toont `decision=managed-local-gate
     command="app footprint show -o json"` EN `decision=managed-local-gate
     command="mcp serve"` op het eigen target — beide parity-helften worden
     nu gestempeld; 'contracts differ' komt in de logs **NIET** meer voor
     (grep 0 hits in beide logs; round-1 had het nog).
     -> de PARITY-VOORWAARDE van deze kaart is technisch vervuld.
   - DE CELL WORDT TOCH ROOD, door een ANDERE, niet-gebaseerde faal in
     dezelfde demo-driver: fixture-stap `new-edit-new-sql` gooit
     `RuntimeError: new-edit-new-sql exceeded no-output timeout:
     elapsed=106-107s no-output=90s limit=90s` (tests/guided/drive.py:415) en
     de oorspronkelijke fout-regel is: `Error: record deployment before
     mutation: candidate submission requires an explicit
     operator/automation consent (--confirm-candidate); refusing to record
     deployment state`. Dat is de WRITE record-deployment digest-/consent-
     verplichting die deze opdracht uitdrukkelijk ONVERANDERD moet laten —
     de demo-fixture (buiten deze repo: _temp/baseharbor-demo-atomic) roept
     de mutatie aan zonder de exacte consent-vlag die de round-2 taaktext
     niet toestaat om aan te tasten. Blijkbaar is de eerdere round-1
     'contracts differ' dus vervangen door de parity-bepaling die WEL doordat
     de MCP-clip slaagt, maar de demo-stap new-edit-new-sql had deels al
     eerder gefaald (zie de 17:47/17:53 timestamps: dezelfde consent-fout).
     GEMELD ALS BEVIND voor de kaart die de demo-fixture/consent-vlag bezit
     (0428-241-pariteit follow-up): de parity-fixture moet de
     `--confirm-candidate` consent-vlag zetten voor new-edit-new-sql OF de
     product-consent-grens is de ware blocker (dan: Owner/247-family).
     Voor deze kaart: STOP-punt bereikt binnen de write-set — verder
     veredern van de consent-grens ZOU het tagged fixture te boven gaan.
8. (done) Akte + ls-tree-witness op plan origin/main.
9. (done) Cleanliness + END.

## Provenance

- base attestation: ls-remote develop = `b27b2ebedb7da10690fb83c24a9f763ee16d7468`
  (twee keer gemeten, identiek); branch-round-1 stond hierop; round-2 is de
  additieve commit `2da7f565`.
- `git log --oneline origin/develop..HEAD` = TWO eigen commits (8f84fcbd,
  2da7f565), geen vreemde.
- `git diff origin/develop...HEAD --name-only` =
  cmd/baha/ci_integration_operator_enabled.go + -enabled_test.go.
- delivery: ls-remote branch-head en pull/1783/head beide =
  `2da7f5657a6b29a7052d7716e42da0aa0527bebf` (NIEUWE head, niet 8f84fcbd).
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` = https://github.com/mcpdev80/baseharbor-plan.git.

## repo-rule compliance

- Write-set: alleen de 2 tagged fixture-bestanden. GEEN product
  operatorauth/mcp.go/deployment_record, GEEN .github, GEEN 237, GEEN
  stage-boundary (#1782 is gemerged en niet aangeraakt). Additieve commit,
  normal push, geen force/amend. PR #1783 blijft READY (geen draft-deme):
  missie beveelt geen nieuwe promotie. Geen merge/kommentaar door deze lane;
  geen subagenten; geen containers op deze host; go-tests in named vorm met
  skip-regex.
- native :edge blijft red (andre defect, buiten scope gem according opdracht;
  niets gefixt).

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 1590692), AFTER = 0 entries
(pid 1923622). Geen compose/container gestart op deze host. Onbedoelde `baha`
build-binary uit de werktree verwijderd vóór commit (git status was 0 na
netjes `git add` van de 2 paden); scratch /var/tmp/0428-223-fc-r2.log en
cel-logs worden vóór END verwijderd. Werkboom workers/0428-241-optawt houdt de
kandidaat (0 delta na commit).

END 0428-223-testctx BLOCKED — 0428-241 round-2: nieuwe head 2da7f5657a6b29a7052d7716e42da0aa0527bebf op #1783 (additief, ls-remote bewezen), exact hosted run 45051057741 terminal — parity-beide-helften gestures en 'contracts differ' weg (ja), other mcp tools denied: ja, MAAR selected docker+podman data-caps cells worden daardoor NIET groen: nieuwe/andere faal `new-edit-new-sql exceeded no-output timeout` met bron `record deployment … requires --confirm-candidate` in de demo-fixture (buiten deze write-set; Owner/247-family vraagstuk). 'selected docker+podman parity gruen: NEIN — parity gebeven, andere oorzaak'. cleanliness: besenrein

## origin/main witness

Exacte uitvoer van `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep optionA-shared-round-2` (plan main = 3e7c50917d556ff85ea62a60f2bcdb5d01f8f5b5):

```
evidence/r28-welle5-2026-11-22/ci-operator-allowlist-0428-241/optionA-shared-round-2.md
```

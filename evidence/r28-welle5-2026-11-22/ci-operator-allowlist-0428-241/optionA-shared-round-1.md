# 0428-241/250 Option-A shared fixture round-1 — footprint show admitted in tagged CI data gates (develop b27b2ebe)

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht: de SHARED test-only unlock die de
selected cells van #1780, #1770 en #1738 nodig hebben, los uit de verfilzte #1780
in eigen PR. #1782 (stage-boundary) is GEMERGT; er is niets aan stage-boundary
gedaan.

footprint-show read in tagged fixture admitted, write record-dep bleibt digest, product unveraendert

## PLAN

1. (done) Realiteit: origin=github URL (remote -v hieronder); ls-remote
   develop=`b27b2ebedb7da10690fb83c24a9f763ee16d7468` (#1782 gemerged als
   b27b2ebe — merge-commit-regel van GitHub, niet door deze lane); branch
   lane-0428-241-optionA-operator-allowlist bestond NIET. docker ps -a before=0,
   eigen pid 799778.
2. (done) STOP-FALL check: de pruebaatzitting is HET BUILD-TAGGED test-only
   fixture. Gemeten: de afwijzing-tekst 'command-not-in-managed-workload-set'
   leeft alleen in cmd/baha/ci_integration_operator_enabled.go:180 (git grep
   over heel de repo); de fixture-match ciIntegrationGuidedFootprintShow
   (:232-233, exact app/footprint/show/-o/json) was alleen onder gate ==
   "guided" (regel ~135). De hostende logs van de gemelde cells (docker job
   137272916006, podman job 137272915982) tonen letterlijk
   `decision=managed-local-gate-rejected: command-not-in-managed-workload-set:
   app footprint show -o json target="atomic-{docker,podman}-data-capabilities"`.
   GEEN stop-fall: product mcp.go/operatorauth niet verantwoordelijk, niet
   aangeraakt.
3. (done) Werktree workers/0428-241-optawt + branch op EXACT b27b2ebe
   (merge-base --is-ancestor OK, ANCESTOR-OK). Disabled-tag variant
   (ci_integration_operator_disabled.go) bekeken: no-op, NIET aangeraakt.
4. (done) Fixture uitgebreid: extra admission-tak
   `(gate == "data-capabilities" || gate == "core-capability") &&
   ciIntegrationGuidedFootprintShow(args)` direct na de bestaande guided-only
   tak (die blijft exact zoals ze was). Zelfde exacte arg-vorm
   (app/footprint/show/-o/json), dus onafhankelijk van de guided-only route
   maar zonder nieuwe forms. WRITE record-deployment blijft digest-pflichtig:
   geen enkele wijziging aan de product-authorisatie of de record/deployment-
   routes. Product fail-closed boundary intact (alleen het tagged fixture is
   ruimer in die ene gate-combinatie).
5. (done) Regression TestCIIntegrationOperatorAllowsFootprintShowInSelectedData
   Gates in cmd/baha/ci_integration_operator_enabled_test.go: operator
   gestempeld (principal present) voor de exacte read-vorm op docker+podman ×
   data-capabilities/core-capability, non-canonical vormen
   (--json / extra arg / vorm-zonder-opties) blijven fail-closed, en de
   exception escape't NIET naar gate lifecycle. Eerste opzet nam
   'app configure demo' op in de reject-lijst; gemeten dat app.configure een
   EIGENAL managed local workload operation is (operatorauth.LocalWorkloadOperation)
   en dus altijd al toegelaten wordt — die cases zijn verwijderd met een
   uitlegcommentaar, de digest-verplichting van record-deployment zit in de
   product-authority en is hier niet versoepeld (test 8 OK).
   CI-home: `ci-integration-operator-seam-tests`
   (go test -tags=baseharbor_ci_operator_testonly ./cmd/baha
   -run '^TestCIIntegrationOperator', ci.yml:1328) — als Validation job in
   elke PR AND in de selected runtime-gate cells; de gate-binary zelf wordt
   met de tag gebouwd (ci.yml:1145).
6. (done) ONE commit `8f84fcbdbd347a103a0829f4ecc490621b914a7b` (+60 regels,
   alleen de 2 fixture-paden), gofmt clean, go vet tagged rc=0, named
   go-test-vorm met skip-regex OK, ci-fast-check rc=0, normal push, DRAFT PR
   #1783 -> per missie gepromoveerd naar READY; ls-remote bewijst branch-head
   en pull/1783/head = 8f84fcbd. (Onbedoelde `baha` build-binary in de
   werktree vóór de commit verwijderd; git status afterward 0.)
7. (done) EXACT hosted normal run **45045885547** @8f84fcbd terminal
   completed/**failure** (failed=5, skipped=25). Conditie van de missie
   'exact hosted soweit startbar' is voldaan en de VOORWAARDE van deze kaart is
   bereikt: in BEIDE native data-capabilities cells (docker 137280787736,
   podman 137280787743) en de native parents 137280389052/137280389091 toont
   de trace `decision=managed-local-gate command="app footprint show -o json"`
   — de operator STEPELT (gestempeld) in plaats van fail-closed;
   'command-not-in-managed-workload-set: app footprint show -o json' komt in
   deze head NIET meer voor (grep=0 op de podman-log; de docker-log toont de
   admitted-beslissing + alleen de verwachte mcp-serve reject voor een andere
   gate-vorm). De overgebleven cel-faal is EEN ANDERE oorzaak: de Demo-
   acceptance-test `footprint_parity` gooit 'actual native CLI JSON/MCP
   Footprint contracts differ' (tests/guided/new_edit.py:63, aangeroepen uit
   baseharbor-demo tests/data-capabilities/new_edit.py:282) — een
   CLI-JSON-vs-MCP-contract divergence in de demo fixture, NIET de
   operator-admission die deze kaart aftikt. Melden als BEVIND voor de
   demo/parity-kaart: de parity-check vergelijkt nu twee levende bronnen
   (CLI footprint show + MCP tool) die uit elkaar lopen.
8. (done) Akte + ls-tree-witness op plan origin/main.
9. (done) Cleanliness + END.

## Provenance

- base attestation: ls-remote develop = `b27b2ebedb7da10690fb83c24a9f763ee16d7468`;
  branch gesneden op dat exacte voorwerp; ANCESTOR-OK.
- `git log --oneline origin/develop..HEAD` = exact EEN eigen commit (8f84fcbd).
- `git diff origin/develop...HEAD --name-only` =
  `cmd/baha/ci_integration_operator_enabled.go`,
  `cmd/baha/ci_integration_operator_enabled_test.go`.
- delivery: ls-remote refs/heads/lane-0428-241-optionA-operator-allowlist en
  refs/pull/1783/head beide = `8f84fcbdbd347a103a0829f4ecc490621b914a7b`.
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` = https://github.com/mcpdev80/baseharbor-plan.git.

## repo-rule compliance

- Write-set: alleen het tagged fixture-bestand + zijn test (missie). GEEN
  product operatorauth/mcp.go, GEEN .github, GEEN deployment_record
  product-pfad, GEEN 237, GEEN disabled-analog (no-op volstond). Geen
  stage-boundary wijzigingen (#1782 gemerged, niet meer aangeraakt). Geen
  merge/kommentaar door deze lane; PR draft→ready per opdracht; geen
  subagenten; geen containers op deze host; go-test uitsluitend in named
  vorm met de verplichte skip-regex.

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 799778), AFTER = 0 entries
(END-shell pid). Geen compose/container gestart op deze host. Onbedoelde build
`baha` in de werktree verwijderd vóór de commit; scratch
`/var/tmp/0428-223-fc-opta.log`, cel-logs worden vóór END verwijderd. Werkboom
workers/0428-241-optawt houdt de kandidaat (0 delta na commit).

END 0428-223-testctx DONE — 0428-241/250 Option-A shared fixture round-1: branch lane-0428-241-optionA-operator-allowlist, head 8f84fcbdbd347a103a0829f4ecc490621b914a7b (ONE commit op exact develop b27b2ebe, ANCESTOR/log/diff bewezen), PR #1783 class READY, exact hosted run 45045885547 terminal (footprint-show operator-admission BEVESTIGD in beide native cells — trace 'managed-local-gate command="app footprint show -o json"', geen command-not-in-managed-workload-set meer voor dit pad op deze head), cel-faal rest = ANDERE oorzaak (demo footprint_parity CLI-vs-MCP contract divergence, bevind gemeld), 'footprint-show read in tagged fixture admitted, write record-dep bleibt digest, product unveraendert', cleanliness: besenrein

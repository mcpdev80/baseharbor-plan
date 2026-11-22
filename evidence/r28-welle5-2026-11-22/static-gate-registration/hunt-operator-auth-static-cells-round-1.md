# Bug-hunt operator-auth static cells round-1 — read-only (karte 0428-231 territory)

Schnitt: de statische gate `atomic/static/shell-ux` faalt in pre-release run 45014836421 met
`Managed-environment machine operations require an authenticated BaseHarbor operator.` (Affected: `shell-ux-static/dev`).
Read-only; geen product-/workflow-/scripts-wijziging, geen commit/push/merge/kommentar, geen subagenten.

## PLAN

1. (done) Read-only vastgesteld: eigen pid 3868175, `docker ps -a` BEFORE = 0; remote truth alleen via
   `git ls-remote https://github.com/mcpdev80/baseharbor.git` + `gh api`/`gh run view`; candidate SHA
   `3d927252fae0af979056d442d19384f72c771a5b` (develop-ancestral, gemeten), demo pin `5d1cf312e18d06915db35c340bebe4e3d4f39d45`
   (uit de job-log DEMO_REF-regel), develop = `8629450ef3c`.
2. (done) Falende job en EXAKTE fail-regel gehaald: job 137187053472 (`Static · shell-ux / Executed static · shell-ux`),
   log-regel 574-576 op timestamp 2026-11-22T11:05:35.06Z.
3. (done) Fund (a): WAAR de eis gezet wordt (datei:zeile) en welke baseline/fixture ontbreekt.
4. (done) Fund (b): de operator-auth helper die WEL bestaat maar door de statische cellen niet geladen wordt.
5. (done) Fund (c): EXAKTE fail-lijn + volgende aktie (welke file, welke zeile, welke baseline).
6. (pending) Akte publiceren + ls-tree-witness; daarna END.

## Fund (a) — waar de eis staat, en welke baseline ontbreekt

De afstel-keten voor de statische shell-ux cel (alles op develop `8629450ef3c` / candidate `3d927252`):

- Eis-herkomst (boodschap): `cmd/baha/mcp.go:317` (`authorizeMCPOperation` bouwt de
  `machine.Error{Code: authentication_failed, cause operator_authentication_required}` na een falende
  boundary-check) en `internal/operatorauth/authorization.go:285` (dezelfde tekst op de
  AuthorizeMachineRoute). Affected-regel `shell-ux-static/dev` = `mcp.go:314` (`Resource: target + "/" + environment`).
- Boundary-check: `cmd/baha/mcp.go:302-308` — bij managed environment en GEEN principal wordt
  `verifiedLocalWorkloadAuthority` geprobeerd; faalt die (local=false), dan roept
  `ensureManagedEnvironmentOperatorBoundary` (`mcp.go:319`) → `ensureOperatorAuthForBoundary`
  (`cmd/baha/operator_auth_boundary.go:55-90`): zonder config (geen OperatorAuthForTargetEnvironment, geen
  `BASEHARBOR_OPERATOR_OIDC_*` env) → `ErrConfigurationRequired` → de boodschap hierboven.
- Waarom de local-workload-route ledig loopt: `cmd/baha/local_workload_authority.go:62` vergelijkt
  `selected.AccessProvider != "local"`. De fixture registreert de Target met `--access local-docker`
  (`baseharbor-demo tests/shell-ux/run.sh:17-22` op pin 5d1cf312), en de CLI registreert die access-reference als
  `AccessProvider: "local-docker"` (de fallback "local" in `internal/deployment/target.go:509-530` geldt alleen voor een targetloos host-default) — de test-fixture in
  `cmd/baha/app_list_all_targets_test.go` laat zien dat `local` en `local-docker` twee verschillende, evenwijdige
  provider-waardes zijn (geen alias). Daarmee valt de grant vór de runtime-probe af (false, geen error) en is er niets om naar door te
  vallen. Dit is het primaire defect.
- Secundair (blijft staan na fix van het eerste): de cel bouwt zijn binary ZONDER de operator-baseline.
  In pre-release run 45014836421 draaide job 137187053472 de ELSE-tak `go build -trimpath -o "$RUNNER_TEMP/atomic-bin/baha" ./cmd/baha`
  (job-log regel ~555, geen `candidate_artifact`/`baha-ci-operator-testonly` in die job) — dus zonder build-tag
  `baseharbor_ci_operator_testonly`, waarmee `withCIIntegrationOperator` in alle normale builds een no-op is
  (`cmd/baha/ci_integration_operator_disabled.go`). Ook de runtime-gate route (`pre-release-runtime-suite.yml`,
  'Run runtime gate' ~regel 296-306) injecteert de testonly-binary alléén `if [ -n inputs.candidate_artifact ]`;
  statische cellen komen daar niet in aanmerking (hun stap is 'Run static gate').
- Zelfde falende baseline, méér cellen: in (gecancelde) run 45015912507 faalden OOK
  `Static · init / Executed static · init` (job 137190621488, idem `init-source-fixture/dev`) en
  `Static · config-matrix / Executed static · config-matrix` (job 137190621449, via
  `contract_check.py:55` → `baha app init --quick` → `app_init_wizard.go:166` — CLI-transport zonder
  operator-principal en zonder geldige local grant, dus dezelfde afstel-tekst). `Static · mcp` (137190621450) faalde in DEZE run um 11:21:03 met een ANDERE oorzaak:
  `MCP contract mismatch: unexpected=['baseharbor.app.perses.*']` — de kandidaat 3d927252 registreert perses-MCP-tools
  die de demo-pin 5d1cf312 niet in zijn verwachte-set kent. Run 45014836421 voerde deze cel niet uit (daar draaide
  alleen shell-ux), dus er is in deze shift GEEN groen getuigenis van deze cel; het blijft een
  kandidaat-/pin-afwijking, geen operator-auth-befund.

## Fund (b) — de operator-auth helper die de statische cellen NIET laden

- Helper 1 (test-only build): `cmd/baha/ci_integration_operator_enabled.go` (build-tag `baseharbor_ci_operator_testonly`,
  `withCIIntegrationOperator` → `ciIntegrationOperatorContext` installeert principal `https://issuer.test`/
  `ci-acceptance-operator` + editor-membership). De statische cel laadt hem NIET, om twee redenen: (i) de cel-build
  `go build ./cmd/baha` draait de tag niet (zie fund a; de testonly-binary `baha-ci-operator-testonly` wordt door
  `pre-release-runtime-suite.yml` alleen aan RUNTIME-gates aangeboden, niet aan static), en (ii) zijn poort
  `ciIntegrationManagedLocalGateReason` eist `BASEHARBOR_TEST_RUNTIME == "docker"|"podman"` en
  `target.Name == "atomic-<runtime>-<gate>"` — de statische cel zet `BASEHARBOR_TEST_RUNTIME: static` en heet
  `shell-ux-static`, dus zelfs met de tag zou de helper hier fail-closed afwĳzen ("runtime-or-gate-mismatch").
- Helper 2 (Go-proces-only): `internal/operatorauth/test_operator.go` (`WithVerifiedTestOperator*`) — geldt
  uitsluitend in Go-testprocessen, niet in het `baha`-binary dat de shell-fixture aanroept. Bestaat dus wél,
  maar is voor statische cellen leeg.
- De echte fixture-baseline (`baha login` met OIDC; operator-session onder `SessionPath` =
  XDG_RUNTIME_DIR/state-root `cache/sessions`, `internal/operatorauth/session.go:37` `LoadSession` /
  `:128` `VerifySession`) bestaat, maar wordt door GEEN enkele statische cel geladen: geen workflow of demo-script
  voert een operator-login uit vór de cel (de cel-omgeving heeft geen ingerichte OIDC-provider en de fixture
  exporteert alleen XDG_*_HOME — `tests/shell-ux/run.sh:11-13`).

## Fund (c) — EXAKTE fail-lijn en volgende aktie

- Exacte fail (job-log 137187053472): `2026-11-22T11:05:35.0619356Z   Managed-environment machine operations require an authenticated BaseHarbor operator.`
  followed by `Affected: shell-ux-static/dev` en `##[error]Process completed with exit code 1.`
  (uitgelokt door `tests/shell-ux/run.sh:26` → `tests/static-adopt-fixture.py` → `baha mcp serve` →
  `baseharbor.app.adopt` → `mcp.go:317`).
- Zinnigste volgende aktie (single minimal, Owner/lane): `cmd/baha/local_workload_authority.go:62` — de
  local-workload-toelating moet de docker-access-vormen erkennen die de fixtures gebruiken: vergelijk niet
  `selected.AccessProvider != "local"` maar laat `local` EN `local-docker` (de ProviderDocker-access van
  `target create --access local-docker`) door, of normaliseer `local-docker`→`local` bij deze check. Daarna
  valt de route op de bestaande, al geteste runtime-grant-probe (`CheckLocalRuntimeGrant` + geverifieerde
  docker engine op de runner: `internal/runtime/docker_engine.go:109-117` plus `:247` (`Verified` alleen na één gelukte engine-probe)). Alternatief voor de CLI-transport-cellen
  (init/config-matrix, waar geen MCP-server loopt): dezelfde normalisatie is genoeg, want `main.go:151`
  zet `withLocalInvocation(ctx,"cli")` en `cliLocalWorkloadOperation` mappet `init`/`app init` → `app.adopt`
  (`local_workload_authority.go:161-178`). Test-aansluiting: een CLI-regresetest die `target create --access local-docker`
  + bron-only `app.adopt` door de real grant voert (of de bestaande grant-tests uitbreiden met AccessProvider
  "local-docker" — de worker moet de mapper en de probe-volgorde zelf op de current source verifiëren); route naar de GitHub CI via de bestaande `cmd/baha`-shards (geen `.github/**`-wijziging nodig).
  Een workflow-zĳde is niet nodig: de statische cel hoeft de testonly-binary niet te krijgen, de fixture is
  already exactly the "local-docker target" case the grant path claims to support (`coreinstallation.Load` must
  stay absent in the cel — shell-ux zet `XDG_DATA_HOME` isolated, dus er staat géén Core-installation).

## Open questions voor de Coordinator (geen blocker voor deze jacht)

- Init en config-matrix (run 45015912507) delen hetzelfde fixture-patroon (target create `--access local-docker`
  + een managed workload-operatie in de real binary zonder principal). Hun eerdere groen-state is in deze
  read-only jacht niet histories bespeurd; de aktie in fund (c) dekt alle drie cellen.

## cleanliness

cleanliness: read-only, besenrein. Eigen pid 3868175. `docker ps -a` BEFORE = 0 entries; AFTER = 0 entries
(pid bevestigd na de aktie). Niets gestart, geen commit/push in enige produkt-repo; worktree
workers/0428-231-authhelper-wt en baseharbor-demo alleen gelezen/bekeken (git status unverändert); scratch
`/var/tmp/0428-223-h231-*` verwijderd vór END.

END 0428-223-testctx DONE (hunt operator-auth-static-cells: fund a eis=mcp.go:317/authorization.go:285,
afval-regel=local_workload_authority.go:62 AccessProvider "local-docker"≠"local" + cel-build zonder
ci_operator_testonly-tag (disabled.go no-op), bewezen in job 137187053472 11:05:35 + 137190621449/488;
fund b helper=ci_integration_operator_enabled.go (tag+runtime-gate-poort sluiten static uit) en
test_operator.go (alleen Go-proces) — cel laden ze NIET; fund c volgende aktie: local-docker toelaten in
local_workload_authority.go:62, regressie via cmd/baha shards zonder .github-wijziging; nevenbefund: kandidaat 3d927252 vs
demo-pin 5d1cf312 MCP-contract mismatch (perses-tools) → Static·mcp rood in run 45015912507; cleanliness: besenrein)

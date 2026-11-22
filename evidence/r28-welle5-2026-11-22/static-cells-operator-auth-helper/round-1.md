# 0428-231 round-1 — STOP-criteria metingen op develop c463edf87ee (helper-roede niet uitvoerbaar als beschreven)

## PLAN

- (done) 1. Claim via scripts/plan.py claim (gepubliceed op plan origin/main); ls-remote develop c463edf87ee; branch lane-0428-231-static-auth-helper op develop gesneden (ancestry OK, base-behind=0)
- (done) 2. Duplikatie-stand op de echte refs afgelezen — zie metingen: de in de mission genoemde paden/regels bestaan niet op develop
- (done) 3. Beslispunt bereikt volgens STOP-conditie van de mission ("als de helper zonder neue interface-erweiterung niet gaat … mit datei:zeile melden, nicht breiter bauen")
- (pending) 4. Umstellung der Test-Dateien + PR + gehoste run — wacht op beslissing van de coordinator
- (done) 5. Akte + publicatie op plan origin/main met ls-tree-witness
- (pending) 6. QUESTION post aan 9142ab1f

## Remote/zone witnesses

- Planning repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` — correcte zone; claim is daarop gecommit/push.
- Product (eerste git-actie in de wermtree): `git remote -v` → `origin https://github.com/mcpdev80/baseharbor.git`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-231-static-auth-helper` → develop `c463edf87ee6f12c9da2ae2ee02ea6fe7c7ef0f9`; branch-ref bestaat NIET op de remote (alleen lokaal, nog geen PR).

## Wat de mission beweert vs. wat gemeten is

- Mission: "de helper-functie internal/testing.NewCLIContextForTargetForApp is dus im kandidaten vorratig".
  - Gemeten: `GitHub contents API internal/testing?ref=c463edf87ee…` → **HTTP 404** (geen dir internal/testing op develop); `grep -rn NewCLIContextForTargetForApp` over de volledige develop-boom → **0 treffers**.
- Mission: "cmd/baha/test_operator_context_test.go:269-273 en :464-468, cmd/baha/cli_test.go:439-443".
  - Gemeten: `cmd/baha/test_operator_context_test.go` is op develop **141 regels** (de regels 269+/464+ bestaan dus niet); `git cat-file -e 1ff16925c4e:cmd/baha/cli_test.go` → **faalt, bestand bestaat niet op develop**. Beide regels stammen kennelijk uit een andere (langere) versie uit de 0428-231-notitie.

## De echte, gemeten duplicatie (op develop c463edf87ee)

De opwand-afdekking die nu 4-5 keer handmatig wordt gerepliceerd in package-main tests:

1. `cmd/baha/test_operator_context_test.go:22-34` — `testOperatorContext`: bouwt `identity.Principal{Issuer:"https://issuer.test", Subject:"cli-test-operator", IssuerVerified:true, Groups:["editor"]}` + `operatorauth.WithVerifiedPrincipal` + `WithMembershipProviderIfAbsent(&readGrantingMembershipProvider{})` + `WithEnforcementIfAbsent`.
2. `cmd/baha/app_env_test.go:36-37` — principal + `operatorauth.WithMembershipProvider(ctx, &readGrantingMembershipProvider{})`; de provider-selfde is hier gedefinieerd: `cmd/baha/app_env_test.go:51-53` (`readGrantingMembershipProvider`).
3. `cmd/baha/app_export_command_test.go:371-377` en `:394-400` — `WithVerifiedPrincipal` + `WithMembershipProvider(readGrantingMembershipProvider{})`.
4. `cmd/baha/installation_destroy_native_test.go:46-47` — `WithVerifiedPrincipal` + `WithMembershipProvider`.
5. `cmd/baha/target_definition_change_test.go:41` — `WithVerifiedPrincipal` bovenop `testOperatorContext`.

`internal/operatorauth/context.go` exporteert de bouwstenen (WithVerifiedPrincipal / WithMembershipProvider(IfAbsent) / WithEnforcement(IfAbsent) / PrincipalFromContext) maar GEEN samengestelde test-operator helper.

## Beslispunt (volgens de mission: melden, niet breder bouwen)

De helper-roede is uitvoerbaar, maar ANDERS dan de mission beschrijft:
- Een exporteerde helper in `internal/operatorauth` (packageregel, Owner-scope OK voor internal/operatorauth/**) zoals `func AuthenticatedOperatorForTest(t, ctx)` die principal + membership + enforcement in één zet — vereist dat het package `internal/operatorauth` een test-only principal/membership-stub exporteert, EN vereist dat de membership-provider-definitie (nu in cmd/baha/app_env_test.go) naar de helper verhuist. Dat raakt precies de 4-5 testbestanden hierboven, dus ALLEEN test-oppervlak + internal/operatorauth — binnen het toegefpaneel, maar de in de mission genoemde regels/bestanden kloppen niet.
- Het alternatief van de mission (fan-out op internal/testing.NewCLIContextForTargetForApp) is onuitvoerbaar: die functie/dir bestaat niet op develop — zonder NUEUWE interface-erweiterung (dir + functie zelf aanmaken, product-zijde) gaat die roede niet, en dat is de letterlijke STOP-conditie.

## repo-rule compliance / cleanliness

- Geen `.github/**`, geen `scripts/**` gewijzigd; er is nog GEEN productwijziging geimplementaeerd (alleen metingen); branch nog niet gepusht. Geen lokale test-runs als bewijs; geen subagenten; posten alleen naar coordinator 9142ab1f.
- cleanliness: nothing started. Eigen pid 2903795; `docker ps -a` BEFORE/AFTER = 0 entries.

END 0428-223-testctx BLOCKED (beslispunt bereikt; branch lane-0428-231-static-auth-helper = develop c463edf87ee, base-behind=0, geen PR nog, run-id n.v.t.)

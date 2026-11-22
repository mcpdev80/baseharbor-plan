# 0428-231 fix round-1 — static cell operator-auth (local-workload grant)

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht: fix van de eigen hunt-befund
(hunt-operator-auth-static-cells-round-1.md, plan main f7e7a23bd; follow-up kaart 0428-243).

defekt: de opdracht-omschrijving van fund (a) ("de grant-check vergelijkt tegen kort-alias
`local`, dus `--access local-docker` valt af") klopt NIET op de current source. De
access-mapper normaliseert al vóór de grant-check: `baha target create NAME --access
local-docker --reference local` zonder `--access-provider` set `accessProvider = "local"`
(cmd/baha/target_mutation.go:71-77) en `Config.ResolveTarget` leest de Provider uit
cfg.Access (internal/deployment/target.go:533-541), dus `selected.AccessProvider == "local"`
en local_workload_authority.go:62 laat die Target WÉL door. Ik heb dit aan beide kanten
gemeten: develop-binary (8629450ef3c) faalt lokaal exact als de cel, en de fixture-waarde
komt uit de mapper niet uit de access-naam.

Het ECHTE, gemeten defect op deze workstation (bewijs onder "fix:"): de grant-check
vergelijkt `selected.Name` met de target-NAAM die de boundary doorgeeft; bij de bootstrap-
route (`authorizeTargetCreation`, mcp.go:408-415, eerste `target create` met lege config en
BASEHARBOR_TARGET=naam-van-nog-te-maken-Target) is die naam NOG NIET geregistreerd, dus
`effectiveTarget` kan hem niet resolven en de grant drop stil (local=false, geen error) —
waarna de boundary dezelfde operator-auth-tekst geeft. Met een AL bestaande lokale Target
loopt dezelfde adoptie gewoon door (gemeten: MCP app.adopt slaagt lokaal zodra de Target
één keer via de gebootstrapde route bestaat). Daarmee is de static-cell blokkade in de
volgorde "eerst target create, dan adopt" een bootstrap-grant-gat, niet een alias-gat.

Omdat de hunt-tekst (kaart 0428-243 acceptatie 1) uitdrukkelijk vraagt om de
local-workload-grant te verbreden naar de runtime-specifieke lokale access-vormen, en die
verbreding语义isch correct en risk-vrij is (de runtime-probe beslist alsnog), is de fix
precies daar aangebracht — plus een naamloze-alias-beoud:

fix: ONE additive commit op branch `lane-0428-231-static-opauth-fix` (base develop
`8629450ef3c5198bb675331c12f56b2c9377aa1c`): cmd/baha/local_workload_authority.go —
isLocalRuntimeAccessProvider() laat "local" EN "local-<runtime>" (local-docker/local-podman)
als host-local access-vormen toe in de grant-check; operator-auth blijft volledig intact
(geen boundary uitgeschakeld; tenant/remote/connector vallen nog steeds fail-closed; de
runtime-probe en de owner-dir checks blijven de echte autoriteit). De naamvergelijking
(selected.Name vs target) blijft ONVERANDERD fail-closed.

tag-noetig: nee — PRIMAIRE-FIX-ROUTE IS AANWEZIG ZONDER TAG, maar de static cell kan er
nu nog niet door: de cel faalt al bij de bootstrap `target create` (grant-drop op de
onbestaande naam). Met de tag (Owner-scope regel in pre-release-runtime-suite.yml) zou
withCIIntegrationOperator die bootstrap afdekken — de jacht zag dat PR #1746
(lane-0428-208-static-release-gate, "ci: run ci-fast-check in the release gate suite") de
statische cellen naar de pre-release-suite takkt; diens diff bevat precies de
testonly-binary route voor gates mét candidate_artifact. Zolang #1746 niet gemerged is, of
de static-gate stap de testonly-binary niet krijgt, is er méder nodig: de bootstrap-route
in de core (deze lane raakt die niet zonder extra review, want het is
grant-eligibility-semantiek). Meld dit als bevinding; GEEN .github-wijziging door deze lane.

## PLAN

1. (done) Realiteitsafgleich: develop=8629450ef3c; #1761 (andere 231-missie, helper fan-out)
   onaangeroerd gelaten; eigen branch lane-0428-231-static-opauth-fix van develop (merge-base
   bewijs + diff-list hieronder); QUESTION over branch-keuze was posted, board 8566e60b7
   ("0428-231 -> active (b90e4ba1): fix local_workload_authority.go:62") bevestigt losse fix;
   "EXACTLY ONE CANDIDATE PER CHAIN" → deze fix = eigen chain, niet PR #1761.
2. (done) Verify op current source: local_workload_authority.go:62 (toen nog één regel),
   target_mutation.go:71-77 mapper, internal/deployment/target.go ResolveTarget,
   mcp.go authorizeMCPOperation/authorizeTargetCreation; lokale repro met develop-binary
   (exact dezelfde fouttekst) en met fix-binary.
3. (done) Fix: additive grant-verbreding (boven), operator-auth intact.
4. (done) Regressie in BESTAAND e cmd/baha shard (geen nieuwe CI-job): subtest in
   TestVerifiedLocalRuntimeGrantSatisfiesManagedEnvironmentBoundary (local access-vormen +
   fail-closed set) en TestSourceAuthoringGrantsCoverLocalRuntimeAccessForms; routing:
   `PR · Go Tests · cli-N` shards verdelen Test* deterministisch (scripts/pr-go-unit-shard.py
   sha256 % 4), bestaande trigger pull_request→develop; uitgevoerd met named form
   (-skip RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication):
   alle drie tests ok op deze host (engine probe slaagt hier).
5. (in akte) Tag-vraag beantwoord: zie tag-noetig.
6. (done) Commit + push + PR (draft tot handoff); ls-remote bewijs.
7. (blocked-gerelateerd, zie END) Gehoste doorloop: statische gates draaien ALLÉÉN in
   Release · Pre-Release Validation (workflow_dispatch, inputs.tag+demo_ref =
   Owner/publish-autorisatie; Ordinary PR pushes runnen ze niet). Deze lane kan die
   niet startend (§ .github = Owner-scope, geen workflow_dispatch). PR CI (ci.yml) bewijst
   implementatie + regressie; de static-cell-groenheid is een owner-gate.

## Provenance

- base: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` =
  `8629450ef3c5198bb675331c12f56b2c9377aa1c`; branch以此为 base (`git merge-base
  --is-ancestor 8629450ef3c HEAD` OK; log list ONLY my commit).
- diff vs base: alleen `cmd/baha/local_workload_authority.go` en
  `cmd/baha/local_workload_authority_test.go`.
- remote guard: origin = https://github.com/mcpdev80/baseharbor.git (beide fetch/push).

## Local repro witnesses

- develop-binary (8629450ef3c) op deze host, exacte cel-shape (isolated XDG, geen
  DOCKER_HOST): `baha target create shell-ux-static --provider docker --access local-docker
  --reference local --scope default` → "Managed-environment machine operations require an
  authenticated BaseHarbor operator." (idem de gehoste job 137187053472).
- Met EEN existing lokale Target (na bootstrap) slaagt dezelfde MCP app.adopt direct
  (grant via de bestaande route) — daarmee: de fix-richting (grant op lokale access-vormen)
  is correct, de bootstrap-eligibility is het restant en vraagt aparte contractkeuze.

## repo-rule compliance

- Mutaies: plan→preflight→apply via normale PR/CI; geen secrets gelogd; geen .github/scripts
  gewijzigd (only cmd/baha/**); geen subagenten; worktree workers/0428-231-opauthfix-wt;
  GOCACHE under /var/tmp/go-cache-0428-231; geen containers op deze host gestart.

PR: https://github.com/mcpdev80/baseharbor/pull/1771 (draft, branch lane-0428-231-static-opauth-fix, head b57f3428b1bc690e1135a972c481d2f2962dc7ac, PR-CI run 45023442557 — deze akte is geschreven TERWIJL de run liep; run-uitkomst wordt na de run bijgewerkt in deze akte).

## cleanliness

cleanliness: read-own-zone only. Eigen pid (zie END-run van deze sessie). `docker ps -a`
BEFORE = 0 entries, AFTER = 0 entries. Geen compose/container gestart op deze host. Alle
repro-state zat in mktemp dirs under /var/tmp (auto-opschoon via trap; resten zijn lege
xdg-dirs in mktemp). Lane scratch /var/tmp/0428-223-* (baha binaries, traces, repros)
VERWIJDERD voor END. Werkboomen: 0428-231-authhelper-wt 0 delta; 0428-231-opauthfix-wt =
alleen deze branch commits; 0428-223-clean (develop-build voor repro) is door DEZE lane
aan het einde VERWIJDERD (git worktree remove, ls-remote-raakt niet aan refs).

END 0428-223-testctx DONE (0428-231 fix-round-1: defekt=bootstrap-grant-drop + jacht-alias-
these gecorrigeerd; fix=additive local_access-vormen in local_workload_authority.go;
tag-noetig: nee-voor-de-grant, wél-of-niet voor de cel via #1746-route — zie boven; PR
<nummer>, head <sha>, run <id>)

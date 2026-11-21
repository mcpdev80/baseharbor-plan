---
id: t-20261121-destroy-authority-stamp
card_number: "0428-214"
card_short_title: "0428-214 destroy stamp"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: active
kanban_lane: active
kanban_summary: "TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget shows which authority mode admitted installation.destroy, instead…"
kanban_title: 0428-214 · 0428-214 destroy stamp
priority: high
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1738]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1738"]
---

- [ ] t-20261121-destroy-authority-stamp · installation.destroy authorization assertion runs on a stamped context #task #release/v0-4-28 #status/active #view/active #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    **PR:** [baseharbor#1738](https://github.com/mcpdev80/baseharbor/pull/1738)  
    **Needs:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1738)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** coordinator  
**Priority:** high  
**PRs:** [baseharbor#1738](https://github.com/mcpdev80/baseharbor/pull/1738)  
**Source:** 
<!-- /generated:links -->

## Goal

`TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget` shows **which authority mode** admitted
`installation.destroy`, instead of printing an authorization green that its own stamp produced.

## Why

H-V23 section 1 (akte `evidence/bug-hunt-2026-11-21/fail-closed-honesty/round-1.md`, Karte A) is the single confirmed
falschlich-authentifiziert case: `cmd/baha/core_installation_runtime_test.go:323` asserts that the fixture cleanup context
is AUTHORIZED for `installation.destroy` in environment `prod`, inside a test whose contract is that cleanup authority is
bound to its local target. The context is stamped at `:298-306`
(`WithEnforcement` -> `WithVerifiedPrincipal` -> `WithMembershipProvider`), and `WithVerifiedPrincipal` implies
`WithEnforcement` (`internal/operatorauth/context.go:54-57`), so `internal/operatorauth/authorization.go:285` is
unreachable by construction. The green demonstrates the fixture, not production authority.

## Scope

Allowed write-set:

- `cmd/baha/core_installation_runtime_test.go`

Forbidden: production code, `internal/operatorauth/**` (Owner rail), every other `cmd/baha/` file — 0428-204 owns those
while it runs, so this card stacks behind it.

## Acceptance criteria

1. Either the authorization is asserted through the boundary the cleanup path really takes
   (`ensureOperatorAuthForBoundary`, `cmd/baha/operator_auth_boundary.go:55`), or the assertion moves to a positive-path
   test and the denial test stays unstamped.
2. The denial subtests (remote AccessProvider, unrelated verified principal) keep passing with the same assertions.
3. The output names the admitting mode (`authenticated` from a session, or `local-runtime` from the grant); an unstamped
   synthetic principal is not acceptable proof.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | Go unit shards for `./cmd/baha/` (PR Selected Checks) |
| Test identifier | `0428-214` |
| Route | `auto-discovery` |

## Dependencies

Needs the seam helper that 0428-204 introduces (content, not a merge wait). Do not commission while 0428-204 writes in
`cmd/baha/`.

## Stop and report

If the mode cannot be observed without touching `internal/operatorauth/**`, stop and report file:line.

## Handoff

Branch: `lane-0428-214-destroystamp` @ `ebc6ac9c3a3032a65256d285aeb510341820e218`
PR: #1738, base `lane-0428-198-cli-shard-operator-env` @ `7db142852d22` (chain rule 3.3.8, content wait on #1726)
Terminal hosted run: 44861212250 (PR Selected Checks aggregate SKIPPED — see evidence; per-shard Go unit runs executed my test, all pass)
Evidence:
`evidence/r28-welle4-2026-11-21/destroy-authority-stamp/round-1.md`.

kommissioniert auf dem freien ornith-sitz: branch vom head der basis-lane 0428-204 (7db142852d22), base-ref des PRs auf den lane-branch 'lane-0428-204-cli-operator-entrypoints'. write-set genau eine datei: cmd/baha/core_installation_runtime_test.go. konfliktfrei gegen 213 und 207. lane 5b17f066, modell verifiziert.

214-lane nannte PR #1738 im feld 'PR', aber 'prs:' war leer; prs gefuellt. gemessen: refs/heads/lane-0428-214-destroystamp = ebc6ac9c3a30, merge-base --is-ancestor 7db142852d22 <head> = 0, eine eigene datei, base-ref = lane-0428-198-cli-shard-operator-env.

kandidat vollstaendig und gemessen: head ebc6ac9c3a30, base-ref 'lane-0428-198-cli-shard-operator-env' @ 7db142852d22 (ketten-regel), draft=false. der ECHTE durchgang 44862425216 (von MIR per undraft ausgeloest) ist terminal: policy/Trusted Plan/Native gate plan/Source format/Focused Python/cli-vet/cli-build/cli-gofmt/source-contracts = SUCCESS, 'PR · Go unit · cli-0..3' = failure (geerbte operator-auth-klasse; scheitert ebenso an der basis #1726). mein eigener grep am protokoll: '--- FAIL: TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget' = 0 zeilen, der karten-fall scheitert also in KEINEM ausgefuehrten shard. reichbarkeits-beleg der lane: 'authorization.go:235' (claim-membership-ast) nur mit verified principal + provider. PROTOKOLL-VERSTOSS FESTGEHALTEN: die lane hat ihre END-zeile per 'codeman agent post 9142ab1f-…' an mich gepostet — genau das ist verboten (AGENTS 3.3.4, die meldung laeuft ueber den watch-pfad, nicht ueber post an eine fremde session). folge: sitz wird freigegeben (rotation), arbeit bleibt gutgeschrieben.

kette nachgezogen, von mir gemessen: head bdc3fcb63912, base 'lane-0428-198-cli-shard-operator-env' (basis-head beim rebase c2f9f2f32fd6, seitdem e45430f2f1b7 — fuenfter owner-push), 'merge-base --is-ancestor' = 0, draft=false; eigener durchgang terminal: run 44867291850 / 44867319394 completed/failure, cli-shards geerbt. WICHTIG FUER DIE ABNAHME: PR Selected Checks faehrt einen pr_merge-commit (85ae26150145 = 'Merge <head> into <base>'), 'exact-head' heisst bei gestapelten PRs der merge, nicht der branch allein. Akte round-3-chainrebase.md (plan 38b79bce).

CODEX-REVIEW 'Verdict: REQUEST CHANGES' (destroy-authority-stamp/review-1.md, origin/main b3816e18/b33d3e3f) an head bdc3fcb63912: P1 = die behauptete RUECKNAHME des eigen-stempels ist im kandidat NICHT enthalten — 'cmd/baha/core_installation_runtime_test.go:294-306' reicht den bereits gestempelten kontext weiter, die neue assertion ':332-346' ruft zwar die produktions-grenze, nutzt aber denselben kontext. Rezept des reviewers: teardown-only fixture-kontext und authority-assertion trennen (':274-306', ':309-346'). P2 zaehlt GENAU DREI erste-level-FAIL-zeilen am durchgang 44867319394 (log 903158 bytes, log-failed 16321) und sagt ausdtruecklich: 'not to be booked as a generic inherited gate class — the exact gate text is absent'. Die drei: (1) 'app_list_all_targets_test.go:26' = karte 0428-210/#1739; (2) 'secure_profile_export_command_test.go:125' 'operator authentication needs interactive setup' (textquelle 'cmd/baha/operator_auth_boundary.go:117'); (3) 'target_hotfix_test.go:201' 'target "edge-a" is not configured'. IHR eigenen fall scheint im protokoll NICHT als fail — was der reviewer als P2-notiz festhaelt, und der grund, warum ich sie zurueck auf 'active' setze statt auf 'review'.

korrektur-lane '0428-214-stampfix' (2dfa5466, ornith) dispatcht; ihr auftrag fuehrt das rezept des reviewers wortlich (trennung von fixture-teardown-kontext und authority-assertion, ':274-306' und ':309-346'), dazu der reichweiten-beweis in beide richtungen als vorbild aus #1741 und die rot-zuerst-pflicht mit STOP-kriterium.

meine entscheidung UBER den gemeldeten blocker der lane (END_BLOCKED, und sie hatte recht): das rezept des reviewers zielt auf einen ast, den es am ziel nicht geben kann. gemessen: 'coreBootstrapFixtureCleanupContext' ('cmd/baha/core_installation_runtime_test.go:274-300') ist ausdruecklich test-only teardown MIT synthetischem editor-principal (kommentar ':297-299': 'production auth and local-runtime authorization paths remain unchanged'; ':279-281' verbieten wiederverwendung eines unrelated principal), und 'installation.destroy' fehlt in 'operatorauth.LocalWorkloadOperation' — darum liefert 'verifiedLocalWorkloadAuthority' ('cmd/baha/local_workload_authority.go:41-59') 'local=false'. DIE gesuchte authority lebt und ist getesteT: 'application_destroy_authorization.go:29-38' (operation='installation.destroy' nur mit 'installationApplicationScope'-proof) -> 'installation_application_scopes.go:23-45' (gerufen in 'runtime_destroy_all.go:103', 'management_remote_installation_destroy.go:80'), unit-abgedeckt in 'installation_application_scopes_test.go:23/:27/:58' + 'installation_sibling_scope_test.go:42/:77/:82'. Auftrag an die lane: assertion auf DEN mechanismus verlagern (positive + negative richtung), teardown-stempel bleibt unangetastet. Karte bleibt 'active', ein PR (#1738).

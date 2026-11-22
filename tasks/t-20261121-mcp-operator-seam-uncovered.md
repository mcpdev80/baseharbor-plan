---
id: t-20261121-mcp-operator-seam-uncovered
card_number: "0428-218"
card_short_title: "0428-218 mcp operator seam"
type: bug
areas: [cli, observability]
release: v0.4.28
version: ""
parent: ""
owner: coordinator (karte) / erster freier worker-sitz (ausfuehrung)
kanban_status: wait
kanban_lane: wait
kanban_summary: Every MCP mutation path whose test expects the verbatim gate message Managed-environment machine operations require an…
kanban_title: 0428-218 · 0428-218 mcp operator seam
priority: normal
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1741, mcpdev80/baseharbor#1738]
sources: []
blocker: ""
wait_reason: "carrier-abhaengigkeit ja; neue basis ist develop 8629450ef3c, der delta wird dort neu geschnitten - die alte PR-basis bleibt nicht in gebrauch"
resolution: ""
created: "2026-11-21T05:55:00Z"
updated: "2026-11-21T05:55:00Z"
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/operator-auth-helper/carrier-census-1737-1738-1740-1741.md"]

---

- [ ] t-20261121-mcp-operator-seam-uncovered · 0428-218 make the MCP operator seam reachable from MCP tests #task #release/v0-4-28 #status/wait #view/wait #area/cli #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator (karte) / erster freier worker-sitz (ausfuehrung) · **Priority:** normal  
    **PR:** [baseharbor#1741](https://github.com/mcpdev80/baseharbor/pull/1741), [baseharbor#1738](https://github.com/mcpdev80/baseharbor/pull/1738)  
    **Waiting:** carrier-abhaengigkeit ja; neue basis ist develop 8629450ef3c, der delta wird dort neu geschnitten - die alte PR-basis bleibt nicht in gebrauch  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/operator-auth-helper/carrier-census-1737-1738-1740-1741.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** coordinator (karte) / erster freier worker-sitz (ausfuehrung)  
**Priority:** normal  
**PRs:** [baseharbor#1741](https://github.com/mcpdev80/baseharbor/pull/1741), [baseharbor#1738](https://github.com/mcpdev80/baseharbor/pull/1738)  
**Source:** 
<!-- /generated:links -->

Source: BUG-HUNT slice H-V29 (coordinator/BUG-HUNT.md), akte `evidence/bug-hunt-2026-11-21/seam-reachability-desk/round-1.md` (plan ab9b5822).

## Goal

Every MCP mutation path whose test expects the verbatim gate message
`Managed-environment machine operations require an authenticated BaseHarbor operator`
(`internal/operatorauth/authorization.go:285`, `cmd/baha/mcp.go:301`) actually reaches that refusal in CI, so the assertion is
made on a production-reachable arm.

## Why

BUG-HUNT H-V29 (`evidence/bug-hunt-2026-11-21/seam-reachability-desk/round-1.md`, plan `ab9b5822`) measured, with file:line,
that `authorizeMCPOperation` (`cmd/baha/mcp.go:268-335`) does not route through `runWithIO`: in `runWithIO`
(`cmd/baha/main.go:134-172`) there is exactly one `WithEnforcement` call (line 153) and it sits before the fixture call, so no
`testOperatorContext` exists on the MCP side. Consequence for the coverage map: class C (10 MCP cases) is not healed by the
owner's central helper in #1615, while class A (80 predicted statically, 79 measured between runs 44863102857 and 44862425216)
is. Because `WithVerifiedPrincipal` implies `WithEnforcement` (`internal/operatorauth/context.go:54-57`), a test that stamps a
verified principal through the fixture silences the refusal it later asserts - the honesty rubric already charged twice today
calls that equal to `err != nil`.

## Scope

Allowed write-set:

  - `cmd/baha/mcp.go` - only the operator-seam arm reached from the MCP mutation entry points
  - `cmd/baha/mcp_test.go` and the `cmd/baha/app_mcp_*_test.go` files named by class C
  - this card's evidence folder in baseharbor-plan

Forbidden:

  - `internal/operatorauth/**` (Owner rail) - if the fix needs it, STOP and report file:line
  - `internal/capability/perses.go`, `cmd/baha/machine_coverage.go` (held by the #1599 lane)
  - `.github/**`
  - any change to a refusal's message, status code or semantics: this card makes existing refusals reachable in tests

## Acceptance criteria

  - Every MCP mutation entry point that reaches `authorizeMCPOperation` is listed, each with a file:line statement of whether
    the operator-auth gate is reachable on the production path.
  - Each class-C test passes in a hosted CI run at the candidate head by observing the gate message, and turns red when the
    fixture stops stamping a principal (mutation proof, not assertion proof).
  - `git diff develop -- internal/operatorauth/` is empty at the candidate head.
  - New tests are covered by an existing CI selection rule; if a rule must change, report it as a file:line finding instead of
    editing `.github/**`.

## Stop criteria

  - The fix requires `internal/operatorauth/**`: STOP and report - Owner rail, coordinator decides.
  - The gate is genuinely unreachable from MCP mutations in production (not only in tests): STOP, this is a security-relevant
    finding for the Owner, not a test fix.
  - Hosted logs unavailable at the candidate head: report the three commands (`gh run view --log`, `--log-failed`,
    `--job <id> --log`) with their byte counts; do not substitute a local run.

## Handoff

Evidence: `evidence/r28-welle4-2026-11-21/mcp-operator-seam/round-1.md`. Base lane: `lane-0428-198-cli-shard-operator-env`
(card 0428-204) per the stacking rule - wait on content, never on merges. Counting law from H-V26: count distinct first-level
`--- FAIL: Test` names (108), not gate-message lines (128); see
`evidence/bug-hunt-2026-11-21/numbers-forensics/round-1.md`.

delivered, abnehmbar: PR #1741 head de4a45ec5ca6, base 'lane-0428-198-cli-shard-operator-env', von MIR undrafted (draft=false gemessen nach GraphQL markPullRequestReadyForReview — ein draft hat keine required checks), der vorherige durchgang 44871830116 am selben head war 'failure', jetzt laeuft 44873244947 (in_progress, 'pull_request'): workflow-policy / native gate plan / Trusted Plan / Source format / Focused Python / go-build / go-vet / 'Go unit · owner' SUCCESS, cli-0/1/3 in arbeit. write-set = GENAU 'cmd/baha/mcp_operator_seam_test.go' (diff gegen e45430f2f1b7 gemessen), stack-beleg 'merge-base --is-ancestor e45430f2f1b7 de4a45ec5ca6' = 0. AKTE '…/mcp-operator-seam/round-1.md' (plaene 0c1f22dd, b4ff4638) haelt die eintragstabelle je MCP-aufrufstelle + 'withoutOperatorAuthTestContext'-befund, und sie hat meinen fehler zwei MAL korrigiert: ihr reichweiten-beweis war es, der meine karte 0428-218 auf den echten kern schmaelte ('der seam fehlt' war falsch, 'die faelle stempeln statt zu markieren' ist wahr). BEFUND, der an die abnahme geht: die commits am PR tragen 'Worker w206 <w206@baseharbor.local>' — ein toter baum wurde wiederverwendet (werkzeug-issue #23), die autorschaft ist also nicht ihr zeuge, ihr session-zeuge steht in der akte.

CODEX-REVIEW 'review-1.md' (plan 9ac0a0cd + 577bd6a8) = 'Verdikt: REQUEST CHANGES', ein einziger inhaltlicher befund. Richtig ist dran: reichbarkeit PASS (echter 'workspaceMutationClientWithContext'-ueber 'CallTool'), BEIDE richtungen PASS (gestempelt = erfolg, anonym = 'authentication_failed'), CI-ROUTING PASS — der fall haelt per 'scripts/pr-go-unit-shard.py' auf cli-3 und ist am head ausgefuehrt (durchgang 44873244947, job 136752270714 success). BEFUND: 'cmd/baha/mcp_operator_seam_test.go:78-87' dekodiert nur 'error.code', die EXAKTE gate-zeile fehlt — der produkt-text kann sich aendern, der fall bleibt gruen. Rezept an die Lane (6c…neue lane 0428-218-msgassert): 'Message string' in die dekodierte form + exakte gleichheit im anonymen request, mutation ROT bei text-aenderung, und — weil zwei kolleginnen heute genau dort gescheitert sind (issue #24) — basis-nachzug MIT 'merge-base --is-ancestor'-beleg VOR dem push. ERBSCHAFT, vom reviewer mit gleichem basis-durchgang 44867737078 belegt: cli-0 = 'TestAppListAllTargetsWorksAfterInstallationDestroy' (0428-210/#1739), packages = 'TestPersesLokiDatasourceMultiSource*' wegen fehlendem 'providers/loki/shared/service-access/pki/client-cert.pem' (owner-stapel #1615). Aggregate bleibt failure bis 'PR Selected Checks' success.

test 218

probe

CODEX-REVIEW 'review-1.md' (plan 9ac0a0cd + 577bd6a8) = REQUEST CHANGES, ein inhaltlicher befund. RICHTIG IST: reichbarkeit PASS (echter 'workspaceMutationClientWithContext' ueber 'CallTool'), BEIDE richtungen PASS (gestempelt = erfolg, anonym = 'authentication_failed'), CI-ROUTING PASS — der fall haelt per 'scripts/pr-go-unit-shard.py' auf cli-3 und wurde am head ausgefuehrt (durchgang 44873244947, job 136752270714 success). BEFUND: 'cmd/baha/mcp_operator_seam_test.go:78-87' dekodiert nur 'error.code'; die EXAKTE gate-zeile fehlt, der produkt-text kann sich aendern und der fall bleibt gruen. Lane 0428-218-msgassert (0e89ddd7, laptop) arbeitet: 'Message string' in die dekodierte form + exakte gleichheit im anonymen request + mutation-beleg (text rot, zurueck gruen). ZUSATZ-PFLICHT, weil zwei kolleginnen heute genau dort gescheitert sind (issue #24): basis-nachzug MIT 'merge-base --is-ancestor'-beleg VOR dem push. ERBSCHAFT vom reviewer mit gleichem basis-durchgang 44867737078 belegt: cli-0 = 'TestAppListAllTargetsWorksAfterInstallationDestroy' (0428-210/#1739), packages = 'TestPersesLokiDatasourceMultiSource*' wegen fehlendem 'providers/loki/shared/service-access/pki/client-cert.pem' (owner-stapel #1615). Der aggregate bleibt failure, bis 'PR Selected Checks' success zeigt.

FORTLAUFEND, SHA-NACHTRAG (Pflicht 3.7): neuer head fb5a5deaf36b auf 'lane-0428-218-mcp-operator-seam' (08:54, author '0428-218-msgassert' = korrekte identitaet, issue #23 ist bei ihr aufgehoben), commit-Text 'test(0428-218): pin exact operator-auth denial…' = der eine reviewer-befund (exakte 'error.message'-gleichheit in 'cmd/baha/mcp_operator_seam_test.go:78-87'). GEHOSTET AM NEUEN head: 'PR · Trusted Plan' = SUCCESS, die sechs Go-unit-zellen (cli-0..3, packages, owner) = in_progress, 20 skipped (pfadfilter), 'PR Selected Checks' noch offen. Zwei commits seit der basis, beide ihrer karte. Ich buche auf 'review', sobald 'PR Selected Checks' terminal success ODER mit begruendeter erbschaft-buchung + meinem gruenen aggregate-nachweis appears.

SHA-NACHTRAG + buchung: neuer head fb5a5deaf36b (08:54, author '0428-218-msgassert' = korrekte identitaet) enthaelt den einen reviewer-befund: 'error.message' wird dekodiert und EXAKT verglichen in 'cmd/baha/mcp_operator_seam_test.go'. GEHOSTET AM NEUEN head (von mir gemessen): 'PR · Trusted Plan' success; 'Go unit · cli-1/cli-2/cli-3/owner' success — der fall haelt auf cli-3 und ist dort GRUEN; 'cli-0' + 'packages' failure; 'PR Selected Checks' failure mit 20 skipped (pfadfilter). Die zwei roten zellen sind dieselbe erbschaft, die der reviewer selbst am gleich-basis-durchgang 44867737078 belegt hat (cli-0 = 0428-210/#1739, packages = loki pki 'service-access/client-cert.pem' owner-stapel #1615). Karte damit 'review': abnahme faehig am inhalt, aggregate abhaengig von #1739 und #1615.

r2 delivered, von mir am remote gemessen: head fb5a5deaf36b, nachkomme von e45430f2f1b7, 2 commits (beide ihrer karte), author '0428-218-msgassert' (KEIN toter name). Die exakte gate-zeile ist jetzt angehangen in 'cmd/baha/mcp_operator_seam_test.go' (ihr eigener befund 1 aus review-1.md). GEHOSTET: cli-1/cli-2/cli-3/owner success — ihr fall gruen in cli-3 (durchgang 44882418434); cli-0 + packages failure; 'PR Selected Checks' failure; 20 skipped (pfadfilter). Sie meldet 'BLOCKED for coordinator' statt fremde dateien anzufassen = richtige eskalationsform. WAS WIRKLICH BLOCKIERT (von mir benannt): die stapel-basis 'lane-0428-198-cli-shard-operator-env' = e45430f2f1b7 enthaelt #1615 NOCH NICHT; der owner hat #1615 um 08:08 in develop gemergt (9bd76324ec6d). Bis diese basis auf den neuen develop hoppt, bleibt die gate-klasse an allen stapel-kandidaten (#1737/#1738/#1741) rot — und kein meiner Lanes darf das selbst beheben, weil ein basis-hop owner-aktion ist. Review r2 laeuft bereits (95971e0a).

CODEX-REVIEW r2 'review-2.md' (plan 14309cf0 + 2ca4c07b + f624354a) = 'Verdikt: REQUEST CHANGES', aber der einzige offen punkt ist NICHT ihr inhalt: anerkennungspunkte 1-4 sind PASS — reichbarkeit/beide richtungen PASS, EXAKTE nachricht PASS (dekodiertes 'Error.Message' gleich der produktquelle inkl. punkt am ende, 'authentication_failed' + fehlender principal behalten, befund 1 aus r1 DAMIT GESCHLOSSEN), mutation PASS (text geaendert = rot, zurueck = gruen), CI-ROUTING PASS (cli-3 job 136780430782 success, 'Trusted Plan' + 'Native gate plan' success). PUNKT 5 = 'Required checks: FAIL': durchgang 44882418434 terminal failure, 'PR Selected Checks' job 136781570119 failure, cli-0 job 136780430791 + packages job 136780430748 failure — und der reviewer selbst bucht das als SAME-BASE erbschaft. Byte-zahlen aus per-job-logs, wie verlangt (894134 / 35949 / 45764 / 66915 / 44206). Karte bleibt 'review' (inhalt abnahme-faehig), der weg zum gruenen aggregate fuehrt ueber den BASIS-HOP der lane-0428-198 auf develop 9bd76324ec6d (#1615 ist dort seit 08:08 gemergt), nicht ueber eine weitere korrekturrunde dieser lane.

r5 plus rebase auf e45430f2 (delta eine datei, head 7e6792939c55). Der aufruf von authorizeMCPOperation mit installation.destroy steht im TEST, nicht im produktionspfad der bootstrap-aufraeum-route. cli-0 zeigt denselben einen fremden fallen wie 1737.

ROUTE NEU FESTGELEGT NACH CENSUS (akte operator-auth-helper/carrier-census-1737-1738-1740-1741.md, plan commit da2176f7f40, von 1450c201 gemessen): PR 1726 wird NICHT wieder eroeffnet und es entsteht KEIN neuer traeger - #1750 ist gemergt, also wird der JEWEILIGE eigene delta des kandidaten auf develop 8629450ef3c neu geschnitten. Fernzeugnis der kinder: alle back=275, mergeStateStatus UNSTABLE, base zeigt auf die tote basis lane-0428-198-cli-shard-operator-env (spitze e45430f2f1b). Carrier-abhaengigkeit: ja. Ihr PR-head gemessen: 1741 siehe akte 'Child PR state and diff against the named carrier'. Naechster schritt: mission auf dem ersten freien arbeits-sitz (neu schneiden statt hoepfen; bei 'nein' reicht der additive hop), dann exact gehosteter durchgang + unabhaengige pruefung. Kein merge aus der alten basis heraus.

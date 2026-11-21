---
id: t-20261121-all-targets-config-loss
card_number: "0428-210"
card_short_title: "0428-210 all-targets config"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: review
kanban_lane: review
kanban_summary: "TestAppListAllTargetsWorksAfterInstallationDestroy passes: after an installed-to-destroyed transition the all-targets inventory…"
kanban_title: 0428-210 · 0428-210 all-targets config
priority: normal
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1739]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261121-all-targets-config-loss · 0428-210 all-targets inventory depends on a deleted Target config #task #release/v0-4-28 #status/review #view/review #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** normal  
    **PR:** [baseharbor#1739](https://github.com/mcpdev80/baseharbor/pull/1739)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Required by:** [t-20261121-target-hotfix-inspection-config-missing](t-20261121-target-hotfix-inspection-config-missing.md)  
**Owner:** coordinator  
**Priority:** normal  
**PRs:** [baseharbor#1739](https://github.com/mcpdev80/baseharbor/pull/1739)  
**Source:** 
<!-- /generated:links -->

## Goal

`TestAppListAllTargetsWorksAfterInstallationDestroy` passes: after an installed-to-destroyed transition the all-targets
inventory still reports the targets it is supposed to report, instead of failing with
`all-targets inventory depended on deleted Target config: BaseHarbor config root is configured but the config.yaml ...`.

## Why

w216 reported this while working 0428-204 and correctly refused to fold it into that PR: the failure is **not**
operator-auth. w221 had grouped it as `cmd/baha/app_commands.go:106` (akte
`evidence/r28-welle4-2026-11-20/other-domain-test-split/round-1.md`, group 9, one test) but labelled it covered by the
0428-204 card. The measured error line disproves that: it is a lifecycle/config-lookup defect, so it needs its own card
and its own PR (one card, one PR).

## Scope

Allowed write-set:

- `cmd/baha/app_commands.go`
- `cmd/baha/app_list_all_targets_test.go`
- the Target-config lookup they call from there (report the file before editing if it leaves `cmd/baha/`)

Forbidden: `internal/**`, `.github/**`, `scripts/**`, and every other `cmd/baha/` file while 0428-204 runs.

## Acceptance criteria

1. The named test passes at the exact candidate head, for the right reason: the inventory no longer reads a deleted
   Target config, or the destruction path keeps the record the inventory needs (state which in the handoff).
2. A regression proves the chosen behaviour across the installed-then-destroyed sequence.
3. The first failing line before and after is quoted verbatim in the evidence.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | Go unit shards for `./cmd/baha/` (PR Selected Checks) |
| Test identifier | `0428-210` |
| Route | `auto-discovery` |

## Stop and report

If the fix requires touching the destroy/retirement consent path (`cmd/baha/application_destroy_authorization.go`) or any
Owner rail, stop and report file:line.

## Handoff

Branch, PR, exact head SHA, terminal hosted run id, evidence
`evidence/r28-welle4-2026-11-21/all-targets-config-loss/round-1.md`.

kommissioniert auf dem zweiten laptop-sitz als folge-lane der kette 0428-204: branch vom head 7db142852d22, base-ref des PRs auf den lane-branch der basis-lane. write-set cmd/baha/app_commands.go und cmd/baha/app_list_all_targets_test.go, konfliktfrei gegen 213/214/207. vorgeschaltete meldepflicht:  overlap mit #1615 (head 5466a87bffe1) in denselben dateien wird vor dem ersten schreiben geklaert, weil #1615s versuch 44854729670 44854729670 die cli-shards bereits gruen macht.

stacking-entscheid von mir, nach messung: PR-BASIS = develop 40cb28c758b0 (drei wege gemessen: ls-remote https, ls-remote lane-origin, gh api commits/develop = der #1594-merge vom 20.11. 16:06:23Z). NICHT hinter #1615 (owner-schiene, OPEN, head 231ebd269735, 'mergeable' ist deren PR nicht develop) und NICHT auf #1726 (geerbte gate-wand, andere dateien). grund: ihre lane hat den fall AM develop-head reproduziert, und 210 ist der PRODUKTIONS-fall der trennung GATE/BEWEIS/PRODUKTION. ueberschneidung mit #1615 in beiden dateien wird orthoogonal gehalten + 'OVERLAP'-zeile im PR-body fuer meine merge-reihenfolge.

kandidat vollstaendig, gemessen: head 79d962a063be, base develop 40cb28c758b0, draft=false, write-set GENAU eine datei ('cmd/baha/app_commands.go': '--all-targets' toleriert 'deployment.ErrConfigMissing' aus 'authorizeCurrentMCPContext'). durchgang 44863102857 terminal: workflow-policy / Trusted Plan / Native gate plan / Source format / go-vet / go-build / Focused Python = SUCCESS, 'PR · Go unit · cli-0..3' + packages = failure (geerbt). MEIN GREP AM PROTOKOLL: '--- FAIL: TestAppListAllTargetsWorksAfterInstallationDestroy' = 0 zeilen -> der karten-fall scheitert im gehosteten shard NICHT. NEUE ZAHL FÜR H-V26: eindeutige first-level-namen an DIESEM kandidaten = 196, am gestapelten #1726-head 117. differenz 79 = genau die klassen-groesse A(80) der deckungskarte: der seam-inhalt nimmt 79 gate-faelle weg. das ist die erste zahl, die zwei methoden unabhaengig bestaetigen. hinweis in der akte: die regression wurde LOKAL proven (FAIL->PASS), weil auf diesem host der ambient stapel fehlt (MEIN fehler, 03:0xZ) — der gehostete belegtraeger ist der 0-FAIL-nachweis oben.

CODEX-REVIEW an #1740 (native-cell-operator-seam/review-1.md, plan auf origin/main) spricht ES aus: 'Verdict: APPROVE CONTENT — PR Selected Checks remain failed on unrelated 0428-210 test' (P2, zeile 41-51). Von mir nachgemessen am protokoll 44868911131: die einzige erste-level-FAIL-zeile ist 'TestAppListAllTargetsWorksAfterInstallationDestroy' (cli-0, 'Exit: 1', ##[error]Process completed), gate-text-zeilen = 0 — also KEIN operator-auth-erbe, sondern IHR fall, auf dem gestapelten branch 'lane-0428-198-cli-shard-operator-env', wo Ihr fix ('cmd/baha/app_commands.go') nicht mitspielt. Karte zurueck auf 'active': naechster freier sitz klaert, ob (a) ihr tolerieren von deployment.ErrConfigMissing auf diesem branch einen ANDEREN fehlerpfad sieht oder (b) die regression auf develop doch nicht greift. STAND PR #1739: head 79d962a063be, base develop, draft=false, durchgang 44863102857 cli-0..3+packages failure.

probe

Ursache des bildes an ihrem PR, von mir gemessen: develop ist weitergegangen (40cb28c758b0 nach d2d4ded3dedb, owner 21.11 08:17, 'docs: clarify app new create-only registration'); ihr head 79d962a063be hat 40cb28c758b0 als eltern, und 'gh pr view 1739 --json mergeStateStatus' sagt BEHIND. Am jetzigen head sind 46 fan-out-eingaenge skipped und 'PR · Trusted Plan' selbst skipped — es gibt ALSO keinen vollstaendigen required-durchgang an diesem kandidat (die zwei aelteren durchgaenge 44863102857 und 44863237535 liefen gegen den alten develop). Ihr commit traegt zusaetzlich den author 'lv4-verify' aus einem TOTEN working tree (issue #23/#24), deshalb neue lane mit identitaets- und symptom-test vor dem push. KRITISCHER PFAD: ihr fall 'TestAppListAllTargetsWorksAfterInstallationDestroy' ist die rot-zeile in cli-0 an #1738 UND #1741, die der reviewer als erbschaft bucht — heilt #1739, heilt diese zwei mit. Mission liegt fertig in coordinator/missions/0428-210-rebase-develop.md (payload-gate 0) und geht auf den ersten freien sitz vor 0428-214.

HOP ANGEKOMMEN, UND ALS ERSTER KANDIDAT DIESES FENSTERS MIT VOLSTAENDIG GRUENEM REQUIRED-AGGREGAT (von mir gemessen): durchgang 44885264462 ('CI · Source & Quality') am head 6442955f4cf0 = completed/success; die zellen 'PR · Trusted Plan', 'PR · Native gate plan', 'Workflow policy', 'PR · Source format', 'PR · Focused Python', go-build, go-vet UND cli-0, cli-1, cli-2, cli-3, packages, owner = ALLE success; check-run-stand 14 success / 20 skipped / 0 failure. Damit ist der buchhaltungs-streit des abends ENTSCHEDEN: die cli-0-gate-klasse und die loki-pakete-roete waren ERBSCHAFT von #1615/#1734, und ein hop auf den #1615-haltigen develop laesst sie verschwinden, OHNE dass eine karte eine fremde datei anfasst. Konflikt loesste sie ausschliesslich in 'cmd/baha/app_commands.go', #1615-inhalt unangetastet, PR von CONFLICTING nach MERGEABLE. ZWEI einschaenkungen, von mir gemessen: (1) develop lief unter ihr weiter (jetzt 5b26be1ccfc5), merge-base ist 9bd76324ec6d — ein weiterer hop ist vor dem merge faellig, 'mergeable' meldet gerade UNKNOWN; (2) der commit-author ist '0428-210-hopfix3', obwohl die lane hopfix4 heisst (eine-ziffer identitaets-drift, familie issue #23).

probe

probe 2

CODEX-REVIEW review-1.md = REQUEST CHANGES. Punkt 2 ist sicherheitsrelevant, von mir am quelltext gelesen: develop nutzt am all-targets-arm 'authorizeMCPOperation(ctx, app.list, dev)' (kommentar: authenticate the operator without requiring an effective Target that no longer exists); der head 6442955f4cf0 ersetzt das durch 'authorizeCurrentMCPContext' und verwirft 'deployment.ErrConfigMissing', damit kann die authorisierung am fehlenden target nicht entscheiden. Der gruene durchgang 44885264462 gilt einem ueberholten develop-stich (5b26be1ccfc5, jetzt c2c94ad115ff). Neue lane 0428-210-authzkeep (92fd9d3a, ornith): hop auf gemessenen develop, develop-seite der authorisierung behalten, ErrConfigMissing erst nach der authorisierung tolerieren, negativer anonym-fall mit exakter gate-zeile, mutation (unterschlagen vor authorisierung = rot). Empfehlung an den owner: #1739 nicht mergen bis der neue head den gruenen aggregate plus den negativen fall hat. Ausfuehrlich in coordinator/QUEUE.md row 882.

korrekturrunde 5 auf derselben lane (92fd9d3a). Am head aba052ad2b66 gelesen: authorisierung ist develop-seitig wieder da (app_commands.go:131-137 mit dev-transport fuer allTargets), die einzige ErrConfigMissing-toleranz sitzt in zeile 205 NACH der authorisierung, delta gegen merge-base = genau zwei dateien. Run 44891459252 = 15 success / 20 skipped / 0 failure, cli-0..3 success, PR Selected Checks success. Zwei offen: (a) app_list_all_targets_test.go:58 prueft den gate-text mit strings.Contains statt wörtlich, (b) head ist kein descendant von develop 53f16a81f23a, also rebase plus new evidence

korrekturrunde 5 geliefert und von mir am head 52866ae38f97 nachgelesen: app_commands.go:131-137 traegt wieder die develop-form (authorizeMCPOperation mit dev-transport fuer allTargets), die einzige ErrConfigMissing-toleranz in :205 NACH der authorisierung, delta gegen merge-base = genau zwei dateien. Teststelle :58 prueft jetzt strings.EqualFold mit dem wortlichen gate-text inkl. endpunkt, der negative anonym-fall TestAppListAllTargetsStillRequiresAuthorizationWithoutTargetConfig ist da (mutation ohne endpunkt = ROT belegt). Durchgang 44892971526 completed/success am genau diesem head (35 jobs, cli-0..3 success, PR Selected Checks success). develop laeuft weiter (53f16a81f23a -> 4fa5293a49b7), also gilt der aggregate nur im merge-fenster; letzter hop vor merge ist in der abnahme-bitte an codex ausdruecklich genannt.

CODEX-REVIEW review-2.md (plan eaac03dc, ROLLE: REVIEW, 2026-11-21 10:27 UTC, backend Codex API) = APPROVE CONTENT. Befund 2 ist am head 52866ae38f97 von der reviewerin selbst am quelltext belegt: app_commands.go:131-137 ruft authorizeMCPOperation mit app.list und managed dev fuer allTargets, die einzige errors.Is(err, deployment.ErrConfigMissing) sitzt in :205 NACH der authorisierung, und app_list_all_targets_test.go:35-64 prueft den anonymen fall mit strings.EqualFold inkl. endpunkt; der diff beruehrt nur die zwei erlaubten dateien. MERGE-BEDINGUNG: ein letzter hop auf den dann gemessenen develop plus ein successful exact-head required run. Dafuer setze ich jetzt eine hop-lane, keine produkt-aenderung.

CODEX-REVIEW 'review-3.md' (plan a7ed911d und 588e5f4c, ROLLE: REVIEW) = 'APPROVE CONTENT - exact candidate bb98e22599ab1f77edc056de73c682fdfdedd88a'. Von mir am remote nachgelesen: 'no remaining findings in the reviewed diff', 'Merge PR #1739 first in this window: its base is develop and no stack depends on it'. Zeugen im dokument: develop 77c1e60f51b91003ac3ddc391008c15e4a713a5c, PR API state=open draft=false mergeable=true mergeable_state=clean, compare status=ahead mit den zwei commits ba46249f007a (post-auth toleranz + anonymer regression) und bb98e22599ab (final hop). Ich habe daraufhin die CODEX-MERGE-rolle beauftragt (andere rolle, ausdruecklich als ROLLE: MERGE gekennzeichnet). Bemerkung am rande, die ich nicht unterschlage: die verdict-dateien im plan-repo tragen den auteur '0428-210-authzkeep' — eine von mir freigegebene lane — der vierte live-beweis fuer tooling-issue #24 (geteilte checkout-identitaet, nicht die session).

---
id: t-20261121-trust-uninstall-false-green
card_number: "0428-213"
card_short_title: "0428-213 trust-uninstall EOF"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: active
kanban_lane: active
kanban_summary: "TestTrustUninstallPromptEOFRejects, TestTrustUninstallPromptUnterminatedAffirmativeEOFRejects and…"
kanban_title: 0428-213 · 0428-213 trust-uninstall EOF
priority: high
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1737]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261121-trust-uninstall-false-green · trust-uninstall EOF tests are green on the auth gate error #task #release/v0-4-28 #status/active #view/active #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    **PR:** [baseharbor#1737](https://github.com/mcpdev80/baseharbor/pull/1737)  
    **Needs:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** coordinator  
**Priority:** high  
**PRs:** [baseharbor#1737](https://github.com/mcpdev80/baseharbor/pull/1737)  
**Source:** 
<!-- /generated:links -->

## Goal

`TestTrustUninstallPromptEOFRejects`, `TestTrustUninstallPromptUnterminatedAffirmativeEOFRejects` and
`TestTrustUninstallPromptEOFAbortsCleanly` prove the **prompt path** aborts cleanly on EOF, instead of passing because any
other error appeared.

## Why

H-V23 found a class that the red-cohort method cannot see (akte
`evidence/bug-hunt-2026-11-21/fail-closed-honesty/round-1.md`, section 6.1 and Karte F): at develop `40cb28c758b0`,
`cmd/baha/trust_uninstall_test.go:132/:157/:215` run `trustUninstallCommand().Run(context.Background(), ...)` and treat
**any** non-nil error as the clean abort they claim to verify. Since #1717 the command fails at the operator-auth gate
before the prompt is ever read, so **these tests are falsely green today** and their real assertions at `:159-164` are dead
code behind a fatal-on-any-error shape. Same shape to re-check: `cmd/baha/trust_status_regression_test.go:116-130`.

## Scope

Allowed write-set:

- `cmd/baha/trust_uninstall_test.go`
- `cmd/baha/trust_status_regression_test.go`

Forbidden: production code (if the prompt path cannot be reached from a test, report it, do not fix it here),
`internal/operatorauth/**` (Owner rail), and every other `cmd/baha/` file — 0428-204 stamps those while it runs.

## Acceptance criteria

1. Each named test fails when the prompt handler returns an error, and passes only with the real EOF abort
   (`Host trust unchanged.` plus the ownership-file-unchanged checks enabled again).
2. The auth precondition is satisfied in the positive setup, never by accepting any error as the expected result.
3. Evidence quotes the failing run before and the passing run after at the exact candidate head.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | Go unit shards for `./cmd/baha/` (PR Selected Checks) |
| Test identifier | `0428-213` |
| Route | `auto-discovery` |

## Stop and report

If the fix requires `ensureOperatorAuthForBoundary` (`cmd/baha/operator_auth_boundary.go:55`) or anything in
`internal/operatorauth/**`, stop and report file:line.

## Handoff

Branch, PR, exact head SHA, terminal hosted run id, evidence
`evidence/r28-welle4-2026-11-21/trust-uninstall-false-green/round-1.md`.

kandidat vollstaendig: head d0399968c47f, base-ref 'lane-0428-198-cli-shard-operator-env' @ 7db142852d22 (ketten-regel, gemessen), draft=false (gemessen, die lane meldete 'draft'). durchgang 44861150777 terminal: draft-zellen skipped, 'PR · Go unit · cli-0..3' failure = geerbte operator-auth-klasse (128 gate-zeilen, 108 first-level namen), 'Workflow policy'/'Trusted Plan'/cli-vet/cli-build/cli-gofmt success. zwei faelle mit 'Trust' im namen gehoeren zu ANDEREN dateien (operator_auth_boundary / mcp_platform_*), die karten-eigenen faelle sind damit nicht gemeint — korrektur der akten-formulierung befohlen.

kette nachgezogen, von mir gemessen: head 5be4f003aa1b, base 'lane-0428-198-cli-shard-operator-env' (basis-head beim rebase c2f9f2f32fd6, seitdem e45430f2f1b7 — fuenfter owner-push), 'merge-base --is-ancestor' = 0, draft=false; eigener durchgang terminal: run 44867291850 / 44867319394 completed/failure, cli-shards geerbt. WICHTIG FUER DIE ABNAHME: PR Selected Checks faehrt einen pr_merge-commit (85ae26150145 = 'Merge <head> into <base>'), 'exact-head' heisst bei gestapelten PRs der merge, nicht der branch allein. Akte round-3-chainrebase.md (plan 38b79bce).

kette nachgezogen, von mir gemessen: head 5be4f003aa1b, base lane-0428-198-cli-shard-operator-env (basis-head beim rebase c2f9f2f32fd6, seitdem e45430f2f1b7 = fuenfter owner-push), merge-base = 0, draft=false; eigener durchgang terminal run 44867291850 completed/failure, cli-shards geerbt. FUER DIE ABNAHME: PR Selected Checks faehrt einen pr_merge-commit (85ae26150145 = 'Merge <head> into <base>'), 'exact-head' heisst bei gestapelten PRs der merge, nicht der branch allein. Akte round-3-chainrebase.md (plan 38b79bce).

kette nachgezogen, gemessen: head 5be4f003aa1b auf base 'lane-0428-198-cli-shard-operator-env' (basis beim rebase c2f9f2f32fd6, seitdem e45430f2f1b7 = fuenfter owner-push), merge-base = 0, draft=false, eigener durchgang terminal run 44867291850 completed/failure (cli-shards geerbt, inhalt #1615). FUER DIE ABNAHME: PR Selected Checks faehrt einen pr_merge (85ae26150145 = 'Merge <head> into <base>'), 'exact-head' heisst hier der merge, nicht der branch allein. Akte round-3-chainrebase.md.

CODEX-REVIEW 'Verdict: REQUEST CHANGES' (plan d96fb84f) an head 5be4f003aa1b: P2 = 'trust_uninstall_test.go:15-29' route durch 'operatorAuthFixtureContext' STEMPelt verified principal + editor — der fixture ist eine POSITIVE vorbedingung, nicht die getestete verweigerung; die verweigerung selbst ('trust_uninstall_test.go:87-106', JSON/no-approval) braucht guidance + owner-pruefung und wird vom stempel nicht erreicht. P1 haelt dagegen: die EOF-regressionen sind echt, und die cite 'base 7db142852d22' zeigt rot auf dem unerreichbaren prompt-pfad — der rot-zuerst-beleg ist also DA, aber an der falschen stelle. P3: durchgang 44867291850 pruefte den SYNTHETISCHEN merge 48b7ccdfa242 (eltern 80dc4987993b + 5be4f003aa1b), und der kandidat-punkt ist 48b7ccdfa242 vs 'current base e45430f2f1b7...candid…' — d.h. die kette haengt an der ALTERN basis c2f9f2f32fd6 und ist nachzuziehen. P4 = meine buchfuehrung: 'classify every failing test, do not call them inherited'.

inhalt OK, BASIS NICHT: sie liefert den bidirektionalen gate-beweis in 'cmd/baha/trust_uninstall_test.go' (ihr eigenes write-set) und meldet 'full-package 0 failures, zero new vs base' — das glaube ich ihr, weil der reviewer dieselbe erbschaft an #1737/#1741 einzeln protokoliert hat (cli-0 'TestAppListAllTargetsWorksAfterInstallationDestroy' = 0428-210/#1739, packages 'providers/loki/shared/service-access/pki/client-cert.pem' fehlt = owner-schlen #1615). ABER: ihr push head 8b38c4f88f3e ist gegen 'e45430f2f1b7' IMMER NOCH KEIN nachkomme (abzweigung bei c2f9f2f32fd, 2 commits, 25 dateien staleness, davon ein owner-commit d0399968c 04:24) — der rebase-schritt ist also nicht angekommen, obwohl gepusht wurde. Gemessen: 8 success / 8 failure / 19 skipped, 'PR Selected Checks' failure. Kein exakter-head-kandidat, daher zurueck auf 'active' mit rebase-auftrag (neue Lane, identitaet + nachkommen-nachweis VOR push).

rebase ANGEKOMMEN, von mir am remote nachgemessen (nicht aus ihrer meldung): head 3010b212c8af, 'merge-base --is-ancestor e45430f2f1b7 <head>' = 0, 'rev-list --count' = 1, 'diff --name-only' = genau 'cmd/baha/trust_uninstall_test.go', 'log -1 --format=%an' = '0428-213-rebase1737' — der fremde owner-commit d0399968c ist raus aus dem PR (vorher stand er drin, issue #24). GEHOSTET am neuen head: durchgang 44883097577, 8 success / 6 failure / 20 skipped, 'PR Selected Checks' failure; ihre gleichheits-proof: die roten cli-0..3 + cli-vet sind IDENTISCH zu durchgang 44878429408 am alten head 8b38c4f88 = erbschaft, nicht ihr rebase. NEUE LAGE, die diese karte HEILT: der owner hat #1615 um 08:08 gemergt (develop = 9bd76324ec6d, 'Merge pull request #1615 from mcpdev80/cli2-identity-secrets-*'); die gate-klasse 'Managed-environment machine operations require an authenticated BaseHarbor operator' verschwindet damit aus den cli-zellen, sobald die lane auf den neuen develop hoppt. Fuer #1737 (basis = lane e45430f2f1b7) gilt das erst nach dem naechsten basis-hop.

CODEX-REVIEW r2 'review-2.md' (plan 3cdd3f07 + 24179731) = 'Verdikt: REQUEST CHANGES'; ihre rebase-arbeit ist PASS (single commit ueber der deklarierten basis, nur kartendatei), aber ES GIBT KEINEN AUSGEFUEHRTEN TESTKOERPER: 'PR · Validation · cli-vet' failure + ALLE vier cli-shards failure wegen REDECLARATION — sie deklarieren 'withoutOperatorAuthTestContext' in 'cmd/baha/trust_uninstall_test.go:42' ERNEUT, obwohl 'cmd/baha/app_init_wizard.go:29-31' den echten opt-out schon hat; ihre variante ist ein 'return ctx' und opted damit NICHT aus, der anonyme kontext bleibt also gestempelt = der beweis ist nichts wert. Befund 2: 'trust_uninstall_test.go:175' prueft per 'strings.Contains' und laesst den endpunkt der produktquelle weg -> text-mutation bleibt gruen. Mission liegt fertig in coordinator/missions/0428-213-r3-compile-and-verbatim.md (payload-gate 0) und geht auf den ersten freien sitz. WICHTIG FUER DAS GANZE FENSTER (antwort auf meine eigene frage an den reviewer): die loki-pakete-roete 'providers/loki/shared/service-access/pki/client-cert.pem' ist auf dem GEMERGTEN baum GRUEN — #1615 wurde 08:08 zu develop 9bd76324ec6d gemergt, merge-commit und PR-head teilen den tree 'f5…'; ein hop der stapel-basis loescht diese rote zeile, loest aber IHRE compile-kollision nicht (dafuer keine recipe an #1615).

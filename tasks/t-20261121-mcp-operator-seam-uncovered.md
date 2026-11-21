---
id: t-20261121-mcp-operator-seam-uncovered
card_number: "0428-218"
card_short_title: "0428-218 mcp operator seam"
type: bug
areas: [cli, observability]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: active
kanban_lane: active
kanban_summary: Every MCP mutation path whose test expects the verbatim gate message Managed-environment machine operations require an…
kanban_title: 0428-218 · 0428-218 mcp operator seam
priority: normal
depends_on: [t-20261120-cli-operator-entrypoints]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1741]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
created: "2026-11-21T05:55:00Z"
updated: "2026-11-21T05:55:00Z"
---

- [ ] t-20261121-mcp-operator-seam-uncovered · 0428-218 make the MCP operator seam reachable from MCP tests #task #release/v0-4-28 #status/active #view/active #area/cli #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** normal  
    **PR:** [baseharbor#1741](https://github.com/mcpdev80/baseharbor/pull/1741)  
    **Needs:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
**Owner:** coordinator  
**Priority:** normal  
**PRs:** [baseharbor#1741](https://github.com/mcpdev80/baseharbor/pull/1741)  
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

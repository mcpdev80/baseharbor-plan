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
kanban_status: review
kanban_lane: review
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

- [ ] t-20261121-trust-uninstall-false-green · trust-uninstall EOF tests are green on the auth gate error #task #release/v0-4-28 #status/review #view/review #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    **PR:** [baseharbor#1737](https://github.com/mcpdev80/baseharbor/pull/1737)  
    **Needs:** [t-20261120-cli-operator-entrypoints](t-20261120-cli-operator-entrypoints.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
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

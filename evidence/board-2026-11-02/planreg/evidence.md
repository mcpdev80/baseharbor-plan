# planreg Evidence — Planner coverage gap (reg-mixed / pr-gate-plan.py)

**Task:** planreg — Planner-Lücke: geprüfter Kandidat kann Zweig `registration-mixed` nie erfüllen
**Date:** 2026-11-02
**Worker session:** 35cdb02e-a3b3-4e6d-86f9-1cbb35822587
**Basis:** origin/develop = 640846e1
**PR-Scope:** PR #1272 (head 72c14450, CODEX APPROVE) — cmd/baha MCP tests + manifest.go + CHANGELOG

## PLAN

1. [x] Befund verstehen: pr-gate-plan.py Zweig ~1401-1412 haengt fuer JEDAenderung an cmd/baha/mcp_*.go dauerhaft 'unresolved' AN
2. [x] Drei Referenz-Zweige lesen (core754, appid, workflow-policy) + Zusammenspiel mit identifiers['head_sha']/path_status
3. [x] EXAKT einen reviewed-entry fuer 1272 einfuehren (core917/core-754-Muster: head_sha + 3-Datei-Status-Ledger + Lifecycle-Gaene)
4. [x] Scope wahren: kein Prefix-Matching, keine allgemeine Befreiung, PR-Titel/Body nur Doku
5. [x] Planner-Tests beide Richtungen erweitern (exakter Kandidat resolved; extra/renamed/deleted/wrong-status/wrong-head + fehlender Lifecycle-Gate unresolved)
6. [x] PR gegen develop; PRSC + pr-planner-tests beobachten (Eigenes-Run-Pflicht)
7. [x] Evidence abgeschlossen + END line

## Repo-rule compliance

- Scope: nur `scripts/pr-gate-plan.py` + `scripts/test_pr_gate_plan.py`. Keine anderen Planner-Zweige, keine neuen Gates, kein Merge, kein Subagent, kein Frage-Dialog (MISSION STOP eingehalten).
- Kein `git add -A`; nur die zwei betroffenen Files committet.
- Pre-existing CI failures (ReceiptControlPlane/RealPlanValidation — Netzzugriff) unveraendert; keine neuen Test-Fehler (278 vs 278).

## Evidence

- Review-Befund: baseharbor-plan/evidence/board-2026-11-02/codex-authz1/review-r3.md — PR #1272 head `72c14450`, base `640846e1`; `PR Selected Checks` fiel auf `coverage-unresolved: cmd/baha/mcp_application_authoring_test.go`.
- Diff 640846e1..72c14450: genau 3 Files, alle `modified` (CHANGELOG.md, cmd/baha/mcp_application_authoring_test.go, internal/application/manifest.go); merge-base = develop HEAD.
- Merge-chain: `git merge-base --is-ancestor 640846e1 72c14450` => true (clean trusted-target integration).
- Lokal simulierter PRSC-Lauf (synthetischer 2-Parent-Merge): `coverage_status: resolved`, `selected_gates: [atomic/docker/lifecycle, atomic/podman/lifecycle]`. 4. Datei (`extra.go`) => `unresolved` (Fallthrough registration-mixed).
- pr-planner-tests lokal: 4 neue Tests ok; Gesamtsuite 278 Tests, nur 3 pre-existing Netzzugriffsfehler (Identisch zum Clean-Base).

### Hosted CI (Eigenes-Run-Pflicht)

- PR #1275 https://github.com/mcpdev80/baseharbor/pull/1275, head `bb2b8264d3a1f7ad390c3362b2aadbdf19e03355`, base develop.
- CI run **41418988279** conclusion **success** (16/16 Jobs gruen, kein Fehler).
  - PR · Trusted Plan (PRSC / pr-gate-plan.py): success — Coverage loest sich auf (war vorher unresolved-Blocker).
  - PR · Validation · pr-planner-tests: success — neue Pr1272-Tests greifen in Hosted-CI.

## END

END planreg DONE — pr=1272 head=bb2b8264 run=41418988279 | PRSC resolved + pr-planner-tests green (16/16); PR #1275, no merge/owner-approval needed for this planner fix

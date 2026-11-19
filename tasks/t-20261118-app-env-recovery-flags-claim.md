---
id: t-20261118-app-env-recovery-flags-claim
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
owner: w01-0428-117r4 (codeman 28318f22)
kanban_status: review
card_number: 0428-117
card_short_title: align app env recovery-flag
kanban_title: 0428-117 · align app env recovery-flag
prs: [mcpdev80/baseharbor#1687]
wait_reason: ""
blocker: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44439013578", "https://github.com/mcpdev80/baseharbor/actions/runs/44441702644"]

---
# t-20261118-app-env-recovery-flags-claim · app-env recovery-flag claim vs actual command contract

- [ ] t-20261118-app-env-recovery-flags-claim · align app env recovery-flag docs with the real command contract #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** w01-0428-117r4 (codeman 28318f22)  
    **PR:** [baseharbor#1687](https://github.com/mcpdev80/baseharbor/pull/1687)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44439013578), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44441702644)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w01-0428-117r4 (codeman 28318f22)  
**Priority:** not set  
**PRs:** [baseharbor#1687](https://github.com/mcpdev80/baseharbor/pull/1687)  
**Source:** 
<!-- /generated:links -->

## Goal
Hunt 915 B1 (mittel, CLI-vertrag): the generic recovery text promises `--uuid`/`-e/--environment` for EVERY `baha app <command>`, but `baha app env` rejects these flags itself (cmd/baha/app_env.go:21 defines only NAME/format/reveal). Align the documentation claim with the actual per-command contract: state explicitly which `baha app` subcommands accept the recovery selectors and note that `app env` is selected BY NAME, not by uuid/environment. Keep the observed read-command Port nuance documented truthfully.

## Scope
- docs only (the recovery-flag passage + app env command reference lines). NO behavior change; wiring flags into `app env` is out of scope (would need its own contract decision).

## Required checks
- docs build/link check; machine-docs consistency job if it exists in the affected group.

## Dependencies and file ownership
- Source: hunt 915 Befund B1, evidence/r28-welle4-2026-11-18/hunt-cli2merged/befund-1.md (origin/main 49323cde).

docs-only, exact-head CI SUCCESS auf 7aa8b01e9, DE-mirror mitgezogen

CODEX-REVIEW comment #6994874926 im thread (formale change-request durch self-author-block nicht moeglich — Konvention): REQUEST CHANGES — 'NAME vor --uuid' falsch (uuid-strip vorher; regression status nur --uuid+ID). r2 ueber neue lane, PR bleibt 7aa8b01e9, kein merge

r2b END akzeptiert: head da7a2ace9 (force-with-lease linear rebase auf 9a37b4bc, lane-exklusiver branch — akzeptierte variante statt mission-kraft; history-pruefung ergab keine fremd-commits), exact-run 44427162228 SUCCESS, akte r2.md mit r2b-revision-label + superseded-vermerk fuer 7aa8b01e9 am band. Doku je subcommand nach wirklichkeit (uuid NAME-frei bei show/status/destroy, plan verweigert --uuid remote, env ablehnt beide) — genau das geforderte realitaetsprofil. Routing an CODEX-REVIEW

reviewer hält #1687 zurück: '-e als Alternative zu --uuid' widerspricht code; 'Registry-Siegel'-verdeutschung im diff. r3-lane dispatched (selektor-getrennte semantik je aussage mit datei:zeile, fachwoerter englisch, hopf auf de53246585, new exact-head run). kein merge bis korrektur+checks

r3 END akzeptiert: head d957de2c8 (hopf monoton), run 44439013578 SUCCESS, alle drei DE-wortfehler geheilt (setzt/ueberschreibt, kollidierendes Deployment, ausser Dienst gestelltes Twin-Deployment) + selektor-getrennte EN/DE-semantik, akte cfff4bb0 am band. Basis-pruefung: traegt develop-Stand gem. ls-remote — falls develop vor merge erneut zog, fenster-hopf wie in der kette verabredet. Routing an CODEX final

reopen fuer basis-freshness (reviewer-pflicht): develop 40b9901398, 116er-kette zeigt das muster — d957de2c bleibt inhaltlich die r3-fassung, NUR basis-hopf + run-refresh + akten-zeile. keine wort-aenderung an der doku vorgesehen

Codex review: EN/DE selector wording passes on head d957de2c8d6f88f4900cb64d54ad374174b3a947; fresh compare develop 40b9901398a6bae5b92ee45494ef3b70f192a2a7 vs candidate shows merge base de53246585560ddf2c3e6ceae6d0f6eea6b71b68, 11 commits behind. Hold for normal owner hopf and exact-head CI.

Update: normal base refresh is complete. Fresh compare is ahead 2 / behind 0 from develop 40b9901. EN/DE diff unchanged and source/docs review still passes; exact-head CI is queued on a1f4dc7. Await terminal run and current evidence.

Codex re-review: selector wording in EN/DE remains accurate on a1f4dc7; base compare ahead 2/behind 0 from current develop 40b9901. Run 44441702644 terminal success; documentation-audit, mkdocs EN/DE strict, source format, trusted plan and selected-check enforcement all passed. Native/runtime/Go jobs skipped as irrelevant for docs-only. Await refreshed r4 evidence with current SHA/base.

r4 END akzeptiert: merge-head a1f4dc76f traegt develop 40b9901398 (monoton, r3-inhalt woertlich), exact-run 44441702644 SUCCESS, docs-audit DOCS_EXIT=0 + vet/tests gruen, akte 53fbaec1 mit supersede-kette am band. Handoff an CODEX — merge-fenster: letzter basis-check vor merge wie verabredet

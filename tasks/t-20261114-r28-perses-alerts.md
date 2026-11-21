---
id: t-20261114-r28-perses-alerts
card_number: "0428-073"
card_short_title: "Define and provision alert"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: Codex (Marcel Wait sweep 2026-11-21)
kanban_status: active
kanban_lane: active
kanban_summary: Provision alert rules through the existing supported Prometheus contract and have Prometheus evaluate them; persist the alert…
kanban_title: 0428-073 · Define and provision alert
priority: normal
depends_on: [t-20261114-r28-perses-datasources]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1613, mcpdev80/baseharbor#1704]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/perses-alerts-hopf/fix-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1613-alert-contract-review.md", "https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1613-0428-073.md"]
---

- [ ] t-20261114-r28-perses-alerts · Define and provision alert rules #task #release/v0-4-28 #status/active #view/active #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Marcel Wait sweep 2026-11-21) · **Priority:** normal  
    **PR:** [baseharbor#1613](https://github.com/mcpdev80/baseharbor/pull/1613), [baseharbor#1704](https://github.com/mcpdev80/baseharbor/pull/1704)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/perses-alerts-hopf/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1613-alert-contract-review.md), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/6aaa17cc5f9291383d9891562e7788aba8c2f939/evidence/r28-welle4-2026-11-19/codex-review-wave/1613-0428-073.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-datasources](t-20261114-r28-perses-datasources.md)  
**Required by:** [t-20261114-r28-perses-contact-routing](t-20261114-r28-perses-contact-routing.md), [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md), [t-20261117-alert-evaluator-persistence-missing](t-20261117-alert-evaluator-persistence-missing.md), [t-20261117-hunt-signals-105](t-20261117-hunt-signals-105.md)  
**Owner:** Codex (Marcel Wait sweep 2026-11-21)  
**Priority:** normal  
**PRs:** [baseharbor#1613](https://github.com/mcpdev80/baseharbor/pull/1613), [baseharbor#1704](https://github.com/mcpdev80/baseharbor/pull/1704)  
**Source:** 
<!-- /generated:links -->

## Goal

Provision alert rules through the existing supported Prometheus contract and have Prometheus evaluate them; persist the alert state history. Fail closed: with no provision-capable backend or no configured rules, there is no alerting. Report undefined states as "unknown" and never silently as "ok". No standalone evaluator, new infrastructure, or new frameworks. PR #1704 is not accepted because CI green does not satisfy real evaluation and persistence.

## Scope and file ownership

Own rule specs/tests only; no contact secrets or presumed provider features. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/metrics/prometheus_render.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_render.go)
- [internal/metrics/prometheus_files.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_files.go)
- [internal/metrics/prometheus_verify.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_verify.go)

Use the existing supported Prometheus rule/evaluation contract and state persistence/lifecycle contracts. Confirm the integration in current Core source before implementation. Do not build an evaluator, add infrastructure, or introduce frameworks. Missing provision-capable backend or missing rules means alerting is disabled; unknown state must be reported as "unknown", never "ok".

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Provision rules through the supported Prometheus contract; Prometheus performs evaluation and the state history persists. Do not use a stub that only reports "unavailable" as a substitute for the release contract.
- Demonstrate that Prometheus evaluates provisioned rules and that alert state history persists across the supported lifecycle. If there is no provision-capable backend or no configured rules, no alerting occurs. Undefined state is reported as "unknown", never silently as "ok". External routing is owned by 0428-074 and is opt-in only.
- Record the release-contract rejection rationale: CI green alone is insufficient; the fail-closed "unavailable" stub advertises a capability without real rule evaluation and persistence and does not meet this release contract.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-alerts](t-20261113-r28-grafana-alerts.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

hopf-runde angesetzt: PR #1613 ist 'dirty' gegen develop (head 470735c1d) — die lane hebt den kandidat monoton per MERGE auf da76c5cf9, loest die manifest-konflikte inhaltserhaltend und bringt einen neuen exaktkopfigen terminalen run; akte perses-alerts-hopf/fix-1.md

hopf abgeliefert und von mir verifiziert: head d8838f622b551cdc8a7f8e8320c3f122b2ae5783, monoton (develop da76c5cf9 ancestor UND der alte head 470735c1d ist Vorfahr), PR #1613 jetzt clean (war 'dirty'), vier konflikte inhaltserhaltend geloest, akte perses-alerts-hopf/fix-1.md. ABER EVIDENZ-LACKE, von mir selbst gefunden: der exact-head lauf 44491028219 meldet SUCCESS, hat aber NUR 'PR · Draft source and routing' + 'PR · Draft Go · cli-0/1/2/3/packages' ausgefuehrt, alle Go-unit/build/vet/policy-zellen sind 'skipped' — der kandidat ist an seinem kopf also NICHT voll geprueft, und 'SUCCESS' darf hier nicht als required-CI gelesen werden (§5.3 'keine gruen gerechneten gates'). die lauf-liste des zweigs zeigt dasselbe muster seit 11-16 (immer nur draft-zellen bei pull_request). ursache-sonde laeuft bereits (akte gate-routing/probe-1.md), gefundenes geht als punkt (g) in 0428-114. daher: review MIT ausdruecklich teil-zeug, abnahme möge nicht auf 'lauf success' allein entscheiden

EVIDENZ-LACKE GESCHLOSSEN, grund war draft-status (nicht die gate-map): PR #1613 war draft=true, und ci.yml haengt source-format/build/vet/unit/policy an 'draft == false' (zeilen 514/1137/1160; probe-akte gate-routing/probe-1.md commit 7d3cb684; der planner scripts/pr-gate-plan.py ist draft-agnostisch, targeted_plan() zeile 763 ohne draft-referenz). ich habe den PR auf ready gesetzt; der neue lauf 44495425072 auf demSELBEN exakten head d8838f622b551cdc8a7f8e8320c3f122b2ae5783 ist TERMINAL SUCCESS mit 14 ausgefuehrten zellen: 'PR Selected Checks', 'PR · Trusted Plan', 'PR · Native gate plan', 'PR · Source format', 'Workflow policy', 'PR · Validation · go-build', 'PR · Validation · go-vet', 'PR · Focused Python', 'PR · Go unit · packages/owner/cli-0/cli-1/cli-2/cli-3'; 19 zellen skipped (runtime/HA/release-pfade, ausserhalb des diff-routings). damit ist der kandidat abnahmefaehig OHNE teil-zeug-vermerk. PR-Zustand: open, draft=false, head d8838f622, monoton auf develop da76c5cf9

required-ci-zeug delivered und verifiziert (akte perses-alerts-hopf/ci-1.md, commit e611d271, ancestor origin/main): alle 30 zellen completed, 0 failure, 9 required zellen pass; skipped sind release-/draft-/native-targeted pfade. head d8838f622b551cdc8a7f8e8320c3f122b2ae5783, check_suite 120443180547. die lane hat dafuer einen FRISCHEN isolierten clone unter /var/tmp benutzt (filter=blob:none) statt der gemeinsam-genutzten kopie — praezedenz fuer alle zeugen-fahrten. karte bleibt review mit vollstaendiger exaktkopfiger evidenz

CODEX-REVIEW welle 4 = REQUEST CHANGES auf dem gepueften kopf (urteil 1613-0428-073.md). korrekture-runde ist vorgemerkt und wartet auf einen freien sitz: die vier perses-karten und 083 teilen sich dateien mit den laufenden lanen, darum kein paralleler start ohne write-set-nachweis. 083: 'runtime provisioning absent' (datasource wird gebaut, aber nicht in Perses bereitgestellt); 073: 'alert rule nicht ausgefuehrt/nicht persistiert' (persesAlertRealEvaluation); 077: 'catalog-availability aus host provider-metrics allein'; 089: 'PersesComposeServices rendert keine config (--config=/etc/perses/config.yaml) + loopback upstream'

Independent read-only review of PR #1613 / 0428-073 (2026-11-19): exact run 44495425072 passed but is stale; PR is DIRTY/CONFLICTING against current develop and needs rebase/rerun. Evaluator remains hardcoded fail-closed; health verifier lacks selected-Perses gate if enabled later; secret contract test is vacuous. See [review evidence](../evidence/r28-welle4-2026-11-19/codex-review-wave/1613-0428-073-independent-review.md).

korrekturrunde aus der unabhaengigen review 1613: hopf (2 konflikte gemessen) + stub-HONESTIE (perses_prometheus_alerts.go:178-182 return false bleibt, unavailable muss aber ALS unavailable erscheinen) + manifest-selected-pruefung in VerifyPersesAlertEvaluatorHealth :194-212. schreibdisjunkt zu #1684/#1702/#1693 (gemessen, keine ueberlappung)

#1613 ist closed (gemessen state=closed), #1704 ist der nachfolger auf LATEST BASE 6e87ddcb4 mit zwei eltern, konfliktfrei, run 44614171320 success am kopf 90e1f1417; zwei dateien internal/metrics/perses_prometheus_alerts{.go,_test.go}

CODEX 1704 REQUEST CHANGES, ein blocker P1 (gemessen bestaetigbar im urteilstext): selected-pfad perses_prometheus_alerts.go:220-222 textet 'fails closed (not_enabled)' statt des verlangten 'unavailable (owner-gated evaluator contract)', test :332-350 haelt den wortlaut nicht fest; dazu kein produktions-callsite-Nachweis. Stub bleibt false (owner-freigabepunkt). Neue lane w073-pr1704-persesalerts-r3 auf ornith:2, uebergabe dokumentiert (c74a1fe2 entlassen)

r3 VON MIR GEMESSEN: head f5dcf12885, base 28fb427f = aktuelle spitze, hopf ist ein ECHTER merge (vater 5763eb7fb mit zwei eltern), fix-commit darueber; ancestry 0, merge-tree konfliktfrei, draft=false; CI run 44621875256 event=pull_request completed success am exakten kopf. DER P1-BLOCKER IST HEILT: prometheus_alerts.go:221 traegt 'the alerting contract is unavailable (owner-gated evaluator contract)', test :365-367 asserts ihn UND :363-364 verbietet '(not_enabled)' ausdbruecklich; stub bleibt false. Offener punkt: unselected-zweig :202-204 sagt 'is not selected ...' statt 'not configured' — das urteil muss sagen, ob die acceptance das wort verlangt. Lane eskaliert correct: null production callers -> karte 0428-152 (angelegt, haengt an 0428-142, deren PR app_status_collect.go aendert)

Owner decision (2026-11-20): scope reduction is rejected. PR #1704 is not accepted: CI green does not meet the release contract; a fail-closed "unavailable" stub is a false capability without real rule evaluation or state persistence. Rework or replace it with rules provisioned through the supported Prometheus contract and evaluated by Prometheus, with persisted state history. No new evaluator, infrastructure, or frameworks. Missing backend/rules disables alerting; undefined state is reported as "unknown", never silently as "ok". External routing remains opt-in under 0428-074.

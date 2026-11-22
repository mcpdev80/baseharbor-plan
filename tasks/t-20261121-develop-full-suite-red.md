---
id: t-20261121-develop-full-suite-red
card_number: "0428-223"
card_short_title: "full-suite unit tests are red"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: fecbada9/1450c201 (review) + Owner (merge autorisiert durch sweep-klaerung)
kanban_status: review
kanban_lane: review
kanban_summary: "The whole-package Go unit suite (go test ./...) is red on develop and no merge gate runs it: make the suite pass on develop…"
kanban_title: 0428-223 · full-suite unit tests are red
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1750]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261121-develop-full-suite-red · CI: full-suite unit tests are red on develop and no merge gate runs them #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** fecbada9/1450c201 (review) + Owner (merge autorisiert durch sweep-klaerung)  
    **PR:** [baseharbor#1750](https://github.com/mcpdev80/baseharbor/pull/1750)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261120-workload-port-flag-ignored-locally](t-20261120-workload-port-flag-ignored-locally.md), [t-20261122-footprint-show-not-admitted-in-data-capabilities-gate](t-20261122-footprint-show-not-admitted-in-data-capabilities-gate.md), [t-20261122-static-cells-operator-auth-helper](t-20261122-static-cells-operator-auth-helper.md)  
**Owner:** fecbada9/1450c201 (review) + Owner (merge autorisiert durch sweep-klaerung)  
**Priority:** not set  
**PRs:** [baseharbor#1750](https://github.com/mcpdev80/baseharbor/pull/1750)  
**Source:** 
<!-- /generated:links -->

## Goal

The whole-package Go unit suite (`go test ./...`) is **red on develop** and **no merge gate runs it**: make the suite pass on develop again and give develop a CI event that actually executes the full-package job.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

H-V50 shows the 14 red cases are an environment gap: probe application resolves target 'company-dev' which no test configures since 80961866f. The fix lane proves it with a CI workflow_dispatch on its own branch, where the validate cell actually runs.

QUERBEZUG vom coordinator: die operator-auth-/test-context-vorbedingung dieser karte blockiert messbar eine ZWEITE karte. der combined validation run 44957245330 fuer PR #1627 (karte 0428-055) fiel in BEIDEN coreless-lifecycle-shards (docker UND podman) mit 'prepare native workload deployment inputs requires authenticated BaseHarbor operator' und einem cleanup ohne verifizierten operator context - derselbe grundtyp wie bei #1746s static suite (akte static-gate-registration/finding-1746-static-suite-failure.md). PR #1750 / karte 0428-223 ist damit der schluessel fuer die 0428-055-abnahme: wer immer diese karte abschliesst, muss danach 0428-055 neu validieren (exakter hosted run mit docker UND podman lifecycle-ausfuehrung).

lane pushed a new exact candidate 4bd779b1501 (parent 1588ee1be72, back=0, additive): ORAS is provisioned inside the test-support path (cmd/baha/runtime_integration_test_support_test.go, provisionORASForIntegrationCell, uses the production installer installORAS with orasSetupVersion + checksum, no-op when exec.LookPath finds oras). no .github/** or scripts/** change. hosted runs 44972447675 (PR CI) and 44972454590 (selected target-context) in_progress; verdict ordered, PR stays draft

akte round-3-oras-provisioning.md auf origin/main; cleanliness gemeldet: keine eigenen container/netzwerke/volumes, scratch entfernt

PR 1753 hopped to develop 8b9a8f50645 at head 91f4e38795a with exact CI green (run 44978381512, 0 failed); PR Selected Runtime still SKIPPED pending card 0428-228 path to gate mapping

independent CODEX-REVIEW gives APPROVE at exact head 17f471cd3fe (required checks pass, job 137087212830); two follow-ups recorded: P3 temp-dir cleanup in cmd/baha/test_operator_context_test.go:112-121 and the skipped Selected Runtime/validate proof that depends on card 0428-228

Hop ist gelandet: head 5d47569f337 (additiv, back=0, run 44986337450 SUCCESS, 0 failed jobs). Acceptance bleibt withheld: Selected Runtime ist an diesem head SKIPPED (job 137097672713), validate skipped (137097623509). Grund ist nicht der kandidaat, sondern die fehlenden catalog-zeilen in pr-gate-coverage.json - karte 0428-230, rezept native-checks-catalog-recipe.md. Der P2 hostConfigIsolationDir cleanup ist als 0428-233 eigenstaendig gefuehrt.

Verdict auf origin/main: APPROVE am exakten head 5d47569f337, ausdruecklich als additiver develop-only hop gegen das fruhere APPROVE bei 17f471cd3fe bestaetigt (akte testcontext-0428-223/review-1750-head5d47569f337.md). Damit ist die merge-blockade weg. Ein additiver hop auf develop 5ca8420c181 laeuft parallel; die merge-session prueft den LEBENDEN refs/pull/1750/head und merged bei CLEAN + terminal SUCCESS (zwei getrennte akten, ROLLE-Label, rule-getreu).

APPROVE am LEBENDEN head f6d3fc5c23e4a3097d4d36130303338b0ff180bd ist publiziert (akte testcontext-0428-223/review-1750-headf6d3fc5c23.md, remote bestaetigt): exact run 44990801974 completed SUCCESS, 14 jobs success / 0 failed / 21 skipped, required aggregate 'PR Selected Checks' success; validate 137111207599, Native matrix 137111239451, Native Keycloak/Core 137111249223 und Selected Runtime 137111249509 sind SKIPPED - erwarteter stand VOR PR 1756, kein ablehnungsgrund. Der hop auf develop 5ca8420c181 fuegt ausschliesslich develop-inhalt bei (log 5d47569f337..f6d3fc5c23e = nur der #1714 squash). CODEX-MERGE ist beauftragt.

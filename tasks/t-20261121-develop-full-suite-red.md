---
id: t-20261121-develop-full-suite-red
card_number: "0428-223"
card_short_title: "full-suite unit tests are red"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: 0428-223-testctx
kanban_status: wait
kanban_lane: wait
kanban_summary: "The whole-package Go unit suite (go test ./...) is red on develop and no merge gate runs it: make the suite pass on develop…"
kanban_title: 0428-223 · full-suite unit tests are red
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1750]
sources: []
blocker: ""
wait_reason: "head ist exakt (4bd779b1501, back=0, draft=true) und die validate-zelle ist groen belegt: run 44973644884 completed/success, job 137058691290, schritt 14 zeigt alle 14 mission-namen groen, schritt 16 das receipt 'PASS: all six native runtime tests and both package teardowns'; ORAS wird jetzt ueber den produktions-installer innerhalb des integration trust plane gepinnt (test-surface only, kein .github/scripts-eingriff, kein skip). das einzige verbleibende rot ist 'PR . Draft Go . cli-3' (job 137054968702 im lauf 44972447675) mit 'zsh: executable file not found in …' aus cmd/baha/context_terminal_test.go:467 - das ist karte 0428-229 / PR #1754, owner-scope. naechster ausloeser: merge von #1754, dann neuer exakter lauf auf dem dann aktuellen develop, dann verdict"
resolution: ""
evidence: []
---

- [ ] t-20261121-develop-full-suite-red · CI: full-suite unit tests are red on develop and no merge gate runs them #task #release/v0-4-28 #status/wait #view/wait #kind/task
    <!-- generated:card -->
    **Owner:** 0428-223-testctx  
    **PR:** [baseharbor#1750](https://github.com/mcpdev80/baseharbor/pull/1750)  
    **Waiting:** head ist exakt (4bd779b1501, back=0, draft=true) und die validate-zelle ist groen belegt: run 44973644884 completed/success, job 137058691290, schritt 14 zeigt alle 14 mission-namen groen, schritt 16 das receipt 'PASS: all six native runti…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261120-workload-port-flag-ignored-locally](t-20261120-workload-port-flag-ignored-locally.md), [t-20261122-footprint-show-not-admitted-in-data-capabilities-gate](t-20261122-footprint-show-not-admitted-in-data-capabilities-gate.md)  
**Owner:** 0428-223-testctx  
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

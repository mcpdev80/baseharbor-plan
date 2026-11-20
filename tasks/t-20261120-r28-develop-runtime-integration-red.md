---
id: t-20261120-r28-develop-runtime-integration-red
card_number: "0428-174"
card_short_title: "runtime Integr tests fail"
type: bug
areas: [ci, runtime]
release: v0.4.28
version: ""
parent: ""
owner: w174-pr0428-174-runtime-red
kanban_status: closed
kanban_lane: closed
kanban_summary: "Make the native runtime integration path green on develop again. The job docker-runtime, step \"Run runtime integration tests…"
kanban_title: 0428-174 · runtime Integr tests fail
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1711]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1711"]
---

- [x] t-20261120-r28-develop-runtime-integration-red · Develop: runtime integration tests fail serially in docker-runtime (base defect) #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/ci #area/runtime #kind/bug
    <!-- generated:card -->
    **Owner:** w174-pr0428-174-runtime-red  
    **PR:** [baseharbor#1711](https://github.com/mcpdev80/baseharbor/pull/1711)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1711)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261114-r28-perses-datasources](t-20261114-r28-perses-datasources.md)  
**Owner:** w174-pr0428-174-runtime-red  
**Priority:** not set  
**PRs:** [baseharbor#1711](https://github.com/mcpdev80/baseharbor/pull/1711)  
**Source:** 
<!-- /generated:links -->

## Goal

Make the native runtime integration path green on `develop` again. The job `docker-runtime`, step "Run runtime integration tests serially", fails when run against plain `develop` with no lane content involved, so every PR whose candidate selects that gate is red for a reason that is not its own.

## Scope

- In scope: reproduce the failing runtime integration step on a neutral `develop` checkout, identify the first failing test and its cause, and fix it on `develop` (or prove the gate needs an environment precondition that the runner does not provide, and record that requirement).
- In scope: the gate family selected by `PR · Native · native/docker/perses-runtime-smoke`.
- Out of scope: datasource and dashboard feature work of other cards. Out of scope: `.github/**` trigger changes - report a needed change as a finding with file:line to the Coordinator (owner scope).

## Acceptance

- A hosted witness on a `develop` commit shows the runtime integration step passing, or names the environment precondition the gate needs and then shows it green.
- The failing test name, file and first error line are recorded verbatim in the evidence file.
- PR mcpdev80/baseharbor#1684 can be re-verified against the fixed base without changing its content.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable.

- **Test binding (select exactly one):** normal (auto-discovered) - the failing step runs the existing package-discovered integration tests; no new catalog entry is expected.

## Dependencies and file ownership

- Owned files or areas: the native runtime integration harness selected by `native/docker/perses-runtime-smoke` (internal/application and the contracts helpers it drives).
- Shared files: coordinate through the owning task. `.github/**` stays with the owner.

## Base defect witnesses (measured by the Coordinator, 2026-11-20)

- https://github.com/mcpdev80/baseharbor/actions/runs/44661597243 - workflow "Runtime · Docker Core", event `workflow_dispatch`, head `ec02d5faad24` (a plain `develop` commit, 2026-11-20T02:33:03Z), job `docker-runtime` conclusion `failure`, failing step "Run runtime integration tests serially".
- The same workflow's ordinary `push` runs on newer tips `f61ef0f4991c` and `36d075fad77f` conclude `success`, so the red path is reached only through the manual/dispatch selection route - which is what the PR gate selects for affected paths.
- Lane witness with a local reproduction on pure `develop`: https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/perses-datasources/fix-1.md

## Handoff

- Opened by the Coordinator from the w083 finding on PR #1684 (card t-20261114-r28-perses-datasources): that candidate cannot reach a green required gate while this base defect stands. Newest first.

base-defekt, gemessen an zwei gehosteten zeugen: run 44661597243 (workflow 'Runtime · Docker Core', workflow_dispatch, head ec02d5faad24 = nacktes develop) job 'docker-runtime' step 'Run runtime integration tests serially' = failure; dieselbe workflow auf develop-push (f61ef0f4991c, 36d075fad77f) = success. mission liegt bei der lane, die den fallback lokal schon reproduziert hat (§5.3: neutraler produktionspfad, nicht reviewer-sandbox)

wurzelgrund UNABHAENGIG belegt durch die read-only PR-sweep-Lane der anderen welt (evidence/r28-welle4-2026-11-20/pr-sweep/continuation-2026-11-20.md): 'required native Perses smoke failed BEFORE ASSERTIONS because Docker could not create /etc/perses/database on the image's read-only root' —environment-voraussetzung, keine produktbehauptung; erklaert success auf develop-push vs. failure im selectierten dispatch-pfad. korrekturmaßstab: kleinste aenderung am tmpfs-mount des tests; waere nur .github/** behebbar, STOP mit datei:zeile an den coordinator (owner-scope)

abnahme ANGEDEUTET und in der reviewer-warteschlange hinter #1650, damit nicht zwei kanditaten gleichzeitig geprueft werden. gemessen: head 0a3805fb = refs/pull/1711/head (ls-remote), base auf develop-spitze 681700ca66f3 gebracht durch rebase + 'git push --force-with-lease' auf den ungeschuetzten branch (decision 2026-11-20-pr-branch-refresh-by-rebase.md), merge-base --is-ancestor 681700ca66f3 <head> = JA, run 44708908050 completed/success 0 failure, die docker-lifecycle-zelle laeuft ('Executed docker · lifecycle'). akte develop-runtime-red/round-2.md auf origin/main @ 91e79c2a. reinlichkeit gemeldet: keine baseharbor-eigenen container/volumes/netzwerke auf ihrer zelle. inhalt: postgres faellt per gosu auf uid70 zurueck, der pruef-code las ein leeres Config.User - behoben am test-seitigen eingang (AllowRootEntrypoint + /proc-Kapazitaetspruefung) in runtime_multi_integration_test.go. DIESE KARTE IST DER SCHLUESSEL fuer 0428-083 (#1684 blockiert auf derselben stoerung) und fuer die smoke-pfade aller folgenden karten

MERGE FERN BESTAETIGT: gh api pulls/1711 -> state=closed merged=true merge_commit=dbe7fbc3905b, closed 09:50:01Z; develop-spitze dbe7fbc3905b. der merge stammt vom OWNER. KLARSTELLUNG ZU IHRE MELDUNG: sie schreiben, der zweite commit ccb630681 habe den head NACH dem merge bewegt; gemessen traegt ccb630681 die zeit 10:39:07+01:00 und der merge-commit dbe7fbc39 die zeit 10:50:00+01:00, also liegt der zweite commit VOR dem merge. ihr kern stimmt trotzdem: der head bewegte sich nach ihrer ersten einfrier-meldung (0a3805fb) und ein zweiter stand war noetig, den sie selbst abgefangen haben. ihr run 44712547340 am exakten head ccb630681 = success, docker-lifecycle-zelle laeuft (nicht skipped), zelle clean, akte develop-runtime-red/round-3.md auf main @ 48ec31fe. FOLGE: die develop-smoke-stoerung (tmpfs an /etc/perses/database auf read-only root, praedenzlauf 44661597243) ist behoben; karte 0428-083 (#1684) ist wieder arbeitbar und auf ihren frei gewordenen sitz gelegt (lane 473e54be, ornith)

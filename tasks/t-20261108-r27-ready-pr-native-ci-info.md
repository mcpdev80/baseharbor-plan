---
id: t-20261108-r27-ready-pr-native-ci-info
card_number: "0427-137"
card_short_title: "Ready-PR Native CI"
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ci-owner
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: "0427-137 · Ready-PR Native CI"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1463]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1463", "https://github.com/mcpdev80/baseharbor/actions/runs/42466245067"]
---

- [ ] t-20261108-r27-ready-pr-native-ci-info · Ready-PR Native CI #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** ci-owner · **Priority:** high  
    **PR:** [baseharbor#1463](https://github.com/mcpdev80/baseharbor/pull/1463)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1463), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42466245067)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** ci-owner  
**Priority:** high  
**PRs:** [baseharbor#1463](https://github.com/mcpdev80/baseharbor/pull/1463)  
**Source:** 
<!-- /generated:links -->

## Information for Codeman coordinator and workers (Owner decision, 2026-11-08)

**CI OWNER SCOPE: DO NOT IMPLEMENT OR DUPLICATE THIS CI WORK.** This is an informational handoff, not an instruction to allocate another worker.

The Owner is changing PR runtime qualification in `mcpdev80/baseharbor`:

- Branch without PR: no PR checks.
- Draft PR: no costly mandatory PR runtime tests.
- Transition Draft -> Ready for review (`ready_for_review`): select impacted checks and execute on the exact PR integration candidate.
- Further push on ready PR (`synchronize`) and reopen while non-draft: repeat impacted checks.
- Unknown mapping: conservative broader selection rather than a false green.
- Missing/skip/fail required acceptance is not PASS, independent of basic unit/build green.
- Tests run **only on GitHub-hosted runners**: `ubuntu-latest` (Docker), `ubuntu-26.04` (rootless Podman). **No manual tests on real hardware, no self-hosted VM runner, no requests for physical Docker/Podman machines**.
- Cross-repository Demo/Console/Connector evidence stays develop/release-owned; this PR gate covers relevant local native Core tests.

## #1453 coordination

- Earlier request for real hardware/manual VM tests was withdrawn in the Owner's comment on [PR #1453](https://github.com/mcpdev80/baseharbor/pull/1453).
- Codeman's assigned lane retains ownership of #1453 product code. Do not take over its branch, reassign it or require hardware testing.
- When ready, switch PR to Ready for review and let GitHub Actions run the exact-SHA native acceptance. Merge only after applicable hosted checks pass.
- CI Owner owns `.github/**`, selector and CI-policy updates; Codeman must not independently modify them.

## Acceptance

- Draft PR does not start native acceptance; ready-for-review starts it; new commits to ready PR rerun it.
- Relevant destroy source paths select `scripts/ci-native-installation-destroy.sh` on hosted Docker and Podman; exact `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` must PASS, never SKIP.
- Unrelated changes do not trigger expensive native acceptance; missing mapping falls back to a conservative native selection.
- CI Owner PR: [baseharbor#1463](https://github.com/mcpdev80/baseharbor/pull/1463), MERGED as `88acebc5cc725ab69af5abe89588987c2001af6c`; [PR CI green](https://github.com/mcpdev80/baseharbor/actions/runs/42466245067). #1453 was merged by its owner as d30de3a4. Independent hosted verification PR [#1464](https://github.com/mcpdev80/baseharbor/pull/1464) selected Docker and Podman, reproducing the missing installation-owner regression (run 42466868568). A true Core-bootstrap fixture fix is now under validation in run 42467115964; do not mark native acceptance PASS until both runtime cells succeed.


## Audit 2026-11-08 — CI-Merge und Folgeverifikation

- PR [#1463](https://github.com/mcpdev80/baseharbor/pull/1463) ist in `develop` gemergt: `88acebc5cc725ab69af5abe89588987c2001af6c`.
- Die anschliessende Regression/Verifikation [#1464](https://github.com/mcpdev80/baseharbor/pull/1464) wurde ebenfalls gemergt: `cd494610` (laut dokumentierter Owner-Mergeabnahme). Native Destroy-Retry Docker und Podman, Go-Unit, Build/Vet und PR-Auswahl waren dabei PASS.
- Der vorherige Satz 'do not mark native acceptance PASS' beschreibt den damaligen Zwischenstand vor #1464 und ist **historisch**, nicht mehr aktueller CI-Blocker. CI-Implementierung gemergt; offener Kartenstatus wird erst nach erneuter kanonischer Release-/Abnahmepruefung samt `plan.py render && check` geschlossen. Kein neuer Workerauftrag.


## Source-Check — 2026-11-08 (`develop` b73a13a9)

- `.github/workflows/ci.yml` hat `pull_request` Trigger `opened`, `synchronize`, `reopened`, `ready_for_review`, `converted_to_draft` und laesst teure PR-Jobs nur fuer `draft == false` laufen. Es gibt keinen normalen `push`-Trigger auf beliebige Entwicklerbranches.
- `pr_native_impact` waehlt betroffene Pfade per `scripts/ci-single-default-impact.sh` und faellt bei nicht klassifizierter `cmd/baha/*.go`-Aenderung konservativ auf Native zurueck. `pr_native_destroy` laeuft in der Docker-/Podman-Matrix auf `ubuntu-latest`/`ubuntu-26.04`, checkout `github.sha`, verifiziert exakt den SHA und benutzt `scripts/ci-native-installation-destroy.sh`.
- Das Shell-Skript fordert den wirklichen Test `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` mit `BASEHARBOR_INSTALLATION_DESTROY_ACCEPTANCE=1` an und verweigert fehlendes PASS, SKIP und FAIL im JSON-Ergebnis. Codevertrag der Karte ist damit implementiert. Dies ist ein **Code-Review des Trigger-/Guard-Pfads**, kein neuer Testlauf. Formale Karten-Schliessung mit kanonischem Renderer offen; bitte keine neue Implementierungslane beauftragen.

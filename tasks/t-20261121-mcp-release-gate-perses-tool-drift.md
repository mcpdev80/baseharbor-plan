---
id: t-20261121-mcp-release-gate-perses-tool-drift
card_number: "0428-225"
card_short_title: "MCP release gate rejects the"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: Codex owner (authenticated base hop)
kanban_status: wait
kanban_lane: wait
kanban_summary: The Pre-Release workflow reports unexpected MCP tools baseharbor.app.perses.disable/enable/remove/status while…
kanban_title: 0428-225 · MCP release gate rejects the
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1751]
sources: []
blocker: ""
wait_reason: "HOP IST ERLEDIGT, VOM OWNER SELBST (03:3xZ gemeldet, von mir an den refs gegengeprueft, sobald sie da sind): additiver merge-commit 89253bd23d6a4c5f9006d624c3d78910c2eea68b, parents = bdc7c1a9e6e6b1de29afb916d28712eba95dff56 (alter PR-head) + 7d4351c6d645353b6b96c8d320b4c832d55f9047 (develop), kein konflikt, diff gegen develop bleibt exakt cmd/baha/agent_mcp_test.go +25, feature-commit erhalten. WARTEGRUND: der fast-forward-push auf den PR-branch und der terminale gruene exakte hosted run auf 89253bd23d6; danach unabhaengiges exact-head verdict, dann ordinary merge. DIE LANE 03c7350a hat keinen auftrag mehr an diesem PR (mission 1d00fc03f12e zurueckgenommen, stand-down sha256 im ledger), weil ein zweiter hop auf demselben PR mit der arbeit des owners kollidieren wuerde; sie liefert nur noch die zwei zeulen zustand/rettungsversuch fuer ihre beiden nicht abgelieferten missionen ab (tooling #35)."
resolution: ""
evidence: []
---

- [ ] t-20261121-mcp-release-gate-perses-tool-drift · MCP release gate rejects the app.perses.* tools the machine contract declares #task #release/v0-4-28 #status/wait #view/wait #kind/task
    <!-- generated:card -->
    **Owner:** Codex owner (authenticated base hop)  
    **PR:** [baseharbor#1751](https://github.com/mcpdev80/baseharbor/pull/1751)  
    **Waiting:** HOP IST ERLEDIGT, VOM OWNER SELBST (03:3xZ gemeldet, von mir an den refs gegengeprueft, sobald sie da sind): additiver merge-commit 89253bd23d6a4c5f9006d624c3d78910c2eea68b, parents = bdc7c1a9e6e6b1de29afb916d28712eba95dff56 (alter PR-head…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Codex owner (authenticated base hop)  
**Priority:** not set  
**PRs:** [baseharbor#1751](https://github.com/mcpdev80/baseharbor/pull/1751)  
**Source:** 
<!-- /generated:links -->

## Goal

The Pre-Release workflow reports unexpected MCP tools `baseharbor.app.perses.disable/enable/remove/status` while `internal/machine/contract.go:205-208` declares exactly those four tools as part of the machine contract. One of the two is stale; the release-suite proof for v0.4.28 is blocked by the drift.


## Problem

Measured by the coordinator on 2026-11-21 at PR #1746 head `e362a71bb6f` (card 0428-208, status `review`):

  - run `44909057730` = workflow `CI · PR #1746`, `event=pull_request` -> **completed/success**.
  - run `44909067224` = workflow `Release · Pre-Release Validation`, `event=workflow_dispatch`, same head ->
    **completed/failure**; failing jobs `Static · init` (`136863713964`), `Static · shell-ux` (`136863714025`),
    `Static · config-matrix` (`136863714030`), `Static · mcp` (`136863714083`), `Pre-Release Checks` (`136864161584`).
  - in both static jobs inspected, the failing step is the gate itself, not setup: `gh api
    repos/mcpdev80/baseharbor/actions/jobs/<id>` names step **18 `Run static gate`**. Hosted per-job logs returned **0 bytes**
    via `gh run view --job <id> --log-failed`; annotations only say `Process completed with exit code 1`.

**Root cause: v0.4.28 is not registered in the release catalog.** On develop `e6c199e7b7dd`:

  - `scripts/release-requirements.json` -> `releases: ["v0.4.22","v0.4.23","v0.4.24","v0.4.25","v0.4.26","v0.4.27"]` and
    `grep -c 'v0\.4\.28'` on that file returns **0 hits**: no release entry and no gate `required_for` list mentions this
    release (checked for `atomic/static/mcp`: `required_for: [v0.4.22..v0.4.27]`, 65 gates total).
  - `scripts/pre-release-check-plan.py:21` fails closed on exactly that: `if tag not in inventory.get('releases', []): raise
    ValueError('release is absent from the candidate check catalog')`.
  - `docs/releases/v0.4.28.selected-gates.json` and `docs/releases/v0.4.28.demo-ref` **do not exist**, while v0.4.23-v0.4.26
    each ship a `selected-gates.json` and v0.4.17-v0.4.23 plus v0.4.27 ship a `demo-ref`. The missing `demo-ref` is the same
    file that blocks card 0428-205 (consumer `.github/workflows/pre-release.yml:175`).

**What the intake triage claimed and what the file shows.** The attribution "the `atomic/static/<gate>` ids are absent from
`scripts/release-requirements.json`" is **refuted**: `atomic/static/init`, `atomic/static/shell-ux`,
`atomic/static/config-matrix` and `atomic/static/mcp` all exist in the `gates` list. What survives is one genuine drift:
`Static · mcp` reports `baseharbor.app.perses.disable/enable/remove/status` as unexpected, although `internal/machine/
contract.go:205-208` declares all four and `contracts/machine/v1/control.golden.json` lists them. The contract moved on
2026-11-19 through commit `1019190d8` (card 0428-084, PR #1598, "Perses lifecycle commands"); the gate's expected surface was
never aligned. `Static · config-matrix` additionally hits managed-environment operator authentication
(`Managed-environment machine operations require an authenticated BaseHarbor operator`, `internal/operatorauth/
authorization.go:285`) in a non-interactive setup - the same field-wide gate as card 0428-198.

Adjacent, from the same triage thread: PR #1736 maps `TestEnvironmentDestroyNativeLifecycle` in `scripts/pr-gate-coverage.json:1454`
and `scripts/test_pr_gate_coverage.py:201`, but `scripts/pre-release-integration.py:17` (`CHECKS`) carries no entry for it, so the
destroy route has PR-gate coverage without release-suite selection. The write-set request for those two `scripts/**` files is
escalated to the Owner in the coordination ledger (row 940); this card does not implement `scripts/**`.

## Scope

  - In scope: the MCP tool surface the release gate expects versus `internal/machine/contract.go` (`app.perses.status`,
    `app.perses.enable`, `app.perses.disable`, `app.perses.remove`) and the contract golden
    `contracts/machine/v1/control.golden.json`; and naming, per failing static job, which step and which assertion failed.
  - Out of scope: `scripts/release-requirements.json`, `scripts/pre-release-integration.py`, `docs/releases/**` and any
    `.github/**` file - all Owner scope. Registration of v0.4.28 in the release catalog is reported here with file:line, it is
    not a lane task, and no lane may self-set its own proof entrance (AGENTS 3.8).

## Acceptance

  - A `workflow_dispatch` run of `Release · Pre-Release Validation` at an exact develop head shows `Static · mcp` green, with
    the running server's tool list compared line by line to `internal/machine/contract.go` in the evidence.
  - The drift is resolved in the direction the contract proves, not by deleting the expectation: if the contract is right, the
    gate fixture is corrected (Owner scope, named here with file:line); if the server does not expose the tools, contract and
    golden change in the same PR, and removing four declared tools is flagged as a breaking machine-surface change for the Owner
    to accept.
  - `Static · init`, `Static · shell-ux` and `Static · config-matrix` each carry one named cause in the evidence (step name plus
    annotation), or the explicit statement that the hosted log endpoint returned 0 bytes, with the command that was used.
  - No card in this window may be closed on the strength of an ordinary PR run alone: `CI · PR #<n>` success is not release-suite
    proof (measured pair `44909057730` success vs `44909067224` failure at the same head `e362a71bb6f`).
  - Blocked until the Owner registers v0.4.28: `scripts/release-requirements.json` (`releases` + `required_for`),
    `docs/releases/v0.4.28.selected-gates.json`, `docs/releases/v0.4.28.demo-ref`.



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

  - Owned files or areas: none by this card while the catalog registration is missing.
  - Blocked by: Owner registration of `v0.4.28` in the release catalog (Owner scope).
  - Shared files: coordinate through the owning task.




- Current state, branch, PR and evidence links. Newest first.

planned -> active: hosted proof from PR #1746 static gate (job 136970241277): 'MCP contract mismatch: missing=[] unexpected=[baseharbor.app.perses.disable,.enable,.remove,.status]'. Fresh laptop lane dispatched (mission coordinator/missions/0428-225-mcp-contract-drift.md). Scope per card: internal/machine/contract.go + contracts/machine/v1/control.golden.json; scripts/**, docs/releases/**, .github/** stay Owner scope.

KORREKTUR NACH OWNER-AUFKLARUNG 00:5xZ, mein vorheriger wait-grund war teilweise FALSCH: der fehlgeschlagene run 44952645994 war ein MISPARAMETERIZETER 'Release Pre-Release Validation'-workflow_dispatch (tag/ref/demo_ref nicht gesetzt), NICHT ein fehlender refs/heads/release/v0.4.28. der gehoffte 'Static · mcp'-cell war deshalb nur skipped. Die eigentliche PR-CI 44951681560 ist completed/success auf head bdc7c1a9e6e (35 jobs, 14 success / 21 skipped, 0 failed); der trusted plan verlangt cli-build/gofmt/go test ./cmd/baha/vet/source-contracts, selected_gates ist leer, weil dieser PR nur cmd/baha/agent_mcp_test.go aendert - alle required checks sind gruen. OFFEN ist damit nur noch: der PR-base ist 1080986, develop ist 513488eeb6d (back=7) -> hop auf den aktuellen develop, dann exakter PR-CI-run, dann review. Keine lokalen tests als ersatz (owner-anweisung).

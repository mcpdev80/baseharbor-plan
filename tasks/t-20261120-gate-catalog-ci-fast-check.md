---
id: t-20261120-gate-catalog-ci-fast-check
card_number: "0428-205"
card_short_title: "Gate catalog for ci-fast-check"
type: bug
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: "Codex (Owner-directed, 2026-11-21)"
kanban_status: blocked
kanban_lane: blocked
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-205 · Gate catalog for ci-fast-check
priority: normal
depends_on: [t-20261120-r28-cli-shard-operator-env]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: "Owner decision needed on corrected scope after Option A (2026-11-21): exact current #1665 base/head b71c6da27e8b/db27880c108a passes both Workflow policy and Gate catalog consistency; hosted Workflow policy job 136733496977 passed on run 44867225115 (overall run cancelled; PR Selected Checks failed separately on native gates). The old failure no longer reproduces because scripts/ci-fast-check.sh is already present in the compared base. To add atomic/static/ci-fast-check as an actual pre-release gate, the dispatcher is .github/workflows/pre-release-runtime-suite.yml:264-270; .github/workflows/ci.yml:1301 dispatches ci-policy and is not that gate. This required workflow line is outside 0428-208 current write-set/stop boundary. Choose: authorize updating 0428-208 scope for the actual pre-release dispatcher and keep the full registration, or drop the no-longer-needed gate registration and close this finding. Candidate fab709a45 remains local/unpublished and is incomplete (catalog entry only)."
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44867225115", "https://github.com/mcpdev80/baseharbor/pull/1665"]
---

- [ ] t-20261120-gate-catalog-ci-fast-check · 0428-205 · Wire scripts/ci-fast-check.sh into the gate catalog #task #release/v0-4-28 #status/blocked #view/blocked #area/ci #kind/bug
    <!-- generated:card -->
    **Owner:** Codex (Owner-directed, 2026-11-21) · **Priority:** normal  
    **Blocker:** Owner decision needed on corrected scope after Option A (2026-11-21): exact current \#1665 base/head b71c6da27e8b/db27880c108a passes both Workflow policy and Gate catalog consistency; hosted Workflow policy job 136733496977 passed on run 4…  
    **Needs:** [t-20261120-r28-cli-shard-operator-env](t-20261120-r28-cli-shard-operator-env.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44867225115), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1665)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-r28-cli-shard-operator-env](t-20261120-r28-cli-shard-operator-env.md)  
**Required by:** [t-20261121-static-gate-registration](t-20261121-static-gate-registration.md)  
**Owner:** Codex (Owner-directed, 2026-11-21)  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

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

## Why

Round-2 of `evidence/r28-welle4-2026-11-20/aggregate-vs-base/round-1.md` (sitz w215) measured: `Workflow policy` is SUCCESS at
PR #1731 head `f90b3f44` (job 136551503837, "Workflow policy PASS: 20 approved workflow files." + "Gate catalog consistency
PASS"), while PR #1665 shows the same cell as FAILURE. The enforcing rule is `scripts/ci-workflow-policy.sh:34-40` (workflow
file inventory + gate catalog), invoked from `.github/workflows/ci.yml:31-32`. The coordinator verified on develop
`40cb28c758b0`: `scripts/ci-fast-check.sh` exists there, and the string `ci-fast-check` appears only in
`scripts/pr-candidate-advisory.py`, NOT in `release-requirements.json`. So the new check surface is not wired into the
catalog that the policy gate compares against.

## What

Add the missing catalog pairing for `scripts/ci-fast-check.sh` in `release-requirements.json` (or wire it into the existing
PR selection surface the policy script reads), so a PR whose base comparison sees the new file does not fail
`Workflow policy`. No workflow file may be added or removed; the policy script itself stays untouched.

## Acceptance

- `scripts/ci-workflow-policy.sh` run locally at the exact head prints "Workflow policy PASS" and "Gate catalog consistency
  PASS" with the same two strings the hosted job uses.
- The failing cell on a stacked/older-base PR (evidence: PR #1665) is explained by this pairing alone, verified by re-running
  the policy script on that head in a scratch worktree - not by any `.github/**` change.
- One PR, base develop, non-draft from the start; hosted `Workflow policy` + `PR Selected Checks` observed at the exact head.

Karte aus w215s round-2-befund gegossen (fund->karte, §3.3.5): scripts/ci-fast-check.sh existiert auf develop, hat aber keine release-requirements.json-paarung, darumfaellt die zelle "Workflow policy" an PRs, deren base-vergleich die neue datei sieht (#1665 gemessen FAILURE, #1731 gemessen SUCCESS job 136551503837). sitz w220 (flash) ergaenzt NUR die paarung, beweis lokal ueber bash scripts/ci-workflow-policy.sh am exakten head + gegenprobe am #1665-head. allowlist-edit an scripts/ci-workflow-policy.sh oder .github/** = STOP + MELDEN (owner-scope).

LANE-BEFUND KORRIGIERT MEINE KARTEN-SCHNEIDE (akte gate-catalog-ci-fast-check/round-1.md, plan-main 93bf3211): der #1665-fallerklaert sich NICHT allein durch die release-requirements.json-paarung - 'scripts/ci-workflow-policy.sh:178-195'verlangt, dass eine neue check-datei im selben wechsel beide 'scripts/pr-gate-plan.py' UND 'scripts/release-requirements.json'aendert. sitz w220 hat local einen kandidaten (branch lane-0428-205-gate-catalog-pairing, head 5e3fa3221b92, diff = nurrelease-requirements.json) und hat RICHTIGERWEISE gehalten statt still zu erweitern (4.2). ICH ERWEITERE DAS SCHREIB-UMFANG AUSDRUECKLICH AUF BEIDE DATEIEN (policy-skript und .github/** bleiben gesperrt) und verlange den beweis ueber'bash scripts/ci-workflow-policy.sh' am exakten head (beide PASS-zeilen), gegenprobe im scratch-worktree am #1665-headdb27880c108a. wenn das immer noch scheitert: STOP + MELDEN, dann ist es ein .github-inventar-thema bei ihnen. KARTE BLEIBTactive; kein zustand gewechselt, weil der kandidaten noch nicht veroeffentlicht ist.

## Owner decision and implementation preflight — 2026-11-21

Owner chose Option A: one combined PR for gate registration plus the Owner-scope dispatch. Codex was assigned to take the card through merge.

The preflight corrected the original diagnosis. On the exact current PR #1665 pair (base `b71c6da27e8bbf180d26762eb9bfb101ec5a7bbe`, head `db27880c108a84c6c11bcb5a02484d3da00244bd`), a detached worktree run of `BASEHARBOR_POLICY_BASE_SHA=<base> BASEHARBOR_POLICY_HEAD_SHA=<head> bash scripts/ci-workflow-policy.sh` prints `Workflow policy PASS: 20 approved workflow files.` and `Gate catalog consistency PASS: no check-file or gate-ID additions/removals.` The script `scripts/ci-fast-check.sh` exists on both sides, so it is not a newly added check in this comparison. Hosted Workflow policy job 136733496977 also passed on run 44867225115; that overall workflow was cancelled and `PR Selected Checks` failed on separate native gates, so this is not a full CI pass.

The planned `ci.yml:1301` arm is the `ci-policy` validation dispatch. The actual static release-gate switch is in `.github/workflows/pre-release-runtime-suite.yml:264-270`. A real static-gate registration requires that additional workflow path, which 0428-208 currently forbids. The existing local candidate fab709a45 only adds a catalog row with `required_for: []`; it is not executable or ready to publish. No product PR was opened and no product source was changed.

STOP pending Owner direction: authorize the corrected `.github/workflows/pre-release-runtime-suite.yml` dispatch and update 0428-208 scope, or drop the now-unneeded gate registration and close this finding based on the exact current #1665 comparison.

END_BLOCKED accepted: the card was cut too narrow BY MY HAND and the lane is correct. Measured consequence: this card cannot produce a green candidate without an Owner-scope line, so it goes to blocked (not wait) because it needs an Owner decision, which is the blocked semantics. 0428-208 is poured for the develop-side registration part and stays planned until the decision is recorded.
